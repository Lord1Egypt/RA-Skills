# Fleece iOS — Decision Log

Key architectural and product decisions, in chronological order. Each entry records what was decided, why, and what was ruled out.

---

## Maps & Location

### Use Apple MapKit instead of Google Maps API
**Decision:** MapKit (`MKLocalSearch`, `Map` SwiftUI view) over Google Places API.  
**Why:** Google Places Nearby Search costs $32/1,000 calls with a $200/month free tier. MapKit is free, unlimited, and on-device — no API key, no billing, no data leaving the device.  
**Ruled out:** Google Maps SDK (CocoaPods/SPM dependency, per-request cost).

### Use `MKLocalPointsOfInterestRequest` over `MKLocalSearch.Request`
**Decision:** `MKLocalPointsOfInterestRequest(coordinateRegion:)` for all place searches.  
**Why:** `MKLocalSearch.Request` with `naturalLanguageQuery` treats the region as a hint and anchors results to the device's GPS location, ignoring the passed coordinate. This caused manual map taps to always return the same GPS-anchored place. `MKLocalPointsOfInterestRequest` is strictly bounded to the given region — no natural language bias.  
**Ruled out:** `MKLocalSearch.Request` + `naturalLanguageQuery = "point of interest"` (root cause of the core bug).

### Manual map tap suppresses push notification
**Decision:** `searchAt(notify: false)` — pin drop updates banner and cards silently.  
**Why:** The user is already looking at the screen. A notification is redundant and noisy. GPS auto-detect (`notify: true`) still fires because the user may not be watching the app.

---

## Place Detection

### `SpatialTapGesture` with `simultaneousGesture` over `onTapGesture`
**Decision:** `.simultaneousGesture(SpatialTapGesture())` on the Map view.  
**Why:** `.onTapGesture` is consumed by MapKit's internal pan/zoom gesture recognisers and never fires. `simultaneousGesture` allows both the map's native gestures and our tap to fire at the same time.

### Manual tap uses 300m radius vs 60m for GPS auto-detect
**Decision:** GPS detection radius = 60m, manual tap radius = 300m.  
**Why:** GPS auto-detect runs continuously as you move — tight radius prevents false positives from nearby businesses. Manual tap is intentional and exploratory — wider radius ensures something is found even if the tapped spot doesn't have a POI at the exact pixel.

---

## Card Recommendations

### Slot ordering: best wallet → best non-wallet → rest
**Decision:** Fixed slot assignment regardless of overall ranking:
- Slot 1: highest-earning card in wallet ("use this now")
- Slot 2: highest-earning card not in wallet ("consider adding")
- Slot 3+: remaining cards by effective rate  

**Why:** Gives every session a clear narrative. Slot 1 is actionable (use it now). Slot 2 is aspirational (what you're missing). The rest is informational. A pure rate-sorted list buries the wallet/non-wallet distinction.

---

## Apple Wallet Integration

### Network detection runs silently — no UI badges
**Decision:** PassKit network detection (Visa/MC/Amex/Discover) runs on launch and re-runs after wallet changes, but no detection badges, banners, or indicators are shown to the user.  
**Why:** The "Detected" badge looked cluttered and added no actionable information — the user already knows what cards they have. Detection is used only to silently sort matching cards to the top of "Add to Wallet".

---

## Foundation Models / Apple Intelligence

### Single `LanguageModelSession` with `@Generable` output — no second session
**Decision:** One session per chat tab open. `@Generable FleeceResponse` embeds spend extraction into every response alongside the answer.  
**Why:** Two concurrent sessions compete for the Neural Engine. Running extraction in a separate session degrades main response latency. Embedding spend fields in `FleeceResponse` extracts them in the same inference pass at zero extra cost.  
**Ruled out:** Separate extraction session, `UpdateSpendingProfileTool` (both require a second inference pass).

### `UpdateSpendingProfileTool` dropped — extraction via `@Generable` instead
**Decision:** No tool for writing spend data. `FleeceResponse` has optional spend fields the model populates when the user mentions amounts.  
**Why:** Tool calls are not guaranteed every turn — the model might forget to call `update_spending_profile`. `@Generable` fields are guaranteed to be present in every response, making extraction reliable.

### `GetSpendingProfileTool` dropped — inject via system prompt instead
**Decision:** No tool for reading the profile. `SpendingProfile.load()` is called at session creation and its summary injected directly into the system instructions.  
**Why:** The profile never changes mid-session (only after the session responds). Injecting it upfront is cheaper than a tool call and ensures the model has the context before the first turn.  
**Ruled out:** `GetSpendingProfileTool` (unnecessary round-trip), automatic bank transaction detection via Plaid/FinanceKit (requires backend, violates privacy-first stance).

### Three tools only: `GetWalletCardsTool`, `LookupMCCTool`, `GetCardROITool`
**Decision:** Minimal tool set — three tools, all offline, all grounded in local data.  
**Why:** Every tool adds schema tokens to the context window. Tools should only exist when the model genuinely cannot answer without them. Card names/rates from training data are unreliable; local `CardDatabase` + `MCCCategory` data is authoritative.

### `LanguageModelSession` preserved across wallet changes
**Decision:** `setCards()` updates the injected `cards` reference but does NOT nil the session.  
**Why:** Nilling the session destroys the conversation transcript. `GetWalletCardsTool` fetches live wallet data on every relevant turn — the session doesn't need to restart to see updated cards.

---

## Spending Profile Persistence

### UserDefaults over SQLite
**Decision:** `SpendingProfile` stored as JSON in `UserDefaults`.  
**Why:** Five numeric fields don't warrant a database. `UserDefaults` is simpler, requires no migration infrastructure, and survives app updates. CLI uses SQLite because it's a command-line tool with richer query needs.

### Two entry points: automatic (Ask tab) + manual (Settings)
**Decision:** Spending profile is written automatically by `FleeceResponse` spend fields when the user mentions amounts in chat, and can be manually viewed/edited in Settings → Spending Profile.  
**Why:** Mirrors `fleece profile` in the CLI. Automatic entry removes friction; manual entry gives the user control and transparency.

---

## Chat / Ask Tab

### Build it — despite iOS 26 requirement
**Decision:** Ship the Ask tab targeted at iOS 26 + Apple Intelligence, with a graceful fallback message on older OS.  
**Why:** The primary user (Yuan) is on iOS 26. The feature is a genuine differentiator — no other credit card app has a private, on-device, tool-grounded conversational advisor. The infrastructure (tools, `@Generable`, `SpendingProfile`) was already designed.  
**Original concern:** iOS 26 requirement excludes many users. **Resolved by:** this is a personal-use app first; App Store reach is secondary.

### History page deferred
**Decision:** No history tab.  
**Why:** A history of recommendations is only valuable if it shows value *captured* — which requires knowing the card actually used and the transaction amount. Without Apple Pay integration, both are unavailable. A list of suggestions that may or may not have been acted on is noise. Revisit when Apple Pay integration provides post-transaction data.  
See: `chat-feature-discussion.md`, `ios-features-backlog.md`.

---

## Privacy

### No API keys, no backend, no analytics
**Decision:** Zero third-party services. All compute is on-device.  
**Why:** Credit card usage patterns are sensitive financial data. On-device processing (MapKit, Foundation Models, PassKit, UserDefaults) means no data ever leaves the device to a Fleece-controlled server.  
**Ruled out:** OpenAI API (requires sending queries to external server), Google Places API (per-request cost + data sharing), Plaid/FinanceKit (bank-level data aggregation).
