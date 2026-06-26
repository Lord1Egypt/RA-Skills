---
name: orchestration-contract
description: >-
  L3 跨场景编排约定：统一路由消歧、执行顺序、outcome_code 与回退策略。
  不承载具体产品 API 参数；执行前共同前提见包根 SKILL.md「运行时契约」。
---

# 编排共用约定（orchestration-contract）

用于 `orchestration/` 下所有场景的最小共识：跨产品流程如何选择目标、如何执行、失败如何回退。  
它不是产品手册，也不替代各 `products/*/*-SKILL.md` 与 `orchestration/*/*-SKILL.md`。

## 标准流程模板（全场景统一）

所有 L2/L3 `Standard Workflow` 均应优先使用以下表格模板：

| Step | 脚本名 | 输入 | 输出 | 下一步 | 失败分支 |
|---|---|---|---|---|---|
| N | `<script>.py` | 必填参数 + 默认值策略 | 结构化产物（id/url/path/status） | Step N+1 | 显式映射 `outcome_code` 并给出处理动作 |

最小执行顺序：

1. 定目标：根据根 `SKILL.md` 路由命中 L2 或 L3。
2. 补参数：仅补 required 参数；可推断参数由 Agent 直接填充默认值。
3. 执行：只调用仓库已有 `scripts/` 与 `cli_capabilities.py` 暴露入口。
4. 交付：返回产物 URL/路径或标准错误语义。

## 冲突消歧

- 完整成片（文案+分镜+口播+画面）→ `chanjing-one-click-video-creation`
- 仅数字人口播（含卡通数字人）→ `chanjing-video-compose`
- 已有视频改口型（非卡通）→ `chanjing-avatar`
- 人设图/LoRA 及后续衍生 → `chanjing-text-to-digital-person`

## outcome_code（统一语义）

| code | 含义 | 下一步 |
|------|------|--------|
| `ok` | 执行成功 | 交付结果 |
| `need_param` | 缺少必要参数 | 继续补参 |
| `auth_required` | 凭据不可用 | 引导鉴权 |
| `upstream_error` | 上游接口失败 | 展示错误并给出重试建议 |
| `timeout` | 超时 | 引导轮询或稍后重试 |

### retry 与降级规则（统一）

- 同产品重试优先，最多 2 次；超过上限返回 `upstream_error` 或 `timeout`。
- `auth_required` 必须回到凭据链路，鉴权完成后从当前业务步骤继续。
- 任何“跨产品降级”都必须先征得用户确认，再执行目标切换。
- 仅当脚本硬校验失败且无法推断时返回 `need_param`，避免过度追问。

## 边界

- 不在编排文档里重复产品 API 字段细节。
- 不在编排层新增“平行产品脚本”替代现有 `products/*/scripts/*`。
- 运行时副作用、凭据读写和落盘边界以根 `SKILL.md` 为准。
