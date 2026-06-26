# DevOps Platform Skill

一个用于访问DevOps效能平台的OpenClaw skill，提供完整的DevOps平台API访问功能。

## 功能特性

- ✅ **配置管理**：保存API地址和Token
- ✅ **应用管理**：查询应用列表、获取应用详情
- ✅ **迭代管理**：研发迭代查询、收藏管理
- ✅ **发布管理**：发布窗口、任务、记录查询
- ✅ **统计信息**：平台数据概览
- ✅ **友好的命令行界面**：彩色输出、表格展示
- ✅ **错误处理**：详细的错误信息和调试信息
- ✅ **基于OpenAPI**：完整的API文档支持

## 安装

### 方法一：作为OpenClaw skill安装
```bash
# 将skill目录复制到OpenClaw skills目录
cp -r devops-platform-skill /opt/homebrew/lib/node_modules/openclaw/skills/
```

### 方法二：作为独立CLI工具安装
```bash
cd devops-platform-skill
npm install -g .
```

## 快速开始

### 1. 配置API地址和Token
```bash
devops-platform config
```
或直接指定：
```bash
devops-platform config --base-url https://your-api.example.com --token your-open-token
```

### 2. 查看配置状态
```bash
devops-platform status
```

### 3. 查看所有可用命令
```bash
devops-platform help-all
```

## 核心功能

### 📱 应用管理
```bash
# 查询所有应用
devops-platform apps --size 50

# 获取应用详细信息
devops-platform app-detail --id 10907

# 查询在线运行的应用
devops-platform apps --status ONLINE_RUN
```

### 🔄 迭代管理
```bash
# 查询所有研发迭代
devops-platform iterations

# 查询我的迭代
devops-platform my-iterations

# 查询迭代下的应用
devops-platform iteration-apps --plan-id 12345

# 收藏迭代
devops-platform favorite-iteration --plan-id 12345

# 查看收藏的迭代
devops-platform favorites
```

### 📅 发布管理
```bash
# 查询发布窗口
devops-platform pub-windows

# 查询发布任务
devops-platform pub-tasks --plan-id 12345

# 查询发布记录
devops-platform pub-records --task-id 67890

# 查询染色环境应用
devops-platform staging-apps
```

### 📈 统计信息
```bash
# 查看平台统计
devops-platform stats
```

## API接口说明

基于OpenAPI 3.0规范，支持完整的DevOps平台API：

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

## 响应格式

接口返回标准格式的响应：
```json
{
  "code": 200,
  "msg": "成功",
  "total": 100,
  "rows": [
    {
      "id": "123",
      "name": "示例应用",
      // ... 其他字段
    }
  ]
}
```

## 错误处理

- **配置缺失**：提示用户先进行配置
- **网络错误**：显示详细错误信息和状态码
- **API错误**：显示错误消息和响应数据
- **超时处理**：15秒超时设置
- **调试信息**：显示请求URL和参数

## 开发

### 项目结构
```
devops-platform-skill/
├── SKILL.md                 # Skill说明文档
├── package.json            # 项目配置
├── README.md              # 用户文档
├── INSTALL.md             # 安装说明
├── SUMMARY.md             # 功能摘要
└── bin/
    ├── devops-platform-enhanced.js  # 增强版主程序
    └── devops-platform-simple.js    # 简单版主程序
```

### 技术栈
- **Commander.js** - 命令行界面
- **Axios** - HTTP客户端
- **Inquirer.js** - 交互式提示

### 添加新功能
1. 在 `bin/devops-platform-enhanced.js` 中添加新的命令
2. 更新 `SKILL.md` 文档
3. 测试功能
4. 更新 `README.md`

## 许可证

MIT