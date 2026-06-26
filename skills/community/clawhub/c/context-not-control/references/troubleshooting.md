# Troubleshooting Guide

Common issues and solutions when using "Context, not Control" workflow.

## Issue 1: AI Asks Too Many Questions

### Symptoms
- Every request triggers 10+ clarification questions
- Feels like an interrogation
- Slows down workflow

### Causes
- PROJECT.md not filled out properly
- Missing context about your preferences
- AI doesn't have enough background

### Solutions

**Solution 1: Complete PROJECT.md**
Fill in all sections with your preferences:
```markdown
## Technical Constraints
- Tech Stack: Python + FastAPI + PostgreSQL
- Platform: Web only
- Deployment: Docker on AWS

## Preferences
- Prefer simplicity over features
- Favor proven libraries over cutting-edge
- Prioritize maintainability
```

**Solution 2: Set Defaults**
Add a "Defaults" section to PROJECT.md:
```markdown
## Defaults
- Unless specified, use: React + Node.js + PostgreSQL
- Unless specified, build for: Web platform
- Unless specified, aim for: Quick prototype
```

**Solution 3: Reference Similar Projects**
```markdown
## Reference Projects
- Style: Like Slack (clean, simple)
- Architecture: Like [previous project]
- Complexity: Keep it simple
```

---

## Issue 2: AI Not Asking Enough Questions

### Symptoms
- AI builds something different from what you wanted
- Frequent rework and corrections
- AI makes wrong assumptions

### Causes
- Permission level too high (Level 1)
- AI over-confident in understanding
- Vague requirements

### Solutions

**Solution 1: Lower Permission Level**
```yaml
# PERMISSION_CONFIG.yaml
permission_level: 2  # Switch from 1 to 2
```

**Solution 2: Explicitly Request Clarification**
```
User: "Build a dashboard [CLARIFY FIRST]"
```

**Solution 3: Provide Examples**
```
User: "Build a dashboard like Grafana, but simpler"
```

---

## Issue 3: Permission Checks Too Restrictive

### Symptoms
- AI asks for confirmation on trivial operations
- Workflow feels slow and tedious
- Constant interruptions

### Causes
- Permission level too low (Level 3)
- Too many custom red/yellow lines

### Solutions

**Solution 1: Raise Permission Level**
```yaml
# PERMISSION_CONFIG.yaml
permission_level: 2  # or 1 for more autonomy
```

**Solution 2: Remove Unnecessary Custom Rules**
```yaml
# Remove overly restrictive rules
custom_yellow_lines: []  # Clear custom restrictions
```

**Solution 3: Trust More**
Start with Level 2, upgrade to Level 1 after you're comfortable.

---

## Issue 4: Permission Checks Too Loose

### Symptoms
- AI does things you didn't expect
- Unwanted changes to important files
- Nervous about what AI might do

### Causes
- Permission level too high (Level 1)
- Missing red lines for your specific needs

### Solutions

**Solution 1: Lower Permission Level**
```yaml
permission_level: 2  # Switch from 1 to 2
```

**Solution 2: Add Custom Red Lines**
```yaml
custom_red_lines:
  - modify_production_config
  - delete_user_data
  - send_external_api_calls
```

---

## Issue 5: Context Not Being Saved

### Symptoms
- AI asks same questions every session
- Previous decisions not remembered
- Have to repeat yourself

### Causes
- PROJECT.md not in workspace root
- AI not updating PROJECT.md
- Working in different directories

### Solutions

**Solution 1: Check PROJECT.md Location**
```bash
# Should be in workspace root
ls PROJECT.md

# If not found, create it
python scripts/init_context.py
```

**Solution 2: Explicitly Save Context**
```
User: "Save this decision to PROJECT.md: 
      We're using PostgreSQL, not MongoDB"
```

**Solution 3: Use update_context.py**
```bash
python scripts/update_context.py --add-note "Using PostgreSQL"
```

---

## Issue 6: AI Makes Wrong Technical Choices

### Symptoms
- AI chooses tech stack you don't want
- Architectural decisions don't match your style
- Have to correct technical choices frequently

### Causes
- Missing technical constraints in PROJECT.md
- AI doesn't know your preferences

### Solutions

**Solution 1: Document Tech Preferences**
```markdown
## Technical Constraints
- Backend: Python only (no Node.js)
- Database: PostgreSQL only (no MongoDB)
- Frontend: React (no Vue/Angular)
- Deployment: Docker + AWS (no Heroku)
```

**Solution 2: Provide Reasoning**
```markdown
## Technical Preferences
- PostgreSQL: Team knows it well
- React: Existing codebase uses it
- AWS: Company standard
```

---

## Issue 7: Scope Creep

### Symptoms
- Project keeps growing
- Never feels "done"
- AI keeps suggesting new features

### Causes
- No clear MVP definition
- Missing success criteria
- No boundaries set

### Solutions

**Solution 1: Define MVP Clearly**
```markdown
## MVP (Must Have)
- User login
- Create/read/update/delete posts
- Basic search

## v2 (Nice to Have)
- Comments
- Likes
- Advanced search

## Out of Scope
- Video uploads
- Real-time chat
- Mobile app
```

**Solution 2: Set Time Boundaries**
```markdown
## Timeline
- MVP: 1 week
- Stop adding features after MVP
- Evaluate before building v2
```

---

## Issue 8: AI Too Slow

### Symptoms
- Takes too long to complete tasks
- Overthinking simple problems
- Too much analysis, not enough action

### Causes
- Permission level too low (Level 3)
- AI being too cautious
- Over-clarifying

### Solutions

**Solution 1: Raise Permission Level**
```yaml
permission_level: 1  # Maximum autonomy
```

**Solution 2: Set Speed Expectations**
```markdown
## Preferences
- Speed > Perfection
- Done > Perfect
- Iterate fast, fix later
```

**Solution 3: Use "Quick Prototype" Mode**
```
User: "Build a quick prototype, don't overthink it"
```

---

## Issue 9: AI Too Fast (Reckless)

### Symptoms
- AI breaks things
- Makes changes without thinking
- Skips important steps

### Causes
- Permission level too high (Level 1)
- Missing safety checks
- No testing requirements

### Solutions

**Solution 1: Lower Permission Level**
```yaml
permission_level: 2  # Add more oversight
```

**Solution 2: Require Testing**
```markdown
## Requirements
- All code must have tests
- Run tests before committing
- No deployments without passing tests
```

**Solution 3: Add Safety Red Lines**
```yaml
custom_red_lines:
  - deploy_without_tests
  - modify_database_without_backup
```

---

## Issue 10: Can't Find Scripts

### Symptoms
- Scripts not found when running commands
- Import errors
- Path issues

### Solutions

**Solution 1: Run from Skill Directory**
```bash
cd ~/.openclaw/workspace/skills/context-not-control
python scripts/init_context.py
```

**Solution 2: Use Absolute Paths**
```bash
python ~/.openclaw/workspace/skills/context-not-control/scripts/init_context.py
```

**Solution 3: Add to PATH (optional)**
```bash
export PATH="$PATH:~/.openclaw/workspace/skills/context-not-control/scripts"
```

---

## Getting Help

If you're still stuck:

1. **Check PROJECT.md** - Is it complete?
2. **Check PERMISSION_CONFIG.yaml** - Is the level right?
3. **Review examples.md** - See working examples
4. **Start fresh** - Re-run init_context.py
5. **Ask AI** - "I'm having trouble with X, help me debug"

---

## Best Practices

✅ **Do**
- Fill out PROJECT.md completely
- Start with Level 2, adjust as needed
- Save important decisions to context
- Review AI's work after completion
- Iterate based on real usage

❌ **Don't**
- Leave PROJECT.md empty
- Jump straight to Level 1 without testing
- Ignore permission warnings
- Micromanage every step
- Expect perfection on first try
