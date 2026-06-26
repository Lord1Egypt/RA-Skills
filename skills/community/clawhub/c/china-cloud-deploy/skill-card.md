## Description: <br>
Helps agents deploy applications to Tencent Cloud, Alibaba Cloud, and Huawei Cloud using official CLIs, with workflows for serverless functions, static hosting, storage, cross-cloud strategy, ICP filing, and China connectivity considerations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to produce deployment guidance, CLI commands, and configuration steps for applications targeting major Chinese cloud providers. It is suited for planning and executing China-region serverless, static hosting, object storage, VPS, container registry, and ICP-aware deployment workflows. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill helps operate cloud deployment workflows that can use sensitive cloud credentials. <br>
Mitigation: Use least-privilege or temporary credentials, avoid entering secrets into shared transcripts, and review every generated command before execution. <br>
Risk: The skill can guide public uploads to Aliyun OSS or similar object storage targets. <br>
Mitigation: Upload only reviewed build output intended to be public, and avoid private directories, source maps, configuration files, or files that may contain secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lm203688/china-cloud-deploy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands and deployment steps require user-provided cloud credentials and review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
