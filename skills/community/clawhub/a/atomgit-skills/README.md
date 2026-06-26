# AtomGit Skill

仓库根目录就是 skill 根目录，核心入口放在 [`SKILL.md`](./SKILL.md)，更细的说明按需拆分到 [`references/`](./references/)。

## 结构

- `SKILL.md`：给 agent 读的主入口，只保留触发语义、工具命名约定和高频工作流
- `references/`：按 17 个 AtomGit 分类拆分的渐进披露文档，另含独立 setup/safety 文档

## 依赖

- 已手动配置好的 [AtomGit MCP Server](https://atomgit.com/zkxw2008/AtomGit-MCP-Server)
- MCP 客户端环境中的 `ATOMGIT_TOKEN`

这个 skill 本身不会替用户安装 MCP 服务，也不会在任务中自动执行远程安装命令。它假定 AtomGit MCP 已经由操作者在客户端级别手动核验并配置完成，然后再由 skill 教 agent 如何安全使用已暴露的 AtomGit 工具。

安装、权限和安全边界请看 [references/setup-and-safety.md](./references/setup-and-safety.md)。

## 上游来源

- Skill 源仓库：<https://atomgit.com/zkxw2008/AtomGit-Skills>
- MCP Server 源仓库：<https://atomgit.com/zkxw2008/AtomGit-MCP-Server>
- MCP Server npm 包：<https://www.npmjs.com/package/@atomgit.com/atomgit-mcp-server>

## 设计目标

- 只在明确的 AtomGit 上下文中触发，避免和 GitHub、GitLab 等平台混淆
- 用渐进披露组织内容，减少主 skill 的上下文负担
- 统一使用 `atomgit_*` 形式的 canonical method 名称，并提醒运行时名称可能带额外命名空间

## License

MIT-0
