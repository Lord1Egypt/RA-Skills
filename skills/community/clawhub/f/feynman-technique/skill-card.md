## Description: <br>
Guides an agent through a Feynman Technique audit to test whether a user can explain, diagnose gaps in, and refine understanding of a specific concept. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to check whether understanding of a specific concept is genuine rather than surface-level. It produces a structured audit that captures the initial explanation, gap diagnosis, sources consulted, refined explanation, analogy checks, and a summary judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may include sensitive personal, business, or proprietary details when adding real observed failure patterns, examples, or audit notes. <br>
Mitigation: Sanitize or omit sensitive details before adding examples or sharing outputs. <br>
Risk: A refined explanation can remain misleading if gaps are filled from weak summaries or unsupported assumptions. <br>
Mitigation: Use primary sources for each diagnosed gap and keep the specific unanswered question attached to the source that clarified it. <br>


## Reference(s): <br>
- [Primary sources for the Feynman Technique skill](references/sources.md) <br>
- [Feynman and the Challenger O-Ring Investigation example](examples/feynman-challenger-o-ring-1986.md) <br>
- [Surely You're Joking, Mr. Feynman!](https://archive.org/details/surelyyourejoki00feyn) <br>
- [The Feynman Lectures on Physics](https://www.feynmanlectures.caltech.edu/) <br>
- [Rogers Commission Appendix F](https://science.ksc.nasa.gov/shuttle/missions/51-l/docs/rogers-commission/Appendix-F.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown with a structured Feynman Understanding Audit template and stepwise coaching prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution, tools, MCP servers, or credential inputs are requested by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
