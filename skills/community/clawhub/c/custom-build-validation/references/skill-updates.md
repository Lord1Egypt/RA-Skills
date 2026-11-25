# Check source without changing the run

The canonical source is TheAngryPit/TheAngrySkills, path
`skills/engineering/openclaw-custom-build-validation`. The installed release
skill's ClawHub updater is not appropriate for this separate TheAngrySkills skill.

For Git-backed skills, run the bundled read-only checker:

```sh
node <skill-directory>/scripts/check-update.mjs
```

It uses the existing GitHub CLI authentication only for read access to that
fixed repository, resolves the default branch to one SHA, and compares Git
tree identities. It never fetches executable code, changes files or installs.
Report one status line: source, local commit, canonical commit, comparison.

- `current`: same skill tree, even if unrelated repository commits differ.
- `source-differs`: committed trees differ; inspect the delta before deciding
  whether it is a newer accepted version, an unpublished branch, or divergence.
- `local-modifications`: tracked or untracked skill changes; preserve them.
- `untracked`: no Git metadata, a copy outside the canonical repository-relative
  skill path, or absent canonical path.
- `different-source`: checkout remotes do not identify the expected repository.
- `check-failed`: access, timeout or response validation failed; version unknown.

A copy without Git metadata is honestly untracked; do not manufacture version
provenance or search unrelated credential stores. Optional check failure does
not block candidate work. In offline/unit-test mode skip network checks.

When a useful update exists, offer it separately. Stage and inspect the candidate
source without executing its helpers. Before promoting it into an active root,
run `theangry-skills security scan <candidate-skill-path> --json` and
`theangry-skills security diff <installed-skill-path> <candidate-skill-path> --json`.
Then run `theangry-skills update-plan --candidate-root <staged-skills-root>
--installed-root <active-skills-root> --json` and review the staged verdict.
Do not bypass review or blocked entries. If these admission tools are unavailable,
keep the candidate staged and report the missing gate. Install accepted source
through the normal skills installer only when authorized and admission permits it;
use `update-apply` only with an accepted plan, `--only-safe`, and `--confirm`.
Preserve local changes; do not overwrite them based on a newer timestamp.
After an actual skill update, resume in a fresh task with the fixed candidate
identity and worksheet. Never mix old loaded instructions with a new skill.
