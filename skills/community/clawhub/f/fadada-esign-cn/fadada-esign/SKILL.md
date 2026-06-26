---
name: fadada-esign
description: 法大大电子合同与电子签署技能（FASC API 5.0）。使用场景：(1) 发送合同给对方签署（发起签署任务）；(2) 查询签署任务状态；(3) 下载已签署合同；(4) 上传文档并处理为签署格式；(5) 创建和管理签署模板；(6) 印章与签名管理。当用户提到"发合同"、"让对方签合同"、"电子签"、"法大大"、"合同签署"、"查询签署状态"、"下载合同"等场景时触发。
---

# 法大大电子签 Skill（FASC API 5.0）

基于法大大 FASC API 5.0，实现合同创建、发送、签署全流程。

## 核心概念

### 1. 签署任务（Sign Task）
一个"签署任务"就是一个签署协作流程控制器，包括：
- 待签署的文档
- 各参与方（企业或个人）
- 控制协作流程的参数

### 2. 发起方（Initiator）
发起方是签署协作流程的发起者，拥有更多控制权限（内容修改、添加参与方、定稿、撤销等）。

### 3. 参与方（Actor）
参与方类型：
- `corp`：企业
- `person`：个人

参与方权限：
- `fill`：填写
- `sign`：签署
- `cc`：抄送

### 4. 文档（Doc）
支持两种来源：
- 直接上传 PDF/图片 → 通过文件处理接口获取 fileId
- 基于文档模板 → 使用 docTemplateId

## 配置

使用前需要以下凭证：

```
FADADA_APP_ID=your_app_id
FADADA_APP_SECRET=your_app_secret
```

## 完整签署流程

### 标准流程

```
1. 上传文档 → 获取 uploadUrl → PUT 上传文件 → 获取 fddFileUrl
2. 文件处理 → 获取 fileId
3. 创建签署任务 → 获取 signTaskId
4. 添加文档（如未在创建时添加）
5. 添加参与方（如未在创建时添加）
6. 提交签署任务
7. （可选）等待填写 → 定稿
8. 查询签署状态 / 等待回调
9. 下载已签署文档
```

### 快速流程（创建时一次性设置）

```json
// 创建签署任务时直接传入文档、参与方，设置 autoStart=true
{
  "initiator": {"idType": "corp", "openId": "xxx"},
  "signTaskSubject": "劳动合同签署",
  "autoStart": true,
  "autoFinish": true,
  "docs": [...],
  "actors": [...]
}
```

## API 调用规范

### 请求头

每次请求必须包含以下 Header：

```
AppId: your_app_id
MsgId: UUID（防重放）
Timestamp: Unix时间戳（秒）
Sign: MD5(AppId + Timestamp + MsgId + AppSecret).toUpperCase()
Content-Type: application/json
```

### 签名计算

```python
import hashlib, time, uuid

def make_headers(app_id: str, app_secret: str) -> dict:
    msg_id = uuid.uuid4().hex.upper()
    timestamp = str(int(time.time()))
    raw = app_id + timestamp + msg_id + app_secret
    sign = hashlib.md5(raw.encode("utf-8")).hexdigest().upper()
    return {
        "AppId": app_id,
        "MsgId": msg_id,
        "Timestamp": timestamp,
        "Sign": sign,
        "Content-Type": "application/json"
    }
```

## 核心接口

### 1. 文件上传（两步）

**步骤一：获取上传地址**
```
POST /file/get-upload-url
{
  "fileType": "doc"  // doc=签署文档, attach=附件
}
→ 返回 uploadUrl + fddFileUrl
```

**步骤二：PUT 上传文件**
```
PUT {uploadUrl}
Content-Type: application/octet-stream
[文件二进制流]
```

### 2. 文件处理

```
POST /file/process
{
  "fddFileUrlList": [{
    "fileType": "doc",
    "fddFileUrl": "xxx",
    "fileName": "合同.pdf",
    "fileFormat": "pdf"  // pdf 或 ofd（国密）
  }]
}
→ 返回 fileId
```

### 3. 创建签署任务（基于文档）

```
POST /sign-task/create
{
  "initiator": {"idType": "corp", "openId": "xxx"},
  "signTaskSubject": "合同签署",
  "signDocType": "contract",  // contract 或 document
  "autoStart": true,          // 自动提交
  "autoFinish": true,         // 自动结束
  "signInOrder": false,       // 是否有序签署
  "docs": [{
    "docId": "doc1",
    "docName": "劳动合同",
    "docFileId": "xxx"
  }],
  "actors": [{
    "actor": {
      "actorId": "乙方",
      "actorType": "person",
      "actorName": "张三",
      "permissions": ["sign"],
      "notification": {
        "sendNotification": true,
        "notifyWay": "mobile",
        "notifyAddress": "13800138000"
      }
    },
    "signConfigInfo": {
      "orderNo": 1
    }
  }]
}
→ 返回 signTaskId
```

### 4. 创建签署任务（基于模板）

```
POST /sign-task/create-with-template
{
  "initiator": {"idType": "corp", "openId": "xxx"},
  "signTaskSubject": "合同签署",
  "signTemplateId": "xxx",
  "autoStart": true,
  "actors": [...]  // 只需指定具体参与方信息
}
→ 返回 signTaskId
```

### 5. 查询签署任务详情

```
POST /sign-task/get-detail
{"signTaskId": "xxx"}

→ 返回：
- signTaskStatus: draft/submitting/fill_wait/filled/sign_progress/finished/cancelled/expired
- actors[].signStatus: wait_sign/signed/sign_rejected
- actors[].actorSignTaskUrl: 签署链接
```

### 6. 获取签署文档下载地址

```
POST /sign-task/owner/get-download-url
{
  "ownerId": {"idType": "corp", "openId": "xxx"},
  "signTaskId": "xxx",
  "fileType": "doc"  // doc 或 attach
}
→ 返回 downloadUrl（有效期1小时）
```

### 7. 撤销签署任务

```
POST /sign-task/cancel
{
  "signTaskId": "xxx",
  "terminationNote": "撤销原因"
}
```

## 签署任务状态流转

```
draft           → 创建中（未提交）
submitting      → 提交中
fill_wait       → 等待填写
filled          → 填写完成
sign_progress   → 签署进行中
finished        → 已完成
cancelled       → 已撤销
expired         → 已过期
```

## 参与方签署状态

```
wait_sign       → 待签署
signed          → 已签署
sign_rejected   → 已拒签
```

## 关键注意事项

1. **参与方身份识别**：可通过 `actorOpenId`（应用用户ID）或 `actorFDDId`（法大大号）指定
2. **签署顺序**：`signInOrder=true` 时，按 `orderNo` 从小到大依次签署
3. **通知机制**：设置 `notification.sendNotification=true` 由法大大发送短信/邮件通知
4. **文件格式**：支持 PDF（国际加密）和 OFD（国密加密）
5. **回调通知**：签署完成后会向 `notifyUrl` 发送回调，需验证签名

## 免验证签（自动盖章）

适用于企业自动落章场景：

1. 创建印章时设置免验证签
2. 创建签署任务时传入 `businessId`（免验证签场景码）
3. 参与方设置 `requestVerifyFree: true`

## 错误码

| code | 含义 |
|------|------|
| 100000 | 成功 |
| 100001 | 参数错误 |
| 100002 | 未授权 |
| 100003 | 签名验证失败 |
| 200001 | 用户不存在 |
| 300001 | 签署任务不存在 |
| 300002 | 签署任务状态不允许此操作 |

## 常见任务示例

### 发起一份合同签署

```python
import requests

BASE = "https://api.fadada.com"

# 1. 获取上传地址
resp = requests.post(f"{BASE}/file/get-upload-url",
    headers=make_headers(APP_ID, APP_SECRET),
    json={"fileType": "doc"}
)
upload_url = resp.json()["data"]["uploadUrl"]
fdd_file_url = resp.json()["data"]["fddFileUrl"]

# 2. 上传文件
with open("contract.pdf", "rb") as f:
    requests.put(upload_url, data=f.read())

# 3. 处理文件
resp = requests.post(f"{BASE}/file/process",
    headers=make_headers(APP_ID, APP_SECRET),
    json={"fddFileUrlList": [{
        "fileType": "doc",
        "fddFileUrl": fdd_file_url,
        "fileName": "contract.pdf",
        "fileFormat": "pdf"
    }]}
)
file_id = resp.json()["data"]["fileIdList"][0]["fileId"]

# 4. 创建签署任务
resp = requests.post(f"{BASE}/sign-task/create",
    headers=make_headers(APP_ID, APP_SECRET),
    json={
        "initiator": {"idType": "corp", "openId": "your_open_corp_id"},
        "signTaskSubject": "服务合同",
        "autoStart": True,
        "autoFinish": True,
        "docs": [{
            "docId": "doc1",
            "docName": "服务合同",
            "docFileId": file_id
        }],
        "actors": [{
            "actor": {
                "actorId": "乙方",
                "actorType": "person",
                "actorName": "张三",
                "permissions": ["sign"],
                "identNameForMatch": "张三",
                "certNoForMatch": "身份证号",
                "notification": {
                    "sendNotification": True,
                    "notifyWay": "mobile",
                    "notifyAddress": "13800138000"
                }
            }
        }]
    }
)
sign_task_id = resp.json()["data"]["signTaskId"]
```

### 查询签署状态

```python
resp = requests.post(f"{BASE}/sign-task/get-detail",
    headers=make_headers(APP_ID, APP_SECRET),
    json={"signTaskId": sign_task_id}
)
status = resp.json()["data"]["signTaskStatus"]
sign_url = resp.json()["data"]["actors"][0]["actorSignTaskUrl"]
```

### 下载已签署合同

```python
resp = requests.post(f"{BASE}/sign-task/owner/get-download-url",
    headers=make_headers(APP_ID, APP_SECRET),
    json={
        "ownerId": {"idType": "corp", "openId": "your_open_corp_id"},
        "signTaskId": sign_task_id,
        "fileType": "doc"
    }
)
download_url = resp.json()["data"]["downloadUrl"]
```

## 详细 API 参考

完整的接口参数和响应格式请参阅 [references/api_reference.md](references/api_reference.md)。
