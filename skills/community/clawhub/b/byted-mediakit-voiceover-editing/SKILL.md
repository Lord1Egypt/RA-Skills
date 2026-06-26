---
name: byted-mediakit-voiceover-editing
display_name: 口播视频智能精剪工具
version: 1.0.9
description: |
  Volcano Engine AI MediaKit talking-head video editing Skill: a one-stop workflow from environment setup through media management, audio processing, talking-head cuts, video export, review UI, and iterative refinement. You MUST invoke this Skill when the user mentions talking-head editing, cutting talking video, video editing, removing pauses, processing audio, exporting talking video, automatic editing, removing verbal slips, or similar. Also invoke when the user uploads video or audio and asks for editing.
category: 音视频处理
env:
  - name: ARK_SKILL_API_BASE
    description: SkillHub VOD 网关 OpenAPI 根 URL（与 ARK_SKILL_API_KEY 同时存在时启用 apig）；通常由宿主/容器注入进程环境，不必写入 .env
    required: false
    secret: false
    default: ''
  - name: ARK_SKILL_API_KEY
    description: SkillHub 网关 Bearer Token；与 ARK_SKILL_API_BASE 同时存在时启用 apig；通常由宿主/容器注入，不必写入 .env
    required: false
    secret: true
    default: ''
  - name: VOLC_ACCESS_KEY_ID
    description: 火山引擎访问密钥ID（直连 OpenAPI 时必填；若进程环境中已有 ARK_SKILL_API_BASE 与 ARK_SKILL_API_KEY 则可不填）
    required: false
    secret: true
    default: ''
  - name: VOLC_ACCESS_KEY_SECRET
    description: 火山引擎访问密钥 Secret（直连 OpenAPI 时必填；若进程环境中已有 ARK_SKILL_API_BASE 与 ARK_SKILL_API_KEY 则可不填）
    required: false
    secret: true
    default: ''
  - name: VOLC_SPACE_NAME
    description: 火山引擎VOD存储空间名称
    required: true
    secret: false
    default: ''
  - name: ASR_API_KEY
    description: 语音识别服务API密钥
    required: true
    secret: true
    default: ''
  - name: ASR_BASE_URL
    description: 语音识别服务接口地址
    required: true
    secret: false
    default: 'https://openspeech.bytedance.com/api/v3/auc/bigmodel'
  - name: VOD_EXPORT_SKIP_SUBTITLE
    description: 导出时是否跳过字幕压制（默认跳过；0/false/no 表示启用字幕压制）
    required: false
    secret: false
    default: '1'
  - name: TALKING_VIDEO_AUTO_EDIT_REVIEW_AUTO_OPEN
    description: 审核页启动时是否自动打开浏览器（默认不打开；1/true/yes 表示打开）
    required: false
    secret: false
    default: '0'
  - name: TALKING_VIDEO_AUTO_EDIT_VIDEO_CUT
    description: 是否开启视频裁剪功能：1 进行（默认）；0 不进行。仅当有字幕或音频静音时生效。
    required: false
    secret: false
    default: '1'
  - name: EXECUTION_MODE
    description: |
      执行模式选择（可选），优先级 apig > cloud > local：
      - apig: 使用 SkillHub 网关（需 ARK_SKILL_API_BASE + ARK_SKILL_API_KEY）
      - cloud: 直连火山引擎 OpenAPI（需 VOLC_ACCESS_KEY_* + VOLC_SPACE_NAME + ASR_*）
      - local: 完全本地执行，使用 Qwen3-ASR / Demucs / ffmpeg，无需任何云端环境变量和 VOD 空间
      留空则自动检测：按 apig > cloud > local 优先级尝试，缺参时打印提示并自动降级。
    required: false
    secret: false
    default: ''
permissions:
  - network
  - file_read
  - file_write
  - temp_storage
triggers:
  - 口播剪辑
  - 剪口播
  - 剪视频
  - 去掉停顿
  - 处理音频
  - 导出口播
  - 自动剪辑
  - 去除口误
  - 视频剪辑
---

## 一、模式与凭据

### 1.1 三种执行模式

| 模式 | 说明 | 所需环境变量 | ASR 方式 |
|------|------|-------------|----------|
| **apig** | SkillHub 网关代理，Bearer Token 认证 | `ARK_SKILL_API_BASE` + `ARK_SKILL_API_KEY`（容器注入）+ `VOLC_SPACE_NAME` + `ASR_API_KEY` + `ASR_BASE_URL` | 豆包语音大模型 |
| **cloud** | 直连火山引擎 OpenAPI，HMAC 签算 | `VOLC_ACCESS_KEY_ID` + `VOLC_ACCESS_KEY_SECRET` + `VOLC_SPACE_NAME` + `ASR_API_KEY` + `ASR_BASE_URL` | 豆包语音大模型 |
| **local** | 完全本地执行，无需云端服务 | 无（可选 `EXECUTION_MODE=local`） | Qwen3-ASR 本地推理 |

**优先级**：`apig > cloud > local`。自动检测按此顺序依次检查环境变量，缺参时打印 `.env` 路径与缺失变量列表并自动降级。

### 1.2 凭据配置

- **`.env` 文件位置**：`<SKILL_DIR>/.env`
- 脚本先读**进程环境变量**，再用 `.env` **补全未设置的项**（不覆盖容器注入）
- `ARK_SKILL_*` 通常由部署容器注入，**不必**手写到 `.env`
- **缺参不阻塞**：不使用终端 `input()` 交互，缺参时打印提示信息并自动降级到可用模式
- Agent 推荐用户通过**编辑 `.env` 文件**或**Agent 文件写入工具**来配置变量，避免终端粘贴问题
- **安全**：控制台创建**仅含所需权限**的密钥；测试请用**独立点播空间**；`.env` 勿提交仓库

### 1.3 模式意图识别（Agent 必读）

当用户在对话中表达模式切换意图时，Agent 应识别并执行：

| 用户表达 | 识别为 | 操作 |
|---------|--------|------|
| "用本地模式" / "不走云端" / "离线处理" | `EXECUTION_MODE=local` | 写入 `.env` 或传 `--mode local` |
| "用云端" / "用火山引擎" / "走 AK/SK" | `EXECUTION_MODE=cloud` | 写入 `.env` 或传 `--mode cloud` |
| "走网关" / "用 apig" / "用 SkillHub" | `EXECUTION_MODE=apig` | 写入 `.env` 或传 `--mode apig` |

**隔离要求**：各任务的模式选择相互独立。一个任务中切换到 local 不应影响另一个任务的模式。Agent 应在每次任务开始时重新检测或遵循用户当次指定。

---

## 二、执行约束（STRICT — NO EXCEPTIONS）

1. **仅使用以下脚本**，禁止创建新脚本
2. **按顺序执行所有步骤**，跳步即任务失败
3. 执行任何脚本前必须先 `cd <SKILL_DIR>/scripts`
4. 每个 CHECKPOINT 必须验证产物后再继续
5. 任何步骤失败必须**立即停止并报告**，不得继续
6. Step 4/5/6 输出**禁止**简化版、占位符、示例或省略内容
7. **最终输出必须保持原样，不能做任何修改**
8. 审核页是否自动打开由 `TALKING_VIDEO_AUTO_EDIT_REVIEW_AUTO_OPEN` 决定（**强制**）：Agent 不得额外执行 `open`/`start`/`xdg-open` 等命令
9. **超时设置**：音视频处理时长较长，宿主超时时间应设置为 **60 分钟**

### 职责分工

| 组件 | 职责 | 不做 |
|------|------|------|
| **脚本（规则引擎）** | ASR 优化、候选生成（标记位置+规则置信度+删除建议） | 不做最终删除/保留决策 |
| **宿主 Agent（你）** | 语义断句、口癖识别确认、候选复核、最终删除/保留决策 | 不修改脚本 |

**核心原则：脚本提供候选（含 deleted_parts + cleaned_text），Agent 做最终决策。**

---

## 三、路径规则

### 3.1 SKILL_DIR 与 Output-dir

- **SKILL_DIR**：`byted-mediakit-voiceover-editing` 目录路径
- **PROJECT_ROOT**：由 `scripts/project_paths.py` 推导：
  1. 环境变量 `VOICEOVER_EDITING_PROJECT_ROOT` 若设置则用之
  2. 否则为 `<SKILL_DIR>` 的 `parents[2]`（沿父链上移 3 级，不依赖中间目录命名）
- **Output-dir**：`<PROJECT_ROOT>/output/<素材名>/`
- 脚本启动时会打印路径推导日志，便于调试确认

### 3.2 素材名推导

| 来源 | 推导规则 | 示例 |
|------|---------|------|
| URL | 取最后一段去扩展名 | `https://x.com/video.mp4` → `video` |
| 本地文件 | 取文件名去扩展名 | `/path/Test_Video_720p.mp4` → `Test_Video_720p` |
| DirectUrl | 取 FileName 去扩展名 | `test.mp4` → `test` |
| Vid | 取 Vid 值 | `v0xxx` → `v0xxx` |

### 3.3 从上下文推导 output-dir

- **推导优先级**（按顺序尝试）：
  1. 对话历史/命令参数中已显式传入 `--output-dir output/<子目录>` → 直接沿用
  2. 无法从对话历史获得 → 询问用户指定
- Agent **不得**扫描仓库来推断 `output-dir`

### 3.4 重复处理

写入任何输出文件/目录前，若目标已存在，**必须提示用户**：
- 目录已存在：「是否删除原目录？[删除/保留并新建(01)]」
- 文件已存在：「是否删除/覆盖/保留？」
- 超时 20 秒默认「保留并新建(01)」

---

## 四、脚本清单

> 执行前必须 `cd <SKILL_DIR>/scripts`

| 脚本 | 用途 |
|------|------|
| `./scripts/setup.sh` | 环境检查与依赖安装 |
| `./scripts/pipeline_url_to_asr.py` | Step 3: URL → ASR 流水线（支持 `--mode local/cloud/apig`） |
| `./scripts/merge_asr_words.py` | Step 4 产出缺 words 时，从 raw 合并 |
| `./scripts/prepare_export_data.py` | Step 6a: 数据预处理（`--width` `--height` `--write-step6`） |
| `./scripts/serve_review_page.py` | Step 6b: 审核页静态服务 + 数据保存 + 导出代理 |
| `./scripts/export_server.py` | 导出服务（独立进程，接收审核页 POST） |
| `./scripts/vod_direct_export.py` | Step 6c: VOD 导出任务提交与查询 |

---

## 五、必经步骤

> 各 Step 完整检查单见 `references/执行步骤/` 下分步文档。

| Step | 说明 | 文档 |
|------|------|------|
| Step 1 | 环境检查与依赖安装 | [1. 环境检查.md](references/执行步骤/1.%20环境检查.md) |
| Step 2 | 语气词/卡顿词确认与规则更新 | [2. 语气词提示与用户行为更新.md](references/执行步骤/2.%20语气词提示与用户行为更新.md) |
| Step 3 | URL → ASR 流水线与候选生成 | [3. URL到ASR流水线与候选生成.md](references/执行步骤/3.%20URL到ASR流水线与候选生成.md) |
| Step 4 | ASR 语义纠错（Agent 执行） | [4. ASR语义纠错.md](references/执行步骤/4.%20ASR语义纠错.md) |
| Step 5 | 口播剪辑（Agent 执行） | [5. 口播剪辑.md](references/执行步骤/5.%20口播剪辑.md) |
| Step 5.5 | 审核逻辑确认 | [5.5 审核逻辑确认.md](references/执行步骤/5.5%20审核逻辑确认.md) |
| Step 6a | 数据预处理 | [6a. 数据预处理.md](references/执行步骤/6a.%20数据预处理.md) |
| Step 6b | 审核与导出 | [6b. 审核与导出.md](references/执行步骤/6b.%20审核与导出.md) |
| Step 6c | VOD 导出任务提交与查询 | [6c. VOD导出任务提交与查询.md](references/执行步骤/6c.%20VOD导出任务提交与查询.md) |

---

## 六、产物对照表

| 产物文件 | 生成步骤 | 说明 |
|---------|---------|------|
| `step1_preuploaded.json` | Step 3 | 素材上传/注册结果（含 `_execution_mode`） |
| `step3_voice_separation_result.json` | Step 3 | 人声分离结果 |
| `step5_asr_raw_*.json` | Step 3 | ASR 原始转写 |
| `step5_asr_optimized.json` | Step 4 | 语义纠错后 ASR |
| `step6_speech_cut.json` | Step 5 | 口播剪辑决策 |
| `review_import_data.json` | Step 6a | 审核页数据（含 `_execution_mode`、`track`、`sentences`） |
| `export_request.json` | Step 6a / 审核保存 | 导出请求（审核页"保存"后会同步更新此文件） |
| `export_submit_*.json` | Step 6b/6c | 最终提交的导出数据 |

---

## 七、审核页与数据联动

### 7.1 模式感知

审核页通过 `review_import_data.json` 中的 `_execution_mode` 字段自动识别当前模式，并在界面上：
- 显示**模式徽标**（APIG 蓝/云端绿/本地橙）
- 调整**导出按钮文案**（本地模式显示"本地导出视频"）
- 调整**导出成功信息**（本地模式显示输出文件路径，云端显示 OutputVid + PlayURL）

### 7.2 本地模式审核页

本地模式**完全支持审核页**。Source 字段使用 `http://127.0.0.1:<port>/local-media/<绝对路径>` 格式，由 `serve_review_page.py` 的 `/local-media/` 路由代理访问本地文件。

### 7.3 数据联动（审核修改 ↔ 直接导出同步）

审核页提供两个操作按钮：

| 按钮 | 功能 | 数据流 |
|------|------|--------|
| **💾 保存审核** | 将修改持久化到磁盘 | POST `/api/save-review` → 更新 `review_import_data.json` + 重新生成 `export_request.json` |
| **导出** | 直接触发视频导出 | POST `/export` → `apply_review_to_export` → `export_submit_*.json` → ffmpeg/VOD |

**关键**：用户在审核页做了修改后，点击"💾 保存审核"即可将修改同步到磁盘。此后即使关闭审核页，Agent 通过 `vod_direct_export.py --output-dir <输出目录> submit --wait` 直接导出时也会读取更新后的 `export_request.json`，确保数据一致。

> ⚠️ **关键约束**：调用 `vod_direct_export.py` 时，`--output-dir` 必须写在 `submit`/`query` 子命令**之前**。一行式调用格式：
> ```
> cd SKILL_DIR/scripts && source .venv/bin/activate && python vod_direct_export.py --output-dir <绝对路径> submit --wait
> ```

### 7.4 审核页服务端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 审核页 HTML |
| `/api/review-data` | GET | 返回 `review_import_data.json` |
| `/api/mode` | GET | 返回当前执行模式 |
| `/api/save-review` | POST | 保存审核修改（回写 review_import_data + 重生成 export_request） |
| `/export` | POST | 触发导出（local: ffmpeg；cloud/apig: vod_direct_export） |
| `/local-media/<path>` | GET | 本地模式媒体文件代理 |

---

## 八、常见问题

| 现象 | 处理 |
|------|------|
| 本地文件走了 DirectUrl 模式 | 本地文件必须作为**第一个位置参数**传入；`--directurl` 仅用于 VOD 空间内已有 FileName |
| step5 写入失败 | 必须写入 `output/<文件名>/step5_asr_optimized.json`，禁止写 output 根目录 |
| concat 规则要删但音频还在播 | actionTime 必须从 step5 words 查出**仅保留**部分的 ms |
| 重复文件未提示 | 写入前必须检查目标是否存在，按 3.4 规则处理 |
| step6 修正未生效 | 确保 step6 顶层为 `optimized_segments` 或 `sentences`；运行 `--write-step6` 写回 |
| segment 起止时间不准 | Step 6a 会依 step5 words 校正 |
| delete 未在 deleted_parts | 每个 `action: delete` 段**必须**在 deleted_parts 中有对应项 |
| 审核页修改关闭后丢失 | 关闭前点击"💾 保存审核"持久化到磁盘 |
| 审核页本地资源 404 | 确认 Source 字段为 `/local-media/` URL 格式；检查 `serve_review_page.py` 是否正常运行 |
| 缺参提示后阻塞 | 不再使用 `input()`，缺参时自动降级并打印 `.env` 路径提示 |

---

## 九、字幕可见性（Alpha）

- **字段**：`textElement.Extra[transform].Alpha`（0～1）
- **含义**：`0` 隐藏（不渲染到画布），`1` 展示
- **删除态**：Alpha 设为 0；**恢复**：Alpha 设为 1
