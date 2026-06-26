# Requirements Elicitation Framework

## Purpose

This framework guides the PM through structured discovery conversations with clients. The goal is to extract what the client actually needs — which is often different from what they initially ask for — and document it clearly enough for engineering assessment.

## The Elicitation Mindset

Clients describe solutions ("I want a dropdown menu"). Your job is to find the problem ("I need users to select from a list of options quickly without typing"). The solution might be a dropdown, or it might be autocomplete, radio buttons, or something else entirely. By understanding the problem, you give engineering the freedom to recommend the best approach.

**Three questions that should underpin every discovery:**
1. What problem are you trying to solve? (the "why")
2. Who experiences this problem and how? (the "who" and "when")
3. How will you know the solution is working? (the success criteria)

## Elicitation Process

### Step 1: Contextual Opening

Start by understanding the big picture before diving into specifics.

**Opening questions:**
- "Tell me about what prompted this request. What's happening in your business or with your users that made this a priority?"
- "Who are the main users affected by this? How do they currently handle this?"
- "Is there a deadline or event driving the timeline?"
- "Have you tried any workarounds or temporary solutions?"

The answers establish business context, user context, urgency, and the current state — all of which shape how you interpret specific requirements.

### Step 2: Feature-Level Discovery

For each feature or change the client describes, walk through this question sequence. You don't need to ask every question for every feature — use judgment — but cover the key areas.

**Understanding the request:**
- "Walk me through how you'd like this to work from the user's perspective, step by step."
- "What should happen when [edge case]?" (empty state, error, too many results, no permission, etc.)
- "Is this for all users or specific roles/groups?"
- "How does this relate to other parts of the system you use?"

**Clarifying scope:**
- "When you say [client's term], can you describe exactly what you mean?" (Clients use imprecise language — "report" could mean a dashboard, a PDF export, an email summary, or a data table)
- "Are there any existing features that are similar to what you're describing?"
- "What's the minimum version of this that would solve your problem?" (Identifies the Must-Have core)
- "What would the ideal version look like if there were no constraints?" (Identifies Nice-to-Haves)

**Uncovering hidden requirements:**
- "Who else uses this area of the system? How might this change affect them?"
- "Do you need this to work on mobile devices?"
- "Should there be any notifications or alerts associated with this?"
- "How should permissions work? Who can see/do what?"
- "Is there any regulatory, compliance, or audit requirement we should account for?"
- "What data is involved? Does any of it need to be preserved or migrated?"
- "Do you have reporting or export needs for this data?"

### Step 3: Priority Classification (MoSCoW)

After you've captured the requirements, classify each one with the client:

| Priority | Definition | Client-Friendly Explanation |
|----------|------------|---------------------------|
| **Must-Have** | The project fails without this | "If we don't deliver this, the project isn't useful" |
| **Should-Have** | Important but the project is usable without it | "We strongly want this, but we could launch without it and add it soon after" |
| **Nice-to-Have** | Desired but not critical | "If we have time and budget, we'd love this, but it's not a dealbreaker" |
| **Out-of-Scope** | Explicitly excluded | "We're not doing this now — maybe in a future phase" |

**Key facilitation technique:** Clients often mark everything as Must-Have. Counter this by asking: "If you had to launch with only three of these features, which three?" This forces real prioritization.

### Step 4: Conflict Detection

Before finalizing the requirements summary, check for these common conflict patterns:

**Contradiction conflicts:**
- Requirement A says users can delete records; Requirement B says all records must be retained for audit. → Resolution: soft delete vs. hard delete distinction.

**Resource conflicts:**
- Requirement A and B are both Must-Have but technically dependent on the same system change, and the client wants them simultaneously. → Flag for engineering to assess parallelization.

**Expectation conflicts:**
- Client expects real-time updates but also expects minimal system load/cost. → Surface the trade-off explicitly.

**Scope conflicts:**
- Client verbally agrees something is out of scope but later describes a requirement that implicitly depends on it. → Surface the dependency.

**Priority vs. dependency conflicts:**
- A Should-Have feature is a technical prerequisite for a Must-Have feature. → Recommend reclassifying the Should-Have as Must-Have.

For each conflict identified, document it with both sides and present it to the client for resolution. Don't resolve conflicts unilaterally.

### Step 5: Validation Summary

End every elicitation session by playing back what you heard. This isn't just politeness — it catches misunderstandings before they become expensive.

"Let me make sure I have this right. You need [summary of key requirements]. The most critical items are [Must-Haves]. You're not including [Out-of-Scope items] at this stage. Does that match your understanding?"

Then produce the formal Requirements Summary using the template in `templates.md`.

## Special Scenarios

### Existing Software — Client Requests Changes

The audit-first approach is essential here. Before you can have a productive conversation about what to change, you need to know what exists. Follow this sequence:

1. **Client describes what they want changed** — capture at a high level, don't deep-dive yet
2. **Request Software Audit from engineer** — focused on the areas the client mentioned
3. **Review audit results** — understand current functionality, dependencies, technical debt
4. **Resume client conversation** — now grounded in reality: "Here's what we found about how that area currently works. Based on this, let's walk through your requests in more detail."
5. **During elicitation, reference current state** — "You mentioned you want to change X. Currently X works by [audit finding]. You'd like it to instead [client's request]. Is that accurate?"

This approach prevents the PM from agreeing to things that are more complex than they appear, and gives the client realistic context.

### 0-to-1 New Build

No audit needed, but extra attention to:
- **Competitive references:** "Are there existing products or features in other tools that do something similar to what you want?" This grounds the conversation in concrete examples.
- **User journey mapping:** "Walk me through a day in the life of your primary user. Where does this software fit in?"
- **MVP definition:** "What's the absolute minimum we need to build for this to be valuable?" Resist the temptation to scope the full vision in v1.
- **Technical environment:** "What existing systems, if any, does this need to integrate with?"

### Client Provides Mockups

Mockups are valuable but can be misleading. Treat them as conversation starters, not specifications.

1. **Acknowledge and validate:** "Thanks for putting this together — it gives me a great starting point for understanding what you're envisioning."
2. **Extract the intent:** For each element in the mockup, ask "What problem does this solve?" or "What does this enable the user to do?" The layout may change but the intent should be preserved.
3. **Flag assumptions:** Mockups often assume things that aren't feasible or that conflict with existing functionality. Note these for the engineer to assess.
4. **Request engineer comparison:** Send the mockup to the engineer via the UI Comparison Request to get an assessment of current vs. proposed and any technical concerns.
5. **Present back:** Show the client the engineer's HTML/CSS rendering of the proposed interface alongside their mockup. Discuss differences and iterate.

## Question Bank Quick Reference

When you're mid-conversation and need a prompt, scan this list:

**Opening / Big Picture:**
- What problem are we solving?
- Who is affected and how?
- What's driving the timeline?
- What does success look like?

**Feature Details:**
- Walk me through the user flow.
- What happens in edge cases?
- Who has access to this?
- How does this connect to other features?

**Hidden Requirements:**
- Mobile compatibility?
- Notifications?
- Permissions and roles?
- Data migration?
- Reporting/export needs?
- Compliance/regulatory?

**Prioritization:**
- If you could only have three features, which ones?
- What's the minimum useful version?
- What would the dream version include?

**Validation:**
- Did I capture this correctly?
- Is anything missing?
- Does the priority feel right?
- Any concerns about what we've scoped?
