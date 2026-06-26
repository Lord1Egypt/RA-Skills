## Description: <br>
Stress-test designs before they ship: constraints, trade-offs, failure modes, and ADR-worthy decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codenova58](https://clawhub.ai/user/codenova58) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review architecture proposals, major refactors, new services, and ADR-worthy decisions before implementation. It helps clarify goals and constraints, surface risks, compare alternatives, and leave decisions traceable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Architecture review inputs may include sensitive details about trust boundaries, secrets, or supply chain dependencies. <br>
Mitigation: Provide architectural descriptions rather than actual secrets, credentials, or production-sensitive values. <br>
Risk: Review guidance can be incomplete or misleading when goals, constraints, current pain, or alternatives are missing. <br>
Mitigation: Supply goals, non-goals, users, SLAs, constraints, current pain points, and alternatives before acting on recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codenova58/arch-review) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown review notes with summaries, risk lists, mitigations, experiments, and open questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable output; guidance depends on the architecture context provided by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
