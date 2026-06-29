# Channel Adaptations

How tone modulates per channel. **Voice never changes — only tone modulates.** Each channel has hard constraints (platform-imposed limits and format), tonal shifts (how the brand's voice expresses itself within those constraints), and prohibited registers.

Use these as the input to the tone modulation matrix in TONE.md, and as the per-channel `do`/`don't` lists.

---

## Table of contents

- [LinkedIn](#linkedin)
- [Twitter / X](#twitter--x)
- [Email (newsletter or transactional)](#email-newsletter-or-transactional)
- [Blog / Long-form essay](#blog--long-form-essay)
- [In-product UI](#in-product-ui)
- [TikTok](#tiktok)
- [Instagram](#instagram)
- [YouTube](#youtube)
- [Podcast](#podcast)
- [Press release](#press-release)
- [Support / Customer service](#support--customer-service)
- [Sales decks](#sales-decks)
- [Recruiting](#recruiting)
- [Disclaimer](#disclaimer)

> Platform hard constraints change frequently. Verify limits against the platform's official help docs at the time of writing; the figures below are approximate guides, not authoritative.

---

## LinkedIn

**Hard constraints:**

- Post body: ~3,000 characters (~500 words). Truncates at ~210 characters in feed with "see more".
- First 1-3 lines must hook (above the fold on mobile).
- Native paragraphs, no markdown rendering; line breaks shape readability.
- Supports unicode bold (better for copy-paste than markdown bold).
- Articles (long-form): ~125,000 characters.
- Comments: 1,250 characters.

**Tonal shift from voice baseline:**

- Dampen irreverence — LinkedIn's audience skews professional and risk-averse compared to Twitter/X.
- Lengthen sentences slightly; the medium tolerates more structure.
- Lead with results, not philosophy. ABT logic (And… But… Therefore…) outperforms narrative essays here.

**Do:**

- Reveal 80% in the hook (the result), keep 20% (the how) for the body — tension drives the scroll.
- Cite specific numbers, dates, costs.
- Format mobile-first: ≤2 visual lines per paragraph on phone.

**Don't:**

- Open with a rhetorical question — signals low confidence.
- Use "incontournable", "supercharge", "next-generation", "leverage" — LinkedIn buzzword fatigue is at saturation.
- Stack emojis or ternary structures (rule of three).

**Cross-reference:** for full LinkedIn ghostwriting workflow, see the `samber/cc-skills@linkedin-ghostwriting` skill.

---

## Twitter / X

**Hard constraints:**

- Single tweet: 280 characters (free) or up to 25,000 (Premium / X Premium+).
- Thread: chain tweets; first tweet is the hook, must work standalone.
- No markdown; line breaks count as characters.
- Quote tweets, replies, polls, media attachments.

**Tonal shift:**

- Sharpen and shorten. Twitter rewards punch over polish.
- Irreverence and wit travel further here than on LinkedIn — within the brand's archetype tolerance.
- Trade nuance for brevity; reserve nuance for thread structure.

**Do:**

- Lead with the verb when possible — "Shipped X." beats "We have shipped X today."
- Use threads for narrative; reserve single tweets for one-shot insight.
- Time-stamp claims when freshness matters ("As of this week...").

**Don't:**

- Quote-tweet your own promotional copy with a fake-naive caption — reads as inauthentic.
- Use vague hooks ("Hot take 🔥"). Specificity beats teasing.
- Abuse 🧵 as a hook — readers have learned to scroll past.

---

## Email (newsletter or transactional)

**Hard constraints:**

- **Subject line:** 30-50 characters before truncation on mobile (Gmail iOS: ~33 chars; Apple Mail iPhone: ~35-41).
- **Preheader:** 40-100 characters (Gmail desktop: ~110; mobile: ~30-50).
- **From-name** matters more than from-address for opens — a real human's name often outperforms a brand name.
- HTML and plain-text alternatives both rendered; some clients block remote images by default.

**Tonal shift:**

- **Newsletter:** voice baseline + structure (header, sections, single CTA).
- **Transactional:** functional first; flourish moves to onboarding/lifecycle.
- Active voice; lead with action; one primary CTA.

**Do:**

- Match the from-name to the relationship (founder for nurture, `support@brand.com` for transactional).
- Mirror the subject line in the preheader (don't repeat it).
- Test on mobile — most opens happen there.

**Don't:**

- Tease in the subject line, deliver in the body (clickbait subjects tank long-term open rates).
- Use marketing language in transactional copy (payment confirmations, password resets) — wrong register destroys trust.
- Hide the CTA below a wall of text.

**Cross-reference:** for Substack-specific workflows, see the `samber/cc-skills@substack-ghostwriting` skill.

---

## Blog / Long-form essay

**Hard constraints:**

- No platform-imposed length cap; reader attention is the cap.
- Markdown supported (most CMS); H2/H3 structure affects SEO and scanability.
- Above-the-fold copy carries most of the engagement load.

**Tonal shift:**

- Voice baseline + room to breathe. Long-form tolerates more nuance, longer sentences, more digression.
- Lead with the thesis; don't bury the lede.

**Do:**

- Use H2/H3 to make scanning useful — readers skim before they commit.
- One idea per paragraph (most paragraphs ≤4 sentences).
- Quote sources inline with attribution.

**Don't:**

- Open with a dictionary definition (cliché, reads as filler).
- Use "in conclusion" — write a conclusion that doesn't need announcing.
- Pad with framing throat-clearing ("Let me start by saying...").

**Cross-reference:** for technical articles specifically, see the `samber/cc-skills@technical-article-writer` skill.

---

## In-product UI

**Hard constraints:**

- Button labels: ~24 characters (most design systems).
- Empty states, error messages, confirmation dialogs: each has its own micro-format.
- Accessibility: WCAG 2.1 AA requires plain language; screen readers parse alt text and aria-labels.
- Localisation: every string lands in a translation memory; idioms and contractions don't travel.

**Tonal shift:**

- **Functional first.** Flourish is permitted in empty states and onboarding; transactional flows (payment, security, account suspension) strip all flourish.
- Use the user's data when available ("Your card ending in 4242 was charged $12.00") instead of generic confirmations.

**Do:**

- Action-first verbs in button labels ("Save", "Continue", "Cancel" — not "Click here").
- Match the error message to the user's action ("Update your card to keep your subscription" — not "An error occurred").
- One idea per microcopy unit; one decision per dialog.

**Don't:**

- Use brand-voice mascot humour in payment-failure or security-warning flows.
- Use marketing language ("Awesome!", "Yay!") in transactional confirmations.
- Use idioms that won't translate ("hit the ground running", "easy as pie").

**Reference:** Nielsen Norman Group's error-message walkthrough is the canonical teaching case.

---

## TikTok

**Hard constraints:**

- Video length: up to 10 minutes; sweet spot 15-60 seconds.
- Caption: ~2,200 characters; first ~80 characters visible before truncation.
- Native-feel beats produced-feel.
- Trend cycles measured in days.

**Tonal shift:**

- Cadence-led. Voice expresses through rhythm of cuts, on-screen text, and audio choice — not only through written caption.
- Irreverence travels furthest here. Even traditionally polished brands (Duolingo, Ryanair) lean Jester on this channel.
- Native register: trending sounds, lo-fi production, direct address.

**Do:**

- Capture attention in the first 2 seconds.
- On-screen text reinforces (doesn't repeat) audio.
- Reply to comments with video (TikTok rewards engagement loops).

**Don't:**

- Repurpose 16:9 horizontal video without re-cropping — reads as inauthentic.
- Force corporate tone onto trending audio — audiences detect it instantly.
- Over-edit. Native = trust on TikTok.

---

## Instagram

**Hard constraints:**

- Feed caption: 2,200 characters; first ~125 visible before "more".
- Stories: 24h ephemeral, multiple formats (poll, quiz, question sticker, link sticker).
- Reels: video up to 90s (some accounts 15 min); algorithm prefers vertical, original audio.
- Hashtags: 30 max in caption, 3-5 typically optimal.

**Tonal shift:**

- Visual-first; copy supports the image, not vice versa.
- Stories tolerate higher-frequency, lower-polish voice (closer to founder voice for personal brands).
- Reels follow TikTok-like cadence but skew slightly more polished and demographically older.

**Do:**

- Hook in the first line of the caption (above the "more" cutoff).
- Match copy register to image — branded studio shots take polished copy; behind-the-scenes Stories take casual copy.
- Use Story polls and questions to generate UGC and feedback loops.

**Don't:**

- Use a single voice across feed + Stories + Reels — each surface tolerates a different register.
- Cross-post Twitter copy verbatim — Instagram audience skews different.

---

## YouTube

**Hard constraints:**

- Title: 100 characters; truncated to ~70 in suggestions.
- Description: 5,000 characters; first 100-150 visible above fold.
- Tags: 500 characters total.
- Chapters: enabled when description contains timestamps.

**Tonal shift:**

- **Long-form video (10+ min):** voice baseline + presenter style. Scripts tolerate more nuance and digression.
- **Shorts (<60s):** TikTok-like cadence.
- Title and thumbnail carry click-through; description carries SEO + retention nudges.

**Do:**

- Hook in the first 15 seconds (retention drops fastest there).
- Use chapters for searchability.
- Match title to thumbnail message — mismatch tanks click-through.

**Don't:**

- Clickbait titles that don't pay off in the first 60 seconds — algorithm penalises drop-off.
- Use marketing-deck language in the script — viewers detect "ad mode" instantly.

---

## Podcast

**Hard constraints:**

- Episode length: 20-90 min typical; algorithm-agnostic medium.
- Show notes: long-form, SEO-relevant, hosted on podcast platforms.
- Audio-only (most episodes) — no visual scaffolding.

**Tonal shift:**

- Conversational voice baseline; scripts that sound written fail.
- Hosts carry voice. Show voice = host voice + production conventions (intro/outro music, segment names, ad reads).

**Do:**

- Write the script for ear, not for eye. Read aloud before recording.
- Segment names and recurring phrases become voice markers over time.
- Ad reads in host voice outperform polished agency reads.

**Don't:**

- Read marketing copy on-air verbatim — register mismatch is jarring.
- Over-edit out conversational pauses — they're part of trust-building.

---

## Press release

**Hard constraints:**

- Headline: ~70 characters for wire-service truncation.
- Boilerplate at the end is fixed.
- Embargo language is conventional ("Under embargo until X").
- AP / Reuters style preferred by wire services and journalists.

**Tonal shift:**

- **Most formal register the brand uses externally.** Voice baseline + journalist-readable conventions.
- Lead with the news, not the opinion.
- Quotes carry the editorial voice; surrounding prose carries the factual voice.

**Do:**

- Inverted pyramid: most important fact first.
- Attribute quotes to a named person with title.
- Include contact details and embargo language explicitly.

**Don't:**

- Use marketing superlatives in the lede ("the most innovative... ever") — journalists strip them.
- Open with a quote.
- Write the headline last — write it first to discipline the lede.

**Cross-reference:** see the `samber/cc-skills@press-release-writer` skill.

---

## Support / Customer service

**Tonal shift:**

- Voice baseline + empathy + outcome-orientation.
- Acknowledge the issue, name the next step, close the loop.

**Do:**

- Start with the customer's named issue: "Your invoice failed because..."
- Offer a concrete next step in every reply.
- Match formality to the customer's own message.

**Don't:**

- Open with "Sorry for the inconvenience" — saturated phrase, reads as scripted.
- Use legal-team passive constructions ("It has been determined that...").
- Forward without context — the next agent inherits the customer's frustration if the handoff is silent.

---

## Sales decks

**Tonal shift:**

- Voice baseline + structured argument. Slides tolerate less nuance than long-form.
- Lead each slide with a claim, support with evidence underneath.

**Do:**

- One claim per slide, in the title.
- Concrete numbers in the title where possible ("Reduced churn 34% in Q3" beats "Better retention").
- Speaker notes carry the nuance; slides carry the headline.

**Don't:**

- Write slides as paragraphs.
- Use clip-art-grade icons or stock photos that contradict the brand visual register (this is a DESIGN.md concern, but voice and visuals are read together).

---

## Recruiting

**Tonal shift:**

- Voice baseline + candidate-empathy + concrete role specificity.
- Job descriptions are content, not HR forms — write them with the same care as marketing copy.

**Do:**

- Lead with what the candidate will _do_, not the company's mission.
- Be specific about the team, the manager's style, and the work.
- State compensation ranges where legally required and culturally expected.

**Don't:**

- "Rockstar", "ninja", "wizard" — these are signals to senior candidates that the role is overstuffed and the culture is immature.
- Bury the disqualifying requirements at the bottom — candidates resent finding them after writing a cover letter.
- Use boilerplate inclusion statements without backing them up in the application process.

---

## Disclaimer

Platform character limits, supported formatting, and algorithm behaviours change frequently. Treat the numbers above as approximate guides — verify against each platform's current help documentation before committing to a specific limit in TONE.md.

Trend cycles on TikTok, Instagram, and Twitter/X are measured in days or weeks. The tonal-shift guidance is more stable than the platform mechanics, but voice norms on social channels do drift over time. Audit channel-specific sections of TONE.md quarterly.
