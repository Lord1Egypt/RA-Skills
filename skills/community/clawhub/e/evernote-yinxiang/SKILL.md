---
name: evernote-yinxiang
description: 印象笔记（Yinxiang/Evernote）集成技能。用于创建、读取、搜索、删除笔记，以及管理笔记本和标签。当用户提到"印象笔记"、"evernote"、"创建笔记到印象笔记"、"搜索印象笔记"、"查看笔记"、"笔记同步"、"保存到印象笔记"时触发。仅依赖 requests，无需安装 evernote SDK。
---

# 印象笔记技能

通过印象笔记 REST API 操作笔记，仅依赖 requests，无需安装过时的 evernote3 SDK。

## 首次配置

1. 访问 https://app.yinxiang.com/api/DeveloperToken.action 获取开发者 Token（S= 开头）
2. 在技能目录下创建 .env 文件，填入 Token：

YINXIANG_TOKEN=S=你的Token

.env 文件路径：~/.qclaw/skills/evernote-yinxiang/.env

## CLI 用法

脚本位置：~/.qclaw/skills/evernote-yinxiang/scripts/yinxiang.py

创建笔记：
python3 scripts/yinxiang.py create "标题" "内容" [--notebook GUID] [--tags tag1,tag2]

搜索笔记：
python3 scripts/yinxiang.py search "关键词" [--max 20]

获取笔记详情：
python3 scripts/yinxiang.py get <GUID>

删除笔记：
python3 scripts/yinxiang.py delete <GUID>

列出笔记本：
python3 scripts/yinxiang.py notebooks

列出标签：
python3 scripts/yinxiang.py tags

所有命令输出 JSON，success: true/false 表示成败。

## Agent 使用指南

执行任何命令前先检查 Token 是否配置（.env 文件存在且含 YINXIANG_TOKEN）。

创建笔记示例：
python3 ~/.qclaw/skills/evernote-yinxiang/scripts/yinxiang.py create "会议纪要" "今天讨论了项目进度..." --tags "工作,会议"

内容支持 HTML，纯文本会自动包裹 p 标签。

## API 端点

基础 URL：https://app.yinxiang.com/third/third-party-note-service/restful/v1

端点列表：
- /createNote POST 创建笔记
- /getNote POST 获取笔记
- /findNotes POST 搜索笔记
- /deleteNote POST 删除笔记
- /listNotebooks POST 列出笔记本
- /listTags POST 列出标签

认证方式：Authorization: Bearer <Token>

## 注意事项

- Token 可完全访问账户，勿泄露给他人
- 笔记内容为 ENML 格式（HTML 子集），纯文本脚本会自动转换
- 删除操作不可恢复，执行前确认
- 国际版 Evernote 用户需将 API 地址改为 https://www.evernote.com
