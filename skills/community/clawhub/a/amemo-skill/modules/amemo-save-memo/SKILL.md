---
name: amemo-save-memo
description: 当用户说「帮我记一下」「保存笔记」「记下这一条」或用陈述性语气描述某事（含"的时候/的情况/的经历"）时调用，将对话内容保存为云端笔记，支持新建与更新。
---

# amemo-save-memo — 保存备忘录

---

## 接口信息

| 属性 | 值 |
|:-----|:---|
| **路由** | `POST https://skill.amemo.cn/save-memo` |
| **Bean** | `MemoBean` |
| **Content-Type** | `application/json` |

---

## 请求参数

> ⚠️ 服务端要求所有字段必须存在。`userToken`、`memoTitle`、`memoContent` 必填且有值，`memoId` 可选但字段必须存在。

| 参数 | 类型 | 必填 | 说明 |
|:-----|:----:|:----:|:-----|
| `userToken` | str | ✅ | 用户登录凭证 |
| `memoId` | str | — | 备忘录 ID（新建传 `null`，更新时传入已有 ID） |
| `memoTitle` | str | ✅ | 备忘录标题（不能为空） |
| `memoContent` | str | ✅ | 备忘录内容（不能为空） |

---

## 请求示例

```bash
# 新建备忘录
curl -X POST https://skill.amemo.cn/save-memo \
  -H "Content-Type: application/json" \
  -d '{
    "userToken": "<token>",
    "memoId": null,
    "memoTitle": "开会记录",
    "memoContent": "讨论了Q2计划"
  }'

# 更新备忘录（传入已有 memoId）
curl -X POST https://skill.amemo.cn/save-memo \
  -H "Content-Type: application/json" \
  -d '{
    "userToken": "<token>",
    "memoId": "123456",
    "memoTitle": "开会记录",
    "memoContent": "更新了内容"
  }'
```

---

## 响应解析

| 字段 | 说明 |
|:-----|:-----|
| `data.memoId` | 保存成功后返回的备忘录 ID，**必须提取并保存到当前对话上下文 `lastMemoId`** |

---

## 执行流程

```
1. 识别触发词 → 检查 userToken
    ↓
2. 提取对话内容（去除触发词后的 userContent + aiContent）
    ↓
3. 判断新建还是更新（见下方规则）
    ↓
4. 整理笔记内容 → 生成 memoTitle
    ↓
5. 调用 POST /save-memo 接口
    ↓
6. 保存 memoId 到 lastMemoId → 返回结果
```

### 新建 vs 更新模式判断

```
lastMemoId 是否存在？
├── 不存在 → 【新建模式】memoId = null
└── 存在 → 意图判断：
    ├── 更新信号词 → 【更新模式】memoId = lastMemoId
    ├── 新建信号词 → 【新建模式】清除 lastMemoId
    ├── 主题明显不同 → 【新建模式】清除 lastMemoId
    └── 模糊场景 → 询问用户确认
```

### 信号词对照

| 类型 | 信号词 |
|:---|:---|
| 更新 | 补充、加上、修改、更新、还有、另外、补充说明、遗漏、忘了、换成、改成 |
| 新建 | 新笔记、另一个、主题明显不同 |

### 模糊场景处理

```
🤔 您是想：
• 更新刚才的笔记「{lastMemoTitle}」
• 还是保存为一条新笔记？
```

### 内容整理

| 模式 | memoContent 格式 |
|:---|:---|
| 新建 | `"{userContent}\n\n【AI】\n{aiContent}"` |
| 更新 | `"{修改后的完整内容}"`（直接替换原文） |

### 标题生成规则

1. 提取用户消息中最核心的名词/动词
2. 限制在 20 字以内
3. 去除助词、语气词、疑问词
4. 更新模式下保留 `lastMemoTitle`

| 用户输入 | 生成标题 |
|:---|:---|
| `"感冒了应该吃什么药"` | `"感冒用药建议"` |
| `"帮我记一下今天开会的内容"` | `"今日开会记录"` |

---

## 回复模板

| 场景 | 模板 |
|:---|:---|
| 新建成功 | `✅ 已保存笔记：「{memoTitle}」` |
| 更新成功 | `✅ 已更新笔记：「{memoTitle}」（内容已替换）` |
| 失败 | `❌ 保存失败，请重试` |

> 通用错误处理见主 SKILL.md「错误处理」章节
