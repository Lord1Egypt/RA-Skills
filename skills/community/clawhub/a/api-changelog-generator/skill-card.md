## Description: <br>
Generate and maintain API changelogs from OpenAPI/Swagger specs - track endpoints added, removed, deprecated, or modified between versions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API documentation teams use this skill to compare OpenAPI or Swagger specifications, identify breaking and non-breaking API changes, and produce changelogs, migration guides, release notes, and consumer impact summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated changelogs or migration guidance may be inaccurate if the supplied API specifications are stale, incomplete, or untrusted. <br>
Mitigation: Review generated output against trusted source specifications before publishing release notes or migration instructions. <br>
Risk: YAML parsing requires PyYAML when YAML OpenAPI specs are used. <br>
Mitigation: Install PyYAML only from a trusted package source and use JSON specs when YAML support is not needed. <br>
Risk: The skill reads user-chosen local spec paths. <br>
Mitigation: Use trusted spec paths and review commands before running them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Human-readable text, Markdown changelogs and migration guides, JSON summaries, RSS/Atom feed format, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-selected local OpenAPI or Swagger spec files; YAML support depends on PyYAML.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
