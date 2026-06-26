---
name: fx-base
description: feima-lab 后端公共基础模块：API 认证校验（FX_AI_API_KEY）、请求封装（POST + Bearer Token）、 通用错误处理（missing_api_key / api_unavailable / api_error）。 这是基础依赖 skill，被其他领域 skill（如 fanli）的脚本通过 source 引用，不直接面向用户使用。 当你看到领域 skill 的 CRITICAL 声明要求读取本文件时触发。
version: 1.1.2
allowed-tools: Bash({baseDir}/scripts/*),Read({baseDir}/**)
metadata:
  openclaw:
    requires:
      env:
        - FX_AI_API_KEY
    primaryEnv: FX_AI_API_KEY
---

# fx-base — feima-lab 公共基础

本 skill 是 feima-lab 后端 API 的公共基础模块。**不直接面向用户调用**，而是被领域 skill 的脚本通过 `import` 引用。

## 提供的函数

领域 skill 的脚本通过 `import { fxCheckAuth, fxPost, fxCheckResponse, FX_BASE_URL } from './fx-api.mjs'` 获得以下函数：

| 函数 | 说明 |
|------|------|
| `fxCheckAuth()` | 校验环境变量 `FX_AI_API_KEY`，未设置时输出标准错误 JSON 并 exit 1 |
| `fxPost(endpoint, body, errMsg?)` | 发送 POST 请求到 `FX_BASE_URL/<endpoint>`，自动拼接认证头。失败时 exit 1 |
| `fxCheckResponse(respJson)` | 校验响应 JSON：`code==200` 返回 `data`，否则输出错误并 exit 1 |

常量：`FX_BASE_URL=https://api-ai-brain.fenxianglife.com/fenxiang-ai-brain`

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `FX_AI_API_KEY` | 是 | 从 [feima-lab 开放平台](https://platform.feima.ai/) 登录获取 |

## 安装

```bash
# ClawHub（推荐）
npx skills install fangshan101-coder/fx-base

# npm
npx skills install fx-base
```

安装后确保 fx-base 与依赖它的领域 skill 在同一个 `.claude/skills/` 目录下（即同级目录）。

## 领域 skill 如何引用

在领域 skill 的脚本头部添加：

```js
import { fileURLToPath } from 'url';
import { join, dirname } from 'path';
import { existsSync } from 'fs';

const _scriptDir = dirname(fileURLToPath(import.meta.url));
const _fxApiPath = join(_scriptDir, '../../fx-base/scripts/fx-api.mjs');
if (!existsSync(_fxApiPath)) {
  process.stderr.write(
    '{"status":"error","error_type":"missing_dependency","suggestion":"缺少 fx-base，请安装：npx skills install fangshan101-coder/fx-base"}\n'
  );
  process.exit(1);
}

const { fxCheckAuth, fxPost, fxCheckResponse } = await import(_fxApiPath);
```

然后即可使用 `fxCheckAuth()`、`fxPost()`、`fxCheckResponse()`。

## 错误输出格式

所有错误统一为 JSON 到 stderr：

```json
{"status":"error","error_type":"<类型>","suggestion":"<用户可见提示>"}
```

| error_type | 触发条件 |
|------------|---------|
| `missing_api_key` | `FX_AI_API_KEY` 环境变量未设置 |
| `api_unavailable` | curl 请求失败（超时、网络错误、HTTP 错误） |
| `api_error` | 响应 `code != 200`，从 `errorMessage` 字段提取具体原因 |
| `missing_dependency` | 领域 skill 找不到 fx-base（未安装） |

## 数据流向

用户提供的数据会被发送到 `https://api-ai-brain.fenxianglife.com` 进行处理，请确保信任该服务后再使用。
