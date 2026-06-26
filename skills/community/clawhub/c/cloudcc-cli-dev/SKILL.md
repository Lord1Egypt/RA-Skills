---
name: cloudcc-cli-dev
description: CloudCC CRM 二次开发 CLI 助手。用于需求拆解与方案选型，并通过 cloudcc-cli（cc 命令）创建/拉取/发布自定义对象、字段、菜单/应用、自定义类、定时器、触发器与 Vue 自定义组件等资产。用户提到 CloudCC、cloudcc-cli、cc 命令、对象/字段/触发器/定时器/自定义组件 时应优先使用。
---

# CloudCC CLI Development Skill

## cloudcc-cli
- 需要检查全局是否安装了cloudcc-cli npm包，如果没有请先安装。

## 工作目录
- 在openclaw环境中，需要在agent的workspace中创建code文件夹，然后在code文件中使用cc create project xxx，创建一个模版项目。

## 使用方式（AI 必须遵循）

- 先阅读 `REQUIREMENTS_BREAKDOWN.md`，输出需求拆解与交付物清单，再进入落地步骤。
- 需要环境/密钥 配置时，阅读 `INSTALL_AND_BOOTSTRAP.md`。
- 需要建模时（对象/字段/菜单/应用），阅读 `OBJECTS_AND_FIELDS.md`。
- 需要后端逻辑时（类/定时器/触发器），阅读 `BACKEND_CODE.md`。
- 需要自定义组件时，阅读 `VUE_CUSTOM_COMPONENT.md`。
- 需要快速对照命令与参数时，阅读 `CLI_CHEATSHEET.md`。

## 强制安全边界

- 不要在输出/代码/提交中包含真实密钥（`CloudCCDev`、`safetyMark`、`secretKey`、`openSecretKey`、token
  等）。
- 后端类/触发器/定时器遵守片段同步：仅在
  `@SOURCE_CONTENT_START`~`@SOURCE_CONTENT_END` 内编写可发布逻辑。
- 客户端脚本遵守片段同步：仅在 `function main($CCDK, obj) { ... }`
  的函数体内编写可发布逻辑。

## 快速入口

- 安装与初始化：`INSTALL_AND_BOOTSTRAP.md`
- 需求拆解与方案选择：`REQUIREMENTS_BREAKDOWN.md`
- 自定义对象与字段：`OBJECTS_AND_FIELDS.md`
- 自定义类/定时器/触发器：`BACKEND_CODE.md`
- Vue 自定义组件：`VUE_CUSTOM_COMPONENT.md`
- CLI 速查：`CLI_CHEATSHEET.md`
