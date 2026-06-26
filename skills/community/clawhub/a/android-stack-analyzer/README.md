# Android Stack Analyzer

一个用于分析安卓设备页面栈的技能工具，支持Windows、Linux和macOS平台。

## 🌟 主要功能

- 🔍 快速查看当前页面
- 📊 分析完整页面栈结构
- 🔧 支持多种ADB命令
- 🌍 跨平台兼容（Windows/Linux/macOS）
- 📱 支持不同Android版本
- 🚀 实时监控功能
- 📋 自动化脚本

## 🚀 快速开始

### Windows用户
```cmd
# 运行快速启动脚本
quick-start.bat

# 或直接运行检查脚本
examples\cross-platform-check.bat

# 实时监控
examples\cross-platform-monitor.bat
```

### Linux/macOS用户
```bash
# 给脚本执行权限
chmod +x quick-start.sh
chmod +x examples/*.sh

# 运行快速启动脚本
./quick-start.sh

# 或直接运行检查脚本
./examples/cross-platform-check.sh

# 实时监控
./examples/cross-platform-monitor.sh
```

## 📦 安装方法

1. 将整个 `android-stack-analyzer` 文件夹复制到 LobsterAI 的 SKILLs 目录中
2. 重启 LobsterAI
3. 在对话中提及 "安卓页面栈分析"、"查看页面栈" 或 "adb 命令" 即可激活此技能

### 详细安装步骤
请参考 [INSTALL.md](./INSTALL.md)

## 📖 使用示例

```
用户: 帮我看看当前安卓手机最上层的页面是什么
技能: 执行跨平台ADB命令查看当前页面...

用户: 查看完整的 Activity 页面栈
技能: 执行跨平台ADB命令分析页面栈...

用户: 实时监控页面切换
技能: 执行跨平台实时监控命令...
```

## 📁 文件结构

```
android-stack-analyzer/
├── SKILL.md              # 技能主文件
├── README.md             # 说明文档
├── INSTALL.md            # 安装指南
├── quick-start.bat       # Windows快速启动
├── quick-start.sh        # Linux/macOS快速启动
└── examples/             # 示例脚本
    ├── cross-platform-check.bat    # Windows快速检查
    ├── cross-platform-check.sh      # Linux/macOS快速检查
    ├── cross-platform-monitor.bat   # Windows实时监控
    ├── cross-platform-monitor.sh     # Linux/macOS实时监控
    ├── quick-check.sh               # Linux/macOS快速检查
    └── monitor-page.sh              # Linux/macOS实时监控
```

## 🔧 支持的命令

### 基础命令
- 查看当前最上层页面
- 查看完整Activity页面栈
- 查看页面栈中的Fragment
- 查看Activity任务栈树形结构
- 查看最近任务列表
- 实时监控当前页面切换
- 查看Activity生命周期状态

### 高级命令
- 查看特定包名的详细Activity信息
- 查看所有运行中的进程及对应的Activity
- 查看Back Stack详细信息

## 🌍 平台兼容性

| 平台 | 支持状态 | 特殊说明 |
|------|----------|----------|
| Windows | ✅ 完全支持 | 使用 `findstr` 命令 |
| macOS | ✅ 完全支持 | 使用 `grep` 命令 |
| Linux | ✅ 完全支持 | 使用 `grep` 命令 |

## 📱 Android版本支持

- Android 5.0+ (Lollipop)
- Android 6.0+ (Marshmallow)
- Android 7.0+ (Nougat)
- Android 8.0+ (Oreo)
- Android 9.0+ (Pie)
- Android 10+ (Q)
- Android 11+ (R)
- Android 12+ (S)
- Android 13+ (Tiramisu)

## 🛠️ 环境要求

### 必需组件
- Android SDK Platform Tools
- ADB已添加到系统PATH
- 已连接的Android设备

### 可选组件
- 开发者选项
- USB调试权限

## 📋 使用流程

1. 安装Android SDK Platform Tools
2. 配置ADB环境变量
3. 连接Android设备
4. 运行快速启动脚本
5. 根据需要使用各种ADB命令

## ⚠️ 注意事项

1. 确保设备已开启USB调试模式
2. 某些设备可能需要授权ADB连接
3. 系统应用信息可能需要root权限
4. 不同Android版本输出格式可能不同
5. 部分设备可能禁用了某些dumpsys命令

## 🔄 更新日志

### v1.0.0 - 初始版本
- 基础页面栈分析功能
- 支持Windows/Linux/macOS

### v1.1.0 - 跨平台支持
- 添加跨平台兼容性支持
- 创建Windows和Linux/macOS专用脚本
- 添加快速启动脚本

### v1.2.0 - 功能增强
- 添加实时监控功能
- 添加自动化脚本
- 添加详细安装指南

## 📞 技术支持

如果遇到问题，请：
1. 检查安装步骤是否正确
2. 验证ADB环境配置
3. 查看错误日志
4. 尝试重新安装技能

## 📄 许可证

MIT License - 可以自由使用和分发

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个技能！