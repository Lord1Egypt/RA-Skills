# Android Stack Analyzer - 安装指南

## 系统要求

### Windows
- Windows 10/11
- 已安装Android SDK Platform Tools
- ADB已添加到系统PATH环境变量

### macOS
- macOS 10.12 或更高版本
- 已安装Android SDK Platform Tools
- ADB已添加到系统PATH环境变量

### Linux
- Ubuntu 18.04+ 或其他主流Linux发行版
- 已安装Android SDK Platform Tools
- ADB已添加到系统PATH环境变量

## 安装步骤

### 1. 下载技能文件
将整个 `android-stack-analyzer` 文件夹复制到以下目录：

**Windows:**
```
C:\Users\<用户名>\AppData\Roaming\LobsterAI\SKILLs\android-stack-analyzer
```

**macOS:**
```
~/Library/Application Support/LobsterAI/SKILLs/android-stack-analyzer
```

**Linux:**
```
~/.config/LobsterAI/SKILLs/android-stack-analyzer
```

### 2. 验证安装
检查文件结构是否完整：
```
android-stack-analyzer/
├── SKILL.md              # 技能主文件
├── README.md             # 说明文档
├── INSTALL.md            # 安装指南
└── examples/             # 示例脚本
    ├── cross-platform-check.bat    # Windows快速检查
    ├── cross-platform-check.sh      # Linux/macOS快速检查
    ├── cross-platform-monitor.bat   # Windows实时监控
    ├── cross-platform-monitor.sh     # Linux/macOS实时监控
    ├── quick-check.sh               # Linux/macOS快速检查
    └── monitor-page.sh              # Linux/macOS实时监控
```

### 3. 配置ADB环境

#### Windows
1. 下载Android SDK Platform Tools
2. 解压到 `C:\AndroidSDK\platform-tools`
3. 添加到系统PATH：
   - 右键"此电脑" → "属性" → "高级系统设置" → "环境变量"
   - 在"系统变量"中找到Path，添加 `C:\AndroidSDK\platform-tools`

#### macOS/Linux
1. 下载Android SDK Platform Tools
2. 解压到 `~/AndroidSDK/platform-tools`
3. 添加到PATH：
```bash
echo 'export PATH=$PATH:~/AndroidSDK/platform-tools' >> ~/.bashrc
source ~/.bashrc
```

### 4. 验证ADB安装
打开终端/命令提示符，运行：
```bash
adb version
```
应该显示ADB版本信息。

### 5. 连接Android设备
1. 开启手机的开发者选项和USB调试
2. 使用USB连接手机到电脑
3. 在手机上授权电脑连接
4. 验证连接：
```bash
adb devices
```

## 使用方法

### 基本使用
1. 重启LobsterAI
2. 在对话中提及以下关键词激活技能：
   - "安卓页面栈分析"
   - "查看页面栈"
   - "adb命令"
   - "当前页面"

### 使用示例脚本

#### 快速检查
**Windows:**
```cmd
cd examples
cross-platform-check.bat
```

**Linux/macOS:**
```bash
cd examples
chmod +x cross-platform-check.sh
./cross-platform-check.sh
```

#### 实时监控
**Windows:**
```cmd
cd examples
cross-platform-monitor.bat
```

**Linux/macOS:**
```bash
cd examples
chmod +x cross-platform-monitor.sh
./cross-platform-monitor.sh
```

## 故障排除

### 常见问题

#### 1. ADB命令未找到
- 确保Android SDK已正确安装
- 检查PATH环境变量是否包含ADB路径
- 重启终端/命令提示符

#### 2. 设备未连接
- 检查USB线是否正常连接
- 确认手机已开启USB调试
- 尝试重新连接设备
- 检查手机是否授权电脑连接

#### 3. 权限问题
- 某些设备可能需要root权限
- 尝试使用不同的ADB命令
- 检查手机安全设置

#### 4. 命令兼容性问题
- 不同Android版本命令输出可能不同
- 某些设备可能禁用了某些dumpsys命令
- 可以先查看原始输出再手动查找

### 调试命令
```bash
# 查看ADB版本
adb version

# 列出连接的设备
adb devices

# 查看设备信息
adb shell getprop

# 查看系统日志
adb logcat
```

## 更新技能
技能文件会不定期更新，请定期检查最新版本。

## 技术支持
如果遇到问题，请：
1. 检查安装步骤是否正确
2. 验证ADB环境配置
3. 查看错误日志
4. 尝试重新安装技能