---
name: domainrank-submit
description: 提交网站到 DomainRank.app 导航站。使用场景：(1) 用户想要提交网站到 AI 导航站，(2) 用户说"提交到 domainrank"、"submit to domainrank"、"提交网站"，(3) 用户需要批量提交多个网站到导航站。触发词：domainrank、提交网站、submit site、导航站提交、AI 导航。
---

# DomainRank 导航站提交

通过 API 将网站提交到 DomainRank.app AI 导航站。

## API 端点

```
POST https://domainrank.app/api/submit-item
```

## 认证

使用 Bearer Token 认证，API Key 从 DomainRank 设置页面获取。

```bash
Authorization: Bearer <YOUR_DOMAINRANK_API_KEY>
```

> 将 `<YOUR_DOMAINRANK_API_KEY>` 替换为你自己的 API Key。建议通过环境变量传入，不要硬编码到代码中。

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 网站名称 |
| link | string | 是 | 网站 URL |
| pricePlan | string | 否 | 定价方案：basic(默认)、pro、ultra |

## 定价方案与积分消耗

| 方案 | 积分 | 功能 |
|------|------|------|
| basic | 100 | 基础收录 |
| pro | 200 | 收录 + 社交媒体推广 |
| ultra | 2000 | 收录 + 社交媒体 + AI 目录分发 |

## 提交示例

```bash
curl -X POST https://domainrank.app/api/submit-item \
  -H "Authorization: Bearer <YOUR_DOMAINRANK_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Website",
    "link": "https://example.com",
    "pricePlan": "basic"
  }'
```

## 响应格式

成功响应 (200):
```json
{
  "success": true,
  "item": "https://domainrank.app/item/my-website",
  "name": "My Website",
  "link": "https://example.com",
  "pricePlan": "basic",
  "creditsConsumed": 100,
  "creditsRemaining": 4900
}
```

错误响应:
- 401: API Key 无效或缺失
- 400: 参数错误 (name/link 缺失或 pricePlan 无效)
- 402: 积分不足
- 409: 网站已存在
- 500: 服务器错误

## 批量提交

批量提交多个网站时，**必须先向用户确认以下信息，得到明确同意后再执行**：

- 提交的网站列表
- 每个网站使用的 pricePlan
- 预计总积分消耗

确认后再依次调用 API：

```bash
for site in "Site1|https://site1.com" "Site2|https://site2.com"; do
  name="${site%|*}"
  link="${site#*|}"
  curl -X POST https://domainrank.app/api/submit-item \
    -H "Authorization: Bearer <YOUR_DOMAINRANK_API_KEY>" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$name\", \"link\": \"$link\", \"pricePlan\": \"basic\"}"
  sleep 1
done
```

## 注意事项

1. URL 会自动清理：移除查询参数和尾部斜杠
2. AI 自动填充：系统会自动抓取网站信息填充描述、分类、标签、图标
3. 重复检测：相同 URL 无法重复提交
4. 积分退款：如果 AI 抓取失败，积分会自动退还

---

更多 AI SEO 技能详见：https://domainrank.app/ai-seo-skills
