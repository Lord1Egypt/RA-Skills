# Workbench & Prompt Testing (ctqa unified framework, migrated 2026-10-29) — moved verbatim from SKILL.md

> Moved verbatim from `SKILL.md` on 2026-11-03 (ct-base §16.1: SKILL.md <=200 lines, detail sinks to `references/`). No content deleted.

---

## 工作台与提示词测试（统一框架，2026-10-29 迁移）

> 已迁移至 CT 系列统一测试框架 `ctqa`（位于 `ct-base/testing/ctqa/`）。运行入口：`python -m ctqa run --skill ct-literature`。配置在 `ctqa.config.json`。规范详见 `ct-base/references/workbench_ui.md` §23。

ct-literature 通过 legacy 桥接保留两套核心测试：

| 层 | 文件（legacy 保留） | 覆盖 |
|---|---|---|
| **W1** | `workbench/_tests/_support.py` + `workbench/_tests/test_static.py` | 前后端事件协议四元核对（传输层 × 后端 × 业务层 × CLI）、i18n 键对齐、DOM id 交叉引用、语法校验 |
| **P5** | `tests/prompt_usage/_support.py` + `tests/prompt_usage/test_l6_coze.py` | Coze 信封 11-key 硬白名单脱敏 + 真实白名单发送 e2e（`CT_COZE_E2E=1`） |

> **运行方式**：`python -m ctqa run --skill ct-literature`（按配置自动执行 W0 + W1 + P5）。
> 旧的独立入口（`workbench/_tests/run_all.py`、`tests/prompt_usage/run_all.py`）已清理。

详细 SOP（四层设计 / 事件协议核对规则 / 七层提示词测试）保留在历史文档：[references/workbench_testing.md](references/workbench_testing.md) 与 [references/prompt_usage_testing.md](references/prompt_usage_testing.md)。
