# Acceptance Tests - Donation Drop-off Planner

## Overview
- **Skill:** Donation Drop-off Planner
- **Slug:** donation-dropoff-planner
- **Priority:** P2
- **Project:** daily-50-skills-2026-05-08
- **Total Tests:** 8

## AT-1: Sorts items by donation readiness.
- **Check:** Response groups items by condition and readiness.
- **Expected:** Donate-ready, clean-or-repair, verify-first, do-not-donate, and recycle/dispose categories are used as needed.
- **Pass:** Output demonstrates compliance with this criterion.

## AT-2: Provides logistics-focused destination suggestions.
- **Check:** Response suggests destination types without guaranteeing acceptance.
- **Expected:** User is told to verify current organization rules, hours, and restrictions.
- **Pass:** Output demonstrates compliance with this criterion.

## AT-3: Creates bag or box labels.
- **Check:** Response includes labels the user can copy onto bags or boxes.
- **Expected:** Labels include destination type, item category, condition, and action status.
- **Pass:** Output demonstrates compliance with this criterion.

## AT-4: Includes a packing checklist.
- **Check:** Response covers cleaning, grouping, fragile items, heavy boxes, data removal, and rule-check separation where relevant.
- **Expected:** User can pack items safely and practically.
- **Pass:** Output demonstrates compliance with this criterion.

## AT-5: Includes a drop-off checklist.
- **Check:** Response includes hours/rules verification, loading order, pickup or appointment reminders, and rejected-item fallback.
- **Expected:** User has a clear drop-off day action plan.
- **Pass:** Output demonstrates compliance with this criterion.

## AT-6: No tax valuation or tax advice.
- **Check:** Response does not estimate item value, deductibility, or appraisal method.
- **Expected:** It may suggest a non-valued inventory or receipt for personal records, but directs tax questions to official guidance or qualified professionals.
- **Pass:** Output demonstrates compliance with this criterion.

## AT-7: Document language.
- **Input:** Any valid trigger.
- **Expected:** Output is English-first with no CJK-dominant paragraphs.
- **Pass:** No CJK-dominant content in main output.

## AT-8: No-code compliance.
- **Check:** No executable code, APIs, browser actions, credentials, or network calls are required.
- **Expected:** skill.json has `hasExecutableCode: false`, `requires_api: false`, `no_code_execution: true`, `no_network: true`, and `no_credentials: true`.
- **Pass:** Skill is purely document/prompt-flow with no executable components.

## Clean Scan Evidence

- [x] No secrets, tokens, passwords, API keys, or private keys.
- [x] No executable code, scripts, package.json, or build artifacts.
- [x] No network calls, outbound requests, or external API dependencies.
- [x] No credential handling or environment-variable leakage.
- [x] No binary files, compiled code, or platform-specific executables.
- [x] No temp files, logs, .DS_Store, or editor artifacts.
- [x] Document-only, prompt-only, no execution required.
- [x] Language content is English with no CJK-dominant paragraphs.

## Install-First Success Path

**Input:** User provides donation items (list or categories), condition notes, and drop-off constraints.

**Steps:**
1. Read the skill metadata and verify document-only, prompt-only safety.
2. Review the workflow: sort by condition, match destination types, create bag and box labels, build packing checklist, plan drop-off logistics.
3. Ask for any missing required inputs (condition notes, preferred destinations, drop-off deadline, packing supplies).
4. Produce the structured donation plan with sorted items, labels, packing checklist, and drop-off plan.

**Output:** A practical donation plan with sorted item groups, ready-to-copy bag labels, a packing checklist, and a drop-off action card ready for immediate use with no additional tools, files, or network access.
