## Description: <br>
Share AI agent conversations as public web pages for external sharing, documentation, or publishing to a public URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imyelo](https://clawhub.ai/user/imyelo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Clawpage to convert AI agent sessions into public web pages for sharing, documentation, or publication. The skill guides setup, session selection, conversion, metadata review, redaction, branch creation, commit creation, and optional pull-request publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exported conversations can expose private reasoning, tool arguments, tool results, file paths, screenshots, raw images, secrets, or personal data in public pages. <br>
Mitigation: Review the generated YAML before publishing, prefer messages-only export unless process details are intentionally public, and redact secrets and personal data before committing or opening a pull request. <br>
Risk: The workflow changes exported chat visibility to public and can publish the result through a branch and pull request. <br>
Mitigation: Publish only after an explicit user request, keep each chat export on a dedicated branch, and use pull-request review to inspect the final content before merge. <br>


## Reference(s): <br>
- [Clawpage skill page](https://clawhub.ai/imyelo/clawpage) <br>
- [Clawpage homepage](https://github.com/imyelo/clawpage) <br>
- [OpenClaw platform profile](references/platforms/openclaw.md) <br>
- [Unknown platform profile](references/platforms/unknown.md) <br>
- [Output template](references/output-template.md) <br>
- [Setup guide](references/setup.md) <br>
- [Publish guide](references/publish.md) <br>
- [Large file handling](references/large-file.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with YAML output and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or updates a chat YAML file and may guide branch, commit, push, and pull-request steps after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
