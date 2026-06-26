---
name: awp-workflow-builder
description: >
  Generate complete Agent Workflow Protocol (AWP) compliant multi-agent
  workflows from natural language descriptions. Produces workflow.awp.yaml,
  agent configs, prompts, schemas, and optionally custom tools and skills.
version: "1.0.0"
user-invocable: true
allowed-tools: Read Write Edit Bash Glob Grep
---

# AWP Workflow Builder

## AWP 7-Layer Model

AWP organizes a workflow into seven protocol layers. Each layer answers one question:

```
 Layer 6  OBSERVABILITY     How do I monitor this workflow?
 Layer 5  ORCHESTRATION     In what order and under what conditions?
 Layer 4  MEMORY & STATE    What does the workflow remember?
 Layer 3  COMMUNICATION     How do agents talk to each other?
 Layer 2  CAPABILITIES      What can an agent do? (tools, skills)
 Layer 1  AGENT IDENTITY    Who is this agent?
 Layer 0  MANIFEST          What is this workflow?
```

You start at the bottom. Layer 0 (manifest) and Layer 1 (agent identity)
are always required. Everything above is opt-in.

## Compliance Feature Layers

Each compliance level adds a set of features. These feature layers map to the
protocol layers above:

| Feature Layer | Name | Purpose |
|---------------|------|---------|
| F0 | Orchestration | DAG-based agent graph, execution modes, timeouts, error handling. |
| F1 | State | Persistent state, sharing strategies, required fields, auto-inject. |
| F2 | Communication | Message bus for inter-agent messaging, channels, direct/broadcast. |
| F3 | Memory | Long-term memory (MEMORY.md), daily logs, search, curation. |
| F4 | Observability | Structured logging, distributed tracing, metrics collection. |
| F5 | Governance | Security audit, rate limiting, circuit breakers, access control. |
| F6 | Extension | Custom MCP tools, project-level skills, hooks, preprocessors. |

## Compliance Levels

| Level | Name | Required Features | Description |
|-------|------|-------------------|-------------|
| L0 Core | Core | F0 | Single agent, basic orchestration. Minimum viable workflow. |
| L1 Composable | Composable | F0 + F1 | Multi-agent DAG with state sharing. |
| L2 Communicative | Communicative | F0-F2 | Inter-agent messaging via message bus. |
| L3 Memorable | Memorable | F0-F3 | Memory tiers for cross-session persistence. |
| L4 Observable | Observable | F0-F4 | Full observability: tracing, metrics, structured logs. |
| L5 Enterprise | Enterprise | F0-F6 | All features, production-grade governance and extensibility. |

## Platform Features

| Feature | Config Location | Description |
|---------|----------------|-------------|
| Agent DAG | `workflow.awp.yaml` graph | Directed acyclic graph of agents with depends_on edges. |
| State Sharing | graph[].share_output | Fields from an agent's output available to dependents. |
| Execution Modes | execution.mode | sequential, parallel, or conditional execution. |
| MCP Tools | agent.awp.yaml tools | Tool calling via the MCP registry (web, file, shell, etc.). |
| Message Bus | communication.bus | In-memory message passing between agents. |
| Memory | memory.tiers | Long-term (MEMORY.md) and working (daily logs) memory. |
| Skills | workflow skills/ | Markdown knowledge injected into agent system prompts. |
| Preprocessor | agent workflow/preprocessor/ | Data extraction and feature engineering before LLM call. |
| Vision | agent.awp.yaml vision | Image processing via base64-encoded data URLs. |


## STRICT RULES

These rules define compliance requirements for AWP workflows. Rules marked **(recommended for Python)** apply to the Python reference implementation but may be adapted for other platforms.

- **R1:** `workflow.name` MUST match the workflow directory name.
- **R2:** All agent IDs MUST be `snake_case` (lowercase letters, digits, underscores).
- **R3 (recommended for Python):** Every `agent.py` SHOULD define a class named `Agent` that extends `AWPAgent` (or a platform-specific base class).
- **R4 (recommended for Python):** The `Agent.name` property MUST return the same string as the agent ID in the graph.
- **R5:** Every agent in the graph MUST have a corresponding directory under `agents/`.
- **R6:** Every agent directory MUST contain `agent.awp.yaml` and `agent.py`.
- **R7:** Every agent MUST have `workflow/instructions/SYSTEM_PROMPT.md`.
- **R8:** Every agent MUST have `workflow/prompt/00_INTRO.md`.
- **R9:** Every agent MUST have `workflow/output_schema/output_schema.json`.
- **R10:** Every agent MUST have `workflow/output_schema_desc/output_schema_desc.json`.
- **R11:** `depends_on` MUST only reference agent names defined in the same graph.
- **R12:** The agent graph MUST be a DAG (no cycles).
- **R13:** `share_output` fields MUST match keys in the agent's output schema.
- **R14:** Tool names in `tools.allowed` MUST reference registered MCP tools. When tool implementation mode is enabled, built-in tools MUST have generated implementations in `mcp/`. When disabled, built-in tools are assumed to be provided by the target runtime.
- **R15:** If `tools.execute` is false, `tools.allowed` MUST be empty or omitted.
- **R16:** `execution.mode` MUST be one of: `sequential`, `parallel`, `conditional`.
- **R17:** All output schemas MUST include a `confidence` field (number, 0.0-1.0).
- **R18:** All `output_schema.json` files MUST be valid JSON Schema draft-07 with `"type": "object"` at the root.


## Workflow Generation Phases

### Phase 0: Planning

Before generating any files, analyze the user's requirements:

1. **Analyze the requirement.** What is the workflow supposed to do? What data flows between agents?
2. **Design the agent graph.** Identify distinct roles, dependencies, and data flow.
3. **Plan state sharing.** Which fields does each agent produce? Which does each consumer need?
4. **Determine compliance level.** What features are needed? Start at L0 and add layers only as required.
5. **Identify tools.** Which MCP tools does each agent need? (web.search, file.read, etc.)
6. **Plan memory.** Does the workflow benefit from cross-session persistence?
7. **Plan communication.** Do agents need to message each other outside the DAG?
8. **Tool implementation mode.** Does the user want tool implementations generated? (See "Tool Implementation Generation" below.)

### Phase 1: Requirements Gathering (Interactive Questionnaire)

**IMPORTANT:** Before generating anything, you MUST present the user with a structured
questionnaire. Do NOT skip this phase. Even if the user gave a detailed description,
there are always decisions that need clarification. Present ALL questions at once in a
single message so the user can answer them together.

For every question: provide concrete suggestions based on what the user already told you,
mark one as the recommended default (with `← empfohlen` / `← recommended`), and always
include a "Sonstiges / Other" option so the user can specify something not listed.

If the user already answered a question clearly in their initial request, pre-fill the
answer and mark it with `✓ (aus deiner Beschreibung)` — but still show it so the user
can correct it.

---

**Present the following questionnaire:**

#### 1. Workflow-Grundlagen / Workflow Basics

**1.1 Name:** Wie soll der Workflow heißen?
> Vorschläge: `{suggest 2-3 snake_case names based on user's description}`
> Sonstiges: ___

**1.2 Beschreibung:** Was soll der Workflow in einem Satz tun?
> Vorschlag: `{1-sentence summary based on user's description}`
> Sonstiges: ___

**1.3 Sprache der Prompts:** In welcher Sprache sollen die System-Prompts und Ausgaben sein?
> a) Deutsch ← empfohlen (wenn User auf Deutsch schreibt)
> b) Englisch
> c) Sonstiges: ___

---

#### 2. Agents & Rollen

**2.1 Welche Agents soll der Workflow haben?** Jeder Agent hat eine klar definierte Rolle.
> Vorschläge (basierend auf deiner Beschreibung):
> {list each suggested agent with id, role name, and 1-line description}
>
> Sollen Agents hinzugefügt, entfernt oder umbenannt werden?
> Sonstiges: ___

**2.2 Ausführungsreihenfolge:** Wie sollen die Agents ausgeführt werden?
> a) Sequenziell (einer nach dem anderen in fester Reihenfolge) ← empfohlen
> b) Parallel (unabhängige Agents gleichzeitig)
> c) Bedingt (Agents werden je nach Ergebnis übersprungen)
> d) Sonstiges: ___

**2.3 Datenfluss:** Welche Daten gibt jeder Agent an den nächsten weiter?
> Vorschlag:
> {show suggested data flow: agent_a → [fields] → agent_b → [fields] → agent_c}
>
> Änderungen? Sonstiges: ___

---

#### 3. LLM-Konfiguration

> **Hinweis:** LLM-Modelle werden **nicht** im Workflow festgelegt. Sie werden
> beim Start über den **Run-Wizard** (`awp run`) oder die Umgebungsvariable
> `LLM_MODEL` konfiguriert. So kann der User das Modell jederzeit wechseln,
> ohne den Workflow zu ändern.

**3.1 Temperatur:** Wie kreativ sollen die Agents antworten?
> a) Niedrig (0.1) — faktisch, präzise ← empfohlen für Analyse/Recherche
> b) Mittel (0.3) — ausgewogen
> c) Hoch (0.7) — kreativ, variabel
> d) Pro Agent unterschiedlich (bitte angeben)
> e) Sonstiges: ___

---

#### 4. Tools, Code Mode & Fähigkeiten

**4.1 Welche Tools brauchen die Agents?**
> Vorschläge pro Agent:
> {for each agent, list suggested tools with brief explanation, e.g.:}
> - `{agent_id}`: `web.search` (Webrecherche), `memory.write` (Ergebnisse speichern)
> - `{agent_id}`: keine Tools (reiner LLM-Agent)
>
> Änderungen? Sonstiges: ___

> **Hinweis:** Erweiterte Tool-Calling-Optionen (`tool_choice`, `parallel_calls`)
> können pro Agent in `agent.awp.yaml` unter `capabilities.tools` konfiguriert werden.
> Defaults sind sinnvoll für die meisten Workflows — nur bei Bedarf anpassen.

**4.2 Tool-Implementierungen generieren?** Sollen funktionierende Implementierungen
für die Tools miterzeugt werden (z.B. `web.search` mit DuckDuckGo, `memory.*` mit
Dateispeicher)? Ohne dies sind Tools nur Platzhalter, die eine AWP-Runtime bereitstellen muss.
> a) Ja — alle verwendeten Tools als MCP-Implementierungen generieren ← empfohlen für Standalone
> b) Nein — nur Tool-Deklarationen, Runtime stellt sie bereit ← empfohlen für AWP-Runtime
> c) Nur bestimmte Tools implementieren (bitte angeben)
> d) Sonstiges: ___

**4.3 Code Mode (Alternative Tool-Ausführung)?** Statt Tools einzeln aufzurufen,
schreibt der Agent Code gegen ein typed SDK. Reduziert Token-Verbrauch und
LLM-Roundtrips bei vielen Tools.
> a) Nein — klassische Tool-Aufrufe ← empfohlen für einfache Workflows
> b) Ja — Agent schreibt TypeScript gegen SDK ← empfohlen bei >5 Tools
> c) Ja — Agent schreibt Python gegen SDK
> d) Sonstiges: ___

---

#### 4b. API Keys & Secrets

**4b.1 Brauchen die Tools API-Schlüssel oder Zugangsdaten?** Secrets werden über
`secrets.yaml` (gitignored) bereitgestellt und sicher an Tools injiziert — das LLM
sieht sie nie.
> Vorschläge basierend auf den gewählten Tools:
> {for each tool that typically needs API keys, e.g.:}
> - `web.search`: Optional — DuckDuckGo (kostenlos, kein Key) oder Premium-API (Google, Bing, SearXNG)
> - `http.request`: Abhängig vom Ziel-API — Bearer Token, API Key, etc.
> - Eigene Tools: bitte Keys auflisten
>
> a) Keine API-Schlüssel nötig ← empfohlen für Einstieg
> b) Ja — folgende Keys werden gebraucht: ___
> c) Sonstiges: ___

---

#### 5. Ausgabeformat & Schemas

**5.1 Ausgabeformat der Agents:**
> a) JSON (strukturiert, maschinenlesbar) ← empfohlen
> b) Markdown (Freitext, menschenlesbar)
> c) Gemischt (manche JSON, manche Markdown — bitte angeben)
> d) Sonstiges: ___

**5.2 Welche Felder soll jeder Agent ausgeben?**
> Vorschläge:
> {for each agent, list suggested output fields with types}
> (Hinweis: `confidence` (0.0-1.0) wird automatisch ergänzt — AWP-Pflichtfeld.)
>
> Änderungen? Sonstiges: ___

---

#### 6. Memory & Persistenz

**6.1 Soll der Workflow ein Langzeitgedächtnis haben?** (Ergebnisse über Sessions hinweg speichern)
> a) Nein — jeder Lauf ist unabhängig ← empfohlen für einfache Workflows
> b) Ja — MEMORY.md für übergreifende Erkenntnisse
> c) Ja — mit täglichen Logs und MEMORY.md ← empfohlen für wiederkehrende Aufgaben
> d) Sonstiges: ___

---

#### 7. Skills & Domänenwissen

**7.1 Braucht der Workflow spezifisches Domänenwissen?** (Wird als SKILL.md in die Prompts injiziert)
> a) Nein
> b) Ja — bitte Thema/Domain beschreiben: ___
> c) Vorschlag: `{suggest a skill based on user's domain, e.g.: "industry-regulations"}`
> d) Sonstiges: ___

---

#### 8. Ausgabeverzeichnis & Projektstruktur

**8.1 Wo soll der Workflow gespeichert werden?**
> a) `{suggest path based on context, e.g.: ~/projects/{workflow_name}/}`
> b) Aktuelles Verzeichnis
> c) Sonstiges: ___

---

#### 9. Ziel-Plattform

**9.1 Wo soll der Workflow laufen?**
> a) **Standalone (Python)** — lokale Ausführung mit `awp-protocol` ← empfohlen für Einstieg
> b) **Cloudflare Workers** — serverless Edge-Deployment (TypeScript)
> c) Sonstiges: ___

---

#### 10. Compliance Level

**9.1 Welches AWP-Compliance-Level?**
> a) **L0 Core** — einfacher Workflow, nur Orchestrierung ← empfohlen für Einstieg
> b) **L1 Composable** — Multi-Agent mit State Sharing ← empfohlen für die meisten Workflows
> c) **L2 Communicative** — mit Inter-Agent-Messaging
> d) **L3 Memorable** — mit Langzeitgedächtnis
> e) **L4 Observable** — mit Tracing, Metriken, Logging
> f) **L5 Enterprise** — alle Features, produktionsreif
> g) Sonstiges: ___

---

#### 11. Sonstiges

**10.1 Gibt es weitere Anforderungen, Einschränkungen oder Wünsche?**
> z.B. Timeouts, Fehlerbehandlung, Sicherheitsanforderungen, spezielle Datenquellen,
> Zielgruppe der Ausgabe, …
> ___

---

**After receiving answers:** Analyze the responses, resolve any conflicts, and proceed
to Phase 2. If answers are ambiguous or contradictory, ask targeted follow-up questions
(but not another full questionnaire). If the user says "defaults" or "passt so", use
all recommended defaults.

### Phase 2: Workflow-Plan (From Abstract to Concrete)

**IMPORTANT:** Before generating any files, you MUST create a structured workflow plan
and present it to the user for confirmation. This plan bridges the gap between the
abstract idea and the concrete implementation. It ensures that the user understands
exactly what will be built before a single file is created.

The plan follows a **top-down refinement** -- starting with the high-level goal and
progressively adding detail until every file, field, and dependency is specified.

Present the plan as a single, structured document:

---

#### Step 1: Goal Statement (Abstract)

Summarize the workflow's purpose in 2-3 sentences. What problem does it solve?
What is the expected input and output? This is the "elevator pitch" for the workflow.

> **Goal:** {what the workflow does, in plain language}
> **Input:** {what the user provides to start the workflow}
> **Output:** {what the user gets at the end}

#### Step 2: Agent Roles & Responsibilities (Conceptual)

For each agent, describe its role in non-technical terms. Focus on **what** it does,
not **how**. Think of this as a team of people -- what is each person's job?

| Agent | Role | Receives from | Delivers to |
|-------|------|--------------|-------------|
| `{id}` | {role in plain language} | {upstream agent or "user input"} | {downstream agent or "final output"} |

#### Step 3: Data Flow & Contracts (Architectural)

Now make the data flow concrete. Define what data moves between agents:

```
User Input
  │
  ▼
[agent_a] ──── produces: {field_1, field_2, confidence}
  │                shares: {field_1, field_2}
  ▼
[agent_b] ──── receives: {field_1, field_2}
  │                produces: {field_3, field_4, confidence}
  │                shares: {field_3}
  ▼
[agent_c] ──── receives: {field_3}
                   produces: {final_output, confidence}
```

For each shared field, specify the type and a one-line description.

#### Step 4: Tool & Capability Mapping (Technical)

Map each agent to its concrete capabilities:

| Agent | Tools | Memory | Skills | Reasoning |
|-------|-------|--------|--------|-----------|
| `{id}` | `{tool.fqn}`, ... | {yes/no, tier} | {skill name or none} | {enabled/disabled} |

#### Step 5: File Manifest (Implementation)

List every file that will be generated, grouped by agent:

```
{workflow_name}/
  workflow.awp.yaml
  secrets.yaml.example          (if secrets needed)
  mcp/
    {tool_file}.py              ← {purpose}
  skills/
    {skill_name}/SKILL.md       ← {purpose}
  agents/
    {agent_id}/
      agent.awp.yaml
      agent.py
      workflow/
        instructions/SYSTEM_PROMPT.md
        prompt/00_INTRO.md
        output_schema/output_schema.json
        output_schema_desc/output_schema_desc.json
    ...
```

State the total file count and the target compliance level.

#### Step 6: Validation Preview

List which of the 24 rules (R1-R24) apply and confirm they will be satisfied:

> **Compliance Target:** L{N} {Level Name}
> **Applicable Rules:** R1-R{max} (all satisfied by this plan)
> **Special Considerations:** {any edge cases, e.g., conditional execution, cyclic risk}

---

#### Step 7: Plan Validation Menu

After presenting the plan (Steps 1-6), you MUST present a **dynamic validation menu**
as a set of multiple-choice questions. Each question targets one key design decision
from the plan. For every question: pre-select the answer that matches your plan
(marked with `→`), provide 2-4 concrete alternatives, and always include a free-text
option. The user validates by confirming or correcting each point.

**IMPORTANT:** The questions must be **specific** to the generated plan -- not generic.
Use actual agent names, field names, tool names, and values from the plan. The menu
is a focused checklist, not a second questionnaire.

---

**Plan-Validierung -- bitte prüfe die folgenden Punkte:**

**V1. Agent-Anzahl und -Rollen**
> → a) {N} Agents: `{agent_1}` ({role_1}), `{agent_2}` ({role_2}), ... ← aus dem Plan
> b) Agent hinzufügen: z.B. `{suggested_extra_agent}` ({suggested_role})
> c) Agent entfernen: welchen? ___
> d) Agent umbenennen: welchen? ___
> e) Sonstiges: ___

**V2. Ausführungsreihenfolge**
> → a) {mode aus dem Plan}: `{agent_1}` → `{agent_2}` → `{agent_3}` ← aus dem Plan
> b) {alternative_mode}: {concrete alternative, e.g., agent_1 + agent_2 parallel, dann agent_3}
> c) Bedingt: {suggest a condition, e.g., "agent_2 nur wenn agent_1.confidence > 0.7"}
> d) Sonstiges: ___

**V3. Datenfluss zwischen Agents**
> → a) Wie geplant: `{agent_1}` teilt `{field_1}, {field_2}` → `{agent_2}` teilt `{field_3}` → `{agent_3}` ← aus dem Plan
> b) Feld hinzufügen: welches, bei welchem Agent? ___
> c) Feld entfernen: welches? ___
> d) Sonstiges: ___

**V4. Tools pro Agent**
> Für jeden Agent eine Zeile:
> → a) `{agent_1}`: `{tool_1}`, `{tool_2}` ← aus dem Plan
> → b) `{agent_2}`: keine Tools ← aus dem Plan
> → c) `{agent_3}`: `{tool_3}` ← aus dem Plan
> Änderungen? Tool hinzufügen/entfernen? ___

**V5. Ausgabefelder pro Agent**
> Für jeden Agent die geplanten Output-Felder:
> → a) `{agent_1}`: `{field_1}` (string), `{field_2}` (array), `confidence` (number) ← aus dem Plan
> → b) `{agent_2}`: `{field_3}` (object), `confidence` (number) ← aus dem Plan
> Felder ändern/hinzufügen/entfernen? ___

**V6. Compliance Level**
> → a) L{N} {Level Name} ← aus dem Plan
> b) Niedriger: L{N-1} {Name} (entfernt: {was wegfällt})
> c) Höher: L{N+1} {Name} (fügt hinzu: {was dazukommt})
> d) Sonstiges: ___

**V7. Memory & Persistenz**
> → a) {geplante Memory-Konfiguration, z.B. "Kein Memory" oder "MEMORY.md + tägliche Logs"} ← aus dem Plan
> b) {alternative, z.B. "Memory hinzufügen: MEMORY.md für übergreifende Erkenntnisse"}
> c) {alternative, z.B. "Nur tägliche Logs, kein Langzeitgedächtnis"}
> d) Sonstiges: ___

**V8. Code Mode**
> → a) {geplanter Code Mode, z.B. "Nein — klassische Tool-Aufrufe"} ← aus dem Plan
> b) {alternative, z.B. "Ja — TypeScript Code Mode mit SDK"}
> c) {alternative, z.B. "Ja — Python Code Mode mit SDK"}
> d) Sonstiges: ___

**V9. Ziel-Plattform**
> → a) {geplante Plattform, z.B. "Standalone (Python)"} ← aus dem Plan
> b) {alternative, z.B. "Cloudflare Workers (TypeScript)"}
> c) Sonstiges: ___

**V10. Tool-Implementierungen**
> → a) {geplanter Modus, z.B. "Ja -- alle Tools als MCP-Implementierungen"} ← aus dem Plan
> b) {alternative, z.B. "Nein -- nur Deklarationen, Runtime stellt sie bereit"}
> c) Nur bestimmte implementieren: welche? ___
> d) Sonstiges: ___

**V11. Gesamtbewertung**
> → a) Plan ist korrekt -- bitte generieren
> b) Plan anpassen (bitte oben die betroffenen Punkte korrigieren)
> c) Plan verwerfen und neu planen
> d) Fragen zum Plan: ___

---

**After receiving validation answers:**
- If V11 = a) (approved): proceed directly to Phase 3 (file generation).
- If V11 = b) (adjustments): apply the corrections from V1-V10, re-present
  **only the changed sections** of the plan (not the full plan), and show
  an updated validation menu with only the changed questions.
- If V11 = c) (discard): return to Phase 1 or Phase 2 Step 1.
- If V11 = d) (questions): answer the questions, then re-present V11.

Iterate until the user selects V11 = a). Do NOT generate any files until
the plan is explicitly approved. The plan is the contract between AI and user.

### Phase 3: Generate the Project

Generate files in this order:

#### Step 1: Workflow Manifest

Create `{workflow_dir}/workflow.awp.yaml` with:
- `project` section (name, version, description).
- `graph` section (all agents with depends_on and share_output).
- `execution` section (mode, timeouts, error handling).
- `state` section (persistence, sharing strategy).
- Additional sections as needed by compliance level: `memory`, `communication`, `observability`, `security`.
- `logging` section.
- `settings` section (LLM models, runtime config).

Use the template at `templates/workflow.awp.yaml` as a starting point.

#### Step 2: Agent Configurations

For each agent, create `{workflow_dir}/agents/{agent_id}/agent.awp.yaml` with:
- `agent` section (name, description).
- `llm` section (model, temperature, reasoning).
- `tools` section (execute flag, max_calls, allowed list).
- `preprocessor`, `vision`, `memory`, `debug` sections as needed.

Use `templates/agent.awp.yaml` (minimal) or `templates/agent-full.awp.yaml` (full-featured).

#### Step 3: Agent Implementations (Platform-Specific)

For each agent, create `{workflow_dir}/agents/{agent_id}/agent.py`.

AWP is platform-agnostic. The `agent.py` file varies by target runtime.
Choose the appropriate **adapter** based on the target platform:

| Platform | Adapter | Generated Files |
|----------|---------|----------------|
| **Standalone (awp-protocol)** | `adapters/standalone.md` | `agent.py` (Python) |
| **Cloudflare Workers** | `adapters/cloudflare-dynamic-workers.md` | `src/index.ts`, `wrangler.toml` (TypeScript) |

**Default:** Use `templates/agent.py` which imports from `awp.agent`.

Read the adapter file in `skill/adapters/` for platform-specific instructions,
then generate `agent.py` accordingly. Third-party platforms can provide their
own adapter files following the same pattern.

#### Step 4: System Prompts

For each agent, create `{workflow_dir}/agents/{agent_id}/workflow/instructions/SYSTEM_PROMPT.md`:
- Clear role description.
- List of responsibilities.
- Available tools (if any) with usage instructions.
- Output format instructions referencing the output schema.

Use `templates/SYSTEM_PROMPT.md` as a starting point.

#### Step 5: Intro Prompts

For each agent, create `{workflow_dir}/agents/{agent_id}/workflow/prompt/00_INTRO.md`:
- Brief task introduction.
- Context about what input the agent receives.

Use `templates/00_INTRO.md` as a starting point.

#### Step 6: Output Schemas

For each agent, create:
- `{workflow_dir}/agents/{agent_id}/workflow/output_schema/output_schema.json` -- JSON Schema draft-07.
- `{workflow_dir}/agents/{agent_id}/workflow/output_schema_desc/output_schema_desc.json` -- Human-readable field descriptions.

All schemas MUST have `"type": "object"` at root and include a `confidence` field. Use `templates/output_schema.json` and `templates/output_schema_desc.json`.

#### Step 7: Custom Tools (if needed)

If the workflow needs custom MCP tools, create `{workflow_dir}/mcp/{tool_file}.py` using the FastMCP pattern. See `templates/mcp-tool.py`.

#### Step 7b: Built-in Tool Implementations (if tool implementation mode is enabled)

When tool implementation mode is **enabled**, generate MCP implementations for every
built-in tool referenced in any agent's `tools.allowed` list that is **not** already
provided by an external runtime or custom tool. This ensures the workflow is
self-contained and can run without a full AWP runtime providing built-in tool stubs.

**Process:**

1. Collect all unique tool FQNs from every agent's `tools.allowed` across the workflow.
2. For each tool FQN that belongs to a **reserved namespace** (`web`, `http`, `file`,
   `shell`, `agent`, `memory`, `arithmetic`):
   - Generate a working MCP implementation in `{workflow_dir}/mcp/{namespace}_{action}.py`.
   - Use the FastMCP pattern from `templates/mcp-tool.py`.
   - Implement real logic (not stubs) appropriate to the tool's purpose.
   - Match the parameter signature from `references/tools-reference.md`.
3. Tools that the user explicitly provides (e.g., as external MCP servers or custom
   implementations already in `mcp/`) are **skipped** — do not overwrite them.

**Implementation guidelines per namespace:**

| Tool | Implementation approach |
|------|----------------------|
| `web.search` | Use `httpx` or `requests` to call a search API (e.g., DuckDuckGo, SearXNG, or a configurable endpoint). Return structured results. |
| `http.request` | Use `httpx` to make arbitrary HTTP requests with timeout and error handling. |
| `file.read` / `file.write` / `file.list` | Use Python `pathlib` with sandboxed path validation. |
| `shell.execute` | Use `subprocess.run` with timeout and cwd support. |
| `memory.write` / `memory.read` / `memory.search` / `memory.curate` | Use file-based storage in a `{workflow_dir}/.memory/` directory. |
| `agent.send_message` / `agent.list_messages` | Use file-based message queue in `{workflow_dir}/.messages/`. |
| `arithmetic.*` | Direct Python arithmetic operations. |

**Note:** When tool implementation mode is **disabled** (the default), this step is
skipped entirely. Built-in tool FQNs in `tools.allowed` are assumed to be provided
by the target runtime, per the AWP specification ("runtimes SHOULD provide").

**R14 compliance:** When tool implementation mode is enabled, R14 ("tools.allowed MUST
reference registered MCP tools") is satisfied by the generated implementations. When
disabled, R14 compliance depends on the target runtime registering these tools.

#### Step 7c: Code Mode SDK & Skill (if Code Mode is enabled)

When an agent has `capabilities.codemode.enabled: true`:

1. Generate a **typed SDK interface** from the agent's `tools.allowed`.
   Group methods by namespace (e.g., `sdk.web.search()`, `sdk.file.read()`).

   **TypeScript SDK template:**

   ```typescript
   // AWP Code Mode SDK — TypeScript Interface
   // Auto-generated from capabilities.tools.allowed

   /** AWP Tool SDK for Code Mode execution. All methods return a standard AWP ToolResult. */
   export interface AWPToolSDK {
     {{SDK_METHODS}}
   }

   /** Standard AWP tool result. */
   export interface ToolResult {
     ok: boolean;
     status: number;
     data: Record<string, unknown>;
     error: string | null;
   }

   /** Execute function signature. The agent writes a function matching this signature. */
   export type AgentExecuteFn = (sdk: AWPToolSDK) => Promise<Record<string, unknown>>;

   // ── Example SDK shape (when tools include web.*, file.*, memory.*) ──
   //
   // interface AWPToolSDK {
   //   web: {
   //     search(query: string, maxResults?: number): Promise<ToolResult>;
   //   };
   //   file: {
   //     read(path: string): Promise<ToolResult>;
   //     write(path: string, content: string): Promise<ToolResult>;
   //     list(directory: string): Promise<ToolResult>;
   //   };
   //   memory: {
   //     read(key: string): Promise<ToolResult>;
   //     write(key: string, value: string): Promise<ToolResult>;
   //     search(query: string): Promise<ToolResult>;
   //   };
   // }
   ```

   **Python SDK template:**

   ```python
   # AWP Code Mode SDK — Python Class
   # Auto-generated from capabilities.tools.allowed

   from typing import Any

   class ToolResult:
       """Standard AWP tool result."""
       ok: bool
       status: int
       data: dict[str, Any]
       error: str | None

   class AWPToolSDK:
       """AWP Tool SDK for Code Mode execution. All methods return a standard AWP ToolResult."""

       {{SDK_METHODS}}

   # ── Example SDK shape (when tools include web.*, file.*, memory.*) ──
   #
   # class AWPToolSDK:
   #     class web:
   #         async def search(query: str, max_results: int = 5) -> ToolResult: ...
   #
   #     class file:
   #         async def read(path: str) -> ToolResult: ...
   #         async def write(path: str, content: str) -> ToolResult: ...
   #         async def list(directory: str) -> ToolResult: ...
   #
   #     class memory:
   #         async def read(key: str) -> ToolResult: ...
   #         async def write(key: str, value: str) -> ToolResult: ...
   #         async def search(query: str) -> ToolResult: ...
   ```

2. Generate a **Code Mode skill** using `templates/codemode-skill.md`:
   - Replace `{{SDK_TYPE_DEFINITIONS}}` with the generated SDK interface
   - Replace `{{SDK_METHOD_LIST}}` with a list of available methods
   - Replace `{{OUTPUT_SCHEMA_FIELDS}}` with the agent's output contract
   - Replace `{{LANGUAGE}}` and `{{CODE_EXAMPLE}}` with appropriate examples

3. Place the skill at `{agent}/workflow/skills/codemode.md` (agent-level skill).

4. Ensure the agent's `agent.awp.yaml` has:
   - `capabilities.codemode.enabled: true`
   - `capabilities.codemode.language: {typescript|python}`
   - `capabilities.sandbox.type` set (not `none`)

#### Step 8: Project Skills (if needed)

If the workflow needs shared domain knowledge, create `{workflow_dir}/skills/{skill_name}/SKILL.md`. See `templates/project-skill.md`.

#### Step 9: WORKFLOW.md (Project Overview)

Generate `{workflow_dir}/WORKFLOW.md` as specified in Phase 4b. This file MUST always
be generated — it is not optional. It serves as the human-readable entry point for
anyone opening the project. The file uses only plain-text ASCII diagrams so it is
universally readable without rendering tools.

### Phase 4: Validation Checklist

After generating all files, verify:

- [ ] R1: workflow.name matches directory name.
- [ ] R2: All agent IDs are snake_case.
- [ ] R3: All agent.py files define class Agent extending AWPAgent (or platform base).
- [ ] R4: Agent.name property returns the correct agent ID.
- [ ] R5: Every graph agent has a directory under agents/.
- [ ] R6: Every agent directory has agent.awp.yaml and agent.py.
- [ ] R7: Every agent has SYSTEM_PROMPT.md.
- [ ] R8: Every agent has 00_INTRO.md.
- [ ] R9: Every agent has output_schema.json.
- [ ] R10: Every agent has output_schema_desc.json.
- [ ] R11: depends_on references only graph-defined agents.
- [ ] R12: No cycles in the agent graph.
- [ ] R13: share_output fields match output schema keys.
- [ ] R14: tools.allowed references valid MCP tools (if tool implementation mode: verify generated implementations exist in mcp/).
- [ ] R15: tools.execute=false implies empty allowed list.
- [ ] R16: execution.mode is sequential, parallel, or conditional.
- [ ] R17: All output schemas include confidence field.
- [ ] R18: All output_schema.json are valid JSON Schema draft-07 with type: object.
- [ ] R19: If codemode.enabled, then tools.enabled must be true.
- [ ] R20: If codemode.enabled, sandbox.type must be set (not "none").
- [ ] R21: codemode.language is typescript, python, or javascript.
- [ ] R22: If sdk_surface.mode is "explicit", include list is non-empty.
- [ ] R23: sdk_surface.exclude entries match tools in tools.allowed.
- [ ] R24: If sandbox.type is "isolate", sandbox.network is defined.
- [ ] R25: WORKFLOW.md exists at project root with ASCII diagram and abstract-to-concrete description.

### Phase 4b: Generate WORKFLOW.md (Project-Level Overview)

**IMPORTANT:** After validation and before presenting the summary, you MUST generate
a `{workflow_dir}/WORKFLOW.md` file at the project root. This file serves as the
always-readable, self-contained documentation of the workflow. It MUST use only
plain-text ASCII diagrams (no Mermaid, no HTML, no images) so it renders correctly
in any Markdown viewer, terminal, or text editor.

The file follows a **top-down structure** from abstract to concrete:

```markdown
# {Workflow Name}

> {One-sentence elevator pitch: what this workflow does and why.}

**AWP Compliance:** L{N} {Level Name} | **Agents:** {count} | **Execution:** {mode}

---

## Workflow-Diagramm

{ASCII box-and-arrow diagram — see format below}

---

## Überblick (Abstract)

{2-3 sentences: What problem does this workflow solve? What is the input,
what is the output? Written for someone who has never seen AWP.}

## Agent-Rollen (Conceptual)

{For each agent: name, role in plain language, what it receives, what it delivers.
Use a table or bullet list.}

| Agent | Rolle | Empfängt von | Liefert an |
|-------|-------|-------------|-----------|
| `{id}` | {role} | {upstream or "User-Eingabe"} | {downstream or "Endausgabe"} |

## Datenfluss (Architectural)

{Concrete data contracts: which fields flow between agents, with types.
Use the ASCII arrow notation from Phase 2 Step 3.}

## Tools & Fähigkeiten (Technical)

{Table mapping each agent to its tools, memory, skills, code mode.}

## Dateistruktur (Implementation)

{Tree listing of all generated files, grouped by agent.}

## Wie starten

{Ready-to-use commands: install, run, validate.}

---

*Generiert von AWP Workflow Builder — {date}*
```

**Diagram rendering rules:**

The ASCII diagram in `WORKFLOW.md` MUST be rendered with care for visual quality.
Use Unicode box-drawing characters (`┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼ ▼ ▶ ◀ ▲`) for clean
rendering. Follow these rules:

1. **All agents** appear as labeled boxes with their role name.
2. **Data flow** between agents as arrows with the shared field names on the edge.
3. **Tools** attached to the agents that use them (as small labels inside the box).
4. **Memory** tiers if the workflow uses persistence.
5. **Input** (top) and **Output** (bottom) clearly marked.
6. **Consistent box widths** — all boxes at the same level should have the same width.
7. **Center-aligned** — the diagram should be visually centered and balanced.
8. For **parallel agents**, show them side by side with a horizontal spread.
9. For **conditional execution**, annotate arrows with the condition in `[brackets]`.
10. **No Mermaid, no HTML** — only plain-text ASCII so the file is universally readable.

### Phase 5: Summary & Workflow Overview

**CRITICAL — This is the final presentation to the user.** Phase 5 MUST always
be displayed **in Claude's terminal output** before any zip/pack file is offered.
The user should see the complete workflow at a glance — diagram, description,
files, and compliance — directly in the conversation. This is NOT optional.
Do not skip to the zip output. Do not abbreviate. The terminal presentation
IS the deliverable that the user reviews before accepting the workflow.

Present the following sections **in this exact order**:

---

#### 5a. Workflow Header

```
═══════════════════════════════════════════════════════════════
  AWP Workflow: {workflow_name}
  Compliance: L{N} {Level Name} │ Agents: {count} │ Mode: {execution_mode}
═══════════════════════════════════════════════════════════════
```

#### 5b. Workflow Architecture Diagram

**This is the visual centerpiece.** The ASCII diagram MUST be rendered directly
in Claude's output with maximum visual quality. It is the first thing the user
sees and must immediately convey the workflow's structure.

Rendering rules:
- Use Unicode box-drawing characters (`┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼ ▼ ▶ ◀ ▲`)
- Align all boxes cleanly, consistent widths per level
- Balance whitespace so the diagram is visually centered
- A well-rendered diagram is worth more than paragraphs of text

The diagram MUST show:

1. **All agents** as labeled boxes with their role name
2. **Data flow** between agents as arrows with shared field names
3. **Tools** attached to each agent (as labels inside the box)
4. **Code Mode** indicator (`⚡ Code Mode`) for agents with codemode enabled
5. **Skills** indicator (`📖 {skill_name}`) for agents with injected skills
6. **Memory** tiers if the workflow uses persistence
7. **Input** (top) and **Output** (bottom) clearly marked

Use this format:

```
                        ┌─────────────────────┐
                        │     User Input       │
                        │  "{task_description}" │
                        └──────────┬──────────┘
                                   │
                                   ▼
                  ┌────────────────────────────────────┐
                  │  {agent_id}                         │
                  │  Role: {role_description}           │
                  │  Tools: {tool_1}, {tool_2}          │
                  │  ⚡ Code Mode ({language})           │
                  │  📖 Skill: {skill_name}              │
                  │  Output: {field_1}, {field_2}       │
                  └──────────────────┬─────────────────┘
                                     │ shares: {field_1}
                                     ▼
                  ┌────────────────────────────────────┐
                  │  {agent_id}                         │
                  │  Role: {role_description}           │
                  │  Tools: {tool_1}                    │
                  │  Output: {field_3}, confidence      │
                  └──────────────────┬─────────────────┘
                                     │
                                     ▼
                        ┌─────────────────────┐
                        │    Final Output      │
                        │  {output_description} │
                        └─────────────────────┘
```

For parallel agents, show them side by side with a horizontal spread.
For conditional execution, annotate arrows with the condition in `[brackets]`.
Adapt the layout to the actual complexity — a 2-agent workflow gets a simple
diagram, a 6-agent DAG with branches gets a more detailed one.

#### 5c. Workflow Description (Narrative Walkthrough)

Directly below the diagram, provide a **narrative walkthrough** of the workflow
in 4-8 sentences. This description must:

1. **Explain the purpose** — What problem does this workflow solve? What goes in,
   what comes out?
2. **Walk through each stage** — Describe what happens at each agent in plain
   language, as if explaining it to someone who hasn't read the config files.
3. **Highlight the generated capabilities** — Which skills were generated and why?
   Which custom MCP tools were created? Which agents use Code Mode and what
   advantage does it give them?
4. **Explain key design decisions** — Why this agent order? Why these tools?
   Why this data flow? Why this compliance level?

Example:

> This workflow automates cloud security audits by orchestrating three specialized
> agents in a sequential pipeline. The **scanner** agent uses Code Mode (TypeScript)
> to execute 14 AWS API calls in a single LLM roundtrip via the generated
> `mcp/aws_scanner.py` tool — checking security groups, IAM policies, and S3
> bucket configurations. Its findings flow to the **analyzer** agent, which uses
> the generated `skills/aws-compliance/SKILL.md` (containing CIS Benchmark v8.0
> controls and NIST 800-53 mappings) to classify each finding by severity and
> recommend remediations. Finally, the **reporter** agent produces an executive
> summary with risk scores, using the `skills/report-writing/SKILL.md` for
> formatting standards. The workflow is L1 compliant (multi-agent DAG with state
> sharing) and requires only an OpenRouter API key to run.

#### 5d. Generated Capabilities Summary

Present a table of all generated skills, MCP tools, and Code Mode configurations:

```
  Generated Capabilities
  ──────────────────────────────────────────────────────────
  Skills:
    • skills/{name}/SKILL.md — {what domain knowledge it contains}
    • skills/{name}/SKILL.md — {what domain knowledge it contains}

  Custom MCP Tools:
    • mcp/{file}.py — {tool_fqn}: {what it does}
    • mcp/{file}.py — {tool_fqn}: {what it does}

  Code Mode Agents:
    • {agent_id} — {language}, sandbox: {type}, SDK surface: {tool_count} tools
  ──────────────────────────────────────────────────────────
```

If no custom skills, tools, or Code Mode agents were generated, state it
explicitly (e.g., "No custom MCP tools generated — workflow uses only built-in tools.").

#### 5e. Files Generated

List all generated files with count:

```
  Files Generated: {count}
  ──────────────────────────────────────────────────────────
  {workflow_name}/
    workflow.awp.yaml
    WORKFLOW.md
    agents/
      {agent_id}/
        agent.awp.yaml
        agent.py
        workflow/
          instructions/SYSTEM_PROMPT.md
          prompt/00_INTRO.md
          output_schema/output_schema.json
          output_schema_desc/output_schema_desc.json
    skills/
      {skill_name}/SKILL.md
    mcp/
      {tool_file}.py
  ──────────────────────────────────────────────────────────
```

#### 5f. Compliance Badge & Validation

```
  ✅ Validation: All {count}/24 applicable rules passed
  🏷️  AWP L{N} {Level Name} Compliant
```

- Reference to `WORKFLOW.md` for the full project documentation.
- Any assumptions made or recommendations for improvement.

#### 5g. Transition to Zip / Pack

**Only after the complete Phase 5 presentation above has been displayed**, offer
the packaged workflow:

```
  ──────────────────────────────────────────────────────────
  📦 Ready to pack: awp pack {workflow_name}/
     → {workflow_name}.awp.zip
  ──────────────────────────────────────────────────────────
```

If the user requested a zip output, generate it now. If not, remind them that
`awp pack` is available. The Phase 5 terminal output is the **review step** —
the user validates the architecture visually before accepting the deliverable.

#### How to Use

Provide ready-to-use commands for running the workflow:

**Install dependencies:**

```bash
cd {workflow_name}/
pip install -r requirements.txt    # if requirements.txt was generated
# or
pip install awp-protocol
```

**Run the workflow:**

```bash
awp run {workflow_name}/ --task "{example_task_description}"
```

**Run with Python:**

```python
from awp.runtime import WorkflowRunner

runner = WorkflowRunner("{workflow_name}")
result = runner.run("{example_task_description}")
print(result["{final_agent_id}"])
```

**Run on Cloudflare Workers** (if Cloudflare adapter was used):

```bash
cd {workflow_name}/
npm install
wrangler kv namespace create STATE
# → copy id into wrangler.toml
wrangler secret put LLM_API_KEY
wrangler deploy
```

```bash
# Invoke the deployed workflow
curl -X POST https://{workflow_name}.{account}.workers.dev \
  -H "Content-Type: application/json" \
  -d '{"task": "{example_task_description}"}'
```

**Customize:**

- Edit agent prompts in `agents/{agent_id}/workflow/instructions/SYSTEM_PROMPT.md`
- Adjust output schemas in `agents/{agent_id}/workflow/output_schema/`
- Add or change tools in `agents/{agent_id}/agent.awp.yaml` under `tools.allowed`
- Add domain knowledge in `skills/{skill_name}/SKILL.md`

If the workflow uses secrets, also show:

```bash
cp secrets.yaml.example secrets.yaml
# Edit secrets.yaml with your API keys
```

**Validate the workflow:**

```bash
awp validate {workflow_name}/
```

#### Required API Keys & Secrets

After the "How to Use" section, you MUST present a summary of **all API keys and
secrets** that are required (or optional) to run this workflow. This allows the
user to prepare everything before the first run.

Generate this section dynamically based on the workflow's actual configuration:

1. **LLM API Key:** Derived from the model the user will select at runtime.
   Always show the most common providers and their key sources.
2. **Tool Secrets:** Derived from the tools used across all agents (from
   `tools.allowed` in each `agent.awp.yaml`). Map each tool to the API key
   it typically needs.
3. **Custom Secrets:** Any secrets declared in the workflow's `env.required`
   section of `workflow.awp.yaml`.

Present in this format:

---

**Erforderliche API Keys / Required API Keys**

> Das LLM-Modell wird beim Start über den **Run-Wizard** oder `LLM_MODEL`
> gewählt. Je nach Modell wird ein passender API Key benötigt:

| Zweck | Env-Variable | Anbieter | Key besorgen |
|-------|-------------|----------|-------------|
| LLM (OpenRouter) | `OPENROUTER_API_KEY` | OpenRouter | https://openrouter.ai/keys (kostenlos) |
| LLM (OpenAI) | `OPENAI_API_KEY` | OpenAI | https://platform.openai.com/api-keys |
| LLM (Groq) | `GROQ_API_KEY` | Groq | https://console.groq.com/keys (kostenlos) |
| LLM (Ollama) | — | Ollama (lokal) | Kein Key nötig — https://ollama.com |
| LLM (Deepseek) | `DEEPSEEK_API_KEY` | DeepSeek | https://platform.deepseek.com/api_keys |
| LLM (Mistral) | `MISTRAL_API_KEY` | Mistral | https://console.mistral.ai/api-keys |
| LLM (Together) | `TOGETHER_API_KEY` | Together AI | https://api.together.xyz/settings/api-keys |
| LLM (Fireworks) | `FIREWORKS_API_KEY` | Fireworks | https://fireworks.ai/account/api-keys |
| LLM (universell) | `LLM_API_KEY` | Beliebig | Überschreibt alle provider-spezifischen Keys |

> **Tipp:** Es wird nur **ein** LLM-Key benötigt — passend zum gewählten Provider.
> OpenRouter ist empfohlen, da es Zugang zu vielen Modellen über einen Key bietet.

{If the workflow uses tools that need API keys, add a second table:}

| Tool | Env-Variable | Beschreibung | Key besorgen |
|------|-------------|-------------|-------------|
| `web.search` (Premium) | `SEARCH_API_KEY` | Optional — DuckDuckGo funktioniert ohne Key | Abhängig vom Anbieter (Google, Bing, SearXNG) |
| `http.request` | `AUTH_TOKEN` | Nur wenn Ziel-API Authentifizierung braucht | Vom jeweiligen API-Anbieter |
| {custom_tool} | `{SECRET_NAME}` | {description} | {where to get it} |

{Only include tool rows that are actually used in this workflow. Omit the tool
table entirely if no tools need secrets.}

> **Secrets einrichten:**
>
> ```bash
> # Option 1: Environment-Variable setzen
> export OPENROUTER_API_KEY="sk-or-..."
>
> # Option 2: In secrets.yaml speichern (wird beim ersten `awp run` angeboten)
> cp secrets.yaml.example secrets.yaml
> # Datei editieren und Keys eintragen
>
> # Option 3: In ~/.awp/.env für alle Workflows global setzen
> echo 'OPENROUTER_API_KEY=sk-or-...' >> ~/.awp/.env
> ```

---

**IMPORTANT:** The API key table must be **specific** to this workflow. Do not
list providers that are irrelevant. If the workflow only uses web.search with
the free DuckDuckGo fallback, state that no tool secrets are required. Always
highlight which keys are **required** vs. **optional**.


## Templates

The `templates/` directory contains starter files for all workflow components:

| Template | Purpose |
|----------|---------|
| `workflow.awp.yaml` | Complete workflow manifest with all sections. |
| `agent.awp.yaml` | Minimal agent configuration. |
| `agent-full.awp.yaml` | Full-featured agent configuration with all options. |
| `agent.py` | Python agent class (platform-specific, see adapters/). |
| `SYSTEM_PROMPT.md` | System prompt with placeholders. |
| `00_INTRO.md` | Intro prompt with placeholders. |
| `output_schema.json` | Output JSON Schema template. |
| `output_schema_desc.json` | Field description template. |
| `mcp-tool.py` | Custom MCP tool template. |
| `project-skill.md` | Project-level skill template. |
| `codemode-skill.md` | Code Mode execution skill (auto-generated from tools). |
| `adapters/cloudflare/` | Cloudflare Workers project templates (wrangler.toml, src/). |

**Auto-generated files (not templates, always created):**

| File | Purpose |
|------|---------|
| `WORKFLOW.md` | Project-level overview with ASCII diagram and abstract-to-concrete description. Always generated at project root. |

## Extensions (Skill Inheritance)

The `extensions/` directory contains domain-specific customizations that
**extend** this base skill -- like subclass inheritance.  An extension can:

- Override defaults (model, compliance level, temperature)
- Add required agents (e.g., `risk_assessor` for financial workflows)
- Add required output fields (e.g., `data_sources` for every agent)
- Add domain-specific rules (F1, F2, ... or D1, D2, ...)
- Inject content into system prompts (prepend/append/replace)
- Include additional project-level skills
- Include additional custom MCP tools
- Set constraints (deny tools, require memory tiers, min compliance)

### How to Use an Extension

When the user requests a domain-specific workflow (e.g., "build a financial
analysis workflow"), load the appropriate extension alongside this base skill:

1. Load this file (`SKILL.md`) -- base rules and generation process
2. Load the adapter (`adapters/*.md`) -- platform-specific agent.py
3. Load the extension (`extensions/examples/*.md`) -- domain overrides
4. Merge: extension rules are **additive**, defaults are **overridden**

### Available Extensions

| Extension | Domain | Key Features |
|-----------|--------|-------------|
| `extensions/examples/financial.md` | Finance | Risk assessor agent, audit trail, compliance controls |
| `extensions/examples/devops.md` | DevOps | Safety checker agent, rollback plans, shell constraints |

See `extensions/README.md` for the full extension format and how to create
custom extensions.


## ClawHub Integration

This skill and all AWP extensions use ClawHub-compatible YAML frontmatter
and can be published directly to the ClawHub registry.

### Publishing this skill

```bash
clawhub publish skill/
```

### Publishing a generated workflow as a ClawHub skill

After generating a workflow, add a `SKILL.md` with ClawHub frontmatter
at the workflow root and publish:

```bash
awp clawhub init my-workflow/    # generates SKILL.md from workflow.awp.yaml
clawhub publish my-workflow/
```

See `adapters/clawhub.md` for the complete ClawHub integration guide including
packaging workflows, publishing extensions, and discovery tag conventions.


## Adapters

| Adapter | Purpose |
|---------|---------|
| `adapters/standalone.md` | Generate `agent.py` for the AWP standalone runtime (Python) |
| `adapters/cloudflare-dynamic-workers.md` | Generate TypeScript project for Cloudflare Workers deployment |
| `adapters/clawhub.md` | Publish AWP skills and workflows to ClawHub registry |

**Adapter selection:** Choose based on the user's answer to question 9.1 (target platform).
If Cloudflare is selected, read `adapters/cloudflare-dynamic-workers.md` for the full
generation instructions and use the templates in `templates/adapters/cloudflare/`.

Third-party platforms can add their own adapters following the same pattern.


## References

The `references/` directory contains condensed documentation for AI context:

| Reference | Purpose |
|-----------|---------|
| `spec-summary.md` | Condensed AWP specification (~2000 words). |
| `compliance-levels.md` | Quick reference for L0-L5 compliance. |
| `validation-rules.md` | R1-R24 checklist format. |
| `tools-reference.md` | Built-in MCP tool catalog. |
| `architecture.md` | Architecture overview. |
