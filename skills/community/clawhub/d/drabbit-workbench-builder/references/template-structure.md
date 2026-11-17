# 工作台模板 — 结构解剖图

本文档标记模板 `assets/template/index.html` 中所有可定制区域。

## 模板总行数：~6400 行

## 不可改动区域（核心引擎）

以下区域是工作台的核心运行引擎，**在所有定制中保持不变**：

| 行号范围 | 内容 | 说明 |
|----------|------|------|
| 3450-3600 | `getTodayStr()`, `uid()`, `escapeHtml()` | 工具函数，永远不变 |
| 3600-4100 | `renderTop3()`, `renderTimeline()`, `renderInbox()` | 核心渲染函数，永远不变 |
| 4100-4300 | `renderAll()`, `switchTab()`, `quickAdd()` | 导航和 FAB，逻辑不变 |
| 4300-4800 | 任务 CRUD、日程 CRUD、提醒逻辑 | 业务逻辑，永远不变 |
| 4880-5170 | `getEmptyData()`, `loadStore()`, `saveStore()` | 存储层框架，结构不变 |
| 5180-5300 | `clearAllData()` | 清空逻辑，永远不变 |
| 5288-5500 | `initCloudBase()`, `syncPush()`, `syncPull()` | 同步引擎，永远不变 |
| 5500-5600 | 导入导出逻辑 | 永远不变 |
| 6250-6288 | `init()` | 初始化流程框架 |

## 可定制区域（按用户需求修改）

### 区域 A：页面元数据（行 1-14）
```
- <title> 的值 → 用户的工作台名称
- <meta name="apple-mobile-web-app-title"> → 简短名称
- <meta name="theme-color"> → 主题色（与 CSS 主色一致）
```
**修改方式**：直接替换文本

### 区域 B：CSS 变量（行 21-50）
```
- --bg-page → 背景色
- --bg-page-gradient → 背景渐变（三组 radial + linear）
- --text-primary / --text-secondary / --text-tertiary → 文字色系
- --color-{project1}, --color-{project2}, ... → 每个项目的主题色
- --color-{project1}-bg, --color-{project2}-bg, ... → 对应的背景色
```
**修改方式**：
1. 根据用户项目数量，生成对应数量的 `--color-*` 和 `--color-*-bg` 变量
2. 主题色推荐方案：
   - 1-2 个项目：蓝 + 绿
   - 3-4 个项目：蓝 + 绿 + 橙 + 紫
   - 5-6 个项目：蓝 + 绿 + 橙 + 紫 + 粉 + 青

### 区域 C：浅色主题 CSS 变量（行 1552-1574）
```
- [data-theme="light"] 下的所有 CSS 变量
- 必须与区域 B 的浅色版本配套
```
**修改方式**：根据区域 B 的深色变量生成对应的浅色版本

### 区域 D：用户顶部信息区域（行 2793-2791）
```
- <div class="greeting"> → 问候语（含用户名）
- <div class="date-display"> → 日期格式
- <div class="status-text"> → 座右铭
- <div class="streak-badge"> → 连续天数
```
**修改方式**：文本替换 + `updateHomeGreeting()` 中的问候语模板

### 区域 E：项目卡片区域（行 2856-2863）
```
- <div class="projects-grid" id="projectsGrid">
  → 由 renderProjects() 动态生成
  → renderProjects() 从 store.projects 读取数据
```
**修改方式**：
- 不需要修改 HTML
- 修改 `getEmptyData()` 中的 `projects` 数组
- 修改 `renderProjects()` 中的项目颜色映射逻辑

### 区域 F：Tab 导航栏（行 3075-3130）
```
- 5 个 tab-item（今日待办、项目、日程、收集箱、我的）
- 每个 tab 有对应的 SVG 图标
- 每个 tab 有通知红点 dot
```
**修改方式**：
- Tab 数量和顺序通常不变（5 个是固定框架）
- 如需增减，需同时修改 HTML、`switchTab()`、`renderAll()`、CSS

### 区域 G：FAB 菜单（行 3139-3165）
```
- 6 个快速操作按钮（任务、灵感、笔记、日程、新建项目、照片上传）
```
**修改方式**：根据用户需求增减 FAB 操作项

### 区域 H：profile 页面设置菜单（行 2960-3015）
```
- 数据导出、导入、导入计划、清空数据
- 编辑个人资料、通知设置、主题设置
```
**修改方式**：通常不变，但可以增减条目

### 区域 I：默认数据 getEmptyData()（行 3330-3360）
```
- userName → 用户名
- bio → 一句话介绍
- occupation → 职业
- userMotto → 座右铭
- projects 数组 → 项目列表（最关键！）
  - 每个项目：{ id, name, icon, colorClass, coverImage, subModules }
- classSchedule → 默认课表（如不需要可设为 []）
```
**修改方式**：直接修改 JS 对象字面量

### 区域 J：项目领域渲染（行 4400-4880）
```
- 每个项目的专属看板（备课、备考、学习、记账、搞事、OOTD）
- 根据用户项目数量，可能不需要全部
```
**修改方式**：
- 如果项目数 ≠ 6，需要调整 `renderProjectDetail()` 中的 switch/case
- 如果某个项目不需要专属看板，删除对应的 case 分支

### 区域 K：新功能函数（行 5740-6220）
```
- 编辑个人资料、通知设置、主题切换
- 编辑课表、月度复盘图表
- 新建项目、照片上传
```

---

## 定制流程

1. 询问用户 → 得到项目列表 + 身份信息 + 风格偏好
2. 确定项目数量 → 生成颜色方案
3. 修改 `getEmptyData()` 中的 `projects` 数组（区域 I）
4. 修改 CSS 变量（区域 B + C）
5. 修改页面元数据和顶部信息（区域 A + D）
6. 调整项目渲染逻辑（区域 J）
7. 修改 `manifest.webmanifest` 的名称
8. 设置 SW 初始版本 `workbench-v1`
9. 部署到 CloudStudio
