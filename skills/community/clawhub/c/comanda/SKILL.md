---
name: comanda
version: 1.1.0
description: Generate, visualize, and execute declarative AI pipelines using the comanda CLI. Use when creating LLM workflows from natural language, viewing workflow charts, editing YAML workflow files, or processing/running comanda workflows. Supports multi-model orchestration (OpenAI, Anthropic, Google, Ollama, Claude Code, Gemini CLI, Codex).
homepage: https://comanda.sh
repository: https://github.com/kris-hansen/comanda
---

# Comanda

Comanda defines and runs LLM workflows as YAML pipelines. Use it to generate workflows, inspect charts, edit workflow YAML, run workflows, improve workflows, orchestrate multiple models, and build agentic loops.

## Core commands

```bash
comanda generate workflow.yaml "Create a workflow that summarizes Markdown files"
comanda chart workflow.yaml
comanda process workflow.yaml
cat input.txt | comanda process workflow.yaml
comanda improve workflow.yaml "Make it output risks and action items"
comanda configure
comanda version
```

Useful execution flags:

```bash
comanda process workflow.yaml --runtime-dir ./data --vars name=value --debug
```

## Workflow editing rules

For detailed YAML patterns, read `references/WORKFLOW-SPEC.md` before creating or changing non-trivial workflows.

Minimal step:

```yaml
summarize:
  input: STDIN
  model: gpt-4o
  action: "Summarize the input."
  output: STDOUT
```

### Critical data-flow rule

For ordinary step-to-step data flow, use only:

1. `output: STDOUT` followed by next step `input: STDIN`
2. explicit files: `output: ./file.json` followed by `input: ./file.json`

Do **not** use `$VARIABLE` syntax for ordinary step chaining. `as $var` is only input aliasing inside the same step's `action` prompt.

```yaml
# Good: same-step input aliasing
compare:
  input: old.md as $baseline
  model: gpt-4o
  action: "Compare the current input with $baseline."
  output: STDOUT

# Bad: not valid step-to-step flow
step1:
  output: STDOUT as $data
step2:
  input: $data
```

For parallel fan-in, write branch outputs to files and combine from those files. For defer/branching, have the prior step emit JSON with `step_name` and `input`; the selected branch reads `STDIN`.

## Tool steps

Use shell tools only in trusted workflows. Prefer `tool:` allowlists; `tool_config:` examples in older docs are stale for step-level allowlists.

```yaml
list_go_files:
  input: "tool: find . -name '*.go' -type f"
  model: NA
  tool:
    allowlist: [find]
    timeout: 30
  action: NA
  output: STDOUT
```

## Agentic workflows

Default to linear workflows. Use `agentic_loop` only when work truly needs iteration until quality/completion. Prefer file outputs such as `.comanda/result.md`, grant explicit allowed paths, and tell the agent to read/update existing files across iterations. Use `comanda loop status/resume/cancel/clean` for long-running loops.

Loop-specific `input_state`/`output_state` variables are valid only inside agentic-loop/multi-loop orchestration; they are not ordinary workflow step variables.

## Models and examples

Common model IDs include `gpt-4o`, `claude-sonnet-4-20250514`, `gemini-pro`, `grok-4-1-fast-reasoning`, `grok-4-1-fast-non-reasoning`, `ollama/<model>`, `claude-code`, `gemini-cli`, and `openai-codex`. Run `comanda configure` for API keys.

Examples live in `~/clawd/comanda/examples/`:
- `parallel-processing/` — file-based parallel fan-in
- `tool-use/` and `security/` — shell tool input/output patterns
- `agentic-loop/` — iterative and multi-loop workflows
- `codebase-index/` — index capture and reuse
- `file-processing/` — chunking, batching, wildcards
- `model-examples/` — provider/model examples

## Troubleshooting

- Validation/structure: `comanda chart workflow.yaml --verbose`
- Execution details: `comanda process workflow.yaml --debug`
- Missing keys: `comanda configure`
- Blocked tool command: add the command to the step's `tool.allowlist`
