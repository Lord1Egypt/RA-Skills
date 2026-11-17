import Foundation

struct CardRecommender {
    /// Returns cards in a fixed slot order:
    ///   #1 — best card in wallet (use this now)
    ///   #2 — best card NOT in wallet (consider adding this)
    ///   #3+ — remaining cards sorted by effective rate
    static func recommend(for place: NearbyPlace, cards: [CreditCard]) -> [CardRecommendation] {
        let category = place.category

        func makeRec(_ card: CreditCard, rank: Int) -> CardRecommendation {
            CardRecommendation(
                card: card,
                multiplier: card.multiplier(for: category),
                category: category,
                place: place,
                rank: rank
            )
        }

        func byRate(_ a: CreditCard, _ b: CreditCard) -> Bool {
            let ra = a.rewardRate(for: category)
            let rb = b.rewardRate(for: category)
            if ra != rb { return ra > rb }
            return a.annualFee < b.annualFee
        }

        let wallet    = cards.filter(\.isInWallet).sorted(by: byRate)
        let nonWallet = cards.filter { !$0.isInWallet }.sorted(by: byRate)

        var result: [CardRecommendation] = []

        // Slot 1: best wallet card
        if let best = wallet.first {
            result.append(makeRec(best, rank: 1))
        }

        // Slot 2: best non-wallet card (upgrade suggestion)
        if let bestOut = nonWallet.first {
            result.append(makeRec(bestOut, rank: 2))
        }

        // Slots 3+: remaining wallet cards then remaining non-wallet, by rate
        let rest = (wallet.dropFirst() + nonWallet.dropFirst()).sorted(by: byRate)
        for (i, card) in rest.enumerated() {
            result.append(makeRec(card, rank: i + 3))
        }

        return result
    }

    /// Returns the single best wallet card (for notifications).
    /// Falls back to the globally best card if the wallet is empty.
    static func bestCard(for place: NearbyPlace, cards: [CreditCard]) -> CardRecommendation? {
        let all = recommend(for: place, cards: cards)
        return all.first(where: { $0.card.isInWallet }) ?? all.first
    }
}
