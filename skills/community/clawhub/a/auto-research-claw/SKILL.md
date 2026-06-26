# AutoResearchClaw

Autonomous research pipeline that turns ideas into papers via literature search, experiments, and LaTeX generation.

## Usage

Start an autonomous research run:
`researchclaw run --topic "Your detailed research topic" --auto-approve`

## Installation

This skill requires Python 3.11+ and various research-specific dependencies.

```bash
cd ~/.openclaw/skills/auto-research-claw
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
./researchclaw setup
```

## Config

Default configuration is stored in `config.arc.yaml`. Bridge mode allows integration with OpenClaw internal tools (sessions, web_fetch, message).
