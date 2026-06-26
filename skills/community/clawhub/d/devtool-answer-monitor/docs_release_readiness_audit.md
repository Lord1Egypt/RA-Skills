# Release Readiness Audit

## 审计结论

当前 `geo-monitor-toolkit` 已具备 **最小可运行评估骨架**，但距离一个让新访客快速建立信任、让协作者明确参与路径、让团队感知版本稳定性的开源项目，仍有明显差距。本轮用户提出的 P0/P1 建议基本成立，尤其集中在 **发布感、演示感、协作感、趋势可视化与 CLI 入口** 五个层面。

## 差距矩阵

| 项目 | 当前状态 | 差距级别 | 后续动作 |
|---|---|---|---|
| 正式版本号与 changelog | 尚无 `CHANGELOG.md`，也没有明确 `v0.2.0` 发布说明 | P0 | 补版本文件、changelog、release note 草稿 |
| README 顶部徽章 | 当前无 Release / CI / Python 运行相关徽章 | P0 | 增加 Release、CI、Python 版本徽章 |
| Quick Demo 体验 | 已有 `make sample-report` 命令，但缺预期输出说明与截图证据 | P0 | 在 README 增加单命令 demo、产物路径与截图 |
| 样例产物快照 | sample-run 已有 summary/metrics/report，但缺统一展示 raw + summary + report 的快照导览 | P0 | 补充样例快照目录与 README 引导 |
| Issues 模板 | 当前无 `.github/ISSUE_TEMPLATE/` | P1 | 增加 bug / feature / new query-pool request 模板 |
| CONTRIBUTING | 当前无贡献流程文档 | P1 | 增加“如何新增一个行业样例”模板化流程 |
| Leaderboard | 当前只有 summary.json 和 metrics.csv，无趋势化展示 | P1 | 增加按模型维度聚合的轻量 leaderboard 与趋势文件 |
| Repair loop 案例 | 目前只有一个 sample repair validation | P1 | 补 2-3 个带 T+7 / T+14 的案例 |
| CLI 入口 | 目前仅脚本调用，无 `python -m geo_monitor` 入口 | P1 | 增加包结构与 CLI 封装 |
| GitHub About 区域 | 仓库 About 为空 | P0 | 准备一句描述、Topics 与主页建议；若权限允许则更新 |
| Release 页面 | 当前无 GitHub Release | P0 | 生成 `v0.2.0` release notes，并尽量通过 CLI 创建 |
| 结果可视化证据 | 当前缺截图或图像化趋势展示 | P0 | 生成 leaderboard 图或截图并在 README 中引用 |

## 立即优先级判断

本周内最应优先完成的不是继续扩展 playbook，而是强化 **首次访问体验** 与 **正式发布信号**。具体而言，应先完成以下闭环：

1. 把仓库升级为 `v0.2.0`，并给出 changelog；
2. 在 README 顶部补齐徽章、Quick Demo 和预期输出证据；
3. 让 sample-run 从“文件存在”升级为“看得懂的完整快照”；
4. 让协作者一眼知道如何提 issue、如何新增行业样例；
5. 让访客能看到至少一个轻量 leaderboard 或趋势视图；
6. 让 CLI 入口把使用门槛从“看脚本”降到“跑命令”。

## 风险与限制

当前主要风险不是仓库结构本身，而是 **GitHub 侧权限**。此前已出现工作流文件推送受 `workflows` 权限限制的问题，因此本轮涉及 GitHub Release、About 区域和部分 `.github/` 文件时，需要预留“本地已完成、远端可能需人工补推”的交付路径。
