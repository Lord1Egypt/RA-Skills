# Codex × WorkBuddy Control

一个可移植的文件协议与标准库 CLI，用任务包、原子队列、回执和独立验收，把 Codex 与 WorkBuddy 的分工固定下来。

## 能力

- `WB-*`：WorkBuddy 执行资料、检索、报告或表格任务，Codex 验收交付物。
- `WBV-*`：Codex 完成并自测代码/Skill 后，WorkBuddy 只读复跑，返回 `WB_PASS`、`WB_FAIL` 或 `WB_PARTIAL`。
- `WBC-*`：WorkBuddy 在隔离目录做代码/Skill 候选，Codex 收到“验收 `<编号>`”后最终复跑。
- 文件原子队列、领取/完成、SHA-256 清单、共享台账、月度复盘。
- 无自动触发器时使用同一包进行人工派发，不产生第二套流程。

## 快速开始

```bash
export WB_BUS_HOME="$PWD/.wb-bus"
python3 scripts/wb_bus.py init
python3 scripts/wb_bus.py dispatch --id WB-YYYYMMDD-NNN --title "资料整理" --goal "形成可核对报告"
python3 scripts/wb_bus.py status
```

Codex 代码交付送验：

```bash
python3 scripts/wb_bus.py verify \
  --id WBV-YYYYMMDD-NNN \
  --title "配置修改独立验收" \
  --goal "确认测试通过且文件未被修改" \
  --changed-file "<交付文件>" \
  --cwd "<项目目录>" \
  --command "python3 -m pytest -q" \
  --evidence "Codex 已执行，EXIT=0"
```

WorkBuddy 候选登记：

```bash
python3 scripts/wb_bus.py verify \
  --id WBC-YYYYMMDD-NNN \
  --title "候选 Skill" \
  --candidate-dir "<隔离候选目录>"
```

候选目录必须已有 `验证请求.md`。Codex 最终验证后：

```bash
python3 scripts/wb_bus.py complete \
  --id WBC-YYYYMMDD-NNN \
  --result PASS \
  --evidence "Codex 实际复跑，EXIT=0"
```

## 目录

- `references/architecture.md`：角色、状态机、正向/反向验收链路。
- `references/setup.md`：安装、路径配置、接入与手动兜底。
- `references/commands.md`：命令清单和示例。
- `references/troubleshooting.md`：常见故障与恢复。
- `references/开工提示词.md`：可直接交给 Codex/WorkBuddy 的提示词。
- `references/step-prompts.md`：分步执行提示词。
- `scripts/wb_bus.py`：纯标准库 CLI。
- `scripts/self_test.py`：隔离回归测试。
- `templates/任务包.md`、`templates/回执包.md`、`templates/验证请求.md`、`templates/验证结果.md`。
- `icons/icon.png`（512×512）与 `icons/icon-256.png`（256×256）：无文字、无渐变的蓝图蓝标。

## 边界

本工具只管理文件状态，不注入 WorkBuddy 聊天窗口、不修改运行中的数据库、不调用云模型、不发布平台。真正执行任务的主体仍受各自权限和数据规则约束。

许可证见 `LICENSE.md`，来源说明见 `NOTICE.md`，版本记录见 `CHANGELOG.md`。
