# Project initialization

Use this workflow when creating a project. Existing projects do not need setup
configuration to pass an audit and must not be bootstrapped again. The
questionnaire records project intent and infrastructure choices; it does not
introduce requirement, task, change, baseline or milestone lifecycle states.

## Agent interview

Use known answers from the current conversation and ask only for material missing
information, in small groups. Resolve these topics before provisioning:

1. Objective, deliverables in and out of scope, title, slug, target directory,
   archetype and any additional engineering domains.
2. Responsible owner/role labels, technical and cost constraints, schedule,
   security/safety/regulatory expectations, milestone targets and acceptance intent.
3. Canonical Git provider, API host/scheme, repository namespace, visibility,
   branch, Git transport and any SSH alias/port. Private visibility is the default.
4. Optional complementary Drive folder, credential references, existing CI runner
   tags and planned test commands. Git remains canonical engineering storage.
5. Whether delegation is available, agent labels, roles, capabilities, worker
   labels, writable paths, maximum simultaneous tasks (1–3), retry bound, and
   review policy. Labels are configurable and do not prove runtime availability.

Keep personal contact information out of shared configuration. Never ask the user
to paste a token, password or private key. Use `env:VARIABLE` or `keychain:item`
references. Authentication stays in the provider CLI or secret store. Setup
preserves reference labels but never reads or exports their secret values.

Use the user's language for the interview. Record new engineering content in
English. The CLI questionnaire is English. It accepts semicolon-separated lists
and supports a partial `--seed` JSON to avoid repeating known answers.

## Prepare and review

From the installed skill directory:

```sh
python3 scripts/project_setup.py --output /path/to/setup.json
# With already-known context:
python3 scripts/project_setup.py --seed /path/to/known-answers.json --output /path/to/setup.json
# Read-only validation and resolved plan:
python3 scripts/bootstrap_project.py --config /path/to/setup.json --dry-run
```

The output includes the complete configuration, exact resolved local destination,
remote effects and an `approval_sha256`. Relative project paths resolve against
the setup JSON's directory, consistently across review and execution. The
questionnaire refuses to overwrite an existing output. Review it with
`project_setup.py --config FILE` or edit a copy and validate again.

Present the resolved plan to the user before creating or pushing a remote. If the
user has already authorized these exact choices, use that authorization rather
than asking again. The execution assertion is tied to the resolved configuration:

```sh
python3 scripts/bootstrap_project.py --config /path/to/setup.json --preflight-only
python3 scripts/bootstrap_project.py --config /path/to/setup.json --approve-config REVIEWED_SHA256
```

The digest detects changes to a reviewed plan; it is not an authentication or
signature mechanism. Any changed configuration must be reviewed again. Never
auto-approve a digest merely because the script printed it.

Dry run performs schema validation only. Preflight checks templates, configured
global Git identity, provider authentication/API access and SSH transport when selected;
it does not create the remote or push. A configured Drive URL, runner label or
worker label is not a verified connection. Check the relevant service explicitly
when needed and report unchecked infrastructure as unchecked. CI runner tags are
applied to generated GitLab jobs; no runner is installed or registered. Planned
test commands are recorded, not executed or injected into CI.

## Configuration contract

The version 1 JSON has four root keys. Unknown fields, malformed values,
credential-bearing URLs and common token formats are rejected.

| Section | Required fields | Optional fields / defaults |
|---|---|---|
| Root | `schema_version: 1`, `project`, `infrastructure`, `delegation` | None |
| `project` | `title`, `slug`, `path`, `archetype`, `objective`, `in_scope` (list), `owners` (role-label list) | `add_domains`, `out_of_scope`, `constraints`, `milestones`: lists |
| `infrastructure` | `git_backend` (`github`/`gitlab`), `repository` | `host`: provider default; `scheme`/`protocol`: `https`; `visibility`: `private`; `default_branch`: `main`; `ssh_host`, `ssh_port`, `drive_url`: null; `credential_refs`, `ci_runner_tags`, `test_commands`: lists |
| `delegation` | Object, which may be empty to disable delegation | `enabled`: false; `agents`: list; `max_parallel`: 1; `max_attempts`: 2; `writable_paths`: relative path list; `approval_policy`: `review-before-integration` or `review-each-task` |
| Each agent | `label`, `role`, `worker` | `capabilities`: list |

Enabled delegation requires at least one agent and explicit writable paths.
Archetype mappings remain unchanged; `custom` requires explicit domains.
GitHub currently uses github.com over HTTPS. GitLab supports nested namespaces,
HTTP(S) API access and HTTP(S)/SSH Git transports, including SSH aliases.
GitLab bootstrap requires authenticated `glab` even when using SSH for Git.
Configure `glab` for the selected API host and HTTP(S) scheme beforehand; the
setup plan records the scheme but does not rewrite `glab` authentication settings.
A fresh local project requires a new remote; bootstrap refuses to adopt an
existing remote automatically. Inspect an existing project through the normal
discovery and migration-assessment workflow instead.

Example: [project-setup.example.json](../templates/project-setup.example.json).

## Persistence and recovery

Fresh projects also initialize the five management registries described in
[management extensions](../docs/MANAGEMENT-EXTENSIONS.md). Setup's milestone
strings are planning intent, not completed or automatically accepted milestones.
After the interview, translate agreed targets into milestone records with an
owner, due date, explicit acceptance criteria and task dependencies. Resolve
which milestones are required for release with the accountable owner. Never
invent dates, approvals, evidence or risk acceptance to complete the setup.

For an existing project, run the read-only migration assessment first, then
explicitly initialize approved extensions with
`python3 scripts/management_init.py PROJECT --actor "Coordinator"`.
The initializer preserves existing registries and legacy documents. Transfer
legacy risks or problems through reviewed CLI operations; do not delete the old
records or imply that an empty new registry has migrated their content.

Projects generated with `--config` contain `00-project/PROJECT-SETUP.json` and its readable
`PROJECT-SETUP.md` companion. The JSON is the setup intent; its machine-specific
local path is omitted. It is not a live discovery inventory, task registry or
substitute for the engineering work products. Populate the existing PROJECT,
PROCESS-SCOPE, QA and task work products from this intent as engineering proceeds.

The canonical bootstrap remains `scripts/bootstrap_project.py`. Explicit legacy
flags still work; `--project-dir` provides an optional portable destination. The
legacy default remains the OpenClaw workspace. Templates and executable sources
are found relative to the installed script, so installation does not depend on a
particular user account or original workspace.

Resume with the same reviewed setup. Passed bootstrap steps are skipped. A
repeated structure step preserves existing documents, configuration registries,
CI and copied audit tools; it does not reset counters or evidence. Invalid
existing JSON is rejected. Conflicting target, domain, branch or setup parameters
are rejected. Completed projects are not reinitialized. Do not delete bootstrap
state to bypass these checks; inspect the failed step and correct its cause.

Audit and management scripts are copied into `tools/project-audit` so generated
projects remain usable without the original skill installation. Current registry
locking requires a POSIX runtime; Windows can prepare/validate configuration,
while bootstrap and registry integration are validated on Linux.

For a project initialized with delegation enabled, run the copied planner from
the generated project root after preparing a READY task with bounded output
paths and acceptance criteria:

```sh
python3 tools/project-audit/delegation_plan.py . TASK-001 --agent AGENT_LABEL --write-path RELATIVE_DIRECTORY
```

The planner reads `00-project/PROJECT-SETUP.json` and canonical task state. It
requires an available Git commit, verifies policy and conflict bounds, and
returns a contract without dispatching a worker. Copied `project_state.py` and
`pm_common.py` supply its local dependencies. Projects created with legacy
explicit bootstrap flags have no setup configuration or delegation enabled by
default; adding reviewed setup intent to an existing project is a separate
controlled edit, not a reason to rerun bootstrap.

## Publication boundary

Setup validation can detect common mistakes, not every arbitrary secret or
personal detail. A real project's setup contains private business and
infrastructure context even without tokens. Do not copy real setup files,
bootstrap runtime state, credentials, SSH configuration or project artifacts into
the public skill package. Use the synthetic example and run the publication
checks on the final staged tree.
