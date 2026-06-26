## Description: <br>
Exo Cluster guides agents through combining Mac, PC, WSL2, and Windows devices into a local distributed AI cluster for running large language models such as DeepSeek, Qwen, and LLaMA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up, start, join, manage, and call a local Exo distributed inference cluster across supported devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides users to run a local cluster and model API services that may expose ports on trusted networks. <br>
Mitigation: Run the cluster only on trusted networks, restrict exposed ports with firewall rules or localhost binding where possible, and avoid sending sensitive prompts or data until access controls are understood. <br>
Risk: The setup flow includes cloning and running external Exo repositories. <br>
Mitigation: Install only from trusted Exo sources, review cloned repositories before running them, and pin known-good versions when reproducibility matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smseow001/exo-cluster) <br>
- [Exo website](https://exolabs.net/) <br>
- [Exo GitHub repository](https://github.com/exo-explore/exo) <br>
- [Exo Windows GitHub repository](https://github.com/tensorsofthewall/exo_windows) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and curl command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
