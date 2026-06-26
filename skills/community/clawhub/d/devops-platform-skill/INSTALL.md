# 安装和使用指南

## 作为OpenClaw Skill安装

### 方法一：复制到Skills目录
```bash
# 复制skill到OpenClaw skills目录
sudo cp -r devops-platform-skill /opt/homebrew/lib/node_modules/openclaw/skills/
```

### 方法二：使用clawhub发布（推荐）
```bash
# 1. 安装clawhub CLI
npm install -g clawhub

# 2. 登录（如果需要）
clawhub login

# 3. 发布skill
clawhub publish devops-platform-skill

# 4. 在其他机器上安装
clawhub install devops-platform-skill
```

## 作为独立CLI工具安装

### 1. 安装依赖
```bash
cd devops-platform-skill
npm install
```

### 2. 全局安装
```bash
npm install -g .
```

### 3. 验证安装
```bash
devops-platform --version
devops-platform --help
```

## 快速开始

### 1. 配置API地址和Token
```bash
# 交互式配置
devops-platform config

# 或直接指定
devops-platform config --base-url https://your-devops-api.example.com --token your-open-token-here
```

### 2. 查看配置状态
```bash
devops-platform status
```

### 3. 获取研发迭代列表
```bash
# 使用默认参数
devops-platform iterations

# 自定义分页
devops-platform iterations --page 2 --size 50

# 自定义搜索条件
devops-platform iterations --search "pub_stage < 5"
```

### 4. 获取应用列表
```bash
# 使用默认参数
devops-platform apps

# 自定义分页
devops-platform apps --page 1 --size 20

# 筛选特定状态的应用
devops-platform apps --status "ONLINE_RUN,CODING"
```

## 在OpenClaw中使用

一旦安装为skill，你可以在OpenClaw中直接使用：

```
# 配置DevOps平台
配置devops平台，地址是 https://api.devops.com，token是 abc123

# 查看迭代列表
获取研发迭代列表

# 查看应用列表
获取应用列表，第一页，每页15个
```

## 配置存储

配置信息存储在本地：
- **macOS/Linux**: `~/.config/configstore/devops-platform.json`
- **Windows**: `%APPDATA%\configstore\devops-platform.json`

文件内容示例：
```json
{
  "baseUrl": "https://your-api.example.com",
  "token": "your-open-token-here"
}
```

## 故障排除

### 1. 命令未找到
```bash
# 确保已全局安装
npm list -g | grep devops-platform

# 或使用本地路径
node ./bin/devops-platform.js --help
```

### 2. 依赖安装失败
```bash
# 清理node_modules重新安装
rm -rf node_modules package-lock.json
npm install
```

### 3. API请求失败
- 检查网络连接
- 验证API地址是否正确
- 确认Token是否有权限
- 查看错误信息中的状态码和响应

### 4. 权限问题
```bash
# 如果遇到权限错误
sudo chmod +x bin/devops-platform.js
```

## 开发说明

### 项目结构
```
devops-platform-skill/
├── SKILL.md          # Skill文档（OpenClaw使用）
├── package.json      # npm配置
├── README.md         # 用户文档
├── INSTALL.md        # 安装指南（本文件）
├── bin/
│   └── devops-platform.js  # 主程序
└── test.js           # 测试脚本
```

### 添加新功能
1. 在 `bin/devops-platform.js` 中添加新命令
2. 更新 `SKILL.md` 文档
3. 测试功能
4. 更新版本号：`npm version patch`

### 发布更新
```bash
# 更新版本
npm version patch

# 重新发布到clawhub
clawhub publish devops-platform-skill
```

## 支持的状态值

### 应用状态 (appStatus)
- `ONLINE_RUN`: 在线运行
- `OFFLINE_RUN`: 离线运行
- `APPLYING`: 申请中
- `CODING`: 编码中

### 搜索条件 (searchValue)
- `pub_stage < 8`: 发布阶段小于8
- 可根据实际API支持调整