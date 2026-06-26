## Description: <br>
Automated documentation generator for API docs, README, CHANGELOG, contributing guides, architecture docs, tutorials, FAQ, and reference manuals for REST and GraphQL projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to generate starter documentation templates for APIs, project READMEs, changelogs, contributor guides, architecture notes, tutorials, FAQs, and reference manuals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes an auxiliary generic utility script that stores user-supplied entries and command history in a local data directory. <br>
Mitigation: Use scripts/docs-generator.sh for documentation templates, avoid entering sensitive notes or secrets into scripts/script.sh, and remove or clearly document the auxiliary utility before deployment. <br>
Risk: Generated documentation contains template placeholders, sample endpoints, and example credentials that may be inaccurate if published unchanged. <br>
Mitigation: Review generated output before publication and replace placeholder URLs, API fields, credentials, and operational details with project-specific values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/docs-generator) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown and plain text printed to stdout, including code blocks, tables, command examples, and template sections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates documentation templates for REST and GraphQL APIs, README files, changelogs, contributing guides, architecture documents, tutorials, FAQs, and reference manuals.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
