---
name: Appliance Failure Troubleshooting Log
description: Creates a repair-ready appliance failure log with symptoms, timing, model details, error codes, safe checks, photo evidence, warranty questions, and technician call notes.
version: "1.0.0"
type: prompt-flow
tags:
  - appliance-repair
  - troubleshooting-log
  - home-admin
  - warranty
  - repair-prep
  - maintenance
author: Bell (design)
---

# Appliance Failure Troubleshooting Log

## Overview

Appliance Failure Troubleshooting Log helps a user organize an appliance problem before contacting a landlord, warranty provider, manufacturer, or repair technician. It turns scattered observations into a clear incident log: what failed, when it happens, what evidence exists, what safe user-level checks were tried, and what questions need answers.

This skill does not diagnose appliance failures or provide risky repair instructions. It supports documentation, communication, and preparation only.

## When to Use

Use this skill when the user is dealing with:

- A refrigerator, washer, dryer, dishwasher, oven, HVAC unit, water heater, microwave, or other household appliance behaving strangely
- Intermittent symptoms that are hard to explain to a technician
- Error codes, noises, leaks, smells, lights, temperature changes, or performance problems
- Warranty, landlord, or service-call preparation
- A need to track attempted fixes, costs, follow-ups, and repair promises

**Trigger phrases:** "help me log an appliance problem", "appliance troubleshooting log before repair", "prepare for appliance repair call", "track this washer issue", "what should I tell the technician"

## Required Inputs

Ask for what the user knows:

- Appliance type, brand, model number, serial number, age, and location
- Warranty, lease, or service plan status if known
- Main symptom in plain language
- When the issue started and how often it happens
- Error codes, lights, sounds, smells, leaks, temperatures, or unusual behavior
- Safe checks already tried, such as resetting a breaker, cleaning a filter, checking a door seal, or confirming power
- Photos or videos the user can capture safely

If the user reports a hazard, shift to safety guidance and professional help instead of routine logging.

## Workflow

### Step 1 - Identify the Appliance

Capture appliance type, brand, model, serial number, age, purchase date, installation date, location, and warranty or landlord responsibility if known. Mark unknown fields clearly.

### Step 2 - Describe the Symptom Plainly

Write a clear symptom summary in the user's words. Include what the appliance should do, what it is doing instead, and whether the problem is constant or intermittent.

### Step 3 - Build the Incident Timeline

Record dates, times, frequency, duration, and conditions. Include context such as load size, cycle, temperature setting, recent power outage, weather, new installation, maintenance, or heavy use.

### Step 4 - Capture Observable Details

Log evidence that can help a repair conversation:

- Error codes or indicator lights
- Sounds, vibration, smells, smoke, sparks, or heat
- Leaks, moisture, frost, food temperature, drainage, or residue
- Photos or videos to capture safely
- Screenshots of app alerts or manuals if already available

### Step 5 - List Safe User-Level Checks

Document only low-risk checks the user has already tried or can do without opening sealed panels, handling wiring, moving gas lines, bypassing switches, or defeating safety mechanisms. Examples include checking the plug, confirming settings, cleaning a visible lint screen, checking a filter, or restarting according to the manual.

### Step 6 - Create Warranty and Responsibility Questions

Generate questions for the landlord, warranty provider, retailer, manufacturer, or technician. Include proof-of-purchase needs, coverage dates, service fees, exclusions, and who authorizes repairs.

### Step 7 - Prepare the Service Call Packet

Produce a concise script and information packet for the call or visit: appliance details, symptom summary, timeline, evidence, safe checks tried, urgency, access notes, and desired next step.

### Step 8 - Track Follow-up

Create a follow-up tracker with date contacted, person or company, case number, appointment window, quoted cost, promised action, parts ordered, warranty decision, and next deadline.

## Output Format

Use this structure:

- **Appliance Failure Troubleshooting Log**
- **Appliance Details:**
- **Symptom Summary:**
- **Incident Timeline:**
- **Observable Evidence:**
- **Safe Checks Tried:**
- **Photos and Videos to Capture:**
- **Warranty or Landlord Questions:**
- **Service Call Script:**
- **Follow-up Tracker:**
- **Safety Notes:**

## Safety Boundaries

- Do not instruct the user to open electrical panels, handle wiring, move gas lines, bypass sensors, defeat safety locks, or perform repairs beyond safe user-level checks.
- If there is gas smell, smoke, sparks, burning odor, active flooding, electrical shock risk, carbon monoxide alarm, or suspected fire risk, tell the user to stop using the appliance and contact emergency services, utility provider, landlord, or a qualified professional as appropriate.
- Do not claim a diagnosis from symptoms alone.
- Do not guarantee warranty coverage, refund outcomes, or repair costs.
- Keep the work to documentation, questions, scripts, and tracking.

## Example Prompts

- "My refrigerator is making a loud buzzing noise and the freezer isn't staying cold. Help me log everything before the repair technician arrives."
- "The washing machine shows error code E3 and stops mid-cycle. Build me a troubleshooting log with timeline and evidence."
- "My oven heats unevenly — some spots burn while others stay raw. Help me document symptoms, model details, and warranty questions."

## Quality Bar

A strong result gives the user a technician-ready record that reduces vague calls, repeat explanations, and lost warranty details while keeping safety first.
