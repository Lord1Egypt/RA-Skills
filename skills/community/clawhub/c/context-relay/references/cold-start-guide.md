# Cold Start Guide

Cold start procedures for various scenarios to ensure Agents can quickly restore context in a memory-less state.

## Core Principle

**Never assume any memory.**

On every startup:
1. Read files → Understand context
2. Verify understanding → Confirm correctness
3. Begin work

## Scenario 1: Main Session Restart

**Triggers**:
- Application restart
- Session timeout disconnection
- Manual restart

**Cold Start Procedure**:

```
Step 1: Read project context
├── Read PROJECT.md → Understand project identity
├── Read state.json → Understand current progress
├── Read todos.json → Understand pending tasks
└── If background needed → Read decisions.md

Step 2: Verify and synchronize
├── Check last_update in state.json
├── Check last_review in todos.json
├── If > 24 hours → Perform todo review
└── Check for any blocked items needing attention

Step 3: Report to user
└── "I see we are working on [current_task],
     last updated on [last_update].
     Current progress: [completed]/[total]
     Shall we continue?"
```

**Example**:

```
[Agent starts]
→ Read PROJECT.md: User Authentication System
→ Read state.json:
   {
     "current_task": "Implement login endpoint",
     "progress": {
       "completed": ["Database design"],
       "in_progress": "Login endpoint (70%)"
     },
     "last_update": "2026-04-20T18:00:00+08:00"
   }

[Agent output]
"I see we are developing the user authentication system, last worked on yesterday at 6 PM.
 Currently implementing the login endpoint, 70% complete.
 Would you like to continue?"
```

## Scenario 2: Sub-Agent Startup

**Triggers**:
- Parent agent spawns child agent
- Child agent has no parent session memory

**Cold Start Procedure**:

```
Step 1: Read context prepared by parent agent
├── Read state.json → Understand delegated task
├── Check delegated_to and expected_output
└── Check input_files or other inputs

Step 2: Execute task
├── Complete delegated work
├── Generate output
└── Update state.json (results, output files)

Step 3: End
└── Parent agent will read results
```

**Example**:

```
[Parent agent preparation]
state.json:
{
  "delegated_to": "code-reviewer",
  "task": "Review code quality in src/auth/*.py",
  "expected_output": "Review report (markdown)"
}

[Child agent starts]
→ Read state.json
→ Understand task: Review Python code in src/auth/ directory
→ Perform review
→ Generate report: docs/reviews/auth-2026-04-20.md
→ Update state.json:
   {
     "result": "Review complete, found 3 issues",
     "report_file": "docs/reviews/auth-2026-04-20.md"
   }

[Parent agent continues]
→ Read state.json results
→ Read review report
→ Decide next steps
```

## Scenario 3: Cron Task Startup

**Triggers**:
- Scheduled task triggers
- Heartbeat check

**Cold Start Procedure**:

```
Step 1: Read context
├── Read PROJECT.md → Understand project identity
└── Read state.json → Understand current state

Step 2: Execute scheduled task
├── Check project status
├── Perform scheduled operation
└── Update state.json

Step 3: Notify (if needed)
└── Send notification via message tool
```

**Example (Daily Health Check)**:

```
[Cron triggers: Daily 09:00]
→ Read PROJECT.md: User Authentication System
→ Read state.json:
   {
     "phase": "development",
     "last_update": "2026-04-19T18:00:00+08:00"
   }

[Perform check]
→ Check for any blocked items
→ Check if todos need updating
→ Update state.json:
   {
     "last_check": "2026-04-20T09:00:00+08:00",
     "health_status": "ok"
   }

[Notify if needed]
→ Send message: "Project status normal, 1 todo currently in_progress"
```

## Scenario 4: New Project Initialization

**Triggers**:
- First time entering a project
- Project lacks context files

**Cold Start Procedure**:

```
Step 1: Detect context files
├── Check if PROJECT.md exists
└── If not → Ask user if they want to initialize

Step 2: Create initial files
├── Run init_context.py
├── Guide user to fill in PROJECT.md
├── Initialize state.json
└── Create empty decisions.md and todos.json

Step 3: Confirm understanding
└── Confirm with user that project understanding is correct
```

**Example**:

```
[Agent detects]
→ PROJECT.md does not exist

[Agent output]
"It looks like this is a new project. I can help create context files
 so I can remember project information across future sessions.
 
 Would you like to create them? If so, please tell me:
 1. Project name and description
 2. Tech stack
 3. Main objectives"
```

## Scenario 5: Multi-Project Switching

**Triggers**:
- User switches between multiple projects
- Agent needs to identify current project

**Cold Start Procedure**:

```
Step 1: Identify project
├── Check current working directory
├── Look for PROJECT.md
└── If found → Read project context

Step 2: Load project state
├── Read state.json
└── Switch to that project context

Step 3: Confirm
└── Confirm current project with user
```

**Example**:

```
[User switches directory]
User: cd /path/to/project-b

[Agent detects]
→ Found PROJECT.md
→ Read project info: project-b (E-commerce Backend)

[Agent output]
"Switched to the E-commerce Backend project.
 Current state: Development phase
 In progress: Order module development
 Shall we continue?"
```

## Quick Checklist

Confirm the following on every cold start:

- [ ] PROJECT.md has been read
- [ ] state.json has been read
- [ ] todos.json has been read
- [ ] Current phase and task are understood
- [ ] Next steps are known
- [ ] Understanding has been confirmed with user

## Common Mistakes

### Mistake 1: Assuming Memory

❌ **Incorrect**:
```
"I'll continue implementing the login endpoint..."  // Assuming memory of last task
```

✅ **Correct**:
```
[First read state.json]
"I see we are implementing the login endpoint, 70% complete.
 Before continuing, please confirm this is correct."
```

### Mistake 2: Ignoring Files

❌ **Incorrect**:
```
[Start working immediately without reading any files]
```

✅ **Correct**:
```
[Read on startup]
PROJECT.md → state.json → todos.json
[Then begin work]
```

### Mistake 3: Not Updating Timely

❌ **Incorrect**:
```
[Work finishes, state.json is not updated]
```

✅ **Correct**:
```
[Update immediately after work finishes]
state.json → Record progress
todos.json → Update todo status
```

## Template Script

Use `init_context.py` to quickly initialize project context:

```bash
python init_context.py /path/to/project

# Creates the following files:
# - PROJECT.md (template)
# - state.json (initial state)
# - decisions.md (empty file)
# - todos.json (empty list)
```