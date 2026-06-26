# Gomboc Code Remediation Skill

**Deterministic, merge-ready code fixes for any codebase.**

Gomboc.ai Community Edition automatically scans and fixes code issues across your entire codebase — infrastructure, applications, configurations, and more — using deterministic AI (no hallucinations). This skill wraps Gomboc's power into agent workflows, CLI tools, and CI/CD pipelines, making it the perfect complement to agentic coding.

## What It Does

- **Scan** any codebase for issues (infrastructure, application code, configs)
- **Generate** deterministic, merge-ready pull requests with fixes
- **Remediate** continuously via GitHub Actions or interactive CLI/MCP
- **Trust** 94%+ fix acceptance rate with zero hallucinations (ORL Engine)
- **Pair with agents** — deterministic remediation that works perfectly alongside agentic coding systems

## Supported Languages & Frameworks

- **Infrastructure as Code** — Terraform, CloudFormation, Kubernetes YAML
- **Configuration Files** — JSON, YAML, HCL
- **Security Issues** — Across any codebase (IaC, applications, configs)
- **Expanding** — More languages and frameworks added regularly

## Quick Start

### 1. Get a Token

```bash
# Sign up at https://app.gomboc.ai (free, Community Edition)
# Generate Personal Access Token in Settings
export GOMBOC_PAT="gpt_your_token"
```

### 2. Scan Code

```bash
python scripts/cli-wrapper.py scan --path ./src
```

### 3. Generate Fixes

```bash
python scripts/cli-wrapper.py fix --path ./src
```

### 4. Apply Fixes (Optional)

```bash
python scripts/cli-wrapper.py remediate --path ./src --commit
```

## Key Features

✅ **Deterministic AI** — Same fix every time, no hallucinations  
✅ **94%+ Accuracy** — Merge-ready fixes users actually accept  
✅ **Free Forever** — Community Edition of Gomboc.ai  
✅ **Production-Ready** — Battle-tested implementation  
✅ **Secure by Design** — No token leaking, proper error handling  
✅ **Agent-Friendly** — Perfect for autonomous code improvement loops  

## CLI Commands

### scan
Detect issues in your codebase

```bash
gomboc scan path:./terraform
gomboc scan path:./src policy:aws-cis format:markdown
```

### fix
Generate merge-ready fixes

```bash
gomboc fix path:./terraform format:pull_request
gomboc fix path:./src format:json
```

### remediate
Apply fixes directly to code

```bash
gomboc remediate path:./src commit:true
gomboc remediate path:./terraform commit:true push:true
```

### config
Manage authentication

```bash
gomboc config --show-token
```

## For Agents

This skill is designed as the ideal complement to agentic coding:

- **Deterministic** — Reliable, repeatable remediation
- **Trustworthy** — 94%+ of fixes are merged as-is
- **Autonomous** — Agents can scan, generate, and apply fixes without human intervention
- **Continuous** — Perfect for ongoing code improvement loops

## Integration Methods

### 1. MCP Server (Agents)

Run the MCP server for interactive agent integration:

```bash
docker-compose -f scripts/docker-compose.yml up
# Server runs on http://localhost:3100
```

See `references/mcp-integration.md` for details.

### 2. CLI Tool (Developers)

Use the Python CLI for local scanning and fixing:

```bash
export GOMBOC_PAT="your_token"
python scripts/cli-wrapper.py scan --path ./src
```

See `references/setup.md` for detailed instructions.

### 3. GitHub Actions (CI/CD)

Automate continuous remediation in your CI/CD pipeline:

```yaml
- uses: gomboc-action@v1
  with:
    path: ./terraform
    auto-fix: true
```

See `references/github-action.md` for configuration.

## Configuration

All configuration is via environment variables:

| Variable | Purpose | Required | Example |
|----------|---------|----------|---------|
| `GOMBOC_PAT` | Personal Access Token | Yes | `gpt_abc123...` |
| `GOMBOC_MCP_URL` | MCP server URL | No | `http://localhost:3100` |
| `GOMBOC_POLICY` | Remediation policy | No | `default` or `aws-cis` |

## Security & Audit

This skill has been:
- ✅ Security-audited for token handling
- ✅ Verified against live Gomboc API
- ✅ Tested with real vulnerabilities
- ✅ Confirmed production-ready

See `SECURITY.md` for complete audit details.

## Support & Documentation

- **Setup Guide:** `references/setup.md`
- **MCP Integration:** `references/mcp-integration.md`
- **GitHub Actions:** `references/github-action.md`
- **Security Audit:** `SECURITY.md`
- **Changelog:** `CHANGELOG.md`
- **GitHub Discussions:** https://github.com/Gomboc-AI/gomboc-ai-feedback/discussions

## License

MIT License — See LICENSE file

---

**Ready to remediate?** Start with the Quick Start section above, then explore integration methods that fit your workflow.
