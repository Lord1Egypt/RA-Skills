## Description: <br>
去除中文/英文/日文文本的“AI味”，以信息传递为核心先补齐事实/证据/取舍/边界，再按场景重写并清理模板化口癖与格式指纹；适用于文案、邮件、报告、PRD、社媒内容与学术写作的去AI味改写，以及识别并拦截假证据句式与虚构参考文献。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yamasite](https://clawhub.ai/user/yamasite) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External writers, editors, and developers use this skill to rewrite Chinese, English, and Japanese text for higher information density, clearer audience fit, fewer templated AI-writing fingerprints, and stronger citation discipline. It can also guide agents to produce rewrite notes and targeted follow-up questions when facts, sources, constraints, or boundaries are missing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive or confidential source text may be exposed to an agent during rewriting. <br>
Mitigation: Review and redact sensitive text before use, especially when the rewrite task involves internal communications, customer support, legal language, reports, or unpublished research. <br>
Risk: The optional scanner can write local JSONL scan summaries when --logfile is used. <br>
Mitigation: Use --logfile only with an approved local path and avoid logging text-derived metadata for sensitive material. <br>
Risk: Style-linter findings may be mistaken for proof that text was AI-generated. <br>
Mitigation: Treat scan output as edit guidance only, and keep the skill's citation-verification and hallucination gates separate from authorship claims. <br>
Risk: Aggressive de-AI rewriting can remove necessary legal, technical, or factual precision. <br>
Mitigation: Preserve names, interface terms, legal commitments, data, citations, and stated constraints unless the user explicitly authorizes changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yamasite/de-ai-voice) <br>
- [“AI 味”与“人味”的本质差别](references/principles.md) <br>
- [Wikipedia 等材料中的“AI 写作迹象”映射表](references/signs-of-ai-writing.md) <br>
- [参考文献/引用验真](references/citation-verification.md) <br>
- [中文：常见 AI 味与改写动作库](references/zh.md) <br>
- [English: AI-writing tells and rewrite moves](references/en.md) <br>
- [日本語：AIっぽさのサインと自然化の手筋](references/ja.md) <br>
- [模型/平台层“AI 味指纹”](references/model-tells.md) <br>
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) <br>
- [Fake citation checker](https://www.aidetectors.io/blog/fake-citation-checker) <br>
- [hallucinator citation verification tool](https://github.com/gianlucasb/hallucinator) <br>
- [Claude system prompt release notes](https://docs.claude.com/en/release-notes/system-prompts) <br>
- [Claude prompt engineering best practices](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with rewritten text, change notes, follow-up questions, and optional JSON scan reports from the local linter] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The optional scanner is a local heuristic style linter, not an AI-authorship detector; optional logging writes compact JSONL summaries only when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
