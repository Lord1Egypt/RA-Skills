## Description:

Guides agents through Chinese passport recognition and field extraction using the Laiye ADP platform and ADP CLI, producing structured JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

Commercial License Agreement

## Use Case:

External developers and operations teams use this skill to configure the Laiye ADP CLI, select the built-in Chinese passport extraction app, and extract passport fields from URL, local file, Base64, batch, or async inputs. The resulting JSON can support immigration review, visa processing, identity verification, and document automation workflows.

### Deployment Geography for Use:

Global; users choose the China mainland or overseas ADP service endpoint documented by Laiye.

## Known Risks and Mitigations:

Risk: The install instructions include package and script-based installation paths that can create supply-chain exposure.

Mitigation: Review the ADP CLI source before installation, prefer a pinned and verifiable package or signed release, and avoid curl-to-shell or irm-to-iex installation flows.

Risk: The workflow requires an ADP API key and may expose credentials if commands are pasted into chats, logs, or shared terminals.

Mitigation: Use a secret store or environment-based credential handling, avoid pasting real API keys into prompts or logged commands, and clear credentials when no longer needed.

Risk: Passport images are sensitive identity documents and are uploaded to the ADP service for processing.

Mitigation: Process only authorized passport files and confirm Laiye ADP privacy, retention, deletion, jurisdiction, and authorization terms before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laiye-adp/skills/adp-passport-recognition-and-extract)
- [Laiye ADP China Mainland Portal](https://adp.laiye.com/?utm_source=clawhub)
- [Laiye ADP Global Portal](https://adp-global.laiye.com/?utm_source=clawhub)
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- [Open API User Guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)
- [ADP Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh)
- [ADP CLI Releases](https://github.com/laiye-ai/adp-cli/releases)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON result structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON result files when ADP CLI export options are used.]

## Skill Version(s):

1.0.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
