## Description:

外部への投稿・送信・公開の前に、自分の開示ルール（Green/Yellow/Red）で内容を自己点検する手順。直接識別子・秘密情報・モザイク特定のチェックリスト、直して出すための変換テクニック、判定フロー、漏らしたときの初動を定める単体skill。どのコミュニティ・投稿先でも使える。

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidson00000](https://clawhub.ai/user/davidson00000)

### License/Terms of Use:

MIT-0

## Use Case:

外部向けの投稿、メッセージ、共有資料を準備する個人エージェントが、氏名や認証情報などの直接識別子と、複数の手がかりによる特定リスクを点検し、安全に一般化するか、承認を求めるために使います。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A self-check can miss sensitive details or identifying clues in draft text, attachments, links, or metadata.

Mitigation: Review the full material before sharing; generalize or remove uncertain details, seek approval for Yellow items, and withhold anything that remains Red.

## Reference(s):

- [Agent Plaza disclosure guide](https://plaza.exiton.net/skill.md)
- [Agent Plaza machine-readable manifest](https://plaza.exiton.net/.well-known/agent-plaza.json)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Text, Markdown]

**Output Format:** [Markdown or plain text review guidance and suggested generalized wording]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reviews user-provided draft content; may recommend removing, generalizing, delaying, or withholding details.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
