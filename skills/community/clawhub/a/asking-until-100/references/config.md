# Config

## Discovery

Look for config in this order:

1. explicit user instructions in the current request
2. `.asking-until-100.yaml` in the repo or workspace root
3. a bundled profile from `assets/`
4. built-in defaults

Repo-local and explicit files may be partial overrides. Bundled profiles should remain complete.

## Core fields

```yaml
version: 1
model_assumptions:
  family: gpt-5.4
  reasoning_effort: xhigh
behavior:
  asking_intensity: 75
  target_readiness: 100
  default_rigor: high
  max_initial_questions: 6
  max_follow_up_questions: 4
  execution_gate: block
  report_basis: repo_plus_prompt
  repo_scan_max_depth: 2
  include_answer_options: true
  thought_provoking_ratio: 0.25
  report_for_high_rigor_coding: true
task_overrides:
  coding:
    rigor: highest
    report_trigger: true
    required_dimensions: [goal, repo_state, architecture, product_behavior, environment, interfaces, constraints, timeline, success_criteria]
```

## Asking intensity mapping

`asking_intensity` is optional and maps to these defaults when the same YAML layer does not set the
behavior fields explicitly:

- `0-24` => `target_readiness=70`, `max_initial_questions=2`, `max_follow_up_questions=1`,
  `min_rigor=low`
- `25-49` => `85`, `3`, `1`, `medium`
- `50-74` => `95`, `5`, `2`, `high`
- `75-100` => `100`, `6`, `4`, `highest`

Explicit YAML values override the values derived from `asking_intensity`.

## Behavior notes

- `execution_gate` must be `block`, `assumptions`, or `ask`.
- `report_basis` must be `repo_plus_prompt`, `prompt_only`, or `template_first`.
- `repo_scan_max_depth` must be a positive integer.
- `model_assumptions` are tuning assumptions, not enforced runtime settings.
- Bundled profiles are pinned to `gpt-5.4` and `xhigh`.

## Canonical values

- Task types: `coding`, `build`, `architecture`, `debugging`, `discovery`, `general`
- Readiness dimensions: `goal`, `success_criteria`, `repo_state`, `architecture`,
  `product_behavior`, `environment`, `interfaces`, `constraints`, `runtime`,
  `package_manager`, `deploy_target`, `ci_provider`, `rollback`, `logs`, `evidence`,
  `boundaries`, `dependencies`, `tradeoffs`, `data_flow`, `scale`, `secrets`, `timeline`

Unknown bundled profile names or paths are load errors and should not fall back silently.
