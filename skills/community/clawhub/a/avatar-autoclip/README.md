# 三剪客 · 数字人自动剪辑（avatar-autoclip）

一张人物图片 + 一段音频，一条命令出成品短视频。

```
人物图片 ─┐
          ├─► 图片数字人 pic_lipsync ──► 口播视频 ─┐
驱动音频 ─┘                                        ├─► 智能剪辑 smart_clip ──► 成片
                                 剪辑模板 + 素材 ──┘
```

本包把平台上两个本来独立的异步应用（图片数字人、智能剪辑）串成一条流水线，
并补齐了它们之间缺的那一段：任务轮询、结果取址、参数预检、授权门禁、AI 标识。

---

## 要准备什么

**最少两样**：**一张人物参考图**（单边 < 2000px，正面半身）+ **一段口播文案**（中文约 4 字/秒）。

想更好，再加：

- **本人的声音样本**（10~60 秒干净人声）→ `clone` 出专属音色，声音才像本人
- 素材图/视频（`--material`，图片按 2 秒/张计，总量 ≤5 分钟）
- 模板 ID（不指定就自动用 realMan 第一条；先跑 `templates` 看）
- API Key（[注册领取](https://api.a7w.cn/)，包内不含密钥）

## 画质：别用 `--quality fast`

实测数字人的 `quality` 直接决定输出分辨率，而成片分辨率由模板画布决定：

| `quality` | 输出（输入 768×1344） | 结果 |
|---|---|---|
| `fast` | **480×840** | ❌ 被放大 2.25 倍，**必然发虚** |
| `standard` | 640×1120 | ⚠️ 放大 1.7 倍 |
| `max` | **768** | **768×1344** | **1.4 倍（最好）** |

用 1080×1920 的图去跑，`max` 档输出仍是 768×1366 ——
所以 **`max` 的语义是「档位上限 768」，不是「跟随输入分辨率」**（已实测纠正）。

本链路能做到的最好画质：

```bash
python -X utf8 scripts/dhclip.py make \
  --ref https://your-cdn/ref.jpg \
  --portrait-resolution 2K --portrait-model nano-banana-pro \
  --fit 1080x1920 \
  --text "文案" --voice <音色ID> --quality max \
  --auto-cover --authorized --wait
```

- 2K **必须**配 `--portrait-model nano-banana-pro`（普通模型配 2K 直接失败）
- 2K 生图 1536×2752 单边超数字人 2000px 上限，`--fit` 缩到 1080×1920 再上传（给上游更多细节去降采样）
- **最终仍会被放大 1.4 倍**，这是这条链路的物理上限

**要真正的 1080p 清晰**：用 `--dh-video` 直接喂一支 **1080p 真人出镜视频**，
跳过数字人那一步，剪辑端就原样渲染、不放大。

## 声音：两种正路

平台自带 38 个音色是**通用音色**，不会像某个人。

```bash
# 路线 A：直接用本人录音（最像）
python -X utf8 scripts/dhclip.py make --image <形象图> \
  --audio https://your-cdn/本人录音.mp3 --quality max --authorized --wait

# 路线 B：克隆本人音色，再用它念文案
python -X utf8 scripts/dhclip.py clone --title "张三的声音" \
  --audio https://your-cdn/本人声音样本.wav
python -X utf8 scripts/dhclip.py make --image <形象图> \
  --text "文案" --voice <音色ID> --quality max --authorized --wait
```

⚠️ **默认音色是列表第一条（女声）**。人物是男性却不换，声音会完全不搭 ——
先 `voices --limit 50` 挑一个性别年龄对得上的（如 `音色1小帅`、`解说2男-秒剪剧`）。

## 前置条件



| 需要什么 | 说明 |
|---|---|
| **Python 3.8+** | 只用标准库，**不需要 `pip install` 任何东西** |
| **一把 API Key** | 到 [算力集市](https://api.a7w.cn/) 注册 → 创建 Key。Key 的权限要允许 `app` 类型 |
| **账号有点数** | 提交类调用会扣点。查询类（模板/音色/价格/余额）免费 |
| **公网可达的素材 URL** | 人物图片、驱动音频、素材都必须公网可访问。**平台探不到媒体时长会直接拒绝创建任务** |
| **人物授权** | 人像与声音是人格权，**必须已获本人授权**。未获授权不要用 |

可选：本机有 `ffprobe` 时，本地视频素材的时长与分辨率会被真正探测，预检更准。

### 配 Key

三选一，按顺序解析：

```bash
# 1) 环境变量（推荐）
export AVATAR_AUTOCLIP_KEY=sk-你的key        # Windows PowerShell: $env:AVATAR_AUTOCLIP_KEY="sk-…"

# 2) 命令行
python -X utf8 scripts/dhclip.py --key sk-你的key balance

# 3) 本机配置文件 ~/.a7w/config.json 的 {"key":"sk-…"}（会被自动读取）
```

也会依次尝试 `A7W_API_KEY` / `A7W_KEY` / `LIKEADMIN_API_KEY`。
**包内不内嵌任何密钥。**

---

## 使用

### 先自检（不花钱、不需要 Key）

```bash
PYTHONDONTWRITEBYTECODE=1 python -X utf8 scripts/selftest.py
# 期望：Ran 60 tests ... OK
```

### 一条命令出片

```bash
python -X utf8 scripts/dhclip.py make \
  --image  https://your-cdn/face.jpg \
  --audio  https://your-cdn/voice.mp3 \
  --template 6a2668a137004e003477b6ed \
  --title "今天聊三件事" \
  --material image=https://your-cdn/a.jpg \
  --material video=https://your-cdn/b.mp4 \
  --introduce-name "张三" --introduce-desc "AI 行业观察" \
  --pack-header --pack-subtitle \
  --authorized --wait
```

- 用 `--text "口播文案"` 代替 `--audio`，内部会先串 TTS 生成音频
- 用 `--dh-video <已有口播视频>` 跳过数字人，只做剪辑
- 不给 `--template` 就自动挑 `realMan` 场景第一条；也可 `--template-name 关键字`

### 分步

```bash
# 看模板（免费）与模板结构
python -X utf8 scripts/dhclip.py templates --scene realMan --page-size 10
python -X utf8 scripts/dhclip.py template --id 6a2668a137004e003477b6ed

# 只做数字人
python -X utf8 scripts/dhclip.py lipsync \
  --image https://your-cdn/face.jpg --audio https://your-cdn/voice.mp3 \
  --quality fast --authorized --wait

# 只做剪辑
python -X utf8 scripts/dhclip.py realman \
  --template 6a2668a137004e003477b6ed --video https://your-cdn/dh.mp4 --wait

# 继续查一个 task_id（等待超时后用这个）
python -X utf8 scripts/dhclip.py task task_xxxxxxxx --wait

# 音色 / TTS / 余额 / 价格 / 上传
python -X utf8 scripts/dhclip.py voices --limit 20
python -X utf8 scripts/dhclip.py tts --text "大家好，欢迎来到今天的分享。"
python -X utf8 scripts/dhclip.py balance
python -X utf8 scripts/dhclip.py pricing
python -X utf8 scripts/dhclip.py upload ./local.mp4
```

### 安全阀

| 开关 | 作用 |
|---|---|
| `--dry-run` | 只打印将要提交的请求体，**不发写请求** |
| `--budget 50` | 预算上限，单位是**点**；超了就地中止，退出码 5 |
| `--authorized` | 声明已获人像/声音授权（`lipsync` / `make` 必需，否则退出码 7） |
| `--json` | JSON 输出，便于脚本消费 |
| `--no-ai-label` | 关掉默认开启的 AI 生成标识 |

**退出码**：0 成功 / 2 用法错 / 3 上游错 / 4 本地预检不过（不花钱）/ 5 超预算 / 6 等待超时 / 7 缺授权声明。

### 13 个子命令

```
balance  pricing  voices  tts  upload  task  templates  template
lipsync  realman  mixcut  news  make
```

---

## 依赖

**运行时零第三方依赖**，只用 Python 标准库（`urllib`、`json`、`argparse` 等）。

- 不需要 `pip install`
- 不需要 Node、不需要 ffmpeg
- `ffprobe` 是**可选**增强：装了它，本地视频素材的时长/分辨率会被真正探测，
  预检更准；没装也不影响出片，只是探不到的项不假装知道

跑自检时建议加 `PYTHONDONTWRITEBYTECODE=1`，避免生成 `__pycache__`。

---

## 安全

- **包内零凭据**：不内嵌任何 Key/Token/Cookie
- Key 只从命令行、环境变量或本机 `~/.a7w/config.json` 读，**不落盘、不进日志、不进错误信息**
- 只连 `--base` 指定的一个地址，无遥测、无第三方埋点
- 不写任何文件、不改任何配置；`--json` 也是打到 stdout
- **有人格权硬门禁**：`lipsync` / `make` 不传 `--authorized` 直接拒绝，一个请求都不发
- 剪辑类命令默认开 AI 生成标识（实测水印真实渲染到画面左下角）

⚠️ **数字人涉及人格权（肖像权、声音权），不是版权。人格权不可转让，只能取得本人授权。**
未获授权的人像与声音不要使用，也不要用明星、公众人物或来源不明的网络图片。

---

## 实测

| 环节 | 结果 |
|---|---|
| 图片数字人 | ✅ 真实 mp4，480x832 / 24fps / 4.875s，含音频；约 36 秒出片 |
| 自动剪辑 | ✅ 真实 mp4，**1080x1920** / 25fps / 4.88s；约 93 秒，实扣 7.32 点 |
| 模板效果 | ✅ 标题图层 + 双语字幕（平台自动 ASR） |
| AI 生成标识 | ✅ 画面左下角实际渲染出「AI 生成」 |
| 离线自测 | ✅ 60/60 通过 |

扣费口径以响应里的 `usage.points_cost` 为准。

---

## 联系我们

- **技术微信：9872659** —— 加好友时说一下是从哪个 Skill 找过来的，直接给你配套的 API Key 与能跑的示例。
- **要算力 / 要 API Key**：[算力集市 · 注册领 API Key](https://api.a7w.cn/) —— 一个 Key 调用全部 AI 算力，注册、充值、创建 Key 都在这里。
- **更多 AI 插件与接口**：[AI 插件市场](https://aigc.a7w.cn/)。

---

## 相关链接

| 链接 | 地址 | 说明 |
|---|---|---|
| 算力集市 · 注册领 API Key | https://api.a7w.cn/ | 一个 Key 调用全部 AI 算力；注册、充值、创建 Key 都在这 |
| AI 插件市场 | https://aigc.a7w.cn/ | 浏览全部 AI 插件与接口说明 |
| 三剪客 · 一句话批量出片 | https://ks.a7w.cn/ | 短剧二创 / 影视解说 / 矩阵号批量混剪桌面客户端 |
| 视频超清 · 在线批量超分 | https://vr.a7w.cn/ | 网页版视频超分，批量处理，最高 4K |
| 0人公司 · AI Agent 平台 | https://a7w.cn/ | 主站，了解整套 AI Agent 生态 |
