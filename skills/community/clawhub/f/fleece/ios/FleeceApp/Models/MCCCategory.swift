import MapKit

enum MCCCategory: String, CaseIterable, Codable, Identifiable {
    case dining       = "Dining"
    case groceries    = "Groceries"
    case gas          = "Gas"
    case hotels       = "Hotels"
    case flights      = "Flights"
    case transit      = "Transit"
    case drugstore    = "Drugstore"
    case entertainment = "Entertainment"
    case streaming    = "Streaming"
    case shopping     = "Shopping"
    case other        = "Other"

    var id: String { rawValue }

    var mccCodes: [String] {
        switch self {
        case .dining:        return ["5812", "5813", "5814"]
        case .groceries:     return ["5411", "5422", "5441", "5451", "5462", "5499"]
        case .gas:           return ["5541", "5542", "5172"]
        case .hotels:        return ["7011", "7012", "7013"]
        case .flights:       return ["4511", "3000", "3001", "3002"]
        case .transit:       return ["4111", "4112", "4121", "4131"]
        case .drugstore:     return ["5912"]
        case .entertainment: return ["7832", "7922", "7993", "7996", "7999"]
        case .streaming:     return ["5815"]
        case .shopping:      return ["5311", "5331", "5691", "5732", "5945"]
        case .other:         return []
        }
    }

    var emoji: String {
        switch self {
        case .dining:        return "🍽️"
        case .groceries:     return "🛒"
        case .gas:           return "⛽"
        case .hotels:        return "🏨"
        case .flights:       return "✈️"
        case .transit:       return "🚇"
        case .drugstore:     return "💊"
        case .entertainment: return "🎭"
        case .streaming:     return "📺"
        case .shopping:      return "🛍️"
        case .other:         return "💳"
        }
    }
}

// MARK: - MKPointOfInterestCategory → MCCCategory (free, no API key)

extension MCCCategory {
    static func from(poiCategory: MKPointOfInterestCategory?) -> MCCCategory {
        guard let poi = poiCategory else { return .other }
        switch poi {
        case .foodMarket:
            return .groceries
        case .restaurant, .cafe, .bakery, .brewery, .winery, .nightlife:
            return .dining
        case .gasStation:
            return .gas
        case .hotel:
            return .hotels
        case .airport:
            return .flights
        case .publicTransport:
            return .transit
        case .pharmacy:
            return .drugstore
        case .movieTheater, .stadium, .amusementPark:
            return .entertainment
        case .store, .fitnessCenter:
            return .shopping
        default:
            return .other
        }
    }
}
