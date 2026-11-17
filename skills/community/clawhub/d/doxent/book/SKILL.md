---
name: book
description: "当用户需要操作 Doxent / 办公本 / 读写笔记里的真实书籍、书架文件、本地文件导入、远程 URL 导入、上传结果确认，或询问 book/open-model-book 相关接口时使用。"
---

# doxent book

## 概览

这个模块负责 Doxent / 办公本里的真实书籍与文件上传操作。
只处理本地文件导入、远程 URL 导入、书架上传结果确认与接口说明。

## 开始前

- 先读 `references/open-model-book-api.md`
- 遵循 `../shared/port-and-health.md`
- 遵循 `../shared/write-and-sync.md`
- **【强制】所有 API 调用必须通过 `../shared/scripts/doxent_api.py` 发送，用法见主 SKILL.md "网络请求规则"**

## 核心流程

1. 通过 `doxent_api.py` 发起请求；脚本会自动检查服务、唤醒 CLI 并处理端口回退
2. 判断 `source` 是本地绝对路径还是远程 URL
3. 如果 URL 没有扩展名且用户未提供 `name`，要求用户补完整文件名
4. 调用 `/open-model-book/file/upload`
5. 返回时区分本地落盘结果与云端上传结果

## 接口范围

- `/open-model-book/health`
- `/open-model-book/file/upload`
- 仅当用户明确要求补一次全量同步，或正在排查跨模块同步状态时，才使用 `/open-model/sync`

## 工作规则

- 本地 `source` 必须是绝对路径
- 远程 `source` 必须是 `http://` 或 `https://`
- 不要猜扩展名
- 不要把 `/open-model/sync` 当成每次上传后的必经步骤

## 响应风格

- `结果`
- `来源`
- `上传结果`
- `补充说明`
- `下一步`
