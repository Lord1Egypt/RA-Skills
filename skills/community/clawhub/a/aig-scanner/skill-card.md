## Description: <br>
AIG Scanner submits and checks authorized A.I.G security scans for AI infrastructure, AI tools and skills, agents, and LLM jailbreak evaluation through Tencent Zhuque Lab AI-Infra-Guard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aigsec](https://clawhub.ai/user/aigsec) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security engineers use this skill to submit authorized scans to a configured A.I.G server, check scan progress, and review formatted security results for AI services, tool or skills projects, saved agents, and model jailbreak evaluations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate scans against local, private-network, or third-party targets. <br>
Mitigation: Use it only for authorized testing and confirm permission for each target before running a scan. <br>
Risk: Targets, model tokens, API keys, and local archives may be sent to the configured A.I.G server. <br>
Mitigation: Set AIG_BASE_URL only to a trusted server, use limited-scope credentials, and upload private archives only when they are intended for analysis by that server. <br>
Risk: Scan submission and result polling depend on environment configuration and short polling windows. <br>
Mitigation: Configure AIG_BASE_URL before use and retain returned session IDs so results can be checked later when a scan continues after the initial polling window. <br>


## Reference(s): <br>
- [AIG Scanner on ClawHub](https://clawhub.ai/aigsec/aig-scanner) <br>
- [Tencent AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text and Markdown-formatted scan status, findings, links, screenshots, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include session IDs, security scores, finding summaries, attachment links, and screenshot links returned by the configured A.I.G server.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
