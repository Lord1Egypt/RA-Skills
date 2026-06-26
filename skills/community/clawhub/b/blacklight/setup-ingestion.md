# Blacklight — Setup Ingestion and Agent Profiling v0.1.0

## Purpose

Blacklight adapts to the user's existing OpenClaw configuration. It does not impose its own worldview. It learns yours and protects it. This document specifies how Blacklight reads, analyses, and responds to the user's specific setup.

---

## Ingestion Sequence

On first load, before the Hardening Check, read the following in order:

### 1. SOUL.md
The agent's identity document. Extract:
- **Testable assertions**: specific commitments ("I always ask before acting," "I never handle money," "I communicate formally"). These become monitored contracts.
- **Personality profile**: cautious vs bold, formal vs casual, proactive vs reactive. This calibrates what counts as "abnormal behaviour."
- **Stated boundaries**: things the SOUL.md says the agent will not do. Violations of these are CRITICAL flags.
- **Communication style**: vocabulary preferences, tone, formality level. This feeds Digital Footprint Monitoring.

### 2. AGENTS.md
Operational parameters:
- Agent name and primary purpose
- Active channels
- Any configured personality overrides
- Multi-agent relationships (if applicable)

### 3. Installed Skills
For each installed skill:
- Name and stated purpose
- Permissions required and granted
- Tools used
- Last updated date
- Whether it's bundled, managed, or workspace-level
- Token cost contribution to system prompt

Build a **Skill Functional Map**: which skills read, which write, which communicate externally, which handle credentials, which process financial transactions.

### 4. Tool Permissions
- Which tools are enabled (exec, file read, file write, network, etc.)
- Sandbox status (enabled/disabled, scope)
- Approval mode (auto-approve, require approval, per-tool settings)
- Any custom permission grants

### 5. Cron Jobs and Scheduled Tasks
- Full schedule: what runs, when, how often
- Permissions each task operates under
- Which skills each task invokes
- Whether tasks have ever been modified since creation

### 6. Memory Contents
- Scan all stored memories
- Classify provenance: user-sourced, conversation-derived, external-sourced
- Flag any external-sourced memories containing actionable instructions
- Note the total memory volume and growth rate if detectable

### 7. Messaging Channels
- Which channels are active
- Channel type (DM, group, public)
- Other participants in group channels
- Which channels have been used for CONSEQUENTIAL or FINANCIAL actions previously

### 8. Model Configuration
- Model name and provider
- Temperature and sampling settings
- Max token configuration
- Any additional system prompt content
- Model's known strengths and weaknesses for instruction-following

---

## Agent Profile Synthesis

Combine all of the above into a structured Agent Profile:

```yaml
agent_profile:
  identity:
    name: [from AGENTS.md]
    soul_commitments: [extracted assertions]
    personality: [cautious/bold/formal/casual/etc]
    stated_boundaries: [list of things SOUL says agent won't do]
    communication_style: [description]

  capabilities:
    skills_count: [total]
    skill_categories: [list: financial, communication, file management, etc]
    tool_permissions: [summary]
    sandbox: [enabled/disabled]
    approval_mode: [setting]
    financial_access: [yes/no, which skills]
    external_communication: [yes/no, which skills and channels]
    credential_access: [yes/no, which skills]

  risk_surface:
    overall: [LOW / MODERATE / HIGH / CRITICAL]
    factors:
      - [specific risk factor]
      - [specific risk factor]
    combinatorial_risks: [flagged skill interactions]
    unmonitored_gaps: [identified gaps]

  schedule:
    cron_jobs: [count and summary]
    unattended_hours: [estimated from schedule]
    unattended_permissions: [what runs without user]

  memory:
    total_entries: [count]
    external_provenance: [count flagged]
    flagged_entries: [list if any]

  channels:
    total: [count]
    group_channels: [count, with participant summary]
    dm_only: [count]

  context_window:
    model_limit: [tokens]
    skill_consumption: [tokens]
    available: [tokens]
    utilisation: [percentage]

  model:
    name: [model]
    provider: [provider]
    instruction_compliance: [expected: high/medium/low based on model]
```

---

## Configuration-Aware Monitoring Calibration

Based on the Agent Profile, auto-adjust Blacklight's monitoring:

| Setup Factor | Monitoring Adjustment |
|---|---|
| Sandbox disabled | Increase all monitoring sensitivity |
| Approval mode: auto-approve | Increase autonomy pattern sensitivity (AG) |
| Financial skills installed | Activate Financial Module at full strength |
| No financial skills | Financial Module in passive mode |
| Group channels active | Activate Source Attribution |
| DM-only channels | Source Attribution in passive mode |
| Local/small model | Increase monitoring (weaker instruction-following) |
| Frontier model (Opus, GPT-4o) | Standard monitoring (stronger compliance expected) |
| SOUL describes cautious agent | Relax AG slightly, increase EP sensitivity |
| SOUL describes bold agent | Increase AG sensitivity |
| Many skills + auto-approve + no sandbox | Maximum monitoring |
| Few skills + sandbox + approval required | Light monitoring |

The monitoring adapts to actual risk. The user does not need to configure this manually. Blacklight figures it out.

---

## /blacklight-profile-agent

Outputs the full Agent Profile in readable format. Most users have never seen their setup described this coherently because they built it incrementally. This command shows them the unified picture.

---

Built by Eliot Gilzene (Shoji)
License: MIT
