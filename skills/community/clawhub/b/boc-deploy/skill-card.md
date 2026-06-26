## Description: <br>
BOC Deploy helps an agent prepare a BOC container platform deployment, generate config.yaml, run bocctl, monitor progress, and verify Kubernetes node and pod status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongruiji](https://clawhub.ai/user/hongruiji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to deploy BOC container platform environments from planned node, VIP, SSH, CNI, and Kubernetes version inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests root SSH access and credentials for deployment targets. <br>
Mitigation: Review the generated config.yaml before use, prefer SSH keys or temporary credentials over passwords, and remove or protect credential-bearing files after deployment. <br>
Risk: The skill can start broad BOC and Kubernetes infrastructure changes through bocctl. <br>
Mitigation: Confirm every target IP, node role, VIP, CNI setting, and Kubernetes version before allowing the agent to run deployment commands. <br>
Risk: Deployment runs in the background and may expose sensitive details through logs or transcripts. <br>
Mitigation: Monitor the background job, restrict log sharing, and avoid exposing credentials in logs, prompts, or agent transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hongruiji/boc-deploy) <br>
- [Publisher profile](https://clawhub.ai/user/hongruiji) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated config.yaml content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include deployment status, log excerpts, and Kubernetes validation results.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release metadata; _meta.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
