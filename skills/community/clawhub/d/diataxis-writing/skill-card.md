## Description: <br>
Diataxis documentation framework practice guide that provides diagnosis, classification, templates, and quality assessment for four documentation types: Tutorial, How-to Guide, Reference, and Explanation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amumulam](https://clawhub.ai/user/amumulam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, technical writers, and documentation maintainers use this skill to classify documentation needs, draft Diataxis-aligned tutorials, how-to guides, reference material, and explanations, and assess documentation quality before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated documentation may be saved locally or published to external services without enough destination clarity. <br>
Mitigation: Confirm the target platform, destination path or repository, document visibility, and permissions before using any non-chat output method. <br>
Risk: Sensitive or private content may persist outside the conversation when sent to Feishu, GitHub, Notion, Google Docs, or local files. <br>
Mitigation: Prefer chat output for sensitive content, and review the generated document before allowing any persistent or external output. <br>
Risk: External publishing paths depend on MCP, mcporter, git, and configured service credentials. <br>
Mitigation: Run the tool availability check first and verify that configured credentials and integrations match the intended workspace or account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amumulam/diataxis-writing) <br>
- [Diataxis official documentation](https://diataxis.fr) <br>
- [Diataxis documentation framework repository](https://github.com/evildmp/diataxis-documentation-framework) <br>
- [Diataxis Compass](references/compass.md) <br>
- [Four Documentation Types](references/four-types.md) <br>
- [Quality Framework](references/quality-framework.md) <br>
- [Output Platform Reference](references/output-platforms.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with prose, checklists, templates, and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce chat responses, local Markdown files, or externally published documents when the user selects and confirms an available output method.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence and CHANGELOG, released 2026-02-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
