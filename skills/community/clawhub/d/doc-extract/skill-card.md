## Description: <br>
Extract text and content from Word documents (.doc and .docx) to Markdown using MinerU. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, assistants, and automation workflows use this skill to extract Word document content from local files or URLs into Markdown for downstream reading and processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents or URLs may be handled by the third-party MinerU service. <br>
Mitigation: Avoid confidential documents or private URLs unless third-party processing is acceptable for the use case. <br>
Risk: MINERU_TOKEN is a credential used for full extraction flows. <br>
Mitigation: Store the token in an environment variable or approved secret store and avoid exposing it in logs, prompts, or shared files. <br>
Risk: The skill depends on the mineru-open-api package or Go installation path. <br>
Mitigation: Verify the package source and installation channel before installing or running the CLI. <br>


## Reference(s): <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU token management](https://mineru.net/apiManage/token) <br>
- [OpenDataLab MinerU](https://github.com/opendatalab/MinerU) <br>
- [Doc Extract on ClawHub](https://clawhub.ai/mzlzyca/doc-extract) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Document content is written to stdout by default or saved to an output directory; progress and status messages are written to stderr.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
