---
name: gaode-c3-us-shop
version: 0.2.0
description: POI 详情页问题排查编排器。自动执行 6 步排查流程：查代码 (sourceId)→查日志→复现请求→解析返回→阅读代码→定位问题。当用户提供 gsid/traceId 排查 POI 详情页问题时触发。触发词：POI 排查、poi 问题、详情页异常、gsid 排查、traceId 分析、poi 调试、contentPerson、手艺人模块。
---

# POI Debug Orchestrator — POI 详情页问题排查编排器

面向 `lse2-us-business-service` 应用的 POI 详情页问题全链路排查工具。自动协调 Loghouse、curl、代码查询等多个技能，输出结构化排查报告。

## 执行流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Step 0     │ →  │  Step 1     │ →  │  Step 2     │ →  │  Step 3     │ →  │  Step 4     │ →  │  Step 5     │
│  查代码     │    │  查日志     │    │  复现请求    │    │  解析返回    │    │  阅读代码    │    │  排查问题    │
│  (sourceId) │    │  (loghouse) │    │  (curl)     │    │  (jq/python)│    │  (code MCP) │    │  (分析总结)  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### 流程说明

| 步骤 | 目标 | 工具 | 输出 |
|------|------|------|------|
| **Step 0** | 确定模块的 `sourceId` | `code::search_code` | sourceId, 配置文件，数据路径 |
| **Step 1** | 查询包含 sourceId 的日志 | `loghouse-mcp::query_log` | 完整 URL, bffServiceParams, traceId |
| **Step 2** | 复现请求 | `curl` | 响应 JSON |
| **Step 3** | 解析响应数据 | `python3 + jq` | 字段比对，异常检测 |
| **Step 4** | 定位相关代码 | `code::get_single_file` | 源码文件，字段定义 |
| **Step 5** | 生成排查报告 | 内置分析 | 根因分析，修复建议 |

## 输入参数

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `gsid` | ✅ | 用户会话 ID | `31033080013090177494736367500059940538728` |
| `poiid` | ✅ | POI ID | `B0LR4UPN4M` |
| `module` | ❌ | 模块名或 sourceId (默认自动检测) | `contentPerson` |
| `app` | ❌ | 应用名（默认 `lse2-us-business-service`） | `lse2-us-business-service` |
| `env` | ❌ | 环境（`gray`/`online`，默认 `gray`） | `gray` |
| `timeRange` | ❌ | 日志查询时间范围（默认 `1h ago`） | `30m ago` |
| `interface` | ❌ | 接口路径（默认 `/search_business/process/middleLayer/poiDetail`） | `/search_business/process/middleLayer/poiDetail` |
| `pageIndex` | ❌ | 分页索引（默认 `2`） | `2` |

## 子技能依赖

| 步骤 | 技能/工具 | 用途 |
|------|----------|------|
| 0 | `code::search_code` | 搜索模块对应的 sourceId |
| 1 | `loghouse-mcp::query_log` | 查询包含 gsid + sourceId 的请求日志 |
| 2 | `curl` | 使用日志中的 URL 复现请求 |
| 3 | `python3 + jq` | 解析 JSON 响应，提取关键字段 |
| 4 | `code::get_single_file` / `code::search_classes` | 读取相关源码类 |
| 5 | (内置分析逻辑) | 比对预期与实际，输出根因建议 |

## 输出格式

结构化排查报告：

```markdown
## 📋 POI 问题排查报告

**GSID**: xxx | **POIID**: xxx | **时间**: xxx

### [1/5] ✅ 日志查询
- 找到 X 条匹配日志
- TraceID: xxx
- 请求耗时：xx ms

### [2/5] ✅ 请求复现
- 请求 URL: http://xxx/xxx
- 响应大小：xx KB
- 状态码：200

### [3/5] ✅ 响应解析
| 字段 | 预期值 | 实际值 | 状态 |
|------|--------|--------|------|
| shopSettlement.state | 付费 | 未入驻 | ❌ 异常 |

### [4/5] ✅ 代码定位
- 相关类：`ShopSettlementDTO.java`
- 关键字段定义位置：L347

### [5/5] 🔍 根因分析
**问题**: shopSettlement 数据未返回
**可能原因**:
1. 商家未入驻（state=未入驻）
2. shopId 为空导致 DTO 未构建
3. 上游接口未透传

**建议**:
- 检查商家入驻状态
- 查看 shopId 生成逻辑
```

## 使用示例

### 基础用法
```bash
# 用户提供 gsid 和 poiid
"帮我排查这个 POI 问题：gsid=31033080013090177494736367500059940538728, poiid=B0LR4UPN4M"
```

### 指定模块名
```bash
# 排查手艺人模块
"帮我排查 POI B0LR4UPN4M 的手艺人模块，gsid=xxx, module=contentPerson"
```

### 指定环境
```bash
"查一下线上环境的 POI 问题，gsid=xxx, poiid=xxx, env=online"
```

### 指定时间范围
```bash
"排查 2 小时内的日志，gsid=xxx, poiid=xxx, timeRange=2h ago"
```

## 执行步骤详解

### Step 0: 查代码 (确定 sourceId)

**目标**: 确定目标模块对应的 `sourceId`

**流程**:
1. 如果用户已提供 `module` 参数（如 `contentPerson`），先在 `references/source_id_map.md` 中查找映射
2. 如果未找到，搜索代码库确认 sourceId

**命令**:
```bash
# 方法 1: 查映射表
grep "contentPerson" references/source_id_map.md

# 方法 2: 搜索代码库
aone-kit call-tool code::search_code '{
  "search": "contentPerson",
  "repo": "gaode.search/us-business-service",
  "pageSize": 10
}'
```

**输出**:
- `sourceId`: 模块的唯一标识 (如 `contentPerson`)
- `dataPath`: 数据在响应中的路径 (如 `data.contentPerson.data.personInfos`)
- `description`: 模块用途说明

**常用模块映射**:
| 模块名 | sourceId | 说明 |
|--------|----------|------|
| 手艺人 | `contentPerson` | 手艺人/匠人列表 |
| 案例集 | `contentCaseBook` | 服务案例 |
| 店铺基础 | `shopBaseInfo` | 商家信息 |
| 入驻信息 | `shopSettlement` | 入驻状态 |
| 广告分发 | `adResourceDistribute` | 广告资源 |

---

### Step 1: 查日志

**目标**: 找到包含 gsid 和 sourceId 的 `/search_business/process/middleLayer/poiDetail` 接口日志

**命令**:
```bash
aone-kit call-tool loghouse-mcp::query_log '{
  "app_name": "lse2-us-business-service",
  "log_name": "nginx_uni",
  "query": "<gsid> AND pageIndex=<pageIndex> AND \"<sourceId>\" AND /search_business/process/middleLayer/poiDetail",
  "start_time": "<timeRange>",
  "end_time": "now",
  "size": 10,
  "reverse": true,
  "emp_id": "501280"
}'
```

**关键改进**: 使用 `sourceId` 精准过滤日志，避免查询无关请求

**输出提取**:
- `url` 字段 → 用于 Step 2 复现
- `traceId` 字段 → 用于关联追踪
- `bffServiceParams` → 验证是否包含目标 sourceId
- `upstream_response_time` → 耗时分析

### Step 2: 复现请求

**目标**: 使用日志中的完整 URL 重新发起请求

**命令**:
```bash
# 从日志 URL 中提取完整请求（替换 IP 为域名）
URL=$(echo "$LOG_URL" | sed 's|http://[0-9.]*|http://gray-us-business.amap.com|')
curl -s "$URL" -o /tmp/poi_response.json
```

**注意**:
- 内网 IP 需替换为 `gray-us-business.amap.com` 或 `us-business.amap.com`
- 保留所有 query 参数

### Step 3: 解析返回

**目标**: 提取关键字段，与预期值比对

**命令**:
```bash
python3 << 'EOF'
import json

with open('/tmp/poi_response.json') as f:
    data = json.load(f)

# 提取关键字段
fields = {
    'shopSettlement': data.get('data', {}).get('middleLayerStrategy', {}).get('shopSettlement'),
    'baseInfo': data.get('data', {}).get('middleLayerStrategy', {}).get('baseInfo'),
    'shopBaseInfo': data.get('data', {}).get('middleLayerStrategy', {}).get('shopBaseInfo'),
}

# 检查异常
issues = []
if not fields['shopSettlement']:
    issues.append('shopSettlement 为空')
if fields['shopSettlement'] and not fields['shopSettlement'].get('shopId'):
    issues.append('shopId 为空')

print(json.dumps({'fields': fields, 'issues': issues}, ensure_ascii=False, indent=2))
EOF
```

### Step 4: 阅读代码

**目标**: 定位相关代码，理解字段生成逻辑

**命令**:
```bash
# 搜索相关类
aone-kit call-tool code::search_classes '{
  "search": "ShopSettlementDTO",
  "repo": "gaode.search/us-business-service"
}'

# 获取完整文件
aone-kit call-tool code::get_single_file '{
  "repo": "gaode.search/us-business-service",
  "ref": "master",
  "filePath": "us-platform/src/main/java/com/amap/us/platform/node/model/shop/ShopSettlementDTO.java"
}'
```

**分析重点**:
- 字段定义（如 `settlementRightInfo.state`）
- 字段生成逻辑（哪个 Service/Manager 填充）
- 空值条件（什么情况下返回 null）

### Step 5: 排查问题

**目标**: 综合以上信息，输出根因分析

**分析框架**:

```
1. 数据层问题？
   - 数据库/缓存中是否有数据
   - 数据是否正确

2. 逻辑层问题？
   - 条件判断导致未返回
   - 空指针/异常被吞

3. 配置层问题？
   - Diamond 配置影响
   - AB 实验开关

4. 链路层问题？
   - 上游未透传
   - 下游超时
```

## 常见问题模式

| 现象 | 可能原因 | 排查方向 |
|------|----------|----------|
| shopSettlement 为空 | 商家未入驻 | 查 `settlementRightInfo.state` |
| shopId 为空 | POI 未关联商家 | 查 POI-Shop 绑定关系 |
| 部分字段缺失 | 版本差异/AB 实验 | 查 `testid` 和 AB 配置 |
| 整个接口 500 | 服务异常 | 查日志异常堆栈 |
| 响应慢 (>1s) | 下游超时 | 查各模块耗时 |

## 扩展能力

### 支持更多接口

修改 `interface` 参数即可适配其他接口：
- `/search_business/process/middleLayer/shopBaseInfo`
- `/search_business/process/middleLayer/shopSettlement`
- `/search_business/process/middleLayer/user`

### 支持更多应用

修改 `app` 参数：
- `lse2-us-business-service` (主应用)
- `us-business-service` (老应用)

### 添加自动修复建议

根据问题类型输出修复建议：
```
【修复建议】
1. 如果是数据缺失 → 联系 DBA 补数据
2. 如果是逻辑问题 → 提 CR 修复代码
3. 如果是配置问题 → 修改 Diamond 配置
```

## 相关文件

- [`scripts/poi-debug.sh`](scripts/poi-debug.sh) — 执行脚本
- [`references/fields.md`](references/fields.md) — 关键字段说明
- [`references/faq.md`](references/faq.md) — 常见问题 FAQ

## 注意事项

1. **内网限制**: Loghouse 和 gray 环境仅限内网访问
2. **认证要求**: 使用前确保 `sf auth login` 和 Aone MCP 已授权
3. **日志延迟**: Loghouse 日志有 1-2 分钟延迟
4. **环境差异**: gray 和 online 环境数据可能不一致

---

_版本：0.1.0 | 作者：土曜 | 最后更新：2026-03-31_
