# Apple Foundation Models in Fleece

How Fleece uses Apple's on-device language model (`FoundationModels` framework, iOS 26+).

---

## Current Usage

### Card explanation (implemented)

When the user opens the recommendations sheet on iOS 26 with Apple Intelligence enabled, `CardExplanationService` generates a one-sentence explanation of why each card is the top pick at the current merchant.

```swift
// Services/CardExplanationService.swift
@available(iOS 26.0, *)
actor CardExplanationService {
    func explanation(for recommendation: CardRecommendation) async -> String? {
        guard SystemLanguageModel.default.isAvailable else { return nil }
        let session = LanguageModelSession()
        let response = try await session.respond(to: buildPrompt(recommendation))
        return response.content
    }
}
```

**Result shown in `RecommendationRowView`:**
> *"Earns 4x Amex MR on every dining dollar — worth 7.2¢ each."*

**Fallback:** if Apple Intelligence is unavailable, the row shows the static multiplier and rate with no explanation — no empty space, no error.

---

## Chat Tab Architecture (planned)

### Two primitives, one session

The Ask tab uses both Foundation Models features together in a **single session**:

| Primitive | Role |
|---|---|
| **Tool calling** | Fetches ground-truth data (wallet, MCC, ROI) — model can't hallucinate facts |
| **`@Generable`** | Constrains the response to a typed Swift struct — drives the UI directly and extracts spend data in the same pass |

Running one session instead of two avoids competing for the Neural Engine. The `@Generable` schema adds only a handful of tokens — negligible overhead.

---

## `@Generable` Response Schema

The model's entire response — answer, card recommendation, and spend extraction — is returned as a single typed struct:

```swift
@available(iOS 26.0, *)
@Generable
struct FleeceResponse {
    @Guide(description: "Direct answer to the user's question, max 40 words. Never mention internal tool calls.")
    var answer: String

    @Guide(description: "The recommended card name from the wallet, nil if not a card recommendation question")
    var recommendedCard: String?

    @Guide(description: "Effective reward rate as a percentage e.g. 7.2, nil if not applicable")
    var effectiveRate: Double?

    @Guide(description: "One short follow-up question to refine the recommendation, nil if the answer is complete")
    var followUp: String?

    // ── Spend extraction — baked into every response, no second session needed ──
    @Guide(description: "Monthly dining spend in USD if the user mentioned it in this message, else nil")
    var diningMonthly: Double?

    @Guide(description: "Monthly grocery spend in USD if the user mentioned it in this message, else nil")
    var groceriesMonthly: Double?

    @Guide(description: "Monthly travel spend in USD if the user mentioned it in this message, else nil")
    var travelMonthly: Double?

    @Guide(description: "Monthly gas spend in USD if the user mentioned it in this message, else nil")
    var gasMonthly: Double?
}
```

After each turn, the UI reads `answer` and the optional card fields to render the response, then silently updates `SpendingProfile` from the spend fields — **one inference pass, zero extra sessions**.

---

## Tools (3 — all offline, all grounded)

### `GetWalletCardsTool`
Returns the user's wallet cards with multipliers — prevents card name / rate hallucination.

```swift
@available(iOS 26.0, *)
struct GetWalletCardsTool: Tool {
    static let name = "get_wallet_cards"
    static let description = "Returns all credit cards in the user's Fleece wallet with reward multipliers per spend category"
    var cards: [CreditCard]

    func call(context: ToolContext) async throws -> ToolOutput {
        let wallet = cards.filter(\.isInWallet)
        guard !wallet.isEmpty else { return ToolOutput("No cards in wallet.") }
        let summary = wallet.map { card in
            "\(card.name) (\(card.issuer), $\(card.annualFee)/yr, \(card.pointsProgram)): " +
            card.categoryMultipliers.sorted { $0.value > $1.value }
                .map { "\(Int($0.value))x \($0.key)" }.joined(separator: ", ") +
            ", \(card.baseMultiplier)x everything else"
        }.joined(separator: "\n")
        return ToolOutput(summary)
    }
}
```

### `LookupMCCTool`
Reverse-looks up any of the 981 bundled MCC codes — fully offline.

```swift
@available(iOS 26.0, *)
struct LookupMCCTool: Tool {
    static let name = "lookup_mcc"
    static let description = "Returns the merchant category name for a 4-digit MCC code"

    @Parameter(description: "4-digit MCC code e.g. '5812'")
    var code: String

    func call(context: ToolContext) async throws -> ToolOutput {
        for category in MCCCategory.allCases {
            if category.mccCodes.contains(code) {
                return ToolOutput("MCC \(code) → \(category.rawValue) \(category.emoji)")
            }
        }
        return ToolOutput("MCC \(code) not found in local database.")
    }
}
```

### `GetCardROITool`
Local first-year ROI math for any card in `CardDatabase` — no Brave search, no network.

```swift
@available(iOS 26.0, *)
struct GetCardROITool: Tool {
    static let name = "get_card_roi"
    static let description = "Calculates first-year net value for a card given monthly spend amounts"

    @Parameter(description: "Card name e.g. 'Amex Gold'")
    var cardName: String
    @Parameter(description: "Monthly dining spend in USD (0 if unknown)")
    var diningMonthly: Double
    @Parameter(description: "Monthly grocery spend in USD (0 if unknown)")
    var groceriesMonthly: Double
    @Parameter(description: "Monthly travel spend in USD (0 if unknown)")
    var travelMonthly: Double
    @Parameter(description: "Monthly gas spend in USD (0 if unknown)")
    var gasMonthly: Double
    @Parameter(description: "Monthly other spend in USD (0 if unknown)")
    var otherMonthly: Double

    func call(context: ToolContext) async throws -> ToolOutput {
        guard let card = CardDatabase.all.first(where: {
            $0.name.localizedCaseInsensitiveContains(cardName)
        }) else { return ToolOutput("Card '\(cardName)' not found.") }

        let spend: [(MCCCategory, Double)] = [
            (.dining, diningMonthly), (.groceries, groceriesMonthly),
            (.hotels, travelMonthly), (.gas, gasMonthly), (.other, otherMonthly),
        ]
        let annualRewards = spend.reduce(0.0) { sum, pair in
            sum + pair.1 * card.multiplier(for: pair.0) * card.pointValueCents / 100 * 12
        }
        let net = annualRewards - Double(card.annualFee)
        return ToolOutput(
            "\(card.name) ($\(card.annualFee)/yr): " +
            "annual rewards ≈ $\(String(format: "%.0f", annualRewards)), " +
            "net = \(net >= 0 ? "+" : "")$\(String(format: "%.0f", net))"
        )
    }
}
```

---

## Spending Profile Persistence

Mirrors `fleece profile` in the CLI (SQLite) — stored in `UserDefaults` on iOS.

**Write path:** spend fields in `FleeceResponse` — extracted automatically by `@Generable` every turn. If the user mentions `$600 dining`, `diningMonthly = 600` comes back in the response struct. No tool call, no second session.

**Read path:** injected into the system prompt at session creation — model starts every session already knowing the user's spend.

```swift
// UserDefaults-backed profile
struct SpendingProfile: Codable {
    var diningMonthly:    Double = 0
    var groceriesMonthly: Double = 0
    var travelMonthly:    Double = 0
    var gasMonthly:       Double = 0
    var otherMonthly:     Double = 0

    static func load() -> SpendingProfile {
        guard let data = UserDefaults.standard.data(forKey: "spendingProfile"),
              let p = try? JSONDecoder().decode(SpendingProfile.self, from: data)
        else { return SpendingProfile() }
        return p
    }

    func save() {
        UserDefaults.standard.set(try? JSONEncoder().encode(self), forKey: "spendingProfile")
    }

    mutating func update(from response: FleeceResponse) {
        if let v = response.diningMonthly     { diningMonthly = v }
        if let v = response.groceriesMonthly  { groceriesMonthly = v }
        if let v = response.travelMonthly     { travelMonthly = v }
        if let v = response.gasMonthly        { gasMonthly = v }
    }

    var isEmpty: Bool { diningMonthly == 0 && groceriesMonthly == 0 &&
                        travelMonthly == 0 && gasMonthly == 0 }

    var summary: String {
        [(diningMonthly, "dining"), (groceriesMonthly, "groceries"),
         (travelMonthly, "travel"), (gasMonthly, "gas")]
            .filter { $0.0 > 0 }
            .map { "$\(Int($0.0))/mo \($0.1)" }
            .joined(separator: ", ")
    }
}
```

A **Profile screen in Settings** lets the user view and manually edit values — same as `fleece profile show` / `fleece profile set` in the CLI.

---

## Wiring It Together

```swift
@available(iOS 26.0, *)
func makeSession(cards: [CreditCard]) -> LanguageModelSession {
    let profile = SpendingProfile.load()

    let instructions = """
    You are a concise credit card expert for the Fleece app.
    Always call get_wallet_cards before making card recommendations.
    Use get_card_roi when the user asks about value or whether a card is worth it.
    Never invent card names, rates, or fees — only use values from tools.
    Keep answers under 40 words.
    \(profile.isEmpty ? "" : "\nUser spending profile: \(profile.summary)")
    """

    return LanguageModelSession(
        tools: [GetWalletCardsTool(cards: cards), LookupMCCTool(), GetCardROITool()],
        instructions: instructions
    )
}

// Per-turn call — one inference pass for answer + spend extraction
@available(iOS 26.0, *)
func respond(to message: String, session: LanguageModelSession) async throws -> FleeceResponse {
    let response = try await session.respond(to: message, generating: FleeceResponse.self)

    // Persist any spend data the model extracted — zero extra inference
    var profile = SpendingProfile.load()
    profile.update(from: response)
    if !profile.isEmpty { profile.save() }

    return response
}
```

**Full session lifecycle:**
```
Session created (once per chat open)
  └─ SpendingProfile injected into system prompt

Each turn:
  User message
    → tool calls if needed (wallet, MCC, ROI)
    → @Generable FleeceResponse generated
    → UI renders answer + card chip
    → SpendingProfile.update() saves any new spend data silently

App relaunched:
  └─ SpendingProfile loaded from UserDefaults
  └─ New session starts with full spending context — no questions asked
```

---

## Availability & Fallback

| iOS | Device | Apple Intelligence | Chat tab behaviour |
|---|---|---|---|
| iOS 26+ | iPhone 15 Pro / 16+ | On | Full chat with tool calling + `@Generable` |
| iOS 26+ | iPhone 15 Pro / 16+ | Off | "Requires Apple Intelligence" message |
| iOS 17–25 | Any | N/A | "Requires iOS 26" message |

All features gated with `#available(iOS 26.0, *)` + `SystemLanguageModel.default.isAvailable`.

---

## References

- [FoundationModels framework — Apple Developer](https://developer.apple.com/documentation/foundationmodels)
- [Tool calling — Apple Developer](https://developer.apple.com/documentation/foundationmodels/tool)
- [`@Generable` structured output — Apple Developer](https://developer.apple.com/documentation/foundationmodels/generable)
- [Managing context window size — TN3193](https://developer.apple.com/documentation/technotes/tn3193-managing-on-device-foundation-model-context-window)
- [WWDC 2025 — Explore the Foundation Models framework](https://developer.apple.com/videos/wwdc2025)
