## Description:

Generate a Chinese guided-reading edition for an academic paper from a user-provided paper PDF, URL, text excerpt, abstract, or LaTeX source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1587causalai](https://clawhub.ai/user/1587causalai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and researchers use this skill to turn a paper PDF, URL, abstract, text excerpt, or LaTeX source into a Chinese guided-reading document with a reading path, section guides, concepts, figure and table notes, claims, limitations, and review questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-provided academic paper content, which may include unpublished or sensitive research material.

Mitigation: Provide only paper content that is appropriate for the agent to process, and avoid credentials or confidential material unless the environment is approved for it.

Risk: Partial, unreadable, or broken paper inputs can lead to incomplete or misleading guide content.

Mitigation: Label partial guides clearly, document missing sections in the report, and avoid claiming coverage of sections that were not available.

Risk: A guided-reading document could drift into excessive translation or reproduction of copyrighted paper text.

Mitigation: Keep quotations short and necessary, focus on explanation and structure, and avoid full-paper translation unless the user has the rights and explicitly requests it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1587causalai/skills/add-chinese-guides-to-paper-sections)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guide document, optionally accompanied by HTML or a coverage report when requested or needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default deliverable is paper-guide.zh.md; partial inputs should be labeled and missing coverage should be reported.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
