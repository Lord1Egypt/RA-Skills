---
name: binance-square-post
description: |
  发送内容到 Binance Square（币安广场）。
  支持纯文字帖子，可带 $代币标签（如 $BTC）和 #话题标签。
  集成每日新闻简报功能，自动获取 Web3/AI 热点并发布到 Square。
  用户需要先配置自己的 API Key 才能使用。
metadata:
  author: shandian
  version: "1.1.0"
---

# Binance Square Post Skill

## 概述

将文字内容发布到 Binance Square（币安广场社交平台），支持自动生成并发布每日新闻简报。

## 使用前配置

用户需要先配置自己的 Square OpenAPI Key：

### 获取 API Key

1. 登录 Binance 账户
2. 访问 [Binance Square OpenAPI](https://www.binance.com/zh-CN/square/openapi) 页面
3. 创建或获取你的 OpenAPI Key

### 配置方法

在 skill 文件中添加配置：

```yaml
config:
  accounts:
    - name: default
      api_key: 你的API密钥
```

---

## 功能 1：手动发帖

### API 调用

#### Endpoint

```
POST https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add
```

#### Headers

| Header | 必填 | 说明 |
|--------|------|------|
| X-Square-OpenAPI-Key | 是 | 你的 Square OpenAPI Key |
| Content-Type | 是 | application/json |
| clienttype | 是 | binanceSkill |

#### Body

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| bodyTextOnly | string | 是 | 帖子内容（支持 $代币标签和 #话题标签）|

#### 示例

```bash
curl -X POST 'https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add' \
  -H 'X-Square-OpenAPI-Key: 你的API密钥' \
  -H 'Content-Type: application/json' \
  -H 'clienttype: binanceSkill' \
  -d '{
    "bodyTextOnly": "Hello Binance Square! $BTC #Crypto"
  }'
```

#### 响应

成功响应：
```json
{
  "code": "000000",
  "message": null,
  "data": {
    "id": "123456789012345"
  },
  "success": true
}
```

帖子链接：`https://www.binance.com/square/post/{id}`

---

## 功能 2：自动每日新闻简报

### 数据源

使用 6551 API 获取每日热点新闻：

- Web3 新闻：`GET https://ai.6551.io/open/free_hot?category=web3`
- AI 新闻：`GET https://ai.6551.io/open/free_hot?category=ai`
- 宏观新闻：`GET https://ai.6551.io/open/free_hot?category=macro`

### 自动生成简报流程

1. 调用以上 API 获取当日热点新闻
2. 筛选高质量内容（A+ 级）
3. 整理成简报格式
4. 调用 Binance Square API 发布

### 简报模板

```
📰 每日新闻简报 - [日期]

🔥 今日热点
1️⃣ [热点1]
2️⃣ [热点2]
3️⃣ [热点3]
4️⃣ [热点4]
5️⃣ [热点5]

---

#每日新闻 #Web3 #AI #加密货币
```

### 定时任务配置（可选）

用户可以通过 OpenClaw cron 设置每日自动发布：

```
任务时间：每天北京时间 00:00（早上8点）
```

---

## 错误码

| 错误码 | 说明 |
|--------|------|
| 000000 | 成功 |
| 10004 | 网络错误，请重试 |
| 10005 | 仅限已完成身份验证的用户 |
| 10007 | 功能不可用 |
| 20002 | 检测到敏感词 |
| 20013 | 内容长度受限 |
| 20020 | 发布空内容不被支持 |
| 30004 | 用户未找到 |
| 30008 | 因违规被禁言 |
| 220003 | API Key 未找到 |
| 220004 | API Key 已过期 |
| 220009 | 每日发帖上限已达 |

---

## 使用示例

### 示例 1：简单发帖

用户：发一条帖子到 Binance Square，内容是 "Hello World"

### 示例 2：币圈分析发帖

用户：帮我发一条关于 $BTC 行情分析的帖子

1. 查询代币当前价格（使用 query-token-info skill）
2. 构造分析内容
3. 调用 API 发送

### 示例 3：发布每日新闻简报

用户：生成并发布今日新闻简报

1. 获取 Web3/AI/宏观 新闻
2. 筛选热点内容
3. 生成简报
4. 发布到 Square
5. 返回帖子链接

### 示例 4：带话题标签

```
$BTC #比特币 #加密货币 #行情分析
```

---

## 安全注意事项

1. **永远不要在公开场合暴露完整的 API Key**
2. 显示 API Key 时只显示首5位+末4位，如：`abc12...xyz9`
3. 定期检查 API Key 权限设置
4. 如发现异常，及时在 Binance 官网重置 Key

---

## 注意事项

1. 目前仅支持纯文字帖子（不支持图片、视频）
2. 内容长度有限制（避免超过 2000 字符）
3. 建议帖子内容加上热门话题标签以获得更多曝光
4. 每日简报会自动筛选高质量新闻，确保内容价值
