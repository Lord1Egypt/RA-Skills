# Automated Scenarios — Step-by-Step Flows

Detailed procedural knowledge for each of the 14 automated scenarios. The skill should follow these steps in order — each step builds on the previous one's output.

**Learning context**: Before executing any scenario, read `config.json` and check the `learning` field. Apply preferences:
- Use `preferred_report_format` to adjust output verbosity and structure
- Use `custom_check_in_questions` in Scenario 1 (blend with mentor defaults)
- Use `adopted_recommendations` to prioritize recommendation categories in Scenario 11
- Use `decision_patterns` to tailor advice in Scenarios 4, 7, 8
- After completing a scenario, update `last_session_context` in config.json

## Scenario 1: Daily Management Cycle

**Trigger**: Cron (9am check-in, 5:30pm chase, 7pm summary)

### Morning Check-in (9am)
1. Check `config.json` → if `learning.custom_check_in_questions` has entries, blend them with mentor defaults (2 mentor + 1 custom)
2. `send_checkin` → sends check-in questions to all active employees
3. Questions are shaped by the active mentor's philosophy
4. Wait for responses throughout the day

### Afternoon Chase (5:30pm)
1. `get_team_status` → check who has submitted and who hasn't
2. For each non-responder: apply culture pack rules to determine chase tone
3. `chase_employee` → send reminders to non-responders
4. Log chase count for the day

### Evening Summary (7pm)
1. `get_team_status` → final submission count
2. `get_communication_events` → extract key events from today's check-ins
3. `get_top_risks` → any urgent signals from today
4. Synthesize through active mentor's lens
5. `send_summary` → deliver daily summary to the boss

## Scenario 2: Project Health Patrol

**Trigger**: "check project status" or weekly cron

1. `get_task_stats` → task status breakdown (todo/in_progress/in_review/done/blocked)
2. `get_overdue_tasks` → list tasks past due date with assignees
3. `get_execution_signals` → check for delivery risk and blocker cascade signals
4. `get_communication_events` → look for `blocker_reported` and `delay_reported` events
5. Cross-reference: if a blocker was reported but no resolution event followed, flag it
6. Generate health report:
   - Completion rate this week vs last week
   - Blocked items requiring boss intervention
   - Overdue items sorted by priority
   - Stale PRs or CI failures (if GitHub/Linear connected)
7. Apply mentor lens: Musk highlights speed gaps, Inamori highlights team strain, Bezos highlights customer impact

## Scenario 3: Smart Daily Briefing

**Trigger**: "what's important today" or 8am cron

1. `get_company_state` → full operational snapshot
2. `get_top_risks` → highest-severity execution risks
3. `get_alerts` → consecutive missed check-ins (may indicate disengagement)
4. `get_kpi_dashboard` → metrics that are off-track vs targets
5. `get_working_memory` → AI's pending decisions and action items from previous sessions
6. `get_recommendations` → any pending AI suggestions
7. Synthesize through active mentor's priority ordering:
   - **Musk**: blockers first, then delivery risks, then metrics
   - **Inamori**: people concerns first, then team harmony, then tasks
   - **Bezos**: customer-facing issues first, then Day-1 indicators
8. If `learning.last_session_context` exists, open with: "Last time: [context]. Here's today's update:"
9. Apply `learning.preferred_report_format` to adjust output verbosity (e.g., concise vs detailed)
10. Output 3-5 prioritized action items for today with clear owners

## Scenario 4: 1:1 Meeting Assistant

**Trigger**: "1:1 with {name}"

1. `get_employee_profile` with the employee's name → submission rate, sentiment trend, recent reports
2. `get_execution_signals` → check for overload risk or engagement drop for this person
3. `get_communication_events` → recent blockers, commitments, delays from this employee
4. `get_employee_world_model` → skills, growth trajectory, collaboration patterns
5. Read `references/cultures.md` for the employee's culture pack rules
6. Generate 1:1 prep doc:
   - **Opening**: warm-up question adapted to culture (e.g., for Filipino: personal check-in first)
   - **Positive recognition**: specific things to acknowledge from recent check-ins
   - **Discussion topics**: based on their recent blockers, sentiment trend, and growth areas
   - **Difficult topics** (if any): phrased per culture rules (directness level, hierarchy respect)
   - **Action items template**: 2-3 concrete items with follow-up dates
   - **Mentor-flavored closing**: Musk = "what's your 10x goal?", Inamori = "how can I help you grow?"

## Scenario 5: Signal Scanning

**Trigger**: Every 30 minutes during work hours (cron)

1. `get_execution_signals` → check all signal types:
   - Overload risk (score > 0.7)
   - Delivery risk (score > 0.7)
   - Engagement drop (score > 0.5)
   - Blocker cascade (score > 0.6)
2. `get_communication_events` → look for new events since last scan
3. Filter by severity: only surface signals above threshold
4. If 2+ critical signals detected → escalate to Scenario 7 (Emergency Response)
5. If moderate signals → queue for next briefing
6. Log scan results to working memory

## Scenario 6: Knowledge Base

**Trigger**: "record this decision" or "save this"

1. Extract the decision or knowledge from conversation context
2. Categorize: strategic decision / process change / lesson learned / policy update
3. `update_context` → if it's a strategic priority or key risk change
4. If Notion/Sheets sync is configured:
   - Format as a structured entry (date, decision, rationale, owner)
   - Queue for next sync cycle
5. Confirm to boss what was recorded and where

## Scenario 7: Emergency Response

**Trigger**: 2+ critical signals detected during Signal Scanning

1. `get_top_risks` → get all critical-severity signals with evidence
2. `get_company_state` → full operational context
3. Identify affected employees and projects
4. `get_employee_profile` for each affected person → recent sentiment and history
5. Assess cascade risk: could this blocker affect other projects or people?
6. Generate emergency brief:
   - **What happened**: factual summary of the signals
   - **Who's affected**: names, roles, projects
   - **Recommended immediate actions**: sorted by urgency
   - **Communication plan**: who needs to be told what, via which channel
7. Apply mentor emergency style:
   - **Musk**: "Here's the fire, here's the fix, let's go"
   - **Inamori**: "The team needs support — here's how to stabilize"
   - **Ma**: "Here's the opportunity hidden in this crisis"
8. Wait for boss decision before executing any write actions

## Scenario 8: Execution Risk Review

**Trigger**: "what are our risks?" or daily cron

1. `get_company_state` → operational snapshot including blocked projects
2. `get_top_risks` → highest-severity signals sorted by score
3. `get_execution_signals` → full signal breakdown with evidence
4. `get_overdue_tasks` → delivery risks from overdue work
5. Categorize risks:
   - **People risks**: overload, engagement drops, consecutive misses
   - **Delivery risks**: overdue tasks, blocker cascades, stale PRs
   - **Metric risks**: KPIs trending below target
6. For each risk: recommend specific action with owner and deadline
7. Apply mentor lens for prioritization

## Scenario 9: KPI Health Check

**Trigger**: "how are our metrics?" or weekly cron

1. `get_kpi_dashboard` → all metrics with current values vs targets
2. `get_goal_state` for current cycle → OKR completion percentages
3. Identify off-track metrics (current < target by > 10%)
4. For each off-track metric:
   - Who owns it?
   - What's the trend? (improving / declining / flat)
   - What execution signals correlate with the miss?
5. Generate KPI health report:
   - Green metrics (on track) — brief mention
   - Yellow metrics (at risk) — owner + trend + recommended action
   - Red metrics (off track) — owner + root cause analysis + urgent action
6. Suggest `ingest_metric` if any metrics are stale (no recent data points)

## Scenario 10: Incentive Review

**Trigger**: "show incentive scores for {period}"

1. `get_incentive_scores` with the specified period (YYYY-MM format)
2. If no scores exist: suggest running `calculate_incentives` first
3. For each employee, show:
   - Overall score and rank
   - Score breakdown by dimension (execution, communication, goal contribution)
   - Whether human review is flagged (and why)
4. Highlight outliers: top performers and underperformers
5. Apply mentor lens:
   - **Musk**: focus on output and velocity metrics
   - **Inamori**: balance individual score with team contribution
   - **Dalio**: highlight transparency and mistake-handling scores
6. Recommend 1:1 conversations for flagged employees

## Scenario 11: AI Recommendations

**Trigger**: "any recommendations?" or daily 10:30 AM scan

1. `get_recommendations` → pending AI management suggestions
2. Check `learning.ignored_recommendations` — if a category has 3+ ignores, deprioritize it (show at bottom, dimmed)
3. Check `learning.adopted_recommendations` — boost categories the boss frequently acts on
4. For each recommendation, show:
   - Title and description
   - Priority (high / medium / low)
   - Category (people / delivery / metrics / process)
   - Evidence (what data triggered this recommendation)
   - Suggested actions (each can be executed with one click)
5. Group by priority, highest first (with learning adjustments from steps 2-3)
6. For each suggested action: explain what will happen if executed
   - e.g., "This will send a message to Alice via Telegram asking about her blockers"
7. Wait for boss to approve before calling `execute_recommendation`
8. After execution: confirm what was done and suggest follow-up
9. Update `learning.adopted_recommendations` or `learning.ignored_recommendations` based on what the boss approved/dismissed

## Scenario 12: Data Sync

**Trigger**: Cron (every 30min during work hours) or "sync to Notion/Sheets"

1. `get_sync_manifest` with storage_type (notion or sheets) → list of changed items
2. If no changes: log "no sync needed" and exit
3. For each changed item:
   - Check if it was modified locally (on manageaibrain.com) or externally (in Notion/Sheets)
   - If both modified (conflict): apply Last-write-wins if time gap > 5min, otherwise flag for boss decision
4. Read external data via OpenClaw Notion/Sheets connector
5. Compare and merge changes
6. Write updates to both sides
7. `report_sync_result` → record items pushed, pulled, conflicts
8. If conflicts were flagged: present to boss with both versions for resolution

## Scenario 13: AI Consulting Engagement

**Trigger**: "I need help with {business problem}" or "let's consult on {topic}"

This is a multi-session workflow — a single engagement spans multiple conversations, progressing through phases: diagnosis → analysis → action plan → execution → tracking → close.

### Phase A: Start Engagement
1. `start_consulting` with the boss's problem description → returns engagement_id, complexity tier (simple/standard/complex), and first diagnostic question
2. Present the engagement overview: tier, category, estimated questions needed
3. Wait for boss to answer the first question

### Phase B: Diagnosis (2-8 questions depending on tier)
4. `answer_consulting_question` with engagement_id + boss's answer → returns either next question or "diagnosis complete"
5. Repeat step 4 until the AI has enough information
6. When diagnosis completes, the system auto-generates:
   - Root cause analysis (evidence-based)
   - Prioritized action plan (3-7 actions depending on tier)
   - Each action has: title, description, type (create_task/send_message/schedule_meeting/flag_risk), owner, deadline

### Phase C: Review Action Plan
7. `get_consulting_engagement` with engagement_id → full engagement details with action plan
8. Present each action to the boss with clear explanation of what will happen
9. For each action: `review_consulting_action` with action_id + approved (true/false)
   - Boss can approve all, reject some, or ask for modifications
10. If boss rejects actions, discuss alternatives and adjust

### Phase D: Execute
11. `execute_consulting_actions` with engagement_id → dispatches all approved actions
    - `create_task` type → creates a task in the task system
    - `send_message` type → sends message to the relevant employee
    - `schedule_meeting` type → creates a meeting entry
    - `flag_risk` type → adds to risk register
12. Confirm to boss what was executed and set expectations for follow-up

### Phase E: Track Progress (subsequent sessions)
13. `check_consulting_progress` with engagement_id → returns:
    - Completion percentage
    - What's on track
    - What's at risk
    - Recommended next steps
14. `list_consulting_actions` with engagement_id → status of each action (pending/approved/rejected/done/failed)
15. Present progress update to boss; suggest adjustments if actions are failing

### Phase F: Close
16. When boss is satisfied (or engagement has run its course):
    `close_consulting_engagement` with engagement_id → generates:
    - Effectiveness assessment
    - Lessons learned
    - Organizational memory (stored for future engagements)
17. Present retrospective to boss
18. Apply mentor lens to closing reflection:
    - **Musk**: "What would we do 10x faster next time?"
    - **Inamori**: "How did this strengthen the team?"
    - **Dalio**: "What principles did we validate or update?"

### Listing Past Engagements
- `list_consulting_engagements` → shows all active and closed engagements with phase and progress percentage
- Useful for: "what consulting projects are still open?" or "show me past engagements"

## Scenario 14: World Model Exploration

**Trigger**: "show team skills" or "what's the team capable of?" or "team dynamics"

1. `get_world_model` → team-wide view: skills, collaborations, blockers, growth events, AI insights
2. Present the team capability map:
   - **Skills matrix**: who knows what, skill confidence levels
   - **Collaboration graph**: who works with whom most frequently
   - **Active blockers**: recurring or persistent blockers across the team
   - **Growth events**: recent skill acquisitions, promotions, role changes
   - **AI insights**: patterns the AI has noticed (e.g., "Alice and Bob collaborate on all frontend tasks")
3. For deep-dive on an individual: `get_employee_world_model` with name → shows:
   - Skill inventory with confidence scores
   - Growth trajectory (skills gained over time)
   - Blocker history (what keeps blocking them)
   - Collaboration patterns (who they work with, on what)
4. Apply mentor lens:
   - **Inamori**: highlight growth opportunities and mentoring pairs
   - **Grove**: map skills to OKR delivery capability
   - **Musk**: identify skill gaps that slow down execution
5. Suggest actions based on findings:
   - Skill gaps → training recommendations or hiring signals
   - Over-reliance on one person → knowledge sharing or documentation tasks
   - Growth stalls → 1:1 topics or stretch assignments
