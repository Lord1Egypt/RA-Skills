# SKILL: skill-creator

## Description

The foundational meta-skill that architects and generates production-grade agent skills from natural language. This is the factory floor — every skill in the Acrid ecosystem is born here. It doesn't just scaffold files; it thinks through design, enforces quality gates, generates battle-tested logic, and outputs skills that work on first run.

## Usage

Invoke this skill when:
- You need to create a new capability, tool integration, or automation
- You're converting a manual workflow into a repeatable skill
- You want to prototype a skill idea rapidly with full documentation
- You need to refactor or rebuild an existing skill from scratch

**Trigger phrases:** "Create a skill...", "Build me a skill...", "I need a skill that...", "Scaffold a new skill for..."

## Inputs

| Parameter | Required | Format | Description |
|-----------|----------|--------|-------------|
| `name` | Yes | kebab-case | Skill identifier (e.g., `stock-checker`, `deploy-monitor`) |
| `description` | Yes | Natural language | What the skill does, in detail |
| `requirements` | No | Natural language | Tools, APIs, constraints, languages, auth needs |
| `outputs` | No | Natural language | What the skill should return (defaults to structured text) |
| `complexity` | No | `simple` \| `standard` \| `advanced` | Determines scaffold depth (default: `standard`) |

## Steps

### Phase 1: Intelligence Gathering

1. **Parse the request** — Extract:
   - Core purpose (single sentence, verb-first: "Fetches...", "Monitors...", "Generates...")
   - Required external APIs or services
   - Required tools (Bash, WebFetch, WebSearch, Read, Write, Grep, Glob, etc.)
   - Input parameters with types and validation rules
   - Expected output format (JSON, markdown, plain text, file)
   - Error scenarios (API down, bad input, rate limits, auth failure, empty results)
   - Edge cases specific to the domain

2. **Determine complexity tier**:
   - **Simple**: Single tool, no external APIs, <20 lines of logic (e.g., file formatter)
   - **Standard**: 1-2 tools, may call external APIs, needs error handling (e.g., stock checker)
   - **Advanced**: Multiple tools, chained API calls, stateful logic, helper scripts required (e.g., deploy pipeline)

3. **Identify the execution model**:
   - **Direct**: Skill logic runs entirely within SKILL.md steps (preferred for simple/standard)
   - **Scripted**: Complex logic lives in `src/` scripts, SKILL.md orchestrates (required for advanced)
   - **Hybrid**: SKILL.md handles orchestration, delegates specific computations to scripts

### Phase 2: Architecture

4. **Design the skill contract**:
   - Define exact input schema with types, defaults, and validation
   - Define exact output schema — what does success look like?
   - Define error responses — what does each failure mode return?
   - Map the dependency chain (what calls what, in what order)

5. **Scaffold the directory**:

   For **simple** skills:
   ```
   skills/<name>/
     SKILL.md
     README.md
   ```

   For **standard** skills:
   ```
   skills/<name>/
     SKILL.md
     README.md
     src/           # Only if computation is complex
   ```

   For **advanced** skills:
   ```
   skills/<name>/
     SKILL.md
     README.md
     src/
       main.py|js   # Core logic
       utils.py|js  # Shared helpers (only if genuinely needed)
     config/
       defaults.json
   ```

### Phase 3: Generation

6. **Generate SKILL.md** — The skill definition must include ALL of these sections:

   ```markdown
   # SKILL: <name>

   ## Description
   <Single paragraph. First sentence is the hook — what it does in <15 words.
   Second sentence adds context. Third sentence covers key differentiator.>

   ## Usage
   <When to invoke. Include 2-3 specific trigger phrases.>

   ## Inputs
   <Table format with: Parameter | Required | Type | Default | Description>
   <Include validation rules inline>

   ## Outputs
   <What the skill returns on success. Include format specification.>

   ## Steps
   <Numbered, imperative steps. Each step must be:
   - Actionable (starts with a verb)
   - Atomic (does one thing)
   - Error-aware (includes failure handling where relevant)
   - Tool-specific (names the exact tool to use when applicable)>

   ## Error Handling
   <Explicit failure modes and recovery actions:
   - What to do when an API is unreachable
   - What to do with malformed input
   - What to do when results are empty
   - Retry logic if applicable>
   ```

   **SKILL.md generation rules:**
   - Steps MUST be deterministic — no ambiguity in what the agent does
   - Every external call MUST have a failure path
   - Steps should reference specific tools by name (WebFetch, Bash, Grep, etc.)
   - Include concrete examples of expected input/output in the steps where helpful
   - Never use vague instructions like "process the data" — specify HOW
   - If a step involves parsing, specify the exact format and extraction method
   - Rate limiting: if the skill calls external APIs, include a note about respecting rate limits

7. **Generate README.md**:

   ```markdown
   # <Skill Name (Title Case)>

   <One-line description>

   ## Quick Start
   <Minimal trigger example>

   ## Parameters
   <Full parameter docs with examples>

   ## Example Usage
   <2-3 real-world invocation examples with expected outputs>

   ## Setup
   <Environment variables, API keys, dependencies — only if needed>

   ## How It Works
   <Brief technical explanation of the skill's approach>

   ## Limitations
   <Honest about what it can't do>
   ```

8. **Generate helper scripts** (if complexity requires):

   **Python scripts must:**
   - Use `argparse` for CLI arguments
   - Output JSON to stdout (parseable by the agent)
   - Include a `if __name__ == "__main__"` guard
   - Handle exceptions with meaningful error messages in JSON format: `{"error": "...", "code": "..."}`
   - Use type hints
   - Include a docstring

   **Node.js scripts must:**
   - Parse args from `process.argv` or use a minimal arg parser
   - Output JSON to stdout
   - Handle errors with try/catch, output: `{"error": "...", "code": "..."}`
   - Use strict mode

### Phase 4: Quality Gates

9. **Run the Acrid Quality Checklist** — Every generated skill must pass ALL gates:

   | Gate | Check | Fail Action |
   |------|-------|-------------|
   | **Atomic** | Does it do exactly ONE thing? | Split into multiple skills |
   | **Named** | Is the name self-documenting? Does `<name>` tell you what it does? | Rename |
   | **Inputs Valid** | Are all inputs typed with clear validation rules? | Add missing validation |
   | **Outputs Defined** | Is the output format explicitly documented? | Add output spec |
   | **Error-Proof** | Does every external call have a failure path? | Add error handling |
   | **Documented** | Does README.md have Quick Start + Examples? | Flesh out docs |
   | **Deterministic** | Given the same input, does it always produce the same flow? | Remove ambiguity |
   | **No Dead Code** | Are all generated files actually used? | Remove unused files |
   | **Dependency-Light** | Does it minimize external dependencies? | Simplify |
   | **First-Run Ready** | Can someone use this skill with zero setup beyond what's documented? | Fix setup docs |

10. **Final review** — Read through the complete generated skill one more time. Ask:
    - Would this work if I ran it right now?
    - Is there anything I'd need to guess or assume?
    - Are the steps clear enough that a different agent could execute them?
    - If any answer is "no", fix it before delivering.

### Phase 5: Delivery

11. **Write all files** to the target directory using the Write tool.

12. **Report to user** with:
    - Skill name and location
    - Quick summary of what was generated
    - Any setup steps required (API keys, env vars)
    - A ready-to-use invocation example

## Error Handling

| Scenario | Action |
|----------|--------|
| Name is not kebab-case | Auto-convert and warn user |
| Description is vague (<10 words) | Ask for clarification before proceeding |
| Requested API has no free tier | Warn user, suggest alternatives, proceed if confirmed |
| Complexity mismatch (user says simple but needs advanced) | Override to correct tier, explain why |
| Generated skill fails quality gate | Fix automatically, do not deliver broken skills |

## Anti-Patterns — Do NOT Generate Skills That:

- Have steps like "analyze the data" without specifying HOW
- Depend on tools not available to the agent
- Require manual intervention mid-execution (unless explicitly designed as interactive)
- Have undocumented environment variables or secrets
- Contain placeholder logic ("TODO: implement this")
- Over-engineer with abstractions for single-use operations
- Include unnecessary comments or boilerplate

## Examples

**Input:**
```
name: stock-checker
description: Fetches the current price of a stock by ticker symbol using a free API
requirements: Must use a free API, return price in USD
```

**Output:** See `examples/stock-checker/` for the complete generated skill.
