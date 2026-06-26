# Installation Guide — Claude Code Memory Kit

## Quick Start (5 minutes)

### Step 1: Copy Template Files
```bash
# Copy the templates folder to your project
cp -r templates/* your-project-directory/
```

### Step 2: Configure Your Project
Edit each file with your specific requirements:

**CLAUDE.md** — Your project rules:
- Coding standards (naming, formatting)
- Allowed/disallowed patterns
- Testing requirements
- Any project-specific instructions

**memory.md** — Cross-session patterns:
- Common decisions and their rationale
- Reusable solutions to recurring problems
- Architecture decisions to remember

**mistakes.md** — What to avoid:
- Past errors and their fixes
- Anti-patterns specific to your project
- Things that didn't work

**bootstrap.md** — Session initialization:
- Current project status
- Active tasks and priorities
- Recent changes to catch up on

### Step 3: Test Your Setup
```bash
# Start a new Claude Code session
claude

# Verify it reads your files
/remember show all
```

### Step 4: Set Up Guardrails (Optional)
Add to `~/.claude/settings.json`:
```json
{
  "preToolGates": {
    "Bash(git push --force)": "confirm",
    "Bash(rm -rf)": "confirm"
  }
}
```

---

## Advanced Setup

### For Teams

1. **Commit templates to repo:**
```bash
git add CLAUDE.md memory.md mistakes.md bootstrap.md
git commit -m "Add Claude Code memory system"
```

2. **Create team-wide standards** in a shared CLAUDE.md at organization level

3. **Onboard new members:**
```bash
# New team member clones repo
git clone your-project
cd your-project
claude  # Already configured with team standards
```

### For Multiple Projects

Create a `~/.claude/projects/` directory with reusable templates:

```bash
~/.claude/projects/
├── javascript/CLAUDE.md
├── python/CLAUDE.md
├── fullstack/CLAUDE.md
```

Then copy appropriate template per project.

### For Enterprise

1. Create organization-level CLAUDE.md
2. Use LDAP/SSO for authentication
3. Audit trail via version control history
4. Regular review cycles (bi-weekly)

---

## File Placement Reference

```
your-project/
├── CLAUDE.md          # Required - project rules
├── memory.md          # Recommended - learned patterns
├── mistakes.md        # Recommended - anti-patterns
├── bootstrap.md       # Optional - session init
└── .claude/
    └── settings.json  # Optional - guardrails
```

---

## Verification Checklist

After installation, verify:

- [ ] CLAUDE.md exists in project root
- [ ] Claude Code reads the file on startup
- [ ] Rules are being followed in conversation
- [ ] Memory persists between sessions
- [ ] Mistakes are logged and avoided

---

## Troubleshooting

If something doesn't work, see TROUBLESHOOTING.md for common issues and solutions.