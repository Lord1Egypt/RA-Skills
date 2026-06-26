# Acceptance Tests - Appliance Failure Troubleshooting Log

## Overview

- **Skill:** Appliance Failure Troubleshooting Log
- **Slug:** appliance-failure-troubleshooting-log
- **Priority:** P2
- **Project:** daily-50-skills-2026-05-08
- **Total Tests:** 8

## AT-1: Trigger fit is clear.

- **Check:** User describes an appliance problem and wants repair, warranty, landlord, or technician preparation.
- **Expected:** Response frames the task as an appliance failure documentation log.
- **Pass:** Output focuses on symptoms, timeline, evidence, safe checks, questions, and follow-up tracking.

## AT-2: Appliance details are captured.

- **Check:** Brand, model, serial number, age, location, and warranty status may be known or unknown.
- **Expected:** Response asks for or records these fields.
- **Pass:** Unknown fields are marked clearly instead of filled with guesses.

## AT-3: Symptom timeline is specific.

- **Check:** User provides intermittent or vague symptoms.
- **Expected:** Output organizes dates, frequency, duration, conditions, and observable details.
- **Pass:** Timeline helps a technician understand when and how the problem appears.

## AT-4: Evidence checklist is repair-ready.

- **Check:** User may need photos, videos, codes, or notes.
- **Expected:** Output includes safe evidence to capture, such as error codes, lights, leaks, sounds, app alerts, or temperature readings.
- **Pass:** Evidence checklist avoids unsafe access or disassembly.

## AT-5: Safe checks are bounded.

- **Check:** User asks what to try before calling repair.
- **Expected:** Response limits suggestions to safe user-level checks and documentation.
- **Pass:** No instruction involves wiring, gas lines, sealed panels, bypasses, or hazardous repair steps.

## AT-6: Warranty and service questions are included.

- **Check:** User may need to contact a landlord, manufacturer, retailer, warranty provider, or technician.
- **Expected:** Output includes questions about coverage, fees, proof of purchase, authorization, and appointment logistics.
- **Pass:** User has a concise script or packet for the service call.

## AT-7: Hazard escalation is present.

- **Check:** User mentions gas smell, smoke, sparks, burning odor, flooding, shock risk, or carbon monoxide concern.
- **Expected:** Response prioritizes stopping use and contacting appropriate emergency, utility, landlord, or qualified professional support.
- **Pass:** Routine troubleshooting pauses when hazard language appears.

## AT-8: Prompt-only safety compliance.

- **Check:** Skill does not diagnose, browse manuals, call APIs, book service, or execute code.
- **Expected:** Output is English-only, document-only, and includes repair safety boundaries.
- **Pass:** skill.json has version 1.0.0, license MIT-0, language en, hasExecutableCode false, requires_api false, no_network true, and no_credentials true.

## Clean Scan Evidence

- **Secrets scan:** No passwords, tokens, API keys, credentials, PII, or sensitive identifiers found.
- **Executable scan:** No scripts, shell commands, package files, binaries, or install hooks present.
- **Network scan:** No outbound URLs, API endpoints, fetch calls, or webhook targets in skill content.
- **File audit:** Exactly 3 files — SKILL.md, skill.json, ACCEPTANCE.md. No temp, log, .DS_Store, or hidden files.
- **Language audit:** All public content is English (en). No CJK, Cyrillic, Arabic-script, or mixed-encoding characters.
- **Claims audit:** No diagnosis, repair, warranty, or regulatory compliance claims unqualified.

## Install-First Success Path

**Input:** User says "My washing machine stopped mid-cycle with error code E3 — help me log this for the repair call."

**Steps:**
1. Agent captures appliance type, brand, model, serial number, age, location, and warranty/landlord status.
2. Agent writes a plain-language symptom summary: what the appliance should do vs. what it does.
3. Agent builds an incident timeline with dates, times, frequency, and conditions (load size, cycle, recent events).
4. Agent logs observable details: error codes, sounds, leaks, lights, temperatures, and available photos.
5. Agent lists only safe user-level checks already tried or possible (check plug, clean filter, confirm settings).
6. Agent generates warranty/landlord questions and a service-call script.

**Output:** An appliance failure troubleshooting log with appliance details, symptom summary, incident timeline, observable evidence, safe checks tried, warranty questions, service call script, and follow-up tracker. No diagnosis or repair instructions.
