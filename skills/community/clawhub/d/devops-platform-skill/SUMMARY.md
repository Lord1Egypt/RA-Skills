# DevOps Platform Skill - 功能摘要

## 版本信息
- **版本**: 2.0.0
- **状态**: 生产就绪
- **基于**: OpenAPI 3.0 规范

## 核心功能模块

### 1. 📱 应用管理模块
| 功能 | 命令 | 描述 |
|------|------|------|
| 查询应用列表 | `devops-platform apps` | 查询所有应用，支持状态筛选 |
| 获取应用详情 | `devops-platform app-detail --id <ID>` | 获取指定应用的详细信息 |
| 染色环境应用 | `devops-platform staging-apps` | 查询染色环境涉及的应用 |

### 2. 🔄 迭代管理模块
| 功能 | 命令 | 描述 |
|------|------|------|
| 查询迭代列表 | `devops-platform iterations` | 查询所有研发迭代 |
| 我的迭代列表 | `devops-platform my-iterations` | 查询我的研发迭代 |
| 迭代应用列表 | `devops-platform iteration-apps --plan-id <ID>` | 查询迭代下的应用 |
| 收藏迭代 | `devops-platform favorite-iteration --plan-id <ID>` | 收藏指定迭代 |
| 取消收藏 | `devops-platform favorite-iteration --plan-id <ID> --remove` | 取消收藏迭代 |
| 收藏列表 | `devops-platform favorites` | 查询我收藏的迭代 |

### 3. 📅 发布管理模块
| 功能 | 命令 | 描述 |
|------|------|------|
| 发布窗口 | `devops-platform pub-windows` | 查询发布窗口列表 |
| 发布任务 | `devops-platform pub-tasks` | 查询发布任务列表 |
| 发布记录 | `devops-platform pub-records` | 查询发布记录列表 |

### 4. 📈 统计与工具模块
| 功能 | 命令 | 描述 |
|------|------|------|
| 平台统计 | `devops-platform stats` | 获取平台统计信息 |
| 配置管理 | `devops-platform config` | 配置API地址和Token |
| 配置状态 | `devops-platform status` | 查看当前配置 |
| 清除配置 | `devops-platform clear` | 清除所有配置 |
| 命令帮助 | `devops-platform help-all` | 显示所有命令 |

## API端点覆盖

### ✅ 已实现接口
- `/application/app/list` - 应用列表
- `/application/app/{id}` - 应用详情
- `/publish/publishplan/list` - 迭代列表
- `/publish/publishplan/myplanlist` - 我的迭代
- `/publish/publishplan/applist` - 迭代应用
- `/publish/publishplan/favorite` - 收藏迭代
- `/publish/publishplan/unfavorite` - 取消收藏
- `/publish/publishplan/myfavoritelist` - 收藏列表
- `/publish/publishplan/stagingapplist` - 染色环境应用
- `/publish/pubwindow/list` - 发布窗口
- `/publish/pubtask/list` - 发布任务
- `/publish/pubrecord/list` - 发布记录

### 🔄 待实现接口
- 更多高级查询功能
- 创建/更新操作
- 批量操作支持

## 技术特性

### 用户体验
- 🎨 **彩色输出**：使用ANSI颜色代码
- 📊 **表格展示**：清晰的数据展示
- 🔍 **调试信息**：显示请求URL和参数
- ⏱️ **超时处理**：15秒请求超时
- 🛡️ **错误处理**：详细的错误信息

### 配置管理
- 🔐 **安全存储**：Token部分隐藏显示
- 📁 **文件存储**：使用JSON配置文件
- 🔄 **配置验证**：使用前验证配置

### 代码质量
- 🏗️ **模块化设计**：易于扩展
- 📝 **完整文档**：详细的帮助信息
- 🧪 **错误处理**：全面的异常捕获
- 🔧 **工具函数**：通用的API请求函数

## 使用示例

### 典型工作流
```bash
# 1. 配置
devops-platform config --base-url https://api.example.com --token your-token

# 2. 查看统计
devops-platform stats

# 3. 查询应用
devops-platform apps --size 20

# 4. 查询迭代
devops-platform iterations

# 5. 查看迭代详情
devops-platform iteration-apps --plan-id 12345

# 6. 收藏重要迭代
devops-platform favorite-iteration --plan-id 12345
```

### 开发调试
```bash
# 查看所有命令
devops-platform help-all

# 查看配置
devops-platform status

# 测试连接
devops-platform apps --size 1
```

## 安装与部署

### 作为CLI工具
```bash
npm install -g .
```

### 作为OpenClaw Skill
```bash
cp -r devops-platform-skill /opt/homebrew/lib/node_modules/openclaw/skills/
```

## 依赖项
- `axios` ^1.13.6 - HTTP客户端
- `commander` ^11.1.0 - 命令行界面
- `inquirer` ^9.3.8 - 交互式提示

## 许可证
MIT License