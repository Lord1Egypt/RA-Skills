---
name: fusion-workflow-hub
description: >
  融合 Graphify 知识图谱 + Everything Claude Code (ECC) 工作流 + OpenClaw 的超级效率中心。
  
  Use when: 用户想要快速理解代码库结构、执行规划/审查/TDD 等标准化工作流、结合知识图谱进行深度代码分析、一站式解决复杂编程任务，或整合多个工具能力提升效率。
  
  NOT for: 简单的单文件编辑、纯文本问答、不涉及代码分析的通用问题。
---

# Fusion Workflow Hub - 融合工作流中心

## 核心定位

本技能整合三大 AI 开发工具的能力，形成完整的智能编码工作流：

| 工具 | 核心能力 | Token 节省 |
|------|----------|------------|
| **Graphify** | 代码知识图谱构建与查询 | 71.5x |
| **ECC** | 68 命令、36 Agent、151 Skill | - |
| **OpenClaw** | 平台集成规则与自动化 | - |

## 工作流程

### 工作流一：代码库深度分析

```
1. 使用 Graphify 构建知识图谱
   python -m graphify <目录路径>
   
2. 读取图谱报告
   graphify-out/GRAPH_REPORT.md
   
3. 查询具体问题
   python -m graphify query "<问题>"
   
4. 追踪概念路径
   python -m graphify path "<概念A>" "<概念B>"
   
5. 交互探索（可选）
   打开 graphify-out/graph.html
```

### 工作流二：功能开发（TDD）

```
1. 使用 tdd-workflow 规划
   use_skill tdd-workflow
   
2. 增量实现代码
   
3. 代码审查
   use_skill code-review
   
4. 增量更新图谱
   python -m graphify . --update
```

### 工作流三：持续学习优化

```
1. 经验积累
   use_skill continuous-learning-v2
   
2. 上下文压缩
   use_skill strategic-compact
   
3. 代码复盘
   use_skill code-review
```

## 工具命令速查

### Graphify 命令

```bash
# 构建知识图谱
python -m graphify <目录>

# 增量更新
python -m graphify <目录> --update

# 查询
python -m graphify query "<问题>"

# 路径追踪
python -m graphify path "<A>" "<B>"
```

### ECC 推荐命令

```bash
# 代码审查
/use code-review

# TDD 工作流
/use tdd-workflow

# 持续学习
/use continuous-learning-v2

# 战略压缩
/use strategic-compact
```

## 输出产物

```
graphify-out/
├── graph.html        # 交互式可视化图谱
├── GRAPH_REPORT.md   # 高层摘要（God Nodes、建议问题）
├── graph.json        # 持久化图谱数据
└── cache/           # SHA256 缓存
```

## 前置要求

- Python 3.8+
- Graphify: `pip install graphifyy`
- 文档支持: `pip install python-docx openpyxl pillow`

## 集成文件

本技能包包含：
- `SKILL.md` - 本说明文件
- `references/graphify-commands.md` - Graphify 命令参考
- `references/ecc-best-practices.md` - ECC 最佳实践

## 使用示例

**用户**: "帮我分析这个代码库的结构"

**AI 执行**:
1. 调用 Graphify 构建图谱
2. 读取 GRAPH_REPORT.md 理解架构
3. 使用 query 查询关键模块
4. 汇总分析结果

---

*本技能包整合了 Graphify (15.8k stars)、Everything Claude Code (50k+ stars) 和 OpenClaw 平台能力*
