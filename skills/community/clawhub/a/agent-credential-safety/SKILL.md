---
name: ps
description: 安全处理本机 API 密钥、环境变量、密码、SSH、远程服务器和身份认证。任务涉及凭据读取、认证操作或远程主机连接时使用。限制秘密读取与输出，强制使用批准的 SSH 别名。
---

<!--
核心功能：约束本机凭据、环境变量和 SSH 访问的读取与使用方式。
输入：当前任务明确需要的凭据变量、认证操作或远程主机。
输出：不泄露秘密值、遵循指定别名和交互限制的安全操作。
-->

# 凭据安全 (Credential Safety)

## 执行顺序

1. 确认当前任务是否确实需要凭据、认证或远程访问。
2. 只读取完成当前任务明确需要的变量名；不得遍历、输出或检查其他变量。
3. 在执行命令前应用对应的凭据或 SSH 规则。
4. 让缺失配置和认证失败直接暴露；不得用默认值、空值或伪装成功掩盖错误。
5. 输出、日志、补丁、提交和经验记录中不得包含秘密值。

## 本机凭据

凭据文件固定为用户目录下的统一文件：

```text
~/.localcfg/base.env
```

### 变量命名规范

- 使用清晰、可读的变量名（如 `OPENROUTER_API_KEY`、`GITHUB_TOKEN`），避免晦涩缩写。
- Agent 通过全局规则获知可用变量名，不自行扫描凭据文件。
- 项目代码只通过环境变量读取，不硬编码路径。

### 禁止操作

- 遍历凭据文件中的变量。
- 输出、回显、记录、复制或提交秘密值。
- 为确认环境而检查当前任务不需要的变量。
- 将秘密值写入源码、测试夹具、命令输出、日志或经验文件。

## Python

在 Python 中必须使用以下方式加载凭据：

```python
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path.home() / ".localcfg" / "base.env")
```

加载后只访问当前任务明确需要的变量。缺失时直接报错，不得提供默认值掩盖问题。

## 凭据桥接

当其他工具或 Agent 需要 base.env 中的凭据时，使用 Python 脚本桥接，避免在命令文本中直接暴露秘密值：

```python
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(Path.home() / ".localcfg" / "base.env")
key = os.getenv("SOME_API_KEY")  # 只取当前需要的变量

if key:
    target_env = Path("/path/to/target/.env")
    content = target_env.read_text()
    if "SOME_API_KEY" not in content:
        target_env.write_text(content + f"\nSOME_API_KEY={key}")
```

原则：

- 只读取当前任务明确需要的变量。
- 写入后需重启目标进程使环境变量生效。
- 不得在日志、输出、补丁中暴露秘密值。

## SSH

SSH 连接统一通过 `~/.ssh/config` 中的别名管理。Agent 只使用别名，不知晓 IP、端口、用户名和私钥路径。

```text
# 示例 ~/.ssh/config 条目
Host myserver
    HostName 192.0.2.1
    Port 22
    User deploy
    IdentityFile ~/.ssh/myserver.pem
    IdentitiesOnly yes
```

规则：

- 只使用预配置的 SSH 别名，不得绕过别名使用 IP 或私钥路径直接连接。
- 需要手动输入密码的主机，不得在非交互式 Agent 终端中自动连接；应提示用户手动操作。
- 不得读取或修改 SSH 私钥内容。
- 只有用户明确要求时，才可修改 SSH 配置文件；即使如此，也不得读取或输出私钥内容。

## 工作区经验记录

仅当工作区存在 `.learnings/` 目录时执行：

- 用户纠正实现、流程或判断后，将可复用结论写入 `.learnings/LEARNINGS.md`。
- 命令、脚本、构建、测试或部署失败后，查明原因和解决办法，再写入 `.learnings/ERRORS.md`。
- 写入前检查是否已有同类记录；已有时更新原记录，不重复追加。
- 只记录可复用结论、原因和解决办法，不记录一次性过程。
- 不得记录凭据、令牌、密码、私钥、个人隐私或其他敏感信息。

## 响应要求

- 对不能安全执行的操作，明确说明限制和用户需要采取的最小动作。
- 不展示经过遮盖、截断或哈希处理的秘密值；除非任务明确需要，否则秘密值的任何派生形式也不应输出。
- 认证成功时只报告操作结果，不报告所用秘密。

## 适配你自己的环境

1. 创建 `~/.localcfg/base.env`，按需添加变量（参考 `.env.example`）。
2. 配置 `~/.ssh/config`，为每台服务器建立别名。
3. 在 Agent 全局规则中声明可用的变量名和 SSH 别名。
4. 项目代码统一通过 `load_dotenv(Path.home() / ".localcfg" / "base.env")` 加载。

## 补充参考

- `references/coding-agent-landscape.md`：主流 CLI Coding Agent 的调度能力总览。
