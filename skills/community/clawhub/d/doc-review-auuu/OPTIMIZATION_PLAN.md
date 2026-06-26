# doc-review-Auuu Skill 优化方案

**版本**: v2.8.0 → v2.9.0  
**日期**: 2026-04-17  
**基于**: 实际审查过程中发现的问题

---

## 问题总结

### 1. 权限授权问题（高优先级）

**问题描述**：
- 需要多次授权：`space:document:retrieve` → `docx:document:create` → `docx:document:write_only`
- 每次授权都中断流程，用户体验差

**根本原因**：
- Skill 未在开始前进行完整的权限检查
- 权限是在执行具体操作时才发现缺失

**优化方案**：
在"第0部分：能力边界"之前添加"权限预检查"部分

```markdown
## 第-1部分：权限预检查（必须首先执行）

### 检查清单

在开始任何审查操作前，必须先检查以下权限：

1. **文档读取权限**：`space:document:retrieve` 或 `docs:document:readonly`
2. **文档创建权限**：`docx:document:create` 或 `docx:document:write_only`
3. **文档写入权限**：`docx:document:write_only`

### 检查方法

```bash
# 检查文档读取权限
lark-cli drive files list --params '{"folder_token":"test"}' --dry-run

# 检查文档创建权限
lark-cli docs +create --title "test" --dry-run

# 检查文档写入权限
lark-cli docs +update --doc "test" --dry-run
```

### 缺失权限处理

如果发现权限缺失，**一次性获取所有缺失权限**：

```bash
# 组合授权命令
lark-cli auth login --scope "space:document:retrieve,docx:document:write_only"
```

**重要**：不要在执行过程中逐个授权，要在开始前一次性完成所有授权。
```

---

### 2. 文档类型自动识别问题（中优先级）

**问题描述**：
- 不能自动识别文档类型
- 需要询问用户，增加交互次数

**优化方案**：
在"步骤1：接收审查请求"中添加自动识别规则

```markdown
### 步骤1：接收审查请求

#### 1.1 文档类型自动识别（优先）

在询问用户之前，先尝试自动识别文档类型：

**识别规则**：

| 文档标题/内容关键词 | 推断类型 |
|-------------------|---------|
| 包含"综述"、"Survey"、"调研"、"文献回顾" | 文献调研 |
| 包含"方案设计"、"技术方案"、"架构设计"、"路线图" | 方案推演 |
| 包含"实验"、"复现"、"评估"、"测试" | 实验设计 |
| 包含"产品介绍"、"宣传"、"对外发布" | 对外材料 |
| 包含"复现"、"demo"、"调试" | 实验设计 |

**识别流程**：
1. 从文档标题提取关键词
2. 从文档开头200字提取关键词
3. 匹配上述规则
4. 如果置信度 > 80%，自动识别并告知用户
5. 如果置信度 ≤ 80%，询问用户确认

#### 1.2 用户确认

```
根据文档标题和内容，我判断这是"文献调研"类型的文档。
是否正确？（如不正确，请告知正确类型）
```
```

---

### 3. AI对话链接检测不准确（高优先级）

**问题描述**：
- 漏检了豆包链接（`www.doubao.com`）
- 错误地将CSDN博客链接标记为AI对话链接

**根本原因**：
- 检测规则不明确
- 没有明确排除技术博客平台
- 豆包的域名格式特殊

**优化方案**：
更新"第3部分：AI对话链接检测"

```markdown
## 第3部分：AI对话链接检测（严格定义）

### ⚠️ 重要：仅检测AI对话/助手平台

**必须严格遵守**：只检测用户与AI进行对话的分享链接，不包括：
- 技术博客（CSDN、掘金、博客园等）
- 问答社区（知乎、Stack Overflow等）
- 代码仓库（GitHub、GitLab等）
- 论坛/社区（V2EX、Reddit等）

### 检测平台列表

从 `config/ai_platforms.yaml` 读取，包括：

**AI对话/助手平台**：
- ChatGPT: `chatgpt.com`、`chat.openai.com`
- Claude: `claude.ai`
- Kimi: `kimi.moonshot.cn`、`moonshot.cn`
- 通义千问: `tongyi.aliyun.com`、`qwen.aliyun.com`、`qwen.ai`
- 豆包: `doubao.com`、`bots.oceanengine.com` ⚠️ **注意豆包主域名是 doubao.com**
- 智谱清言: `zhipuai.cn`、`chatglm.cn`
- 文心一言: `wenxin.baidu.com`、`yiyan.baidu.com`
- Gemini: `gemini.google.com`、`aistudio.google.com`
- Copilot: `copilot.microsoft.com`

### 检测方法

**步骤1**：使用正则表达式精确匹配

```bash
# 正确的检测模式
grep -iE "(chatgpt\.com|chat\.openai\.com|claude\.ai|kimi\.moonshot\.cn|doubao\.com|tongyi\.aliyun\.com|zhipuai\.cn|wenxin\.baidu\.com|gemini\.google\.com|copilot\.microsoft\.com)"
```

**步骤2**：验证链接格式

AI对话分享链接通常包含：
- ChatGPT: `/share/` 或 `/c/`
- Claude: 无特定路径格式
- 豆包: `/thread/` ⚠️ **注意：豆包链接不是对话分享，而是社区帖子**

**步骤3**：特殊处理

对于豆包链接：
- 如果是 `doubao.com/thread/` → 这不是对话分享链接，是社区帖子
- 如果是 `doubao.com/chat/` 或类似 → 这是对话链接
- **建议**：将豆包社区帖子标记为"非正式来源"，而非"AI对话链接"

### 排除规则

**必须排除**以下链接模式：
- CSDN: `blog.csdn.net`、`\.csdn\.net`
- 掘金: `juejin.cn`
- 知乎: `zhihu.com`
- GitHub: `github.com`
- Stack Overflow: `stackoverflow\.com`

### 检测结果报告

**如果检测到AI对话链接**：
```markdown
## 🤖 AI对话链接检测

⚠️ **检测到AI对话链接**

| 平台 | 链接 | 位置 |
|------|------|------|
| ChatGPT | https://chatgpt.com/share/xxx | 第X段 |
| 豆包社区 | https://www.doubao.com/thread/xxx | 第X段 |

**风险提示**：
- AI对话链接可能包含敏感讨论或未验证的信息
- 豆包社区链接属于非正式讨论，建议替换为原始论文或官方文档
```

**如果未检测到**：
```markdown
## 🤖 AI对话链接检测

✅ 未检测到AI对话链接
```

### 常见错误示例

❌ **错误**：将 CSDN 博客链接列为 AI 对话链接
✅ **正确**：在"引用规范"部分指出"使用了非正式博客来源"

❌ **错误**：将豆包社区帖子列为 AI 对话链接
✅ **正确**：在"引用规范"部分指出"使用了非正式社区讨论"
```

---

### 4. lark-cli 命令规范问题（中优先级）

**问题描述**：
- 使用了 `docs +fetch "URL"` 而不是 `docs +fetch --doc "URL"`
- 参数格式不正确导致命令失败

**优化方案**：
添加"lark-cli 命令规范"部分

```markdown
## 附录A：lark-cli 命令规范

### 常用命令正确格式

#### 文档读取

```bash
# ✅ 正确
lark-cli docs +fetch --doc "文档URL或token"

# ❌ 错误（位置参数）
lark-cli docs +fetch "文档URL"
```

#### 文档创建

```bash
# ✅ 正确
lark-cli docs +create --title "文档标题" --markdown "文档内容"

# ❌ 错误（缺少参数）
lark-cli docs +create "文档标题"
```

#### 文档更新

```bash
# ✅ 正确
lark-cli docs +update --doc "文档token" --mode overwrite --markdown "内容"

# ❌ 错误（缺少mode）
lark-cli docs +update --doc "文档token" --markdown "内容"
```

#### 文件夹列表

```bash
# ✅ 正确
lark-cli drive files list --params '{"folder_token":"token"}'

# ❌ 错误（位置参数）
lark-cli drive files list "token"
```

### 命令模式说明

| 操作 | 命令 | 必需参数 | 可选模式 |
|------|------|---------|---------|
| 读取文档 | `docs +fetch` | `--doc` | - |
| 创建文档 | `docs +create` | `--title`, `--markdown` | - |
| 更新文档 | `docs +update` | `--doc`, `--mode` | `overwrite`, `append`, `replace_range` |
| 列出文件 | `drive files list` | `--params` | - |

### 模式参数

- `overwrite`: 完全覆盖文档内容
- `append`: 追加内容到文档末尾
- `replace_range`: 替换指定范围
```

---

### 5. 文档创建流程优化（中优先级）

**问题描述**：
- 创建文档时因权限问题需要多次重试
- 汇总表的创建/追加逻辑不清晰

**优化方案**：
添加"文档创建最佳实践"部分

```markdown
## 附录B：文档创建最佳实践

### 创建流程

1. **权限确认**：确保已获取 `docx:document:write_only` 权限
2. **创建报告**：使用 `docs +create` 创建新文档
3. **保存链接**：记录返回的 `doc_url`
4. **更新汇总表**：
   - 先尝试读取现有汇总表
   - 如果存在，使用 `overwrite` 模式追加新行
   - 如果不存在，创建新汇总表

### 汇总表管理

**汇总表结构**：
```markdown
| 审查日期 | 文档名称 | 文档类型 | 文档链接 | AI对话链接 | 审查状态 | 审查报告链接 |
```

**追加新记录**：
1. 读取现有汇总表内容
2. 解析出所有现有记录
3. 添加新记录到末尾
4. 使用 `overwrite` 模式重新写入完整表格

**示例**：
```bash
# 读取现有汇总表
EXISTING=$(lark-cli docs +fetch --doc "汇总表token")

# 追加新记录
NEW_CONTENT="${EXISTING}
| 2026-04-17 | 新文档 | 文献调研 | URL | - | ✅ | URL |"

# 重新写入
lark-cli docs +update --doc "汇总表token" --mode overwrite --markdown "$NEW_CONTENT"
```

### 错误处理

如果创建失败：
1. 检查权限：`lark-cli auth status`
2. 查看错误信息中的 `hint` 字段
3. 根据提示进行授权
4. 重试创建操作

如果更新汇总表失败：
1. 确认汇总表文档 ID 正确
2. 确认有写入权限
3. 如果汇总表不存在，创建新表而非更新
```

---

### 6. 文档内容过大处理（低优先级）

**问题描述**：
- 文档内容过大时输出被保存到临时文件
- 需要额外读取操作

**优化方案**：
添加"大文档处理"部分

```markdown
## 附录C：大文档处理策略

### 检测大文档

当 `lark-cli docs +fetch` 返回包含：
```
"persisted-output": "Output too large (X.KB)"
```

### 处理方法

**方法1：使用 jq 提取关键信息**
```bash
lark-cli docs +fetch --doc "URL" | jq '.data.mark[:1000]'
```

**方法2：保存到临时文件后分段读取**
```bash
# 保存完整输出
OUTPUT=$(lark-cli docs +fetch --doc "URL")

# 提取文件路径
FILE=$(echo "$OUTPUT" | grep -oP 'Full output saved to: \K[^ ]+')

# 读取文件内容
head -n 500 "$FILE"
```

**方法3：使用 offset 分批读取**
```bash
# 读取前500行
lark-cli docs +fetch --doc "URL" | jq -r '.data.mark' | head -n 500

# 读取500-1000行
lark-cli docs +fetch --doc "URL" | jq -r '.data.mark' | sed -n '500,1000p'
```

### AI对话链接检测（大文档）

对于大文档，使用流式处理：
```bash
lark-cli docs +fetch --doc "URL" | jq -r '.data.mark' | grep -iE "(chatgpt\.com|doubao\.com|...)"
```
```

---

## 版本更新

### v2.9.0（优化版本）

**新增**：
- 权限预检查流程
- 文档类型自动识别
- AI对话链接检测的严格定义和排除规则
- lark-cli 命令规范说明
- 文档创建最佳实践
- 大文档处理策略

**修改**：
- 更新 AI 链接检测规则，明确排除技术博客
- 改进豆包链接的处理方式
- 完善错误处理流程

**删除**：
- 无

---

## 实施建议

1. **立即实施**（高优先级）：
   - 权限预检查
   - AI对话链接检测规则更新
   - lark-cli 命令规范

2. **短期实施**（1周内）：
   - 文档类型自动识别
   - 文档创建最佳实践

3. **长期优化**（持续改进）：
   - 大文档处理策略
   - 错误处理自动化
