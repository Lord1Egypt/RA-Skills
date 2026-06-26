---
name: claw-doctor
description: Diagnose and fix common OpenClaw / NanoClaw issues — broken skills, missing scripts, API key failures, path resolution bugs, and configuration problems. The meta-skill for when your claw is broken.
version: 1.0.0
keywords:
  - openclaw
  - nanoclaw
  - debugging
  - troubleshooting
  - skills
  - skill-not-found
  - script-path
  - api-key
  - configuration
  - repair
metadata:
  openclaw:
    emoji: "🦞"
    homepage: https://github.com/tianyilt/openclaw-repair-skills
    requires:
      anyBins:
        - python3
        - python
---

# Claw Doctor — OpenClaw Self-Repair Skill

This skill diagnoses and fixes common OpenClaw / NanoClaw problems. When something breaks, run through the checklist below before giving up.

---

## When to Activate

Activate this skill when the user reports any of the following:

- "skill not found" / skill does not trigger
- "No such file or directory" when running a skill script
- API key errors from a skill
- Skill produces no output or wrong output
- "SKILL.md is invalid" / YAML parse errors
- A skill works globally but not in workspace (or vice versa)
- Skills were working before but stopped after an update

---

## Skill Load Order & Paths

OpenClaw loads skills from two locations. **Workspace skills take priority.**

```
Priority 1 (high): <workspace>/skills/<skill-name>/SKILL.md
Priority 2 (low):  ~/.openclaw/skills/<skill-name>/SKILL.md
```

### Diagnostic: list all loaded skills

```bash
# Show what's installed globally
ls ~/.openclaw/skills/ 2>/dev/null || echo "No global skills dir"

# Show what's installed in current workspace
ls ./skills/ 2>/dev/null || echo "No workspace skills dir"
```

If a skill appears in both, the **workspace version wins** — check for version mismatches.

---

## Problem 1 — Skill Does Not Trigger

**Symptom**: User invokes a skill but Claude ignores it or does not follow the skill procedure.

**Diagnosis checklist**:

1. Is the `SKILL.md` actually present and readable?
   ```bash
   cat ./skills/<skill-name>/SKILL.md | head -20
   ```

2. Does the frontmatter YAML parse correctly?
   ```bash
   python3 -c "
   import re, sys
   txt = open('skills/<skill-name>/SKILL.md').read()
   fm = re.search(r'^---\n(.*?)\n---', txt, re.DOTALL)
   print('Frontmatter found:', bool(fm))
   if fm:
       import yaml; d = yaml.safe_load(fm.group(1)); print('Keys:', list(d.keys()))
   "
   ```

3. Do the `keywords` in the SKILL.md match what the user said?
   - Add more keyword variants (synonyms, abbreviations) if not matching.

4. Is `description` clear enough for the model to identify the skill?
   - Short, specific descriptions outperform vague ones.

**Fix**: Ensure frontmatter is valid YAML (no tabs, proper quoting, correct indentation).

---

## Problem 2 — Script Not Found (Path Resolution)

**Symptom**: `bash: scripts/run: No such file or directory`

This is the most common skill bug. Scripts referenced in SKILL.md as `scripts/foo` are relative to the skill's **installation directory inside the OpenClaw plugin cache**, not the current working directory.

**Canonical fix** — resolve the script path dynamically before every use:

```bash
# For a skill named "my-skill" with a script named "run"
MY_SCRIPT=$(find ~/.openclaw -name "run" -path "*/my-skill/*/scripts/*" -type f 2>/dev/null | head -1)
# Fallback: check workspace skills
[ -z "$MY_SCRIPT" ] && MY_SCRIPT=$(find ./skills -name "run" -path "*/my-skill/scripts/*" -type f 2>/dev/null | head -1)

if [ -z "$MY_SCRIPT" ]; then
  echo "ERROR: script not found. Is the skill installed?"
  exit 1
fi

$MY_SCRIPT <args>
```

**Also check**: Is the script executable?

```bash
chmod +x ~/.openclaw/skills/my-skill/scripts/*
chmod +x ./skills/my-skill/scripts/*
```

---

## Problem 3 — API Key Not Configured

**Symptom**: Skill returns `{"success": false, "setup_required": true}` or 401/403 errors.

**Standard API key setup flow**:

1. The skill's SKILL.md should document where the key is stored (usually `~/.openclaw/secrets/<skill-name>.key` or an env var).
2. Check if the key file exists:
   ```bash
   ls ~/.openclaw/secrets/ 2>/dev/null || echo "No secrets dir"
   ```
3. Run the skill's setup command (usually `scripts/run setup <api-key>`).
4. Verify the key was saved:
   ```bash
   cat ~/.openclaw/secrets/<skill-name>.key 2>/dev/null | head -c 20
   ```

**If no setup command exists**, ask the user to set the env var directly:
```bash
export SKILL_API_KEY="their-key-here"
# Add to ~/.zshrc or ~/.bashrc for persistence
```

---

## Problem 4 — Dependency Missing (Node.js / Python / tool)

**Symptom**: `node: command not found`, `python3: No such file or directory`, `jq: command not found`

**Quick dependency check**:

```bash
echo "=== Core deps ===" && \
node --version 2>/dev/null || echo "MISSING: node" && \
python3 --version 2>/dev/null || echo "MISSING: python3" && \
jq --version 2>/dev/null || echo "MISSING: jq" && \
curl --version 2>/dev/null | head -1 || echo "MISSING: curl"
```

**Fix by platform**:

| Tool | macOS | Ubuntu/Debian |
|------|-------|---------------|
| Node.js | `brew install node` | `apt install nodejs npm` |
| Python 3 | `brew install python3` | `apt install python3` |
| jq | `brew install jq` | `apt install jq` |

For Python skill dependencies:
```bash
pip3 install -r skills/<skill-name>/requirements.txt 2>/dev/null \
  || echo "No requirements.txt found"
```

For Node skill dependencies:
```bash
cd skills/<skill-name> && npm install 2>/dev/null \
  || echo "No package.json found"
```

---

## Problem 5 — YAML Frontmatter Errors

**Symptom**: Skill loads but metadata is wrong / keywords not indexed.

**Valid frontmatter template**:

```yaml
---
name: my-skill-name         # lowercase, hyphens only
description: One clear sentence describing what this skill does.
keywords:
  - keyword-one
  - keyword-two
license: MIT
---
```

**Common mistakes**:

| Mistake | Fix |
|---------|-----|
| Tabs instead of spaces | Replace with 2-space indentation |
| Unquoted `:` in description | Wrap value in quotes |
| Missing `name` field | Add it — it's required |
| `keywords` as inline list `[a, b]` | Use block list `- a\n- b` |

**Validate**:

```bash
python3 -c "
import yaml, sys
txt = open('skills/<skill-name>/SKILL.md').read().split('---')[1]
try:
    d = yaml.safe_load(txt)
    print('OK:', d)
except yaml.YAMLError as e:
    print('YAML ERROR:', e)
    sys.exit(1)
"
```

---

## Problem 6 — Skill Worked Before, Broke After Update

**Symptom**: OpenClaw updated and a skill stopped working.

**Checklist**:

1. Check if the OpenClaw plugin cache was cleared:
   ```bash
   ls ~/.openclaw/plugins/cache/ 2>/dev/null | head -10
   ```

2. Reinstall the skill from source:
   ```bash
   # From a cloned skills repo
   cp -r /path/to/skills-repo/skills/<skill-name> ~/.openclaw/skills/
   ```

3. Check for breaking changes in OpenClaw's skill API — look at the OpenClaw changelog for `SKILL.md` format updates.

4. Test the script directly (bypassing OpenClaw):
   ```bash
   bash skills/<skill-name>/scripts/<main-script> --help
   ```

---

## Full Health Check

Run this to get a complete snapshot of the OpenClaw environment:

```bash
echo "=== OpenClaw Health Check ===" && \
echo "--- Global skills ---" && ls ~/.openclaw/skills/ 2>/dev/null || echo "(none)" && \
echo "--- Workspace skills ---" && ls ./skills/ 2>/dev/null || echo "(none)" && \
echo "--- Secrets ---" && ls ~/.openclaw/secrets/ 2>/dev/null || echo "(none)" && \
echo "--- Plugin cache ---" && ls ~/.openclaw/plugins/cache/ 2>/dev/null | head -5 || echo "(empty)" && \
echo "--- Dependencies ---" && \
  node --version 2>/dev/null && \
  python3 --version 2>/dev/null && \
  jq --version 2>/dev/null && \
echo "=== Done ==="
```

---

## For Claude Code Users

This skill also works as a Claude Code user-invocable skill. Add the following to `~/.claude/CLAUDE.md` under `## User-Invocable Skills`:

```markdown
### claw-doctor

Diagnose and fix OpenClaw / NanoClaw problems.

**Trigger**: user mentions skill not loading, script not found, API key error, SKILL.md broken, OpenClaw not working

**Procedure**: Follow the claw-doctor SKILL.md checklist:
1. Identify symptom category (trigger / script path / API key / dependency / YAML / post-update)
2. Run the relevant diagnostic commands
3. Apply the fix and verify with the Full Health Check
```

---

## Contributing

Found a new OpenClaw failure mode? Open a PR with:
1. The symptom (exact error message or behavior)
2. Root cause
3. Diagnostic command
4. Fix

Keep entries short and command-first. The doctor should be fast to consult.
