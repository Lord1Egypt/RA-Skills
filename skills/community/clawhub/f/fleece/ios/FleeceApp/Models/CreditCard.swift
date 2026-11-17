import SwiftUI

struct CreditCard: Identifiable, Codable, Equatable {
    let id: UUID
    let name: String
    let issuer: String
    let annualFee: Int
    let pointsProgram: String       // "Chase UR", "Amex MR", "Cash Back", etc.
    let pointValueCents: Double     // cents per point (e.g. 1.5 for Chase UR)
    let categoryMultipliers: [String: Double] // MCCCategory.rawValue → multiplier
    let baseMultiplier: Double
    let cardColor: String           // hex string e.g. "#1A1A2E"
    let textColor: String           // hex string for card text
    var isInWallet: Bool

    // Effective reward rate as a percentage for a given category
    func rewardRate(for category: MCCCategory) -> Double {
        let multiplier = categoryMultipliers[category.rawValue] ?? baseMultiplier
        return multiplier * pointValueCents / 100.0 * 100.0 // → percentage
    }

    func multiplier(for category: MCCCategory) -> Double {
        categoryMultipliers[category.rawValue] ?? baseMultiplier
    }
}

extension CreditCard {
    var color: Color { Color(hex: cardColor) ?? .blue }
    var labelColor: Color { Color(hex: textColor) ?? .white }
}

// MARK: - Color hex init
extension Color {
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
