## Description: <br>
Guides agents through Oracle Workload Capture setup, customer-started DBMS_WORKLOAD_CAPTURE collection, sqla parsing into merge.json, and validation or repair steps for CMH traffic replay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database migration engineers use this skill to plan and execute Oracle workload capture, parse WCR capfiles with sqla, and prepare merge.json for CMH traffic replay. It is intended for operational capture runbooks where the customer starts or finishes database capture actions after reviewing the commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Operational Oracle workload capture can affect a production database if commands are run without review. <br>
Mitigation: Review the generated runbook, validate first in a test or low-risk window, and keep database capture start and finish actions under customer control. <br>
Risk: The runbook downloads the sqla toolkit from Alibaba Cloud OSS during execution. <br>
Mitigation: Review the download source and verify the documented SHA-256 hash before extracting or running the toolkit. <br>
Risk: merge.json repair can produce derived output that may differ from the original parser result. <br>
Mitigation: Preserve original merge.json files and inspect any merge_fixed output before using it for replay. <br>


## Reference(s): <br>
- [RAM Permission Statement](references/ram-policies.md) <br>
- [sqla 3.3.26 toolkit download](https://cmh-prod-ap-southeast1.oss-ap-southeast-1.aliyuncs.com/agent/frodo/sqla-3.3.26.tar.gz) <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-migration-dbm-oracle-traffic-capture) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration instructions] <br>
**Output Format:** [Markdown with SQL and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses are English-only and include an end-to-end runbook plus expected merge.json deliverable path.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
