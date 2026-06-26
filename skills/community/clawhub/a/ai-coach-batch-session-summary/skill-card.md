## Description: <br>
Generates AI coach and outreach insight reports from authorized ASR transcript records after clarifying the user's time range, analysis focus, and delivery format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[legionspace-hackathon](https://clawhub.ai/user/legionspace-hackathon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw or Legion agents use this skill to summarize batches of ASR recordings into user-requested AI coach, outreach, sales script, or customer-need reports. The workflow asks for missing scope details before fetching data and grounds final conclusions in transcript text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private ASR transcripts and bearer-token API access. <br>
Mitigation: Install and run it only in trusted Legion/OpenClaw environments where authorization headers, LEGION_* environment variables, and the API base URL are controlled by trusted configuration. <br>
Risk: Untrusted LEGION_USER_MESSAGE or LEGION_SKIP_CLARIFICATION values can change the requested time range or analysis scope. <br>
Mitigation: Do not set those environment variables from untrusted sources; require explicit user or gateway confirmation when time range or analysis focus is ambiguous. <br>
Risk: Reports could include unsupported conclusions if they use non-transcript fields or infer content when the selected theme is absent. <br>
Mitigation: Ground conclusions only in asrText, avoid aiJiaolianResultJson and aiSummaryContent as evidence, and return no related content when transcript text does not match the requested theme. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/legionspace-hackathon/ai-coach-batch-session-summary) <br>
- [Report page template](templates/insight-report-page.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown report page or text summary; helper scripts return JSON for intent parsing, clarification, fetch results, and report planning.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask a clarification question before fetching recordings; large result sets include a hint to prioritize recent samples and sample excerpts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
