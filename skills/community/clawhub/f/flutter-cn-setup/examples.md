# Flutter CN 示例模板

在执行本 Skill 时，可直接复用以下输出模板。

## 示例 1：全新 macOS（Android + iOS）

### 用户诉求
在中国区网络下，从 0 安装完整 Flutter 开发环境。

### 建议执行
```bash
cd .cursor/skills/flutter-cn-setup
bash scripts/bootstrap-flutter-cn.sh
bash scripts/validate-flutter-cn.sh
```

### 建议回复格式
```markdown
当前状态
- 已安装：Homebrew、Git、Flutter stable
- 已配置：中国区镜像、Flutter PATH
- 待完成：Android Studio 首次初始化、Xcode 首次启动

已执行命令
- bootstrap-flutter-cn.sh
- validate-flutter-cn.sh

阻塞问题
- Android licenses 尚未接受
- Xcode 首次启动未完成

下一步
- flutter doctor --android-licenses
- sudo xcodebuild -runFirstLaunch

最终验收
- 环境接近可用，完成上述两步后重新执行 validator。
```

## 示例 2：仅 Android 环境

### 用户诉求
只做 Android 开发，不需要 iOS。

### 建议执行
```bash
cd .cursor/skills/flutter-cn-setup
NEED_IOS=no bash scripts/bootstrap-flutter-cn.sh
NEED_IOS=no bash scripts/validate-flutter-cn.sh
```

### 建议回复格式
```markdown
当前状态
- Android toolchain 与 Flutter 已就绪
- iOS 检查按需跳过

已执行命令
- NEED_IOS=no bootstrap 脚本
- NEED_IOS=no validator 脚本

阻塞问题
- 无

下一步
- 启动模拟器并运行示例工程

最终验收
- Android 开发环境已就绪（READY）。
```

## 示例 3：已安装 Flutter，但 `doctor` 报错

### 用户诉求
在不全量重装的前提下修复现有环境。

### 建议执行
```bash
cd .cursor/skills/flutter-cn-setup
bash scripts/validate-flutter-cn.sh || true
# 先修复报告中优先级最高的 FAIL 项
bash scripts/bootstrap-flutter-cn.sh
bash scripts/validate-flutter-cn.sh
```

### 建议回复格式
```markdown
当前状态
- 检测到已有 Flutter，并已更新到 stable
- 当前 shell 配置中的镜像已修正

已执行命令
- 验收 -> 安装修复 -> 验收

阻塞问题
- iOS 依赖阶段 CocoaPods 超时

下一步
- cd ios && pod install --verbose
- 若仍超时，记录失败 host/path 后再做针对性网络策略

最终验收
- Android 已可用；iOS 仍受 CocoaPods 网络问题影响。
```

## 使用要求

对用户反馈结果时，至少包含：
- 已完成内容
- 当前阻塞项
- 最小可执行的下一条命令
