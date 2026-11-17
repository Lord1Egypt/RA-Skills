# 付费模式部署指南

本指南面向**技能作者**，说明如何部署 License Key 验证服务。部署完成后，用户购买 API Key 即可启用完整检测。整个过程约 **5 分钟**，全程免费。

---

## 架构说明

```
用户写文章 → WorkBuddy调用SKILL → detect_words.py
  → 检查是否有API Key
    → 有Key：POST请求Cloudflare Worker验证
      → 验证通过：扣1次 + 完整检测(9409词全量)
      → 验证失败：回退到免费模式(前3个词)
    → 无Key：免费模式(前3个词) + 升级提示
```

**技术栈**：Cloudflare Workers（免费，每天10万次请求）+ KV存储（免费，每天10万次读）

---

## 部署步骤

### 第1步：注册 Cloudflare（1分钟）

1. 打开 https://dash.cloudflare.com/sign-up
2. 用邮箱注册（免费，不需要绑定信用卡）

### 第2步：创建 KV 存储（1分钟）

1. 登录后，左侧菜单 → **Storage & Databases** → **KV**
2. 点击 **Create a namespace**
3. 名称填 `KEYS`，点击 **Add**
4. 记住这个名称，后面要绑定到 Worker

### 第3步：创建 Worker（2分钟）

1. 左侧菜单 → **Workers & Pages**
2. 点击 **Create application** → **Create Worker**
3. 名称填 `geo-word-checker`，点击 **Deploy**
4. 部署成功后点击 **Edit code**
5. **删除编辑器中的所有默认代码**
6. 打开本技能目录下的 `scripts/billing_worker.js`，**复制全部内容**粘贴到编辑器中
7. 点击右上角 **Deploy**

### 第4步：绑定 KV 到 Worker（30秒）

1. 回到 Worker 页面 → **Settings** → **Bindings**
2. 点击 **Add binding** → 选择 **KV Namespace**
3. Variable name 填 `KEYS`，选择刚创建的 KV namespace
4. 点击 **Save and deploy**

### 第5步：设置管理令牌（30秒）

1. 在 **Settings** → **Variables and Secrets**
2. 点击 **Add variable**
3. Variable name 填 `ADMIN_TOKEN`，Value 填一个你自己设的密码（如 `my-secret-token-2026`）
4. Type 选 **Secret**（加密存储），点击 **Save and deploy**

### 第6步：获取 Worker URL

在 Worker 概览页面，你会看到类似：
```
https://geo-word-checker.<你的子域名>.workers.dev
```
这就是你的 **API_ENDPOINT**，用户配置时需要用到。

---

## 管理操作

### 发放 API Key（用户购买后）

```bash
curl -X POST https://geo-word-checker.<你的子域名>.workers.dev/admin/add \
  -H "Content-Type: application/json" \
  -d '{"admin_token":"你的ADMIN_TOKEN","api_key":"gw-abc123xyz","credits":100,"note":"客户A"}'
```

返回：
```json
{"success": true, "api_key": "gw-abc123xyz", "credits": 100, "message": "Key 已添加/充值成功，当前余额 100 次"}
```

> 不填 `api_key` 则自动生成，如 `gw-aBcDeFgH...`

### 查询余额

```bash
curl "https://geo-word-checker.<你的子域名>.workers.dev/admin/balance?admin_token=你的ADMIN_TOKEN&api_key=gw-abc123xyz"
```

返回：
```json
{"api_key": "gw-abc123xyz", "remaining": 95, "total_used": 5, ...}
```

### 充值（给已有Key加次数）

```bash
curl -X POST https://geo-word-checker.<你的子域名>.workers.dev/admin/add \
  -H "Content-Type: application/json" \
  -d '{"admin_token":"你的ADMIN_TOKEN","api_key":"gw-abc123xyz","credits":50}'
```

### 吊销 Key

```bash
curl -X POST https://geo-word-checker.<你的子域名>.workers.dev/admin/revoke \
  -H "Content-Type: application/json" \
  -d '{"admin_token":"你的ADMIN_TOKEN","api_key":"gw-abc123xyz"}'
```

---

## 用户配置方式

用户购买 API Key 后，在 WorkBuddy 中通过环境变量配置：

### 方式1：环境变量（推荐）

在系统环境变量中设置：
```
GEO_API_KEY=gw-abc123xyz
GEO_API_ENDPOINT=https://geo-word-checker.<你的子域名>.workers.dev
```

### 方式2：脚本参数

```bash
python detect_words.py --file article.txt --wordlist words.txt --classify \
  --api-key gw-abc123xyz \
  --api-endpoint https://geo-word-checker.<你的子域名>.workers.dev
```

---

## 定价建议

| 套餐 | 次数 | 建议价格 |
|---|---|---|
| 试用包 | 10次 | 1元 |
| 基础包 | 100次 | 9.9元 |
| 专业包 | 500次 | 39.9元 |
| 企业包 | 2000次 | 99元 |

> 每次检测一篇文章扣1次。Cloudflare 免费层每天10万次请求，无需支付任何服务器费用。

---

## 常见问题

**Q: 免费层够用吗？**
A: Cloudflare Workers 免费层每天10万次请求，KV 每天10万次读+1000次写。即使有1000个付费用户每天各检测10篇文章，也只用到1万次请求，完全够用。

**Q: 用户没有配置 API Key 会怎样？**
A: 自动进入免费模式，只显示前3个违禁词。功能不中断，只是结果不完整。

**Q: Key 验证服务挂了怎么办？**
A: 脚本会捕获连接错误，自动回退到免费模式，不会影响用户使用。

**Q: 如何收款？**
A: 通过你的渠道（微信/支付宝/淘宝等）收款后，用 admin/add 接口发放 Key。后续可以做一个简单的购买页面自动化这个过程。
