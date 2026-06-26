# AgentShield – Platform Guide

AgentShield works with **any AI agent** – not just OpenClaw.
The 77 security tests run locally on your machine. Only pass/fail scores and your public key are sent to the API.

---

## Supported Platforms

| Platform | Auto-Detection | Manual | Notes |
|----------|---------------|--------|-------|
| **OpenClaw** | ✅ Automatic | ✅ | Full auto-detect via IDENTITY.md |
| **n8n** | ✅ Automatic | ✅ | Reads workflow name from n8n config |
| **LangChain** | ✅ Automatic | ✅ | Reads agent name from config/env |
| **Any other** | ❌ | ✅ | Use `--name` and `--platform` flags |

---

## 🦞 OpenClaw

**Auto-detection:** Fully automatic. AgentShield reads `IDENTITY.md` for your agent name.

```bash
cd ~/.openclaw/workspace/skills/agentshield-audit
pip install -r requirements.txt

# Recommended: dry-run first
python3 initiate_audit.py --auto --dry-run

# Run real audit
python3 initiate_audit.py --auto
```

**Result:** Certificate saved to `~/.openclaw/workspace/.agentshield/certificate.json`

---

## 🔄 n8n

n8n is a workflow automation platform where agents run as workflows.
AgentShield audits the security configuration of your n8n agent workflow.

### Prerequisites

- Python 3.8+ installed on the machine running n8n
- n8n running locally or self-hosted (not n8n Cloud)

### Installation

```bash
# 1. Install AgentShield
pip install cryptography requests

# 2. Download the audit script
curl -L -o agentshield-audit.zip https://clawhub.ai/bartelmost/agentshield-audit/download
unzip agentshield-audit.zip -d agentshield-audit
cd agentshield-audit
```

Or via ClawHub (if OpenClaw is installed):
```bash
clawhub install agentshield-audit
cd ~/.openclaw/workspace/skills/agentshield-audit
```

### Run the Audit

```bash
# Auto-detection (recommended) – reads ~/.n8n/ and instance name automatically
python3 initiate_audit.py --auto

# Manual: with your n8n workflow/agent name
python3 initiate_audit.py --name "MeinN8nAgent" --platform "n8n"

# Optional: add your n8n version
python3 initiate_audit.py --name "MeinN8nAgent" --platform "n8n" --version "1.0"
```

**Auto-Detection erkennt automatisch:**
- `~/.n8n/` Verzeichnis → Platform wird als `n8n` gesetzt
- `~/.n8n/config` instanceName → wird als Agent-Name vorgeschlagen
- Bestätigung nötig bei Confidence < 80%

### What gets tested?

AgentShield tests your **n8n agent's security posture**:
- ✅ Prompt injection resistance (does your agent follow malicious instructions?)
- ✅ Secret exposure (are API keys hardcoded in workflow nodes?)
- ✅ Output data leakage (does your agent leak sensitive data?)
- ✅ Tool sandboxing (does your agent restrict dangerous operations?)
- ✅ Supply chain security (suspicious imports in Code nodes?)

### Tip: n8n Code Node Check

If your n8n workflow contains **Code nodes**, copy the code into a file and point AgentShield to it:

```bash
python3 initiate_audit.py \
  --name "MeinN8nAgent" \
  --platform "n8n" \
  --system-prompt "$(cat my_workflow_system_prompt.txt)"
```

---

## 🦜 LangChain / LangGraph

LangChain and LangGraph agents are Python-based. AgentShield integrates directly.

### Prerequisites

- Python 3.8+
- Your LangChain agent project

### Installation

```bash
pip install cryptography requests
pip install agentshield  # coming soon to PyPI

# For now, clone directly:
git clone https://github.com/bartelmost/agentshield.git
cd agentshield/agentshield-audit
```

Or via ClawHub (if OpenClaw is installed):
```bash
clawhub install agentshield-audit
cd ~/.openclaw/workspace/skills/agentshield-audit
```

### Option A: CLI (Quickest)

```bash
python3 initiate_audit.py \
  --name "MeinLangChainAgent" \
  --platform "langchain"
```

### Option B: Inline in your Python code

Add AgentShield to your LangChain agent startup for continuous verification:

```python
import subprocess
import json
from pathlib import Path

def verify_agent_certificate(agent_name: str) -> dict:
    """Run AgentShield audit and return certificate."""
    result = subprocess.run(
        ["python3", "initiate_audit.py", "--name", agent_name, "--platform", "langchain"],
        cwd=Path.home() / ".openclaw/workspace/skills/agentshield-audit",
        capture_output=True,
        text=True
    )
    
    cert_path = Path.home() / ".openclaw/workspace/.agentshield/certificate.json"
    if cert_path.exists():
        return json.loads(cert_path.read_text())
    return {}

# In your agent initialization:
from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(agent=agent, tools=tools)

# Run AgentShield audit on startup
cert = verify_agent_certificate("MeinLangChainAgent")
print(f"Agent certified: {cert.get('agent_id')} | Score: {cert.get('security_score')}/100")
```

### Option C: System Prompt Audit

If your LangChain agent uses a system prompt, you can include it in the audit for deeper analysis:

```bash
python3 initiate_audit.py \
  --name "MeinLangChainAgent" \
  --platform "langchain" \
  --system-prompt "$(cat my_system_prompt.txt)"
```

---

## 🌐 Any Other Platform

Works with: **Flowise, Botpress, Rasa, AutoGen, CrewAI, custom Python agents, or any other setup.**

### Quickest Way

```bash
python3 initiate_audit.py \
  --name "MeinAgent" \
  --platform "flowise"   # or: autogen, crewai, botpress, custom, ...
```

Platform name is free text – use whatever describes your setup.

### With System Prompt

If your agent has a system prompt or instruction file:

```bash
python3 initiate_audit.py \
  --name "MeinAgent" \
  --platform "custom" \
  --system-prompt "Du bist ein hilfreicher Assistent der..."
```

### Privacy: Dry-Run First

Not sure what gets sent? Check it first:

```bash
python3 initiate_audit.py --name "MeinAgent" --platform "custom" --dry-run
```

Output shows the **exact payload** that would be submitted. No data is sent in dry-run mode.

---

## 📜 After the Audit

### View your certificate

```bash
python3 show_certificate.py
```

### Verify another agent

```bash
python3 verify_peer.py agent_xxxxx
```

### Public verification URL

After audit, your agent is publicly verifiable at:
```
https://agentshield.live/api/verify/<your-agent-id>
```

Share this URL with your users, customers, or integration partners as proof of security verification.

---

## ❓ FAQ

**Q: Do I need OpenClaw to use AgentShield?**
No. OpenClaw is one supported platform. AgentShield works independently with any agent.

**Q: Does AgentShield read my system prompt?**
Only if you explicitly pass it via `--system-prompt`. Even then, it stays local – only pass/fail scores are sent to the API. Use `--dry-run` to verify.

**Q: Can I run AgentShield in CI/CD?**
Yes. Use `--yes` flag to skip consent prompts (recommended only after reviewing the dry-run output first).

```bash
python3 initiate_audit.py --name "MeinAgent" --platform "n8n" --yes
```

**Q: How often should I re-audit?**
Certificates are valid for 90 days. Re-audit when you change your agent's system prompt, tools, or configuration.

**Q: What platforms are you adding next?**
Currently prioritizing: n8n auto-detection, Flowise, AutoGen.
Missing your platform? Contact us: support@agentshield.live

---

## 📞 Support

- **Website:** https://agentshield.live
- **Email:** support@agentshield.live
- **GitHub:** https://github.com/bartelmost/agentshield
