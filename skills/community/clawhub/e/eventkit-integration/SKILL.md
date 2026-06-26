---
name: eventkit-integration
description: EventKit integration patterns, permission handling, zero-width character steganography, and batch operations for macOS/iOS apps
domain: ios-macos
homepage: https://github.com/soponcd/timeflow-skills/tree/main/teams/skills/eventkit-integration
metadata:
  clawdbot:
    emoji: 📅
---

# EventKit Integration

Expert-level EventKit patterns for macOS/iOS applications. Specialized for reminder systems, permission handling, and bidirectional sync.

## When to Use

Use this skill when:
- Integrating EventKit Reminders or Events
- Handling EventKit permissions and authorization
- Implementing bidirectional sync with external data
- Using zero-width character steganography for identity tracking
- Batch EventKit operations
- Building zombie task self-healing logic

---

## Core Principles

### 1. Actor-Based Service

```swift
import EventKit
import Foundation

actor EventKitService {
    private let eventStore = EKEventStore()
    private var timeFlowCalendar: EKCalendar?

    func initialize() async throws {
        let remindersGranted = try await eventStore.requestFullAccessToReminders()
        let eventsGranted = try await eventStore.requestFullAccessToEvents()

        guard remindersGranted && eventsGranted else {
            throw EventKitError.permissionDenied
        }

        timeFlowCalendar = try await getOrCreateTimeFlowCalendar()
    }
}
```

### 2. Calendar Management

```swift
private func getOrCreateTimeFlowCalendar() async throws -> EKCalendar {
    let calendars = eventStore.calendars(for: .reminder)

    if let existing = calendars.first(where: { $0.title == "TimeFlow" }) {
        return existing
    }

    let calendar = EKCalendar(for: .reminder, eventStore: eventStore)
    calendar.title = "TimeFlow"
    calendar.source = eventStore.defaultCalendarForNewReminders()?.source

    try eventStore.saveCalendar(calendar, commit: true)
    return calendar
}
```

### 3. Batch Fetch Pattern

```swift
func fetchAllReminders() async throws -> [ReminderSnapshot] {
    guard let calendar = timeFlowCalendar else {
        throw EventKitError.calendarNotFound
    }

    let incompletePredicate = eventStore.predicateForIncompleteReminders(
        withDueDateStarting: nil, ending: nil, calendars: [calendar]
    )

    return try await withCheckedThrowingContinuation { continuation in
        eventStore.fetchReminders(matching: incompletePredicate) { reminders in
            if let reminders = reminders {
                let snapshots = reminders.map { $0.toSnapshot() }
                continuation.resume(returning: snapshots)
            } else {
                continuation.resume(returning: [])
            }
        }
    }
}
```

---

## Permission Handling

### Authorization Flow

```swift
enum EventKitError: Error, LocalizedError {
    case permissionDenied
    case calendarNotFound

    var errorDescription: String? {
        switch self {
        case .permissionDenied:
            return "需要访问提醒事项的权限"
        case .calendarNotFound:
            return "找不到 TimeFlow 日历"
        }
    }
}
```

### Check Before Operations

```swift
func updateReminder(_ reminder: EKReminder) async throws {
    // Verify calendar exists before operation
    guard timeFlowCalendar != nil else {
        throw EventKitError.calendarNotFound
    }

    try eventStore.save(reminder, commit: true)
}
```

---

## Sync Patterns

### Zero-Width Character Steganography

Embed identity signatures invisibly in EventKit notes:

```swift
func buildNotes(from task: IdentityMap) -> String {
    let baseNotes = task.notesSnapshot ?? ""

    // Embed zero-width signature for identity tracking
    let signature = "\u{200B}TIMEFLOW:\(task.localUUID)\u{200C}"

    return baseNotes.isEmpty ? signature : baseNotes + "\n" + signature
}

func extractSignature(from notes: String?) -> String? {
    guard let notes = notes else { return nil }

    let pattern = #"\u{200B}TIMEFLOW:([^\u{200B}]+)\u{200C}"#
    guard let regex = try? NSRegularExpression(pattern: pattern),
          let match = regex.firstMatch(in: notes, range: NSRange(notes.startRange, in: notes)) else {
        return nil
    }

    guard let range = Range(match.range(at: 1), in: notes) else { return nil }
    return String(notes[range])
}
```

### Critical: Prevent Sync Loops

When creating new IdentityMap from EventKit, bind immediately:

```swift
private func findOrCreateIdentityMap(for reminder: ReminderSnapshot) -> IdentityMap? {
    if let existing = swiftDataService.findIdentityMap(by: reminder.id) {
        return existing
    }

    let newMap = swiftDataService.createIdentityMap(
        title: reminder.title,
        projectName: nil,
        contextTags: []
    )

    // CRITICAL: Bind immediately and mark as clean
    // This prevents: New Map -> Dirty -> Push -> Duplicate infinite loop
    newMap.ekIdentifier = reminder.id
    newMap.lastSyncDate = Date()
    newMap.isDirty = false

    return newMap
}
```

---

## Batch Operations

### Batch Delete with Chunking

```swift
func deleteReminders(identifiers: [String]) async throws -> Int {
    var deletedCount = 0
    let batchSize = 500

    for id in identifiers {
        if let reminder = eventStore.calendarItem(withIdentifier: id) as? EKReminder {
            try eventStore.remove(reminder, commit: false)
            deletedCount += 1
        }

        // Commit in batches for performance
        if deletedCount % batchSize == 0 {
            try eventStore.commit()
        }
    }

    // Final commit
    try eventStore.commit()
    return deletedCount
}
```

---

## Zombie Task Self-Healing

### Grace Period Pattern

Don't delete immediately created tasks:

```swift
nonisolated func purgeZombieTasksBackground() {
    let context = ModelContext(container)
    context.autosaveEnabled = false

    // Grace period: 1 hour
    // Newly created tasks have nil ekID, but aren't zombies
    let oneHourAgo = Date().addingTimeInterval(-3600)

    let descriptor = FetchDescriptor<IdentityMap>(
        predicate: #Predicate { $0.ekIdentifier == nil && $0.createdAt < oneHourAgo }
    )

    let zombies = (try? context.fetch(descriptor)) ?? []
    guard !zombies.isEmpty else { return }

    // Group by title to identify duplicates
    let grouped = Dictionary(grouping: zombies, by: { $0.titleSnapshot })

    for (title, tasks) in grouped where tasks.count > 1 {
        // Keep oldest, delete duplicates
        let sorted = tasks.sorted { $0.createdAt < $1.createdAt }
        for task in sorted.dropFirst() {
            context.delete(task)
        }
    }

    try? context.save()
}
```

---

## Testing Patterns

### Mock EventKit for Tests

```swift
@MainActor
final class EventKitServiceTests: XCTestCase {
    var mockService: MockEventKitService!

    override func setUp() async throws {
        try await super.setUp()
        mockService = MockEventKitService()
    }

    func testFetchAllReminders() async throws {
        // Given: Mock reminders
        mockService.addReminder(id: "EK-1", title: "Task 1")
        mockService.addReminder(id: "EK-2", title: "Task 2")

        // When: Fetch
        let reminders = try await mockService.fetchAllReminders()

        // Then: Verify
        XCTAssertEqual(reminders.count, 2)
    }
}
```

---

## Best Practices

| Practice | Reason |
|----------|---------|
| Use `actor` for EventKitService | Thread-safe access to EKEventStore |
| Check permissions before operations | Prevents silent failures |
| Batch operations with commit | Improves performance |
| Bind ekID immediately on create | Prevents sync loops |
| Use grace period for zombie purge | Allows sync time for new tasks |
| Extract zero-width signatures carefully | Identity recovery across ID changes |

---

## Common Pitfalls

| Pitfall | Consequence | Prevention |
|---------|-------------|------------|
| Sync loop (infinite duplicates) | Database bloat + sync chaos | Bind `ekIdentifier` immediately on create |
| Missing permission checks | Silent failures | Check authorization before each operation |
| Deleting too eagerly | Lost tasks on slow sync | Use 1-hour grace period |
| N+1 EventKit queries | Slow sync performance | Batch fetch, then process in-memory |
| Committing on each delete | Slow performance | Chunk and batch commits |

---

## Running EventKit Tests

```bash
# Test EventKit integration
xcodebuild test -scheme YourApp \
  -destination 'platform=macOS' \
  -only-testing:'YourAppTests/EventKitTests/testFetchAllReminders'
```
