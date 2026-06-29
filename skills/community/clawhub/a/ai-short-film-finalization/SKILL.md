---
name: ai-short-film-finalization
description: Finalize an AI-generated short film using the free Route C pipeline (Google Flow Omni Flash text-to-video, Nano Banana 2 image generation, edge-tts narration, Chrome CDP automation). Covers shot generation, consistency checks, 1080p composition with subtitles/BGM, director review console, and highlight trailer.
agent_created: true
---

# AI 短片制作与 Finalization — 路线 C：Flow 免费方案

## 概述

本 Skill 覆盖 **零成本 AI 短片全链路**，采用 **路线 C**：

| 环节 | 工具 | 成本 |
|------|------|------|
| 文生图 | Google Flow Nano Banana 2 | 免费（Google Labs 积分） |
| 图生视频 / 文生视频 | Google Flow Omni Flash | 免费（Google Labs 积分） |
| 配音 | edge-tts | ¥0 |
| 浏览器自动化 | Chrome CDP + Playwright | ¥0 |
| 合成 / 字幕 / 审片 | FFmpeg + PIL + Python | ¥0 |

适用场景：用户已有分镜脚本，需要批量生成画面、配音、字幕，并输出带导演审片功能的 1080p 成片。

两大阶段：
1. **RPA 批量生成**：通过 CDP 复用用户已登录的 Chrome，自动化 Google Flow 的 Nano Banana 2 与 Omni Flash。
2. **Finalization**：一致性检查、配音/字幕/画面节奏同步、BGM 混音、导演审片控制台、高光预告片。

## 路线 C：RPA 视频生成工作流

核心模式：**Chrome DevTools Protocol (CDP) + Playwright 人类化操作**。

- 启动 Chrome 并开启 `--remote-debugging-port=9222`。
- Playwright 通过 `chromium.connectOverCDP('http://127.0.0.1:9222')` 连接。
- 复用用户已有的 Google 登录态，无需处理 OAuth / 2FA / cookie。
- 使用 `humanMove` / `humanClick` / `humanScroll` / `humanType` 等随机延迟/抖动操作，降低被检测风险。

### 1. 环境准备

**启动 Chrome（macOS 示例）：**
```bash
pkill -9 "Google Chrome"; sleep 2
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/Library/Application Support/Google/Chrome/Default" \
  "https://labs.google/fx/tools/flow" &
sleep 5
```

**Node 依赖：**
```bash
cd /Users/zzhwj2026/.workbuddy/binaries/node/workspace
/Users/zzhwj2026/.workbuddy/binaries/node/versions/22.12.0/bin/npm install playwright-core
```

运行时设置：
```bash
export NODE_PATH=/Users/zzhwj2026/.workbuddy/binaries/node/workspace/node_modules
```

**Python 依赖（TTS / 字幕 / 合成）：**
```bash
/Users/zzhwj2026/.workbuddy/binaries/python/versions/3.13.12/bin/python3 -m venv /Users/zzhwj2026/.workbuddy/binaries/python/envs/default
/Users/zzhwj2026/.workbuddy/binaries/python/envs/default/bin/pip install edge-tts pillow
```

**验证 CDP：**
```bash
curl -s http://127.0.0.1:9222/json/version | head -3
```

### 2. Nano Banana 2 文生图

用于生成关键帧、参考图、角色肖像、fallback 静态图。

示例：
```bash
node generate-image.js \
  --prompt "Cinematic portrait of a young Chinese woman soldier, round face, short black hair, wearing grey cotton Eighth Route Army uniform, flat-topped cloth cap with two plain front buttons, red scarf, determined expression, 1940 northern China, soft daylight" \
  --aspect 16:9 \
  --count x2 \
  --output ./images
```

参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--prompt` | 英文提示词 | **必填** |
| `--aspect` | 16:9 / 9:16 / 4:3 / 1:1 / 3:4 | 16:9 |
| `--count` | 1x / x2 / x3 / x4 | x2 |
| `--model` | Nano Banana 2 / Nano Banana Pro | Nano Banana 2 |
| `--output` | 输出目录 | /tmp/flow-images |

### 3. Omni Flash 文生视频 / 图生视频

**文生视频：**
```bash
node generate-one.js \
  --prompt "Video of a young Chinese woman soldier riding a black horse across a dusty mountain valley, 1940 northern China, grey cotton uniform, flat-topped cloth cap, red scarf, modern rifle, cinematic lighting" \
  --output ./videos
```

⚠️ **Omni Flash 提示词必须以 `Video of` 开头**，否则模型会出图。脚本应自动补前缀。

**图生视频（推荐，一致性更强）：**
```bash
node generate-img2video.js \
  --image ./images/01-李林肖像.jpg \
  --prompt "Slow camera push in, gentle ambient motion, cinematic lighting" \
  --duration x2 \
  --output ./videos
```

参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--image` | 参考图路径 | 图生视频必填 |
| `--prompt` | 视频运动/镜头描述 | 自动生成 |
| `--duration` | x2(10s) / x3(15s) / x4(20s) | x2 |
| `--aspect` | 16:9 / 9:16 | 16:9 |

### 4. 角色一致性策略

- 用 Nano Banana 2 生成一张主角标准像 `standard-portrait-v2.jpg`。
- 需要人物一致性的镜头：先用 Nano Banana 2 生成该镜头关键帧，再用 `generate-img2video.js` 图生视频。
- 平民 / 学生 / 童年场景：禁用参考图，避免军装污染。
- 群像镜头：禁用参考图，避免所有人脸都变成主角。
- 在提示词中明确重复角色外貌与时代服饰，比模糊形容词更有效。

### 5. 批量编排：flow-workflow.js

分镜脚本格式：
```json
{
  "project": "li-lin",
  "episodes": [{
    "id": "E01",
    "shots": [
      {
        "id": "S01",
        "type": "narration",
        "prompt_image": "英文图片提示词，用于 Nano Banana 2",
        "prompt_video": "Video of ... 英文视频提示词，用于 Omni Flash",
        "duration": "x2"
      }
    ]
  }]
}
```

运行：
```bash
node flow-workflow.js --script storyboard.json --mode full --output ./output
```

模式：

| 模式 | 行为 | 适用场景 |
|------|------|----------|
| `full` | 文生图 → 图生视频 | 默认，一致性最好 |
| `image-only` | 只出图 | 需要人工挑选关键帧 |
| `video-only` | 直接文生视频 | 快速出片，一致性略弱 |

输出结构：
```
output/项目名称/
├── images/                 # 生成的参考图
├── videos/                 # 生成的视频片段
├── workflow-results.json   # 制作报告
└── debug-*.png             # 调试截图
```

### 6. Flow RPA 关键 know-how

- **提示词必须以 `Video of` 开头**，否则 Omni Flash 会生成图片。
- **每次生成前点击 "New session"**，否则输入会被当成聊天回复。
- **空状态页面**：若出现 "doesn't seem to be anything here"，脚本应自动返回主页创建项目。
- **DOM 状态检测优于 URL 判断**：Flow 的项目 URL 可能不含 `/project/`，应检测页面元素。
- **进程退出**：脚本 `finally` 块末尾必须调用 `process.exit(0)`；CDP WebSocket 会保持事件循环活跃，导致 Node 不退出。**不要调用 `browser.close()`**，否则会关闭用户 Chrome。
- **下载视频**：通过 DOM 检测新生成的 `<video src>`，用 `page.request.get()` 复用 cookie/CORS 下载。
- **积分参考**：Omni Flash 约 15 credits/条，Nano Banana 2 约 3-5 credits/条。
- **生成超时**：图片通常 30-60s，视频通常 2-5min；高需求时可能排队 30s-5min。

### 7. 历史题材提示词规范

**正面描述（八路军 / 抗战题材）：**
```
young Chinese woman commander, round face, short black hair,
grey cotton Chinese Communist Eighth Route Army uniform,
flat-topped cloth cap with two plain front buttons,
red scarf around neck, no cap badge, no insignia,
holding a modern rifle, 1940 northern China
```

**负面提示词（每条生成必须带）：**
```
no ancient armor, no spears, no longbows, no crossbows,
no Japanese uniforms on Chinese soldiers,
no peaked caps, no cap badges, no visors, no samurai helmets,
no modern clothing, no suits, no ties, no dresses,
no smartphones, no cars, no electric lights, no concrete buildings,
no feudal castles, no palaces, no ancient Chinese architecture unless scripted
```

## 一致性检查清单（合成前闸门）

合成前对 **每个镜头** 运行以下检查。任一失败 = 重制该镜头。

### A. 角色一致性

| 检查 | 通过标准 | 失败示例 |
|------|----------|----------|
| 面容 / 身份 | 主角在所有镜头中为同一人 | 镜头 06 换了演员 |
| 发型 | 长度、颜色、样式一致 | 镜头 01 短发，镜头 05 长发 |
| 性别 | 每镜性别正确 | 女主角被画成男性士兵 |
| 年龄 | 表观年龄一致（±5 岁） | 闪回童年却像成人 |
| 标准像匹配 |  resembles `standard-portrait-v2.jpg` | 生成的脸与参考图无关 |
| 服装连续性 | 同一场景内服装不变 | 连续镜头中外套变了 |

### B. 时代 / 年代一致性

| 检查 | 通过标准 | 失败示例 |
|------|----------|----------|
| 服装年代 | 服饰符合所述历史时期 | 1940 年抗战场景出现清朝长袍 |
| 武器年代 | 武器符合同期技术 | 1940 年出现火绳枪或 AK-47 |
| 建筑 | 建筑符合时期与地域 | 1940 年村庄出现混凝土高楼 |
| 交通 | 无时代错乱载具 | 1940 年中国农村出现汽车（除非剧本需要） |
| 电子设备 | 无时代错乱设备 | 1950 年前场景出现智能手机、电灯 |
| 文字 | 使用正确的文字体系 | 1956 年前出现简化字 |

### C. 军装 / 制服准确性（战争题材）

| 检查 | 通过标准 | 失败示例 |
|------|----------|----------|
| 制服颜色 | 派系颜色正确 | 八路军穿蓝色制服（应为灰色） |
| 帽型 | 帽型正确 | 平顶布帽被画成大檐帽 |
| 帽饰 | 无禁用元素 | 帽徽、帽檐、帽舌出现在八路军帽上 |
| 徽章 | 符合时代或不存在 | 国民党标志出现在共军士兵身上 |
| 武器类型 | 符合军队与时代 | 正规军主力武器是长矛 |
| 敌人形象 | 敌人不得穿中国军装 | 日军穿着八路军制服 |

### D. 背景 / 地点连续性

| 检查 | 通过标准 | 失败示例 |
|------|----------|----------|
| 季节 | 同一场景内季节一致 | 镜头 03 下雪，镜头 04 绿叶（同一天） |
| 时间 | 光照方向一致 | 同一场景广角是晨光，特写是正午 |
| 地形 | 地点符合剧本 | 北方战场出现热带丛林 |
| 天空 | 阴晴符合场景天气 | 剧本写“阴天硝烟”却出现蓝天 |
| 道具连续性 | 重复出现的道具一致 | 连续骑兵镜头马匹颜色不同 |

### E. 反时代错乱负面提示词（每条生成必须带）

```
no ancient armor, no spears, no longbows, no crossbows,
no Japanese uniforms on Chinese soldiers,
no peaked caps, no cap badges, no visors, no samurai helmets,
no modern clothing, no suits, no ties, no dresses,
no smartphones, no cars, no electric lights, no concrete buildings,
no feudal castles, no palaces, no ancient Chinese architecture unless scripted
```

### F. 参考图使用规则

| 场景类型 | `useRef` | 原因 |
|----------|----------|------|
| 军装 / 制服镜头 | `true` | 需要与制服保持角色一致 |
| 平民 / 学生 / 童年 | `false` | 参考图含军装，会污染平民服装 |
| 群像镜头（多人） | `false` | 参考图会让所有人长得像主角 |
| 风景 / 无角色 | `false` | 没有角色需要保持一致 |

## 后期审片工作流（v4 导演控制台）

首次成片渲染后，生成一个**自包含的导演审片控制台**，让人类导演独立检查每一镜的**画面、音频、字幕**，对每一部分决定是否重制，填写修改意见后自动生成可执行提示词，并支持在镜头之间**插入或删除镜头**。

### v4 核心能力

| 能力 | 说明 |
|------|------|
| 审片粒度 | **按组件**：画面 / 音频 / 字幕 各自独立通过/待定/重制 |
| 重制表单 | 每个组件有独立表单：问题类型、导演意见、自动提示词、工具选择、参考图开关 |
| 镜头管理 | 可在任意两镜之间**插入新镜头**；可**删除**任意镜头并撤销 |
| 新增镜头 | 默认所有组件为“重制”，填写标题/旁白/字幕/视频提示词即可 |
| 导出格式 | `director-fix-pack.json`，含 `fix_list` + `insert_list` + `delete_list` |
| 执行命令 | 每个 fix 条目生成对应的 `execution_cmd` |

### 审片包内容

每个镜头 / 段落包含：

1. **时间戳范围**（`start_ts`、`end_ts` 在成片中的位置）
2. **镜头 ID + 标题**（可编辑）+ 时代 + 情绪 + 镜头类型
3. **三个独立面板**：
   - 🎬 **画面面板**：独立 `.mp4` 片段 → 截图 → 通过/待定/重制开关 → 重制表单
   - 🔊 **音频面板**：独立 `.mp3` 片段 → 通过/待定/重制开关 → 重制表单
   - 📝 **字幕面板**：字幕文本展示 → 通过/待定/重制开关 → 重制表单
4. **插入区**：每两个镜头之间的 ➕ 按钮
5. **删除/撤销**：每镜标题上的 🗑 / ↩ 按钮
6. **卡片边框颜色**：绿色=全部通过，红色=有重制，橙色=有待定
7. **摘要栏**：总时长、有效镜头数、通过/待定/重制/删除计数

### 生成审片包

```bash
cd /path/to/project
python3 review-final-v4.py --project-root . \
  --output review-v4/ \
  --template-html review-director-template.html
```

该脚本会：
- 读取 `storyboard-v2.json` 并计算每镜时间戳
- 用 ffmpeg 提取每镜视频片段到 `review-v4/clips/`
- 提取每镜音频到 `review-v4/audio/`
- 提取中间帧到 `review-v4/frames/`
- 写入 `review-v4/manifest.json`
- 读取 `review-director-template.html` 并替换 `__MANIFEST_DATA__` 和 `__PROJECT_NAME__`
- 输出 **自包含单文件 HTML** `review-v4/review.html`，数据内联，无需服务器/CORS

### 导演审片流程

1. 在浏览器或 WorkBuddy 预览面板中打开 `review.html`
2. 每镜独立检查三个面板：
   - 点击 ✅ 通过 / ⚠️ 待定 / ❌ 重制
   - 选择 ❌ 重制 后展开对应表单
3. **插入镜头**：点击两镜之间的 ➕，填写标题、旁白、字幕、视频提示词
4. **删除镜头**：点击 🗑 变灰，可点击 ↩ 撤销
5. 点击 **📋 导出修改包** → 下载 `director-fix-pack.json`

### 导出格式：`director-fix-pack.json`

```json
{
  "project": "li-lin",
  "summary": {
    "total_shots": 12,
    "fix_items": 3,
    "new_shots": 1,
    "deleted_shots": 1
  },
  "fix_list": [
    {
      "uid": "shot-06",
      "shot_id": 6,
      "title": "抗日烽火",
      "component": "video",
      "director_note": "李林的脸不像参考图",
      "prompt": "Cinematic wide shot... [导演修改要求] 在提示词中强化角色外貌描述...",
      "tool": "flow-img2video",
      "use_ref": true,
      "problem_type": "角色不一致",
      "execution_cmd": "node generate-img2video.js --image images/06-抗日烽火.jpg --prompt '...' --output videos/06-抗日烽火.mp4",
      "start_ts": 34.9,
      "end_ts": 43.1
    }
  ],
  "insert_list": [
    {
      "uid": "new-1719312000000",
      "title": "过渡镜头",
      "position": 6,
      "narration": "旁白文本...",
      "video_prompt": "Video of ...",
      "video_tool": "flow-img2video",
      "use_ref": false,
      "voice": "zh-CN-XiaoxiaoNeural",
      "rate": "+0%"
    }
  ],
  "delete_list": [
    { "uid": "shot-07", "id": 7, "title": "军民情深" }
  ]
}
```

### 精确重制循环

1. 导演导出 `director-fix-pack.json`
2. AI 读取并处理三份列表：
   - **fix_list**：按组件重制（画面/音频/字幕），执行对应 `execution_cmd`
   - **insert_list**：在指定位置生成新镜头的视频 + 音频 + 字幕
   - **delete_list**：从分镜中删除镜头并重新合成
3. 更新 `storyboard-v2.json`
4. 重新运行 `compose-final-v4.py` 合成成片
5. 重新运行 `review-final-v4.py` 生成新的审片包
6. 导演再次审片，循环直至定稿

## Finalization 工作流

1. **等待批量生成任务完成**。若单镜头卡住超过 10 分钟，杀掉并生成 fallback。
2. **合成前一致性审查**：按上述检查清单逐镜检查。
3. **修复或替换问题镜头**：
   - 收紧提示词的负面约束。
   - 对超时的镜头，用 Nano Banana 2 生成静态图 + ffmpeg zoompan 生成慢推视频作为 fallback。
4. **运行最终合成**：`compose-final-v4.py` 生成 TTS、ASS 字幕、1080p 成片（含 hook/CTA/BGM）。
5. **生成审片包**：`review-final-v4.py` 输出自包含导演控制台。
6. **精确重制循环**：按导演反馈重制指定组件，更新分镜，重新合成。
7. **验证成片**：检查时长、分辨率、字幕同步（最后一条字幕结束与音频结束差距 ≤ 0.1s）。
8. **生成高光预告片**：使用 FFmpeg 从成片剪辑高光片段，避免依赖付费服务。

## 创新点与踩坑总结

### RPA / 浏览器自动化

1. **CDP 复用登录态省掉认证地狱**。连接用户已登录 Chrome，无需处理 Google OAuth / 2FA / cookie。
2. **人类化操作原语**。随机鼠标路径、点击停留、滚动步长、输入延迟，抽象成 `humanMove` / `humanClick` / `humanScroll` / `humanType` 复用。
3. **DOM 状态检测优于 URL 判断**。Flow 的页面状态变化不一定体现在 URL；应检测具体元素。
4. **每次生成前点击 "New session"**。否则输入会被当作聊天回复，导致失败。
5. **进程必须显式退出**。CDP WebSocket 会保持事件循环，脚本末尾调用 `process.exit(0)`；**绝不能调用 `browser.close()`** 关闭用户 Chrome。
6. **用 `page.request.get()` 下载生成结果**。自动携带 cookie 和 CORS 上下文。

### 提示词工程 / 历史准确性

7. **年代描述必须 explicit 且重复**。"grey cotton uniform, flat-topped cloth cap with two plain buttons, red scarf" 比 "revolutionary soldier" 有效。
8. **负面约束是必需的**。每条生成提示词必须带 no-list。
9. **参考图开关**。平民/学生/童年镜头禁用参考图，避免军装污染。
10. **Omni Flash 必须以 `Video of` 开头**。否则模型出图。

### 音频 / 字幕 / 节奏同步

11. **ASS 字幕必须与音频使用同一 TTS rate**。`edge-tts` 的 `SentenceBoundary` 偏移依赖 rate；rate 不同会导致字幕漂移数秒。
12. **每镜动态节奏优于固定时长**。`target_dur = audio_dur + 0.5s`，视频够长则裁剪，稍短则轻微慢放（≤15%）。
13. **禁止冻结最后一帧**。`tpad=stop_mode=clone` 会让影片像幻灯片。
14. **采样率一致性不可妥协**。`edge-tts` 输出 24000 Hz 单声道；在 `filter_complex` 中 `aresample=44100`，最终 concat 用 `-c:a aac -ar 44100` 重编码。`-c copy` 混音会导致几乎静音。
15. **FFmpeg 无 libass/libfreetype 时用 PNG 覆盖**。PIL 生成透明 PNG，通过 `overlay` + `enable='between(t\,start,end)'` 烧录字幕。

### 工具链 / 环境

16. **固定托管运行时**。使用 `/Users/zzhwj2026/.workbuddy/binaries/node/versions/22.12.0/bin/node` 与隔离的 `playwright-core`。
17. **批量运行器要容错**。单个镜头失败不应中断整批；try/catch 包裹并记录。
18. **预告片优先 FFmpeg**。本路线为零成本方案，高光预告片应使用 FFmpeg 从成片直接剪辑，不依赖额外付费服务。

## 可复用脚本清单

| 脚本 | 用途 |
|------|------|
| `generate-image.js` | Nano Banana 2 文生图 |
| `generate-one.js` | Omni Flash 文生视频 |
| `generate-img2video.js` | Omni Flash 图生视频 |
| `flow-workflow.js` | 短剧全流程编排：按 `storyboard.json` 批量出图/视频 |
| `compose-final-v4.py` | 导演级最终合成：TTS、ASS→PNG 字幕、节奏同步、BGM、hook/CTA |
| `review-final-v4.py` | v4 导演控制台生成器：拆分片段、提取音画、输出自包含 HTML |
| `review-director-template.html` | v4 导演控制台 HTML 模板，含 `__MANIFEST_DATA__` 占位符 |
| `generate-trailer-v4.py` | 基于 FFmpeg 的高光预告片 |

## 资源

- `references/consistency_checklist.md` — 逐镜检查清单。
- `references/fallback_prompts.md` — 常见问题镜头的收紧提示词。

## 备注

- 默认项目路径：`li-lin/videos/`、`li-lin/audio/`、`li-lin/subtitles/`、`li-lin/final/`。
- ffmpeg 路径：`/opt/homebrew/bin/ffmpeg`。
- Python venv：`/Users/zzhwj2026/.workbuddy/binaries/python/envs/default/bin/python3`。
- Node 二进制：`/Users/zzhwj2026/.workbuddy/binaries/node/versions/22.12.0/bin/node`。
- CDP 端点：`http://127.0.0.1:9222`（要求 Chrome 以 `--remote-debugging-port=9222` 启动）。
- Flow 地址：`https://labs.google/fx/tools/flow`。
