# amis-json-skills

百度amis低代码框架JSON Schema生成专家。精准理解业务意图，生成正确、交互友好的amis配置，支持复杂交互（点击、回调、重载、弹层），兼容移动端。

<p align="center">
  <a href="https://github.com/baidu/amis">
    <img src="https://img.shields.io/badge/amis-6.12+-blue.svg" alt="amis version">
  </a>
  <a href="https://opensource.org/licenses/Apache-2.0">
    <img src="https://img.shields.io/badge/License-Apache%202.0-green.svg" alt="License">
  </a>
</p>

---

## 功能特性

- **智能意图理解** - 根据业务场景自动匹配最佳组件方案
- **9+ 预设模板** - 覆盖常见CRUD、表单、弹层、向导等场景
- **自动校验** - JSON Schema 语法检查、错误警告、优化建议
- **移动端适配** - 内置响应式配置规范，兼容多端
- **复杂交互** - 支持点击、回调用、弹层、重载等事件动作

---

## 快速开始

### 在 OpenCode 中使用

#### 方式一：加载Skill（推荐）

在对话中直接加载：

```
@amis-json-skills
```

或描述需求自动触发：

```
帮我生成一个用户管理页面
需要一个带搜索的CRUD
创建一个登录表单
```

#### 方式二：手动引用模板

模板位于：`~/.claude/skills/amis-json-skills/templates/`

```bash
# 查看可用模板
ls ~/.claude/skills/amis-json-skills/templates/
```

复制模板到你的项目：

```bash
cp ~/.claude/skills/amis-json-skills/templates/basic-crud.json ./my-crud.json
```

---

### 在 Claude Code 中使用

#### 方式一：通过 /skill 命令

```bash
# 加载 skill
/skill load amis-json-skills

# 或在对话中直接使用
```

#### 方式二：引用模板文件

```bash
# 列出模板
ls ~/.claude/skills/amis-json-skills/templates/

# 读取模板
cat ~/.claude/skills/amis-json-skills/templates/basic-crud.json
```

#### 方式三：对话中触发

直接描述需求：

```
创建一个订单管理页面，需要有搜索筛选功能
```

---

### 在 Antigravity 中使用

Antigravity 通过MCP（Model Context Protocol）集成，可以自动加载skill。

```python
# 在 Antigravity 配置中启用 skill
{
  "skills": ["amis-json-skills"]
}
```

或运行时加载：

```
@amis-json-skills 帮我生成一个商品列表页面
```

---

## 模板清单

| 模板文件                 | 适用场景         | 核心组件            |
| ------------------------ | ---------------- | ------------------- |
| `login.json`             | 用户登录页面     | Form                |
| `basic-crud.json`        | 基础增删改查列表 | CRUD + Dialog       |
| `filter-crud.json`       | 带条件搜索的CRUD | CRUD + filter       |
| `search-form.json`       | 独立搜索筛选表单 | Form + target       |
| `detail-dialog.json`     | 查看详情弹层     | Dialog + static     |
| `edit-dialog.json`       | 编辑数据弹层     | Dialog + Form       |
| `select-crud.json`       | 弹层中选择数据   | Dialog + CRUD       |
| `multi-step-wizard.json` | 多步骤流程向导   | Wizard              |
| `dashboard.json`         | 数据看板         | Page + Chart + Card |

---

## 意图理解与组件映射

### 场景 → 组件

| 业务场景     | amis组件            | 关键配置               |
| ------------ | ------------------- | ---------------------- |
| 数据列表展示 | CRUD                | api, columns, filter   |
| 表单提交     | Form                | api, controls, rules   |
| 详情查看     | Dialog/Drawer       | title, body, actions   |
| 搜索筛选     | Form (filter)       | submitOnChange, target |
| 批量操作     | Button + actionType | ajax, reload           |
| 页面跳转     | Button + actionType | url, link              |
| 状态提示     | Button + actionType | toast, confirm         |
| 多步骤流程   | Wizard              | steps, source          |

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

---

## 移动端适配规范

### 响应式配置

| 桌面端   | 移动端   | 配置方式                          |
| -------- | -------- | --------------------------------- |
| 3列      | 1列      | `columnCount` + `responsive`      |
| 横向布局 | 垂直布局 | `mode: 'horizontal'` → responsive |
| 完整表单 | 紧凑表单 | `size: 'md'` → `'sm'`             |

### 移动端优先原则

- 默认使用 `mode: 'horizontal'`
- 表单项使用 `mode: 'inline'` 或 `responsive`
- 弹层使用 `size: 'md'` 或 `'sm'`
- 列表使用 `mode: 'list'` 替代 `table`

---

## JSON Schema 生成规范

### 必填字段

| 组件类型  | 必填字段               |
| --------- | ---------------------- |
| Page      | type, body             |
| Form      | type, body/controls    |
| CRUD      | type, api, columns     |
| Dialog    | type, body             |
| Button    | type, label/actionType |
| Form Item | type, name             |

### API 配置

```json
{
  "api": "/api/users"
}
```

或详细配置：

```json
{
  "api": {
    "method": "get",
    "url": "/api/users",
    "data": { "&": "$$" }
  }
}
```

支持的 method: `GET`, `POST`, `PUT`, `DELETE`

### 事件动作配置

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

---

## 自动校验

### 校验级别

| 级别    | 说明                  | 示例                   |
| ------- | --------------------- | ---------------------- |
| error   | 语法错误/缺失必填字段 | 缺失type、JSON语法错误 |
| warning | 建议优化项            | 建议添加loading配置    |
| info    | 最佳实践提示          | 建议添加description    |

### 校验规则

- JSON 语法完整性
- 必填字段检查 (type, name, api, columns等)
- 组件层级结构
- API 配置规范
- 事件动作配置

### 使用校验

```javascript
const { validateAmisSchema } = require("./rules/schema-validator.js");

const schema = {
  /* 你的 amis 配置 */
};
const result = validateAmisSchema(schema);

console.log(result.errors); // 错误列表
console.log(result.warnings); // 警告列表
console.log(result.suggestions); // 建议列表
```

---

## 示例

### 订单管理页面

输入：

```
帮我生成一个订单管理页面，需要有搜索筛选功能，包括订单号、客户姓名、订单状态、支付状态和下单日期
```

输出：`examples/order-management.json`

---

### 更多示例

更多业务场景示例持续添加中...

---

## 目录结构

```
amis-json-skills/
├── README.md                     # 本文件
├── examples/                     # 业务示例
│   └── order-management.json    # 订单管理页面
├── templates/                    # 预设模板 (位于 ~/.claude/skills/amis-json-skills/templates/)
│   ├── login.json
│   ├── basic-crud.json
│   ├── filter-crud.json
│   ├── search-form.json
│   ├── detail-dialog.json
│   ├── edit-dialog.json
│   ├── select-crud.json
│   ├── multi-step-wizard.json
│   └── dashboard.json
├── rules/                        # 校验规则 (位于 ~/.claude/skills/amis-json-skills/rules/)
│   ├── schema-validator.js
│   └── common-patterns.js
└── SKILL.md                      # Skill 说明 (位于 ~/.claude/skills/amis-json-skills/)
```

---

## 相关链接

- [amis 官方文档](https://baidu.github.io/amis/zh-CN/docs/index)
- [amis GitHub](https://github.com/baidu/amis)
- [amis Editor 在线编辑器](https://aisuda.github.io/amis-editor-demo/)

---

## License

Apache License 2.0
