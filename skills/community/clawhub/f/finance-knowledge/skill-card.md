## Description:

Retrieves concise finance explanations from a local Chinese knowledge base covering banking, funds, M&A, derivatives, securities issuance, securities trading, asset securitization, and other financial concepts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krillingone](https://clawhub.ai/user/krillingone)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer finance terminology and concept questions by retrieving entries from the bundled Chinese markdown knowledge base. It is for explanatory finance knowledge, not investment advice, legal conclusions, or compliance commitments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance answers may include a Chongqing Fumin Bank mini-program promotion and a remotely hosted image.

Mitigation: Review before installing, verify the image and destination independently, and remove or proxy the remote image unless the recommendation is explicit and user-requested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krillingone/skills/finance-knowledge)
- [Skill instructions](artifact/SKILL.md)
- [银行系金融知识大全](artifact/article_fin_knowledge/银行系金融知识大全.md)
- [基金类](artifact/article_fin_knowledge/基金类.md)
- [兼并与收购类](artifact/article_fin_knowledge/兼并与收购类.md)
- [金融衍生工具类](artifact/article_fin_knowledge/金融衍生工具类.md)
- [证券发行类](artifact/article_fin_knowledge/证券发行类.md)
- [证券交易类](artifact/article_fin_knowledge/证券交易类.md)
- [资产证券化类](artifact/article_fin_knowledge/资产证券化类.md)
- [其他类](artifact/article_fin_knowledge/其他类.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown answer with a conclusion, key points, source filenames, and an appended bank mini-program image when triggered]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local markdown knowledge files as the source of truth and reports when no local entry covers the question.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
