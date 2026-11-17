## Description:

FitConverter helps agents guide users through converting exported fitness and workout records from Huawei, Zepp, Xiaomi, vivo, Samsung, Keep, GPX, TCX, FIT, KML, and other sources into formats or destinations such as COROS, Garmin, Strava, RQrun, FIT, TCX, GPX, and KML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daozhao](https://clawhub.ai/user/daozhao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to configure FitConverter access, collect conversion parameters, upload fitness export files, submit trial or paid conversion jobs, and check status until results are delivered by email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fitness exports can contain location history and sensitive workout data sent to an external FitConverter service.

Mitigation: Confirm user consent before upload, explain the destination service, and avoid submitting files that are not required for the requested conversion.

Risk: Sync modes may require third-party account credentials and the skill asks for a FitConverter API key.

Mitigation: Prefer manual secret configuration through mcporter and avoid pasting API keys or account passwords into chat unless the user explicitly accepts that handling.

Risk: Payment flows can return QR-code or off-channel payment links.

Mitigation: Show payment links only when the user requested a conversion and make clear that payment is handled by FitConverter.

## Reference(s):

- [FitConverter homepage](https://www.fitconverter.com)
- [FitConverter API key generation](https://api.fitconverter.com/mcp/generate-api-key)
- [FitConverter MCP endpoint](https://api.fitconverter.com/mcp)
- [FitConverter conversion submission endpoint](https://api.fitconverter.com/mcp/submit_conversion)
- [ClawHub skill page](https://clawhub.ai/daozhao/skills/fitconverter)
- [Daozhao publisher profile](https://clawhub.ai/user/daozhao)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown with inline JSON, bash, JavaScript, and status-response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter and a FitConverter API key; conversion submissions use multipart/form-data and may return payment status or QR payment links.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
