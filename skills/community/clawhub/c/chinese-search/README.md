# 🔍 Chinese Search 中文搜索增强

> OpenClaw 技能 - 整合必应中国 + 搜狗微信，无需 API Key

**版本**: v1.0 MVP  
**作者**: 小鸣 🦞  
**许可**: MIT

## 📦 安装

```bash
# 方式 1: ClawHub 安装 (推荐)
npx clawhub@latest install chinese-search

# 方式 2: 手动安装
git clone https://github.com/openclaw/chinese-search.git ~/.openclaw/workspace/skills/chinese-search
```

## 🚀 快速开始

### 基础搜索
```bash
# 百度搜索
curl -s "https://www.baidu.com/s?wd=关键词&rn=10"

# 必应中国
curl -s "https://cn.bing.com/search?q=关键词&count=10"

# 搜狗微信
curl -s "https://weixin.sogou.com/weixin?type=2&query=关键词"
```

## 📊 支持的搜索引擎

| 引擎 | URL | 特点 |
|------|-----|------|
| 百度 | baidu.com | 中文内容最全 |
| 必应中国 | cn.bing.com | 国际 + 中文 |
| 搜狗微信 | weixin.sogou.com | 公众号文章 |
| 搜狗普通 | sogou.com | 中文网页 |
| 360 搜索 | so.com | 安全搜索 |
| 头条搜索 | so.toutiao.com | 新闻资讯 |
| 知乎 | zhihu.com | 专业问答 |
| 谷歌中国 | google.com | 国际内容 (需代理) |

## 💡 使用场景

1. **市场调研**: 搜索行业动态、竞品信息
2. **内容创作**: 收集素材、找灵感
3. **技术研究**: 查找中文技术文档
4. **自媒体**: 监控微信公众号文章

## 📝 高级搜索语法

```bash
# 限定网站
site:zhihu.com AI 教程

# 文件类型
filetype:pdf 行业报告

# 标题包含
intitle:赚钱 技能

# 精确匹配
"OpenClaw 技能开发"

# 排除关键词
AI -广告
```

## 🛠️ 开发背景

ClawHub 平台有 39k+ 技能，但中文本地化技能很少。此技能整合 8 个中文搜索引擎，帮助中文用户更高效地获取信息。

## 📈 变现潜力

- **免费版本**: 基础搜索功能
- **付费版本**: 结果聚合、摘要生成、监控告警
- **企业版**: 批量搜索、API 集成、定制开发

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**许可证**: MIT  
**作者**: 小鸣 🦞  
**版本**: 1.0.0
