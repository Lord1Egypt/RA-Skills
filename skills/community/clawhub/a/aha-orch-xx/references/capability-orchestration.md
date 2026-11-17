# Capability Orchestration

## Core Positioning

This agent-facing file is the source of truth for runtime-neutral capability orchestration. It defines how an AI agent detects available capability surfaces, converges them into a capability route across the agent task lifecycle, uses capabilities with transparency, and re-orchestrates when a capability gap appears.

This is a capability orchestration framework for the consuming AI agent, not an operator guide or SOP. It must not prescribe a fixed runtime implementation, concrete discovery command, tool name, private source reference, or operator procedure. The consuming agent must apply the framework as a high-density decision contract across native runtime capability, enhancement layers, skills, MCP surfaces, commands, and subagent/worktree collaboration patterns.

Public distributions must not reference private documents, private project paths, or organization-only governance sources.

## Hard Constraints vs Strategy Guidance

Hard constraints use `must` and are mandatory:

- The agent must trigger secondary confirmation by orchestration features: large subagent fan-out, worktree usage, cross-domain integration, and high work cost. Confirmation must not be bound to a tier name.
- The agent must keep the full orchestration chain transparent: initial orchestration, lifecycle-relevant capability choices, gap-triggered re-orchestration, and Out-of-Session recommendations.
- The agent must not include credentials, tokens, cookies, browser session material, provider state, live state, account state, or equivalent secrets in Out-of-Session handoff material.
- The main session must not override explicit instructions, project rules, permission gates, confirmation gates, or product/business ownership. Subagent output is advisory evidence, not authority.
- Autonomous loops, persistent work, large fan-out, worktrees, cross-domain integration, or high-cost parallelism must require explicit secondary confirmation and a stated rollback path.
- Public repositories must not reference private documents, private project sources, or private operating knowledge.

Strategy guidance uses `should` or `may` and is adaptive:

- The agent should judge orchestration complexity from Hyper downward, then converge to the lowest sufficient route. Judgment starts from Hyper; capability use does not.
- The tier table should be used as a coordinate reference, not as agent-visible mode label.
- The agent should transparently skip irrelevant higher-complexity routes when the task evidence makes them unnecessary.
- The agent may mix capabilities across native runtime, enhancement layer, skill, MCP, command, subagent, and worktree surfaces when mixed orchestration is lower-risk or more complete than choosing a single surface.
- For non-trivial work, the current primary session should act as the orchestrator, not as the default do-everything executor. It should own goal framing, boundary checks, task decomposition, capability routing, integration, verification, and final task synthesis.
- For non-trivial work, the agent must perform a delegation-first scan before equivalent inline work: identify bounded task-lifecycle units that could be delegated to available subagents, enhancement-layer lanes, review lanes, QA lanes, background lanes, or worktrees. Delegation execution remains gated: delegate only when the unit is bounded, independently verifiable, lower-risk or higher-evidence than inline work, and does not cross a confirmation gate. Native direct work remains valid for urgent blockers, tiny tasks, tightly coupled integration, secret/session boundaries, write-conflict risk, unavailable lanes, or cases where coordination cost would exceed outcome-evidence gain.
- Before full discovery, the agent should apply a native fast path: if the request is simple, local, low-risk, and has an obvious direct route, skip orchestration discovery and complete it with native tools.

## Agent Task Lifecycle as the Orchestration Target

Capability orchestration applies to the whole AI agent task lifecycle, not only to the moment of carrying out an already-made plan. The lifecycle includes intake, goal framing, project-rule loading, runtime detection, capability discovery, planning, implementation, verification, review, re-orchestration, handoff, and rollback.

For each non-trivial task-lifecycle phase, the agent should judge whether native runtime capability, enhancement layers, skills, MCPs, commands, validators, or subagents materially improve route choice, risk control, implementation quality, review quality, or validation confidence. Planning is one phase in that lifecycle, but it is not a special pre-plan ritual and not the only phase where capability support matters.

Use task-lifecycle support capabilities when requirements, code context, external facts, route choice, implementation risk, review needs, or validation path are uncertain enough that a direct single-surface route would be brittle. Stay native and direct when the task is obvious, local, low-risk, and has a clear route.

This requires a delegation-first scan for non-trivial tasks, not mandatory fan-out. It must not require subagents, full capability discovery, candidate-lane artifacts, or operator ceremony for simple tasks. If no unit is delegated after the scan, the agent should keep the reason concrete: trivial task, urgent blocker, tight coupling, secret/session boundary, write-conflict risk, unavailable lane, or coordination cost greater than evidence gain. The selected task-lifecycle route should remain the lowest sufficient route and should be disclosed only when it affects cost, latency, permission, collaboration shape, or operator choice.

## Five-Step Flow

### 1. Runtime Detection

Detect the active agent runtime context before selecting lifecycle capability use.

The agent should determine:

- Runtime family and invocation mode.
- Active enhancement layer, if any.
- Runtime version and enhancement version when version-sensitive behavior affects capability availability.
- Current permission envelope: read-only, workspace-write, external-write, network availability, approval policy, and destructive-action limits.
- Available collaboration surfaces: native subagent, configured subagent, skill, command, MCP, plugin, worktree, background task, validator, shell, browser, or equivalent runtime-neutral capability class.
- Explicit invocation signals that change orchestration expectations.

Runtime Detection must stay runtime-neutral in this source file. Implementations may define concrete commands elsewhere, but this framework only requires capability-class detection and evidence-aware version handling.

**Multi-level capability detection**: Enhancement layers often expose multiple capability surfaces (binary installed, CLI commands, interactive bridges, feature-specific surfaces). The agent must detect at multiple levels and must not collapse a partial failure into a full fallback. If the binary is installed but a specific surface is unavailable, only skip that surface and continue using available surfaces. Do not equate "one surface unavailable" with "enhancement layer unavailable."

If detection fails at the binary level (enhancement layer not installed), the agent should proceed with the safest native capability assumption, state the uncertainty, and avoid claiming unavailable surfaces. If detection fails at a specific surface level only, the agent should use the enhancement layer's other available surfaces and state which surface was skipped.

**Enhancement layer is optional.** The native route remains valid when it is sufficient or when the enhancement layer is absent. Multi-level detection (binary, CLI, interactive bridge, feature-specific surface) determines which specific surfaces are available. The agent must skip only unavailable surfaces and must not abandon all enhancement surfaces on a partial failure.

### 2. Capability Discovery

Pull the full capability surface for the current runtime context on every orchestration pass. Discovery must include native capability plus any active enhancement layer, skill, MCP, command, validator, and collaboration surfaces available to the session.

Each discovered capability record should include seven fields:

| Field | Meaning |
|---|---|
| Type | Capability class such as native, enhancement layer, skill, MCP, command, validator, subagent, worktree, browser, or other runtime-neutral surface. |
| Name | Stable capability name as exposed by the runtime or enhancement surface. |
| Category | Primary use class: planning, exploration, implementation, review, verification, browser, external API, context, handoff, rollback, or equivalent. |
| Status | Available, unavailable, configured, detected, uncertain, failed, disabled, or requires confirmation. |
| Description | Short operational description of what the capability can do. |
| Trigger Conditions | When the agent should consider using it and when it should avoid it. |
| Risk Level | Low, medium, or high, based on permission surface, external side effects, credential/provider/browser/live exposure, state mutation, cost, and reversibility. |

The agent should run discovery every time because capability surfaces can change across sessions, projects, runtime versions, permission modes, and enhancement activation states.

If discovery fails, the agent must transparently disclose that live capability discovery failed, may use built-in reference knowledge as a fallback, mark it as possibly outdated, and request current capability information only when needed. The fallback route must not overclaim actual availability.

Capability Discovery is complete only when the agent has enough capability records to choose a route or enough failure evidence to choose a conservative native route.

Before full discovery, apply the native fast path. If the task is trivial, local, low-risk, and has an obvious direct route, complete it natively and do not pay a discovery or delegation tax. Full discovery is required when capability choice materially affects outcome, risk, cost, context size, or verification confidence.

### 3. Initial Orchestration

Build an orchestration plan from the discovered capability surface and task shape.

The agent should determine:

- Goal decomposition: smallest complete units, dependency order, and validation gates.
- Capability convergence: which surfaces are sufficient, redundant, risky, unavailable, or better held in reserve.
- Orchestration granularity: single-agent, few subagents, multiple subagents, large fan-out, worktree-backed lanes, or external handoff.
- Collaboration complexity: simple serial work, planned serial work, simple parallel work, autonomous loops, persistent work, cross-domain integration, or high-cost parallel integration.
- Confirmation triggers: whether orchestration features require secondary confirmation before any task-lifecycle phase changes permission, cost, state, or collaboration shape.
- Transparency payload: what capability route will be used, what is intentionally not used, and what follow-up instruction can request if they want a different capability route.

Initial orchestration must be disclosed before meaningful task-lifecycle work when the route materially changes collaboration shape, risk, cost, or confirmation needs. The disclosure should provide capability-use guidance, but must not expose the tier name as the operator-facing explanation.

**Goal and startline anchor.** At initial orchestration, the agent must state the goal, the startline (current state and known constraints), and the validation path. During re-orchestration, the agent must reference the original goal and startline to prevent drift. In Out-of-Session handoff, the goal and startline must be carried forward. Normal progress updates only need a short reference to the original goal and startline.

When the current session is not the right container for the task, the agent may recommend an Out-of-Session path instead of forcing the current route into a poor context.

### Main-Session Orchestrator Default

For non-trivial work, the current primary session should behave as the orchestrator and final integrator:

- Keep the goal, startline, constraints, confirmation gates, and acceptance criteria in the primary session.
- Split work into bounded units with disjoint ownership where possible.
- Perform a delegation-first scan for concrete exploration, implementation, review, and verification units before doing equivalent inline work.
- Continue useful non-overlapping work locally while delegated lanes run; do not block on a delegate unless its output is on the immediate critical path.
- Integrate delegate results before claiming success; a delegate response is evidence input, not the final outcome.

Delegation is inappropriate when the task is trivial, the next action is an urgent blocker, the work requires private/session material that must not be shared, the write set cannot be bounded, or the added coordination cost would exceed the likely outcome gain.

Delegation scanning is mandatory for non-trivial work; delegation execution is shape-gated. Use subagents or enhancement lanes when a unit is non-trivial, independently bounded, and reduces context load, risk, latency, or verification cost. If the agent chooses not to delegate, the reason must be concrete rather than implicit. For trivial Q&A, known-location edits, and single-file low-risk changes, work natively without delegation.

### v1.1 Delegation Contract

The primary session is the **decision maker and integrator**, not the default reader, searcher, or writer. It retains goal framing, project and permission checks, decomposition, delegation decisions, integration, acceptance decisions, and final verification. For non-trivial work, prefer a bounded available subagent or capability lane for a separable unit when it improves context economy, independence, latency, or evidence; this is a default preference, not compulsory fan-out.

| Unit | Default delegation route | Required return / boundary |
|---|---|---|
| Repository search, file location, local relationship mapping | Available exploration/discovery agent or read-only tool lane | Paths, facts, and uncertainty; no writes. |
| Focused file reading or context extraction | Available read-only exploration agent | Relevant excerpts/relations and no inferred success claim. |
| External or version-sensitive research | Available research/documentation agent | Sources, version limits, and applicability. |
| Diagnosis, tests, review, or regression evidence | Available debugging, test, verification, or review agent | Command/result, findings, and uncovered risks. |
| Bounded implementation or documentation write | One explicitly assigned implementation/writer agent | Exact `write_set`, expected diff, validation command, and changed-file report. |

Use the closest currently available capability, not a promised agent name. A runtime adapter may provide a role mapping, but it must detect role availability and resolve model selection from the active runtime; this public contract never hardcodes a model identifier.

**Single-writer rule.** Every write unit must name a bounded, mutually exclusive `write_set`. Only its assigned writer may change that set while the unit is active. Parallel writers are allowed only for disjoint sets with separately declared validation. Shared files, conflict resolution, permission-gated writes, and final integration return to the primary session serially. A delegate must not expand its write set or perform external, credential, provider, browser/session, live, destructive, or otherwise confirmation-gated work; it reports the needed handoff instead.

**Fixed direct-work exceptions.** The primary session may keep a unit inline when it is tiny and at a known location, unblocks an urgent failure, is tightly coupled to current integration, contains secret/session material, has an unbounded or conflicting write set, lacks an available safe lane, or would cost more to coordinate than the evidence it can add. State the applicable exception when non-delegation materially changes collaboration shape or evidence.

**Tool-composition boundary.** Programmatic orchestration may aggregate predictable, read-only, independently interpretable tool calls. It must not substitute for authorization, confirmation-gated or write actions, semantic judgment, conflict resolution, or final acceptance. Tool reachability and delegate summaries remain evidence inputs, never outcome proof.

### Orchestration vs Capability-Use Role Separation

The orchestration decision role and the capability-use role are distinct and must not be fused. Separating them prevents silent re-planning and conflation of capability activation with outcome success, and keeps the capability route accountable to a disclosed plan.

The orchestration decision role owns capability route selection, goal decomposition, granularity judgment, confirmation-trigger judgment, and gap-triggered re-orchestration. Its output is a disclosed capability route plus a validation path, not a tool call.

The capability-use role owns carrying out the selected route unit by unit, preserving hard safety boundaries, and producing verification evidence per unit. Its output is task outcome evidence, not a re-plan.

Role separation rules:

- The agent must not silently switch from the capability-use role back to the orchestration decision role without a disclosed gap trigger. Re-orchestration is an orchestration decision role act and must be announced before it changes the route.
- The agent must not treat a capability-use role success (a tool ran, a file was written, a surface replied) as an orchestration decision role success (the task outcome is met). Capability activation is not outcome evidence.
- While acting in the capability-use role, the agent should follow the route chosen in the orchestration decision role and avoid mid-unit re-planning unless a gap appears.
- While acting in the orchestration decision role, the agent should disclose the route and validation path before handing control to the capability-use role.
- A single agent may hold both roles across time, but at any given decision point it must be clear which role is acting, and any role switch must be transparent.

### 4. Capability Use

Carry out the selected capability route with unit-level verification.

The agent should:

- Keep one active unit at a time unless the orchestration plan explicitly uses safe parallel lanes.
- Use the lowest sufficient capability surface for each unit.
- Run the delegation-first scan before equivalent inline work on non-trivial bounded task-lifecycle units. Delegate when the unit is bounded, parallelizable or independently reviewable, and supported by an available native or enhancement-layer subagent; keep orchestration, integration, and final claims in the primary session. If no delegation is used, record or state the concrete non-delegation reason when it affects collaboration shape or outcome evidence.
- Preserve hard safety boundaries: confirmation-gated actions, secret exclusion, permission limits, public-repo private-reference exclusion, and destructive-action constraints.
- Verify each completed unit with the most relevant diagnostics, tests, builds, validators, direct observation, or structured evidence available in the runtime.
- Keep operator-visible transparency proportional: report meaningful orchestration shifts and verification evidence, not every tool call.
- Avoid re-planning churn while the selected capability route still matches the discovered capability surface and task constraints.

Capability use should not treat activation as success. Success requires task outcome evidence, not merely tool reachability, installation success, help output, or agent opinion.

Capability detection proves availability only. It never proves task success. Every delegated unit should return task-specific evidence such as changed files, tests, diagnostics, review findings, or an explicit no-change rationale tied to the original acceptance criteria.

### 5. Re-Orchestration on Gap

When any task-lifecycle phase reveals a capability gap, constraint conflict, failed validation, unavailable surface, context overload, or permission mismatch, the agent must re-orchestrate instead of silently degrading.

Gap-triggered re-orchestration should answer:

- Which route failed or became insufficient.
- Which gap class appeared: missing capability, unsafe capability, failed capability, stale discovery, permission limit, context limit, validation failure, or cross-domain mismatch.
- Which route is next: converge downward to a simpler route, mix capabilities, select a different capability class, request secondary confirmation, or recommend Out-of-Session.
- How the new route will be orchestrated: serial, simple parallel, autonomous loop, worktree-backed, review-gated, or handoff-based.
- Whether capability mixing or single-route selection is safer and why.
- Disclosure payload: changed capability route, changed risk/cost, changed validation path, and any capability-use instruction.

Re-orchestration must be transparent. The agent must disclose what changed and why, but must not announce tier names as the explanation.

## Re-Orchestration Thought Path

When a gap appears, the agent should reason through this path before acting:

1. Which route should handle the gap: current session or Out-of-Session bypass?
2. If current session is enough, how should capabilities be recombined?
3. If no single coordinate fits, should the agent mix capabilities from multiple coordinates or choose one dominant shape?
4. What must be disclosed in plain language before proceeding?

Current-session handling is appropriate when the gap is local, reversible and within the current permission boundary. Out-of-Session bypass is appropriate when clean context, different permissions or a different project boundary is necessary and explicitly allowed.

The agent should frame this as re-orchestration around observed constraints, not as a capability reduction.

## Tier Coordinate Reference

The tier table is a coordinate reference for judging orchestration granularity and collaboration complexity. It is not a surfaced label, not a fixed escalation ladder, and not a substitute for capability discovery.

| Tier | Orchestration Granularity | Collaboration Complexity | Operator Confirmation |
|---|---|---|---|
| Hyper | Main-session orchestration across large subagent fan-out, worktrees, isolated lanes, or external handoff | Complex parallel / cross-domain integration | Secondary confirmation |
| Full | Main-session orchestration with multiple subagents, review or QA lanes, and bounded loops | Parallel / persistent / review-gated | Feature-triggered secondary confirmation |
| Standard | Main-session orchestration with a few focused subagents or simple parallel lanes | Planned serial / simple parallel | None |
| Base | Direct native work or minimal subagent use | Simplest collaboration | None |

Complexity judgment should start from Hyper and converge downward:

1. Check whether the task has Hyper features: large subagent fan-out, worktree-backed lanes, cross-domain integration, and high work cost.
2. If Hyper features are absent or unnecessary, keep the primary session as orchestrator and evaluate whether Full-level multiple-subagent, review, QA, or autonomous-loop collaboration is useful.
3. If autonomous loops, multiple lanes, or persistence are unnecessary, converge to Standard and use only focused subagents that materially improve exploration, implementation, review, or verification.
4. If planned serial work or simple parallelism is unnecessary, converge to Base and work directly or with minimal support.
5. Use the lowest sufficient route, not the highest judged route; do not convert "hyper/ultra" into gratuitous fan-out.

Secondary confirmation is triggered by orchestration features, not by a tier name. A route that combines large subagent fan-out, worktree usage, cross-domain integration, and high cost must request secondary confirmation even if an implementation does not call it Hyper. A route without those features must not require confirmation merely because a tier table exists.

Hyper/Ultra-style modes are exceptional escalation paths, not maturity levels. They are appropriate only when the task shape needs their coordination power and when the primary session can still integrate and verify the result.

## Orchestration Transparency Rules

The agent must keep orchestration transparent across initial orchestration and re-orchestration.

Transparency must include:

- Capability route: which capability classes will be used.
- Non-use rationale: which tempting capability classes are skipped and why.
- Follow-up guidance: what follow-up instruction can request if they want more parallelism, less autonomy, a different runtime container, or stricter verification.
- Risk and confirmation: what requires secondary confirmation and which orchestration features triggered it.
- Validation path: how task outcome success will be verified.

**verbosity:low** governs how every transparency statement is worded. Concrete constraints:

- Disclosures must be at most three sentences per orchestration event.
- Progress updates must be at most one line per task-lifecycle unit.
- No internal reasoning narration: state the chosen route and the evidence, not the deliberation that produced it.
- No tier name exposure: tier names must not appear in operator-facing text as the explanation.
- Compact wording: keep every transparency statement short; prefer one concrete sentence over a paragraph, and never expand a disclosure into a reasoning trace.

Transparency must not include tier names as the primary operator-facing explanation. Say what will happen, not the tier label.

## Out-of-Session Bypass

Out-of-Session is a bypass recommendation for cases where the current session is a poor task container. It is a context and boundary control measure, not a runtime-switch prescription.

The agent should recommend Out-of-Session when one or more conditions apply:

- Clean context is materially better than continuing with polluted or overloaded context.
- Different permission scope is needed and should not be requested inside the current session.
- Different project boundary is required.
- The task needs a handoff artifact before another task container continues.

Reference examples include clean context, different permissions, and different project. Do not use runtime replacement as the defining example in this framework.

When recommending Out-of-Session, the agent should create or request permission to create a handoff file with six fields:

| Field | Required Content |
|---|---|
| Reason | Why the current session is not the right container. |
| Complete Prompt | A complete prompt that can be pasted into the next session. |
| Task Background | Goal, constraints, acceptance criteria, and known risks. |
| Suggested Runtime / Enhancement Layer | Runtime-neutral recommendation based on capability needs, without claiming availability. |
| Related File Paths | Relevant repo-relative or local paths needed for continuation. |
| Context Summary | Minimal state summary, completed work, verification evidence, and remaining decisions. |

Handoff file location priority:

1. Workspace temporary directory.
2. `~/tmp/`.
3. `/tmp/`.

Security rule: Out-of-Session material must not include credentials, tokens, cookies, browser session material, provider state, live state, account state, private auth paths, or secret-derived receipts.

Permission rule: in a read-only environment, the agent must request write permission for the handoff file. If permission is denied or unavailable, the agent must output the handoff content inline instead of attempting unauthorized writes.

## Terminology

| Term | Definition |
|---|---|
| capability orchestration | Runtime-neutral process for detecting, selecting, combining, using, and reselecting available AI-agent capability surfaces across the agent task lifecycle. |
| capability convergence | Decision process that reduces the discovered capability surface to the lowest sufficient route for the current task and validation needs. |
| gap-triggered re-orchestration | Route revision event caused by a capability, permission, context, safety, or validation gap discovered during any task-lifecycle phase. |
| orchestration transparency | Requirement that the agent disclose the capability route, material changes, confirmation triggers, and validation path without exposing tier labels as the explanation. |
| orchestration granularity | Scale of lifecycle decomposition and capability fan-out, from minimal single-route work to large subagent and worktree-backed lanes. |
| collaboration complexity | Degree of coordination required across serial work, parallel lanes, autonomous loops, persistence, review gates, cross-domain integration, and handoff. |
| Hyper | Coordinate reference for large subagent plus worktree orchestration under complex parallel or cross-domain integration; feature-triggered secondary confirmation applies. |
| Full | Coordinate reference for main-session orchestration with multiple subagents, review or QA lanes, and bounded loops. Autonomous loops, persistent work, high-cost parallelism, or other confirmation-triggering features still require secondary confirmation. |
| Standard | Coordinate reference for a small number of subagents with planned serial or simple parallel collaboration. |
| Base | Coordinate reference for the minimum subagent footprint and simplest collaboration route. |
| Out-of-Session | Bypass recommendation to move continuation to a cleaner or more appropriate session container with a safe handoff artifact. |
