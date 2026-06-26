## Description: <br>
Scans AI skills for potential security risks and unsafe commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thenox21](https://clawhub.ai/user/thenox21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill for first-pass local static checks of AI skill code, scanning piped source text for dangerous or suspicious patterns and returning a structured risk report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A SAFE result can miss obfuscated code, unlisted APIs, and broader agentic risks. <br>
Mitigation: Treat scanner output as advisory and perform manual review before using sensitive or high-impact skills. <br>
Risk: Pattern-based matching can produce incomplete or noisy findings. <br>
Mitigation: Review each reported pattern in source context and update rules.json when new risky patterns are identified. <br>


## Reference(s): <br>
- [ClawShield Lite ClawHub listing](https://clawhub.ai/thenox21/clawshield-lite) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, json, guidance] <br>
**Output Format:** [JSON security report printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a risk_level and issue list from pattern-based static scanning; results are advisory and require human review for sensitive use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
