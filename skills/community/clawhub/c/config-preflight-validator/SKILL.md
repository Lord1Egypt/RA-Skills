---
name: config-preflight-validator
description: OpenClaw 配置预校验工具。在执行 config.patch 或修改 openclaw.json 前进行本地 Schema 验证，提供具体的错误字段描述。
version: 1.0.0
author: DeepEye
tags: [config, validation, schema, production, safety]
---

# 🔍 Config Preflight Validator

解决 "Validation issues" 错误信息模糊的问题，在调用网关 API 前给出具体错误字段描述。

## 🎯 功能特性

- **Schema 同步**：自动从 `gateway config.schema` 获取最新规范。
- **本地校验**：在提交修改前，基于 JSON Schema 验证数据结构。
- **特定规则检查**：针对 `plugins.allow` 等列表格式、`channels` 对象格式进行硬编码校验。

## 🚀 使用方法

### 校验补丁
```bash
python3 ~/.openclaw/workspace/.lib/config-preflight-validator.py --patch '{"plugins": {"allow": ["new-plugin"]}}'
```

### 校验完整文件
```bash
python3 ~/.openclaw/workspace/.lib/config-preflight-validator.py --file ~/.openclaw/openclaw.json
```

### 更新 Schema 缓存
```bash
python3 ~/.openclaw/workspace/.lib/config-preflight-validator.py --update-schema
```

## 🛠️ 安装要求

- Python 3.9+
- 推荐安装 `jsonschema` (pip install jsonschema)
