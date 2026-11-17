---
name: dlazy-ecommerce-avatar
version: 1.0.0
description: Ecommerce livestream avatar / AI spokesperson for product selling videos — 18 production-grade base-portrait recipes plus the full script→TTS→avatar→B-roll pipeline. Use when the user wants a digital human to sell a product on TikTok Shop, Douyin, Amazon, Shopee or a brand store.
metadata: {"clawdbot":{"emoji":"🛍️","requires":{"bins":["npm","npx"],"env.optional":["DLAZY_API_KEY"]},"install":"npm install -g @dlazy/cli@1.2.3","installAlternative":"npx @dlazy/cli@1.2.3","homepage":"https://dlazy.com","configLocation":"~/.dlazy/config.json","apiEndpoints":["api.dlazy.com","files.dlazy.com"]},"openclaw":{"systemPrompt":"When invoking this skill, read recipes.md before writing any base-portrait prompt, and run `dlazy <model> -h` to confirm current flags before building a command."}}
---

# 电商带货数字人口播

做一条带货口播视频，画面质量的胜负在**底图**就已经定了。

数字人模型（omnihuman / videoretalk / heygen）是音频驱动的口型与体态重建，它不重画你的人。`jimeng-omnihuman-1.5` 的提示词上限只有 **300 字符且可选**，`videoretalk`、`heygen-lipsync-speed`、`sync-lipsync-3` **根本没有 prompt 字段**。所以"让画面更真实细腻"这件事，写在数字人这一步是没有杠杆的——要写在生成底图那一步，那里 `gpt-image-2` 能吃 **2000 字符**。

差了 6.7 倍。这个技能就是把杠杆用在有杠杆的那一步。

（实际配方每条约 450~500 字符，远没到 2000 上限——重点不是写得长，是写得准：那 450 字里有一半在描述光比、焦段、皮肤质感和驱动约束，这些才是"真实细腻"的来源。）

## 何时使用

- 要做抖音 / TikTok Shop / 视频号 / Shopee 的带货口播视频
- 要一个稳定复用的虚拟主播形象（同一张脸出多条视频）
- 已经有数字人视频但"看着假"、"嘴部糊"、"手很怪"，需要回到底图定位问题
- 要给一个商品从零做出成片：选题 → 脚本 → 配音 → 数字人 → 空镜 → 装配

不适用于：真人出镜的口型替换（那是 `videoretalk` 直接上，不需要底图）、纯商品图（用 `dlazy-image-guide`）。

## 五条硬约束

这五条决定成败，先记住再动手。

**1. 底图必须"可驱动"，不是"好看"。**

数字人模型对底图有硬性要求，违反了口型和体态会直接崩：

| 必须 | 禁止 |
|---|---|
| 单人、正脸或侧脸 ≤ 20° | 多人同框、大角度侧脸、背身 |
| 五官完整清晰，嘴部无遮挡 | 口罩、话筒挡嘴、手托下巴、刘海遮眼 |
| 上半身入镜，肩部完整 | 只有头部特写、下巴被裁切 |
| 双手自然下垂或轻放（或不入镜） | 手在脸前、抱胸、手持复杂物件 |
| 柔和均匀光，光比 ≤ 2:1 | 强逆光、硬阴影切脸、彩色光打脸 |
| 背景与人物有明显景深分离 | 高对比花纹背景、背景有其他人脸 |

一张漂亮但侧脸 45° 的图，驱动出来嘴会飘。这是最常见的失败原因。

**2. 时长是硬上限，超了要分段。**

`jimeng-omnihuman-1.5` 的音频时长上限：**1080p ≤ 30 秒，720p ≤ 60 秒**。

一条 60 秒的带货口播，1080p 下必须切成 2~3 段分别驱动再拼接。写脚本时就按 25 秒一段来分，不要写完了才发现要重切。

**3. 尺寸参数六种写法互不通用，写错整次 400，积分不退。**

带货视频要竖屏 9:16：

- `gpt-image-2` → `--size 2160x3840`（4K 竖屏）或 `1024x1536`（2:3，注意不是 9:16）
- `seedream-5.0` → `--size 9:16 --resolution 4k`
- `banana-pro` → `--aspectRatio 9:16 --imageSize 4K`
- `qwen-image-2-pro` → `--size 1536*2688`

`gpt-image-2` **没有 9:16 的中等尺寸**，只有 `2160x3840` 这一个竖屏 4K 选项和 `1024x1536`（2:3）。要 9:16 又不想上 4K，用 `seedream-5.0`。

**4. 中文 prompt 走 `--input` JSON 文件，不要用 shell 变量拼。**

用 `$(...)` 把中文塞进命令行，在 Windows 上会静默变成乱码——命令依然返回 `ok: true`，但出图跟 prompt 毫无关系（通常是一张不知所云的"通用美女写真"）。实测踩过，排查成本很高。批量生产一律：

```bash
dlazy gpt-image-2 --input @payload.json --save ./avatar/base.png
```

详见 `troubleshooting.md` 的"编码陷阱"一节。

**5. 不确定先 `--dry-run`。** 打印载荷和积分预估，不出图不扣分：

```bash
dlazy gpt-image-2 --prompt "..." --size 2160x3840 --quality high --dry-run
```

## 五层流水线

```
① 底图     gpt-image-2 (2000字) / seedream-5.0 (500字)   ← 提示词杠杆全在这
② 脚本     claude-sonnet-5 / qwen3.8-max                  ← 按 25 秒/段切好
③ 配音     qwen-tts (512字上限) / doubao-tts              ← 超 512 整次 400
④ 驱动     jimeng-omnihuman-1.5 (300字, ≤30秒@1080p)      ← 只写运镜和幅度；单点依赖
⑤ 空镜     seedance-2.5 / kling-v3                        ← 长 prompt 全吃
⑥ 装配     dlazy chat --skill product-to-ecommerce-video  ← CLI 本身不做合成
```

**CLI 没有视频合成能力**——它是模型调用器。要交付一个 mp4，最后一步必须走沙箱模板（`dlazy chat --skill ...`）或你自己的 ffmpeg。别指望 `dlazy` 有 merge 命令。

**六层的输出规格互不相同。** omnihuman 720p 档出 704x1248@25fps/24000Hz 单声道，`seedance-2.5` 出 720x1280@24fps/32000Hz 立体声——拼接必须全重编码，`-c copy` 会让时间戳错位。详见 `pipeline.md` ⑥。

**④ 是单点依赖。** 5 个数字人模型里只有 `jimeng-omnihuman-1.5` 吃「静态图 + 音频」，其余四个都要「现成的说话视频 + 音频」才能换口型。它一挂，整条链路就断——降级要走「i2v 生成说话视频 → videoretalk 对口型」，成本翻倍。详见 `pipeline.md`。

完整逐步命令见 `pipeline.md`。

## 配方索引

`recipes.md` 里有 18 条经过参数校验的底图配方，每条都是可直接粘贴执行的完整命令。

| 组 | 配方 | 适用 |
|---|---|---|
| A 场景主播 | 01 白底极简 / 02 直播间实景 / 03 家居生活 / 04 美妆柔光 / 05 3C 冷调 / 06 服装衣帽间 / 07 食品暖调 / 08 母婴浅调 | 按品类选一条即可开工 |
| B 权威人设 | 09 专家型 / 10 商务型 / 11 工厂溯源 / 12 原产地 | 需要信任背书的品类 |
| C 景别变体 | 13 中近景主机位 / 14 情绪特写 / 15 全景带陈列 | 同一人设多机位，剪辑用 |
| D 产品镜头 | 16 手持展示 / 17 纯净白底主图 / 18 使用场景 | B-roll 与主图 |

选不动就用 **配方 01**：白底极简是转化率最稳的带货底图，也是最不容易驱动失败的。

## 保持同一张脸

带货账号要靠人设复用。三种做法，从稳到弱：

1. **存图复用**（推荐）——第一次生成满意后把底图存下来，之后所有视频都用同一个文件，脸 100% 一致
2. **参考图重绘**——`gpt-image-2 --images base.png --prompt "同一人物，换成..."`，能换背景服装保住脸，积分翻倍（33 起）
3. **纯文字复现**——不要指望，同样的 prompt 两次出的脸不是一个人

## 认证

```bash
dlazy login          # 设备码流程，自动保存 key
dlazy auth set KEY   # 已有 key 时直接写入
```

Key 从 https://dlazy.com/dashboard/organization/api-key 获取，保存在 `~/.dlazy/config.json`。也可用 `DLAZY_API_KEY` 环境变量按次传入。

积分不足返回 `insufficient_balance`，充值入口：https://dlazy.com/dashboard/organization/settings?tab=credits

## Reference Map

| 文件 | 内容 |
|---|---|
| `recipes.md` | 18 条底图配方，完整可执行命令 + 每条的驱动注意事项 |
| `pipeline.md` | ①~⑥ 逐步命令，含分段、拼接、成本估算 |
| `troubleshooting.md` | 驱动失败对照表、省积分策略、合规红线 |
