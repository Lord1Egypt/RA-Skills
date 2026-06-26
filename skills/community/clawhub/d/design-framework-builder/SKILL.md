---
name: design-framework-builder
description: 设计框架自动生成套件（框架生成器）：收到设计需求后自动生成完整设计框架并发送群预览
---

# 设计框架套件 - 框架生成器

「设计框架自动生成套件」的第二个 skill，负责接收设计需求、生成框架文档、调用生图 prompt 脚本、发送预览到群组。

## 触发条件

群消息包含 `@huluxiaojinganghuluwa`（或你配置的 mention），且 `/tmp/design-framework-lock` 不存在（无进行中的任务）。

## 执行流程

1. **原子锁**：`mkdir /tmp/design-framework-lock`，防止并发触发
2. **去重检查**：与上次任务对比，完全相同则提示"已完成过"
3. **需求校验**：检测消息是否包含 ≥2 个设计需求字段（任务名称/尺寸/设计要求/文案等）
4. **参考图提取**：如消息含图片附件，提取路径供后续使用
5. **生成设计框架**：包含项目概述、设计定位、文案层级、视觉风格、版式结构、设计元素、字体建议、输出规范
6. **生成生图 Prompt**：调用 `generate_prompt.sh`
7. **发送预览**：群内发送框架预览 + 确认按钮

## 依赖脚本

所有脚本均位于 `design-framework-sender/` 目录：

- `generate_prompt.sh`：调用 OpenRouter API 生成生图 prompt
- `send_text.sh`：发送文本消息到 Telegram
- `config.py`：统一配置读取

## 无文字输出

全程通过 exec 执行 bash，不输出任何说明文字。

## 安装说明

请参考 `design-framework-sender` skill 的安装文档。
