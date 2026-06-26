# 阿里云域名管理技能

<div align="center">

**通过阿里云 OpenAPI 管理您的域名资产**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Aliyun SDK](https://img.shields.io/badge/aliyun--sdk-domain-orange.svg)](https://next.api.aliyun.com/api/Domain/2018-01-29)

</div>

## 📋 功能特性

- ✅ **域名查询** - 列表查询、详情查询、域名可用性检查
- ✅ **域名管理** - 续费、DNS 修改、转移锁、自动续费
- ✅ **任务管理** - 任务列表查询、任务详情查询
- ✅ **分组管理** - 创建分组、域名分组管理
- ✅ **DNS 主机** - DNS 主机创建、修改、删除
- ✅ **联系人管理** - 注册者信息模板管理
- ✅ **统计分析** - 域名统计、过期预警
- ✅ **优惠政策咨询** - 注册活动价格、批量优惠、转入优惠、续费折扣、优惠口令查询

## 🚀 快速开始

### 1. 安装依赖

```bash
pip3 install -r requirements.txt
```

### 2. 配置凭证

```bash
# 复制配置模板
cp config/credentials.json.example config/credentials.json

# 编辑配置文件，填入您的阿里云 AK/SK
vim config/credentials.json
```

配置文件格式：

```json
{
  "access_key_id": "LTAI5t...",
  "access_key_secret": "abcdef...",
  "region_id": "cn-hangzhou"
}
```

### 3. 获取阿里云 AccessKey

1. 登录 [阿里云 RAM 控制台](https://ram.console.aliyun.com/)
2. 创建用户或使用现有用户
3. 创建 AccessKey
4. 为用户授权 `AliyunDomainFullAccess` 权限

## 💻 使用方法

### 命令行工具

```bash
# 查询域名列表
python3 scripts/aliyun_domain.py list

# 按后缀筛选
python3 scripts/aliyun_domain.py list --tld com

# 关键词搜索
python3 scripts/aliyun_domain.py list -k example

# 查询域名详情
python3 scripts/aliyun_domain.py detail -d example.com

# 查询即将过期域名
python3 scripts/aliyun_domain.py expiring --days 30

# 域名续费
python3 scripts/aliyun_domain.py renew -d example.com --years 1

# 查询任务列表
python3 scripts/aliyun_domain.py tasks

# 查询域名分组
python3 scripts/aliyun_domain.py groups --list

# 创建域名分组
python3 scripts/aliyun_domain.py groups --create "我的域名"

# 查询 DNS 主机
python3 scripts/aliyun_domain.py dns -d example.com --list

# 域名统计
python3 scripts/aliyun_domain.py stats

# 查询联系人信息
python3 scripts/aliyun_domain.py contact -d example.com
```

### Python 代码

```python
from aliyun_domain import AliyunDomainClient

# 初始化客户端
client = AliyunDomainClient()

# 查询域名列表
domains = client.list_domains(page_size=100)
for domain in domains:
    print(f"{domain['DomainName']} - {domain['ExpirationDate']}")

# 查询域名详情
detail = client.query_domain_detail("example.com")
print(detail)

# 查询即将过期域名
expiring = client.query_expiring_domains(days=30)
print(f"即将过期：{len(expiring)} 个域名")

# 域名续费
result = client.renew_domain("example.com", years=1)
print(f"续费任务编号：{result['TaskNo']}")

# 获取域名统计
stats = client.get_domain_statistics()
print(f"总域名数：{stats['total']}")
print(f"即将过期 (30 天): {stats['expiring_30_days']}")
```

## 📚 API 参考

### 域名查询

| 方法 | 说明 |
|------|------|
| `list_domains()` | 查询域名列表（支持分页、筛选） |
| `scroll_domains()` | 滚动查询域名列表（适合大数据量） |
| `query_domain_detail()` | 查询域名详情 |
| `query_domain_by_instance()` | 根据实例 ID 查询 |
| `check_domain()` | 检查域名是否可注册 |
| `query_contact_info()` | 查询联系人信息 |

### 域名管理

| 方法 | 说明 |
|------|------|
| `renew_domain()` | 域名续费 |
| `batch_renew_domains()` | 批量域名续费 |
| `modify_domain_dns()` | 修改 DNS 服务器 |
| `set_transfer_prohibition_lock()` | 设置转移锁 |
| `query_transfer_out_info()` | 查询转出信息 |
| `query_transfer_authorization_code()` | 查询转移密码 |
| `approve_transfer_out()` | 批准转出 |
| `cancel_transfer_out()` | 取消转出 |
| `setup_auto_renew()` | 设置自动续费 |

### 任务管理

| 方法 | 说明 |
|------|------|
| `query_task_list()` | 查询任务列表 |
| `query_task_detail()` | 查询任务详情 |
| `query_task_history()` | 查询任务历史 |

### 分组管理

| 方法 | 说明 |
|------|------|
| `create_domain_group()` | 创建域名分组 |
| `query_domain_group_list()` | 查询分组列表 |
| `update_domain_to_group()` | 将域名移到分组 |
| `delete_domain_group()` | 删除分组 |

### DNS 主机管理

| 方法 | 说明 |
|------|------|
| `create_dns_host()` | 创建 DNS 主机 |
| `modify_dns_host()` | 修改 DNS 主机 |
| `delete_dns_host()` | 删除 DNS 主机 |
| `query_dns_host()` | 查询 DNS 主机 |

### 注册者信息管理

| 方法 | 说明 |
|------|------|
| `create_registrant_profile()` | 创建注册者模板 |
| `query_registrant_profiles()` | 查询注册者模板列表 |
| `set_default_registrant_profile()` | 设置默认模板 |

### 辅助方法

| 方法 | 说明 |
|------|------|
| `query_expiring_domains()` | 查询即将过期域名 |
| `get_all_domains()` | 获取所有域名 |
| `get_domain_statistics()` | 获取域名统计 |

## 📁 文件结构

```
aliyun/
├── SKILL.md                    # 技能说明文档
├── README.md                   # 本文件
├── requirements.txt            # Python 依赖
├── .gitignore                  # Git 忽略配置
├── config/
│   ├── credentials.json        # 凭证配置（需自行创建）
│   └── credentials.json.example # 配置模板
├── knowledge/                          # 本地知识库
│   └── domain_pricing_discounts.md     # 优惠政策知识库
└── scripts/
    ├── aliyun_domain.py        # 域名 API 客户端
    └── aliyun_cli.py           # 命令行工具（待开发）
```

## 🔐 安全建议

- ⚠️ **不要将 credentials.json 提交到 Git**（已添加到 .gitignore）
- ✅ 建议使用 RAM 子账号 AK，而非主账号
- ✅ 遵循最小权限原则，只授予必要权限
- ✅ 定期轮换 AccessKey
- ✅ 使用环境变量或密钥管理服务存储敏感信息

## ⚠️ 注意事项

1. **API 调用限制**：阿里云 API 有 QPS 限制，请避免高频调用
2. **权限要求**：需要 `AliyunDomainFullAccess` 或自定义权限策略
3. **地域选择**：域名 API 主要使用 `cn-hangzhou` 地域
4. **费用说明**：部分 API 调用可能产生费用（如域名续费）
5. **超时设置**：大量域名查询时建议增加超时时间

## 🆘 故障排查

### 问题：配置文件不存在

```
❌ 配置错误：配置文件不存在：...
```

**解决**：复制配置模板并填入正确的 AK/SK

```bash
cp config/credentials.json.example config/credentials.json
vim config/credentials.json
```

### 问题：AccessKey 无效

```
❌ 服务端错误：InvalidAccessKeyId.NotFound
```

**解决**：检查 credentials.json 中的 AK/SK 是否正确，确认 RAM 用户已授权

### 问题：权限不足

```
❌ 服务端错误：Forbidden.Ram
```

**解决**：为 RAM 用户添加 `AliyunDomainFullAccess` 权限策略

### 问题：API 调用失败

```
❌ 客户端错误：SDK.Server.Unreachable
```

**解决**：检查网络连接，确认可以访问 api.aliyuncs.com

### 问题：修改 DNS 时报错 `MissingAliyunDns`

```
❌ 服务端错误：HTTP Status: 400 Error:MissingAliyunDns
```

**解决**：确保调用时设置了 `set_AliyunDns(False)` 参数

```python
request.set_DomainNames(domain_name)
request.set_DomainNameServers(dns_servers)
request.set_AliyunDns(False)  # ✅ 必需参数
```

### 问题：修改 DNS 时报错 `set_DomainList` 不存在

```
❌ AttributeError: 'SaveBatchTaskForModifyingDomainDnsRequest' object has no attribute 'set_DomainList'
```

**解决**：使用正确的参数名

```python
# ❌ 错误
request.set_DomainList([...])

# ✅ 正确
request.set_DomainNames(domain_name)        # 字符串
request.set_DomainNameServers(dns_servers)  # 列表
```

### 问题：`query_task_list()` 返回空列表

**现象**：即使有任务，`client.query_task_list()` 也返回 `[]`

**解决**：使用原始 API 调用

```python
from aliyunsdkdomain.request.v20180129.QueryTaskListRequest import QueryTaskListRequest

request = QueryTaskListRequest()
request.set_PageNum(1)
request.set_PageSize(100)

response = client.client.do_action_with_exception(request)
data = json.loads(response)
tasks = data['Data']['TaskInfo']  # ✅ 正确获取
```

---

## 📝 常见问题与解决方案

详细的 API 参数问题和解决方案，请参阅：

- 📄 [DNS_MODIFICATION_ISSUES.md](DNS_MODIFICATION_ISSUES.md) - DNS 修改 API 参数问题记录

**常见问题**：
1. ❌ `set_DomainList()` 不存在 → ✅ 使用 `set_DomainNames()` + `set_DomainNameServers()`
2. ❌ `set_DnsName()` 不存在 → ✅ 使用 `set_DomainNameServers()`
3. ❌ 缺少 `set_AliyunDns()` → ✅ 必须设置 `set_AliyunDns(False)`
4. ❌ `query_task_list()` 返回空 → ✅ 使用原始 API 调用

## 📞 支持

- **阿里云域名 API 文档**: https://next.api.aliyun.com/api/Domain/2018-01-29
- **阿里云帮助文档**: https://help.aliyun.com/product/35836.html
- **SDK GitHub**: https://github.com/aliyun/alibaba-cloud-sdk-python

## 📝 更新日志

### v1.0.0 (2026-03-13)

- ✨ 初始版本发布
- ✅ 支持域名查询、管理、任务、分组、DNS 主机等功能
- ✅ 提供命令行工具和 Python SDK
- ✅ 支持域名统计和过期预警

---

<div align="center">

**版本**: v1.3.2  
**最后更新**: 2026-03-14

</div>
