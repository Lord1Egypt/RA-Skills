## Description: <br>
Provides CI/CD pipeline templates and setup guidance for Java and Vue projects using GitLab CI or Jenkins with linting, testing, packaging, Docker image building, Kubernetes deployment, and notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallest-ming](https://clawhub.ai/user/smallest-ming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to configure CI/CD workflows for Java, Vue, or Java plus Vue projects. It helps generate platform-specific pipeline, deployment, notification, and setup guidance for GitLab CI or Jenkins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generated Docker setup path may expose Docker remote control on 0.0.0.0:2376. <br>
Mitigation: Prefer SSH-based Docker control, or require mutual TLS and network allowlisting before enabling remote Docker access. <br>
Risk: CI/CD credentials, kubeconfig files, SSH keys, registry secrets, and webhook URLs can expose deployment environments if mishandled. <br>
Mitigation: Store secrets only in protected CI credential stores, restrict deployment jobs to protected branches or environments, and limit build metadata sent to chat webhooks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smallest-ming/cicd-workflow) <br>
- [GitLab CI documentation](https://docs.gitlab.com/ee/ci/) <br>
- [Jenkins Pipeline documentation](https://www.jenkins.io/doc/book/pipeline/) <br>
- [Kubernetes Deployment guide](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown setup guidance with CI/CD configuration files and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates platform-specific pipeline and deployment assets for GitLab CI or Jenkins.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
