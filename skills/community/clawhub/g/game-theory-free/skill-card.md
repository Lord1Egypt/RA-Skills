## Description: <br>
This skill helps agents perform qualitative game-theory analysis of crypto and Web3 protocols using Five Questions modeling, common crypto game patterns, and basic red-flag checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, protocol designers, and reviewers can use this skill to structure early analysis of incentives, equilibrium behavior, governance capture risk, MEV exposure, and related mechanism-design concerns in crypto protocols. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security verdict is suspicious because the skill requests shell execution and mentions callback URLs without clear data-handling limits. <br>
Mitigation: Review the skill before installation, run it where shell execution is disabled or explicitly approved, and avoid callback URLs unless their data exposure is understood. <br>
Risk: The skill provides qualitative game-theory risk analysis and is not a substitute for a formal security audit. <br>
Mitigation: Use its findings as preliminary review input and validate protocol risks through dedicated security, economic, and governance review processes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/game-theory-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or structured text with qualitative analysis and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-shaped summaries when requested by the calling agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
