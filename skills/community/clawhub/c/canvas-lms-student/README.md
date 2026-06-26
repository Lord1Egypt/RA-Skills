# Canvas LMS Student Skill

Read-only Canvas LMS skill bundle for AI agents.

This repository is the publishable skill bundle used by skill installers and registries. The development source lives in the source repository:

- Source repository: <https://github.com/Efan404/canvas-lms-source>

## Install

### skills.sh

```bash
npx skills add Efan404/canvas-lms-student-skill
```

### ClawHub

After the first registry publish, install with:

```bash
npx clawhub install canvas-lms-student
```

### Manual install

```bash
# Claude Code
git clone git@github.com:Efan404/canvas-lms-student-skill.git
cp -r canvas-lms-student-skill ~/.claude/skills/canvas-lms-student

# Codex
cp -r canvas-lms-student-skill ~/.codex/skills/canvas-lms-student
```

## Runtime Requirements

- Python 3.8+
- `canvasapi`
- `requests`
- Canvas API token and base URL

Install Python dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Configuration

Configure using either environment variables or the shared config file:

```bash
export CANVAS_BASE_URL="https://your-school.instructure.com"
export CANVAS_API_TOKEN="your-api-token"
```

Or create:

```json
{
  "base_url": "https://your-school.instructure.com",
  "api_token": "your-api-token"
}
```

at `~/.config/canvas-lms/config.json`.

Get the Canvas API token from:
1. Canvas → Account → Settings
2. Approved Integrations → + New Access Token
3. Copy the generated token immediately

## Typical Prompts

- "List my Canvas courses"
- "Check my homework"
- "Show upcoming assignments"
- "Download lecture PDFs from CS101"
- "Export my deadlines to a calendar"

## Bundle Contents

```
canvas-lms-student-skill/
├── SKILL.md
├── README.md
├── requirements.txt
├── scripts/
└── references/
```

## Related

- Full source monorepo: <https://github.com/Efan404/canvas-lms-source>
- Human CLI package: <https://github.com/Efan404/canvas-lms-source/tree/main/packages/canvas-lms-cli>

## License

MIT License in this GitHub repository. Note that ClawHub republishes published skills under MIT-0 per its registry policy.
