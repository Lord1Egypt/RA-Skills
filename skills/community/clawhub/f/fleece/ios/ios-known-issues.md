# Fleece iOS — Known Issues

---

## 1. Manual map tap does not update place banner or card recommendations

**Status:** ✅ Fixed  
**Affected build:** all current builds  
**Affects:** Simulator and physical device  

### Symptom
Tapping the map drops the native red `Marker` pin at the tapped coordinate, but the place banner and card recommendation strip do not update to reflect the tapped location — they remain on the last GPS-detected place.

### What was tried
| Approach | Result |
|---|---|
| `onTapGesture` on `Map` | Swallowed by MapKit's pan/zoom gesture handlers — tap never fires |
| `simultaneousGesture(SpatialTapGesture())` on `Map` | Tap fires, pin drops, but `MKLocalSearch` returns same result as GPS location |
| Increased search radius to 300m for manual taps | No change in banner output |

### Root cause hypothesis
`MKLocalSearch` with `naturalLanguageQuery: "point of interest"` appears to anchor results to the device's current GPS location rather than the `region.center` passed in the request when running on the iOS 26 simulator. The search returns the same prominent landmark (Point Reyes National Seashore) regardless of the tapped coordinate.

### Root cause
`MKLocalSearch.Request` with `naturalLanguageQuery` treats the region as a hint and anchors results to the device's GPS location, ignoring the tapped coordinate.

### Fix applied
Replaced `MKLocalSearch.Request` + `naturalLanguageQuery` with `MKLocalPointsOfInterestRequest(coordinateRegion:)` which anchors strictly to the passed region. No natural language query — returns all POIs within the given radius of the tapped point.

---

## 2. iOS 26 Simulator — MapKit tiles intermittently blank on launch

**Status:** Known simulator bug (not a Fleece bug)  
**Affected:** iOS 26.5 simulator only  

### Symptom
On app launch the map area renders white. The nav bar, tab bar, and recommendation strip all appear correctly.

### Fix
Shut down and reboot the simulator before launching:
```bash
xcrun simctl shutdown <UDID>
xcrun simctl boot <UDID>
xcrun simctl location <UDID> set 37.7749,-122.4194
```

---

## 3. Apple Intelligence chat returns "Something went wrong" on KB tool queries

**Status:** ✅ Partially mitigated (root cause: on-device context window limit)
**Affected:** Physical device, iOS 26+, Apple Intelligence enabled
**Triggers:** Questions that invoke `get_application_rules` or `get_point_valuations`

### Symptom
Asking questions like "Can I get the Amex Gold bonus again?" or "How much are my Chase points worth?" causes the AI chat to return a generic error instead of an answer.

### Console output (noise — unrelated to this bug)
The following lines appear in the Xcode console on every run and are **not** related to this issue:
```
Failed to locate resource named "default.csv"
Connection error: com.apple.PerfPowerTelemetryClientRegistrationService … Sandbox restriction
(+[PPSClientDonation …]) Permission denied: Maps / SpringfieldUsage
CAMetalLayer ignoring invalid setDrawableSize width=0.000000 height=0.000000
```
These are simulator sandbox and telemetry artifacts. Safe to ignore.

### Root cause
`KnowledgeBase.applicationRules()` and `KnowledgeBase.valuationText` were returning 100–200 word strings per tool call. After a tool call, the full response (system prompt + conversation + tool result) is passed back to the on-device model for `FleeceResponse` guided generation. Long tool responses exhaust the context budget, causing the generation to fail and throw.

The error was also silently swallowed — "Something went wrong" gave no diagnostic information.

### Fix applied
- Trimmed `rulesText` and `valuationText` from ~150 words to ~40 words each, preserving the key facts.
- Changed catch block to show the actual `NSError.localizedDescription` in the chat bubble so future errors are diagnosable.
- Committed in `39157be`.

### If the error recurs
Check the chat bubble — it now shows the real error message. Common follow-ons:
- `"generation failed: context length exceeded"` → further trim the relevant KB text string
- `"schema validation failed"` → check `@Generable FleeceResponse` field count / optionality
- `"model unavailable"` → Apple Intelligence is off or device is not eligible
- `"detected content likely to be unsafe"` → see Issue #4 below

---

## 4. Apple Intelligence returns "detected content likely to be unsafe" on application eligibility queries

**Status:** ⚠️ Unresolved — suggestion pill removed, question type avoided  
**Affected:** Physical device, iOS 26+, Apple Intelligence enabled  
**Triggers:** Any query about card application eligibility / sign-up offer re-eligibility (e.g. "Can I get the Amex Gold bonus again?", "Am I eligible for the Amex Gold sign-up offer?")

### Symptom
Chat returns "detected content likely to be unsafe" for legitimate credit card application eligibility questions regardless of phrasing. This is a persistent false positive — the content is standard US consumer finance.

### Mitigation attempts (all failed to fully resolve)
| Attempt | Change | Result |
|---|---|---|
| 1 | System prompt legitimate-use framing | Still triggers |
| 2 | KB text: "welcome bonus" → "sign-up offer" | Still triggers |
| 3 | `sanitizeForSafety`: "bonus" → "sign-up offer" in input | Still triggers |
| 4 | `sanitizeForSafety`: "Can I get the" → "am i eligible for the" | Still triggers |
| 5 | System prompt: always say "sign-up offer" not "bonus" | Still triggers |
| 6 | Session reset on safety error to clear contaminated history | Still triggers |

### Root cause hypothesis
Apple's on-device safety filter appears to flag the entire **topic** of card application eligibility rules, not just specific vocabulary. The `get_application_rules` tool call itself, or the content it returns (issuer rules about offer re-eligibility), may be what triggers the filter regardless of how the question is phrased. The filter may be inspecting tool responses in the context window, not just the user's input text.

### Resolution
- Removed the application eligibility suggestion pill from `AskView` — don't surface this question type as a suggested prompt.
- The `get_application_rules` tool remains in the session for users who manually ask; the session resets on safety error so it doesn't contaminate subsequent queries.
- If Apple updates the safety filter calibration in a future iOS 26 beta, re-test with "What are the Chase 5/24 rules?" as a lower-risk phrasing.

### Still-working workarounds
Questions about application rules that do NOT mention re-eligibility or "can I get" are less likely to trigger:
- ✅ "What is Chase 5/24?"
- ✅ "What are the Citi 24-month rules?"
- ✅ "How many Amex cards can I hold at once?"
- ❌ Anything asking whether a specific person can get a specific card's offer

---

## 5. Foundation Models is on-device only — no developer API for Apple's cloud LLM

**Status:** Platform limitation (not a Fleece bug)  
**Affected:** All builds using the Foundation Models framework

### Summary
The `Foundation Models` framework gives developers access exclusively to Apple's **on-device 3B-parameter model**. Apple's larger cloud-based models (used by Siri for complex system tasks) run on **Private Cloud Compute (PCC)** but Apple does not expose a public PCC API for third-party developers. If the device lacks Apple Intelligence hardware (pre-A17 Pro / pre-M1) or the user has Apple Intelligence disabled, the framework returns an error — there is no automatic cloud fallback.

### Implications for Fleece
The 3B on-device model handles simple retrieval well (wallet lookups, lounge access, transfer partners) but struggles with multi-step reasoning across several tool calls. Queries that require the model to combine results from `get_application_rules` + `get_point_valuations` in a single response are at the edge of what the model can reliably handle.

### Workarounds considered

| Option | Pros | Cons |
|---|---|---|
| **Tool-augmented on-device** (current) | Free, private, no user setup | 3B model; context window ~4K tokens |
| **BYOK cloud fallback** (OpenAI/Anthropic) | Powerful; user pays own tokens | User must generate and paste an API key; data leaves device |
| **App developer-paid cloud API** | Seamless UX | Cost at scale; App Review scrutiny |

### If a BYOK fallback is added later
1. Store the user's API key in **Keychain**, never `UserDefaults`.
2. Add a "Validate Key" button that fires a 1-token test call before saving.
3. Route complex requests to the cloud model when `SystemLanguageModel.default.isAvailable == false` or when the on-device model returns a safety error.
4. Declare data-sharing clearly in App Privacy labels.

---

## 6. Siri / App Intents integration not working

**Status:** Unresolved  
**Affected:** Physical device, iOS 26+  
**Implementation:** `AskFleeceIntent` + `FleeceShortcuts` in `Intents/AskFleeceIntent.swift`

### Symptom
Fleece does not appear in Settings → Siri & Search. Saying "Ask Fleece about my cards" to Siri does not invoke the intent.

### What was tried
| Attempt | Change | Result |
|---|---|---|
| 1 | Added `AskFleeceIntent: AppIntent` + `FleeceShortcuts: AppShortcutsProvider` | App not visible in Siri |
| 2 | Added `FleeceShortcuts.updateAppShortcutParameters()` to `FleeceApp.init()` | Still not working |

### Possible root causes (unverified)
- **Spotlight indexing delay** — App Shortcuts registration can take minutes to propagate after first launch; may need to wait longer or reboot the device.
- **Provisioning profile** — Some App Intents features (especially those that run out-of-process) may require specific capabilities in the provisioning profile used for the physical device build.
- **iOS 26 beta instability** — App Intents + Siri integration is known to be flaky in early iOS 26 betas; may resolve in later seeds.
- **`#if canImport(FoundationModels)` gate** — The intent's `perform()` body is conditionally compiled; if there's a compile-time mismatch the intent registers but always falls through to the "requires iOS 26" message, which Siri may suppress.

### Things to try if revisiting
1. Reboot the device after first launch and wait 5 minutes before testing with Siri.
2. Check **Settings → Siri & Search → Fleece** — if it appears but phrases don't trigger, the issue is phrase matching, not registration.
3. Test the intent directly via the **Shortcuts app** (add a shortcut manually) to verify `perform()` executes correctly before debugging Siri phrase registration.
4. Add `NSUserActivityTypes` to `Info.plist` if required by the specific iOS 26 build.

---

## 7. `xcodebuild` CLI fails with plugin error

**Status:** One-time fix required per machine  
**Error:** `xcodebuild failed to load a required plug-in`  

### Fix
Run once with sudo:
```bash
sudo xcodebuild -runFirstLaunch
```
