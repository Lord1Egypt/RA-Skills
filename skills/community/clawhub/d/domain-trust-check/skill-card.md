## Description: <br>
URL safety scanner and domain reputation checker for checking whether links and domains may be associated with phishing, malware, brand abuse, or scams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jamesouttake](https://clawhub.ai/user/jamesouttake) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to check URLs before visiting, recommending, or sharing them, and to interpret domain trust results returned by the Outtake Trust API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URLs submitted to the third-party API may reveal private links, internal hostnames, or sensitive query parameters. <br>
Mitigation: Use only with URLs appropriate to share with Outtake, and strip or redact sensitive query parameters before checking. <br>
Risk: The skill requires an OUTTAKE_API_KEY credential for authenticated API requests. <br>
Mitigation: Store the API key as an environment variable and avoid placing it in prompts, logs, source files, or shared command history. <br>
Risk: Unknown or suspicious verdicts may not prove that a URL is safe. <br>
Mitigation: Treat unknown results with caution and follow the returned recommended action rather than relying on the skill as the sole security control. <br>


## Reference(s): <br>
- [Domain Trust Check API Reference](references/api.md) <br>
- [Outtake](https://outtake.ai) <br>
- [Domain Trust Check on ClawHub](https://clawhub.ai/jamesouttake/domain-trust-check) <br>
- [Outtake Bounty Network](https://clawhub.ai/jamesouttake/outtake-bounty-network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl commands, JSON response examples, and interpretation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and an OUTTAKE_API_KEY credential for API calls; batch checks support up to 50 URLs per request.] <br>

## Skill Version(s): <br>
1.2.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
