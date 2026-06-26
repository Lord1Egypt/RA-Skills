## Description: <br>
Manage Felo LiveDocs, including creating and managing knowledge bases, adding documents or URLs, and retrieving relevant content with natural-language queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate Felo LiveDocs from an agent, including creating knowledge bases, adding documents or URLs, managing resources, and searching stored content semantically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends knowledge-base content, uploaded files, URLs, and retrieval queries to the external Felo service. <br>
Mitigation: Use an approved, revocable Felo API key and avoid uploading secrets, regulated data, or private documents unless approved for that service. <br>
Risk: The skill can delete or bulk-update remote LiveDocs and resources without clear confirmation safeguards. <br>
Mitigation: Require explicit confirmation before delete or bulk update commands and verify the target LiveDoc or resource IDs before execution. <br>
Risk: The security verdict is suspicious because the skill is purpose-aligned but can modify remote knowledge-base data. <br>
Mitigation: Review the bundled script before deployment and restrict use to environments where Felo is an intended external knowledge-base provider. <br>


## Reference(s): <br>
- [Felo LiveDoc ClawHub Page](https://clawhub.ai/wangzhiming1999/felo-livedoc) <br>
- [Felo](https://felo.ai) <br>
- [Felo OpenAPI Endpoint](https://openapi.felo.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown summaries, JSON API responses, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FELO_API_KEY; commands call the external Felo API and can upload or delete remote LiveDoc resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
