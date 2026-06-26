# Stage Gates

Use this reference to diagnose where an AI-native startup is in the lifecycle and what evidence is needed to move forward.

## Stage Selection

| Signal | Likely Stage |
| --- | --- |
| The user has an idea, target customer guess, or market thesis but little direct evidence | Idea |
| The user has validated a specific problem and is deciding what to build first | MVP |
| The user has early traction and must make growth, product, security, and operations repeatable | Launch |
| The user has meaningful scale, enterprise pressure, mature GTM needs, or founder bottleneck issues | Scale |
| The user has pieces from several stages | Diagnose the riskiest missing gate first |

## Idea Stage

Goal: Validate that a real, specific, frequent problem exists for a reachable market before building.

Stage gate: Problem-solution fit.

Evidence to require:

- A named target segment with a specific pain, frequency, severity, current workaround, and budget or urgency.
- Real customer conversations or equivalent direct evidence.
- A competitive map that includes direct, indirect, adjacent, and potential incumbent solutions.
- Disconfirming evidence and reasons the idea might fail.
- A solution concept tied to the validated problem, not the founder's first assumption.

Exit only when:

- The problem is real and specific.
- The proposed solution addresses the revealed problem.
- Enough qualitative signal exists to justify an MVP, even though certainty is unavailable.

Failure modes:

- Treating a prototype as validation.
- Letting agentic coding outrun evidence.
- Asking AI to confirm the founder's belief instead of pressure-testing it.
- Building for a broad market before finding a sharp wedge.

Default next moves:

1. Sharpen the problem hypothesis.
2. Run adversarial research.
3. Draft non-leading discovery questions.
4. Interview the target segment.
5. Synthesize supporting and challenging evidence after every five interviews.
6. Build only the smallest prototype needed to test one core interaction.

## MVP Stage

Goal: Translate a validated problem into the smallest working product that produces real evidence of value, while preserving enough architecture, scope, security, and context to avoid AI-generated entropy.

Stage gate: Early product-market fit evidence.

Evidence to require:

- Retention, revenue, referral, or repeat usage from a specific user group.
- A written MVP scope that states what is deliberately out of scope.
- An architecture/context document for coding agents.
- A measurement framework defined before launch.
- A security review before real user data is exposed.
- Feedback loops that distinguish signal from founder enthusiasm.

Exit only when:

- A specific group returns, pays, refers, or otherwise demonstrates repeated value.
- Metrics hold across multiple iteration cycles.
- The product starts pulling usage instead of requiring constant founder push.

Failure modes:

- Agentic technical debt from undocumented architecture and drifting sessions.
- False product-market fit from launch spikes or friendly early users.
- Zero-friction scope creep.
- Insecure code that works but exposes users.

Default next moves:

1. Write architecture context before coding.
2. Write the MVP scope and feature amendment criteria.
3. Build with short coding-agent sessions and update context after each session.
4. Run a focused security pass before real users.
5. Define activation, Day 7, Day 30, retention, revenue, referral, and false-positive metrics.
6. Iterate toward evidence, not feature completeness.
7. If three cycles do not move PMF metrics, run a pivot diagnostic.

## Launch Stage

Goal: Turn early traction into repeatable growth and production-grade operations without letting the founder become the limiting dependency.

Stage gate: Repeatable channel-driven growth, production readiness, and founder-independent operating loops.

Evidence to require:

- Acquisition channels with known unit economics such as CAC, LTV, and payback period.
- Infrastructure, security, compliance, reliability, and test coverage that hold under production conditions.
- Processes and automation for support, triage, sprint planning, reporting, and documentation.
- A backlog of technical debt remediation sequenced against growth needs.

Exit only when:

- Growth is repeatable, not only launch-driven.
- Product and infrastructure survive real production load.
- Recurring operations run without founder memory as the trigger.

Failure modes:

- MVP technical debt becomes a structural liability.
- Founder remains in every loop.
- Security and compliance are deferred after real exposure begins.
- Expansion into new markets obscures the original PMF signal.

Default next moves:

1. Audit architecture, brittle areas, and test gaps.
2. Sequence remediation across sprints.
3. Inventory founder attention and convert repeatable work into systems.
4. Make security and compliance a product workstream.
5. Stand up a lightweight product management operating system.
6. Instrument weekly metrics and routing loops.

## Scale Stage

Goal: Build systematic growth, mature operations, enterprise trust, and defensible advantages while the founder shifts from builder/operator to executive.

Stage gate: The company can sustain growth, governance, customer trust, and moat depth without the founder running daily operations.

Evidence to require:

- Governance, compliance, finance, support, and reliability infrastructure that external reviewers can audit.
- Enterprise-grade documentation, SLAs, support playbooks, observability, and incident response.
- A real GTM function with segmentation, messaging, pipeline reporting, sales playbooks, and customer success loops.
- Captured domain expertise that improves the product over time.
- Data and workflow advantages that become harder to copy as customers use the product.

Exit condition:

- Sustainable profitability, IPO readiness, or acquisition readiness.
- Growth is systematic and auditable.
- A well-funded copycat would struggle to replicate the product's domain depth, data loops, integrations, and workflow lock-in.

Failure modes:

- Handing off too much before context is codified.
- Holding too much and becoming the constraint.
- Selling to enterprise without support, security, compliance, and reliability maturity.
- Reaching the ceiling of founder-led growth without a GTM engine.

Default next moves:

1. Build a founder bottleneck map.
2. Test what breaks if the founder is unavailable for a week.
3. Convert institutional knowledge into auditable systems.
4. Build enterprise procurement readiness artifacts.
5. Create a GTM engine, not only campaigns.
6. Turn domain edge cases into tests, prompts, validations, integrations, and support workflows.
7. Design data flywheels and workflow integration audits.
