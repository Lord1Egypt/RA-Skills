---
name: amis-ui
description: >-
  百度amis低代码框架JSON
  Schema生成专家。精准理解业务意图，生成正确、交互友好的amis配置，支持复杂交互（点击、回调、重载、弹层），兼容移动端。
version: 1.0.1
---

# amis-ui Skill

本技能专注于百度amis低代码框架的JSON Schema生成，帮助快速构建企业级中后台页面。

## 意图理解与组件映射

### 场景 → 组件映射表

| 业务场景 | amis组件 | 关键配置 |
|---------|---------|---------|
| 数据列表展示 | CRUD | api, columns, filter |
| 表单提交 | Form | api, controls, rules |
| 详情查看 | Dialog/Drawer | title, body, actions |
| 搜索筛选 | Form (filter) | submitOnChange, target |
| 批量操作 | Button + actionType | ajax, reload |
| 页面跳转 | Button + actionType | url, link |
| 状态提示 | Button + actionType | toast, confirm |
| 多步骤流程 | Wizard | steps, source |

### 组件选择决策树

```
用户需求
    │
    ├── 登录/注册 → Form (login.json)
    │
    ├── 数据列表 → CRUD
    │       │
    │       ├── 需要搜索 → filter-crud.json
    │       ├── 需要选择数据 → select-crud.json
    │       └── 基础列表 → basic-crud.json
    │
    ├── 搜索表单 → Form (search-form.json)
    │
    ├── 弹层操作
    │       ├── 查看详情 → detail-dialog.json
    │       ├── 编辑数据 → edit-dialog.json
    │       └── 选择数据 → select-crud.json
    │
    ├── 多步骤 → Wizard (multi-step-wizard.json)
    │
    └── 数据看板 → Dashboard (dashboard.json)
```

## 移动端适配规范

### 响应式配置规则

| 桌面端 | 移动端 | 配置方式 |
|-------|-------|---------|
| 3列 | 1列 | `columnCount` + `responsive` |
| 横向布局 | 垂直布局 | `mode: 'horizontal'` → responsive |
| 完整表单 | 紧凑表单 | `size: 'md'` → `'sm'` |

### 移动端优先原则

- 默认使用 `mode: 'horizontal'`
- 表单项使用 `mode: 'inline'` 或 `responsive`
- 弹层使用 `size: 'md'` 或 `'sm'`
- 列表使用 `mode: 'list'` 替代 `table`

## JSON Schema 生成规范

### 必填字段清单

| 组件类型 | 必填字段 |
|---------|---------|
| Page | type, body |
| Form | type, body/controls |
| CRUD | type, api, columns |
| Dialog | type, body |
| Button | type, label/actionType |
| Form Item | type, name |

### 组件嵌套层级

```
Page
└── body: (Component | Component[])
    ├── Form
    │   └── controls: (FormItem | FormItem[])
    ├── CRUD
    │   ├── filter (可选)
    │   ├── columns: Column[]
    │   └── headerToolbar / footerToolbar
    ├── Dialog / Drawer
    │   ├── title
    │   └── body
    └── Grid / Flex
        └── columns / items
```

### API配置规范

```json
{
  "api": "/api/users",
  "api": {
    "method": "get",
    "url": "/api/users",
    "data": { "&": "$$" }
  }
}
```

支持的method: `GET`, `POST`, `PUT`, `DELETE`

### 事件动作配置模板

#### 点击提示
```json
{
  "type": "button",
  "label": "提交",
  "onEvent": {
    "click": {
      "actions": [
        {
          "actionType": "toast",
          "args": {
            "msgType": "success",
            "msg": "操作成功"
          }
        }
      ]
    }
  }
}
```

#### 点击刷新
```json
{
  "onEvent": {
    "click": {
      "actions": [
        {
          "actionType": "reload",
          "componentName": "targetCrud"
        }
      ]
    }
  }
}
```

#### 打开弹层
```json
{
  "actionType": "dialog",
  "dialog": {
    "title": "弹层标题",
    "body": { ... }
  }
}
```

#### 提交表单
```json
{
  "api": "post:/api/submit",
  "redirectTo": "/success",
  "onEvent": {
    "submitSucc": {
      "actions": [
        {
          "actionType": "toast",
          "args": { "msg": "提交成功" }
        },
        {
          "actionType": "reload",
          "componentName": "targetCrud"
        }
      ]
    }
  }
}
```

## 自动校验机制

### 校验级别

| 级别 | 说明 | 示例 |
|-----|-----|-----|
| error | 语法错误/缺失必填字段 | 缺失type、JSON语法错误 |
| warning | 建议优化项 | 建议添加loading配置 |
| info | 最佳实践提示 | 建议添加description |

### 常见错误模式

见 `rules/common-patterns.js`

### 校验函数

见 `rules/schema-validator.js`

## 预设模板使用说明

### 模板目录

```
templates/
├── login.json              # 登录页面
├── basic-crud.json        # 基础增删改查
├── filter-crud.json       # 带过滤搜索
├── search-form.json       # 搜索筛选表单
├── detail-dialog.json     # 详情查看弹层
├── edit-dialog.json       # 编辑弹层
├── select-crud.json       # 弹层选择数据
├── multi-step-wizard.json # 多步骤向导
└── dashboard.json         # 数据看板
```

### 使用方法

1. 根据业务场景选择对应模板
2. 复制模板作为起点
3. 修改API地址、字段名、列配置
4. 运行校验工具检查配置正确性

### 模板自定义要点

- **API地址**: 修改 `api` 或 `url` 字段
- **字段配置**: 修改 `columns` 中的 name/label
- **表单控件**: 修改 `controls` 中的表单项
- **按钮文字**: 修改 `label` 字段
- **弹层标题**: 修改 `title` 字段
