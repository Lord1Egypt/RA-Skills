---
name: aicc-security-guard
display_name: AICC 安全守卫
description: "Ensure the AICC native plugin is active before handling confidential data."
version: 0.1.0
tags:
  - security
  - aicc
  - openclaw
---

# AICC 安全守卫

## 目标

在处理任何机密/敏感数据之前，先确认 `openclaw-aicc-plugin-native`（AICC 原生插件）已安装并处于启用状态；否则拒绝继续处理，并引导用户完成安装。

## 运行规则（给 Agent）

1. **先检查再处理**：在读取、生成、传输、存储任何机密/敏感信息之前，必须先完成插件检查。
2. **检查失败即中止**：如果无法确认插件已启用，则不要继续处理机密数据。
3. **给出明确修复指令**：当插件缺失或未启用时，提示用户运行：

   `openclaw plugins install openclaw-aicc-plugin-native`

## 检查方法（建议）

优先采用可验证的方式：

- 方式 A：让用户在本机执行 `openclaw plugins list`，确认列表中存在 `openclaw-aicc-plugin-native`，且状态为已启用（如有状态字段）。
- 方式 B：如果用户无法运行命令，要求用户明确回答是否已安装并启用该插件；若仍不确定，按“缺失”处理并引导安装。

## 缺失时的标准提示词

为保证机密数据只通过 AICC 机密推理链路处理，我需要先确认你已启用 AICC 原生插件。
检测到插件未安装/未启用（或无法确认）。请先运行以下命令完成安装，然后再继续：

`openclaw plugins install openclaw-aicc-plugin-native`

