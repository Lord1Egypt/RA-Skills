# ai-company

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](CHANGELOG.md)
[![License: GPL-3.0](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](LICENSE)
[![Scale tier](https://img.shields.io/badge/scale_tier-micro-teal)](references/scaling.md)

**LLM Agent 治理技能 —— 微型档（micro）：2 个部门、18 个职能块、一个可安装的技能包。**

[English](README.md) | 简体中文

> `README.en.md` 是 `README.md` 的同内容英文副本，保留它是为了让 `.en` /
> `.zh` 语言后缀保持对称，便于 i18n 工具识别。

## 快速开始

1. **安装** —— 把 `ai-company/` 整个目录复制到你的 Agent 技能
   工作区。
2. **激活** —— 技能通过唯一运行时入口 `SKILL.md` 注册；其他任何文件都不
   参与路由与激活。
3. **使用** —— 向你的 Agent 提出治理或交付类问题；它会经由 `SKILL.md`
   路由到 `references/departments/` 下对应的部门规范。
4. **人工模式** —— 从 `prompts/01-implement-method.md` 或
   `prompts/02-robustness-checks.md` 复制现成提示词，粘贴到任意 AI 对话
   窗口。两个文件均为 `human-paste` 模式，不引用任何内部路径。
5. **验证** —— 运行 `python tests/test-method-patterns.py`；用
   `powershell -File scripts/self-scale.ps1 -Action evaluate` 检查档位
   就绪度。

## 包速览

| 项目 | 值 |
|---|---|
| 技能名 | `ai-company` |
| 版本 | 1.0.0 |
| 档位 | `micro`（XS，微型） |
| 部门数 | 2（`governance-and-delivery`、`engineering-and-safety`） |
| 职能块 | 18（8 + 10） |
| 文件总数 | 25 |
| 许可证 | GPL-3.0 |

## 项目结构（Project Structure）

```text
ai-company/
├── .editorconfig
├── .gitignore
├── .scaling-state.json
├── AGENTS.md
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README-FOR-AI.md
├── README.en.md
├── README.md
├── README.zh.md
├── SECURITY.md
├── SKILL.md
├── _meta.json
├── prompts/
│   ├── 01-implement-method.md
│   └── 02-robustness-checks.md
├── references/
│   ├── method-patterns.md
│   ├── error-codes.md
│   ├── scaling.md
│   └── departments/
│       ├── governance-and-delivery.md
│       └── engineering-and-safety.md
├── scripts/
│   ├── self-scale.ps1
│   └── scaling-config.json
└── tests/
    └── test-method-patterns.py
```

## 文档

- [CONTRIBUTING.md](CONTRIBUTING.md) —— 分支、提交、测试与 PR 规则
- [SECURITY.md](SECURITY.md) —— 支持版本与漏洞上报渠道
- [CHANGELOG.md](CHANGELOG.md) —— 版本发布记录
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) —— 社区行为准则
- `AGENTS.md` —— 面向维护本仓库的编码 Agent 的贡献入口（不参与技能
  路由与激活）
- `README-FOR-AI.md` —— 面向 LLM Agent 的生成与维护规格（本独立项目自带、
  完全自包含的唯一权威规格，读者无需任何外部或上层文档）

## 档位升级

本技能包为成长而设计：`scripts/self-scale.ps1 -Action evaluate` 会依据
`scripts/scaling-config.json` 做只读的就绪度检查；真正的档位变更始终需要
人工批准，并记录到 `.scaling-state.json`。阈值、路径与别名等升级规格见
[references/scaling.md](references/scaling.md)；本包的档位阶梯在
`README-FOR-AI.md` §1 本地定义。

## 许可证

Copyright (c) 2026. 采用
[GNU General Public License v3.0](LICENSE) 许可。
