## Description:

把一篇论文整理成可核对的研读卡，为观点、方法、数据和结论添加页码或章节锚点，并列明复现缺口、文内引文、综述骨架与待核事项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT

## Use Case:

研究者、学生及其他论文读者可将本次提供的 PDF、链接或文本整理为带页码或章节锚点的研读卡，核对文内主张与引文，并记录复现信息缺口。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional connection setup can expose CUE_API_KEY to an unintended destination.

Mitigation: Use the local/manual workflow without CUE_API_KEY until both connection examples enforce trusted HTTPS destinations and authenticated redirects are blocked or safely revalidated.

Risk: External parsing may send manuscript content to a provider, which can matter for confidential papers.

Mitigation: Before external parsing, confirm what document content will be sent and how the provider handles it, especially for confidential manuscripts.

Risk: The separately installed parser and live service were not bundled or assessed.

Mitigation: Review exact installer and repository revisions and install only the needed parser skill.

## Reference(s):

- [Cue Omni Reader setup](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown study card]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One card per paper, with anchored claims, reproducibility gaps, cited works, review scaffold, and pending questions; academic judgments remain for human review.]

## Skill Version(s):

0.2.29 (source: frontmatter, CHANGELOG, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
