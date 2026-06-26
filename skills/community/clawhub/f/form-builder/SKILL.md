---
name: form-builder
description: Automated form generation from roadflow.rf_form with similarity-based copying. Use when Codex needs: (1) Generate HTML form templates based on existing similar forms, (2) Create dynamic forms via database-assisted similarity matching, (3) Implement client-side validation with real-time feedback, or (4) Generate multi-step wizard forms optimized from rf_form table in roadflow database
---

# 表单生成器 Form Builder 📜

> "致君尧舜上，再使风俗淳" —— 杜子美

本技能提供自动化表单生成、验证和管理功能。**核心特色**：与 **数据库管理员**技能协同工作，基于 `roadflow.rf_form` 表中的现有表单数据，通过相似度匹配算法（名称编辑距离+HTML 结构相似度）复制修改并保存为新表单。所有表单均遵循无障碍设计原则（WCAG 2.1）和响应式设计规范。

## 核心能力 Core Capabilities

### 🔹 HTML 表单模板生成
- **框架支持**: Bootstrap 5 / Tailwind CSS
- **输入控件**: text, email, password, tel, url, number, date, datetime-local
- **高级控件**: select (dropdown), radio, checkbox, file upload
- **布局控件**: fieldset, legend, tabpanels, collapsibles
- **富文本域**: textarea with optional rich text toolbar

### 🔹 数据库驱动的智能生成（RoadFlow 集成）⭐ NEW
- **相似度匹配算法**：基于 roadflow.rf_form 表的现有表单数据
  - `name`字段编辑距离计算（如"出差申请单"vs"请假申请单"）
  - `html`模板结构相似度（基于 HTML 标签/元素）
  - `type`类型相同则权重加倍
- **复制修改流程**：
  a. 接收新建表单需求描述
  b. 查询 roadflow.rf_form 表找到相似度最高的现有记录
  c. 读取该记录的完整内容（html, fieldsjson等）
  d. 根据新需求修改字段名、标题、字段定义等
  e. 生成新 ID，保存为新表单
- **输出格式**：
  - 相似度计算结果（top 3 匹配项）
  - 匹配到的源表单名称
  - 新生成的表单 HTML+JSON 配置

### 🔹 动态表单映射
- **JSON Schema to HTML**: 自动将 JSON Schema 转换为完整 HTML 表单
- **UI 组件库绑定**: React Hook Form / Vue Formulate / jQuery validation
- **API 端点集成**: 自动生成 submit 事件处理和错误反馈

### 🔹 客户端验证 Client-side Validation
- **实时验证**: input onchange/onblur 触发即时校验
- **错误提示**: inline error messages + visual indicators (red border, tooltip)
- **渐进式增强**: graceful degradation 当 JS 被禁用时表单仍可提交
- **自定义验证器**: 支持正则表达式和异步 API 调用验证

### 🔹 多步骤向导 Multi-step Wizards
- **步骤导航**: progress bar + step indicator
- **数据持久化**: 使用 sessionStorage/localStorage 保存已填内容
- **步骤验证**: 每步验证通过后才能进入下一步
- **返回编辑**: 支持在任何步骤返回上一步修改

### 🔹 文件上传 File Uploads
- **拖拽支持**: drag-and-drop API integration
- **预览功能**: image preview + file type detection
- **限制规则**: max size, max files, allowed extensions
- **上传处理**: progress bar + success/error handling

### 🔹 条件字段 Conditional Logic
- **显隐逻辑**: if [field] equals [value] then show/hide [target fields]
- **级联下拉**: 选择 A 后显示相关 B 选项（如城市→区县）
- **动态追加**: submit 时动态添加新字段到表单

## 数据库配置（roadflow）

- **主机**: 192.168.1.136
- **端口**: 35438
- **用户**: postgres
- **密码**: Hxkj510510
- **目标库**: roadflow

## 使用场景 Use Cases

当你需要以下功能时，请触发此技能：

- "为注册页面生成一个包含姓名、邮箱、密码的表单"
- "将 schema.json 转换为 Bootstrap 5 格式的 HTML"
- "创建一个多步骤问卷向导（基本信息→联系方式→偏好设置）"
- "基于 roadflow.rf_form 中的相似表单快速生成新表单（如：新建'员工请假申请单'，参考现有的'出差申请单'和'请假申请单'）"
- "生成带实时验证的文件上传表单"
- "根据用户角色动态显示不同字段（管理员→编辑按钮，普通用户→查看按钮）"

## 技术细节 Technical Details

本技能在幕后会使用：
- **驱动**: 原生浏览器 API + DOM manipulation + `pg` (PostgreSQL) for roadflow DB
- **框架支持**: Bootstrap 5 / Tailwind CSS (CSS-in-JS)
- **验证库**: jQuery Validation / Formik / react-hook-form
- **响应式**: mobile-first CSS with media queries
- **无障碍**: ARIA labels, keyboard navigation support
- **数据库集成**: roadflow.rf_form表相似度匹配（名称编辑距离 + HTML 结构相似度）

## 示例 Examples

### 生成 HTML 表单
```
创建一个产品注册表单：
- 产品名称（文本输入，必填）
- SKU（文本输入，最大 50 字符）
- 价格（number，最小 0，步长 0.01）
- 库存数量（number，最小 0）
- 描述（textarea，最多 2000 字）
- 上传产品图片（file，限制 jpg/png，最大 5MB）
- 提交按钮

框架：Bootstrap 5
```

### 基于 RoadFlow 现有表单生成新表单
```
根据 roadflow.rf_form 表生成新表单：
需求：新建'员工考勤管理表'
参考逻辑：查找相似度最高的现有表单（如'请假申请单'）
操作：复制其 HTML 模板，修改 name, html, fieldsjson 等字段
输出：新 ID + 完整表单内容

### 工时数据表生成案例
```
需求：新建'工时数据表'（记录员工工作时间和薪资）
相似度算法发现表中无"工时"关键词表单→判定为全新创建
CKEditor 输出特征分析：
- HTML 使用<table>布局，width:98%
- 字段顺序：工号→姓名→部门→日期→班次→工时相关字段→工资总额（只读）
- fieldsjson 字段类型：string, datetime, number, select, textarea
- 生成 ID:777082588573769（MAX(id)+1）
SQL 插入成功保存至 rf_form 表

注意：当无相似表单时，新表可全新创建而非强制复制
```

### JSON Schema 转换
```
将以下 schema 转换为 HTML:
{
  "type": "object",
  "properties": {
    "firstName": { "type": "string" },
    "lastName": { "type": "string" }
  }
}
```

### 多步骤向导
```
创建一个 3 步问卷：
第 1 步：基本信息（姓名、邮箱）
第 2 步：联系方式（电话、地址）
第 3 步：偏好设置（兴趣选项、频率选择）
每步验证通过后显示下一步
```

### 条件字段逻辑
```
当 [country] 为"美国"时显示州列表，否则显示省列表
当 [file_type] 为"image"时允许选择 jpg/png/gif，否则 pdf/doc/xlsx
```

---

*技能由杜甫（📜）编写，秉承"工欲善其事，必先利其器"的精神*
