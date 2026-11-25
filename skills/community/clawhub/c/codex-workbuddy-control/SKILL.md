---
name: codex-workbuddy-control
description: "编排 WorkBuddy 派发、只读验收与候选交接；不代替业务执行。"
version: 0.1.0
license: MIT
---

# Codex × WorkBuddy 控制

## 何时使用

- 把资料检索、报告、表格交给 WorkBuddy，由 Codex 验收结果。
- Codex 已完成代码、脚本、配置、构建或安全检查，需要 WorkBuddy 只读复跑。
- 用户在 WorkBuddy 直接完成代码/Skill 候选，回到 Codex 输入“验收 `<编号>`”。
- 需要共享任务台账、月度复盘、人工派发兜底或排障。

不用于：纯问答、单事实核对、临时诊断、失败实验；这些直接由当前会话完成。

## 固定分工

| 主体 | 职责 |
|---|---|
| Codex | 代码、脚本、配置、构建、测试、安全检查和最终发布 |
| WorkBuddy | 资料、检索、报告、表格；代码/Skill 只做独立验收或隔离候选 |

WorkBuddy 验收时不得改码、修复、格式化、合并或发布。Codex 不得把 WorkBuddy 的自报改成 PASS。

## 四条路径

1. **普通执行**：Codex 建 `WB-YYYYMMDD-NNN` 任务包 → WorkBuddy 执行并写 `回执包.md` → Codex 核对实际交付。
2. **Codex 交付验收**：Codex 自测 → 建 `WBV-*` 只读验收包 → WorkBuddy 独立复跑 → `WB_PASS/WB_FAIL/WB_PARTIAL` → Codex 决定完成或返工。
3. **WorkBuddy 候选**：新建 `WBC-*` → 只写隔离候选目录 → 写 `验证请求.md` 和 `待验证/<编号>.md` → 状态 `WAITING_VERIFY` → 用户回 Codex 说“验收 `<编号>`” → Codex 最终复跑、合并或发布。
4. **手动兜底**：无自动触发器时，仍用同一任务包和队列；人工把包交给 WorkBuddy，完成后调用 `complete`。

验收编号不复用。`WB_FAIL` 或候选返工必须另起新编号。

## 最小命令

```bash
python3 scripts/wb_bus.py --root "$WB_BUS_HOME" init
python3 scripts/wb_bus.py --root "$WB_BUS_HOME" dispatch --id WB-YYYYMMDD-NNN --title "标题" --goal "目标"
python3 scripts/wb_bus.py --root "$WB_BUS_HOME" verify --id WBV-YYYYMMDD-NNN --title "验收标题" --goal "验收目标" --changed-file "<文件>" --cwd "<目录>" --command "<可移植命令>" --evidence "自测 EXIT=0"
python3 scripts/wb_bus.py --root "$WB_BUS_HOME" claim --worker workbuddy
python3 scripts/wb_bus.py --root "$WB_BUS_HOME" complete --id WBV-YYYYMMDD-NNN
python3 scripts/wb_bus.py --root "$WB_BUS_HOME" status
```

候选入口：

```bash
python3 scripts/wb_bus.py --root "$WB_BUS_HOME" verify \
  --id WBC-YYYYMMDD-NNN --title "候选标题" --candidate-dir "<隔离候选目录>"
python3 scripts/wb_bus.py --root "$WB_BUS_HOME" complete \
  --id WBC-YYYYMMDD-NNN --result PASS --evidence "Codex 实际复跑 EXIT=0"
```

`--root` 也可用环境变量 `WB_BUS_HOME`；台账和复盘目录分别用 `WB_BUS_LEDGER`、`WB_BUS_REVIEW_DIR` 覆盖。不得把机器专用路径写进发布包。

## 执行规则

1. 建包前确认编号唯一，并读取实际文件、README、项目规则和任务边界。
2. 正向验收包至少包含：改动文件 SHA-256、cwd、可移植复验命令、Codex 自测证据、验收标准、风险和数据边界。
3. 复验命令不得依赖 `rg`、`codex` 或交互式配置；优先 Python、绝对路径工具和纯 shell。
4. WorkBuddy 必须逐条记录实际 `EXIT`、关键输出和失败原因；无法安全复跑只能 `WB_PARTIAL`。
5. 回执存在不等于通过；Codex 要核对文件、哈希、命令证据和未完成项。
6. 候选目录只能是 WorkBuddy 工作区或用户指定隔离目录，不得直接写 Codex 生产路径、全局 Skill、插件或发布包。
7. 完成或失败都要更新共享台账和当月复盘，只写真实结果；未知写“待补充”。

## 数据与安全

- 公司图纸、施工资料、客户信息和密钥不得进入公开任务包、回执、日志或发布物。
- 联网、上传、在线 OCR、第三方转换和 Git 远端传输前，先列范围与字节并取得明确同意。
- 不修改运行中的 WorkBuddy SQLite 或内部配置；不恢复每小时 ACTIVE 自动轮询。
- 不删除任务包、回执、原始资料或交付物；临时缓存只清理本次产生且已核验的文件。
- 不伪造测试、节省比例、发布状态或审核结果。

## 参考资料

- 架构与状态机：`references/architecture.md`
- 安装与路径配置：`references/setup.md`
- 命令与人工兜底：`references/commands.md`
- 排障：`references/troubleshooting.md`
- 可直接复制的开工提示词：`references/开工提示词.md`
- 分步提示词：`references/step-prompts.md`
- 脚本：`scripts/wb_bus.py`
- 模板：`templates/任务包.md`、`templates/回执包.md`、`templates/验证请求.md`、`templates/验证结果.md`
