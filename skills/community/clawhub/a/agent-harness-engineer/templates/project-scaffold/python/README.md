# Agent项目脚手架 - Python版本

## 文件清单

本目录包含一个完整的Python Agent项目模板，包含以下文件：

### 配置文件
- `config/settings.yaml` - 主配置文件
- `config/agents/default.md` - 默认Agent角色定义
- `config/hooks/pre-tool-use.py` - 工具执行前Hook示例
- `config/hooks/post-tool-use.py` - 工具执行后Hook示例

### 核心代码
- `src/main.py` - 入口文件
- `src/agent/core.py` - Agent核心循环
- `src/agent/session.py` - 会话管理
- `src/agent/context.py` - 上下文管理
- `src/agent/memory.py` - 记忆系统
- `src/tools/registry.py` - 工具注册表
- `src/tools/file_tools.py` - 文件操作工具
- `src/tools/network_tools.py` - 网络请求工具
- `src/tools/browser_tools.py` - 浏览器工具
- `src/llm/client.py` - LLM客户端抽象
- `src/llm/factory.py` - 工厂函数
- `src/llm/providers/anthropic.py` - Anthropic实现
- `src/llm/providers/openai.py` - OpenAI实现
- `src/llm/providers/local.py` - 本地模型实现
- `src/permissions/models.py` - 权限模型
- `src/permissions/hooks.py` - Hook系统
- `src/permissions/sandbox.py` - 沙箱管理
- `src/utils/logging.py` - 日志配置
- `src/utils/errors.py` - 错误定义

### 其他文件
- `skills/example-skill.md` - Skill示例模板
- `tests/test_agent.py` - Agent测试
- `tests/test_tools.py` - 工具测试
- `tests/test_permissions.py` - 权限测试
- `docs/architecture.md` - 架构文档
- `docs/api.md` - API文档

## 使用方法

1. 复制此目录到你的项目
2. 修改 `config/settings.yaml` 配置
3. 安装依赖：`pip install -r requirements.txt`
4. 启动Agent：`python src/main.py`
