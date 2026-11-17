# 旧项目引导 2.1

当现有项目已有 CMS 记录、但没有可信 Active Packet 时使用 Legacy Bootstrap。默认始终只读。

## 读取边界

1. 将项目根目录解析为真实路径。
2. 大小写不敏感地寻找一个直接子目录 `Docs`。
3. Docs 目录不唯一，或真实路径越出项目时拒绝继续。
4. 先索引文件名、大小和修改时间。
5. 只读取可能代表当前状态的文件，以及它们明确链接的文件。
6. 不递归读取历史 Markdown 正文、Handoff 或完整日志。

可能的当前文件包括 Active Packet、TARGET、ACCEPTANCE、当前 Work Order、Current Assignment、当前状态和最新有效 QA 决策。名称含 `archive`、`history`、`completed` 或 `handoff` 的文件，除非被已选择文件明确链接，否则不视为当前权限来源。

## 冲突检测

出现以下任何重大冲突时零写入：

- 存在两个或以上 Current Assignment，且没有明确 Current Override；
- TARGET、STATUS 或 Work Order 指向不同当前路线；
- Accepted 标题后存在具有替代效力的 Failed 或 Blocked 决策；
- 缺少目标、验收、范围或授权；
- 把 Contract、Governance 或 Artifact 证据描述为 Runtime 完成；
- 权威链接越出项目；
- 已有 Active Packet 的权限无效或互相矛盾。

只返回一个 Owner 请求，其中合并所有路线选择、冲突证据路径、建议默认值及各选择后果。

## 明确覆盖

清楚标记为 `Current Override`、`Current Effective` 或同义当前路线声明的文件，可以覆盖旧记录。保留旧文件为历史，并以该覆盖声明作为权限依据。不能只因时间较新就推断发生覆盖。

## 无冲突草案

生成一个 Packet，包含：

- 用户可见目标；
- 最小当前范围与 Non-Goals；
- 交付类别；
- 一个有界阶段结果；
- 与证据类别对应的验收标准；
- 项目内写入边界；
- 权威来源与 SHA-256 指纹；
- 唯一一个 Next Action。

原则上不超过约 120 行。`--write` 只原子写入 `Docs/ACTIVE_PACKET.md`；不会重命名、删除或改写旧记录。

## 命令

```text
bootstrap-active-packet.mjs --workspace <path> --language zh-CN --json
bootstrap-active-packet.mjs --workspace <path> --language zh-CN --json --write
```

第一条命令永远只读。冲突结果使用非零退出码，并返回 `written: false`。
