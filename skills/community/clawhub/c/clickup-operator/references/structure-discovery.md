# ClickUp Structure Discovery

This is a core setup step for the skill.

The user may already have a working ClickUp structure. Do not assume the skill should impose a new one.

## Goal

Teach the agent to learn the user's existing ClickUp language and routing model before acting at full speed.

That means discovering:

- which space is the main operating area
- which lists hold general to-dos
- which lists hold ideas
- which lists are project-specific
- which people should be default assignees
- which phrases the user naturally uses for different buckets of work

## Important principle

The setup is not only technical auth plus IDs.

It is also:

- structure discovery
- language mapping
- routing preference discovery

That is what turns a generic ClickUp connection into an actually useful operator skill.

## What the agent should learn

### Workspace and space

- Which workspace should the agent operate in by default?
- Which space is the main home base?

### General task bucket

- Where should general to-dos, reminders, and one-off action items go?
- Should they be auto-assigned?
- Should they get a due date by default?

### Ideas bucket

- Where should uncategorized ideas go?
- Should ideas stay unassigned by default?
- Should ideas stay undated by default?

### Project routing

- When the user names a project, where should that work go?
- Are projects organized as lists, folders, spaces, or some other pattern?
- Should project-contained items avoid auto-assignment and auto-dating unless requested?

### Language mapping

The agent should explicitly learn the user's natural phrases, for example:

- "make a note of this"
- "put this in the website project"
- "add this to my to-do list"
- "this belongs in X"

The key is not literal phrase matching.
The key is understanding what bucket those phrases imply in the user's system.

### Naming / shorthand

The agent should also learn shorthand references, for example:

- "my task list"
- "ideas"
- "website project"
- "that client"

If the user has internal nicknames for lists or projects, those should be captured during setup.

## Best setup flow

1. connect ClickUp
2. inspect the real workspace hierarchy
3. ask targeted questions about how the user organizes work
4. map their language to actual destination lists/projects
5. save those routing defaults in config
6. run a small smoke test

## Product implication

This discovery step is part of the product value.

The skill should not feel like:

- "paste in some IDs and good luck"

It should feel like:

- "the agent learns how your ClickUp is already organized, then operates inside it correctly"
