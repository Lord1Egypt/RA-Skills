# Expert Selection Taxonomy v0.1.0-scaffold

Use this taxonomy to select expert archetypes. Do not treat it as exhaustive.

For the expanded archetype bucket model, read `archetype-buckets.md`. This file lists common professional/domain selections; `archetype-buckets.md` explains broader lenses such as stakeholder, adversary, institution, constraint, translation, field wisdom, and taste.

## Product and strategy

- Product strategist: clarifies user value, sequencing, positioning, tradeoffs.
- Market researcher: studies category, competitors, alternatives, buyer behaviour.
- Customer researcher: finds user needs, pain points, language, workflows.
- Business model analyst: revenue logic, pricing, unit economics, incentives.
- Go-to-market strategist: launch path, channels, adoption, messaging.

## Design and communication

- UX designer: flows, friction, interaction patterns, affordances.
- UI designer: visual hierarchy, layout, component clarity.
- Accessibility specialist: WCAG, assistive tech, inclusive patterns.
- Content designer: microcopy, labels, comprehension, tone.
- Technical writer: docs, onboarding, procedures, reference clarity.
- Editor: structure, coherence, audience fit, concision.

## Engineering and systems

- Software architect: boundaries, maintainability, integration, evolution.
- Backend engineer: APIs, data flow, reliability, server-side implementation.
- Frontend engineer: state, components, browser constraints, UI performance.
- Data engineer: pipelines, schemas, lineage, data quality.
- ML/AI engineer: model behaviour, evals, prompts, inference constraints.
- DevOps/SRE: deployment, observability, uptime, incident response.
- Security engineer: threat modelling, auth, secrets, abuse paths.
- QA/test lead: test strategy, edge cases, regression risk.

## Operations and support

- Operations manager: process design, handoffs, runbooks, staffing load.
- Support lead: user failure modes, triage, escalation, help content.
- Incident commander: response, prioritization, communications under pressure.
- Reliability reviewer: recovery, monitoring, backups, graceful degradation.

## Governance, risk, and compliance

- Privacy specialist: data minimization, consent, retention, privacy risk.
- Legal/compliance reviewer: rules, contracts, regulatory exposure.
- Safety engineer: hazard analysis, fail-safe behaviour, human harm prevention.
- Finance analyst: costs, forecasts, margins, financial controls.
- Procurement/vendor reviewer: third-party risk, contracts, lock-in.

## Domain and industry experts

Create these based on project context. Examples:

- Textile industry merchandiser.
- Medical workflow specialist.
- Education curriculum designer.
- Construction estimator.
- Logistics planner.
- Retail operations specialist.
- Community manager.
- Grant writer.

## Selection patterns by phase

### Discovery

Use: product strategist, customer researcher, domain expert, market researcher.

### Planning

Use: product strategist, software architect, UX designer, operations manager, risk reviewer.

### Build

Use: implementation specialist, QA lead, security reviewer, technical writer.

### Review

Use: QA lead, accessibility specialist, compliance reviewer, editor, adversarial critic.

### Launch

Use: go-to-market strategist, support lead, operations manager, analytics lead.

### Maintenance

Use: SRE/operations, support lead, product analyst, documentation specialist.

## Archetype bucket prompt

When the obvious professional roles feel too narrow, ask:

- Who builds this?
- Who uses this?
- Who maintains this?
- Who approves or blocks this?
- Who can be harmed by this?
- Who can abuse this?
- Who has seen this fail before?
- Who understands the unofficial process?
- Who translates this for non-experts?
- Who knows what “good” feels like in this field?
- What harsh constraint will stress-test the plan?
- What kind of evidence should dominate the decision?

## Anti-patterns

- Selecting 10 experts for every activation.
- Choosing many experts that all say the same thing.
- Choosing only optimistic builder roles and no reviewer roles.
- Choosing only risk reviewers and no implementation owner.
- Choosing only job titles when a stakeholder, adversary, institution, or constraint lens would be more useful.
- Loading every dossier into every reply.
- Letting expert mode become a verbose ritual instead of a practical tool.
