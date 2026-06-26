---
name: feishu-crm-automation
description: 飞书CRM自动化技能。当用户提到客户管理、销售跟进、CRM录入、飞书表格自动填充、跟进提醒、生成本周客户报告时使用。功能：客户信息录入多维表格、超期未跟进自动提醒、客户周报生成。
version: 1.0.0
---

# 飞书CRM自动化技能

## 快速开始

### 核心功能
1. **客户录入** - 将客户信息写入飞书多维表格
2. **跟进提醒** - 自动找出超过N天未跟进的客户
3. **周报生成** - 生成本周新增客户汇总

### 前提条件
- 飞书多维表格（Bitable）已创建，包含以下字段：
  - 客户名称（文本）
  - 联系方式（文本）
  - 客户需求（文本）
  - 最近跟进日期（日期）
  - 销售负责人（用户）
  - 状态（单选：潜在客户/跟进中/已成交/流失）

## 使用场景

### 场景1：录入新客户
```
用户：添加客户 张三，手机 13800138000，需要买我们的企业版
我：提取信息并写入飞书多维表格
```

### 场景2：检查待跟进客户
```
用户：有哪些客户超过3天没跟进？
我：查询多维表格，返回超期客户列表，并询问是否发送飞书提醒
```

### 场景3：生成本周周报
```
用户：生成本周客户周报
我：查询本周新增客户，生成摘要，包含：新增客户数、各状态分布、待跟进数量
```

## 工具调用

使用 `feishu_bitable_*` 系列工具操作多维表格：

```python
# 1. 获取表格元信息
feishu_bitable_get_meta(url="飞书多维表格URL")

# 2. 列出所有记录
feishu_bitable_list_records(app_token="xxx", table_id="xxx")

# 3. 创建新记录
feishu_bitable_create_record(app_token="xxx", table_id="xxx", fields={
    "客户名称": "张三",
    "联系方式": "13800138000",
    "客户需求": "企业版采购",
    "最近跟进日期": 1743004800000,  # 毫秒时间戳
    "销售负责人": [{"id": "ou_xxx"}],
    "状态": "潜在客户"
})

# 4. 更新记录
feishu_bitable_update_record(app_token="xxx", table_id="xxx", record_id="xxx", fields={
    "最近跟进日期": 1743091200000,
    "状态": "跟进中"
})
```

## 关键参数格式

### 日期字段
- 飞书日期字段需要毫秒时间戳
- Python转换：`int(datetime.timestamp() * 1000)`

### 用户字段
```python
{"id": "飞书open_id"}  # 单个用户
[{"id": "ou_xxx"}, {"id": "ou_yyy"}]  # 多个用户
```

### 日期计算（跟进超期判断）
```python
from datetime import datetime, timedelta

# 判断是否超过N天未跟进
def is_overdue(last_followup_ts, days=3):
    last_date = datetime.fromtimestamp(last_followup_ts / 1000)
    return (datetime.now() - last_date).days > days
```

## 默认多维表格配置

如用户未指定表格，使用此默认配置引导创建：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 客户名称 | 文本 | 必填 |
| 联系方式 | 文本 | 手机号/微信/邮箱 |
| 客户需求 | 文本 | 简要描述需求 |
| 最近跟进日期 | 日期 | 上次跟进时间 |
| 销售负责人 | 用户 | 责任人 |
| 状态 | 单选 | 潜在客户/跟进中/已成交/流失 |
| 创建时间 | 创建时间 | 自动填充 |

## 飞书CRM表格配置

**表格URL**: https://my.feishu.cn/base/KgoqbzS5ZaTwLRskzKxcVucvn0e
**app_token**: KgoqbzS5ZaTwLRskzKxcVucvn0e
**table_id**: tblzrBS1Gb73OhIS

### 字段ID映射
| 字段名 | field_id | 类型 |
|--------|----------|------|
| CRM客户管理 | fldKtf8UQz | 文本（主字段） |
| 联系方式 | fldTnmsqI8 | 文本 |
| 客户需求 | fldFObE09f | 文本 |
| 最近跟进日期 | fld153WFu1 | 日期 |
| 销售负责人 | fldK7mPBKS | 用户 |
| 状态 | fld0I7rChc | 单选 |

## 参考文档

详细实现逻辑见：
- [跟进提醒逻辑](references/跟进提醒逻辑.md)
- [周报生成逻辑](references/周报生成逻辑.md)

## 注意事项

- 所有时间使用Asia/Shanghai时区
- 跟进提醒默认超期天数：3天（可配置）
- 录入新客户时，状态默认为"潜在客户"
