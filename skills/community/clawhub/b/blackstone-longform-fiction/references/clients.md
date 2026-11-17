# 支持的 AI 客户端

作者问"我能在别的 AI 里用吗""换台电脑怎么办""能不能在 Cursor 里接着写"时，用这份资料回答。

## 一句话

作品保存在作者的账号下，不绑定任何客户端。在新的 AI 里装上同一份技能、授权一次，就能接着写同一部书。

## 各客户端的技能目录

| 客户端 | 全局技能目录 | 项目内目录 | 云端连接 |
|---|---|---|---|
| WorkBuddy | `~/.workbuddy/skills/` | — | 授权后自动合并连接配置 |
| Claude Code | `~/.claude/skills/` | — | 手工粘贴一次配置 |
| Codex | `~/.codex/skills/` | `.agents/skills/` | 手工粘贴一次配置 |
| Cursor | `~/.cursor/skills/` | — | 手工粘贴一次配置 |
| Windsurf | `~/.codeium/windsurf/skills/` | `.windsurf/skills/` | 手工粘贴一次配置 |
| Google Antigravity | `~/.gemini/antigravity/skills/` | — | 手工粘贴一次配置 |
| Gemini CLI | `~/.gemini/skills/` | — | 手工粘贴一次配置 |
| QoderWork | `~/.qoderwork/skills/` | — | 手工粘贴一次配置 |
| OpenCode | `~/.config/opencode/skills/` | — | 手工粘贴一次配置 |
| OpenClaw | `~/.openclaw/skills/` | — | 手工粘贴一次配置 |

这份表的机器可读版本在 `https://blackstone.wansu.tech/install/catalog.json` 的 `clients` 字段；表格与那里不一致时以那里为准。

不在表上的客户端：只要它支持技能和 MCP，同样可以用，但**不要猜测它的目录**。让作者按 `https://blackstone.wansu.tech/install/blackstone.md` 安装，或者去 `https://blackstone.wansu.tech/app/connect` 复制配置。

## 云端连接那一列的含义

- **授权后自动合并连接配置**：仅适用于 WorkBuddy。作者明确同意连接云端后，只增改 `blackstone` 条目，不覆盖其他设置。流程见 [account.md](account.md)。
- **手工粘贴一次配置**：授权流程一样由你完成，但写入配置这一步目前只在 WorkBuddy 上做了自动化。其他客户端要请作者到 `https://blackstone.wansu.tech/app/connect` 复制一次配置粘贴进去，这是一次性的。

**不要为了走完流程去猜测某个客户端的 MCP 配置文件在哪、格式是什么。**猜错会写坏作者的配置，而这比多让他粘贴一次严重得多。

## 换客户端 / 换电脑

告诉作者三步，不要展开讲实现：

1. 在新的 AI 里装上黑石写作助手技能；
2. 说一句"黑石，连接云端"，按提示在浏览器里登录并确认一次；
3. 说"黑石，看看我的云端作品"，原有作品就都在。

要点：**同一个账号**，用同一个手机号登录即可。作品、六项作品资料和故事图谱都在账号下，不会因为换客户端而丢失或需要重新导入。

本地正文文件不会跟着账号走。作者需要在新电脑上继续编辑本地文件时，得自己把正文目录带过去（网盘、Git、U 盘都行）；云端保存的正文可以按章取回，但那属于云端记忆的读取，会按次计费。

## 两个装错了不会报错的地方

作者自行安装遇到"装完了但技能没出现"时，先查这两处：

- **Gemini CLI 与 Google Antigravity 的目录是嵌套的**：`~/.gemini/skills/` 与 `~/.gemini/antigravity/skills/`。装进了另一个，客户端不会报错，只是永远看不到这份技能。
- **装进了项目内目录**：只有 Codex 和 Windsurf 有项目内目录。装在那里，换个项目就用不了。

两种情况都是把技能目录整个挪到正确位置，然后新开一个会话。

## 新开会话

几乎所有客户端都要新开会话才会加载新装或刚更新的技能。作者说"装好了怎么没反应"时，第一句就问他是不是还在原来那个会话里。
