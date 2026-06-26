---
name: bic-qa
description: 当用户询问数据库或操作系统相关知识、需要基于 BIC-QA 知识库检索专业资料时使用。调用官方 API 需要有效凭据，详见正文 Setup
homepage: https://www.bic-qa.com
version: 1.0.2
---

## 概述

通过 **BIC-Skills 知识问答 API**（HTTPS）查询 **BIC-QA 知识库**。在具备网络与有效 API Key 的前提下，向服务端发送 HTTP 请求即可。

**Base URL（问答）**：`https://api.bic-qa.com/skills/qa`

## Setup

> **Security note：** 本技能仅向 **BIC-QA 官方 API**（`api.bic-qa.com`）发送凭据，与官网账户体系一致。API Key 仅以 `Authorization: Bearer …` 形式出现在请求头中，不会写入其它域名、本地日志或随技能文件分发。

### 1. 注册并获取 API Key

按顺序完成（界面以官网实际为准）：

1. 打开 **BIC-QA 官网**：https://www.bic-qa.com  
2. **注册**账号（按页面提示填写邮箱/手机等并完成验证，若已有账号则直接登录）。  
3. 登录后进入 **用户中心 / 控制台 / API 管理** 等页面（具体名称以官网为准），找到 **API Key** 或 **访问令牌** 入口。  
4. **创建或查看** API Key，复制并妥善保存（仅自己可见，勿提交到公开仓库）。

官网提供免费 API Key；若页面有「重置 / 轮换」功能，更新后需同步修改本地或环境变量中的配置。

### 2. 存储 API Key（二选一）

集成层或 Agent 在发请求前需能读到 Key，并组装为 **`Authorization: Bearer <你的_API_Key>`**。

**方式 A — 配置文件（推荐）：**

```bash
mkdir -p ~/.bic/config
chmod 700 ~/.bic/config
echo "your_api_key_here" > ~/.bic/config/api_key
chmod 600 ~/.bic/config/api_key
```

**方式 B — 环境变量：**

```bash
export BIC_API_KEY="your_api_key_here"
```

Agent 会按优先级依次尝试：环境变量 → 配置文件。

## 凭证预检

每次调用 API 前，先确认 API Key 可用。若为空，停止调用并提示用户按 **Setup** 完成注册与配置。

```bash
# Load user-provisioned BIC-QA API key (used ONLY for api.bic-qa.com authentication)
BIC_QA_KEY="${BIC_API_KEY:-$(cat ~/.bic/config/api_key 2>/dev/null)}"
if [ -z "$BIC_QA_KEY" ]; then
  echo "缺少 BIC-QA API Key，请先在 https://www.bic-qa.com 注册获取，并按 Setup 配置 BIC_API_KEY 或 ~/.bic/config/api_key"
  exit 1
fi
```

## API 调用模板

问答接口为 **HTTP POST + JSON Body**，仅发往 **`https://api.bic-qa.com/skills/qa`**。

```bash
# All requests go ONLY to the official BIC-QA API (api.bic-qa.com)
# 将 QUESTION、DBTYPE 替换为实际值；question 中含引号时需自行转义或使用 jq/python 构造 JSON body
curl -s -X POST "https://api.bic-qa.com/skills/qa" \
  -H "Authorization: Bearer ${BIC_QA_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"question":"QUESTION","dbtype":"DBTYPE"}'
```

含特殊字符时建议用 `jq -n --arg q "..." --arg t "..." '{question:$q,dbtype:$t}'` 生成 body，再传给 `curl -d @-`。

| 字段       | 必填 | 说明 |
| ---------- | ---- | ---- |
| `question` | 是   | 用户的问题文本 |
| `dbtype`   | 是   | 数据库或主题类型（见下表） |

**成功响应**：JSON，通常含 `result` 字段。**请仅基于 `result` 与用户问题组织回答**，并遵守其中关于版本、措辞与结构的说明。

## 支持的数据库类型（`dbtype`）

`dbtype` 须为服务端支持的标识之一：

### 关系型数据库
- **Oracle** - Oracle 数据库
- **MySQL** - MySQL 数据库
- **GreatSQL** - GreatSQL 数据库
- **PostgreSQL** - PostgreSQL 数据库, 简写: pg
- **SQL Server** - Microsoft SQL Server
- **DB2** - IBM DB2 数据库
- **DM（达梦）** - 达梦数据库
- **KingBase（人大金仓）** - 人大金仓数据库, 简写: kb, kbase
- **OceanBase** - OceanBase 数据库
- **GoldenDB** - GoldenDB 数据库
- **GaussDB** - 华为 GaussDB 数据库
- **openGauss** - openGauss 数据库
- **TDSQL** - 腾讯 TDSQL 数据库
- **TiDB** - PingCAP TiDB 数据库
- **GBase** - 南大通用 GBase 数据库
- **GBase 8a** - 南大通用 GBase 8a 数据库
- **GBase Distributed** - 南大通用分布式数据库
- **Oscar** - 神舟通用 Oscar 数据库
- **YashanDB** - 崖山数据库
- **PanWeiDB** - 盘古数据库
- **XuGu** - 虚谷数据库
- **HashData** - HashData 数据库

### NoSQL 数据库

- **Redis** - Redis 缓存数据库
- **Redis Cluster** - Redis 集群
- **MongoDB** - MongoDB 文档数据库

### 操作系统

- **OS** - 操作系统相关问题（Linux、Windows 等）

若无法从用户问题判断类型，先请用户补充后再调用。

## 错误与未授权时的行为

- **401** 或缺少/无效 `Authorization`：不要用模型自身知识编造技术细节；用与用户一致的语言说明需前往 https://www.bic-qa.com 获取或更新 API Key，并在请求头使用 `Bearer` 方式携带。  
- **400**（如不支持的 `dbtype`）：根据服务端错误信息提示用户修正类型或补充信息。  
- **5xx** 或其它错误：如实说明调用失败，可建议稍后重试，**不要**用训练数据顶替知识库答案。

## 工作流程建议

1. 理解用户问题并确定 `dbtype`（不确定则先追问）。  
2. 使用已配置的 API Key 调用 `POST https://api.bic-qa.com/skills/qa`。  
3. 解析响应中的 `result`，严格基于知识库内容作答。

## 相关资源

- 官网：https://www.bic-qa.com  
- 技术支持：support@dbaiops.com  
- Gitee：https://gitee.com/BIC-QA/BIC-QA  
- GitHub：https://github.com/BIC-QA/BIC-QA  
