import Foundation

// Shared model written by the main app, read by the fee calendar widget extension.
// Both targets include this file; only Foundation is imported so there are no target conflicts.
struct FeeCalendarWidgetData: Codable, Sendable {
    struct RenewalItem: Codable, Sendable {
        let cardName: String
        let cardColor: String       // hex e.g. "#B8860B"
        let textColor: String       // hex e.g. "#FFFFFF"
        let annualFee: Int
        let nextRenewalDate: Date
        let daysUntil: Int
    }

    let renewals: [RenewalItem]     // sorted ascending by daysUntil
    let updatedAt: Date

    static let appGroupID  = "group.io.getfleece.app"
    static let defaultsKey = "fleeceFeeCalendarData"

    static func load() -> FeeCalendarWidgetData? {
        guard let defaults = UserDefaults(suiteName: appGroupID),
              let data = defaults.data(forKey: defaultsKey) else { return nil }
        return try? JSONDecoder().decode(FeeCalendarWidgetData.self, from: data)
    }

    func save() {
        guard let defaults = UserDefaults(suiteName: FeeCalendarWidgetData.appGroupID),
              let data = try? JSONEncoder().encode(self) else { return }
        defaults.set(data, forKey: FeeCalendarWidgetData.defaultsKey)
    }
}
