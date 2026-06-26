---
name: flutter-cn-setup
description: 为中国区开发者在新电脑上搭建完整 Flutter 开发环境，覆盖 Android/iOS toolchain、镜像配置、诊断和验收。用户提到安装 Flutter、中国区镜像、修复 flutter doctor、或新 macOS 初始化 Flutter 环境时使用。
---

# Flutter CN 环境安装

## 快速开始

大多数场景直接执行：

```bash
cd .cursor/skills/flutter-cn-setup
bash scripts/bootstrap-flutter-cn.sh
bash scripts/validate-flutter-cn.sh
```

仅 Android 快速路径：

```bash
cd .cursor/skills/flutter-cn-setup
NEED_IOS=no bash scripts/bootstrap-flutter-cn.sh
NEED_IOS=no bash scripts/validate-flutter-cn.sh
```

## 适用范围

本 Skill 用于在中国区网络下，为 **全新 macOS 设备**搭建完整 Flutter 环境。

目标结果：
- Flutter SDK 已安装并加入 `PATH`
- Flutter 与 Dart 包下载镜像已配置
- Android toolchain 可用（Android Studio + SDK + licenses）
- iOS toolchain 可用（Xcode + CocoaPods，按需）
- `flutter doctor` 达到可日常开发状态

## 快速诊断

1. 确认系统与芯片架构：
   - `uname -m`（期望 `arm64` 或 `x86_64`）
   - `sw_vers`
2. 检查 Homebrew 是否存在：
   - `brew --version`
3. 检查当前 Flutter 状态：
   - `which flutter`
   - `flutter --version`
   - `flutter doctor -v`
4. 若已安装 Flutter，优先 **修复/升级**，除非用户明确要求全量重装。

## 中国区镜像配置

下载依赖前先配置：

```bash
export PUB_HOSTED_URL=https://pub.flutter-io.cn
export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
```

持久化到 shell 配置（zsh 默认 `~/.zshrc`）：

```bash
cat <<'EOF' >> ~/.zshrc
# Flutter 中国区镜像
export PUB_HOSTED_URL=https://pub.flutter-io.cn
export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
EOF
source ~/.zshrc
```

如果镜像不稳定，先和用户确认替代方案再切换 URL。

## 安装流程（macOS）

可复制以下清单跟踪进度：

```text
Flutter CN 安装进度
- [ ] 1) 安装基础工具（git、curl、unzip、xz）
- [ ] 2) 安装 Flutter SDK
- [ ] 3) 配置 PATH 与镜像
- [ ] 4) 执行 flutter precache 与 doctor
- [ ] 5) 安装 Android Studio + Android SDK + licenses
- [ ] 6) 安装 Xcode + CocoaPods（如需 iOS）
- [ ] 7) 验证 Android emulator / iOS simulator
- [ ] 8) 创建并运行示例应用
```

### 1) 基础工具

优先使用 Homebrew：

```bash
brew install git curl unzip xz
```

如果缺少 Homebrew，先安装后重试。

### 2) 安装 Flutter SDK

推荐目录：
- Apple Silicon：`~/development/flutter`
- Intel：`~/development/flutter`

建议使用 git 安装（便于后续升级）：

```bash
mkdir -p ~/development
git clone https://github.com/flutter/flutter.git -b stable ~/development/flutter
```

### 3) 配置 PATH 与镜像

添加 Flutter 可执行路径：

```bash
cat <<'EOF' >> ~/.zshrc
# Flutter SDK 路径
export PATH="$PATH:$HOME/development/flutter/bin"
EOF
source ~/.zshrc
```

确认 `~/.zshrc` 中也已写入镜像变量（见上文镜像配置）。

### 4) 执行 precache 与 doctor

```bash
flutter --version
flutter precache
flutter doctor -v
```

若提示命令不存在，重新打开终端或再次 `source` shell profile 后重试。

### 5) Android toolchain

1. 安装 Android Studio（图形界面安装即可）。
2. 打开 Android Studio 一次，完成首次 SDK 初始化。
3. 确认已安装以下 SDK 组件：
   - Android SDK Platform (latest stable API)
   - Android SDK Platform-Tools
   - Android SDK Command-line Tools
   - Android Emulator
4. 接受 licenses：

```bash
flutter doctor --android-licenses
```

若提示缺少 `sdkmanager`，在 SDK Manager 补装 command-line tools 后重试。

### 6) iOS toolchain（按需）

1. 从 App Store 安装 Xcode。
2. 执行：

```bash
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -runFirstLaunch
```

3. 安装 CocoaPods：

```bash
brew install cocoapods
pod --version
```

若 CocoaPods 因网络或权限失败，优先使用 Homebrew 路径，不要先切 Ruby gem 方案。

### 7) 设备与模拟器就绪检查

```bash
flutter devices
```

期望结果：
- Android 开发至少有一个 emulator 或真机
- iOS 开发可识别 simulator（`open -a Simulator`）

### 8) 端到端验证

```bash
flutter create hello_flutter_cn
cd hello_flutter_cn
flutter pub get
flutter run
```

若 pub 下载慢或失败，重新检查**当前 shell 会话**与 shell profile 中的镜像变量。

## 常见问题处理

### `flutter doctor` 提示 Android toolchain 缺失

- 确保 Android Studio 至少打开并初始化过一次。
- 检查 Flutter 的 Android SDK 配置：
  - `flutter config --android-sdk <sdk-path>`
- 重新执行：
  - `flutter doctor -v`
  - `flutter doctor --android-licenses`

### `Unable to find git in your PATH`

- 安装 git（`brew install git`）
- 重启终端
- 验证 `git --version`

### CocoaPods repo/spec timeout

- 先确认基础网络与镜像配置。
- 重试 `pod --version` 与 iOS 构建。
- 仍失败时，先记录完整报错，再与用户确定 mirror/proxy 策略。

### Xcode license 或首次启动未完成

- 执行：
  - `sudo xcodebuild -license accept`
  - `sudo xcodebuild -runFirstLaunch`

## 工具脚本

使用内置脚本执行可重复安装：

```bash
bash scripts/bootstrap-flutter-cn.sh
```

可选环境变量：

```bash
NEED_IOS=no \
FLUTTER_DIR="$HOME/development/flutter" \
SHELL_PROFILE="$HOME/.zshrc" \
bash scripts/bootstrap-flutter-cn.sh
```

脚本行为：
- 通过 Homebrew 安装基础工具
- 通过 git 安装或更新 Flutter `stable`
- 以幂等方式写入镜像和 PATH
- 执行 `flutter precache` 与 `flutter doctor -v`
- 输出 Android/iOS 后续人工步骤
- 创建冒烟工程 `~/hello_flutter_cn`

执行验收：

```bash
bash scripts/validate-flutter-cn.sh
```

验收参数：

```bash
# 仅 Android
NEED_IOS=no bash scripts/validate-flutter-cn.sh

# 仅 iOS
NEED_ANDROID=no bash scripts/validate-flutter-cn.sh
```

验收输出：
- 每项检查输出 PASS/WARN/FAIL
- 最终结果：`READY for development` 或 `NOT READY`
- 退出码：ready 为 `0`，not ready 为 `1`

## 验收闭环

排障时建议按以下循环执行：

1. 运行 bootstrap 脚本：
   - `bash scripts/bootstrap-flutter-cn.sh`
2. 运行 validator：
   - `bash scripts/validate-flutter-cn.sh`
3. 如果 validator 失败：
   - 先修复优先级最高的 FAIL 项
   - 再次运行 validator
4. 仅当结果为 `READY for development` 时结束

## 技能输出格式

执行本 Skill 后给用户的回复应包含：

1. **当前状态**：已安装与缺失项
2. **已执行命令**：按阶段归类
3. **阻塞问题**：精确报错与可能原因
4. **下一步动作**：最小可执行解阻命令
5. **最终验收**：对 `flutter doctor -v` 的简明结论

## 约束

- 不要默认要求 iOS；先确认用户是否仅需 Android。
- 默认使用 stable channel，除非用户明确要求 beta/master。
- 不要粗暴覆盖 shell profile；优先幂等追加。
- 不要默认卸载现有 SDK，除非用户明确要求清理。

## 附加资料

- 错误到修复速查：`[troubleshooting.md](troubleshooting.md)`
- 分场景回复模板：`[examples.md](examples.md)`
- Skill 回归检查清单：`[self-test.md](self-test.md)`
