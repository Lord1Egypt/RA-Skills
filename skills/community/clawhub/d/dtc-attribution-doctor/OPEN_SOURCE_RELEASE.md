# Open-Source Release Plan

This directory is a clean publication candidate. Do not publish the parent
validation repository or preserve its Git history.

## 1. Release Scope

Include:

- `SKILL.md`, `functions.md`, and `access.yaml`
- `plans/` and `utilities/`
- Public documentation, governance, and GitHub configuration

Exclude:

- Competitor skills or copied third-party repositories
- Customer names, account IDs, API responses, reports, and validation evidence
- Model transcripts and internal evaluation documents
- Archives, local agent configuration, `.env` files, and API keys
- Internal roadmaps, pricing, subscription data, or other non-public business
  material

## 2. Confirmed Release Decisions

The following publication decisions are confirmed for the initial release:

- **GitHub organization:** `RTOAI`
- **Organization website:** `https://www.rto.ai/`
- **Copyright holder:** `RTOAI`
- **License:** MIT-0
- **Public scope:** API addresses, field definitions, and analysis rules are
  approved for publication
- **Initial release:** `v0.1.0` with Preview status

The planned repository URL is
`https://github.com/RTOAI/convbox-diagclaw`. Update references only if the
repository name changes before publication.

## 3. Pre-Publication Checks

Run from this directory:

```bash
python -m pip install -r requirements.txt
python -m py_compile utilities/config-health-check/config_health_check.py
python -c "import pathlib,yaml; yaml.safe_load(pathlib.Path('access.yaml').read_text(encoding='utf-8'))"
```

Then verify:

- No secret scanner findings
- All IDs and payloads in `access.yaml` are synthetic
- All Markdown links resolve
- `SKILL.md` and the root `LICENSE` both say `MIT-0`
- Scenario readiness in `functions.md` matches the public README
- Health checker never prints or serializes the API key
- A test installation works from a fresh directory

## 4. Create A Clean Repository

Create an empty GitHub repository without generated README or license files.
Then copy this directory outside the current validation repository and create a
new history:

```bash
git init -b main
git add .
git commit -m "feat: publish Convbox-DiagClaw skill"
git remote add origin git@github.com:RTOAI/convbox-diagclaw.git
git push -u origin main
```

Do not use `git filter-branch`, subtree splitting, or a normal push from the
parent repository. A new history is the simplest reliable boundary against
recovering customer and competitor material.

With GitHub CLI, repository creation can instead be performed after the local
commit:

```bash
gh repo create RTOAI/convbox-diagclaw \
  --public --source=. --remote=origin --push
```

## 5. GitHub Settings

Enable before announcing the repository:

- Default branch: `main`
- Branch protection: pull request required; status checks required
- Secret scanning and push protection
- Private vulnerability reporting
- Dependabot security updates
- Delete head branches after merge
- Discussions only if maintainers can support them

Suggested repository topics:

```text
agent-skills ecommerce analytics attribution marketing-ai dtc convbox
```

## 6. First Release

1. Merge the publication pull request.
2. Confirm CI passes on `main`.
3. Create the Preview tag `v0.1.0`.
4. Publish the GitHub release from the matching `CHANGELOG.md` entry.
5. Test installation from the release tag in a clean agent environment.
6. Monitor issues and security reports during the first two weeks.

Reserve `v1.0.0` for a later stable release after a separate readiness review.

## 7. Ongoing Maintenance

- Use short-lived branches and reviewed pull requests.
- Update `CHANGELOG.md` for user-visible behavior.
- Treat changes to metric caliber and API fields as compatibility changes.
- Re-run privacy and secret scans before every release.
- Never use customer payloads as public regression fixtures.
- Archive or deprecate scenarios explicitly instead of silently changing their
  meaning.
