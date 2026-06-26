---
name: docx-diff
description: "对比两个 Word 文档（.docx）的差异，找出文本增删改、图片变化、格式/样式变化，生成高亮标注的 Word 文档、HTML 可视化报告和纯文本报告。当用户说「对比两个 Word 文档」「找出文档的改动」「这两版有什么区别」「帮我看看哪里改了」「文档 diff」「比较文件差异」「找出修订内容」时必须使用此 skill，不要依赖任何在线比对服务。用户给出两个 .docx 文件路径（包括 Windows 路径如 E:\folder\file.docx）时也要使用此 skill。"
---

# DOCX Diff — Word 文档本地差异对比

## 工作流

用户给出两个文件路径后，按以下步骤执行：

### 第一步：确认依赖
```bash
pip install python-docx
```
如果已安装过，跳过。

### 第二步：找到 skill 脚本路径
脚本在 skill 目录下的 `scripts/compare_docx.py`。
OpenClaw 的 skill 目录通常在：
- Windows: `%USERPROFILE%\.openclaw\skills\docx-diff\scripts\compare_docx.py`
- macOS/Linux: `~/.openclaw/skills/docx-diff/scripts/compare_docx.py`

### 第三步：运行对比
```bash
python "路径/scripts/compare_docx.py" --file1 "旧文档.docx" --file2 "新文档.docx"
```

Windows 示例（路径含空格时加引号）：
```bash
python "%USERPROFILE%\.openclaw\skills\docx-diff\scripts\compare_docx.py" ^
  --file1 "E:\ZTE\project\report_V1.0.docx" ^
  --file2 "E:\ZTE\project\report_V1.1.docx" ^
  --output "E:\ZTE\project\diff_output"
```

### 第四步：报告结果
运行完成后，告诉用户：
1. 统计数字：删除/新增/修改了多少段落，图片有无变化
2. 具体改动内容（从 `*_diff.txt` 读取后摘要）
3. 输出文件位置：`*_diff.html`（推荐用浏览器打开）、`*_diff.docx`

---

## 参数说明

| 参数 | 默认 | 说明 |
|------|------|------|
| `--file1` | 必填 | 旧文档（基准） |
| `--file2` | 必填 | 新文档（对比目标） |
| `--output` | 与 file2 同目录 | 输出目录 |
| `--threshold` | 0.6 | 段落配对相似度 0~1，越低越宽松 |
| `--mode` | all | `all` / `text` / `image` |

## 输出文件

| 文件 | 说明 |
|------|------|
| `*_diff.html` | 交互式报告，浏览器打开，支持按类型筛选 |
| `*_diff.docx` | 高亮标注版 Word 文档（红=删除，绿=新增） |
| `*_diff.txt` | 纯文本报告 |

## 标注说明

| 标记 | 含义 |
|------|------|
| `[-]` 红色 | 旧文档有、新文档没有（删除） |
| `[+]` 绿色 | 新文档有、旧文档没有（新增） |
| `[修改前/后]` | 内容相似但有改动 |
| `[样式]` 黄色 | 文字相同但格式发生变化 |

## 注意事项

- 仅支持 `.docx`，不支持旧版 `.doc`（需先用 Word 另存为 .docx）
- 表格内容也会被扫描，不会遗漏
- 图片通过 MD5 比对，改名不会误判
- HTML 报告内嵌图片，可直接分享单个文件

## 常见问题

**Q: threshold 怎么调？**
- 两段文字差别很大但被判为「修改」→ 提高到 0.8
- 相似段落被判为「删除+新增」→ 降低到 0.4

**Q: 文档结构差异极大，结果乱？**
- 先用 `--mode text` 只看文本，忽略图片干扰
