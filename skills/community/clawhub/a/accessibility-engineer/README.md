# accessibility-engineer（超级技能 · Superpowers 架构）

> 一个完整的无障碍工程技能库：让 AI 编程助手交付"盲用也好用"的 Web 界面——覆盖 WCAG 2.2 合规模型、语义化 HTML 与 ARIA、键盘可达与焦点管理、读屏器实测、静态审计与修复工作流。

采用 **Superpowers 架构**：薄 `SKILL.md` 作路由，`references/` 存放按需加载的完整 playbook，`scripts/` 提供确定性可重复脚本，`assets/` 提供即取即用的清单与模板。上下文按需渐进式加载（progressive disclosure）。

## 覆盖能力

| 域 | Playbook | 关键工具 |
|----|----------|----------|
| WCAG 2.2 合规模型 | [references/wcag-playbook.md](references/wcag-playbook.md) | POUR / A-AAA / EAA·ADA |
| 语义化 HTML 与 ARIA | [references/semantic-html-aria.md](references/semantic-html-aria.md) | 语义优先 / ARIA 决策树 |
| 键盘可达与焦点管理 | [references/keyboard-focus.md](references/keyboard-focus.md) | 焦点陷阱 / roving tabindex |
| 读屏器实测 | [references/screen-reader-testing.md](references/screen-reader-testing.md) | NVDA / VoiceOver |
| 审计与修复工作流 | [references/audit-remediation.md](references/audit-remediation.md) | 严重度分级 / CI 门禁 |

## 细粒度子技能

可整库安装，也可只取其中一个：

| 技能 | 说明 | 来源 |
|------|------|------|
| `semantic-markup` | 为组件编写语义化 HTML 与正确 ARIA（按钮/对话框/菜单/标签页） | derived · jakubkrehel/skills@better-accessibility (11.4K) |
| `keyboard-a11y` | 键盘可达与焦点管理（模态陷阱/归还、roving tabindex、SPA 焦点转移） | derived · ibelick/ui-skills@fixing-accessibility (17.6K) |
| `alt-text` | 为图片/SVG/图标按钮/图表撰写替代文本，配合对比度校验 | derived · addyosmani/web-quality-skills@accessibility (49.5K) |
| `a11y-audit` | 跑静态无障碍审计并产出分级修复报告，可接入 CI 作门禁 | derived · addyosmani/web-quality-skills@accessibility (49.5K) |

## 安装

### 安装完整技能库（推荐，含 references / scripts / assets）

```bash
npx skills add skills-repo/accessibility-engineer -g -y
```

### 只安装某个细粒度子技能

```bash
npx skills add skills-repo/accessibility-engineer@semantic-markup -g -y
npx skills add skills-repo/accessibility-engineer@keyboard-a11y -g -y
npx skills add skills-repo/accessibility-engineer@alt-text -g -y
npx skills add skills-repo/accessibility-engineer@a11y-audit -g -y
```

## 目录结构

```
accessibility-engineer/
├── SKILL.md                 # 薄路由：触发词 + 能力索引 + 脚本/资源索引 + 核心原则
├── README.md                # 本文件
├── AGENTS.md                # AI 助手使用指引
├── references/              # 5 个按需加载的 playbook
├── skills/                  # 4 个可单独安装的细粒度子技能
├── scripts/                 # 确定性脚本（纯标准库，无依赖）
│   ├── contrast_check.py    # WCAG 对比度计算与 AA/AAA 判定
│   ├── a11y_audit.py        # 静态 HTML 可访问性审计
│   └── aria_lint.py         # ARIA 用法静态校验
└── assets/                  # 模板与清单
    ├── wcag-checklist.md
    ├── a11y-audit-report-template.md
    └── component-a11y-acceptance.md
```

## 快速开始

```bash
# 对比度（前景 #777 / 背景 #fff → 4.48:1，恰低于 AA）
python3 scripts/contrast_check.py "#777777" "#ffffff" --strict

# 静态 HTML 审计
python3 scripts/a11y_audit.py page.html --strict

# ARIA 用法校验
python3 scripts/aria_lint.py page.html --strict
```

## 设计原则

1. 语义优先：原生标签优于 ARIA，错误 ARIA 比没有更糟。
2. 键盘是底线：所有功能不用鼠标也能完成，焦点可见且不丢失。
3. 对比度算出来：用脚本判定，不靠目测。
4. 自动化只覆盖约三成问题：读屏实测必须人工做。
5. 先读对应 playbook 再动手。
6. 给技术对齐路径，法律结论以官方文本为准。

## 许可

MIT
