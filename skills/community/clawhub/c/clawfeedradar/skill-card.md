## Description:

Claw RSS Feed Radar is a personal news radar skill that uses a clawsqlite knowledge base and interest clusters to score article candidates and generate personalized RSS/JSON feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ernestyu](https://clawhub.ai/user/ernestyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users with an existing clawsqlite knowledge base use this skill to run personalized news radar jobs against RSS, Hacker News, arXiv, or configured sources, score candidates by interest clusters, and generate feed outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs mutable third-party Python package releases with access to the agent environment.

Mitigation: Pin and review an exact package version, install in an isolated environment, and limit exposed environment variables.

Risk: The runtime may read clawsqlite interest data and access network sources, full-text fetchers, LLM services, and optional git publishing credentials.

Mitigation: Keep JSON sidecars private, restrict allowed sources and credentials at the agent or host level, and disable git publishing unless it is explicitly required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ernestyu/skills/clawfeedradar)
- [clawfeedradar homepage](https://github.com/ernestyu/clawfeedradar)
- [clawfeedradar docs](https://github.com/ernestyu/clawfeedradar/tree/main/docs)
- [clawsqlite](https://github.com/ernestyu/clawsqlite)

## Skill Output:

**Output Type(s):** [JSON, Text, Files]

**Output Format:** [JSON responses with generated RSS XML feeds and JSON sidecar files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include article scores, output paths, warnings, optional summaries, bilingual content, and next-step hints.]

## Skill Version(s):

0.1.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
