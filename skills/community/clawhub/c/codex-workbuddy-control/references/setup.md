# 安装与接入

## 前置条件

- Python 3.10 或更高版本。
- 一个 Codex 技能目录：`${CODEX_HOME:-$HOME/.codex}/skills`。
- 一个 WorkBuddy 能读取的共享目录，或允许人工传递任务包的目录。
- 可选自动触发器：文件监听器、桌面 Helper、计划任务或其他本地事件机制。

## 安装 Skill

把完整目录放到：

```text
${CODEX_HOME:-$HOME/.codex}/skills/codex-workbuddy-control/
```

也可以把仓库克隆到自定义位置，再创建指向该目录的符号链接。不要只复制 `SKILL.md`；脚本、参考和模板需要一起保留。

## 选择总线根

总线根是运行时数据目录，不在 Skill 发布包内。选择两个工作区都能读写、且不暴露敏感数据的目录：

```bash
export WB_BUS_HOME="<共享状态目录>"
python3 scripts/wb_bus.py init
```

独立配置共享台账和复盘目录：

```bash
export WB_BUS_LEDGER="<台账.md>"
export WB_BUS_REVIEW_DIR="<复盘目录>"
python3 scripts/wb_bus.py init
```

命令行覆盖优先于环境变量：

```bash
python3 scripts/wb_bus.py --root "<状态目录>" --ledger "<台账.md>" --review-dir "<复盘目录>" init
```

路径只存在于本机配置；不要把真实路径写入公开文档、样例或发布包。

## WorkBuddy 接入

自动执行器需要完成以下最小动作：

1. 调用 `claim --worker workbuddy`，取得最早的 pending 任务。
2. 读取 JSON 中的 `package_path` 和 `receipt_path`。
3. 按任务包执行；验收任务只读复跑并写 `回执包.md`。
4. 调用 `complete --id <编号>`。
5. 不能开始或无法执行流程时，调用 `fail --id <编号> --error "<真实原因>"`。

Codex/WorkBuddy 的总控提示词见 `references/开工提示词.md`。自动执行器不要在空队列时调用模型。

## 正向代码交付接入

Codex 完成任务后：

```bash
python3 scripts/wb_bus.py verify \
  --id WBV-YYYYMMDD-NNN \
  --title "<验收标题>" \
  --goal "<可观察的验收目标>" \
  --changed-file "<文件或配置>" \
  --cwd "<项目目录>" \
  --command "<不依赖交互式工具的命令>" \
  --evidence "<Codex 实际自测结果>"
```

至少提供一个改动文件和一个可复跑命令。脚本会生成 SHA-256 清单并拒绝 `rg`/`codex` 命令段。

## 反向候选接入

WorkBuddy 在隔离目录完成候选后，必须：

1. 写 `验证请求.md`，列出候选目录、文件、基线、命令、真实输出、风险和边界。
2. 在总线的 `待验证/<编号>.md` 写同一入口，或由 Codex 执行 `verify --candidate-dir` 登记。
3. 状态写 `WAITING_VERIFY`，不要自动唤醒 Codex。
4. 用户回 Codex 输入“验收 `<编号>`”。
5. Codex 实际复跑后调用 `complete --result PASS|FAIL --evidence`。

## 手动兜底

没有自动触发器时：

```bash
python3 scripts/wb_bus.py dispatch --id WB-YYYYMMDD-NNN --title "<标题>" --goal "<目标>"
python3 scripts/wb_bus.py status
```

把任务包路径和启动提示词人工交给 WorkBuddy。WorkBuddy 完成后写回执；控制台执行 `claim` 和 `complete`，或在用户明确知情时由 WorkBuddy 自己执行。

不要为了兜底复制任务包到第二个目录。复制会造成两份状态和重复劳动。

## 安全配置

- 总线根不要放在公开同步盘；如必须同步，先确认数据边界和权限。
- 任务包只写本机路径和数据范围，不写密钥、token、私有证书。
- 自动触发器账号只获得必要目录权限。
- 不修改运行中的 WorkBuddy 数据库；需要修改内部配置时先关闭 App 并取得授权。
- 不恢复每小时 ACTIVE 轮询。事件触发失效时保留人工兜底，不盲目重试。
