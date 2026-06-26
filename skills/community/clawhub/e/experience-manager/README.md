# Experience Manager

> Agent 经验管理工具 - 创建、分享、学习经验包

---

## 为什么要做这个 Skill？

### 现在的痛点

1. **经验无法沉淀**
   - Agent 每次犯错后，教训只存在于对话中
   - 下次遇到同样问题，可能重复犯错
   - 经验无法跨会话、跨 Agent 传递

2. **知识无法共享**
   - 每个 Agent 独立学习，效率低下
   - 一个 Agent 掌握的技能，其他 Agent 需要重新学习
   - 没有标准化的经验传递机制

3. **学习成本高**
   - 新 Agent 需要从零开始学习
   - 最佳实践散落在各处文档中
   - 没有统一的知识库

### 这样做的意义

**建立 Agent 经验分享网络**

```
┌─────────────┐     创建经验包      ┌─────────────┐
│   Agent A   │ ──────────────────→ │  经验市场   │
│  (遇到错误)  │                     │  (zip包)   │
└─────────────┘                     └──────┬──────┘
                                           │
                                           │ 学习经验
                                           ↓
┌─────────────┐                     ┌─────────────┐
│   Agent C   │ ←────────────────── │   Agent B   │
│  (避免错误)  │      分享经验        │  (学习进步)  │
└─────────────┘                     └─────────────┘
```

**核心价值**:
- ✅ **经验可沉淀** - 错误和教训转化为标准化经验包
- ✅ **知识可共享** - Agent 之间可以相互学习
- ✅ **能力可复制** - 新 Agent 快速获得最佳实践
- ✅ **持续进化** - 经验包版本管理，持续改进

---

## 经验包格式 (Schema v1)

```yaml
schema: openclaw.experience.v1
name: feishu-doc-best-practice
description: feishu_doc 操作前必须先检查权限
metadata:
  version: 1.0.0
  author: zhulianxin
soul: references/soul.md
agents: references/agents.md
tools: references/tools.md
skills:
  - feishu_doc
```

---

## 使用方法

### 1. 创建经验包

#### 方式一：从自然语言描述创建

```bash
node scripts/create.mjs "feishu_doc 写入后必须验证 block_count"
```

中文描述需要指定 name:
```bash
node scripts/create.mjs "收到群消息后必须先检查 chat_id" --name=chat-id-check
```

#### 方式二：从记忆中搜索提取经验

**步骤 1: 搜索记忆**
```bash
# 搜索近7天的记忆，查找经验、教训、错误、解决方案
# 查看 memory/ 目录下最近更新的文件
ls -lt ~/.openclaw/workspace/memory/*.md | head -10
```

**步骤 2: 分析记忆内容**
打开记忆文件，寻找以下内容：
- ❌ 错误记录（"失败"、"错误"、"问题"）
- ✅ 解决方案（"修复"、"解决"、"成功"）
- 💡 最佳实践（"应该"、"必须"、"注意"）
- ⚠️ 踩坑记录（"坑"、"陷阱"、"注意点"）

**步骤 3: 提取经验**
从记忆中提取结构化信息：
```
问题场景: Auto ETL 调用 API 时认证失败
错误信息: "未登录，请先登录"
根本原因: aac-client-uid 需要通过 Cookie 传递，而不是 Header
解决方案: 在请求头中添加 Cookie: aac-client-uid=xxx
复用价值: 所有 EasyData 平台开发者都需要
```

**步骤 4: 创建经验包**
```bash
node scripts/create.mjs "EasyData API 调用时 aac-client-uid 需要通过 Cookie 方式传递"
```

#### 方式三：从会话历史中挖掘

**查看近期会话**:
```bash
# 查看会话历史文件
ls -lt ~/.openclaw/agents/main/sessions/*.jsonl | head -5
```

**分析高频问题**:
- 哪些问题被多次问到？
- 哪些错误重复出现？
- 哪些解决方案被多次使用？

**经验提取模板**:
| 字段 | 说明 | 示例 |
|:---|:---|:---|
| 问题场景 | 什么情况下会遇到 | 调用 EasyData API |
| 错误表现 | 具体错误信息 | "未登录，请先登录" |
| 根本原因 | 为什么会这样 | UID 传递方式错误 |
| 解决方案 | 怎么解决 | 使用 Cookie 传递 |
| 复用范围 | 谁会用到 | EasyData 开发者 |
| 优先级 | 高/中/低 | 高 |

**输出**:
- 生成 `~/.openclaw/experiences/packages/{name}.zip`
- 包含 exp.yml 和 references/ 目录

### 2. 学习经验

**学习到当前 Agent**:
```bash
node scripts/learn.mjs ~/.openclaw/experiences/packages/feishudoc.zip
```

**学习到指定 Agent**:
```bash
node scripts/learn.mjs exp.zip --agent=严哥
```

**仅预览变更**:
```bash
node scripts/learn.mjs exp.zip --agent=严哥 --dry-run
```

**自动确认**:
```bash
echo "Y" | node scripts/learn.mjs exp.zip --yes
```

### 3. 查看列表

```bash
node scripts/list.mjs
```

输出示例:
```
📚 经验列表

✅ 已学习 (5)
  feishu-doc-best-practice    v1.0.0  feishu_doc 操作前检查权限
  chat-id-check               v1.0.0  收到群消息后检查 chat_id
  ...

⏳ 未学习 (3)
  browser-timeout             v1.0.0  browser 工具超时处理
  ...
```

### 4. 发布经验到 Hub

```bash
node scripts/publish.mjs ~/.openclaw/experiences/packages/feishu-doc-best-practice.zip
```

### 5. 搜索经验包

```bash
node scripts/search.mjs feishu
node scripts/search.mjs "飞书 文档"
```

### 6. 下载学习他人发布的经验

```bash
node scripts/learn.mjs https://www.expericehub.com:18080/pkg/feishu-doc-best-practice-1.0.0.zip
node scripts/learn.mjs ~/Downloads/feishu-doc-best-practice.zip
```

---

## 工作流程示例

### 场景：记录一个错误教训

**Step 1**: Agent A 遇到错误并记录
```
用户: 你刚才犯了什么错误？
Agent A: 我直接调用了 feishu_doc 导致 400 错误...
```

**Step 2**: 创建经验包
```bash
node scripts/create.mjs "feishu_doc 操作前必须先检查权限"
# 生成: feishu-doc-best-practice.zip
```

**Step 3**: 分享给其他 Agent
```bash
# 复制 zip 包到其他 Agent 可访问的位置
cp ~/.openclaw/experiences/packages/feishu-doc-best-practice.zip /shared/
```

**Step 4**: Agent B 学习经验
```bash
node scripts/learn.mjs /shared/feishu-doc-best-practice.zip --agent=严哥
# 写入到严哥的 SOUL.md 和 AGENTS.md
```

**Step 5**: Agent B 避免同样错误
```
用户: 帮我操作一下飞书文档
Agent B: 好的，我先检查权限...
       （应用了学习到的经验）
```

## 经验提取最佳实践

### 何时创建经验包？

| 场景 | 示例 | 优先级 |
|:---|:---|:---:|
| **踩坑记录** | 花了很长时间解决的问题 | ⭐⭐⭐ |
| **重复错误** | 同一错误出现 2 次以上 | ⭐⭐⭐ |
| **最佳实践** | 发现更好的做事方式 | ⭐⭐⭐ |
| **平台限制** | 发现 API/工具的隐藏限制 | ⭐⭐⭐ |
| **配置陷阱** | 容易被忽略的配置项 | ⭐⭐ |
| **环境差异** | 不同环境的特殊处理 | ⭐⭐ |

### 经验分享流程

```
发现经验 → 验证有效性 → 创建经验包 → 本地测试 → 分享/发布 → 收集反馈
    ↑___________________________________________________________↓
```

---

**愿景**: 让每个 Agent 都能从其他 Agent 的经验中学习，建立真正的 Agent 协作网络。