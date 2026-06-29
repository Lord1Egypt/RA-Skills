## Description: <br>
Generate a Chinese guided-reading edition for an academic paper from a user-provided paper PDF, URL, text excerpt, abstract, or LaTeX source. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1587causalai](https://clawhub.ai/user/1587causalai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and researchers use this skill to turn academic paper content they provide into a Chinese guided-reading document with a reading path, section guide, key concepts, figures and tables notes, claims, limitations, and review questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be implicitly invoked and produces Chinese output by default. <br>
Mitigation: Use it when the user asks for a Chinese paper guide, reading scaffold, or section-by-section guided-reading document. <br>
Risk: Partial, broken, or unavailable paper content can lead to incomplete or overconfident guidance. <br>
Mitigation: Label partial guides clearly, document missing sections in guide-report.md, and avoid claiming to have read unavailable content. <br>
Risk: Generated guides may overuse copyrighted paper text if treated as translation output. <br>
Mitigation: Keep direct quotations short and necessary, and produce a guided-reading document rather than a full translation unless the user has rights and explicitly requests it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guide, with optional HTML when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default deliverable is paper-guide.zh.md; guide-report.md records input coverage, assumptions, and missing parts.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
