# 法大大数据模型参考

## 枚举类型

### SignType (签署类型)

| 值 | 说明 |
|----|------|
| POSITION | 坐标位置签署 |
| KEYWORD | 关键字签署 |
| TEMPLATE | 模板预设位置签署 |

### SignerType (签署人类型)

| 值 | 说明 |
|----|------|
| PERSONAL | 个人签署 |
| CORP | 企业签署 |

### TaskStatus (任务状态)

| 值 | 说明 |
|----|------|
| DRAFT | 草稿 |
| SIGNING | 签署中 |
| COMPLETED | 已完成 |
| REJECTED | 已拒绝 |
| CANCELLED | 已撤销 |
| EXPIRED | 已过期 |

### AuthStatus (认证状态)

| 值 | 说明 |
|----|------|
| UNAUTHORIZED | 未认证 |
| AUTHORIZING | 认证中 |
| AUTHORIZED | 已认证 |
| FAILED | 认证失败 |

### UserAuthScope (个人授权范围)

| 值 | 说明 |
|----|------|
| IDENT_INFO | 身份信息 |
| SIGN_TASK_INIT | 发起签署任务 |
| SEAL_MANAGE | 印章管理 |

### CorpAuthScope (企业授权范围)

| 值 | 说明 |
|----|------|
| IDENT_INFO | 企业身份信息 |
| SIGN_TASK_INIT | 发起签署任务 |
| SEAL_MANAGE | 印章管理 |
| ORG_MANAGE | 组织管理 |

### IdentType (证件类型)

| 值 | 说明 |
|----|------|
| ID_CARD | 中国大陆居民身份证 |
| PASSPORT | 护照 |
| HK_MACAO_CARD | 港澳居民来往内地通行证 |
| TAIWAN_CARD | 台湾居民来往大陆通行证 |
| OTHER | 其他 |

### SealType (印章类型)

| 值 | 说明 |
|----|------|
| PERSONAL | 个人印章 |
| CORP | 企业印章 |
| OFFICIAL | 公章 |
| CONTRACT | 合同专用章 |
| FINANCE | 财务专用章 |
| INVOICE | 发票专用章 |
| LEGAL_PERSON | 法人章 |

---

## 数据对象

### AccessTokenRes (访问凭证响应)

```python
class AccessTokenRes:
    access_token: str      # 访问凭证
    expires_in: int        # 有效期（秒）
    token_type: str        # Token 类型，固定值 "Bearer"
```

### UserInfo (用户信息)

```python
class UserInfo:
    client_user_id: str    # 用户标识
    user_name: str         # 用户姓名
    ident_type: str        # 证件类型
    ident_no: str          # 证件号（脱敏）
    mobile: str            # 手机号（脱敏）
    auth_status: str       # 认证状态
    create_time: str       # 创建时间
    auth_time: str         # 认证时间
```

### CorpInfo (企业信息)

```python
class CorpInfo:
    client_corp_id: str        # 企业标识
    corp_name: str             # 企业名称
    corp_ident_type: str       # 企业证件类型
    corp_ident_no: str         # 统一社会信用代码（脱敏）
    auth_status: str           # 认证状态
    legal_person_name: str     # 法人姓名（脱敏）
    legal_person_ident_no: str # 法人证件号（脱敏）
    create_time: str           # 创建时间
    auth_time: str             # 认证时间
```

### OrgMember (企业成员)

```python
class OrgMember:
    client_user_id: str    # 用户标识
    user_name: str         # 用户姓名
    mobile: str            # 手机号（脱敏）
    role: str              # 角色
    join_time: str         # 加入时间
```

### SealInfo (印章信息)

```python
class SealInfo:
    seal_id: str           # 印章ID
    seal_name: str         # 印章名称
    seal_type: str         # 印章类型
    seal_image_url: str    # 印章图片URL
    create_time: str       # 创建时间
    status: str            # 状态
```

### FileInfo (文件信息)

```python
class FileInfo:
    file_id: str           # 文件ID
    file_name: str         # 文件名
    file_size: int         # 文件大小（字节）
    file_type: str         # 文件类型
    create_time: str       # 创建时间
    status: str            # 文件状态
```

### TemplateInfo (模板信息)

```python
class TemplateInfo:
    template_id: str       # 模板ID
    template_name: str     # 模板名称
    template_type: str     # 模板类型
    create_time: str       # 创建时间
    status: str            # 状态
```

### TemplateFillValue (模板填充值)

```python
class TemplateFillValue:
    field_id: str          # 字段ID
    field_value: str       # 字段值
    field_name: str        # 字段名称（可选）
```

### SignPosition (签署位置)

```python
class SignPosition:
    page: int              # 页码（从1开始）
    x: float               # X坐标（左下角为原点，单位：像素）
    y: float               # Y坐标
    seal_id: str           # 印章ID（可选，不传使用默认印章）
    width: float           # 印章宽度（可选）
    height: float          # 印章高度（可选）
```

### SignKeyword (签署关键字)

```python
class SignKeyword:
    keyword: str           # 关键字
    match_strategy: str    # 匹配策略：FIRST/LAST/ALL
    offset_x: float        # X偏移量（可选）
    offset_y: float        # Y偏移量（可选）
    seal_id: str           # 印章ID（可选）
```

### Signer (签署人)

```python
class Signer:
    client_user_id: str        # 用户标识
    signer_type: str           # 签署人类型
    sign_type: str             # 签署类型
    sign_position: SignPosition    # 签署位置（POSITION类型时必填）
    sign_keyword: SignKeyword      # 签署关键字（KEYWORD类型时必填）
    sign_order: int            # 签署顺序（可选，用于顺序签署）
    sign_deadline: str         # 签署截止时间（可选）
```

### SignTaskInfo (签署任务信息)

```python
class SignTaskInfo:
    task_id: str               # 任务ID
    client_task_id: str        # 应用任务ID
    task_subject: str          # 任务主题
    task_status: str           # 任务状态
    file_id: str               # 文件ID
    template_id: str           # 模板ID
    signers: List[SignerStatus]    # 签署人状态列表
    create_time: str           # 创建时间
    update_time: str           # 更新时间
    complete_time: str         # 完成时间
    expire_time: str           # 过期时间
    initiator_id: str          # 发起人标识
```

### SignerStatus (签署人状态)

```python
class SignerStatus:
    client_user_id: str        # 用户标识
    signer_type: str           # 签署人类型
    sign_status: str           # 签署状态
    sign_time: str             # 签署时间
    reject_reason: str         # 拒绝原因
```

---

## 请求对象

### CreateSignTaskReq (创建签署任务请求)

```python
class CreateSignTaskReq:
    access_token: str                  # 访问凭证
    client_task_id: str                # 应用任务ID（必填，唯一）
    task_subject: str                  # 任务主题（必填）
    file_id: str                       # 文件ID（文件签署时必填）
    template_id: str                   # 模板ID（模板签署时必填）
    template_fill_values: List[TemplateFillValue]  # 模板填充值
    signers: List[Signer]              # 签署人列表（必填）
    expire_time: str                   # 过期时间（可选）
    auto_initiate: bool                # 是否自动发起（可选，默认true）
    callback_url: str                  # 回调地址（可选）
    business_id: str                   # 业务ID（可选，用于关联业务）
```

### GetSignTaskReq (查询签署任务请求)

```python
class GetSignTaskReq:
    access_token: str                  # 访问凭证
    task_id: str                       # 任务ID（与client_task_id二选一）
    client_task_id: str                # 应用任务ID
```

### CancelSignTaskReq (撤销签署任务请求)

```python
class CancelSignTaskReq:
    access_token: str                  # 访问凭证
    task_id: str                       # 任务ID
    cancel_reason: str                 # 撤销原因（可选）
```

### GetUserAuthUrlReq (获取用户授权链接请求)

```python
class GetUserAuthUrlReq:
    access_token: str                  # 访问凭证
    client_user_id: str                # 用户标识
    auth_scopes: List[str]             # 授权范围列表
    redirect_url: str                  # 跳转地址（可选）
    redirect_type: str                 # 跳转方式（可选）
```

### GetCorpAuthUrlReq (获取企业授权链接请求)

```python
class GetCorpAuthUrlReq:
    access_token: str                  # 访问凭证
    client_corp_id: str                # 企业标识
    corp_name: str                     # 企业名称（可选）
    corp_ident_no: str                 # 统一社会信用代码（可选）
    corp_ident_info_match: bool        # 是否严格匹配企业信息（可选）
    auth_scopes: List[str]             # 授权范围列表
    redirect_url: str                  # 跳转地址（可选）
```

### GetSignTaskSignUrlReq (获取签署链接请求)

```python
class GetSignTaskSignUrlReq:
    access_token: str                  # 访问凭证
    task_id: str                       # 任务ID
    client_user_id: str                # 签署人标识
    redirect_url: str                  # 跳转地址（可选）
```

---

## 响应对象

### BaseRes (基础响应)

```python
class BaseRes:
    code: str              # 响应码，"0"表示成功
    message: str           # 响应消息
    data: T                # 响应数据（泛型）
```

### CreateSignTaskRes (创建签署任务响应)

```python
class CreateSignTaskRes:
    task_id: str           # 任务ID
    client_task_id: str    # 应用任务ID
    task_status: str       # 任务状态
```

### GetSignTaskFileUrlRes (获取文件下载链接响应)

```python
class GetSignTaskFileUrlRes:
    file_url: str          # 文件下载URL
    file_name: str         # 文件名
    file_size: int         # 文件大小
    expire_time: str       # 链接过期时间
```

### GetUserAuthUrlRes (获取用户授权链接响应)

```python
class GetUserAuthUrlRes:
    auth_url: str          # 授权页面URL
    expire_time: str       # 链接过期时间
```

### GetCorpAuthUrlRes (获取企业授权链接响应)

```python
class GetCorpAuthUrlRes:
    auth_url: str          # 授权页面URL
    expire_time: str       # 链接过期时间
```

### GetSignTaskSignUrlRes (获取签署链接响应)

```python
class GetSignTaskSignUrlRes:
    sign_url: str          # 签署页面URL
    expire_time: str       # 链接过期时间
```

---

## 回调通知

### 签署任务状态变更回调

```python
class SignTaskCallback:
    task_id: str               # 任务ID
    client_task_id: str        # 应用任务ID
    task_status: str           # 任务状态
    signers: List[SignerStatus]    # 签署人状态
    complete_time: str         # 完成时间
    timestamp: str             # 回调时间戳
    nonce: str                 # 随机数
    sign: str                  # 签名
```

### 回调验证

```python
def verify_callback(callback_data: dict, app_secret: str) -> bool:
    """验证回调签名"""
    # 1. 提取参数
    timestamp = callback_data.get("timestamp")
    nonce = callback_data.get("nonce")
    sign = callback_data.get("sign")
    
    # 2. 构造签名串
    sign_str = f"timestamp={timestamp}&nonce={nonce}&app_secret={app_secret}"
    
    # 3. 计算签名
    calculated_sign = hashlib.sha256(sign_str.encode()).hexdigest()
    
    # 4. 验证
    return calculated_sign == sign
```

---

## 使用示例

### 创建带多个签署人的任务

```python
from fadada_api.models import *

# 创建签署人列表
signers = [
    Signer(
        client_user_id="user_001",
        signer_type=SignerType.PERSONAL,
        sign_type=SignType.POSITION,
        sign_position=SignPosition(page=1, x=100, y=200),
        sign_order=1
    ),
    Signer(
        client_user_id="corp_001",
        signer_type=SignerType.CORP,
        sign_type=SignType.KEYWORD,
        sign_keyword=SignKeyword(keyword="甲方盖章", match_strategy="FIRST"),
        sign_order=2
    )
]

# 创建任务请求
create_req = CreateSignTaskReq(
    access_token=access_token,
    client_task_id="task_20240327_001",
    task_subject="多方签署合同",
    file_id="file_abc123",
    signers=signers,
    expire_time="2024-04-27T23:59:59",
    callback_url="https://your-app.com/callback"
)
```

### 模板填充示例

```python
# 准备模板填充值
fill_values = [
    TemplateFillValue(field_id="contract_no", field_value="HT2024001"),
    TemplateFillValue(field_id="party_a", field_value="甲方科技有限公司"),
    TemplateFillValue(field_id="party_b", field_value="乙方服务有限公司"),
    TemplateFillValue(field_id="amount", field_value="¥100,000.00"),
    TemplateFillValue(field_id="sign_date", field_value="2024-03-27")
]

# 创建模板签署任务
create_req = CreateSignTaskReq(
    access_token=access_token,
    client_task_id="task_template_001",
    task_subject="服务协议",
    template_id="template_service_agreement",
    template_fill_values=fill_values,
    signers=[Signer(client_user_id="user_001", signer_type=SignerType.PERSONAL)]
)
```
