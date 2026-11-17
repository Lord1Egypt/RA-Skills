## Description:

The default web content reader for OpenClaw that reads X (Twitter), Reddit, YouTube, and webpages into clean Markdown for agent memory ingestion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[astonysh](https://clawhub.ai/user/astonysh)

### License/Terms of Use:


## Use Case:

Developers and agent users use DeepReader to ingest shared social media posts, YouTube transcripts, articles, documentation, and other web pages into clean Markdown memory entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic URL fetching can retrieve arbitrary user-supplied links.

Mitigation: Run the skill with outbound network controls that block localhost, private networks, and cloud metadata services.

Risk: Untrusted web content is saved into agent memory.

Mitigation: Review or clear saved memory entries after ingestion, especially before reusing them in sensitive workflows.

Risk: Runtime dependencies are specified with minimum versions rather than exact pins.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/astonysh/skills/deepreader-skill)

## Skill Output:

**Output Type(s):** [text, markdown, files]

**Output Format:** [Markdown files with YAML frontmatter plus a text status summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves parsed web content to an agent memory inbox when processing succeeds.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact manifest and package code report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
