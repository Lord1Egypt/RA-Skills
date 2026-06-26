## Description: <br>
Connect to security cameras, capture snapshots, and process video feeds with protocol support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security-system operators, and camera owners use this skill to generate camera capture commands, integrate with systems such as Home Assistant or Frigate, and troubleshoot image or video capture workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide access to sensitive camera streams and stored images. <br>
Mitigation: Use it only with cameras and systems the operator is authorized to access, and keep credentials in protected environment variables or secret storage. <br>
Risk: Captured snapshots or clips may contain private footage. <br>
Mitigation: Minimize capture scope, delete saved media when no longer needed, and apply retention limits for any monitoring workflow. <br>
Risk: Cloud vision examples may upload private camera footage to third-party providers. <br>
Mitigation: Prefer local processing where possible, and upload footage only with appropriate consent and retention review. <br>
Risk: Some examples include unsafe transport patterns such as unencrypted RTSP or curl -k certificate bypasses. <br>
Mitigation: Use secure network segmentation, encrypted transport where available, and proper TLS certificate validation for production integrations. <br>


## Reference(s): <br>
- [Cameras ClawHub listing](https://clawhub.ai/ivangdavila/cameras) <br>
- [Webcam and USB camera capture](capture.md) <br>
- [DSLR and mirrorless control](photography-control.md) <br>
- [Video and image processing](processing.md) <br>
- [Security camera integration](security-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, Python, JavaScript, curl, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are user-driven and often require user-provided camera URLs, credentials, device identifiers, or local tool installation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
