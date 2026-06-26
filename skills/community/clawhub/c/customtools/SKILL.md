# Custom Tools - OpenClaw 插件

## 简介

Custom Tools 是 OpenClaw 的扩展插件，提供 18 个实用工具，涵盖任务管理、代码智能、配置管理等场景。

## 包含工具

### Task 任务管理
- `task_create` - 创建新任务
- `task_list` - 列出所有任务
- `task_get` - 获取任务详情
- `task_update` - 更新任务状态
- `task_stop` - 停止/完成任务

### Skill 技能加载
- `skill_load` - 动态加载技能
- `skill_list` - 列出可用技能
- `skill_search` - 搜索技能

### LSP 代码导航
- `lsp_goto_definition` - 跳转到定义
- `lsp_find_references` - 查找引用
- `lsp_document_symbols` - 获取文档符号
- `lsp_hover` - 获取悬停信息
- `lsp_workspace_symbol` - 工作区符号搜索

### Config 配置管理
- `config_get` - 获取配置项
- `config_set` - 设置配置项
- `config_list` - 列出配置分类
- `config_export` - 导出配置
- `config_reset` - 重置配置

### MCP 客户端
- `mcp_echo` - 测试MCP服务器连接
- `mcp_list_servers` - 列出已添加的MCP服务器
- `mcp_list_tools` - 获取MCP工具列表
- `mcp_call_tool` - 调用MCP工具

## 安装

```bash
openclaw plugins install @custom/openclaw-custom-tools
```

## 使用示例

### 创建任务
```
task_create { "subject": "完成项目报告" }
```

### 列出任务
```
task_list
```

### 搜索技能
```
skill_search { "query": "天气" }
```

## 系统要求

- OpenClaw >= 2026.4.0
- Node.js >= 18

## 许可证

MIT-0
