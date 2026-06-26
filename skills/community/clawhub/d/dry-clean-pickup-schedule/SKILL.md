---
name: dry-clean-pickup-schedule
displayName: "Dry-Clean Pickup Schedule Keeper"
version: "1.0.0"
description: "Create a simple dry-cleaning pickup tracker and bag tag note template for dropped-off garments, pickup dates, special notes, and reminder text, without handling payments, disputes, or accounts."
triggerKeywords:
  - dry cleaning pickup schedule
  - dry clean tracker
  - laundry pickup reminder
  - dry cleaner bag tag
  - garment pickup checklist
  - cleaning ticket tracker
  - clothes drop off tracker
  - pickup date reminder
tags:
  - home-admin
  - errands
  - clothing
  - scheduling
  - checklist
license: "MIT-0"
language: "en"
hasExecutableCode: false
promptOnly: true
execution: "noExec"
---

# Dry-Clean Pickup Schedule Keeper

## Purpose

Use this prompt-only skill when a user has dropped off dry cleaning, alterations, or special garment cleaning and wants a simple tracker so pickup dates, ticket numbers, garment notes, and reminder text are not forgotten. The deliverable is a pickup tracker plus a bag tag note template.

This skill is for ordinary household scheduling and item memory. It does not handle payment, refunds, billing disputes, damage claims, insurance claims, chargebacks, customer accounts, loyalty accounts, passwords, or official communication with the dry cleaner.

## Safety Boundary

Do not ask for or manage payment cards, receipts with full payment details, account logins, loyalty credentials, private account numbers, claim forms, dispute evidence, legal threats, refund demands, or compensation requests.

Do not decide who is at fault for missing, damaged, stained, or delayed garments. Do not draft dispute messages or negotiate with a dry cleaner. If the user has a payment issue, damage issue, missing item, or account problem, tell them this skill can organize neutral facts only and they should contact the cleaner directly.

Keep output limited to scheduling, neutral garment notes, ticket references, reminder text, and pickup preparation.

## Required Inputs

Ask only for practical pickup details:

- Cleaner name or pickup location nickname.
- Drop-off date.
- Promised pickup date and time window.
- Ticket number or claim check reference, if the user wants to include it.
- Garment categories, such as suit, coat, dress, shirt, sweater, uniform, curtains, or household textile.
- Count of items.
- Neutral special notes, such as press only, stain pointed out, alteration, hang dry, fold, bag separately, or fragile trim.
- Whether someone else may pick up the order and what neutral reminder they need.
- Preferred reminder timing, such as day before, morning of, or after work.
- Where the claim ticket is stored.

If details are unknown, mark them as "confirm with cleaner" rather than inventing them.

## Workflow

1. **Record the order snapshot.** Capture cleaner name, drop-off date, pickup date, ticket reference, and item count.
2. **List garments neutrally.** Group by category and note count, color, owner initials if useful, and non-sensitive special notes.
3. **Mark pickup readiness.** Identify what to bring: ticket, reusable garment bag, ID if the cleaner requires it, and any hangers or bags to return.
4. **Create reminder text.** Draft short reminders for calendar, phone, sticky note, or household message without making any external send action.
5. **Create bag tag note.** Provide a compact note the user can attach to the ticket, closet hook, or entryway bag.
6. **Flag confirm items.** Note uncertain pickup date, missing ticket, special instruction, altered item, or pickup authorization to confirm directly with the cleaner.
7. **Prepare after-pickup check.** Include quick item count, garment bag check, ticket storage, and next errand note.

## Tracker Categories

Use categories that fit the order:

- Ready for pickup: date known, ticket stored, reminder set.
- Confirm date: pickup date or time window unclear.
- Confirm instruction: special cleaning or alteration note unclear.
- Bring item: ticket, reusable bag, hanger return, coupon if already available, or cleaner-required ID.
- Pickup helper: neutral note for household member or assistant.
- After pickup: count items, inspect enough to confirm the order is complete, hang up garments, recycle packaging, and file ticket.

Avoid payment tracking, refund calculations, account management, dispute evidence, or blame language.

## Output Format

Return a one-page dry-clean pickup schedule with these sections:

1. **Order Snapshot**
   - Cleaner or location
   - Drop-off date
   - Pickup date and time window
   - Ticket reference
   - Item count
2. **Garment Tracker**
   - Item or group
   - Count
   - Color or identifier
   - Neutral special note
   - Pickup status
3. **Reminder Plan**
   - Day-before reminder text
   - Day-of reminder text
   - Optional household note
   - Where to place the reminder
4. **What to Bring**
   - Ticket or claim check
   - Reusable garment bag
   - Hangers or packaging to return
   - Any cleaner-required ID note, if already known
5. **Bag Tag Note Template**
   - Cleaner
   - Pickup date
   - Ticket reference
   - Item count
   - Special note summary
6. **Confirm With Cleaner**
   - Unknown detail
   - Why it matters
   - Status
7. **Pickup Checklist**
   - Bring ticket
   - Check item count
   - Collect all bags or boxed items
   - Save or discard ticket as desired
   - Hang or unpack garments at home
8. **Next Errand Note**
   - Return date if needed
   - Repair or alteration follow-up if already planned
   - Closet or packing reminder

## Quality Bar

A strong tracker prevents missed pickup dates and lost-item confusion while staying neutral and lightweight. It should help the user remember what was dropped off, when to pick it up, what to bring, and what to confirm, without touching payments, disputes, claims, or accounts.

## Example Prompts

1. **Basic pickup tracker:** "I dropped off 4 dress shirts, 2 suits, and a coat at Sunny Cleaners on Monday. They said pickup is Thursday after 4pm. Ticket #4421. Make me a pickup tracker with reminders."

2. **Multi-garment with special notes:** "I have a mixed order at QuickPress: 3 dresses (press only), 2 sweaters (fold, don't hang), and a winter coat with a torn lining they said they'd note. Drop-off was Saturday, pickup promised Wednesday. I need a bag tag too."

3. **Household reminder format:** "Help me track dry cleaning pickups for the week. I have orders at two different cleaners, and my partner might pick up one of them. I need a shared reminder note."
