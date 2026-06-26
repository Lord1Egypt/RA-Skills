## Description: <br>
Track flights in real time with detailed status, gate information, delay calculations, and live position data from AviationStack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[copey02](https://clawhub.ai/user/copey02) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to look up commercial flight status by IATA flight number and return formatted flight details or raw JSON for integration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default AviationStack free-tier setup sends the API key and flight lookup queries over unencrypted HTTP. <br>
Mitigation: Use an HTTPS-capable AviationStack plan or another provider for sensitive use, use a limited-purpose key, avoid public or untrusted networks, and avoid storing the key permanently in shared shell profiles. <br>
Risk: Flight data availability, rate limits, and live position fields depend on AviationStack API coverage and account limits. <br>
Mitigation: Check API responses before relying on results, handle missing fields, and monitor free-tier request usage. <br>


## Reference(s): <br>
- [AviationStack API Setup](references/api-setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/copey02/aviationstack-flight-tracker) <br>
- [AviationStack signup](https://aviationstack.com/signup/free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Formatted text or JSON, with setup guidance and shell commands in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AVIATIONSTACK_API_KEY environment variable and the Python requests package.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
