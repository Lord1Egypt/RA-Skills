---
name: feishu-wiki-writer
description: |
  飞书知识库文档写入最佳实践。当需要向飞书知识库新建文档、写入大量内容（>50 block）、生成知识图谱/索引页/读书笔记等复杂文档时激活。
  解决 ordering conflict 和重复文档问题。
---

# 飞书文档写入最佳实践

> 适用场景：新建知识库文档、写入 >50 block 的内容、知识图谱/索引页/读书笔记等复杂文档

## ⚠️ 核心原则

1. **永远用 `write` 写新文档，不用 `insert`/`append`**
   - `insert`/`append` 在大文档上会触发 ordering conflict（血泪教训：铁路文档死 5 次、读书笔记 conflict）
   - `write` 全量替换新文档 = 零 conflict

2. **不要先 `feishu_doc create` 再 `feishu_wiki create`**
   - 这样会建出两个文档（一个云盘、一个知识库），需要手动清理
   - 正确做法：只用 `feishu_wiki create`，它本身就会建空文档

3. **内容在本地完全组装好，再一次性写入**
   - 不要边想边写边调 API
   - 先把全部 markdown 准备好，然后一个 `write` 搞定

4. **写完必须读回来验证**
   - "写入成功" ≠ 内容完整
   - 用 `feishu_doc read` 确认关键内容存在，再告诉用户完成

---

## 📋 标准流程（新建知识库文档）

**Step 1：本地组装全部内容**
- 把所有 markdown 在脑子里（或草稿里）组装完整
- 包括标题、表格、列表、摘要——全部准备好再动手

**Step 2：`feishu_wiki create` 在知识库目标位置新建节点**
```json
{
  "action": "create",
  "space_id": "7618419613059140549",
  "parent_node_token": "目标父节点 token",
  "title": "文档标题",
  "obj_type": "docx"
}
```
→ 返回 `obj_token`（这就是文档 token）

**Step 3：`feishu_doc write` 一次性写入全部内容**
```json
{
  "action": "write",
  "doc_token": "Step 2 返回的 obj_token",
  "content": "完整的 markdown 内容..."
}
```

**Step 4：`feishu_doc read` 验证内容完整**
```json
{
  "action": "read",
  "doc_token": "obj_token"
}
```
- 确认 block_count 合理（通常 >50）
- 确认关键章节标题出现在 content 中
- 验证通过再告诉用户完成

---

## 📋 流程变体

### 仅在云盘（不进知识库）
```
feishu_doc create（folder_token 指定位置）
→ feishu_doc write（写内容）
→ feishu_doc read（验证）
```

### 更新现有知识库文档
```
feishu_wiki get（拿 obj_token）
→ 本地组装全部新内容
→ feishu_doc write（全量替换，不用 insert）
→ feishu_doc read（验证）
```

---

## ❌ 禁止操作

| 禁止 | 原因 |
|------|------|
| 大文档用 `insert` | 触发 ordering conflict，必翻车 |
| `feishu_doc create` + `feishu_wiki create` | 产生两个文档，需要手动清理 |
| 分批写入同一文档 | 版本号冲突 |
| 写完不验证就汇报完成 | Done ≠ Claimed |
| 收到 conflict 错误就盲目重试 | 可能已写入成功，重试会导致重复内容 |

---

## 📊 成功案例参考

| 任务 | 块数 | 结果 |
|------|------|------|
| 名校录取画像文档 | 216 块 | 零 conflict ✅ |
| OpenClaw 技术路线图 | 102 块 | 零 conflict ✅ |
| 投资书单知识图谱索引页 | 241 块 | 零 conflict ✅ |
| 指数基金读书笔记 | 88 块 | 零 conflict ✅ |

---

*基于实战踩坑经验整理，2026-04-07*
