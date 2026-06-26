# 商拍图接口

## 新版（access-token，推荐）

`POST /waic/core/creationDesk/draw`

### 入参

外层结构：

| 参数 | 类型 | 必传 | 说明 |
|------|------|------|------|
| ips | Boolean | 否 | 默认 false |
| needRank | Boolean | 否 | 是否需要排序，默认 true |
| num | Integer | 是 | 生成数量，如 4 |
| type | Integer | 是 | 创作类型，固定传 `1002` |
| data | Object | 是 | 创作参数，见下方子参数 |

### data 子参数

| 参数 | 类型 | 必传 | 说明 |
|------|------|------|------|
| aiStyle | Boolean | 否 | 是否使用 AI 风格，建议 true |
| bgColor | String | 否 | 背景颜色，空字符串表示无指定 |
| height | Integer | 是 | 画布高度（像素），如 1024 |
| width | Integer | 是 | 画布宽度（像素），如 1024 |
| industry | String | 否 | 行业分类，如 "其他" |
| negPrompt | String | 否 | 负向提示词 |
| prompt | String | 否 | 正向提示词 |
| promptAi | String | 否 | AI 提示词，空字符串由模型自动生成 |
| randomStyle | Boolean | 否 | 是否随机风格，默认 true |
| referenceUrl | String | 否 | 风格参考图 URL |
| seed | Integer | 否 | 随机种子，0 表示随机 |
| styleCode | String | 否 | 风格代码，如 "A0072" |
| skill | Boolean | **是** | **固定传 `true`** |
| picList | Array\<Object\> | 是 | 图片列表 |

### picList 子参数

| 参数 | 类型 | 必传 | 说明 |
|------|------|------|------|
| imageUrl | String | 是 | 展示图 URL（抠图后的） |
| sourceImageUrl | String | 是 | 原始图 URL |
| imageCaption | String | 否 | 图片描述 |
| width | Integer | 是 | 图片宽度（像素） |
| height | Integer | 是 | 图片高度（像素） |
| left | Float | 是 | X 轴偏移量（px） |
| top | Float | 是 | Y 轴偏移量（px） |
| scaleX | Float | 是 | X 轴缩放比例 |
| scaleY | Float | 是 | Y 轴缩放比例 |
| type | Integer | 是 | 图片类型，1=产品图 |
| parentId | String | 否 | 父元素 ID，空字符串表示无父级 |

### 出参

```json
{
    "errcode": "0",
    "errmsg": "ok",
    "data": {
        "creationId": 238562,
        "taskId": 634422,
        "taskItemIds": [902024, 902025, 902026, 902027],
        "ranks": [0, 0, 0, 0]
    },
    "globalTicket": "..."
}
```

### 调用示例

```python
import requests, json
from wime_auth import get_auth

body = {
    "ips": False,
    "needRank": True,
    "num": 4,
    "type": 1002,
    "data": {
        "aiStyle": True,
        "bgColor": "",
        "height": 1024,
        "industry": "其他",
        "negPrompt": "",
        "picList": [
            {
                "height": 396,
                "imageCaption": "A blue and gold microfiber mop",
                "imageUrl": "https://image-c.weimobwmc.com/...",
                "left": 356.07,
                "parentId": "",
                "scaleX": 1.55,
                "scaleY": 1.55,
                "sourceImageUrl": "https://image-c.weimobwmc.com/...",
                "top": 266,
                "type": 1,
                "width": 201
            }
        ],
        "prompt": "",
        "promptAi": "",
        "randomStyle": True,
        "referenceUrl": "",
        "seed": 0,
        "styleCode": "A0072",
        "width": 1024,
        "skill": True
    }
}

auth = get_auth(uri_path="/waic/core/creationDesk/draw", body_dict=body)

resp = requests.post(
    f"{auth['base_url']}/waic/core/creationDesk/draw",
    headers=auth["headers"],
    data=auth["body_str"].encode("utf-8")
)
print(resp.json())
# 用返回的 taskItemIds 轮询 queryItemForSaas
```

