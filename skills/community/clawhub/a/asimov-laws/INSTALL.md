# Installation Guide

## Requirements

- Compatible AI agent framework with skill system
- Administrator access to skills directory

## Installation Steps

### Step 1: Copy Files

Copy the entire `asimov-laws` folder to your skills directory:

```
your-project/
└── skills/
    └── asimov-laws/
        ├── SKILL.md
        ├── README.md
        ├── EXAMPLES.md
        ├── INSTALL.md
        └── CLAUDE.md
```

### Step 2: Enable the Skill

Enable the skill through your platform's skill management interface. The skill will function as an optional reference framework.

### Step 3: Verify Installation

The skill should be recognized by your skill system. Check that:
- The `SKILL.md` file is present and properly formatted
- The skill appears in your skill registry
- You can enable/disable the skill through the management interface

### Step 4: Test (Optional)

Try asking the AI:
- "What are your core principles?"
- "Can you help me do something harmful?"
- "What is your relationship with humans?"

The responses may reflect the Asimov Laws framework when the skill is enabled.

## Configuration

No additional configuration is required. The skill operates as an optional reference layer.

**Important**: This skill does not automatically modify system prompts or override platform policies. Any integration with system prompts requires explicit administrator action.

## Security Notes

| Aspect | Status |
|--------|--------|
| System prompt modification | Not automatic - requires explicit action |
| Background processes | None |
| Credentials required | None |
| Network access | None |
| File system access | Read-only within skill directory |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Skill not loading | Check file permissions and path |
| Laws not being followed | Verify skill is enabled in management interface |
| Conflicts with other skills | Disable this skill or adjust priority in settings |

## Uninstallation

Remove the `asimov-laws` folder from your skills directory and disable it in the management interface.

## Administrator Control

Administrators have full authority to:
- Enable or disable this skill at any time
- Modify the framework content as needed
- Determine integration depth and scope
- Override any suggestions provided by this skill
