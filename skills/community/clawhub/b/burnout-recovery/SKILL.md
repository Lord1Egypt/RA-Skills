---
name: burnout-recovery
description: >-
  Structured burnout recovery protocol based on clinical burnout dimensions. Use when someone is exhausted, cynical about work, feels ineffective, can't disconnect, or says they're burned out.
metadata:
  category: mind
  tagline: >-
    A structured recovery plan for when you're running on empty — identify your burnout stage, set real boundaries, and rebuild energy without quitting everything
  display_name: "Burnout Recovery Protocol"
  openclaw:
    requires:
      tools: [calendar, filesystem]
    install: "npx clawhub install howtousehumans/burnout-recovery"
---

# Burnout Recovery Protocol

Burnout isn't being tired. It's a three-dimensional syndrome: emotional exhaustion, depersonalization, and reduced accomplishment. Recovery requires addressing all three, in order. This skill uses the Maslach Burnout framework adapted into a practical, step-by-step protocol anyone can follow.

## Sources & Verification

- Maslach Burnout Inventory: Maslach, C. & Jackson, S.E., *Maslach Burnout Inventory Manual*, 4th ed., Mind Garden, 2016
- Three dimensions of burnout (exhaustion, depersonalization, reduced accomplishment): Maslach, C. & Leiter, M.P., *The Truth About Burnout*, Jossey-Bass, 1997
- Exercise as burnout intervention: Gerber et al., "Aerobic exercise training and burnout: a pilot study," *BMC Research Notes*, 2013 ([DOI: 10.1186/1756-0500-6-78](https://doi.org/10.1186/1756-0500-6-78))
- Lack of control as burnout predictor: Karasek, R., "Job Demands, Job Decision Latitude, and Mental Strain," *Administrative Science Quarterly*, 1979
- Burnout and depression comorbidity: Bianchi et al., "Burnout-depression overlap," *Clinical Psychology Review*, 2015
- 988 Suicide & Crisis Lifeline: [988lifeline.org](https://988lifeline.org/) — verified active as of March 2026

## When to Use

- User says they're burned out, exhausted, or "running on empty"
- Can't stop thinking about work at night
- Feels cynical, detached, or like nothing they do matters
- Dreads Monday starting from Sunday morning
- Physical symptoms: insomnia, headaches, constant fatigue
- Knows they need to change but doesn't know where to start

## Instructions

### Step 1: Identify burnout stage

**Agent action**: Administer the assessment interactively — ask each question one at a time, record the score, and calculate totals. Store the scores and burnout stage in agent state. Compare to any previous assessments to show trend.

Ask the user these questions and score each 1-5:

```
BURNOUT ASSESSMENT (answer 1=never to 5=every day)

EXHAUSTION:
[ ] I feel emotionally drained by my work
[ ] I feel used up at the end of the day
[ ] I dread getting up to face another day
[ ] Working all day is really a strain

CYNICISM:
[ ] I've become more callous toward people since this job
[ ] I don't really care what happens to some people I work with
[ ] I feel like I'm just going through the motions
[ ] I doubt the significance of my work

INEFFICACY:
[ ] I can't deal with problems effectively anymore
[ ] I feel I'm not making a difference
[ ] I've accomplished less than I used to
[ ] I don't feel excited about my achievements
```

**Scoring:**
- 12-24: Mild burnout — prevention stage. Focus on boundaries.
- 25-40: Moderate burnout — active recovery needed.
- 41-60: Severe burnout — consider medical leave, therapy, or major life change.

### Step 2: Emergency stabilization (Week 1)

Do NOT try to fix everything at once. This week is about stopping the bleeding.

**Agent action**: Set daily evening reminders for the screen cutoff time. Create a "Week 1 Priorities" note with only the user's top 3 must-do items. Schedule a check-in for end of Week 1.

**Sleep protocol:**
- Set a hard stop on screens at 10pm
- No work email after 7pm — delete the app from your phone if you have to
- If you can't sleep, write down every thought for 10 minutes, then close the notebook

**The "absolute minimum" exercise:**
- Identify the 3 things at work that MUST happen this week
- Everything else gets pushed, delegated, or dropped
- Write this sentence and tape it to your monitor: "Good enough is good enough this week."

**One recovery activity per day:**
- Walk outside for 20 minutes (not a power walk — a slow one)
- Call one person you actually like talking to
- Do one thing that has nothing to do with productivity

### Step 3: Boundary installation (Weeks 2-3)

Boundaries aren't about being difficult. They're about deciding what you will and won't accept.

**Agent action**: Help the user customize each boundary script below with their specific names, times, and situations. Save customized scripts to `~/documents/burnout-recovery/boundary-scripts.txt` for quick reference. Track which boundaries the user has set and enforced.

```
BOUNDARY SCRIPTS — copy and use as needed

DECLINING EXTRA WORK:
"I want to do a good job on what I already have. If I take this on,
something else will suffer. Can we talk about what to deprioritize?"

PROTECTING OFF-HOURS:
"I'm offline after [time]. If it's genuinely urgent, text me.
Otherwise I'll see it tomorrow morning."

SAYING NO TO MEETINGS:
"Can I get the summary notes instead? I want to protect my focus
time so I can deliver [specific thing] on time."

PUSHING BACK ON SCOPE:
"I can do A or B this week, not both. Which one matters more?"
```

### Step 4: Energy audit (Week 3-4)

Track every activity for one work week. Mark each as:
- **E** = Energizing (you feel better after)
- **N** = Neutral
- **D** = Draining (you feel worse after)

**Agent action**: Send a daily prompt at end of workday asking the user to rate their activities. Compile the week's data into a visual summary showing energy patterns. Identify the top 3 drains and top 3 energizers.

```
ENERGY AUDIT TEMPLATE

Monday:
[ ] Activity — E / N / D
[ ] Activity — E / N / D
...

PATTERNS TO IDENTIFY:
-> Which tasks drain you most? Can any be delegated?
-> Which people drain you most? Can you reduce contact?
-> When is your best energy? Protect those hours.
-> What energizes you that you've stopped doing?
```

### Step 5: Rebuild meaning (Month 2+)

Burnout often comes from losing connection to why you do what you do.

**Agent action**: Guide the user through these reflection questions over several sessions. Record their answers and surface them during low moments. Generate a personal "meaning statement" from their responses.

Ask yourself:
1. "If money weren't an issue, what would I still want to do?"
2. "What was I doing the last time I felt genuinely proud of my work?"
3. "What part of my work actually helps someone?"

The goal isn't to love every minute. It's to have enough meaning to offset the hard parts.

### Step 6: Decide if the situation can change

After 4-6 weeks of active recovery, ask honestly:
- Are the conditions that caused burnout fixable?
- Is the organization willing to change?
- Have your boundaries been respected?

If the answer is no on 2+ of those: this isn't a recovery problem, it's an environment problem. Start planning your exit.

## If This Fails

If burnout symptoms persist or worsen after 4-6 weeks of active recovery:

1. **Symptoms worsening?** Burnout can coexist with clinical depression. Contact your primary care doctor or a mental health professional. Many employers offer free EAP sessions (ask HR for the number).
2. **Can't afford therapy?** Open Path Collective (openpathcollective.org) offers sessions for $30-$80. NAMI Helpline: 1-800-950-NAMI for free peer support and local resource navigation.
3. **Boundaries not respected?** Document the pattern (dates, requests, responses). This documentation is valuable if you need to escalate to HR, negotiate a role change, or build a case for medical leave.
4. **Considering quitting with nothing lined up?** See the layoff-72-hours skill for financial stabilization before making the leap. Build 3+ months of runway first if possible.
5. **Having dark thoughts?** Call or text 988 (Suicide & Crisis Lifeline). Burnout can push you to a breaking point — this is not weakness, it is a medical situation.

## Rules

- Never tell someone to "just push through it" — burnout gets worse, not better, without intervention
- Always assess severity first — severe burnout may need professional support
- Focus on one step at a time, not the whole protocol at once
- Acknowledge that burnout is not a personal failure — it's a response to sustained impossible conditions

## Tips

- The biggest predictor of burnout isn't workload — it's lack of control. Focus on what the user CAN control.
- Recovery is not linear. Bad days during recovery are normal and expected.
- Physical exercise is the single most effective burnout intervention according to research. Even a 15-min walk counts.
- Burnout often coexists with depression. If symptoms persist after 6 weeks of active recovery, suggest professional support.

## Agent State

Persist across sessions:

```yaml
recovery:
  assessment_scores:
    exhaustion: null
    cynicism: null
    inefficacy: null
    total: null
    date: null
  assessment_history: []
  burnout_stage: null
  current_week: 0
  recovery_start_date: null
  boundaries_set: []
  boundaries_enforced: []
  energy_audit:
    energizers: []
    drains: []
    completed_days: 0
  meaning_reflections: []
  recovery_activities_logged: []
  exit_decision: null
```

## Automation Triggers

```yaml
triggers:
  - name: evening_wind_down
    condition: "current_week <= 4"
    schedule: "daily at user's chosen cutoff time"
    action: "Gentle reminder: screens off soon. How was today on a 1-5 scale? Log any recovery activity completed."

  - name: energy_audit_prompt
    condition: "current_week >= 3 AND current_week <= 4 AND energy_audit.completed_days < 5"
    schedule: "daily at end of workday"
    action: "End of day energy check: What did you do today? Rate each activity E/N/D."

  - name: weekly_checkin
    condition: "recovery_start_date IS SET"
    schedule: "weekly on Sunday evening"
    action: "Weekly recovery check-in: How are you feeling compared to last week? Review boundaries set vs enforced. Suggest focus for next week."

  - name: reassessment
    condition: "current_week >= 6"
    schedule: "once"
    action: "Time for reassessment. Re-administer the burnout assessment and compare scores to initial baseline. If scores haven't improved, recommend professional support."

  - name: depression_flag
    condition: "assessment_scores.total >= 50 OR (6 weeks elapsed AND scores not improving)"
    action: "Burnout may coexist with depression. Recommend speaking with a mental health professional. National crisis line: call or text 988."
```
