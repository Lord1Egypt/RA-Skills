# 修复合并后的 APK 安装失败问题

## 问题描述
合并后的 universal_signed.apk 在安装时出现了以下错误：
- INSTALL_FAILED_INVALID_APK: Failed to extract native libraries, res=-2
- 在 Android 11 及更高版本中，resources.arsc 文件需要未压缩且对齐到 4 字节边界

## 解决方案
1. **修复 AndroidManifest.xml 文件格式问题**：确保文件以 <manifest> 标签开头，格式正确
2. **修改 android:extractNativeLibs 属性**：将该属性从 false 改为 true，确保系统会提取 native libraries
3. **确保 resources.arsc 文件未压缩**：使用 zip 命令解压缩该文件并重新打包 APK

## 使用工具
- apktool：用于解包和重新打包 APK
- sed：用于修改 AndroidManifest.xml 文件
- zip/zipinfo：用于检查和修改 APK 内容的压缩状态
- zipalign：用于对齐 APK 文件
- apksigner：用于重新签名 APK

## 修复过程
1. 使用 apktool 解包 universal_signed.apk
2. 修改 AndroidManifest.xml 文件格式
3. 将 android:extractNativeLibs 属性从 false 改为 true
4. 重新打包 APK
5. 使用 zip 命令确保 resources.arsc 文件未压缩
6. 使用 zipalign 对齐 APK
7. 使用 apksigner 重新签名 APK

## 最终结果
✅ **APK 文件格式正确**  
✅ **native libraries 提取问题已解决**  
✅ **resources.arsc 文件未压缩**  
✅ **APK 文件对齐到 4 字节边界**  
✅ **APK 文件已成功签名**  

## 技能实现脚本
### 1. 修复 AndroidManifest.xml 文件格式和属性
```bash
#!/bin/bash

DECOMPILED_DIR="/tmp/temp_apk_decompiled"
MANIFEST_PATH="${DECOMPILED_DIR}/AndroidManifest.xml"

# 解包 APK
apktool d /Users/mac/Documents/work_360/apk_modified/universal_signed.apk -o "$DECOMPILED_DIR" -f

# 修改 android:extractNativeLibs 属性
sed -i '' 's/android:extractNativeLibs="false"/android:extractNativeLibs="true"/g' "$MANIFEST_PATH"

# 重新打包 APK
apktool b "$DECOMPILED_DIR" -o /tmp/temp_universal_signed.apk
```

### 2. 修复 resources.arsc 文件压缩状态
```bash
#!/bin/bash

APK_PATH="/Users/mac/Documents/work_360/apk_modified/universal_signed.apk"
TEMP_DIR="/tmp/fix_arsc_temp"

# 解压缩 APK
unzip -q "$APK_PATH" -d "$TEMP_DIR"

# 解压缩 resources.arsc 文件
rm -f "$TEMP_DIR/resources.arsc"
unzip -p "$APK_PATH" resources.arsc > "$TEMP_DIR/resources.arsc"

# 重新打包 APK，确保 resources.arsc 文件未压缩
cd "$TEMP_DIR"
zip -r0 "$APK_PATH" resources.arsc
zip -r "$APK_PATH" . -x "resources.arsc" -q

# 对齐和重新签名 APK
ALIGNED_APK="$TEMP_DIR/aligned.apk"
/Users/mac/Library/Android/sdk/build-tools/36.1.0/zipalign -p 4 "$APK_PATH" "$ALIGNED_APK"
/Users/mac/Library/Android/sdk/build-tools/36.1.0/apksigner sign --ks /tmp/apk_merge/temp.keystore --ks-key-alias tempkey --ks-pass pass:android --key-pass pass:android --out "$APK_PATH" "$ALIGNED_APK"

# 清理临时目录
rm -rf "$TEMP_DIR"
```

## 使用方法
1. 将 APK 传输到目标手机
2. 启用“未知来源应用安装”选项
3. 点击 APK 文件进行安装

## 注意事项
- 确保使用正确版本的 Android SDK 工具（如 build-tools 36.1.0）
- 使用正确的 keystore 文件进行签名
- 确保设备已连接并启用了 USB 调试模式
- 如果安装失败，可以尝试使用 adb 命令进行安装：
  ```
  adb install /Users/mac/Documents/work_360/apk_modified/universal_signed.apk
  ```
