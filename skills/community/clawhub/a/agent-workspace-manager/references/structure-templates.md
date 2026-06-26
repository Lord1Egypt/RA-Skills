# Workspace Structure Templates

Pre-defined templates for different agent types. Choose the template that best matches the agent's primary function.

## Template 1: Personal Assistant

Best for: Individual productivity, personal knowledge management

```
workspace/
├── MEMORY.md              # Core memory index
├── memory/
│   ├── daily/             # Daily logs and events
│   ├── conversations/     # Important conversations
│   └── events/            # Significant events
├── knowledge/
│   ├── personal/          # Personal information
│   └── reference/         # General reference
├── tasks/
│   ├── active/            # Current tasks
│   └── completed/         # Finished tasks
├── preferences/           # User preferences
└── archives/              # Historical records
```

## Template 2: Project Manager

Best for: Team coordination, project tracking, delivery management

```
workspace/
├── MEMORY.md              # Core memory index
├── memory/
│   ├── meetings/          # Meeting notes
│   ├── decisions/         # Decision records
│   └── milestones/        # Project milestones
├── knowledge/
│   ├── domain/            # Domain knowledge
│   ├── processes/         # Work processes
│   └── team/              # Team information
├── tasks/
│   ├── backlog/           # Pending items
│   ├── sprint/            # Current sprint
│   └── blocked/           # Blocked items
├── decisions/             # Major decisions with rationale
├── templates/             # Project templates
└── archives/              # Completed projects
```

## Template 3: Knowledge Base

Best for: Documentation, research, information storage

```
workspace/
├── MEMORY.md              # Core memory index
├── memory/
│   ├── updates/           # Knowledge updates log
│   └── sources/           # Source tracking
├── knowledge/
│   ├── core/              # Core concepts
│   ├── advanced/          # Advanced topics
│   ├── faq/               # Common questions
│   └── external/          # External references
├── templates/             # Document templates
├── decisions/             # Knowledge structure decisions
└── archives/              # Deprecated knowledge
```

## Template 4: Development Agent

Best for: Coding assistants, technical workflows

```
workspace/
├── MEMORY.md              # Core memory index
├── memory/
│   ├── sessions/          # Work sessions
│   └── issues/            # Issues encountered
├── knowledge/
│   ├── codebase/          # Codebase understanding
│   ├── patterns/          # Design patterns used
│   └── tech-stack/        # Technology details
├── tasks/
│   ├── features/          # Feature development
│   ├── bugs/              # Bug fixes
│   └── refactoring/       # Code improvements
├── decisions/             # Technical decisions
├── preferences/           # Coding preferences
└── templates/             # Code templates
```

## Template 5: Minimal

Best for: Simple agents, starting point

```
workspace/
├── MEMORY.md              # Core memory index
├── memory/                # All memory content
├── knowledge/             # All knowledge
├── tasks/                 # All tasks
└── archives/              # Archived content
```

## Choosing a Template

1. **Identify primary function:** What does this agent do most?
2. **Match to template:** Select the closest match
3. **Customize as needed:** Add/remove directories based on specific needs
4. **Document changes:** Note any modifications for consistency

## Directory Naming Conventions

- Use lowercase letters and hyphens: `my-directory/`
- Be descriptive but concise: `active-tasks/` not `at/`
- Group related items: `knowledge/domain/` not `domain-knowledge/`
- Use consistent depth: Avoid deeply nested structures (>3 levels)
