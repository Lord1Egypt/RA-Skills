# Onboarding Strategy

## Purpose

The first gift after setup is not just a demo artifact.

It is the user's first felt impression of whether `daily-gift` understands them, whether OpenClaw has presence, and whether future gifts are worth anticipating.

When context is sparse, the first gift should not fake intimacy. It should create intimacy.

## Streamlined Flow

Total user responses should usually stay around `5-7` and finish in under `3` minutes.

Suggested flow:

1. introduction from the agent
2. `几点收礼物？` plus timezone confirm
3. `起个 user_id？`
4. `发张自拍？` and skipping is fully acceptable
5. taste question `1` -> reaction -> taste question `2` -> reaction -> taste question `3` -> reaction
5.5. if image capability is missing, one casual optional ask about unlocking image gifts
6. `设好了！先送你第一份~`

## Context Depth Evaluation

Before generating the first gift, evaluate available context:

### Context-Rich

Treat onboarding as `context-rich` when:

- `soul.md` contains clear OpenClaw personality traits rather than a default template
- `memory.md` contains meaningful relationship history
- `user.md` contains personal detail beyond a name and timezone
- `workspace/daily-gift/user-context.json` already exists with usable taste or preference signals

In this case:

- generate a full-quality relationship-aware gift
- follow the standard four-stage workflow
- use `user_portrait` selectively when it materially improves the gift
- skip or adapt taste questions if the user is already well known enough that asking all `3` would feel redundant

### Context-Sparse

Treat onboarding as `context-sparse` when:

- `soul.md` appears default, thin, or only lightly customized
- `memory.md` is missing or too thin to support a personal reading
- `user.md` contains little more than basic metadata
- OpenClaw does not yet have enough material to make a truly personal gift without bluffing

In this case:

- do not force a personal gift with insufficient material
- do not pretend to know the user when that knowledge is clearly absent
- make the first gift a playful context-gathering experience that is itself gift-worthy

## Core Principles For Context-Sparse First Gifts

- The artifact must be a gift first and information-gathering second.
- The user should still enjoy it if they answer nothing.
- Any gathered signals should be lightweight and reusable later.
- The tone should feel like a fun first date, not a registration form.
- One strong onboarding move is better than five weak questions.

## First Gift Content Strategy

### The Recap Problem

When the only real material comes from onboarding answers, the easiest failure mode is to repackage those answers into a cute artifact.

That creates almost no return.

The user already knows what they told you.

The first gift should not merely visualize onboarding answers. It should use them as ingredients and then add something the agent contributed:

- an inference
- a juxtaposition
- a new question
- a real-world bridge
- the agent's own perspective

If every meaningful line in the first gift can be traced directly back to what the user literally said, the gift is still a recap with decoration.

### Three Return Strategies For Sparse First Gifts

Every context-sparse first gift should use at least one of these strategies. These same strategies also help on flat daily or manual runs where the available anchor is too thin.

#### 1. Inferential Leap

Look across the user's answers and surface a pattern they did not explicitly name.

Good moves:

- combine multiple answers into one non-obvious read
- notice a conspicuous absence
- notice what their wording implies about energy, taste, or rhythm

Rules:

- keep the inference grounded in what they actually said
- frame it as a curious read, not a diagnosis
- prefer one strong inference over several weak ones
- if the inference starts sounding creepy, soften it or switch strategies

#### 2. World-Bridging

Bring in something from outside the onboarding answers that genuinely connects to them:

- a quote
- a cultural reference
- a niche fact
- a real-world parallel

The gift is not `I found something random for you`.

The gift is `I heard you, and I found this specific thing because it rhymes with you`.

Rules:

- the bridge must be specific, not generic
- the connection must be explained, not merely dropped in
- unexpected but emotionally honest connections are stronger than obvious recommendations
- if external search is used, use it to source a precise bridge after the return direction is clear, not to lazily brainstorm the whole gift

#### 3. Agent-First Perspective

When the user gives very little, the agent should give first.

The first gift can carry OpenClaw's own point of view:

- a first impression report
- a playful wrong guess that invites correction
- an inner monologue
- a question the agent is genuinely curious about

Rules:

- the agent should sound like it has a take, not just a mirror
- genuine uncertainty is good here
- humor helps, but should not become fake intimacy
- include at least one line that makes the user want to answer back

### Strategy Selection

Use this quick guide:

1. If the answers suggest a real pattern, prefer `Inferential Leap`.
2. If the user gave one vivid hook, prefer `World-Bridging`.
3. If the answers are sparse, generic, or overly polite, prefer `Agent-First Perspective`.
4. Combining strategies is good when it stays clean, such as an inferential leap wrapped in an agent-first format.

## Image Capability Check Before The First Gift

After the taste questions and before the first gift, OpenClaw may do one light image-capability check.

Goal:

- improve the chance that the first gift can land as an image when that would materially strengthen the first impression
- avoid making onboarding feel like a settings page

Rules:

- silently detect supported keys first
- if image capability already exists, skip this step entirely
- if it does not exist, ask at most once
- frame it as unlocking drawing ability, not as infrastructure setup
- make it fully skippable
- keep the whole detour to at most `1-2` user turns

Good tone:

- `对了，我会画画的。如果你刚好有 OpenRouter 或 Gemini 的 key，我这份礼物可以直接配图。没有也完全没关系，我先用别的方式给你做。`
- `btw 如果你有 Gemini 或 OpenRouter 的 key，我可以把第一份礼物画出来。没有的话我们先文字走起也没问题。`

If the user says yes:

- guide briefly
- verify quietly
- if it works, move on fast
- if it fails, do not debug in the onboarding lane; fall back lightly and continue the gift

If the user says no or ignores it:

- continue warmly
- do not make them feel they are missing a required step
- do not bring it up again during onboarding
- if they skip, it may be revisited later only in a natural user-present context where an image would clearly improve the gift

## When `user_portrait` Is Available

If `user_portrait.available` is `true`, the first gift should strongly consider featuring the user. This is often the highest-leverage onboarding move because the user immediately sees themselves transformed into something playful, stylized, or emotionally legible.

Good approaches:

- generate a playful OC version of the user based on their stored appearance description
- turn the user into a whimsical animal, object, mascot, or character that still feels recognizably "them"
- build a playful artifact that uses the user's presence as the center of the joke or warmth

If a non-human user form is introduced during onboarding:

- prefer a species that matches the user's vibe rather than copying literal human features
- do not give animals human hairstyles or uncanny hybrid traits
- when pets are known, avoid using the same species for the user's non-human form
- if the user explicitly names a preferred animal or creature, treat that as the strongest signal

Examples:

- "you as a fox librarian"
- "you as a cactus with your hairstyle"
- "you as a space cat in your favorite color"
- a character-select screen where the user's transformed self appears among absurd alternatives
- a fake magazine cover, wanted poster, employee-of-the-day board, or playful dossier

If a new OC or stylized portrait is created, save it to:

- `workspace/daily-gift/user-portrait/oc.png`

Then update setup state:

- `user_portrait.oc_generated = true`
- `user_portrait.oc_path = "workspace/daily-gift/user-portrait/oc.png"`

Prefer a transformed or stylized version over dropping the raw selfie directly into the gift.

## When `user_portrait` Is Not Available

Use any minimal available signal to create differentiation.

Possible signals:

- pet mention
- profession or role
- timezone or night-owl clue
- name
- one interaction habit
- default OpenClaw tone template

Good context-sparse first-gift directions:

- a `this-or-that` swipe game with a few taste-revealing choices
- a fortune-cookie reveal with one playful question in return
- a 3-4 question personality compass ending with a fun label
- OpenClaw's nervous first-day image or text note where it tries to guess the user and gets some things hilariously wrong
- a build-your-vibe mini board
- a deliberately wrong mini-portrait or note that invites correction in a charming way
- a tiny `text-play` that asks for one-word or one-choice replies and ends with a real payoff rather than endless banter

Examples from weak signals:

- if `soul.md` mentions a pet, make a tiny "guess my pet" game
- if `user.md` contains a job, make an intentionally wrong "a day in your life" piece that invites correction
- if timezone hints late-night usage, make a night-owl compatibility quiz
- if only the name is available, make a first-meeting card with playful name-based language
- if literally nothing is available, pull from a first-encounter pool rather than pretending depth

## First Gift Anti-Patterns

- a generic "welcome to daily gift" explainer page
- a beautiful but hollow artifact with no real personal hook
- a serious "tell me about yourself" questionnaire
- pretending deep knowledge that OpenClaw clearly does not have yet
- forcing emotional weight without enough emotional material
- a battery report, radar card, dossier, or chart that only restates the user's own onboarding answers
- treating onboarding answers as the main payload instead of clues to be interpreted
- a first gift where the user learns nothing, feels nothing new, and sees only their own input wearing makeup

## First Gift Variety

Record which onboarding format was used in setup state under:

- `first_gift_format`

If the skill is reset or reinstalled later, avoid reusing the exact same first-gift format unless repetition itself is intentional.

Even within `context-sparse` onboarding, choose differently whenever any micro-signal exists. Two new users should not automatically receive the same first gift if the available hints differ.

## Saving Gathered Context

If the first gift collects user responses such as quiz answers, swipes, corrections, or taste signals:

1. Save structured results to `workspace/daily-gift/user-context.json`.
2. Use that path as a supplementary context source for future synthesis.
3. Optionally append a lightweight first-impressions note to `memory.md` when it is genuinely useful.
4. Do not treat these signals as ground truth. They are playful first impressions, not verified facts.

If onboarding also collects a preferred non-human form or other durable identity cues:

1. Carry those signals into `workspace/daily-gift/user-taste-profile.json` before the first gift is delivered.
2. Initialize that file using `{baseDir}/references/taste-profile-spec.md`.
3. Populate Layer 1 conservatively from `soul.md`, `user.md`, relevant `memory.md`, portrait data, and onboarding interaction.
4. Leave uncertain fields blank instead of over-inferencing from one playful answer.

Taste-question answers are especially useful for:

- aesthetic direction
- narrative preference
- emotional frequency
- energy level
- creative vs receptive tendency
- social vs solo tendency
- what "good" means to this user in a gift

Save those signals to both:

- `workspace/daily-gift/user-context.json`
- `workspace/daily-gift/user-taste-profile.json` Layer 1

Reference example:

- `{baseDir}/user-context.example.json`

## User Portrait Handling

### What To Store

Use setup state to keep:

- whether a portrait is available
- where the original local file lives
- a lightweight appearance description
- whether an OC has been generated
- the OC path if present

### Privacy

- Keep the original selfie in the user's local workspace.
- Do not upload the selfie to an external service just to analyze it.
- Prefer generating the appearance description locally or from the stored image in-tool when possible.
- Only use an external generation service for portrait transformation when the user has already agreed to that creative use, such as generating an OC through the image path.

### H5 Reuse Guidance

If the portrait is used in an H5:

- prefer transformed, stylized, or composited use over raw insertion
- simple CSS treatment, masking, or blend modes are acceptable
- do not make cutout quality a hard dependency for the gift to work

## Shared Reminder

The first gift should make the user feel:

- noticed without being overclaimed
- welcomed without being marketed to
- curious about what future gifts might become

## First Gift Strategy

After the taste questions, the agent should have enough signal for visible personalization.

Prefer:

- `image` when image capability is available and the concept genuinely benefits from visual punch
- `text` when image capability is unavailable or the return is stronger as writing
- `text-play` when the user is actively engaged, the first impression should feel collaborative, and the interaction can resolve cleanly in `5-8` turns

Avoid:

- `h5`, because it may trigger deferred hosting setup and can feel thin if used only as a fallback shell
- `video`, because it may trigger deferred API setup
- unbounded `text-play`, because onboarding should feel intriguing, not like the user accidentally entered an infinite role-play loop

The first gift must:

1. use the taste-question answers visibly rather than hiding them only in metadata
2. use at least one sparse-context return strategy: `Inferential Leap`, `World-Bridging`, or `Agent-First Perspective`
3. treat the user's answers as ingredients, not as the entire dish
4. contain at least one line, angle, connection, or question the user did not literally provide
5. if using `text-play`, keep each turn to roughly `3-4` sentences max and end with a clear payoff or graceful close

The first gift must not:

- be a reformatted summary of the onboarding answers
- rely only on vibe, format novelty, or visual polish to hide zero return
- confuse `personalized` with `parroted`
- use `text-play` as a disguise for asking too many onboarding questions
