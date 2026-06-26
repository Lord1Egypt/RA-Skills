## Description: <br>
Download a file from a URL and save it locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to download an HTTP or HTTPS resource to a local file path when they need to save remote content such as an image, document, audio file, or video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted remote files may be saved locally and later opened or executed. <br>
Mitigation: Use trusted URLs and treat downloaded content as untrusted until it has been inspected. <br>
Risk: A chosen save path could overwrite important project, configuration, or system files. <br>
Mitigation: Use an explicit destination such as a dedicated downloads folder and avoid saving over important files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands] <br>
**Output Format:** [JSON status message with the saved local file path; downloaded content is written as a local file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Python requests package. The URL is required; save_path is optional and defaults to a filename derived from the URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
