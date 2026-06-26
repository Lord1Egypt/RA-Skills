# Project Portal 后台管理系统 - Skill 文件

## 项目概述

Project Portal 是一个基于 Vue 3 + Flask 的项目动态管理系统，具备完整的 RBAC 权限管理、多项目管理、图片上传管理和 S3 存储集成等功能。

## 核心功能模块

### 1. RBAC 权限管理系统

#### 1.1 角色管理 (Role Management)
- **功能点**：
  - 创建/编辑/删除角色
  - 角色权限分配（支持细粒度权限控制）
  - 权限包含：动态管理、分类管理、用户管理、角色管理、菜单管理、系统设置、系统日志
- **前端实现**：`frontend/src/views/admin/RoleList.vue`
- **后端 API**：`/api/roles`
- **数据库表**：`roles`（角色表）、`role_menus`（角色菜单关联表）

#### 1.2 用户管理 (User Management)
- **功能点**：
  - 用户 CRUD 操作
  - 角色分配
  - 密码重置
  - 用户状态管理（启用/禁用）
  - 用户搜索和筛选
- **前端实现**：`frontend/src/views/admin/UserList.vue`
- **后端 API**：`/api/users`
- **数据库表**：`users`（用户表）

#### 1.3 菜单管理 (Menu Management)
- **功能点**：
  - 菜单 CRUD 操作
  - 菜单权限分配（支持树形结构）
  - 菜单排序
  - 支持多级菜单
- **前端实现**：`frontend/src/views/admin/MenuList.vue`、`frontend/src/views/admin/MenuAuthModal.vue`
- **数据库表**：`menus`（菜单表）

### 2. 多项目管理系统

#### 2.1 项目管理 (Project Management)
- **功能点**：
  - 项目 CRUD 操作
  - 项目基本信息管理（名称、编码、描述、封面）
  - 项目状态管理（进行中/已结束）
  - 项目负责人分配
  - 项目起止日期管理
  - 项目看板功能（支持 iframe 嵌入外部看板）
  - 项目搜索和筛选
- **前端实现**：`frontend/src/views/admin/ProjectList.vue`、`frontend/src/views/admin/ProjectForm.vue`
- **后端 API**：`/api/projects`
- **数据库表**：`projects`（项目表）

#### 2.2 项目成员管理 (Project Members)
- **功能点**：
  - 项目成员分配
  - 成员角色权限管理（项目经理/开发人员/测试人员/普通成员）
  - 成员添加/移除
- **前端实现**：内嵌在 ProjectForm.vue 中
- **数据库表**：`project_members`（项目成员表）

### 3. 图片上传管理系统

#### 3.1 图片选择器 (Image Selector)
- **功能点**：
  - 图片库浏览（支持网格和列表两种视图）
  - 目录树导航（支持多级目录）
  - 图片搜索功能
  - 图片上传（支持拖拽上传）
  - 图片选择（支持单选）
  - 自动刷新和加载
- **前端实现**：`frontend/src/components/ImageSelector.vue`
- **组件**：`frontend/src/components/DirectoryTreeNode.vue`（目录树节点）
- **后端 API**：`/api/s3/images`

#### 3.2 富文本编辑器集成
- **功能点**：
  - 基于 wangEditor 的富文本编辑器
  - 自定义图片插入按钮
  - 附件上传功能（支持 PDF、Word、Excel）
  - 实时预览功能
- **前端实现**：`frontend/src/views/admin/NewsForm.vue`

### 4. S3 存储系统集成

#### 4.1 S3 存储服务
- **架构**：独立的 Flask 服务（端口 5050）
- **功能点**：
  - 文件上传和下载
  - 存储桶管理（创建、删除、重命名）
  - 目录管理（创建、删除）
  - 文件预览和下载
  - Web 管理界面
  - S3 兼容 API（支持 AWS SDK）
- **实现文件**：`backend/s3/s3_server.py`
- **认证模块**：`backend/s3/auth.py`
- **认证配置**：`backend/s3/auth.json`

#### 4.2 文件上传 API
- **上传接口**：`/api/upload/image`
- **功能点**：
  - 支持图片和附件上传
  - 文件大小限制（最大 20MB）
  - 支持多种格式（图片、PDF、Word、Excel）
  - 超时处理（30 秒）
  - 错误处理机制

#### 4.3 文件代理服务
- **代理接口**：`/api/s3-image/{object_key}`
- **功能**：直接代理访问 S3 存储中的文件

### 5. 动态内容管理

#### 5.1 项目动态管理 (News Management)
- **功能点**：
  - 动态 CRUD 操作
  - 富文本内容编辑
  - 封面图片设置
  - 分类管理
  - 置顶/热门标记
  - 发布时间设置
  - 所属项目管理
  - 预览功能
- **前端实现**：`frontend/src/views/admin/NewsList.vue`、`frontend/src/views/admin/NewsForm.vue`
- **后端 API**：`/api/news`
- **数据库表**：`news`（动态表）

#### 5.2 分类管理 (Category Management)
- **功能点**：
  - 分类 CRUD 操作
  - 分类使用统计
- **前端实现**：`frontend/src/views/admin/CategoryList.vue`
- **数据库表**：`categories`（分类表）

### 6. 系统管理

#### 6.1 系统设置 (Settings)
- **功能点**：
  - 网站基本信息设置（标题、描述、关键词）
  - 联系信息设置（邮箱、电话）
  - Logo 上传和设置
- **前端实现**：`frontend/src/views/admin/Settings.vue`
- **数据库表**：`settings`（设置表）

#### 6.2 系统日志 (Logs)
- **功能点**：
  - 操作日志查询
  - 登录日志查询
  - 日志详情查看
- **前端实现**：`frontend/src/views/admin/LogList.vue`
- **数据库表**：`operation_logs`（操作日志表）、`login_logs`（登录日志表）

### 7. 认证与授权

#### 7.1 登录认证
- **实现方式**：
  - Token-based 认证（Bearer Token）
  - 本地存储 Token（localStorage）
  - 路由守卫保护后台页面
- **前端实现**：`frontend/src/views/Login.vue`
- **路由守卫**：`frontend/src/router/index.js`

#### 7.2 权限控制
- **实现方式**：
  - 基于角色的访问控制（RBAC）
  - 菜单级权限控制
  - 操作权限校验
- **权限数据**：存储在 `roles` 表的 `permissions` 字段

## 技术架构

### 前端技术栈
- **框架**：Vue 3 + Vite
- **UI 组件库**：Arco Design Vue
- **路由管理**：Vue Router 4
- **富文本编辑器**：wangEditor
- **轮播组件**：Swiper
- **状态管理**：Composition API
- **构建工具**：Vite

### 后端技术栈
- **框架**：Flask 3.0.0
- **数据库**：SQLite（开发）/ MySQL（生产建议）
- **跨域支持**：Flask-CORS
- **文件存储**：S3 兼容存储服务
- **认证方式**：Token-based 认证

### S3 存储服务
- **服务类型**：独立的 Flask 应用
- **存储方式**：本地文件系统（目录结构模拟）
- **认证方式**：用户名/密码认证
- **API 兼容性**：兼容 AWS S3 API
- **管理界面**：完整的 Web UI

## 数据库设计

### 核心数据表
1. **users**：用户表（存储用户基本信息）
2. **roles**：角色表（存储角色和权限）
3. **role_menus**：角色菜单关联表
4. **menus**：菜单表（存储系统菜单）
5. **projects**：项目表（存储项目信息）
6. **project_members**：项目成员表
7. **news**：动态表（存储项目动态）
8. **categories**：分类表
9. **settings**：设置表
10. **operation_logs**：操作日志表
11. **login_logs**：登录日志表

## API 接口规范

### 通用规范
- **基础 URL**：`/api`
- **认证方式**：Bearer Token（Header: Authorization）
- **响应格式**：JSON
- **状态码**：200（成功）、400（请求错误）、401（未认证）、403（无权限）、404（不存在）、500（服务器错误）

### 主要接口分组
1. **动态管理**：`/api/news/*`
2. **分类管理**：`/api/categories/*`
3. **项目管理**：`/api/projects/*`
4. **用户管理**：`/api/users/*`
5. **角色管理**：`/api/roles/*`
6. **菜单管理**：`/api/menus/*`
7. **系统设置**：`/api/settings/*`
8. **日志管理**：`/api/logs/*`
9. **文件上传**：`/api/upload/*`
10. **S3 存储**：`/api/s3/*`

## 部署配置

### Docker 部署
- **S3 服务**：独立容器（端口 5050）
- **后端 API**：Flask 应用（端口 5002）
- **前端**：Nginx 静态服务（端口 3000）
- **数据卷**：s3_data、backend_data

### 环境变量
- **S3 配置**：S3_ENDPOINT、S3_ACCESS_KEY、S3_SECRET_KEY、S3_BUCKET
- **数据库**：DATABASE_PATH
- **前端 API**：VITE_API_BASE_URL

## 开发规范

### 代码组织
- **前端**：按功能模块组织（views、components、composables）
- **后端**：API 路由按功能分组
- **数据库**：表结构清晰，外键约束完整

### 命名规范
- **文件**：CamelCase（Vue 组件）、kebab-case（普通 JS）
- **API**：RESTful 风格
- **数据库**：小写 + 下划线分隔

### 安全规范
- **密码加密**：SHA256 加密存储
- **认证**：Token-based 认证
- **文件上传**：类型和大小限制
- **SQL 注入**：使用参数化查询

## 扩展建议

1. **存储扩展**：支持阿里云 OSS、腾讯云 COS 等云存储
2. **消息通知**：集成邮件、短信通知功能
3. **工作流**：添加审批流程
4. **数据分析**：增加数据报表和统计功能
5. **移动端**：开发移动端适配或小程序
6. **性能优化**：
   - 图片压缩和 CDN 加速
   - 数据库索引优化
   - 缓存机制（Redis）
   - 前端性能优化（代码分割、懒加载）
