# Chat / Chatbot Feature — Discussion

Should Fleece iOS add a chat tab powered by Apple Foundation Models?

---

## The Pitch

The iOS app currently answers one question: *"What card should I use right now?"*

A chat tab would answer a different class of questions:
- *"Is the Amex Gold worth the $325 fee for my spending?"*
- *"Compare Chase Sapphire Reserve vs Preferred for someone who travels twice a year"*
- *"What's the best card to use at Costco?"*
- *"I spend $800/month on dining and $400 on groceries — what's my best wallet?"*

These are research questions, not real-time questions. The CLI already handles them (`fleece roi`, `fleece compare`, `fleece recommend`). A chat tab would bring that capability to iOS natively, powered entirely on-device via Foundation Models tool calling.

The `apple-foundation-models.md` doc has the full tool calling architecture ready to build on — four tools: `GetWalletCardsTool`, `LookupMCCTool`, `GetCardROITool`, and `UpdateSpendingProfileTool` (silently persists spend amounts to `UserDefaults` so the model never asks the same question twice).

---

## Arguments For

### 1. The infrastructure is already designed
`GetWalletCardsTool`, `GetNearbyPlacesTool`, and `GetCardROITool` (see `apple-foundation-models.md`) give the model real data. Unlike a naive GPT wrapper, it would never hallucinate card names or invent multipliers — every factual claim is grounded in live tool output.

### 2. Completely on-device and private
No API key, no OpenAI bill, no data leaving the device. That's a genuine differentiator — most financial chatbots send your spending data to external servers.

### 3. Covers the research gap
The Nearby tab answers *right now*. Chat answers *planning ahead*. They're complementary — users who add a card based on a chat recommendation will immediately benefit from the Nearby tab.

### 4. The Streamlit chatbot already validates demand
The existing `fleece.py` chatbot proves the conversational interface resonates. A native iOS version is the natural evolution.

---

## Arguments Against

### 1. Hard iOS 26 / Apple Intelligence requirement
`LanguageModelSession` requires iOS 26 and Apple Intelligence enabled on iPhone 15 Pro or later. As of mid-2026 that's a meaningful portion of the user base, but not everyone. On iOS 17–25 the tab would show a dead "requires Apple Intelligence" message — wasted real estate.

### 2. Without tool calling it's dangerous
A chatbot without grounded tools would hallucinate card details. If we ship chat without the tool calling layer, users would get confidently wrong answers about earning rates and fees — worse than no chatbot. This is a hard dependency, not optional polish.

### 3. Chat quality depends on model capability
The on-device model is smaller than GPT-4. For nuanced multi-card comparisons with complex tradeoffs it may give shallow answers. We can't fine-tune it. Quality ceiling is unknown until tested on real queries.

### 4. Adds a fourth tab
The current three-tab layout (Nearby / Wallet / Settings) is clean and purposeful. A fourth tab adds navigation weight. If chat is used rarely it would feel like bloat.

### 5. Support burden
Chat surfaces are hard to reason about. A buggy recommendation is a bad UX. A chatbot confidently giving wrong financial advice is a trust problem.

---

## Recommendation: Defer — Conditions to Revisit

**Don't build it now.** The core app is not yet on the App Store. A chatbot is a second-order feature. Shipping the Nearby + Wallet loop, getting real user feedback, and clearing the App Store are higher priorities.

**Revisit when:**
1. Apple Developer account is active and app is in TestFlight
2. We've tested `GetWalletCardsTool` + `GetCardROITool` manually against real queries
3. iOS 26 adoption is ≥ 40% of the user base (so the feature reaches most users, not a minority)
4. We have a clear answer for iOS 17–25 users: either a graceful fallback (static FAQ? link to CLI?) or a decision to gate the tab behind a version check

**If we do build it, the right shape is:**
- Fourth tab: "Ask" with a `bubble.left.and.bubble.right` icon
- On iOS 26 + AI enabled: full conversational interface with tool calling
- On iOS 17–25 or AI off: a static screen with the 5 most common questions answered as expandable cards (no LLM, just hardcoded answers)
- No OpenAI or external API — on-device only or nothing
- System prompt pre-loaded with the user's wallet and spending profile from Settings

---

## What the UI Would Look Like (if built)

```
┌─────────────────────────────────────┐
│  Ask Fleece                    ⋯    │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────────────────────┐    │
│  │ Is Amex Gold worth it for   │    │
│  │ $600/mo dining?             │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │ Yes. At $600/mo dining you  │    │  ← tool-grounded answer
│  │ earn ~$518/yr in MR points. │    │
│  │ Net after $325 fee: +$193.  │    │
│  └─────────────────────────────┘    │
│                                     │
│  ╔═════════════════════════════╗    │
│  ║ Ask about your cards...     ║    │
│  ╚═════════════════════════════╝    │
└─────────────────────────────────────┘
```
