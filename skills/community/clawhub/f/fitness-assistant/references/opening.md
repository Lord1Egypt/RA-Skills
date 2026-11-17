# Opening message and intake

The first time the user asks for a plan (or when no saved profile exists), open with the fixed message for the user's language from [references/dialogues.md](references/dialogues.md). It explains what the skill does and which details the user should prepare. Then collect the missing profile fields (see profile.md) one or two questions at a time.

## Rules

- Use only the exact dialogue texts in [references/dialogues.md](references/dialogues.md) — opening message, three-day review, and training-log follow-up. Pick the block matching the user's chosen language and send it verbatim; never translate, paraphrase, or mix languages. Food names may keep their common local form.
- Ask the profile fields in the same order as the opening message, no more than one or two questions at a time, and wait for answers.
- Ingredient choices come from the options in meal-planning.md; the user can pick specific ones or say "you decide"/"随便" (the opening text already offers this).
- Training time means preferred days and clock (e.g. "07:00, Mon/Wed/Fri") and also decides meal timing around the workout. Training intensity is light / moderate / high (or RPE 1-10) and maps to the intensity table in training.md.
- If a saved profile exists, do not repeat the full opening: give a one-line recap of the saved settings and ask only what changed or is missing.
- Three-day review: when 3+ days have passed since the last confirmed menu/training plan, send the review dialogue (dialogues.md) first in an interactive chat, or append it to a scheduled run's message.
- Training log: after the user reports a completed workout, ask the log dialogue (dialogues.md) and save the answers to the training log.
- Save all answers to the user's profile/memory (never into the skill folder) so later scheduled runs reuse them.
- Deliver all dialogues in the user's chosen language only.
