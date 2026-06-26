#!/bin/bash

# 修复合并后的 APK 安装失败问题

# 设置变量
APK_PATH="/Users/mac/Documents/work_360/apk_modified/universal_signed.apk"
DECOMPILED_DIR="/tmp/temp_apk_decompiled"
TEMP_DIR="/tmp/fix_arsc_temp"
KEYSTORE="/tmp/apk_merge/temp.keystore"
KEY_ALIAS="tempkey"
KEY_PASS="android"
KS_PASS="android"
BUILD_TOOLS="/Users/mac/Library/Android/sdk/build-tools/36.1.0"

echo "开始修复合并后的 APK 安装失败问题..."

# 1. 解包 APK
echo "正在解包 APK 文件..."
apktool d "$APK_PATH" -o "$DECOMPILED_DIR" -f

# 2. 修复 AndroidManifest.xml 文件
MANIFEST_PATH="${DECOMPILED_DIR}/AndroidManifest.xml"
echo "正在修复 AndroidManifest.xml 文件..."

# 确保 AndroidManifest.xml 文件格式正确
# 检查是否以 <manifest> 标签开头
if [ "$(head -2 "$MANIFEST_PATH" | grep -c "<manifest")" -eq 0 ]; then
    echo "AndroidManifest.xml 文件格式有误，正在修复..."
    # 读取原始内容
    ORIG_CONTENT=$(cat "$MANIFEST_PATH")
    # 重新格式化
    FIXED_CONTENT='<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" android:versionCode="1480" android:versionName="1.4.8" android:compileSdkVersion="36" android:compileSdkVersionCodename="16" package="com.holaglobal.cash.loan.mx" platformBuildVersionCode="36" platformBuildVersionName="16">
    '$(echo "$ORIG_CONTENT" | sed '1d')
    echo "$FIXED_CONTENT" > "$MANIFEST_PATH"
fi

# 修改 android:extractNativeLibs 属性
echo "正在修改 android:extractNativeLibs 属性..."
sed -i '' 's/android:extractNativeLibs="false"/android:extractNativeLibs="true"/g' "$MANIFEST_PATH"

# 3. 重新打包 APK
echo "正在重新打包 APK..."
apktool b "$DECOMPILED_DIR" -o /tmp/temp_universal_signed.apk

# 4. 修复 resources.arsc 文件压缩状态
echo "正在修复 resources.arsc 文件压缩状态..."

rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# 解压缩 APK
unzip -q /tmp/temp_universal_signed.apk -d "$TEMP_DIR"

# 解压缩 resources.arsc 文件
rm -f "$TEMP_DIR/resources.arsc"
unzip -p /tmp/temp_universal_signed.apk resources.arsc > "$TEMP_DIR/resources.arsc"

# 重新打包 APK，确保 resources.arsc 文件未压缩
cd "$TEMP_DIR"
zip -r0 "$APK_PATH" resources.arsc
zip -r "$APK_PATH" . -x "resources.arsc" -q

# 5. 对齐和重新签名 APK
echo "正在对齐和重新签名 APK..."

ALIGNED_APK="$TEMP_DIR/aligned.apk"
"$BUILD_TOOLS/zipalign" -p 4 "$APK_PATH" "$ALIGNED_APK"
"$BUILD_TOOLS/apksigner" sign --ks "$KEYSTORE" --ks-key-alias "$KEY_ALIAS" --ks-pass pass:"$KS_PASS" --key-pass pass:"$KEY_PASS" --out "$APK_PATH" "$ALIGNED_APK"

# 6. 清理临时文件
echo "正在清理临时文件..."
cd /tmp
rm -f temp_universal_signed.apk
rm -rf temp_apk_decompiled
rm -rf "$TEMP_DIR"

echo "修复完成！"
echo "修复后的 APK 文件已保存到：$APK_PATH"

# 7. 验证修复后的 APK
echo "正在验证修复后的 APK..."
APK_INFO=$(aapt dump badging "$APK_PATH")
if [ $? -eq 0 ]; then
    echo "✅ APK 文件验证成功！"
else
    echo "❌ APK 文件验证失败！"
fi
