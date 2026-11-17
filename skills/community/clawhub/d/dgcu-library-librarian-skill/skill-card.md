## Description:

远程调用东莞城市学院图书馆 AI 馆员，查询本馆与东莞图书馆馆藏、人民邮电和电子工业出版社知阅电子书，以及借阅规则和文献检索指导。无需企业微信登录。当用户消息包含“图书”“图书检索”“图书搜索”“书”“书名”“查找图书”“找书”“查书”，或表达找书、查询图书的意图时触发；也适用于图书馆咨询和文献检索指导。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenxianlong](https://clawhub.ai/user/chenxianlong)

### License/Terms of Use:

MIT

## Use Case:

External users, including students and community readers, can ask library questions and search Dongguan City University and Dongguan Library print holdings, plus ebooks from two publishers. The skill returns guidance and live search results while noting that borrowing and full-text access depend on each institution’s rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad book-related trigger terms may activate the skill on unrelated messages.

Mitigation: Review the trigger behavior and invoke the skill only for intentional library questions or book searches.

Risk: Queries are sent to the remote library service, and consultation requests may also be handled by its configured model provider.

Mitigation: Send only the query needed for the task; do not include chat history, credentials, account details, or sensitive personal information.

## Reference(s):

- [Server-resolved source repository](https://github.com/chenxianlong/dgcu-library-librarian-skill)
- [DGCU public library API](https://lib.dgcu.edu.cn/libai/api/public)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Text or Markdown summaries of consultation and live catalog results, with source links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the remote service and its limits; catalog hits do not grant borrowing or ebook access.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
