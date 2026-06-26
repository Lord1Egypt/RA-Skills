# Publishing Checklist (Local Skill → ClawHub)

Use this checklist before running `clawhub publish` or `clawhub sync`.

## 1) Confirm the Skill Folder Is Valid

- Folder contains a `SKILL.md` at the root of the skill directory.
- `SKILL.md` has frontmatter with at least:
  - `name`
  - `description`
- `SKILL.md` clearly tells the agent:
  - when to use it
  - what inputs it needs
  - what commands/actions to run
  - what safety rules to follow

## 2) Ensure No Secrets Will Be Published

Before publishing, scan for and exclude:

- `.env`, `*.env`
- API tokens, passwords, session cookies
- SSH keys and certificates
- cloud credentials files (AWS/GCP/Azure)
- internal URLs or proprietary data you are not allowed to share

If needed, add a `.gitignore`-like exclusion strategy (depending on what the ClawHub CLI supports) or remove the files from the folder before publishing.

## 3) Pick a Good Slug

Slug rules of thumb:

- lowercase
- hyphen-separated
- stable (avoid dates)
- unique and descriptive (e.g. `docker-compose-cli`, `git-cli`, `azure-devops-helper`)

## 4) Choose Version + Tags

- Version must be valid SemVer (`MAJOR.MINOR.PATCH`), e.g. `0.1.0`
- Tag should match intent:
  - `latest` for the default stable
  - `beta` for pre-release
  - `internal` if intended for private/limited use (only if supported/desired)

## 5) Publish Command Template

```bash
clawhub publish <skill-folder> \
  --slug <slug> \
  --name "<Display Name>" \
  --version <semver> \
  --tags latest
```

## 6) Post-Publish Verification

- Run `clawhub list` (if it reflects published state in the lockfile)
- Search on the website by slug or display name
- Install the published slug into a clean workspace and verify behavior

