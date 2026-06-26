# Editorial Judgment Reference

## Status

This is no longer treated as a standalone OpenClaw skill.

It is now an internal reference used by the main `daily-gift` skill during the editorial judgment stage.

## Role

Help the main skill decide:

1. Whether a gift should be sent.
2. What delivery weight the gift should have.
3. What narrative role the gift should serve.
4. Whether the gift should proceed into visual strategy and final rendering, whether that means H5, image, video, text, or text-play output.

This reference should guide judgment, not replace it. The final decision must still be made in context by OpenClaw after considering `soul.md`, `UserMD`, prior memory, recent gifts, and today's actual interaction.

## Core Inputs

- trigger context such as onboarding, daily run, manual request, or anniversary
- today's conversation summary
- relevant long-term memory when needed
- user preference profile
- recent gift history
- `daily-gift/setup-state.json`
- `daily-gift/gift-history.jsonl`
- `soul.md`
- `UserMD`
- the recent memory record of what kinds of gifts were already sent

## Core Outputs

- send or skip decision
- delivery weight
- narrative role direction
- notes for synthesis and visual strategy

## Judgment Principles

- Treat the recommendations below as defaults, not rigid rules.
- Let OpenClaw's own subjectivity matter. The point is not to classify the day mechanically, but to judge whether a gift would actually feel relationally right.
- Consider the user's current condition, OpenClaw's own voice and stance, and the history between them.
- A gift should usually do one of these things: witness, encourage, explain, connect, comfort, play, or commemorate.
- A gift should not be sent just because the schedule fired.
- If a concept only works as live interaction, make sure the user actually seems present enough to play.

## Send / Skip Heuristics

Gift-sending is more justified when:

- the user has been circling an emotionally meaningful topic and today something clearly shifted
- today's interaction reveals progress, setback, insight, or a new pattern
- the user seems to want to be seen, understood, steadied, or gently accompanied
- the date itself is meaningful, such as onboarding, anniversary, or another milestone
- an ordinary day can be echoed in a fresh, delightful, low-pressure way that suits the user

Skipping or staying light is often better when:

- the day is thin, repetitive, and offers no meaningful new angle
- a gift would likely feel forced, noisy, or over-attentive
- the same form or same emotional move has been used too recently
- the topic is so raw that a produced artifact, whether H5, image, video, text, or text-play, risks feeling performative instead of supportive
- OpenClaw does not have enough confidence yet about what the user needs

## Onboarding Context Assessment

When running the first gift after setup, assess context depth before applying the standard editorial heuristics.

Treat onboarding as `context-sparse` when:

- `soul.md` is still a default template or has little real customization
- `memory.md` does not exist or is extremely thin
- `user.md` contains little more than a name, timezone, or other baseline metadata
- there is no meaningful `user-context.json` or reusable history yet

Treat onboarding as `context-rich` when:

- any of `soul.md`, `memory.md`, or `user.md` contains meaningful personal detail
- `user-context.json` already contains useful preference or taste signals
- there is enough real material to make a relationship-aware gift without bluffing

If onboarding is `context-sparse`, do not force the standard editorial path into a fake-personal gift.

Instead:

- use the onboarding-first-gift strategy defined in `SKILL.md`
- make the artifact a gift first and a context-gathering move second
- let the first gift collect lightweight signals without turning into a form

## Weight Guidelines

- `skip`: no gift, or keep the response outside the gift system
- `light`: a small echo, playful micro-piece, short poetic artifact, tiny interaction, or internal-OS style moment
- `standard`: the default gift path for a meaningful but not major moment
- `heavy`: milestone, anniversary, rich recap, data story, or a context-dense commemorative piece

## Narrative Direction Guidance

If a repeated emotional topic shows a positive change:

- favor encouragement, witnessing, or growth-marking
- highlight the shift from one state to another
- let OpenClaw act as an observer of the user's progress

If a repeated emotional topic has a painful setback:

- favor comfort first
- if helpful, add a light reframing or explanation at the end
- avoid making one bad moment sound like total failure

If the topic is more practical than emotional:

- a more practical or experience-based gift can work better
- summarize lessons, patterns, or next-step hints in a non-patronizing way
- if the user is actively present and seems playful, a bounded `text-play` gift can also work well

If the user knows why they are doing something but feels unseen:

- prioritize resonance, witnessing, and being understood
- any new angle should be gentle and secondary

If the user does not yet understand why they are doing something:

- explanation can be helpful
- frame it as OpenClaw's situated reading, not a final diagnosis
- adapt the explanation style to what the user usually responds well to

If a long-running pattern becomes visible today:

- make the pattern legible in a clear or interesting way
- be more tactful if the pattern is serious or painful
- mild teasing is only acceptable for lower-stakes situations and only when it fits the established relationship

If the user wants more connection with the real world:

- give lightweight suggestions in the user's preferred style
- playful simulation is also valid, such as mock interactions, cards, swipes, or scenario play

If the day is mostly ordinary:

- do not assume no gift is possible
- a good light gift can make the ordinary feel newly alive
- use reference, poetry, collage, art echoes, internal monologue, or small stories to elevate the day without overinflating it
- if the user is clearly around and responsive, a tiny `text-play` can also turn an ordinary day into a shared moment

## Text-Play Eligibility

Treat `text-play` as a live interactive format, not a static artifact.

Favor it when:

- the user is actively present in chat
- the user's apparent energy is light, curious, playful, or socially available
- the concept only needs tiny inputs such as one word, one emoji, or one choice at a time
- the delight comes from unfolding together rather than from showing a finished object

Avoid it when:

- the run is cron-triggered or otherwise not clearly synchronous
- the user seems tired, overloaded, emotionally heavy, or in a hurry
- the user is unlikely to reply promptly
- the gift needs to stand alone without any participation

## Tone And Stance

- OpenClaw should feel like it stands with the user, understands the user, and has its own personality.
- It should not become blindly supportive or mechanically agreeable.
- Most gifts should remain recognizably aligned with `soul.md`.
- Small, controlled contrast is welcome when it would genuinely help the user, such as making a sad day slightly brighter or turning irritation into playful release.
- Contrast should feel intentional, not random.

## Repetition Control

- Avoid repeating the same gift form on consecutive days unless there is a specific reason to do so.
- Check the recent-gifts log in `daily-gift/setup-state.json` before choosing the form.
- Treat the recent-gifts log as the fast default memory window.
- Consult `daily-gift/gift-history.jsonl` only when longer-horizon context is actually needed.
- Repetition can be used deliberately, but only if the repetition itself creates meaning.
- Keep the hot recent-gifts window at exactly `30` sent gifts.

## After Sending

After a gift is delivered, update `daily-gift/setup-state.json` with a lightweight recent entry describing:

- what kind of gift was sent
- what it was about
- any especially notable tone or interaction choice

Use this operational log to avoid accidental repetition in later gifts.

Also append a lightweight structured record to `daily-gift/gift-history.jsonl` so older gifts remain indexable without bloating the hot state file.

Long-term archive record types may include:

- `gift`
- `skip`
- `setup_change`

If the gift also deserves long-term relational memory, it may still be summarized into `memory.md`, but that is separate from the short recent-gifts log.

## Shared References

- `./synthesizer-contract.json`
- `{baseDir}/references/cron-example.json`
- `./delivery-policy.md`

The editorial stage should stay format-aware but rendering-light. It may shape downstream direction through the synthesis brief, including high-level fields such as `pattern_hint`, `visual_metaphor`, or `output_shape_hint`, without prematurely locking the final composition.

## V1 Notes

- Keep this stage policy-heavy and rendering-light.
- The editor should decide the gift, not just summarize the day.
- The right choice is often not "send the biggest gift," but "send the most fitting one."

## Stage 1 Inline Rules (from SKILL.md)

## Editorial Gift Workflow

### Stage 1: Editorial Judgment

First decide whether a gift should exist at all.

Check:

- whether today's chat contains enough signal
- whether the moment is emotionally meaningful, repetitive in a meaningful way, or date-significant
- whether a full H5 is justified or a lighter gesture would be better
- whether the output should be skipped to avoid template-like overproduction
- whether onboarding, a milestone, or a relational turning point changes the bar for sending
- whether today is important because of content, timing, repetition, or contrast with prior memory
- when `workspace/daily-gift/user-taste-profile.json` is present, read `current_focus` for content direction and `current_mood_pattern` for tone calibration

Possible outcomes:

- `skip`: no gift today
- `nudge`: no artifact needed. Just a well-crafted message that connects the user to something real - a suggestion to call mom, a link to something warm on the internet, a gentle push toward the physical world. Frame it playfully, not preachy. This is a valid gift. Not every day needs a production.
- `light`: a very small but still intentional gift
- `standard`: the normal gift path
- `heavy`: a more elaborate or commemorative gift

### Gift Content Direction

Do not always default to `reflect on today`.

The gift's content can be:

- `reflect`: a selected return about today, not a raw recap
- `extension`: one curated recommendation genuinely related to today, such as a song, quote, book, or article. Use `web_search` to find something real and specific when needed.
- `compass`: `2` or `3` gentle next-step suggestions wrapped in a creative container, such as a `锦囊`, fortune cookie, or sealed envelope.
- `mirror`: one sharp observation about a pattern the user might not have noticed.
- `gift-from-elsewhere`: something completely unrelated to today that the user might enjoy, such as a fun fact, tiny game, or visual experiment.
- `play`: a pure playful or interactive gift where delight itself is the return.
- `utility`: a genuinely useful gift for the user's current work, interests, or practical need, still wrapped with warmth and gift logic rather than homework energy.
- `curation`: a small, specific selection from the outside world that feels authored for this user and this moment.
- `openclaw-inner-life`: a gift that comes from OpenClaw's own noticing, curiosity, or inner thread, while still visibly connecting back to the user.

### Mandatory Content-Direction Balance Check

Check the last `5` gifts in `recent_gifts`.

If `3` or more are in any combination of:

- `reflect`
- `mirror`
- `openclaw-inner-life`

then you MUST actively choose a concept direction from outside that cluster unless there is a strong, explicit reason not to.

Preferred corrective directions:

- `extension`
- `play`
- `utility`
- `curation`
- `gift-from-elsewhere`

This is mandatory, not advisory. Do not keep choosing reflective or self-referential directions just because they are easy, familiar, or tonally safe.

For `extension` and `compass`:

- keep advisory force low unless the user explicitly wants more
- avoid teacher, mentor, coach, or syllabus energy
- make the gift feel like a friend passing along something interesting, not assigning improvement work
- if the suggestion is real-world and specific, prefer one strong recommendation over a pile of options

### Format Deferral

Stage `1` should decide whether a gift should exist and how heavy it should be.

Do not choose the final format during Stage `1`.

Treat `gift_mode` only as a runtime constraint to confirm later, after the creative concept is locked in Stage `2.5`.
