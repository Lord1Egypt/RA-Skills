## Description: <br>
Runs an autonomous research workflow that turns a research topic into paper drafts, LaTeX, experiment code, charts, and citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical writers use this skill to run a 23-stage research pipeline for literature discovery, experimental planning, execution support, analysis, and academic paper generation. The skill is also documented as a compatibility layer for a unified research entry point. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch a broad autonomous command pipeline with auto-approval, local or SSH experiment execution, and weak command/input scoping. <br>
Mitigation: Install only if comfortable with a long autonomous research workflow; start in simulated mode, keep manual approvals enabled, and verify the researchclaw executable source before use. <br>
Risk: The workflow requires sensitive credentials and may send research topics or literature requests to third-party APIs. <br>
Mitigation: Prefer environment variables for API keys and avoid confidential research topics unless third-party API and local retention behavior are acceptable. <br>
Risk: Remote SSH execution can expose host access or credentials if configured carelessly. <br>
Mitigation: Avoid SSH mode unless you control the host and credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jirboy/autonomous-research-jirboy) <br>
- [AutoResearchClaw project](https://github.com/aiming-lab/AutoResearchClaw) <br>
- [AutoResearchClaw integration guide](https://github.com/aiming-lab/AutoResearchClaw/blob/main/docs/integration-guide.md) <br>
- [AutoResearchClaw Chinese tester guide](https://github.com/aiming-lab/AutoResearchClaw/blob/main/docs/TESTER_GUIDE_CN.md) <br>
- [AutoResearchClaw showcase](https://github.com/aiming-lab/AutoResearchClaw/blob/main/docs/showcase/SHOWCASE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, LaTeX, BibTeX, generated experiment files, charts, and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local artifacts such as paper_draft.md, paper.tex, references.bib, charts, and experiment_runs.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
