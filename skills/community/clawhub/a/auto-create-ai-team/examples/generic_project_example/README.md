# Generic Project Example

This is an example of how the Auto-Create-AI-Team skill works with a generic project.

## Usage

```bash
python3 create_ai_team.py --project-path ./generic_project_example --auto-detect
```

## Expected Output

The skill will create a single internal AI team with the following structure:

```
generic_project_example/
└── ai-team/
    ├── internal-team/
    │   └── team-info/
    │       ├── AI_TEAM_CONFIG.md
    │       └── TEAM_MEMBERS.md
    └── PROJECT_PROGRESS.md
```

## Team Members

For generic projects, the internal AI team includes:
- AI Assistant
- Data Processor  
- Content Generator
- Quality Checker