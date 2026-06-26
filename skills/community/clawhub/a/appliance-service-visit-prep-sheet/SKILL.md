---
name: appliance-service-visit-prep-sheet
displayName: "Appliance Service Visit Prep Sheet"
version: "1.0.0"
description: "Prepare a technician-ready appliance service visit sheet with model and serial details, symptom timeline, photo checklist, access notes, questions, and visit-day prep."
triggerKeywords:
  - appliance service visit
  - appliance repair appointment
  - technician handoff
  - repair visit prep
  - appliance technician coming
  - model serial checklist
  - washer repair visit
  - refrigerator repair visit
tags:
  - home-admin
  - appliance-repair
  - service-visit
  - technician-handoff
  - repair-prep
license: "MIT-0"
language: "en"
hasExecutableCode: false
promptOnly: true
execution: "noExec"
---

# Appliance Service Visit Prep Sheet

## Purpose

Use this prompt-only skill when an appliance repair visit is booked, or when the user needs to prepare a technician-ready handoff for an appliance failure. The deliverable is a practical visit-day prep sheet: appliance identifiers, symptom timeline, photos to capture, access notes, questions, and fields for technician findings.

This skill supports documentation and communication only. It does not diagnose appliance failures, instruct internal repairs, bypass safety features, or replace manufacturer or technician guidance.

## Safety Boundary

Do not instruct the user to open sealed panels, handle wiring, move gas lines, bypass sensors, defeat safety locks, remove covers, disassemble components, or perform internal repairs. Do not tell the user to disconnect power, water, or gas unless the manufacturer manual, utility provider, landlord, or technician has instructed them to do so.

If the user reports gas smell, smoke, sparks, burning odor, electric shock, active flooding, carbon monoxide alarm, exposed wiring, fire risk, sewage backup, or unsafe heat, stop routine prep and direct them to leave the area if needed and contact emergency services, the utility provider, landlord, building management, or a qualified professional as appropriate.

Do not guarantee warranty coverage, repair cost, diagnosis, part availability, or technician outcome. Do not collect permanent gate codes, alarm codes, payment card numbers, full account numbers, or unnecessary private information.

## When to Use

Use this skill when:

- A technician appointment has been scheduled for a refrigerator, washer, dryer, dishwasher, oven, microwave, water heater, HVAC unit, or other appliance.
- The user wants to avoid a failed visit caused by missing model details, blocked access, unavailable photos, or unclear symptoms.
- A landlord, warranty provider, manufacturer, or service company needs a concise appliance handoff.
- The user wants a visit-day checklist and question list.

Do not use it for live emergency troubleshooting, internal repair instructions, buying decisions, or broad home service visits that are not appliance-specific.

## Required Inputs

Ask for practical details the user knows:

- Appliance type, brand, model number, serial number, age, and location.
- Appointment date, arrival window, service company, technician contact, and case or work order number if available.
- Warranty, service plan, landlord, retailer, or manufacturer responsibility if known.
- Main symptom in plain language.
- When the symptom started, frequency, conditions, and any changes.
- Error codes, app alerts, indicator lights, sounds, smells, leaks, temperature readings, cycle names, or load conditions.
- Photos or videos the user can capture safely from outside the appliance.
- Access needs: parking, entry, pets, children, appliance location, clearance, stairs, building rules, or someone who can approve work.
- Questions the user wants answered before approving repairs.

Mark unknown fields clearly. Do not require the user to move heavy appliances, expose wiring, or reveal sensitive access data.

## Workflow

1. **Capture appliance details.** Record type, brand, model, serial, location, age, purchase or install date if known, and warranty or landlord context.
2. **Log symptoms.** Build a plain-language symptom timeline with start date, frequency, conditions, error codes, sounds, smells, leaks, temperatures, app alerts, and what changed.
3. **Create the photo checklist.** List safe photos and videos to capture before the visit, including model label, error display, surrounding area, visible leaks or residue, damage, install area, and short symptom videos when safe.
4. **Prepare access notes.** Capture parking, entry, rooms, pets, children, building rules, appliance clearance, elevator or stair issues, and who can authorize work.
5. **Draft technician questions.** Include diagnosis, repair options, estimate, parts, warranty, expected timeline, what to use or avoid until fixed, cleanup, and follow-up documentation.
6. **Build the visit-day sheet.** Produce a single handoff page with appointment snapshot, appliance details, symptom timeline, evidence checklist, access notes, questions, authorization limits, and technician notes fields.
7. **Plan follow-up.** Add fields for findings, work performed, parts ordered, cost estimate, invoice or work order, warranty terms, next appointment, and symptoms to monitor.

## Photo and Evidence Checklist

Suggest only safe, external evidence:

- Model and serial label, if visible without moving heavy equipment or opening unsafe areas.
- Error code, display panel, app alert, or indicator light.
- Wide shot of appliance location and access path.
- Visible leak, frost, residue, loose part, damage, or floor condition.
- Short video of sound, vibration, drainage issue, cycle behavior, or intermittent symptom if it can be captured safely.
- Purchase receipt, warranty document, prior service invoice, or manual cover if already available.

## Technician Questions

Tailor questions to the appliance and symptom:

- What did you find, and what evidence supports that finding?
- Is this a repair, maintenance, installation, user-setting, part, or warranty issue?
- What are the repair options, estimated cost, and expected timeline?
- Are parts needed, and are they available today or ordered?
- Is the appliance safe to use until repair is complete?
- What should we avoid using or changing until the next step?
- Is the work covered by warranty, service plan, landlord, or manufacturer process?
- What documentation, photos, invoice, or job number should we keep?
- Who should we contact if the symptom returns?

## Output Format

Return a technician-ready prep sheet with these sections:

1. **Appointment Snapshot**
   - Service company
   - Date and arrival window
   - Contact method
   - Case, claim, or work order number
   - Responsible person on site
2. **Appliance Details**
   - Appliance type
   - Brand
   - Model number
   - Serial number
   - Location
   - Age, purchase, install, warranty, or landlord notes
3. **Symptom Timeline**
   - Main symptom
   - Start date
   - Frequency and conditions
   - Error codes or app alerts
   - Sounds, smells, leaks, temperatures, cycles, or visible changes
   - Safe checks already tried, if any, without adding repair instructions
4. **Photos and Documents Checklist**
   - Photos or videos to capture safely
   - Receipts, warranty, manual, prior invoice, or service plan documents
5. **Access Notes**
   - Parking and entry
   - Rooms or equipment to access
   - Pets, children, building rules, stairs, clearance, and supervision
   - Sensitive access details omitted or handled separately
6. **Questions for the Technician**
   - Diagnosis and evidence
   - Options, estimate, parts, warranty, timeline, safe use, and follow-up
7. **Authorization Limits**
   - Who can approve work
   - Maximum spend before calling back
   - Decisions requiring written estimate or owner approval
8. **Visit-Day Notes**
   - Findings
   - Work performed
   - Parts used or ordered
   - Cost or invoice
   - Next appointment
   - Symptoms to monitor
9. **Safety Note**
   - No internal repairs. Follow manufacturer, utility, landlord, or technician guidance for power, water, gas, and safe use.

## Example Prompts

- "My refrigerator repair technician is coming tomorrow. Help me prepare a visit sheet with model details, symptom timeline, and questions."
- "The dishwasher has been making noise and leaking. I have a service appointment this week — build a technician handoff sheet."
- "I need a prep sheet for a washer repair visit. The machine shows error code LE and the spin cycle stopped working."

## Quality Bar

A strong result lets a technician understand the appliance, symptom history, access constraints, and user questions within one minute. It should reduce repeated explanations and missed details while keeping the user away from risky repair actions.
