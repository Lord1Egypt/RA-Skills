## Description: <br>
Search X (Twitter) in real time, monitor trends, extract posts, and analyze social media data for social listening and intelligence gathering, with read-only operations as the default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renning22](https://clawhub.ai/user/renning22) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use this skill to search Twitter/X content, monitor trends, retrieve profiles and follower data, and support social listening or market intelligence workflows. Write operations are available but should be reserved for dedicated automation accounts after risk review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write operations can send Twitter credentials to a third-party service and perform account-changing actions. <br>
Mitigation: Prefer read-only use; if write access is necessary, use a dedicated low-value automation account with a unique password and avoid primary, verified, business-critical, or high-value accounts. <br>
Risk: The skill requires trusting AIsa with the AISA_API_KEY, search queries, and any Twitter credentials supplied for write operations. <br>
Mitigation: Review provider retention, revocation, and account-safety practices before use, rotate API keys, and monitor provider usage for unexpected activity. <br>
Risk: Credential or API-key exposure can affect account security and service usage. <br>
Mitigation: Keep secrets in environment variables, do not hardcode them in scripts or repositories, and rotate credentials after suspected exposure. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/renning22/asia-twitter-api-v1) <br>
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction) <br>
- [AIsa Website and Security Policies](https://aisa.one) <br>
- [OpenClaw Documentation](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples, Python client commands, and JSON API responses from the service] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY plus curl or python3 for the documented command workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
