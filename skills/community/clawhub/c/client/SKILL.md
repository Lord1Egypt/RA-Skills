---
name: client
description: >
  Design, manage, and improve client relationships across sales, onboarding, delivery,
  communication, retention, and account growth. Use when someone needs to work with
  clients more effectively from first agreement through long-term relationship success.
---

# Client

A client is not just a customer who paid.

A client is an ongoing relationship that must be understood, managed, and delivered on.

Most client problems do not begin at the moment of complaint. They begin much earlier:
at misaligned expectations, weak onboarding, unclear communication, vague scope,
slow follow-up, hidden decision-makers, or a relationship that was never actively managed.

This skill helps build stronger client systems so the relationship works in practice,
not just in theory.

## Trigger Conditions

Use this skill when the user needs to:
- onboard a new client
- improve a client relationship
- manage client communication
- define expectations, scope, and boundaries
- reduce churn, confusion, or friction
- improve delivery, handoff, or account management
- prepare client-facing processes, documents, or messaging
- identify what makes a client relationship succeed or fail

Also trigger when the user says things like:
- "Help me manage this client"
- "How do I onboard a client"
- "My client relationship is messy"
- "How do I set expectations better"
- "How do I retain clients"
- "What should I send a new client"
- "How do I handle difficult clients"

## Core Principle

A healthy client relationship depends on clarity before complexity.

Clients rarely become difficult for no reason.
More often, the relationship was built on assumptions that were never made explicit:
what success means, who decides, how communication works, what is included, what is not,
how changes are handled, and what happens when problems appear.

Good client management creates trust by reducing ambiguity.

## What This Skill Does

This skill helps:
- define what a client relationship requires to work well
- improve onboarding, communication, and delivery systems
- clarify scope, ownership, and expectations
- identify risks in client management before they become problems
- structure client-facing documents, workflows, and touchpoints
- improve retention, trust, and long-term account quality
- turn ad hoc service into a more stable client system

## Default Outputs

Depending on the request, produce one or more of the following:

1. Client Onboarding Plan  
A structured process for starting the relationship well.

2. Client Communication Framework  
Rules, cadences, and templates for updates, feedback, and next steps.

3. Client Success Map  
A relationship model showing goals, expectations, milestones, and risk points.

4. Scope and Boundary Framework  
A structure for what is included, excluded, change-controlled, and escalated.

5. Client Risk Audit  
A diagnosis of likely friction points, misunderstandings, or retention threats.

6. Retention and Growth Plan  
A system for maintaining trust, expanding value, and deepening the relationship over time.

## Response Rules

When responding:
- identify the type of client relationship
- define what success means for both sides
- separate sales promises from delivery reality
- reduce ambiguity around scope, timing, and communication
- surface risks early
- distinguish relationship issues from process issues
- make ownership explicit
- prefer clarity, trust, and usability over performative sophistication

## Client Lifecycle
~~~python
CLIENT_LIFECYCLE = {
  "stage_1_pre_close": {
    "purpose": "Ensure the relationship is sold honestly and clearly",
    "focus": [
      "expectation setting",
      "fit assessment",
      "decision-maker mapping",
      "scope clarity",
      "risk signals before close"
    ]
  },
  "stage_2_onboarding": {
    "purpose": "Start the relationship with alignment and momentum",
    "focus": [
      "intake",
      "goals",
      "roles",
      "timeline",
      "deliverables",
      "communication norms"
    ]
  },
  "stage_3_active_delivery": {
    "purpose": "Deliver value while keeping expectations aligned",
    "focus": [
      "updates",
      "feedback loops",
      "change handling",
      "issue resolution",
      "progress visibility"
    ]
  },
  "stage_4_stabilization": {
    "purpose": "Move from reactive execution to a steady working rhythm",
    "focus": [
      "relationship trust",
      "predictability",
      "repeatability",
      "reduced confusion",
      "review cadences"
    ]
  },
  "stage_5_retention_growth": {
    "purpose": "Preserve and expand a valuable relationship",
    "focus": [
      "renewal readiness",
      "new opportunities",
      "expansion",
      "risk prevention",
      "long-term fit"
    ]
  }
}
~~~

## Client Relationship Architecture
~~~python
CLIENT_ARCHITECTURE = {
  "core_elements": {
    "outcome": "What the client is actually trying to achieve",
    "scope": "What is and is not included",
    "timeline": "When key milestones happen",
    "communication": "How updates, questions, and decisions are handled",
    "ownership": "Who is responsible for what",
    "success_measure": "How both sides know things are going well",
    "change_management": "How revisions, additions, and surprises are handled"
  },
  "guiding_questions": [
    "Why did this client hire us",
    "What do they think they bought",
    "What do we think we are delivering",
    "Who influences satisfaction and renewal",
    "What would make this relationship fail",
    "What is unclear right now that may become expensive later"
  ]
}
~~~

## Client Onboarding Framework
~~~python
CLIENT_ONBOARDING = {
  "step_1_alignment": {
    "purpose": "Confirm goals, scope, and expectations",
    "outputs": [
      "desired outcome",
      "success criteria",
      "constraints",
      "key contacts",
      "timeline assumptions"
    ]
  },
  "step_2_information_gathering": {
    "purpose": "Collect what is needed to start well",
    "outputs": [
      "intake information",
      "documents",
      "access",
      "history",
      "preferences",
      "known risks"
    ]
  },
  "step_3_working_model": {
    "purpose": "Define how the relationship will operate",
    "outputs": [
      "meeting cadence",
      "communication channel",
      "approval process",
      "feedback mechanism",
      "escalation path"
    ]
  },
  "step_4_first_value": {
    "purpose": "Create early confidence through visible progress",
    "outputs": [
      "quick win",
      "first milestone",
      "clear next step",
      "evidence of momentum"
    ]
  }
}
~~~

## Common Client Failure Patterns
~~~python
CLIENT_FAILURE_PATTERNS = {
  "patterns": [
    "Scope was never truly understood",
    "The buyer and day-to-day stakeholder wanted different things",
    "Communication rhythm was too vague",
    "The client did not understand what was required from them",
    "Problems were noticed late and discussed vaguely",
    "Too much was customized informally",
    "No one tracked satisfaction until renewal time",
    "The provider focused on output while the client cared about outcome"
  ],
  "responses": [
    "Re-clarify goals and success criteria",
    "Create explicit status and decision checkpoints",
    "Define boundaries and change process",
    "Map stakeholders and priorities",
    "Review risk signals earlier and more often",
    "Translate delivery into client-visible value"
  ]
}
~~~

## Client Communication Logic
~~~python
CLIENT_COMMUNICATION = {
  "principles": [
    "Silence creates anxiety faster than bad news",
    "Clients tolerate problems better than ambiguity",
    "Updates should answer: what happened, what matters, what is next",
    "Tone should match confidence without hiding reality",
    "Escalation is better than drift"
  ],
  "cadence_examples": {
    "high_touch_service": "Weekly updates plus milestone reviews",
    "project_based_work": "Milestone-based updates with decision checkpoints",
    "advisory_relationship": "Regular strategic reviews plus as-needed support"
  }
}
~~~

## Client Output Format

### Client Summary
- Client Type:
- Desired Outcome:
- Current Stage:
- Main Expectations:
- Scope and Boundaries:
- Communication Model:
- Risks or Friction Points:
- Recommended Improvements:
- Recommended Next Step:

## Boundaries

This skill helps design and improve client relationship systems, communication,
onboarding, and delivery structure.

It does not replace legal, financial, HR, compliance, or contract advice.
For regulated or high-stakes engagements, adapt outputs to the user's jurisdiction,
industry requirements, and formal agreements.

## Quality Check Before Delivering

- [ ] The client type and relationship context are clear
- [ ] Success is defined from the client's perspective
- [ ] Scope, timing, and communication are explicit
- [ ] Roles and ownership are clear
- [ ] Risks or friction points are identified
- [ ] Recommendations improve clarity, trust, or retention
- [ ] Output ends with a concrete next step
