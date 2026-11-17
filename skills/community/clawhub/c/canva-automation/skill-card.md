## Description:

Automates Canva tasks via Rube MCP (Composio), including designs, exports, folders, brand templates, autofill, and current-schema tool discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sohamganatra](https://clawhub.ai/user/sohamganatra)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to guide agents through Canva design creation, browsing, asset upload, export, folder organization, and brand-template autofill workflows through Rube MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Canva OAuth access lets the agent act on Canva designs, assets, folders, exports, and brand-template workflows.

Mitigation: Connect only the intended Canva account and review each upload, export, folder move, or autofill request before execution.

Risk: Uploaded files, design contents, OAuth access, and generated export download links can expose sensitive third-party data.

Mitigation: Treat these data flows as sensitive, share generated links only with intended recipients, and avoid uploading confidential assets unless the Canva/Rube connection is approved for that data.

Risk: Upload, export, and autofill operations are asynchronous and may fail or return incomplete results if the job is not checked.

Mitigation: Poll the relevant job status until a success or failed state is returned, then handle failures before using asset IDs, design IDs, or download URLs.

## Reference(s):

- [Rube MCP](https://rube.app/mcp)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration instructions]

**Output Format:** [Markdown instructions with MCP tool sequences, parameter notes, and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Rube MCP and an active Canva OAuth connection.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
