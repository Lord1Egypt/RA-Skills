## Description: <br>
CN SEO Optimizer helps agents check Chinese marketing and platform content for advertising-law banned words, SEO issues, safe replacements, and pre-publication performance predictions using bundled guidance and optional API-backed scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content teams, and developers use this skill to review or generate Chinese content for Baidu, Xiaohongshu, Douyin, Taobao, and JD with platform SEO guidance and advertising-law compliance checks. It can produce reports, safer rewrite suggestions, and prediction-calibration guidance before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checked content may be sent to the listed remote API service when API-backed scripts are used. <br>
Mitigation: Use the scripts only with content that is appropriate to send to the provider, and review the provider's data handling before using confidential, regulated, or client material. <br>
Risk: The server security review reports unsafe shell/Python argument handling in the scripts. <br>
Mitigation: Review and patch script argument handling before automated or high-trust use, and avoid passing untrusted text directly to the scripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lm203688/cn-seo-optimizer) <br>
- [Web App](https://1341839497-jv04655vcs.ap-shanghai.tencentscf.com/) <br>
- [Remote API Endpoint](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com) <br>
- [Token Request Issues](https://github.com/lm203688/cn-seo-optimizer/issues) <br>
- [Banned Words Reference](references/banned-words.md) <br>
- [Keyword Research Reference](references/keyword-research.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, rewritten Chinese content, JSON from local keyword checks, and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Script-assisted checks may call remote API endpoints for compliance scans, replacement suggestions, and prediction scoring.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
