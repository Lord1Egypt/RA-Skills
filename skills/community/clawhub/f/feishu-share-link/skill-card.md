## Description: <br>
Generates Feishu share links in both tenant-specific and root-domain formats for documents, Bitable bases, wikis, and sheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AndersonHJB](https://clawhub.ai/user/AndersonHJB) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and Feishu users use this skill when an agent needs to return reliable Feishu document, Bitable, wiki, or sheet links with both tenant-domain and fallback root-domain URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read ~/.openclaw/workspace/TOOLS.md to find a Feishu custom domain. <br>
Mitigation: Before installation, confirm that TOOLS.md contains only intended Feishu configuration or provide the Feishu domain manually when requesting links. <br>
Risk: A missing or incorrect custom Feishu domain can produce incomplete or unusable tenant-domain links. <br>
Mitigation: Verify the configured Feishu custom domain and keep the root-domain fallback link in generated responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AndersonHJB/feishu-share-link) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/AndersonHJB) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown with Feishu share links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces paired tenant-domain and root-domain links when a custom Feishu domain is available.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
