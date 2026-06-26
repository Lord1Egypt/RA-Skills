# 📖 feishu-doc-block-writer 快速参考

**版本：** v2.0（支持 folder_token）  
**更新日期：** 2026-03-20

---

## 🚀 快速开始

### 基础用法

```bash
# 创建在根目录
python block-writer.py --title "标题" --content "内容"

# 创建在指定文件夹
python block-writer.py \
  --title "标题" \
  --content "内容" \
  --parent-node-token "W5udwK8V7ip7bskn3EhcPTbOnOp"
```

---

## 📋 参数列表

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--title` | ✅ | - | 文档标题 |
| `--content` | ✅ | - | 文档内容 |
| `--chunk-size` | ❌ | 500 | 每块字数 |
| `--parent-node-token` | ❌ | None | 文件夹 token |
| `--no-verify` | ❌ | False | 禁用验证 |

---

## 💡 常用示例

### 示例 1：创建简报（根目录）

```bash
python block-writer.py \
  --title "2026-03-20 日报" \
  --content "今日完成工作：..."
```

### 示例 2：创建项目文档（指定文件夹）

```bash
python block-writer.py \
  --title "项目计划" \
  --content "项目目标：..." \
  --parent-node-token "W5udwK8V7ip7bskn3EhcPTbOnOp"
```

### 示例 3：创建长文档（自定义分块）

```bash
python block-writer.py \
  --title "技术文档" \
  --content "详细内容..." \
  --chunk-size 800 \
  --parent-node-token "W5udwK8V7ip7bskn3EhcPTbOnOp"
```

---

## 📁 如何获取文件夹 token

### 方法 1：从 URL 提取

1. 打开飞书知识库
2. 进入目标文件夹
3. 查看 URL：`https://feishu.cn/wiki/W5udwK8V7ip7bskn3EhcPTbOnOp`
4. 提取 token：`W5udwK8V7ip7bskn3EhcPTbOnOp`

### 方法 2：使用命令查询

```bash
openclaw feishu_wiki --action get --token <文件夹 token>
```

---

## 🔍 验证文档位置

### 方法 1：查看返回结果

```bash
python block-writer.py --title "测试" --content "内容" --parent-node-token "W5udwK8V7ip7bskn3EhcPTbOnOp"
```

输出中检查：
```json
{
  "success": true,
  "parent_node_token": "W5udwK8V7ip7bskn3EhcPTbOnOp"  // ← 检查此项
}
```

### 方法 2：使用 feishu_wiki 验证

```bash
openclaw feishu_wiki --action get --token <文档 token>
```

查看返回的 `parent_node_token` 字段。

---

## ⚠️ 常见问题

### Q1: 不传 parent-node-token 会怎样？
**A:** 文档创建在知识库根目录（默认行为）。

### Q2: 如何批量创建多个文档到同一文件夹？
**A:** 重复使用相同的 `--parent-node-token` 参数。

### Q3: folder_token 和 parent_node_token 是同一个吗？
**A:** 是的，在 feishu_doc API 中称为 `parent_node_token`。

### Q4: 如何确认文档创建成功？
**A:** 检查返回的 JSON 中 `"success": true` 和文档链接。

---

## 📊 输出示例

### 成功输出

```
📄 开始创建文档：测试文档
📊 内容长度：1234 字
📁 存放位置：文件夹 W5udwK8V7ip7bskn3EhcPTbOnOp

✏️  步骤 1: 创建空文档...
✅ 文档创建成功！Token: abc123xyz
🔗 文档链接：https://applink.feishu.cn/doc/abc123xyz

✂️  步骤 2: 内容拆分为 3 个 Blocks

📝 步骤 3: 逐块追加内容...
  写入 Block 1/3 (500 字)... ✅
  写入 Block 2/3 (500 字)... ✅
  写入 Block 3/3 (234 字)... ✅

✅ 所有内容写入完成！

🔍 步骤 4: 验证文档内容...
✅ 验证完成（简化版）

============================================================
📋 执行结果
============================================================
✅ 文档创建成功！
🔗 链接：https://applink.feishu.cn/doc/abc123xyz
📊 Blocks: 3 个
📏 字数：1234 字
📁 文件夹：W5udwK8V7ip7bskn3EhcPTbOnOp
============================================================

{
  "success": true,
  "doc_token": "abc123xyz",
  "url": "https://applink.feishu.cn/doc/abc123xyz",
  "total_blocks": 3,
  "content_length": 1234,
  "parent_node_token": "W5udwK8V7ip7bskn3EhcPTbOnOp"
}
```

---

## 🎯 最佳实践

1. **始终指定文件夹** - 避免文档散落在根目录
2. **使用有意义的标题** - 便于后续查找
3. **合理设置 chunk-size** - 长文档建议 800-1000 字
4. **保留验证步骤** - 确保内容完整写入
5. **记录文档 token** - 便于后续操作

---

## 📞 支持

- **技能位置：** `~/.agents/skills/feishu-doc-block-writer/`
- **测试报告：** `TEST-REPORT.md`
- **完整文档：** `SKILL.md`

---

_快速参考卡片 by 阿丽 🧪_
