#if canImport(FoundationModels)
import FoundationModels

// MARK: - Argument types (@Generable structs the model populates)

@available(iOS 26.0, *)
@Generable
struct NoArguments {}

@available(iOS 26.0, *)
@Generable
struct MCCLookupArguments {
    @Guide(description: "4-digit MCC code e.g. '5812'")
    var code: String
}

@available(iOS 26.0, *)
@Generable
struct ROIArguments {
    @Guide(description: "Card name e.g. 'Amex Gold'")
    var cardName: String
    @Guide(description: "Monthly dining spend in USD, 0 if unknown")
    var diningMonthly: Double
    @Guide(description: "Monthly grocery spend in USD, 0 if unknown")
    var groceriesMonthly: Double
    @Guide(description: "Monthly travel spend in USD, 0 if unknown")
    var travelMonthly: Double
    @Guide(description: "Monthly gas spend in USD, 0 if unknown")
    var gasMonthly: Double
    @Guide(description: "Monthly other spend in USD, 0 if unknown")
    var otherMonthly: Double
}

@available(iOS 26.0, *)
@Generable
struct TransferPartnerArguments {
    @Guide(description: "Points program: 'Chase UR', 'Amex MR', 'Capital One Miles', 'Citi ThankYou', or 'Bilt'")
    var program: String
}

@available(iOS 26.0, *)
@Generable
struct ValuationArguments {
    @Guide(description: "Points program: 'Chase UR', 'Amex MR', 'Capital One Miles', 'Citi ThankYou', or 'Bilt'")
    var program: String
}

@available(iOS 26.0, *)
@Generable
struct ApplicationRulesArguments {
    @Guide(description: "Card issuer: 'Chase', 'Amex', 'Citi', or 'Capital One'")
    var issuer: String
}

@available(iOS 26.0, *)
@Generable
struct CardBenefitsArguments {
    @Guide(description: "Card name e.g. 'Sapphire Reserve', 'Amex Platinum', 'Venture X', 'Bilt'")
    var cardName: String
}

// MARK: - Tools

@available(iOS 26.0, *)
struct GetWalletCardsTool: Tool {
    let name = "get_wallet_cards"
    let description = "Returns all credit cards in the user's Fleece wallet with reward multipliers per category. Always call before making recommendations."
    let cards: [CreditCard]

    func call(arguments: NoArguments) async throws -> String {
        let wallet = cards.filter(\.isInWallet)
        guard !wallet.isEmpty else {
            return "No cards in wallet. Ask the user to add cards in the Wallet tab."
        }
        return wallet.map { card in
            "\(card.name) (\(card.issuer), $\(card.annualFee)/yr, \(card.pointsProgram)): " +
            card.categoryMultipliers.sorted { $0.value > $1.value }
                .map { "\(Int($0.value))x \($0.key)" }.joined(separator: ", ") +
            ", \(card.baseMultiplier)x everything else"
        }.joined(separator: "\n")
    }
}

@available(iOS 26.0, *)
struct LookupMCCTool: Tool {
    let name = "lookup_mcc"
    let description = "Returns the merchant category name and emoji for a 4-digit MCC code from the bundled offline database of 981 codes."

    func call(arguments: MCCLookupArguments) async throws -> String {
        let code = arguments.code.trimmingCharacters(in: .whitespaces)
        for category in MCCCategory.allCases {
            if category.mccCodes.contains(code) {
                return "MCC \(code) → \(category.rawValue) \(category.emoji)"
            }
        }
        return "MCC \(code) not found in local database."
    }
}

@available(iOS 26.0, *)
struct GetCardROITool: Tool {
    let name = "get_card_roi"
    let description = "Calculates first-year net value for a card given monthly spend. Use when user asks if a card is worth it or wants to compare value."

    func call(arguments: ROIArguments) async throws -> String {
        guard let card = CardDatabase.all.first(where: {
            $0.name.localizedCaseInsensitiveContains(arguments.cardName)
        }) else {
            return "Card '\(arguments.cardName)' not found. Available: \(CardDatabase.all.map(\.name).joined(separator: ", "))"
        }
        let spend: [(MCCCategory, Double)] = [
            (.dining, arguments.diningMonthly),
            (.groceries, arguments.groceriesMonthly),
            (.hotels, arguments.travelMonthly),
            (.gas, arguments.gasMonthly),
            (.other, arguments.otherMonthly),
        ]
        let annualRewards = spend.reduce(0.0) { sum, pair in
            sum + pair.1 * card.multiplier(for: pair.0) * card.pointValueCents / 100 * 12
        }
        let net = annualRewards - Double(card.annualFee)
        return "\(card.name) ($\(card.annualFee)/yr, \(card.pointsProgram)): " +
               "annual rewards ≈ $\(String(format: "%.0f", annualRewards)), " +
               "net = \(net >= 0 ? "+" : "")$\(String(format: "%.0f", net))"
    }
}

// MARK: - KB-backed tools

@available(iOS 26.0, *)
struct GetTransferPartnersTool: Tool {
    let name = "get_transfer_partners"
    let description = "Returns airline and hotel transfer partners with ratios and transfer times for a given points program (Chase UR, Amex MR, Capital One Miles, Citi ThankYou, Bilt). Call when the user asks where they can transfer points or which airlines a card partners with."

    func call(arguments: TransferPartnerArguments) async throws -> String {
        KnowledgeBase.transferPartners(for: arguments.program)
    }
}

@available(iOS 26.0, *)
struct GetPointValuationsTool: Tool {
    let name = "get_point_valuations"
    let description = "Returns cents-per-point estimates for each redemption path in a given program. Call when the user asks how much points are worth, whether a program is good, or wants to compare redemption value."

    func call(arguments: ValuationArguments) async throws -> String {
        KnowledgeBase.pointValuations(for: arguments.program)
    }
}

@available(iOS 26.0, *)
struct GetApplicationRulesTool: Tool {
    let name = "get_application_rules"
    let description = "Returns issuer-specific application rules: Chase 5/24, Amex once-per-lifetime sign-up offer rule, Citi 24/48-month cooldowns, Capital One card limits. Call when the user asks about eligibility, sign-up offer availability, or application strategy."

    func call(arguments: ApplicationRulesArguments) async throws -> String {
        KnowledgeBase.applicationRules(for: arguments.issuer)
    }
}

@available(iOS 26.0, *)
struct GetCardBenefitsTool: Tool {
    let name = "get_card_benefits"
    let description = "Returns lounge access and travel protection details (trip cancellation, trip delay, rental car CDW, baggage) for a specific card. Call when the user asks about insurance, lounge access, protections, or whether a card covers rental cars or trip delays."

    func call(arguments: CardBenefitsArguments) async throws -> String {
        KnowledgeBase.cardBenefits(for: arguments.cardName)
    }
}

// MARK: - Structured response

@available(iOS 26.0, *)
@Generable
struct FleeceResponse {
    @Guide(description: "Direct answer, max 40 words. Never mention internal tool calls.")
    var answer: String
    @Guide(description: "Recommended card name from wallet, nil if not applicable")
    var recommendedCard: String?
    @Guide(description: "Effective reward rate as a percentage e.g. 7.2, nil if not applicable")
    var effectiveRate: Double?
    @Guide(description: "One short follow-up question, nil if answer is complete")
    var followUp: String?
    @Guide(description: "Monthly dining spend in USD if user mentioned it this turn, else nil")
    var diningMonthly: Double?
    @Guide(description: "Monthly grocery spend in USD if user mentioned it this turn, else nil")
    var groceriesMonthly: Double?
    @Guide(description: "Monthly travel spend in USD if user mentioned it this turn, else nil")
    var travelMonthly: Double?
    @Guide(description: "Monthly gas spend in USD if user mentioned it this turn, else nil")
    var gasMonthly: Double?
    @Guide(description: "Preferred airline loyalty program if user mentioned it this turn e.g. 'United MileagePlus', else nil")
    var preferredAirlinePartner: String?
    @Guide(description: "Preferred hotel loyalty program if user mentioned it this turn e.g. 'World of Hyatt', else nil")
    var preferredHotelPartner: String?
}

#endif
