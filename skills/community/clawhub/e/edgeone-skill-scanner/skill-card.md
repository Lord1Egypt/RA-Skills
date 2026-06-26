## Description: <br>
Scans agent skills locally for security risks before installation or use, using Tencent Zhuque Lab A.I.G static analysis guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aigsec](https://clawhub.ai/user/aigsec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to perform local static security reviews of one or more agent skills before installing, enabling, or trusting them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports that one review helper can default to a nested review mode that bypasses normal sandbox and approval protections. <br>
Mitigation: Review the helper command before use and prefer the no-yolo option unless a full-access nested review is explicitly intended. <br>
Risk: Static analysis reports are limited to the discovered files and the current release, so future updates or runtime behavior may introduce different risks. <br>
Mitigation: Re-scan the skill after updates and review findings before installation or deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/aigsec/edgeone-skill-scanner) <br>
- [Tencent AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown security report with verdicts, findings, recommendations, and summary tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Language follows the triggering user message; analysis is based on static review of the current skill files.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
