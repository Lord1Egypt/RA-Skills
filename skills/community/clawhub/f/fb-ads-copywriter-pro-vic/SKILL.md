---
name: copywriter
description: AI 营销文案生成器 - 生成高转化率广告文案、社交媒体内容、邮件营销内容
author: AI Company
version: 0.1.0
metadata: {"emoji": "✍️", "category": "marketing"}
---

# Copywriter - AI 营销文案生成器

生成高转化率的营销文案，适用于广告、社交媒体、邮件营销等场景。

## 功能特性

- 📝 **广告文案生成** - Google Ads、Facebook Ads、抖音广告等
- 📱 **社交媒体内容** - 微博、小红书、Twitter、LinkedIn
- 📧 **邮件营销** - 开发信、促销邮件、新闻通讯
- 🛒 **电商产品描述** - 亚马逊、淘宝、Shopify 产品页面
- 🎯 **落地页文案** - 销售页面、着陆页优化

## 使用方法

### 基础用法

```bash
# 生成广告文案
uv run scripts/copywriter.py generate --type ad --product "智能手表" --platform facebook

# 生成社交媒体内容
uv run scripts/copywriter.py generate --type social --topic "健身打卡" --platform xiaohongshu

# 生成邮件营销
uv run scripts/copywriter.py generate --type email --purpose "促销" --product "冬季大促"
```

### 高级选项

```bash
# 指定语气风格
uv run scripts/copywriter.py generate --type ad --tone "professional" --product "企业软件"

# 生成多个变体
uv run scripts/copywriter.py generate --type ad --variations 5 --product "咖啡机"

# 指定目标受众
uv run scripts/copywriter.py generate --type ad --audience "25-35 岁女性" --product "护肤品"
```

## 文案类型

| 类型 | 描述 | 适用场景 |
|------|------|----------|
| `ad` | 广告文案 | Google/Facebook/抖音广告 |
| `social` | 社交媒体 | 微博/小红书/Twitter/LinkedIn |
| `email` | 邮件营销 | 开发信/促销邮件/新闻通讯 |
| `product` | 产品描述 | 电商产品页面 |
| `landing` | 落地页 | 销售页面/着陆页 |
| `blog` | 博客文章 | 内容营销/SEO |
| `video` | 视频脚本 | 抖音/B 站/YouTube |

## 语气风格

| 风格 | 描述 |
|------|------|
| `professional` | 专业正式 |
| `casual` | 轻松随意 |
| `persuasive` | 说服力强 |
| `humorous` | 幽默风趣 |
| `urgent` | 紧迫感 |
| `friendly` | 友好亲切 |
| `luxury` | 高端奢华 |

## 输出格式

```json
{
  "type": "ad",
  "platform": "facebook",
  "variations": [
    {
      "headline": " headline text",
      "body": "body text",
      "cta": "call to action"
    }
  ],
  "metadata": {
    "tone": "persuasive",
    "audience": "target audience",
    "generatedAt": "2026-02-28T01:04:00Z"
  }
}
```

## 定价建议

| 版本 | 功能 | 价格 |
|------|------|------|
| 基础版 | 单次生成，3 个变体 | $29 |
| 专业版 | 无限生成，10 个变体，A/B 测试建议 | $99 |
| 企业版 | 定制语气，批量生成，API 访问 | $299 |

## 示例

### Facebook 广告文案

**输入：**
```bash
uv run scripts/copywriter.py generate --type ad --product "无线耳机" --platform facebook --tone "casual"
```

**输出：**
```
🎧 终于找到完美的无线耳机了！

✅ 40 小时超长续航
✅ 主动降噪，静享音乐
✅ 舒适佩戴，整天不累

限时优惠：买一送一！
👉 立即抢购：[链接]

#无线耳机 #音乐爱好者 #限时优惠
```

### 小红书种草文案

**输入：**
```bash
uv run scripts/copywriter.py generate --type social --topic "早 C 晚 A 护肤" --platform xiaohongshu
```

**输出：**
```
✨ 早 C 晚 A 护肤法｜28 天焕肤实录📝

姐妹们！坚持了一个月的早 C 晚 A
皮肤真的亮了一个度！！💡

☀️ 早上：VC 精华 + 防晒
🌙 晚上：A 醇 + 修复霜

⚠️ 注意事项：
1. 新手从低浓度开始
2. 一定要做好防晒
3. 敏感肌先做皮试

产品清单在评论区👇

#早 C 晚 A #护肤分享 #焕肤秘籍
```

## 技术实现

- 使用 Qwen3.5-Plus 模型生成文案
- 支持批量生成和 A/B 测试
- 可集成到 OpenClaw 工作流

## 更新日志

### v0.1.0 (2026-02-28)
- 初始版本发布
- 支持 7 种文案类型
- 支持 7 种语气风格
- 多平台适配

## 待开发功能

- [ ] 多语言支持
- [ ] SEO 优化建议
- [ ] 竞品分析集成
- [ ] 转化率追踪
- [ ] A/B 测试结果分析

---

**开发者：** VIC ai-company  
**许可：** MIT  
**支持：** 联系 main agent
