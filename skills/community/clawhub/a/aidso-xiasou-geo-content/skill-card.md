## Description: <br>
AIDSO 虾搜生成式引擎优化内容生产 Skill，支持 API Key 绑定和检查，并根据品牌、AI 问题与目标优化 AI 平台生成内容。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangyuanmile-coder](https://clawhub.ai/user/tangyuanmile-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content operators use this skill to generate AIDSO GEO content for a named brand, AI question, and target AI platform after checking or binding an API key and confirming the 6-credit charge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AIDSO API key and may store it locally when bound. <br>
Mitigation: Prefer setting AIDSO_GEO_API_KEY in the environment, avoid exposing the full key, and rebind only when intended. <br>
Risk: Brand and AI question prompts are sent to AIDSO's remote API. <br>
Mitigation: Avoid submitting confidential customer or business secrets in brand or issue prompts. <br>
Risk: Confirmed content generation spends 6 credits. <br>
Mitigation: Run generation only after explicit user confirmation of the 6-credit charge. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/tangyuanmile-coder/aidso-xiasou-geo-content) <br>
- [AIDSO API key settings](https://geo.aidso.com/setting?type=apiKey) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON command output and generated article text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIDSO_GEO_API_KEY; confirmed generation consumes 6 credits and calls AIDSO's remote API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
