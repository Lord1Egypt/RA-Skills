# Gaokao-Calculus Bridge Skill

🎓 **高考-高数衔接智慧课程 Skill**

桥接2026高考数学改革与高等数学教育，培养真实世界问题解决能力。

## 核心功能

| 功能 | 描述 | 对应Workflow |
|------|------|-------------|
| 改革要点解析 | 分析2026高考数学改革核心要求 | Workflow 1 |
| 情境化题目生成 | 生成真实世界背景的数学问题 | Workflow 2 |
| 长题干解析 | 信息提取与建模指导 | Workflow 3 |
| 概念映射 | 高中→大学知识衔接 | Workflow 4 |
| 项目式学习 | 完整PBL项目设计 | Workflow 5 |
| 学习路径推荐 | 个性化学习方案 | Workflow 6 |

## 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 使用示例

**生成情境化题目：**
```bash
python3 scripts/problem_generator.py --domain ai --difficulty bridge
```

**概念映射：**
```bash
python3 scripts/concept_mapper.py --from 导数 --to 微分学
```

**长题干解析：**
```bash
python3 scripts/model_extractor.py --text "你的题目文本"
```

**学习路径规划：**
```bash
python3 scripts/learning_path_advisor.py --goal bridge --duration 12周
```

## 文件结构

```
gaokao-calculus-bridge/
├── SKILL.md                      # Skill主文件
├── hermes.config.yaml            # OpenClaw配置
├── requirements.txt              # Python依赖
├── scripts/                      # 可执行脚本
│   ├── problem_generator.py      # 题目生成器
│   ├── concept_mapper.py         # 概念映射器
│   ├── model_extractor.py        # 题目解析器
│   └── learning_path_advisor.py  # 路径推荐器
├── references/                   # 参考文档
│   ├── gaokao_2026_reform.md     # 高考改革要点
│   ├── real_world_cases.md       # 真实案例库
│   └── modeling_templates.md     # 建模模板
├── templates/                    # 模板文件
│   └── project_guide.md          # PBL项目指南
└── assets/                       # 资源文件
    └── demo_problems/            # 示例题目
```

## 与OpenClaw集成

本Skill设计为OpenClaw/ClawHub生态系统的一部分，可与以下Skill协同：

- `calculus-concept-visualizer`: 概念可视化
- `derivation-animation-skill`: 推导动画
- `error-analysis-skill`: 错题分析
- `calculus-resource-harvester`: 资源采集

## 作者

**daigx@ok**

## 许可证

MIT License
