
# Contradiction Analyzer - Installation Guide

## Prerequisites

- OpenClaw running normally
- No additional dependencies required

---

## Method 1: Manual Installation (Recommended)

### 1. Copy skill to OpenClaw skills directory

```powershell
# Windows
xcopy /E /I contradiction-analyzer %USERPROFILE%\.openclaw\skills\contradiction-analyzer

# Linux/Mac
cp -r contradiction-analyzer ~/.openclaw/skills/contradiction-analyzer
```

### 2. Restart OpenClaw Gateway

```bash
# Restart Gateway service
openclaw restart
```

### 3. Verify Installation

Open OpenClaw Dashboard and check if the skill is loaded:
http://127.0.0.1:18789/

---

## Method 2: Install via ClawdHub (if published)

```bash
clawdhub install contradiction-analyzer
```

---

## Usage Verification

### Test Contradiction Analysis

Ask OpenClaw questions like:
- "What are the different views on AI's impact on employment?"
- "What are the debates around universal basic income?"
- "What are the controversies surrounding social media regulation?"

Observe if the answer:
- Identifies and categorizes contradictions
- Distinguishes primary from secondary contradictions
- Maps information source stances
- Flags extreme or biased viewpoints
- Provides structured analysis briefing

---

## Synergy with Other Skills

### With Dialectics Skill

**Workflow:**
1. Contradiction Analyzer identifies and categorizes contradictions
2. Dialectics Skill performs synthesis and transcendence
3. Result: Comprehensive analysis with integrated solutions

**Usage:**
```
User: "What are the debates on AI and employment?"
[Contradiction Analyzer activates, generates briefing]
User: "Now provide a dialectical synthesis"
[Dialectics Skill activates, uses briefing as input]
```

### With Devil's Advocate Skill

**Workflow:**
1. Contradiction Analyzer maps out all contradictions
2. Devil's Advocate tests specific claims or strengthens arguments
3. Result: More robust analysis with tested claims

**Usage:**
```
User: "What are the different views on UBI?"
[Contradiction Analyzer activates, generates briefing]
User: "Challenge the claim that UBI reduces work incentives"
[Devil's Advocate activates, tests the claim]
```

### Combined Workflow

For comprehensive analysis:
1. **Contradiction Analyzer** → Identify all contradictions
2. **Devil's Advocate** → Test key claims
3. **Dialectics** → Synthesize and transcend

---

## Configuration Options

### Customization

You can customize the skill by modifying `CLAUDE.md`:

- **Trigger keywords**: Add or modify trigger conditions
- **Credibility criteria**: Adjust weighting factors
- **Output format**: Modify briefing structure
- **Flagging rules**: Adjust extreme content detection

---

## Uninstall

```powershell
# Windows
rmdir /S /Q %USERPROFILE%\.openclaw\skills\contradiction-analyzer

# Linux/Mac
rm -rf ~/.openclaw/skills/contradiction-analyzer
```
