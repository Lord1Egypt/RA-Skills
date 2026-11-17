# 箱熵（Entropy Box）具身智能全景图与知识编译器

> 一个面向机器人与具身智能研发的 Agent 原生知识编译器与能力基座。把边界明确的技术需求转化为候选实现方法与有依据的工程工作流。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![语言](https://img.shields.io/badge/lang-zh--CN-green.svg)](SKILL.md)
[![Skill](https://img.shields.io/badge/WorkBuddy-ClawHub-orange.svg)](https://clawhub.ai/)

## 这个 Skill 能做什么

箱熵（Entropy Box）把分散在论文、代码仓库、ROS 软件包、模型、数据集、仿真器、基准、标准与工程文档中的具身智能知识，编译为持久化、类型化、可机器使用的知识产物，并通过四个运行时能力对外提供服务：

- **Consult（方案咨询）**：把"某个具身智能任务该怎么做"拆成候选实现方法、涉及的能力、依赖、资产、约束与缺口，组装成有依据的研发路径。
- **Search（具体问题检索）**：针对具体问题做 RAG 检索，深入了解已经选中的技术。
- **Lookup（实体锚定）**：把已知 ID、名称或别名解析为结构化主题 / 能力 / 资产档案。
- **Evidence（证据核验）**：查找带来源的技术对比、限制、工程记录与基准背景。

公开全景图覆盖 **15 个顶层领域、2,511 个垂直主题库、7,000+ 条任务链与 6 万+ 依赖边**，支持全景定位、能力依赖分析、资产选型与知识缺口分析。

## 安装

### 方式一：ClawHub（推荐）

1. 打开 https://clawhub.ai/ ，用 GitHub 账号登录。
2. 点击「发布技能 / 导入」，选择本仓库 `chenli-yy/entropy-box-zh`，或搜索 `entropy-box-zh` 一键安装。

### 方式二：手动安装

```bash
git clone https://github.com/chenli-yy/entropy-box-zh ~/.workbuddy/skills/entropy-box-zh
```

重启 WorkBuddy 或执行 `/reload-skills` 后，WorkBuddy 会根据 SKILL.md 的触发词自动加载本技能。

## 目录结构

```
entropy-box-zh/
├── SKILL.md                      # 技能定义与运行时工作流（核心）
├── README.md                     # 本文件
└── references/
    ├── api.md                    # /api/consult 等接口说明
    ├── knowledge-compiler.md     # 知识编译器原理
    └── panorama.md               # 15 个顶层领域全景说明
```

## 使用场景

- 需要回答"某个具身智能任务该怎么做"，并得到候选方法、能力、依赖、资产、约束与缺口；
- 做领域全景梳理、能力版图分析、任务链拆解或研发工作流组装；
- 已形成技术选型，需要进一步用 Search / Lookup / Evidence 深入了解、锚定实体或核验依据。

## 安全与边界

- 箱熵不直接授权代码部署、采购或物理机器人控制；涉及物理系统须经专业人员审查与受控测试。
- 向公开 API 发送项目上下文前，先剔除凭证与敏感细节；含专有 / 个人信息须先取得明确同意。

## 相关链接

- 项目网站：https://xiangshang.ngrok.app/
- 公开文档：https://chenli-yy.github.io/entropy-box-public/
- 集成说明：https://chenli-yy.github.io/entropy-box-public/integrate/
- 在线 API Schema：https://xiangshang.ngrok.app/openapi.json
- 归档与引用：https://doi.org/10.5281/zenodo.21712178

## 许可

MIT © 王玉琪（Yuqi Wang）
