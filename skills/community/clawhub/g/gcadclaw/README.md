# GcadClaw

**通过自然语言生成和修改 GstarCAD 二维工程图纸的 OpenClaw 技能包**

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-blue)]()

## 概述

GcadClaw 是一个 OpenClaw 技能包，利用 `pygcadwin` Python 库实现通过自然语言控制 GstarCAD 进行二维图纸的创建、修改、校验和修复。用户只需用中文或英文描述所需的机械零件或装配体，技能包即可自动生成 DWG 工程图纸，并提供完整的反馈验证链。

## 功能特点

- **自然语言转 CAD**：用自然语言描述零件/装配体，自动生成二维工程图纸
- **DWG 输出**：直接生成标准 DWG 格式文件，兼容 GstarCAD / AutoCAD
- **强制截图反馈**：每次绘图任务必须生成 PNG 截图作为视觉证据
- **实体验证**：自动捕获前后实体状态，对比验证绘图结果
- **修复循环**：校验失败时自动分类问题、最小化修复、重新验证
- **三视图绘制**：默认输出俯视图、正视图和右视图
- **支持场景**：机械零件、装配体、法兰、支架、齿轮组、叶轮、轴、外壳等

## 系统要求

| 项目 | 要求 |
|------|------|
| 操作系统 | Windows（GstarCAD COM 服务器依赖） |
| CAD 软件 | GstarCAD（已安装并注册 COM 服务器） |
| Python | >= 3.9 |
| Python 包 | `pygcadwin`（从 PyPI 安装） |

## 安装

### 1. 在 OpenClaw 中安装本技能

```bash
# 从本地目录加载
openclaw skill load ./gcadclaw

# 或从 ClawHub 安装（发布后）
openclaw skills install gcadclaw
```

### 2. 配置 Python 环境

技能包通过 PyPI 安装 `pygcadwin`：

```bash
# 进入技能目录
cd gcadclaw

# 验证 Python 环境
python scripts/validate_env.py

# 如果验证失败，从 PyPI 安装 pygcadwin
python scripts/setup_python_env.py

# 再次验证
python scripts/validate_env.py
```

## 使用示例

```text
"画一个80x50x8mm的L型支架，三视图，标注两个6mm通孔和三角加强筋"

"Create a 2D three-view drawing in millimeters for a circular flange.
Draw a top view of an 80 mm outside diameter flange centered at the origin."

"画一个行星齿轮组装配图，包含太阳轮、三个行星轮和内齿圈"
```

更多示例见 [examples.md](examples.md)。

## 技能架构

```
gcadclaw/
├── SKILL.md              # 技能描述文档（OpenClaw 入口）
├── README.md             # 项目说明
├── CHANGELOG.md          # 版本变更记录
├── LICENSE               # MIT 开源协议
├── skill.yaml            # 技能配置
├── examples.md           # 使用示例
├── requirements.txt      # Python/PyPI 依赖
├── scripts/              # 辅助脚本
│   ├── setup_python_env.py   # 环境安装
│   ├── validate_env.py       # 环境验证
│   └── capture_feedback.py   # 实体反馈捕获
├── references/           # 参考文档
│   ├── 2d-pygcadwin-workflow.md  # 绘图工作流
│   └── feedback-loop.md         # 反馈循环规范
├── agents/               # 智能体配置
│   └── openai.yaml
```

## 工作流程

```
用户指令 → 编写 brief.md → 捕获 before 状态 → 执行绘图操作
    → 捕获 after 状态 → 截图验证 → 修复（如需）→ 输出 DWG + 反馈报告
```

## 反馈产物

每次成功的绘图任务会产生以下文件：

- `brief.md` — 设计摘要
- `actions.jsonl` — 操作记录
- `before_entities.json` — 操作前实体状态
- `after_entities.json` — 操作后实体状态
- `review.png` — 截图验证
- `feedback.md` — 完整反馈报告
- `.dwg` — 最终 DWG 文件

## 注意事项

- 本技能仅支持 Windows 平台，需要 GstarCAD 已安装并注册 COM 服务器
- 截图是强制要求，不能跳过
- 不支持 AutoCAD COM 接口（仅兼容 GstarCAD）
- 生成的 DWG 文件可被 GstarCAD 和 AutoCAD 打开

## 作者

浩辰软件 — 图转CAD产品团队

## 许可证

MIT License - 详见 [LICENSE](LICENSE)
