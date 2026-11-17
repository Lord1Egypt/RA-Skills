---
name: note
description: "当用户需要操作 Doxent / 读写笔记里的真实笔记或文件夹，包括搜索、读取正文、创建、移动、重命名、删除、按时间范围整理笔记素材，或询问 note/open-model-note 相关接口时使用。"
---

# doxent note

## 概览

这个模块负责 Doxent / 读写笔记里的真实笔记与文件夹操作。
只处理读取、搜索、创建、移动、重命名、删除和正文读取。

## 开始前

- 先读 `references/open-model-note-api.md`
- 遵循 `../shared/port-and-health.md`
- 遵循 `../shared/write-and-sync.md`
- **【强制】所有 API 调用必须通过 `../shared/scripts/doxent_api.py` 发送，用法见主 SKILL.md "网络请求规则"**

## 核心流程

1. 通过 `doxent_api.py` 发起请求；脚本会自动检查服务、唤醒 CLI 并处理端口回退
2. 先做查询再做写操作
3. 读操作按场景选接口，不要固定走 `search`
4. 写操作基于真实结果再执行
5. 删除前必须先确认对象
6. 写操作成功后再按共享规则决定是否补调 `/open-model/sync`

## 接口范围

- `/open-model-note/health`
- `/open-model-note/list`
- `/open-model-note/search`
- `/open-model-note/file/content`
- `/open-model-note/file/create`
- `/open-model-note/folder/create`
- `/open-model-note/file/delete`
- `/open-model-note/folder/delete`
- `/open-model-note/file/rename`
- `/open-model-note/folder/rename`
- `/open-model-note/file/move`
- `/open-model-note/folder/move`

## 工作规则

- 时间范围类读取或总结请求，优先使用 `fileList`，不要先用 `search`
- 这类请求包括但不限于：`本周笔记`、`今天笔记`、`最近笔记`、`日报素材`、`周报素材`、`总结本周笔记要点`
- `search` 只适合“按名称找笔记 / 文件夹”，不适合“按时间范围找素材”
- `list` 适合已知目录或已知父文件夹 id 的场景，不适合替代时间范围筛选
- 读取正文前，优先先缩小候选范围
- 删除文件或文件夹前，确认 `id`、名称和类型
- 创建文件只保留最小输入：`parentId`、`name`、`markdown`
- 创建文件必须以 POST JSON 调用，body 必须是 JSON 对象，禁止使用 URL 查询串、表单 body 或 `parentId=root` 这类裸字符串
- 创建文件的 `markdown` 必须是真 Markdown：标题用 `#`，列表用 `-`/`1.`，加粗用 `**文本**`，禁止传入 `<h1>`、`<ul>`、`<li>`、`<b>` 等 HTML 标签
- 如果素材已经包含 HTML 标签，先转换成 Markdown 再调用创建接口，不要原样写入 `markdown`
- 创建文件夹只保留最小输入：`parentId`、`name`

## 读取策略

- 用户按名字找笔记：`search` → 必要时 `file/content`
- 用户按目录看内容：`list` → 必要时 `file/content`
- 用户按时间范围整理素材：`fileList` → 对候选逐条 `file/content`
- 用户要“总结 / 整理 / 提炼要点”，且对象是最近、本周、今日这类时间范围笔记：先 `fileList` 缩小范围，再读正文，不要直接回答“没找到”

## 响应风格

- `结果`
- `命中项`
- `正文摘要`
- `下一步`
