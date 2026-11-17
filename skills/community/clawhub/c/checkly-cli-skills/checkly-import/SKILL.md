---
name: checkly-import
description: Import existing Checkly resources into Monitoring as Code with the plan, apply, commit, and cancel lifecycle. Use when migrating UI-managed checks to code, generating Checkly resource code, safely reserving imported resources, or completing an import after merge. Triggers on import checks, migrate to code, import plan, import apply, import commit, import cancel, checkly import.
---

# checkly import

Import existing Checkly resources into code through an explicit plan → apply → commit lifecycle.

## Safety model

The stages have different effects:

1. **Preview** generates a code preview without creating an import plan.
2. **Plan** generates code and creates a plan, but does not link live resources yet.
3. **Apply** links existing resources to the generated code in a pending state. Deployments can then modify those resources, but pending-import safeguards prevent absent resources from being deleted.
4. **Commit** permanently places the imported resources under normal Checkly CLI project management. The plan can no longer be canceled, and a later deploy can delete resources removed from code.
5. **Cancel** removes an uncommitted plan and its pending links. It does not undo live-resource changes made by earlier deploys.

Do not deploy generated import code before applying its plan: that can create duplicate resources and block the import.

## Recommended agent/PR workflow

### 1. Preview or create a plan

```bash
# Inspect generated code without creating a plan
npx checkly import --preview

# Create a real import plan and write generated files under __checks__
npx checkly import plan

# Use another generated-code root when required
npx checkly import plan --root src/__checks__
```

Both `npx checkly import` and `npx checkly import plan` expose the plan command surface. By default, all importable resources are considered; pass only documented resource selectors when narrowing the import.

### 2. Review generated code before linking anything

```bash
git status --short
git diff --check
git diff
npx checkly test
```

Confirm that the generated project contains every resource that future deployments must preserve. Do not commit secrets generated from environment-backed or locked values.

### 3. Apply a specific plan but leave it pending

```bash
npx checkly import apply --plan-id <plan-id> --no-commit
```

`--plan-id` avoids interactive or implicit selection. `--no-commit` applies only and skips the trailing interactive commit prompt. Non-interactive agent/CI sessions also leave the plan pending automatically and print the exact later commit command.

If `--plan-id` is omitted:

- one candidate plan is selected automatically in non-interactive mode;
- multiple candidates cause a non-zero error that lists plan IDs and asks for `--plan-id`;
- no candidate is a successful no-op with an informational message.

Applying reserves the resources and changes live linkage state. Get explicit authorization before applying, then verify the CLI-reported plan ID and generated files.

### 4. Open and merge the generated-code PR

Keep the import plan pending while the generated code is under review. This protects against another deployment omitting the imported resources before the code reaches the branch used for deployments.

### 5. Preview and commit only after the code is durable

```bash
# Preview the permanent action
npx checkly import commit --plan-id <plan-id> --dry-run

# Request confirmation; in agent mode this returns a confirmation envelope
npx checkly import commit --plan-id <plan-id>
```

Commit is permanent even though it does not directly delete resources. After commit, the plan cannot be canceled and normal deploy semantics apply.

## Confirmation protocol for commit and cancel

In agent mode, `import commit` and `import cancel` without `--force` return exit code 2 and JSON with:

- `status: "confirmation_required"`
- a human-readable `changes` array
- a `confirmCommand`

Present `changes` to the user and run `confirmCommand` verbatim only after explicit approval. Do not append `--force` yourself or edit flags in the returned command.

When the CLI auto-resolves a single plan, it pins that plan into the confirmation command, for example:

```text
checkly import commit --plan-id="<resolved-id>" --force
```

The added `--plan-id` is deliberate: it guarantees that the approved execution targets the same plan that was previewed.

## Command reference

### Create or preview a plan

```bash
npx checkly import [RESOURCE...]
npx checkly import plan [RESOURCE...]
```

| Flag | Meaning |
|------|---------|
| `--preview` | Preview generated code without creating an import plan. |
| `--root <path>` | Generated-code root; defaults to `__checks__`. |
| `--config, -c <path>` | Checkly configuration file. |

### Apply

```bash
npx checkly import apply --plan-id <id> --no-commit
```

| Flag | Meaning |
|------|---------|
| `--plan-id <id>` | Target a specific unapplied plan. |
| `--no-commit` | Apply only and leave the plan pending. |
| `--config, -c <path>` | Checkly configuration file. |

### Commit

```bash
npx checkly import commit --plan-id <id> --dry-run
npx checkly import commit --plan-id <id>
```

| Flag | Meaning |
|------|---------|
| `--plan-id <id>` | Target a specific applied, uncommitted plan. |
| `--dry-run` | Preview without committing or prompting. |
| `--force, -f` | Skip confirmation; use only through an approved `confirmCommand` or explicitly approved automation. |
| `--config, -c <path>` | Checkly configuration file. |

### Cancel

```bash
# Preview one cancellation
npx checkly import cancel --plan-id <id> --dry-run

# Request confirmation for one plan
npx checkly import cancel --plan-id <id>

# Preview every currently uncommitted plan
npx checkly import cancel --all --dry-run
```

| Flag | Meaning |
|------|---------|
| `--plan-id <id>` | Target one uncommitted plan. |
| `--all` | Target all currently uncommitted plans. |
| `--dry-run` | Preview without canceling or prompting. |
| `--force, -f` | Skip confirmation; use only after explicit approval. |
| `--config, -c <path>` | Checkly configuration file. |

`--all` and `--plan-id` are mutually exclusive. `--all` intentionally re-resolves the set of uncommitted plans at execution time, so repeat the dry run and review if the set may have changed.

## Failure handling

### Explicit plan ID is missing

An unsatisfied `--plan-id` exits non-zero. Re-check the ID and plan stage; do not fall back to an implicit candidate.

### Multiple plans are available

Re-run with one of the candidate IDs:

```bash
npx checkly import apply --plan-id <id> --no-commit
npx checkly import commit --plan-id <id> --dry-run
npx checkly import cancel --plan-id <id> --dry-run
```

### Generated code conflicts with existing files

Commit or stash intentional local work first, regenerate the plan in a clean branch/worktree, and review every diff. Cancel the uncommitted plan if the generated output should be abandoned.

### A deploy happened after apply

Canceling removes the pending links but does not roll back changes already deployed to live resources. Inspect the deployed state and use an explicit corrective deployment only after review.

## Related skills

- See `checkly-deploy` for preview and deployment deletion safety.
- See `checkly-test` to validate generated checks.
- See `checkly-checks` and `checkly-monitors` for construct-specific review guidance.
