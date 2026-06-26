# 工作流编排

## 合并与字段来源

**合并**：`null` = 不覆盖。顺序：默认铺底 → 非 `null` 覆盖 → 布尔/整数校正。字段默认见 [`workflow-json-schema.md`](workflow-json-schema.md)「输入」；未在表中展开的缺省由 **`run_render.py`**（及子进程）按实现与环境变量读取（**不含**音色/数字人：`audio_man`、`person_id`/`avatar_id`、`figure_type` 仅来自 **`workflow.json`**，见下文前置约束）。

**`duration_sec`**：策划参考，非 ffmpeg 上限。**成片时长**以 TTS+`ffprobe` 为准。`scene_count` 见 **`video-brief-plan.md`**；切段与 AI 条数依实测与字幕轴（**`render-rules.md` §3·C.5**）。禁止为凑时长裁已定稿口播（除非用户要求）。

**选题**：去空白 <5 字、占位串（如「你好」「test」）拒收；可扩写；严格模式模糊则失败。

## 步骤链

1) Plan → `video-brief-plan`（败则全败；模板见 **`video-brief-plan.md`**）  
2) Script（**hook / 首段与首镜对齐**：**≤20 字硬上限**，见 **`script-prompt.md`**）  
3) Storyboard：语义切分；**`storyboard-prompt.md`**（**首个分镜 `voiceover` 同上硬上限**）；非当代 **`history-storyboard-prompt.md`**；DH **`chanjing-video-compose`**，AI **`chanjing-ai-creation`**；TTS/多段 AI/mux **`render-rules.md` §3**、**§5**  
4) Render：**`render-rules.md` §3**（含 **§3·C.6**）、**§4**（表 4–6）；`ref_prompt` 质检见 **`storyboard-prompt.md`** / **`history-storyboard-prompt.md`**（[`ref-prompt-pointers.md`](ref-prompt-pointers.md)）；重试/`partial` **`render-rules.md` §1**  
5) 成功：**`render-rules.md` §1**

**仅渲染**：`run_render.py` + `full_script` + `scenes[]`。**顺序**：Plan → Script → Storyboard → Render（各阶段用哪份模板见上列步骤）。详见 [`run-render.md`](run-render.md)。

## 前置约束（业务）

**勿**用环境变量或仓库内缓存保存跨任务的默认 `audio_man` / `person_id` / `figure_type`。每次任务在 **`workflow.json` 根级显式填写**；由 Agent 先按 **`video_plan`**（含 `presenter_gender`、`application_context`、`tone`）与口播人设调用 **`list_voices.py`** 选 `audio_man`，再按该音色与同一人设调用 **`list_figures.py`**（`--source` 与本次一致：`common` / `customised` 等）选公共数字人；`audio_man` 优先与最终所选形象的 **`audio_man_id`** 一致。

**公共数字人选型（禁止「只取列表前几项」）**：

1. **全量拉取**：MUST 使用 `list_figures.py --source common --fetch-all --json` 拉取全部公共数字人（接口约 478 条，默认仅返回 20 条首页远不够）。**禁止**仅用默认 `--page-size 20` 的首页结果选型。

2. **语义匹配维度**：在全量候选中按以下属性与 `video_plan`/口播人设做**语义匹配**，择优选型：

   | 属性 | 路径 | 匹配用途 |
   |------|------|---------|
   | `name` | 顶层 | 人设气质（如"海城"偏休闲、"文昊"偏教师） |
   | `gender` | 顶层 | 与口播人设性别一致（注意：值为 `male`/`female` 或 `男`/`女`） |
   | `audio_name` | 顶层 | 音色气质匹配（如"温和青年男生""磁性中年男声"） |
   | `tag_names` | 顶层数组 | 场景/行业/年龄/风格标签（如"国风""商务""青年""电商""情感""教育""大健康"等）；与选题行业和 `video_plan.tone` 匹配 |
   | `figures[].type` | figures 数组 | 形态（`whole_body` 站姿全身 / `sit_body` 坐姿 / `circle_view` 圆形头像）；→ `workflow.json` 的 `figure_type` |
   | `figures[].width` × `height` | figures 数组 | 画幅须竖屏 1080×1920（与 **D.1c** 一致） |
   | `figures[].bg_replace` | figures 数组 | 是否支持换背景（`true` 约 62 个；需自定义背景时筛选此项） |
   | `audio_man_id` | 顶层 | → `workflow.json` 的 `audio_man`；MUST 与所选形象一致 |
   | `audio_preview` | 顶层 | 可供用户试听的音色预览 URL |

3. **匹配优先级**：
   - 在已满足**文案人设**与**已选 `audio_man`**一致的前提下：**gender 与已选 TTS 一致** > **audio_man_id 与 `workflow.json.audio_man` 一致** > **tag_names 行业/场景匹配** > **audio_name 音色气质** > **name 名称语义**
   - **默认偏好年轻**：`tag_names` 含"青年"或 `audio_name` 含"青年/元气/学生/年轻"时优先；仅当选题明确要求成熟、权威、中老年、国风等气质时再选对应人设
   - **竖屏筛选**：`tag_names` 含"竖版"且 `figures` 中存在 1080×1920 的 `whole_body` 或 `sit_body`

4. **figure_type 选取**：从所选人物的 `figures[]` 中选取 `width=1080, height=1920` 的形态（`whole_body` 或 `sit_body`）；**禁止**选 `circle_view`（圆形头像，不适用于成片）。

定制源 `customised` 同样对比 **`name`**、**`width`/`height`**、**`audio_man_id`** 等，勿未经比较直接取页首（与 **`storyboard-prompt.md`** / **`render-rules.md`** 中 D 类规则一致）。

**公共语音选型（TTS `audio_man`）**：

> **选型策略**：先锚定文案人设，再决定语音；存在公共数字人镜时，再按已选语音反选公共数字人。当 `use_avatar: true` 时，MUST 先从 `list_voices.py` 选出与 `presenter_gender`、`application_context`、`tone` 一致的 `audio_man`，再在同性别公共形象中优先选择 `audio_man_id` 与其一致的数字人；仅当数字人自带音色与内容气质明显不匹配时，才允许保留已选 `audio_man` 并改选另一位**同性别**公共数字人。当 `use_avatar: false` 时 MUST 从 `list_voices.py` 独立选型。

1. **全量拉取**：MUST 使用 `list_voices.py --fetch-all --json` 拉取全部公共语音（当前约 89 条，1 页可覆盖；脚本已支持自动翻页以应对未来扩容）。**禁止**仅凭记忆或硬编码 id 选音色。

2. **语义匹配维度**：在全量候选中按以下属性与 `video_plan`/口播人设做**语义匹配**：

   | 属性 | 匹配用途 |
   |------|---------|
   | `name` | **核心匹配维度**——名称蕴含丰富语义线索：年龄（小/学→年轻；大叔/老/阿姨/婆婆→年长）、风格（带货→电商；专业→权威；情感→感性；温柔/温和→温暖；激昂/激情→激情；磁性/浑厚→厚重；知心→治愈）、角色（评书/说书→叙事；播音→正式；演讲→激励）、方言（东北腔/河南/闽南/台湾腔→地域特色） |
   | `gender` | 与口播人设性别一致（`male`/`female`，少数为空串） |
   | `audition` | 试听 URL（选型不确定时可提供给用户试听） |

3. **匹配优先级**：
   - **`name` 语义匹配** > **`gender` 性别** > **`audition` 试听确认**
   - **默认偏好年轻、有活力**：名称含"小哥""小姐姐""学""青年""活力"等优先
   - **内容导向覆盖**：选题为历史叙事 → 偏好"评书""说书""磁性""浑厚""渊博"等；选题为电商 → 偏好"带货"系列；选题为情感 → 偏好"情感""知心""温柔"等；选题为教育/科普 → 偏好"专业""科普""中年专家"等

4. **与数字人形象的一致性**：
   - 当 `use_avatar: true` 时，**先保证 `audio_man.gender` 与口播人设一致**，再在公共数字人中选择 **`gender` 同步**、且 **`audio_man_id` 优先对齐** 的形象
   - 若某个公共数字人的默认 `audio_man_id` 与内容气质明显不匹配，可保留已选 `audio_man`，但必须改选另一位**同性别**公共数字人；**禁止**男声配女性形象、女声配男性形象
   - `workflow.json` 中 MUST 显式填写 `audio_man`，禁止依赖环境变量默认音色

环境变量与路径见 [`../../../references/top-level-runtime-contract.md`](../../../references/top-level-runtime-contract.md)。安全、凭据边界与运行时副作用扩展说明见 [`extended-runtime-notes.md`](extended-runtime-notes.md)（**若与 `manifest.yaml` 冲突以 manifest 为准**）。
