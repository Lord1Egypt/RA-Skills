# YAML Config Specification

Complete reference for the mlflow-skills test configuration YAML format.

## Full Config Template

```yaml
name: "{skill-name}-test"           # Required: test run name
project_dir: {skill}-workdir        # Required: temp project directory name
project_root: ../..                 # Optional: base dir for resolving skills/judges

skills:                             # Required: list of skill directory names
  - {skill-name}

prompt: "Your test prompt here"     # Required: prompt sent to Claude Code
test_scope: all                     # Optional: default scope filter (default: "all")

timeout_seconds: 900                # Optional: Claude Code timeout (default: 900)
verification_timeout: 300           # Optional: judge verification timeout (default: 300)
allowed_tools: "Bash,Read,Write,Edit,Grep,Glob,WebFetch"  # Optional: tool allowlist

mlflow_port: 5000                   # Optional: local MLflow server port
tracking_uri: null                  # Optional: external MLflow/Databricks URI

test_runs_dir: /tmp                 # Optional: parent dir for temp work dirs
keep_workdir: true                  # Optional: keep work dir after test

# ==============================================================
# Judge Definitions
#
# scope values:
#   all        — runs in all test scenarios
#   {scope1}   — only when test_scope={scope1}
#   {scope2}   — only when test_scope={scope2}
# ==============================================================
judge_definitions:

  - name: example-check
    scope: all
    question: >
      Check that the agent did X. Look in the trace for Y.
      Answer 'yes' if Z is true.

environment:
  OPENAI_API_KEY: ""
  OPENAI_BASE_URL: ""
```

## Field Reference

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `name` | yes | — | Test run name |
| `project_dir` | yes | — | Temp project directory name |
| `skills` | yes | — | List of skill directory names to install |
| `prompt` | yes | — | Prompt sent to Claude Code |
| `project_root` | no | repo root | Base directory for resolving paths (relative to YAML) |
| `test_scope` | no | `all` | Scope filter — controls which judges run |
| `timeout_seconds` | no | `900` | Claude Code execution timeout |
| `verification_timeout` | no | `300` | Judge verification timeout |
| `allowed_tools` | no | `Bash,Read,...` | Comma-separated tool allowlist |
| `mlflow_port` | no | `5000` | Local MLflow server port |
| `tracking_uri` | no | none | External MLflow tracking URI |
| `test_runs_dir` | no | `/tmp` | Parent dir for temp work directories |
| `keep_workdir` | no | `true` | Keep work directory after test |
| `judge_definitions` | no | `[]` | List of judge definition dicts |
| `environment` | no | `{}` | Extra env vars (empty values won't override existing) |

## Judge Definition Structure

Each entry in `judge_definitions`:

```yaml
- name: kebab-case-name      # Required: unique scorer name
  scope: all                  # Optional: "all" (default), or custom scope string
  question: >                 # Required: yes/no question for the LLM judge
    Full question text...
```

## Scope Filtering Logic

```
test_scope = "checklist"

Judge scope: "all"       → RUNS    (always runs)
Judge scope: "checklist" → RUNS    (matches test_scope)
Judge scope: "assessment"→ SKIPPED (doesn't match)
```

## CLI Override

```bash
python test_skill.py config.yaml test_scope=assessment prompt="New prompt here"
```
