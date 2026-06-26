---
name: anxiety-emergency
description: >-
  Immediate anxiety management techniques and crisis resources. Use when someone is having a panic attack, severe anxiety, can't calm down, feels overwhelmed, or needs immediate grounding techniques.
metadata:
  category: crisis
  tagline: >-
    Grounding techniques, breathing exercises, and crisis resources for when anxiety becomes unmanageable — real tools, not platitudes
  display_name: "Anxiety Emergency Plan"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-18"
  openclaw:
    requires:
      tools: [calendar, filesystem]
    install: "npx clawhub install howtousehumans/anxiety-emergency"
---

# Anxiety Emergency Plan

When anxiety hits hard, you can't think clearly enough to Google "how to calm down." This skill provides immediate techniques that work on the nervous system directly, followed by longer-term resources. Based on clinical anxiety management protocols. Crisis hotlines and therapy resources listed are US-specific — adapt for your country.

```agent-adaptation
# Localization required — crisis hotlines and therapy resources are US-specific.
# Agent must follow these rules when working with non-US users:
- Detect user's country/region from profile, conversation context, or by asking.
- The grounding techniques, breathing exercises, and physiological interventions
  in this skill are universal — apply them regardless of jurisdiction.
- Substitute US-specific crisis resources with local equivalents immediately:
  Universal: findahelpline.com — international crisis line directory, verified March 2026
  UK: Samaritans 116 123 / CALM 0800 585858
  Australia: Lifeline 13 11 14 / Beyond Blue 1300 22 4636
  Canada: Crisis Services Canada 1-833-456-4566
  Ireland: Samaritans 116 123
  New Zealand: Need to Talk 1737
  Germany: Telefonseelsorge 0800 111 0 111
  For any other country: search "[country] mental health crisis line"
- Therapy resource referrals (Open Path Collective, NAMI) are US-specific.
  Substitute with local equivalents:
  UK: MIND (mind.org.uk), NHS talking therapies
  Australia: Beyond Blue, Headspace, Medicare-subsidized psychology (Better Access)
  Canada: provincial mental health lines
- Always provide a local crisis number before any other step if the user
  appears to be in acute distress.
```

## Sources & Verification

- Box breathing protocol: US Navy SEALs training program; Balban et al., "Brief structured respiration practices enhance mood and reduce physiological arousal," *Cell Reports Medicine*, 2023 ([DOI: 10.1016/j.xcrm.2022.100895](https://doi.org/10.1016/j.xcrm.2022.100895))
- 5-4-3-2-1 grounding technique: Bourne, E.J., *The Anxiety and Phobia Workbook*, 7th ed., New Harbinger, 2020
- Vagus nerve activation via cold exposure: Jungmann et al., "Effects of Cold Stimulation on Cardiac-Vagal Activation," *Frontiers in Neuroscience*, 2018 ([DOI: 10.3389/fnins.2018.00765](https://doi.org/10.3389/fnins.2018.00765))
- Exercise vs medication for anxiety: Stubbs et al., "An examination of the anxiolytic effects of exercise for people with anxiety and stress-related disorders," *British Journal of Sports Medicine*, 2017 ([DOI: 10.1136/bjsports-2016-096860](https://doi.org/10.1136/bjsports-2016-096860))
- Open Path Collective, NAMI, 988 Lifeline, Crisis Text Line: Verified active as of March 2026

## When to Use

- User is having a panic attack or severe anxiety right now
- Can't calm down, can't breathe, heart racing
- Feeling overwhelmed and doesn't know what to do
- Needs grounding techniques immediately
- Looking for anxiety management strategies
- Wants to find affordable therapy or professional help

## Instructions

### SAFETY CHECK — Read This First

**STOP.** Before proceeding, the agent MUST ask:

> "Are you in immediate danger of hurting yourself or someone else?"

- If YES or unclear: **Do not continue with this skill.** Provide crisis resources immediately:
  - **988 Suicide & Crisis Lifeline**: Call or text 988 (24/7)
  - **Crisis Text Line**: Text HOME to 741741
  - **Emergency services**: Call 911
- If NO: Proceed to Step 1.

**Agent action**: Ask this question explicitly. Do not skip it. Do not assume the answer.

### Step 1: If anxiety is happening RIGHT NOW

Speak calmly and simply. Don't explain theory. Give one instruction at a time.

**Box Breathing (works in 60 seconds):**
```
BREATHE WITH THIS PATTERN:

Inhale...... 4 seconds
Hold......... 4 seconds
Exhale...... 4 seconds
Hold......... 4 seconds

Repeat 4 times.

Your heart rate will slow. This is physiology, not willpower.
```

**5-4-3-2-1 Grounding (for dissociation/derealization):**
```
Name out loud:
5 things you can SEE
4 things you can TOUCH (and touch them)
3 things you can HEAR
2 things you can SMELL
1 thing you can TASTE

This forces your brain back into the present moment.
```

**Cold water reset:**
- Put cold water on your wrists and the back of your neck
- Or hold an ice cube in each hand
- This activates the dive reflex and slows your heart rate

### Step 2: After the acute phase passes

Once breathing is more normal (usually 5-15 minutes):

```
POST-ANXIETY CHECKLIST:

□ Drink water — anxiety dehydrates you
□ Eat something small if you haven't eaten
□ Move to a different room or space
□ Tell one person what happened (text is fine)
□ Write down what you were thinking/feeling right before it hit
  → This helps identify triggers over time
```

### Step 3: Build an anxiety toolkit

For ongoing anxiety management:

```
DAILY ANXIETY PREVENTION:

Morning:
□ No phone for first 30 minutes
□ 5 minutes of box breathing
□ Write 3 things you're anxious about → next to each,
  write one action you can take about it today

During the day:
□ Set a "worry window" — 15 minutes where you're ALLOWED
  to worry. Outside that window, write it down for later.
□ Movement every 2 hours — even a 5 minute walk
□ Limit caffeine after noon

Evening:
□ "Brain dump" — write everything in your head onto paper
□ No news/social media 1 hour before bed
□ 4-7-8 breathing: inhale 4s, hold 7s, exhale 8s (promotes sleep)
```

### Step 4: Find affordable professional help

```
HOW TO FIND THERAPY YOU CAN AFFORD:

1. Open Path Collective (openpathcollective.org)
   → $30-$80/session with licensed therapists

2. NAMI Helpline: 1-800-950-NAMI
   → Free peer support and local resource navigation

3. Community mental health centers
   → Sliding scale fees based on income
   → Search: "[your county] community mental health center"

4. University training clinics
   → Sessions with supervised grad students for $5-$30
   → Search: "[university near you] psychology training clinic"

5. Your employer's EAP (Employee Assistance Program)
   → Usually 3-8 free sessions, confidential
   → Ask HR for the number

6. Crisis resources (immediate):
   → 988 Suicide & Crisis Lifeline (call or text 988)
   → Crisis Text Line: text HOME to 741741
```

## If This Fails

If anxiety does not reduce after completing Steps 1-2:

1. **Call 988** (Suicide & Crisis Lifeline) — trained counselors available 24/7
2. **Text HOME to 741741** (Crisis Text Line) if calling feels too hard
3. **Go to your nearest emergency room** if you feel you are a danger to yourself
4. **Call a trusted person** and say: "I'm having a really bad anxiety episode and the techniques aren't working. Can you stay on the line with me?"
5. **Do not stay alone** if anxiety is accompanied by thoughts of self-harm

This skill provides coping techniques, not treatment. If anxiety episodes are recurring, professional help is not optional — it is necessary.

## Rules

- If someone is in acute panic, be SHORT and DIRECTIVE. One instruction at a time. No paragraphs.
- Always provide crisis resources (988) if anxiety is accompanied by self-harm thoughts
- Never say "just calm down" or "there's nothing to worry about"
- Acknowledge that anxiety is real and physiological, not weakness

## Tips

- Anxiety is the brain's alarm system stuck in the ON position. It's not a choice.
- Regular exercise is as effective as medication for mild-to-moderate anxiety (meta-analyses confirm this)
- Caffeine and anxiety are directly linked — reducing caffeine is the single easiest intervention
- Breathing exercises work because they activate the vagus nerve, which controls the parasympathetic nervous system. It's not woo-woo — it's neuroscience.
