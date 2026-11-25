# Graham's editing preferences (from real feedback)

These are the calls Graham made across three projects. The reason matters more than the rule: apply the reasoning to new situations.

## Visual identity
- **Style source: the OpenClaw Foundation announcement image** (`assets/style-reference.png`): a Michelangelo-style "Creation of Adam" with a lobster claw reaching toward a human finger, an ember spark between them, a near-black cracked-fresco background, lobster red and bone. His words: the claw-and-hand "doesn't have to be that exact image, it just has to be that style of imagery." Reuse the motifs (claw, spark, fresco, engraved bone linework, warm embers), never a copy of the image.
- **Drawn in code, not generated.** When offered AI image generation that spends his Figma credits, he chose procedural. Don't spend paid credits without asking. The procedural look has been accepted on every project since.
- **His old house style** (Avenir/Helvetica white block type on black, cartoon red lobster mascot, plain white name tags) is what gets replaced. When a video arrives with those burned in, swap them for the new style. Look for a clean source first.

## Title card
- Keep **his exact title wording**. If his video already has a title ("What is OpenClaw Enterprise and why does it matter"), reuse it. For updates: kicker "OPENCLAW <version>", title "OpenClaw Update", sub "and other features you should know" or a close variant.
- Layout: the claw slides in from the left toward a spark at center top; Baskerville title below. It's an opaque card that dissolves into the footage as speech begins, and it's silent underneath.

## End card
- **Only "OpenClaw Foundation."** He explicitly removed "Welcome to the age of the lobster" and the "openclaw.ai" line: "Don't do that. Just say OpenClaw Foundation." The claw and spark stay. It dissolves in over the last ~0.3 s of footage and fades to black.

## Cutting raw footage (release shorts)
- **Cut personal preamble; start on substance.** For 9.9 he had the opening ("it's been about 30 days since I joined OpenClaw… big release today") removed so the video starts at "There's been a lot of new stuff…". Get to the point.
- **Choose the cleanest complete take** of each line from a multi-take recording. Skip false starts, stretched words, repeated attempts, off-topic asides (the dog break), and wrong words (he said "Mac 10.1" in one close; use the take without it).
- **Group related features into one quick run.** For 10.1 he wanted "the part where I say there's a few features that kind of all go together" to cover everything except the Mac update, strung together "as one quick thing", with the Mac update last. Build such runs by splicing a list across takes at a natural comma pause. Cover it with one full-screen list card where each feature lights up as it's named. That also hides the splice and any look-down-at-notes moments.
- **Shorts stay short**, around 30–40 s. One list card beats a card per feature.
- Use full-screen cards to **cover bad picture moments** (looking away, reading notes) when the audio is the best take.

## Interviews / already-edited videos
- Don't re-cut his edit. Add:
  - **Name tags** per person, inside each person's half of a split screen, timed to when each is introduced. Use their real roles from the conversation, and flag anything you inferred (the old tag said "MOTS OpenAI"; we used "Leads OpenClaw Enterprise" from what Kevin said).
  - **Section overlays**, about every 1–3 minutes at topic changes: "01 · SHOW NAME" kicker plus a short title, centered at the bottom. He specifically said section *overlays*, not section *cards*.
  - **Animated explainers** only over "really particularly illustrative sections": architecture, comparisons, lists, before/after. Time each element to the word. Keep each to about 15–35 s, and report the total cutaway time (about 3 min of 22 was accepted).
  - A closing "Get involved" overlay when they mention how to join.
- If he asks "can't you just add them all?", he usually means he wants one finished file. Make sure the deliverable has everything composited, and say so clearly.

## Captions, wording, and accuracy
- Lower thirds and cards should **paraphrase what the speaker actually says**. When you write a subtitle he didn't say ("Even easier to get started on a Mac"), list it in your report so he can veto it.
- **Don't print things you're unsure of.** Whisper turned two model names into "6.1 Soul / 5.5 Haiku", so the card said "New Model Support" and the report asked for the real names. Common Whisper mishearings on this content:
  - OpenClaw → "OpenCloud"
  - Red Hat → "GideHat"
  - Anthropic → "entropic"
  - OpenShell → "OpenShall"
  - claws → "clause"
  - SPIFFE/SPIRE → "Spiffy, Spire"
  - "conversation snooze" → "conversations news"
  - "called" → "color"
- Spell names the way his notes do (he spells it "Vyctor").

## Delivery
- **Show him the file.** After every render, give the full path in plain words. He has asked "where's the video?" and "show me the file" every time. On a Mac GUI session, also `open -R` it in Finder.
- **New version each change** (v1 → v2 → v3); leave earlier versions alone and mention which is current.
- A short README with a placement table in `Motion Graphics/`, so he can rebuild it in his own editor.
- **Thumbnail:** when he supplies one, make a 1920×1080 copy (`thumbnail.png` and `.jpg`), hold it as the first 1 s (sites like X, LinkedIn and Slack preview the first frame), and embed it as cover art. Remind him YouTube needs a separate thumbnail upload.
- After the video, offer the **YouTube description with chapters, an X post plus optional thread, and a LinkedIn post** (see `social-copy.md`). He asked for all three for the Enterprise interview.

## Communication
- He speaks casually and briefly. Answer in plain language: what you did, where the file is, and what to check. Skip the internals unless asked.
- Status lines during long renders ("rendering in the background, about 20 min") are welcome. Don't go quiet for long stretches.
