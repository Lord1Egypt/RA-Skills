## Description:

一键同步1688店铺运营数据，自动整合并推送可视化运营数据分析日报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[howerlin0329](https://clawhub.ai/user/howerlin0329)

### License/Terms of Use:

MIT-0

## Use Case:

1688 sellers and operations teams use this skill to collect seller workbench and business-advisor metrics, generate a daily Markdown operations report, and optionally push that report to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad browser extension and CDP access can expose seller data outside the active reporting task.

Mitigation: Restrict extension host permissions and external messaging to required 1688 origins and authorized senders before production use.

Risk: Login QR codes, raw report data, and Feishu token caches may be disclosed or reused if sent or stored too broadly.

Mitigation: Send login media only to the active user-approved destination and secure or remove raw-data and token cache files after use.

Risk: Downloaded browser or runtime installers and shared browser profiles can expand the execution trust boundary.

Mitigation: Verify downloaded installers and run the browser in a dedicated isolated profile or machine.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/howerlin0329/skills/1688-alibaba-data-fetcher-1)
- [Publisher Profile](https://clawhub.ai/user/howerlin0329)
- [1688 Data Claw Agent Guide](artifact/plugin/AGENT_GUIDE.md)
- [1688 Data Claw README](artifact/plugin/README.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with supporting JSON data and setup or execution commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local raw-data JSON, a daily report Markdown file, login QR-code media, and Feishu message delivery results.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
