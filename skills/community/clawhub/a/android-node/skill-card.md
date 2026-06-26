## Description: <br>
Convert Android phones running Termux into local Ollama inference nodes for AI task processing without cloud or special hardware. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to provision Android phones as local Ollama worker nodes and route AI inference requests across healthy devices on a trusted private network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup guidance may encourage running a Termux provisioning script fetched from the network. <br>
Mitigation: Inspect the setup script before execution and prefer the bundled setup.sh content when possible. <br>
Risk: The phone node exposes an unauthenticated local Ollama service on the network. <br>
Mitigation: Run nodes only on trusted private networks or behind firewall or VPN controls, especially before sending sensitive prompts. <br>
Risk: Downloaded binaries or models may change over time if they are not pinned or verified. <br>
Mitigation: Pin or verify downloaded binaries and model artifacts where practical before deployment. <br>


## Reference(s): <br>
- [Android Node on ClawHub](https://clawhub.ai/albionaiinc-del/android-node) <br>
- [Publisher profile: albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and routing guidance for local Android Ollama nodes; users provide device IP addresses, model choices, and node names.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
