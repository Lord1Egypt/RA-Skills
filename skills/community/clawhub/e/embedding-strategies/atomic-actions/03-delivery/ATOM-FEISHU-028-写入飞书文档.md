# ATOM-FEISHU-028 - 写入飞书文档

> 版本：V1.0  
> 状态：🟡 新建  
> 最后更新：2026-03-07

---

## 📋 动作定义

**名称：** 写入飞书文档  
**分类：** 交付层（Delivery Layer）  
**编号：** ATOM-FEISHU-028

**一句话描述：** 将内容写入飞书文档，支持分块写入避免 400 错误

---

## 🎯 输入输出

### 输入
- **类型：** 文本 + 文档 Token
- **内容：** Markdown 内容 + 飞书文档 Token
- **必填：** 是

### 输出
- **类型：** 布尔值
- **内容：** 写入成功/失败
- **附加：** 写入的 blocks 数量

---

## ⚙️ 偏好设置

### 分块写入策略
- **单次限制：** ≤200 blocks（避免 400 错误）
- **分块大小：** 30-50 blocks 一块
- **写入模式：** write → append → append

### 内容组织
- **第 1 块：** 标题 + 前言 + 部分表格
- **第 2 块：** 主体内容（表格/章节）
- **第 3 块：** 附录 + 更新日志 + 说明

### 增量更新原则 🆕（2026-03-07 15:57）
- **不覆盖历史：** 增量添加，不删除旧内容
- **版本记录必更：** 每次更新后必须在"版本记录"表新增一行
- **版本号递增：** 次版本 +1（V1.2 → V1.3）
- **时间标注：** 记录更新时间（精确到分钟）
- **修改人标注：** 记录修改人（阿福）

### 版本记录更新流程 🆕
```
1. 读取当前版本记录表
2. 获取最新版本号（如 V1.2）
3. 生成新版本号（V1.3）
4. 在版本记录表顶部插入新行
5. 内容：版本号 + 时间 + 修改内容 + 修改人
6. 更新文档头部的"版本：V1.3"
```

### 错误处理
- **400 错误：** 自动减小分块大小重试
- **网络错误：** 重试 3 次
- **权限错误：** 立即报错
- **版本记录未更新：** ❌ 视为失败

### ⚠️ 严重警告 🆕（2026-03-07 16:05）

**`write` 模式会覆盖整个文档！**

**❌ 错误用法：**
```powershell
# 只想更新版本号，结果覆盖了整个文档！
feishu_doc -action write -doc_token $docToken -blocks "版本：V1.3"
# 后果：原文档 500 blocks → 只剩 1 block
```

**✅ 正确用法：**
```powershell
# 创建新文档或完全重写时才用 write
feishu_doc -action write -doc_token $docToken -content $完整新内容

# 增量更新用 append 或 insert
feishu_doc -action append -doc_token $docToken -content $新增内容
feishu_doc -action insert -after_block_id "xxx" -content $插入内容

# 更新单个 block 用 update_block
feishu_doc -action update_block -block_id "xxx" -content "新内容"
```

**血泪教训：**
> 永远不要用 `write` 更新单个字段！除非你想重写整个文档！

---

## 📝 操作步骤

### 基础流程

```powershell
# 1. 准备文档和内容
$docToken = "GeG0dywMxof8dLx1tcUckSFNndh"
$content = Get-Content "content.md" -Raw

# 2. 分块（按内容长度估算 blocks）
$blocks = $content -split "`n"
$blockSize = 50  # 每块 50 行
$chunks = @()
for ($i = 0; $i -lt $blocks.Count; $i += $blockSize) {
    $chunks += , $blocks[$i..([Math]::Min($i + $blockSize - 1, $blocks.Count - 1))]
}

# 3. 第 1 块：write 模式（覆盖）
Write-Host "写入第 1 块..."
feishu_doc -action write -doc_token $docToken -content ($chunks[0] -join "`n")

# 4. 第 2 块及以后：append 模式（追加）
for ($i = 1; $i -lt $chunks.Count; $i++) {
    Write-Host "写入第 $($i + 1) 块..."
    feishu_doc -action append -doc_token $docToken -content ($chunks[$i] -join "`n")
}

# 5. 确认
Write-Host "✅ 飞书文档写入完成！共 $($chunks.Count) 块"
return $true
```

### 增量更新流程 🆕（2026-03-07 15:57）

```powershell
# 1. 读取当前文档，获取最新版本号
$currentDoc = feishu_doc -action read -doc_token $docToken
$lastVersion = $currentDoc | Select-String "V\d+\.\d+" | Select-Object -First 1
# 例如：V1.2

# 2. 生成新版本号
$major, $minor = $lastVersion -split "\."
$newVersion = "$major.$([int]$minor + 1)"
# V1.2 → V1.3

# 3. 生成版本记录行
$currentTime = Get-Date -Format "yyyy-MM-dd HH:mm"
$changeSummary = "新增 SKILL-TTS-001 和 SKILL-SYNC-001"
$modifier = "阿福"

# 4. 在版本记录表插入新行（在表头后第一行）
$versionRow = "| $newVersion | $currentTime | $changeSummary | $modifier |"
feishu_doc -action insert -doc_token $docToken -after_block_id "version_table_header" -content $versionRow

# 5. 更新文档头部的版本号
feishu_doc -action write -doc_token $docToken -blocks "版本：$newVersion"

# 6. 确认
Write-Host "✅ 版本记录已更新：$lastVersion → $newVersion"
```

---

## 🔄 使用场景

### 场景 1：创建原子动作清单
```
触发：需要创建飞书文档
  ↓
调用：ATOM-FEISHU-028
  ↓
内容：28 个原子动作表格（402 blocks）
  ↓
分块：3 次写入（181 + 178 + 43）
```

### 场景 2：更新项目文档
```
触发：项目文档需要更新
  ↓
调用：ATOM-FEISHU-028
  ↓
内容：新增章节（100 blocks）
  ↓
分块：2 次写入（50 + 50）
```

---

## 🔗 关联动作

### 前置动作
- ATOM-IO-019：读取 HTML 模板（如需要）
- ATOM-IO-020：写入 HTML 内容（如需要）

### 后置动作
- 无

### 常组合使用
- ATOM-DATA-003 + ATOM-FEISHU-028
  （读取内容 → 写入飞书）

---

## ✅ 检查清单

### 执行前确认
- [ ] 文档 Token 正确
- [ ] 有编辑权限
- [ ] 内容已分块（≤200 blocks/块）
- [ ] 网络正常

### 执行后确认 🆕（2026-03-07 15:57）
- [ ] 版本记录表已更新（新增一行）
- [ ] 文档头部版本号已更新
- [ ] 更新时间已标注（精确到分钟）
- [ ] 修改人已标注
- [ ] 版本号递增（V1.2 → V1.3）

### ⚠️ 模式选择确认 🆕（2026-03-07 16:05）
- [ ] **确认没有误用 `write` 模式**（会覆盖全文档！）
- [ ] 增量更新用 `append` 或 `insert`
- [ ] 单个 block 更新用 `update_block`
- [ ] 只在创建新文档或完全重写时用 `write`

---

## ⚠️ 常见错误

### 错误 1：一次性写入太多
```
❌ 错误：402 blocks 一次性写入 → 400 错误
✅ 正确：分 3 块写入（181 + 178 + 43）
```

### 错误 2：分块大小不合理
```
❌ 错误：每块 500 blocks → 仍可能 400 错误
✅ 正确：每块 30-50 blocks
```

### 错误 3：模式使用错误
```
❌ 错误：所有块都用 write 模式（会覆盖）
✅ 正确：第 1 块 write，后续 append
```

---

## 💡 核心原则

> **飞书长文档必须分块写入！**

**分块策略：**
1. 估算 blocks 数量（1 行 ≈ 1 block）
2. 超过 200 blocks → 分块
3. 第 1 块 write，后续 append
4. 每块 30-50 blocks 最安全

**经验教训：**
- 原子动作清单文档：402 blocks → 分 3 块
- 单次上限：≤200 blocks
- 安全范围：30-50 blocks/块

---

_模块化定义 | 可独立调用 | 分块写入 | 2026-03-07_
