# clawvet

**Skill vetting & supply chain security for OpenClaw.**

ClawVet scans OpenClaw `SKILL.md` files for prompt injection, credential theft, remote code execution, typosquatting, and social engineering — before they reach your agent.

## Install

```bash
npm install -g clawvet
```

## Usage

### Scan a local skill

```bash
clawvet scan ./my-skill/
clawvet scan ./my-skill/SKILL.md
```

### JSON output (for CI/CD)

```bash
clawvet scan ./my-skill/ --format json
```

### Fail on severity threshold

```bash
clawvet scan ./my-skill/ --fail-on high
# exits 1 if any high or critical findings
```

### Fetch and scan from ClawHub

```bash
clawvet scan weather-forecast --remote
```

### Audit all installed skills

```bash
clawvet audit
```

### Watch for new skill installs

```bash
clawvet watch --threshold 50
```

## What it detects

ClawVet runs a 6-pass analysis on every skill:

| Pass | What it checks |
|------|---------------|
| **Skill Parser** | Extracts YAML frontmatter, code blocks, URLs, IPs, domains |
| **Static Analysis** | 54 regex patterns: RCE, reverse shells, credential theft, obfuscation, DNS exfil, privilege escalation |
| **Metadata Validator** | Undeclared binaries, env vars, missing descriptions, invalid semver |
| **Dependency Checker** | `npx -y` auto-install, global `npm install`, risky packages |
| **Typosquat Detector** | Levenshtein distance against popular skills, suspicious naming patterns |
| **Semantic Analysis** | AI-powered detection of social engineering & prompt injection (optional) |

## Risk Scoring

| Score | Grade | Action |
|-------|-------|--------|
| 0-10 | A | Approve |
| 11-25 | B | Approve |
| 26-50 | C | Warn |
| 51-75 | D | Warn |
| 76-100 | F | Block |

## CI/CD Integration

```yaml
# GitHub Actions example
- name: Vet skill
  run: npx clawvet scan ./my-skill --format json --fail-on high
```

## License

MIT
