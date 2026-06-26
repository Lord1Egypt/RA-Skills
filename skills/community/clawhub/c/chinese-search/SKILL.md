---
name: chinese-search
description: 中文搜索增强，整合必应中国、搜狗微信等中文搜索引擎 (MVP v1.0)
homepage: https://github.com/openclaw/chinese-search
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["curl"]}}}
---

# Chinese Search 中文搜索增强

**MVP v1.0** - 整合 2 个核心中文搜索引擎，无需 API Key，支持高级搜索语法。

## 快速使用

### 基础搜索
```bash
# 百度搜索
curl -s "https://www.baidu.com/s?wd=关键词&rn=10"

# 必应中国
curl -s "https://cn.bing.com/search?q=关键词&count=10"

# 搜狗微信搜索
curl -s "https://weixin.sogou.com/weixin?type=2&query=关键词"
```

### 高级搜索语法

| 语法 | 说明 | 示例 |
|------|------|------|
| `site:` | 限定网站 | `site:zhihu.com AI 教程` |
| `filetype:` | 文件类型 | `filetype:pdf 研究报告` |
| `intitle:` | 标题包含 | `intitle:赚钱 技能` |
| `inurl:` | URL 包含 | `inurl:blog 教程` |
| `""` | 精确匹配 | `"OpenClaw 技能开发"` |
| `-` | 排除关键词 | `AI -广告` |

## 搜索引擎列表

### ✅ v1.0 已实现

#### 1. 必应中国 (Bing CN)
- URL: `https://cn.bing.com/search?q={query}`
- 特点：国际内容 + 中文
- 适用：技术文档、学术搜索、通用查询
- 状态：✅ 工作正常

#### 2. 搜狗微信 (Sogou WeChat)
- URL: `https://weixin.sogou.com/weixin?type=2&query={query}`
- 特点：微信公众号文章
- 适用：自媒体内容、行业动态、营销素材
- 状态：✅ 工作正常
- **独特价值**: 全网唯一可搜索微信公众号的技能

### 🚧 计划中 (v1.1-v2.0)

| 引擎 | 状态 | 说明 |
|------|------|------|
| 百度 | 🚧 优化中 | 需要 User-Agent/Cookie 处理 |
| 知乎 | 🚧 优化中 | 需要调整请求格式 |
| 360 | 📋 计划中 | 可能需要浏览器自动化 |
| 头条 | 📋 计划中 | 可能需要浏览器自动化 |
| 搜狗普通 | 📋 计划中 | 后续迭代 |
| 谷歌中国 | 📋 计划中 | 需要代理支持 |

## 实战案例

### 案例 1: 搜索中文技术教程
```bash
# 搜索 OpenClaw 技能开发教程
curl -s "https://www.baidu.com/s?wd=OpenClaw+ 技能开发 + 教程&rn=10"

# 搜索知乎相关讨论
curl -s "https://www.zhihu.com/search?type=content&q=OpenClaw+ 技能"
```

### 案例 2: 搜索行业报告
```bash
# 搜索 PDF 格式的行业报告
curl -s "https://www.baidu.com/s?wd=AI+ 行业报告+2026+filetype:pdf"
```

### 案例 3: 搜索微信公众号文章
```bash
# 搜索自媒体相关内容
curl -s "https://weixin.sogou.com/weixin?type=2&query=AI+ 自动化+ 赚钱"
```

## 集成到 OpenClaw

### 安装
```bash
npx clawhub@latest install chinese-search
```

### 使用
```bash
# 调用技能
/search 中文关键词

# 或直接用 curl
curl -s "wttr.in/中文搜索 + 关键词"
```

## 注意事项

1. **反爬虫**: 部分搜索引擎有频率限制，建议添加延迟
2. **结果解析**: 搜索结果需要解析 HTML 提取内容
3. **代理需求**: 谷歌搜索需要代理才能访问
4. **API 限制**: 商业使用建议申请官方 API

## 扩展方向

1. **结果聚合**: 整合多个引擎结果，去重排序
2. **摘要生成**: 自动提取搜索结果摘要
3. **监控告警**: 关键词监控，有新内容时通知
4. **批量搜索**: 支持批量关键词搜索

---

**作者**: 小鸣 🦞  
**版本**: v1.0  
**创建时间**: 2026-03-29
