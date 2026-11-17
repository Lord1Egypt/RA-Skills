# Prompt 工程规则（实战踩坑）

> **本文职责**：记录从实际生成中总结的**实战踩坑规则**——角色描述、背景控制、武器道具、一致性保障、错误模式等。
> **模板结构**（6 段式、语言选择）→ 主 SKILL.md §6
> **资产生成**（角色 11 视图的具体 prompt）→ `references/asset-generation.md`

---

## 1. 角色外貌描述

### 1.1 头发/头饰

- **必须具体**：不能写"传统头巾""经典发型"——模型会自由发挥
- **写法**：颜色 + 位置 + 系法/样式
  - ✅ `"额头缠绕客家蓝染头巾，在前额上方打结固定"`
  - ❌ `"戴客家传统头巾"`
  - ✅ `"灰蓝色红军八角帽，帽檐微微上翘，正中缀红五星"`
  - ❌ `"红军帽"`

### 1.2 同一角色的外貌描述必须跨视图统一

- `hair` 字段被 `_clothes` 变量共享 → 所有视图的服饰描述一致
- `face` 视图的 prompt 不应包含 `_clothes`（含 body/build/color 等全身级描述），否则模型把面部特写画成全身照
- face 视图应只含：`fd_str`（五官细节）+ `hair`（发型/头饰）+ `base`（身份）+ `face`（面容）+ `_white_bg`

---

## 2. 背景控制

### 2.1 纯白背景

- 背景指令必须放在 prompt **开头和末尾**双重强调
  - 开头：`"纯白色背景。{视图描述}..."`
  - 末尾：`"...{_white_bg}"`
- `_white_bg` 内容：`"纯白色背景(#FFFFFF)，没有任何颜色、纹理或环境元素，只有纯空白底。"`
- 负面提示词必须包含：`"暖色背景, 灰色背景, 米色背景, 有颜色的背景, 背景光, 复杂背景, 渐变背景, 纹理背景, 环境元素, 场景, 天空, 地面"`
- 原因：模型倾向自动填充浅色背景（浅灰/米色），即使 prompt 写了纯白也可能忽略

---

## 3. 武器和道具控制

### 3.1 标准视图禁止武器

- front/face/side/back 四视图：必须包含 `_no_weapon` + `_neg_weapons`
  - `_no_weapon`：`"双手自然垂下，手中不持任何武器，不能有剑、枪、刀、弓、盾等任何武器道具。"`
  - `_neg_weapons`：`"手中持剑, 手中持枪, 手持武器, 握剑, 握刀, 武器, 道具, ..."`

### 3.2 武器视图

- action_xxx / pose_xxx 视图：**不能**包含 `_no_weapon`（与武器描述矛盾）
- 武器视图也需共享 `_clothes` 以确保衣着一致

---

## 4. 一致性保障

### 4.1 跨视图一致性

| 规则 | 说明 |
|------|------|
| 衣着统一 | front/side/back 共享 `_clothes` 变量（face 不用，避免 body 侵入）|
| 面部统一 | face/side/back 以 front（全身正面无武器白底图）为 ref_image |
| 背景统一 | 所有标准视图 + 武器/动作视图统一用 `_white_bg` |
| 武器统一 | 标准视图禁用武器，武器视图没有 `_no_weapon` |
| 发型/头饰统一 | `hair` 字段跨视图共享，必须具体到颜色+位置+系法 |

### 4.2 ref_image 的选择

- face/side/back 的 ref_image = front（标准四视图使用前视图保持一致性）
- 武器视图：不设 ref_image（free generation），因为 ref_image 是无武器白底图，与武器 intent 冲突
- 避免路径通配符回退：**不要从目录级别的通配符读取 ref_image**，只使用本角色前视图的具体路径

### 4.3 画质描述不硬编码铠甲

- [画质要求] 段中的"铠甲金属质感"不能硬编码——项目可能是现代题材（无铠甲）
- 代码中根据 `character_cards` 的 `armor/clothing` 字段自动检测：包含"铠甲/铁甲/甲胄/战甲"等关键词才追加
- 无铠甲时默认只写：`"电影级写实，服装材质细节，光影层次丰富，氛围情绪饱满。"`

### 4.4 纯场景镜头不要写"加入各角色"

- **纯场景镜头（只有 1 张场景参考图）**：编辑指令不能写"在场景中加入各角色"——模型会脑补古人
- 代码中根据 `ref_count` 自动判断：仅 1 张参考图时，编辑指令改为 `以图1为基础，{desc}`，去掉"加入角色"
- 这个规则也影响了 [保留元素] 段——**已完全禁用 [保留元素]**（无论几张参考图都不加，因为会导致角色朝向被参考图锁定）

### 4.5 构图必须指定角色空间位置

- 含角色的镜头（尤其是多角色），description 必须描述 **前/中/背景 + 左/右位置**
  - ✅ `"客家老人坐在左侧长椅上看报，现代青年从右侧跑步经过"`
  - ❌ `"青年与老人相视而笑"`（模型不知道人放哪里）
- 全景+人物镜头：前景=人物站位，中景=城市/场景，背景=天空/远景

### 4.6 角色行为必须匹配身份

- video_prompt 和首帧图 prompt 中角色行为必须符合其身份特征：
  - ❌ 客家老人在城市公园看报（客家老人是传统文化守护者，不会出现在城市）
  - ❌ 古代角色穿T恤、现代角色穿铠甲
  - ❌ 老者做敏捷动作（除非角色卡明确写了）
- 验证方法：写完 description 后，问自己"这个角色真的会做这件事吗？"

---

## 5. 常见错误模式

| 错误 | 现象 | 根因 | 修复 |
|------|------|------|------|
| face 画成全身照 | face 视图是全身而非特写 | face prompt 末尾拼了 `_clothes`（含 body/build/color）覆盖了"面部特写"指令 | face 只用 `fd_str` + `hair` + `base` + `face`，不用 `_clothes` |
| 背景不是纯白 | 浅灰/米色背景 | 背景描述在 prompt 中间权重不足，被前面气氛词覆盖 | 开头+末尾双重强调 + 增强负面词 |
| 头饰不一致 | 不同视图显式不同头饰 | `hair` 字段模糊（如"传统头巾"），模型自由发挥 | 描述精确到颜色+位置+系法 |
| 人物有武器 | 标准视图手持武器 | 武器描述在 armor 字段中，被错误引入标准视图 | `_armor_clean` 剥离武器关键词 + `_no_weapon` + `_neg_weapons` |
| 脚部被截断 | 脚踝以下被裁切 | prompt 缺少明确的全身指示 | 加 `_full_body`：`"包含鞋子的完整全身从头到脚，不能截断脚部。"` |
| feishu_doc_id 为空 | poll 显示"无项目数据" | `script.json` 没配 `feishu_doc_id`，飞书查询按空 doc_id 过滤 | `create_project.py` 已自动填充；手动创建时检查 `script.feishu_doc_id` 是否从 URL 提取 |

---

## 6. 生成模式选择

### 6.1 默认使用 standard 模式

- **所有视频生成默认使用 `standard` 模式**（首帧合成图作参考 + video_prompt 驱动的动态视频）
- 流程：`bff`（构建首帧配置）→ `gi`（生成首帧合成图）→ `submit`（standard 模式提交视频）
- 即使是多角色/场景+人组合，也应先生成合成首帧图（场景+角色合为一张），再用 `standard` 模式

### 6.2 multi-image 模式的定位

`multi-image` 模式是**多张参考图之间的过渡动画**，不是真正的场景视频合成。它只适用于纯视觉过渡效果，不适用于需要角色动作/剧情推进的场景。

- ❌ 不用于常规视频生成（效果是"图A渐变到图B"的动画）
- ✅ 仅用于特殊的纯过渡/风格变换场景

### 6.3 参考图完整性

- 如果使用了 `multi-image` 模式：至少需要 2 张参考图，否则提交失败
- 参考图路径必须指向**实际存在的文件**
- 三种资产类型的依赖关系：

```
character_cards → auto阶段3 → images/characters/{name}_front.png
troop_cards     → auto阶段4 → images/troops/{name}_front.png
scene_cards     → auto阶段5 → images/scenes/{name}_宽高.png
```

> `troop_cards` 是"辅助资产卡"——可包含道具、军队、武器、群众等。

### 6.4 引用了就一定要生成

- shot 的 `reference_images` 中用到的所有资产路径必须确保文件存在
- 不会自动回退

---

## 7. 常见运行错误

### 7.1 GitHub 图片缓存不更新

- `image_api.upload_to_url()` 检测到文件在 GitHub 上已存在时，**不会比较 SHA**，直接返回旧 URL
- 即使本地首帧图已重新生成，传给 Agnes API 的参考图 URL 还是旧的
- 修复：比较本地 SHA 与远程 SHA，不同则上传新版本
- **定性**：视频内容"看起来一样"时，优先检查 GitHub 上参考图 URL 指向的图片是否已更新

### 7.2 模块 import 路径被覆盖

- `audio.py` 用 `from config import get_freesound_key`，但 `sys.modules["config"]` 可能已被 agnes-ai 的 config 模块覆盖（通过 `_agnes_mod()` 注入）
- 此时 `from config import xxx` 会拿到 agnes-ai 的 config，缺少项目级 config 的函数
- 修复：不用顶层 import，改为通过 `_shared_tools` 统一配置读取（走 Layer 2 优先级链）
- **定性**：项目级模块（`project-generate/scripts/modules/`）不要用 `from config import`，改用 `from modules.config import` 或直接读取配置

### 7.3 lark-cli 在 subprocess 中找不到

- `feishu.py` 的 `_lark()` 通过 `subprocess.run` 调用 `lark-cli.cmd`
- 在 Windows nohup 环境下，`.cmd` 批处理文件可能无法被 `subprocess.run` 正确执行
- 手动在 Bash 中跑 `lark-cli` 能成功，但 Python `subprocess.run` 静默失败
- **后果**：飞书 Base 写入（`upsert_task`）静默失败，poll 找不到记录，但提交者以为成功了
- 修复：加 `shell=True` 或用 `"cmd" "/c"` 前缀（注意参数长度限制）
- 变通：通过 Bash 工具手动执行 `lark-cli base +record-upsert` 插入记录

### 7.4 轮询死循环：旧记录不删 + 新记录写不回

这是 7.3 的连锁后果：

```
1. submit 创建新任务 → upsert_task(lark-cli) 失败 → 飞书无新记录
2. 飞书里只有旧记录（有旧 task_id，已过期/HTTP 400）
3. poll 轮询 → 按旧 task_id 查 Agnes API → 400 → 触发重试
4. 重试提交新任务 → 新任务完成 ✅ 但 upsert_task 又失败了
5. 回到步骤 3 → 死循环 🔄
```

**判断标准**：
- poll log 持续显示 `🔴 重试提交成功` 但任务状态一直是"queued"
- 飞书 Base 记录数不变（全是旧记录）
- 手动查 Agnes API 发现新 task_id 其实已完成

**修复**：
1. 查 Agnes API 获取最新已完成的任务 ID
2. 手动用 `lark-cli base +record-upsert` 插入正确记录
3. 删掉旧记录
4. 修复 lark-cli subprocess 问题（见 §7.3）

### 7.5 FeishuTracker 本地缓存兜底

- `FeishuTracker.upsert_task()` 始终**优先写入本地 JSON 缓存**（`tasks/task_tracker_fallback.json`），再写飞书 Base
- 飞书写入失败时打印 `⚠️ 飞书写入失败` 日志，但数据不丢（本地缓存保底）
- `list_tasks()` 读取飞书后，用本地缓存**覆盖** task_id 和 status
- 即使飞书完全不可用，重试也不进死循环

### 7.6 原子化重试流程

重试视频任务的三步流程：

| 步骤 | 操作 | 关键点 |
|------|------|--------|
| 1 | `upsert_task("", "pending")` | 清空旧 task_id，状态→pending，写入本地缓存 |
| 2 | `provider.submit_video(...)` | 提交新任务 |
| 3 | `upsert_task(new_task, "queued")` | 写回新 task_id，状态→queued |

即使步骤 1/3 飞书写入失败，本地缓存确保下次 poll 读到正确数据。

---

## 8. BGM 管理

### 8.1 自定义 BGM 优先

- `sounds/bgm_custom.mp3` 存在时**优先使用**，跳过 FreeSound 自动搜索
- 不存在时回退到 FreeSound 搜索（按 `script.tone` → 关键词 → 搜索 → 下载预览）

### 8.2 多段 BGM 拼接

- 可用 ffmpeg 将多段音乐拼接成自定义 BGM，匹配视频的叙事段落
- 每段用 `atrim` 截取所需长度，`acrossfade` 做交叉淡入淡出过渡
- 示例（三段式：史诗→传统→希望）：
  ```
  [0:a]atrim=0:15[seg1];[1:a]atrim=0:10[seg2];[2:a]atrim=0:15[seg3]
  [seg1][seg2]acrossfade=d=1.0[mix1];[mix1][seg3]acrossfade=d=1.0[final]
  ```

### 8.3 推荐套索来源

| 来源 | 协议 | 说明 |
|------|------|------|
| FreeSound (freesound.org) | CC0/CC | 已内置 API 支持，自动搜索+下载 |
| Pixabay Music | Pixabay License | 免费可商用，直接下载 MP3 |
| FreePD (freepd.cn) | CC0 | 公共领域，无需署名 |

---

## 9. Windows ffmpeg 避坑

### 9.1 禁用 xfade 转场

- **Windows 上 xfade + acrossfade 链式叠加有音视频时间轴漂移问题**
- 漂移随转场次数累积，7 段拼接时约在 27s 处出现画面卡死
- 修复：禁用 xfade，全用简单 concat（`-f concat -safe 0 -c copy`）
- 简单 concat 帧级精确，无漂移风险
- `shot_durations()` 计算镜头开始/结束时间时**不加 xfade 重叠**

### 9.2 像素格式必须指定

- `subtitles` 滤镜或某些 filter graph 在 Windows 上默认输出 `yuv444p`
- `yuv444p` 不被部分播放器支持 → 画面黑屏/无法播放
- 修复：所有 ffmpeg 输出加 `-pix_fmt yuv420p`

### 9.3 subtitles 滤镜中文路径问题

- Windows 上 libass 对中文路径支持不好，`subtitles` 滤镜可能导致 ffmpeg 退出码 4294967274
- 修复：复制 SRT 到纯 ASCII 临时路径（`C:\Users\...\cb_xxxx\subs.srt`），在 filter_complex 中引用
- filter_complex 方式：在 filter_complex_script 末尾追加 `;[0:v]subtitles='path'[vsub]`，输出映射改为 `[vsub]`

### 9.4 音频采样率冲突

- FreeSound 预览 BGM 通常是 24000Hz mono，TTS 输出也是 24000Hz mono
- amix 混合后默认输出可能保持 24000Hz，但视频标准是 48000Hz stereo
- 修复：`-ar 48000 -ac 2` 强制输出 48kHz 立体声

---

## 10. TTS 与字幕

### 10.1 edge-tts 不支持 SSML

- `edge_tts.Communicate(ssml, voice)` 不解析 SSML 标签，直接**朗读 XML 标签内容**
- 导致 TTS 时长飙升至 30s+（在念 "speak version 1.0 xmlns"）
- 修复：始终使用纯文本调用 `edge_tts.Communicate(text, voice).save(path)`
- 如需控制停顿，在原始文本中加入标点符号（edge-tts 会自然停顿）

### 10.2 字幕时长与实际 TTS 同步

- 字幕结束时间使用 `_wav_duration()` 读取 WAV 实际时长，而不是字符数估算
- `_char_per_sec()` 作为回退（读取失败时使用）
- 字幕文本去掉/替换标点符号为空格：
  - 句末（。！？）→ 两个全角空格
  - 句中（，、：；）→ 一个全角空格
