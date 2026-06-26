---
name: wime-creator
description: WIME AI 电商创作平台 OpenAPI。提供两个核心能力：1）抠图 — 上传本地图片（或 URL）自动抠图，返回透明背景图 URL；2）商拍图 — 自动抠图后生成多张 AI 商拍图。触发场景：用户提到抠图、商拍图、商品图、WIME、电商图片处理时激活。
---

# WIME OpenAPI

电商 AI 创作平台，提供两个核心 Skill。

## 认证

该 skill 仅支持 `WIME_ACCESS_TOKEN`。

> 安全与权限说明：该 skill 需要 WIME 专用凭证，并且会把用户明确提供的本地图片上传到 WIME 服务；当输入是远程图片 URL，或 WIME 返回远程抠图结果 URL 时，可能会拉取对应图片做处理。为降低风险，远程下载应仅用于用户提供或 WIME 返回的公开图片地址，不应用于 localhost、内网或其他非公开地址。

统一使用 `scripts/wime_auth.py` 的 `get_auth()` 函数：

```python
from wime_auth import get_auth

auth = get_auth(uri_path="/waic/core/creationDesk/draw", body_dict=body)

resp = requests.post(
    f"{auth['base_url']}/waic/core/creationDesk/draw",
    headers=auth["headers"],
    data=auth["body_str"].encode("utf-8")
)
```

`get_auth()` 返回：
- `base_url`: API 根地址
- `headers`: 完整请求 headers dict（含 `access-token`）
- `body_str`: JSON 序列化后的 body 字符串（用于 `data=` 发送），body_dict 为 None 时为 None

### 配置方式

```bash
export WIME_ACCESS_TOKEN='你的token'

# 可选，默认 https://wime-ai.com
export WIME_BASE_URL='https://wime-ai.com'
```

若未配置 `WIME_ACCESS_TOKEN`，调用前应直接报错并提示用户先完成配置。

### 获取凭证

访问 [wime-ai.com](https://wime-ai.com/)，页面右下角有 **API 对接**的联系方式，通过该入口申请获取 `access-token`。

如果当前环境未配置凭证，应直接告知用户先去官网联系获取，而不是盲目调用接口。

## 图片来源判断（通用前置步骤）

用户输入可能是 **本地路径** 或 **URL**，统一处理为可访问的图片 URL：

```
判断用户输入:
  ├─ 本地路径 (如 /Users/.../image.jpg)
  │    → upload → imageUrl
  │
  └─ URL (以 http:// 或 https:// 开头)
       → 直接使用该 URL 作为 imageUrl
       → （若后续接口不接受外部 URL，则下载 → upload → imageUrl）
```

### 新版上传接口

`POST /waic/core/file/py/upload`（multipart/form-data）

直接返回 `data.url`（可访问的图片 URL），**不再返回 mediaId**。

```python
from wime_auth import get_auth

auth = get_auth()

with open("image.png", "rb") as f:
    resp = requests.post(
        f"{auth['base_url']}/waic/core/file/py/upload",
        headers={"access-token": auth["headers"]["access-token"]},
        files={"file": ("image.png", f, "image/png")}
    )
image_url = resp.json()["data"]["url"]
```

**注意：** 上传接口需要 `access-token` header。

### URL 下载注意事项（仅本地路径场景需上传）

- 如果用户直接给了 URL，**优先直接用**，不需要下载再上传
- 只有本地文件才需要走上传流程
- 上传完成后清理本地临时文件
- 若必须下载远程图片进行处理，只允许公开 `http/https` 地址；拒绝 `localhost`、`.local`、回环地址和内网 IP

## Skill 1：抠图

**触发词：** 抠图、去背景、透明背景、matting

### 新版流程（access-token）

```
用户提供本地图片路径或 URL
  → [图片来源判断] → imageUrl
  → removeBg([{imageUrl}]) → taskItemIds
  → queryItemForSaas(taskItemId) 轮询 → 抠图结果 URL
```

**接口：** `POST /waic/core/creationDesk/removeBg`

**⚠️ 新版抠图为异步接口**，返回 `taskItemIds`，需轮询获取结果。

**步骤：**
1. 获取图片 URL：本地路径 → 上传获取 url；URL → 直接使用
2. 构建请求体：
   ```python
   import json
   body = {
       "data": json.dumps([{"imageUrl": image_url}]),
       "skill": True
   }
   ```
   注意 `data` 字段是 **JSON 字符串**（不是 object），内部为 imageUrl 数组。
3. 调用 `removeBg`，获取 `taskItemIds`
4. 用 `taskItemIds[0]` 轮询 `queryItemForSaas`，`itemStatus == 2` 且 `url` 有值时完成

**输出给用户：** 抠图结果 URL

## Skill 2：商拍图

**触发词：** 商拍图、商品图、AI 商拍、产品摄影

### 新版流程（access-token）

```
用户提供本地图片路径或 URL
  → [图片来源判断] → imageUrl（原图 URL，记为 sourceImageUrl）
  → removeBg → taskItemIds → 轮询 → cutoutUrl
  → crop_alpha_bbox(cutoutUrl) → 本地裁剪图 (cropped.png)
  → upload(cropped.png) → croppedUrl
  → removeBg(croppedUrl) → 轮询 → croppedCutoutUrl（紧凑抠图）
  → draw(picList 使用 croppedCutoutUrl) → taskItemIds
  → queryItemForSaas 轮询 → 出一张返回一张
```

**步骤：**
1. **获取原图 URL**：
   - URL 输入 → 直接用作 `sourceImageUrl`
   - 本地路径 → 上传获取 url，作为 `sourceImageUrl`
2. **首次抠图**：调用 `removeBg` 传入原图 URL → 轮询获取 `cutoutUrl`
3. **裁剪非透明区域**：使用 `scripts/crop_alpha.py` 的 `crop_alpha_bbox(cutoutUrl)` 裁剪最小外接矩形，去除多余透明边距
4. **上传裁剪图**：将裁剪后 PNG 通过 `/waic/core/file/py/upload` 上传 → 获取 `croppedUrl` 及裁剪后宽高
5. **二次抠图**：调用 `removeBg` 传入 `croppedUrl` → 轮询获取 `croppedCutoutUrl`
6. **构建 `draw` 请求**：

**接口：** `POST /waic/core/creationDesk/draw`

```python
body = {
    "ips": False,
    "needRank": True,
    "num": 4,
    "type": 1002,
    "data": {
        "aiStyle": True,
        "bgColor": "",
        "height": 1024,
        "width": 1024,
        "industry": "其他",
        "negPrompt": "",
        "prompt": "",
        "promptAi": "",
        "randomStyle": True,
        "referenceUrl": "",
        "seed": 0,
        "styleCode": "A0072",
        "skill": True,
        "picList": [
            {
                "imageUrl": cropped_cutout_url,
                "sourceImageUrl": source_image_url,
                "imageCaption": "",
                "width": crop_w,
                "height": crop_h,
                "left": calculated_left,
                "top": calculated_top,
                "scaleX": calculated_scale,
                "scaleY": calculated_scale,
                "type": 1,
                "parentId": ""
            }
        ]
    }
}
```

**注意新版 body 结构：** 外层有 `ips`/`needRank`/`type`，画布参数在 `data` 内，`data.skill` 必须为 `True`。

7. 提交后获得 `taskItemIds`
8. 轮询 `queryItemForSaas`（每个 taskItemId 单独查），**每完成一张立即输出**
9. **清理**：删除本地临时裁剪文件

### picList 位置与缩放规则

根据**商品图裁剪后的宽高比**判断横竖版，分别计算缩放和位置：

```python
canvas_w, canvas_h = 1024, 1024  # 画布尺寸
img_w, img_h = crop_w, crop_h  # 裁剪后的商品尺寸

if img_w >= img_h:
    # 横版/方图商品：商品宽度 = 画布宽度 × 60%
    scale = (canvas_w * 0.6) / img_w
else:
    # 竖版商品：商品高度 = 画布高度 × 80%
    scale = (canvas_h * 0.8) / img_h

# 安全 clamp：缩放后商品不能超出画布任意一边
scale = min(scale, canvas_w / img_w, canvas_h / img_h)

# 水平方向：居中
left = (canvas_w - img_w * scale) / 2

# 垂直方向：总空白区域中，上方占 65%，下方占 35%
total_v_blank = canvas_h - img_h * scale
top = total_v_blank * 0.65
```

### 裁剪脚本用法

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from crop_alpha import crop_alpha_bbox

cropped_path, (crop_w, crop_h) = crop_alpha_bbox(cutout_url, "/tmp/wime_cropped.png")
```

### 结果轮询

**接口：** `POST /waic/core/task/queryItemForSaas`

```python
body = {"taskItemId": task_item_id}  # 单个 taskItemId（Long）
auth = get_auth(uri_path="/waic/core/task/queryItemForSaas", body_dict=body)
resp = requests.post(
    f"{auth['base_url']}/waic/core/task/queryItemForSaas",
    headers=auth["headers"],
    data=auth["body_str"].encode("utf-8")
)
# data.itemStatus == 2 且 data.url 有值 → 完成
```

### 轮询状态码（实测）

| itemStatus | 含义 |
|------------|------|
| 0 | **需区分：调度延迟 vs 真正失败**（见下方判定逻辑） |
| 1 | 执行中（未出图） |
| 2 | **完成**（`url` 字段有值） |
| 3 | 执行中 |
| 4 | 排队中 |

**判断完成的条件：** `itemStatus == 2` 且 `url` 非空。

**⚠️ itemStatus=0 的判定逻辑：**

实测发现：任务在较长一段时间内**持续返回 `status=0` 仍可能最终成功**。**不要因为连续几次 `0` 就判定失败**。

**推荐轮询策略：**
- 完成条件：`itemStatus == 2` 且 `url` 非空
- 轮询间隔：`5~10` 秒
- 默认最长等待：`3~10` 分钟
- 在超时前，**不要仅因 `status=0` 就判失败**
- 超时后仍无结果，标记为 "超时/未完成"

**输出给用户：** 每张图完成时立即返回结果 URL

---

## API 路径对照

| 功能 | 路径 |
|------|------|
| 图片上传 | `POST /waic/core/file/py/upload` |
| 抠图 | `POST /waic/core/creationDesk/removeBg` |
| 商拍图 | `POST /waic/core/creationDesk/draw` |
| 结果轮询 | `POST /waic/core/task/queryItemForSaas` |

## 环境

| 环境 | Base URL | 说明 |
|------|----------|------|
| 生产 | `https://wime-ai.com` | 线上环境 |

默认使用生产环境。`WIME_BASE_URL` 可覆盖。

## 接口参考

| 文件 | 说明 |
|------|------|
| `references/upload-image.md` | 图片上传 |
| `references/cutout.md` | 抠图 |
| `references/photo-shoot.md` | 商拍图 |
| `references/asset-query.md` | 结果轮询 + 资产查询 |
| `references/error-codes.md` | 全局错误码 |

## 注意事项

- 新版上传图片直接得到 URL，不再有 mediaId 概念
- 抠图为**异步**接口，需轮询获取结果
- 商拍图始终为**异步**接口，轮询时出一张返回一张
- body 中含 `skill: true` 的接口必须传此字段
- QPS 限制，超限返回 errcode=1000007
- 该 skill 依赖 `WIME_ACCESS_TOKEN`；发布到注册表时应显式声明该环境变量与主凭证需求
