# anime-download-skill

OpenClaw skill for searching and downloading anime torrents from miobt.com.

## Install

```bash
clawhub install anime-download-skill
```

## Usage

Once loaded, ask the agent:

- "搜索 JOJO 的动漫资源"
- "帮我下载最新一集鬼灭之刃"
- "看看这个季度有哪些新番"

## Requirements

- [uv](https://docs.astral.sh/uv/) — for `uvx` zero-install execution
- Or `pipx install anicatch` as fallback

## Other Platforms

Also works with Claude Code, Cursor, Gemini CLI, or any agent supporting the [AgentSkills.io](https://agentskills.io) standard:

```bash
# Claude Code
clawhub install anime-download-skill --dir ~/.claude/skills

# Manual install
git clone https://github.com/isongxw/anime-download-skill.git ~/.agents/skills/anime-download-skill
```

## Related

- [anicatch](https://github.com/isongxw/anicatch) — the underlying CLI tool
- [anicatch on PyPI](https://pypi.org/project/anicatch/)
- [ClawHub](https://clawhub.ai) — skill marketplace
