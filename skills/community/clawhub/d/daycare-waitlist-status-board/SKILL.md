---
name: daycare-waitlist-status-board
description: "Build a privacy-conscious daycare waitlist status board with provider contacts, licensing checks, policy questions, availability signals, follow-up dates, and decision notes. Use when the user is comparing childcare waitlist options without exposing private child details."
---
# Daycare Waitlist Status Board

## Purpose

Turn scattered childcare waitlist notes into a clear status board for comparing daycare, preschool, nursery, or early-childhood program options. The board helps the user track application status, follow-up timing, licensing checks, policy questions, availability signals, visit notes, and enrollment next steps.

This is a prompt-only family admin workflow. It is not childcare, legal, medical, licensing, safety, or parenting advice. The user must verify licensing status, policies, availability, costs, health requirements, and enrollment terms directly with official provider and regulator sources.

## Use This Skill When

Use this skill when the user needs to organize childcare waitlist logistics, especially when:

- They have applied to multiple daycare or preschool programs and need one comparison board.
- They need a follow-up cadence that is polite and not spammy.
- They want provider-specific questions about licensing, ratios, hours, fees, meals, naps, sick policies, holidays, pickup rules, and start dates.
- They need to track offers, deposits, tours, paperwork, and decision deadlines.
- They want a version of the board that avoids unnecessary private child details for sharing with another caregiver.

Do not use this skill to judge whether a program is safe based only on incomplete information, replace official licensing checks, collect sensitive child details, or pressure a provider for unfair priority.

## Best Inputs

Ask only for the details needed to build the board. Keep child information minimal and avoid including private details in shared artifacts.

- Program name, campus, neighborhood, phone or general email, and application date.
- Current waitlist status, estimated opening window, age group or classroom category, and desired start month.
- Tour status, deposit status, application fee status, paperwork needed, and decision deadline.
- Public licensing link or regulator name if available.
- Program policies the user wants to compare: hours, holidays, sick policy, food, naps, diapers, toilet learning, pickup authorization, security, communication app, late fees, and withdrawal terms.
- User priorities: commute, schedule fit, budget range, language, outdoor time, meals, curriculum, caregiver ratio, or sibling coordination.
- Follow-up history: date contacted, channel, staff name or role, response, and promised next update.

Avoid asking for full child name, birth certificate, medical record numbers, immunization records, custody documents, home address, payment data, or unnecessary identifying details unless the user explicitly needs a private, non-shared checklist.

## Workflow

1. **Define the board scope.** Decide whether the output is for private planning or sharing with a partner, and redact private child details for any shared version.
2. **Create one row per program.** Capture provider name, location, status, desired start window, application date, last contact, next follow-up, and decision deadline.
3. **Add licensing and policy checks.** Include columns for official licensing verification, inspection or regulator review, policies, ratio questions, health rules, fee terms, and enrollment documents.
4. **Track availability signals.** Record waitlist position if provided, estimated opening, classroom age group, part-time or full-time option, tour availability, and deposit requirements.
5. **Score only stated priorities.** Use the user's own priorities, such as commute, hours, cost, schedule fit, or communication style; do not infer safety or quality from incomplete facts.
6. **Draft follow-up messages.** Create polite, concise messages asking for current waitlist status, likely timing, tour options, policy documents, and next steps.
7. **Prepare a decision checkpoint.** List what must be verified before accepting an offer or paying a deposit.
8. **Protect privacy.** Remove unnecessary child identifiers, medical details, payment details, and family-sensitive notes from the board unless it is explicitly private.

## Output Format

Return the status board in this order:

1. **Privacy Note**

State whether the board is private or share-safe. If share-safe, confirm that private child details should be omitted.

2. **Waitlist Status Board**

| Program | Location | Status | Desired start | Last contact | Next follow-up | Availability signal | Decision deadline |
|---|---|---|---|---|---|---|---|

3. **Licensing and Policy Verification Board**

| Program | Licensing check source | Current verification status | Ratio or staffing question | Health and sick policy | Fees and deposit terms | Documents needed |
|---|---|---|---|---|---|---|

4. **Priority Fit Notes**

| Program | Commute or schedule fit | Cost fit | Care model or curriculum notes | Communication notes | Concerns to verify |
|---|---|---|---|---|---|

5. **Follow-Up Message Templates**

Provide short copy-ready messages for:

- Initial waitlist status check.
- Post-tour follow-up.
- Offer clarification before deposit.
- Polite monthly update request.

6. **Decision-Ready Checklist**

| Item to verify | Why it matters | Verified? | Source or contact |
|---|---|---|---|
| Official licensing status | | | |
| Opening date and schedule | | | |
| Total monthly cost and fees | | | |
| Deposit and refund terms | | | |
| Health, sick, and medication policy | | | |
| Pickup, emergency, and authorization policy | | | |
| Required forms and deadlines | | | |

7. **Open Questions**

A short list of missing facts to confirm directly with each provider.

## Message Style

- Be organized, tactful, and privacy-conscious.
- Use neutral language such as "availability signal," "verification needed," and "policy to confirm."
- Keep follow-up messages short and respectful of provider workload.
- Avoid ranking a provider as safe or unsafe unless the user provides official regulator findings and asks only for a documentation summary.
- Avoid private child details in shareable outputs.

## Safety Boundary

- This skill helps organize waitlist administration only; it does not provide childcare, safety, legal, medical, licensing, or parenting advice.
- Always tell the user to verify licensing, inspections, policies, staff ratios, fees, enrollment deadlines, and availability through official provider or regulator sources.
- Do not collect or expose unnecessary child details, medical records, custody documents, home addresses, payment information, or identity documents.
- Do not include private child details in shared artifacts; use initials, age range, or classroom category only when needed.
- Do not tell the user to misrepresent application details, pressure staff unfairly, skip required paperwork, or bypass safety policies.

## Example Prompts

- "Organize our daycare waitlist status across three preschools into one board."
- "Draft a polite follow-up message to check our waitlist position."
- "Build a licensing and policy verification board so I know what to confirm before enrolling."
