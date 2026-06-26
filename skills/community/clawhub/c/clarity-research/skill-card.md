## Description: <br>
Search protein folding research data from Clarity Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarityprotocol](https://clawhub.ai/user/clarityprotocol) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External researchers, developers, and agents use this skill to query Clarity Protocol protein variant records by disease or protein name and inspect mutation, disease, UniProt, confidence, and creation metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries are sent to clarityprotocol.io, and using higher rate limits requires an API key. <br>
Mitigation: Only submit queries you are comfortable sharing with Clarity Protocol, use a dedicated CLARITY_API_KEY, and avoid storing unrelated secrets in that environment variable. <br>
Risk: Remote API rate limits, timeouts, or service errors can interrupt variant queries. <br>
Mitigation: Handle 429, timeout, and server errors in agent workflows, and use the optional API key when higher request limits are appropriate. <br>


## Reference(s): <br>
- [Clarity Protocol](https://clarityprotocol.io) <br>
- [ClawHub release page](https://clawhub.ai/clarityprotocol/clarity-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON results or summary text, with Markdown guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are fetched from clarityprotocol.io and may be rate limited; CLARITY_API_KEY is optional for higher request limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
