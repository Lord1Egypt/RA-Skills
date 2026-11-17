## Description:

Autonomous OSINT investigation tool that searches a subject, extracts entities, maps connections into an interactive 3D graph, follows money, detects shell chains, flags suspicious gaps, and expands through cross-links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinndarkblade](https://clawhub.ai/user/sinndarkblade)

### License/Terms of Use:

MIT-0

## Use Case:

Investigators, researchers, journalists, security analysts, and finance teams use this skill to build OSINT investigations around people, companies, money flows, events, and document corpora. It helps collect entities, score relationships, identify gaps and cross-links, and produce investigation summaries and graph artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch and run a full third-party application from a mutable GitHub repository and install Python dependencies.

Mitigation: Run it in a sandbox or dedicated environment, review the upstream repository before first use, and pin the repository revision and dependencies when possible.

Risk: The installed application may have broad local access while building investigations and serving the local board.

Mitigation: Keep investigation workspaces isolated, avoid granting unnecessary file access, and keep the local server bound to localhost.

Risk: Investigations may involve sensitive subjects and can send prompts or data to external AI providers.

Mitigation: Use external providers only when their data policies are acceptable for the investigation, or configure a local provider for sensitive work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sinndarkblade/skills/deepdive-osint)
- [Publisher profile](https://clawhub.ai/user/sinndarkblade)
- [DeepDive homepage](https://github.com/Sinndarkblade/deepdive)
- [DuckDuckGo Search package](https://pypi.org/project/duckduckgo-search/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline Python and shell commands, plus generated investigation data and 3D HTML board files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local investigation directories, JSON graph data, HTML board artifacts, and summaries with confidence-scored findings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
