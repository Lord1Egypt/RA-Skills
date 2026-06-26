# contributor-guide-writer

## 功能说明
这个 skill 专门为开源项目维护者设计，它能够通过自动分析当前工作区的项目结构、包管理器（如 `package.json`, `go.mod`, `requirements.txt`）以及构建工具（如 `Makefile`, 各种 `lint` 配置），为你自动生成一份量身定制、专业规范的 `CONTRIBUTING.md` 文件。

它会自动填入：
- 项目名称
- 本地开发环境的搭建命令（如 `pnpm install` 或 `go mod download`）
- 运行、测试和代码检查的具体命令（如 `pnpm run dev`, `pytest`）
- 标准的 Fork -> Branch -> PR 工作流说明
- 支持中英双语输出，会根据用户的提问语言自动适配。

## 使用场景
当你开源了一个新项目，或者想要规范化现有项目的社区贡献流程时，可以直接在项目根目录调用此 skill，它会帮你省去手写指南的繁琐工作。

## 提问示例

**中文模式：**
```text
帮我为当前项目写一份 CONTRIBUTING.md
```

**英文模式：**
```text
Generate a contributor guide for this project.
```