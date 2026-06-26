## Description: <br>
Helps agents configure ByteHouse multimodal vector storage and hybrid search for text, image, and video content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to build ByteHouse-backed multimodal retrieval workflows, including vector search, hybrid search, text-to-image/video search, and image-to-image search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or write ByteHouse database content. <br>
Mitigation: Use a dedicated least-privilege ByteHouse account and review the database authority granted before installation or execution. <br>
Risk: SQL may be routed through an MCP client by default when available. <br>
Mitigation: Disable or explicitly configure MCP use unless that routing is intended and reviewed. <br>
Risk: Indexed text, media URLs, and metadata may be stored persistently in ByteHouse and sent to the Ark embedding API. <br>
Mitigation: Avoid indexing sensitive inputs unless persistent database storage and external embedding API processing are approved. <br>
Risk: Dependency versions are not pinned in the provided installation command. <br>
Mitigation: Pin and review dependencies in sensitive or production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-bytehouse-multimodal-search) <br>
- [ByteHouse vector search SQL documentation](https://www.volcengine.com/docs/6464/1208707) <br>
- [Volcengine multimodal embedding API documentation](https://www.volcengine.com/docs/82379/1409291) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python, SQL, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides integration guidance and example commands; runtime scripts can call the Ark embedding API and read or write ByteHouse data when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
