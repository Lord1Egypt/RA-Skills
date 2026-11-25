# 分步提示词

每一步都可直接复制。只有上一步通过才进入下一步。把 `<...>` 换成本任务实际值。

## S1：范围与契约

```text
只执行协作流程的第 1 步：锁定范围与契约，不写业务代码、不发布。

读取项目 AGENTS.md、README、相关规则和 $codex-workbuddy-control 的 references/architecture.md。输出：
- 总线根、共享台账和复盘目录（只写占位值，不写私人路径）；
- Codex 与 WorkBuddy 各自负责/不负责的事项；
- 本次使用 WB、WBV、WBC 中的哪些编号；
- 数据边界、外发限制、验收命令和失败处理；
- 明确不修改运行中 SQLite、不恢复 ACTIVE 轮询。

完成后运行 init/status，报告真实路径和状态。未通过不进入 S2。
```

## S2：实现与自测

```text
只执行第 2 步：Codex 完成实现并自测；不创建 WorkBuddy 验收包，不发布。

先读项目规则和现有代码，再做最小必要修改。完成：
- 运行语法检查、构建和可执行测试；
- 记录真实命令、EXIT、关键输出；
- 生成变更文件清单和 SHA-256；
- 列出无法验证项与风险。

自测未通过先修复；修复失败如实报告 FAIL。不要写“应该通过”。
```

## S3：独立验收包

```text
只执行第 3 步：创建 WBV 只读独立验收包；不发布。

使用真实自测证据运行：
python3 <SKILL_ROOT>/scripts/wb_bus.py --root "<WB_BUS_HOME>" verify \
  --id WBV-YYYYMMDD-NNN --title "<标题>" --goal "<目标>" \
  --changed-file "<文件>" --cwd "<目录>" \
  --command "<纯 shell/Python 可复跑命令>" --evidence "<实际自测证据>"

检查包内 SHA-256、cwd、命令、验收标准、风险和只读边界。WorkBuddy 不得改码、修复、合并或发布。等待 WB_PASS/WB_FAIL/WB_PARTIAL；只有 WB_PASS 才完成。失败另建新编号。
```

## S4：候选交接或发布准备

```text
只执行第 4 步：处理 WBC 候选或准备发布，不擅自发布。

若为 WBC-YYYYMMDD-NNN 候选：
- 读取验证请求和真实候选差异；
- Codex 实际复跑；
- PASS 写验证结果并移到 verified；
- FAIL 写返工项并移到返工；
- 不把 WorkBuddy 自报当最终结论。

若为发布准备：
- 先确认用户已授权目标平台和版本；
- 做隐私/路径/敏感词扫描、完整性检查和打包；
- 只有全部通过并得到 WB_PASS 才进入发布；
- pending 只写 pending，不写成已发布；
- 发布后逐个回查版本、审核、图标和 latest 状态。
```

## S5：收尾

```text
只执行收尾：更新共享台账和 YYYY-MM 固定复盘，写审计记录，清理本次临时缓存。

保留任务包、回执、验证结果、原始资料、交付物、台账和复盘。报告：
- 最终结果；
- 实际验证命令和输出；
- 遗留风险；
- 回滚方式；
- 绝对路径。
```
