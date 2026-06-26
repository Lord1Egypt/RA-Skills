# 域名锁定操作指南

**创建日期**: 2026-03-14  
**最后更新**: 2026-03-14  
**状态**: ✅ 已验证

---

## 📋 操作概述

域名锁定是保护域名安全的重要措施，包括两种锁：

| 锁类型 | 英文名称 | 作用 | 推荐 |
|:---|:---|:---|:---|
| 转移锁 | Transfer Prohibition Lock | 禁止域名转移 | ⭐⭐⭐⭐⭐ 必开 |
| 更新锁 | Update Prohibition Lock | 禁止信息修改 | ⭐⭐⭐⭐ 推荐 |

---

## 🔐 锁定状态说明

| 状态值 | 含义 | 说明 |
|:---|:---|:---|
| `OPEN` | 已开启 | 🔒 锁定状态 |
| `CLOSE` | 已关闭 | 🔓 解锁状态 |

---

## 🛠️ API 调用方法

### 1. 开启/关闭转移锁

**API 名称**: `SaveSingleTaskForTransferProhibitionLock`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| DomainName | String | ✅ | 域名名称 |
| Status | String | ✅ | 状态值：`true`=开启，`false`=关闭 |

**⚠️ 关键参数说明**:

```python
# ✅ 正确 - 使用字符串 "true" 或 "false"
request.set_Status('true')   # 开启锁定
request.set_Status('false')  # 关闭锁定

# ❌ 错误 - 以下值都会报错
request.set_Status(True)           # 布尔值
request.set_Status('OPEN')         # 字符串 OPEN
request.set_Status('Enable')       # 字符串 Enable
request.set_Status('clientTransferProhibited')  # 状态码
```

**代码示例**:

```python
from aliyunsdkdomain.request.v20180129.SaveSingleTaskForTransferProhibitionLockRequest import SaveSingleTaskForTransferProhibitionLockRequest
import json

# 开启转移锁
request = SaveSingleTaskForTransferProhibitionLockRequest()
request.set_DomainName('shenyue.xyz')
request.set_Status('true')  # ⚠️ 必须是字符串 "true"

response = client.client.do_action_with_exception(request)
result = json.loads(response)
task_no = result.get('TaskNo', '')

print(f'转移锁开启成功！任务编号：{task_no}')
```

---

### 2. 开启/关闭更新锁

**API 名称**: `SaveSingleTaskForUpdateProhibitionLock`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| DomainName | String | ✅ | 域名名称 |
| Status | String | ✅ | 状态值：`true`=开启，`false`=关闭 |

**⚠️ 关键参数说明**:

```python
# ✅ 正确 - 使用字符串 "true" 或 "false"
request.set_Status('true')   # 开启锁定
request.set_Status('false')  # 关闭锁定

# ❌ 错误 - 以下值都会报错
request.set_Status(True)           # 布尔值
request.set_Status('OPEN')         # 字符串 OPEN
request.set_Status('Enable')       # 字符串 Enable
request.set_Status('clientUpdateProhibited')  # 状态码
```

**代码示例**:

```python
from aliyunsdkdomain.request.v20180129.SaveSingleTaskForUpdateProhibitionLockRequest import SaveSingleTaskForUpdateProhibitionLockRequest
import json

# 开启更新锁
request = SaveSingleTaskForUpdateProhibitionLockRequest()
request.set_DomainName('shenyue.xyz')
request.set_Status('true')  # ⚠️ 必须是字符串 "true"

response = client.client.do_action_with_exception(request)
result = json.loads(response)
task_no = result.get('TaskNo', '')

print(f'更新锁开启成功！任务编号：{task_no}')
```

---

## 📊 完整操作代码

### 批量锁定域名（转移锁 + 更新锁）

```python
from aliyun_domain import AliyunDomainClient
import json

client = AliyunDomainClient()

def lock_domain(domain_name: str, lock_transfer: bool = True, lock_update: bool = True) -> dict:
    """
    锁定域名（转移锁和/或更新锁）
    
    Args:
        domain_name: 域名名称
        lock_transfer: 是否开启转移锁
        lock_update: 是否开启更新锁
    
    Returns:
        包含任务编号的字典
    """
    result = {
        'domain': domain_name,
        'transfer_task': None,
        'update_task': None,
        'success': True
    }
    
    # 开启转移锁
    if lock_transfer:
        try:
            from aliyunsdkdomain.request.v20180129.SaveSingleTaskForTransferProhibitionLockRequest import SaveSingleTaskForTransferProhibitionLockRequest
            
            request = SaveSingleTaskForTransferProhibitionLockRequest()
            request.set_DomainName(domain_name)
            request.set_Status('true')  # ⚠️ 关键：字符串 "true"
            
            response = client.client.do_action_with_exception(request)
            task_result = json.loads(response)
            result['transfer_task'] = task_result.get('TaskNo', '')
            print(f'✅ {domain_name} 转移锁开启成功：{result["transfer_task"]}')
        except Exception as e:
            print(f'❌ {domain_name} 转移锁开启失败：{str(e)}')
            result['success'] = False
    
    # 开启更新锁
    if lock_update:
        try:
            from aliyunsdkdomain.request.v20180129.SaveSingleTaskForUpdateProhibitionLockRequest import SaveSingleTaskForUpdateProhibitionLockRequest
            
            request = SaveSingleTaskForUpdateProhibitionLockRequest()
            request.set_DomainName(domain_name)
            request.set_Status('true')  # ⚠️ 关键：字符串 "true"
            
            response = client.client.do_action_with_exception(request)
            task_result = json.loads(response)
            result['update_task'] = task_result.get('TaskNo', '')
            print(f'✅ {domain_name} 更新锁开启成功：{result["update_task"]}')
        except Exception as e:
            print(f'❌ {domain_name} 更新锁开启失败：{str(e)}')
            result['success'] = False
    
    return result

# 使用示例
if __name__ == '__main__':
    domains = ['shenyue.xyz', 'claw88.cn', 'claweat.com']
    
    for domain in domains:
        print(f'\n🔒 锁定域名：{domain}')
        print('-' * 50)
        result = lock_domain(domain)
        print(f'结果：{"✅ 成功" if result["success"] else "❌ 失败"}')
```

---

## 🔍 查询锁定状态

### 方法一：通过域名详情查询

```python
detail = client.query_domain_detail('shenyue.xyz')

transfer_lock = detail.get('TransferProhibitionLock', 'CLOSE')
update_lock = detail.get('UpdateProhibitionLock', 'CLOSE')

print(f'转移锁：{"🔒 OPEN" if transfer_lock == "OPEN" else "🔓 CLOSE"}')
print(f'更新锁：{"🔒 OPEN" if update_lock == "OPEN" else "🔓 CLOSE"}')
```

### 方法二：通过任务编号查询状态

```python
from aliyunsdkdomain.request.v20180129.QueryTaskDetailListRequest import QueryTaskDetailListRequest
import json

def query_task_status(task_no: str) -> str:
    """查询任务执行状态"""
    request = QueryTaskDetailListRequest()
    request.set_TaskNo(task_no)
    request.set_PageNum(1)
    request.set_PageSize(10)
    
    response = client.client.do_action_with_exception(request)
    result = json.loads(response)
    
    task_detail = result.get('Data', {}).get('TaskDetail', [{}])[0]
    return task_detail.get('TaskStatus', 'UNKNOWN')

# 使用示例
status = query_task_status('47acf182-efea-4472-ab9c-ab9e599582e3')
print(f'任务状态：{status}')  # SUCCESS / RUNNING / FAILED
```

---

## ❌ 常见错误及解决方案

### 错误 1: InvalidStatus

**错误信息**:
```
HTTP Status: 400 Error:InvalidStatus Specified parameter Status is not valid.
```

**原因**: Status 参数值不正确

**错误示例**:
```python
request.set_Status(True)                    # ❌ 布尔值
request.set_Status('OPEN')                  # ❌ 字符串 OPEN
request.set_Status('Enable')                # ❌ 字符串 Enable
request.set_Status('clientTransferProhibited')  # ❌ 状态码
```

**正确做法**:
```python
request.set_Status('true')   # ✅ 字符串 "true"
request.set_Status('false')  # ✅ 字符串 "false"
```

---

### 错误 2: MissingPageNum

**错误信息**:
```
HTTP Status: 400 Error:MissingPageNum PageNum is mandatory for this action.
```

**原因**: 查询任务时缺少必填参数

**错误示例**:
```python
request = QueryTaskDetailListRequest()
request.set_TaskNo(task_id)
# ❌ 缺少 set_PageNum 和 set_PageSize
```

**正确做法**:
```python
request = QueryTaskDetailListRequest()
request.set_TaskNo(task_id)
request.set_PageNum(1)       # ✅ 必填
request.set_PageSize(10)     # ✅ 必填
```

---

### 错误 3: 锁定后无法立即生效

**现象**: 锁定操作返回成功，但查询状态仍为 CLOSE

**原因**: 锁定操作是异步的，需要一定时间生效

**解决方案**:
```python
# 1. 执行锁定操作
result = lock_domain('shenyue.xyz')

# 2. 等待 30-60 秒
import time
time.sleep(60)

# 3. 查询确认状态
detail = client.query_domain_detail('shenyue.xyz')
print(detail.get('TransferProhibitionLock'))  # 应为 OPEN
```

---

## 📝 操作检查清单

### 锁定前

- [ ] 确认域名所有权
- [ ] 确认域名不在转移过程中
- [ ] 确认域名无未完成的工单

### 锁定后

- [ ] 等待 1-2 分钟让操作生效
- [ ] 查询域名详情确认锁定状态
- [ ] 记录任务编号以备查询

### 解锁前

- [ ] 确认需要解锁的原因
- [ ] 确认操作环境安全
- [ ] 准备好解锁后的后续操作

### 解锁后

- [ ] 尽快完成所需操作
- [ ] 操作完成后立即重新锁定
- [ ] 确认锁定状态已恢复

---

## 🎯 最佳实践

### 1. 新注册域名立即锁定

```python
def register_and_lock(domain_name: str, years: int = 1):
    """注册域名并立即锁定"""
    # 1. 注册域名
    register_result = client.register_domain(domain_name, years)
    
    # 2. 等待注册完成
    time.sleep(30)
    
    # 3. 锁定域名
    lock_domain(domain_name)
    
    print(f'✅ {domain_name} 注册并锁定完成')
```

### 2. 批量锁定账号下所有域名

```python
def lock_all_domains():
    """批量锁定所有域名"""
    domains = client.list_domains(page_size=100)
    
    for domain in domains:
        name = domain.get('DomainName')
        print(f'\n🔒 锁定：{name}')
        lock_domain(name)
        time.sleep(1)  # 避免 API 限流
```

### 3. 定期检查锁定状态

```python
def check_lock_status():
    """检查所有域名的锁定状态"""
    domains = client.list_domains(page_size=100)
    
    print('📊 域名锁定状态检查')
    print('=' * 60)
    
    for domain in domains:
        name = domain.get('DomainName')
        detail = client.query_domain_detail(name)
        
        transfer = '🔒' if detail.get('TransferProhibitionLock') == 'OPEN' else '🔓'
        update = '🔒' if detail.get('UpdateProhibitionLock') == 'OPEN' else '🔓'
        
        print(f'{name:<30} 转移：{transfer} 更新：{update}')
```

---

## 📚 相关文档

- [SKILL.md](../SKILL.md) - 技能说明文档
- [SAFE_OPERATION_GUIDE.md](../SAFE_OPERATION_GUIDE.md) - 安全操作指南
- [API_FIELD_CASE_ISSUE.md](../API_FIELD_CASE_ISSUE.md) - API 字段大小写问题

---

## 🔖 快速参考

### Status 参数值速查

| 操作 | 参数值 | 说明 |
|:---|:---|:---|
| 开启锁定 | `'true'` | ⚠️ 必须是字符串 |
| 关闭锁定 | `'false'` | ⚠️ 必须是字符串 |

### API 导入速查

```python
# 转移锁
from aliyunsdkdomain.request.v20180129.SaveSingleTaskForTransferProhibitionLockRequest import SaveSingleTaskForTransferProhibitionLockRequest

# 更新锁
from aliyunsdkdomain.request.v20180129.SaveSingleTaskForUpdateProhibitionLockRequest import SaveSingleTaskForUpdateProhibitionLockRequest

# 查询任务
from aliyunsdkdomain.request.v20180129.QueryTaskDetailListRequest import QueryTaskDetailListRequest
```

### 状态查询速查

```python
detail = client.query_domain_detail(domain_name)
transfer_lock = detail.get('TransferProhibitionLock')  # OPEN / CLOSE
update_lock = detail.get('UpdateProhibitionLock')      # OPEN / CLOSE
```

---

**经验总结**: Status 参数必须用字符串 `'true'` 或 `'false'`，不能用布尔值或其他字符串！

**创建时间**: 2026-03-14  
**最后更新**: 2026-03-14
