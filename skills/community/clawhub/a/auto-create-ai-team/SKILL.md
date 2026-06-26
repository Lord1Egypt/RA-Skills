# Auto Create AI Team

## Description
Creates AI team directory structures for projects with full internationalization support (Chinese/English). This is a standalone Python script that generates organized team folders and configuration files locally using a template engine.

## Usage
```bash
python create_ai_team.py --project-path /path/to/project [options]
```

### Basic Examples
```bash
# Create single team with default settings (Chinese)
python create_ai_team.py --project-path ./my-project

# Create dual team for web app (English)
python create_ai_team.py --project-path ./my-project --team-type dual --project-type web_app --lang en

# Create with custom team members
python create_ai_team.py --project-path ./my-project --internal-members "CTO,Lead Dev,Dev,QA" --lang en
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--project-path` | Path to the project directory (required) | - |
| `--team-type` | `single`, `dual`, or `custom` | `single` |
| `--project-type` | `web_app`, `ecommerce`, `mobile_app`, `generic` | `generic` |
| `--lang` | Output language: `zh` (Chinese) or `en` (English) | `zh` |
| `--internal-members` | Comma-separated list of internal team members | Project-type defaults |
| `--internet-members` | Comma-separated list of internet team members | Project-type defaults |
| `--primary-model` | Primary AI model name | `GPT-4` |
| `--fallback-models` | Comma-separated fallback models | `GPT-3.5, Claude` |
| `--log-file` | Path to log file | None |
| `--verbose`, `-v` | Enable verbose output | False |

## Features

### Template Engine
- Simple template engine built-in (no external dependencies)
- Supports variable substitution: `{{variable}}`
- Supports conditionals: `{% if variable == "value" %}...{% endif %}`
- Supports elif/else branches

### Internationalization (i18n)
- Full Chinese and English support
- Translated UI text and team role names
- Language-aware default team members

### Configuration Inheritance
- Reads default settings from `templates/default_config.json`
- CLI arguments override default configuration

### Output Structure

#### Single Team Mode
```
project/
└── ai-team/
    ├── team-info/
    │   ├── AI_TEAM_CONFIG.md
    │   └── TEAM_MEMBERS.md
    ├── PROJECT_PROGRESS.md
    └── WORKFLOW.md
```

#### Dual Team Mode
```
project/
└── ai-team/
    ├── internal-team/
    │   └── team-info/
    │       ├── AI_TEAM_CONFIG.md
    │       └── TEAM_MEMBERS.md
    ├── internet-team/
    │   └── team-info/
    │       ├── INTERNET_TEAM_CONFIG.md
    │       └── TEAM_MEMBERS.md
    ├── PROJECT_PROGRESS.md
    └── WORKFLOW.md
```

### Project Type Defaults

| Project Type | Internal Team (CN) | Internal Team (EN) |
|--------------|-------------------|-------------------|
| web_app | 产品经理, 前端开发工程师, 后端开发工程师, QA测试工程师, UI/UX设计师 | Product Manager, Frontend Developer, Backend Developer, QA Engineer, UI/UX Designer |
| ecommerce | 技术架构师, 全栈开发工程师, UI设计师, 支付集成专家, QA工程师 | Technical Architect, Full-stack Developer, UI Designer, Payment Integration Specialist, QA Engineer |
| mobile_app | 移动端开发工程师, 后端工程师, UI/UX设计师, QA工程师, DevOps工程师 | Mobile Developer, Backend Engineer, UI/UX Designer, QA Engineer, DevOps Engineer |
| generic | AI助手, 数据处理专员, 内容创作者, 质量审核员, 项目协调员 | AI Assistant, Data Processor, Content Creator, Quality Checker, Project Coordinator |

## Requirements
- Python 3.6+
- No external dependencies (uses only standard library)

## Security
- **Completely offline**: No network calls, API requests, or external data transmission
- **Local file operations only**: Only reads/writes files in the specified project directory
- **No credentials required**: Does not require or store any authentication tokens or API keys
- **Fully transparent**: All functionality is contained in the `create_ai_team.py` file
- **No environment variables**: All configuration is done via command line arguments

## Files

| File | Purpose |
|------|---------|
| `create_ai_team.py` | Main script with template engine and i18n support |
| `error_handler.py` | Error handling utilities |
| `templates/default_config.json` | Default configuration values |
| `templates/progress_template.md` | Project progress template |
| `templates/workflow_template.md` | Workflow configuration template |
| `templates/team_config_template.md` | Team configuration template |
| `templates/team_members_template.md` | Team members template |

## Version
v2.0 - Enhanced version with template engine, i18n, and improved output
