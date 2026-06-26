# CareerClaw Release Checklist

Use this for every npm publish and ClawHub submission.

---

## Pre-publish gate

Run all of the following from the project root. All must pass before proceeding.

```bash
# 1. Offline tests — must be 270/270
npm test

# 2. Type check — must be clean (no output)
npm run lint

# 3. Live source connectivity
npm run smoke:sources

# 4. Full pipeline end-to-end
npm run smoke:briefing

# 5. LLM keys + Pro license validation
npm run smoke:llm
```

If any step fails — stop. Do not publish.

---

## Version bump checklist

Before tagging, confirm these 3 locations are updated to the new version:

- [ ] `package.json` — `"version"` field
- [ ] `src/config.ts` — `HTTP_USER_AGENT` string
- [ ] `SKILL.md` — frontmatter `version:` field and JSON output schema example

Verify with:

```bash
grep -rn "1\.0\.0" package.json src/config.ts SKILL.md README.md CHANGELOG.md src/tests/models.test.ts
```

```powershell
Select-String -Path "package.json", "src/config.ts", "SKILL.md", "README.md", "CHANGELOG.md", "src/tests/models.test.ts" -Pattern "1\.0\.0"
```

---

## Build + pack dry run

```bash
# Build TypeScript
npm run build

# Inspect what will be published (must NOT include .careerclaw/, .env, scripts/)
npm pack --dry-run
```

Confirm `files` in `package.json` includes: `dist`, `SKILL.md`, `README.md`,
`CHANGELOG.md`, `SECURITY.md` — and nothing else.

---

## npm publish (v0.11.0 first, then v1.0.0)

```bash
# Publish v0.11.0 first to preserve npm history
# (only if not already published)
git checkout v0.11.0
npm publish --access public

# Then publish v1.0.0
git checkout main
npm publish --access public
```

Verify on npm:

```
https://www.npmjs.com/package/careerclaw-js
```

---

## VirusTotal scan

After `npm pack` produces `careerclaw-js-1.0.0.tgz`:

1. Go to https://www.virustotal.com/gui/home/upload
2. Upload `careerclaw-js-1.0.0.tgz`
3. Save the scan URL — format: `https://www.virustotal.com/gui/file/<hash>`
4. Include the scan URL in the GitHub release notes

Expected result: 0 detections. If any vendor flags it, investigate before publishing.

---

## Git tag + GitHub release

```bash
git tag -a v1.0.0 -m "v1.0.0 — First ClawHub release"
git push origin v1.0.0
```

Create a GitHub release from the tag:
- Title: `v1.0.0 — CareerClaw`
- Body: paste the `[1.0.0]` section from `CHANGELOG.md`
- Attach: `careerclaw-js-1.0.0.tgz` + VirusTotal scan URL

---

## OpenClaw test gate (required before ClawHub submission)

On your AWS Lightsail OpenClaw host:

```bash
# Install the published package
npm install -g careerclaw-js@1.0.0

# Verify install
careerclaw-js --version
# Expected: 1.0.0

# Set env vars (Pro key + LLM key)
# Then run full briefing
careerclaw-js --resume-txt ~/.careerclaw/resume.txt --json --dry-run
```

Confirm in the JSON output:
- [ ] `run.version` = `"1.0.0"`
- [ ] `drafts[0].llm_enhanced` = `true` (Pro + LLM key set)
- [ ] `run.timings.draft_ms` > 0
- [ ] `.careerclaw/.license_cache` exists and is hash-only

---

## ClawHub submission

After the OpenClaw test gate passes:

1. Go to https://clawhub.io/submit (or current submission URL)
2. Package name: `careerclaw-js`
3. npm version: `1.0.0`
4. Upload or link `SKILL.md`
5. Category: Career / Job Search
6. Pricing: Free tier + Pro ($39 lifetime, Gumroad)
7. VirusTotal scan URL: (from step above)

---

## Post-publish verification

```bash
# Install from npm in a clean directory
mkdir /tmp/cc-verify && cd /tmp/cc-verify
npm install careerclaw-js@1.0.0
npx careerclaw-js --help
```

Confirm help text prints correctly and version matches.

---

## Rollback

If a critical bug is found after publishing:

```bash
# Deprecate (does not unpublish — npm policy)
npm deprecate careerclaw-js@1.0.0 "Critical bug — use 1.0.1"

# Fix, bump to 1.0.1, re-run this checklist from the top
```
