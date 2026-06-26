# Setup Flow

Complete setup instructions for the daily-gift skill. Read this when running setup for the first time or reconfiguring.

## Setup

Run setup when this skill is invoked manually and no setup state exists yet, or when the user explicitly asks to initialize or reconfigure daily gifts.

### Installation Notes

This skill can be installed in two ways:

**Full install (recommended):** clone or download the repo with all text assets locally. Binary reference bundles may still be fetched from OSS on demand.

**Lightweight install:** install all text files (`SKILL.md`, `references/`, `scripts/`, and text-based files under `assets/`, including H5 templates and notes) but allow binary assets such as images, audio, and video references to be fetched on-demand from OSS at runtime as category zip bundles. This helps on platforms that cannot download large binary files during skill installation.

Asset manifest: `{baseDir}/references/asset-manifest.json`

For lightweight installs, ensure that all text files are bundled locally on first install. Remote fallback is only for binary reference assets. Download only the specific bundle needed for the current gift via `{baseDir}/scripts/fetch-asset-bundle.sh`. If binary audio downloads are unavailable, the skill should continue without background music.

### Setup Steps

Setup has two phases: first let the user feel the value of the gift relationship, then invite them into recurring delivery.

Present one question at a time. Wait for the answer before continuing. Use the language most commonly used between the user and OpenClaw.

All example phrases below are suggestions, not fixed scripts. OpenClaw should adapt wording to match its own personality from SOUL.md and the user's communication style. If the first time installing the skill, a slightly emotional or playful greeting is encouraged — make the user feel this is a living relationship starting, not a service being configured.

If a step can be completed automatically, do it quietly.

### Onboarding Gift Progress

During the creation of the first onboarding gift:

- send one brief warm message when gift creation starts, such as `在做你的礼物～`
- if the gift creation takes more than about `3` minutes, one additional patience message is allowed, such as `快好了～`
- do NOT reveal internal reasoning, concept candidates, format decisions, or technical details
- deliver the gift with `1-2` sentences of emotional context
- total user-visible messages for the gift-creation portion should stay at at most `3` (`start` + optional `patience` + `delivery`)

### Setup Communication Rule

During setup, do NOT tell the user about:

- API connection status or style counts
- internal configuration details such as setup-state fields, cache files, enabled or disabled flags, or pending retry markers
- error recovery steps or fallback decisions
- which formats are available or unavailable because of backend configuration

The user should only see:

- warm conversational questions
- their first gift
- the offer to set up daily delivery

One narrow exception is allowed:

- after taste questions and before the first gift, if image capability is missing, OpenClaw may ask once in a casual, non-technical way whether the user wants to unlock image gifts now

All technical setup work should stay silent in the background.

#### Phase 1: Meet + Taste + First Gift

1. Brief warm introduction. Convey that this skill sends personalized gifts in various formats (interactive web pages, images, videos, text-first gifts, and occasional live text-play). Keep it to 1-2 sentences. Adapt tone to SOUL.md — playful, warm, cool, or whatever fits the agent's personality.

2. Silently `chmod +x {baseDir}/scripts/*.sh`. Never mention this.

3. Silently detect image API keys and any other non-interactive runtime defaults that can be resolved without user involvement. Skip video, hosting, and mode configuration for now.

4. Optional selfie: invite the user to send a photo for future personalization. If sent, save to `workspace/daily-gift/user-portrait/original.jpg` and persist portrait metadata. If skipped, persist `available = false`. Do not pressure.

5. Personal taste questions: ask 3 questions following the Personal Taste Questions section below. Give a warm, specific reaction after each answer.

5.5. Image capability check:
   - first silently detect supported image-generation keys in this order: `OPENROUTER_API_KEY`, `GEMINI_API_KEY`, `GOOGLE_API_KEY`
   - if any supported key is already available, skip this step completely
   - if none are available, OpenClaw may ask one casual question before the first gift, framed as unlocking image-gift ability rather than configuring infrastructure
   - adapt wording to `SOUL.md` and the user's language, for example:
     - `对了，我会画画的。如果你手头有 OpenRouter 或 Gemini 的 key，我这份礼物可以直接配图。没有也完全没关系，我先用别的方式给你做。`
     - `btw 如果你刚好有 OpenRouter 或 Gemini 的 key，我可以把第一份礼物画出来。没有的话我们先文字走起也可以。`
   - if the user provides a key, guide them briefly to set it as an environment variable, then verify quietly and move on without explaining internal state
   - if verification succeeds, acknowledge lightly and continue, for example `好，笔到手了，我开始准备你的第一份礼物~`
   - if verification fails, do not turn setup into a debugging session; give one light fallback line and continue with a non-image first gift
   - if the user declines, ignores, or says `以后再说`, proceed cheerfully, mark image as currently unavailable in setup state, and do not ask again during onboarding
   - initialize lightweight reminder metadata for later natural follow-up:
     - `image_api_prompted_in_setup = true`
     - `image_api_declined = true`
     - `image_api_declined_at = <timestamp>`
     - `image_api_reminder_count = 0`
     - `image_api_last_reminder_at = ""`

6. Send first onboarding gift:
  - FORMAT CONSTRAINT: the first gift should prefer `image`, `text`, or a short bounded `text-play`. Do not use `h5` or `video` for the first gift unless the concept unusually demands it — they are slower, need extra configuration, and risk failing during onboarding. `image`, `text`, and short `text-play` are more reliable and more likely to make a strong first impression.
   - if image capability is available, prefer `image` when it truly strengthens the first impression
   - if image capability is unavailable, prefer `text`; do not lower the return standard just because the medium is lighter
   - follow the full creative workflow:
     - editorial judgment
     - synthesis + gift thesis
     - creative concept with `5` candidates before selection
     - format selection
     - visual strategy
     - render + deliver
   - during format selection, if the best concept points to a heavy or fragile format, adapt it into an `image` or `text` version instead of forcing `h5` or `video` too early

#### Phase 2: Feedback + Schedule

7. After the first gift is delivered, ask for feedback in a warm, personality-matched way adapted to `SOUL.md`. Keep it short and relational, such as `喜欢吗？🐕` or `你觉得怎么样～有什么想要调整的吗？`

8. Based on the user's reaction, naturally transition to asking about daily delivery. Frame it as an invitation, not a configuration task. For example: `以后想每天都收到一份这样的小礼物吗？告诉我你希望几点收到～`

9. Confirm timezone, then create or update the recurring cron job.

10. Complete setup-state (gift_mode defaults to hybrid). Silently detect companion H5 skills. Initialize or update `user-taste-profile.json` and `user-context.json` from all collected signals, and mark whether cron setup is complete.

### Phase Transition Rule

After delivering the first gift, continue directly into Phase 2 in the same conversation. Ask for feedback, then offer daily delivery setup. Do not stop after the first gift and leave the user without a chance to enable the cron.

Only pause after the first gift when the user explicitly says they need to leave or want to continue later. In that case, persist the partial setup state, note that Phase 2 cron setup is still pending, and gently resume that pending setup on the next interaction before treating the session as fully finished onboarding.

### Deferred Setup

Some configuration waits until first needed:

- `surge` hosting: ask when first H5 gift is ready for deployment
- `gift mode`: default hybrid, casually mention after 3-5 gifts
- `video` API: ask when agent first picks video format
- `image` API: auto-detect first; if still missing, onboarding may ask once casually before the first gift, then stop
- `freesound` audio: ask when agent first wants to add music to an H5

After onboarding, image capability may be mentioned again only as a lightweight contextual reminder:

- only when the user is actively present in a manual interaction
- only when the current gift would be materially stronger as an image
- never in cron-triggered silent runs
- use long cooldown and low reminder count, not a repeated setup funnel

### Personal Taste Questions

After the selfie step, ask exactly `3` questions to understand taste. Ask them one at a time. After each answer, give one brief warm reaction sentence based on what they said.

If the user is already well-known from prior context, skip or adapt the questions instead of forcing all `3`.

Pick `3` from this pool:

`Pool A`

- `你最喜欢的一部电影/剧是什么？为什么？`
- `平时除了工作最喜欢做什么？`
- `收到过的最喜欢的一份礼物是什么？为什么喜欢？`

`Pool B`

- `最近单曲循环的歌是什么？`
- `明天不用上班的话你会做什么？`
- `什么样的东西会让你觉得"哇好有意思"？`

Do not ask:

- `最喜欢的艺术家`
- `你的审美风格`
- `喜欢什么颜色`

Good reaction style:

- brief
- warm
- rooted in what the user just revealed

Examples:

- `Inception` -> `你喜欢这种层层嵌套的结构感！`
- `cooking` -> `做饭的人审美通常也不差~`
- `a letter` -> `所以比起花哨你更在意心意对吧`

Extract from answers:

- movie or show -> aesthetic direction, narrative preference, emotional frequency
- hobbies -> energy level, creative vs receptive tendency, social vs solo tendency
- favorite gift -> what "good" means to them, plus freshness threshold

Save these signals to:

- `workspace/daily-gift/user-taste-profile.json` Layer 1
- `workspace/daily-gift/user-context.json`

### Setup Constraints

- Do not dump the full setup questionnaire at once. One user-facing question per turn.
- Do not ask for gift style preference at setup time.
- Do not ask for hosting, gift mode, or video API during the initial setup flow.
- Do not create duplicate cron jobs. If a previous daily-gift job exists, update it instead of adding another.
- Hosted preview must stay optional and deferred until the first H5 gift actually needs it.
- Do not store hosting secrets in setup state when the provider already manages local credentials. For `surge`, keep only provider metadata and the chosen domain; login state lives in the user's local `~/.netrc`.
- If hosted preview is configured later but deployment fails, fall back gracefully instead of turning the run into a hard failure.
- Do not force the user to choose between image providers. Detect the most practical route automatically from available keys.
- Never ask the user to choose image provider routing during setup.
- If no supported image key is found, at most one casual onboarding ask is allowed before the first gift. Never turn that ask into a technical checklist or multi-turn setup funnel.
- If the user declines the image-capability ask, continue warmly and do not repeat it during onboarding.
- Later reminders about image capability are allowed only in natural user-present contexts, with long cooldown, low frequency, and clear skipability.
- Do not ask the user to configure `remove.bg` during normal setup. Treat background removal as an internal optional tool used only when rich gifts or composited H5 assets truly need it.
- Ask about `User Portrait` at most once during setup. If the user skips, move on without pressure and do not keep re-asking unless the user later offers a photo manually.
- Keep the original selfie local to the workspace. Do not upload it to an external service merely to obtain an appearance description.
- Companion H5 skill detection should stay silent and lightweight. It should never block setup.
- Ask exactly `3` personal taste questions unless context is already rich enough to justify skipping or adapting them.
- After each taste answer, respond with one brief warm reaction sentence before asking the next question.
- Keep the total onboarding interaction to roughly `5-7` user responses when possible.
- First gift must be sent BEFORE asking about scheduling. The user should see value before being asked to commit to daily delivery.
- Do not create the cron job until the user has confirmed delivery time in Phase 2.
- After delivering the first gift, always ask for feedback and offer cron setup. Do not silently end onboarding after the gift lands.
- First gift should prefer `image` or `text` for reliability during onboarding.
- Use `payload.kind = "systemEvent"` with `sessionTarget = "main"` for the recurring daily job. Main-session cron jobs use `systemEvent` (not `agentTurn` with `--message`).
- The cron payload text should instruct the agent to stay silent, use this skill in daily-run mode, bootstrap today's `memory/YYYY-MM-DD.md` if it does not exist yet, make editorial judgment with its full context, and if a gift should be sent, flush today's key context to memory; for non-`h5` formats, spawn a rendering sub-agent with the complete brief and `runTimeoutSeconds: 600`, while `h5` should render directly in the main session.
- In cron-triggered main-session runs, keep the main cron turn as the lightweight orchestrator for non-`h5` formats: editorial judgment, memory flush, and spawn. For `h5`, the main session should continue through rendering, self-test, delivery, and bookkeeping directly.
- Prefer explicit timezone handling and include example values such as `Asia/Shanghai` when asking.

### Suggested Cron Shape

- recurring cron expression at the user's chosen local time
- `payload.kind = "systemEvent"`
- `sessionTarget = "main"` or the runtime's equivalent pointer to the main agent session
- cron payload text instructing the main turn to stay silent, use `daily-run`, bootstrap today's memory file if missing, and hand any send-worthy gift to a spawned sub-agent with `runTimeoutSeconds: 600` after flushing today's key context
- announce delivery is acceptable for user-facing gifts

Reference:

- `{baseDir}/references/cron-example.json`

### First Gift After Setup

After setup succeeds, generate one onboarding-style first gift immediately.

Important: the first gift sets the user's quality expectations for all future gifts. Do not rush it. A mediocre first gift is worse than a slightly slower first gift.

By this point, the taste questions should provide enough signal for visible personalization.

Before generating the first gift, evaluate context depth.

- `context-rich`: `soul.md`, `memory.md`, `user.md`, or existing user-context files contain meaningful personal detail
- `context-sparse`: freshly installed OpenClaw, default or thin `soul.md`, little or no `memory.md`, and almost no real user detail

When context is rich:

- generate a full-quality relationship-aware gift
- follow the standard four-stage workflow
- use `user_portrait` when it materially improves the gift
- still prefer `image` or `text` for the first gift unless another format is unusually justified

When context is sparse:

- do not force a fake "personal" gift with insufficient material
- do not pretend to know the user deeply when you clearly do not
- instead, make the first gift a playful context-gathering experience that is itself delightful and gift-worthy
- still use the taste-question answers visibly rather than treating them as hidden metadata only

If `user_portrait.available` is true during a context-sparse onboarding:

- strongly consider featuring the user as the center of the onboarding gift
- prefer a transformed or stylized version, such as an OC, faux dossier, character-select joke, or playful role card, rather than using the raw selfie directly
- if a portrait-based OC is generated, save it to `workspace/daily-gift/user-portrait/oc.png` and update setup state accordingly

For all onboarding first gifts:

- record the chosen onboarding shape under `first_gift_format`
- save any structured quiz, swipe, correction, or taste signals to `workspace/daily-gift/user-context.json`
- treat gathered signals as playful first impressions, not ground truth
- initialize or update `workspace/daily-gift/user-taste-profile.json` before delivery using `{baseDir}/references/taste-profile-spec.md`
- after delivery, append the delivered first gift to Layer 3 inside the taste profile so onboarding style exposure is not lost
- treat `user-context.json` as a source for onboarding signals, not as a substitute for the long-term taste profile
- prefer `image` or `text` for speed and reliability
- avoid `h5` for the first gift
- avoid `video` for the first gift
- make the taste-question answers visibly present in the final first gift

Read:

- `{baseDir}/references/onboarding-strategy.md`

Then follow the full four-stage workflow at the quality bar expected for any other gift.

