import Foundation

struct CardRecommendation: Identifiable {
    let id = UUID()
    let card: CreditCard
    let multiplier: Double
    let category: MCCCategory
    let place: NearbyPlace
    let rank: Int               // 1 = best

    /// Effective cash-equivalent rate as a percentage (e.g. 6.0 = 6%)
    var effectiveRate: Double {
        multiplier * card.pointValueCents / 100.0 * 100.0
    }

    /// What you earn per $100 spent
    var perHundred: Double {
        multiplier * card.pointValueCents
    }

    var isInWallet: Bool { card.isInWallet }
    var isBestInWallet: Bool { isInWallet && rank == 1 }
}
