# Douyin Scraper - 抖音搜索爬虫技能

支持自然语言搜索抖音视频内容的 OpenClaw 技能。

## 快速开始

```bash
# 直接使用自然语言搜索
python scripts/search_douyin.py "搜索一下海鲜视频"
```

## 功能

- ✅ 中文自然语言理解
- ✅ 自动提取关键词、数量、排序方式
- ✅ 格式化输出 / JSON 输出
- ✅ 可扩展的浏览器自动化接口

## 文件结构

```
douyin-scraper/
├── SKILL.md              # AI 代理使用的技能说明
├── README.md             # 本文件
├── _meta.json            # 元数据
├── scripts/
│   └── search_douyin.py  # 核心搜索脚本
├── examples/
│   └── search_requests.txt # 搜索请求示例
└── references/           # 参考文档目录
```

## 使用示例

```bash
# 基础搜索
python scripts/search_douyin.py "搜索一下海鲜视频"

# 带条件的搜索
python scripts/search_douyin.py "找5个最热猫咪视频"

# JSON 输出
python scripts/search_douyin.py "海鲜视频" --json
```

## 在 OpenClaw 中使用

此技能会在用户提出抖音视频搜索相关请求时自动触发。支持以下自然语言表达：
- "搜索一下海鲜视频"
- "帮我找抖音上的猫咪视频"
- "抖音有什么搞笑视频吗"

## 扩展真实爬取

当前版本包含模拟搜索结果。如需实现真实爬取，可以：
1. 结合 agent-browser skill 进行浏览器自动化
2. 对接抖音开放平台 API
3. 使用第三方抖音数据服务
