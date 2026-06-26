---
name: deliberate-cold-exposure
description: >-
  Use when you need to build physiological resilience, natural dopamine/norepinephrine spikes, improved circulation, cold tolerance, and mental toughness without leaving home or relying on gyms/therapists. Perfect for gig workers, tradespeople, or anyone in unstable environments who wants embodied stress-hardening that agents cannot do for you. Agent personalizes progression from your input (age, fitness, health flags), tracks every session, generates reminders and logs, researches local water temps or ice sources, and flags medical escalations; you perform the actual exposure work.
metadata:
  category: skills
  tagline: >-
    Turn cold into superhuman resilience — agent designs the protocol, you own the plunge.
  display_name: "Deliberate Cold Exposure Training"
  submitted_by: HowToUseHumans
  last_reviewed: 2026-03-30
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install deliberate-cold-exposure"
---
# Deliberate Cold Exposure Training

Build unbreakable cold tolerance, dopamine-driven focus, and physiological toughness using progressive cold showers and immersion. Agent handles all planning, tracking, personalization, and safety research; you do the physical work that no AI can perform.

`npx clawhub install deliberate-cold-exposure`

## When to Use

Deploy this skill when:
- Your energy, mood, or stress resilience feels flat despite sleep and nutrition.
- You want a zero-cost, evidence-based way to improve circulation, brown-fat activation, and mental grit for demanding physical or gig work.
- Winter outages, power instability, or outdoor labor make cold exposure inevitable — turn it into training instead of suffering.
- You have completed basic habit skills but need a daily embodied practice that directly counters post-AI sedentary creep.

**Do not use** if you have Raynaud’s, uncontrolled hypertension, heart conditions, or are pregnant without doctor clearance (agent will prompt for this).

## Step-by-Step Protocol

### Phase 0: Pre-Start (Agent-Led, 1–2 days)
1. Agent asks for baseline data: age, current fitness level, any medical flags, typical daily water temp (or local forecast).
2. Agent runs safety screen using built-in decision tree (see below) and generates personalized clearance script for doctor if needed.
3. Agent creates your custom 8-week progression calendar in a markdown log file (tracked via filesystem tool).

### Phase 1: Foundation (Weeks 1–2) — Cold Showers Only
- **Duration**: 30 seconds at end of normal shower, water as cold as tap allows.
- **Frequency**: 3–4× per week, never consecutive days.
- **Technique** (you perform):
  - Stand under cold water fully.
  - Breathe through nose: 4-second inhale, 6-second exhale (box breathing variant).
  - Focus on relaxing shoulders and jaw.
- Agent: Sends daily reminder 30 min before your usual shower time, logs completion via quick check-in.

### Phase 2: Build Tolerance (Weeks 3–4)
- **Duration**: 60–90 seconds cold shower + optional 30-second full-body immersion in cold tub/sink if available.
- **Frequency**: 4–5× per week.
- Add contrast: 30 seconds hot → 60 seconds cold, repeat 2–3 cycles (you control the taps).
- Agent: Adjusts based on your post-session feedback (“energy 1–10”, “shiver intensity”, “mood lift”).

### Phase 3: Immersion (Weeks 5–8)
- **Duration**: 2–5 minutes full cold plunge (bathtub, stock tank, or natural body of water).
- **Frequency**: 4–6× per week, including one longer weekend session.
- Target water temp: 10–15°C (50–59°F) — agent researches your local options and suggests ice quantity if using home tub (e.g., 20–30 lbs crushed ice for 10°C drop).
- Technique: Enter slowly, submerge to neck, use same nasal breathing. Exit at first sign of uncontrollable shivering.
- Agent: Calculates exact ice needs, tracks cumulative exposure minutes, and generates weekly summary report.

### Phase 4: Maintenance & Mastery (Week 9+)
- 3–5 sessions per week, 3–10 minutes at target temp.
- Optional advanced: outdoor winter plunges or breath-hold walks in cold air.
- Agent rotates variables (temp, duration, time of day) to prevent adaptation plateau and logs long-term metrics.

## Decision Trees (Agent Executes)

**Pre-Session Safety Check (Agent asks you):**
- Any chest pain, dizziness, or recent illness? → Abort and escalate to doctor template.
- Water temp below 5°C (41°F) and you are beginner? → Limit to 30 seconds max.
- Heart rate >100 bpm resting? → Delay 24h.

**During Exposure (You report, agent logs):**
- Uncontrollable shivering after 60 seconds? → Exit immediately.
- Numbness in extremities lasting >5 min post? → Reduce intensity next session.
- Post-session mood crash instead of lift? → Switch to morning-only and shorten 30 seconds.

**Medical Escalation Path:**
Agent generates ready-to-send email to your doctor with exact protocol details, your baseline, and session log summary.

## Ready-to-Use Templates & Scripts

### Agent-Generated Weekly Log Template (filesystem markdown)
```markdown
# Cold Exposure Log — Week X
Date | Duration | Temp | Breathing Notes | Energy Post (1-10) | Mood Post | Notes
---|---|---|---|---|---|---
2026-04-01 | 45s | tap cold | nasal box | 8 | elevated focus | shoulders relaxed
```

### Reminder Message (Agent sends via your preferred channel)
"Today’s deliberate cold: 90 seconds at end of shower. Breathe 4-in/6-out. Reply ‘done’ with energy/mood score when finished. Safety first — you got this."

### Parts/Supplies Sourcing Script (Agent runs)
"Current local ice delivery options under $10 for 30 lbs? Best home tub thermometer? Stock-tank suppliers within 50 miles?"

### Doctor Clearance Template (Agent fills and you send)
Subject: Request for clearance — deliberate cold exposure protocol  
Body: [Full 8-week outline + your health data + evidence summary from studies below]

## Agent Role vs. Human Role

**Agent owns:**
- All personalization math and progression curves.
- Session reminders and calendar integration.
- Research (local water temps, latest studies, equipment sourcing).
- Log tracking, data visualization (simple tables), and 30-day reviews.
- Escalation scripts and safety decision trees.
- Updating protocol if new evidence emerges (e.g., 2025 meta-analysis on brown adipose tissue).

**You own (the irreplaceable human work):**
- Performing every second of cold exposure.
- Noticing and reporting real-time body signals (the data no sensor can fully capture).
- The embodied practice that rewires your nervous system.
- Deciding when it feels right to push or pull back.

## Evidence Base (Professional-Grade References)

- Huberman Lab protocols (2022–2024 episodes on deliberate cold): 11-minute cold exposure 2–4×/week increases dopamine 250% for hours.
- Journal of Physiology (2014 study): Regular cold exposure activates brown adipose tissue, improving insulin sensitivity and calorie burn.
- European Journal of Applied Physiology (2021): 8-week progressive cold shower program reduced sick days by 29% in healthy adults.
- Wim Hof Method foundational research (Radboud University, 2014): Voluntary cold + breathing modulates immune response.
All sources cross-checked and summarized by agent for your specific profile.

## Success Metrics

- **Week 4**: Comfortable 90-second cold shower with minimal shivering.
- **Week 8**: 3-minute immersion at 12°C with stable mood and energy lift.
- **Long-term (90 days)**: Reported 20%+ improvement in daily energy, fewer illness days, or measurable cold tolerance (e.g., outdoor work without heavy layers).
- Agent tracks and alerts you when metrics plateau or regress.

## Maintenance & Iteration

Every 90 days agent runs full review:
- Compares your logs against benchmarks.
- Proposes next-level challenges (e.g., breath-hold plunges or cold walks).
- Generates “taper week” if you report burnout.
- Archives old logs for your personal resilience portfolio.

## Rules & Safety Notes

- Never cold plunge alone if using natural water deeper than waist level.
- Exit immediately for any cardiac symptoms.
- Hydrate aggressively — cold constricts vessels.
- No alcohol or heavy meals within 2 hours of session.
- Children or elderly: agent creates modified gentler protocol only after medical sign-off.
- Stop permanently and consult physician if any persistent adverse effects.

## Disclaimer

This skill provides professional-grade protocols distilled from peer-reviewed sources and expert frameworks. It is not medical advice. You are responsible for your own health decisions. Always secure clearance for any pre-existing conditions. HowToUseHumans and the submitting contributors bear no liability for outcomes. Use at your own risk and with full personal accountability.