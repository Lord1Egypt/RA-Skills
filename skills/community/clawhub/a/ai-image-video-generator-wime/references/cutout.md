# 抠图接口

## 新版（access-token，推荐）

`POST /waic/core/creationDesk/removeBg`

**同步接口**，直接返回抠图结果。传入 imageUrl 列表，无需 mediaId。

**入参:**

| 参数 | 类型 | 必传 | 说明 |
|------|------|------|------|
| data | String (JSON array) | 是 | imageUrl 的 JSON 数组字符串，如 `"[{\"imageUrl\":\"https://...\"}]"` |
| skill | Boolean | 是 | 固定传 `true` |

**出参:**

```json
{
    "errcode": "0",
    "errmsg": "ok",
    "data": {
        "creationId": 238564,
        "taskId": 634428,
        "taskItemIds": [902035],
        "ranks": null
    },
    "globalTicket": "..."
}
```

**注意：** 新版抠图为**异步接口**，返回 `taskItemIds`，需要用结果轮询接口查询结果。

### 调用示例

```python
import requests, json
from wime_auth import get_auth

body = {
    "data": json.dumps([{"imageUrl": "https://example.com/image.webp"}]),
    "skill": True
}

auth = get_auth(uri_path="/waic/core/creationDesk/removeBg", body_dict=body)

resp = requests.post(
    f"{auth['base_url']}/waic/core/creationDesk/removeBg",
    headers=auth["headers"],
    data=auth["body_str"].encode("utf-8")
)
result = resp.json()
# 用 taskItemIds 去轮询 queryItemForSaas 获取抠图结果
```

