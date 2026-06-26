# Prompt 3: App Update Release Notes

Copy and paste this prompt into Claude. Replace all [BRACKETED] fields with your update details.

---

```
You are an ASO expert writing app update release notes. Generate release notes for the following update. The goal: make users excited to update, not ignore the notification.

App Details:
- App name: [APP_NAME]
- Version: [VERSION_NUMBER — e.g., 2.1.0]
- Changes this update:
  [LIST_EACH_CHANGE — bullet points OK here; be specific: "Fixed crash when switching tabs", "Added dark mode", "New widget for home screen"]
- Tone: [TONE — friendly / professional / playful / minimal]
- Top 1-2 user-facing improvements (most impactful for users): [HIGHLIGHT_1], [HIGHLIGHT_2]

---

Generate the following:

**iOS WHAT'S NEW** (max 4,000 characters — but 100-300 words is the sweet spot; long notes rarely get read)

Version [VERSION_NUMBER]

[Opening line: lead with the single most impactful user-facing change. Write from the user's perspective, not the developer's. "App no longer crashes when you switch tabs" not "Fixed null pointer exception in TabController."]

[Changes — benefit-framed, not technical. Format as a tight list or short paragraphs. Each item should pass the "so what?" test — why does the user care?]

Examples of bad → good framing:
- BAD: "Refactored authentication module"
- GOOD: "Logging in is now 40% faster"
- BAD: "Fixed memory leak in image loader"
- GOOD: "Images load faster and the app uses less battery"
- BAD: "Updated third-party dependencies"
- GOOD: [Don't mention this — users don't care]

[Optional closing: 1 line thank-you or tease of what's coming next]

Character count: X/4,000

**ANDROID WHAT'S NEW** (max 500 characters — extremely tight; pick the top 3 changes only and compress)
[500-char version]
Character count: X/500

**A/B OPENING LINE VARIANTS** (test these — the opening line determines if users read the rest)
1. [opening variant A] — angle: user-benefit ("You asked for X, here it is")
2. [opening variant B] — angle: social proof ("Based on your feedback...")
3. [opening variant C] — angle: problem-solved ("No more [frustrating thing]")

**PUSH NOTIFICATION TEXT** (for update available notification — optional, if app sends update prompts)
- Short (40 chars): [text] (X/40)
- Long (100 chars): [text] (X/100)

**INTERNAL RELEASE NOTES** (for your team, testers, or changelog.md — technical detail is fine here)
Version [VERSION_NUMBER] — [DATE]

**Added:**
- [Technical detail]

**Fixed:**
- [Technical detail]

**Changed:**
- [Technical detail]

**Removed:**
- [Technical detail, if any]

**Known issues:**
- [List any known bugs shipping in this version]
```

---

## Why Release Notes Matter for ASO

- **Keyword opportunity:** Apple and Google index "What's New" text. Each update is a chance to introduce new keywords naturally.
- **User trust:** Detailed, user-friendly release notes → higher update rates → more active users → better rankings.
- **Review trigger timing:** Well-framed updates that fix user-reported bugs = perfect moment to request a review. "You reported X — we fixed it. Loving the app? Leave us a review." 
- **Update rate signal:** High update rates are a positive signal in both App Store and Google Play ranking algorithms.
