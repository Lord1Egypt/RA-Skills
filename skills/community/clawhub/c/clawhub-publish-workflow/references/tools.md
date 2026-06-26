# TOOLS & PREREQUISITES

## Required Tools

### 1. SKILL_EVALUATOR (Evaluation)

| Attribute | Value |
|-----------|-------|
| **Location** | `~/.openclaw/skills/SKILL_EVALUATOR/` or workspace version |
| **Script** | `evaluator.py` |
| **Language** | Python 3 |
| **Purpose** | Evaluate and improve skills |
| **Usage** | `python3 <path-to-evaluator>/evaluator.py <skill-path> --verbose --improve` |

**Example paths:**
```
# On Merlin:
/media/ezekiel/Merlin/.openclaw/skills/SKILL_EVALUATOR/evaluator.py

# On Ezekiel:
/home/ezekiel/.openclaw/skills/SKILL_EVALUATOR/evaluator.py

# On Morgana:
/media/ezekiel/Morgana/skills/SKILL_EVALUATOR/evaluator.py
```

---

### 2. ClawHub CLI (Publication)

| Attribute | Value |
|-----------|-------|
| **Command** | `clawhub` |
| **Install** | `npm i -g clawhub` |
| **Purpose** | Publish and manage skills on ClawHub |

**Required Commands:**
```bash
# Login with API token
clawhub login --token <token> --no-browser

# Check if logged in
clawhub whoami

# Publish a skill
clawhub publish <path> --slug <slug> --name "<Name>" --version 1.0.0 --changelog "<desc>"

# Inspect a published skill
clawhub inspect <slug>
```

---

### 3. OpenClaw CLI (Management)

| Attribute | Value |
|-----------|-------|
| **Command** | `openclaw` |
| **Purpose** | Manage OpenClaw workspace and skills |

**Useful Commands:**
```bash
# List skills
openclaw skills list

# Check skill status
openclaw skills list | grep <skill-name>
```

---

## Required Skills

### 1. skill-creator (Skill Creation)

**Purpose:** Guide for creating effective skills following best practices.

**Key Points:**
- Keep SKILL.md under 500 lines
- Use frontmatter with name + description
- Include tools, usage, examples sections
- Follow progressive disclosure design

---

### 2. SKILL_EVALUATOR (Evaluation)

**Purpose:** Automatically evaluate skills and suggest improvements.

**Evaluation Dimensions:**
| Dimension | Weight | Focus |
|-----------|--------|-------|
| Structure | 20% | Header, sections, formatting, meta |
| Clarity | 20% | Description, instructions, examples |
| Completeness | 20% | Tools, prerequisites, errors, edge cases |
| Consistency | 20% | Cluster alignment, style, naming |
| Functionality | 20% | Commands work, expected results |

**Target Score:** 70+ (APPROVED)

---

## API Token Management

### Getting ClawHub Token

1. Go to https://clawhub.com/settings/tokens
2. Create new token
3. Store securely in credentials file

### Token Storage (Merlin example)

Store in: `memory/credentials.md`
```
## ClawHub
- **Clé API:** `clh_...`
- **Utilisateur:** @YourUsername
- **Statut:** Connected
```

### Login with Token

```bash
clawhub login --token <your-token> --no-browser
```

---

## File Path References

### Core Files (for core-files-management skill)

| File | Path |
|------|------|
| identity.md | `~/.openclaw/workspace/identity.md` |
| soul.md | `~/.openclaw/workspace/soul.md` |
| agents.md | `~/.openclaw/workspace/agents.md` |
| user.md | `~/.openclaw/workspace/user.md` |
| memory.md | `~/.openclaw/workspace/memory.md` |
| tools.md | `~/.openclaw/workspace/tools.md` |
| bootstrap.md | `~/.openclaw/workspace/bootstrap.md` |

---

## Package Skill (For Distributing)

### Validator + Packager

**Location:** `skill-creator/scripts/`

**Commands:**
```bash
# Validate skill structure
python3 <skill-creator>/scripts/quick_validate.py <skill-path>

# Package skill to .skill file
python3 <skill-creator>/scripts/package_skill.py <skill-path> [--output-dir]
```

---

_In Altum Per Partage._
🧙‍♂️ Merlin — Tools & Prerequisites Reference