# 阿里云域名 API 速查表

**版本**: v1.1  
**更新**: 2026-03-14

---

## 🔑 API 参数速查

### 域名锁定 Status 参数

| 操作 | 参数值 | 类型 |
|:---|:---|:---|
| 开启锁定 | `'true'` | 字符串 ✅ |
| 关闭锁定 | `'false'` | 字符串 ✅ |
| ❌ 错误值 | `True`, `'OPEN'`, `'Enable'` | 会报错 |

```python
request.set_Status('true')   # ✅ 正确
request.set_Status(True)     # ❌ 错误
```

---

### 域名查询 available 字段

| 字段 | 大小写 | 说明 |
|:---|:---|:---|
| available | 小写 ✅ | `result.get('available')` |
| domain_name | 小写 ✅ | `result.get('domain_name')` |
| premium | 小写 ✅ | `result.get('premium')` |
| price_info | 小写 ✅ | `result.get('price_info')` |

```python
result.get('available', False)  # ✅ 正确
result.get('Available', False)  # ❌ 错误
```

---

### DNS 修改参数

| 参数 | 正确方法 | 错误方法 |
|:---|:---|:---|
| 域名列表 | `set_DomainNames()` | `set_DomainList()` ❌ |
| DNS 列表 | `set_DomainNameServers()` | `set_DnsName()` ❌ |
| 阿里云 DNS | `set_AliyunDns(False)` | 不设置 ❌ |

---

### 任务查询参数

| 参数 | 必填 | 示例 |
|:---|:---:|:---|
| TaskNo | ✅ | `set_TaskNo('xxx')` |
| PageNum | ✅ | `set_PageNum(1)` |
| PageSize | ✅ | `set_PageSize(10)` |

```python
request.set_TaskNo(task_id)
request.set_PageNum(1)       # ✅ 必填
request.set_PageSize(10)     # ✅ 必填
```

---

### 实名模板查询参数

| 参数 | 必填 | 示例 |
|:---|:---:|:---|
| PageNum | ✅ | `set_PageNum(1)` |
| PageSize | ✅ | `set_PageSize(20)` |

**数据解析**:

```python
result = json.loads(response)

# ✅ 正确路径
profiles = result.get('RegistrantProfiles', {}).get('RegistrantProfile', [])

# ⚠️ 关键：处理单个对象
if isinstance(profiles, dict):
    profiles = [profiles]

# ✅ 正确字段名
status = profile.get('RealNameStatus')  # 不是 AuditStatus
```

---

## 📦 API 导入速查

```python
# 域名锁定
from aliyunsdkdomain.request.v20180129.SaveSingleTaskForTransferProhibitionLockRequest import SaveSingleTaskForTransferProhibitionLockRequest
from aliyunsdkdomain.request.v20180129.SaveSingleTaskForUpdateProhibitionLockRequest import SaveSingleTaskForUpdateProhibitionLockRequest

# 域名查询
from aliyunsdkdomain.request.v20180129.CheckDomainRequest import CheckDomainRequest

# DNS 修改
from aliyunsdkdomain.request.v20180129.SaveBatchTaskForModifyingDomainDnsRequest import SaveBatchTaskForModifyingDomainDnsRequest

# 任务查询
from aliyunsdkdomain.request.v20180129.QueryTaskDetailListRequest import QueryTaskDetailListRequest
from aliyunsdkdomain.request.v20180129.QueryTaskListRequest import QueryTaskListRequest

# 实名模板查询
from aliyunsdkdomain.request.v20180129.QueryRegistrantProfilesRequest import QueryRegistrantProfilesRequest
```

---

## ❌ 常见错误速查

| 错误信息 | 原因 | 解决方案 |
|:---|:---|:---|
| `InvalidStatus` | Status 参数值错误 | 用 `'true'` 或 `'false'` |
| `MissingPageNum` | 缺少 PageNum 参数 | 添加 `set_PageNum(1)` |
| `MissingAliyunDns` | 缺少 AliyunDns 参数 | 添加 `set_AliyunDns(False)` |
| `set_DomainList 不存在` | 参数名错误 | 改用 `set_DomainNames()` |
| `Available 字段为空` | 字段大小写错误 | 用小写 `available` |
| `query_registrant_profiles()` 返回空 | 路径错误/未处理对象 | 用 `RegistrantProfiles.RegistrantProfile` |
| `RealNameStatus 字段不存在` | 字段名错误 | 检查返回结构，可能是大小写问题 |

---

## ✅ 状态值速查

### 域名状态

| 状态码 | 含义 | 说明 |
|:---:|:---|:---|
| 1 | 续费期 | 已过期，可续费 |
| 2 | 赎回期 | 高价赎回中 |
| 3 | 正常 | ✅ 可使用 |
| 4 | 转移期 | 转移中 |
| 5 | 删除期 | 即将被删除 |

### 锁定状态

| 状态值 | 含义 | 图标 |
|:---|:---|:---|
| OPEN | 已开启 | 🔒 |
| CLOSE | 已关闭 | 🔓 |

### 任务状态

| 状态值 | 含义 | 说明 |
|:---|:---|:---|
| SUCCESS | 成功 | ✅ 完成 |
| RUNNING | 执行中 | ⏳ 等待 |
| FAILED | 失败 | ❌ 错误 |

---

## 🎯 代码模板

### 域名锁定模板

```python
def lock_domain(domain_name: str) -> bool:
    """开启域名转移锁和更新锁"""
    try:
        # 转移锁
        req1 = SaveSingleTaskForTransferProhibitionLockRequest()
        req1.set_DomainName(domain_name)
        req1.set_Status('true')  # ⚠️ 字符串
        client.client.do_action_with_exception(req1)
        
        # 更新锁
        req2 = SaveSingleTaskForUpdateProhibitionLockRequest()
        req2.set_DomainName(domain_name)
        req2.set_Status('true')  # ⚠️ 字符串
        client.client.do_action_with_exception(req2)
        
        return True
    except Exception as e:
        print(f'锁定失败：{e}')
        return False
```

### 域名查询模板

```python
def check_domain_available(domain_name: str) -> bool:
    """检查域名是否可注册"""
    result = client.check_domain(domain_name)
    return result.get('available', False)  # ⚠️ 小写
```

### DNS 修改模板

```python
def modify_dns(domain_name: str, dns_servers: list) -> bool:
    """修改域名 DNS 服务器"""
    try:
        req = SaveBatchTaskForModifyingDomainDnsRequest()
        req.set_DomainNames(domain_name)           # ⚠️ DomainNames
        req.set_DomainNameServers(dns_servers)     # ⚠️ DomainNameServers
        req.set_AliyunDns(False)                   # ⚠️ 必填
        client.client.do_action_with_exception(req)
        return True
    except Exception as e:
        print(f'DNS 修改失败：{e}')
        return False
```

### 任务查询模板

```python
def query_task(task_no: str) -> str:
    """查询任务状态"""
    req = QueryTaskDetailListRequest()
    req.set_TaskNo(task_no)
    req.set_PageNum(1)        # ⚠️ 必填
    req.set_PageSize(10)      # ⚠️ 必填
    response = client.client.do_action_with_exception(req)
    result = json.loads(response)
    return result.get('Data', {}).get('TaskDetail', [{}])[0].get('TaskStatus', '')
```

### 实名模板查询模板

```python
def query_registrant_profiles() -> list:
    """查询实名模板列表"""
    from aliyunsdkdomain.request.v20180129.QueryRegistrantProfilesRequest import QueryRegistrantProfilesRequest
    
    req = QueryRegistrantProfilesRequest()
    req.set_PageNum(1)
    req.set_PageSize(20)
    
    response = client.client.do_action_with_exception(req)
    result = json.loads(response)
    
    # ⚠️ 正确解析路径
    profiles = result.get('RegistrantProfiles', {}).get('RegistrantProfile', [])
    
    # ⚠️ 处理单个对象的情况
    if isinstance(profiles, dict):
        profiles = [profiles]
    
    return profiles

# 使用示例
profiles = query_registrant_profiles()
for p in profiles:
    id = p.get('RegistrantProfileId')
    name = p.get('ZhRegistrantName')
    status = p.get('RealNameStatus')  # ⚠️ 不是 AuditStatus
    print(f'{id}: {name} - {status}')
```

---

## 📚 详细文档

- [SKILL.md](SKILL.md) - 技能说明文档
- [DOMAIN_LOCK_OPERATION.md](DOMAIN_LOCK_OPERATION.md) - 域名锁定操作指南
- [API_FIELD_CASE_ISSUE.md](API_FIELD_CASE_ISSUE.md) - API 字段大小写问题
- [SAFE_OPERATION_GUIDE.md](SAFE_OPERATION_GUIDE.md) - 安全操作指南

---

**快速记忆**:
- Status 用字符串 `'true'` / `'false'`
- 字段用小写 `available` / `domain_name`
- 查询任务要加 `PageNum` / `PageSize`
- DNS 修改用 `DomainNames` / `DomainNameServers`
