# 碎片知识缝纫师 (Fragment Stitcher)

让散落的碎片信息，自动编织成体系化知识。

## 简介

碎片知识缝纫师是一个智能的知识管理工具，帮助你将散落在微信、网页、文档、会议记录中的碎片信息进行体系化整理。它不仅仅是"收藏"或"摘录"，更重要的是提供"自动关联+深度重组"能力，让你的知识碎片逐步形成完整的知识体系。

## 核心功能

### 1. 智能收集 🧩

一键捕获任意选中的文本/截图，自动提取核心信息：

- **多种输入方式**
  - 直接粘贴文本（文章片段、聊天金句、临时想法）
  - 上传截图（自动 OCR 提取文字）
  - 提供文件路径（读取文档内容）
  - 提供 URL（抓取网页内容）

- **自动提取**
  - 核心观点和关键信息
  - 来源标识（网页/微信/文档/会议）
  - 主题标签
  - 创建时间

- **结构化存储**
  - 自动分析文本，提取关键概念
  - 识别重要句子和主要观点
  - 生成摘要

### 2. 关系发现 🔗

分析新内容与已有知识库的关联：

| 关联类型 | 检测方式 | 示例 |
|---------|---------|------|
| 概念相似 | 关键词重叠、语义相似 | "AI安全"与"模型对齐" |
| 话题相关 | 同一主题域 | 多篇关于"产品增长"的笔记 |
| 逻辑延续 | 前后文的承接关系 | 需求文档→技术方案→实现记录 |
| 补充增强 | 同一问题的不同角度 | 正面案例+反面案例 |

### 3. 自动缝合 🧵

生成"知识连接笔记"，将相关碎片自动缝合：

```
📌 连接发现
来源: [新碎片]
关联: [已有知识]
关联点: [具体说明]
```

**典型输出示例**：

- "您今天读的 AI 安全文章，与上周保存的'模型对齐'论文在第三章有共同假设"
- "这条产品笔记，可以补充到您正在写的 PRD 文档的'风险章节'"

### 4. 渐进式成文 ✍️

当某个主题的碎片积累到一定量，自动生成大纲草案：

- **主题大纲**: 基于碎片自动生成结构化大纲
- **PRD 草案**: 针对产品相关碎片生成 PRD 文档草案
- **技术文档**: 针对技术相关碎片生成技术文档结构
- **周报摘要**: 每周自动生成知识总结

## 快速开始

### 前提条件

- Python 3.7+
- WorkBuddy 环境

### 安装

将 `fragment-stitcher` 目录安装到你的 WorkBuddy skills 目录：

```bash
# 用户级安装
cp -r fragment-stitcher ~/.workbuddy/skills/

# 项目级安装
cp -r fragment-stitcher .workbuddy/skills/
```

## 使用示例

### 场景 1: 收集碎片

```
用户: 帮我收集这段文字："大模型的安全性是一个重要议题，需要对齐模型价值观。"

Skill:
  ✅ 已收集碎片
  ID: frag_abc123
  核心观点: 需要对齐模型价值观
  关键概念: 大模型, 安全性, 模型对齐
  标签: AI, 安全
  已保存到知识库
```

### 场景 2: 发现关联

```
用户: 我刚保存了一篇关于 AI 安全的文章

Skill:
  📌 连接发现
  来源: 网页阅读
  时间: 2026-03-20 17:00

  💡 概念关联
  与「frag_model_alignment...」共享概念: 模型对齐
  这两篇内容都涉及到 模型对齐 相关的话题

  📚 话题相关
  与「frag_ai_safety...」同属 AI 安全 话题
  可以将这些碎片归类到 AI 安全 的知识体系下
```

### 场景 3: 自动缝合

```
用户: 帮我把这条产品笔记和相关的知识缝合起来

Skill:
  📋 PRD 补充建议

  ✅ 需求相关:
     来源: 用户访谈
     内容: 用户希望能够快速找到相关产品，推荐算法需要优化...

  ⚠️  风险相关:
     来源: 竞品分析
     内容: 竞品在个性化推荐方面存在隐私问题...

  🧧 技术方案参考:
     来源: 技术调研
     内容: 协同过滤和深度学习结合可以提升推荐效果...
```

### 场景 4: 生成大纲

```
用户: 帮我生成关于"AI 安全"主题的大纲

Skill:
  主题: AI 安全
  碎片数: 5

  大纲结构:
  {
    "title": "AI 安全：模型对齐、内容过滤相关内容整理",
    "abstract": "大模型的安全性是一个重要议题 模型对齐技术包括多种方法...",
    "sections": [
      {
        "title": "一、概述",
        "subsections": [
          {
            "title": "1.1 背景与动机",
            "fragments": ["frag_001", "frag_002"]
          }
        ]
      },
      ...
    ]
  }
```

## 技术架构

### 核心模块

```
fragment-stitcher/
├── SKILL.md                 # Skill 核心定义
├── README.md                # 使用文档
└── scripts/                 # 分析脚本
    ├── collector.py           # 智能收集器
    ├── relationship_finder.py  # 关系发现器
    ├── stitcher.py           # 自动缝纫师
    └── draft_generator.py     # 大纲生成器
```

### 数据流

1. **收集阶段**: 接收碎片 → 提取信息 → 结构化存储
2. **关联发现**: 分析内容 → 匹配知识库 → 发现关系
3. **自动缝合**: 理解关系 → 生成连接笔记
4. **成文阶段**: 统计碎片 → 分析主题 → 生成大纲

### 核心技术

- **文本分析**: 正则表达式提取关键概念和句子
- **关系发现**: Jaccard 相似度、关键词匹配、逻辑链识别
- **知识图谱**: 构建碎片间的关系网络
- **自动生成**: 基于模板的结构化大纲生成

## API 参考

### collector.py

```python
from scripts.collector import FragmentCollector

# 初始化收集器
collector = FragmentCollector('path/to/knowledge_base')

# 从文本收集
fragment = collector.collect_from_text(
    text="大模型的安全性是一个重要议题",
    source="微信文章",
    tags=["AI", "安全"]
)

# 从文件收集
fragment = collector.collect_from_file('/path/to/file.txt')

# 搜索碎片
results = collector.search_fragments("模型对齐", limit=10)

# 保存知识库
collector.save_fragments()
```

### relationship_finder.py

```python
from scripts.relationship_finder import RelationshipFinder

# 初始化关系发现器
finder = RelationshipFinder(knowledge_base)

# 发现关系
relationships = finder.find_relationships(new_fragment, top_k=5)

# 构建关系图谱
graph = finder.build_relationship_graph()

# 发现话题聚类
clusters = finder.find_topic_clusters(min_cluster_size=3)
```

### stitcher.py

```python
from scripts.stitcher import FragmentStitcher

# 初始化缝纫师
stitcher = FragmentStitcher(knowledge_base)

# 生成缝合笔记
note = stitcher.generate_stitch_note(new_fragment, relationships)

# 生成 PRD 补充说明
prd_note = stitcher.generate_prd_supplement_note(
    fragment, related_fragments
)

# 生成每周摘要
digest = stitcher.generate_weekly_digest(
    weekly_fragments, relationship_finder
)
```

### draft_generator.py

```python
from scripts.draft_generator import DraftGenerator

# 初始化生成器
generator = DraftGenerator(knowledge_base)

# 生成主题大纲
outline = generator.generate_outline(
    topic="AI 安全",
    min_fragments=5
)

# 生成 PRD 草案
prd = generator.generate_prd_draft("用户增长")

# 生成 Markdown 格式
markdown = generator.generate_markdown(outline)
```

## 最佳实践

### 1. 持续收集

- 养成习惯，每天定期收集碎片
- 使用清晰的标签（如：技术、产品、设计）
- 添加来源信息，便于追溯

### 2. 主动关联

- 定期查看"连接发现"笔记
- 根据关联提示补充相关知识
- 主动寻找相关碎片，扩大知识网络

### 3. 渐进式写作

- 当碎片积累到 5 个以上时，生成大纲
- 根据大纲补充缺失的碎片
- 循环迭代，不断完善知识体系

### 4. 定期回顾

- 每周查看"每周知识摘要"
- 定期整理过时的碎片
- 合并重复或相似的内容

## 扩展性

### 支持新的输入源

在 `collector.py` 中添加新的输入方法：

```python
def collect_from_wechat(self, message_id: str) -> Dict:
    """从微信消息收集"""
    # 实现微信 API 集成
    pass
```

### 自定义关系类型

在 `relationship_finder.py` 中添加新的关系检测逻辑：

```python
def _check_custom_relationship(self, frag1, frag2):
    """自定义关系检测"""
    # 实现你的关系判断逻辑
    pass
```

### 自定义大纲模板

在 `draft_generator.py` 中添加新的大纲模板：

```python
def _build_custom_outline(self, fragments, analysis):
    """自定义大纲结构"""
    # 实现你的大纲模板
    pass
```

## 常见问题

### Q: 如何导入已有的笔记？

A: 可以通过脚本批量导入：

```python
collector = FragmentCollector('path/to/knowledge_base')

# 从文件导入
with open('my_notes.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    fragment = collector.collect_from_text(
        text=content,
        source="批量导入",
        tags=["导入"]
    )

collector.save_fragments()
```

### Q: 如何导出知识库？

A: 知识库存储为 JSON 格式，可以直接复制或使用脚本导出：

```bash
# 知识库默认位置
~/.workbuddy/knowledge_base/fragments.json

# 或自定义路径
cp /path/to/your/knowledge_base/fragments.json ./backup.json
```

### Q: 碎片太多会影响性能吗？

A: 不会。Skill 使用高效的索引和搜索算法，即使数千个碎片也能快速响应。但如果碎片数量超过 10,000，建议定期归档旧内容。

## 未来规划

- [ ] 集成 AI 模型提升语义理解
- [ ] 支持图片碎片（图片识别和标签）
- [ ] 支持语音碎片（语音转文字）
- [ ] 可视化知识图谱
- [ ] 与 Notion、Obsidian 等工具集成
- [ ] 多人协作知识库

## 贡献指南

欢迎贡献代码、报告问题或提出改进建议！

### 开发环境

```bash
# 克隆仓库
git clone https://github.com/your-org/fragment-stitcher.git

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖（如有）
pip install -r requirements.txt
```

### 运行测试

```bash
# 运行脚本示例
python scripts/collector.py
python scripts/relationship_finder.py
python scripts/stitcher.py
python scripts/draft_generator.py
```

## 许可证

MIT License

## 致谢

灵感来源于每个被碎片信息困扰的知识工作者。我们相信，真正的价值不在于收集，而在于连接和重组。

---

让知识碎片，编织成智慧 🧵
