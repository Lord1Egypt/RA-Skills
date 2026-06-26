# AskUserQuestion Usage Patterns

## When to Use

1. **Decision needed** - Multiple options require selection
2. **Confirmation needed** - User consent before risky actions
3. **Next step suggestion** - Post-completion follow-up selection
4. **Ambiguous requirements** - Don't guess, ask

## Writing Rules

```typescript
AskUserQuestion({
  questions: [{
    question: "Clear and specific question?",
    header: "Short label",  // max 12 chars
    options: [
      { label: "Option name", description: "Consequence of this choice" },
      // 2-4 options, recommended first + "(Recommended)"
    ],
    multiSelect: false  // true if multiple selection needed
  }]
})
```

## Common Patterns

### Distribution Selection

```json
{
  "questions": [{
    "question": "Where should this automation be deployed?",
    "header": "Distribution",
    "options": [
      {"label": "Open Source", "description": "Publish to claudemarketplaces.com"},
      {"label": "Team/Project", "description": "Git commit, share with team"},
      {"label": "Personal (Recommended)", "description": "Save to ~/.claude/"}
    ],
    "multiSelect": false
  }]
}
```

### Trigger Selection

```json
{
  "questions": [
    {
      "question": "When should this feature run?",
      "header": "Trigger",
      "options": [
        {"label": "Automatic (context-based)", "description": "Auto-activate on specific file/keyword detection"},
        {"label": "Manual (command)", "description": "User runs /command directly"},
        {"label": "Event reaction", "description": "On file save, commit, or other events"}
      ],
      "multiSelect": false
    },
    {
      "question": "Where will you use this?",
      "header": "Scope",
      "options": [
        {"label": "All projects (Recommended)", "description": "Global install as personal workflow"},
        {"label": "This project only", "description": "For team sharing, include in Git"}
      ],
      "multiSelect": false
    }
  ]
}
```

### Type Selection

```json
{
  "questions": [{
    "question": "Which approach fits best?",
    "header": "Type Selection",
    "options": [
      {"label": "Skill", "description": "Auto-activation, instruction-based response improvement"},
      {"label": "Agent", "description": "Autonomous execution, multi-step task delegation"},
      {"label": "Hook", "description": "Event-based, automatic shell command execution"}
    ],
    "multiSelect": false
  }]
}
```

### Automation Candidates (from conversation analysis)

```json
{
  "questions": [{
    "question": "Found these automation opportunities. Which to implement?",
    "header": "Candidates",
    "options": [
      {"label": "[Pattern 1]", "description": "Brief description of what it automates"},
      {"label": "[Pattern 2]", "description": "Brief description"},
      {"label": "All of above", "description": "Create multiple automations"}
    ],
    "multiSelect": true
  }]
}
```

## Patterns to Include in Generated Automations

```markdown
## User Interaction

Use AskUserQuestion in situations requiring decisions:
- Selection between multiple approaches
- Confirmation before risky operations
- Suggest next steps after completion
```

## Avoid

- Don't proceed with guesses
- Don't list options as long text (use AskUserQuestion)
- Don't proceed with risky operations without user response
