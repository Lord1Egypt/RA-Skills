---
name: arxiv-paper-with-diagram
description: 解读arXiv论文并生成结构图。将论文翻译为中文的同时，自动生成论文对应的模型架构图、流程图、数据流程图等可视化图表。触发词：arxiv画图、论文结构图、生成论文图表、paper with diagram、论文配图。
---

# arxiv-paper-with-diagram

将arXiv论文解读为中文内容，并生成对应的结构图。

## 流程图

```
[用户输入arXiv URL/ID]
        │
        ▼
┌─────────────────────────┐
│ Step 1: 解析输入         │
│ 识别URL格式，提取arXiv ID │
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│ Step 2: 获取论文信息     │
│ Crossref API / arXiv API │
│ 网页抓取 / 网络搜索      │
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│ Step 3: 内容翻译         │
│ 学术标准术语对照         │
│ 保留公式与变量名英文     │
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│ Step 4: 生成结构图        │
│ 分析论文类型             │
│ 选择Diagram类型          │
│ 调用Archify渲染器        │
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│ Step 5: 输出结果         │
│ 中文内容 + HTML图表文件  │
└─────────────────────────┘
```

## 工作流程详解

### Step 1: 解析输入

识别用户提供的 arXiv URL 或 ID：
- URL格式：`https://arxiv.org/abs/XXXX.XXXXX` → 提取 ID：`XXXX.XXXXX`
- 短URL：`https://arxiv.org/pdf/XXXX.XXXXX`
- 纯ID：`XXXX.XXXXX`

### Step 2: 获取论文信息

按优先级尝试以下方式获取论文内容：

**优先方案 A（Crossref API）**：
```bash
curl -s "https://api.crossref.org/works/https://doi.org/10.48550/arXiv.XXXXXXX" -H "User-Agent: Mozilla/5.0"
```

**方案 B（arXiv API）**：
```bash
curl -s "http://export.arxiv.org/api/query?id_list=XXXXXXX" -H "User-Agent: Mozilla/5.0"
```

**方案 C（网页抓取）**：
- `https://arxiv.org/abs/XXXXXXX` → 摘要
- `https://arxiv.org/html/XXXXXXX` → 全文HTML
- `https://arxiv.org/pdf/XXXXXXX` → PDF

**方案 D（网络搜索）**：
```bash
tavily_search query="title of the paper"
tavily_extract urls=["https://arxiv.org/abs/XXXXXXX"]
```

### Step 3: 内容翻译

将英文论文翻译为中文，遵循学术标准：
- 保留专业术语英文原词
- 公式和变量名保留英文
- 人名按约定翻译或保留英文

### Step 4: 生成结构图

根据论文内容选择最合适的 Diagram 类型：

| 论文类型 | Diagram 类型 | 说明 |
|---------|-------------|------|
| 模型架构类（如YOLO、ResNet等） | `architecture` | 系统组件、模型结构、资源连接 |
| 方法流程类（如训练流程、检测Pipeline） | `workflow` | 技术流程、步骤顺序、决策分支 |
| 数据流动类（如ETL、数据处理管道） | `dataflow` | 数据流转、多阶段处理 |
| 状态机类（如训练阶段、生命周期） | `lifecycle` | 状态转换、终端状态 |
| 交互时序类（如Agent协作、API调用） | `sequence` | 时序交互、多方调用链 |

**调用 Archify 渲染器**（从 Archify 技能目录）：
```bash
cd /root/.openclaw/workspace/skills/archify
node renderers/<type>/render-<type>.mjs <input>.json <output>.html
```

### Step 5: 输出结果

交付两个文件：
1. **论文中文内容**（结构化 Markdown）
2. **HTML 结构图**（可交互、可导出 PNG/SVG）

## 参考资料

- Archify 渲染器详细用法：[references/archify-guide.md](references/archify-guide.md)
- arXiv 获取工具链：[references/arxiv-guide.md](references/arxiv-guide.md)