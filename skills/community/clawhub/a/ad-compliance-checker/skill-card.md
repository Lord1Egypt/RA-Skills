## Description: <br>
(组合技能) 对电商素材（图片/视频）进行两阶段的合规性审查：API快筛通用风险，再由AI模型结合专属知识库进行广告法深度分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahsbnb](https://clawhub.ai/user/ahsbnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External teams and operators use this skill to review e-commerce ad text, images, and videos for common content risks, advertising-law concerns, platform policy issues, and concrete revision suggestions before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted unreleased ads, videos, or URLs may be processed by downstream review subskills or third-party review services. <br>
Mitigation: Before installing or using the skill, confirm which api-check and video-check skills will run in the environment and whether their data handling is acceptable for privacy and compliance requirements. <br>
Risk: AI-generated compliance findings may miss jurisdiction-specific rules or platform-specific enforcement changes. <br>
Mitigation: Review generated reports with the responsible compliance or legal owner before relying on them for publication decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ahsbnb/ad-compliance-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown compliance review report with risk ratings, detailed findings, and modification suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow may include staged results from api-check or video-check when those subskills are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
