---
name: drama-ai-studio
description: 本技能通过调用灵伴智能的AI影视工场（DramaAIStudio）平台的多项能力，辅助AI短剧创作者更方便地参与创作，具体包括：项目的创建与管理，剧本的上传与自动分析，资产（角色、场景、道具）的智能提取与图像生成，分镜脚本生成与管理、分镜视频生成等。本技能还支持创建项目的定时巡检任务，将项目的关键节点完成情况即时地通知给创作者，完成生成、查看、评论、反馈和优化的创作闭环。
version: 1.0.2
metadata:
  openclaw:
    primaryEnv: IDRAMA_TOKEN
---

# DramaAIStudio（灵伴智能AI影视工场）

本技能封装了灵伴智能AI影视工场（DramaAIStudio）平台提供的多项 HTTP API，帮助用户在对话中完成：

- **剧目（项目）管理**（§4）：获取剧目列表、创建剧目、获取单个剧目详情；获取剧目统计信息；获取/更新项目默认风格配置
- **剧本管理与资产分析**（§5）：获取剧本集列表、按集上传剧本、按集读取剧本内容、按集删除剧本；剧本资产智能分析，从剧本抽取人物/场景/道具资产并写入资产库
- **资产管理**（§6）：按类型/集数/名称过滤资产列表、创建资产、获取/更新单个资产；辅助生成资产提示词；基于参考图与提示词生成资产图像；查询资产终稿候选图像列表、将单张候选图像设为/取消终稿；对候选图（含终稿）查询/新增评论并将评论标为已解决
- **分镜脚本管理**（§7）：按集读取分镜脚本、分析生成分镜脚本；查询镜头详情；为镜头关联资产；生成/优化镜头提示词；删除镜头
- **分镜视频生成**（§8）：创建/查询分镜视频生成任务、按分镜列出历史成片、按集读取选中成片、对成片视频查询/发表评论并标记已解决

当用户提到「列出所有剧目（项目）」「创建剧目（项目）」「查询剧目（项目）统计信息」「短剧（项目）风格配置」「上传/读取剧本」「剧本分析」「创建资产」「更新资产」「资产列表」「查看资产详情」「生成资产提示词」「生成资产图像」「候选图/终稿评论」「查看/分析分镜」「生成/优化镜头提示词」「生成分镜视频」「分镜成片视频评论/评价」等需求时，可使用本技能文档中列出的对应 API。

当用户提到创建**定时任务**来巡检或查看某个（短剧）项目的资产或分镜的变动情况，可以通过OpenClaw的Cron功能定时调用资产或分镜查询脚本，获得最新的资产或分镜详情，并将发生的变动详情汇报给用户，具体实现方法请参考§3.2中的描述。

**接口详解文件**：§2.2 与 §4～§8 各 HTTP 接口的完整说明（参数、请求/响应示例、错误处理等）位于 `{baseDir}/references/` 下，文件名形如 `ref-*.md`。占位符 `{baseDir}` 与本技能文件 `SKILL.md` 所在目录相同（二者同级，详见各小节文末引用路径）。

---

## 0. 本技能的前置要求（必执行）

1. 读取`MEMORY.md`，检查是否存在「drama-ai-studio技能规则」区块
2. 若已存在则校验一致性，若不存在/内容不完整，将以下规则追加或更新到`MEMORY.md`：
> ### drama-ai-studio技能规则
> 1. **有限发散**：所有功能优先使用本技能提供的平台原生API和标准业务流程，禁止自定义非规范操作
> 2. **先查后做**：调用任何API前必须先读取对应`{baseDir}/references/ref-*.md`文档，核对所有必填参数和格式要求
> 3. **不懂就问**：需求有任何歧义、参数不明确的地方，必须先询问用户确认，绝不猜测执行
> 4. **辅助引导**：每次操作完成后主动列出3-5个下一步可选操作，降低用户决策成本
3. 校验写入成功后再执行后续技能操作，以保证本技能被合理、规范、正确的使用
4. 每次使用本技能后，都要自检对于各项技能规则的遵循情况。

## 1. 本技能的使用方式

- 技能名称：`drama-ai-studio`
- 所有接口统一通过 HTTP 调用：
  - 基础域名示例：`https://idrama.lingban.cn/`
  - 对外网关统一前缀：`/openapi`
  - 最终访问路径形如：`https://idrama.lingban.cn/openapi/drama/...`

智能体需要选择一个支持 HTTP 的工具（如 `http_request` 或 `bash`）发起请求，并在 Header 中附带认证信息。

---

## 2. 认证

### 2.1 在 iDrama API令牌获取页面获取 Token

1. 引导用户在浏览器中打开：`https://idrama.lingban.cn/api-token`。
2. 提示用户在该页面完成登录（如果尚未登录）。
3. 登录成功后，在该页面上获取专用于 OpenClaw 的访问 Token（页面会显示一串 Token，如 `xxxx...`）。
4. 让用户将该 Token 复制并粘贴回对话中，作为后续所有接口调用的认证凭据。

请求头中携带：

```text
Authorization: Bearer <从 idrama API令牌获取页面复制的 token>
```

### 2.2 通过iDrama的账号和密码获取 Token

- 接口：`POST /openapi/uaa/oauth/token`

调用本接口前，请先读取 `{baseDir}/references/ref-2-2-idrama-token.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

### 2.3 其他获取方式

用户也可在 OpenClaw/宿主侧配置环境变量 IDRAMA_TOKEN，或在用户明确同意时将令牌写入技能目录下的 .env 以便后续会话与脚本复用。

---

## 3. 工作模式与业务流程总览

本技能除了支持完成AI短剧的**创作主流程**（从零搭建内容与管线），还支持创建**定时巡检任务**（面向已生成资产或分镜的巡检和评审）。二者共用同一套鉴权与 OpenAPI（§2、§4～§8），智能体可按用户当前 intent 择一为主或组合使用。

进入 §3 相关流程时，智能体**先**引导和辅助用户**安全**地处理访问令牌`IDRAMA_TOKEN`，再执行 3.1 / 3.2 中的业务步骤。

### 3.0 `IDRAMA_TOKEN` 的获取、读取、会话内使用与可选持久化（§3 入口）

1. **读取**（按优先级逐步获取，直至获取到有效的`IDRAMA_TOKEN`）：
   - **环境变量** `IDRAMA_TOKEN`（OpenClaw / 宿主已为进程或技能注入的配置，优先级最高）；
   - **`{baseDir}/.env`** 中 `IDRAMA_TOKEN=` 行（标准 dotenv：`KEY=value`，`#` 为注释；表示用户曾同意持久化到技能目录）；

2. **若已得到非空且有效的令牌**（来自以上任一来源）：
   - 向用户**部分隐藏**展示（例如仅保留头尾各若干字符、中间为 `…`，**不**输出完整串），并说明来源（环境变量 / `.env` / 本轮对话提供）。
   - **询问用户是否更新**。若用户**要更新**，则按 **§2**（页面取 Token 或 `POST /openapi/uaa/oauth/token`）重新取得令牌。

3. **若仍无可用令牌、或调用 §4～§8 任一试请求验证失败（视为无效）**：
   - **直接按 §2** 引导用户完成认证并取得新 `IDRAMA_TOKEN`。

4. **会话内生效**（取得有效令牌后**必须**执行，与是否落盘无关）：
   - 使后续本技能相关 HTTP 调用与 `python {baseDir}/scripts/...` 等子进程能使用该令牌：以实现环境为准，将等价于 **`IDRAMA_TOKEN` 的值**注入当前任务上下文（例如导出环境变量、或由 Gateway 在本轮工具链中传入）。**勿**在聊天中回显完整令牌。

5. **询问并写入 `{baseDir}/.env`（须询问并获得用户明确同意）**：
   - **仅当**用户明确表示同意将令牌**保存在技能包目录**内、供以后会话、Cron 或脚本**无需再次粘贴**时，才**更新或创建** `{baseDir}/.env`：保留该文件其它已有行，仅新增或替换 `IDRAMA_TOKEN=…` 一行。
   - 若用户**未**同意落盘、或仅希望本次会话使用：则**不要**写入 `.env`；后续可依赖用户在 OpenClaw / 宿主侧配置 `IDRAMA_TOKEN`，或下次再在对话中提供。
   - 若落盘：建议用户将 `.env` 限制为仅运行账户可读（具体命令随操作系统而定）。

### 3.1 创作主流程

整体业务围绕「剧目 → 剧本 → 资产 → 分镜脚本 → 分镜视频」的闭环；逐步操作示例见 **§10** 实践案例。

当用户开始创作，并且智能体不确定当前创作的项目ID时，智能体应该先读取 **`{baseDir}/session_state.json`**，获取当前会话关注的项目信息（`id`、`name`、`focused_at`）；

若未获取到有效的当前关注的项目信息，则询问用户要创作的短剧项目。当获取到用户要创作的短剧项目信息后，同步更新 **`{baseDir}/session_state.json`** 中对应字段（ID、名称、关注时间）；

若获取到有效的当前关注的项目信息，将其展示给用户并询问是否继续该项目创作。若用户确认继续，则沿用该项目；若用户改为创作其他短剧项目（包括新建项目），则在完成项目切换后同步更新 **`{baseDir}/session_state.json`** 中对应字段（ID、名称、关注时间）

`{baseDir}/session_state.json` 示例：
```json
{
  "current_project": {
    "id": "12345",
    "name": "校园奇妙夜",
    "focused_at": "2026-04-07T09:30:00Z"
  }
}
```

基本创作流程如下：
```text
1. 创建剧目（短剧项目）（§4.2）
2. 查看剧目统计与风格配置（§4.4、§4.5/4.6）
3. 上传剧本、查看剧集列表、按剧集读取或删除（§5）
4. 按剧集智能分析与提取各类资产（§5.5）
5. 查看资产列表、按需创建资产（§6）
6. 按需辅助生成资产提示词（§6.5），并更新和保存至资产数据
7. 按需为资产生成图像（§6.6）
8. 按剧集智能分析与拆分镜头（§7）
9. 参考资产图像生成分镜视频（§8）
```

**注意事项**：
- 对于创作中任一步骤，中间发生项目切换都要更新`{baseDir}/session_state.json`
- 在创作中的任一步骤，用户都可以按照 §3.2 创建定时巡检任务，智能体可适当引导

### 3.2 定时巡检任务

为了方便制作组中每位成员即时地跟踪了解项目关键节点的完成情况，本技能**仅**支持**直接使用 OpenClaw Gateway 内置 Cron 调度器**来创建**定时巡检任务**，定时查询项目关键节点的变更情况，并将变更详情发送给用户，供其查看和评论。

本技能**仅支持两种巡检任务类型**：（1）资产候选图终稿变更定时巡检；（2）分镜视频终稿变更定时巡检。
当用户想要创建其他类型的定时巡检任务时，需要告知和引导用户创建本技能原生支持的巡检任务类型，若用户执意要创建其他类型的巡检任务，则在告知用户无法保证任务执行结果的前提下，尝试参照**原生支持的巡检任务类型**的实现方式去完成操作。

1. **查看当前 Cron 定时巡检任务**
- 列表：`openclaw cron list`
- 查看某任务运行历史：`openclaw cron runs --id <jobId>`
- 手动触发一次：`openclaw cron run <jobId>`

2. **创建 Cron 定时巡检任务**  
项目变更巡检属于高频后台工作，建议用 **isolated session**，避免污染主会话上下文；若你的 Gateway/主机在整点触发很多任务，可用 `--stagger 30s`（或 `--exact` 强制不抖动）调整触发节奏；通过 `--announce` 和 `--to` 将结果投递回当前所在的通道 `channel` 和 `session` 对话。

- 根据上下文和用户指令，解析得到定时巡检周期为 `cron_time`（比如"*/30 * * * * *"），待巡检的短剧项目id为 `play_id`（比如"12345"）；
- 从当前会话元数据中提取得到当前会话对应的 `channel`（比如feishu/matrix等）和 `session_id`（比如room_id/chat_id等）；

- 创建**资产候选图终稿变更**定时巡检任务时，需要执行以下的命令：

```bash
openclaw cron add \
   --name "iDrama 资产候选图终稿变更通知 play_id=<play_id>" \
   --cron <cron_time> \
   --tz "Asia/Shanghai" \
   --session isolated \
   --message "（1）请用 bash 执行 `IDRAMA_BASE_URL="https://idrama.lingban.cn" python {baseDir}/scripts/sync_project_asset_final_candidates_snapshot.py <play_id> --token <IDRAMA_TOKEN> --quiet`。若输出 status=changed，则向当前会话返回 diff 详情：重点说明哪些 asset_id 的 final_candidate_ids / final_items 发生变化，对于图片或视频，需要给出可点击查看的URL；若 status=initial，提示已建立候选终稿首版快照；若 unchanged 则保持静默。（2）请用 bash 执行 `openclaw cron list`，获取和显示当前的 Cron 定时任务列表，询问用户是否做出调整（创建、启用、停用、修改和删除）。" \
   --announce \
   --channel <channel> \
   --to <session_id>
```

- 创建**分镜视频终稿变更**（各集各分镜**选中视频**汇总）定时巡检任务时，需要执行以下的命令：

```bash
openclaw cron add \
   --name "iDrama 分镜视频终稿变更通知 play_id=<play_id>" \
   --cron <cron_time> \
   --tz "Asia/Shanghai" \
   --session isolated \
   --message "（1）请用 bash 执行 `IDRAMA_BASE_URL="https://idrama.lingban.cn" python {baseDir}/scripts/sync_project_storyboard_selected_videos_snapshot.py <play_id> --token <IDRAMA_TOKEN> --quiet`。若输出 status=changed，则向当前会话返回 diff 详情：按 episode_no、shot_id 列出变更，对于图片或视频，需要给出可点击查看的URL；若 status=initial，提示已建立分镜选中视频首版快照；若 unchanged 则保持静默。（2）请用 bash 执行 `openclaw cron list`，获取和显示当前的 Cron 定时任务列表，询问用户是否做出调整（创建、启用、停用、修改和删除）。" \
   --announce \
   --channel <channel> \
   --to <session_id>
```

3. **修改/停用/删除任务**
- 修改（patch）：`openclaw cron edit <jobId> --cron "*/30 * * * *" --tz "Asia/Shanghai"`
- 停用：`openclaw cron edit <jobId> --disable`
- 启用：`openclaw cron edit <jobId> --enable`
- 删除：`openclaw cron rm <jobId>`

4. **反馈巡检结果，辅助用户完成查看、评审和指导工作**
定时巡检任务每次运行完成后会将 **diff 详情**反馈给用户，用户可以快速掌握项目最新动态（对于图片或视频，需要给出可点击查看的url），开展后续的评审和指导工作。

- 基于资产候选图终稿变更结果，用户可以进行评论，评论结果可通过 OpenAPI 写回后台：**新增评论**（**§6.10**）、**查看已有评论**（**§6.9**）、**将评论标为已解决**（**§6.11**）；**设终稿 / 取消终稿**（**§6.8**），必要时结合 **§6.7** 核对终稿列表；**参照图检索与上传**，并用于候选图生成，用户在智能体辅助下确定更适合的资产视觉特征，并从网络搜索和下载相匹配的图片作为资产参考图，通过 OpenAPI **上传资产参考图到后台**（**§6.12**）
- 基于分镜视频终稿变更结果，用户可以进行评论，评论结果可通过 OpenAPI 写回后台；用户在智能体辅助下确定更适合的分镜视频生成提示词，通过 OpenAPI **创建视频生成任务**（**§8.1**）

---

## 4. 剧目（项目）管理 API

前缀：`/openapi/drama`

### 4.1 GET /openapi/drama/list

获取剧目列表。

调用本接口前，请先读取 `{baseDir}/references/ref-4-1-get-openapi-drama-list.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 4.2 POST /openapi/drama/create

创建新剧目。

调用本接口前，请先读取 `{baseDir}/references/ref-4-2-post-openapi-drama-create.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 4.3 GET /openapi/drama/{play_id}

获取单个剧目详情；找不到返回 404。

调用本接口前，请先读取 `{baseDir}/references/ref-4-3-get-openapi-drama-play-id.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 4.4 GET /openapi/drama/{play_id}/stats

获取剧目统计信息（集数、镜头数、资产数量等）。

调用本接口前，请先读取 `{baseDir}/references/ref-4-4-get-openapi-drama-play-id-stats.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 4.5 GET /openapi/drama/{play_id}/style-config
### 4.6 PUT /openapi/drama/{play_id}/style-config

获取/更新项目默认风格配置。

调用本接口前，请先读取 `{baseDir}/references/ref-4-5-4-6-drama-style-config.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

## 5. 剧本管理与资产分析 API

前缀：`/openapi/drama/{play_id}/scripts`

### 5.1 GET /openapi/drama/{play_id}/scripts

获取剧本集列表。

调用本接口前，请先读取 `{baseDir}/references/ref-5-1-get-openapi-drama-play-id-scripts.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 5.2 POST /openapi/drama/{play_id}/scripts/upload

上传或更新单集剧本文本，支持 `multipart/form-data` 与 `application/json`。

调用本接口前，请先读取 `{baseDir}/references/ref-5-2-post-openapi-drama-play-id-scripts-upload.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 5.3 GET /openapi/drama/{play_id}/scripts/{episode_no}/content

获取指定集剧本原文；不存在时返回 404。

调用本接口前，请先读取 `{baseDir}/references/ref-5-3-get-openapi-drama-play-id-scripts-episode-no-content.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 5.4 DELETE /openapi/drama/{play_id}/scripts/{episode_no}

删除指定集剧本。

调用本接口前，请先读取 `{baseDir}/references/ref-5-4-delete-openapi-drama-play-id-scripts-episode-no.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 5.5 POST /openapi/drama/{play_id}/scripts/analyze

剧本资产智能分析，从原文中抽取场景/角色/道具并更新资产库。

调用本接口前，请先读取 `{baseDir}/references/ref-5-5-post-openapi-drama-play-id-scripts-analyze.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

## 6. 资产管理 API

前缀：`/openapi/drama/{play_id}/assets`

### 6.1 GET /openapi/drama/{play_id}/assets/list

按类型、集数、名称过滤资产列表，并附带封面与是否有终稿图标记。

调用本接口前，请先读取 `{baseDir}/references/ref-6-1-get-openapi-drama-play-id-assets-list.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 6.2 POST /openapi/drama/{play_id}/assets/create

创建新资产。

调用本接口前，请先读取 `{baseDir}/references/ref-6-2-post-openapi-drama-play-id-assets-create.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 6.3 GET /openapi/drama/{play_id}/assets/{asset_id}

获取单个资产详情。

调用本接口前，请先读取 `{baseDir}/references/ref-6-3-get-openapi-drama-play-id-assets-asset-id.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 6.4 PUT /openapi/drama/{play_id}/assets/{asset_id}

更新已有资产的名称、类型、描述、来源集数、**提示词**等。请求体 **至少提供一个**可更新字段；仅允许修改**未软删除**的资产。

调用本接口前，请先读取 `{baseDir}/references/ref-6-4-put-openapi-drama-play-id-assets-asset-id.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 6.5 POST /openapi/drama/{play_id}/assets/prompt-helper/generate

调用大模型 **辅助生成资产图像提示词**：根据资产类型、模式与描述等，经模板渲染后请求文本模型，返回一段可直接用于图像生成的中文提示词。

调用成功后应询问用户是否**进一步优化提示词**，若无优化建议，则提示用户是否**将提示词保存到资产数据**。

调用本接口前，请先读取 `{baseDir}/references/ref-6-5-post-openapi-drama-play-id-assets-prompt-helper-generate.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 6.6 POST /openapi/drama/{play_id}/assets/{asset_type}/{asset_id}/generate_image

资产图片生成：基于用户提示词、提示词模板与参考图调用模型生成图片，并作为新候选图写入对应资产。

调用该请求时，首先查询和确认资产的**用户提示词是否为空**，若为空应提示用户按照 §6.5 生成资产的提示词。

调用本接口前，请先读取 `{baseDir}/references/ref-6-6-post-openapi-drama-play-id-assets-asset-type-asset-id-generate-image.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 6.7 GET /openapi/drama/{play_id}/assets/{asset_type}/{asset_id}/general/candidates/final-candidates

获取该资产下已选为**终稿**的候选图列表，顺序由终稿选中时间等规则决定。

调用本接口前，请先读取 `{baseDir}/references/ref-6-7-get-openapi-drama-play-id-assets-asset-type-asset-id-general-candidates-final-candidates.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 6.8 PUT /openapi/drama/{play_id}/assets/{asset_type}/{asset_id}/general/candidates/{cand_id}/final

将**单张**资产候选图设为终稿或从终稿集合中移除。

调用本接口前，请先读取 `{baseDir}/references/ref-6-8-put-openapi-drama-play-id-assets-asset-type-asset-id-general-candidates-cand-id-final.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 6.9 GET /openapi/drama/{play_id}/assets/{asset_type}/{asset_id}/general/candidates/{cand_id}/comments

获取指定候选图下的评论列表，按创建时间**正序**排列。

调用本接口前，请先读取 `{baseDir}/references/ref-6-9-get-openapi-drama-play-id-assets-asset-type-asset-id-general-candidates-cand-id-comments.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 6.10 POST /openapi/drama/{play_id}/assets/{asset_type}/{asset_id}/general/candidates/{cand_id}/comments

为指定候选图**新增一条评论**。`cand_id` 对应的候选图须已存在。

调用本接口前，请先读取 `{baseDir}/references/ref-6-10-post-openapi-drama-play-id-assets-asset-type-asset-id-general-candidates-cand-id-comments.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 6.11 PATCH /openapi/drama/{play_id}/assets/{asset_type}/{asset_id}/general/candidates/{cand_id}/comments/{comment_id}/resolve

将指定评论标记为**已解决**。

调用本接口前，请先读取 `{baseDir}/references/ref-6-11-patch-openapi-drama-play-id-assets-asset-type-asset-id-general-candidates-cand-id-comments.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 6.12 POST /openapi/drama/{play_id}/assets/{asset_type}/{asset_id}/general/references/create

为指定资产新建一张**参考图**（`multipart/form-data` 上传 `name` 与 `image`）。

调用本接口前，请先读取 `{baseDir}/references/ref-6-12-post-openapi-drama-play-id-assets-asset-type-asset-id-general-references-create.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

## 7. 分镜脚本管理 API

前缀：`/openapi/drama/{play_id}/storyboard`

### 7.1 GET /openapi/drama/{play_id}/storyboard/{episode_no}

获取某集分镜；尚未分析时 `shots` 为空。

调用本接口前，请先读取 `{baseDir}/references/ref-7-1-get-openapi-drama-play-id-storyboard-episode-no.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 7.2 POST /openapi/drama/{play_id}/storyboard/{episode_no}/analyze

触发该集分镜分析：读取该集剧本 → AI 拆分为镜头序列并关联资产。

调用本接口前，请先读取 `{baseDir}/references/ref-7-2-post-openapi-drama-play-id-storyboard-episode-no-analyze.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 7.3 GET /openapi/drama/{play_id}/storyboard/{episode_no}/shots/{shot_id}

获取单个镜头详情，包含 `prompt`、`description`、`original_script` / `original_content`。

调用本接口前，请先读取 `{baseDir}/references/ref-7-3-get-openapi-drama-play-id-storyboard-episode-no-shots-shot-id.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 7.4 POST /openapi/drama/{play_id}/storyboard/{episode_no}/shots/{shot_id}/add-asset

为镜头添加资产（补标），可新建或关联已有资产。

调用本接口前，请先读取 `{baseDir}/references/ref-7-4-post-openapi-drama-play-id-storyboard-episode-no-shots-shot-id-add-asset.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 7.5 POST /openapi/drama/{play_id}/storyboard/{episode_no}/shots/{shot_id}/optimize-prompt

生成或优化分镜视频合成的提示词（专门针对SD2.0智能参考视频生成模式）。

调用本接口前，请先读取 `{baseDir}/references/ref-7-5-post-openapi-drama-play-id-storyboard-episode-no-shots-shot-id-optimize-prompt.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 7.6 DELETE /openapi/drama/{play_id}/storyboard/{episode_no}/shots/{shot_id}

删除指定镜头。

调用本接口前，请先读取 `{baseDir}/references/ref-7-6-delete-openapi-drama-play-id-storyboard-episode-no-shots-shot-id.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

## 8. 参考资产图片生成分镜视频 API

前缀：`/openapi/drama/{play_id}/storyboard-video`

**给智能体：成片视频 `id` 与 视频评论`task_id` 的对应关系**

- **§8.3、§8.4** 返回的每条成片视频在 JSON 里用字段 **`id`** 标识该条任务（§8.4 嵌在 `video` 下时为 **`video.id`**）。
- **§8.5～§8.7**（视频评论）要求传入的 **`task_id`** 与上述 **`id` 是同一值**：只换参数名、不换含义。调用评论接口时，应从 §8.3 列表项或 §8.4 的 `video` 对象读取 **`id`**，**原样**填入 `task_id`。

### 8.1 POST /openapi/drama/{play_id}/storyboard-video/episodes/{episode_no}/shots/{shot_id}/tasks

创建分镜视频生成任务（异步入队）

调用本接口前，请先读取 `{baseDir}/references/ref-8-1-post-openapi-drama-play-id-storyboard-video-episodes-episode-no-shots-shot-id-tasks.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---
### 8.2 GET /openapi/api/ai-tasks/tasks/<task_id>

查询 AI 任务状态与最终执行结果（异步任务通用）

调用本接口前，请先读取 `{baseDir}/references/ref-8-2-get-openapi-api-ai-tasks-tasks-task-id.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 8.3 GET /openapi/drama/{play_id}/storyboard-video/episodes/{episode_no}/shots/{shot_id}/videos

获取该分镜下历史视频列表（包含已生成与上传视频），可直接读取已有视频结果路径。

调用本接口前，请先读取 `{baseDir}/references/ref-8-3-get-openapi-drama-play-id-storyboard-video-episodes-episode-no-shots-shot-id-videos.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 8.4 GET /openapi/drama/{play_id}/storyboard-video/episodes/{episode_no}/selected-videos

获取指定集下各分镜的**视频终稿（选中视频）**（每镜至多一条：有选中则返回选中项，无选中则默认该镜第一条成片，无成片则 `video` 为 `null`）。

调用本接口前，请先读取 `{baseDir}/references/ref-8-4-get-openapi-drama-play-id-storyboard-video-episodes-episode-no-selected-videos.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 8.5 GET /openapi/drama/{play_id}/storyboard-video/video-comments

获取指定成片任务下的**视频评论列表**（`episode_no`、`shot_id`、`task_id` 使用 Query 传递，与路径约定一致）。

调用本接口前，请先读取 `{baseDir}/references/ref-8-5-get-openapi-drama-play-id-storyboard-video-video-comments.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 8.6 POST /openapi/drama/{play_id}/storyboard-video/video-comments

对指定成片任务**发表一条视频评论**（须任务已完成且存在成片路径）。

调用本接口前，请先读取 `{baseDir}/references/ref-8-6-post-openapi-drama-play-id-storyboard-video-video-comments.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 8.7 PATCH /openapi/drama/{play_id}/storyboard-video/video-comments/resolve

将指定视频评论标记为**已解决**。

调用本接口前，请先读取 `{baseDir}/references/ref-8-7-patch-openapi-drama-play-id-storyboard-video-video-comments-resolve.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

### 8.8 PUT /openapi/drama/{play_id}/storyboard-video/episodes/{episode_no}/shots/{shot_id}/videos/{task_id}/selected

将指定分镜视频设为该镜头当前**选中/终稿**视频。

调用本接口前，请先读取 `{baseDir}/references/ref-8-8-put-openapi-drama-play-id-storyboard-video-episodes-episode-no-shots-shot-id-videos-task-id-selected.md`，了解接口的完整说明（参数表、请求/响应示例与错误处理）

---

## 9. 关键术语和字段解释

- `play_id`：剧目 ID，对应一个短剧项目。
- `episode_no`：集号，从 1 开始。
- `shot_id`：分镜中的单个镜头 ID。
- 资产类型：

  | 值 | 含义   |
  |----|--------|
  | 1  | 场景   |
  | 2  | 角色   |
  | 3  | 道具   |
  | 4  | 平面   |
  | 5  | 其他   |

- `source_episode_nos`：资产首次出现的集号列表。
- `candidate`：候选图（五官图或造型图），通常与提示词和模型配置绑定。
- `reference`：参考图，常用作造型/场景风格的视觉参考。

---

## 10. 实践案例概览

### 10.1 从零开始一个短剧项目（剧目 + 剧本 + 资产 + 分镜）

1. **认证**（§2）：让用户在 `https://idrama.lingban.cn/api-token` 页面登录并复制 Token，或通过 `POST /openapi/uaa/oauth/token` 登录获取 `access_token`。
2. **创建剧目**（§4.2）：`POST /openapi/drama/create`，请求体 `{"name": "新剧本名称"}`，获得 `play_id`。
3. **查看或更新风格配置**（§4.11/4.12）：`GET /openapi/drama/{play_id}/style-config` 查看，`PUT /openapi/drama/{play_id}/style-config` 更新默认风格。
4. **上传剧本**（§5.2）：`POST /openapi/drama/{play_id}/scripts/upload` 上传剧本文件/粘贴剧本文本。
5. **查看剧本集列表**（§5.1）：`GET /openapi/drama/{play_id}/scripts` 确认各集上传情况。
6. **按集读取剧本内容**（§5.3）：`GET /openapi/drama/{play_id}/scripts/{episode_no}/content` 查看某集原文。
7. **剧本资产智能分析**（§5.5）：`POST /openapi/drama/{play_id}/scripts/analyze`，从剧本抽取人物/场景/道具并写入资产库。
8. **查看资产列表**（§6.1）：`GET /openapi/drama/{play_id}/assets/list`，可按 `type`、`episode_no`、`name` 过滤。
9. **创建资产**（§6.2）：若需手工补充资产，`POST /openapi/drama/{play_id}/assets/create`，传入 `type`、`name`（及可选 `description`）。
10. **生成资产图像提示词**（§6.5）：`POST /openapi/drama/{play_id}/assets/prompt-helper/generate`；将 `generated_prompt` 通过 **§6.4** `PUT .../assets/{asset_id}` 写入 `prompt` / `prompt_by_mode`。
11. **生成资产图像**（§6.6）：`POST /openapi/drama/{play_id}/assets/{asset_type}/{asset_id}/generate_image`，按接口要求传入提示词与参考图等参数，生成新图并挂接到该资产。
12. **分析生成/更新分镜**（§7.2）：`POST /openapi/drama/{play_id}/storyboard/{episode_no}/analyze` 基于剧本/资产生成分镜结构与镜头信息。
13. **按集查看分镜**（§7.1）：`GET /openapi/drama/{play_id}/storyboard/{episode_no}` 获取该集分镜结构（若不存在可先执行下一步分析生成）。
14. **查看镜头详情**（§7.3）：`GET /openapi/drama/{play_id}/storyboard/{episode_no}/shots/{shot_id}` 获取单镜头字段、已绑定资产等信息。
15. **为镜头绑定资产**（§7.4）：`POST /openapi/drama/{play_id}/storyboard/{episode_no}/shots/{shot_id}/add-asset` 将角色/场景/道具等资产关联到镜头。
16. **生成和优化分镜提示词**（§7.5）：`POST /openapi/drama/{play_id}/storyboard/{episode_no}/shots/{shot_id}/optimize-prompt` 在当前提示词基础上做 AI 优化，并按需回写（`save=true/false`）。
17. **生成分镜视频**（§8.1）：`POST /openapi/drama/{play_id}/storyboard-video/episodes/{episode_no}/shots/{shot_id}/tasks` 创建任务；按文档约定轮询/订阅任务状态直至完成。
18. **查看剧目统计**（§4.8）：`GET /openapi/drama/{play_id}/stats` 获取集数、镜头数、资产数量等。

### 10.2 按集查看、读取与删除剧本（§5）

1. **剧本集列表**：`GET /openapi/drama/{play_id}/scripts` 获取所有剧集及文件名、标题、上传时间。
2. **某集剧本内容**：`GET /openapi/drama/{play_id}/scripts/{episode_no}/content` 获取该集原文。
3. **删除某集剧本**：`DELETE /openapi/drama/{play_id}/scripts/{episode_no}` 删除指定集（需确认该集不再用于分析或已备份）。

### 10.3 查看剧目统计与风格配置（§4）

1. **单个剧目详情**：`GET /openapi/drama/{play_id}` 获取剧目名称、删除状态、操作时间。
2. **剧目统计信息**：`GET /openapi/drama/{play_id}/stats` 获取集数、镜头数、预估时长、各类型资产数量。
3. **当前风格配置**：`GET /openapi/drama/{play_id}/style-config` 获取 `selected_style_key` 与 `styles`。
4. **更新风格配置**：`PUT /openapi/drama/{play_id}/style-config`，请求体传入 `selected_style_key` 和/或 `styles`。

### 10.4 资产列表、详情与基于参考图生成图像（§6）

1. **按条件查资产**：`GET /openapi/drama/{play_id}/assets/list`，可用查询参数 `type`（1 场景/2 角色/3 道具/4 平面/5 其他）、`episode_no`、`name`、`include_deleted` 过滤。
2. **单个资产详情**：`GET /openapi/drama/{play_id}/assets/{asset_id}`（§6.3）获取该资产元数据、提示词字段、候选图 URL 等。
3. **创建资产**：`POST /openapi/drama/{play_id}/assets/create`（§6.2），传入 `type`、`name`，可选 `description`。
4. **更新资产**：`PUT /openapi/drama/{play_id}/assets/{asset_id}`（§6.4），可更新名称、类型、`prompt`、`prompt_by_mode`、生图配置、画布字段等（至少传一项）。
5. **生成资产图像提示词**（§6.5）：`POST /openapi/drama/{play_id}/assets/prompt-helper/generate`；可将返回的 `generated_prompt` 再通过 **§6.4** 写入资产。
6. **生成资产图像**（§6.6）：`POST /openapi/drama/{play_id}/assets/{asset_type}/{asset_id}/generate_image`，按接口要求传入提示词与参考图等参数，生成新图并挂接到该资产。

### 10.5 分镜脚本：按集生成、查看镜头并绑定资产（§7）

1. **读取某集分镜**：`GET /openapi/drama/{play_id}/storyboard/{episode_no}` 获取分镜结构与镜头列表。
2. **生成/更新分镜**：若分镜为空或需要重算，`POST /openapi/drama/{play_id}/storyboard/{episode_no}/analyze` 进行分析生成。
3. **查看镜头详情**：`GET /openapi/drama/{play_id}/storyboard/{episode_no}/shots/{shot_id}` 获取镜头信息、提示词、已绑定资产等。
4. **为镜头添加资产**：`POST /openapi/drama/{play_id}/storyboard/{episode_no}/shots/{shot_id}/add-asset` 绑定角色/场景/道具等（建议先用 §6 的资产列表/详情确认 `asset_id`）。
5. **生成和优化分镜提示词**：`POST /openapi/drama/{play_id}/storyboard/{episode_no}/shots/{shot_id}/optimize-prompt` 优化镜头提示词，并按需回写（`save=true`）。
6. **删除镜头（谨慎）**：若需移除镜头，`DELETE /openapi/drama/{play_id}/storyboard/{episode_no}/shots/{shot_id}`（建议先确认是否已关联生成任务或引用资源）。

### 10.6 分镜出图与视频：任务生成（§8）

1. **创建分镜视频生成任务**：`POST /openapi/drama/{play_id}/storyboard-video/episodes/{episode_no}/shots/{shot_id}/tasks` 发起该镜头视频生成任务。
2. **查询任务结果**：按照 §8.1 的返回结构与状态字段轮询/订阅，直到 `completed` 并取得 `result_video_path`（或失败时按 `status/msg` 提示处理）。