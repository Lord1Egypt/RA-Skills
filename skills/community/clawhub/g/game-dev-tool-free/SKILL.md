---
name: "game-dev-tool-free"
description: "全流程游戏开发向导,涵盖设计、编码、测试、发布与运营基础。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "游戏开发助手免费版"
  version: "1.0.0"
  summary: "全流程游戏开发向导,涵盖设计、编码、测试、发布与运营基础"
  tags:
    - "游戏开发"
    - "全流程"
    - "设计文档"
    - "编码指导"
    - "测试发布"
    - "独立游戏"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write
---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。

# 游戏开发助手 (免费版)
## 概述
本工具为独立开发者与小团队提供全流程游戏开发向导,涵盖从概念设计到发布运营的完整生命周期。包括游戏设计文档 (GDD) 撰写、编码实现指导、测试策略制定、发布流程管理、基础运营支持等内容,帮助开发者系统化推进游戏项目。

免费版聚焦个人与小型团队场景,适合独立开发者、学生、Game Jam 参与者使用。

## 核心能力
| 能力模块 | 描述 | 免费版支持 |
|:--------|:-----|:-----------|
| 游戏概念设计 | 概念文档与市场分析 | 支持 |
| GDD 撰写 | 完整设计文档 | 支持 |
| 编码指导 | 架构与代码示例 | 支持 |
| 测试策略 | 测试用例与流程 | 支持 |
| 发布流程 | 平台发布指南 | 支持 |
| 基础运营 | 社区与更新策略 | 基础 |
| 项目管理 | 任务与进度跟踪 | 基础 |
| 多人协作 | 团队协作平台 | 不支持 (升级 PRO) |
| 资产管理 | 资产版本控制 | 不支持 (升级 PRO) |
| 数据分析 | 玩家数据分析 | 不支持 (升级 PRO) |

### 核心功能执行
用`input_params`参数进行配置。

**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：全流程游戏开发向、涵盖设计、发布与运营基础、面向独立开发者与、小团队的全流程游、戏开发向导、核心能力、游戏设计文档、运营基础、适用场景、独立游戏开发、小型团队协作、Game、Jam、学习游戏开发、差异化、免费版覆盖完整开、发流程、适合个人与小型团、适用关键词、游戏开发等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景
### 场景一: 游戏设计文档
撰写完整的游戏设计文档。

```markdown
# 游戏设计文档 (GDD)
## 不适用场景
以下场景游戏开发助手免费版不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件
需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求。

## 1. 游戏概述
- 游戏名称: [名称]
- 类型: [RPG/动作/策略/...]
- 平台: [PC/移动/主机/...]
- 目标受众: [年龄与玩家类型]
- 一句话描述: [核心卖点]

## 2. 核心玩法
- 核心循环: [探索 → 战斗 → 收集 → 升级]
- 独特卖点 (USP): [与同类游戏的差异]
- 玩家动机: [成就感/探索/社交/...]
- 失败状态: [玩家失败的条件与惩罚]

## 3. 游戏系统
### 3.1 角色系统
- 属性: [生命/攻击/防御/速度/...]
- 等级: [最大等级、经验曲线]
- 技能树: [分支结构、解锁条件]

### 3.2 战斗系统
- 类型: [实时/回合/动作]
- 伤害公式: [基础伤害 = 攻击力 × 技能倍率 - 防御力]
- 状态效果: [中毒/眩晕/增益/...]

### 3.3 经济系统
- 货币: [金币/钻石/...]
- 获取: [战斗/任务/出售]
- 消耗: [购买/升级/解锁]

## 4. 内容设计
- 主线剧情: [章节大纲]
- 关卡设计: [难度曲线、关卡数量]
- 角色 NPC: [主要角色列表]

## 5. 美术与音效
- 美术风格: [像素/手绘/3D/...]
- 音乐风格: [史诗/轻松/紧张/...]
- 音效: [环境/UI/战斗]

## 6. 技术规格
- 引擎: [Unity/Godot/Unreal/...]
- 目标性能: [60FPS @ 1080p]
- 存档: [本地/云端]
```

### 场景二: 编码架构指导
为游戏提供架构建议与代码示例。

```csharp
// 推荐架构: MVC + 事件驱动
// Model: 游戏数据
public class PlayerModel
{
    public int Health { get; private set; }
    public int MaxHealth { get; private set; }
    public int Level { get; private set; }

    public event Action<int, int> HealthChanged;
    public event Action<int> LevelUp;

    public PlayerModel(int maxHealth)
    {
        MaxHealth = maxHealth;
        Health = maxHealth;
        Level = 1;
    }

    public void TakeDamage(int damage)
    {
        Health = Math.Max(0, Health - damage);
        HealthChanged?.Invoke(Health, MaxHealth);
    }

    public void GainExperience(int xp)
    {
        if (xp >= Level * 100)
        {
            Level++;
            LevelUp?.Invoke(Level);
        }
    }
}

// View: 显示层
public class PlayerView : Node
{
    private ProgressBar _healthBar;
    private Label _levelLabel;

    public override void _Ready()
    {
        _healthBar = GetNode<ProgressBar>("HealthBar");
        _levelLabel = GetNode<Label>("LevelLabel");
    }

    public void UpdateHealth(int current, int max)
    {
        _healthBar.Value = (float)current / max * 100;
    }

    public void UpdateLevel(int level)
    {
        _levelLabel.Text = $"Lv.{level}";
    }
}

// Controller: 控制层
public class PlayerController : Node
{
    private PlayerModel _model;
    private PlayerView _view;

    public override void _Ready()
    {
        _model = new PlayerModel(100);
        _view = GetNode<PlayerView>("PlayerView");

        _model.HealthChanged += _view.UpdateHealth;
        _model.LevelUp += _view.UpdateLevel;
    }
}
```

### 场景三: 测试与发布
制定测试策略与发布流程。

```python
# 测试计划模板
test_plan = {
    "unit_tests": [
        {"module": "PlayerModel", "coverage": "90%"},
        {"module": "CombatSystem", "coverage": "85%"},
    ],
    "integration_tests": [
        {"scenario": "player_level_up_flow"},
        {"scenario": "battle_damage_calculation"},
    ],
    "playtests": [
        {"phase": "alpha", "players": 5, "duration": "1 week"},
        {"phase": "beta", "players": 50, "duration": "2 weeks"},
    ],
    "performance_targets": {
        "min_fps": 60,
        "max_memory_mb": 2048,
        "load_time_seconds": 5,
    },
}

# 发布清单
release_checklist = [
    "所有 P0/P1 缺陷已修复",
    "通过了所有自动化测试",
    "完成了至少 2 轮玩家测试",
    "性能达到目标规格",
    "商店页面准备完成 (截图、视频、描述)",
    "隐私政策与用户协议已准备",
    "客服渠道已建立",
    "营销素材已制作",
    "发布日议程已确认",
]
```

## 快速开始
### Step 1: 定义项目
```bash
# 创建项目目录
mkdir -p $HOME/my-game/{design,src,assets,tests,docs}
cd $HOME/my-game

# 初始化设计文档
cat > design/GDD.md << 'EOF'
# 游戏设计文档
[按照模板填写]
EOF
```

### Step 2: 选择技术栈
```yaml
# 技术栈选择指南
引擎选择:
  Unity:
    适用: 3D/2D 全平台
    语言: C#
    优势: 生态成熟、文档全
  Godot:
    适用: 2D 优先,3D 可用
    语言: GDScript/C#
    优势: 开源免费、轻量
  Unreal:
    适用: 3A 级 3D
    语言: C++/Blueprint
    优势: 画质顶尖、蓝图可视化
```

### Step 3: 制定开发计划
```bash
# 里程碑规划
milestones:
  - M1 (4 周): 核心玩法原型
  - M2 (6 周): 核心系统完成
  - M3 (4 周): 内容填充
  - M4 (2 周): 优化与测试
  - M5 (1 周): 发布准备
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

## 示例
### 项目配置文件
```yaml
# $HOME/my-game/project.yaml
project:
  name: "我的游戏"
  version: "0.1.0"
  engine: godot
  target_platforms: [windows, macos, linux]

team:
  size: 1-3
  roles: [designer, programmer, artist]

development:
  version_control: git
  branches: [main, dev, feature/*]
  code_review: optional

testing:
  framework: gotcha
  coverage_target: 80%
  playtest_schedule: "every_2_weeks"

release:
  platforms: [steam, itch_io]
  target_date: "2026-12-01"
  price_usd: 9.99
```

### 代码规范
```python
# 代码规范示例 (Python 伪代码)
CODING_STANDARDS = {
    "命名": {
        "类名": "PascalCase: PlayerController",
        "方法名": "PascalCase: TakeDamage",
        "变量名": "camelCase: playerHealth",
        "常量": "UPPER_SNAKE: MAX_HEALTH",
    },
    "注释": {
        "类注释": "必填: 描述类的作用",
        "方法注释": "必填: 参数与返回值说明",
        "复杂逻辑": "必填: 解释为什么这么实现",
    },
    "结构": {
        "单一职责": "每个类只做一件事",
        "依赖注入": "通过构造函数传入依赖",
        "事件驱动": "使用事件解耦模块",
    },
}
```

## 优选实践
### 1. 最小可行产品 (MVP)
```text
MVP 原则:
- 聚焦核心玩法,砍掉非必要功能
- 用最简资产验证玩法是否有趣
- 尽早让真实玩家试玩
- 根据反馈迭代,而非闭门造车

砍功能清单 (常见陷阱):
- 多人模式 (除非核心玩法)
- 复杂剧情 (除非叙事为核心)
- 自定义编辑器 (除非是工具型游戏)
- 多平台 (先做一个平台做好)
```

### 2. 版本控制
```bash
# 推荐的 Git 工作流
git flow:
  main:        # 生产分支,只接受合并
  develop:     # 开发分支
  feature/*:   # 功能分支
  hotfix/*:    # 紧急修复
  release/*:   # 发布准备
# 标签管理
git tag -a v0.1.0 -m "Alpha 版本"
git tag -a v0.5.0 -m "Beta 版本"
git tag -a v1.0.0 -m "正式发布"
```

### 3. 性能预算
```yaml
# 性能预算示例
performance_budget:
  target_fps: 60
  frame_budget_ms: 16.67
  breakdown:
    rendering: 8ms
    physics: 3ms
    ai: 2ms
    audio: 0.5ms
    script: 2ms
    overhead: 1.17ms
  memory:
    total: 2048MB
    textures: 800MB
    audio: 200MB
    meshes: 400MB
    other: 648MB
```

### 4. 持续集成
```yaml
# .github/workflows/build.yml
name: Build & Test
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Godot
        uses: chickensoft-games/setup-godot@v1
      - name: Run Tests
        run: godot --headless --run-tests
      - name: Build
        run: godot --export "Windows Desktop"
```

## 常见问题
### Q1: 免费版支持多人协作吗?
免费版提供基础项目管理建议,但不包含多人协作平台。需要协作功能可升级 PRO 版本。

### Q2: 推荐哪个游戏引擎?
新手推荐 Godot (开源免费、易上手)。3D 复杂项目推荐 Unity 或 Unreal。

### Q3: 如何获取美术资源?
免费版推荐使用 OpenGameArt、Kenney.nl 等免费资源站。商业项目需要购买或自制。

### Q4: 发布到哪些平台?
独立游戏推荐 Steam、itch.io、Epic Games Store。移动端推荐 App Store、Google Play。

### Q5: 测试应该花多少时间?
测试应该占开发周期的 20-30%。越早测试越好,不要等到完成才测试。

## 依赖说明
### 运行环境
- **Agent 平台**: 支持 SKILL.md 规范的任意 AI Agent (Claude Code、Cursor、Codex、Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **游戏引擎**: 用户自选 (Godot/Unity/Unreal)

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | 推理服务 | 必需 | 由 Agent 内置 LLM 提供 |
| Git | 版本控制 | 推荐 | git-scm.com 下载 |
| 游戏引擎 | 开发工具 | 必需 | 按选择下载 |

### API Key 配置
```bash
# 免费版无需外部 API Key
# 所有指导通过 Agent LLM 本地推理完成
# 可选: 项目默认配置
export GAME_DEV_ENGINE="godot"
export GAME_DEV_PROJECT_DIR="$HOME/my-game"
```

### 可用性分类
- **分类**: MD (纯 Markdown 指令 + 模板)
- **说明**: 本 Skill 通过自然语言指令驱动 Agent 提供游戏开发全流程指导
- **免费版限制**: 个人与小型团队、无多人协作平台、无资产管理、基础运营支持

## 错误处理
| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制
- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。