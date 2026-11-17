## Description:

Guides agents through Chinese-focused songwriting with rhymed lyric planning, pypinyin validation, pronunciation QA, MiniMax mmx music generation, and file delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to plan Chinese song projects, write rhymed lyrics, validate rhyme and pronunciation, configure MiniMax mmx music generation, and deliver generated songs after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Topic prompts, lyrics, and generation parameters may be sent to MiniMax through mmx.

Mitigation: Confirm MiniMax processing is intended before generation and confirm the delivery destination before sending generated audio to a chat or platform.

Risk: Chinese lyric rhymes, rare characters, or multitone characters may produce incorrect pronunciation in generated music.

Mitigation: Run pypinyin rhyme validation, scan rare and multitone characters, add explicit pronunciation hints, and perform listening review before final delivery.

Risk: Long lyrics or direct command-line lyric input can make generation unreliable.

Mitigation: Use a lyrics file for mmx generation and repeat or expand structures only after validating the full lyric workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/andyrenxu7255/skills/ai-songwriter-renxu)
- [MiniMax CLI](https://github.com/MiniMax-AI/cli)
- [MiniMax Platform Docs](https://platform.minimaxi.com/docs)
- [Rhyme Table Validation](references/rhyme-table-20260522.md)
- [Chengfei Songwriting Case Study](references/session-20260522-chengfei.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline code blocks, command templates, generated lyrics, and music generation parameters.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce generated audio files or delivery instructions when MiniMax mmx tooling is available.]

## Skill Version(s):

3.3.0 (source: server release evidence, SKILL.md frontmatter, clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
