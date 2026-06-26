# Feishu Document Generation - 飞书文档生成 Skill

> 版本：V1.0  
> 状态：🆕 新建  
> 最后更新：2026-03-08 00:30  
> 创建原因：标准化飞书文档生成流程，解决空白文档问题

---

## 📋 Skill 定义

**名称：** 飞书文档生成 Skill  
**编号：** SKILL-FEISHU-DOC-001  
**触发：** 用户要求生成飞书文档时

**一句话描述：** 生成长文档到飞书，分章节写入，避免空白文档问题

---

## 🎯 目标

**解决什么问题：**
- ❌ 长文件一次性写入 → 返回空白文档
- ❌ 使用 write 模式覆盖整个文档
- ❌ 文档生成后未单独发送链接
- ✅ 分章节写入，避免 400 错误
- ✅ 区分 write（首次）和 append（增量）
- ✅ 生成后单独发送文档链接

**核心价值：**
- 稳定生成飞书文档（无空白）
- 支持长文档（分章节写入）
- 方便用户查找（单独发送链接）

---

## 🔄 工作流程（6 步标准化流程）

```
🆕 第 0 步：维护版头信息（版本/时间/内容/人）
  ↓
第 1 步：提取 AI 生成的结论文字
  ↓
第 2 步：创建空白飞书文档（create 动作）
  ↓
第 3 步：分章节写入内容（write/append 选择）
  ↓
第 4 步：处理 400 错误（分块写入）
  ↓
第 5 步：单独发送文档链接到对话框
```

---

## 📝 详细步骤

### 🆕 第 0 步：维护版头信息（版本/时间/内容/人）

**目标：** 在文档开头维护版本信息，方便追踪变更历史

**版头格式：**
```markdown
# 文档标题

> **版本：** V{主版本}.{次版本}.{修订号}  
> **创建时间：** YYYY-MM-DD HH:mm  
> **最后更新：** YYYY-MM-DD HH:mm（更新说明）  
> **维护方式：** 三线同步（飞书 + MD + TXT）
```

**版本信息内容：**
- **版本号：** V{主版本}.{次版本}.{修订号}（如 V2.0、V1.1）
- **更改时间：** YYYY-MM-DD HH:mm（亚洲/上海时区）
- **更改内容：** 简要说明本次更新内容
- **更改人：** 阿福（AI 助理）

**处理逻辑：**
```powershell
# 生成版头信息
$version = "V$major.$minor.$patch"
$currentTime = Get-Date -Format "yyyy-MM-dd HH:mm"
$updateNote = "本次更新说明"

$versionHeader = @"
# $docTitle

> **版本：** $version  
> **创建时间：** $createTime  
> **最后更新：** $currentTime（$updateNote）  
> **维护方式：** 三线同步（飞书 + MD + TXT）

---

"@

# 版头放在文档最开头，在所有章节之前
$fullContent = $versionHeader + $chapterContent
```

**输出：**
- 版头信息（Markdown 格式）
- 版本号
- 更新时间
- 更新说明

**示例：**
```markdown
# AI 专业术语知识库

> **版本：** V2.0  
> **创建时间：** 2026-03-08 00:25  
> **最后更新：** 2026-03-08 00:32（标准化流程测试）  
> **维护方式：** 三线同步（飞书 + MD + TXT）

---
```

**原子动作编号：** ATOM-FEISHU-DOC-000（新建）

---

### 第 1 步：提取 AI 生成的结论文字

**目标：** 从 AI 分析结果中提取要写入飞书文档的内容

**输入：**
- AI 生成的结论文字（Markdown 格式）
- 文档标题
- 文档结构（章节划分）

**处理：**
```powershell
# 提取结论文字
$conclusionText = $aiResult.conclusion

# 解析章节结构
$chapters = Parse-Chapters $conclusionText

# 每个章节包含：
# - title: 章节标题
# - content: 章节内容（Markdown）
# - blocks: 预估 block 数量（按 50 字符/block）
```

**输出：**
- 章节列表（数组）
- 总 block 数

---

### 第 2 步：创建空白飞书文档

**动作：** `feishu_doc -action create`

**参数：**
- `title`: 文档标题
- `content`: **留空**（不写入内容，避免空白文档）

**示例：**
```powershell
$createResult = feishu_doc `
    -action "create" `
    -title "AI 专业术语知识库 V2.0"

$docToken = $createResult.document_id
$docUrl = $createResult.url
```

**返回：**
- `document_id`: 文档 Token
- `url`: 文档链接
- `title`: 文档标题

**⚠️ 注意：**
- ❌ 不要在 create 时写入长内容（会导致空白文档）
- ✅ 只创建空白文档，内容后续写入

---

### 第 3 步：分章节写入内容

**关键决策：** 选择 write 还是 append？

| 场景 | 动作 | 说明 |
|------|------|------|
| **首次写入** | `write` | 写入第 1 个章节（≤200 blocks） |
| **增量更新** | `append` | 追加后续章节 |
| **完全重写** | `write` | 覆盖整个文档（谨慎使用） |
| **单个 block 更新** | `update_block` | 更新指定 block |

**写入逻辑：**
```powershell
# 第 1 章：使用 write
feishu_doc `
    -action "write" `
    -doc_token $docToken `
    -content $chapters[0].content

# 第 2-N 章：使用 append
for ($i = 1; $i -lt $chapters.Count; $i++) {
    feishu_doc `
        -action "append" `
        -doc_token $docToken `
        -after_block_id $lastBlockId `
        -content $chapters[$i].content
    
    # 更新 lastBlockId
    $lastBlockId = $result.block_ids[-1]
}
```

**⚠️ write 模式严重警告：**
- ❌ `write` 会覆盖整个文档！
- ✅ 仅在首次写入或完全重写时使用
- ✅ 增量更新必须用 `append`
- ✅ 单个 block 更新用 `update_block`

---

### 第 4 步：处理 400 错误（分块写入）

**问题：** 长文件一次性写入 → 400 错误 → 空白文档

**原因：** 单次写入超过限制（约 200 blocks）

**解决方案：** 分块写入（每块 30-50 blocks）

**分块逻辑：**
```powershell
# 计算分块
$blockSize = 40  # 每块 40 blocks
$chunks = Split-IntoChunks $content $blockSize

# 第 1 块：write
feishu_doc `
    -action "write" `
    -doc_token $docToken `
    -content $chunks[0]

# 后续块：append
for ($i = 1; $i -lt $chunks.Count; $i++) {
    feishu_doc `
        -action "append" `
        -doc_token $docToken `
        -after_block_id $lastBlockId `
        -content $chunks[$i]
    
    $lastBlockId = $result.block_ids[-1]
}
```

**分块大小建议：**
- 短文档（<200 blocks）：一次性写入
- 中等文档（200-500 blocks）：分 2-3 块
- 长文档（>500 blocks）：分 5-10 块

**检查清单：**
- [ ] 预估总 block 数
- [ ] 决定分块数量
- [ ] 第 1 块用 write
- [ ] 后续块用 append
- [ ] 记录每个 block_id

---

### 第 5 步：单独发送文档链接

**要求：** 文档链接单独发送，不要附在回复里

**原因：** 附在回复里搜不到，单独发送方便以后查找

**示例：**
```powershell
# ❌ 错误：附在回复里
"文档已生成：https://feishu.cn/docx/XXX"

# ✅ 正确：单独发送
message `
    -action "send" `
    -message "## 📄 飞书文档已生成`n`n**标题：** AI 专业术语知识库 V2.0`n`n🔗 **链接：** https://feishu.cn/docx/XXX`n`n已单独发送，方便你以后通过对话记录查找！" `
    -target $userId
```

**消息模板：**
```markdown
## ✅ 飞书文档已生成！

**📄 文档标题：** [标题]

🔗 **文档链接：** [链接]

已单独发送到对话框，方便你以后通过对话记录查找！
```

---

## 📊 示例对比

### 错误做法 vs 正确做法

| 步骤 | ❌ 错误 | ✅ 正确 |
|------|--------|--------|
| **创建** | `create -content "长内容"` | `create`（空白文档） |
| **写入** | 一次性写入全部内容 | 分章节写入 |
| **模式** | 全部用 write | 第 1 章 write，后续 append |
| **分块** | 不分块 | 长文档分块（30-50 blocks/块） |
| **发送** | 附在回复里 | 单独发送链接 |

---

### 成功案例：AI 术语知识库（2026-03-08 00:25）

**文档信息：**
- 标题：AI 专业术语知识库 V2.0
- Token: `KVgQdxnlVoiPbexfKR3cnEIWnId`
- 链接：https://feishu.cn/docx/KVgQdxnlVoiPbexfKR3cnEIWnId
- 内容：26 个术语，6 大分类

**执行流程：**
1. ✅ 提取 AI 生成的术语内容
2. ✅ 创建空白文档（create）
3. ✅ 分章节写入（write + append）
4. ✅ 无 400 错误
5. ✅ 单独发送文档链接

**结果：** 文档正常显示，无空白

---

## 🔗 关联动作

### 前置动作
- AI 分析生成结论文字

### 后置动作
- message 工具发送文档链接

### 复用原子动作
- ATOM-FEISHU-028：写入飞书文档
- ATOM-DELIVERY-010：飞书发送文字

---

## ✅ 检查清单

### 执行前
- [ ] **维护版头信息（版本/时间/内容/人）**
- [ ] 提取结论文字（Markdown 格式）
- [ ] 解析章节结构
- [ ] 预估总 block 数
- [ ] 决定分块策略

### 执行中
- [ ] create 创建空白文档
- [ ] 第 1 章用 write（≤200 blocks）
- [ ] 后续章节用 append
- [ ] 长文档分块（30-50 blocks/块）
- [ ] 记录每个 block_id

### 执行后
- [ ] 文档内容完整显示
- [ ] 无空白文档问题
- [ ] 单独发送文档链接
- [ ] 链接可正常访问

---

## ⚠️ 常见错误

### 错误 1：create 时写入长内容

```
❌ 错误：feishu_doc -action create -content "长内容"
后果：返回空白文档
✅ 正确：feishu_doc -action create（留空）
```

### 错误 2：误用 write 模式

```
❌ 错误：增量更新用 write
后果：覆盖整个文档（500 blocks → 1 block）
✅ 正确：增量更新用 append
```

### 错误 3：不分块写入长文档

```
❌ 错误：一次性写入 500 blocks
后果：400 错误，空白文档
✅ 正确：分块写入（30-50 blocks/块）
```

### 错误 4：文档链接附在回复里

```
❌ 错误：附在回复底部
后果：用户搜不到文档
✅ 正确：单独发送消息
```

---

## 💡 核心原则

> **分章节写入，避免空白文档！**

**关键点：**
1. ✅ create 创建空白文档（不写入内容）
2. ✅ 第 1 章用 write（≤200 blocks）
3. ✅ 后续章节用 append
4. ✅ 长文档分块（30-50 blocks/块）
5. ✅ 单独发送文档链接

**口诀：**
- 创建要空白
- 写入分章节
- 长文要分块
- 链接单独发

---

## 📁 文件位置

**MD 模块：** `skills/feishu-document-generation/SKILL.md`

**TXT 说明：** `skills/feishu-document-generation/SKILL.txt`（待创建）

---

## 🎯 使用示例

### 场景 1：生成术语知识库

```
用户：在飞书给我同步创建一个术语知识库的飞书文档吧

AI 执行：
1. 提取术语内容（26 个词汇，6 大分类）
2. create 创建空白文档
3. 分章节写入（基础概念→大模型→Agent→协议→算法→工具）
4. 每章用 append（第 1 章用 write）
5. 单独发送文档链接
```

### 场景 2：更新现有文档

```
用户：更新术语库，添加 6 个新术语

AI 执行：
1. 提取新增内容（6 个术语）
2. append 追加到文档末尾
3. 更新版本号和更新时间
4. 单独发送更新通知
```

### 场景 3：生成长文档（>500 blocks）

```
用户：生成项目解决方案文档

AI 执行：
1. 解析章节结构（10 章，约 600 blocks）
2. create 创建空白文档
3. 分块写入（每块 40 blocks，共 15 块）
4. 第 1 块 write，后续 14 块 append
5. 单独发送文档链接
```

---

_分章节写入 | 避免空白文档 | 链接单独发送 | 2026-03-08 00:30_


---

## 🎯 2026-03-14 重大更新（Thomas 要求）

### Thomas 的完整文档偏好（今日固化）

**1. 拆分 Block 写入（16:10 要求）**
- ✅ 每个章节独立 Block
- ✅ 使用 append 多次调用
- ✅ 禁止一次性写入整个文档
- ✅ 目标：5+ 个 Block

**2. 开通编辑权限（多次强调）**
- ✅ create 时设置 grant_to_requester: true
- ✅ 参数位置正确（顶层）
- ✅ 验证 Thomas 有编辑权限

**3. Markdown 表格（16:58 要求）**
- ✅ 使用 Markdown 表格语法
- ✅ 禁止使用 create_table 工具
- ✅ 飞书自动渲染

**4. 文件编辑用 Out-File（16:16 要求）**
- ✅ 禁止使用 edit 工具
- ✅ 使用 PowerShell Out-File
- ✅ 强制 UTF8 编码
- ✅ 验证写入成功

**5. 强制记忆检索（16:37 要求）**
- ✅ 创建文档前调用 memory_search
- ✅ 查询历史教训
- ✅ 避免重复犯错

---

### 标准化流程（2026-03-14 版）

**步骤 1：记忆检索**
`powershell
memory_search(query="拆分 Block 飞书文档 历史教训")
`

**步骤 2：创建文档**
`json
{
  "action": "create",
  "title": "文档标题",
  "folder_token": "",
  "grant_to_requester": true  // ✅ 关键！
}
`

**步骤 3：验证权限**
- 检查返回结果确认 grant_to_requester: true

**步骤 4：拆分 Block 写入**
`json
// Block 1
{
  "action": "append",
  "doc_token": "xxx",
  "content": "# 标题\n\n简介..."
}

// Block 2
{
  "action": "append",
  "doc_token": "xxx",
  "content": "## 第 1 章\n\n内容..."
}

// Block 3（表格用 Markdown）
{
  "action": "append",
  "doc_token": "xxx",
  "content": "| 列 1 | 列 2 |\n|------|------|\n| 值 1 | 值 2 |"
}
`

**步骤 5：验证**
- Block 数量 >= 5
- 表格正常显示
- Thomas 有编辑权限

**步骤 6：发送链接**
`json
{
  "action": "send",
  "message": "✅ 文档已创建：https://feishu.cn/docx/xxx"
}
`

---

### 检查清单（2026-03-14 版）

**创建前：**
- [ ] memory_search 查询历史
- [ ] 规划 Block 结构（5+ 个）
- [ ] 准备 grant_to_requester: true

**创建中：**
- [ ] 用 create 不用 write
- [ ] 用 append 多次调用
- [ ] 表格用 Markdown

**创建后：**
- [ ] 验证 doc_token
- [ ] 验证权限
- [ ] 验证 Block 数量
- [ ] 验证表格显示

---

**记住：这是 Thomas 的强制要求！永久生效！**
