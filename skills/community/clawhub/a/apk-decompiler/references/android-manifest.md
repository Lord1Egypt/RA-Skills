# AndroidManifest.xml 修改指南

## 结构概览

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.app"
    android:versionCode="1"
    android:versionName="1.0">
    
    <uses-permission android:name="android.permission.INTERNET"/>
    
    <application
        android:label="@string/app_name"
        android:icon="@drawable/ic_launcher">
        
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
        
    </application>
</manifest>
```

## 常见修改

### 1. 修改应用名称
```xml
<!-- 在 res/values/strings.xml 中修改 -->
<string name="app_name">新名称</string>
```

### 2. 修改包名
```xml
<manifest 
    package="com.new.package.name"
    ...>
```

注意：修改包名后需要：
- 更新所有 Java/Smali 中的包名引用
- 更新 R 类引用
- 重新签名

### 3. 添加/移除权限

添加权限：
```xml
<uses-permission android:name="android.permission.CAMERA"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
```

移除权限：
删除对应的 `<uses-permission>` 标签

### 4. 修改入口 Activity
```xml
<activity android:name=".NewMainActivity">
    <intent-filter>
        <action android:name="android.intent.action.MAIN"/>
        <category android:name="android.intent.category.LAUNCHER"/>
    </intent-filter>
</activity>
```

### 5. 添加 Activity
```xml
<activity 
    android:name=".NewActivity"
    android:label="New Activity"
    android:exported="false"/>
```

### 6. 修改调试标志
```xml
<application
    android:debuggable="true"
    ...>
```

### 7. 允许明文 HTTP（API 28+）
```xml
<application
    android:usesCleartextTraffic="true"
    ...>
```

### 8. 备份配置
```xml
<application
    android:allowBackup="true"
    android:fullBackupContent="@xml/backup_rules"
    ...>
```

## 权限对照表

| 权限 | 用途 |
|------|------|
| INTERNET | 网络访问 |
| CAMERA | 摄像头 |
| READ_EXTERNAL_STORAGE | 读取存储 |
| WRITE_EXTERNAL_STORAGE | 写入存储 |
| ACCESS_FINE_LOCATION | 精确位置 |
| ACCESS_COARSE_LOCATION | 粗略位置 |
| BLUETOOTH | 蓝牙 |
| BLUETOOTH_ADMIN | 蓝牙管理 |
| RECORD_AUDIO | 录音 |
| VIBRATE | 振动 |
| WAKE_LOCK | 保持唤醒 |
| RECEIVE_BOOT_COMPLETED | 开机启动 |

## apktool-out 目录结构

```
apktool-out/
├── AndroidManifest.xml    # 主配置文件（已解码为文本）
├── apktool.yml            # apktool 配置
├── assets/                # 资源文件
├── res/                   # Android 资源
│   ├── values/
│   │   ├── strings.xml   # 字符串资源
│   │   ├── colors.xml    # 颜色
│   │   └── styles.xml    # 样式
│   ├── layout/           # 布局文件
│   ├── drawable*/        # 图片资源
│   └── xml/              # XML 配置
├── smali*/               # Smali 源码（如果没使用 -s）
└── lib/                  # Native 库
```

## 修改流程

1. **反编译**
   ```bash
   python3 decompile.py app.apk
   ```

2. **编辑文件**
   - 修改 `AndroidManifest.xml`
   - 修改 `res/values/strings.xml`
   - 修改 `smali-out/` 中的代码

3. **重新打包**
   ```bash
   python3 rebuild.py ./app-decompiled
   ```

4. **安装测试**
   ```bash
   adb install app-rebuilt.apk
   ```

## 注意事项

- 修改后必须重新签名
- 调试密钥签名只能用于测试
- 发布需要使用正式密钥
- 某些应用有完整性校验，可能需要额外处理
