# Change Management & Scope Control

## Purpose

This reference defines how the PM handles change requests after an SRS has been signed off and work has begun. Scope creep is the number one killer of project timelines and budgets. A clear protocol protects the client, the engineering team, and the project.

## Core Principle

Once an SRS is signed off, every new request is a **change request** until proven otherwise. This isn't bureaucratic — it's protective. It ensures that new requests are properly assessed for impact before being absorbed into the work stream, and that the client understands the consequences of changes.

## Change Request Flow

```
Client mentions a change
        │
        ▼
PM captures the request (Change Request Log)
        │
        ▼
PM classifies impact level (1-5)
        │
        ├── Level 1-2 (Cosmetic / UI-Only)
        │   PM can assess impact directly
        │   ▼
        │   Present impact to client → Approve/Decline
        │   ▼
        │   If approved: Update SRS, update Asana, proceed
        │
        └── Level 3-5 (Logic / Data / Cross-cutting)
            PM sends to engineer for assessment
            ▼
            Engineer returns impact analysis
            ▼
            PM translates for client → Present options
            ▼
            Client decides: Approve / Modify / Defer / Decline
            ▼
            If approved: Update SRS (new version), update
            engineering plan if needed, update Asana tasks,
            communicate revised timeline
```

## Impact Classification Reference

### Level 1 — Cosmetic / Copy Changes
**What it is:** Text changes, label updates, color adjustments, typo fixes.
**System impact:** None. No logic, data, or workflow changes.
**PM action:** Assess directly. No engineer needed. Minimal effort — update SRS and create/update Asana task.
**Timeline impact:** None to negligible.
**Example:** Client wants a button to say "Submit Request" instead of "Submit."

### Level 2 — UI-Only Changes
**What it is:** Layout changes, adding static UI elements, style overhauls, reorganizing existing content display.
**System impact:** Frontend only. No logic or data changes.
**PM action:** Quick engineer consult to confirm no hidden complexity, then present to client.
**Timeline impact:** Typically 1-3 days added.
**Example:** Client wants the dashboard layout reorganized so charts appear above the data table instead of below.

### Level 3 — Logic Changes
**What it is:** New validation rules, conditional display logic, workflow changes, business rule modifications.
**System impact:** Frontend and/or backend logic. May affect multiple components but not the data model.
**PM action:** Full engineer assessment required. Changes to this level and above require SRS amendment.
**Timeline impact:** Typically 3-10 days added.
**Example:** Client wants a new approval step in an existing workflow — when a user submits a form, it now goes to a manager for review before processing.

### Level 4 — Data Model Changes
**What it is:** New database fields, schema changes, data migration requirements, changes to how data is stored or structured.
**System impact:** Database + backend + potentially frontend. May require data migration for existing records.
**PM action:** Full technical assessment. SRS amendment. Possibly revised engineering plan. Risk assessment for data migration.
**Timeline impact:** Typically 1-3 weeks added.
**Example:** Client wants to track a new attribute for each customer record that needs to be searchable, sortable, and included in exports.

### Level 5 — Integration / Cross-Cutting Changes
**What it is:** New external integrations, changes affecting multiple modules simultaneously, new subsystem requirements, architectural implications.
**System impact:** Multiple system layers and potentially external systems. May require new infrastructure.
**PM action:** Full cycle: technical assessment → SRS amendment → engineering plan review → Asana rebuild for affected areas. Essentially a mini-project within the project.
**Timeline impact:** Typically 2-6 weeks added.
**Example:** Client wants the system to sync data bidirectionally with their CRM (Salesforce), including real-time updates.

## Scope Creep Detection

Scope creep often doesn't announce itself. Watch for these signals during client interactions:

### Gradual Expansion Signals
- "Oh, and while you're working on that, could you also..."
- "I assumed that was included"
- "Just one more small thing..."
- "Can we make it so that it also..." (feature stacking)
- Requirements that reference functionality not in the SRS

### Ambiguity Exploitation
- Client interprets a vague SRS requirement broadly
- "When you said 'reports,' I thought that included [thing not specified]"
- This is why specific, testable acceptance criteria in the SRS are so important — they prevent ambiguity from becoming scope creep

### Legitimate Clarification vs. Scope Creep
Not every client question is scope creep. Distinguish between:

| Clarification (Not Scope Creep) | Scope Creep |
|-------------------------------|------------|
| "What color will the button be?" (detail within scope) | "Can we add another button that does X?" (new functionality) |
| "Will this work on tablets too?" (verifying stated requirements) | "Actually, we need a native mobile app version too" (new platform) |
| "Can you explain how the export will work?" (understanding) | "Can you add three more export formats?" (new requirements) |

### Responding to Scope Creep

When you detect scope creep, respond professionally and clearly:

"That's a great idea, and I can see how it would add value. Since this wasn't part of our agreed-upon requirements in the SRS, I'll need to log this as a change request so we can properly assess the impact on timeline and cost. Let me document what you're describing, and I'll get back to you with an assessment."

This response:
1. Validates the client's idea (doesn't dismiss them)
2. Clearly identifies it as outside scope (not combative, just factual)
3. Commits to following the proper process
4. Sets expectations for what happens next

## SRS Amendment Protocol

When a change request is approved:

1. **Create a new SRS version.** Never edit the signed-off version in place.
2. **Increment version number.** Major scope changes: increment whole number (2.0). Minor adjustments: increment decimal (1.1).
3. **Update the Change Log** (SRS Section 11) with:
   - New version number
   - Date
   - Description of changes
   - Change Request ID that prompted the change
4. **Update all affected sections:**
   - New/modified requirements with IDs
   - Updated acceptance criteria
   - Updated Cost & Effort Analysis
   - Updated Assumptions & Dependencies (if applicable)
   - Updated Out of Scope (if items moved in or out)
5. **Mark changed items clearly.** Use `[NEW in v2.0]` or `[MODIFIED in v1.1]` tags next to changed requirements so the client can quickly see what's different.
6. **Client re-review.** The client must review and approve the amended SRS before engineering proceeds with the changes.
7. **Update Asana.** Create new tasks or modify existing ones to reflect the approved changes. Tag them with the change request ID.

## Communication Templates for Change Scenarios

### Acknowledging a Change Request
"Thank you for that feedback. I've logged this as Change Request CR-[XXX]. Since this involves [level description — e.g., 'changes to the system's data structure'], I'll need to coordinate with engineering to assess the impact. I'll have an assessment for you by [date]."

### Presenting Change Impact
"Here's what we found about your requested change (CR-[XXX]):

The change would [plain-language description of what it involves]. It affects [areas of the system]. We estimate it would add approximately [time range] to the project timeline and [cost range] in additional effort.

Your options:
1. Approve as-is — we'll amend the SRS and adjust the timeline
2. Modify the request — [suggest a lighter alternative if possible]
3. Defer to a future phase — we'll document it for later
4. Decline — no changes to current plan

What would you prefer?"

### Pushing Back on Excessive Changes
If a client submits many change requests that would fundamentally alter the project:

"I want to make sure we're set up for success here. We've received [X] change requests since the SRS was signed off, and together they represent a significant shift in the project's scope. Rather than continuing to amend the existing SRS piecemeal, I'd recommend we pause and do a focused requirements review to reassess the overall direction. This will give us a cleaner, more cohesive plan rather than a patchwork of amendments. Would you be open to scheduling time for that?"

## Tracking Change Requests

Maintain a running log of all change requests for a project. This serves as both a project management record and an audit trail.

```
CHANGE REQUEST LOG
Project: [Project Name]
SRS Base Version: [X.X]

| CR ID | Date | Description | Level | Status | SRS Impact | Decision | Decision Date |
|-------|------|-------------|-------|--------|------------|----------|--------------|
| CR-001 | ... | ... | 3 | Approved | v1.1 | Approved | ... |
| CR-002 | ... | ... | 1 | Completed | v1.1 | Approved | ... |
| CR-003 | ... | ... | 4 | Under Review | TBD | Pending | — |
| CR-004 | ... | ... | 2 | Declined | None | Declined | ... |
```

Keep this log accessible and reference it during status updates when relevant. It demonstrates that scope is being managed deliberately and that every change was properly assessed.
