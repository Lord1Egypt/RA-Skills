---
name: dental-self-care
description: >-
  Use when you lack dental insurance, face high costs for dental care, live in remote/gig-economy situations, or work physical trades with irregular access to professionals and need to prevent painful, expensive emergencies through consistent self-managed protocols. Agent personalizes daily routines based on your age/job/diet/symptoms, maintains filesystem trackers and supply lists, researches low-cost providers, drafts scripts/emails, sets automated reminders, runs decision trees on reported symptoms, and logs progress so you stay focused on the physical hands-on care.
metadata:
  category: skills
  tagline: >-
    Evidence-based oral health maintenance and emergency self-management — agent handles tracking, research, and bureaucracy; you keep teeth functional without debt or downtime.
  display_name: "Dental Self-Care & Emergency Protocol"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-31"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install dental-self-care"
---

# Dental Self-Care & Emergency Protocol

You don't need perfect teeth or a dentist on speed dial to keep your mouth healthy and functional. This protocol delivers professional-grade, evidence-based daily maintenance routines, symptom tracking systems, home remedies for common issues, and crystal-clear decision trees for when to escalate. In the post-AI gig economy where agents already manage your money crises and benefits navigation, this skill lets the agent own the admin, research, and reminders while you focus on the embodied work of brushing, flossing, and self-exams — protecting your ability to eat, speak, and work without sudden pain or five-figure bills.

`npx clawhub install dental-self-care`

## When to Use This Skill

Deploy immediately if any of these match:
- Dental insurance has lapsed, never existed, or has massive deductibles.
- You work physical trades, shift work, or gig delivery where time off for appointments is impossible and benefits are nonexistent.
- You are in austerity mode, remote living, or preparing for supply-chain disruptions where professional care may be unavailable.
- Minor symptoms have appeared (sensitivity, bleeding gums, occasional ache) and you want to halt progression before they become emergencies.
- You simply want to minimize lifetime dental spending through prevention while maintaining peak oral function for daily living.

At first install, the agent will prompt you for baseline data: age, current symptoms (pain level/location), diet habits, job type (e.g., dusty outdoor work increases risk), access to water/supplies, and any medical conditions (diabetes, dry mouth from medications). It then builds a personalized tracker file in the filesystem and sets recurring reminders.

## Agent Role vs. Human Role

**Agent (bureaucracy, logic, tracking):**
- Personalizes every routine and timeline based on your input.
- Creates and maintains filesystem logs (daily symptom tracker, supply inventory, progress dashboard).
- Researches real-time local resources (sliding-scale clinics, dental schools, charity programs) using your location.
- Generates ready-to-send emails, call scripts, and negotiation templates.
- Runs automated decision trees on your symptom reports and flags escalations.
- Sends timed reminders, follow-up prompts, and monthly reviews.
- Logs adherence and suggests micro-adjustments.

**Human (embodied physical work):**
- Performs all hands-on hygiene (brushing, flossing, self-exams).
- Conducts weekly self-checks in front of a mirror.
- Applies home remedies exactly as instructed.
- Reports symptoms honestly and promptly.
- Makes the final go/no-go decision on professional care and physically attends if needed.
- Provides feedback after each cycle so the agent refines the protocol.

This division ensures the agent never does the physical work — only the planning and admin — so you stay in your body and in control.

## Step-by-Step Protocol

### Phase 1: Days 1–7 — Baseline & Habit Installation (Agent sets daily reminders)
1. **Morning Routine (3 minutes)**  
   Brush with soft-bristled toothbrush + ADA-approved fluoride toothpaste (1,000–1,500 ppm fluoride) for full 2 minutes using gentle circular motions at 45° to the gumline. Spit, do not rinse immediately (allows fluoride to work). Scrape tongue with dedicated plastic scraper or spoon edge to remove overnight bacterial film.  
   *Evidence*: ADA guidelines (2024) and a 2022 meta-analysis in *Journal of Clinical Periodontology* confirm this reduces plaque by 50–70% vs. brushing alone.

2. **Evening Routine (5 minutes)**  
   Repeat morning brush. Floss or use interdental brushes/water flosser between every tooth. If budget-constrained, use waxed floss or cut-up plastic water bottle as emergency interdental tool (agent provides diagrams).  
   Chew one piece of xylitol gum (≥1g xylitol) for 5 minutes post-dinner.  
   *Evidence*: Multiple randomized trials (e.g., *Journal of Dental Research* 2019) show xylitol reduces *Streptococcus mutans* by up to 85% and cuts new cavities by 40–60%.

3. **Nightly Self-Exam (1 minute)**  
   Use small mirror + headlamp/phone flashlight. Check gums for redness/swelling/bleeding points, teeth for chips/cracks/white spots, tongue for unusual patches. Report findings to agent via simple voice note or text.

Agent logs completion automatically and sends “missed day” alert if skipped.

### Phase 2: Weeks 2–4 — Deep Maintenance & Early Intervention
- **Weekly Deep Clean (Sunday evening, 20 minutes)**: Soak toothbrush heads in 3% hydrogen peroxide for 10 minutes. Perform 10-minute oil pull with coconut oil (swish gently, spit into trash). Re-examine and report.  
- **Bi-weekly Supply Check**: Agent maintains inventory list; when low, generates reorder list or cheapest local source.  
- **Symptom Reporting**: Any new ache, sensitivity, or bleeding triggers an immediate decision-tree walkthrough with the agent.

### Phase 3: Ongoing (Month 2+)
- Monthly agent-led review: Compare logs to baseline, calculate adherence percentage, suggest tweaks (e.g., switch to prescription-strength fluoride rinse if high cavity risk from job dust).  
- Quarterly “professional simulation”: Agent drafts a self-assessment report you could take to a dentist if you ever go.

## Nutrition & Lifestyle Integration (Agent Cross-References Existing Skills)
- Limit sugary/acidic intake; agent can pull from your austerity-living or budget-meal-prep logs to flag high-risk foods.  
- Counter dry mouth (common in shift work) with frequent water sips and sugar-free gum.  
- Chew fibrous vegetables daily for natural cleaning.  
- Agent suggests simple swaps: replace energy drinks with water + xylitol.

## Symptom Tracking System (Agent-Maintained Filesystem Log)
Agent creates and updates a markdown table daily:

| Date | Time | Symptom (1-10 pain) | Location | Trigger | Action Taken | Notes |
|------|------|---------------------|----------|---------|--------------|-------|
| YYYY-MM-DD | HH:MM | 3 (throbbing) | Lower left molar | Cold drink | Saltwater rinse + clove oil | Improved after 30 min |

You reply with updates; agent analyzes trends (e.g., “Pain spikes after sugary coffee — flag for dietary adjustment”).

## Decision Trees (Agent Runs Live)

**Bleeding Gums**  
- Mild, stops after 3 days of flossing → Continue + add warm saltwater rinse 2× daily.  
- Persistent >7 days or pus → Agent drafts provider contact script; prepare for possible scaling.

**Tooth Sensitivity**  
- Mild to cold/sweet → Switch to desensitizing toothpaste (potassium nitrate or stannous fluoride) for 14 days.  
- Worsens or hot sensitivity → Log as possible crack; escalate to professional within 48 hours.

**Toothache**  
- Mild, no swelling → Saltwater rinse (½ tsp salt in 8 oz warm water) + clove oil on cotton (eugenol is natural analgesic, per *Journal of Endodontics* studies) + OTC ibuprofen.  
- Moderate + swelling → Ice pack outside cheek 15 min on/off; agent researches nearest low-cost urgent dental.  
- Severe + fever + facial swelling + difficulty swallowing/breathing → Immediate ER — this is potential spreading infection. Agent provides driving directions and what to tell triage.

**Trauma (knocked tooth, crack)**  
- Adult tooth knocked out → Agent gives exact 5-minute re-implantation steps (rinse gently, place back in socket, bite on gauze).  
- Chip or crack → Stabilize with OTC temporary filling material (Dentemp or equivalent); seek care within 72 hours.

## Emergency Home Kit (Agent Maintains Inventory & Reorder Schedule)
Must-have, low-cost items (total build cost ~$25):
- 2 soft toothbrushes + fluoride toothpaste  
- Dental floss + interdental brushes  
- Xylitol gum/mints  
- Hydrogen peroxide (3%)  
- Unflavored dental wax or temporary filling kit  
- Clove oil or eugenol drops  
- Small dental mirror + headlamp  
- Salt + baking soda (for rinses)  

Agent tracks expiration and auto-generates shopping list when <30 days remain.

## Resource Navigation & Bureaucracy Scripts (Agent Handles All)
1. Ask for your zip code → Search sliding-scale clinics, dental schools (students provide care at 50–70% discount), community health centers, or Medicaid dental if eligible.  
2. Prepare call script: “Hi, I’m a gig worker without insurance. Do you offer sliding-scale fees based on income? What is your next available appointment for a cleaning/exam?”  
3. Email template for payment plans or charity applications (fully personalized with your data).

**Ready-to-Use Email Template (Agent fills placeholders):**
```
Subject: Request for Sliding-Scale Dental Appointment – [Your Name]

Dear [Clinic Name] Team,

I am a [your job, e.g., construction worker] with no current dental insurance and limited income. I have been maintaining my oral health at home but now need a professional exam for [brief symptom]. 

I understand you offer sliding-scale fees. My monthly income is approximately $[amount] and I can provide proof of income. 

Would you have availability in the next [2 weeks]? I am available [your flexible times].

Thank you,
[Your Name]
[Phone]
```

Agent can iterate the template after you report responses.

## Progress Logging, Iteration & Maintenance
- **Weekly Check-in**: Agent asks 3 questions, updates dashboard.  
- **Monthly Review**: Full log analysis + adherence score. If <80%, agent diagnoses cause (forgotten reminders? supply shortage?) and fixes.  
- **Annual Self-Assessment**: Agent generates printable report of your entire year’s logs for any future dentist.  
- Iteration rule: New research (e.g., new ADA guideline) → Agent updates protocol automatically and notifies you of changes.

## Rules & Safety Notes
- Red-flag symptoms requiring immediate professional care: facial swelling, fever >100.4°F with dental pain, pus drainage, inability to open mouth, or numbness in lip/tongue.  
- Never attempt to pull your own tooth or use unverified internet “DIY” methods.  
- If you have diabetes, heart conditions, or are pregnant, shorten escalation timelines by half.  
- This protocol assumes basic access to water and over-the-counter supplies; in true no-water scenarios, cross-reference hygiene-without-infrastructure skill.  
- Track any allergies (e.g., to clove oil) and report immediately.

## Success Metrics
- 90-day rolling average: zero moderate-or-higher unexplained pain episodes.  
- Gum health score: no bleeding on flossing for 30 consecutive days.  
- Adherence >85% (agent-tracked).  
- Zero emergency dental visits caused by preventable issues.  
- Subjective: ability to eat any food without discomfort.

Track these in the agent’s dashboard; celebrate milestones with a simple “protocol win” log entry.

## Disclaimer
This skill compiles publicly available guidelines from the American Dental Association, peer-reviewed studies in *Journal of Clinical Periodontology*, *Journal of Dental Research*, and *Journal of Endodontics*, plus standard public-health emergency protocols. It is informational only and not a substitute for professional dental or medical advice. In any emergency, contact a licensed dentist, urgent-care facility, or ER immediately. Outcomes depend on your individual health; the HowToUseHumans project, contributors, and agents assume no liability for use or non-use of this protocol. Always verify with a qualified provider when possible.