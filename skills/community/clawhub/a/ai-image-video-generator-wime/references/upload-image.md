# 图片上传接口

## 新版（access-token，推荐）

`POST /waic/core/file/py/upload`

Content-Type: multipart/form-data

直接上传图片文件，返回可访问的图片 URL。**不再返回 mediaId**。

**入参:**

| 参数 | 类型 | 必传 | 说明 |
|------|------|------|------|
| file | MultipartFile | 是 | 文件流数据 |

**出参:**

```json
{
    "errcode": "0",
    "errmsg": "ok",
    "data": {
        "url": "https://image-c-dev.weimobwmc.com/qa-5W/xxx.png"
    },
    "globalTicket": "..."
}
```

| 参数 | 类型 | 说明 |
|------|------|------|
| data.url | String | 图片可访问 URL（可直接用于抠图/商拍图的 imageUrl 参数） |

### 调用示例

```python
import requests
from wime_auth import get_auth

auth = get_auth()

with open("image.png", "rb") as f:
    resp = requests.post(
        f"{auth['base_url']}/waic/core/file/py/upload",
        headers={"access-token": auth["headers"]["access-token"]},
        files={"file": ("image.png", f, "image/png")}
    )
print(resp.json())
# {"errcode": "0", "errmsg": "ok", "data": {"url": "https://..."}}
```

