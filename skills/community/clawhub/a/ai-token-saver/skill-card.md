## Description:

한국어 특화 Context DB로 AI 토큰 사용량을 최대 96% 절감하며 프롬프트를 최적화하고 메모리 검색을 지원합니다.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorongss](https://clawhub.ai/user/dorongss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill to save, search, and summarize Korean-language working context through TokenSaver so repeated prompts can retrieve compact memory instead of reloading full source context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User content may be sent to and stored by the remote TokenSaver API without sufficient privacy, retention, or deletion disclosure.

Mitigation: Do not save secrets, credentials, regulated data, or confidential project material unless TokenSaver's handling terms have been reviewed and accepted.

Risk: Broad memory-related triggers can increase unintended activation risk.

Mitigation: Invoke the skill explicitly for scoped save or search tasks, and prefer a pinned, verified package version in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dorongss/skills/ai-token-saver)
- [TokenSaver website](https://tokensaver.ai)
- [TokenSaver API base](https://api.tokensaver.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown and terminal text with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include retrieved memory summaries, usage information, and TokenSaver API responses.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata; artifact manifest states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
