# AGENTS.md 飞书同步章节（补充模板）

> 以下内容由 feishu-sync-obsidian Skill 生成，
> 安装本 Skill 后，会追加到 vault/AGENTS.md 末尾。
> 如已有 AGENTS.md，小墨会在末尾追加以下章节。

---

## 飞书同步说明

本 vault 已安装 feishu-sync-obsidian Skill。
飞书 Wiki 文档会同步到本 vault。

### 同步规范

详见 `SYNC-RULES.md`。

### 同步操作

- **手动**：告诉小墨"同步飞书"
- **自动**：每周日 00:00 自动同步

---

## 禁止事项

### 通用
- ❌ 不修改 00原料池 层文件
- ❌ 不删除已有链接（可标记过时）
- ❌ 不在未确认情况下合并矛盾观点
- ❌ 不在 converter.py 中硬编码白名单或不必要的字段映射

### 飞书同步专项
- ❌ 同步时不得删除 vault 中已有文件
- ❌ 不得跳过 feishu_doc_token 去重检查
- ❌ 不得在未读取 SYNC-RULES.md 的情况下执行同步
- ❌ 不得将非 docx 类型（sheet/bitable/mindnote）的飞书内容直接写入正文

---

## 注意事项

### 飞书同步
- 同步前必须读取 SYNC-RULES.md 确认路由规则
- 同步为单向操作（飞书 → Obsidian），不会反向修改飞书文档
- 出现网络错误时，同步中断位置之前的文件已写入，报告失败条目
- 重新同步会跳过已有 feishu_doc_token 的文件（幂等）

---

## 常见问题

**Q: 同步后内容有错误怎么办？**
A: 在 Obsidian 里直接编辑。同步只写入一次，不会覆盖已有内容。

**Q: 想重新同步某个文档怎么办？**
A: 先删除 vault 中对应文件，再执行同步。

**Q: 同步漏了几个文档？**
A: 检查 SYNC-RULES.md 路由规则，确认关键词命中。

**Q: 如何查看同步历史？**
A: 查看 `/tmp/feishu-sync-obsidian/sync_state.json`。
