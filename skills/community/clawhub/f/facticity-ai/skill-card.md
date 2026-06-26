## Description: <br>
Complete Facticity.AI integration - fact-check claims, extract claims from content, transcribe links, check link reliability, check credits, and monitor task status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shahruj](https://clawhub.ai/user/shahruj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to route OpenClaw requests to Facticity.AI for claim fact-checking, claim extraction, media transcription, link reliability scoring, credit checks, and async task status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided claims, text, URLs, media links, transcripts, and related account metadata to Facticity.AI for processing. <br>
Mitigation: Install and use it only when Facticity.AI is trusted for that content, and avoid sending secrets, confidential material, or data outside your policy scope. <br>
Risk: FACTICITY_API_KEY is a sensitive credential used to access the service. <br>
Mitigation: Store the key in the configured environment or OpenClaw secret location, restrict access to it, and avoid exposing it in prompts, logs, or shared files. <br>
Risk: Fact-checking, transcription, and reliability outputs can be incomplete or incorrect for high-stakes decisions. <br>
Mitigation: Review returned evidence and source assessments before relying on the output, especially for legal, medical, financial, safety, or public-facing decisions. <br>


## Reference(s): <br>
- [Facticity.AI app](https://app.facticity.ai) <br>
- [Facticity.AI API](https://api.facticity.ai) <br>
- [Facticity.AI API docs](https://api.facticity.ai/docs) <br>
- [ClawHub skill page](https://clawhub.ai/shahruj/facticity-ai) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Configuration guidance] <br>
**Output Format:** [JSON API responses and concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include fact-check classifications, evidence sources, transcripts, reliability scores, credit counts, task status, or API-key setup guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
