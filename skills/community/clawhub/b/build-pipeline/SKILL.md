---
name: build-pipeline
description: Orchestrate agent build workflow. you handle parse and research, then delegates the full build to Builder. Use for new builds and error handling.
---

# Build Pipeline Skill

Your build orchestration workflow: parse → spawn research workers + Builder in parallel → wait for research → feed research to Builder → wait for result → report.

---

## Pipeline Overview

1. **Create Build** — Initialize build record (`shared/builds/{build-id}/build.yaml`)
2. **Parse** — Extract domain, classify complexity, apply smart defaults, write parse-report.yaml
3. **Parallel Spawn** — Spawn all research workers AND Builder simultaneously
4. **Wait for Research** — Poll until all expected research partials exist in `research-partials/`
5. **Feed Research to Builder** — Send Builder phase 2 task with research findings via `sessions_send`
6. **Wait for Builder** — Poll for `shared/builds/{build-id}/builder-result.yaml`
7. **Report** — Read builder-result.yaml and report success or failure to the user

---

## User-Facing Progress Contract (Required)

You must communicate pipeline progress with structured stepper events, not technical narration.

### Event rules

1. At start: emit `status.changed` = `running`.
2. For each pipeline step, emit `progress.step.started`.
3. When moving to the next step, emit `progress.step.completed` for the previous step first.
4. Then emit `progress.step.started` for the next step.
5. Do not emit `phase.changed` for new builds.
6. Do not send repetitive assistant text on each transition; rely on stepper events.

### Step IDs + friendly copy

| Pipeline step | step_id | title | description |
|---|---|---|---|
| Create Build Record | `build_record` | `Starting your build` | `I'm setting up your build session.` |
| Parse | `parse` | `Understanding your request` | `I'm reading your request and mapping the plan.` |
| Research | `research` | `Gathering what we need` | `I'm collecting the tools and references for your build.` |
| Building | `building` | `Building your agent` | `I'm designing, assembling, and testing your agent now.` |
| Final report | `finalize` | `Finalizing` | `I'm wrapping up and preparing your result.` |

### Prohibited user-facing language

Do not output internal-engineering narration such as:

- "Now I'll spawn all research workers."
- "Spawning the Builder agent now."
- "Waiting for Builder to complete."

Always translate internal work into friendly progress copy from the table above.

---

## Spawning Rules

1. **Research workers MUST read their SKILL.md** — Don't summarize instructions in the task. Tell them to read the file.
2. **Research workers use `agentId: null`** — they have no workspace, just task prompts.
3. **Builder uses `agentId: "builder"`** — it has a workspace at `workspace_builder/`.
4. **Never pass `streamTo="parent"`** for any subagent.
5. **Parallel spawn:** Research workers and Builder are spawned in the same function call block; do not wait between spawns.
6. **Use stronger models for complex workers** — gpt-4o for api-scout, tools-catalog, skills-finder. Haiku for domain-researcher.
7. **Add readable labels** — Format: `{worker-type}-{build-id}` (e.g., `api-scout-8bc5666a`).

### Critical Sub-Agent Pattern

Sub-agents must:
1. Read their SKILL.md file first
2. Follow ALL instructions in the file
3. Write output to YAML file (not chat back)
4. Exit silently after writing

If a sub-agent reports findings in chat instead of writing the file, **it failed**.

### Task Prompt Template

```
## FIRST: Read Your Instructions

Before doing anything, read your SKILL.md file:
~/.openclaw-factory/workspace/skills/research-workers/{worker_name}/SKILL.md

Follow ALL instructions in that file exactly. Pay special attention to:
- The "CRITICAL: Your Output is the FILE" section
- Minimum output requirements (you MUST meet these)
- Writing the YAML file at the end (MANDATORY)

## Build Context

- domain: {domain}
- archetypes: {archetypes}
- build_id: {build_id}
- output_path: ~/.openclaw-factory/shared/builds/{build_id}/research-partials/{output_file}

## Execute

Read SKILL.md → Research → Write YAML file → Exit silently.
```

---

## Step 1: Create Build Record

Write to: `shared/builds/{build-id}/build.yaml`

Set `status: "initiated"`.

### Build Record Schema

```yaml
build:
  id: "{build-id}" # UUID
  status: "initiated"  # or: parsed, researching, building, complete, failed
  user_prompt: "build me a flight booking agent"
  current_phase: null
  domain: "flight booking"        # filled after parse
  complexity: "medium"            # simple|medium|complex|system
  started_at: "2026-03-09T14:30:00Z"
  completed_at: null
  phase_history: []
  error: null                      # or {phase: "...", message: "...", retries: 0}
  builder_session_key: null        # filled after Builder spawn
```

---

## Step 2: Parse

Analyze user prompt. Write parse report to: `shared/builds/{build-id}/parse-report.yaml`

If `confidence < 0.20`, ask user for clarity. Do not proceed. Confidence >= 0.7 to proceed normally.

### Channel Connection Policy (v1)

- Default all builds to `channel_type: local`.
- Do **not** ask users which channel to connect during parse.
- Only capture channel intent if the prompt explicitly requests it (e.g. Telegram/WhatsApp/Discord).

### Parse Report Schema

```yaml
parse_report:
  id: [uuid or timestamp]
  timestamp: [ISO 8601]
  raw_prompt: [exact user input, verbatim]

  classification:
    domain: [primary domain]
    sub_domains: [list]
    archetypes: [primary, secondary, ...]
    complexity_tier: [simple | medium | complex | system]
    clarity: [high | medium | low]

  inferred:
    end_user_type: [consumer | business | internal | self]
    interaction_mode: [chat | command | scheduled | event-driven]
    persistence: [one-shot | session | always-on]
    approval_needed: [true | false]
    memory_needed: [true | false]
    channel_type: local
    channel_intent: [none | telegram | whatsapp | discord | signal | other]

  architecture_recommendation:
    pattern: [single-agent | spawn-workers | agent-teams | lobster-workflow]
    estimated_skills: [count or "TBD"]

  research_targets:
    - query: "How do real [domain] agents work?"
      priority: critical
    - query: "What APIs exist for [domain]?"
      priority: critical
    - query: "What OpenClaw skills cover [domain]?"
      priority: high

  friction:
    must_ask: []
    smart_defaults: []

  confidence: [0.0 - 1.0]
```

---

## Step 3: Parallel Spawn (Research Workers + Builder)

After successful parse, spawn all research workers **and** Builder simultaneously in a single spawn block.

### 3a. Create Research Partials Directory

```bash
mkdir -p ~/.openclaw-factory/shared/builds/{build-id}/research-partials/
```

### 3b. Spawn All Research Workers + Builder

Use a single `sessions_spawn` block with multiple calls. Do not wait between spawns.

**Research Worker Registry (Updated):**

| Worker | SKILL.md path | Writes | Always? | Model |
|--------|---------------|--------|---------|-------|
| Domain Researcher | `skills/research-workers/domain-researcher/SKILL.md` | `domain_model.yaml` | Yes | `anthropic/claude-haiku-4-5` |
| API Scout | `skills/research-workers/api-scout/SKILL.md` | `api_research.yaml` | Yes | `openai/gpt-5.2` |
| Tools Catalog | `skills/research-workers/tools-catalog-worker/SKILL.md` | `tools_catalog.yaml` | Yes | `openai/gpt-4o` |
| Skills Finder | `skills/research-workers/skills-finder-worker/SKILL.md` | `skills_research.yaml` | Yes | `anthropic/claude-haiku-4-5` |
| Regulation Scanner | `skills/research-workers/regulation-scanner/SKILL.md` | `regulation_research.yaml` | If needed | `anthropic/claude-sonnet-4-6` |
| Edge Case Scanner | `skills/research-workers/edge-case-scanner/SKILL.md` | `edge_case_research.yaml` | If needed | `anthropic/claude-sonnet-4-6` |

**Note:** Use `gpt-4o` (not mini) for complex evaluation tasks (api-scout, tools-catalog, skills-finder).

**Spawn pattern — tell workers to read their SKILL.md:**

```yaml
sessions_spawn:
  runtime: subagent
  mode: run
  label: "domain-researcher-{build_id}"
  model: anthropic/claude-haiku-4-5
  runTimeoutSeconds: 300
  task: |
    ## FIRST: Read Your Instructions
    
    Before doing anything, read your SKILL.md file:
    ~/.openclaw-factory/workspace/skills/research-workers/domain-researcher/SKILL.md
    
    Follow ALL instructions in that file exactly. Pay special attention to:
    - The "CRITICAL: Your Output is the FILE" section
    - Minimum output requirements
    - Writing the YAML file at the end (MANDATORY)
    
    ## Build Context
    
    - domain: {domain}
    - archetypes: {archetypes}
    - build_id: {build_id}
    - output_path: ~/.openclaw-factory/shared/builds/{build_id}/research-partials/domain_model.yaml
    
    ## Execute
    
    Read SKILL.md → Research → Write YAML file → Exit silently.

# Repeat for each worker with appropriate SKILL.md path and output file
```

**Spawn Builder in the same block:**

```yaml
sessions_spawn (Builder):
  agentId: "builder"
  runTimeoutSeconds: 700
  model: [no override; use system default]
  task: |
    Build ID: {build-id}
    Shared builds path: ~/.openclaw-factory/shared/builds/
    
    Phase 1: Initialize Isolated Profile
    ────────────────────────────────────
    Task: Initialize a new isolated profile at ~/.openclaw-factory/workspace_builder/{build-id}/
    
    Steps:
    1. Create the profile directory structure
    2. Set up minimal metadata and configuration placeholders
    3. Ensure the profile is ready for agent design/build in phase 2
    
    Output: When profile initialization is complete, write the marker:
    PROFILE_INITIALIZED
    
    Then wait for Phase 2 instructions. Do NOT start building yet.
```

**Rules:**
- All research workers spawn simultaneously
- Builder spawns in the same block as workers
- Do not wait for workers or Builder init to complete before proceeding to Step 4
- Store Builder's `sessionKey` for later use in Step 5

---

## Step 4: Wait for Research Workers to Complete

Poll the `research-partials/` directory until all expected partial files exist.

**Expected files:**
- `domain_model.yaml` ✓
- `api_research.yaml` ✓
- `skill_research.yaml` ✓
- `regulation_research.yaml` (if spawned) ✓
- `edge_case_research.yaml` (if spawned) ✓

**Poll behavior:**
- Check every 5 seconds
- Timeout per worker: 300 seconds
- If a worker times out: continue with partial research; Builder will design with what exists
- User message if timeout: "I'll proceed with the research we have so far."

---

## Step 5: Feed Research to Builder (Phase 2 Task)

Once all expected research partials exist, send Phase 2 task to Builder via `sessions_send`:

```yaml
sessions_send:
  sessionKey: {builder_session_key}
  message: |
    Phase 2: Design & Build Agent
    ─────────────────────────────
    
    Research is complete. Here's what we found:
    
    **Domain:** {domain}
    **Complexity:** {complexity}
    **Interaction Mode:** {interaction_mode}
    
    **Research Summary:**
    
    Domain Model:
    {domain_model.yaml excerpt or summary}
    
    Available APIs:
    {api_research.yaml excerpt or summary}
    
    Applicable OpenClaw Skills:
    {skill_research.yaml excerpt or summary}
    
    {if regulation_research.yaml exists:}
    Regulatory Considerations:
    {regulation_research.yaml excerpt or summary}
    
    {if edge_case_research.yaml exists:}
    Edge Cases & Gotchas:
    {edge_case_research.yaml excerpt or summary}
    
    **Your Task:**
    Design and build the agent using this research. Follow your standard assembly pipeline:
    1. Apply architecture recommendations from research
    2. Design the agent (prompts, tools, skills)
    3. Assemble the agent with selected skills
    4. Set up the isolated profile
    5. Validate and test
    6. Write builder-result.yaml with final status, agent name, profile path, and any notes
    
    When complete, write: BUILDER_COMPLETE
```

---

## Step 6: Wait for Builder Result

Poll for: `shared/builds/{build-id}/builder-result.yaml`

**Poll behavior:**
- Check every 10 seconds
- Timeout: 700 seconds
- If file appears: read it and proceed to Step 7
- If timeout: report failure to user with last known status from `build.yaml`

---

## Step 7: Report

Read `builder-result.yaml`.

### Success Path
If `status: complete`:
```
✓ Agent built successfully.

Agent Name: {agent_name}
Profile: {profile_path}
Port: {port}
Ready to use.
```

### Failure Path
If `status: failed`:
```
The build encountered an issue:

Error: {builder_result.error.message}
Phase: {builder_result.error.phase}

Would you like to:
1. Retry the build
2. Start fresh with a new idea
3. Adjust the scope and try again
```

---

## Multiple Builds

Each build gets its own `{build-id}` directory with independent research and builder outputs.

If a build is in progress: "You have a build in progress ([domain]). Start a new one, or finish that first?"

---

## Error Handling

**Research worker timeout (>300s):**
- Continue with partial research found so far
- User message: "I'll proceed with the research we have so far."

**Builder timeout (>700s):**
- User message: "The build is taking longer than expected. Let me check what happened."
- Read `build.yaml` for last known status
- Report to user with context
- Offer retry or fresh start

**Builder reports failure:**
- Read `builder_result.error` field
- Translate to user-friendly message
- Offer to retry or start fresh

### Retry Strategy

1. **First failure** → Tell user. Retry automatically (resend phase 2 task).
2. **Second failure** → Tell user exactly what happened. Offer options.
3. **Third attempt** → Give up. Report to user. No more retries.

---

## Builder Result Schema (builder-result.yaml)

```yaml
builder_result:
  status: "complete" | "failed"
  timestamp: "2026-03-14T15:50:00Z"
  
  # On success:
  agent:
    name: "flight-booking-agent"
    profile_path: "~/.openclaw-factory/workspace_builder/{build-id}/"
    port: 8080
    entry_point: "agent.py"
  
  notes: "Agent ready for deployment"
  
  # On failure:
  error:
    phase: "design" | "assembly" | "validation" | "etc"
    message: "Clear error description"
    retries: 0
```
