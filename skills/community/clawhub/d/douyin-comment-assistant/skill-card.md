## Description:

读取抖音公开数据，按关键词搜索视频和图文、查看热榜、抓取博主公开作品并获取视频评论，以结构化 JSON 返回。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

短视频运营、品牌和数据分析人员可用它发现抖音内容与热点、查看公开账号作品，并汇总视频评论，用于选题、竞品分析和舆情观察。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 查询会把用户提供的关键词或链接发送给第三方数据服务；扫描覆盖不完整，部分源文件也未能完全解析。

Mitigation: 启用前核对技能用途及其发送的数据是否符合需要；只查询抖音公开数据，并避免提交不必要的信息或令牌。

## Reference(s):

- [使用说明与参数选项](references/options.md)
- [更新日志](references/changelog.md)
- [抖音数据服务与令牌配置](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [结构化 JSON 数据，以及命令使用和令牌配置说明]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [结果包含搜索、热榜、公开作品或评论数据；支持按关键词、时间、排序、内容类型和数量筛选。]

## Skill Version(s):

1.4.0 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
