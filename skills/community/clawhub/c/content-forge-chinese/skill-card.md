## Description: <br>
Content Forge converts Chinese-language articles, podcasts, private-community posts, paywalled media, and videos into reports, podcasts, mind maps, and presentation-ready outputs with NotebookLM or local-LLM fallbacks. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[sirkayzh](https://clawhub.ai/user/sirkayzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-language content creators, analysts, and knowledge workers use this skill to transform WeChat articles, podcasts, community posts, news articles, and videos into summaries, deep-analysis reports, podcasts, mind maps, and slide decks. The workflows emphasize source-completeness labels, AI-inference labels, and fallback paths when NotebookLM or network access is unavailable. <br>

### Deployment Geography for Use: <br>
Global; optimized for Chinese-language content and China network conditions. <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill may use browser automation, logged-in sessions, raw cookies, proxies, external AI services, and cloud document systems. <br>
Mitigation: Run browser automation in an isolated profile, avoid pasting raw session cookies, use only credentials required for the chosen workflow, and review each external upload or write destination before execution. <br>
Risk: The security summary flags paywall bypass behavior and use with content that may be confidential, personal, or subscription-protected. <br>
Mitigation: Use the skill only with content the user is authorized to access and transform; prefer local-only or manual input paths for paywalled, confidential, or personal material. <br>
Risk: Generated outputs can mix source facts with AI interpretation, especially when only metadata or partial content is available. <br>
Mitigation: Keep the artifact's required source-completeness, AI-inference, and warning labels in every output, and verify important claims against the original source. <br>


## Reference(s): <br>
- [Content Forge README](artifact/README.md) <br>
- [Honesty Rules](artifact/references/honesty-rules.md) <br>
- [Tool Map](artifact/references/tool-map.md) <br>
- [China Network Guidance](artifact/references/china-network.md) <br>
- [Paywall Strategies for China](artifact/references/paywall-strategies-cn.md) <br>
- [Troubleshooting](artifact/references/troubleshooting.md) <br>
- [WeChat to IMA/Feishu Scenario](artifact/scenarios/01-wechat-to-ima.md) <br>
- [Podcast to Feishu/IMA Scenario](artifact/scenarios/02-xiaoyuzhou-to-feishu.md) <br>
- [Video to PPT Scenario](artifact/scenarios/05-shipinhao-to-ppt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, structured JSON metadata, Mermaid mind maps, shell command snippets, and guidance for generated audio, PDF, or PPTX artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include source completeness, AI inference ratio, warnings, and links or destinations for IMA, Feishu, NotebookLM, or local files when applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
