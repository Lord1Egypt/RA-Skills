import UserNotifications

@MainActor
final class NotificationManager: NSObject, ObservableObject {
    @Published var isAuthorized = false

    private var lastFiredPlaceID: String?
    private var lastFiredAt: Date?

    override init() {
        super.init()
        UNUserNotificationCenter.current().delegate = self
    }

    func requestPermission() async {
        do {
            let granted = try await UNUserNotificationCenter.current()
                .requestAuthorization(options: [.alert, .sound, .badge])
            isAuthorized = granted
        } catch {
            isAuthorized = false
        }
    }

    /// Fires a local notification for the best card at the current place.
    /// Respects Config.notificationCooldown to avoid repeated fires.
    func notify(recommendation rec: CardRecommendation) {
        let now = Date()
        if let lastID = lastFiredPlaceID,
           lastID == rec.place.id,
           let lastTime = lastFiredAt,
           now.timeIntervalSince(lastTime) < Config.notificationCooldown {
            return
        }

        lastFiredPlaceID = rec.place.id
        lastFiredAt = now

        let content = UNMutableNotificationContent()
        content.title = "\(rec.category.emoji) \(rec.place.name)"
        content.body  = buildBody(rec)
        content.sound = .default
        content.userInfo = ["placeId": rec.place.id, "cardName": rec.card.name]

        // Category for actionable notification
        content.categoryIdentifier = "CARD_RECOMMENDATION"

        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 0.5, repeats: false)
        let request = UNNotificationRequest(
            identifier: "fleece-\(rec.place.id)",
            content: content,
            trigger: trigger
        )
        UNUserNotificationCenter.current().add(request)
    }

    private func buildBody(_ rec: CardRecommendation) -> String {
        let rate = String(format: "%.1f%%", rec.effectiveRate)
        let programShort = rec.card.pointsProgram.replacingOccurrences(of: "Cash Back", with: "cash back")
        let multiplierStr = rec.multiplier == rec.multiplier.rounded()
            ? "\(Int(rec.multiplier))x"
            : String(format: "%.1fx", rec.multiplier)
        return "Use \(rec.card.name) · \(multiplierStr) \(rec.category.rawValue) = \(rate) back (\(programShort))"
    }

    func registerActionCategory() {
        let viewAction = UNNotificationAction(
            identifier: "VIEW_RECS",
            title: "View All Cards",
            options: [.foreground]
        )
        let category = UNNotificationCategory(
            identifier: "CARD_RECOMMENDATION",
            actions: [viewAction],
            intentIdentifiers: [],
            options: []
        )
        UNUserNotificationCenter.current().setNotificationCategories([category])
    }
}

extension NotificationManager: UNUserNotificationCenterDelegate {
    nonisolated func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification
    ) async -> UNNotificationPresentationOptions {
        // Show banner even when app is in foreground
        return [.banner, .sound]
    }
}
