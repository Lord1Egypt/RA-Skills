## Description: <br>
Builds and maintains a personal Obsidian-based knowledge base from articles, papers, repositories, datasets, spreadsheets, and local files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[durugy](https://clawhub.ai/user/durugy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to collect source material into a local markdown wiki, generate Obsidian-friendly source and concept pages, ask questions against the KB, and produce research outputs such as briefs, Marp slide drafts, charts, and health reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch web content, copy local files, clone repositories, and write persistent notes under configured KB folders. <br>
Mitigation: Keep KB roots narrowly scoped, avoid ingesting sensitive private material, and review generated files before relying on them. <br>
Risk: Cloned repositories and extracted external content may contain untrusted or misleading material. <br>
Mitigation: Treat cloned repos and extracted text as untrusted data, preserve provenance, and review suspicious or incomplete entries before synthesis. <br>
Risk: The daily shell wrapper sources runtime configuration from a local .env file. <br>
Mitigation: Use only a trusted .env file and keep tokens, secrets, and private paths out of committed skill artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/durugy/duru-obsidian-kb) <br>
- [Layout Reference](references/layout.md) <br>
- [Phase Plan](references/phase-plan.md) <br>
- [Daily Ops](references/daily-ops.md) <br>
- [prompt-shield-lite dependency](https://github.com/DuruGY/duru-prompt-shield-lite) <br>
- [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) <br>
- [LLM Knowledge Bases reference](https://x.com/karpathy/status/2039805659525644595) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, JSON status output, shell command examples, configuration snippets, and optional chart artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persistent KB files under configured roots, including raw source records, manifests, wiki pages, indexes, outputs, lint reports, Marp drafts, and PNG charts.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence; artifact pyproject.toml says 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
