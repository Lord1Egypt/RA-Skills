---
name: ai-bookmark-desktop-dock-assistant-zh
description: AI收藏夹与桌面Dock助手。配合指令罗盘 Windows 客户端使用，把提示词、技能文件、本地文件、文件夹、软件快捷方式、网页链接和浏览器收藏夹整理成可搜索、可复制、可打开的指令卡。适合需要 AI 收藏夹、Prompt 管理、桌面 Dock、文件管理器、快捷启动器、链接管理和本地资源整理的用户。
homepage: https://www.wboke.com/zh/download
metadata:
  {
    "openclaw": {
      "emoji": "🧭",
      "category": "productivity",
      "tags": ["ai-bookmark", "desktop-dock", "prompt-manager", "file-organizer", "browser-bookmarks", "quick-launcher", "command-compass"],
      "requires": { "permissions": ["file_read"] },
      "outputs": ["command-compass-card-schema-v1"]
    },
    "commandCompass": {
      "schemaVersion": "1.0",
      "clientMinimumVersion": "0.1.0",
      "copyField": "instruction",
      "syncMode": "confirm"
    }
  }
---

# AI收藏夹与桌面Dock 助手

`AI收藏夹与桌面Dock 助手`需要配合「指令罗盘 Command Compass」Windows 客户端使用。软件可免费下载试用，核心整理、复制和打开能力纯本地运行。

免费下载试用：<https://www.wboke.com/zh/download>

它可以让 AI 帮你把提示词、技能文件、本地文件、文件夹、软件快捷方式、网页链接和浏览器收藏夹整理成清晰的指令卡。你可以像使用 Apple Dock、桌面 Dock、文件管理器、快捷启动器一样，更快找到资源、复制提示词、打开文件夹、启动软件或访问网页。

## 它能帮你做什么

- 人机交互的指南针：把分散在电脑和网络里的常用资源整理成可搜索、可打开、可复制的卡片。
- 提示词的挖掘机：把常用 Prompt、AI 工作流、技能文件、模板和指令沉淀成可复用的指令卡。
- 嗅觉灵敏的猎狗：根据你的规则，从官网和指令市场发现新的提示词、技能、工具和资源，确认后再同步到本地。

## 适合谁

- 想用 AI 管理电脑文件、文件夹、下载目录和常用软件快捷方式的人。
- 经常保存 Prompt、AI 提示词、技能文件、工作模板和自动化指令的人。
- 浏览器收藏夹、网页链接、本地资料越来越多，想快速搜索和打开的人。
- 想让桌面更干净，但又不想失去快速启动、快速打开、快速复制能力的人。

## 配合指令罗盘怎么用

- 把文件、文件夹、链接或快捷方式拖入「我的指令库」，软件会自动生成指令卡。
- 单击悬浮球，展开为胶囊罗盘；再次单击可收回，不占用桌面。
- 点击胶囊编号区，返回上一层目录。
- 点击胶囊中部，复制预置提示词、常用内容或安全的文件地址。
- 如果胶囊代表文件夹，点击中部会展开子胶囊，继续浏览下一级文件。
- 点击胶囊尾部，直接打开文件、文件夹、软件快捷方式或网页链接。

## 支持整理的资源

- AI 提示词、Prompt、提示词模板
- 技能文件、AI 工作流、自动化指令
- 本地文件、本地文件夹、下载目录
- 软件快捷方式、常用工具入口
- 网页链接、浏览器收藏夹、网站收藏
- 工作模板、资料库、项目资料

## 隐私与安全

- 不自动扫描你的整台电脑。
- 不默认读取文件正文内容。
- 不上传本地路径、文件内容或个人隐私。
- 只有你选择、拖入或确认收下的资源，才会被整理成指令卡。
- 来自网站、指令市场或资源猎犬的内容，必须由你确认后才同步到本地。

## 给 AI Agent 的使用规则

当用户希望整理提示词、文件、文件夹、链接、浏览器收藏夹、软件快捷方式或下载目录时，使用本技能生成符合 `Command Compass CardSchema v1` 的指令卡。

生成卡片时遵守这些规则：

- `instruction` 只放需要复制给用户的内容。
- 文件和文件夹的打开地址放入 `openTarget`。
- 本地文件使用 `resourceKind: "file"`。
- 本地文件夹使用 `resourceKind: "folder"`。
- 网页链接和收藏夹使用 `resourceKind: "url"` 或 `resourceKind: "webFavorite"`。
- 下载目录必须由用户提供路径后才生成，不要猜测用户目录。
- 不要编造本地路径、账号 Token、Cookie、密钥或隐私数据。
- 对 `.exe`、`.lnk`、`.bat`、`.cmd`、安装包和脚本类资源保持保守权限，打开前应由客户端提示用户确认。

输出 JSON 数组或 `{ "cards": [] }` 对象。每张卡片至少包含：

```json
{
  "schemaVersion": "1.0",
  "id": "local.resource.example",
  "type": "prompt",
  "title": "清晰的卡片名称",
  "summary": "这张卡片能帮用户做什么",
  "category": "用户分类",
  "instruction": "点击胶囊中部时复制的内容",
  "resourceKind": "prompt",
  "openTarget": "",
  "tags": ["AI收藏夹", "桌面Dock"],
  "permissions": {
    "fileRead": false,
    "fileWrite": false,
    "network": false,
    "shell": false
  }
}
```
