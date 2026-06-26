## Description: <br>
Creates and populates Feishu documents by structuring user-provided content, splitting long text into API-sized segments, appending each segment, retrying failures, and verifying the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tc1993](https://clawhub.ai/user/tc1993) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, developers, and agents use this skill to turn supplied content into complete Feishu documents such as technical documentation, PRDs, project plans, reports, notes, articles, or long-form drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update remote Feishu documents, which may send sensitive, regulated, or confidential content outside the local agent environment. <br>
Mitigation: Confirm the target document, account or workspace, and content before use; avoid sending secrets or regulated data unless Feishu permissions and retention policies allow it. <br>
Risk: Long or complex document content may fail to append cleanly because Feishu document operations can reject oversized or unsupported formatting. <br>
Mitigation: Use the skill's segmentation, retry, and format simplification workflow, then verify the final document content after creation. <br>


## Reference(s): <br>
- [Feishu API Guide](references/feishu_api_guide.md) <br>
- [Create Feishu Doc ClawHub Page](https://clawhub.ai/tc1993/create-feishu-doc) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Files, Markdown, Guidance] <br>
**Output Format:** [Feishu document content and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Segments long content into smaller append operations, retries failed writes, and returns document identifiers, links, and write status.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
