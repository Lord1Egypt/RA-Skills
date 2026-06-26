# Blueprint 实体定义规范

本文档定义 Blueprint JSON 中所有实体的字段含义与分类规则。

## 实体概览

| 实体 | 定义 | 示例数量 |
|------|------|---------|
| **capabilities** | 业务能力领域 | 5-15 |
| **actors** | 参与角色 | 3-10 |
| **flowSteps** | 流程步骤 | 5-20 |
| **systems** | IT系统 | 5-15 |

---

## Capabilities（业务能力）

业务能力的抽象定义，不绑定具体系统或角色。

### 字段定义

```json
{
  "id": "cap-xxx",
  "name": "客户管理",
  "level": 1,
  "description": "提供客户档案、商机跟进、合同管理等客户全生命周期管理能力",
  "ownerActorIds": ["actor-001"],
  "supportingSystemIds": ["sys-001"]
}
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | ✅ | 唯一标识，格式 `cap-{seq}` |
| `name` | ✅ | 能力名称，简洁概括 |
| `level` | ✅ | 能力层级（1=核心能力，2=子能力） |
| `description` | ✅ | 能力描述（"提供XX能力"） |
| `ownerActorIds` | ⭕ | 负责该能力的角色ID列表 |
| `supportingSystemIds` | ⭕ | 支撑该能力的系统ID列表 |

### 能力命名规则

- 以动词+名词为主："客户管理"、"订单处理"、"风险控制"
- 避免："XX系统"、"XX模块"（这是systems，不是capabilities）

---

## Actors（参与角色）

参与业务流程的角色定义。

### 字段定义

```json
{
  "id": "actor-xxx",
  "name": "企业普通员工"
}
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | ✅ | 唯一标识，格式 `actor-{seq}` |
| `name` | ✅ | 角色名称 |

### 角色命名规则

- 具体："企业普通员工"、"销售经理"、"财务审批员"
- 避免："用户"、"管理员"（过于泛化）

---

## FlowSteps（流程步骤）

业务流程中的具体步骤，绑定角色和能力。

### 字段定义

```json
{
  "id": "flow-xxx",
  "name": "发起审批申请",
  "actorId": "actor-001",
  "capabilityIds": ["cap-003"],
  "systemIds": ["sys-001", "sys-005"],
  "stepType": "task",
  "inputRefs": [],
  "outputRefs": []
}
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | ✅ | 唯一标识，格式 `flow-{seq}` |
| `name` | ✅ | 步骤名称（动词开头："发起XX"、"审批XX"） |
| `actorId` | ✅ | 执行该步骤的角色ID |
| `capabilityIds` | ✅ | 涉及的能力ID列表 |
| `systemIds` | ⭕ | 涉及的系统ID列表 |
| `stepType` | ✅ | 步骤类型：`task`（任务）或 `decision`（判断） |
| `inputRefs` | ⭕ | 输入依赖的flowStep ID（用于泳道布局） |
| `outputRefs` | ⭕ | 输出指向的flowStep ID（用于泳道布局） |

### 流程步骤命名规则

- 动词开头："发起审批申请"、"审核报销单"、"配置组织架构"
- 避免："审批流程"、"会议管理"（这是capability，不是step）

---

## Systems（IT系统）

详见 `systems-schema.md`。

### 快速区分

| 类型 | category | 示例 |
|------|----------|------|
| 技术架构层 | `layer` | 客户端层、网关层、数据存储层 |
| 业务服务模块 | `service` | 会议服务、审批服务、CRM系统 |

---

## Relations（关系）

系统与能力之间的支撑关系。

### 字段定义

```json
{
  "id": "rel-xxx",
  "type": "supports",
  "from": "sys-001",
  "to": "cap-001",
  "label": "支撑"
}
```

### 关系类型

| type | from → to | 说明 |
|------|-----------|------|
| `supports` | system → capability | 系统支撑能力 |
| `depends` | system → system | 系统依赖关系 |
| `realizes` | actor → capability | 角色实现能力 |

---

## 行业Hints（提取指导）

行业特定的实体提取指导，位于 `templates/{industry}/seed.json` 的 `industryHints.checklist`。

### 示例

```json
{
  "industryHints": {
    "title": "金融行业蓝图关注点",
    "checklist": [
      "风险控制：风险评估、预警、处置、反欺诈",
      "信贷管理：授信、用信、贷后管理",
      "客户画像：客户分层、画像标签、精准营销"
    ]
  }
}
```

### 使用方式

AI读取 `industryHints.checklist` 后：
- 确保提取的 capabilities 覆盖 checklist 提到的领域
- 避免遗漏关键业务能力

---

## 文件组织

| 文件 | 作用 | 内容 |
|------|------|------|
| `SKILL.md` | 路由层 | 指向 specs/ 和 templates/ |
| `specs/entities-schema.md` | 实体定义 | 本文档（字段含义） |
| `specs/systems-schema.md` | Systems分类 | Systems的category/layer规则 |
| `templates/common/seed.json` | 字段示例 | 所有实体的示例字段 |
| `templates/{industry}/seed.json` | 行业指导 | industryHints.checklist |

---

## 常见错误

### 1. 混淆 capability 和 system

❌ 错误：
```json
{
  "name": "审批系统",  // ← 这是system，不是capability
  "level": 1,
  "description": "提供审批能力的系统"
}
```

✅ 正确：
```json
// Capability
{
  "name": "流程审批",
  "level": 1,
  "description": "提供请假、报销、采购等全场景审批能力"
}

// System
{
  "name": "审批流程服务",
  "category": "service",
  "description": "提供流程设计、流转、通知等审批相关业务服务能力"
}
```

### 2. 混淆 flowStep 和 capability

❌ 错误：
```json
{
  "name": "审批流程",  // ← 这是capability
  "stepType": "task"
}
```

✅ 正确：
```json
{
  "name": "发起审批申请",  // ← 具体动作
  "stepType": "task"
}
```

### 3. Actor过于泛化

❌ 错误：
```json
{
  "name": "用户"  // ← 不明确
}
```

✅ 正确：
```json
{
  "name": "企业普通员工"
}
```