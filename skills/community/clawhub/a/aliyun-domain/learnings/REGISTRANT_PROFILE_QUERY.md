# 实名模板查询操作指南

**创建日期**: 2026-03-14  
**问题**: API 返回数据解析错误导致模板查询失败  
**状态**: ✅ 已解决

---

## 🐛 问题现象

### 错误表现

使用封装方法 `query_registrant_profiles()` 查询实名模板，返回空列表，但实际账号下有 4 个模板。

```python
# ❌ 错误结果
templates = client.query_registrant_profiles(page_num=1, page_size=20)
print(f'模板数量：{len(templates)}')  # 输出：0（错误！）
```

### 实际情况

通过原始 API 调用发现账号下有 4 个模板：

| 模板 ID | 类型 | 姓名 | 状态 |
|:---|:---|:---|:---|
| 24485442 | 个人 | 叶峰 | ✅ 已通过 |
| 24485412 | 个人 | 叶峰 | ✅ 已通过 |
| 24427643 | 个人 | 叶峰 | ⏳ 审核中 |
| 24414746 | 个人 | 叶峰 | ⏳ 审核中 |

---

## 🔍 问题原因

### 原因 1：API 返回格式特殊

阿里云 `QueryRegistrantProfiles` API 返回的数据结构是**嵌套对象**，而非直接数组：

```json
{
  "RegistrantProfiles": {
    "RegistrantProfile": [
      { ... },
      { ... }
    ]
  }
}
```

### 原因 2：单条数据时返回对象而非数组

当只有 1 条数据时，`RegistrantProfile` 是**对象**而非**数组**：

```json
{
  "RegistrantProfiles": {
    "RegistrantProfile": { ... }  // 单个对象，不是数组！
  }
}
```

### 原因 3：封装方法解析错误

原封装方法假设 `Data` 下直接有 `RegistrantProfile`，但实际路径是：

```python
# ❌ 错误路径
response['Data']['RegistrantProfile']

# ✅ 正确路径
response['RegistrantProfiles']['RegistrantProfile']
```

---

## ✅ 正确调用方法

### 方法一：原始 API 调用（推荐）

```python
from aliyunsdkdomain.request.v20180129.QueryRegistrantProfilesRequest import QueryRegistrantProfilesRequest
import json

# 创建请求
request = QueryRegistrantProfilesRequest()
request.set_PageNum(1)
request.set_PageSize(20)

# 执行请求
response = client.client.do_action_with_exception(request)
result = json.loads(response)

# 正确解析数据
profiles_data = result.get('RegistrantProfiles', {}).get('RegistrantProfile', [])

# ⚠️ 关键：如果是单个对象，转为数组
if isinstance(profiles_data, dict):
    profiles_data = [profiles_data]

# 遍历结果
for profile in profiles_data:
    template_id = profile.get('RegistrantProfileId')
    name = profile.get('ZhRegistrantName', profile.get('RegistrantName'))
    status = profile.get('RealNameStatus')
    print(f'{template_id}: {name} - {status}')
```

---

### 方法二：修复封装方法

```python
def query_registrant_profiles(self, page_num: int = 1, 
                               page_size: int = 100) -> List[Dict]:
    """
    查询注册者信息模板列表（修复版）
    
    Args:
        page_num: 页码
        page_size: 每页数量
    
    Returns:
        注册者信息列表
    """
    from aliyunsdkdomain.request.v20180129.QueryRegistrantProfilesRequest import QueryRegistrantProfilesRequest
    
    request = QueryRegistrantProfilesRequest()
    request.set_PageNum(page_num)
    request.set_PageSize(page_size)
    
    response = self._do_request(request)
    
    # ⚠️ 关键修复点 1: 正确的数据路径
    profiles_data = response.get('RegistrantProfiles', {}).get('RegistrantProfile', [])
    
    # ⚠️ 关键修复点 2: 处理单个对象的情况
    if isinstance(profiles_data, dict):
        profiles_data = [profiles_data]
    
    return profiles_data
```

---

## 📊 API 返回结构详解

### 完整返回示例

```json
{
  "PrePage": false,
  "CurrentPageNum": 1,
  "RequestId": "ED0B26B4-82AE-5CCD-BB1F-6640B753B285",
  "PageSize": 20,
  "TotalPageNum": 1,
  "RegistrantProfiles": {
    "RegistrantProfile": [
      {
        "RegistrantProfileId": 24485442,
        "RegistrantProfileType": "common",
        "RegistrantType": "1",
        "RegistrantName": "ye feng",
        "ZhRegistrantName": "叶峰",
        "RegistrantOrganization": "ye feng",
        "ZhRegistrantOrganization": "叶峰",
        "Email": "115785563@qq.com",
        "Telephone": "15001373822",
        "RealNameStatus": "SUCCEED",
        "DefaultRegistrantProfile": false,
        "CreateTime": "2026-03-02 12:13:36",
        "UpdateTime": "2026-03-02 13:59:31"
      }
    ]
  },
  "TotalItemNum": 4,
  "NextPage": false
}
```

### 关键字段说明

| 字段 | 路径 | 类型 | 说明 |
|:---|:---|:---|:---|
| 模板列表 | `RegistrantProfiles.RegistrantProfile` | Array/Object | ⚠️ 可能是对象或数组 |
| 模板 ID | `RegistrantProfileId` | Integer | 唯一标识 |
| 模板类型 | `RegistrantProfileType` | String | common=个人，enterprise=企业 |
| 注册者类型 | `RegistrantType` | String | 1=个人，2=企业 |
| 姓名 | `ZhRegistrantName` | String | 中文姓名 |
| 实名状态 | `RealNameStatus` | String | SUCCEED/AUDITING/FAILED |
| 是否默认 | `DefaultRegistrantProfile` | Boolean | 是否默认模板 |

---

## 🎯 完整查询代码

```python
from aliyun_domain import AliyunDomainClient
import json

client = AliyunDomainClient()

def query_registrant_profiles_correct():
    """正确查询实名模板列表"""
    
    from aliyunsdkdomain.request.v20180129.QueryRegistrantProfilesRequest import QueryRegistrantProfilesRequest
    
    request = QueryRegistrantProfilesRequest()
    request.set_PageNum(1)
    request.set_PageSize(20)
    
    response = client.client.do_action_with_exception(request)
    result = json.loads(response)
    
    # 正确解析
    profiles_data = result.get('RegistrantProfiles', {}).get('RegistrantProfile', [])
    
    # 处理单个对象的情况
    if isinstance(profiles_data, dict):
        profiles_data = [profiles_data]
    
    # 格式化输出
    print(f'{"模板 ID":<15} {"类型":<8} {"姓名":<15} {"状态":<10} {"默认"}')
    print('-' * 70)
    
    for profile in profiles_data:
        template_id = profile.get('RegistrantProfileId', 'N/A')
        template_type = '个人' if str(profile.get('RegistrantType')) == '1' else '企业'
        name = profile.get('ZhRegistrantName', profile.get('RegistrantName', 'N/A'))
        status = profile.get('RealNameStatus', 'N/A')
        is_default = profile.get('DefaultRegistrantProfile', False)
        
        status_icon = '✅' if status == 'SUCCEED' else '⏳' if status == 'AUDITING' else '❌'
        default_icon = '⭐' if is_default else ''
        
        print(f'{template_id:<15} {template_type:<8} {name:<15} {status_icon} {status:<6} {default_icon}')
    
    return profiles_data

# 使用示例
if __name__ == '__main__':
    profiles = query_registrant_profiles_correct()
    print(f'\n共 {len(profiles)} 个模板')
```

---

## ❌ 常见错误

### 错误 1：路径错误

```python
# ❌ 错误 - 使用了错误的路径
profiles = response['Data']['RegistrantProfile']

# ✅ 正确 - 使用正确的路径
profiles = response['RegistrantProfiles']['RegistrantProfile']
```

### 错误 2：未处理单个对象

```python
# ❌ 错误 - 假设总是数组
for profile in profiles_data:
    print(profile.get('RegistrantProfileId'))
    # 如果是单个对象，会遍历对象的键而非列表

# ✅ 正确 - 先转为数组
if isinstance(profiles_data, dict):
    profiles_data = [profiles_data]
for profile in profiles_data:
    print(profile.get('RegistrantProfileId'))
```

### 错误 3：字段名错误

```python
# ❌ 错误 - 使用了不存在的字段
status = profile.get('AuditStatus')  # 这个字段不存在

# ✅ 正确 - 使用正确的字段名
status = profile.get('RealNameStatus')  # 正确的字段名
```

---

## 📋 字段对照表

| 用途 | 正确字段 | 错误字段 |
|:---|:---|:---|
| 实名状态 | `RealNameStatus` | `AuditStatus` ❌ |
| 中文姓名 | `ZhRegistrantName` | `RegistrantName` (英文) |
| 模板类型 | `RegistrantProfileType` | `RegistrantType` ❌ |
| 注册者类型 | `RegistrantType` | `RegistrantProfileType` ❌ |
| 是否默认 | `DefaultRegistrantProfile` | `IsDefault` ❌ |

---

## 🔖 快速参考

### API 导入

```python
from aliyunsdkdomain.request.v20180129.QueryRegistrantProfilesRequest import QueryRegistrantProfilesRequest
```

### 请求参数

```python
request = QueryRegistrantProfilesRequest()
request.set_PageNum(1)       # 页码
request.set_PageSize(20)     # 每页数量
```

### 数据解析

```python
result = json.loads(response)
profiles = result.get('RegistrantProfiles', {}).get('RegistrantProfile', [])

# ⚠️ 关键：处理单个对象
if isinstance(profiles, dict):
    profiles = [profiles]
```

### 状态值

| 值 | 含义 | 图标 |
|:---|:---|:---|
| SUCCEED | 已通过 | ✅ |
| AUDITING | 审核中 | ⏳ |
| FAILED | 审核失败 | ❌ |

---

## 🎯 最佳实践

### 1. 始终检查数据类型

```python
profiles = result.get('RegistrantProfiles', {}).get('RegistrantProfile', [])
if isinstance(profiles, dict):
    profiles = [profiles]
```

### 2. 使用容错取值

```python
name = profile.get('ZhRegistrantName', profile.get('RegistrantName', 'N/A'))
```

### 3. 验证返回结构

```python
if 'RegistrantProfiles' not in result:
    print('API 返回格式异常')
    return []
```

### 4. 记录原始响应

```python
import json
print(f'原始响应：{json.dumps(result, indent=2, ensure_ascii=False)}')
```

---

## 📚 相关文档

- [SKILL.md](../SKILL.md) - 技能说明文档
- [API_QUICK_REFERENCE.md](../API_QUICK_REFERENCE.md) - API 速查表
- [API_FIELD_CASE_ISSUE.md](../API_FIELD_CASE_ISSUE.md) - API 字段大小写问题
- [DOMAIN_LOCK_OPERATION.md](../DOMAIN_LOCK_OPERATION.md) - 域名锁定操作指南

---

**经验总结**: 
1. ✅ API 返回路径是 `RegistrantProfiles.RegistrantProfile`，不是 `Data.RegistrantProfile`
2. ✅ `RegistrantProfile` 可能是对象或数组，需要先判断类型
3. ✅ 实名状态字段是 `RealNameStatus`，不是 `AuditStatus`

**创建时间**: 2026-03-14  
**最后更新**: 2026-03-14
