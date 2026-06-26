---
name: baidu-qianfan-search
description: |
  Comprehensive search API integration for Baidu Qianfan Web Search. 
  Use when Claude needs to perform web searches using Baidu Qianfan's enterprise search API.
  Use cases include: General web search with Chinese language support, Time-filtered search (last 7 days, month, year), Site-specific or site-blocked search, Multi-resource type search (web, images, videos), Safe search filtering, Advanced search with custom parameters.
  This is Baidu Qianfan Search API, not the regular Baidu web search - requires separate API key registration.
---

# 百度千帆搜索技能 (Baidu Qianfan Search)

**重要提示：这是百度千帆搜索API，不是普通的百度网页搜索。** 百度千帆搜索是百度智能云千帆平台的企业级搜索API，需要单独申请API Key。

## 前置要求

### 1. API Key配置（首次使用前必须配置）
首次使用前必须配置你的百度千帆API Key，方式如下：

#### 方式1：环境变量（推荐）
```bash
export BAIDU_QIANFAN_API_KEY="你的百度千帆API Key"
```

#### 方式2：配置文件
在技能目录创建 `.env` 文件：
```
BAIDU_QIANFAN_API_KEY=你的百度千帆API Key
```

### 2. 如何获取API Key
1. 访问 https://cloud.baidu.com/
2. 登录后进入千帆平台
3. 创建应用并获取AppBuilder API Key（格式：`bce-v3/ALTAK-xxxxx`）

## 快速开始

### 基础搜索
```bash
node {baseDir}/scripts/search.mjs "搜索关键词"
```

### 指定结果数量
```bash
node {baseDir}/scripts/search.mjs "搜索关键词" -n 10
```

### 时间范围搜索
```bash
# 最近7天
node {baseDir}/scripts/search.mjs "搜索关键词" --time week

# 最近30天
node {baseDir}/scripts/search.mjs "搜索关键词" --time month

# 过去48小时
node {baseDir}/scripts/search.mjs "搜索关键词" --from "now-2d/d" --to "now/d"
```

## 完整参数说明

### 核心参数
| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `query` | 无（位置参数） | 搜索关键词，建议36个汉字以内 | 必填 |
| `--count` | `-n` | 返回结果数量 | 网页默认20，最大50 |
| `--edition` | 无 | 搜索版本：`standard`（完整）或 `lite`（轻量） | `standard` |

### 时间过滤参数
| 参数 | 说明 |
|------|------|
| `--time` | 快速时效过滤：`week`/`month`/`semiyear`/`year` |
| `--from` | 起始时间：固定日期`YYYY-MM-DD`或相对时间（见下方） |
| `--to` | 结束时间：格式同上 |

#### 相对时间表达式
- `now/d` - 当天
- `now-1w/d` - 最近一周
- `now-2d/d` - 最近两天
- `now-1M/d` - 最近一个月
- `now-3M/d` - 最近三个月
- `now-6M/d` - 最近六个月
- `now-1y/d` - 最近一年

### 站点过滤参数
| 参数 | 说明 |
|------|------|
| `--site` | 指定搜索站点（可重复使用） |
| `--block` | 屏蔽搜索站点（可重复使用） |

### 资源类型参数
| 参数 | 说明 |
|------|------|
| `--types` | 资源类型：`web`/`image`/`video`/`aladdin`，逗号分隔<br>可带数量：`web:10,image:5` |

### 其他参数
| 参数 | 说明 |
|------|------|
| `--safe` | 开启安全搜索 |
| `--config` | query干预配置ID（高级） |
| `--raw` | 输出原始JSON响应 |

## 使用示例

### 1. 基础网页搜索
```bash
node {baseDir}/scripts/search.mjs "北京有哪些旅游景区"
```

### 2. 限定站点搜索
```bash
node {baseDir}/scripts/search.mjs "北京天气" --site "www.weather.com.cn"
# 多个站点
node {baseDir}/scripts/search.mjs "北京天气" --site "site1.com" --site "site2.com"
```

### 3. 时间范围搜索
```bash
# 最近7天
node {baseDir}/scripts/search.mjs "人工智能最新进展" --time week

# 固定日期范围
node {baseDir}/scripts/search.mjs "历史事件" --from "2025-01-01" --to "2025-12-31"
```

### 4. 多资源类型搜索
```bash
# 网页+图片+视频
node {baseDir}/scripts/search.mjs "北京故宫" --types web,image,video

# 仅图片
node {baseDir}/scripts/search.mjs "北京故宫" --types image

# 自定义各类型数量
node {baseDir}/scripts/search.mjs "北京故宫" --types web:10,image:5,video:3
```

### 5. 屏蔽特定站点
```bash
node {baseDir}/scripts/search.mjs "Python教程" --block "csdn.net" --block "jianshu.com"
```

### 6. 安全搜索
```bash
node {baseDir}/scripts/search.mjs "敏感内容" --safe
```

## 输出格式

默认输出格式：
```
#1 网页标题
站点: 站点名称
链接: https://example.com
时间: 2025-01-01 12:00:00
摘要: 搜索摘要...
---
```

使用 `--raw` 参数输出完整JSON响应。

## 技能结构

### 核心文件
- `scripts/search.mjs` - 主搜索脚本，处理所有参数和API调用
- `references/api-reference.md` - 完整的API参数说明和参考文档

### 依赖文件
- `package.json` - Node.js依赖配置
- `.env` - API Key配置文件（用户创建）
- `.gitignore` - 忽略敏感文件和依赖

## 故障排除

### Q: 提示401认证失败？
A: 检查API Key是否正确，确认账号已开通百度千帆搜索API服务。

### Q: 提示429请求超限？
A: 降低请求频率，或联系百度智能云升级配额。

### Q: 提示400参数错误？
A: 检查参数格式，特别是时间格式和站点URL格式。

### Q: 没有搜索结果？
A: 检查关键词是否过长（超过72字符），或尝试放宽时间/站点过滤条件。

## 详细API文档
完整API参数说明、错误码和高级用法请参阅 [references/api-reference.md](references/api-reference.md)。

## 注意事项
1. **无硬编码API Key** - 技能不包含任何硬编码的API Key，用户必须配置自己的Key
2. **区分明确** - 这是百度千帆搜索API，不是普通百度搜索
3. **参数完整** - 支持百度千帆搜索API的所有参数
4. **社区规范** - 符合OpenClaw技能社区规范，可被其他agent直接使用
