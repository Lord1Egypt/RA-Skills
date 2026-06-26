## Description: <br>
Checks Chinese marketing content for advertising-law banned words, platform SEO issues, safe replacement suggestions, and pre-publication performance predictions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content marketers, ecommerce operators, and developers use this skill to review or generate Chinese content for Baidu, Xiaohongshu, Douyin, Taobao, and JD while checking compliance wording, SEO fit, and publication readiness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted drafts, keywords, product plans, or client content may be sent to external Tencent Cloud API endpoints when the API scripts are used. <br>
Mitigation: Only run the API scripts on content approved for external processing, and avoid using them with confidential, regulated, or sensitive client drafts. <br>
Risk: API token handling can expose CN_SEO_TOKEN if secrets are copied into shared files or source control. <br>
Mitigation: Store CN_SEO_TOKEN only in a local .env file or an approved secret store, and keep it out of repositories and shared artifacts. <br>
Risk: The security scan reports unsafe script input handling for predict.sh and suggestions.sh. <br>
Mitigation: Avoid passing untrusted raw text to those scripts until their input handling is fixed, and review script behavior before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lm203688/cn-seo-optimizer) <br>
- [Web app](https://1341839497-jv04655vcs.ap-shanghai.tencentscf.com/) <br>
- [Compliance API base](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com) <br>
- [Banned Words Reference](references/banned-words.md) <br>
- [Keyword Research Reference](references/keyword-research.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with optional shell command usage and JSON-backed API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send submitted content, keywords, and platform selections to external Tencent Cloud API endpoints when API scripts are used.] <br>

## Skill Version(s): <br>
3.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
