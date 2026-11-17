## Description:

Helps agents write fact-checkable Chinese WeChat-style popular history and culture articles with scene-led openings, restrained humor, and clear boundaries between historical evidence, folklore, and fiction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and writing agents can use this skill to draft or revise Chinese popular-history articles for WeChat-style publication, including titles, sectioned article prose, concise references, and optional image-scene guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated history or culture articles can contain incorrect or misleading claims if the agent does not verify recent events, dates, people, statistics, or historical assertions.

Mitigation: Use the skill's evidence checklist: verify each key fact with reliable sources, label inference, and remove or mark unverified material before publication.

Risk: Humor or simplified comparisons may mishandle religion, ethnicity, colonialism, class, suffering, or other sensitive topics.

Mitigation: Apply the skill's stated boundaries: avoid jokes at the expense of believers, victims, rituals, or groups, and present sensitive comparisons with balanced, qualified language.

Risk: In multilingual or neutral-writing workflows, the skill can unnecessarily reshape content into a Chinese casual-history WeChat style.

Mitigation: Enable it only when that writing style is explicitly requested, as recommended by the security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songhonglei/skills/casual-history-article)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [CHANGELOG.md](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prose with title options, sectioned article drafts, concise references, and optional image-scene prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include 3-5 title options, a publish-ready article, 3-6 concise references, and optional cover or illustration scene lists when requested.]

## Skill Version(s):

1.1.0 (source: SKILL.md, CHANGELOG released 2026-07-26, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
