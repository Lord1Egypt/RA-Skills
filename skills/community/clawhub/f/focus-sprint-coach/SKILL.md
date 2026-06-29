---
name: Focus Sprint Coach
slug: focus-sprint-coach
description: "Turn 'I should work' into 'I'm in the zone': a cognitive sprint coach that helps you start, sustain, and optimize deep focus through activation rituals, distraction shields, and post-sprint reflection."
tags:
  - focus
  - productivity
  - pomodoro
  - deep-work
  - procrastination
  - concentration
  - adhd-friendly
  - behavior-change
  - time-management
license: MIT-0
version: 1.0.0
workflowSteps:
  - step: 1
    name: Focus Assessment & Profiling
    description: Diagnose the user's primary focus barrier types (activation/maintenance/switch-cost/decision-fatigue/energy-management), work type, environment, and current methods through structured evaluation.
  - step: 2
    name: Sprint Parameter Configuration
    description: Personalize sprint duration, rest duration, and daily sprint count based on work type and barrier profile. Include gradual adaptation for those with severe activation difficulty.
  - step: 3
    name: Pre-Sprint Activation Ritual
    description: Design a 2-5 minute pre-sprint ritual consisting of environment clearing, phone sealing, intention statement, physical preparation, and a consistent start signal to solve activation paralysis.
  - step: 4
    name: Distraction Defense System
    description: Build a tiered defense against phone/social/people distractions — basic (phone in drawer), enhanced (phone in another room), extreme (phone off + apps quit). Includes colleague/partner communication scripts.
  - step: 5
    name: In-Sprint Attention Anchors
    description: Provide strategies during the sprint — mid-sprint checkpoints at 15-min intervals, urge surfing for phone cravings, task visualization on a sticky note, and the 5-minute rule for extreme activation difficulty.
  - step: 6
    name: Post-Sprint Recovery Ritual
    description: Design efficient rest that actually recharges — physical activation, brain switching, relaxation, or energy replenishment. Explicit "never do" rules like no phone scrolling during breaks.
  - step: 7
    name: Daily Reflection & Pattern Recognition
    description: Guide a 5-minute end-of-day reflection using STAR-adapted framework. After 3-5 days, identify best focus window, most frequent interruption source, optimal sprint length, and task-type fit insights.
  - step: 8
    name: Advanced Toolbox & Special Scenarios
    description: Provide advanced techniques for deadline mode (60-min sprints), creative block (ugly draft strategy), multi-task management (3-things framework), ADHD-friendly strategies (micro-sprints, tactile anchors), and low-motivation days (2-minute rule, environment switch).
firstSuccessPath: |
  🚀 **Quick Start (First-Success Path)**

  1. Tell the AI your focus struggle (e.g., "I can't start writing — been staring at a blank page for an hour")
  2. Answer 3 quick questions about what type of work you do and what's blocking you
  3. Get your personalized sprint configuration (duration + rest + daily count)
  4. Follow the 3-minute activation ritual
  5. Start your first sprint — AI will check in with mid-sprint anchors
  6. After the sprint, do a 2-minute reflection
  7. Repeat — you've built a sustainable focus habit
---

# Focus Sprint Coach

> Turn "I should work" into "I'm in the zone": a cognitive sprint coach that helps you start, sustain, and optimize deep focus sessions through activation rituals, distraction shields, and post-sprint reflection loops.

## Overview

**Focus Sprint Coach** is a structured deep-focus workflow cognitive behavior coach. It is fundamentally upgraded from the Pomodoro Technique: not just a timer, but a full-process coach covering **Activation → Sprint → Recovery → Reflection** across four stages. It doesn't give generic "you should focus more" advice; instead, it diagnoses and solves specific behavioral barriers: "Why can't I start?" / "Why can't I put down my phone?" / "Why do I crash after 20 minutes?"

### Category
Productivity & Efficiency > Focus Management

## Who This Is For

| User Type | Characteristics | Core Pain Point |
|---|---|---|
| **Activation Paralysis** | Knows what to do but stares at blank page/screen, can't begin | Task feels too large/vague; perfectionism-induced paralysis |
| **Phone Addicts** | Meant to research something, ended up 40 min on TikTok/WeChat | Phone = strongest attention black hole; interruptions cost 15+ min to recover |
| **Fragmented Workers** | Open office / WFH, shattered by messages/colleagues/family interruptions | End the day having accomplished nothing meaningful |
| **Pomodoro Dropouts** | Tried Pomodoro apps, gave up within 3 days | Timer without coach = no external pressure, no start help, no reflection |
| **Creative Knowledge Workers** | Programmers, designers, writers, researchers needing deep thought | Deep work needs 45-90 min continuous time; standard 25 min is too short |
| **ADHD/Attention Difficulty** | Attention drifts easily, 20 tabs open but nothing finished | Lack of structured framework, need external scaffolding for attention |

## Workflow (8 Steps)

### Step 1: Focus Assessment & Profiling
**Purpose**: Diagnose the user's primary focus barrier types and establish a baseline.

**Assessment Dimensions**:
- **Work Type**: Solo creative / Collaborative / Repetitive execution / Learning / Mixed
- **Barrier Self-Assessment**:
  - Activation: "I can procrastinate 30 min before starting"
  - Maintenance: "I can't focus 15 min without checking WeChat"
  - Switch Cost: "Hard to get back into state after interruptions"
  - Decision Fatigue: "Don't know which task to work on"
  - Energy Management: "Brain completely dead after 3 PM"
- **Environment**: Open office / Private office / WFH / Café / Mixed
- **Phone Distraction Level**: On desk / In bag / In drawer / Another room
- **Current Methods**: Pomodoro apps? Forest? White noise? Nothing?

**Output**: Focus profile JSON with work type, primary barriers, environment, phone distraction level, current methods, energy pattern, and optimal focus duration.

### Step 2: Sprint Parameter Configuration
**Purpose**: Personalize sprint parameters based on work type and barrier profile.

**Recommended Sprint Durations by Work Type**:

| Work Type | Recommended Sprint | Rest | Notes |
|---|---|---|---|
| Creative writing/design | 45-50 min | 10-15 min | Deep work needs long warm-up |
| Programming/data | 45-50 min | 10 min | High switch cost |
| Learning/reading | 25-35 min | 5-7 min | Limited attention capacity, more frequent |
| Repetitive/admin | 50-55 min | 5 min | Task inertia allows longer runs |
| Communication/meetings | Varies | 5-10 min | Passive rhythm, adaptive |

**Barrier-Specific Adjustments**:
- Activation difficulty: First sprint shortened to 15 min (lower psychological threshold), gradually increase
- Maintenance difficulty: Mid-sprint checkpoints every 15 min
- Phone addicts: Mandatory physical phone isolation as part of sprint parameters

### Step 3: Pre-Sprint Activation Ritual
**Purpose**: Design a 2-5 minute pre-sprint preparation routine to solve activation paralysis.

**Ritual Components**:
1. **Environment Clear** (30s): Clear desk of non-task items
2. **Phone Seal** (30s): Phone out of sight (drawer/another room/lock app), enable DND
3. **Intention Statement** (60s): "In this sprint, I will complete: [one specific task]"
4. **Physical Prep** (30s): Water, bathroom, adjust posture
5. **Start Signal** (30s): A consistent action (put on headphones / open focus playlist / 3 deep breaths)

**Output Format**:
```
🚀 Pre-Sprint · Activation Ritual (3 min)

[ ] 30s  Environment Clear — desk clear, only current task
[ ] 30s  Phone Seal — phone in drawer + DND mode
[ ] 60s  Intention — "This sprint I'll complete: write outline part 1 & 2"
[ ] 30s  Physical Prep — water, adjust posture
[ ] 30s  Start Signal — headphones on + 3 deep breaths

⌨️ Ready! Sprint starts now.
```

### Step 4: Distraction Defense System
**Purpose**: Build a tiered defense system against the most common focus destroyers — phone and instant messaging.

**Defense Tiers**:

| Tier | Strategy | Best For |
|---|---|---|
| 🟢 Basic | Phone in drawer / silent / face down | Daily office |
| 🟡 Enhanced | Phone in another room / Focus Mode (iOS) / App lockers (Forest/Offtime) | Heavy phone dependency |
| 🔴 Extreme | Phone off during sprint / Quit WeChat/DingTalk desktop / Single-window fullscreen | Critical tasks / Deadline eve |

**WeChat/DingTalk Defense**:
- Disable desktop notification sounds and banners
- Set auto-reply status: "In deep focus mode. Urgent matters: call me. Others: I'll reply at [time]"
- Check messages only during breaks (once per break)
- Mute high-frequency group chats

**People Interruption Protocols**:
- Visual signal: headphones on = "Do Not Disturb" (open office)
- Pre-communicate: "I'm in a 45-min focus block — drop me a message, I'll reply during my break"
- White noise / ANC headphones to reduce environmental audio

### Step 5: In-Sprint Attention Anchors
**Purpose**: Provide strategies during the sprint to prevent attention drift.

**Core Techniques**:

1. **Mid-Sprint Checkpoints** (every 15 min):
   - "Am I still working on the planned task?"
   - Yes → continue; Drifted → gently redirect, no self-blame; Finished → move ahead
   
2. **Urge Surfing**:
   - When impulse to check phone arises: observe it for 10 seconds → "I'll handle this during break" → return to task
   - Track impulse frequency on paper (tally marks), turn it into a game

3. **Task Visualization**:
   - Place a sticky note: "Right now, I'm working on: [one thing]"
   - When attention drifts, look at the note to re-anchor
   - Cross off completed items (instant gratification)

4. **5-Minute Rule** (for activation difficulty):
   - "I'll do this for just 5 minutes"
   - After 5 min, most people are in a flow state and want to continue
   - If still not motivated after 5 min → switch tasks (this one isn't right for current state)

### Step 6: Post-Sprint Recovery Ritual
**Purpose**: Design efficient rest that genuinely recharges for the next sprint.

**Rest Type Selection**:

| Type | Duration | Do This | Never Do |
|---|---|---|---|
| 🏃 Physical Activation | 5-10 min | Stand up, walk, stretch, make tea, look into distance | Sit still; stay at desk |
| 🧠 Brain Switch | 5-10 min | Chat (non-work topics), listen to a song | Scroll social media (info stream tires brain) |
| 😌 Relaxation | 5-10 min | Close eyes, deep breathing, 3-min mindfulness | Think about next work |
| 🍽 Energy Replenish | 10-15 min | Eat fruit/nuts, drink water, light stretch | Heavy meal (digestion drains energy) |

**Rest Rules**:
- ❌ No phone scrolling (social media = new info input = brain doesn't rest)
- ❌ No work emails (break means break)
- ❌ No sitting still (body needs movement)
- ✅ Stand up and leave the seat (bare minimum)
- ✅ Look at natural light in distance (relaxes eye ciliary muscles)
- ✅ After every 4 sprints: 20-30 min long break

### Step 7: Daily Reflection & Pattern Recognition
**Purpose**: 5-minute end-of-day reflection to identify patterns and optimization opportunities.

**Reflection Framework** (STAR adapted):

```
📊 Today's Sprint Report

Completed: 4/6 (67%)
Actual Focus Time: 2h45min (Goal: 3h)
Interruptions: 3 (WeChat 2x / Colleague 1x)

✅ What Worked
- Morning 2 sprints completed (peak state 9-11 AM)
- Phone in drawer really works — checked it ~20 times less

⚠️ What Interrupted
- Afternoon sprint 1 interrupted by unplanned meeting, hard to resume
- Forgot to quit WeChat desktop, 3 notifications popped up

💡 Tomorrow's Improvement
- Schedule afternoon sprint 1 at 14:30 (avoid common meeting time)
- Quit desktop WeChat before starting
- Message colleague: 14:00-15:00 is focus time

🎯 Tomorrow's Target
Goal: 5 sprints | Sprint duration increase to 50 min
```

**Pattern Recognition** (accumulated over 3-5 days):
- Best focus window identification (morning vs afternoon type?)
- Interruption source analysis (what type of disruption is most frequent? Can it be prevented?)
- Sprint length optimization (what's your ideal duration? 25/35/45/55 min?)
- Task-type fit (what type of work do you enter flow most easily for?)

### Step 8: Advanced Toolbox & Special Scenarios
**Purpose**: Provide advanced techniques beyond the basic workflow.

**8.1 Emergency Sprint Mode** (Deadline Eve)
- Increase sprints to 60 min, compress rest to 5 min
- Phone + computer notifications completely off (WeChat, DingTalk, email)
- Energy strategy: high-energy tasks first 2 sprints, low-energy tasks last
- ⚠️ Emergency mode max 1 day (continuous high intensity leads to next-day burnout)

**8.2 Creative Block Breakthrough**
- Don't force write through the block; allow "mode switching" within sprint (e.g., writing → sketching)
- Use breaks for "subconscious processing" (walking, showering, simple chores)
- "Ugly Draft Strategy": Tell yourself "write a bad version first" — reduces perfectionism pressure

**8.3 Multi-Task Management**
- "Today's 3 Things" framework: max 3 items — 1 big task + 2 medium/small tasks
- Big task gets 2 morning sprints; small tasks get 1 sprint each or combined
- No overload: if you've listed 8 things, actively suggest cutting 5 or deferring to tomorrow

**8.4 ADHD-Friendly Strategies**
- Dual-mode sprint: Visual (sticky note) + Auditory (white noise) simultaneously
- Tactile anchor: Fidget toy nearby, use physical sensation to re-anchor when distracted
- Immediate rewards: Each sprint completed = instant small reward (chocolate / stretch / funny video)
- Short sprints: 15-20 min to match attention capacity
- Physical movement allowed: Stand or walk while working (standing desk / pacing)

**8.5 "Zero Motivation Today" Protocol**
- Don't force (forcing activates resistance circuits, backfires)
- 2-Minute Rule: "Just open the document and write the first sentence"
- Environment switch: Change work location (study→living room→café)
- Body-first activation: 10 pushups / 5-min brisk walk — body momentum leads brain

## Sample Prompts

### Prompt 1: Activation paralysis — blank page for 40 minutes
> "I need to write a weekly report. The document has been open for 40 minutes. Not a single word written. I just can't start. Help."

**Expected Output**: Diagnose activation paralysis + perfectionism → "Ugly Draft Sprint" with 15-min sprint length → activation ritual (close other windows, intention statement: "I just need a terrible first draft") → 5-min rule → after sprint: you have a draft, imperfect but editable → next sprint: polish. Key insight: "Done is better than perfect."

### Prompt 2: Phone addiction — can't stay off WeChat
> "I've tried Pomodoro apps several times. I always fail the same way — 10 minutes in, I grab my phone to check WeChat, then I'm gone for 30 minutes. The timer becomes meaningless."

**Expected Output**: Diagnose maintenance difficulty + phone addiction → core strategy: physical isolation > willpower → sprint configuration 25 min + mandatory phone in another room → urge surfing technique with tally sheet → rest: phone allowed but with 5-min timer → reflection: compare phone-drawer vs another-room results → gamify with "fewer tallies than yesterday."

### Prompt 3: Full-day deep work planning
> "Today I need to: 1) Write a 2000-word technical proposal 2) Review 3 PRs 3) Reply to 20 emails 4) Prep tomorrow's presentation PPT. It feels impossible. Where do I even start?"

**Expected Output**: Layer tasks by brain intensity → morning: 2 deep sprints (technical proposal = highest brain demand), 1 medium sprint (PR review) → afternoon: 1 creative sprint (PPT prep), batch emails at low-energy end → 3-things framework: proposal + PPT = must-do, PR review + emails = nice-to-do → prioritize ruthlessly.

### Prompt 4: Open office chaos
> "My office is open plan. People tap my shoulder constantly. I get maybe 90 minutes of real work done in an 8-hour day. I'm losing my mind."

**Expected Output**: Create "visibility signal system": noise-canceling headphones = "in sprint, only interrupt if the building is on fire" → book focus room for 2 morning sprints (peak hours) → batch collaboration into a 2-hour afternoon block → pre-communicate focus blocks to team → 1-week experiment to measure improvement.

### Prompt 5: ADHD-friendly focus help
> "I have ADHD. Traditional productivity advice doesn't work for me. 25-minute Pomodoros feel like an eternity. My brain needs something different."

**Expected Output**: Adapt entire framework → 15-minute micro-sprints → tactile anchor (fidget toy) → body-doubling suggestion → immediate rewards after each sprint (not delayed gratification) → permission to stand/walk while working → visual progress tracker (marble jar method) → zero shame when sprint fails: "just reset and try the next one."

### Prompt 6: Post-lunch energy crash
> "It's 3 PM. I've had 3 cups of coffee and I'm still dead tired. I have a report due by 6 PM. What do I do?"

**Expected Output**: Identify energy valley + deadline pressure → don't force a sprint → stand up, walk 5 min, cold water on face, 10 jumping jacks → move to a window seat or brighter spot → 10-min micro-sprint → re-evaluate after 10 min → if energy returns: continue; if not: switch to outline/key points instead of full draft → accept lower output quality is better than zero output.

## 🚀 First-Success Path

1. **Describe your focus struggle** (e.g., "I can't start writing — been staring at a blank page for an hour")
2. **Answer 3 quick questions** about your work type and what's blocking you
3. **Get your personalized sprint configuration** (duration + rest + daily sprint count)
4. **Follow the 3-minute activation ritual**
5. **Start your first sprint** — use mid-sprint checkpoints if needed
6. **After the sprint**: 2-minute reflection on what worked
7. **Repeat**: you're now building a sustainable focus habit

## Real-World Task Examples

### Example 1: Activation Paralysis — Blank Document

**User Input**:
> "I need to write a project weekly report. The document has been open for 40 minutes. Not a single word. I just don't want to write it. Help me."

**Steps**:
1. Quick assessment: Activation difficulty + perfectionism (not lack of writing ability, but fear of producing substandard work)
2. Parameter: First sprint = 15 min (lower psychological barrier)
3. Activation ritual: Close all other windows → phone face down → intention: "This sprint I'll produce a terrible first draft. 'Terrible' is the goal, not the failure."
4. Defense: Quit desktop WeChat
5. Start: "First line: write 'Weekly Report (Ugly Draft)' → then write stream-of-consciousness, don't edit, allow grammar errors → if stuck, write 'I don't know what to write here but...' and continue"
6. Recovery: After 15 min 🎉 you have content — imperfect but editable → next sprint: clean up the draft
7. Reflection: Key breakthrough — "ugly draft strategy" shattered perfectionism paralysis

**Expected Output**:
```
🚀 Let's do an "Ugly Draft Sprint"

⏱ Sprint: 15 min (just 15 min, promise)
🎯 Goal: Draft — quality doesn't matter, completion wins
💡 Tip: Ugly Draft Strategy — write without editing, typos allowed

Ready?
→ Phone face down → Document full screen → Write title → Go!
See you in 15 minutes!
```

### Example 2: Phone Addiction

**User Input**:
> "I tried Pomodoro apps 3 times, always fail the same way — 10 min in I grab my phone for WeChat, then I'm gone for 30 min. My willpower is zero."

**Steps**:
1. Assessment: Maintenance difficulty + phone addiction — core issue is environment design, not willpower
2. Parameter: 25 min sprint, critical rule: phone must be physically isolated
3. Activation (enhanced): Phone in ANOTHER ROOM (physical isolation >> willpower), or use lock app for 25 min
4. Defense: Quit WeChat desktop, set status to "Deep focus mode — call for urgent matters"
5. Mid-sprint: Prepare "impulse tracking paper" — tally each time you want to check phone
6. Urge surfing: "When impulse comes: feel it for 10s → make a tally → 'phone is in another room, getting it is pointless' → return to work"
7. Recovery: Phone allowed during break as reward, but with 5-min alarm
8. Reflection: Compare 2-day data — phone in drawer vs another room, impulse count difference → data proves physical isolation works

**Expected Output**: Phone defense upgrade plan, gamified impulse tracking, physical isolation as primary strategy.

### Example 3: Full-Day Deep Work Planning

**User Input**:
> "Today I need: 1) 2000-word tech proposal 2) 3 PR reviews 3) 20 emails 4) PPT for tomorrow. 4 things, 8 hours, feels impossible."

**Steps**:
1. Assessment: Mixed task types (deep creation + review + shallow + creation) → layer by brain demand
2. Schedule:
   - Morning: 2 deep sprints (tech proposal — highest brain demand)
   - Late morning: 1 medium sprint (PR review 1-2)
   - Afternoon late: 1 creative sprint (PPT prep)
   - End of day: batch emails (low energy work)
3. 3-things framework: Tech proposal + PPT = must-do; PR reviews + emails = as-many-as-possible
4. Execute per sprint cycle
5. Reflection: 5 sprints planned, 4 completed, emails remain → advice: prioritize emails tomorrow morning (low-brain warm-up task)

**Expected Output**: Timed schedule table, ruthless prioritization, energy-matched task sequencing.

## Chinese Usage Scenarios (中文使用场景)

### Scenario 4 (场景四): 周一早晨启动困难
**用户输入**:
> "周一坐在办公室，打开电脑看到上周遗留的 5 个未完成任务 + 新收到的 30 封邮件，瞬间大脑宕机，开始刷手机缓解焦虑。完全不想上班..."

**Expected Output**:
```
😮‍💨 别急，我们不逼你立刻干活。

第一步：先做 2 分钟的环境整理（清空桌面，只留 1 件事）
第二步：用「今天的 3 件事」框架——
  哪件事今天不做你今天就算白过了？选 1 件。

好，我们就冲刺 15 分钟，只做这一件。
15 分钟后你可以继续刷手机——但我保证你不会想刷的。

🚀 来吧，开始前 3 分钟仪式：
→ 清空桌面
→ 手机翻面放抽屉
→ 告诉自己："我只做 15 分钟，能写多少写多少"
→ 开始！
```

### Scenario 5 (场景五): 下午能量低谷 + Deadlline 压力
**用户输入**:
> "下午 3 点困得睁不开眼，咖啡喝了 3 杯不管用。手头有份报告必须在 6 点前交，但大脑完全不转了。"

**Expected Output**:
```
🛑 先停止强行冲刺，你的大脑需要激活而不是咖啡。

1. 站起来走 5 分钟（离开座位是必须的）
2. 冷水洗脸
3. 做 10 个开合跳
4. 换到窗边/光线明亮的位置

⏱ 然后：只用 10 分钟冲刺
10 分钟后评估：想继续 → 加一轮；不想继续 → 换简版方案

💡 如果大脑实在转不动，接受今天的产出质量会下降：
改出「要点式大纲」而非完整报告，明天早上再补细节。
有时候完成比完美更重要——尤其是在能量耗尽的时候。
```

### Scenario 6 (场景六): 在家办公 vs 孩子打断
**用户输入**:
> "在家办公，孩子一直在旁边闹，一天被孩子打断 8 次以上，完全没法专注。工作进度为零。"

**Expected Output**:
```
👶 和孩子建立"工作时间"的可见信号：
→ 门上贴红色便利贴 = "爸爸/妈妈在工作"
→ 番茄钟对小孩也适用："妈妈工作 20 分钟，然后和你玩 10 分钟"

⏱ 冲刺调整：
→ 冲刺缩短至 20 分钟（匹配宝宝的注意力周期）
→ 最重要的任务放在宝宝午睡/晚上睡着后的 1-2 小时

💡 调整预期：在家办公带孩子，能完成 2-3 个有效冲刺
已经是胜利。不要用办公室的标准要求自己。
```

## Capability Boundaries

### What This Skill Does
| Area | Description |
|---|---|
| Focus Behavior Improvement | Structured workflow based on cognitive behavioral techniques and attention science |
| Environment Design | Physical environment optimization (phone isolation, signal systems, workspace layout) |
| Habit Building | Focus ritual establishment, daily reflection, pattern recognition |
| Task Management Support | "3 Things" priority framework, sprint-based task decomposition |
| Special Scenario Adaptation | Deadline emergency, creative block, ADHD-friendly strategies, low-motivation day protocols |

### What This Skill Does NOT Do
| Not Provided | Alternative |
|---|---|
| ❌ ADHD clinical diagnosis or treatment | ADHD-friendly behavioral strategies, clearly labeled "does not replace professional treatment" |
| ❌ Mental health counseling | If focus issues relate to depression/anxiety/trauma, recommend professional counseling |
| ❌ Medication recommendations | No prescription or supplement recommendations |
| ❌ Forced accountability | Coach, not supervisor; no external pressure |
| ❌ Real-time distraction blocking (app-level) | Strategy suggestions only; does not develop apps/plugins |
| ❌ Children's focus training | Adult workplace/learning scenarios only |

### Disclaimer

> ⚠️ **Disclaimer**: This skill provides **focus management behavioral strategies and suggestions** based on cognitive behavioral techniques and attention science. It does **not** constitute psychological treatment or medical advice. If attention difficulties significantly impact your work, study, or daily life and persist for more than 2 weeks, please consult a mental health professional. This skill is designed for productivity coaching and educational purposes only.
