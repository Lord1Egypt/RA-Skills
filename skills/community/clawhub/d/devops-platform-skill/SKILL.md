# DevOps Platform Skill

管理DevOps效能平台，提供完整的DevOps平台API访问功能。

## 配置

使用前需要配置：
1. 后端接口地址
2. 用户的Open Token

## 功能

### 📊 应用管理
- 查询应用列表
- 获取应用详细信息
- 按状态筛选应用

### 🔄 迭代管理
- 查询研发迭代列表
- 查询我的研发迭代列表
- 查询迭代下的应用列表
- 收藏/取消收藏迭代
- 查询收藏的迭代列表

### 📅 发布管理
- 查询发布窗口列表
- 查询发布任务列表
- 查询发布记录列表
- 查询染色环境应用列表

### 📈 统计信息
- 平台统计信息概览

## 使用方法

### 初始化配置
```bash
devops-platform config --base-url <后端地址> --token <用户token>
```

### 查看配置状态
```bash
devops-platform status
```

### 应用相关命令
```bash
# 查询应用列表
devops-platform apps [--page <页码>] [--size <每页大小>] [--status <状态>]

# 获取应用详细信息
devops-platform app-detail --id <应用ID>

# 查询染色环境应用列表
devops-platform staging-apps [--page <页码>] [--size <每页大小>]
```

### 迭代相关命令
```bash
# 查询研发迭代列表
devops-platform iterations [--page <页码>] [--size <每页大小>] [--search <搜索词>] [--status <状态>]

# 查询我的研发迭代列表
devops-platform my-iterations [--page <页码>] [--size <每页大小>]

# 查询迭代下的应用列表
devops-platform iteration-apps --plan-id <迭代ID> [--page <页码>] [--size <每页大小>]

# 收藏迭代
devops-platform favorite-iteration --plan-id <迭代ID>

# 取消收藏迭代
devops-platform favorite-iteration --plan-id <迭代ID> --remove

# 查询收藏的迭代列表
devops-platform favorites [--page <页码>] [--size <每页大小>]
```

### 发布相关命令
```bash
# 查询发布窗口列表
devops-platform pub-windows [--page <页码>] [--size <每页大小>] [--status <状态>] [--window-date <日期>]

# 查询发布任务列表
devops-platform pub-tasks [--page <页码>] [--size <每页大小>] [--plan-id <迭代ID>] [--status <状态>]

# 查询发布记录列表
devops-platform pub-records [--page <页码>] [--size <每页大小>] [--task-id <任务ID>] [--status <状态>]
```

### 统计信息
```bash
# 获取平台统计信息
devops-platform stats
```

### 帮助信息
```bash
# 显示所有命令
devops-platform help-all
```

## API 详情

基于OpenAPI 3.0规范，支持以下接口：

### 应用管理接口
- `GET /application/app/list` - 查询应用列表
- `GET /application/app/{id}` - 获取应用详细信息

### 迭代管理接口
- `GET /publish/publishplan/list` - 查询研发迭代列表
- `GET /publish/publishplan/myplanlist` - 查询我的研发迭代列表
- `GET /publish/publishplan/applist` - 查询迭代下应用列表
- `POST /publish/publishplan/favorite` - 收藏迭代
- `POST /publish/publishplan/unfavorite` - 取消收藏迭代
- `GET /publish/publishplan/myfavoritelist` - 查询收藏的迭代列表
- `GET /publish/publishplan/stagingapplist` - 查询染色环境应用列表

### 发布管理接口
- `GET /publish/pubwindow/list` - 查询发布窗口列表
- `GET /publish/pubtask/list` - 查询发布任务列表
- `GET /publish/pubrecord/list` - 查询发布记录列表

## 请求头
所有接口都需要以下请求头：
- `authorization: Bearer {用户token}`
- `from: openapi`
- `content-type: application/json`

## 错误处理
- 配置缺失时会提示用户先进行配置
- 网络错误会显示详细错误信息
- API错误会显示状态码和响应数据
- 支持超时设置（15秒）