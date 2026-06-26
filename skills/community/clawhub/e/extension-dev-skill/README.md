**[English](README_EN.md)** | 中文

# extension-dev-skill

用于 嘉立创EDA & EasyEDA 专业版扩展开发的 skill 。使用此skill可以实现通过 AI Agent 自动完成插件开发，配合extension-dev-mcp-tools由AI自动开发、构建、调试插件。

## 配置skill
### 1. 找到/创建skills目录
依照你所使用的AI Agent说明文档找到或创建存放SKILL的目录  
例如：  
**项目代理兼容**：`.agents/skills`  
**全局代理兼容**：`~/.agents/skills`

### 2. 拉取skill仓库
打开终端，进入skills目录，拉取仓库  
`git clone https://github.com/easyeda/extension-dev-skill`


### 3. 测试
完成后你可以在你所使用的AI Agent中验证  
例如opencode: 执行`/skills`，检查是否存在`extension-dev-skill`


## MCP 调试工具（可选）

推荐安装：[extension-dev-mcp-tools](https://github.com/easyeda/extension-dev-mcp-tools)

可自动将AI Agent构建的扩展导入浏览器中
## 目录结构

```
jlceda-plugin-builder/
  SKILL.md                 # Skill 核心定义（规则、工作流、运行时约束）
  AGENTS.md                # Agent 补充指南（搜索规范、递归查询、代码约定）
  README.md                # 项目说明（本文件）
  resources/
    api-reference.md        # 完整 API 模块列表、枚举定义、MCP 工具文档
    experience.md           # 常见经验总结
```
## 演示视频
基于opencode:  

https://github.com/user-attachments/assets/742954b8-9527-43ad-ae08-3f08ec083fa2