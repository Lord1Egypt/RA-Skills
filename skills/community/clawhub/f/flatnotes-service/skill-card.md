## Description: <br>
Flatnotes 笔记服务 helps an agent create, search, retrieve, update, and delete Markdown notes through a Flatnotes API, using environment-provided credentials only after explicit user consent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cal0rie](https://clawhub.ai/user/cal0rie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers with a Flatnotes instance use this skill to save generated Markdown reports, search and retrieve existing notes, and manage note lifecycle actions from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credentials for a Flatnotes instance may grant access to sensitive notes or files. <br>
Mitigation: Use credentials you are comfortable granting to an agent, keep them in environment variables, and obtain explicit user approval before any Flatnotes call. <br>
Risk: Create, update, delete, and attachment operations can alter or expose user data. <br>
Mitigation: Confirm destructive actions and uploads manually, and review the target note title, content, and file before execution. <br>
Risk: Server-resolved provenance is unavailable for this release. <br>
Mitigation: Do not infer repository provenance from skill text; review the artifact files and ClawHub security summary before installation. <br>


## Reference(s): <br>
- [Flatnotes API 完整文档](references/api_docs.md) <br>
- [Publisher homepage](https://cnb.cool/iceicc-ai-made/skills) <br>
- [ClawHub skill page](https://clawhub.ai/cal0rie/flatnotes-service) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and curl command examples; helper scripts print text summaries and return JSON-shaped Flatnotes API results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FLATNOTES_BASE_URL, FLATNOTES_USERNAME, and FLATNOTES_PASSWORD; note contents and credentials may be sensitive.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
