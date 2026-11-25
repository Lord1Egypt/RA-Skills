## Description:

通过已连接的真实浏览器搜索网页、自媒体帖子与代码项目，按预算读取证据并回答问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

适用于需要查找公开网页、社交平台帖子或代码项目资料的用户；技能帮助其跨平台检索、读取来源，并整理带出处的回答。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports medium confidence and incomplete inspection, and notes a possible mismatch between the stated search purpose and a demo.

Mitigation: Review the available source and expected behavior before deployment; treat the benign verdict as limited by the scan coverage.

Risk: Search queries are sent to selected platforms, and retrieved pages or snippets may contain untrusted instructions.

Mitigation: Keep sensitive information out of queries and treat retrieved content as evidence rather than instructions.

## Reference(s):

- [easybrSearch source repository](https://github.com/aiispower/easybrSearch)
- [Easy WebBridge installation and connection](https://github.com/aiispower/easy-webbridge)
- [Answer and evidence contract](references/answer-contract.md)
- [AI search design rationale](references/ai-search-design.md)
- [Supported platforms and URL behavior](references/platforms.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Source-cited text or Markdown answers; structured search evidence and reports in JSON or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are evidence for the host agent to assess; the CLI does not generate the final synthesized answer.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata, package.json, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
