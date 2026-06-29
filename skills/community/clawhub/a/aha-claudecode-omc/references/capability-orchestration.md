# Capability Orchestration

## Core Positioning

This file is the source of truth for runtime-neutral capability orchestration. It defines how an AI agent detects available capability surfaces, converges them into an execution route, executes with transparency, and re-orchestrates when a capability gap appears.

This is a capability orchestration framework, not an SOP. It must not prescribe a fixed runtime implementation, concrete discovery command, tool name, private source reference, or human-facing checklist. Agents must apply the framework as a high-density decision contract across native runtime capability, enhancement layers, skills, MCP surfaces, commands, and subagent/worktree collaboration patterns.

Public distributions must not reference private documents, private project paths, or organization-only governance sources.

## Hard Constraints vs Strategy Guidance

Hard constraints use `must` and are mandatory:

- The agent must trigger secondary confirmation by orchestration features: large subagent fan-out, worktree usage, cross-domain integration, and high execution cost. Confirmation must not be bound to a tier name.
- The agent must keep the full orchestration chain transparent: initial orchestration, execution-relevant capability choices, gap-triggered re-orchestration, and Out-of-Session recommendations.
- The agent must not include credentials, tokens, cookies, browser session material, provider state, live state, account state, or equivalent secrets in Out-of-Session handoff material.
- Public repositories must not reference private documents, private project sources, or private operating knowledge.

Strategy guidance uses `should` or `may` and is adaptive:

- The agent should judge orchestration complexity from Hyper downward, then converge to the lowest sufficient route. Judgment starts from Hyper; execution does not.
- The tier table should be used as a coordinate reference, not as user-facing status text.
- The agent should transparently skip irrelevant higher-complexity routes when the task evidence makes them unnecessary.
- The agent may mix capabilities across native runtime, enhancement layer, skill, MCP, command, subagent, and worktree surfaces when mixed orchestration is lower-risk or more complete than choosing a single surface.

## Five-Step Flow

### 1. Runtime Detection

Detect the active execution context before planning capability use.

The agent should determine:

- Runtime family and invocation mode.
- Active enhancement layer, if any.
- Runtime version and enhancement version when version-sensitive behavior affects capability availability.
- Current permission envelope: read-only, workspace-write, external-write, network availability, approval policy, and destructive-action limits.
- Available collaboration surfaces: native subagent, configured subagent, skill, command, MCP, plugin, worktree, background task, validator, shell, browser, or equivalent runtime-neutral capability class.
- Explicit user invocation signals that change orchestration expectations.

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

If discovery fails, the agent must transparently tell the user that live capability discovery failed, may use built-in reference knowledge as a fallback, mark it as possibly outdated, and invite the user to provide current capability information. The fallback route must not overclaim actual availability.

Capability Discovery is complete only when the agent has enough capability records to choose a route or enough failure evidence to choose a conservative native route.

### 3. Initial Orchestration

Build an orchestration plan from the discovered capability surface and task shape.

The agent should determine:

- Goal decomposition: smallest complete units, dependency order, and validation gates.
- Capability convergence: which surfaces are sufficient, redundant, risky, unavailable, or better held in reserve.
- Orchestration granularity: single-agent, few subagents, multiple subagents, large fan-out, worktree-backed lanes, or external handoff.
- Collaboration complexity: simple serial work, planned serial work, simple parallel work, autonomous loops, persistent execution, cross-domain integration, or high-cost parallel integration.
- Confirmation triggers: whether orchestration features require secondary confirmation before execution.
- Transparency payload: what capability route will be used, what is intentionally not used, and what the user can say if they want a different capability route.

Initial orchestration must be disclosed to the user before meaningful execution when the route materially changes collaboration shape, risk, cost, or confirmation needs. The disclosure should provide capability-use guidance, but must not expose the tier name as the user-facing explanation.

**Goal and startline anchor.** At initial orchestration, the agent must state the goal, the startline (current state and known constraints), and the validation path. During re-orchestration, the agent must reference the original goal and startline to prevent drift. In Out-of-Session handoff, the goal and startline must be carried forward. Normal progress updates only need a short reference to the original goal and startline.

When the current session is not the right container for the task, the agent may recommend an Out-of-Session path instead of forcing execution into a poor context.

### 4. Execution

Execute through the selected capability route with unit-level verification.

The agent should:

- Keep one active unit at a time unless the orchestration plan explicitly uses safe parallel lanes.
- Use the lowest sufficient capability surface for each unit.
- Preserve hard safety boundaries: confirmation-gated actions, secret exclusion, permission limits, public-repo private-reference exclusion, and destructive-action constraints.
- Verify each completed unit with the most relevant diagnostics, tests, builds, validators, manual observation, or structured evidence available in the runtime.
- Keep user-facing transparency proportional: report meaningful orchestration shifts and verification evidence, not every tool call.
- Avoid re-planning churn while execution still matches the discovered capability surface and task constraints.

Execution should not treat capability activation as success. Success requires task outcome evidence, not merely tool reachability, installation success, help output, or agent opinion.

### 5. Re-Orchestration on Gap

When execution reveals a capability gap, constraint conflict, failed validation, unavailable surface, context overload, or permission mismatch, the agent must re-orchestrate instead of silently degrading.

Gap-triggered re-orchestration should answer:

- Which route failed or became insufficient.
- Which gap class appeared: missing capability, unsafe capability, failed capability, stale discovery, permission limit, context limit, validation failure, or cross-domain mismatch.
- Which route is next: converge downward to a simpler route, mix capabilities, select a different capability class, request secondary confirmation, or recommend Out-of-Session.
- How the new route will be orchestrated: serial, simple parallel, autonomous loop, worktree-backed, review-gated, or handoff-based.
- Whether capability mixing or single-route selection is safer and why.
- What the user needs to know: changed capability route, changed risk/cost, changed validation path, and any capability-use instruction.

Re-orchestration must be transparent. The agent must tell the user what changed and why, but must not announce tier names as the explanation.

## Re-Orchestration Thought Path

When a gap appears, the agent should reason through this path before acting:

1. Which route should handle the gap: current session or Out-of-Session bypass?
2. If current session is enough, how should capabilities be recombined?
3. If no single coordinate fits, should the agent mix capabilities from multiple coordinates or choose one dominant shape?
4. What must be told to the user in plain language before proceeding?

Current-session handling is appropriate when the gap is local, reversible and within the current permission boundary. Out-of-Session bypass is appropriate when clean context, different permissions or a different project boundary is necessary and explicitly allowed.

The agent should frame this as re-orchestration around observed constraints, not as a capability reduction.

## Tier Coordinate Reference

The tier table is a coordinate reference for judging orchestration granularity and collaboration complexity. It is not a user-facing label, not a fixed escalation ladder, and not a substitute for capability discovery.

| Tier | Orchestration Granularity | Collaboration Complexity | Human Confirmation |
|---|---|---|---|
| Hyper | Large subagent fan-out + worktree | Complex parallel / cross-domain integration | Secondary confirmation |
| Full | Multiple subagents | Autonomous loops / parallel / persistent | None |
| Standard | Few subagents | Planned serial / simple parallel | None |
| Base | Minimal subagents | Simplest collaboration | None |

Complexity judgment should start from Hyper and converge downward:

1. Check whether the task has Hyper features: large subagent fan-out, worktree-backed execution, cross-domain integration, and high execution cost.
2. If Hyper features are absent or unnecessary, transparently skip them and evaluate Full-level collaboration complexity.
3. If autonomous loops, parallel lanes, or persistence are unnecessary, converge to Standard.
4. If planned serial work or simple parallelism is unnecessary, converge to Base.
5. Execute the lowest sufficient route, not the highest judged route.

Secondary confirmation is triggered by orchestration features, not by a tier name. A route that combines large subagent fan-out, worktree usage, cross-domain integration, and high cost must request secondary confirmation even if an implementation does not call it Hyper. A route without those features must not require confirmation merely because a tier table exists.

## Orchestration Transparency Rules

The agent must keep orchestration transparent across initial orchestration and re-orchestration.

Transparency must include:

- Capability route: which capability classes will be used.
- Non-use rationale: which tempting capability classes are skipped and why.
- User guidance: what the user can request if they want more parallelism, less autonomy, a different runtime container, or stricter verification.
- Risk and confirmation: what requires secondary confirmation and which orchestration features triggered it.
- Validation path: how execution success will be verified.
- Compact wording: disclosures must be short; do not narrate internal reasoning; do not expose tier names by default.

Transparency must not include tier names as the primary user-facing explanation. Say what will happen, not the tier label.

## Out-of-Session Bypass

Out-of-Session is a bypass recommendation for cases where the current session is a poor execution container. It is a context and boundary control measure, not a runtime-switch prescription.

The agent should recommend Out-of-Session when one or more conditions apply:

- Clean context is materially better than continuing with polluted or overloaded context.
- Different permission scope is needed and should not be requested inside the current session.
- Different project boundary is required.
- The task needs a handoff artifact before another execution container continues.

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
| capability orchestration | Runtime-neutral process for detecting, selecting, combining, executing, and reselecting available AI-agent capability surfaces for a task. |
| capability convergence | Decision process that reduces the discovered capability surface to the lowest sufficient route for the current task and validation needs. |
| gap-triggered re-orchestration | Replanning event caused by a capability, permission, context, safety, or validation gap discovered during execution. |
| orchestration transparency | Requirement that users are told the capability route, material changes, confirmation triggers, and validation path without exposing tier labels as the explanation. |
| orchestration granularity | Scale of execution decomposition and capability fan-out, from minimal single-route work to large subagent and worktree-backed lanes. |
| collaboration complexity | Degree of coordination required across serial work, parallel lanes, autonomous loops, persistence, review gates, cross-domain integration, and handoff. |
| Hyper | Coordinate reference for large subagent plus worktree orchestration under complex parallel or cross-domain integration; feature-triggered secondary confirmation applies. |
| Full | Coordinate reference for multiple-subagent orchestration with autonomous loop, parallel, or persistent collaboration, without feature-triggered secondary confirmation by default. |
| Standard | Coordinate reference for a small number of subagents with planned serial or simple parallel collaboration. |
| Base | Coordinate reference for the minimum subagent footprint and simplest collaboration route. |
| Out-of-Session | Bypass recommendation to move continuation to a cleaner or more appropriate session container with a safe handoff artifact. |
