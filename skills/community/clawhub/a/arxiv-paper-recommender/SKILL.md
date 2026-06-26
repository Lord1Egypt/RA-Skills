---
name: arxiv-paper-recommender
description: 推荐高质量的 Agent/RAG 论文。当用户提到"推荐论文"、"arxiv论文"、"Agent论文"、"RAG论文"、"论文推荐"、"看论文"、"找论文"、"最近有什么好论文"时触发此技能。支持主题：Agent测评、RAG测评、Agent架构、RAG架构。自动验证 GitHub 代码，生成结构化报告。
---

# arXiv 论文推荐器

推荐近期高质量 Agent/RAG 领域论文，确保有配套代码，1分钟内让读者抓住核心价值。

## 触发词

- "推荐一篇论文"、"帮我找篇论文"
- "Agent论文"、"RAG论文"
- "论文推荐"、"arxiv推荐"
- "最近有什么好论文"
- "推荐一篇 Agent/RAG 相关的论文"

## 支持的主题

| 主题代码 | 中文名称 | 说明 |
|---------|---------|------|
| agent-eval | Agent测评 | Agent 评估方法、Benchmark |
| rag-eval | RAG测评 | RAG 评估方法、Benchmark |
| agent-arch | Agent架构 | Agent 框架设计、系统构建 |
| rag-arch | RAG架构 | RAG 系统架构、框架设计 |

用户可指定主题，不指定则随机选择。

## 工作流程

### Step 1: 确定主题

```
如果用户指定了主题 → 使用指定主题
否则 → 从四个主题中随机选择一个
```

### Step 2: 执行搜索脚本

```bash
cd ~/.openclaw/workspace/skills/arxiv-paper-recommender/scripts
python3 recommend.py [topic]
```

参数：
- `topic` 可选，值为 `agent-eval`、`rag-eval`、`agent-arch`、`rag-arch` 之一
- 不传参数则随机选择

### Step 3: 读取生成的报告

脚本会自动：
1. 搜索 arXiv 最近 6 个月的论文
2. 访问论文页面查找 GitHub 链接
3. 验证 GitHub 仓库有效性
4. 分析论文摘要提取关键信息
5. 生成 Markdown 报告

报告保存位置：`~/papers/recommendations/YYYY-MM-DD_[arxiv_id].md`

### Step 4: 向用户展示推荐结果

输出格式示例：

```
📄 推荐论文：[标题]

🎯 主题：Agent架构设计
📅 发布：2026-03-01
⭐ GitHub：1.2k stars

一句话：这篇论文提出了 [方法名]，解决了 [问题]。

推荐理由：
1️⃣ 解决了 [具体问题]
2️⃣ 采用 [方法]，亮点是 [创新点]
3️⃣ 实践建议：[核心建议]
4️⃣ 代码质量：⭐ X stars，最近 X 天更新

🔗 arxiv.org/abs/xxxx.xxxxx
💻 github.com/xxx/xxx

完整报告已保存至：~/papers/recommendations/xxx.md
```

### Step 5: 后续交互

推荐完成后，询问用户：

```
需要我进一步帮你：
1. 📖 深入解读这篇论文？
2. 🔍 查找相关论文？
3. 🛠️ 分析代码实现？
4. 📋 生成论文阅读笔记模板？
```

## 报告结构

生成的 Markdown 报告包含：

1. **基本信息表** - arXiv ID、发布日期、作者、链接
2. **摘要** - 论文摘要（截取前 600 字）
3. **推荐理由**：
   - 解决了什么问题
   - 使用了什么方法
   - 工程实践建议
   - 代码质量评估
4. **1分钟速览** - 快速理解论文核心
5. **快速链接** - PDF、GitHub、arXiv

## 质量控制

### 论文筛选标准

- ✅ 必须有 GitHub 代码链接
- ✅ 发表时间在最近 6 个月内
- ✅ GitHub 仓库存在且公开
- ✅ 自动分析摘要提取关键信息

### 避免

- ❌ 纯理论无代码的论文
- ❌ GitHub 仓库已删除或私有

## 记忆功能

记录用户已推荐的论文，避免重复：

```json
// 保存到 ~/papers/history.json
{
  "recommended": [
    {
      "arxiv_id": "2403.12345",
      "title": "论文标题",
      "date": "2026-03-15",
      "topic": "Agent架构"
    }
  ]
}
```

每次推荐前自动检查历史记录。

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `search.py` | arXiv 搜索 + GitHub 链接提取 + 仓库验证 |
| `analyze.py` | 论文摘要智能分析，提取问题/方法/结论 |
| `recommend.py` | 完整推荐流程，生成报告 |

## 依赖

- Python 3.8+
- arXiv API（免费，无需密钥）
- GitHub API（公开接口）
- 网络访问

## 示例用法

**用户**：推荐一篇 Agent 论文

**执行**：
```bash
python3 recommend.py agent-eval
```

**输出**：
```
📄 推荐论文：Video Streaming Thinking: VideoLLMs Can Watch and Think Simultaneously
🎯 主题：Agent测评
📅 发布：2026-03-12
⭐ GitHub：53 stars
...
```

---

*技能版本：1.0 | 创建时间：2026-03-15*
