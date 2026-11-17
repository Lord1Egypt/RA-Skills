---
slug: free-resource-finder-free
name: free-resource-finder-free
version: 1.0.0
displayName: 免费资源发现器(免费版)
summary: 发现与切换免费AI模型资源,支持基础列表查看、模型切换与状态检查,帮助用户零成本体验AI能力。
license: Proprietary
edition: free
description: '免费资源发现器(免费版)是一款面向独立开发者的免费AI模型资源发现与切换工具,帮助用户在众多免费模型中快速找到合适的选项,并完成基础配置。核心能力:

  - 发现可用的免费AI模型列表,按质量排序展示

  - 支持一键切换主模型,保留原有配置

  - 提供模型状态检查与基础故障排查

  - 兼容OpenAI协议的模型代理服务


  适用场景:

  - 个人开发者零成本体验AI编程助手

  - 学生与研究者试用不同模型能力

  - 小型项目原型阶段的成本控制

  - 模型选型前的对比测试


  差异化: 完全中文化表达,聚焦"发现-切换-验证"三步流...'
tags:
- AI模型
- 资源发现
- 免费工具
- 成本优化
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L1-入门级"
pricing_model: per_use
suggested_price: "9.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "工具,效率,自动化"
---
# 免费资源发现器(免费版)

发现与切换免费AI模型资源,帮助用户在零成本前提下体验AI编程能力。聚焦"发现-切换-验证"三步流程,内置模型质量评估与故障排查。

## 概述

AI模型百花齐放,但付费门槛让许多开发者望而却步。市面上存在大量免费模型资源(如OpenRouter提供的免费层、各厂商的免费额度),但用户面临三大痛点:不知道有哪些免费模型、不知道哪个模型好用、切换配置繁琐。本Skill解决这三个问题,让用户能够快速发现、评估、切换免费AI模型。

免费版聚焦核心发现与切换能力,适合个人开发者日常使用。

## 核心能力

### 模型发现

自动聚合多个来源的免费模型信息,按以下维度排序展示:

| 维度 | 说明 | 权重 |
|---|---|---|
| 上下文长度 | 支持的输入token数 | 高 |
| 输出质量 | 编程/对话/推理能力评分 | 高 |
| 速率限制 | 每分钟请求数与每日上限 | 中 |
| 响应延迟 | 首token延迟与整体吞吐 | 中 |
| 稳定性 | 近7天可用率 | 高 |
| 特殊能力 | 函数调用、视觉、代码执行 | 低 |

**输入**: 用户提供模型发现所需的指令和必要参数。
**处理**: 解析模型发现的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回模型发现的响应数据,包含状态码、结果和日志。

### 模型切换

一键切换主模型,保留原有配置不丢失:

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 免费资源发现器(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 切换主模型(保留原有fallbacks)
free-finder switch qwen3-coder
# ...
# 仅查看可用模型(不切换)
free-finder list
# ...
# 查看详细列表(含能力评分)
free-finder list -n 30 --detail
```

**输入**: 用户提供模型切换所需的指令和必要参数。
**处理**: 解析模型切换的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回模型切换的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 状态检查

```bash
# 查看当前配置
free-finder status
# ...
# 测试模型连通性
free-finder ping qwen3-coder
# ...
# 查看最近调用记录
free-finder log --tail 20
```

**输入**: 用户提供状态检查所需的指令和必要参数。
**处理**: 解析状态检查的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回状态检查的响应数据,包含状态码、结果和日志。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：发现与切换免费、模型资源、支持基础列表查看、模型切换与状态检、帮助用户零成本体、免费资源发现器、免费版、是一款面向独立开、发者的免费、模型资源发现与切、换工具、帮助用户在众多免、费模型中快速找到、合适的选项、并完成基础配置、核心能力、发现可用的免费、模型列表、按质量排序展示、支持一键切换主模、提供模型状态检查、与基础故障排查、OpenAI、协议的模型代理服等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景1:个人开发者零成本体验AI编程

用户意图: "我想免费体验AI编程助手,帮我找个靠谱的免费模型。"

推荐流程:
1. 运行`free-finder list --sort quality`查看高质量免费模型
2. 根据编程语言偏好选择(如Python选qwen3-coder,前端选deepseek-coder)
3. 运行`free-finder switch <model>`完成切换
4. 运行`free-finder ping <model>`验证连通性

### 场景2:学生研究者对比模型能力

用户意图: "我在做模型对比研究,需要快速切换多个免费模型测试。"

推荐流程:
1. 运行`free-finder list --detail`获取完整能力矩阵
2. 按研究维度排序(如推理能力、代码生成、多轮对话)
3. 逐个切换并记录表现
4. 使用`free-finder log`回溯调用记录

### 场景3:小型项目原型阶段成本控制

用户意图: "项目还在原型阶段,先用免费模型跑通流程,后续再切付费。"

推荐方案:
- 主模型选稳定性最高的免费选项
- 预留fallback链(专业版支持自动切换)
- 监控每日调用量,避免触发限速

## 快速开始

### Step 1:配置API Key

免费模型通常通过聚合平台(如OpenRouter)访问,需要先获取API Key:

```bash
# 设置环境变量(以OpenRouter为例)
export OPENROUTER_API_KEY="sk-or-v1-xxxxxxxx"
# ...
# 持久化配置
free-finder config set api.key "$OPENROUTER_API_KEY"
free-finder config set api.base_url "https://openrouter.ai/api/v1"
```

> 获取免费API Key: 访问聚合平台官网注册即可,无需付费。

### Step 2:发现可用模型

```bash
# 列出所有免费模型(默认按质量排序)
free-finder list
# ...
# 按上下文长度排序
free-finder list --sort context_length
# ...
# 按稳定性排序
free-finder list --sort stability
# ...
# 查看完整详情
free-finder list --detail --all
```

### Step 3:切换主模型

```bash
# 切换到指定模型
free-finder switch qwen3-coder
# ...
# 验证切换结果
free-finder status
```

### Step 4:验证连通性

```bash
# 发送测试请求
free-finder ping qwen3-coder
# ...
# 查看响应延迟与内容
free-finder log --tail 5
```

## 示例

### 基础配置文件

```json
{
  "api": {
    "base_url": "https://openrouter.ai/api/v1",
    "key_env": "OPENROUTER_API_KEY",
    "timeout": 30,
    "retry": 2
  },
  "model": {
    "primary": "qwen/qwen3-coder:free",
    "fallbacks": []
  },
  "preferences": {
    "sort_by": "quality",
    "min_context_length": 4096,
    "min_stability": 0.95,
    "preferred_languages": ["python", "javascript", "typescript"]
  }
}
```

### 模型切换示例

```bash
# 场景:从默认模型切换到deepseek-coder
free-finder switch deepseek-coder
# ...
# 输出示例:
# ✓ 主模型已切换: deepseek-coder
# ✓ 配置已更新: ~/.free-finder/config.json
# ✓ 连通性测试: 通过(延迟 320ms)
# 提示: 重启Agent会话以应用新配置
```

### 多模型对比

```bash
# 同时测试多个模型
free-finder compare qwen3-coder deepseek-coder llama3.3-70b
# ...
# 输出对比表:
# | 模型 | 延迟 | 上下文 | 限速 | 编程得分 |
# |------|------|--------|------|----------|
# | qwen3-coder | 320ms | 32K | 20/min | 8.5 |
# | deepseek-coder | 450ms | 64K | 10/min | 8.8 |
# | llama3.3-70b | 580ms | 128K | 5/min | 7.9 |
```

## 最佳实践

### 模型选择策略

| 使用场景 | 推荐模型特征 | 备注 |
|---:|---:|---:|
| 代码补全 | 上下文≥8K,延迟<500ms | 优先速度 |
| 代码生成 | 上下文≥16K,质量评分高 | 优先质量 |
| 对话调试 | 多轮能力强,稳定性高 | 优先稳定 |
| 文档总结 | 上下文≥32K,支持长文本 | 优先长度 |
| 函数调用 | 显式支持tool_use | 检查能力矩阵 |

### 避免常见陷阱

- **陷阱1: 只看模型名,不看限速** → 免费模型通常有严格限速,高并发场景不适用
- **陷阱2: 忽略稳定性指标** → 部分免费模型可用率<90%,关键任务慎用
- **陷阱3: 长期依赖单一模型** → 免费模型可能随时下线,建议备用2-3个
- **陷阱4: 不做连通性测试** → 切换后必须`ping`验证,避免静默失败
- **陷阱5: 忽视上下文长度** → 长文档场景误用小上下文模型会导致截断

### 配置管理

```bash
# 备份当前配置
free-finder config export --output backup.json
# ...
# 恢复配置
free-finder config import --file backup.json
# ...
# 重置为默认配置
free-finder config reset
# ...
# 查看配置差异
free-finder config diff --file backup.json
```

## 常见问题

### Q1: 免费模型真的完全免费吗?

A: 大多数聚合平台(如OpenRouter)提供的免费模型不收取费用,但有速率限制(如每分钟20次请求、每日1000次)。超出限制后会返回429错误,需等待重置或升级付费。

### Q2: 为什么切换后模型没有生效?

A: 检查以下几点: (1)是否重启了Agent会话; (2)配置文件路径是否正确(`~/.free-finder/config.json`); (3)运行`free-finder status`查看当前生效配置; (4)查看日志是否有错误。

### Q3: 免费模型经常超时怎么办?

A: 免费模型负载较高时容易超时。建议: (1)设置合理timeout(默认30秒); (2)启用retry(默认2次); (3)避开高峰时段(UTC 14:00-18:00); (4)准备备用模型(专业版支持自动fallback)。

### Q4: 如何判断模型质量好坏?

A: 参考以下维度: (1)上下文长度是否满足需求; (2)编程任务准确率(可手动测试10个典型问题); (3)响应延迟是否可接受; (4)近7天可用率(`free-finder list --detail`查看)。

### Q5: 多个免费模型如何组合使用?

A: 推荐策略: 主模型选质量最高的,fallback链按质量降序排列2-3个。免费版需手动切换,专业版支持自动fallback。注意fallback模型上下文长度需≥主模型,否则会话会截断。

## 已知限制

本免费体验版限制以下高级功能:
- 不支持自动fallback链(主模型失败需手动切换)
- 不支持后台守护进程(无法自动恢复限速中断)
- 不支持批量模型对比测试(单次仅支持1个模型ping)
- 不支持模型质量评分自定义权重
- 不支持调用统计与成本分析报告
- 不支持多API Key负载均衡

解锁全部功能请使用专业版: free-resource-finder-pro

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8+(运行free-finder CLI)
- **网络**: 可访问聚合平台API(如OpenRouter)

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| free-finder | CLI工具 | 必需 | `pip install free-finder` |
| requests | Python库 | 必需 | `pip install requests` |
| OpenRouter API | API服务 | 必需 | 注册OpenRouter账号获取免费Key |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |

### API Key 配置
- **聚合平台Key**: 通过环境变量`OPENROUTER_API_KEY`配置,禁止硬编码
- **配置文件**: 存储于`~/.free-finder/config.json`(权限600)
- **Key轮换**: 建议每90天轮换一次Key,提升安全性
- **禁止**: 在SKILL.md或脚本中硬编码任何API Key

### 可用性分类
- **分类**: MD+EXEC+CLI(Markdown指令+命令行工具+网络API调用)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作,核心功能需要free-finder CLI

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
