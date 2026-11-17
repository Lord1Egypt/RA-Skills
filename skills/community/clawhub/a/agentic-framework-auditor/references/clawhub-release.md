# ClawHub Release Checklist

Load this reference before publishing this skill or when auditing a skill intended for ClawHub.

## Package Boundary

- Publish `skills/agentic-framework-auditor/`, not the repository root.
- Include `SKILL.md`, `agents/openai.yaml`, required scripts, and required references.
- Exclude `stress-lab/`, generated reports, caches, backups, local state, unrelated projects, and private framework files.
- Keep supporting files text-based unless a binary asset is explicitly necessary and permitted.

## Metadata

- Keep `SKILL.md` frontmatter limited to accurate `name` and `description` fields.
- Keep `agents/openai.yaml` aligned with the skill's actual behavior.
- Declare no credentials, provider, network, or runtime requirement that the skill does not use.
- State that deterministic findings are heuristic evidence rather than certification.

This skill uses Python standard-library scripts and requires no credentials or external model provider.

## Release Validation

1. Run `python scripts/run_self_check.py` from the skill folder.
2. From the source repository root, run `python stress-lab/run_stress_lab.py`.
3. Run the skill validator from `skill-creator`.
4. Audit the skill folder itself in deterministic-only mode.
5. Review prompt-injection, hidden install, remote execution, credential, destructive, path-scope, review-gate, and metadata findings manually.
6. Confirm likely secret files remain excluded by default.
7. Confirm no generated output or stress fixture is inside the package folder.
8. Inspect the exact package file list before publication.

## Publish Flow

Use a dry run before a real publication:

```bash
clawhub login
clawhub skill publish ./skills/agentic-framework-auditor --slug agentic-framework-auditor --name "Agentic Framework Auditor" --dry-run
clawhub skill publish ./skills/agentic-framework-auditor --slug agentic-framework-auditor --name "Agentic Framework Auditor"
```

Use `--owner <handle>` when publishing under an organization. Do not publish while the package review or stress suite is failing.
