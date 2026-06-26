## Description: <br>
Securitysuite is a comprehensive agent security platform with seven endpoints for scanning text for prompt injection, auditing SKILL.md files, generating security reports, browsing known attack patterns, and batch-auditing multiple skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to run a local FastAPI service that scans AI-agent text and SKILL.md content for prompt injection, malware-like patterns, scope issues, and security reporting across one or more skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local audit server that receives complete skill files and text inputs. <br>
Mitigation: Keep the service bound to localhost and avoid submitting secrets or proprietary material. <br>
Risk: Batch mode can send multiple full skill files to the running service. <br>
Mitigation: Check whether the service logs request bodies and sanitize inputs before using batch audits. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mirni/gh-securitysuite) <br>
- [Publisher Profile](https://clawhub.ai/user/mirni) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, guidance] <br>
**Output Format:** [JSON API responses with risk scores, verdicts, findings, severity ratings, summaries, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Input limits are 100,000 characters for text scans, 500,000 characters for a single skill audit, and up to 100 skills for batch audit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
