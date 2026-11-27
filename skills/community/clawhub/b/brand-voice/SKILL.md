---
name: brand-voice
description: Define, document and enforce a consistent brand or creator voice for social media, video and marketing copy. Builds a voice guide (personality, tone dials, vocabulary, do and don't examples) from interviews and real writing samples, measures writing habits with a script, rewrites drafts in that voice, audits existing content for consistency, and adapts tone per platform, audience and situation, including Roman Urdu, Urdu, Hinglish and English. Use this skill whenever the user wants a brand voice, tone of voice, voice guide, "sounds like me" writing, consistent captions or scripts, to rewrite text in their style, to check whether content matches their brand, or says "build my brand voice", "my tone", "style guide", even if they never say "voice".
---

# Brand voice

Turns "how we sound" from a feeling into a short guide plus a few measurable habits, so every post, script and reply sounds like the same person or brand. Replies follow the user's language preference; the voice guide is written in the language(s) the brand publishes in.

## Principles

- Base the voice on evidence: the user's real posts, emails, scripts, replies, plus an interview. Do not invent a personality from the industry.
- The goal is recognisable and useful, not clever. A voice that cannot be followed by someone else on the team is not finished.
- Never imitate a named real person or copy a competitor's voice. Use competitors for contrast only ("we are less formal than X").
- Measured numbers describe habits only; humour, warmth and taste need a human read.
- Keep the guide short (1 to 2 pages) so it gets used.

## Workflow

1. **Intake.** Brand or person, audience, languages (English, Roman Urdu, Urdu script, Hinglish, mix), platforms, goals, what the brand sells or stands for, 3 brands they admire and why, 3 they do not want to sound like, words they love or hate, topics to avoid. Ask only for missing items. If samples exist, ask for at least 10 posts (1,000+ words); say that fewer gives a rough sketch.
2. **Measure.** Put samples in text files (posts separated by a line with `---`) and run `python scripts/voice_tools.py profile samples.txt --out profile.json`. Read it with the numbers in mind: sentence length, emoji and hashtag habits, questions and exclamations, openers, signature phrases, Roman Urdu share. Note what the numbers cannot show.
3. **Interpret.** Pick 3 to 5 personality traits, each as "X, but not Y" (for example "direct, but not blunt"), with evidence from the samples. Set tone dials (formal to casual, serious to playful, reserved to enthusiastic, technical to plain) as positions with a one-line example. See `references/voice-guide-template.md`.
4. **Write the guide.** Use the template: voice summary, traits, dials, language rules (which language when, how Roman Urdu is spelled, code-switching rules), vocabulary (use, avoid, banned), sentence and format habits, platform shifts, emoji and hashtag rules, situation tones (launch, complaint, apology, crisis, sensitive topics), 6 before-and-after examples, and a "sounds like us" checklist. Put it in a doc if the session offers a docs type; otherwise markdown.
5. **Rules file.** Turn the hard rules into `rules.json` (banned, preferred replacements, must-include terms, limits) so drafts can be checked mechanically.
6. **Apply.** Rewrite or draft in the voice, keep facts unchanged, and show a short list of what changed and why. Run `python scripts/voice_tools.py check draft.txt --profile profile.json --rules rules.json` before delivering and fix real issues.
7. **Audit (optional).** Check 10 to 20 recent posts against the guide: score each trait 1 to 5 with a quote, list the drifts and the fixes, and say which posts feel most "on voice".
8. **Maintain.** Suggest a review every quarter or after a rebrand; add new good examples to the guide; record decisions (for example "we no longer use emoji in LinkedIn posts").

## Commands

```bash
python scripts/voice_tools.py profile FILE [FILE ...] [--out profile.json]
python scripts/voice_tools.py check DRAFT.txt [--profile profile.json] [--rules rules.json] [--strict] [--json out.json]
python scripts/voice_tools.py cliches
```

Standard library only. The built-in list flags stock phrases that often make text read as machine-written (for example "game-changer", "unlock your", "delve into"); treat them as prompts to be specific, not as a ban.

## Language notes

- Roman Urdu and Hinglish have no standard spelling. Choose one spelling for each common word in the guide (for example the words for "no", "is" and the polite "you") and keep it.
- Decide the mix: for example English for product terms and numbers, Roman Urdu for explanation and warmth. Write examples of both.
- Right-to-left Urdu script needs separate checks of line breaks and punctuation. The profile tool measures Roman-script text best.
- Do not claim a regional dialect, slang or humour is "right" for an audience without evidence from the user's samples or audience.

## Rules

- Do not fabricate testimonials, quotes or customer stories to make copy sound human.
- Do not write the user's voice to deceive people about who wrote something where that matters (for example impersonating a person in a private conversation). Brand copy and ghostwriting for the user's own accounts are fine.
- Keep claims accurate; voice never overrides facts, legal notices or required disclosures.
- Sensitive situations (apologies, safety, health, money, grief) get a plain, careful tone even when the brand is playful.

## References

- `references/voice-guide-template.md`: the guide template, tone-dial scale, before-and-after format, situation tones, rewrite checklist.
- `references/extraction-method.md`: how to gather and read samples, interview questions, interpreting the profile numbers, audit scoring.
