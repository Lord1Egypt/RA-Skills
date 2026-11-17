import Foundation

// Shared model written by the main app, read by the widget extension.
// Both targets include this file; only Foundation is imported so there are no target conflicts.
struct FleeceWidgetData: Codable, Sendable {
    let cardName: String
    let cardColor: String       // hex e.g. "#B8860B"
    let textColor: String       // hex e.g. "#FFFFFF"
    let multiplier: Double
    let categoryEmoji: String
    let categoryName: String
    let placeName: String?
    let rewardRate: Double      // effective % e.g. 7.2
    let updatedAt: Date

    static let appGroupID   = "group.io.getfleece.app"
    static let defaultsKey  = "fleeceWidgetData"

    static func load() -> FleeceWidgetData? {
        guard let defaults = UserDefaults(suiteName: appGroupID),
              let data = defaults.data(forKey: defaultsKey) else { return nil }
        return try? JSONDecoder().decode(FleeceWidgetData.self, from: data)
    }

    func save() {
        guard let defaults = UserDefaults(suiteName: FleeceWidgetData.appGroupID),
              let data = try? JSONEncoder().encode(self) else { return }
        defaults.set(data, forKey: FleeceWidgetData.defaultsKey)
    }
}
