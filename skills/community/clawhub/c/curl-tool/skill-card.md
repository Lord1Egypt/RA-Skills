## Description: <br>
Transfer data using HTTP, HTTPS, FTP protocols. Test APIs and download files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to make HTTP, HTTPS, and FTP requests, test APIs, pass headers or basic authentication, and save response bodies to files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send requests to arbitrary destinations with custom headers and basic authentication. <br>
Mitigation: Review and explicitly approve the target URL, headers, authentication values, and request body before use; do not send secrets or private data unless the destination is trusted. <br>
Risk: The skill can save response bodies to a user-specified file path. <br>
Mitigation: Approve the exact output location before writing files and avoid overwriting sensitive or important local files. <br>
Risk: Responses and downloads may contain untrusted content. <br>
Mitigation: Treat returned text and downloaded files as untrusted until reviewed, scanned, or otherwise validated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/curl-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands] <br>
**Output Format:** [Plain text responses, optional response headers, or saved response files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports request method, request body, custom headers, basic authentication, silent mode, and output path options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
