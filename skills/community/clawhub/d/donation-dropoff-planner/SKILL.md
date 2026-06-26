---
name: Donation Drop-off Planner
description: Turn a pile of household donation items into sorted bundles, labels, packing steps, and a drop-off checklist without giving tax valuation or tax advice.
version: "1.0.0"
type: prompt-flow
tags:
  - home-admin
  - decluttering
  - donations
  - logistics
  - checklist
author: Bell (design)
---

# Donation Drop-off Planner

## Overview

Donation Drop-off Planner helps users turn donation clutter into labeled, ready-to-move bundles. It sorts user-listed items by condition, likely destination type, packing needs, and drop-off logistics. The deliverable is a practical donation plan with bag labels, a packing checklist, and a drop-off day action list.

This skill is for donation logistics only. It does not estimate fair market value, prepare tax records, determine deductibility, or give tax advice. If the user asks about tax value, direct them to official tax guidance, a qualified tax professional, or the donation organization's receipt policy.

## When to Use

Use this skill when the user wants help with:

- Clearing a pile of items for donation
- Sorting clothing, books, toys, household goods, or small electronics
- Creating labels for bags or boxes
- Planning a drop-off route or pickup preparation
- Avoiding donation chaos before a move, spring clean, or closet reset

**Trigger phrases:** "Help me donate these items", "Make a donation drop-off checklist", "Sort my donation pile", "What should go in each donation bag", "Plan a charity drop-off"

## Required Inputs

Ask for only the missing essentials. If the user already listed items, continue with that list.

- Item list or rough categories
- Condition notes: new, good, worn, damaged, missing parts, needs washing
- User location constraints at a high level, if relevant, such as has a car, walking, pickup only, limited time
- Preferred destination types, such as thrift store, shelter, library sale, school drive, animal shelter, electronics recycler, textile recycling
- Drop-off deadline or available time window
- Packing supplies available: bags, boxes, labels, tape, bins

Do not ask for receipts, income information, tax bracket, item prices, or donation values.

## Workflow

### Step 1 - Sort by Condition

Group the items into practical categories:

- Donate ready: clean, working, complete, and acceptable for most organizations
- Clean or repair first: useful but needs laundering, wiping, batteries removed, or parts gathered
- Check rules first: electronics, mattresses, car seats, cribs, helmets, open toiletries, medical items, large furniture, hazardous items, or anything with safety concerns
- Do not donate: unsafe, recalled, broken beyond use, dirty, pest-exposed, moldy, heavily stained, or unsanitary items
- Recycle or dispose: items that are not donation-suitable but may have a recycling route

Be direct when an item should not be donated. Donation is not a dumping route.

### Step 2 - Match Destination Types

Suggest destination types based on item category, without claiming a specific organization will accept them unless the user has already verified it.

Common matches:

- Clothing and shoes: thrift store, shelter, mutual aid drive, textile recycling for worn fabric
- Books: library sale, school, little free library, thrift store
- Toys and kids items: family charity, school, community group, thrift store, with safety checks
- Kitchenware and home goods: thrift store, refugee support group, community pantry, shelter
- Pet supplies: animal shelter or rescue, if clean and allowed
- Electronics: certified electronics recycler or organization that explicitly accepts working devices
- Furniture: pickup charity, local reuse group, or shelter, if clean and safe

Tell the user to verify current acceptance rules, hours, and pickup requirements before loading the items.

### Step 3 - Create Bag and Box Labels

Create clear labels the user can write on tape or paper:

- Destination type
- Item category
- Condition status
- Action needed before drop-off
- Priority or deadline

Example labels:

- "Thrift - clean adult clothes - ready"
- "Library sale - books - ready"
- "Check rules - small electronics - verify first"
- "Textile recycling - worn fabric - not for resale"

### Step 4 - Build the Packing Checklist

Include practical packing steps:

- Wash or wipe items that need it
- Pair shoes and bundle cords
- Remove personal data from devices before donation or recycling
- Bag clothing by type or size if helpful
- Box heavy books in small boxes
- Keep fragile items padded and labeled
- Separate items requiring rule checks
- Put "do not donate" items aside for safe disposal or recycling

### Step 5 - Plan the Drop-off

Create a simple drop-off action card:

- Confirm destination hours and accepted items
- Confirm whether appointment, pickup request, or unloading instructions are required
- Load items in reverse order if visiting multiple locations
- Bring labels, tape, and a small cleanup bag
- Ask for a receipt only if the user wants one for personal records; do not assign value
- Mark any rejected items for alternate reuse, recycling, or disposal

## Output Format

Use this structure:

1. **Donation Goal** - one sentence
2. **Sorted Item Plan** - item groups with condition and action
3. **Bag and Box Labels** - ready-to-copy labels
4. **Packing Checklist** - before-loading steps
5. **Drop-off Plan** - route/order checklist and verification reminders
6. **Do Not Donate / Verify First** - safety and rule-check list
7. **Tax Boundary** - brief note that no valuation or tax advice is provided

## Safety Boundaries

- Focus on donation logistics, sorting, packing, and drop-off preparation.
- Do not provide tax valuation, deductibility guidance, appraisal methods, or tax advice.
- Do not claim a specific charity accepts an item unless the user has verified it.
- Flag unsafe, unsanitary, recalled, broken, pest-exposed, moldy, or hazardous items as not donation-ready.
- Remind the user to remove personal data from electronics before donation or recycling.
- Suggest official recycling or disposal routes for unsuitable items.
- Encourage verifying current organization rules, hours, pickup limits, and item restrictions.

## Acceptance Criteria

1. Output groups items by condition and donation readiness.
2. Output includes destination-type suggestions without guaranteeing acceptance.
3. Output provides ready-to-use bag or box labels.
4. Output includes a packing checklist and drop-off checklist.
5. Unsafe or unsanitary items are flagged as do-not-donate or verify-first.
6. Tax valuation and tax advice are explicitly excluded.
7. No web search, external API use, credentials, executable code, or file automation is required.

## Example Prompts

- "Help me donate these items: three bags of clothes, old books, a lamp, and some kitchen stuff."
- "Make a donation drop-off checklist for my closet cleanout."
- "Sort my donation pile and create bag labels for each destination."

## Examples

### Example 1: Closet Cleanout

**User says:** "I have two bags of clothes, some stained shirts, old sneakers, and three coats. Help me donate."

**Skill guides:** Sort clean wearable clothes and coats as donation-ready, stained shirts as textile recycling or disposal depending on condition, and sneakers as donate-ready only if clean and wearable. Create labels and a loading checklist.

### Example 2: Mixed Garage Pile

**User says:** "Donate: lamp, broken toaster, books, old phone, kids helmet, dishes."

**Skill guides:** Put books and clean dishes in donation-ready or check rules groups, lamp in working-condition check, broken toaster in recycling/disposal, old phone in data-wipe plus electronics route, and kids helmet in safety verify-first or do-not-donate.

### Example 3: Tax Value Request

**User says:** "What tax value should I put on each bag?"

**Skill responds:** Explain that the skill does not provide valuation or tax advice. Offer to make a non-valued inventory and suggest checking official tax guidance, a qualified tax professional, or the organization's receipt policy.
