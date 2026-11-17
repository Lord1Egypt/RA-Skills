# AideNote for Hermes

AideNote 录音笔记与本机智能体连接技能。安装后，Hermes 可以查询用户真实的录音、转写、AI 摘要、会议待办和知识库，并可通过已验证的安装程序连接 AideNote 手机 App。

## 安装

推荐通过 ClawHub 安装，Hermes 会下载完整技能目录并执行安全扫描：

```bash
hermes skills install clawhub/aidenote-hermes
```

也可以直接告诉 Hermes：

```text
请安装 ClawHub 上的 aidenote-hermes 技能，并帮我连接 AideNote 手机 App。
```

本仓库同步保存最新开源源码，`skills/aidenote-hermes/` 是完整的 Hermes Skill 目录。

## 首次连接

安装技能后，对 Hermes 说：

```text
帮我安装并连接 AideNote。
```

Hermes 会调用技能内的安全安装流程。如果本机尚未授权，会显示一个 8 位配对码：

1. 打开 AideNote App。
2. 添加或编辑 Hermes 助手。
3. 输入电脑上显示的配对码。
4. 点击“确认连接”。

确认后，电脑会自动安装并启动 AideNote tunnel、MCP server 和 Hermes bridge。用户不需要在对话中发送 API Key。

## 使用示例

- “查看最近的录音笔记”
- “查看分享给我的录音”
- “总结昨天的产品会议”
- “今天有哪些待办？”
- “搜索提到 RainCentral 的会议”
- “查看我的知识库”
- “查看这个知识库里保存的录音”
- “检查 AideNote 手机连接状态”

技能要求 Hermes 在回答录音、会议、摘要和待办问题前先调用 AideNote 脚本，禁止根据聊天记忆猜测数据或在调用失败时声称没有记录。

## 支持平台

- macOS Intel / Apple Silicon
- Windows x64 / ARM64

Hermes Skill 版本：`1.2.9`。本机连接套件版本：`3.2.6`。

## 安全设计

- 安装脚本和二进制文件使用固定版本地址。
- 下载内容在执行前进行 SHA-256 校验。
- 只向安装进程传递必要环境变量。
- 配对凭据绑定当前 AideNote 账号和设备。
- 不在聊天内容中展示 API Key、访问令牌或配置文件。

## 项目文件

- `SKILL.md`：Hermes 行为和工具选择规则。
- `scripts/aidenote.py`：录音、摘要、待办和知识库查询。
- `scripts/bridge.py`：配对、安装和连接状态检查。
- `scripts/configure.py`：无法使用 App 配对时的本机恢复工具。
- `references/api-contract.md`：接口与返回值维护说明。

官网：[https://www.aidenote.cn](https://www.aidenote.cn)
