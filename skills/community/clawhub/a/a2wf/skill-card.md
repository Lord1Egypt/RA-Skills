## Description:

Validate, generate, and audit A2WF siteai.json files for website AI-agent governance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wolfuser45](https://clawhub.ai/user/wolfuser45)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to create, validate, and review siteai.json policies that describe how AI agents may interact with a website.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live website audit examples may imply URL-based network auditing, while the authoritative security evidence says normal validation is offline and audit documentation is not fully aligned with the script implementation.

Mitigation: Use web_fetch to retrieve a site's siteai.json first, then run local validation; treat URL audit examples as guidance unless the implementation is separately confirmed.

## Reference(s):

- [A2WF Homepage](https://a2wf.org)
- [A2WF Specification](https://a2wf.org/specification/)
- [A2WF Core v1.0 Schema](https://a2wf.org/schema/core-v1.0.json)
- [A2WF GitHub Specification](https://github.com/a2wf/spec)
- [A2WF Agent Implementer's Guide](references/implementer-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/wolfuser45/skills/a2wf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON siteai.json output, and structured validation or audit reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated siteai.json content is written to stdout or to a requested file; validation exits 0 for valid documents and 1 for invalid documents.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
