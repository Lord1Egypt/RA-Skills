# Systems 字段定义与分类规则

## Systems 数据模型

`systems` 数组包含两类系统：

### 1. 技术架构层 (category: "layer")

定义技术架构的分层结构，如客户端层、网关层、数据存储层等。

**特征**：
- `category`: "layer"
- `layer`: 显式指定层级名称（如 "访问入口层"、"接入网关层"、"平台基础层"、"数据存储层"）
- `name` 通常以"层"结尾
- `description` 描述这一层包含的内容（"包含XX、XX等组件"）

**示例**：
```json
{
  "id": "sys-001",
  "kind": "system",
  "name": "客户端层",
  "category": "layer",
  "layer": "访问入口层",
  "aliases": ["前端层", "Frontend"],
  "description": "包含移动端APP、Web端、桌面端、小程序等多端访问入口",
  "resolution": {"status": "canonical", "canonicalName": "客户端层"},
  "capabilityIds": ["cap-001"]
}
```

### 2. 业务服务模块 (category: "service")

具体业务能力系统，如会议服务、审批服务、CRM系统等。

**特征**：
- `category`: "service"
- 无需 `layer` 字段（系统会自动推断）
- `name` 通常以"服务"、"系统"结尾
- `description` 描述具体业务能力（"提供XX能力"）

**示例**：
```json
{
  "id": "sys-002",
  "kind": "system",
  "name": "会议日程服务",
  "category": "service",
  "aliases": [],
  "description": "提供会议预约、日程管理、会议室冲突检测等能力",
  "resolution": {"status": "canonical", "canonicalName": "会议日程服务"},
  "capabilityIds": ["cap-002"]
}
```

## 自动分层推断规则

如果 `category` 或 `layer` 字段缺失，系统会根据 `name` 自动推断：

### 技术架构层推断

| 名称关键词 | 推断层级 |
|-----------|---------|
| 客户端、前端、APP | 访问入口层 |
| 网关、接入、Gateway | 接入网关层 |
| 微服务、核心、Core | 平台基础层 |
| 数据、存储、Database | 数据存储层 |
| 基础设施、运维、Ops | 基础设施层 |

### 业务服务层推断

| 名称关键词 | 推断层级 |
|-----------|---------|
| 开放平台、API、开发者 | 平台能力层 |
| XX服务、XX系统 | 核心业务层 |

## 产品蓝图 vs 技术蓝图

### 产品蓝图分层（推荐）

按产品能力价值分层：
- L1: 访问入口层（用户接入）
- L2: 接入网关层（API网关）
- L3: 平台基础层（用户中心、消息中心、权限中心）
- L4: 平台能力层（开放平台）
- L5: 核心业务层（具体业务服务）
- L6: 数据存储层（数据库）

### 技术蓝图分层（可选）

按技术调用链路分层：
- Frontend → Gateway → Backend → Database

**区别**：
- 产品蓝图：体现产品价值层次（业务能力为主）
- 技术蓝图：体现技术调用链路（技术架构为主）

## 导出布局路由规则

详见 `business_blueprint/export_routes.py`：

| 路由 | 触发条件 | 优先级 |
|------|---------|--------|
| poster | layer字段 OR ≥4 systems | 高 |
| swimlane | ≥3 actors + ≥4 flowSteps + 有流程顺序 | 低（最严格） |

**泳道布局最低优先级**，仅在明确流程编排场景触发。