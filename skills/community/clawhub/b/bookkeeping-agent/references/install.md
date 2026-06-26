# 安装

## 前置条件

本 skill 依赖本地已可用的 `bookkeeping` 命令。

macOS 推荐先用 Homebrew 安装 `bookkeeping-tool`：

```bash
brew install lastarla/tap/bookkeeping-tool
```

安装后确认下面的命令可运行：

```bash
bookkeeping --help
```

如果这条命令不可用，本 skill 无法完成导入、查询、汇总和看板启动。

## 放置到 OpenClaw skills 目录

OpenClaw 会从 skills 目录发现本 skill。

推荐两种放置方式：

### 方式 1：当前工作区

把本仓库放到当前 OpenClaw 工作区的 `skills/` 目录下，例如：

```text
<workspace>/skills/bookkeeping-agent/
```

这种方式便于跟当前项目一起管理。

### 方式 2：用户级共享目录

也可以放到：

```text
~/.openclaw/skills/bookkeeping-agent/
```

适合多个工作区复用同一个 skill。

## 重新加载 skill

放置完成后，启动新的 OpenClaw 会话，让 skill 被重新发现和加载。

如果你修改了 `SKILL.md` 后没有立即生效，请开启新会话后重试。

## 处理消息附件的可选增强

如果 OpenClaw 当前消息上下文已经提供了本地 inbound 附件路径，bookkeeping skill 会优先直接使用该路径。

如果上下文里没有本地路径、只有 Feishu 附件引用，再额外安装并启用 `@angli/openclaw-message-attachments` 作为下载 fallback。

推荐链路是：

1. 优先使用 OpenClaw 已落盘的本地 inbound 文件
2. 如果没有本地路径，再调用附件下载插件
3. 使用返回的本地路径执行 `bookkeeping import <file> --json`

另外要注意：OpenClaw inbound 落盘文件名可能不保留 `.csv` / `.xlsx` 后缀，文件类型应优先根据附件原始文件名或 MIME 信息判断。

## 维护者发布注意事项

如果计划发布到 ClawHub：

1. 不要在 `SKILL.md` 正文中写 `curl`、`wget`、下载二进制或执行远程脚本的安装指令
2. 不要添加会在运行时自动下载外部可执行程序的包装脚本
3. 把依赖安装方式写到 `SKILL.md` 的 metadata `install` 字段里，让平台展示安装提示
4. 在 `SKILL.md` 开头明确声明：仅在 `bookkeeping` 已经在 `PATH` 上时使用本 skill

## 验证

验证点至少包括：

1. `bookkeeping --help` 可运行
2. skill 目录中存在 `SKILL.md`
3. 新会话中可以看到 bookkeeping skill 已被加载
4. 上传账单或询问交易汇总时，OpenClaw 能自动路由到该 skill
