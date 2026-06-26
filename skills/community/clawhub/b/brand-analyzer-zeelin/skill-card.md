## Description: <br>
品牌分析 Skill（零配置版）。用户仅需提供 Zeelin App-Key 和品牌名，调用服务端封装接口生成品牌底座；计费在服务端完成（成功扣50额度，失败不扣费）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linhai806806-cell](https://clawhub.ai/user/linhai806806-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External brand, marketing, and strategy users can provide a Zeelin App-Key and brand name to generate a structured brand foundation report covering positioning, competitors, audience, and brand tone. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports clean scanner signals but notes that the adjudication did not have a full artifact-backed review. <br>
Mitigation: Install only after reviewing the actual skill files or when the publisher is trusted. <br>
Risk: The skill sends the supplied brand name, optional query, and optional attachment to a third-party brand analysis service. <br>
Mitigation: Avoid submitting confidential or regulated data unless that third-party processing is acceptable for the user or organization. <br>
Risk: The artifact points at a temporary Cloudflare tunnel host and deploy notes say to replace it with a stable HTTPS domain. <br>
Mitigation: Verify the endpoint is a trusted, stable production service before using the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/linhai806806-cell/brand-analyzer-zeelin) <br>
- [Deploy Notes](references/deploy_notes.md) <br>
- [Zeelin Skill platform](https://skills.zeelin.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown brand analysis report with concise status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful runs report consumed credits and remaining balance; failures return actionable service messages.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
