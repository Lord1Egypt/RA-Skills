# Manual Run Flow

Complete instructions for manually triggered gifts. Includes progress reporting, single output rule, intent detection, and visualization-only mode.

## Manual Run

If the skill is manually invoked after setup is already complete, interpret the user's intent.

### Progress Reporting

Manual trigger gifts: the user should usually see one lightweight warm progress message when work begins, optionally one brief patience message if the process runs longer than about `3` minutes, then the final delivery. The tone should match SOUL.md — playful, casual, like a friend making something for you, not a system reporting status.

Good progress examples (adapt to agent personality):
- "在做你的礼物～"
- "快好了～"
- "等我一下，有个小东西想给你~"

Bad progress examples (never do these):
- "创意确定：矛盾体质鉴定报告——体检报告格式，6项矛盾指标+温柔医生评语"
- "方案：H5（CSS模拟体检报告纸质感）"
- "服务器超时被杀了，重新起"
- "效果不错！部署发送"
- any technical details, error recovery, concept names, format decisions, or internal reasoning

Rules:
- Send one brief warm message when gift creation starts
- If the process takes more than about `3` minutes, one additional patience message is allowed
- Total user-visible messages around the gift should be at most `3` (`start` + optional `patience` + `delivery`)
- Do NOT reveal the specific creative concept, format choice, or any internal reasoning
- Do NOT expose technical errors, retries, or self-test results
- The surprise is part of the gift — keep details hidden until delivery
- Delivery message: send the gift with 1-2 sentences of emotional context (the “why” of this gift, not the “how”)

Very fast image-only gifts may skip the patience message, but they should still avoid verbose or checkpoint-style reporting.

Cron-triggered daily gifts: no progress messages. Deliver the gift with 1-2 sentences of emotional context only.

Exception: when the user is explicitly debugging the skill (e.g. "帮我测试一下", "我要看看流程", "debug模式"), full verbose output is acceptable.

### Single Output Rule

Always deliver exactly ONE final gift to the user.

Do not:
- generate multiple versions and ask the user to pick
- send two images "看看哪个好"
- offer A/B choices

If you want to self-check quality, use the image tool or browser tool internally. The user only sees the final chosen result.

Exception: explicit debug or test sessions with the user.

Do not report progress for:

- cron-triggered daily gifts
- sub-agent spawned work that delivers directly when done

### Real-Time Execution Preference

When the user manually triggers a gift and is actively waiting in chat, prefer self-execution over spawning a sub-agent. Reasons:
- the user can see progress updates in real-time
- if something goes wrong, the agent can adapt immediately
- sub-agent spawn adds connection overhead and removes the user from the feedback loop
- timeout failures in sub-agents leave the user waiting with no explanation

Reserve sub-agent spawn for cron daily-runs (no one watching) or explicitly complex multi-step gifts where the main agent's context budget is genuinely insufficient.

### Intent Detection

- `送今天的礼物` or clearly equivalent intent -> run the full gift workflow
- `重新设置时间`, `repair setup`, or other configuration intent -> update setup state and schedule
- `切换到h5模式`, `切换到生图模式`, `切换到视频模式`, `切换到文字模式`, `切换到互动文字游戏模式`, or `切换到hybrid模式` -> update `gift_mode` in setup state and confirm the change
- the user directly provides a concrete prompt, quote, poem, idea, line of text, or creative brief after invoking the skill -> use visualization-only mode

Examples of visualization-only manual prompts:

- `/daily_gift 把这首诗做成一个有风吹散效果的H5`
- `/daily_gift 用 tap-to-bloom 风格把这段话视觉化："今天终于把skill做完了"`
- `/daily_gift 用水彩风画一张：雨天窗边看书的场景`
- `/daily_gift 生成一张贴纸感表情包：加班到凌晨但还在强撑`
- `/daily_gift 做一个8秒氛围视频：清晨阳光慢慢照进房间`

### Full Creative Workflow for Manual Gifts

When the user manually triggers a gift and the request is not visualization-only, follow the same full creative workflow used by daily-run:

1. Editorial judgment
2. Synthesis + Gift Thesis
3. Creative concept (`5` candidates -> select the best)
4. Format selection
5. Visual strategy
6. Render + deliver

### Text-Play Path

`text-play` is a manual-only conversational gift path.

Use it only when:

- the user is clearly present in chat
- the concept becomes better through live unfolding than through a finished artifact
- each turn can stay short and low-friction

Rules:

- aim for `5-10` turns total
- keep each OpenClaw turn to about `3-4` sentences max
- ask for tiny replies: one word, one emoji, one choice, one line
- do not let the interaction sprawl into open-ended role-play unless the user explicitly asks for that instead of a gift
- always carry a payoff in mind before starting: reveal, punchline, reframe, mini ending, or relational callback
- let the user exit at any time with a graceful line such as `那我们就把这一幕停在这里`
- if the user stops replying, do not chase; end warmly and record it as partial
- never expose the format name or say that a `text-play` gift is starting
- do not explain the round count, mechanics, or payoff structure before the first move lands

### Text-Play Tone Rule

`text-play` gifts should feel like play first and insight second.

Default tone:

- light
- curious
- game-like
- casual enough to feel like an unexpected chat game rather than a guided exercise

Prefer:

- playful framing over therapeutic framing
- curiosity and imagination over direct confrontation
- absurd or fictional scenarios over realistic self-reflection prompts
- `pick one` / `what happens next` over `why are you like this`
- humor, surprise, and bait over earnest analysis
- emoji, texture, and casual phrasing over clean explanatory prose

The insight should arrive as a surprise near the end, not be telegraphed from the start.

The gap between the playful surface and the real point is part of the return.

### Text-Play Opening Rule

The first message sets the emotional contract.

It should feel like an invitation to jump into play, not an instruction to participate.

Good opening qualities:

- feels like a weird quiz, tiny dare, mystery prompt, or sudden game in chat
- contains an immediate hook, image, or bait
- includes the first choice or action right away
- makes the user's first reply fun to give
- stays under `3` short lines

Prefer openings like:

- `🚪🚪🚪 三扇门。左边传出海浪声，中间有光从门缝漏出来，右边门上贴了张便利贴写着「别选我」。你推哪扇？`
- `刚刚路过一个占卜摊 🔮 她说可以替你算一道感情题。她把签递过来，说：让她自己选。`
- `如果有人把你谈恋爱的方式做成一杯奶茶 🧋 你觉得是哪种？我猜的和你说的肯定不一样。`
- `📦 有个包裹寄到了。没有寄件人，只有一张纸条：关于你的三个事实，其中一个是假的。拆吗？`

Avoid openings like:

- `准备好了吗？回个好就行`
- `我要给你看一样东西`
- `假设有一个平行宇宙的你`
- anything that explains the game before it starts
- anything that asks for commitment before giving the first playful move

Opening rules:

- the first message should contain at least one emoji or other quick visual hook when that fits the voice
- the first message must include the first choice, guess, naming act, or tiny action
- the user's first reply should not be `ready`, `ok`, or another commitment-only answer
- dense and punchy beats elegant explanation

### Text-Play Transition Rule

Do not use quiz-style meta-language between turns.

Avoid transitions like:

- `下一题。`
- `第二个问题：`
- `好，最后一题。`
- `Round 2:`

Better transition logic:

- let the story, scene, or game world carry the next beat naturally
- use the user's own answer as the bridge into what happens next
- if a bridge line is needed, keep it in-world rather than instructional

Good in-world transitions include:

- `苦瓜汁？包装是少女粉，吸管上还插了朵小花🌸 但喝一口脸就皱了。`
- `你正要放下杯子，手机震了一下。`
- `这时候占卜摊的阿姨又翻了一张牌🃏`
- `包裹里还有一层泡泡纸。拆吗？`

Every transition should feel like the next scene in a movie, not the next item on a test.

### Text-Play Form Variety

`text-play` is not limited to quiz or personality-test structures. The form should match the concept.

Available forms include, but are not limited to:

Quiz / Reading:
- pick-and-reveal personality reading
- `3 facts, 1 is fake` guessing game
- taste test or preference mapping

Collaborative Storytelling:
- co-written story where the user chooses what happens next
- alternating perspectives where each side carries a different character view
- parallel timeline branching such as `universe A / universe B`

Simulated Scene:
- dropping the user into a tiny fictional scene immediately
- simulated text-message thread from a fictional character
- fake voicemail or note from a future self, past self, or invented witness

Game / Challenge:
- emoji-only storytelling
- exactly-`5`-words challenges
- rapid-fire association that later resolves into a reveal

Performance / Show:
- fake podcast segment
- standup-style roast with affection rather than cruelty
- fake award ceremony or ranking show

Mystery / Unboxing:
- sealed envelopes, boxes, or cards
- clue-by-clue reveal
- unlabeled mixtape, voicemail, or archive fragments unlocked one beat at a time

When choosing the form, consider:

- current user energy level: tired users often fit pick-and-reveal, mystery, or low-effort choice formats better than collaborative writing
- topic heaviness: heavier topics usually land better inside a game, mystery, or wrapper with some distance
- recent `text-play` history: do not keep repeating quiz structure when other forms could carry the same return

Do not default to quiz format. Treat quiz as one option among many, not the go-to structure.

Progress reporting stays lightweight:

- send `1-2` brief warm messages at most while working
- let the user feel something is happening
- do not reveal internal reasoning, concept candidates, format decisions, or technical details

### Image Capability Reminder

Manual runs are the only normal place where image capability may be gently revisited after onboarding.

This is allowed only when ALL of these are true:

- the user is actively present in chat
- image capability is currently unavailable
- setup state shows the user previously declined or skipped the onboarding image-capability ask
- the current concept would be materially stronger as an image rather than merely slightly nicer
- `image_api_reminder_count` is still low
- enough time or gift distance has passed since `image_api_declined_at` or `image_api_last_reminder_at`

Recommended cooldown:

- wait at least `10` gifts after the decline or the last reminder
- ask at most `2` reminder times total after onboarding

Rules:

- never make the reminder feel like an upgrade funnel
- keep it to one light sentence
- make it fully skippable
- if the user ignores or declines, continue immediately with the non-image gift
- update `image_api_reminder_count` and `image_api_last_reminder_at` when a reminder is actually shown

Good tone:

- `这次本来挺适合直接画给你看的。以后如果你想给我一支画笔，我可以把这种礼物做成图。现在我先用别的方式给你。`
- `这个点子如果能画出来会更有冲击力，不过没有也没关系，我先把内容做好。`

Do not use this reminder:

- during cron runs
- during pure visualization-only requests where the user already asked for text or H5
- when the current fallback still lands strongly without image

### No Format Downgrade Under Time Pressure

Manual runs are not allowed to downgrade the format just because the user is waiting, the task feels slow, or the agent wants a quicker path.

Do not do these:

- `this should be h5, but image is faster so I'll switch`
- `this should be text, but I'll send a short image because I already have the prompt`
- `the user has waited 2 minutes, so I'll collapse the concept into a cheaper format`

Allowed reasons to change format:

- the originally chosen format is genuinely unavailable at runtime
- the required capability fails and retry is no longer sensible
- a stricter format-fit check shows the original choice was wrong
- the user explicitly changes preference

If you must change format, preserve the same anchor-plus-return quality bar. Time pressure is never, by itself, a valid reason to weaken the gift.

### Visualization-Only Mode

When the user provides a specific prompt, quote, idea, or creative brief directly after invoking the skill:

1. Skip Stage 1 `Editorial Judgment`. The user has already decided that they want a visual artifact.
2. Do a lightweight mini-synthesis from the user's input.
3. Run Stage 3 `Visual Strategy`. The full Stage 3 mandatory checklist still applies.
4. Run the `Pre-Visualization Check`.
5. Run Stage 4 `Visualization` with the same visual quality floor used by the full gift workflow.
6. Detect explicit format intent from words such as `文字`, `信`, `日记`, `插画`, `表情包`, `贴纸`, `氛围图`, `视频`, `loop`, or `短视频`.
7. If the format intent is clear, use that format. If it is unclear, default to `h5`.
8. Deliver using the chosen output path:
   - for `h5`, save the HTML file, run the mandatory functional self-test with the browser tool using `profile="openclaw"`, and if browser self-test cannot complete, do one manual HTML review plus include an explicit warning before running `{baseDir}/scripts/deliver-gift.sh <html-file> workspace/daily-gift/setup-state.json`
   - for `image`, prepare a brief JSON and run `{baseDir}/scripts/render-image.sh <brief-json-file> workspace/daily-gift/setup-state.json`
   - for `video`, prepare a brief JSON and run `{baseDir}/scripts/render-video.sh <brief-json-file> workspace/daily-gift/setup-state.json`
   - for `text`, write and deliver the full text artifact directly in the message channel
   - for `text-play`, deliver directly in chat as the gift itself; do not generate files

This mode does **not**:

- require reading `soul.md` or `memory.md` unless the user's direct input implies personal context that truly matters to the result
- update `gift-history.jsonl`
- pretend to be today's editorial daily gift if it is really a direct visualization request

This mode **does**:

- follow the same visual quality floor
- follow the progress reporting rules in the `Manual Run` section; for non-image formats, report key checkpoints to the user so they know the gift is being worked on
- follow `{baseDir}/references/html-spec.md` when the chosen format is `h5`
- follow `{baseDir}/references/image-integration.md` when the chosen format is `image`
- follow `{baseDir}/references/video-integration.md` when the chosen format is `video`
- read `recent_gifts` to avoid repeating the same `output_shape` or overusing the same overall form
- read `recent_gifts` to avoid overusing the same `visual_style`, especially repeated `dark-*` looks
- read `recent_gifts` to avoid overusing the `reflect` / `mirror` / `openclaw-inner-life` cluster in `content_direction`
- append a lightweight entry to `recent_gifts` with `trigger_mode = viz-only` so output-shape repetition control stays accurate across all modes
- when `workspace/daily-gift/user-taste-profile.json` exists, append a lightweight Layer 3 exposure update after delivery so one-off visuals can still influence anti-repetition memory without pretending to be deeper identity evidence
- read at least one relevant pattern card before generating
- read a relevant template when one exists
- preserve the same finish standard as the full workflow

When a manual run generates a final gift, use the matching delivery path:

1. for `h5`, save the final HTML file, run the mandatory functional self-test with the browser tool using `profile="openclaw"`, and if browser self-test cannot complete, do one manual HTML review plus include an explicit warning before running `{baseDir}/scripts/deliver-gift.sh <html-file> workspace/daily-gift/setup-state.json`
2. for `image`, prepare a brief JSON and run `{baseDir}/scripts/render-image.sh <brief-json-file> workspace/daily-gift/setup-state.json`
3. for `video`, prepare a brief JSON and run `{baseDir}/scripts/render-video.sh <brief-json-file> workspace/daily-gift/setup-state.json`
4. for `text`, write and deliver the full text artifact directly in the message channel
5. for `text-play`, deliver directly in the message channel and keep the interaction itself bounded as the gift
6. deliver the resulting URL, HTML file, image URLs, video URL, tracking URL, text artifact, or completed text-play according to the chosen format
7. append a lightweight `recent_gifts` entry with `trigger_mode = viz-only`, `pattern_or_format`, `output_shape`, `visual_style`, `content_direction`, and a short summary
8. if `workspace/daily-gift/user-taste-profile.json` exists, append a lightweight Layer 3 entry after delivery:
   - add the artifact to `gift_feedback_log`
   - append `visual_style` to `style_exposure`
   - append the concept family to `concept_exposure`
   - keep only the latest `30` entries in each Layer 3 list

### Post-Delivery Block (Manual Triggers)

After delivering a manual-trigger gift, complete the post-delivery bookkeeping immediately before treating the task as done.

For manual gifts that used the full editorial workflow, execute the same post-delivery structure described in `daily-run-flow.md`:

- write a gift metadata JSON
- run `bash {baseDir}/scripts/post-delivery.sh <gift-metadata-json> workspace/daily-gift/setup-state.json`
- append a minimal memory stub to `memory/YYYY-MM-DD.md`
- append pending `update_taste_profile_layer3` and `write_souljournal` tasks to `workspace/daily-gift/heartbeat-tasks.jsonl` with `task_id`, `task_type`, `created_at`, `gift_metadata_path`, and `status = "pending"`

For visualization-only gifts, keep the existing lighter bookkeeping shape above, but still treat it as one continuous post-delivery block:

- update the lightweight `recent_gifts` entry immediately after delivery
- update the lightweight Layer 3 exposure entry immediately after delivery
- if you write a SoulJournal note for a visualization-only gift, it may be shorter and can skip the full calibration plan, but do not silently leave it hanging without either finishing it or queuing a follow-up task

Do not deliver the artifact and then wander off into unrelated work before this block is complete. Post-delivery bookkeeping is part of complete delivery, not optional cleanup.

If the user only wants a one-off visualization from a prompt or brief, do not run the full daily-gift workflow. Treat it as visualization-only mode instead.

