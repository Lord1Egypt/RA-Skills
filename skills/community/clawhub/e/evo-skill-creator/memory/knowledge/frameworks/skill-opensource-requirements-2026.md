# Skill / 自我进化智能体项目开源要求（2026）

> 来源：Web 搜索 + 已有知识（#43 Frontmatter、#46 Skill 分发）综合
> 学习时间：2026-04-05（深度学习）
> 类别：frameworks / open-source / distribution
> 波动性：low（开源标准已成熟，Skill 标准在演进但核心稳定）
> 置信度：high（多方实践验证）

## 一、通用开源项目要求（仓库级）

### 必需文件

| 文件 | 用途 | 我们现状 |
|------|------|---------|
| `README.md` | 项目说明、安装、使用 | ✅ 有，但内容偏简 |
| `LICENSE` | 法律许可声明 | ❌ **缺失** |
| `CONTRIBUTING.md` | 贡献指南（PR流程、代码规范） | ❌ **缺失** |
| `CODE_OF_CONDUCT.md` | 行为准则 | ❌ **缺失** |
| `.gitignore` | 排除敏感/运行时文件 | ✅ 有 |

### 推荐文件

| 文件 | 用途 | 优先级 |
|------|------|--------|
| `SECURITY.md` | 安全策略、漏洞报告方式 | 高（有状态智能体需要） |
| `CHANGELOG.md` | 版本变更记录 | 中 |
| Issue/PR 模板 | 标准化反馈流程 | 中 |
| `docs/` | 深度文档 | 已有 |

### LICENSE 选择建议

| 许可证 | 特点 | 适用场景 |
|--------|------|---------|
| **MIT** | 极度宽松，几乎无限制 | 最大化采用率 |
| **Apache 2.0** | 宽松 + 专利保护 + 贡献者协议 | 企业友好，推荐 |
| **GPL-3.0** | 强 copyleft，修改必须开源 | 保护开源生态 |

**建议**：Apache 2.0 — 平衡开放性和保护性，企业可用，且有专利条款。

## 二、Skill 特有开源要求

### SKILL.md 规范

每个 skill 的 SKILL.md 必须包含 YAML frontmatter：

```yaml
---
name: skill-name
description: >
  一句话描述 + 触发条件列表。
  最大 1024 字符。
license: Apache-2.0
compatibility: macOS/Linux, Claude Code CLI
metadata:
  version: "1.0.0"
  author: "evo-skill-creator"
  type: self-evolving-agent
  tags: ["self-evolving", "domain-tag"]
---
```

### Skills.sh 生态兼容

发布到 skills.sh 的要求：
1. 公开 GitHub 仓库
2. 每个 skill 一个目录，内含 `SKILL.md`
3. 用户通过 `npx skills add <user>/<repo>` 安装
4. 支持单独安装某个 skill：`npx skills add <user>/<repo>/<skill-name>`

### 目录结构标准

```
my-skills-repo/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── skill-name-1/
│   ├── SKILL.md
│   ├── references/
│   └── ...
├── skill-name-2/
│   └── SKILL.md
└── ...
```

## 三、有状态自我进化智能体的特殊要求

这是我们与普通工具 Skill 的最大差异。普通 Skill 是无状态的，我们的智能体有 memory/、output/、private/ 等持久化数据。

### 3.1 隐私与数据脱敏（最关键）

#### 必须排除的内容

| 类别 | 具体内容 | 处理方式 |
|------|---------|---------|
| **个人数据** | `memory/private/` 下所有文件 | .gitignore 排除 |
| **运行产出** | `output/` 下所有文件 | .gitignore 排除 |
| **个人路径** | SKILL.md 中的 `/Users/xxx/` 绝对路径 | 替换为相对路径或模板变量 |
| **个人配置** | scheduler/configs/*.yaml（含个人路径和调度偏好） | .gitignore 排除，提供 example.yaml |
| **API 密钥** | .env、credentials 等 | .gitignore 排除 |
| **用户偏好** | preferences.md（老板的个人习惯） | 在 private/ 下，已排除 |

#### 必须提供的模板

当用户首次安装 skill 时，需要自动初始化个人数据目录。有两种方式：

**方式 A（推荐）：初始化模板文件**
```
memory/private/README.md          → 说明各文件用途
memory/private/backlog.md.template → 待办模板
memory/private/evolution-log.md.template → 进化记录模板
```
首次运行时复制 `.template` 为实际文件。

**方式 B：SKILL.md 中写明首次运行自动创建逻辑**

### 3.2 SKILL.md 中的路径处理

**问题**：我们当前的 SKILL.md 中「数据目录」段硬编码了绝对路径。

**解决方案**：
- SKILL.md 中使用相对路径（相对于 skill 安装目录）
- 或使用 `$SKILL_DIR` 占位符
- 安装时由安装脚本解析为实际路径

### 3.3 知识库（memory/knowledge/）的开源策略

知识库是我们的核心价值之一，需要决策：

| 策略 | 优点 | 缺点 |
|------|------|------|
| **完全开源** | 用户开箱即有丰富知识 | 知识量大，安装包重 |
| **精选开源** | 只放核心知识，保持轻量 | 用户需要自己 learn |
| **独立仓库** | 知识和框架分离管理 | 增加管理复杂度 |

**建议**：精选开源——只保留 `references/evo-agent-model.md` 等框架核心文件，knowledge/ 目录留空让用户自己 learn 填充。

### 3.4 安全声明（SECURITY.md）

对于有状态智能体，必须声明：
1. 本项目存储哪些数据（memory/ 目录结构说明）
2. 哪些数据是私有的（private/ 目录）
3. 数据存储位置（本地文件系统）
4. 不会上传任何数据到外部服务（除 LLM API 调用外）
5. 如何清除所有个人数据

## 四、evo-skills 仓库的特殊考虑

### scheduler 服务

scheduler 是基础设施代码，开源时需要注意：
- `configs/*.yaml` 全部排除（已做），只保留 `example.yaml`
- `logs/` 和 `state.json` 排除（已做）
- `install.sh`/`uninstall.sh` 要适配不同平台
- 路径不能硬编码

### 多 skill 仓库结构

当前结构 `skills/evo-skill-creator/` 放在仓库内。需要决策：
- 是整个 `evo-skills/` 一起开源？（仓库 = scheduler + skills）
- 还是 skills 独立仓库？

**建议**：一起开源。scheduler 是生态的核心基础设施，skills 是实例。分开会增加理解成本。

## 五、开源前检查清单

### Phase 1：代码脱敏

- [ ] 移除所有硬编码绝对路径（SKILL.md、脚本中的 `/Users/xxx/`）
- [ ] 确认 .gitignore 覆盖所有私有数据（memory/private/、output/、configs/*.yaml）
- [ ] 搜索代码中是否有 API key、token、密码等
- [ ] 搜索是否有公司内部 URL 或内网地址
- [ ] Git history 中是否有敏感数据（可能需要 git filter-branch 或 BFG）

### Phase 2：标准文件补充

- [ ] LICENSE 文件（建议 Apache 2.0）
- [ ] CONTRIBUTING.md（贡献指南）
- [ ] CODE_OF_CONDUCT.md（行为准则）
- [ ] SECURITY.md（安全策略）
- [ ] README.md 升级（英文版本、安装指南、使用示例）

### Phase 3：Skill 标准化

- [ ] 所有 SKILL.md 添加 YAML frontmatter
- [ ] SKILL.md 中路径改为相对路径或模板变量
- [ ] 提供 memory/private/ 下的模板文件（.template 后缀）
- [ ] knowledge/ 目录策略决定（完全开源 or 精选）

### Phase 4：文档完善

- [ ] README.md 英文化（或中英双语）
- [ ] 架构说明文档
- [ ] 如何创建自己的 self-evolving skill 教程
- [ ] 如何安装和使用 scheduler 教程

### Phase 5：仓库准备

- [ ] 清理 Git history（如有敏感数据）
- [ ] 设置 GitHub repo 描述和 topics/tags
- [ ] 创建 Issue/PR 模板
- [ ] 设置 CI/CD（可选，基础 lint 检查）
- [ ] 发布第一个 Release/Tag（v1.0.0）

## 核心抽象

> **有状态智能体开源的本质挑战**：与无状态工具 Skill 不同，自我进化智能体的价值在于其"记忆"和"进化轨迹"——但这恰恰是不能开源的部分。开源的是**框架**（SKILL.md + evo-agent-model.md + scheduler），不是**实例**（memory/private/ + output/ + 你的知识库）。

> **类比**：开源自我进化智能体就像开源一个"空白大脑的机器人" + "操作手册"——你给出骨架和训练方法，但每个用户自己积累经验和记忆。

## 与已有知识的交叉

- **#43 SKILL.md YAML Frontmatter**：frontmatter 是开源 skill 的发现基础，必须补充
- **#46 Skill 市场化分发**：本学习项直接覆盖并扩展 #46，#46 可标记为已合并
- **#29 Anthropic Modular Skill Architecture**：官方 skill 标准是兼容目标
- **#54 Agent 安全架构**：SECURITY.md 和数据隔离是安全需求的子集
