## Description:

闲鱼多账号任务工作台。用户需要把多个闲鱼账号的商品草稿、竞品搜索或消息整理按 EasyBR 浏览器环境分组执行时使用。每个账号必须绑定唯一 browserId 和账号别名，同一浏览器串行、不同浏览器可有限并行；默认只读或 draft-only，不自动私信、改价、下架、删除或发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

面向管理多个闲鱼店铺的运营者，按各自的 EasyBR 浏览器环境整理商品草稿、查看公开竞品、汇总消息或处理订单任务，并生成清楚标注账号归属的结果。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 安全扫描指出，发布与订单履行可能无法始终遵守预期的确认边界；部分行为未检查，仍有不确定性。

Mitigation: 仅在确有需要且能先审阅运行脚本和权限时安装；监督发布与订单履行，并尽量使用只读或 draft-only 任务。

## Reference(s):

- [账号隔离规则](references/账号隔离.md)
- [Easy WebBridge 源码与安装说明](https://github.com/xxjrq/easy-webbridge)
- [Easy WebBridge Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)
- [EasyBR 官方下载页](https://www.ebrower.com/down.html)
- [EasyBR GitHub Release 镜像](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [按账号分组的 JSON 报告与 Markdown 汇总]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [结果包含账号、browserId、别名、任务状态和后续操作。]

## Skill Version(s):

1.1.1 (source: package.json; ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
