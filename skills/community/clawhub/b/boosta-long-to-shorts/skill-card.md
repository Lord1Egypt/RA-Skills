## Description: <br>
Create, monitor, and troubleshoot Boosta API video-processing jobs from natural-language requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hundevmode](https://clawhub.ai/user/hundevmode) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Creators, agencies, and automation engineers use this skill to submit long-form video URLs to Boosta, monitor processing, and retrieve generated short clip URLs through an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends video URLs to Boosta as an external processor. <br>
Mitigation: Use the skill only when Boosta's policies meet the user's needs, and avoid submitting private or sensitive video URLs unless that processing is acceptable. <br>
Risk: The skill requires a Boosta API key for authenticated network requests. <br>
Mitigation: Provide BOOSTA_API_KEY through the environment, grant the minimum access practical, and do not print or store raw API keys in agent output. <br>
Risk: Boosta allows one active job at a time per account or key and may rate-limit polling. <br>
Mitigation: Reuse the returned active job when present, respect retry_after values, and keep polling intervals bounded. <br>
Risk: An incorrect video_type can produce invalid requests or lower-quality processing. <br>
Mitigation: Use the bundled video type reference, state any inference explicitly, and ask a clarifying question when confidence is low. <br>


## Reference(s): <br>
- [Boosta Homepage](https://boosta.pro) <br>
- [Boosta API Getting Started](https://docs.boosta.pro/api/getting-started) <br>
- [Boosta API Authentication](https://docs.boosta.pro/api/authentication) <br>
- [Boosta API Endpoints](https://docs.boosta.pro/api/endpoints) <br>
- [Boosta API Reference](references/api-reference.md) <br>
- [Boosta Video Type Selection](references/video-types.md) <br>
- [Boosta API Error Handling](references/errors.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/hundevmode/boosta-long-to-shorts) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Boosta job_id, status, progress, clips_count, clip_urls, and next-step guidance; requires BOOSTA_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
