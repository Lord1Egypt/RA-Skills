# Auto Create AI Team

A simple, transparent Python script that creates organized AI team directory structures for your projects with full internationalization support.

## What it actually does
This tool creates a standardized `ai-team` folder in your project directory containing:
- Team configuration files (internal and/or internet team)
- Project progress tracking file
- Workflow configuration file
- Detailed team member documentation

**Important**: This is a **local file creation tool only**. It does not:
- Make any network requests
- Connect to external services  
- Require API keys or credentials
- Collect or transmit any data

## Installation
No installation required! Just download the script and templates folder, then run it.

## Usage Examples

### Basic usage (single team, Chinese):
```bash
python create_ai_team.py --project-path ./my-project
```

### Dual team mode (English):
```bash
python create_ai_team.py --project-path ./my-project --team-type dual --lang en
```

### Specify project type with custom members:
```bash
python create_ai_team.py --project-path ./my-ecommerce-site --team-type dual --project-type ecommerce --internal-members "CTO,Lead Dev,Dev,QA" --lang en
```

### Mobile app with verbose output:
```bash
python create_ai_team.py --project-path ./my-app --project-type mobile_app --team-type dual --verbose
```

## Command Line Options
| Option | Description | Default |
|--------|-------------|---------|
| `--project-path` | Path to your project directory (required) | - |
| `--team-type` | `single`, `dual`, or `custom` | `single` |
| `--project-type` | `web_app`, `ecommerce`, `mobile_app`, `generic` | `generic` |
| `--lang` | Output language: `zh` or `en` | `zh` |
| `--internal-members` | Custom internal team members (comma-separated) | Project-type defaults |
| `--internet-members` | Custom internet team members (comma-separated) | Project-type defaults |
| `--primary-model` | Primary AI model | `GPT-4` |
| `--fallback-models` | Fallback AI models | `GPT-3.5, Claude` |
| `-v, --verbose` | Enable verbose output | `False` |

## Output Structure

### Single Team Mode
```
project/
└── ai-team/
    ├── team-info/
    │   ├── AI_TEAM_CONFIG.md
    │   └── TEAM_MEMBERS.md
    ├── PROJECT_PROGRESS.md
    └── WORKFLOW.md
```

### Dual Team Mode
```
project/
└── ai-team/
    ├── internal-team/team-info/
    ├── internet-team/team-info/
    ├── PROJECT_PROGRESS.md
    └── WORKFLOW.md
```

## Features

### Internationalization
- Full Chinese (zh) and English (en) support
- Language-aware team member names
- Translated UI text and labels

### Template Engine
- Built-in simple template engine (no dependencies)
- Supports variables and conditionals
- Customizable templates in `templates/` folder

### Flexible Configuration
- Project-type-specific default team members
- Custom member configuration via CLI
- Default config file support

## Security & Privacy
- **100% offline**: No network connectivity whatsoever
- **Local files only**: Only creates files in your specified project directory
- **No dependencies**: Uses only Python standard library
- **Fully auditable**: All code is in the `create_ai_team.py` file
- **No hidden functionality**: What you see is exactly what it does

## Requirements
- Python 3.6 or higher
- No additional packages needed

## License
MIT License
