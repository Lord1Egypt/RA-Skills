# Copywriter - AI 营销文案生成器 v0.1.0

🚀 **VIC ai-company 首款商业化技能**

---

## 快速开始

### 安装

```bash
# 克隆或复制技能到 OpenClaw workspace
cp -r copywriter ~/.openclaw/workspace/skills/

# 安装依赖（如有）
cd ~/.openclaw/workspace/skills/copywriter
pip install -r requirements.txt
```

### 使用示例

```bash
# 生成 Facebook 广告文案
python3 scripts/copywriter.py generate --type ad --product "智能手表" --platform facebook --tone casual

# 生成小红书种草内容
python3 scripts/copywriter.py generate --type social --topic "护肤分享" --platform xiaohongshu --tone friendly

# 生成促销邮件
python3 scripts/copywriter.py generate --type email --product "冬季大促" --platform promotion --tone urgent
```

---

## 功能特性

✅ **7 种文案类型**
- 广告文案 (ad)
- 社交媒体 (social)
- 邮件营销 (email)
- 产品描述 (product)
- 落地页 (landing)
- 博客文章 (blog)
- 视频脚本 (video)

✅ **多平台适配**
- Facebook/Google/抖音广告
- 小红书/微博/Twitter
- 邮件营销平台

✅ **7 种语气风格**
- 专业、轻松、说服力强、幽默、紧迫感、友好、高端

✅ **批量生成**
- 支持一次生成多个变体进行 A/B 测试

---

## 定价策略

| 版本 | 价格 | 功能 |
|------|------|------|
| **基础版** | $29 | 单次生成，3 个变体 |
| **专业版** | $99 | 无限生成，10 个变体，A/B 测试建议 |
| **企业版** | $299 | 定制语气，批量生成，API 访问 |

---

## 开发路线图

### v0.1.0 (当前) ✅
- [x] 基础文案生成
- [x] 多平台支持
- [x] 多语气风格

### v0.2.0 (计划中)
- [ ] 集成 Qwen API 实时生成
- [ ] 多语言支持
- [ ] SEO 优化建议

### v1.0.0 (目标)
- [ ] 转化率追踪
- [ ] A/B 测试结果分析
- [ ] 竞品分析集成
- [ ] 自动化工作流集成

---

## 技术栈

- Python 3.8+
- OpenAI 兼容 API (Qwen)
- JSON 输出格式

---

## 贡献者

**VIC ai-company**
- 开发：skill-dev agent
- 协调：main agent (CEO)
- 成立日期：2026-02-28

---

## 许可

MIT License

---

## 联系方式

- 购买/定制：联系 main agent
- 技术支持：查看文档或提交 issue

---

**📈 让 AI 为你的营销赋能！**
