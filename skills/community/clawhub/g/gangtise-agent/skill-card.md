## Description: <br>
通过 Gangtise Agent OpenAPI 拉取可直接引用的 Markdown 投研文本、热点话题报告和投研线索，适用于研究速览、纪要整理和 Agent 编排中的事实与观点补充。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gangtisegts](https://clawhub.ai/user/gangtisegts) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, analysts, and agent builders use this skill to call Gangtise OpenAPI endpoints for company summaries, investment logic, peer comparisons, earnings reviews, viewpoint debate, theme tracking, hot-topic reports, and research clues. It is suited to workflows that need fast Markdown research context for notes, briefings, or agent orchestration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Gangtise access credentials and can read them from environment variables or a local scripts/.authorization file. <br>
Mitigation: Prefer environment-provided secrets, restrict local credential-file permissions, and do not commit scripts/.authorization. <br>
Risk: Authorization headers are sent to the configured Gangtise OpenAI endpoint. <br>
Mitigation: Use the default trusted Gangtise endpoint and avoid setting GANGTISE_OPENAI_ROOT to an untrusted URL. <br>
Risk: The skill returns investment-research summaries, viewpoints, and structured clues that may be incomplete or time-sensitive. <br>
Mitigation: Review returned content against authoritative source material before using it for financial analysis or decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gangtisegts/gangtise-agent) <br>
- [Gangtise OpenAI API root](https://open.gangtise.com/application/open-ai) <br>
- [Gangtise authorization endpoint](https://open.gangtise.com/application/auth/oauth/open/loginV2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown text with optional saved Markdown or JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some calls poll asynchronous Gangtise content for up to 600 seconds; security-clue results may include usage-cost messaging.] <br>

## Skill Version(s): <br>
1.4.2 (source: server release metadata; artifact frontmatter reports 1.4.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
