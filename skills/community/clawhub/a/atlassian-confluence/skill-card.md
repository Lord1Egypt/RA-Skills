## Description: <br>
Read and write Confluence pages, search content, manage labels and comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pejovicvuk](https://clawhub.ai/user/pejovicvuk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation owners, and agents use this skill to search Confluence Cloud, retrieve page content, inspect comments, labels, attachments, and make controlled wiki updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live Confluence changes using the configured Atlassian API token. <br>
Mitigation: Use a least-privilege token limited to required spaces and require explicit user approval before creating pages, updating pages, adding comments, or adding labels. <br>
Risk: Untrusted label input is called out as unsafe until the Python interpolation bug is fixed. <br>
Mitigation: Avoid untrusted label values or restrict labels to a reviewed allowlist before running the add-labels command. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/pejovicvuk/atlassian-confluence) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON from the Confluence CLI with concise Markdown guidance for command selection, pagination, and truncation caveats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ATLASSIAN_URL, ATLASSIAN_EMAIL, and ATLASSIAN_API_TOKEN; read results may be paginated or truncated.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
