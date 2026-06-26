## Description: <br>
深度抓取和分析 Moltbook（AI agents 社交网络），挖掘 AI Agents 关注的核心问题和解决方案，生成可视化分析报告。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[Lucasyao1985](https://clawhub.ai/user/Lucasyao1985) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and analysts use this skill to browse public Moltbook feeds, identify recurring AI-agent community problems and solutions, and generate a daily Markdown analysis report for personal learning and research-oriented review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill browses Moltbook and can save scraped posts, comments, and generated reports locally. <br>
Mitigation: Run it only when the clawdchat workflow is intended, review the output directory, and delete retained reports or raw data when they are no longer needed. <br>
Risk: Moltbook page structure may change, which can break extraction or reduce report quality. <br>
Mitigation: Use browser snapshots to verify current page structure and update references/selectors.md when key elements no longer match. <br>
Risk: Community summaries may overstate consensus or include low-quality, spam, or unverified content. <br>
Mitigation: Apply the bundled spam rules, prefer high-value posts and comments, and review source posts before relying on generated conclusions. <br>


## Reference(s): <br>
- [ClawdChat Skill Page](https://clawhub.ai/Lucasyao1985/clawdchat) <br>
- [Moltbook](https://moltbook.com) <br>
- [Moltbook Page Selectors](references/selectors.md) <br>
- [Moltbook Spam Filtering Rules](references/spam-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown report with concise text status updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves daily reports under ~/myassistant/chat/moltbook-daily/ and may optionally retain raw scraped data locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact metadata lists 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
