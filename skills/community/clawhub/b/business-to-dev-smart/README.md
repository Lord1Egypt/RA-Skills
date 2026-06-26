# Business-to-Dev Smart

智能业务需求转研发需求文档工具。

## 理念

**AI 先理解项目，再理解需求，最后写文档。**

传统的需求文档工具需要人工指定项目结构、技术栈。
这个工具让 AI 自主探索代码库，像资深工程师一样理解项目，
然后结合业务需求，参考实际代码，生成可执行的研发文档。

## 特点

- 🧠 **自主理解** - AI 自动分析项目类型、技术栈、架构
- 💾 **项目记忆** - 一次分析，多次使用
- 🔍 **精准参考** - 自动查找相关代码作为实现参考
- 🌐 **完全通用** - 支持任何技术栈，不限定任何框架

## 快速开始

### Step 1: 让 AI 理解你的项目（只需一次）

```bash
kimi "帮我理解这个项目：~/projects/my-oms-system"
```

AI 会自动：
1. 探索项目目录结构
2. 分析技术栈和框架
3. 理解代码组织方式
4. 保存项目记忆到 `.ai-memory/project-profile.md`

### Step 2: 分析业务需求

```bash
kimi "分析需求：
业务：客户希望在订单列表增加批量导出功能
截图：~/screenshots/order-export.png"
```

AI 会：
1. 读取项目记忆
2. 理解业务需求和 UI 截图
3. 在项目中查找相似实现
4. 生成完整的需求文档

## 输出示例

### Phase 1: 项目分析输出

```
【项目理解完成】

项目类型：B端订单管理系统 (OMS)
技术栈：Vue3 + Element Plus + Java Spring Boot
主要模块：订单管理、库存管理、客户管理、报表统计

代码组织：
- 前端按模块划分页面，使用 Composition API
- 后端分层架构：Controller-Service-Mapper-Entity
- API 风格：RESTful，统一返回格式

项目记忆已保存到 .ai-memory/project-profile.md
```

### Phase 2: 需求分析输出

```markdown
# 订单批量导出 研发需求文档

## 1. 需求概述
客户需要在订单列表页面增加批量导出功能...

## 6. 实现参考
基于项目代码库分析：

**参考现有实现：**
- 列表页面：`src/views/order/IndexView.vue`（第 45-120 行）
  - 使用 `el-table` 展示数据
  - 已有选择框功能（`@selection-change`）
  - 工具栏按钮组织方式

- API 调用模式：`src/api/order.js`
  - 参考 `getOrderList()` 方法（第 12-28 行）
  - 统一使用 `createAxios` 封装

- 导出功能参考：`src/utils/exportUtil.js`
  - 已有 `exportExcel()` 工具函数
  - 使用 `Blob` 处理文件下载

**建议实现：**
1. 前端：在 IndexView.vue 工具栏添加"批量导出"按钮
2. 后端：在 OrderController 添加 `POST /api/order/export` 接口
3. 复用现有的表格选择功能和导出工具
```

## 技术无关性

这个工具不依赖任何特定技术：

| 你的项目 | AI 能理解 |
|---------|----------|
| React + Node.js | ✅ |
| Vue + Python Django | ✅ |
| Angular + Go | ✅ |
| 小程序 + Java | ✅ |
| 甚至混合项目 | ✅ |

AI 通过分析代码文件、目录结构、命名规范自主理解项目。

## 项目记忆

首次分析后，项目信息存储在 `.ai-memory/project-profile.md`：

```markdown
# Project Profile: my-oms-system

## Overview
- Type: B端管理系统
- Stack: Vue3 + Java Spring Boot
- Patterns: RESTful API, Modular structure

## Structure
frontend/src/
  - views/      # Module-based pages
  - components/ # Shared components
  - api/       # API clients
  
backend/src/
  - controller/ # REST endpoints
  - service/    # Business logic
  - entity/     # Data models

## Key Patterns
- API: createAxios wrapper
- Table: el-table with pagination
- Forms: el-form validation
```

## 对比

| 特性 | 传统工具 | Business-to-Dev Smart |
|------|---------|----------------------|
| 项目配置 | 手动指定路径 | AI 自动探索 |
| 技术栈 | 预设模板 | 自动识别 |
| 代码参考 | 人工查找 | AI 自动匹配 |
| 适用性 | 特定框架 | 完全通用 |

## License

MIT
