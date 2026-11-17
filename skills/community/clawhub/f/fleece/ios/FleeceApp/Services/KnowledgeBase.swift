import Foundation

// Offline knowledge base encoding data from kb/ directory.
// All query methods accept case-insensitive partial names and return
// pre-formatted strings ready for tool responses in a LanguageModelSession.
enum KnowledgeBase {

    // MARK: - Transfer Partners

    private struct Partner {
        let name: String
        let ratio: String
        let time: String
        let note: String?
        init(_ name: String, _ ratio: String, _ time: String, note: String? = nil) {
            self.name = name; self.ratio = ratio; self.time = time; self.note = note
        }
    }

    private static let airlinePartners: [String: [Partner]] = [
        "chase ur": [
            Partner("Air Canada Aeroplan",          "1:1", "Instant",   note: "Star Alliance; great for United/Lufthansa partner awards"),
            Partner("Air France/KLM Flying Blue",   "1:1", "Instant",   note: "Frequent Promo Rewards discounts 25–50%"),
            Partner("Aer Lingus AerClub",           "1:1", "Instant",   note: "Oneworld Avios, pools with BA/Iberia"),
            Partner("British Airways Avios",        "1:1", "Instant",   note: "Oneworld; short-haul and AA codeshares"),
            Partner("Emirates Skywards",             "1:1", "1–2 days", note: "Emirates metal only"),
            Partner("Iberia Plus",                  "1:1", "Instant",   note: "Cheapest transatlantic on Iberia metal"),
            Partner("Singapore KrisFlyer",          "1:1", "1–2 days", note: "Top-tier for Singapore Suites and partners"),
            Partner("Southwest Rapid Rewards",      "1:1", "Instant",   note: "No partner awards; best for Companion Pass"),
            Partner("United MileagePlus",           "1:1", "Instant",   note: "Star Alliance; strong close-in saver availability"),
            Partner("Virgin Atlantic Flying Club",  "1:1", "Instant",   note: "Best use: ANA business class and Delta One"),
        ],
        "amex mr": [
            Partner("Air Canada Aeroplan",          "1:1", "2–5 days"),
            Partner("Air France/KLM Flying Blue",   "1:1", "Instant",   note: "Frequent transfer bonuses 15–40%"),
            Partner("ANA Mileage Club",             "1:1", "2–5 days", note: "Best for Japan and round-the-world business class"),
            Partner("British Airways Avios",        "1:1", "Instant"),
            Partner("Cathay Pacific Asia Miles",    "1:1", "2–5 days", note: "Oneworld; excellent premium cabin on Cathay metal"),
            Partner("Delta SkyMiles",               "1:1", "Instant",   note: "Dynamic pricing; rarely the best use of MR"),
            Partner("Emirates Skywards",             "1:1", "2–5 days"),
            Partner("Etihad Guest",                 "1:1", "2–5 days", note: "Oneworld partner access"),
            Partner("Hawaiian Miles",               "1:1", "2–5 days"),
            Partner("Iberia Plus",                  "1:1", "Instant"),
            Partner("JetBlue TrueBlue",             "250:200", "Instant", note: "Below 1:1; generally a poor conversion"),
            Partner("Qantas Frequent Flyer",        "1:1", "2–5 days"),
            Partner("Singapore KrisFlyer",          "1:1", "2–5 days"),
            Partner("Virgin Atlantic Flying Club",  "1:1", "Instant",   note: "Best use: ANA and Delta One"),
        ],
        "capital one": [
            Partner("Air Canada Aeroplan",          "1:1", "1–2 days"),
            Partner("Air France/KLM Flying Blue",   "1:1", "1–2 days"),
            Partner("Avianca LifeMiles",            "1:1", "1–2 days", note: "No fuel surcharges; good Star Alliance coverage"),
            Partner("British Airways Avios",        "1:1", "1–2 days"),
            Partner("Emirates Skywards",             "1:1", "1–2 days"),
            Partner("Etihad Guest",                 "1:1", "1–2 days"),
            Partner("EVA Air Infinity MileageLands","2:1.5", "1–2 days", note: "Below 1:1 ratio"),
            Partner("Finnair Plus",                 "1:1", "1–2 days"),
            Partner("Singapore KrisFlyer",          "1:1", "1–2 days"),
            Partner("Turkish Miles&Smiles",         "1:1", "1–2 days", note: "Low pricing for Star Alliance business class"),
            Partner("Virgin Red",                   "1:1", "1–2 days", note: "Converts to Virgin Atlantic Flying Club"),
        ],
        "citi": [
            Partner("Air France/KLM Flying Blue",   "1:1", "24–48 hrs", note: "Strong program with Promo Rewards"),
            Partner("Avianca LifeMiles",            "1:1", "24–48 hrs", note: "No fuel surcharges"),
            Partner("Cathay Pacific Asia Miles",    "1:1", "24–48 hrs"),
            Partner("Emirates Skywards",             "1:1", "24–48 hrs"),
            Partner("Etihad Guest",                 "1:1", "24–48 hrs"),
            Partner("EVA Air Infinity MileageLands","1:1", "24–48 hrs", note: "Better ratio than Capital One's 2:1.5"),
            Partner("Qantas Frequent Flyer",        "1:1", "24–48 hrs"),
            Partner("Singapore KrisFlyer",          "1:1", "24–48 hrs"),
            Partner("Turkish Miles&Smiles",         "1:1", "24–48 hrs", note: "Best Citi use for Star Alliance business class"),
            Partner("Virgin Atlantic Flying Club",  "1:1", "24–48 hrs"),
        ],
        "bilt": [
            Partner("Air Canada Aeroplan",          "1:1", "Instant"),
            Partner("Air France/KLM Flying Blue",   "1:1", "Instant",   note: "Promo Rewards discounts apply"),
            Partner("Alaska Mileage Plan",          "1:1", "Instant",   note: "Excellent for domestic and Oneworld partner routes"),
            Partner("American AAdvantage",          "1:1", "Instant",   note: "Oneworld; useful for Qantas/Cathay partner awards"),
            Partner("British Airways Avios",        "1:1", "Instant"),
            Partner("Cathay Pacific Asia Miles",    "1:1", "Instant"),
            Partner("Emirates Skywards",             "1:1", "Instant"),
            Partner("Iberia Plus",                  "1:1", "Instant"),
            Partner("Turkish Miles&Smiles",         "1:1", "Instant"),
            Partner("United MileagePlus",           "1:1", "Instant"),
            Partner("Virgin Atlantic Flying Club",  "1:1", "Instant",   note: "ANA and Delta One"),
        ],
    ]

    private static let hotelPartners: [String: [Partner]] = [
        "chase ur": [
            Partner("World of Hyatt",  "1:1", "Instant", note: "Best hotel transfer; ~1.7–2.2 cpp at aspirational properties"),
            Partner("IHG One Rewards", "1:1", "Instant", note: "Best with 4th-night-free benefit"),
            Partner("Marriott Bonvoy", "1:1", "Instant", note: "Generally poor value; avoid unless specific property"),
        ],
        "amex mr": [
            Partner("Choice Privileges", "1:1", "2–5 days", note: "Low aspirational value; niche domestic use"),
            Partner("Hilton Honors",     "1:2", "Instant",  note: "Favorable ratio but Hilton points are low value (~0.5 cpp)"),
            Partner("Marriott Bonvoy",   "1:1", "2–5 days", note: "Poor value; same caution as Chase → Marriott"),
        ],
        "capital one": [
            Partner("Wyndham Rewards", "1:1", "1–2 days", note: "Useful for Vacasa vacation rentals via Wyndham"),
            Partner("Accor Live Limitless", "2:1", "1–2 days", note: "Poor ratio; avoid"),
        ],
        "citi": [
            Partner("Wyndham Rewards", "1:1", "24–48 hrs"),
        ],
        "bilt": [
            Partner("World of Hyatt",  "1:1", "Instant", note: "Same top-tier value as Chase UR → Hyatt; Bilt is the only no-fee card with this partner"),
            Partner("IHG One Rewards", "1:1", "Instant"),
            Partner("Marriott Bonvoy", "1:1", "Instant", note: "Poor value as with other programs"),
            Partner("Hilton Honors",   "1:1", "Instant", note: "1:1 here vs Amex's 1:2 — better ratio"),
        ],
    ]

    static func transferPartners(for program: String) -> String {
        let key = programKey(program)
        let airlines = airlinePartners[key]
        let hotels   = hotelPartners[key]
        guard airlines != nil || hotels != nil else {
            return "Unknown program '\(program)'. Supported: Chase UR, Amex MR, Capital One Miles, Citi ThankYou, Bilt."
        }
        var lines: [String] = ["Transfer partners for \(key.uppercased()):"]
        if let a = airlines {
            lines.append("Airlines:")
            lines += a.map { p in
                var s = "  • \(p.name) (\(p.ratio), \(p.time))"
                if let n = p.note { s += " — \(n)" }
                return s
            }
        }
        if let h = hotels {
            lines.append("Hotels:")
            lines += h.map { p in
                var s = "  • \(p.name) (\(p.ratio), \(p.time))"
                if let n = p.note { s += " — \(n)" }
                return s
            }
        }
        return lines.joined(separator: "\n")
    }

    // MARK: - Point Valuations

    private static let valuationText: [String: String] = [
        "chase ur": """
        Chase UR valuations:
        Floor: 1.0 cpp cash back. Portal: 1.5 cpp (CSR) / 1.25 cpp (CSP).
        Best: Hyatt 1.7–2.2 cpp, Virgin Atlantic→ANA/Delta 1.5–2.0 cpp, Singapore 1.5–2.0 cpp.
        Good: Aeroplan 1.3–1.6 cpp, Flying Blue 1.3–1.5 cpp, United 1.2–1.5 cpp.
        Blended average: ~1.5–1.8 cpp.
        """,
        "amex mr": """
        Amex MR valuations:
        Floor: 0.6 cpp statement credit — avoid. Portal: 1.0 cpp — avoid.
        Best: ANA 1.5–2.2 cpp, Virgin Atlantic→ANA/Delta 1.5–2.0 cpp, Singapore 1.5–2.0 cpp.
        Good: Cathay 1.4–1.8 cpp, Flying Blue 1.3–1.7 cpp. Avoid Delta (dynamic pricing).
        Blended average: ~1.3–1.8 cpp.
        """,
        "capital one": """
        Capital One Miles valuations:
        Floor: 0.5 cpp — avoid. Portal: 1.0 cpp.
        Best: Turkish Miles&Smiles 1.5–2.2 cpp, Virgin Atlantic 1.5–2.0 cpp.
        Good: Avianca 1.3–1.6 cpp, Singapore 1.4–1.8 cpp, Flying Blue 1.3–1.5 cpp.
        Blended average: ~1.2–1.6 cpp.
        """,
        "citi": """
        Citi ThankYou valuations:
        Floor: 0.5–1.0 cpp — avoid. Portal: 1.0 cpp.
        Best: Turkish Miles&Smiles 1.5–2.2 cpp, Virgin Atlantic 1.5–2.0 cpp.
        Good: Singapore 1.4–1.8 cpp, EVA Air 1.3–1.6 cpp (Citi transfers 1:1, better than C1's 2:1.5).
        Blended average: ~1.2–1.6 cpp.
        """,
        "bilt": """
        Bilt valuations:
        Floor: 1.0 cpp rent/statement credit. Portal: 1.25 cpp.
        Best: Hyatt 1.7–2.2 cpp (unique — only no-fee card with Hyatt), Turkish 1.5–2.2 cpp.
        Good: Alaska 1.4–1.6 cpp, Virgin Atlantic 1.5–2.0 cpp.
        Blended average: ~1.4–1.8 cpp. Rent Day (1st of month) doubles earn rates.
        """,
    ]

    static func pointValuations(for program: String) -> String {
        let key = programKey(program)
        return valuationText[key] ?? "Unknown program '\(program)'. Supported: Chase UR, Amex MR, Capital One Miles, Citi ThankYou, Bilt."
    }

    // MARK: - Application Rules

    private static let rulesText: [String: String] = [
        "chase": """
        Chase application rules:
        5/24: Denied if 5+ new cards (any issuer) opened in past 24 months. Business cards from Amex/Citi/Chase don't count.
        Sapphire: 48-month cooldown from last Sapphire sign-up offer. Can't hold Preferred + Reserve simultaneously.
        Ink: Each Ink product has its own 24-month offer cooldown.
        Velocity: ~2 personal / 1 business card per 30 days.
        """,
        "amex": """
        Amex application rules:
        Once-per-lifetime: Each Amex card's sign-up offer can only be earned once per person, even after cancelling and reapplying.
        Pop-up: Amex may show a "not eligible" notice before you apply. Proceeding gives approval but no offer.
        Limit: Max 5 Amex credit cards at once. Platinum/Gold/Green are charge cards with a separate limit.
        Velocity: ~4 Amex cards per 90 days before potential declines.
        """,
        "citi": """
        Citi application rules:
        24-month rule: Can't earn a sign-up offer if you hold the card, closed it, or earned its offer within 24 months.
        48-month rule: Strata Premier and Prestige have a 48-month offer cooldown.
        Velocity: Max 1 card per 8 days, 2 cards per 65 days.
        """,
        "capital one": """
        Capital One application rules:
        Card limit: Max 2 personal cards at once.
        Velocity: Typically 1 personal card per 6 months.
        Bureau pull: Pulls all 3 bureaus (Equifax, Experian, TransUnion) on most applications.
        """,
    ]

    static func applicationRules(for issuer: String) -> String {
        let key = issuer.lowercased()
            .replacingOccurrences(of: "american express", with: "amex")
        let matched = rulesText.keys.first { key.contains($0) || $0.contains(key) }
        guard let k = matched else {
            return "No application rules found for '\(issuer)'. Supported: Chase, Amex, Citi, Capital One."
        }
        return rulesText[k]!
    }

    // MARK: - Card Benefits

    private struct CardBenefitData {
        let lounges: String?
        let tripCancellation: String?
        let tripDelay: String?
        let rentalCar: String?
        let baggage: String?
        let other: String?
    }

    private static let benefits: [(keys: [String], data: CardBenefitData)] = [
        (
            keys: ["sapphire reserve", "csr"],
            data: CardBenefitData(
                lounges: "Chase Sapphire Lounges (BOS, HKG, JFK, LAS, LGA, PHL, PHX, SFO + expanding) + Priority Pass Select (1,400+ lounges worldwide, $35/guest)",
                tripCancellation: "$10,000/person, $20,000/trip",
                tripDelay: "$500/ticket after 6-hour delay or overnight",
                rentalCar: "Primary CDW up to $75,000 — decline rental company's CDW",
                baggage: "Lost/damaged: $3,000/passenger; Delay: $100/day for 5 days after 6 hours",
                other: "Travel accident: up to $1,000,000; Purchase protection: 120 days up to $10,000; Extended warranty: +1 year on warranties ≤ 3 years"
            )
        ),
        (
            keys: ["sapphire preferred", "csp"],
            data: CardBenefitData(
                lounges: "None",
                tripCancellation: "$10,000/person, $20,000/trip",
                tripDelay: "$500/ticket after 12-hour delay or overnight",
                rentalCar: "Primary CDW",
                baggage: "Lost/damaged: $3,000/passenger; Delay: $100/day for 5 days after 12 hours",
                other: "Travel accident: up to $500,000; Purchase protection: 120 days up to $500; Extended warranty: +1 year on warranties ≤ 3 years"
            )
        ),
        (
            keys: ["amex platinum", "platinum card"],
            data: CardBenefitData(
                lounges: "Centurion Lounges ($50/guest fee unless $75k+ annual spend) + Priority Pass Select + Delta Sky Club (10 visits/year cap unless $75k+ spend) + International Amex Lounges",
                tripCancellation: "$10,000/trip",
                tripDelay: "$500/ticket after 6-hour delay (up to 2 claims per 12 months)",
                rentalCar: "Secondary CDW only (not primary); Premium Car Rental Protection add-on available for ~$25",
                baggage: "Lost: $3,000 carry-on, $2,000 checked (excess over airline reimbursement)",
                other: "Travel accident: up to $500,000; Purchase protection: 90 days up to $10,000; Extended warranty: +1 year on warranties ≤ 5 years"
            )
        ),
        (
            keys: ["amex gold", "gold card"],
            data: CardBenefitData(
                lounges: "None",
                tripCancellation: "Not included — key gap vs Platinum",
                tripDelay: "$300/ticket after 12-hour delay",
                rentalCar: "Secondary CDW only",
                baggage: "Lost: $1,250 carry-on, $500 checked",
                other: "Purchase protection: 90 days up to $10,000; Extended warranty: +1 year on warranties ≤ 5 years"
            )
        ),
        (
            keys: ["amex green"],
            data: CardBenefitData(
                lounges: "LoungeBuddy credit $100/year (pay-per-visit access at 50+ lounges)",
                tripCancellation: "Not included",
                tripDelay: "Not included",
                rentalCar: "Secondary CDW only",
                baggage: nil,
                other: "CLEAR Plus credit $100/year"
            )
        ),
        (
            keys: ["venture x"],
            data: CardBenefitData(
                lounges: "Capital One Lounges (unlimited, 2 free guests) + Priority Pass Select ($35/guest)",
                tripCancellation: "$2,000/person",
                tripDelay: "$500/ticket after 6 hours",
                rentalCar: "Primary CDW",
                baggage: "Lost: $3,000/passenger",
                other: "Purchase protection: 90 days up to $10,000; Extended warranty: +2 years on warranties ≤ 3 years; Global Entry/TSA PreCheck credit"
            )
        ),
        (
            keys: ["venture", "capital one venture"],
            data: CardBenefitData(
                lounges: "None (Venture only; Venture X has lounge access)",
                tripCancellation: nil,
                tripDelay: nil,
                rentalCar: "Primary CDW",
                baggage: nil,
                other: "Global Entry/TSA PreCheck credit (once every 4 years)"
            )
        ),
        (
            keys: ["bilt"],
            data: CardBenefitData(
                lounges: "None",
                tripCancellation: "$5,000/trip",
                tripDelay: "$200/day up to $1,800 after 6-hour delay",
                rentalCar: "Primary CDW",
                baggage: nil,
                other: "Cell phone protection: $800/claim, $1,600/year, $25 deductible (pay phone bill with card)"
            )
        ),
        (
            keys: ["freedom unlimited", "cfu"],
            data: CardBenefitData(
                lounges: "None",
                tripCancellation: nil,
                tripDelay: nil,
                rentalCar: "Primary CDW",
                baggage: nil,
                other: "Purchase protection: 120 days up to $500"
            )
        ),
        (
            keys: ["strata premier", "citi premier"],
            data: CardBenefitData(
                lounges: "None",
                tripCancellation: "$5,000/trip (when booked with TYP or card)",
                tripDelay: nil,
                rentalCar: nil,
                baggage: nil,
                other: nil
            )
        ),
        (
            keys: ["double cash"],
            data: CardBenefitData(
                lounges: "None",
                tripCancellation: nil,
                tripDelay: nil,
                rentalCar: "Secondary CDW",
                baggage: nil,
                other: "Worldwide travel accident insurance; Citi Concierge; no notable travel protections — pair with Strata Premier for transfer access"
            )
        ),
        (
            keys: ["freedom flex"],
            data: CardBenefitData(
                lounges: "None",
                tripCancellation: "$1,500/trip",
                tripDelay: "$500 after 12 hours",
                rentalCar: "Primary CDW",
                baggage: nil,
                other: "Cell phone protection: $800/claim, $1,000/year, $50 deductible (pay phone bill with card); Purchase protection: 120 days up to $500"
            )
        ),
        (
            keys: ["blue cash preferred", "amex blue cash"],
            data: CardBenefitData(
                lounges: "None",
                tripCancellation: nil,
                tripDelay: nil,
                rentalCar: "Secondary CDW only",
                baggage: nil,
                other: "Purchase protection: 90 days up to $1,000/item; Extended warranty: +1 year on warranties ≤ 5 years; Return protection: 90 days up to $300/item"
            )
        ),
        (
            keys: ["autograph", "wells fargo autograph"],
            data: CardBenefitData(
                lounges: "None",
                tripCancellation: nil,
                tripDelay: nil,
                rentalCar: "Secondary CDW",
                baggage: nil,
                other: "Cell phone protection: $600/claim, $1,200/year, $25 deductible (pay phone bill with card); Travel accident insurance; Roadside dispatch"
            )
        ),
        (
            keys: ["united club business", "united club"],
            data: CardBenefitData(
                lounges: "Full United Club membership (45+ United hubs) + Star Alliance lounges internationally",
                tripCancellation: "$1,500/trip",
                tripDelay: "$500 after 12 hours",
                rentalCar: nil,
                baggage: nil,
                other: nil
            )
        ),

        // Business cards
        (
            keys: ["sapphire reserve for business"],
            data: CardBenefitData(
                lounges: "Chase Sapphire Lounges + Priority Pass Select ($35/guest)",
                tripCancellation: "$10,000/person, $20,000/trip",
                tripDelay: "$500/ticket after 6 hours",
                rentalCar: "Primary CDW up to $75,000",
                baggage: "Lost: $3,000/passenger; Delay: $100/day after 6 hours",
                other: nil
            )
        ),
        (
            keys: ["ink business preferred", "ink preferred"],
            data: CardBenefitData(
                lounges: "None",
                tripCancellation: "$5,000/trip",
                tripDelay: "$500 after 12 hours",
                rentalCar: "Primary CDW",
                baggage: nil,
                other: "Cell phone protection: $1,000/claim, $1,800/year, $100 deductible (pay phone bill with card)"
            )
        ),
        (
            keys: ["ink business cash", "ink cash"],
            data: CardBenefitData(
                lounges: "None",
                tripCancellation: nil,
                tripDelay: nil,
                rentalCar: "Primary CDW",
                baggage: nil,
                other: "Cell phone protection: $1,000/claim, $1,800/year, $100 deductible (pay phone bill with card)"
            )
        ),
        (
            keys: ["ink business unlimited", "ink unlimited"],
            data: CardBenefitData(
                lounges: "None",
                tripCancellation: nil,
                tripDelay: nil,
                rentalCar: "Primary CDW",
                baggage: nil,
                other: nil
            )
        ),
        (
            keys: ["ink business premier", "ink premier"],
            data: CardBenefitData(
                lounges: "None",
                tripCancellation: "$5,000/trip",
                tripDelay: "$500 after 12 hours",
                rentalCar: "Primary CDW",
                baggage: nil,
                other: nil
            )
        ),
        (
            keys: ["united business"],
            data: CardBenefitData(
                lounges: "Two single-day United Club passes per year",
                tripCancellation: "$1,500/trip",
                tripDelay: "$500 after 12 hours",
                rentalCar: nil,
                baggage: nil,
                other: nil
            )
        ),
        (
            keys: ["sw premier business", "southwest premier business"],
            data: CardBenefitData(
                lounges: "None",
                tripCancellation: nil,
                tripDelay: nil,
                rentalCar: nil,
                baggage: nil,
                other: "Earns toward Companion Pass (requires 135,000 qualifying points/calendar year)"
            )
        ),
        (
            keys: ["sw performance business", "southwest performance business"],
            data: CardBenefitData(
                lounges: "4 upgraded boardings/year + Global Entry/TSA PreCheck credit",
                tripCancellation: nil,
                tripDelay: nil,
                rentalCar: nil,
                baggage: nil,
                other: "Earns toward Companion Pass; in-flight Wi-Fi credits (365/year)"
            )
        ),
        (
            keys: ["ihg premier business"],
            data: CardBenefitData(
                lounges: "None",
                tripCancellation: nil,
                tripDelay: nil,
                rentalCar: nil,
                baggage: nil,
                other: "4th night free on award stays; IHG Platinum Elite status; annual free night certificate"
            )
        ),
        (
            keys: ["hyatt business"],
            data: CardBenefitData(
                lounges: "None",
                tripCancellation: nil,
                tripDelay: nil,
                rentalCar: nil,
                baggage: nil,
                other: "Hyatt Discoverist status; 5 qualifying night credits per year; free night certificate after $15k spend"
            )
        ),
    ]

    static func cardBenefits(for cardName: String) -> String {
        let key = cardName.lowercased()
        // "venture x" must be checked before plain "venture"
        let match = benefits.first { entry in
            entry.keys.contains { k in key.contains(k) || k.contains(key) }
        }
        guard let entry = match else {
            return "No benefits data found for '\(cardName)'. Try the full card name e.g. 'Sapphire Reserve', 'Amex Platinum', 'Venture X'."
        }
        let d = entry.data
        var lines = ["Benefits for \(cardName):"]
        if let v = d.lounges           { lines.append("Lounge access: \(v)") }
        if let v = d.tripCancellation  { lines.append("Trip cancellation: \(v)") }
        if let v = d.tripDelay         { lines.append("Trip delay: \(v)") }
        if let v = d.rentalCar         { lines.append("Rental car: \(v)") }
        if let v = d.baggage           { lines.append("Baggage: \(v)") }
        if let v = d.other             { lines.append("Other: \(v)") }
        return lines.joined(separator: "\n")
    }

    // MARK: - Helpers

    private static func programKey(_ input: String) -> String {
        let s = input.lowercased()
        if s.contains("chase") || s.contains("ur") || s.contains("ultimate") { return "chase ur" }
        if s.contains("amex") || s.contains("membership") || s.contains("mr") { return "amex mr" }
        if s.contains("capital one") || s.contains("c1") { return "capital one" }
        if s.contains("citi") || s.contains("thankyou") || s.contains("typ") { return "citi" }
        if s.contains("bilt") { return "bilt" }
        return s
    }
}
