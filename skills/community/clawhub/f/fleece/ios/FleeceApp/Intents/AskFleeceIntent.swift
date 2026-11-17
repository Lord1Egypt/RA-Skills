import AppIntents
#if canImport(FoundationModels)
import FoundationModels
#endif
import Foundation

// MARK: - Intent

struct AskFleeceIntent: AppIntent {
    static let title: LocalizedStringResource = "Ask Fleece"
    static let description = IntentDescription(
        "Ask Fleece a question about credit card rewards, transfer partners, lounge access, or travel benefits.",
        categoryName: "Finance"
    )

    @Parameter(title: "Question", description: "e.g. Which card earns the most on dining?")
    var question: String

    static var parameterSummary: some ParameterSummary {
        Summary("Ask Fleece: \(\.$question)")
    }

    func perform() async throws -> some ReturnsValue<String> & ProvidesDialog {
        #if canImport(FoundationModels)
        if #available(iOS 26.0, *) {
            let answer = try await performWithAI()
            return .result(value: answer, dialog: IntentDialog(stringLiteral: answer))
        }
        #endif
        let msg = "Fleece AI requires iOS 26 with Apple Intelligence enabled."
        return .result(value: msg, dialog: IntentDialog(stringLiteral: msg))
    }

    // Reads wallet membership from the same UserDefaults key AppState writes.
    private func loadWalletCards() -> [CreditCard] {
        let ids = Set(UserDefaults.standard.stringArray(forKey: "fleeceWallet") ?? [])
        return CardDatabase.all.map {
            var c = $0
            c.isInWallet = ids.contains($0.id.uuidString)
            return c
        }
    }
}

// MARK: - Foundation Models implementation

#if canImport(FoundationModels)
@available(iOS 26.0, *)
private extension AskFleeceIntent {
    func performWithAI() async throws -> String {
        guard SystemLanguageModel.default.isAvailable else {
            return "Enable Apple Intelligence in Settings → Apple Intelligence & Siri."
        }
        let cards = loadWalletCards()
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
        let session = LanguageModelSession(
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
        let response = try await session.respond(
            to: ChatService.sanitizeForSafety(question),
            generating: FleeceResponse.self
        )
        return response.content.answer
    }
}
#endif

// MARK: - Siri voice shortcuts

struct FleeceShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: AskFleeceIntent(),
            phrases: [
                "Ask \(.applicationName)",
                "Ask \(.applicationName) a question",
            ],
            shortTitle: "Ask Fleece",
            systemImageName: "creditcard"
        )
    }
}
