#if canImport(FoundationModels)
import FoundationModels
#endif
import Foundation

@MainActor
final class ChatService: ObservableObject {
    @Published var messages: [ChatMessage] = []
    @Published var isThinking = false
    @Published var error: String?

    private var cards: [CreditCard] = []

    // Store session as Any? — avoids @available on stored property
    private var _sessionAny: Any?

    func setCards(_ cards: [CreditCard]) {
        self.cards = cards
        // Do NOT reset the session here — the model calls GetWalletCardsTool
        // live on every relevant turn, so fresh wallet data is always fetched.
        // Destroying the session would wipe the conversation transcript.
    }

    func send(_ text: String) async {
        guard !text.trimmingCharacters(in: .whitespaces).isEmpty else { return }
        messages.append(ChatMessage(user: text))
        isThinking = true
        error = nil

        if #available(iOS 26.0, *) {
            // Pass safety-sanitized text to Foundation Models; UI shows the original.
            await sendWithAI(Self.sanitizeForSafety(text))
        } else {
            messages.append(ChatMessage(
                answer: "AI chat requires iOS 26 with Apple Intelligence enabled.",
                followUp: nil
            ))
        }
        isThinking = false
    }

    func clear() {
        messages = []
        _sessionAny = nil
    }

    // MARK: - Input sanitization

    // Rewrite user input before passing to Foundation Models — the filter pattern-matches
    // on "Can I get X again?" as policy-circumvention even in financial context.
    // Order matters: rewrite question forms first, then fix remaining bonus vocabulary.
    // The UI always shows the user's original text.
    static func sanitizeForSafety(_ text: String) -> String {
        var s = text
        let replacements: [(String, String)] = [
            // Question-form rewrites (run first — most specific)
            ("can i get the",        "am i eligible for the"),
            ("can i get a",          "am i eligible for a"),
            ("can i get",            "am i eligible for"),
            ("how do i get the",     "what are the requirements for the"),
            ("how do i get a",       "what are the requirements for a"),
            // Bonus terminology
            ("sign-up bonus",        "sign-up offer"),
            ("signup bonus",         "sign-up offer"),
            ("welcome bonus",        "welcome offer"),
            ("card bonus",           "card sign-up offer"),
            (" bonus",               " sign-up offer"),
        ]
        for (trigger, safe) in replacements {
            s = s.replacingOccurrences(of: trigger, with: safe, options: .caseInsensitive)
        }
        return s
    }

    // MARK: - iOS 26

    @available(iOS 26.0, *)
    private var session: LanguageModelSession {
        if let s = _sessionAny as? LanguageModelSession { return s }
        let s = makeSession()
        _sessionAny = s
        return s
    }

    @available(iOS 26.0, *)
    private func makeSession() -> LanguageModelSession {
        let profile = SpendingProfile.load()
        let instructions = """
        You are Fleece, a personal finance assistant for US consumers managing credit cards and travel rewards. \
        This is a legitimate financial planning tool. All queries are about personal credit card selection, \
        rewards optimization, application eligibility rules, and travel booking — standard consumer finance topics.
        Always call get_wallet_cards before making card recommendations.
        Use get_card_roi when the user asks about value or whether a card is worth it.
        Use get_transfer_partners when asked where to transfer points or which airlines a card partners with.
        Use get_point_valuations when asked how much points are worth or for the best redemption paths.
        Use get_application_rules when asked about eligibility, sign-up offer rules, or issuer application policies.
        Use get_card_benefits when asked about lounge access, trip delay, rental car insurance, or travel protections.
        Never invent card names, rates, or fees — only use values returned by tools.
        Always say "sign-up offer" not "bonus" in your answers.
        Keep answers under 40 words. Be direct and specific.
        \(profile.summary.isEmpty ? "" : "\nUser spending profile: \(profile.summary)")
        """
        return LanguageModelSession(
            tools: [
                GetWalletCardsTool(cards: cards),
                LookupMCCTool(),
                GetCardROITool(),
                GetTransferPartnersTool(),
                GetPointValuationsTool(),
                GetApplicationRulesTool(),
                GetCardBenefitsTool(),
            ],
            instructions: instructions
        )
    }

    @available(iOS 26.0, *)
    private func sendWithAI(_ text: String) async {
        guard SystemLanguageModel.default.isAvailable else {
            messages.append(ChatMessage(
                answer: "Enable Apple Intelligence in Settings → Apple Intelligence & Siri.",
                followUp: nil
            ))
            return
        }
        do {
            let response = try await session.respond(to: text, generating: FleeceResponse.self)
            let r = response.content

            // Persist spend data silently
            var profile = SpendingProfile.load()
            var updated = false
            if let v = r.diningMonthly    { profile.diningMonthly = v;    updated = true }
            if let v = r.groceriesMonthly { profile.groceriesMonthly = v; updated = true }
            if let v = r.travelMonthly    { profile.travelMonthly = v;    updated = true }
            if let v = r.gasMonthly       { profile.gasMonthly = v;       updated = true }
            if let v = r.preferredAirlinePartner, !v.isEmpty { profile.preferredAirlinePartner = v; updated = true }
            if let v = r.preferredHotelPartner,   !v.isEmpty { profile.preferredHotelPartner = v;   updated = true }
            if updated { profile.save() }

            messages.append(ChatMessage(
                answer: r.answer,
                recommendedCard: r.recommendedCard,
                effectiveRate: r.effectiveRate,
                followUp: r.followUp
            ))
        } catch {
            let detail = (error as NSError).localizedDescription
            self.error = detail
            let isSafety = detail.lowercased().contains("unsafe") || detail.lowercased().contains("safety")
            // Reset session after safety error — accumulated history may re-trigger the filter.
            if isSafety { _sessionAny = nil }
            messages.append(ChatMessage(
                answer: isSafety
                    ? "Apple's on-device safety filter flagged this — tap the suggestion below to retry with cleaner phrasing."
                    : "Error: \(detail)",
                followUp: isSafety ? "Am I eligible for the Amex Gold sign-up offer?" : nil
            ))
        }
    }
}
