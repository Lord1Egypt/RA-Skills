# Flutter CN 故障速查

本手册用于中国区 Flutter 环境常见问题的快速定位与修复。

## 1) `flutter pub get` 很慢或超时

### 现象
- `Resolving dependencies...` 长时间卡住
- 访问 `pub.dev` 出现连接超时

### 检查
```bash
echo "$PUB_HOSTED_URL"
echo "$FLUTTER_STORAGE_BASE_URL"
```

期望值：
- `https://pub.flutter-io.cn`
- `https://storage.flutter-io.cn`

### 处理
```bash
export PUB_HOSTED_URL=https://pub.flutter-io.cn
export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
flutter pub get -v
```

如果生效，请写入 `~/.zshrc` 并重开终端。

## 2) Gradle 依赖下载慢或失败

### 现象
- Android 构建卡在 `Download https://services.gradle.org/...`
- Gradle 依赖频繁出现 `Read timed out`

### 建议策略
- 优先使用稳定网络链路（办公网络、可用代理/VPN）。
- 团队仓库中不要默认改项目级 Gradle 镜像，除非用户明确要求。

### 可选：仅本机优化
编辑 `~/.gradle/gradle.properties`：

```properties
org.gradle.daemon=true
org.gradle.parallel=true
org.gradle.configureondemand=true
org.gradle.jvmargs=-Xmx4g -Dfile.encoding=UTF-8
org.gradle.internal.http.connectionTimeout=120000
org.gradle.internal.http.socketTimeout=120000
```

然后执行：
```bash
cd android
./gradlew --refresh-dependencies
```

## 3) CocoaPods 安装或更新超时

### 现象
- `pod install` hangs or fails on spec repo update
- CDN 拉取超时

### 检查
```bash
pod --version
which pod
```

### 处理顺序
1. 优先确认 CocoaPods 来自 Homebrew：
   ```bash
   brew install cocoapods
   ```
2. 在 iOS 目录重试并打开详细日志：
   ```bash
   cd ios
   pod install --verbose
   ```
3. 若仍失败，先记录失败的 host/path，再决定是否更改源配置。

## 4) `flutter doctor` 缺少 `Android toolchain`

### 现象
- `Android toolchain - develop for Android devices` 显示 `✗`
- 提示缺少 `cmdline-tools` 或 licenses

### 处理
1. 打开一次 Android Studio 并完成初始化向导。
2. 在 SDK Manager 安装：
   - Android SDK Platform
   - Android SDK Platform-Tools
   - Android SDK Command-line Tools
3. 执行：
   ```bash
   flutter doctor --android-licenses
   flutter doctor -v
   ```

如果 SDK 路径是自定义：
```bash
flutter config --android-sdk "$HOME/Library/Android/sdk"
```

## 5) Xcode 未配置完成

### 现象
- `Xcode - develop for iOS and macOS` 显示 `✗`
- license 或首次启动未完成

### 处理
```bash
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -license accept
sudo xcodebuild -runFirstLaunch
flutter doctor -v
```

## 6) `git` 找不到 / `flutter` 命令找不到

### 现象
- `Unable to find git in your PATH`
- `zsh: command not found: flutter`

### 处理
```bash
brew install git
echo 'export PATH="$PATH:$HOME/development/flutter/bin"' >> ~/.zshrc
source ~/.zshrc
git --version
flutter --version
```

## 7) 检测不到模拟器/设备

### 现象
- `flutter devices` 返回无设备

### 处理
- Android：在 Android Studio Device Manager 启动 emulator。
- iOS:
  ```bash
  open -a Simulator
  flutter devices
  ```

如果使用真机，确认 USB 调试/信任流程已完成。

## 最小化排障信息采集

需要升级排障时，先收集：

```bash
flutter doctor -v
flutter devices
flutter --version
echo "$PUB_HOSTED_URL"
echo "$FLUTTER_STORAGE_BASE_URL"
```

请提供：执行命令、完整报错、开始出现问题的时间点。
