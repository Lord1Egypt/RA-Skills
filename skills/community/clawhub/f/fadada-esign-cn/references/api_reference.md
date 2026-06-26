# 法大大 FASC API 5.0 接口参考

> 基础域名：`https://api.fadada.com`（正式环境）/ `https://testapi.fadada.com`（沙箱环境）

---

## 目录

1. [公共说明](#1-公共说明)
2. [文件处理](#2-文件处理)
3. [模板管理](#3-模板管理)
4. [签署任务](#4-签署任务)
5. [签署任务控制](#5-签署任务控制)
6. [印章管理](#6-印章管理)
7. [企业成员管理](#7-企业成员管理)
8. [计费管理](#8-计费管理)
9. [审批管理](#9-审批管理)

---

## 1. 公共说明

### 1.1 请求头

| Header | 说明 |
|--------|------|
| `AppId` | 开发者平台申请的 App ID |
| `MsgId` | 请求唯一标识（UUID，防重放） |
| `Timestamp` | Unix 时间戳（秒），有效期 ±5 分钟 |
| `Sign` | 签名字符串：MD5(AppId + Timestamp + MsgId + AppSecret).toUpperCase() |
| `Content-Type` | application/json |

### 1.2 签名算法

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

### 1.3 OpenId 结构

```json
{
  "idType": "corp" | "person",
  "openId": "xxx"
}
```

### 1.4 错误码

| code | 含义 |
|------|------|
| 100000 | 成功 |
| 100001 | 参数错误 |
| 100002 | 未授权 |
| 100003 | 签名验证失败 |
| 200001 | 用户不存在 |
| 300001 | 签署任务不存在 |
| 300002 | 签署任务状态不允许此操作 |

---

## 2. 文件处理

### 2.1 获取文件上传地址

**POST** `/file/get-upload-url`

```json
{
  "fileType": "doc"  // doc=签署文档, attach=附件
}
```

**响应**：
```json
{
  "code": "100000",
  "data": {
    "uploadUrl": "https://file-xxx.fadada.com/...?sign=...",
    "fddFileUrl": "https://file-xxx.fadada.com/xxx"
  }
}
```

### 2.2 上传本地文件

使用步骤一返回的 `uploadUrl`，通过 PUT 请求上传文件二进制内容。

### 2.3 文件处理

**POST** `/file/process`

```json
{
  "fddFileUrlList": [{
    "fileType": "doc",
    "fddFileUrl": "https://file-xxx.fadada.com/xxx",
    "fileName": "合同.pdf",
    "fileFormat": "pdf"  // pdf 或 ofd
  }]
}
```

**响应**：
```json
{
  "code": "100000",
  "data": {
    "fileIdList": [{
      "fileId": "xxx",
      "fileType": "doc",
      "fddFileUrl": "xxx",
      "fileName": "合同.pdf",
      "fileTotalPages": 10
    }]
  }
}
```

### 2.4 查询文档关键字坐标

**POST** `/file/get-keyword-positions`

```json
{
  "fileId": "xxx",
  "keywords": ["甲方", "乙方", "签署日期"]
}
```

**响应**：
```json
{
  "code": "100000",
  "data": [{
    "keyword": "甲方",
    "positions": [{
      "positionPageNo": 1,
      "coordinates": [{
        "positionX": "157.699",
        "positionY": "152.887"
      }]
    }]
  }]
}
```

---

## 3. 模板管理

### 3.1 查询文档模板列表

**POST** `/doc-template/get-list`

```json
{
  "ownerId": {"idType": "corp", "openId": "xxx"},
  "listFilter": {"docTemplateName": "模板名"},
  "listPageNo": 1,
  "listPageSize": 10
}
```

### 3.2 查询文档模板详情

**POST** `/doc-template/get-detail`

```json
{
  "ownerId": {"idType": "corp", "openId": "xxx"},
  "docTemplateId": "xxx"
}
```

返回模板中的控件列表（填写控件、签章控件）。

### 3.3 填写文档模板生成文件

**POST** `/doc-template/fill-values`

```json
{
  "openCorpId": "xxx",
  "docTemplateId": "xxx",
  "fileName": "填充后的合同",
  "docFieldValues": [
    {"fieldId": "xxx", "fieldValue": "填充内容"}
  ]
}
```

**响应**：
```json
{
  "code": "100000",
  "data": {
    "fileId": "xxx",
    "fileDownloadUrl": "xxx"
  }
}
```

### 3.4 获取模板管理链接

**POST** `/template/manage/get-url`

```json
{
  "openCorpId": "xxx",
  "redirectUrl": "https://your-domain.com/callback"
}
```

---

## 4. 签署任务

### 4.1 创建签署任务（基于文档）

**POST** `/sign-task/create`

关键参数：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| initiator | OpenId | 是 | 发起方 |
| signTaskSubject | string | 是 | 任务主题 |
| signDocType | string | 否 | contract/document |
| expiresTime | long | 否 | 过期时间（毫秒时间戳） |
| autoStart | boolean | 否 | 自动提交，默认false |
| autoFinish | boolean | 否 | 自动结束，默认true |
| autoFillFinalize | boolean | 否 | 自动定稿，默认true |
| signInOrder | boolean | 否 | 是否有序签 |
| fileFormat | string | 否 | pdf/ofd |
| docs | array | 否 | 文档列表 |
| actors | array | 否 | 参与方列表 |

**docs 文档参数**：

```json
{
  "docId": "doc1",
  "docName": "劳动合同",
  "docFileId": "xxx",        // 或
  "docTemplateId": "xxx",    // 二选一
  "docFields": [...]         // 可选，控件列表
}
```

**actors 参与方参数**：

```json
{
  "actor": {
    "actorId": "乙方",
    "actorType": "person",    // corp/person
    "actorName": "张三",
    "permissions": ["sign"],  // fill/sign/cc
    "actorOpenId": "xxx",    // 应用用户ID
    "actorFDDId": "xxx",     // 法大大号
    "identNameForMatch": "张三",
    "certNoForMatch": "身份证号",
    "accountName": "手机号或邮箱",
    "notification": {
      "sendNotification": true,
      "notifyWay": "mobile",   // mobile/email
      "notifyAddress": "13800138000"
    }
  },
  "fillFields": [...],        // 填写控件
  "signFields": [...],       // 签章控件
  "signConfigInfo": {
    "orderNo": 1,
    "verifyMethods": ["sms", "face"],  // 意愿验证方式
    "signerSignMethod": "standard",    // 签名方式
    "requestMemberSign": false,
    "joinByLink": true,
    "readingToEnd": false,
    "freeLogin": false
  }
}
```

**响应**：
```json
{
  "code": "100000",
  "data": {
    "signTaskId": "1677137745347153488"
  }
}
```

### 4.2 创建签署任务（基于模板）

**POST** `/sign-task/create-with-template`

```json
{
  "initiator": {"idType": "corp", "openId": "xxx"},
  "signTaskSubject": "合同签署",
  "signTemplateId": "xxx",
  "autoStart": true,
  "actors": [...]  // 只需指定参与方信息
}
```

### 4.3 查询签署任务详情

**POST** `/sign-task/get-detail`

```json
{
  "signTaskId": "xxx"
}
```

**响应关键字段**：

| 字段 | 说明 |
|------|------|
| signTaskStatus | 任务状态 |
| actors[].signStatus | 参与方签署状态 |
| actors[].actorSignTaskUrl | 参与方签署链接 |
| actors[].joinStatus | 加入状态 |
| actors[].fillStatus | 填写状态 |

**任务状态**：
- `draft` - 创建中
- `submitting` - 提交中
- `fill_wait` - 等待填写
- `filled` - 填写完成
- `sign_progress` - 签署进行中
- `finished` - 已完成
- `cancelled` - 已撤销
- `expired` - 已过期

**参与方签署状态**：
- `wait_sign` - 待签署
- `signed` - 已签署
- `sign_rejected` - 已拒签

### 4.4 提交签署任务

**POST** `/sign-task/start`

```json
{
  "signTaskId": "xxx"
}
```

### 4.5 定稿签署任务

**POST** `/sign-task/doc-finalize`

```json
{
  "signTaskId": "xxx"
}
```

### 4.6 添加签署任务文档

**POST** `/sign-task/doc/add`

```json
{
  "signTaskId": "xxx",
  "docs": [...]
}
```

### 4.7 填写控件内容

**POST** `/sign-task/field/fill-values`

```json
{
  "signTaskId": "xxx",
  "docFieldValues": [
    {"docId": "doc1", "fieldId": "xxx", "fieldValue": "内容"}
  ]
}
```

### 4.8 查询参与方填写内容

**POST** `/sign-task/field/list`

```json
{
  "signTaskId": "xxx"
}
```

### 4.9 获取签署文档下载地址

**POST** `/sign-task/owner/get-download-url`

```json
{
  "ownerId": {"idType": "corp", "openId": "xxx"},
  "signTaskId": "xxx",
  "fileType": "doc",    // doc/attach
  "id": "docId",       // 可选，指定文档
  "customName": "文件名"
}
```

**响应**：
```json
{
  "code": "100000",
  "data": {
    "downloadUrl": "https://..."
  }
}
```

### 4.10 获取签署过程保全报告

**POST** `/sign-task/evidence-report/get-download-url`

```json
{
  "signTaskId": "xxx"
}
```

---

## 5. 签署任务控制

### 5.1 撤销签署任务

**POST** `/sign-task/cancel`

```json
{
  "signTaskId": "xxx",
  "terminationNote": "撤销原因"
}
```

### 5.2 催办签署任务

**POST** `/sign-task/urge`

```json
{
  "signTaskId": "xxx"
}
```

### 5.3 阻塞签署任务

**POST** `/sign-task/block`

```json
{
  "signTaskId": "xxx",
  "actorId": "参与方ID"
}
```

### 5.4 解阻签署任务

**POST** `/sign-task/unblock`

```json
{
  "signTaskId": "xxx",
  "actorId": "参与方ID"
}
```

### 5.5 结束签署任务

**POST** `/sign-task/finish`

```json
{
  "signTaskId": "xxx"
}
```

### 5.6 作废签署任务

**POST** `/sign-task/abolish`

```json
{
  "signTaskId": "已完成的任务ID",
  "abolishedInitiator": {
    "initiatorId": "xxx"  // 或
    // "actorId": "xxx"
  },
  "reason": "作废原因"
}
```

### 5.7 删除签署任务

**POST** `/sign-task/delete`

```json
{
  "signTaskId": "xxx"
}
```

### 5.8 延期签署任务

**POST** `/sign-task/extension`

```json
{
  "signTaskId": "xxx",
  "extensionTime": "1699999999999"  // 毫秒时间戳
}
```

---

## 6. 印章管理

### 6.1 创建模板印章

**POST** `/seal/create-by-template`

```json
{
  "openCorpId": "xxx",
  "sealName": "公司公章",
  "categoryType": "official_seal",  // official_seal/contract_seal/hr_seal/financial_seal/other
  "sealTag": "标签",
  "sealTemplateStyle": "round",
  "sealSize": "round_40_40",
  "sealColor": "red"
}
```

### 6.2 创建图片印章

**POST** `/seal/create-by-image`

```json
{
  "openCorpId": "xxx",
  "sealName": "图片印章",
  "sealImage": "base64编码的图片",
  "sealWidth": 40,
  "sealHeight": 40
}
```

### 6.3 查询印章列表

**POST** `/seal/get-list`

```json
{
  "openCorpId": "xxx",
  "listFilter": {
    "categoryType": ["official_seal"]
  }
}
```

**响应**：
```json
{
  "code": "100000",
  "data": {
    "sealInfos": [{
      "sealId": 123456,
      "sealName": "公章",
      "categoryType": "official_seal",
      "picFileUrl": "https://...",
      "sealStatus": "enable",
      "certCAOrg": "CFCA"
    }]
  }
}
```

### 6.4 获取印章管理链接

**POST** `/seal/manage/get-url`

```json
{
  "openCorpId": "xxx",
  "redirectUrl": "https://..."
}
```

---

## 7. 企业成员管理

### 7.1 查询企业成员列表

**POST** `/corp/member/get-list`

```json
{
  "openCorpId": "xxx"
}
```

### 7.2 添加企业成员

**POST** `/corp/member/create`

```json
{
  "openCorpId": "xxx",
  "employeeInfos": [{
    "memberName": "张三",
    "memberMobile": "13800138000",
    "memberEmail": "zhangsan@example.com"
  }]
}
```

---

## 8. 计费管理

### 8.1 获取计费链接

**POST** `/billing/get-bill-url`

```json
{
  "openId": {"idType": "person", "openId": "xxx"},
  "urlType": "account",  // account=费用页, order=订购页
  "redirectUrl": "https://..."
}
```

---

## 9. 审批管理

### 9.1 查询审批流程列表

**POST** `/approval-flow/get-list`

```json
{
  "openCorpId": "xxx",
  "approvalType": "sign_task_start"  // template/sign_task_start/sign_task_finalize/sign_task_seal/sign_task_abolish
}
```

---

## 回调通知

签署任务状态变更时，法大大会向配置的回调地址发送 POST 请求。

### 回调签名验证

使用相同签名算法验证 Header 中的 Sign。

### 回调事件类型

- `sign_task_created` - 任务创建
- `sign_task_started` - 任务提交
- `sign_task_filled` - 填写完成
- `sign_task_signed` - 签署完成
- `sign_task_finished` - 任务完成
- `sign_task_cancelled` - 任务撤销
- `sign_task_expired` - 任务过期
