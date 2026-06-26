## Description: <br>
AIPPT生成 helps agents create PowerPoint presentations from a topic by generating an outline, supporting outline edits and template selection, and returning a PPT download link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luych888-design](https://clawhub.ai/user/luych888-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to produce slide decks for reports, presentations, year-end summaries, product launches, and similar PPT workflows. The process is interactive: users review the generated outline and choose a template before the PPT generation task is submitted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends PPT topics, generated outlines, reporter names, user and chat metadata, and a stable host-derived hashed identifier to ai.mingyangtek.com. <br>
Mitigation: Use only when that data sharing is acceptable, get explicit privacy consent before the first API call, minimize metadata, and avoid sensitive presentation content. <br>
Risk: Generated PPT files and previews are delivered through external OSS download links. <br>
Mitigation: Review generated files and links before sharing, and handle downloads according to the user's security and data-handling requirements. <br>


## Reference(s): <br>
- [API Endpoints Reference](references/api-endpoints.md) <br>
- [MindPPT website](https://mindppt.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance, API calls] <br>
**Output Format:** [Markdown responses with outline previews, template lists, status updates, and PPT download links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before outline approval and template selection; relies on external PPT generation and download services.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
