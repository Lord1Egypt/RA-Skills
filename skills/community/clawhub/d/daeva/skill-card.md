## Description: <br>
Daeva routes agent requests for GPU-backed AI inference and pod lifecycle operations through a local or remote Daeva service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asmolebot](https://clawhub.ai/user/asmolebot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Daeva to route transcription, image generation, OCR, vision, and GPU pod management tasks to a Daeva service while checking status and lifecycle state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ordinary media requests can be routed into shared GPU pod controls that may start, stop, swap, or install pods. <br>
Mitigation: Use Daeva only when the user intentionally wants Daeva routing and is authorized to manage the target pod environment. <br>
Risk: Commands may affect a shared local or remote Daeva service rather than a per-user session. <br>
Mitigation: Confirm the resolved host, pod, service, and expected lifecycle side effects before allowing start, stop, swap, register, or install actions. <br>


## Reference(s): <br>
- [Daeva ClawHub listing](https://clawhub.ai/asmolebot/daeva) <br>
- [Daeva repository](https://github.com/asmolebot/daeva) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash, JSON, and REST endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a reachable Daeva service and HTTP/curl access; guidance may include commands that start, stop, swap, register, or install GPU pods.] <br>

## Skill Version(s): <br>
0.2.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
