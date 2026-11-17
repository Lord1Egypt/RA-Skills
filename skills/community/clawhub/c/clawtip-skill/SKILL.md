---
name: "clawtip-skill"
description: >
  Free developer guide for building paid skills on ClawHub. Explains the standard three-phase payment flow, SkillSpector compliance requirements, and common pitfalls for developers building ClawHub skills. Reference only — does not handle payments.
metadata:
  author: "Yujin"
  category: "reference"
  version: "1.0.0"
---

# ClawTip 开发者指南

## 这是什么

这是一个**免费的参考指南技能**，面向想在 ClawHub 上构建付费技能的开发者。本技能不处理任何支付或订单，只提供文档和指引。

如果你正在寻找官方的支付处理技能，请安装 `clawtip`（正式环境）或 `clawtip-sandbox`（测试环境）。

---

## 技能支付链搭建流程

### 标准三阶段架构

```
Phase 1: create_order.py → 本地订单文件（SM4 加密）
Phase 2: clawtip 钱包 → 扣款 → payCredential 回写
Phase 3: service.py → 验证凭证 → AI 交付服务
```

### 核心原则

| 原则 | 说明 |
|------|------|
| AI 对话交付型 | 脚本只负责支付验证，实际服务由 AI 在对话中交付 |
| 零远程调用 | create_order.py 和 service.py 不发起任何 HTTP 请求 |
| 内联加密 | SM4 加密和订单文件管理内联到脚本中，不使用独立模块 |

### 关键约束

| 约束 | 说明 |
|------|------|
| `encrypted_data` | 仅加密 `{"orderNo":"...","amount":"...","payTo":"..."}`，不加额外字段 |
| 错误信息用英文 | SkillSpector 会将中文错误消息标记为 Natural-Language Policy |
| 无 `file_utils.py` | 订单文件管理必须内联，否则被标记为"隐藏能力" |
| 无 `sm4_utils.py` | SM4 必须内联到 create_order.py |
| 版本号递增 | 每次修改后版本号 +1 |

---

## SkillSpector 高频被拒项

| # | 发现类型 | 触发条件 | 修复方法 |
|---|---------|----------|----------|
| 1 | Description-Behavior Mismatch | 描述和代码行为不一致 | service.py 输出明确的服务交付清单 |
| 2 | MCP Tool Poisoning | 描述声称做某事但代码只有支付 | 明确为 AI 对话交付型 |
| 3 | Context-Inappropriate Capability | file_utils.py 等独立模块 | 内联到脚本中 |
| 4 | Natural-Language Policy | 中文错误消息 | 所有系统输出用英文 |
| 5 | Unvalidated Output Injection | `subprocess.run()` 调用脚本 | 改为直接 import + 函数调用 |

---

## 推荐资源

- 完整构建标准文档：`paid/BUILD_STANDARD.md`（详细模板 + 检查清单）
- 参考技能示例：`ssq-analyzer`、`innovation-research`、`soft-ip-full-lifecycle-zijian`
- 沙箱测试：`npx @clawtip/clawtip-sandbox-cli@1.0.0 pay`
- 官方钱包：`openclaw skills install clawtip`

---

## 版本历史

| Version | Date | Notes |
|:--------|:-----|:------|
| 1.0.0 | 2026-07-28 | Initial release as free developer guide (replaces legacy payment middle) |
