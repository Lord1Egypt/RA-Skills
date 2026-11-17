# Ad Clone

Script: `scripts/ad_clone.py`

## Two steps: analyze first, then clone

```bash
# Step 1: analyze the reference video to get a prompt
python3 scripts/ad_clone.py analyze --video-url https://.../reference.mp4

# Step 2: use the analysis result to generate the new video
python3 scripts/ad_clone.py generate --prompt "<prompt returned by the previous step>" \
  --video-url https://.../reference.mp4
```

`analyze` is synchronous and returns a structured shot breakdown and prompt. Feed its prompt into `generate` as-is, or tweak a few lines first to match the user's needs — this is the most effective place to adjust the cloned result.

## analyze — video analysis (synchronous)

```bash
python3 scripts/ad_clone.py analyze --video-url https://.../ref.mp4 \
  --clip-start 3 --clip-end 15
```

- `--clip-start` / `--clip-end` trim by seconds so only that segment is analyzed
- **Each segment is capped at 12 seconds** — trim longer videos first

## generate — clone generation (asynchronous)

```bash
python3 scripts/ad_clone.py generate --prompt "..." --duration 12 --ratio 9:16
```

- `--duration` must be 4 / 8 / 12 / 16 / 20 seconds; defaults to 12
- `--ratio` defaults to 9:16

Passing `--video-url` with the original reference video anchors the style so the resulting clip stays closer to the source's look and feel; omit it to generate purely from the prompt.

## inspect — analysis only, no generation (asynchronous)

```bash
python3 scripts/ad_clone.py inspect --video-url https://.../any.mp4
```

Runs a shot-by-shot content analysis on any video. The difference from `analyze`: `analyze` produces a prompt **for cloning**, while `inspect` produces a **human-readable** content breakdown, suited to use cases like competitor teardown and asset archiving.

## Editable clone (v2beta draft flow)

When the user wants to **rewrite the dialogue, swap in their own on-screen person or product, or see the credit cost first**, use the draft flow instead of `analyze → generate`:

```bash
# 1. Create a draft; the script waits for the analysis by default (the trimmed source must be ≤15 seconds)
python3 scripts/ad_clone.py draft-create --video-url https://.../ref.mp4 --clip-start 0 --clip-end 12

# 2. Preview: returns the rebuilt prompt, reference bindings and the credit quote -- no charge, nothing generated
python3 scripts/ad_clone.py draft-preview --clone-id acl_xxx \
  --line "L1=This serum changed my skin in a week." \
  --ref "person@subject_1=https://.../my_actor.jpg" \
  --aspect-ratio 9:16 --duration 12 --quantity 2

# 3. After the user accepts the quote, submit with exactly the same edits (credits are charged, then the task is created)
python3 scripts/ad_clone.py draft-submit --clone-id acl_xxx \
  --line "L1=This serum changed my skin in a week." \
  --ref "person@subject_1=https://.../my_actor.jpg" \
  --aspect-ratio 9:16 --duration 12 --quantity 2
```

What you can edit in the draft (the `draft` returned by `draft-create` / `draft-get`):

- `lines`: lines of dialogue. Only `text` is editable; `--line L2=` with empty text mutes that line
- `slots`: subjects detected in the footage. Replace one with your own image via `--ref TYPE@SLOT_ID=IMAGE_URL`, where TYPE is `product`, `person` or `scene`; the `--ref` flags are the **final** set of reference images
- `gen_options`: available aspect ratios and resolutions; `pricing`: the default quote; `limits`: at most 9 reference images (at most 2 people), 4–15 seconds, up to 4 videos per submission

Key points:

- When `draft-preview` and `draft-submit` get **exactly the same** edits, the submission uses the prompt you saw in the preview
- `draft-submit` charges credits -- **tell the user the quote from `draft-preview` and get their confirmation before submitting**
- Drafts are kept for 24 hours and are readable only with the API key that created them; an expired or unknown draft makes `draft-get` return `status=not_found` rather than an error
- For complex edits, pass the whole `edits` object: `--edits-json '{"lines": [...], "references": [...], "prompt": "..."}'` or `--edits-json @edits.json`
- Not supported yet: multi-segment clones longer than 15 seconds, `other`-type reference images, choosing a voice
- The generation task behaves like `generate`: on timeout, resume with `query --workspace-id <id>`; with `--quantity` above 1 the script waits for each video in turn

## Typical chaining

The cloned output often needs further processing, chained across skills:

```bash
# Clone → swap in your own on-screen character
python3 scripts/ad_clone.py generate --prompt "..." --no-wait
# Once you have the workspace_id, continue with adsturbo-video-transform's character-swap

# Clone → translate to English for overseas placement
# Use adsturbo-video-transform's translate --target-lang en
```

## Assets must be public URLs

`--video-url` only accepts URLs — upload local files first:

```bash
python3 scripts/upload.py file ./reference.mp4
```

## Time estimates

| Operation | Estimated time |
|---|---|
| `analyze` | 30 seconds – 2 minutes (synchronous return) |
| `generate` | 3–10 minutes |
| `inspect` | 1–3 minutes |
| `draft-create` | Async analysis; the script waits for the draft by default (up to 10 minutes) |
| `draft-preview` | Synchronous |
| `draft-submit` | Similar to `generate` |

Asynchronous commands poll automatically by default; if it times out, use `query --workspace-id <id>` to keep waiting — the task is not lost.

---

# 广告视频复刻 / Ad Clone

脚本：`scripts/ad_clone.py`

## 两步走：先拉片，再复刻

```bash
# 第一步：分析参考视频，拿到提示词
python3 scripts/ad_clone.py analyze --video-url https://.../reference.mp4

# 第二步：用分析结果生成新视频
python3 scripts/ad_clone.py generate --prompt "<上一步返回的 prompt>" \
  --video-url https://.../reference.mp4
```

`analyze` 是同步的，返回结构化的分镜与提示词。把它的 prompt 原样喂给 `generate`，也可以先按用户的需求改几句再喂——这是调整复刻结果最有效的地方。

## analyze — 拉片（同步）

```bash
python3 scripts/ad_clone.py analyze --video-url https://.../ref.mp4 \
  --clip-start 3 --clip-end 15
```

- `--clip-start` / `--clip-end` 按秒裁剪，只分析其中一段
- **单个片段上限 12 秒**，超长视频要先裁

## generate — 复刻生成（异步）

```bash
python3 scripts/ad_clone.py generate --prompt "..." --duration 12 --ratio 9:16
```

- `--duration` 只能是 4 / 8 / 12 / 16 / 20 秒，不传按 12 秒
- `--ratio` 不传按 9:16

`--video-url` 传原参考视频可以锚定风格，让成片更贴近原片质感；不传则纯按 prompt 生成。

## inspect — 只分析不生成（异步）

```bash
python3 scripts/ad_clone.py inspect --video-url https://.../any.mp4
```

对任意视频做逐镜头内容分析。跟 `analyze` 的区别：`analyze` 的产出是**为了复刻**的提示词，`inspect` 的产出是**给人读**的内容理解，适合竞品拆解、素材归档这类场景。

## 可编辑复刻（v2beta 草稿流程）

用户想在生成前**改台词、把出镜人物或产品换成自己的、先看要花多少积分**时，用草稿流程代替 `analyze → generate`：

```bash
# 1. 创建草稿，脚本默认等分析完成（源片段截取后须 ≤15 秒）
python3 scripts/ad_clone.py draft-create --video-url https://.../ref.mp4 --clip-start 0 --clip-end 12

# 2. 预览：返回重建后的 prompt、参考图绑定和积分报价，不扣费、不生成
python3 scripts/ad_clone.py draft-preview --clone-id acl_xxx \
  --line "L1=This serum changed my skin in a week." \
  --ref "person@subject_1=https://.../my_actor.jpg" \
  --aspect-ratio 9:16 --duration 12 --quantity 2

# 3. 用户确认报价后，用完全相同的编辑参数提交（先扣积分，再建任务）
python3 scripts/ad_clone.py draft-submit --clone-id acl_xxx \
  --line "L1=This serum changed my skin in a week." \
  --ref "person@subject_1=https://.../my_actor.jpg" \
  --aspect-ratio 9:16 --duration 12 --quantity 2
```

草稿（`draft-create` / `draft-get` 返回的 `draft`）里能改什么：

- `lines`：台词句。只有 `text` 能改，`--line L2=` 传空串表示这句不说
- `slots`：画面里识别出的主体。用 `--ref TYPE@SLOT_ID=图片URL` 换成自己的图，TYPE 为 `product`（产品）、`person`（人物）、`scene`（场景）；`--ref` 给的是**最终**参考图集合
- `gen_options`：可选画幅和分辨率；`pricing`：默认报价；`limits`：参考图最多 9 张（人物最多 2 张）、时长 4–15 秒、一次最多生成 4 条

要点：

- `draft-preview` 和 `draft-submit` 传**完全相同**的编辑参数时，提交的就是预览里看到的 prompt
- `draft-submit` 会扣积分，**提交前先把 `draft-preview` 的报价告诉用户，确认后再提交**
- 草稿保存 24 小时，只有创建它的 API Key 能读到；过期或不存在时 `draft-get` 返回 `status=not_found`，不报错
- 复杂编辑可以直接传整个 `edits` 对象：`--edits-json '{"lines": [...], "references": [...], "prompt": "..."}'`，或 `--edits-json @edits.json`
- 暂不支持：超过 15 秒的多段复刻、`other` 类参考图、自选配音音色
- 生成任务和 `generate` 一样，超时用 `query --workspace-id <id>` 续等；`--quantity` 大于 1 时会逐条等完

## 典型串联

复刻出来的成片常常还要再加工，跨 skill 串起来：

```bash
# 复刻 → 换成自己的出镜人
python3 scripts/ad_clone.py generate --prompt "..." --no-wait
# 拿到 workspace_id 后，用 adsturbo-video-transform 的 character-swap 接着处理

# 复刻 → 翻译成英文投海外
# 用 adsturbo-video-transform 的 translate --target-lang en
```

## 素材必须是公网 URL

`--video-url` 只收 URL，本地文件先传：

```bash
python3 scripts/upload.py file ./reference.mp4
```

## 耗时参考

| 操作 | 预计 |
|---|---|
| `analyze` | 30 秒 – 2 分钟（同步返回） |
| `generate` | 3–10 分钟 |
| `inspect` | 1–3 分钟 |
| `draft-create` | 异步分析，脚本默认等到草稿完成（最多 10 分钟） |
| `draft-preview` | 同步返回 |
| `draft-submit` | 与 `generate` 相当 |

异步命令默认自动轮询；超时用 `query --workspace-id <id>` 续等，任务不会丢。
