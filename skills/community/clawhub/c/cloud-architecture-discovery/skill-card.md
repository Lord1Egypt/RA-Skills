## Description: <br>
Discover and map your cloud architecture automatically. View architecture directories, topology, and resource relationships via Tencent Cloud Smart Advisor API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stinggit](https://clawhub.ai/user/stinggit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud architects, and cloud operators use this skill to inspect Tencent Cloud Smart Advisor architecture directories, architecture details, resource relationships, and Well-Architected evaluation results for the current credentialed account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Tencent Cloud credentials and can generate temporary console login links. <br>
Mitigation: Use a least-privilege subaccount, keep generated login links private, and avoid sharing command output that contains temporary access URLs. <br>
Risk: Some bundled operations can create or delete CAM roles or enable Tencent Cloud Smart Advisor authorization. <br>
Mitigation: Run role-management and authorization commands only after explicit approval, and review the requested CAM actions before execution. <br>
Risk: The artifact includes unrelated bulk-publishing tooling in addition to the Smart Advisor workflow. <br>
Mitigation: Do not run the bundled publishing scripts unless you specifically intend to publish ClawHub content and have reviewed their behavior. <br>
Risk: The server security verdict is suspicious because of broad cloud-account administration behavior and unrelated publishing files. <br>
Mitigation: Review the artifact before installation and install only if the Tencent Cloud permissions and bundled tooling match the intended use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/stinggit/cloud-architecture-discovery) <br>
- [Tencent Cloud Smart Advisor API overview](https://cloud.tencent.com/document/product/1264/63122) <br>
- [Tencent Cloud API Explorer](https://console.cloud.tencent.com/api/explorer) <br>
- [DescribeArch API reference](artifact/references/api/DescribeArch.md) <br>
- [DescribeArchList API reference](artifact/references/api/DescribeArchList.md) <br>
- [DescribeLastEvaluation API reference](artifact/references/api/DescribeLastEvaluation.md) <br>
- [DescribeStrategies API reference](artifact/references/api/DescribeStrategies.md) <br>
- [CreateAdvisorAuthorization API reference](artifact/references/api/CreateAdvisorAuthorization.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, JSON, Markdown] <br>
**Output Format:** [Markdown responses with shell commands, JSON API results, and Tencent Cloud console links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include architecture summaries, risk evaluation details, and sensitive temporary console login links for the current Tencent Cloud account.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
