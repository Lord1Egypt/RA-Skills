---
name: business-to-dev-smart
description: Smart business-to-dev requirement translator. AI first analyzes and memorizes project structure, then understands business requirements, references actual code, and generates implementation-ready developer documents. Universal - works with any tech stack.
---

# Business-to-Dev Smart

智能业务需求转研发需求文档工具。AI 自主分析项目结构，理解业务需求，参考实际代码，生成可直接执行的研发文档。

## 核心特点

- 🧠 **自主项目理解** - AI 自动探索代码库，理解项目类型和架构
- 💾 **项目记忆** - 存储项目概述和结构，后续复用
- 🎯 **需求智能分析** - 结合项目上下文理解业务需求
- 🔍 **代码精准参考** - 自动查找相关代码作为实现参考
- 📝 **生成完整文档** - 需求概述、页面原型、接口设计、任务拆分

## 工作流程

### Phase 1: 项目分析（首次使用）

当遇到新项目时，AI 会：

1. **探索项目根目录** - 识别项目类型和技术栈
2. **分析关键文件** - package.json, README, 配置文件等
3. **理解项目架构** - 目录结构、模块划分、代码组织方式
4. **存储项目记忆** - 保存项目概述和结构到 `.ai-memory/`

```
项目分析输出示例：

【项目概述】
- 项目名称：电商订单管理系统 (OMS)
- 技术栈：Vue3 + Element Plus + Java Spring Boot
- 项目类型：B端管理系统
- 主要模块：订单、库存、客户、报表

【项目结构】
frontend/
  - src/views/          # 页面：按模块组织
  - src/components/     # 公共组件
  - src/api/           # API 接口
  - src/router/        # 路由配置
backend/
  - controller/        # REST API
  - service/          # 业务逻辑
  - entity/           # 数据模型
  - mapper/           # 数据访问

【代码风格】
- 前端：Composition API, 模块化组织
- 后端：分层架构，RESTful 风格
- 命名：驼峰命名，模块前缀
```

### Phase 2: 需求分析

用户提供：
1. **业务描述**（文字）
2. **UI 截图**（可选，图片路径）

AI 会：
1. 理解业务目标和场景
2. 分析 UI 截图中的功能点
3. 结合项目上下文判断实现方式
4. 识别需要修改/新增的模块

### Phase 3: 代码参考

AI 自动在项目中查找：

1. **相似功能实现** - 查找类似页面的代码
2. **API 调用模式** - 了解前后端交互方式
3. **组件使用方式** - 查看常用 UI 组件
4. **数据模型定义** - 参考现有实体类

### Phase 4: 生成需求文档

输出包含：

```markdown
# [需求标题] 研发需求文档

## 1. 需求概述
- 业务背景：...
- 用户场景：...
- 预期效果：...

## 2. 功能需求
### 2.1 功能点列表
- [ ] 功能1：...
- [ ] 功能2：...

### 2.2 交互流程
1. 用户操作...
2. 系统响应...

## 3. 页面设计
### 3.1 页面结构（HTML 原型）
```html
<div style="border:1px solid #ccc; padding:10px;">
  <h4>页面标题</h4>
  <!-- 简单框线图 -->
</div>
```

### 3.2 关键交互
- 点击...触发...
- 选择...后...

## 4. 接口设计
### 4.1 新增/修改接口
| 接口 | 方法 | 路径 | 描述 |
|------|------|------|------|
| 接口1 | POST | /api/xxx | ... |

### 4.2 请求/响应示例
```json
{
  "code": 200,
  "data": {...}
}
```

## 5. 数据模型
### 5.1 新增/修改实体
```java
// 参考现有代码风格
public class XxxEntity {
    // 字段定义
}
```

## 6. 实现参考
### 6.1 参考代码
- 相似功能：`src/views/xxx/IndexView.vue`（第 45-78 行）
- API 调用：`src/api/xxx.js`（参考 getList 方法）
- 组件使用：参考 `components/XxxComponent.vue`

### 6.2 建议实现步骤
1. **前端**：在 `views/xxx/` 目录新增/修改...
2. **后端**：在 `controller/` 添加接口，在 `service/` 实现逻辑...
3. **数据库**：在 `entity/` 定义模型...

## 7. 开发任务
- [ ] 前端：页面开发（预计 x 小时）
- [ ] 后端：接口开发（预计 x 小时）
- [ ] 联调：前后端对接
- [ ] 测试：功能验证
```

## 使用方法

### 首次使用（项目分析）

```bash
# AI 会自动分析项目并保存记忆
kimi "帮我理解这个项目：项目路径 ~/projects/my-app"
```

### 日常需求分析

```bash
# 基础用法
kimi "分析需求：在订单列表增加批量导出功能，截图在 ~/screenshot.png"

# 完整用法
kimi "分析需求：
业务：客户希望在订单列表增加批量导出功能，可以选择时间范围和状态筛选后导出 Excel。
截图：/Users/xxx/screenshots/order_list.png
项目：~/projects/my-app"
```

## 项目记忆存储

项目分析结果存储在：
```
项目根目录/
  └── .ai-memory/
      └── project-profile.md    # 项目概述和结构
```

用户可以随时查看或更新：
```bash
# 查看项目记忆
kimi "查看这个项目的记忆"

# 更新项目记忆（代码结构变化后）
kimi "重新分析这个项目，更新记忆"
```

## 最佳实践

1. **首次使用先让 AI 理解项目** - 项目分析质量决定后续输出质量
2. **提供清晰的业务描述** - 说明用户是谁、要解决什么问题
3. **UI 截图很有用** - 帮助 AI 理解页面布局和功能点
4. **查看生成的参考代码** - 确保建议符合实际代码风格
5. **迭代优化** - 如果需求复杂，可以多次对话完善文档

## 注意事项

- AI 会尽量理解项目，但复杂项目可能需要人工补充说明
- 生成的代码参考是示意性的，需要根据实际情况调整
- 对于全新项目类型，AI 可能需要更多上下文
- 建议定期更新项目记忆（当项目结构重大变化时）
