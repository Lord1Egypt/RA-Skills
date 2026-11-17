# URL to Video

Script: `scripts/url2video.py`

Paste a product page link and get a 15-second short-video ad. Defaults to 9:16, 720p.

## create — Make the Ad (Async)

```bash
# A product page link: the easiest way
python3 scripts/url2video.py create --product-url https://shop.example.com/products/linen-sheet-set

# With a spoken voiceover: set ugc and the voiceover language
python3 scripts/url2video.py create --product-url https://shop.example.com/products/linen-sheet-set \
  --ad-type ugc --language English

# The page can't be fetched (login required, unsupported category): pass product data you already have. --ad-type is then required
python3 scripts/url2video.py create --title "Rose Quartz Face Roller Set" \
  --description "Cooling rose quartz roller and gua sha for a morning de-puff routine." \
  --price 24.99 --images https://shop.example.com/images/roller-set.jpg \
  --ad-type ugc --language English
```

Pass **either** `--product-url` **or** product data (`--title` / `--description` / `--price` / `--images` / `--brand`).

| Flag | Notes |
|---|---|
| `--ad-type` | `ugc`: a person filming themselves recommending the product, with voiceover in `--language`. `product_showcase`: studio-style product shots, **music only, no voiceover**. When omitted, the style is picked from the product and may have no voiceover; pass `ugc` if you need one. Required with product data, otherwise the server's pre-check rejects it with `ret=60819` and creates no task or charge |
| `--language` | Voiceover language, e.g. `English`. When omitted it is inferred from the input, falling back to English. Only styles with a voiceover speak it |
| `--aspect-ratio` | `9:16` (default) / `1:1` / `16:9` |
| `--resolution` | `720p` (default) / `1080p` |
| `--idempotency-key` | 1–64 letters, digits, `_` or `-`; a UUID works well. Reuse the same value when retrying |

The duration is fixed at 15 seconds; there is nothing to set.

## Credits

- 720p: about 270 credits
- 1080p: about 675 credits

This step charges credits. **Tell the user the estimated credits and get a go-ahead before submitting.** `estimated_credits` in the response is the estimate for this run.

## Idempotency and Error Codes

Retrying with `--idempotency-key` is safe:

| Situation | Result |
|---|---|
| Same key, same content | Returns the first task as is; no duplicate task, no second charge |
| Same key, different content | `ret=60822` |
| First attempt failed and credits were refunded | `ret=60823`; retry with a new key |
| A request with the same key is still being processed | `ret=429`; retry shortly |
| Product data without `ad_type` | `ret=60819`; no charge |

If the network times out or the script stops waiting, resume with `query --workspace-id <id>`. **Do not resubmit.**

## query — Keep Waiting on an Existing Task

```bash
python3 scripts/url2video.py query --workspace-id ws_xxx
```

---

# 商品链接出广告 / URL to Video

脚本：`scripts/url2video.py`

贴一个商品页链接，出一条 15 秒的短视频广告。默认 9:16、720p。

## create — 出广告（异步）

```bash
# 商品页链接，最省事
python3 scripts/url2video.py create --product-url https://shop.example.com/products/linen-sheet-set

# 要真人口播：指定 ugc，并给口播语言
python3 scripts/url2video.py create --product-url https://shop.example.com/products/linen-sheet-set \
  --ad-type ugc --language English

# 页面抓不到（要登录、品类不支持）：改传已有的商品数据，此时 --ad-type 必填
python3 scripts/url2video.py create --title "Rose Quartz Face Roller Set" \
  --description "Cooling rose quartz roller and gua sha for a morning de-puff routine." \
  --price 24.99 --images https://shop.example.com/images/roller-set.jpg \
  --ad-type ugc --language English
```

`--product-url` 和商品数据（`--title` / `--description` / `--price` / `--images` / `--brand`）**二选一**。

| 参数 | 说明 |
|---|---|
| `--ad-type` | `ugc`：真人自拍口播种草，有口播，语言按 `--language`。`product_showcase`：棚拍产品质感，**只有配乐、没有口播**。不传时按商品自动选型，可能没有口播；要口播就传 `ugc`。传商品数据时必填，否则服务端预检以 `ret=60819` 拒绝，不建任务、不扣积分 |
| `--language` | 口播语言，如 `English`。不传时按输入识别，识别不到用 English。只有带口播的类型才会念出来 |
| `--aspect-ratio` | `9:16`（默认）/ `1:1` / `16:9` |
| `--resolution` | `720p`（默认）/ `1080p` |
| `--idempotency-key` | 1–64 位字母、数字、`_`、`-`，建议用 UUID。重试时带同一个值 |

时长固定 15 秒，不用传。

## 积分

- 720p：预计 270 积分
- 1080p：预计 675 积分

这一步会扣积分。**提交前把预计积分告诉用户，确认后再提交。**返回里的 `estimated_credits` 是本次预计消耗。

## 幂等和错误码

带 `--idempotency-key` 后重试是安全的：

| 情况 | 返回 |
|---|---|
| 同键、同内容 | 原样返回第一次的任务，不重复建单、不重复扣积分 |
| 同键、内容不同 | `ret=60822` |
| 第一次建单失败，积分已退 | `ret=60823`，换一个新键重试 |
| 同键的请求还在处理 | `ret=429`，稍后重试 |
| 传了商品数据但没传 `ad_type` | `ret=60819`，不扣积分 |

网络超时、脚本等不到结果时，用 `query --workspace-id <id>` 接着等，**不要重新提交**。

## query — 接着等已有任务

```bash
python3 scripts/url2video.py query --workspace-id ws_xxx
```
