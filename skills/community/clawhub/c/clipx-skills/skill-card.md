## Description: <br>
Thin client for the private ClipX BNBChain API, returning text-only JSON metrics and rankings for BNB Chain with no client-side scraping code or API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ClipXonchain](https://clawhub.ai/user/ClipXonchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request BNB Chain rankings, market snapshots, network metrics, and Binance announcement summaries through the ClipX API. It is suited for text-based analytics workflows where outputs are returned as JSON, markdown, or pre-formatted tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected BNB Chain analytics requests, including queried wallet addresses, are sent to the private ClipX API. <br>
Mitigation: Submit only queries you are comfortable sharing with ClipX, and avoid sending sensitive addresses or data unless the API endpoint is trusted for that use. <br>
Risk: Market metrics and Binance announcements are third-party content returned by the service. <br>
Mitigation: Verify important financial or operational decisions against primary sources before acting on the results. <br>
Risk: The skill runs Python commands that make outbound HTTP requests, and CLIPX_API_BASE can redirect those requests. <br>
Mitigation: Review the command and environment before execution, especially any custom CLIPX_API_BASE value. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ClipXonchain/clipx-skills) <br>
- [ClipX Publisher Profile](https://clawhub.ai/user/ClipXonchain) <br>
- [ClipX API Base](https://skill.clipx.app) <br>
- [BNB Chain](https://bnbchain.org) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown responses with code-block tables, plain markdown announcements, or compact JSON from the Python CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and the requests package; the default API base is https://skill.clipx.app and can be overridden with CLIPX_API_BASE.] <br>

## Skill Version(s): <br>
1.0.20 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
