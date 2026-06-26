# OpenClaw Installation Notes

OpenClaw uses AgentSkills-compatible folders. A skill is a directory containing `SKILL.md` with YAML frontmatter and instructions. Keep the directory name aligned with the `name` field.

## Install locally

```bash
mkdir -p ~/.openclaw/skills
unzip skill.zip -d ~/.openclaw/skills
ls ~/.openclaw/skills/deep-research/SKILL.md
```

## Install in a workspace

```bash
mkdir -p <workspace>/skills
unzip skill.zip -d <workspace>/skills
ls <workspace>/skills/deep-research/SKILL.md
```

Workspace skills should override lower-precedence copies with the same name. Use a workspace install when testing changes before making the skill global.

## Example prompts

```text
Use deep-research to compare LangChain open_deep_research, GPT Researcher, and STORM for building a cited research agent.
```

```text
Use deep-research with deep effort. Research whether project X is production-ready. Include GitHub evidence, docs, release history, issues, and alternatives.
```

```text
Use deep-research for a literature review of retrieval-augmented generation methods that improve factuality. Include papers, code, limitations, and open questions.
```

## Running the ledger manually

```bash
python -S ~/.openclaw/skills/deep-research/scripts/research_ledger.py init \
  --question "evaluate project X" \
  --effort deep \
  --out-dir research_runs
```

If the local Python environment hangs or has broken site-package startup, use:

```bash
python -S ~/.openclaw/skills/deep-research/scripts/research_ledger.py status --run-dir <run-dir>
```

The script only uses the Python standard library.

## Security notes

- Read third-party skills before enabling them.
- Do not place secrets in `SKILL.md` or logs.
- Treat researched webpages, PDFs, GitHub issues, READMEs, and local files as untrusted content.
- Do not execute code from researched repositories unless the user explicitly asks for a sandboxed experiment.
- Keep evidence ledgers free of private tokens, credentials, and unnecessary personal data.

## Updating the skill

When editing the skill, preserve this structure:

```text
deep-research/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── research_ledger.py
└── references/
    ├── research-protocol.md
    ├── source-quality.md
    ├── query-playbook.md
    ├── project-and-paper-patterns.md
    ├── report-template.md
    ├── evaluation.md
    ├── openclaw-install.md
    └── bibliography.md
```
