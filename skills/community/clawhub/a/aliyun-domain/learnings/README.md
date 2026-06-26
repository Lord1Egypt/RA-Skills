# 📚 经验教训库

本文件夹收录了 aliyun-domain 技能在使用过程中遇到的 API 问题、故障排查经验和解决方案。

---

## 📖 文档列表

| 文档 | 大小 | 内容说明 |
|:---|:---|:---|
| [RENEW_LINK_FEATURE.md](RENEW_LINK_FEATURE.md) | 🔗 NEW | 自动续费链接功能说明（v1.10.0） |
| [DOMAIN_ASSET_DASHBOARD.md](DOMAIN_ASSET_DASHBOARD.md) | 📊 NEW | 域名资产评估仪表盘说明（v1.9.0） |
| [SIX_LETTER_DOMAIN.md](SIX_LETTER_DOMAIN.md) | 🔤 NEW | 6 字母域名推荐功能说明（v1.8.0） |
| [DOMAIN_INVESTMENT_HOTSPOT.md](DOMAIN_INVESTMENT_HOTSPOT.md) | 🔥 NEW | 热点域名投资分析指南 |
| [BUY_LINK_UNIVERSAL.md](BUY_LINK_UNIVERSAL.md) | 🔗 NEW | 购买链接通用功能说明（v1.7.0） |
| [BUY_LINK_FEATURE.md](BUY_LINK_FEATURE.md) | 🔗 | 购买链接功能说明（v1.6.0，已升级） |
| [API_QUICK_REFERENCE.md](API_QUICK_REFERENCE.md) | 7.4 KB | API 快速参考手册，常用 API 调用方式和参数 |
| [API_FIELD_CASE_ISSUE.md](API_FIELD_CASE_ISSUE.md) | 6.0 KB | API 字段大小写问题记录（小写 `available` vs 大写 `Available`） |
| [DOMAIN_LOCK_OPERATION.md](DOMAIN_LOCK_OPERATION.md) | 12 KB | 域名锁定操作指南（转移锁/更新锁，Status 参数必须用字符串） |
| [REGISTRANT_PROFILE_QUERY.md](REGISTRANT_PROFILE_QUERY.md) | 9.8 KB | 实名模板查询问题记录（API 返回路径解析、单条数据转数组） |

---

## 🔧 技能版本

**当前版本**: v1.10.0  
**最新功能**: 自动续费链接功能（查询域名时自动生成 Markdown 格式续费链接）  
**更新日期**: 2026-03-15

---

## 🔍 常见问题速查

### API 字段大小写

| ❌ 错误 | ✅ 正确 |
|:---|:---|
| `result.get('Available')` | `result.get('available')` |
| `result.get('DomainName')` | `result.get('domain_name')` |
| `result.get('PriceInfo')` | `result.get('price_info')` |

**详情**: [API_FIELD_CASE_ISSUE.md](API_FIELD_CASE_ISSUE.md)

---

### 域名锁定参数

| ❌ 错误 | ✅ 正确 |
|:---|:---|
| `set_Status(True)` | `set_Status('true')` |
| `set_Status('OPEN')` | `set_Status('true')` |
| `set_Status('Enable')` | `set_Status('true')` |

**详情**: [DOMAIN_LOCK_OPERATION.md](DOMAIN_LOCK_OPERATION.md)

---

### 实名模板查询

| ❌ 错误 | ✅ 正确 |
|:---|:---|
| `response['Data']['RegistrantProfile']` | `response['RegistrantProfiles']['RegistrantProfile']` |
| `profile.get('AuditStatus')` | `profile.get('RealNameStatus')` |
| 直接遍历（单条时是对象） | 先判断类型，对象转数组 |

**详情**: [REGISTRANT_PROFILE_QUERY.md](REGISTRANT_PROFILE_QUERY.md)

---

### DNS 修改 API

| ❌ 错误 | ✅ 正确 |
|:---|:---|
| `set_DomainList([...])` | `set_DomainNames(domain)` |
| `set_DnsName([...])` | `set_DomainNameServers([...])` |
| 缺少 `set_AliyunDns()` | 必须设置 `set_AliyunDns(False)` |

**详情**: [API_QUICK_REFERENCE.md](API_QUICK_REFERENCE.md)

---

### 任务查询

| ❌ 错误 | ✅ 正确 |
|:---|:---|
| 省略分页参数 | 必须设置 `set_PageNum(1)` 和 `set_PageSize(10)` |
| `query_task_list()` 返回空 | 使用原始 API 调用 |

**详情**: [API_QUICK_REFERENCE.md](API_QUICK_REFERENCE.md)

---

## 📝 贡献指南

当遇到新的 API 问题或故障时，请：

1. **记录问题现象**：错误信息、API 名称、请求参数
2. **分析原因**：API 文档、返回数据、网络抓包
3. **记录解决方案**：正确的参数、调用方式、代码示例
4. **更新本文档**：在对应的文档中添加记录，或创建新文档

---

## 📅 更新历史

| 日期 | 文档 | 更新内容 |
|:---|:---|:---|
| 2026-03-15 | 全部 | 整理到 `learnings/` 文件夹 |
| 2026-03-14 | REGISTRANT_PROFILE_QUERY.md | 实名模板查询 API 返回路径问题 |
| 2026-03-14 | DOMAIN_LOCK_OPERATION.md | 域名锁定 Status 参数必须用字符串 |
| 2026-03-14 | API_FIELD_CASE_ISSUE.md | API 字段大小写问题（available vs Available） |
| 2026-03-14 | API_QUICK_REFERENCE.md | API 快速参考手册 |

---

**维护者**: 神月 🦐  
**最后更新**: 2026-03-15
