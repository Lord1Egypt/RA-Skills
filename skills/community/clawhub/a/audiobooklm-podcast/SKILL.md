---
name: audiobooklm-podcast
description: 基于新音剪创作平台以及珠峰AI自研音色，提供播客创作、内容管理、音频生成、专辑上架等功能。适用于用户提出"播客生成"、"播客制作"等需求。
homepage: https://aigc.ximalaya.com
---

# audiobooklm-podcast

`audiobooklm_mcp` 的标准播客/有声书生产链路。用户提供文本(或让用户先生成),最终产出可上架的章节音频。

---

## 核心原则

1. **每一步可选择的操作都要征求用户意见**
2. **工具调用前必须先问用户确认，禁止自动决定**
3. **使用播客类音色时优先选择 category 为"播客"的音色**
4. **整章合成用 chapter_task_create，不要逐段 task_create**
5. **先混音再上架，顺序不能乱**

---

## Step 0 · 环境自检

调用任意 `mcp__audiobooklm_mcp__*` 工具时，如果返回 401/403/unauthorized/token expired/connection refused 等错误，暂停业务流程并提示用户配置 MCP。

**配置指引：**
> 看起来你还没接入 `audiobooklm_mcp`，按以下 4 步完成配置：
> 1. 注册/登录 https://aigc.ximalaya.com/user
> 2. 创建制作组，生成 API Token
> 3. 把 MCP 服务写入配置：
> ```jsonc
> {
>   "mcpServers": {
>     "audiobooklm_mcp": {
>       "type": "http",
>       "url": "https://aigc.ximalaya.com/audiobooklm/mcp",
>       "headers": {
>         "Authorization": "Bearer <Token>"
>       }
>     }
>   }
> }
> ```
> 4. 重启服务，确认mcp已连接成功(需要结合当前环境给出具体的重启提示)

---

## 标准流程

### 1. 确认信息

开始前必须确认以下信息：

| 字段 | 是否必需 | 处理方式 |
|---|---|---|
| 文本内容 | 必需 | 用户已给直接用；让你生成则先出文案确认 |
| 书籍 | 必需 | 询问：新建还是用已有？ |
| 章节名 | 必需 | 询问用户确认 |
| 文本形态 | 必需 | 普通旁白/单人播客 vs 多人对话（决定导入工具） |
| 音色 | 必需 | 调用 list_tts_voices 向用户展示候选 |
| 专辑 | 可选 | 仅上架时需要，询问：新建/已有/不上架 |

---

### 2. 确定书籍

**询问用户：新建书籍还是用已有书籍？**

- **新建** → 向用户确认书名后调用：
  ```
  book_create(book_name="<书名>", book_type="podcast")
  ```

- **已有** → 用 `read_abs(scope={"domain":"books"})` 拉取书架，列出最近 10 本让用户选择

---

### 3. 创建章节

根据文本形态选择工具：

**普通旁白/单人播客 → `podcast_import`**
```
podcast_import(
  book_id=<book_id>,
  chapter_name="<章节名>",  # 新建章节时必填
  script_lines=["文本1", "文本2", ...], # 单人播客只需要传入文本列表，不需要角色标识
)
```

**多人对话 → `podcast_import`**
```
podcast_import(
  book_id=<book_id>,
  chapter_name="<章节名>",  # 新建章节时必填
  script_lines=["[角色名] 文本1", "[角色名] 文本2", ...] # 多人播客需要给出每段文本的角色名
)
```

**注意：**
- 多人播客每行格式必须为 `[角色名] 文本`
- 单人播客每行只需要文本，不需要角色名，格式为`文本`
- chapter_name 和 chapter_id 二选一：新建章节传 chapter_name，追加到已有章节传 chapter_id
- 返回 chapter_id 和 characters (角色名与 character_id 映射)

---

### 4. 列出音色

调用 `list_tts_voices()` 获取音色列表。

**筛选建议：**
- 播客类优先选 category 包含"播客"的音色
- 根据角色特征推荐合适的音色给用户选择
- 向用户展示 3-5 个候选 + 简短描述

**询问用户**：每个角色分别选哪个音色？

---

### 5. 绑定音色到角色

```
mcp__audiobooklm_mcp__patch_abs(
  scope={"domain": "book", "book_id": <book_id>},
  operations=[
    {
      "op_id": "op-<角色序号>",
      "type": "update_character",
      "character_id": <character_id>,
      "patch": {"speaker_id": <speaker_id>},
      "reason": "绑定音色"
    }
    // 多个角色用逗号分隔
  ]
)
```

⚠️ **注意**：
- 每个 operation 都要有唯一 op_id
- type 是 "update_character" 不是 "op"

---

### 6. 整章合成

使用 `chapter_task_create` 一次提交整章：

```
mcp__audiobooklm_mcp__chapter_task_create(
  book_id=<book_id>,
  chapter_id=<chapter_id>
)
```

返回 task_ids 列表。

---

### 7. 查询任务结果

```
mcp__audiobooklm_mcp__task_query(
  task_ids=[<task_ids列表>],
  wait_timeout=120  # 可根据段落数调整
)
```

所有段落 status=succeeded 后继续。

---

### 8. 章节混音

```
mcp__audiobooklm_mcp__chapter_audio_mix(
  book_id=<book_id>,
  chapter_id=<chapter_id>
)
```

⚠️ **顺序要求**：必须先完成第 7 步，再调用混音。

返回 `audio_url` 即章节完整音频。

---

### 9. 上架专辑（可选）

**询问用户**：需要上架到专辑吗？新建/已有/不上架？

- **新建专辑** → 询问专辑名后调用：
  ```
  mcp__audiobooklm_mcp__create_album(
    album_name="<专辑名>",
    book_content="<简介>"  # 可选，让 AI 生成封面
  )
  ```

- **已有专辑** → 用户提供 album_id

- **上架**：
  ```
  mcp__audiobooklm_mcp__upload_audio_to_album(
    album_id=<album_id>,
    audio_url=<第8步返回的audio_url>
  )
  ```

---

## 交付内容

完成后告诉用户：

- 书籍 ID / 章节 ID
- 选用的音色 (speakerId + 名称)
- **章节完整音频 URL**
- **编辑页面**：https://aigc.ximalaya.com/edit/<book_id>/<chapter_id>
- **账单或充值页面**: https://aigc.ximalaya.com/payment

---

## 常见问题

| 现象 | 原因 | 解决 |
|---|---|---|
| 找不到 `mcp__audiobooklm_mcp__*` | MCP 未注册 | 配置 MCP |
| 401/403/unauthorized | Token 无效/过期 | 重新生成 Token |
| patch_abs validation_failed | 缺 op_id 或 type | 检查 operation 格式 |
| task_query 返回 processing | 异步任务未完成 | 继续轮询 task_query |
| 音色不对 | character 未绑定 speaker | 重新绑定步骤 |
| create_album 失败 | 需要 book_content | 传入简介文本 |

---

## 多人对话模板

适用于用户已提供：book_id + 章节名 + 对话脚本（格式为 `[角色名] 文本`）

### 流程
1. `podcast_import` 导入章节 → 获得 chapter_id 和 characters
2. `list_tts_voices` 列出音色 → 用户为每个角色选择
3. `patch_abs` 绑定音色 → 每个角色都要绑
4. `chapter_task_create` 提交整章
5. `task_query` 查询结果
6. `chapter_audio_mix` 混音

