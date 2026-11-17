# Contributing

Thank you for improving Convbox-DiagClaw.

## Before Opening A Pull Request

1. Open or reference an issue for behavior changes.
2. Keep one scenario or concern per pull request.
3. Never include customer data, API responses, account IDs, or credentials.
4. Confirm that the change follows the metric caliber in `functions.md` and
   the API contract in `access.yaml`.
5. Add or update a plan when analysis behavior changes.

## Development Setup

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python utilities/config-health-check/config_health_check.py --config-only
```

Use an isolated test account for network checks. Do not run tests against a
customer account unless you are authorized to access it.

## Change Rules

- `SKILL.md`: routing, global behavior, prerequisites, and safety boundaries.
- `functions.md`: interface semantics, scenario catalog, tier, and readiness.
- `access.yaml`: API request/response definitions and synthetic examples only.
- `plans/*.md`: one atomic diagnostic workflow per file.
- `utilities/`: deterministic helpers; utilities must not print credentials.

Do not duplicate report cadence or role rules inside plans when they belong in
`functions.md`.

## Required Verification

```bash
python -m py_compile utilities/config-health-check/config_health_check.py
python utilities/config-health-check/config_health_check.py --config-only
```

For API-contract changes, also run an authorized health check and report only
the pass/fail summary in the pull request. Redact all returned business data.

## Pull Request Description

Include:

- Problem and intended behavior
- Files and scenarios changed
- Data-caliber or API-contract impact
- Verification performed
- Security and privacy impact
- Rollback approach for contract changes

By contributing, you agree that your contribution is licensed under MIT-0.
