# 用户资产 & 任务查询

## 结果轮询接口

### 新版（access-token，推荐）

`POST /waic/core/task/queryItemForSaas`

用于查询商拍图/抠图等异步任务的单个 taskItem 结果。

**入参:**

| 参数 | 类型 | 必传 | 说明 |
|------|------|------|------|
| taskItemId | Long | 是 | 单个任务项 ID（从 draw/removeBg 返回的 taskItemIds 中取） |

**出参:**

```json
{
    "errcode": "0",
    "errmsg": "ok",
    "data": {
        "id": 902035,
        "taskId": 634428,
        "url": "https://image-c-dev.weimobwmc.com/qa-5W/xxx.png",
        "itemStatus": 2,
        "userId": 2369671,
        "sceneType": null,
        "bosId": null,
        "transData": null
    },
    "globalTicket": "..."
}
```

| 参数 | 类型 | 说明 |
|------|------|------|
| data.id | Long | taskItemId |
| data.taskId | Long | 父任务 ID |
| data.url | String | 结果图 URL（仅 itemStatus=2 时有值） |
| data.itemStatus | Integer | 状态：0=待处理/失败, 1=执行中, 2=完成, 3=执行中, 4=排队中 |

### 调用示例

```python
import requests
from wime_auth import get_auth

body = {"taskItemId": 902035}
auth = get_auth(uri_path="/waic/core/task/queryItemForSaas", body_dict=body)

resp = requests.post(
    f"{auth['base_url']}/waic/core/task/queryItemForSaas",
    headers=auth["headers"],
    data=auth["body_str"].encode("utf-8")
)
result = resp.json()
# data.itemStatus == 2 且 data.url 有值 → 完成
```

### 轮询策略

- 完成条件：`itemStatus == 2` 且 `url` 非空
- 轮询间隔：5~10 秒
- 默认最长等待：3~10 分钟
- `itemStatus=0` 不代表一定失败，可能是调度延迟，超时前不要判定失败

