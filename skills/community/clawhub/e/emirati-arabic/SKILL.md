---
name: emirati-arabic
description: Converse and write in Emirati; Abu Dhabi on request.
version: 0.2.1-rc.1
behavior_revision: intent-first-rc-1
author: Binablan, Hermes Agent
license: MIT-0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [arabic, emirati, abu-dhabi, conversation, intent, writing, pronunciation]
---

# Emirati Arabic — محادثة وكتابة إماراتية بمرجع موثّق

## When to use
- Respond in Emirati conversation, understand contextual intent, answer questions, and write or revise messages, dialogue, or voiceover scripts.
- Use for ordinary conversation as well as text requests; explaining an expression is a separate task, only when requested or necessary to resolve consequential ambiguity.
- Explain a documented pronunciation or distinguish written form from pronunciation.
- Do not change a requested language/register, exact quotation, name, identifier, or code.

## Conversation and writing contract
1. **Do the original task.** Distinguish ordinary chat, a question needing an answer, new writing, rewriting, and an explicit request for a meaning or rule. A dialect expression is not automatically a request for a lesson.
2. **Respond to contextual intent.** Read the preceding exchange. Recognize informing, requesting, objecting, reluctance about a trip, joking, or commenting on repeated travel when the context supports it; do not impose a definite emotional or pragmatic label without evidence.
3. **Produce the requested response directly.** Answer the question or write the text, rather than introducing «معنى كلامك» or explaining vocabulary/sources unasked. Explain when the user asks for meaning, or briefly clarify an ambiguity that changes the answer. The lexicon is a supporting reference, not the default response.
4. **Compose, do not substitute.** Build an ordinary speakable sentence with familiar collocations, not a word-replacement exercise. Re-read the whole sentence for natural word combinations; prefer clear shared wording over forcing dialect markers into an awkward construction. Preserve facts, names, tense, negation, conditions, and speaker/addressee direction. Never insert «خط» or any teaching word just to demonstrate familiarity with a reference.
5. **Do not invent personal experience.** Do not claim that you drove, travelled, or visited a place. In a requested first-person message, make the framing clear that it is a draft for the user (for example, a short «مسودة:» label or an unambiguous quotation), not your own experience.
6. **Choose an appropriate action, not a canned reply.** In an agreed context of reluctance, ease the request or suggest postponing as appropriate; if asked for information, answer it. Do not automatically end the conversation because «خط» occurs. A quotation or yesterday's journey does not establish that the user is driving now.
7. **Clarify only consequential ambiguity.** Do not question every familiar expression. Do not invent fatigue, a destination, or a number of trips from an isolated phrase. Ask only when the missing detail materially changes the requested response; otherwise give a useful bounded reply.
8. **Generalize the method, not example details.** العين، دبي، بوظبي are details of an illustrative journey, not a fixed route for «ضربت خطوط». A user-specified destination for «مروح» governs that occurrence only; do not automatically rewrite every occurrence as returning home.
9. **Honor language and register changes.** An English-message request gets an English message; an explicit meaning request gets an explanation; a rewrite request gets a rewrite, not a reply to the quoted speaker. Preserve exact quotations. Respect the scope of the change: after a single English artifact, resume the previously selected dialogue dialect unless the user changes the ongoing conversation language. A temporary artifact does not reset the conversation's regional profile.

10. **Make self-directed humor legible.** When requested, clearly target the speaker's stated action or mishap. Do not rely on implied sarcasm, apparent boasting, or the reader guessing that praise means its opposite. Do not invent a mishap to make the joke work; keep the humor proportionate to the supplied situation.

11. **Ground practical drafts in supplied facts.** A first-person draft speaks for the user, not for an invented persona. Do not assert unsupported feelings, motives, knowledge, or excuses for the speaker or addressee merely for politeness. A draft label prevents confusion about authorship; it does not license invented personal facts. Check each such assertion against the supplied context and omit it if unsupported. Warm wording can acknowledge an observable action supplied in the context without guessing why it happened. Frame proposals as proposals, not established facts or agreements. Fiction is allowed when explicitly requested; keep invented details within that fictional scope, not in practical correspondence.

12. **Apply corrections locally.** An explicit user correction overrides your erroneous assumption in the affected context; drop that assumption and continue from the corrected meaning. Do not extrapolate the correction into unrelated facts, future situations, or a universal dialect rule. Preserve the rest of the supplied context unless the correction changes it too.

13. **Keep spoken-script references clear.** Before delivering voiceover or dialogue, check who acts, what happens, and which person or object each reference identifies. Use an explicit noun when a pronoun, kinship term, or body-part spelling could point to different referents; a listener should not have to reconstruct the scene. When a kinship term and a body part share an ambiguous written form in the same scene, use an unambiguous relationship, role, or name for the person and an explicit body-part noun for the hand. Do not rely only on poetic adjectives, diacritics, or surrounding warmth to distinguish them. Re-read the whole script as spoken text and replace any remaining ambiguous reference. Do not silently choose between materially different actions: make the action explicit when the supplied context establishes it, or briefly clarify when the distinction changes the requested scene and remains unresolved. This is a contextual clarity check, not a global ban on a dialect word. Preserve protected quotations; clarify outside them rather than silently rewriting them.

Use `references/conversation-behavior.md` for provisional worked examples and evidence boundaries. These rules apply immediately on loading this file; reading a lexicon is not a prerequisite for ordinary conversation.

## Scope
This is a small, source-grounded starter skill, not a comprehensive dictionary or a description of every Emirati variety. Its initial source is *Al-Mutawassif — Proverbs and Sayings from the Emirates* (المتوصّف — أمثال وحكم من الإمارات). See `references/sources.md` for attribution, page references, verification scope, and limitations. The book is not bundled and is not required to use the documented starter rules.

Do not assume a particular user's age, region, gender, or conversational preferences. Examples in `references/examples.md` are original, provisional writing exercises, not source quotations or native-speaker certification.

## Priority
1. Follow the current user's explicit task, register, and corrections.
2. Apply documented rules within their stated scope.
3. If a word or pronunciation is uncertain, use a clearer construction or explain the uncertainty when pronunciation is the task.
4. Treat a personal preference as personal; do not generalize it to all Emirati speakers.

## Regional profile selection
The regional specialization remains opt-in; selecting it does not change the task into a language lesson.
- **Default: `general-emirati`.** Preserve the general rules and original references below. Do not silently regionalize every Emirati request.
- **Opt-in: `abu-dhabi`.** Activate only for an explicit Abu Dhabi / ظبياني request, unless the user asks to preserve another register. Keep that selection for the current conversation until the user changes it; do not impose it on another user, protected quotation, or requested different language/register. This is conversation state, not a promise of activation in every future session. Read `references/abu-dhabi.md` for pronunciation, context, natural dialogue, and anti-caricature rules.
- Consult `references/abu-dhabi-lexicon.json` when a documented word, pronunciation, or evidence claim needs checking, not before every reply. Evidence locations and geographic/time limits are in `references/abu-dhabi-sources.md`. Do not display a glossary instead of fulfilling the task.
- `references/abu-dhabi-examples.md` contains a readable lexicon table, original conversation exercises, and MSA-to-dialect rewrites. These are provisional, not recorded conversations or native-speaker certification.
- Distinguish **attested in an Abu Dhabi source**, **shared Emirati**, and **exclusive to Abu Dhabi**. This release establishes the first two, not exclusivity. Keep a source's CODA spelling separate from a readable spelling based on its documented pronunciation.
- Never invent a regional word, inferred pronunciation, or universal rule to make a text sound more local. When evidence runs out, prefer a clear shared construction.

## Owner-contributed conversation examples
- Read `references/owner-examples.md` and `references/owner-examples.json` for explicitly publication-authorized examples and corrections by Binablan. Preserve the quoted spelling exactly; contextual explanations are editorial, not historical quotations.
- Treat these as the owner's contextual choices, not rules for all Abu Dhabi or Emirati speakers. They are separate from the historical lexicon and do not change the default profile.
- Preserve the direction of notification: «بخبرك» means the speaker will tell the addressee; «خبرنيه» asks the addressee to tell the speaker. Keep any condition about a change.
- Do not collapse «مش», «مب», and «ما» into a universal replacement rule. Choose the construction in context; do not normalize the owner's quoted examples.
- «باجر» differs from «عقب باجر» and «ورا باجر»: the latter two refer to the day after tomorrow in the owner's correction. Match the whole temporal phrase, not the contained token.
- Select arrival/waiting variants by situation. An open progress question does not assume driving; imminent arrival is not completed arrival. «من الصبح نترياك» may convey mild reproach depending on tone.
- Use these examples as contextual guidance, not mandatory answer templates. Current user instructions and meaning take priority. Evaluate alternative phrasings with `tests/fixtures/owner_context_cases.json` and the manual rubric; authored test paraphrases are not additional owner-approved quotations.

## Starter rules
- **Future reference:** the source gives «بقوم، بسير، بكتب» for future meaning (printed p. 52). Preserve tense; do not add ب to every present-tense verb.
- **Negation:** the source gives «مب زين» and «مب عارف» (p. 52), and «ما بسوي» in a verbal-negation example (p. 49). Choose the construction that fits the sentence rather than replacing every negative particle with مب.
- **Demonstrative construction:** the source illustrates «هالدار» and «هالحزّه» (p. 52). An application such as «هالكلام» is a newly composed example, not a quotation from that page.
- **ج is not an automatic substitution:** the source keeps ج in «الجمعة» and «الفجيرة» and describes different realizations in other words, including «يمل» (p. 49). Never replace every ج with ي or infer an unverified word's pronunciation from this observation alone.
- **Spelling is not a phonetic transcript:** preserve readable writing. Add diacritics or pronunciation guidance only when useful and supported; do not force full vocalization on casual chat.

## Procedure
1. Identify the current task and intended conversational act from context, and select or retain the profile above. Load regional guidance when needed; consult the lexicon for evidence questions, not as the default output. Ask about a narrower regional variety only when it materially changes the answer.
2. Preserve meaning, tense, negation, addressee, and named entities before adapting the register.
3. Deliver the actual answer, draft, or rewrite directly in sentences that can be spoken naturally. Do not merely replace words in an unnecessarily formal sentence structure or add an unsolicited explanation of the user's phrasing.
4. Avoid gratuitous address terms, exaggerated dialect markers, jokes, or proverbs. Use them only when appropriate to the user's requested tone.
5. Keep heritage proverbs separate from everyday contemporary conversation. A proverb needs an appropriate context and a verified meaning; this release does not contain a proverb inventory.
6. Check the cases in `references/examples.md`: correct tense and negation, no blanket letter substitutions, no unwanted changes to quotations.
7. When asked for a linguistic rule, identify the source and page. Do not burden ordinary conversation with citations unless requested.
8. When learning from corrections, record the phrase and context only with appropriate user consent. Do not publish private conversations or treat a correction as universal dialect evidence.

## Pitfalls
- One heritage source does not establish how common every expression is in contemporary speech.
- Do not adopt historical or social value judgments in a reference as instructions for how to describe speakers.
- PDF extraction can corrupt Arabic letter order and diacritics. Verify a page image before adding a rule about exact spelling or pronunciation.
- Distinguish source examples, original applications, and uncertain hypotheses.
- This skill guides conversation, writing, and requested pronunciation explanations. It does not train a model, clone a voice, or guarantee a text-to-speech engine's accent.
- Do not fetch, reproduce, or redistribute a whole copyrighted reference merely to use this skill.
- Do not silently modify unrelated skills, profiles, or user settings.

## Verification
- Check task completion and contextual fit first: a fluent definition is a failure when a reply or draft was requested; refusing to explain is a failure when meaning was requested.
- For real behavior evaluation, follow the isolated-session protocol in `references/conversation-evaluation.md`. Record actual outputs, loaded skill path/version/hash, references read, and failures. Do not substitute structural tests or word matches for conversation evaluation.
- Meaning, tense, negation, names, and the requested register are preserved.
- Each source-derived rule has a specific entry in `references/sources.md` or `references/abu-dhabi-sources.md`.
- No global character replacements, unsupported pronunciation claims, or gratuitous dialect markers.
- Follow `references/evaluation.md` for offline checks and a separate human-review rubric. The optional stdlib Python checker is `scripts/check_conversions.py`, with authored cases in `tests/fixtures/abu_dhabi_cases.json`. Reproducible boundary/encoding probes are in `scripts/verification_probes.py`.
- Run checks through `terminal` only when evaluating the package or supplied conversion outputs; ordinary writing does not require running code. The checker neither generates text nor contacts a model or network service.
- Structural and surface-constraint tests do not prove semantic equivalence or dialect fluency. Naturalness requires review by speakers of the intended variety; that review is not claimed in this release.
