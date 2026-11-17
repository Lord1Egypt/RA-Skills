## Description:

品牌分析 Skill（零配置版）。用户仅需提供 Zeelin App-Key 和品牌名，调用服务端封装接口生成品牌底座；计费在服务端完成（成功扣50额度，失败不扣费）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linhai806806-cell](https://clawhub.ai/user/linhai806806-cell)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing teams use this skill to turn a brand name, optional query, and optional attachment into a structured brand foundation report. It supports brand positioning, competitor landscape, user persona, and brand tone analysis through a Zeelin paid API workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to send a billable App-Key to a temporary Cloudflare tunnel that the package notes say should be replaced before publishing.

Mitigation: Install only after the publisher replaces the tunnel with a stable, verifiably controlled production domain and documents how App-Keys are protected.

Risk: Optional attachments may be sent to the remote service without documented retention or deletion practices.

Mitigation: Avoid confidential attachments until the publisher documents file handling, retention, and deletion practices.

Risk: The App-Key functions as a billing credential for Zeelin credits.

Mitigation: Treat the App-Key as sensitive, use a revocable key if available, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linhai806806-cell/skills/brand-analyzer-zeelin)
- [Publisher profile](https://clawhub.ai/user/linhai806806-cell)
- [Deploy Notes](artifact/references/deploy_notes.md)
- [Zeelin Skill platform](https://skills.zeelin.cn)
- [Brand Analyzer API endpoint](https://following-hull-easy-interactions.trycloudflare.com/v1/brand-analyzer/generate)

## Skill Output:

**Output Type(s):** [markdown, text, guidance]

**Output Format:** [Markdown brand analysis report with concise billing and error status messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful generations report the 50-credit charge and remaining credits when returned by the service.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
