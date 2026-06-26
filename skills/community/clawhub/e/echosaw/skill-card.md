## Description: <br>
Analyzes video, audio, and image files using AI to produce structured intelligence reports including transcripts, content moderation signals, sentiment analysis, visual object labels, geographic metadata, and LLM-generated summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[echosaw](https://clawhub.ai/user/echosaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and media teams use this skill to submit media files or URLs to Echosaw, monitor analysis jobs, retrieve structured results, and search or browse an account-backed media library. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected media files, media URLs, transcripts, metadata, and account-backed library results may be sent to Echosaw and its listed AI processing providers. <br>
Mitigation: Submit only content approved for Echosaw processing and review privacy, retention, and provider terms before use. <br>
Risk: OAuth or API credentials and account-backed library access can expose private media records if mishandled. <br>
Mitigation: Use supported OAuth where available, protect API keys, and limit access to trusted users and environments. <br>
Risk: Media analysis can involve paid usage, especially for long audio or video files. <br>
Mitigation: Confirm the active plan and pricing before submitting media for analysis. <br>


## Reference(s): <br>
- [Echosaw MCP Integration Guide](https://echosaw.com/developers/mcp-integration) <br>
- [Echosaw API Reference](https://echosaw.com/developers/api-reference) <br>
- [Echosaw Pricing](https://echosaw.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON response envelopes with human-readable summaries and structured media intelligence results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Asynchronous media analysis returns job identifiers before completed reports are retrieved.] <br>

## Skill Version(s): <br>
1.3.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
