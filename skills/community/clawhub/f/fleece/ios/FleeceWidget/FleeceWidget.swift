import WidgetKit
import SwiftUI

// MARK: - Provider

struct FleeceTimelineProvider: TimelineProvider {
    func placeholder(in context: Context) -> FleeceWidgetEntry {
        .placeholder
    }

    func getSnapshot(in context: Context, completion: @escaping (FleeceWidgetEntry) -> Void) {
        completion(entry(from: FleeceWidgetData.load()))
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<FleeceWidgetEntry>) -> Void) {
        let e = entry(from: FleeceWidgetData.load())
        // Main app calls WidgetCenter.reloadAllTimelines() on each location update;
        // this 30-min policy is just a safety fallback.
        let next = Calendar.current.date(byAdding: .minute, value: 30, to: .now)!
        completion(Timeline(entries: [e], policy: .after(next)))
    }

    private func entry(from data: FleeceWidgetData?) -> FleeceWidgetEntry {
        guard let data else { return .empty }
        return FleeceWidgetEntry(
            date: .now,
            cardName: data.cardName,
            cardColor: Color(hex: data.cardColor) ?? .blue,
            textColor: Color(hex: data.textColor) ?? .white,
            multiplier: data.multiplier,
            categoryEmoji: data.categoryEmoji,
            categoryName: data.categoryName,
            placeName: data.placeName,
            rewardRate: data.rewardRate
        )
    }
}

// MARK: - Entry

struct FleeceWidgetEntry: TimelineEntry {
    let date: Date
    let cardName: String
    let cardColor: Color
    let textColor: Color
    let multiplier: Double
    let categoryEmoji: String
    let categoryName: String
    let placeName: String?
    let rewardRate: Double

    var multiplierText: String {
        multiplier == multiplier.rounded(.toNearestOrAwayFromZero) && multiplier == Double(Int(multiplier))
            ? "\(Int(multiplier))"
            : String(format: "%.1f", multiplier)
    }

    static let placeholder = FleeceWidgetEntry(
        date: .now,
        cardName: "Gold Card",
        cardColor: Color(hex: "#B8860B") ?? .yellow,
        textColor: .white,
        multiplier: 4,
        categoryEmoji: "🍽️",
        categoryName: "Dining",
        placeName: "Chez Paul",
        rewardRate: 7.2
    )

    static let empty = FleeceWidgetEntry(
        date: .now,
        cardName: "Open Fleece to start",
        cardColor: Color(hex: "#8E8E93") ?? .gray,
        textColor: .white,
        multiplier: 1,
        categoryEmoji: "💳",
        categoryName: "General",
        placeName: nil,
        rewardRate: 1.0
    )
}

// MARK: - Small (systemSmall)

struct FleeceSmallWidgetView: View {
    let entry: FleeceWidgetEntry

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack(alignment: .top) {
                Text(entry.categoryEmoji)
                    .font(.title2)
                Spacer()
                Text("\(entry.multiplierText)×")
                    .font(.title2.weight(.bold))
                    .foregroundStyle(entry.textColor)
            }
            Spacer()
            Text(entry.cardName)
                .font(.headline)
                .foregroundStyle(entry.textColor)
                .lineLimit(2)
                .minimumScaleFactor(0.85)
            Text(entry.categoryName)
                .font(.caption)
                .foregroundStyle(entry.textColor.opacity(0.7))
        }
        .padding(14)
        .widgetURL(URL(string: "fleece://home"))
    }
}

// MARK: - Medium (systemMedium)

struct FleeceMediumWidgetView: View {
    let entry: FleeceWidgetEntry

    var body: some View {
        HStack(spacing: 0) {
            VStack(alignment: .leading, spacing: 6) {
                Text("Best card nearby")
                    .font(.caption2)
                    .foregroundStyle(entry.textColor.opacity(0.6))
                    .textCase(.uppercase)
                    .kerning(0.5)
                Spacer()
                Text(entry.cardName)
                    .font(.title3.weight(.bold))
                    .foregroundStyle(entry.textColor)
                    .lineLimit(2)
                    .minimumScaleFactor(0.85)
                if let place = entry.placeName {
                    Text(place)
                        .font(.caption)
                        .foregroundStyle(entry.textColor.opacity(0.7))
                        .lineLimit(1)
                }
            }
            Spacer(minLength: 8)
            VStack(spacing: 4) {
                Text(entry.categoryEmoji)
                    .font(.largeTitle)
                Text("\(entry.multiplierText)×")
                    .font(.title.weight(.bold))
                    .foregroundStyle(entry.textColor)
                Text(String(format: "%.1f%%", entry.rewardRate))
                    .font(.caption)
                    .foregroundStyle(entry.textColor.opacity(0.7))
            }
            .frame(width: 80)
        }
        .padding(16)
        .widgetURL(URL(string: "fleece://home"))
    }
}

// MARK: - Lock screen rectangular (accessoryRectangular)

struct FleeceRectangularView: View {
    let entry: FleeceWidgetEntry

    var body: some View {
        HStack(spacing: 8) {
            Text(entry.categoryEmoji)
                .font(.title3)
            VStack(alignment: .leading, spacing: 2) {
                Text("Use \(entry.cardName)")
                    .font(.headline)
                    .lineLimit(1)
                Text("\(entry.multiplierText)× \(entry.categoryName)")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}

// MARK: - Lock screen circular (accessoryCircular)

struct FleeceCircularView: View {
    let entry: FleeceWidgetEntry

    var body: some View {
        ZStack {
            AccessoryWidgetBackground()
            VStack(spacing: 1) {
                Text(entry.categoryEmoji)
                    .font(.title3)
                Text("\(entry.multiplierText)×")
                    .font(.caption.weight(.bold))
            }
        }
    }
}

// MARK: - Router

struct FleeceWidgetEntryView: View {
    @Environment(\.widgetFamily) private var family
    let entry: FleeceWidgetEntry

    var body: some View {
        switch family {
        case .systemSmall:
            FleeceSmallWidgetView(entry: entry)
        case .systemMedium:
            FleeceMediumWidgetView(entry: entry)
        case .accessoryRectangular:
            FleeceRectangularView(entry: entry)
        case .accessoryCircular:
            FleeceCircularView(entry: entry)
        default:
            FleeceSmallWidgetView(entry: entry)
        }
    }
}

// MARK: - Widget definition

struct FleeceWidget: Widget {
    let kind = "FleeceWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: FleeceTimelineProvider()) { entry in
            FleeceWidgetEntryView(entry: entry)
                .containerBackground(for: .widget) {
                    entry.cardColor
                }
        }
        .configurationDisplayName("Best Card Nearby")
        .description("Shows your best credit card for the current location.")
        .supportedFamilies([
            .systemSmall,
            .systemMedium,
            .accessoryRectangular,
            .accessoryCircular,
        ])
    }
}

// MARK: - Bundle

@main
struct FleeceWidgetBundle: WidgetBundle {
    var body: some Widget {
        FleeceWidget()
        FeeCalendarWidget()
    }
}

// MARK: - Color hex init (duplicated from CreditCard.swift — widget is a separate target)

private extension Color {
    init?(hex: String) {
        var h = hex.trimmingCharacters(in: .whitespaces).uppercased()
        if h.hasPrefix("#") { h = String(h.dropFirst()) }
        guard h.count == 6, let val = UInt64(h, radix: 16) else { return nil }
        self.init(
            red:   Double((val >> 16) & 0xFF) / 255,
            green: Double((val >> 8)  & 0xFF) / 255,
            blue:  Double( val        & 0xFF) / 255
        )
    }
}

// ===========================================================================
// MARK: - Fee Calendar Widget
// ===========================================================================

// MARK: Provider

struct FeeCalendarTimelineProvider: TimelineProvider {
    func placeholder(in context: Context) -> FeeCalendarEntry {
        .placeholder
    }

    func getSnapshot(in context: Context, completion: @escaping (FeeCalendarEntry) -> Void) {
        completion(entry(from: FeeCalendarWidgetData.load()))
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<FeeCalendarEntry>) -> Void) {
        let e = entry(from: FeeCalendarWidgetData.load())
        // Refresh at midnight so "days away" counts stay accurate
        let midnight = Calendar.current.startOfDay(
            for: Calendar.current.date(byAdding: .day, value: 1, to: .now)!
        )
        completion(Timeline(entries: [e], policy: .after(midnight)))
    }

    private func entry(from data: FeeCalendarWidgetData?) -> FeeCalendarEntry {
        FeeCalendarEntry(date: .now, renewals: data?.renewals ?? [])
    }
}

// MARK: Entry

struct FeeCalendarEntry: TimelineEntry {
    let date: Date
    let renewals: [FeeCalendarWidgetData.RenewalItem]

    static let placeholder = FeeCalendarEntry(date: .now, renewals: [
        .init(cardName: "Sapphire Reserve", cardColor: "#1A1A2E", textColor: "#FFFFFF",
              annualFee: 550, nextRenewalDate: .now.addingTimeInterval(86400 * 23), daysUntil: 23),
        .init(cardName: "Amex Gold",        cardColor: "#B8860B", textColor: "#FFFFFF",
              annualFee: 325, nextRenewalDate: .now.addingTimeInterval(86400 * 71), daysUntil: 71),
    ])
}

// MARK: Small view — next single renewal

struct FeeCalendarSmallView: View {
    let entry: FeeCalendarEntry

    var body: some View {
        if let next = entry.renewals.first {
            VStack(alignment: .leading, spacing: 0) {
                HStack {
                    Text("💳")
                        .font(.title3)
                    Spacer()
                    Text("$\(next.annualFee)")
                        .font(.caption.weight(.semibold))
                        .foregroundStyle(.secondary)
                }
                Spacer()
                Text(next.cardName)
                    .font(.headline)
                    .lineLimit(2)
                    .minimumScaleFactor(0.8)
                Spacer(minLength: 4)
                Text(next.daysUntil == 0 ? "Due today" : "\(next.daysUntil) days")
                    .font(.title2.weight(.bold))
                    .foregroundStyle(feeUrgencyColor(days: next.daysUntil))
                Text("annual fee")
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            }
            .padding(14)
            .widgetURL(URL(string: "fleece://wallet"))
        } else {
            VStack(spacing: 8) {
                Text("💳")
                    .font(.largeTitle)
                Text("No renewal\ndates set")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .multilineTextAlignment(.center)
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .widgetURL(URL(string: "fleece://wallet"))
        }
    }
}

// MARK: Medium view — up to 3 renewals

struct FeeCalendarMediumView: View {
    let entry: FeeCalendarEntry

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            Text("Annual Fee Calendar")
                .font(.caption2.weight(.semibold))
                .foregroundStyle(.secondary)
                .textCase(.uppercase)
                .kerning(0.4)
                .padding(.bottom, 8)

            if entry.renewals.isEmpty {
                Spacer()
                Text("Open Fleece → Wallet to set renewal dates.")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                Spacer()
            } else {
                ForEach(Array(entry.renewals.prefix(3).enumerated()), id: \.offset) { index, item in
                    HStack(spacing: 10) {
                        RoundedRectangle(cornerRadius: 4)
                            .fill(Color(hex: item.cardColor) ?? .gray)
                            .frame(width: 6, height: 32)

                        VStack(alignment: .leading, spacing: 1) {
                            Text(item.cardName)
                                .font(.subheadline.weight(.medium))
                                .lineLimit(1)
                            Text("$\(item.annualFee)/yr")
                                .font(.caption2)
                                .foregroundStyle(.secondary)
                        }

                        Spacer()

                        VStack(alignment: .trailing, spacing: 1) {
                            Text(item.daysUntil == 0 ? "Today" : "\(item.daysUntil)d")
                                .font(.subheadline.weight(.bold))
                                .foregroundStyle(feeUrgencyColor(days: item.daysUntil))
                            Text(item.nextRenewalDate, format: .dateTime.month(.abbreviated).day())
                                .font(.caption2)
                                .foregroundStyle(.secondary)
                        }
                    }
                    if index < min(entry.renewals.count, 3) - 1 {
                        Divider().padding(.vertical, 4)
                    }
                }
            }
        }
        .padding(16)
        .widgetURL(URL(string: "fleece://wallet"))
    }
}

// MARK: Router

struct FeeCalendarWidgetEntryView: View {
    @Environment(\.widgetFamily) private var family
    let entry: FeeCalendarEntry

    var body: some View {
        switch family {
        case .systemMedium:
            FeeCalendarMediumView(entry: entry)
        default:
            FeeCalendarSmallView(entry: entry)
        }
    }
}

// MARK: Widget definition

struct FeeCalendarWidget: Widget {
    let kind = "FeeCalendarWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: FeeCalendarTimelineProvider()) { entry in
            FeeCalendarWidgetEntryView(entry: entry)
                .containerBackground(.background, for: .widget)
        }
        .configurationDisplayName("Annual Fee Calendar")
        .description("Tracks upcoming credit card annual fee renewal dates.")
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}

private func feeUrgencyColor(days: Int) -> Color {
    if days <= 7  { return .red }
    if days <= 30 { return .orange }
    return .primary
}
