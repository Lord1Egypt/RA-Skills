# 错误记录：edit 工具编辑中文内容失败

**日期：** 2026-03-11  
**错误信息：** `⚠️ 📝 Edit: in ~\.openclaw\workspace\memory\2026-03-11.md (1832 chars) failed`

## 问题描述

用户尝试使用 edit 工具编辑 `memory/2026-03-11.md` 文件时失败。

## 根本原因

### 1. 编码匹配问题
- **文件编码：** UTF8（无 BOM）
- **edit 工具期望：** UTF8（但内部字符串比较可能使用 UTF16）
- **问题：** 中文内容在文件中实际存储的字节和 edit 工具构造的 oldText 字节可能不同

### 2. 精确匹配问题
- edit 工具要求 `oldText` **完全匹配**（包括空格、换行、不可见字符）
- 中文标点符号（如全角空格、中文换行）可能被存储为不同字节
- 手动构造的 oldText 很难做到 100% 精确匹配

### 3. PowerShell 编码陷阱
- `Out-File` 默认使用 UTF16-LE（带 BOM）
- `Add-Content` 默认使用系统编码（可能是 GBK）
- 必须显式指定 `-Encoding UTF8`

## 诊断结果

| 检查项 | 结果 |
|--------|------|
| 文件编码 | UTF8（无 BOM）✅ |
| 文件只读 | False ✅ |
| 文件可写 | True ✅ |
| 文件被占用 | 否 ✅ |

## 解决方案

### ✅ 推荐方案 A：使用 Add-Content（追加内容）

```powershell
Add-Content -Path "文件路径" -Value "新内容" -Encoding UTF8
```

**优点：**
- 最简单可靠
- 无需读取整个文件
- 编码明确指定

### ✅ 推荐方案 B：使用 read + write（覆盖写入）

```powershell
$content = Get-Content "文件路径" -Encoding UTF8 -Raw
$newContent = $content + "新内容"
write --path "文件路径" --content $newContent
```

**优点：**
- 完全控制编码
- 适合需要修改现有内容的场景

### ❌ 避免方案：使用 edit 工具

```powershell
# ❌ 不推荐：中文内容容易匹配失败
edit --path "文件路径" --oldText "旧内容" --newText "新内容"
```

**问题：**
- oldText 必须完全匹配（包括编码）
- 中文内容字节表示可能不一致
- 调试困难（失败时不知道哪里不匹配）

## 最佳实践

1. **追加内容** → 优先使用 `Add-Content -Encoding UTF8`
2. **修改内容** → 使用 `read` 工具 + 内存拼接 + `write` 工具
3. **统一编码** → 所有文件操作显式指定 `-Encoding UTF8`
4. **编辑前检查** → 用 try-catch 测试文件可写性

## 相关记忆

- 已更新 `memory/self-improving/best_practices.jsonl`
- 添加最佳实践：「文件编辑最佳实践 - 避免 edit 工具失败」

## 修复验证

```powershell
# 测试追加
Add-Content -Path "memory/2026-03-11.md" -Value "测试" -Encoding UTF8 ✅

# 测试覆盖
$content = Get-Content "memory/2026-03-11.md" -Encoding UTF8 -Raw
$newContent = $content + "新内容"
[System.IO.File]::WriteAllText("memory/2026-03-11.md", $newContent, [System.Text.UTF8Encoding]::new($false)) ✅
```

---

**教训：** 不要在中文内容文件上使用 edit 工具！
