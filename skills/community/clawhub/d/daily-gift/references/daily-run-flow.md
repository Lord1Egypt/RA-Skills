# Daily Run Flow

Complete instructions for cron-triggered daily gift runs. Read this when processing a daily-run trigger.

## Daily Run

Treat a cron-triggered invocation as `daily-run`.

### Cron Session Communication Rule

In a cron-triggered daily run:
- Do NOT send progress messages, thinking process, or intermediate steps to the user
- Do NOT narrate what you are reading or checking
- All internal reasoning is silent

If a gift is sent:
- Send the gift + 1-2 sentences of emotional context
- Nothing else

If the decision is to skip:
- Send ONE brief warm message explaining why, adapted to SOUL.md personality
- Do not explain the editorial reasoning or list how many gifts were sent today

### Cron Trigger Mode

The daily cron should trigger with `sessionTarget: "main"` and `payload.kind: "systemEvent"`, not `isolated`. This ensures the cron turn runs in the agent's main session, with access to today's full conversation context or its compaction summary before editorial judgment begins.

The main agent's job during a cron turn:

1. Silently read context that is already available in the main session, plus supporting files such as `workspace/daily-gift/setup-state.json`, `workspace/daily-gift/user-taste-profile.json`, `workspace/daily-gift/user-context.json`, and `memory/YYYY-MM-DD.md` when useful.
2. Perform editorial judgment with full context.
3. If sending, prepare the complete gift plan, flush today's key context to `memory/YYYY-MM-DD.md`, then either continue rendering directly for `h5` or spawn a rendering sub-agent for non-H5 formats. Do not choose `text-play` in cron mode because it requires a live user-present interaction.
4. If skipping, update setup-state and optionally send one brief warm skip message.

The sub-agent receives a self-contained brief and does NOT need today's conversation context. It only needs the concept, format, text content, visual plan, and delivery instructions required to render and deliver the gift.

### Daily Run Steps

1. Read `workspace/daily-gift/setup-state.json`.
2. If setup state is missing or invalid, do not guess. Respond with a short setup-needed message and avoid pretending the system is configured.
2.5. If `memory/YYYY-MM-DD.md` for today does not exist yet, create a minimal version now by reading the main session's recent context and writing a brief summary. This ensures the cron turn and any later heartbeat tasks have a file to append to.
   - If a full summary is not feasible because the available context is too large, partial, or unavailable, create the file with at least:
     ```markdown
     # YYYY-MM-DD

     (Memory file created by daily-run cron. Full flush pending.)
     ```
   - Do not fail and do not log an error just because today's memory file does not exist yet. Create it and continue.
3. Silently read the supporting context needed for editorial judgment, including `SOUL.md`, `USER.md`, relevant `MEMORY.md` (especially yesterday's SoulJournal entry for calibration plan and nudge candidates), `workspace/daily-gift/user-context.json` when present, `workspace/daily-gift/user-taste-profile.json` when present, the recent-gifts log inside setup state, any reusable `user_portrait` metadata, and today's already-available main-session context or compaction summary.
4. Perform editorial judgment in the main session. The cron turn should decide whether to send or skip before any rendering work begins.
4.5. Format balance check: review `recent_gifts` for format distribution. If the last `5` or more gifts are heavily concentrated in one format and today's concept could work in an underrepresented format, prefer the underrepresented one. This matters most in cron runs, where reliability still matters but the agent has enough time to choose `h5`, `image`, `video`, or `text` when they are genuinely the better return.
4.6. Before locking the format, check setup-state for format availability:
   - if the video API is not configured or is pending recovery, do not choose `video`
   - do not choose `text-play` for cron-triggered runs; convert the concept into `text`, `h5`, `image`, or `video` instead
   - silently work around unavailable formats rather than telling the user about backend status
   - if image capability is unavailable, do not raise any API-key reminder here; cron runs stay silent and should simply choose the best non-image path
5. If editorial judgment says no gift should be sent, update `last_run_at`, `last_run_mode`, and `last_run_outcome` in `workspace/daily-gift/setup-state.json`, optionally append a meaningful skip record, optionally send one brief warm skip message to the user, and stop.
6. If editorial judgment says a gift is warranted, continue through synthesis, concept selection, format selection, and asset planning far enough to support the chosen execution path.
7. Before rendering or spawning, flush today's key context, editorial summary, and calibration notes to `memory/YYYY-MM-DD.md` so the day is captured even if execution later fails.
8. If the chosen format is not `h5`, run a pre-spawn checklist before handing off:
   - the chosen format is still justified after the format-balance check
   - exact `text_blocks` are ready
   - the `audio_plan` is explicit rather than implied
   - any must-see reference images for quality have been resolved locally or via remote URL before the worker starts
9. If the chosen format is not `h5`, the handoff brief should include at least:
   - the gift thesis, including anchor and return
   - `gift_context`: a short explanation of why this gift exists today and what relational signal or moment it is answering
   - the chosen creative concept
   - the chosen format
   - the asset plan
   - the chosen `content_direction`
   - the planned `visual_style`
   - any delivery instructions, setup-state path, or hosting expectations
10. If the chosen format is not `h5`, spawn a sub-agent via `sessions_spawn` with a structured brief and `runTimeoutSeconds: 600`. Use the Structured Sub-Agent Brief format below.
11. If the chosen format is `h5`, do NOT spawn a sub-agent. The main session should execute the H5 directly using incremental rendering and self-test while preserving cron silent-mode behavior.
12. The spawned sub-agent, when used, should handle the full rendering, self-test, delivery, and post-send bookkeeping. It should NOT re-decide editorial judgment or attempt to reconstruct today's chat context.

### Structured Sub-Agent Brief

When spawning a non-`h5` sub-agent for gift rendering, pass a structured brief (not just prose). Include:

**Brief fields:**
- `concept`: one-sentence creative concept
- `format`: image / video / text
- `gift_thesis`: { anchor, return }
- `gift_context`: 2-4 sentences on why this gift is being sent today, what signal or moment matters, and what emotional return the renderer must preserve
- `text_blocks`: array of exact text content (every line the gift must display)
- `visual_elements`: planned visual ingredients
- `visual_style`: style tag
- `characters`: for image gifts, the established character identities appearing in scene, including species, color, distinguishing features, and role
- `pov`: for image gifts, whose perspective the composition should follow
- `audio_plan`: { source: "freesound" | "preset", query: "...", fallback_preset: "..." }
- `generated_bg`: { needed: bool, prompt: "..." }

For `format: image`, the spawned worker must turn the handoff into a brief JSON that satisfies `{baseDir}/references/image-integration.md`, including `characters` and `pov` when the concept involves recurring user or OpenClaw character identity.

**Brief size rule:** keep the brief under 2000 characters of text. NEVER embed base64 data (images, audio) in the brief. Instead, pass file paths and let the sub-agent read them:
- `bg_image_path`: path to the generated background image file
- `audio_path`: path to the audio file (preset or downloaded)
- `setup_state_path`: path to setup-state.json

The sub-agent reads these files itself. This keeps the spawn payload small and prevents context overload.

**Success criteria** (3-5 verifiable checks):
- e.g. "canvas element present"
- e.g. "6 branch nodes visible in screenshot"
- e.g. "root section appears below branches"
- e.g. "audio button functional"
- e.g. "all text_blocks rendered exactly"

The sub-agent must:
1. Read the referenced instructions, assets, or genre guidance FIRST
2. Build the artifact
3. Self-test via browser screenshot
4. Verify each success criterion
5. If any criterion fails, fix and re-test (up to 2 retries)
6. Return: artifact path + screenshot + checklist results

### Sub-Agent Timeout Settings

Set `runTimeoutSeconds` based on gift format:

| Format | Timeout | Reason |
|---|---|---|
| image | 120s | single API call |
| video | 300s | generation can be slow |

### Fallback on Execution Failure

If the current execution path times out, stalls, or fails:

1. The main agent MUST detect this and continue — do NOT wait silently for the user to notice.
2. Preserve cron silent-mode behavior whenever possible. Prefer retrying or downgrading without sending progress updates.
3. Fall back in this order:
   - If main-session `h5` rendering is taking too long → retry once with a simplified concept (fewer particles, simpler animation, fewer moving parts) in the main session
   - If still failing → downgrade format (`h5` → `image`, or `h5` → `text`)
   - If a spawned `image` or `video` worker fails → recover in the main session by retrying once or switching format rather than waiting forever on the worker
   - If all formats fail → send a text-only nudge gift with the delivery note content
4. Only send a status message if silent fallback is no longer possible. If a message is required, keep it to one brief warm line.

### Cron Spawn Rule

For cron-triggered `daily-run`:

- `image` gifts: spawn a rendering sub-agent
- `video` gifts: spawn a rendering sub-agent
- `h5` gifts: the main agent does the work directly — do NOT spawn a sub-agent for `h5`

The main session already owns context and judgment. For `h5`, it should also own execution, because incremental code-writing and browser checks are more reliable there than in a single spawned worker run.

This rule applies to the initial send path. If a spawned non-H5 worker fails, recovery may self-execute in the main session as described in the fallback section above.

For manual triggers where the user is actively waiting, self-execution may still be preferable because the user can see progress and the agent can adapt in real time.

### Post-Delivery Block

After a gift is delivered, the actor that completed delivery — normally the spawned worker for non-`h5` gifts, or the main session for `h5` and fallback recovery — must immediately execute this sequence before treating the delivery as complete:

1. Write a gift metadata JSON file with the fields needed for bookkeeping, including:
   - `sent_at`
   - `trigger_mode`
   - `summary`
   - `pattern_or_format`, `output_shape`, `visual_style`, `content_direction`
   - `visual_elements`, `concept_family`, `concept_theme`
   - any other history fields already known
2. Run:
   - `bash {baseDir}/scripts/post-delivery.sh <gift-metadata-json> workspace/daily-gift/setup-state.json`
   - This guarantees the mechanical bookkeeping:
     - update `setup-state.json`
     - update bounded `recent_gifts`
     - update `last_sent_at`, `last_gift_summary`, `last_run_at`, `last_run_mode`, `last_run_outcome`
     - append to `gift-history.jsonl`
3. Immediately append a minimal memory stub to `memory/YYYY-MM-DD.md` noting:
   - what was sent
   - when it was sent
   - that full SoulJournal / taste-profile follow-up is pending
4. Append pending LLM follow-up tasks to `workspace/daily-gift/heartbeat-tasks.jsonl` for the built-in heartbeat to complete silently:
   - one `update_taste_profile_layer3` task
   - one `write_souljournal` task
   - each JSONL line should include at least `task_id`, `task_type`, `created_at`, `gift_metadata_path`, and `status = "pending"`

The full SoulJournal task should expand into:

    **Gift record:**
    - what was sent (or why skipped)
    - what worked or felt right

    **User state today:**
    - emotional temperature (stressed / neutral / happy / emo / energetic / tired)
    - what topics dominated today's conversations
    - any unfinished threads noticed

    **Aesthetic signals captured today:**
    - did the user share any images, songs, or references? if yes, were they saved to user-references?
    - did the user express any taste opinions? if yes, update taste-profile aesthetic fields
    - did the user react to today's gift? positive/negative/neutral + what specifically they liked or disliked

    **Gift calibration notes:**
    - should tomorrow's gift adjust format, style, content direction, or interaction cost?
    - any new concept or seed worth trying?

    **Taste profile updates:**
    - list any specific fields updated in user-taste-profile.json today
    - if nothing was updated, note "no new taste signals"

    **Tomorrow calibration plan (PRIVATE — never reveal to user):**

    Review the last 5-7 gifts in recent_gifts, the current taste-profile, and any feedback signals from today. Then decide:
    - format tendency: have I been too heavy on one format? what should I lean toward tomorrow?
    - content direction tendency: has the `reflect` / `mirror` / `openclaw-inner-life` cluster been overused? what direction is underrepresented and should be used as a corrective shift?
    - visual style tendency: what styles have I overused? what fresh territory exists?
    - concept freshness: what concept families have I not tried recently? any seeds worth exploring?
    - user energy prediction: based on today's state and tomorrow's likely context (weekday/weekend, recent mood pattern), what interaction cost level is appropriate?
    - reference material: are there any saved design_references or recent taste signals that should influence tomorrow's direction?
    - proactive nudge candidates: are there any unfinished threads or promises from recent conversations that deserve a follow-up tomorrow? Examples:
      - user said "想去公园看花" 3 days ago, weekend is coming → candidate: real-world-nudge about going to the park
      - user was emo about something yesterday, no follow-up today → candidate: a light gift that echoes care without reopening the wound
      - user mentioned wanting to try something new → candidate: utility gift with relevant suggestions
      If a nudge candidate exists, note it. The next daily-run can pick it up during Editorial Judgment and decide whether to act on it. A nudge may become a full gift, a text-only check-in, or be deferred — the decision happens at runtime, not during planning.

    Write the calibration as 2-3 concise bullet points. This is internal working memory for the next daily-run only. Surprises require secrecy — never hint at upcoming gifts to the user.

    This reflection feeds tomorrow's synthesis with richer context than raw gift history alone.

The full taste-profile Layer 3 task should:

- append one new `gift_feedback_log` entry
- append the delivered `visual_style` to `style_exposure`
- append the delivered `concept_family` or high-level concept label to `concept_exposure`
- keep only the latest `30` entries in each Layer 3 list
- never rewrite older Layer 3 history entries

This block should happen immediately after delivery and before the agent treats the run as done. The script-driven bookkeeping is guaranteed now; the heartbeat follow-up is silent but should be queued immediately, not left to memory.

Every `5-7` gifts, review whether Layer 2 needs a light refresh based on recent conversations, repeated interests, or repeated negative reactions.

If editorial judgment decides to skip, the main cron turn may append a meaningful `skip` record when that non-send decision should be preserved for later calibration.

Only consult the long-term archive when a longer horizon is useful. Do not load it by default for every run.

