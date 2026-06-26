# ApiTest Skill

当用户需要从本地服务器获取工具数据时，自动调用 `http://localhost:8080/gettool` 接口获取工具信息。

## 前置要求

### 设置环境变量

**在使用本 skill 之前**，你必须先设置环境变量 `API_TEST_KEY`：

```bash
# Linux/macOS
export API_TEST_KEY="你的API密钥"

# Windows (CMD)
set API_TEST_KEY=你的API密钥
```

**注意**: 环境变量需要在启动 OpenClaw 之前设置，或者在系统级别设置。

## 使用方法

设置好环境变量后，当用户说以下内容时，skill 会自动调用接口：

- "帮我访问localhost获取工具"
- "获取localhost的工具数据"
- "调用 localhost:8080/gettool"
- "从本地服务器获取工具列表"

## API 调用

本 skill 会使用以下格式调用接口：

```bash
curl -H "Authorization: Bearer ${API_TEST_KEY}" http://localhost:8080/gettool
```

## 注意事项

- 确保本地服务器 localhost:8080 已启动
- 确保 /gettool 接口可访问
- API_TEST_KEY 必须在系统环境变量中设置好才能使用本 skill
