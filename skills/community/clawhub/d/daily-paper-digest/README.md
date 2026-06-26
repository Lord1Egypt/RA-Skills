# 📚 每日论文速递 Skill

一个用于 OpenClaw 的每日 AI 论文速递技能，自动聚合 arXiv 和 HuggingFace 的最新论文。

## ✨ 特性

- 🔍 自动抓取 arXiv 最新论文（支持多个分类）
- 🤗 获取 HuggingFace 每日热门论文
- 🎯 支持关键词过滤
- 📅 每日定时推送
- 🎨 优雅的格式化输出
- ⚙️ 灵活的配置选项

## 📁 项目结构

```
daily_paper_digest/
├── config/
│   └── sources.json          # 信息源配置文件
├── skill.json                 # Skill 定义文件
├── main.py                    # 主程序入口
├── arxiv_fetcher.py          # arXiv 爬取模块
├── huggingface_fetcher.py    # HuggingFace 爬取模块
├── requirements.txt          # Python 依赖
└── README.md                 # 本文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd daily_paper_digest
pip install -r requirements.txt
```

### 2. 配置信息源

编辑 `config/sources.json` 文件：

```json
{
  "sources": [
    {
      "name": "arxiv",
      "enabled": true,
      "categories": [
        "cs.AI",    // 人工智能
        "cs.CL",    // 计算语言学
        "cs.CV",    // 计算机视觉
        "cs.LG",    // 机器学习
        "cs.NE"     // 神经网络
      ],
      "max_results": 10
    },
    {
      "name": "huggingface",
      "enabled": true,
      "max_results": 10
    }
  ],
  "filter": {
    "keywords": ["LLM", "transformer", "GPT"],
    "exclude_keywords": ["medical", "biology"]
  }
}
```

### 3. 测试运行

```bash
# 测试 arXiv 模块
python arxiv_fetcher.py

# 测试 HuggingFace 模块
python huggingface_fetcher.py

# 运行完整程序
python main.py
```

## 📝 配置说明

### arXiv 分类代码

常用的 arXiv 分类：

- `cs.AI` - 人工智能
- `cs.CL` - 计算语言学/自然语言处理
- `cs.CV` - 计算机视觉
- `cs.LG` - 机器学习
- `cs.NE` - 神经网络
- `cs.RO` - 机器人
- `stat.ML` - 统计机器学习

更多分类请参考：https://arxiv.org/category_taxonomy

### 输出格式配置

```json
{
  "output_format": {
    "include_abstract": true,    // 是否包含摘要
    "include_authors": true,     // 是否包含作者
    "include_links": true,       // 是否包含链接
    "language": "zh-CN"          // 输出语言
  }
}
```

### 过滤器配置

```json
{
  "filter": {
    "keywords": ["LLM", "GPT"],           // 包含关键词（留空表示不过滤）
    "exclude_keywords": ["medical"]        // 排除关键词
  }
}
```

## 🔧 OpenClaw 集成

### 1. 部署到 OpenClaw

将整个 `daily_paper_digest` 文件夹复制到 OpenClaw 的 skills 目录：

```bash
cp -r daily_paper_digest /path/to/openclaw/skills/
```

### 2. 在 OpenClaw 中使用

触发方式：

1. **关键词触发**：在聊天中发送 "论文速递"、"今日论文"、"最新论文"
2. **命令触发**：发送 `/papers` 或 `/digest`
3. **定时触发**：每天早上 9:00 自动推送（在 `skill.json` 中配置）

### 3. 修改定时任务

编辑 `skill.json` 中的 `schedule` 字段（Cron 表达式）：

```json
{
  "schedule": "0 9 * * *"  // 每天 9:00
}
```

常用 Cron 表达式：
- `0 9 * * *` - 每天 9:00
- `0 9,18 * * *` - 每天 9:00 和 18:00
- `0 9 * * 1-5` - 工作日 9:00

## 📊 输出示例

```
╔══════════════════════════════════════════════════════════╗
║           🎓 AI 论文每日速递 - 2026年02月20日           ║
╚══════════════════════════════════════════════════════════╝

📊 今日共收录 15 篇论文

============================================================
📄 论文 1
============================================================

📌 标题: Attention Is All You Need
👥 作者: Ashish Vaswani, Noam Shazeer, Niki Parmar 等 8 人
🏷️  来源: ARXIV | 日期: 2026-02-20

📝 摘要:
The dominant sequence transduction models are based on complex 
recurrent or convolutional neural networks...

🔗 arXiv: http://arxiv.org/abs/1706.03762
📥 PDF: http://arxiv.org/pdf/1706.03762

...

============================================================
📈 信息源统计:
   • arXiv: 10 篇
   • HuggingFace: 5 篇

⏰ 更新时间: 2026-02-20 09:00:00
============================================================
```

## 🛠️ 高级用法

### 手动获取特定主题论文

```python
from arxiv_fetcher import ArxivFetcher

fetcher = ArxivFetcher(categories=['cs.AI'], max_results=5)
papers = fetcher.search_papers("large language model", max_results=10)

for paper in papers:
    print(f"标题: {paper['title']}")
    print(f"链接: {paper['arxiv_url']}\n")
```

### 自定义输出格式

修改 `main.py` 中的 `format_paper()` 和 `format_digest()` 方法。

## 🐛 故障排除

### 1. arXiv API 访问失败

- 检查网络连接
- 确认是否被限流（arXiv 有访问频率限制）
- 尝试使用代理

### 2. HuggingFace 页面解析失败

- HuggingFace 页面结构可能更新，需要调整 `huggingface_fetcher.py` 中的解析逻辑
- 检查是否被反爬虫机制拦截

### 3. 依赖安装失败

```bash
# 使用清华镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 📈 未来计划

- [ ] 支持更多论文源（Papers with Code, Semantic Scholar）
- [ ] 添加论文摘要的中文翻译
- [ ] 支持订阅特定关键词
- [ ] 论文相关性推荐
- [ ] 导出为 PDF/Markdown
- [ ] Web Dashboard

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题，请通过以下方式联系：

- 提交 GitHub Issue
- OpenClaw 社区讨论

---

**享受每日论文速递！📚✨**
