## Description: <br>
Verify, repair, explain, and generate BibTeX references with Bibverify's DOI-first CLI and MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hylouis233](https://clawhub.ai/user/hylouis233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and agents use Bibverify to validate and repair BibTeX references, generate BibTeX from DOI values, explain source ranking, and review field-level citation changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external bibverify command or MCP tooling. <br>
Mitigation: Before installing, verify that the PyPI bibverify package is the intended package and prefer a virtual environment. <br>
Risk: Generated or updated BibTeX entries could introduce incorrect citation metadata. <br>
Mitigation: Review generated BibTeX changes before replacing originals and do not invent missing bibliographic metadata. <br>
Risk: Local configuration may contain sensitive values such as API keys or personal contact details. <br>
Mitigation: Avoid sharing API keys or sensitive local config values in prompts or outputs. <br>


## Reference(s): <br>
- [Bibverify ClawHub page](https://clawhub.ai/hylouis233/bibverify) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference timestamped backup, updated, and problem-entry files produced by Bibverify.] <br>

## Skill Version(s): <br>
0.2.4 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
