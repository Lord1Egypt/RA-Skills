## Description: <br>
Generates 4K information posters from text, files, or existing images through the Datu external API, with support for AI image editing and optional deep research reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laozhangai](https://clawhub.ai/user/laozhangai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, content creators, brand operators, and business users use this skill to turn source material into high-resolution information posters, edit existing posters, and optionally request deep research outputs before image generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text, documents, files, and image URLs may be sent to Datu's external service. <br>
Mitigation: Run the upload safety check first and obtain explicit approval before sending secrets, regulated data, or highly sensitive personal data. <br>
Risk: DATU_API_KEY is a sensitive credential used to access the external Datu service. <br>
Mitigation: Store DATU_API_KEY in the host credential vault, avoid exposing it in public records, and reconfigure it only when missing, expired, deleted, or rejected. <br>
Risk: Deep research and generic edit requests can send content off-platform and consume additional credits and time. <br>
Mitigation: Require confirmation before enabling deep_research or proceeding with ambiguous edit requests. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/laozhangai/datu-ai-poster-generator) <br>
- [Datu documentation](https://datu.digilifeform.com/docs) <br>
- [Datu homepage](https://datu.digilifeform.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown responses with API payloads, image links, status updates, and optional Word document downloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DATU_API_KEY for Datu API access; outputs may include image_url, download_url, and research_report_download_url values.] <br>

## Skill Version(s): <br>
1.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
