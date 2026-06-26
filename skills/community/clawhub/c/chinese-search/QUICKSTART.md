# 🚀 Chinese Search 快速开始指南

> 5 分钟上手中文搜索增强

---

## ⚡ 快速安装

```bash
npx clawhub@latest install chinese-search
```

---

## 🔍 基础使用

### 1. 必应中国搜索

```bash
curl -s "https://cn.bing.com/search?q=关键词&count=10"
```

**示例**:
```bash
curl -s "https://cn.bing.com/search?q=AI+ 自动化&count=10"
```

### 2. 搜狗微信搜索

```bash
curl -s "https://weixin.sogou.com/weixin?type=2&query=关键词&ie=utf8"
```

**示例**:
```bash
curl -s "https://weixin.sogou.com/weixin?type=2&query=AI+ 赚钱&ie=utf8"
```

---

## 💡 高级搜索语法

### 限定网站
```bash
# 只搜索知乎内容
curl -s "https://cn.bing.com/search?q=site:zhihu.com+AI+ 教程"
```

### 文件类型
```bash
# 搜索 PDF 文档
curl -s "https://cn.bing.com/search?q=filetype:pdf+ 行业报告"
```

### 标题搜索
```bash
# 标题包含关键词
curl -s "https://cn.bing.com/search?q=intitle:赚钱 + 技能"
```

### 精确匹配
```bash
# 精确短语匹配
curl -s "https://cn.bing.com/search?q=%22OpenClaw+ 技能开发%22"
```

---

## 📊 使用场景

### 场景 1: 市场调研
```bash
# 搜索行业动态
curl -s "https://cn.bing.com/search?q=AI+ 行业报告+2026"

# 搜索竞品信息
curl -s "https://weixin.sogou.com/weixin?type=2&query= 竞品分析+AI"
```

### 场景 2: 内容创作
```bash
# 找灵感素材
curl -s "https://cn.bing.com/search?q=自媒体 + 选题 +2026"

# 搜索公众号文章
curl -s "https://weixin.sogou.com/weixin?type=2&query= 内容创作 + 技巧"
```

### 场景 3: 技术研究
```bash
# 搜索技术文档
curl -s "https://cn.bing.com/search?q=OpenClaw+ 技能开发 + 教程"

# 搜索知乎讨论
curl -s "https://cn.bing.com/search?q=site:zhihu.com+AI+ 自动化"
```

---

## ⚠️ 注意事项

1. **频率限制**: 建议每次请求间隔 1-2 秒
2. **User-Agent**: 部分引擎需要设置 UA
3. **结果解析**: 返回的是 HTML，需要解析提取内容
4. **网络环境**: 确保能访问相关网站

---

## 🆘 常见问题

### Q: 搜索结果为空？
A: 检查关键词编码，中文需要 URL 编码

### Q: 请求被拒绝？
A: 添加 User-Agent 头，降低请求频率

### Q: 如何解析结果？
A: 使用 `grep`、`sed` 或 HTML 解析库

---

## 📚 更多文档

- [完整文档](SKILL.md)
- [测试结果](TEST-RESULTS.md)
- [发布指南](CLAWHUB-PUBLISH.md)

---

**版本**: v1.0  
**更新时间**: 2026-03-29
