---
name: audiobook
description: 基于音剪AI创作平台以及珠峰AI自研音色，提供有声书创作、内容管理、音频生成、专辑上架等能力。适用于用户提出“有声书生成”“小说配音”“章节音频制作”等需求。
homepage: https://aigc.ximalaya.com
9. 旁白书风语义匹配（强约束，2026-05-23 新增，必须严格执行）：
   - 适用范围：整本书多播匹配场景。
   - 旁白候选池：仅从 `tag` 包含“旁白”的音色中选择。
   - 旁白禁用名单：默认剔除 `大宇茶馆`、`单田芳`；若用户明确新增禁用项，必须一并剔除。
   - 旁白选型方式：必须执行“书风语义打分”，禁止按候选顺序直接取第一个。
     - `category` 命中书风标签优先（例如：玄幻/仙侠/悬疑/历史）。
     - `description` 命中叙事气质优先（例如：宏大、沉稳、浑厚、热血、史诗、说书感、代入感）。
     - 在同等语义命中下，优先性别与年龄段更匹配的旁白音色。
   - 绑定落地规则：
     - `character_type=1`（旁白角色）必须绑定到上述“语义最优旁白音色”。
     - 非旁白角色必须按角色匹配规则全量分配音色，不允许因 `word_count` 低而兜底到旁白。
   - 一致性校验：提交 `patch_abs(update_character)` 后，必须用 `character_query(book_id=...)` 回查并输出：
     - 旁白角色是否 100% 命中目标旁白音色；
     - 排名字数 `>5000` 的角色是否 100% 命中旁白兜底（若存在）；
     - 若任一项未达 100%，必须继续补齐，禁止进入后续合成流程。


10. 音色列表缓存规则（强约束，2026-05-23 新增，必须严格执行）：
   - `list_tts_voices` 默认优先使用本地全量缓存，禁止每次实时拉取。
   - 缓存时效为 `1h`：
     - 缓存未超过 `1h`：直接使用本地缓存参与匹配；
     - 缓存超过 `1h`：先刷新一次全量音色，再写回本地缓存并用于本次匹配。
   - 必须记录并输出：`cache_last_update_time`、`cache_age_minutes`、`cache_hit`（true/false）。
   - 若缓存文件缺失或损坏，允许立即全量拉取一次并重建缓存。

---

# audiobook

`audiobooklm_mcp` 的标准有声书生产链路。用户提供文本http可直接下载链接（或先协助生成文本），最终产出可上架的章节音频。

---

## 核心原则

1. **每一步可选择的操作都要征求用户意见**
2. **工具调用前必须先问用户确认，禁止自动决定**
3. **音色推荐优先贴合角色设定（性别必须一致、年龄尽可能接近、性格与叙事语气一致）**
4. **整章合成用 chapter_task_create，不要逐段 task_create**
5. **先混音再上架，顺序不能乱**
6. **拆章默认2000字/章需先确认用户，并提示按4字/s估算时长**
7. **单播时所有角色统一按旁白处理；多播时按角色与音色适配流程执行**
8. **MCP tool 调用失败时，禁止自行切换/尝试其他 tools；必须直接报错并等待用户指令**
9. **多播角色音色匹配时，主角与核心配角尽可能使用不同音色，避免主要角色间音色重复**

---

## Step 0 · 环境自检（强制前置，必须最先执行）

⚠️ **在询问用户任何业务问题（文本来源、书籍、章节名等）之前，必须先确认 MCP 服务可用。**

**检查方式（二选一即可）：**
1. 查看当前会话已注册的 MCP 工具列表，是否存在 `mcp__audiobooklm_mcp__*` 前缀的工具（例如 `mcp__audiobooklm_mcp__book_create`、`mcp__audiobooklm_mcp__list_tts_voices`）。
2. 或调用一个轻量只读工具试探，例如 `mcp__audiobooklm_mcp__list_tts_voices(exclude_role_voice=True)`。

**判定与处理：**

| 情况 | 处理 |
|---|---|
| 工具列表中存在 `mcp__audiobooklm_mcp__*` 且调用正常 | ✅ 进入第 1 步 |
| 找不到 `mcp__audiobooklm_mcp__*` 工具 | ❌ 输出下方配置指引，**停下来等用户配置并重启**，不要继续问业务问题 |
| 工具存在但返回 401/403/unauthorized/token expired/connection refused | ❌ 同上，Token 失效或服务不可达，提示用户检查 Token 并重启 |

**配置指引（未配置时输出给用户）：**
> 检测到当前会话尚未接入 `audiobooklm_mcp`，需要先完成 MCP 配置再继续。按以下 4 步操作：
> 1. 注册/登录 https://aigc.ximalaya.com/user/center
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
>
> 配置并重启后告诉我，我再继续帮你制作有声书。

**重要：** 在用户确认 MCP 配置完成并重启之前，**不要**询问文本来源、书籍、章节等任何业务信息，避免做无用功。
**提示信息：** 结合当前环境，给出用户简单的MCP配置方法，并提示用户如何重启能够生效。

---

## 标准流程

### 1. 确认信息
开始前必须确认以下信息：

| 字段   | 是否必需 | 处理方式                                                  |
|------|---|-------------------------------------------------------|
| 文本内容 | 必需 | 用户已给纯文本可直接用；若提供文本链接则先执行 chapter_split 再继续；让你生成则先出文案确认 |
| 书籍   | 必需 | 询问：新建还是用已有？                                           |
| 演绎形式 | 必需 | 单播 vs 多播 （决定音色匹配策略）                                   |
| 旁白   | 必需 | 调用 list_tts_voices 展示候选，询问用户使用哪个音色还是自动推荐              |
| 专辑   | 可选 | 后置确认：完成角色音色匹配后再询问“新建/已有/不上架”                         |

---

### 2. 确定书籍
**询问用户：新建书籍还是用已有书籍？**

- **新建** → 向用户确认书名后调用：
  ```
  book_create(book_name="<书名>", book_type="audiobook")
  ```

- **已有** → 用 `read_abs(scope={"domain":"books"})` 拉取书架，列出最近 10 本让用户选择

---

### 3. 链接文本预处理（用户提供文本链接时必做）
当用户提供的是 TXT/Markdown/文档下载链接，而不是直接粘贴文本时，先调用 `chapter_split`。默认按 2000 字/章拆分，但执行前必须先让用户确认。拆章完成后，必须使用拆章返回的 zip 包走批量导入。

```
chapter_split(
  content_file="<文本链接>",
  filename="<文件名，可从链接推断>",
  max_chapter_length=2000
)
```

**执行前确认（必做）：**
- 明确告知用户：将按默认 `2000字/章` 拆分。
- 给出时长估算（按 `4字/s`）：
  - 单章预计时长（秒）= `章节字数 / 4`
  - 单章预计时长（分钟）= `章节字数 / 240`
  - 以默认 2000 字为例：约 `500秒`（约 `8分20秒`）/章
- 询问用户是否按该参数继续；用户确认后再执行 `chapter_split`。

**处理要求：**
- 成功后获取拆章产物中的 `zip` 包地址（或文件标识），作为批量导入入参
- 拆分失败（下载失败/格式不支持）时，提示用户改为直接粘贴文本或提供可访问的新链接

---

### 3.5 本地文件上传（用户传本地文件时必做）
当用户提供的是本地文件路径（非 http/https 链接）时，必须先上传文件，拿到 `file_path` 后再传给后续步骤（如 `chapter_split` / 批量生产流程）。

上传接口示例：
```bash
curl --location --request POST 'https://aigc.ximalaya.com/audiobooklm/oauth/api/common/upload' --header 'Authorization: {{TOKEN}}' --form 'file=@"/本地文件绝对路径/xxx.txt"'
```

响应体取值要求（强约束）：
- 仅使用 `data.file_info.file_path` 作为后续入参
- 不要使用本地路径直接传给远端工具
- 若上传失败或 `file_path` 为空，必须报错并等待用户处理

处理要求：
- 调用上传接口前先征求用户确认
- 成功后向用户回传 `filename` 与 `file_path` 供确认
- 本地文件场景下，`filename` 去掉后缀默认作为书名（例如 `重生之奶爸的幸福生活.txt` -> `重生之奶爸的幸福生活`）
- 若用户未单独指定书名，默认使用上述文件名（去后缀）创建书籍
- 再进入 `chapter_split` 或后续流程

---

### 4. 批量导入章节（internal）
拆章成功后，使用拆章后的 zip 包调用 `chapter_batch_import` 批量创建章节：

```
chapter_batch_import(
  book_id=<book_id>,
  chapter_zip_file="<chapter_split 返回的 zip 包>"
)
```

然后调用 `chapter_batch_import_status` 轮询导入状态，直到完成：

```
chapter_batch_import_status(
  book_id=<book_id>,
  import_task_id=<chapter_batch_import 返回的任务ID>
)
```

**处理要求：**
- 进入角色音色匹配前，必须先执行 `chapter_batch_import_status` 并读取 `state`（`0`=处理中，`1`=完成，`2`=失败）。
- 仅当 `state=1` 时，才可进入角色音色匹配。
- 当 `state=0` 时，继续按 1 分钟间隔轮询并主动回报进度。
- 当 `state=2` 时，立即中止后续匹配并反馈失败原因与重试建议。
- 若部分章节失败，需将失败章节列表反馈给用户并确认是否重试。
- 批量导入成功后，读取章节清单并与用户确认本次导入范围。
- 批量导入成功后，必须立刻征询用户确认“是否进入角色音色匹配环节”。
- 仅在用户明确确认后，才进入角色音色自动匹配流程（见下一步）。

---

### 5. 批量导入后角色音色自动匹配（必做）
对该书角色执行自动匹配，目标是“整本书全角色完成 `speaker_id` 绑定”。

执行流程（唯一口径）：
1. 拉取角色：`character_query(book_id=...)`
2. 拉取音色池：优先本地缓存（`<=1h` 直接用缓存，`>1h` 先刷新再用）
3. 按模式执行匹配：
   - 单播：所有角色统一使用旁白音色（或用户指定单一音色）
   - 多播：按本文档 `N` 章节的硬约束 + 软匹配执行
4. 先向用户展示“全量角色-音色清单”，再等待用户明确确认
5. 用户确认后调用 `patch_abs(update_character)` 批量写入 `speaker_id`
6. 写入后再次 `character_query` 回查，输出 `total_count` / `unbound_count`
7. `character_query` 回查结果需由用户确认后，再进入下一步
8. 仅当 `unbound_count=0` 且用户已确认回查结果时，允许进入合成与混音

强制约束（不得违反）：
- 禁止只处理前 N 个角色（如前 200）；整本书匹配必须覆盖全部角色。
- 禁止在未获用户确认前执行任何 `update_character` 写入。
- 禁止在 `unbound_count>0` 时进入 `chapter_task_create` / `chapter_audio_mix`。
- 禁止用 `read_abs cast` 代替 `character_query` 做绑定校验。

阶段输出（每阶段必报）：
- 已完成内容
- 下一步动作
- 预计完成时间
- 当前风险/阻塞（若有）

`character_query` 回查补充约束：
- 当 `total_count > 1000` 时，回查前必须主动提示用户：角色量较大，结果展示与核对可能消耗额外 token。
- 完成回查后，需等待用户确认（例如“确认继续”）；未确认前不得进入合成链路。

---

### 6. 创建章节（非批量场景备用）
根据文本形态选择导入格式（统一使用 `podcast_import`）：

**旁白叙述 / 单人朗读**
```
podcast_import(
  book_id=<book_id>,
  chapter_name="<章节名>",
  script_lines=["文本1", "文本2", ...]
)
```

**多人对话 / 角色演绎**
```
podcast_import(
  book_id=<book_id>,
  chapter_name="<章节名>",
  script_lines=["[角色名] 文本1", "[角色名] 文本2", ...]
)
```

**注意：**
- 单播场景下可忽略角色前缀，统一按旁白合成。
- 多人对话每行格式必须为 `[角色名] 文本`
- 单人朗读每行只需要文本，不需要角色名
- `chapter_name` 和 `chapter_id` 二选一：新建章节传 `chapter_name`，追加到已有章节传 `chapter_id`
- 返回 `chapter_id` 和 `characters`（角色名与 `character_id` 映射）

---

### 7. 列出音色
调用 `list_tts_voices(exclude_role_voice=False)` 获取音色列表。

**筛选建议：**
- 旁白优先选择清晰、稳定、长听不疲劳的音色
- 角色音色按年龄、性别气质、性格差异进行区分
- 向用户展示 3-5 个候选 + 简短描述

**询问用户**：是否接受全量自动匹配结果；若不接受，再对关键角色人工改配后重新出全量清单确认。

**流程优化（强约束）**：专辑上架相关确认后置到本步骤之后。即：先完成角色音色匹配确认与绑定，再询问用户“新建专辑 / 已有专辑 / 不上架”。

---

### 8. 绑定音色到角色
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
  ]
)
```

⚠️ **注意：**
- 每个 operation 都要有唯一 `op_id`
- `type` 必须是 `update_character`

---

### 9. 整章合成
使用 `chapter_task_create` 一次提交整章：

```
mcp__audiobooklm_mcp__chapter_task_create(
  book_id=<book_id>,
  chapter_id=<chapter_id>
)
```

返回 `task_ids` 列表。

---

### 10. 查询任务结果
```
mcp__audiobooklm_mcp__task_query(
  task_ids=[<task_ids列表>],
  wait_timeout=120
)
```

所有段落 `status=succeeded` 后继续。

---

### 11. 章节混音
```
mcp__audiobooklm_mcp__chapter_audio_mix(
  book_id=<book_id>,
  chapter_id=<chapter_id>
)
```

⚠️ **顺序要求**：必须先完成第 11 步，再调用混音。

返回 `audio_url` 即章节完整音频。

---

### 12. 上架专辑（可选，后置确认）
**询问用户**：需要上架到专辑吗？新建/已有/不上架？

- **新建专辑** → 询问专辑名后调用：
  ```
  mcp__audiobooklm_mcp__create_album(
    album_name="<专辑名>",
    book_content="<简介>",
    style_name="<需从风格列表中选择，不得编造>"
  )
  ```

**风格列表**: ['亲密特写漫风', '古韵二次元水彩绘风', '日系水彩现代言情插画风', '日系潮流杂志漫画插画风', '现言手绘插画风','现言都市立绘风', '言情Q版漫画插画风', '古言新中式国风插画', '古言双人唯美古风', '都市大男主霸气风','都市异能/高武风', '韩漫精致美男风', '神豪 / 商业霸总风', '暗黑悬疑 / 都市诡秘风', '二次元轻小说风','港风/年代写实风', '娱乐明星 / 偶像风', '后宫 / 美女群像都市风', '国漫热血-玄幻', '反派修仙-玄幻','卡通轻松-玄幻', '玄幻宏大场景风', '仙侠修仙-玄幻', '末世废土风', '宏大宇宙风', '帝王霸业风', '古风权谋朝堂风','铁血战场风', '东方意境/水墨古风', '历史大男主立绘风', '后宫红颜/群像风', '二次元轻历史爆笑风']

- **已有专辑** → 用户提供 `album_id`

- **上架**：
  ```
  mcp__audiobooklm_mcp__upload_audio_to_album(
    album_id=<album_id>,
    audio_url=<第12步返回的audio_url>,
    title=<专辑音频标题>
  )
  ```

上架完成后，交付用户看的站内地址目前只要求返回专辑 URL：
- 专辑 URL：`https://www.ximalaya.com/album/<album_id>`

注意：`uploaded_tracks[].audio_url` 若是 COS 或 mix 文件地址，只能作为底层音频文件地址，不等同于用户可访问的喜马拉雅站内页面 URL。当前 `upload_audio_to_album` 未稳定返回 `sound_id`，不要编造或推断 `https://www.ximalaya.com/sound/<sound_id>`。

---

## 交付内容

完成后告诉用户：

- 书籍 ID / 章节 ID（批量导入时给出章节 ID 列表）
- 选用的音色（speakerId + 名称）
- **章节完整音频文件 URL**：第 12 步混音返回的 `audio_url`（通常是 COS/mix 文件地址）
- **专辑 URL**：如果执行了上架，返回 `https://www.ximalaya.com/album/<album_id>`
- **编辑页面**：https://aigc.ximalaya.com/edit/<book_id>/<chapter_id>
- **账单或充值页面**：https://aigc.ximalaya.com/payment
- **编辑或充值页面需要在用户中心切换制作组身份登录操作**：https://aigc.ximalaya.com/user

---



## 本次实战沉淀（2026-05）

### A. MCP 调用握手（强约束）

生产环境调用 `https://aigc.ximalaya.com/audiobooklm/mcp` 时，必须使用以下顺序：

1. `initialize`
2. `notifications/initialized`
3. 再调用 `tools/list` / `tools/call`

若跳过第 2 步，后续接口可能返回 `-32602 Invalid request parameters`。

---

### B. 批量导入参数与状态（已验证）

- `chapter_batch_import` 入参使用：
  - `book_id`
  - `zip_file_path`（不是 `chapter_zip_file`）
- `chapter_batch_import_status` 只需 `book_id`

状态建议按汇总字段同步：
- `state`
- `processedCount`
- `totalCount`
- `successCount`
- `failureCount`

避免直接输出 `records` 全量明细（数据量极大，影响可读性）。

---

### C. chapter_id 来源（重要）

- `chapter_batch_import_status.response.records[].id` 不是可用于 `chapter_task_create` 的章节ID。
- 合成/混音时使用的 `chapter_id`，应从 `read_abs(scope={"domain":"book","book_id":...})` 的 `content_abs.chapter_ids` 获取。

---

### D. 角色音色匹配口径

- 角色匹配执行规则：
  - 性别严格一致（男->男声，女->女声，禁止错配）
  - 人设/性格优先贴合
  - 年龄段尽可能接近
- `read_abs` 可能不返回 `speaker_id` 字段；该情况不作为异常。
- 角色与音色绑定结果回查，优先使用 `character_query(book_id=...)`，并从 `data.result.items` 读取 `character_id/character_name/speaker_id/mix_mode`。
- **强约束**：执行 `patch_abs(update_character)` 之前，必须先向用户展示“完整角色-音色匹配清单（全量）”，得到用户确认后才能写入。
- **强约束**：匹配策略以“最佳匹配”优先，不得默认退化为仅男/女两音色方案；若需要降级，必须先征得用户明确同意。
- 匹配完成状态可优先以页面可见结果为准，再辅以后端接口信息。

---

### F. 角色合并（merge_characters）参数与故障处理

- `merge_characters` 必须使用以下字段名：
  - `source_character_ids`
  - `target_character_id`
- 不要使用 `source_ids` / `target_id`，否则会返回 `validation_failed`。
- 若返回 `merge_reference_inconsistent`（配置不一致无法合并）：
  1. 先用 `update_character` 将源角色对齐到目标角色（至少 `speaker_id`、`mix_mode`、`gender`、`age_stage`）
  2. 再重试 `merge_characters`

---

### E. 生产进度同步规范（用户体验）

当用户要求“及时试听”时：
- 不等全部章节完成再汇报。
- 每章 `chapter_audio_mix` 一旦返回 `audio_url`，立即单独回传该章链接。
- 章节仍在处理中时，明确标注 `PROCESSING`。

---

### H. 批量导入状态轮询间隔（强约束，2026-05-21 新增）

- 对 `chapter_batch_import_status` 的轮询频率，默认固定为 **每 1 分钟 1 次**。
- 未经用户主动要求，不得自行改为更高频（如 5s / 10s / 20s）。
- 如需调整间隔，必须先征求用户确认并按用户指定执行。
- 在批量导入进行中（`processedCount < totalCount`）时，Agent 必须按该间隔**主动回报**进度，无需等待用户催促。
- 主动回报应持续到导入完成（`processedCount = totalCount`）或明确失败（出现失败状态/失败计数增长并已告知用户）。

---

### I. 音色池拉取工具约束（强约束，2026-05-21 新增）

- 拉取音色池统一使用 `list_tts_voices`。
- 不使用 `tts_voice_list`。
- 若历史流程或提示词出现 `tts_voice_list`，执行时必须自动替换为 `list_tts_voices` 并继续，不中断流程。

---

### J. 执行协同与推进规范（强约束，2026-05-21 新增）

1. 进入角色音色匹配前必须先查询 `chapter_batch_import_status`，并基于 `state` 判定：仅 `state=1` 可进入；`state=0` 持续轮询；`state=2` 中止并反馈失败。
2. 每个阶段结束后必须同步：已完成内容、下一步动作、预计完成时间，避免无感停顿。
3. 若某一步必须用户确认，需先准备好可执行产物（如全量匹配清单），再一次性发起确认，禁止先空等。

---

### K. `character_type` 枚举口径（强约束，2026-05-21 新增）

- `0` -> `未知`
- `1` -> `旁白`
- `2` -> `主角`
- `3` -> `配角`
- `4` -> `路人`

---

### O. 角色绑定校验接口约束（强约束，2026-05-22 新增）

- 角色音色绑定完整性（`speaker_id` 是否已写入）必须使用 `character_query(book_id=...)` 进行最终校验。
- 禁止使用 `read_abs(scope.path=\"cast\")` 作为角色音色绑定校验依据；该接口用于内容结构读取，不作为 `speaker_id` 校验口径。
- 在进入 `chapter_task_create` / `chapter_audio_mix` 前，必须先基于 `character_query` 输出：
  - `total_count`
  - `unbound_count`（`speaker_id` 为空/0）
  - 结论：`可继续合成` 或 `需先补齐绑定`

---

### L. 角色音色绑定提交闸门（强约束，2026-05-21 新增）

- 在执行任何 `patch_abs(update_character)` 写入前，必须先向用户展示完整的“角色-音色匹配清单（全量）”，并获得用户明确确认（例如“确认提交”）。
- 未获得确认时，严禁提交任何角色音色绑定写操作（包括部分提交、试探性提交、预提交）。
- 到达写入步骤时，必须先进行并输出以下检查项：
  - `是否已展示全量匹配清单：是/否`
  - `是否已收到用户明确确认：是/否`
- 若任一检查项为“否”，流程必须停止在确认阶段，不得继续写入。

---

### M. 整本书音色覆盖率约束（强约束，2026-05-22 新增）

- 当执行“整本书匹配”时，所有角色必须完成音色绑定（`speaker_id` 不得为空）。
- 若存在未绑定角色，禁止进入后续 `chapter_task_create`、`task_query`、`chapter_audio_mix` 等合成/混音步骤。
- 如发现未绑定角色，必须先补齐角色音色绑定，再继续后续生产流程。

---

### N. 整本书旁白与角色音色匹配策略（强约束，2026-05-23 整理版）

整本书多播匹配采用“旁白规则”和“角色规则”分离执行，先旁白后角色，最后统一回查。

前置条件：
- 角色按整本 `word_count` 从高到低排序后执行匹配。
- 旁白兜底仅允许用于排序名次 `>5000` 的角色。

1. 旁白匹配（`character_type=1`）
- 候选池：仅 `tag` 包含“旁白”的音色。
- 禁用名单：默认剔除 `大宇茶馆`、`单田芳`；用户新增禁用项必须一并剔除。
- 限额过滤：`specified=true` 的旁白音色必须先剔除；若剔除后无候选，必须报错并等待用户指令。
- 优先级（严格顺序）：
  - 第一优先：`category` 匹配（按书风类别）。
  - 第二优先：性别、年龄等硬约束。
  - 第三优先：软约束打分（`description` / `personality` / `tag` 等）。
- 产出：确定“全书旁白基准音色”。

2. 低频/长尾角色兜底规则（强约束）
- 角色必须先按 `word_count` 从高到低排序（整本维度）。
- 仅排序名次 `>5000` 的角色允许走旁白兜底；名次 `<=5000` 的角色必须走正常角色匹配逻辑。
- 除上述“名次 >5000”场景外，不允许因字数少直接归旁白；仅 `character_type=1` 的旁白角色默认绑定旁白音色。

3. 角色匹配（非旁白）
- 优先级（严格顺序）：
  - 第一优先：性别、年龄等硬约束。
  - 第二优先：软约束打分（`feature` / `tag` / `description` / `personality` / `category`）。
- 分层约束：
  - 主角（`character_type=2`）必须优先独立音色。
  - `word_count >= 1000` 的角色必须优先独立音色。
  - 配角（`character_type=3`）且 `word_count >= 300` 优先独立音色；`100 <= word_count < 300` 可按性别年龄复用。
  - 路人/未知（`character_type=4/0`）且 `word_count >= 100` 可受控复用。
- 复用控制：
  - 主角之间禁止复用同一音色（除非候选池不足且用户明确确认）。
  - 核心配角优先分配未使用音色，尽量与主角和核心配角区分。
- 禁止项：
  - 不得使用“音色名称是否数字编号/是否好读”作为优先级或降级依据。

4. 提交闸门（必须先满足）
- 提交 `patch_abs(update_character)` 前，必须先向用户展示“全量角色-音色匹配清单”，并获得明确确认。

5. 回查闸门（必须先满足）
- 写入后必须使用 `character_query(book_id=...)` 回查并输出：
  - `total_count`
  - `unbound_count`
  - 旁白角色命中率（目标旁白音色）
  - `word_count` 排名 `>5000` 的角色是否 100% 命中旁白兜底（若存在）
  - `word_count` 排名 `<=5000` 的角色是否 100% 按角色规则匹配（不走旁白兜底）
- 若任一项不达标（含 `unbound_count > 0`），必须继续补齐，禁止进入合成流程。

---

### G. 合成与查询结果判读（强约束）

- `chapter_task_create` 返回判读：
  - 先校验顶层：`success/code/msg`，再读取 `data`。
  - `data` 关键字段：`book_id`、`chapter_id`、`task_ids`、`submitted_paragraph_ids`、`submitted_count`、`skipped_finished_count`、`finished_paragraph_ids`。
  - 若 `submitted_count>0`，表示本次确实提交了新合成任务；后续必须使用返回的 `task_ids` 查询状态。
  - 若 `submitted_count=0` 且 `skipped_finished_count>0`，表示该章已完成（或无需重复提交），不视为失败。
  - 若 `submitted_count=0` 且 `skipped_finished_count=0`，视为异常态：需输出原始响应 `body` 并排查。
- `task_query` 结果解析：
  - 仅当 `task_ids` 非空时调用 `task_query`。
  - 优先从 `data.result.items` 读取任务明细（兼容旧结构时可回退到 `data.items/data.tasks`）。
  - 明细中重点字段：`task_id`、`status/task_state`、`audio_url`、`error_message`。

---

## 常见问题

| 现象 | 原因 | 解决 |
|---|---|---|
| 找不到 `mcp__audiobooklm_mcp__*` | MCP 未注册 | 配置 MCP |
| 401/403/unauthorized | Token 无效/过期 | 重新生成 Token |
| patch_abs validation_failed | 缺 op_id 或 type | 检查 operation 格式 |
| merge_characters validation_failed | 字段名错误（如 `source_ids`/`target_id`） | 改为 `source_character_ids` / `target_character_id` |
| merge_reference_inconsistent | 源/目标角色配置不一致 | 先 `update_character` 对齐 `speaker_id`/`mix_mode`/`gender`/`age_stage`，再合并 |
| chapter_batch_import 失败 | zip 包无效或入参错误 | 检查 chapter_split 产物与 book_id，重新发起导入 |
| chapter_batch_import_status 长时间 processing | 批量导入未完成 | 持续轮询 status，必要时告知用户稍后重试 |
| 角色过多导致匹配耗时高 | 角色数过大 | 仍需全量匹配；可先产出“核心角色优先”预览清单，但最终必须补齐全部角色再进入合成 |
| 自动匹配覆盖率低 | 音色库与角色设定差异大 | 输出未匹配清单并让用户人工指定关键角色音色 |
| task_query 返回 processing | 异步任务未完成 | 继续轮询 task_query |
| 音色不对 | character 未绑定 speaker | 重新执行绑定步骤 |
| create_album 失败 | 需要 book_content | 传入简介文本 |

---

## 多角色演绎模板

适用于用户已提供：`book_id` + 章节名 + 对话脚本（格式为 `[角色名] 文本`）

### 流程
1. 若文本来自链接：`chapter_split` → `chapter_batch_import` → `chapter_batch_import_status`；若用户直接给脚本：`podcast_import`
2. `list_tts_voices` 列出音色并自动匹配角色：必须覆盖全部角色；可先展示核心角色预览，再补齐全量并确认
3. `patch_abs` 批量绑定匹配到的音色 → 输出已匹配/未匹配清单，再让用户确认是否人工调整
4. `chapter_task_create` 提交整章
5. `task_query` 查询结果
6. `chapter_audio_mix` 混音
