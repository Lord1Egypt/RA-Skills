---
name: credential-exposure-map
description: Map all credentials your OpenClaw agent can access. Scans env vars, config, memory, skills, MCP servers, git history. Generates exposure report with risk scoring. Activate when user says "credential audit", "exposure map", "security audit", or "what can my agent access".
version: 1.1.1
---

# Credential Exposure Map

> See every credential your agent can touch. Score the blast radius. Shrink the attack surface.


## Onboarding (First Use)

When the user first triggers this skill and `memory/credential_exposure_map_state.json` doesn't exist, run a one-time setup:

1. **Introduce capability** (one sentence): _"I can scan every credential your agent can access (env/config/memory/git history) and generate a risk-scored report."_

2. **Quick configuration:**

1. **Scan scope**(Default: All)
   - All(env + config + memory + skills + MCP + git history)
   - Environment variables and config files only
   - Git history only
2. **Risk threshold**(Default: Medium)
   - Low: list all exposures (including safe ones)
- : medium and high risk(recommended)
   - High: critical risk only (may miss some)
3. **Save last scan results**(Default: Yes, for comparison with next scan)

3. **Write initial state file** `memory/credential_exposure_map_state.json`(JSON format, with `onboarded: true` and timestamp)

4. **Confirm completion**: _"Setup done! Just use it from now on. Say 'reset settings' anytime to reconfigure."

**Onboarding runs exactly once.** Subsequent activations read the state file directly. When the user says "reset settings", delete the state file and re-run setup.

---

## When to Activate

- User says: "credential audit", "exposure map", "security audit"
- User says: "what can my agent access", "credential scan"
- User says: "credential cleanup", "redact credentials"

Do NOT activate for normal work conversations.

## Audit Flow

When user asks for a credential audit or exposure map:

1. Run the scanner:

```bash
python3 skills/credential-exposure-map/scripts/scan_exposure.py
```

2. Present the output in a clean format:
   - Summary: total findings, risk distribution
   - Credential Inventory: table with preview, risk level, source, location
   - Skill Capability Matrix: which skills have exec/read/network/write
   - Top recommendations for reducing exposure

3. Highlight CRITICAL findings prominently.

## Recommendation Generation

After presenting the scan, offer specific recommendations:

- **CRITICAL credentials in env**: "Move to secrets vault or remove from agent context"
- **Credentials in MEMORY.md**: "These persist across sessions. Consider redacting."
- **Skills with full exec+network**: "Review if this skill needs both capabilities"
- **Secrets in git history**: "Use git filter-branch or BFG to scrub history"
- **MCP servers with auth**: "Verify each MCP server's permission scope"

## Output Format

### Summary

```
Scan Complete: X finding(s)
Risk: N Critical | N High | N Medium | N Low
```

### Credential Inventory

Table showing each credential with:
- Preview (first 8 chars + ***)
- Risk level (CRITICAL/HIGH/MEDIUM/LOW)
- Source (env/config/memory/skill/mcp/git)
- Location (file:line or config path)

### Skill Capability Matrix

Table showing each installed skill with exec/read/network/write permissions and risk score.

## Security Considerations

- NEVER output full credential values. Always mask as `first8chars***`
- Report is saved to `~/.openclaw/credential-exposure-report.json` with 600 permissions
- Scan is read-only, does not modify any files
- Skill capability inference is conservative (assumes exec = full filesystem access)

## Detection Coverage

| Source | What It Finds |
|--------|--------------|
| Environment variables | API keys, tokens, passwords in process.env |
| openclaw.json | Provider keys, webhook secrets, MCP auth |
| .env files | Any .env in workspace or ~/.openclaw |
| MEMORY.md / memory/*.md | Credentials written into agent memory |
| memory/*.json | Credential caches, state files with tokens |
| Installed skills | Skills with exec, read, or network capabilities |
| MCP server config | Connected services with auth scope |
| Git history | Secrets committed in last 50 commits |
