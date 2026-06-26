# Comanda Workflow Spec

Detailed YAML patterns for Comanda workflows. Validate workflows with `comanda chart <file.yaml>` before running; execute with `comanda process <file.yaml>`.

## Table of Contents

- [Standard steps](#standard-steps)
- [Data flow](#data-flow)
- [Tool steps](#tool-steps)
- [Parallel fan-out/fan-in](#parallel-fan-outfan-in)
- [Defer/branching](#deferbranching)
- [Meta steps](#meta-steps)
- [Chunking and batching](#chunking-and-batching)
- [Codebase indexes](#codebase-indexes)
- [Agentic loops](#agentic-loops)
- [Common commands](#common-commands)

## Standard steps

```yaml
step_name:
  input: STDIN        # STDIN, NA, file path, URL, tool command, or input list/map
  model: gpt-4o      # or claude-*, gemini-*, grok-*, ollama/*, claude-code, etc.
  action: "Instruction for the model"
  output: STDOUT     # STDOUT, file path, or tool command
```

Use `NA` when a required field has no useful value, especially for tool-only pass-through steps.

Inputs may be a scalar, list, or structured map:

```yaml
compare:
  input:
    - ./old.md as $old_doc
    - ./new.md as $new_doc
  model: gpt-4o
  action: "Compare $old_doc and $new_doc. Return the important differences."
  output: STDOUT

scrape:
  input:
    url: https://example.com
    scrape_config:
      allowed_domains: [example.com]
      extract: text
  model: gpt-4o
  action: "Summarize the page."
  output: STDOUT
```

`as $var` aliases inputs inside the same step's `action` prompt only.

## Data flow

Ordinary workflow steps pass data in only two supported ways:

1. **Implicit STDIN chain**: `output: STDOUT` from one step becomes `input: STDIN` for the next sequential step.
2. **Explicit files**: write `output: ./file.json`, then later use `input: ./file.json`.

```yaml
extract:
  input: ./source.pdf
  model: gpt-4o
  action: "Extract key facts as JSON."
  output: STDOUT

summarize:
  input: STDIN
  model: claude-sonnet-4-20250514
  action: "Summarize the JSON for an executive reader."
  output: STDOUT
```

```yaml
extract:
  input: ./source.pdf
  model: gpt-4o
  action: "Extract key facts as JSON."
  output: ./facts.json

summarize:
  input: ./facts.json
  model: claude-sonnet-4-20250514
  action: "Summarize the JSON for an executive reader."
  output: ./summary.md
```

Do **not** use `$VARIABLE` for ordinary step-to-step data flow. `output: STDOUT as $data`, `output: $data`, and `input: $data` are not valid general chaining patterns. Use STDIN or files.

## Tool steps

Shell tools can be used as input or output. Commands are security-filtered; allowlist commands explicitly when needed.

```yaml
list_go_files:
  input: "tool: find . -name '*.go' -type f"
  model: NA
  tool:
    allowlist: [find]
    timeout: 30
  action: NA
  output: STDOUT

extract_names:
  input: "tool: jq -r '.[].name' ./deps.json"
  model: NA
  tool:
    allowlist: [jq]
    timeout: 30
  action: NA
  output: STDOUT
```

Tool outputs can also run commands, but they receive the step response as stdin. Use this after model steps or commands that produce stdout:

```yaml
filter_errors:
  input: ./app.log
  model: gpt-4o
  action: "Extract log lines that may indicate errors."
  tool:
    allowlist: [grep]
  output: "STDOUT|grep -i error"
```

Prefer read-only commands. Avoid untrusted workflows that execute shell commands.

## Parallel fan-out/fan-in

Use `parallel-process:` for concurrent branches. Persist each branch to a file, then combine from those files.

```yaml
parallel-process:
  security_review:
    input: ./design.md
    model: claude-sonnet-4-20250514
    action: "Review for security risks."
    output: ./security.md

  performance_review:
    input: ./design.md
    model: gpt-4o
    action: "Review for performance risks."
    output: ./performance.md

combine:
  input:
    - ./security.md
    - ./performance.md
  model: gpt-4o
  action: "Synthesize both reviews into prioritized recommendations."
  output: ./review.md
```

Do not fan in with `$RESULT_A`/`$RESULT_B`; use files.

## Defer/branching

`defer:` defines named branches. The previous step emits JSON selecting the branch and payload:

```json
{"step_name":"handle_bug","input":"the payload for that branch"}
```

The selected branch receives that payload as `STDIN`.

```yaml
classify:
  input: STDIN
  model: gpt-4o
  action: >
    Classify this request. Output only JSON like
    {"step_name":"handle_bug","input":"<original request plus useful context>"}
    where step_name is one of: handle_bug, handle_feature, handle_question.
  output: STDOUT

defer:
  handle_bug:
    input: STDIN
    model: claude-sonnet-4-20250514
    action: "Triage this bug report and propose next steps."
    output: STDOUT

  handle_feature:
    input: STDIN
    model: claude-sonnet-4-20250514
    action: "Turn this feature request into an implementation plan."
    output: STDOUT

  handle_question:
    input: STDIN
    model: gpt-4o
    action: "Answer the question clearly."
    output: STDOUT
```

## Meta steps

Generate a workflow, then process it:

```yaml
create_workflow:
  input: NA
  generate:
    action: "Create a workflow that summarizes Markdown files."
    output: ./generated.yaml

run_workflow:
  input: NA
  process:
    workflow_file: ./generated.yaml
```

The CLI can also do this directly:

```bash
comanda generate generated.yaml "Create a workflow that summarizes Markdown files"
comanda process generated.yaml
comanda improve generated.yaml "Make the summary include risks and action items"
```

## Chunking and batching

Use chunking for large inputs. `{{ current_chunk }}` is available in chunk prompts; output paths may use `{{ chunk_index }}` in chunked workflows.

```yaml
analyze_chunks:
  input: ./large.log
  model: gpt-4o-mini
  chunk:
    by: lines
    size: 200
    overlap: 20
    max_chunks: 10
  batch_mode: individual
  action: "Summarize this chunk: {{ current_chunk }}"
  output: ./chunks/chunk-{{ chunk_index }}.md
```

## Codebase indexes

Use codebase index steps when a workflow needs a compact, reusable view of a repository.

```yaml
index_project:
  step_type: codebase-index
  codebase_index:
    root: ./src
  output:
    store: project-index
    path: ./project-index.json
    encrypt: false
  expose:
    workflow_variable: true
  max_output_kb: 512

analyze:
  input: STDIN
  model: claude-sonnet-4-20250514
  action: |
    Use the codebase index at {{ env "PROJECT_INDEX" }} to identify risky modules.
  output: ./analysis.md
```

Manage registered indexes with `comanda index capture/list/show/diff/update/remove`.

## Agentic loops

Default to linear workflows. Use agentic loops only when the task truly needs iteration until a quality condition is met or the agent decides it is done.

Prefer file outputs for agentic loops so work survives long runs and resumes. Give the agent explicit read/write instructions and allowed paths.

```yaml
iterative_writer:
  input: ./requirements.md
  model: claude-code
  action: |
    Iteratively draft and improve the document. Read ./requirements.md and update
    .comanda/draft.md each iteration. When complete, say DONE.
  output: .comanda/draft.md
  agentic_loop:
    max_iterations: 5
    exit_condition: pattern_match
    exit_pattern: DONE
    allowed_paths:
      - .comanda/draft.md
```

Loop orchestration has loop-specific state fields such as `input_state` and `output_state`. Those `$STATE`-style names are for agentic-loop/multi-loop orchestration only; do not treat them as ordinary workflow step variables.

## Common commands

```bash
comanda version
comanda configure
comanda chart workflow.yaml
comanda process workflow.yaml
cat input.txt | comanda process workflow.yaml
comanda process workflow.yaml --runtime-dir ./data --vars name=value
comanda loop status
comanda loop resume <run-id>
```
