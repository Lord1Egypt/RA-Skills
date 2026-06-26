---
name: context-not-control
description: Enable "Context, not Control" workflow - clarify requirements through multi-turn dialogue, reduce rework, and execute with appropriate permission levels. Use when users want AI to take more autonomy, need help clarifying vague requirements, or want to establish trust-based collaboration patterns. Supports three permission levels (Master/Collaborative/Assistant) and automatic context management.
---

# Context, not Control

A skill that transforms how you work with AI - from micromanaging every step to providing context and letting AI make decisions. Inspired by the "Context, not Control" philosophy from the OpenClaw community.

## Core Philosophy

**Traditional approach**: You tell AI exactly what to do, step by step.  
**This approach**: You tell AI what you want to achieve, AI figures out how.

The key insight: AI works best when you give it rich context about your goals, constraints, and preferences - then trust it to execute within appropriate boundaries.

## When to Use This Skill

- Starting a new project with vague requirements
- Want to reduce back-and-forth and rework
- Need AI to take more initiative and make decisions
- Want to establish clear permission boundaries
- Transitioning from "micromanaging AI" to "trusting AI"

## Quick Start

### 1. Initialize Your Context

Run the initialization script to set up your project context and permission level:

```bash
python scripts/init_context.py
```

This creates:
- `PROJECT.md` - Your project context (goals, constraints, preferences)
- `PERMISSION_CONFIG.yaml` - Your permission boundaries

### 2. Set Your Permission Level

Choose one of three levels:

**Level 1 - Master Mode** (Full autonomy)
- AI makes all technical decisions
- Only confirms: spending money, public messages, deleting databases
- Best for: High trust, high risk tolerance

**Level 2 - Collaborative Mode** (Balanced, recommended)
- AI executes most tasks autonomously
- Confirms: money, public messages, important deletions, system changes
- Best for: Most users, balanced control

**Level 3 - Assistant Mode** (High control)
- AI provides suggestions and code
- Confirms: All operations before execution
- Best for: New users, low risk tolerance, learning mode

### 3. Start with Requirements

Instead of detailed specifications, start with what you want:

```
"I need a team chat tool"
```

AI will ask clarifying questions:
- Who is this for?
- What's the core use case?
- Any similar products to reference?
- Technical constraints?
- Time/budget limits?

### 4. Iterate and Execute

AI clarifies → You answer → AI confirms understanding → You approve → AI executes

All clarified requirements are saved to `PROJECT.md` for future reference.

## How It Works

### Requirement Clarification Framework

When you provide a vague requirement, AI uses a structured approach:

1. **Understand the domain** - What type of project is this?
2. **Identify the user** - Who will use this?
3. **Clarify the goal** - What problem does this solve?
4. **Establish constraints** - Technical, time, budget limits?
5. **Set success criteria** - What does "done" look like?
6. **Confirm understanding** - Repeat back what you heard

See `references/clarification-framework.md` for detailed question templates.

### Permission System

The skill automatically checks permissions before executing operations:

```python
# Example: AI wants to delete a file
if permission_check('delete_file', user_permission_level):
    # Ask user for confirmation
else:
    # Execute directly
```

Customize your red/yellow/green lines in `PERMISSION_CONFIG.yaml`.

### Context Management

All clarified requirements are automatically saved to `PROJECT.md`:

- Project goals and constraints
- Technical stack decisions
- Success criteria
- Permission level
- Iteration history

This context is loaded in future conversations, eliminating repeated questions.

## Permission Levels in Detail

### Level 1: Master Mode

**Philosophy**: Maximum autonomy, minimum interruption

**AI can do without asking**:
- Write, test, and deploy code
- Install dependencies and tools
- Modify configurations
- Create/update files
- Make architectural decisions
- Research and learn new technologies

**AI must confirm**:
- Spending money (API calls, services, domains)
- Sending public messages (emails, tweets, posts)
- Deleting databases or critical data
- Restarting production services

**Best for**: Experienced users who trust AI and can handle mistakes

### Level 2: Collaborative Mode (Default)

**Philosophy**: Trust but verify on important operations

**AI can do without asking**:
- Write and test code
- Create/update files
- Research and documentation
- Install development dependencies
- Run tests and checks

**AI must confirm**:
- Spending money
- Sending any external messages
- Deleting important files/data
- Modifying system configurations
- Restarting services
- Installing system-level packages

**Best for**: Most users, balanced approach

### Level 3: Assistant Mode

**Philosophy**: AI suggests, you decide

**AI can do without asking**:
- Provide suggestions and explanations
- Show code examples
- Research information

**AI must confirm**:
- All file operations
- All code execution
- All installations
- All external calls

**Best for**: New users, learning mode, high-stakes environments

## Examples

See `references/examples.md` for detailed examples including:
- Building a chat application from vague requirements
- Migrating a legacy system with unclear scope
- Creating automation tools with evolving needs

See `assets/EXAMPLE_DIALOG.md` for sample conversations.

## Customization

### Custom Permission Rules

Edit `PERMISSION_CONFIG.yaml` to define your own boundaries:

```yaml
permission_level: 2

custom_red_lines:
  - deploy_to_production
  - modify_database_schema
  - send_customer_emails

custom_yellow_lines:
  - install_npm_packages
  - modify_env_files

# Everything else is green (no confirmation needed)
```

### Project Templates

Create custom templates in `assets/` for recurring project types:
- `PROJECT_TEMPLATE_WEBAPP.md`
- `PROJECT_TEMPLATE_API.md`
- `PROJECT_TEMPLATE_AUTOMATION.md`

## Troubleshooting

See `references/troubleshooting.md` for common issues:
- AI asking too many questions
- AI not asking enough questions
- Permission checks too restrictive/loose
- Context not being saved properly

## Scripts Reference

### `init_context.py`
Initialize project context and permission config

```bash
python scripts/init_context.py [--project-name NAME] [--permission-level 1|2|3]
```

### `clarify_requirement.py`
Run requirement clarification dialogue

```bash
python scripts/clarify_requirement.py "I need a chat app"
```

### `permission_check.py`
Check if an operation requires confirmation

```bash
python scripts/permission_check.py --action delete_file --level 2
```

### `update_context.py`
Update project context with new information

```bash
python scripts/update_context.py --add-goal "Support 1000 concurrent users"
```

## Philosophy: Three Modes of AI Usage

### Mode 1: Paintbrush (Micromanagement)
- You specify every detail
- AI is a tool that executes exactly what you say
- Upper limit: Your expertise

### Mode 2: Employee (Delegation)
- You assign tasks with some guidance
- AI follows your preferred patterns
- Still requires oversight

### Mode 3: Master (Autonomy)
- You set goals and constraints
- AI makes decisions and executes
- You review outcomes, not process

This skill helps you transition from Mode 1 → Mode 3 at your own pace.

## Credits

Inspired by the "Context, not Control" philosophy discussed in the OpenClaw community, particularly the experiences shared by contributors who achieved remarkable results by trusting AI with more autonomy.

## Version

1.0.0 - Initial release
