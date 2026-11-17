# Fleece iOS — Features Backlog

Planned features, ideas discussed during development, and deferred work.

---

## History Page

### What it would show
A log of past card recommendations — places visited, card suggested, category, estimated reward rate.

### Why we're not building it yet
A history page is only valuable if it shows *value captured*, not just places visited. To do that usefully it needs two things we don't have:

1. **Confirmation the user actually used the recommended card.** There's no way to know this without Apple Pay integration (which exposes card network + merchant post-transaction) or manual user input — both add significant friction.
2. **Transaction amount.** Without it we can't calculate real earned value (e.g. "$4.80 MR on a $60 dinner"). A history of recommendations without dollar amounts is just a worse version of the iPhone's Maps recents list.

Without those two signals, history is a log of *suggestions that may or may not have been acted on* — low signal, adds complexity, and competes with better-designed native apps (Maps, Wallet). The current three-tab layout (Nearby / Wallet / Settings) is clean and focused; a fourth tab with low-value data would dilute it.

### When to revisit
Once Apple Pay integration is in place (see PassKit section). Post-transaction callbacks from Apple Pay can provide card used + merchant + amount — at that point history becomes a genuine value-captured ledger and is worth building.

### What good looks like when we do build it
- Per-transaction row: merchant name, category emoji, card used, points earned, cash value
- Weekly/monthly summary: total points earned, estimated cash value, top merchant categories
- "Missed value" indicator: if user paid with a suboptimal card, show what they left on the table

---

## PassKit

### Lock screen pass / Wallet pass
Issue a Fleece-branded pass into Apple Wallet that surfaces the best card recommendation as a live lock screen widget.

- Use `PKPass` + a signed `.pkpass` bundle served from a backend
- Pass type: Generic pass with a custom barcode or QR
- Dynamic fields: merchant name, best card, multiplier, reward rate
- Update pass via Apple's push notification service for passes (`PKPushRegistry`)
- Requires: PassKit certificate from Apple Developer portal + a small server to sign passes

### Wallet network auto-populate
Currently detection fires on launch and silently sorts the "Add to Wallet" list. Future improvement:
- After user adds a card to Fleece wallet, offer to also add a branded pass to Apple Wallet
- Deep-link to relevant card issuer app for full application

---

## Maps & Place Detection

### Fix manual map tap (MKLocalPointsOfInterestRequest)
✅ Fixed — replaced `MKLocalSearch.Request` + `naturalLanguageQuery` with `MKLocalPointsOfInterestRequest(coordinateRegion:)`. Banner and card recommendations now update correctly when tapping anywhere on the map.

### Real-time place tracking
Use `CLLocationManager.startMonitoringSignificantLocationChanges()` for background location updates — fires a notification when you arrive at a new type of merchant without the user having the app open.

### Geofencing for recurring places
Let users save favourite stores (Trader Joe's, favourite gas station) and get a card reminder notification on entry via `CLCircularRegion` geofence monitoring.

---

## Apple Intelligence / Foundation Models

### Richer AI explanation
Current: one-sentence explanation per card in the recommendations sheet.
Future:
- Stream the response word-by-word using `LanguageModelSession.streamResponse`
- Add a "Why?" button on the horizontal card chips to expand the explanation inline
- Structured output with `@Generable`: return `headline`, `reasoning`, and `estimatedAnnualValue` fields

### AI-powered card database
Use Foundation Models to interpret freeform place names and map them to MCC categories when `MKLocalSearch` returns ambiguous types (e.g. "establishment only").

---

## Wallet & Cards

### Full card database
Expand beyond the current 9 cards to include:
- Chase Freedom Flex, Ink Business cards
- Citi Custom Cash, Premier, Prestige
- Amex EveryDay, Delta co-brands, Marriott Bonvoy
- Discover it, US Bank Altitude
- Synchrony store cards (Amazon, Costco)

### Card image / art
Show the actual card artwork in the wallet using `AsyncImage` loaded from card issuer CDNs or a Fleece-hosted asset catalog.

### iCloud sync
Sync wallet selection across iPhone, iPad, and Mac using `NSUbiquitousKeyValueStore` or CloudKit so the user's card setup carries over to new devices.

### Spending profile
Port the CLI `fleece profile` feature to iOS — stored in `UserDefaults` (same pattern as CLI's SQLite profile). Fields: `dining_monthly`, `groceries_monthly`, `travel_monthly`, `gas_monthly`, `other_monthly`.

Two entry points:
1. **Automatically** — the chat's `UpdateSpendingProfileTool` saves amounts the user mentions in conversation silently, no form required
2. **Manually** — a Profile screen in Settings lets the user view and edit stored values (equivalent to `fleece profile show` / `fleece profile set`)

The stored profile is injected into the `LanguageModelSession` system prompt at session creation so the model starts every chat already knowing the user's spend — no repeated questions.

---

## Notifications

### Rich notifications
Add card art thumbnail to the push notification via `UNNotificationAttachment`.

### Notification actions
Currently "View All Cards" opens the sheet. Add a second action:
- "Add to Wallet" → one tap adds the recommended card to the Fleece wallet

### Smart cooldown
Current: 5-minute global cooldown per place ID. Future: per-category cooldown so moving from a restaurant to a grocery store fires a new notification even within the cooldown window.

---

## App Store

### Developer account
Pending Apple Developer Program approval (`cysbc1999@gmail.com`). Once active:
1. Run `ios/release.sh <TEAM_ID>` to archive + upload
2. Add screenshots from `ios/screenshots/framed/` to App Store Connect
3. Write privacy policy (required — app uses location)
4. Submit for review

### Privacy policy page
✅ Done — hosted at **https://getfleece.io/privacy-policy**. Use this URL in the App Store Connect privacy policy field.

### App Clip
Lightweight `<10 MB` version that activates via NFC or QR at a merchant — shows the best card for that specific store without requiring the full app install.

---

## Widget

### Home screen widget
`WidgetKit` extension showing the best card for the current location, updating via `TimelineProvider` on significant location changes.

- Small: card name + multiplier + category emoji
- Medium: card chip + place name + reward rate
- Lock screen: single line "Use Amex Gold · 4x Dining"

---

## Dynamic Island / Live Activity

When the user enters a store, start a `LiveActivity` showing the best card in the Dynamic Island and on the lock screen. Ends automatically when the user leaves the area.

- Compact leading: category emoji + card name abbreviation
- Compact trailing: multiplier e.g. "4x"
- Expanded: full card chip + place name + reward rate
- Requires `ActivityKit` framework + `NSSupportsLiveActivities` in Info.plist
- iPhone 14 Pro and later only

---

## Siri / App Intents

### "What's my best card for dining?"
`AppIntent` that returns the top dining card from the user's wallet. Surfaces in Siri, Spotlight, and Shortcuts app.

```swift
struct BestCardIntent: AppIntent {
    static var title: LocalizedStringResource = "Best card for category"
    @Parameter(title: "Category") var category: MCCCategoryEntity
    func perform() async throws -> some ReturnsValue<String> { ... }
}
```

### "Add Amex Gold to my Fleece wallet"
Second intent for adding a card by name — useful for onboarding via Siri.

---

## Onboarding Flow

First-launch walkthrough shown once before the main UI:

1. **Welcome** — "Fleece finds your best card at every store"
2. **Location permission** — explain why location is needed, request `whenInUse`
3. **Notification permission** — explain push notifications, request authorization
4. **Add your first card** — inline mini wallet picker (top 3 most popular cards)
5. **Done** — land on Home tab with map ready

Store completion in `UserDefaults("onboardingComplete")`. Skip entirely on re-install if wallet already has cards.

---

## Accessibility

### VoiceOver
- Add `accessibilityLabel` to all card chips: "Amex Gold, best card, 4x Dining, 7.2% back"
- Add `accessibilityHint` to map tap: "Double tap to search for places at this location"
- `accessibilityValue` on wallet toggle buttons: "In wallet" / "Not in wallet"

### Dynamic Type
- Card chip text currently uses fixed font sizes — switch to `scaledFont` so text grows with user's preferred text size setting

---

## CarPlay

Read-only CarPlay scene showing current place + best card on the car's display — no interaction required, updates automatically as the user drives.

- `CPInformationTemplate` with place name, card name, multiplier
- Requires `com.apple.developer.carplay-information` entitlement

---

## watchOS Companion

Standalone Apple Watch app (or complication) showing the best card for the current location.

- Complication: card name + multiplier (e.g. "Amex Gold 4x")
- App: full place + ranked card list
- Shares wallet data with iPhone via `WatchConnectivity`

---

## Spotlight Search

Register cards with `CoreSpotlight` so searching "Amex Gold" or "Chase dining" in Spotlight opens the card detail in Fleece.

```swift
let item = CSSearchableItem(uniqueIdentifier: card.id.uuidString,
                             domainIdentifier: "cards",
                             attributeSet: attributes)
CSSearchableIndex.default().indexSearchableItems([item])
```

---

## Share Enhancement

Current share text is plain string. Improvements:
- Use `ShareLink(item:subject:message:)` with a structured subject line
- Generate a card-branded image (card color + multiplier) via `ImageRenderer` and share as image
- Deep link back to Fleece: `fleece://card/<id>` in the share body

---

## TestFlight

Once Apple Developer account is active, distribute to beta testers via TestFlight before App Store submission:
1. Archive with `ios/release.sh <TEAM_ID>`
2. Upload to App Store Connect
3. Add internal testers (up to 100 with no review)
4. External testers require a brief Beta App Review (~1–2 days)
