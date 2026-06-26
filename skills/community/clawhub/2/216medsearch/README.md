# 216medsearch 技能

## 概述

这是一个用于查询药品通用名的技能，通过内部 API 进行药品信息查询。

## 快速开始

```bash
# 查询药品通用名
~/.openclaw/workspace/skills/216medsearch/tool.sh 环吡酮搽剂
```

## 配置

- **API URL**: `http://10.1.23.216:8280/rest/schema/med/query`
- **API Token**: 已内置在脚本中
- **查询方式**: 模糊查询（通过 `name##` 条件）

## 使用场景

- 用户询问某个药品的通用名时
- 需要确认药品名称的正确性时
- 查询药品基本信息时

## 技术细节

- 使用 `curl` 调用 REST API
- 查询条件：`name##'药品名称'` 表示模糊查询
- 查询字段：`name` 字段
- 返回格式：JSON

## 测试

```bash
# 测试查询
~/.openclaw/workspace/skills/216medsearch/tool.sh 环吡酮搽剂

# 预期返回 JSON 格式的药品信息
```

## 维护

- 定期更新 API token（如过期）
- 确保 API 服务可用
- 测试不同药品名称的查询效果
