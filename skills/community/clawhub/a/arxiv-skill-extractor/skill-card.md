## Description: <br>
Automates the process of extracting reusable skill code from arXiv papers to turn paper insights into actual OpenClaw skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanng-ide](https://clawhub.ai/user/wanng-ide) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to turn arXiv paper content into reusable OpenClaw skill scaffolds. It fetches paper data, extracts key algorithms, and generates skill templates for further review and implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent new OpenClaw skills from externally sourced paper content without a clear sanitization or approval step. <br>
Mitigation: Review each generated SKILL.md, scripts/run.js, and paper.json before enabling or relying on the generated skill, and verify the arxiv-paper-reviews helper it depends on. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanng-ide/arxiv-skill-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Generated OpenClaw skill directory containing SKILL.md, Node.js runner code, paper.json, and JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent local skill files and depends on the arxiv-paper-reviews helper for paper retrieval.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
