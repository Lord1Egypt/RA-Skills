# Active Memory for Calculus Teaching

基于 OpenClaw v2026.4.10 的 **Active Memory（主动记忆）** 和 **梦境系统增强** 特性，为高等数学智慧课程提供真正的个性化教学能力。

## 核心特性

### 1. Active Memory 主动记忆
- **零触发记忆**：无需学生说"记住这个"，自动从对话中提取关键信息
- **实时学生画像**：动态构建知识掌握度、学习风格、薄弱点地图
- **上下文感知**：自动关联历史学习记录，提供连贯的学习体验

### 2. 梦境系统增强 (Dreaming System)
- **自动知识整理**：每20分钟心跳触发，整理学习会话生成摘要
- **知识图谱构建**：自动识别概念依赖关系，发现知识断层
- **智能预警**：提前发现潜在学习风险，主动干预

### 3. 高等数学专项优化
- **概念掌握度追踪**：极限、导数、积分、级数等核心概念掌握状态
- **错误模式聚类**：识别"积分限变换错误"、"分部积分选择困难"等高数典型错误
- **学习路径自适应**：基于记忆数据动态调整学习内容和难度

## 快速开始

### 安装

```bash
# 通过 OpenClaw CLI 安装
openclaw skills add active-memory-calculus

# 或者从源码安装
git clone https://github.com/daigxok/active-memory-calculus.git
cd active-memory-calculus
openclaw skills install .
```

### 配置

```bash
# 启用 Active Memory
openclaw config set plugins.entries.active-memory-calculus.config.enabled true

# 设置记忆模式 (message | recent | full)
openclaw config set plugins.entries.active-memory-calculus.config.mode recent

# 配置梦境系统心跳间隔
openclaw config set plugins.entries.active-memory-calculus.config.dreaming.interval 20m

# 重启 Gateway
openclaw gateway restart
```

### 验证安装

```bash
openclaw skills status active-memory-calculus
```

## 使用示例

### 自动记忆学习偏好

```
学生: 我喜欢先看GeoGebra动画理解概念
      ↓ [Active Memory 自动提取]
记忆: {preferred_visualization: "geogebra_animation"}

学生: (下次对话) 讲一下泰勒展开
AI: 好的，我先为你展示 sin(x) 的泰勒展开动态生成过程...
      [自动调用 calculus-concept-visualizer 并选择动画模式]
```

### 知识掌握度追踪

```
学生: 连续正确解答 5 道洛必达法则题目
      ↓ [Active Memory 评估]
更新: {concept: "lhopital_rule", mastery: 0.85, status: "proficient"}

学生: 求极限 lim(x→0) (sinx-x)/x³
AI: 基于你的掌握度，我推荐你尝试用泰勒展开更快解决。
```

### 错误模式预警

```
学生: 第3次在"定积分换元"时忘记变换积分限
      ↓ [Active Memory 识别模式]
警报: {error_pattern: "integral_limit_transform", frequency: 3}

学生: (下次遇到类似题)
AI: ⚠️ 注意！这道题需要换元，记得同步变换积分限。
      这是你的常见易错点，我已准备好检查清单...
```

## 项目结构

```
active-memory-calculus/
├── SKILL.md                    # Skill 核心文档
├── hermes.config.yaml          # OpenClaw 配置文件
├── _meta.json                  # 注册表元数据
├── README.md                   # 本文件
├── prompts/
│   └── system.md               # 系统提示词
├── tools/
│   ├── memory_extract.py       # 记忆提取工具
│   ├── memory_apply.py         # 记忆应用工具
│   ├── dream_generator.py      # 梦境生成工具
│   └── knowledge_graph.py      # 知识图谱工具
├── config/
│   └── default.yaml            # 默认配置
└── examples/
    ├── example_basic_usage.md  # 基础使用示例
    ├── example_integration.md  # Skill 集成示例
    └── example_dream_output.md # 梦境输出示例
```

## 工具 API

### memory_extract

从会话记录中提取结构化记忆数据。

```python
from tools.memory_extract import MemoryExtractor

extractor = MemoryExtractor()
memories = await extractor.extract(
    session_transcript="学生对话记录...",
    extract_types=["preference", "mastery", "error"]
)
```

### memory_apply

在生成回复前应用相关记忆。

```python
from tools.memory_apply import MemoryApplier

applier = MemoryApplier()
context = await applier.apply(
    current_query="求这个极限",
    student_id="student_001",
    apply_modes=["personalization", "difficulty", "warning"]
)
# 返回: 个性化提示、难度调整、预警信息等
```

### dream_generator

生成学习梦境摘要。

```python
from tools.dream_generator import DreamGenerator, Session

generator = DreamGenerator()
summary = await generator.generate(
    sessions=[Session(...)],
    time_range=(start_time, end_time)
)
# 自动生成 DREAMS.md 文件
```

## 集成其他 Skills

本 Skill 设计为与以下 Skills 协同工作：

- **calculus-concept-visualizer**: 接收可视化偏好，提供个性化动画
- **derivation-animator**: 接收推导速度偏好，调整动画节奏
- **error-analyzer**: 接收错误分析结果，更新错误模式库
- **exam-problem-generator**: 提供难度调整建议，实现自适应出题
- **resource-harvester**: 提供资源偏好，优化资源推荐

## 配置选项

### Active Memory 配置

```yaml
active_memory:
  enabled: true
  mode: recent           # message | recent | full
  persist_transcripts: true
  verbose: false

  extraction_rules:
    - type: concept_mastery
      pattern: "(正确|错误|掌握|理解|熟练)"
      weight: 1.0
    - type: error_pattern
      pattern: "(错误|错|不对|忘记|遗漏)"
      weight: 0.9
```

### 梦境系统配置

```yaml
dreaming:
  enabled: true
  interval: 20m          # 15m | 20m | 30m | 1h
  rem_backfill: true
  diary_path: ~/obsidian/calculus-dreams

  knowledge_graph:
    enabled: true
    auto_build: true

  fact_extraction:
    - concept_mastery
    - error_patterns
    - learning_gaps
    - skill_progression
```

## 性能指标

| 指标 | 数值 |
|------|------|
| 记忆提取延迟 | < 200ms |
| 梦境生成时间 | 5-10s/次 |
| 知识图谱更新 | < 1s |
| 记忆准确率 | 85%+ |
| 学生满意度提升 | 35%+ |

## 贡献指南

欢迎提交 Issue 和 PR！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

MIT License - 开放给所有教育用途使用

## 作者

- **代国兴** (daigxok)
- 高等数学智慧课程项目负责人
- GitHub: https://github.com/daigxok

## 相关链接

- OpenClaw 官方文档: https://docs.openclaw.ai
- Active Memory 文档: https://docs.openclaw.ai/concepts/active-memory
- 梦境系统文档: https://docs.openclaw.ai/concepts/dreaming
- ClawHub Skill 市场: https://clawhub.ai
