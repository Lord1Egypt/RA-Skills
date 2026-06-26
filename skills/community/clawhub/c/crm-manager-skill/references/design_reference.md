# CRM Manager - 设计参考

## 数据模型

### 客户实体 (Customer)

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 客户姓名（主键） |
| phone | string | 是 | 电话号码 |
| email | string | 否 | 邮箱地址（可选） |
| wechat_id | string | 否 | 微信ID（可选） |
| gender | enum | 否 | 性别：男/女/未知 |
| age | number | 否 | 年龄 |
| level | enum | 否 | 等级：普通/会员/VIP |
| source | string | 否 | 客户来源 |
| tags | list | 否 | 标签列表 |
| status | enum | 否 | 状态：新增/跟进中/已成交/暂停/流失 |
| last_contact | date | 否 | 最后联系日期 |
| notes | list | 否 | 跟进记录（日常沟通） |
| service_records | list | 否 | 服务记录（结构化服务数据） |
| created_at | datetime | 自动 | 创建时间 |
| updated_at | datetime | 自动 | 更新时间 |

### 服务记录 (ServiceRecord)

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 服务记录ID（格式：SR001） |
| date | date | 是 | 发生日期 |
| type | enum | 是 | 服务类型：课程购买/单次服务/体验课/续费/课程调整/进度评估/反馈沟通 |
| description | string | 是 | 描述说明 |
| attendance | enum | 否 | 出勤状态：出席/缺席/请假/补课 |
| duration | number | 否 | 服务时长（分钟） |
| progress | enum | 否 | 进度评级：优秀/良好/一般/需加强 |
| amount | number | 否 | 涉及金额 |
| outcome | enum | 否 | 结果：成功/失败/进行中 |
| related_note_id | string | 否 | 关联的跟进记录ID |

## 意图定义

### add_customer
- **描述**: 新增客户
- **必填实体**: name, phone
- **可选实体**: email, wechat_id, gender, age, level, source, tags
- **动作**: create_customer

### update_customer
- **描述**: 更新客户信息
- **必填实体**: name
- **可选实体**: phone, email, wechat_id, gender, age, level, source, tags, status
- **动作**: update_customer

### add_note
- **描述**: 添加跟进记录
- **必填实体**: name
- **可选实体**: note, status
- **动作**: add_note

### add_service_record
- **描述**: 添加服务记录
- **必填实体**: name, type, description
- **可选实体**: attendance, duration, progress, amount, outcome, related_note_id
- **动作**: add_service_record

### query_customer
- **描述**: 查询客户详情
- **必填实体**: name
- **动作**: query_customer

### search_customers
- **描述**: 搜索客户
- **可选实体**: tags, status, level, age_range, email, wechat_id
- **动作**: search_customers

### analyze_service_data
- **描述**: 服务数据分析
- **可选实体**: time_range, type
- **动作**: analyze_service_data

## YAML 文件示例

```yaml
name: "李雷"
phone: "13800001111"
email: "lilei@example.com"
wechat_id: "leilei123"
gender: "男"
age: 35
level: "VIP"
source: "推荐"
tags:
  - "健身会员"
  - "老客户"
status: "跟进中"
last_contact: "2026-04-03"
notes:
  - "2026-04-03: 今天深蹲进步了10kg"
  - "2026-04-01: 首次体验课，对力量训练很感兴趣"
service_records:
  - id: "SR001"
    date: "2026-04-01"
    type: "体验课"
    description: "力量训练体验课，客户表现积极"
    attendance: "出席"
    duration: 60
    progress: "良好"
    outcome: "成功"
    related_note_id: null
  - id: "SR002"
    date: "2026-04-03"
    type: "单次服务"
    description: "私教课程，深蹲训练，从50kg进步到60kg"
    attendance: "出席"
    duration: 90
    progress: "优秀"
    amount: 300
    outcome: "成功"
    related_note_id: null
  - id: "SR003"
    date: "2026-04-05"
    type: "课程购买"
    description: "购买10次私教课程包"
    amount: 3000
    outcome: "成功"
    related_note_id: null
created_at: "2026-04-01 10:30:00"
updated_at: "2026-04-05 15:20:00"
```

## 触发词示例

- "新增客户李雷，电话13800001111"
- "添加客户王芳，电话13900002222，微信wangfang99"
- "新增客户张三，电话13700003333，邮箱zhangsan@example.com"
- "更新王芳的等级为VIP"
- "给张三添加跟进记录：今天状态很好"
- "为李雷添加服务记录：单次服务，健身课60分钟，深蹲进步明显"
- "记录王芳的课程购买：买了10次心理咨询课，金额3000"
- "查询李雷的信息"
- "搜索所有VIP客户"
- "列出标签为健身会员的客户"
- "搜索微信ID包含wang的客户"
- "服务数据分析"
- "查看服务类型为单次服务的客户"