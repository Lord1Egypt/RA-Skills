---
name: 1688-ranking
Version: 1.0.1
description: >-
 1688榜单SKILL：查询1688商品榜单列表和热搜词。
 支持按类目ID查询综合榜/热卖榜/好价榜，以及获取类目维度的热搜关键词。
 使用1688开放平台官方API，统一鉴权，Token全局缓存共享。
metadata:
 openclaw:
 primaryEnv: ALI1688_APP_KEY, ALI1688_APP_SECRET, ALI1688_REFRESH_TOKEN
 requires:
 env:
 - ALI1688_APP_KEY
 - ALI1688_APP_SECRET
 - ALI1688_REFRESH_TOKEN
---

# 1688榜单SKILL

通过1688开放平台官方API查询商品榜单和热搜词。

## 鉴权说明

每个 Skill 内置独立的鉴权模块（`scripts/auth.py`），**不依赖任何外部 Skill**。

所有 1688 Skill 的 Token 缓存指向同一个固定路径，实现"独立运行 + 鉴权只发生一次"。

- Token 缓存路径: `skills/.1688_token_cache.json`（所有 1688 Skill 共用）
- 任意一个 Skill 首次请求完成鉴权后，其他 Skill 直接复用缓存
- Token 过期前自动用 refresh_token 刷新
- 支持 `ALI1688_REFRESH_TOKEN`（自动刷新）和 `ALI1688_ACCESS_TOKEN`（直接使用）两种模式

### 配置

在 OpenClaw config 中设置环境变量：

```json5
{
 skills: {
 entries: {
 "1688-ranking": {
 env: {
 ALI1688_APP_KEY: "your_app_key",
 ALI1688_APP_SECRET: "your_app_secret", 
 ALI1688_REFRESH_TOKEN: "your_refresh_token"
 }
 }
 }
 }
}
```

### 如何获取 AppKey / AppSecret / Token

如果遇到 Token 相关错误（如 401、签名失败、Token 过期），按以下步骤操作：

#### Step 1：注册开发者 & 创建应用 → 获取 AppKey + AppSecret

1. 打开 [1688开放平台](https://open.1688.com)，用1688账号登录
2. 进入 [控制中心](https://open.1688.com/console)
3. 点击「我的应用」→「创建应用」
4. 填写应用信息，提交审核
5. 审核通过后，在应用详情页可以看到 **AppKey** 和 **AppSecret**

#### Step 2：订购解决方案 → 获取 API 调用权限

1. 打开 [跨境ERP/独立站SaaS数字化解决方案](https://open.1688.com/solution/solutionDetail.htm?solutionKey=1697015308755)
2. 点击「立即订购」，将解决方案绑定到你的应用
3. 订购成功后，应用才有权限调用方案内的 API

#### Step 3：用户授权 → 获取 access_token + refresh_token

1. 在浏览器中访问授权页面（替换 YOUR_APPKEY 和 YOUR_REDIRECT_URI）：
 ```
 https://auth.1688.com/oauth/authorize?client_id=YOUR_APPKEY&site=1688&redirect_uri=YOUR_REDIRECT_URI
 ```
2. 用1688账号登录并同意授权
3. 页面会跳转到你的回调地址，URL 中带有 `code` 参数
4. 用 code 换取 Token（有效期短，需在10分钟内使用）：
 ```bash
 curl -X POST "https://gw.open.1688.com/openapi/param2/1/system.oauth2/getToken/YOUR_APPKEY" \
 -d "grant_type=authorization_code" \
 -d "need_refresh_token=true" \
 -d "client_id=YOUR_APPKEY" \
 -d "client_secret=YOUR_APPSECRET" \
 -d "redirect_uri=YOUR_REDIRECT_URI" \
 -d "code=授权码"
 ```
5. 返回结果中包含：
 - `access_token` — 用于调用 API（有效期约10小时）
 - `refresh_token` — 用于刷新 access_token（有效期约半年）

#### Step 4：配置到环境变量

- `ALI1688_APP_KEY` = 应用的 AppKey
- `ALI1688_APP_SECRET` = 应用的 AppSecret
- `ALI1688_REFRESH_TOKEN` = 上一步获得的 refresh_token（推荐，支持自动刷新）
- `ALI1688_ACCESS_TOKEN` = 上一步获得的 access_token（备用，过期需手动换）

#### 常见 Token 错误及解决

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `HTTP 400` 刷新失败 | refresh_token 无效或已过期 | 重新走 Step 3 授权，获取新的 refresh_token |
| `HTTP 401` 未授权 | access_token 过期或无效 | 设置 ALI1688_REFRESH_TOKEN 启用自动刷新 |
| `签名错误(code=25)` | AppSecret 不正确 | 检查 ALI1688_APP_SECRET 是否与应用详情页一致 |
| `无权限调用` | 未订购解决方案 | 回到 Step 2 订购对应解决方案 |
| `refresh_token 半年后过期` | Token 自然过期 | 重新走 Step 3 授权 |

#### 参考链接

- [1688开放平台 - 控制中心](https://open.1688.com/console)
- [API 调用说明](https://open.1688.com/doc/apiInvoke.htm)
- [签名规则](https://open.1688.com/doc/signature.htm)
- [授权说明](https://open.1688.com/doc/apiAuth.htm)
- [解决方案订购](https://open.1688.com/solution/solutionDetail.htm?solutionKey=1697015308755)

## 使用方法

### 0. 自动类目查询
当用户调用商品榜单或热搜词接口但未提供有效类目ID时，系统会自动调用类目接口（`cateId=0`, `language=en`）并完整列出所有一级类目（不省略任何类目），帮助用户选择正确的类目ID。

### 1. 查询商品榜单

```bash
# 查询类目ID=1111的综合榜，返回10个商品（默认英语）
python3 scripts/ranking.py top-list 1111

# 查询热卖榜，返回20个商品（默认英语）
python3 scripts/ranking.py top-list 1111 --type hot --limit 20

# 查询好价榜（默认英语）
python3 scripts/ranking.py top-list 1111 --type goodPrice
```

**参数说明：**

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `rank_id` | 榜单ID / 类目ID（必填） | 类目ID数字 |
| `--type` | 榜单类型 | `complex`(综合榜) / `hot`(热卖榜) / `goodPrice`(好价榜) |
| `--limit` | 返回商品数量（最多20） | 1-20，默认10 |
| `--lang` | 语言代码 | 默认 `en` |

**注意：** 内部调用时，`--type` 参数会转换为 `rankType` 发送到1688 API。

### 2. 查询热搜词

```bash
# 查询类目ID=1的热搜词（英语）
python3 scripts/ranking.py top-keyword 1

# 查询热搜词（英语）
python3 scripts/ranking.py top-keyword 1
```

**参数说明：**

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `source_id` | 类目ID（必填） | 类目ID数字 |
| `--country` | 语言代码 | 默认 `en` |
| `--type` | 热搜类型 | 固定为 `cate`（类目维度） |

### 3. 查询所有一级类目

当需要查询类目时，系统会自动调用类目接口获取完整的类目列表：

```bash
# 查询所有一级类目（英语）
python3 scripts/category.py 0
```

**类目查询参数：**
- `cate_id`: 类目ID，传 `0` 获取所有一级类目
- `--language`: 语言代码，默认 `en`

**注意：** 当用户查询商品榜单或热搜词但未提供有效类目ID时，系统会自动调用类目接口（`cateId=0`, `language=en`）并列出所有可用的一级类目供用户选择。

## 输出格式

JSON 格式，直接返回1688 API 的原始响应数据。
**重要提示：所有商品查询结果都会包含商品ID（itemId字段），这是商品的唯一标识符，可用于后续的商品详情查询或其他操作。**

### 商品榜单返回字段说明
- `itemId` - **商品ID**（重要标识，可用于商品详情查询）
- `title` - 商品中文标题
- `translateTitle` - 商品英文翻译标题
- `imgUrl` - 商品主图URL
- `sort` - 排名序号
- `serviceList` - 服务列表（如 `sendGoods24H`、`sendGoods48H`）
- `buyerNum` - 买家数量
- `soldOut` - 月销量
- `goodsScore` - 商品评分

### 热搜词返回字段说明
- `seKeyword` - 中文热搜关键词
- `seKeywordTranslation` - 英文翻译关键词

### 错误处理
- **失败时不会返回mock数据**：所有API调用失败时都会直接抛出错误
- **错误格式**：返回包含`error`字段的JSON对象，程序退出码为1
- **常见错误**：
  - `Missing ALI1688_APP_KEY or ALI1688_APP_SECRET` - 缺少必要的环境变量
  - `API request failed: ...` - API调用失败（网络、认证、参数等）
  - `Token response missing access_token` - Token刷新失败

## API 接口地址

| 接口 | 完整URL |
|------|---------|
| 查询商品榜单 | `POST https://gw.open.1688.com/openapi/param2/1/com.alibaba.fenxiao.crossborder/product.topList.query/${APPKEY}` |
| 商品热搜词 | `POST https://gw.open.1688.com/openapi/param2/1/com.alibaba.fenxiao.crossborder/product.search.topKeyword/${APPKEY}` |

## 1688接口通用说明

### API接入要点
- **语言支持**: 默认使用 `country=en`，但返回字段包含中英双语
  - 中文字段示例: `title`  
  - 英文字段示例: `translateTitle`
- **Access Token**: 当前解决方案产生的access_token是**长久有效**的
- **筛选条件**: 支持多种商品筛选条件（发货时效、认证工厂、一件代发等）
- **排序功能**: 支持按价格/复购率/月销量排序，但仅对当前页有效

### 重要限制
- **数据量限制**: 每个查询最多返回2000个商品
- **图片搜索**: 仅推荐使用1688图片地址，其他域名成功率不稳定  
- **价格显示**: API返回的是原价，下单时会享受营销价格

### 服务列表映射
- `sendGoods24H` → **24小时发货**
- `sendGoods48H` → **48小时发货**

## API 参考文档

完整的 API 接口和数据结构文档请参阅 [references/api.md](references/api.md)。

## 📋 1688接口通用说明

### 语言支持
- 默认使用 `country=en`（英语）
- 返回数据包含**中英双语字段**：
  - 中文字段：如 `title`（1688商品标题）
  - 英文字段：如 `translateTitle`（翻译后的标题）

### 重要特性
- **Access Token 长久有效**：无需频繁刷新
- **商品筛选**：支持发货时效、认证工厂、一件代发等多种筛选条件
- **排序功能**：支持按价格/复购率/月销量排序（仅当前页有效）

### 限制说明
- **数据量限制**：每个查询最多返回2000个商品
- **图片搜索**：建议使用1688官方图片地址以保证成功率
- **价格显示**：API返回原价，实际下单享受营销优惠价格

### 服务列表映射
- `sendGoods24H` → **24小时发货**
- `sendGoods48H` → **48小时发货**
- 其他服务类型按实际返回值展示