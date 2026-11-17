import Foundation

// Hard-coded card data for major US cards.
// Multipliers reflect published category bonuses as of mid-2025.
// Point values are conservative mid-market estimates (TPG/NerdWallet baseline).
enum CardDatabase {
    static let all: [CreditCard] = [
        CreditCard(
            id: UUID(uuidString: "A0000001-0000-0000-0000-000000000001")!,
            name: "Sapphire Reserve",
            issuer: "Chase",
            annualFee: 550,
            pointsProgram: "Chase UR",
            pointValueCents: 1.5,
            categoryMultipliers: [
                MCCCategory.dining.rawValue:        3,
                MCCCategory.hotels.rawValue:        3,
                MCCCategory.flights.rawValue:       3,
                MCCCategory.transit.rawValue:       3,
            ],
            baseMultiplier: 1,
            cardColor: "#1A1A2E",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000001-0000-0000-0000-000000000002")!,
            name: "Sapphire Preferred",
            issuer: "Chase",
            annualFee: 95,
            pointsProgram: "Chase UR",
            pointValueCents: 1.25,
            categoryMultipliers: [
                MCCCategory.dining.rawValue:        3,
                MCCCategory.groceries.rawValue:     3,
                MCCCategory.streaming.rawValue:     3,
                MCCCategory.hotels.rawValue:        2,
                MCCCategory.flights.rawValue:       2,
                MCCCategory.transit.rawValue:       2,
            ],
            baseMultiplier: 1,
            cardColor: "#1B4F72",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000001-0000-0000-0000-000000000003")!,
            name: "Freedom Unlimited",
            issuer: "Chase",
            annualFee: 0,
            pointsProgram: "Chase UR",
            pointValueCents: 1.0,
            categoryMultipliers: [
                MCCCategory.dining.rawValue:        3,
                MCCCategory.drugstore.rawValue:     3,
                MCCCategory.hotels.rawValue:        5,
                MCCCategory.flights.rawValue:       5,
                MCCCategory.transit.rawValue:       5,
            ],
            baseMultiplier: 1.5,
            cardColor: "#2C3E50",
            textColor: "#F39C12",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000001-0000-0000-0000-000000000004")!,
            name: "Gold Card",
            issuer: "American Express",
            annualFee: 325,
            pointsProgram: "Amex MR",
            pointValueCents: 1.8,
            categoryMultipliers: [
                MCCCategory.dining.rawValue:        4,
                MCCCategory.groceries.rawValue:     4,
                MCCCategory.flights.rawValue:       3,
            ],
            baseMultiplier: 1,
            cardColor: "#B8860B",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000001-0000-0000-0000-000000000005")!,
            name: "Platinum Card",
            issuer: "American Express",
            annualFee: 695,
            pointsProgram: "Amex MR",
            pointValueCents: 2.0,
            categoryMultipliers: [
                MCCCategory.flights.rawValue:       5,
                MCCCategory.hotels.rawValue:        5,
            ],
            baseMultiplier: 1,
            cardColor: "#A8A9AD",
            textColor: "#000000",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000001-0000-0000-0000-000000000006")!,
            name: "Blue Cash Preferred",
            issuer: "American Express",
            annualFee: 95,
            pointsProgram: "Cash Back",
            pointValueCents: 1.0,
            categoryMultipliers: [
                MCCCategory.groceries.rawValue:     6,
                MCCCategory.streaming.rawValue:     6,
                MCCCategory.gas.rawValue:           3,
                MCCCategory.transit.rawValue:       3,
            ],
            baseMultiplier: 1,
            cardColor: "#007DC3",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000001-0000-0000-0000-000000000007")!,
            name: "Bilt Mastercard",
            issuer: "Bilt / Wells Fargo",
            annualFee: 0,
            pointsProgram: "Bilt Points",
            pointValueCents: 1.5,
            categoryMultipliers: [
                MCCCategory.dining.rawValue:        3,
                MCCCategory.hotels.rawValue:        2,
                MCCCategory.flights.rawValue:       2,
                MCCCategory.transit.rawValue:       2,
            ],
            baseMultiplier: 1,
            cardColor: "#2D2D2D",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000001-0000-0000-0000-000000000008")!,
            name: "Venture X",
            issuer: "Capital One",
            annualFee: 395,
            pointsProgram: "Capital One Miles",
            pointValueCents: 1.7,
            categoryMultipliers: [
                MCCCategory.hotels.rawValue:        10,
                MCCCategory.flights.rawValue:       5,
            ],
            baseMultiplier: 2,
            cardColor: "#C0392B",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000001-0000-0000-0000-000000000009")!,
            name: "Double Cash",
            issuer: "Citi",
            annualFee: 0,
            pointsProgram: "Cash Back",
            pointValueCents: 1.0,
            categoryMultipliers: [:],
            baseMultiplier: 2,
            cardColor: "#212F3C",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000001-0000-0000-0000-000000000010")!,
            name: "Freedom Flex",
            issuer: "Chase",
            annualFee: 0,
            pointsProgram: "Chase UR",
            pointValueCents: 1.0,
            categoryMultipliers: [
                MCCCategory.dining.rawValue:        3,
                MCCCategory.drugstore.rawValue:     3,
                MCCCategory.hotels.rawValue:        5,
                MCCCategory.flights.rawValue:       5,
                MCCCategory.transit.rawValue:       5,
            ],
            baseMultiplier: 1,
            cardColor: "#1A5276",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000001-0000-0000-0000-000000000011")!,
            name: "Green Card",
            issuer: "American Express",
            annualFee: 150,
            pointsProgram: "Amex MR",
            pointValueCents: 1.8,
            categoryMultipliers: [
                MCCCategory.dining.rawValue:        3,
                MCCCategory.hotels.rawValue:        3,
                MCCCategory.flights.rawValue:       3,
                MCCCategory.transit.rawValue:       3,
            ],
            baseMultiplier: 1,
            cardColor: "#1E8449",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000001-0000-0000-0000-000000000012")!,
            name: "Strata Premier",
            issuer: "Citi",
            annualFee: 95,
            pointsProgram: "Citi ThankYou",
            pointValueCents: 1.5,
            categoryMultipliers: [
                MCCCategory.dining.rawValue:        3,
                MCCCategory.groceries.rawValue:     3,
                MCCCategory.flights.rawValue:       3,
                MCCCategory.hotels.rawValue:        3,
                MCCCategory.gas.rawValue:           3,
            ],
            baseMultiplier: 1,
            cardColor: "#154360",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000001-0000-0000-0000-000000000013")!,
            name: "Venture",
            issuer: "Capital One",
            annualFee: 95,
            pointsProgram: "Capital One Miles",
            pointValueCents: 1.5,
            categoryMultipliers: [
                MCCCategory.hotels.rawValue:        5,
                MCCCategory.flights.rawValue:       5,
            ],
            baseMultiplier: 2,
            cardColor: "#A93226",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000001-0000-0000-0000-000000000014")!,
            name: "Autograph",
            issuer: "Wells Fargo",
            annualFee: 0,
            pointsProgram: "WF Rewards",
            pointValueCents: 1.0,
            categoryMultipliers: [
                MCCCategory.dining.rawValue:        3,
                MCCCategory.hotels.rawValue:        3,
                MCCCategory.flights.rawValue:       3,
                MCCCategory.gas.rawValue:           3,
                MCCCategory.transit.rawValue:       3,
                MCCCategory.streaming.rawValue:     3,
            ],
            baseMultiplier: 1,
            cardColor: "#C0392B",
            textColor: "#FFFFFF",
            isInWallet: false
        ),

        CreditCard(
            id: UUID(uuidString: "A0000001-0000-0000-0000-000000000015")!,
            name: "Robinhood Gold Card",
            issuer: "Robinhood",
            annualFee: 50,
            pointsProgram: "Cash Back",
            pointValueCents: 1.0,
            categoryMultipliers: [:],
            baseMultiplier: 3,
            cardColor: "#C8A400",
            textColor: "#000000",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000001-0000-0000-0000-000000000016")!,
            name: "Active Cash",
            issuer: "Wells Fargo",
            annualFee: 0,
            pointsProgram: "Cash Back",
            pointValueCents: 1.0,
            categoryMultipliers: [:],
            baseMultiplier: 2,
            cardColor: "#CC0000",
            textColor: "#FFFFFF",
            isInWallet: false
        ),

        CreditCard(
            id: UUID(uuidString: "A0000001-0000-0000-0000-000000000017")!,
            name: "Discover it Cash Back",
            issuer: "Discover",
            annualFee: 0,
            pointsProgram: "Cash Back",
            pointValueCents: 1.0,
            categoryMultipliers: [
                MCCCategory.gas.rawValue:           5,
                MCCCategory.groceries.rawValue:     5,
                MCCCategory.dining.rawValue:        5,
                MCCCategory.drugstore.rawValue:     5,
            ],
            baseMultiplier: 1,
            cardColor: "#F76B1C",
            textColor: "#FFFFFF",
            isInWallet: false
        ),

        // MARK: - Business Cards

        CreditCard(
            id: UUID(uuidString: "A0000002-0000-0000-0000-000000000001")!,
            name: "Sapphire Reserve for Business",
            issuer: "Chase",
            annualFee: 795,
            pointsProgram: "Chase UR",
            pointValueCents: 1.5,
            categoryMultipliers: [
                MCCCategory.hotels.rawValue:        8,
                MCCCategory.flights.rawValue:       8,
                MCCCategory.shopping.rawValue:      3,  // social media / search advertising
            ],
            baseMultiplier: 1,
            cardColor: "#0D1B2A",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000002-0000-0000-0000-000000000002")!,
            name: "Ink Business Preferred",
            issuer: "Chase",
            annualFee: 95,
            pointsProgram: "Chase UR",
            pointValueCents: 1.25,
            categoryMultipliers: [
                MCCCategory.flights.rawValue:       3,
                MCCCategory.hotels.rawValue:        3,
                MCCCategory.transit.rawValue:       3,
                MCCCategory.shopping.rawValue:      3,  // shipping, internet/cable/phone, social media ads
            ],
            baseMultiplier: 1,
            cardColor: "#1F618D",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000002-0000-0000-0000-000000000003")!,
            name: "Ink Business Cash",
            issuer: "Chase",
            annualFee: 0,
            pointsProgram: "Cash Back",
            pointValueCents: 1.0,
            categoryMultipliers: [
                MCCCategory.shopping.rawValue:      5,  // office supply stores, internet/cable/phone
                MCCCategory.dining.rawValue:        2,
                MCCCategory.gas.rawValue:           2,
            ],
            baseMultiplier: 1,
            cardColor: "#1A252F",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000002-0000-0000-0000-000000000004")!,
            name: "Ink Business Unlimited",
            issuer: "Chase",
            annualFee: 0,
            pointsProgram: "Cash Back",
            pointValueCents: 1.0,
            categoryMultipliers: [:],
            baseMultiplier: 1.5,
            cardColor: "#283747",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000002-0000-0000-0000-000000000005")!,
            name: "Ink Business Premier",
            issuer: "Chase",
            annualFee: 195,
            pointsProgram: "Cash Back",
            pointValueCents: 1.0,
            categoryMultipliers: [
                MCCCategory.hotels.rawValue:        5,  // Chase Travel portal
                MCCCategory.flights.rawValue:       5,
            ],
            baseMultiplier: 2,
            cardColor: "#1C2833",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000002-0000-0000-0000-000000000006")!,
            name: "United Business",
            issuer: "Chase",
            annualFee: 150,
            pointsProgram: "United Miles",
            pointValueCents: 1.2,
            categoryMultipliers: [
                MCCCategory.flights.rawValue:       2,
                MCCCategory.dining.rawValue:        2,
                MCCCategory.gas.rawValue:           2,
                MCCCategory.transit.rawValue:       2,
                MCCCategory.shopping.rawValue:      2,  // office supply stores
            ],
            baseMultiplier: 1,
            cardColor: "#003580",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000002-0000-0000-0000-000000000007")!,
            name: "United Club Business",
            issuer: "Chase",
            annualFee: 695,
            pointsProgram: "United Miles",
            pointValueCents: 1.2,
            categoryMultipliers: [
                MCCCategory.flights.rawValue:       2,
                MCCCategory.hotels.rawValue:        5,  // Renowned Hotels
            ],
            baseMultiplier: 1,
            cardColor: "#002244",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000002-0000-0000-0000-000000000008")!,
            name: "SW Premier Business",
            issuer: "Chase",
            annualFee: 149,
            pointsProgram: "SW Rapid Rewards",
            pointValueCents: 1.3,
            categoryMultipliers: [
                MCCCategory.flights.rawValue:       3,
                MCCCategory.dining.rawValue:        2,
                MCCCategory.gas.rawValue:           2,
            ],
            baseMultiplier: 1,
            cardColor: "#304CB2",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000002-0000-0000-0000-000000000009")!,
            name: "SW Performance Business",
            issuer: "Chase",
            annualFee: 299,
            pointsProgram: "SW Rapid Rewards",
            pointValueCents: 1.3,
            categoryMultipliers: [
                MCCCategory.flights.rawValue:       4,
                MCCCategory.dining.rawValue:        2,
                MCCCategory.gas.rawValue:           2,
                MCCCategory.transit.rawValue:       2,
                MCCCategory.hotels.rawValue:        2,
            ],
            baseMultiplier: 1,
            cardColor: "#1A3A8F",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000002-0000-0000-0000-000000000010")!,
            name: "IHG Premier Business",
            issuer: "Chase",
            annualFee: 99,
            pointsProgram: "IHG Points",
            pointValueCents: 0.5,
            categoryMultipliers: [
                MCCCategory.hotels.rawValue:        10,
                MCCCategory.flights.rawValue:       5,
                MCCCategory.dining.rawValue:        5,
                MCCCategory.gas.rawValue:           5,
            ],
            baseMultiplier: 3,
            cardColor: "#2E7D32",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
        CreditCard(
            id: UUID(uuidString: "A0000002-0000-0000-0000-000000000011")!,
            name: "Hyatt Business",
            issuer: "Chase",
            annualFee: 199,
            pointsProgram: "Hyatt Points",
            pointValueCents: 1.7,
            categoryMultipliers: [
                MCCCategory.hotels.rawValue:        4,
                MCCCategory.dining.rawValue:        2,
            ],
            baseMultiplier: 1,
            cardColor: "#1B2631",
            textColor: "#FFFFFF",
            isInWallet: false
        ),
    ]
}
