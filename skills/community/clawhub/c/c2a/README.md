# App Store Skill for OpenClaw

应用商店管理 Skill，支持通过自然语言对话来搜索、安装、卸载和查看应用。

## 功能特性

- 🔍 **搜索应用** - 按名称或关键词搜索应用商店
- 📋 **列出应用** - 查看所有已安装的应用
- 📥 **安装应用** - 从应用商店一键安装
- 📤 **卸载应用** - 卸载不需要的应用

## 快速开始

### 1. 部署到 clawhub.ai

1. 访问 https://clawhub.ai/ 并登录
2. 创建新 Skill，上传 `dist/plugin.js`
3. 设置为 Private（私有）
4. 在 OpenClaw 中搜索并添加 "App Store Skill"
5. 配置：
   ```
   1Panel 地址: http://your-server:port
   1Panel API 密钥: your-api-key
   ```

### 2. 本地开发

```bash
# 安装依赖
npm install

# 编译
npm run build

# 测试（需要先设置环境变量）
APPSTORE_BASE_URL=http://your-server:port \
APPSTORE_API_KEY=your-api-key \
node dist/cli.js list
```

## 使用示例

```
你: 看看我安装了哪些应用
AI: 📦 您已安装以下应用：
    • MySQL (ID: 62)
    • WordPress (ID: 63)

你: 搜索 Redis
AI: 🔍 找到 Redis - 高性能开源键值数据库
    是否需要安装？

你: 帮我安装 Redis
AI: 📦 正在安装 Redis...
    ✅ 安装完成！
```

## 工具列表

| 工具 | 功能 |
|------|------|
| `search_apps` | 搜索应用商店 |
| `list_installed_apps` | 列出已安装应用 |
| `get_app_detail` | 获取应用详情 |
| `install_app` | 安装应用 |
| `uninstall_app` | 卸载应用 |

## 项目结构

```
app-store-skill/
├── dist/
│   └── plugin.js       # 主入口（上传此文件）
├── src/
│   ├── client.ts       # API 客户端
│   ├── plugin.ts       # 插件入口
│   └── modules/
│       └── appstore.ts # 功能模块
├── openclaw.plugin.json # 配置
└── SKILL.md            # 使用文档
```

## License

MIT
