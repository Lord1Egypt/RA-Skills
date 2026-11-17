import PassKit

// Maps PKPaymentNetwork → card IDs in CardDatabase
// One network can match multiple cards; user confirms which ones they actually have.
enum WalletDetectionService {

    struct DetectionResult {
        let detectedNetworks: Set<PKPaymentNetwork>
        let suggestedCards: [CreditCard]   // candidates matching detected networks
        let confirmedCards: [CreditCard]   // already in wallet
    }

    // Which networks to probe (everything CardDatabase covers)
    static let probedNetworks: [PKPaymentNetwork] = [.amex, .visa, .masterCard, .discover]

    static func detect(cards: [CreditCard]) -> DetectionResult {
        let detected = probedNetworks.filter { network in
            PKPaymentAuthorizationController.canMakePayments(usingNetworks: [network])
        }
        let detectedSet = Set(detected)

        let suggestions = cards.filter { card in
            !card.isInWallet && networkMatches(card: card, networks: detectedSet)
        }
        let confirmed = cards.filter(\.isInWallet)

        return DetectionResult(
            detectedNetworks: detectedSet,
            suggestedCards: suggestions,
            confirmedCards: confirmed
        )
    }

    // Card → network mapping (based on CardDatabase issuers)
    private static func networkMatches(card: CreditCard,
                                       networks: Set<PKPaymentNetwork>) -> Bool {
        switch card.issuer {
        case "American Express":    return networks.contains(.amex)
        case "Bilt / Wells Fargo":  return networks.contains(.masterCard)
        case "Citi":                return networks.contains(.masterCard)
        default:                    return networks.contains(.visa)   // Chase, Capital One
        }
    }
}

extension PKPaymentNetwork {
    var displayName: String {
        switch self {
        case .amex:       return "Amex"
        case .visa:       return "Visa"
        case .masterCard: return "Mastercard"
        case .discover:   return "Discover"
        default:          return rawValue.capitalized
        }
    }

    var emoji: String {
        switch self {
        case .amex:       return "💳"
        case .visa:       return "🔵"
        case .masterCard: return "🔴"
        case .discover:   return "🟠"
        default:          return "💳"
        }
    }
}
