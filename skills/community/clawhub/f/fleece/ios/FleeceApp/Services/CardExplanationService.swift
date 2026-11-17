import Foundation
#if canImport(FoundationModels)
import FoundationModels
#endif

// On iOS 18.1+ with Apple Intelligence enabled this generates a one-sentence
// explanation of why a card is the best choice at the current merchant.
// On all other devices / configurations it returns nil silently — callers
// must treat the explanation as optional progressive enhancement.

@available(iOS 26.0, *)
actor CardExplanationService {
    static let shared = CardExplanationService()

    private var cache: [String: String] = [:]

    func explanation(for recommendation: CardRecommendation) async -> String? {
        let key = cacheKey(recommendation)
        if let hit = cache[key] { return hit }

        guard isAvailable() else { return nil }

        let prompt = buildPrompt(recommendation)
        do {
            let session = LanguageModelSession()
            let response = try await session.respond(to: prompt)
            let text = response.content
                .trimmingCharacters(in: .whitespacesAndNewlines)
                // strip any leading/trailing quotes the model sometimes adds
                .trimmingCharacters(in: CharacterSet(charactersIn: "\"'"))
            cache[key] = text
            return text
        } catch {
            return nil
        }
    }

    // MARK: - Private

    private func isAvailable() -> Bool {
        SystemLanguageModel.default.isAvailable
    }

    private func cacheKey(_ rec: CardRecommendation) -> String {
        "\(rec.card.id.uuidString)-\(rec.category.rawValue)"
    }

    private func buildPrompt(_ rec: CardRecommendation) -> String {
        let rate   = String(format: "%.1f%%", rec.effectiveRate)
        let mult   = rec.multiplier == rec.multiplier.rounded()
                     ? "\(Int(rec.multiplier))x"
                     : String(format: "%.1fx", rec.multiplier)
        return """
        You are a concise credit card expert. Write exactly one sentence (12 words max) \
        explaining why \(rec.card.name) is the top choice at \(rec.place.name). \
        Key fact: earns \(mult) on \(rec.category.rawValue) = \(rate) back (\(rec.card.pointsProgram)). \
        Be specific. No filler words. No quotation marks in your response.
        Good example: "Earns 4x Amex MR on dining — worth 7.2¢ per dollar."
        """
    }
}
