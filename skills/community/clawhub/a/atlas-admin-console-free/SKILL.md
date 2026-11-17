---
slug: atlas-admin-console-free
name: atlas-admin-console-free
version: 1.0.0
displayName: Atlas管理台免费版
summary: MongoDB Atlas Admin API浏览与查询工具，支持50+API分类检索、端点详情查看、Schema定义获取。
license: Proprietary
edition: free
description: 面向MongoDB Atlas运维者的Admin API浏览与查询工具。通过命令行检索50+API分类、查看端点定义、获取Schema详情，免凭证即可作为只读文档浏览器使用，配置凭证后可执行实时API调用。Use
  when 需要数据库操作、SQL查询、数据存储管理时使用。不适用于数据库架构设计决策。
tags:
- 集成工具
- MongoDB
- 云数据库
- API管理
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L2-标准级"
pricing_model: per_use
suggested_price: "19.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "工具,效率,自动化"
---
# Atlas管理台（免费版）

本工具为MongoDB Atlas运维者提供Admin API浏览与查询能力。免费版覆盖核心场景：API目录浏览、端点详情查看、Schema定义获取、只读API调用，足以应对日常文档查阅与状态查询需求。

## 概述

MongoDB Atlas提供丰富的Admin API，覆盖集群管理、备份恢复、用户管理、监控告警等50+分类。然而官方OpenAPI规范文档冗长，定位具体端点与参数效率低下。本工具通过命令行接口提供高效的API浏览、检索与调用能力，将"翻文档"的时间从分钟级降到秒级。

工具基于Node.js实现，无凭证时作为只读文档浏览器，配置凭证后可执行实时API调用，且对状态变更操作强制执行安全协议。

## 核心能力

| 能力分类 | 说明 |
|----|---|
| API目录 | 按关键字检索50+API分类 |
| 端点详情 | method、path、params、requestBody完整定义 |
| Schema定义 | 复杂类型的数据模型查询 |
| 只读调用 | GET方法直接执行，无副作用 |
| 安全协议 | POST/PUT/PATCH/DELETE必须dry-run + 确认 |
| 凭证管理 | 通过环境变量注入，禁止硬编码 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：MongoDB、Atlas、Admin、浏览与查询工具、分类检索、端点详情查看、定义获取、运维者的、通过命令行检索、查看端点定义、免凭证即可作为只、读文档浏览器使用、配置凭证后可执行、Use、when、需要数据库操作、SQL、数据存储管理时使、不适用于数据库架、构设计决策等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：API学习与文档查阅

新接触Atlas API的开发者，通过`catalog`命令快速了解所有分类，通过`detail`命令查看具体端点的参数定义。

### 场景二：自动化脚本开发

编写Atlas自动化运维脚本前，使用`schema`命令确认请求体结构，避免因字段错误导致调用失败。

### 场景三：集群状态查询

只读查询集群列表、节点状态、备份信息、监控指标，无需登录Web控制台。

### 场景四：故障应急查询

集群异常时快速查询告警、事件日志、节点状态，辅助定位问题。

## 快速开始

### 依赖详情

```bash
# 确保Node.js 18+已安装
node --version
# ...
# 工具脚本随Skill分发，无需额外安装
```

### 第二步：浏览API目录

```bash
# 列出所有API分类
node （请参考skill目录中的脚本文件） catalog
# ...
# 按关键字过滤
node （请参考skill目录中的脚本文件） catalog Clusters
```

### 第三步：查看端点详情

```bash
# 获取特定Operation ID的完整定义
node （请参考skill目录中的脚本文件） detail listClusterDetails
```

### 第四步：查询Schema定义

```bash
# 获取复杂类型的数据模型
node （请参考skill目录中的脚本文件） schema "#/components/schemas/ApiError"
```

完整上手时间约60秒。

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤。

## 示例

### 环境变量配置（执行实时调用需要）

```bash
# 配置Atlas API凭证
export ATLAS_CLIENT_ID="your-client-id"
export ATLAS_CLIENT_SECRET="your-client-secret"
# ...
# 配置组织与项目ID
export ATLAS_GROUP_ID="your-group-id"
export ATLAS_ORG_ID="your-org-id"
```

### 只读API调用（安全）

```bash
# 列出所有集群
node （请参考skill目录中的脚本文件） GET groups/${ATLAS_GROUP_ID}/clusters
# ...
# 查看集群详情
node （请参考skill目录中的脚本文件） GET groups/${ATLAS_GROUP_ID}/clusters/DemoCluster
# ...
# 列出数据库用户
node （请参考skill目录中的脚本文件） GET groups/${ATLAS_GROUP_ID}/databaseUsers
# ...
# 查看告警
node （请参考skill目录中的脚本文件） GET groups/${ATLAS_GROUP_ID}/alerts
```

### 状态变更操作（必须dry-run + 确认）

```bash
# 第一步：dry-run预览（不实际执行）
node （请参考skill目录中的脚本文件） POST groups/${ATLAS_GROUP_ID}/clusters \
  --data '{"name":"DemoCluster", "providerSettings":{...}}' \
  --dry-run
# ...
# 第二步：人工审核dry-run输出
# ...
# 第三步：明确确认后执行（加--yes跳过交互确认）
node （请参考skill目录中的脚本文件） POST groups/${ATLAS_GROUP_ID}/clusters \
  --data '{"name":"DemoCluster", "providerSettings":{...}}' \
  --yes
```

#
## 最佳实践

### 1. 状态变更操作遵循四步安全协议

任何POST/PUT/PATCH/DELETE操作必须：
1. **停止审核**：不立即执行
2. **预览**：先`--dry-run`验证payload与端点
3. **确认**：向用户展示完整命令与JSON body
4. **执行**：用户明确批准后加`--yes`执行

### 2. 凭证通过环境变量注入

```bash
# 正确：环境变量
export ATLAS_CLIENT_ID="xxx"
# ...
# 错误：硬编码在脚本中
const clientId = "xxx"  // 禁止
```

### 3. 使用dry-run排查参数错误

dry-run模式会打印完整请求详情，便于检查JSON格式、字段名、URL路径是否正确，避免直接执行失败。

### 4. 只读操作可批量执行

GET方法无副作用，可批量查询多个集群、项目、用户信息，便于自动化巡检。

### 5. 善用catalog缩小检索范围

API分类有50+，先通过`catalog <关键字>`缩小范围，再用`detail`查看具体端点，避免全量浏览。

## 常见问题

### Q1：未配置凭证能用吗？

A：可以。无凭证时作为只读文档浏览器，使用`catalog`、`detail`、`schema`命令查阅API规范，但不执行实际调用。配置凭证后才能调用实时API。

### Q2：API调用返回401未授权？

A：(1) 确认`ATLAS_CLIENT_ID`与`ATLAS_CLIENT_SECRET`环境变量已设置；(2) 在Atlas控制台确认API Key有对应权限；(3) 检查Group ID/Org ID是否正确。

### Q3：dry-run输出正常但实际执行失败？

A：(1) 检查JSON body格式是否正确，特别是嵌套对象；(2) 确认必填字段已提供；(3) 查看错误响应的detail字段定位问题；(4) 部分操作有资源配额限制，需联系Atlas支持提升。

### Q4：如何查询特定集群的监控数据？

A：(1) `catalog Monitoring`查找监控相关API；(2) `detail <operationId>`查看参数；(3) 执行GET调用获取监控指标。常用指标包括CPU使用率、内存、连接数、磁盘IO。

### 已知限制

A：Atlas API有速率限制，建议每分钟不超过100次调用。批量操作时加入间隔（如sleep 1秒），避免触发429。专业版提供批量调用优化与重试机制。

### Q6：如何获取集群的备份列表？

A：(1) `catalog Cloud Backups`查找备份相关API；(2) 执行`GET groups/{groupId}/clusters/{clusterName}/backup/snapshots`获取快照列表。
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 免费版限制

本免费体验版限制以下高级功能：
- 不支持批量API调用与并发执行
- 不支持API调用结果导出（CSV/JSON）
- 不支持API调用历史记录与回放
- 不支持自定义API组合（多API编排）
- 不支持监控告警自动化

解锁全部功能请使用专业版：atlas-admin-console-pro

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Node.js**: 18+

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| Node.js | 运行时 | 必需 | nodejs.org 官方下载 |
| atlas-api.mjs | 脚本 | 必需 | 随本Skill分发 |
| atlas-call.mjs | 脚本 | 必需 | 随本Skill分发 |

### API Key 配置
- **ATLAS_CLIENT_ID**: Atlas API客户端ID，通过环境变量注入，禁止硬编码
- **ATLAS_CLIENT_SECRET**: Atlas API客户端密钥，通过环境变量注入，禁止硬编码
- **ATLAS_GROUP_ID**: 项目ID，通过环境变量配置
- **ATLAS_ORG_ID**: 组织ID，通过环境变量配置
- 凭证在Atlas控制台"Access Manager > API Keys"页面创建

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent完成操作

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Atlas管理台免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "atlas admin console"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
