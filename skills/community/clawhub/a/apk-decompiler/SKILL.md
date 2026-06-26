---
name: apk-decompiler
description: Android APK 逆向工程工具集，支持反编译、修改和重新打包。使用场景：(1) 反编译 APK 查看 Smali/Java 源码 (2) 分析应用架构和权限 (3) 修改 UI 文本、功能、逻辑 (4) 重新打包并签名 APK (5) 提取字符串、权限、组件等信息。触发词：反编译 APK、逆向 Android 应用、修改 APK、分析 DEX、Smali 编辑、APK 签名、Android 逆向。
version: 1.0.0
---

# APK Decompiler

Android APK 逆向工程工具集，支持完整的反编译、修改和重新打包流程。

## 快速开始

### 1. 设置工具

首次使用需要下载必要工具：

```bash
cd /path/to/apk-decompiler/scripts
chmod +x setup_tools.sh
./setup_tools.sh
```

这会下载：
- **baksmali/smali** - DEX ↔ Smali 转换
- **apktool** - 资源解码/打包
- **dex2jar** - DEX → JAR 转换
- **uber-apk-signer** - APK 签名

### 2. 反编译 APK

```bash
python3 scripts/decompile.py app.apk
```

输出目录结构：
```
app-decompiled/
├── smali-out/         # Smali 源码（可编辑）
├── apktool-out/       # 解码的资源文件
│   ├── AndroidManifest.xml
│   ├── res/
│   └── assets/
└── extracted/         # 原始 APK 内容
```

### 3. 修改代码/资源

编辑相关文件：
- `smali-out/` - 修改 Smali 代码
- `apktool-out/AndroidManifest.xml` - 修改配置
- `apktool-out/res/values/strings.xml` - 修改文本

### 4. 重新打包

```bash
python3 scripts/rebuild.py ./app-decompiled
```

输出：`app-rebuilt.apk`（已签名）

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `setup_tools.sh` | 下载并设置反编译工具 |
| `decompile.py` | 反编译 APK |
| `rebuild.py` | 重新打包并签名 |
| `analyze.py` | 分析 APK 结构 |

## 常用命令

### 反编译选项

```bash
# 基本反编译
python3 decompile.py app.apk

# 同时生成 JAR（可用 jadx 查看 Java 源码）
python3 decompile.py app.apk --java

# 只解码资源
python3 decompile.py app.apk --resources-only

# 只反编译 Smali
python3 decompile.py app.apk --smali-only
```

### 分析选项

```bash
# 完整分析
python3 analyze.py app.apk

# 只看权限
python3 analyze.py app.apk --permissions

# 查看 Activities
python3 analyze.py app.apk --activities

# 查看应用类（需要先反编译）
python3 analyze.py app.apk --smali ./smali-out --classes
```

### 重新打包选项

```bash
# 打包并签名
python3 rebuild.py ./project-dir

# 只签名 APK
python3 rebuild.py ./project-dir --sign-only app.apk

# 跳过签名
python3 rebuild.py ./project-dir --no-sign
```

## 修改示例

### 修改字符串

1. 找到字符串定义：
```bash
grep -r "原始文本" ./apktool-out/res/values/
```

2. 编辑 `strings.xml`：
```xml
<string name="app_name">新名称</string>
```

### 修改逻辑（Smali）

1. 找到目标类：
```bash
find ./smali-out -name "MainActivity.smali"
```

2. 编辑 Smali 代码：
```smali
# 修改返回值
.method public isEnabled()Z
    const/4 v0, 0x1
    return v0
.end method
```

3. 参考 [references/smali-syntax.md](references/smali-syntax.md) 了解 Smali 语法

### 修改 AndroidManifest

编辑 `apktool-out/AndroidManifest.xml`：
- 添加/移除权限
- 修改应用名称
- 添加 Activity
- 启用调试模式

参考 [references/android-manifest.md](references/android-manifest.md)

## 工具目录

设置完成后，工具存储在 `~/.apk-tools/`：

```
~/.apk-tools/
├── baksmali.jar       # DEX → Smali
├── smali.jar          # Smali → DEX
├── apktool.jar        # 资源解码/打包
├── dex2jar/           # DEX → JAR
└── uber-apk-signer.jar # APK 签名
```

可设置环境变量：
```bash
export TOOLS_DIR=/custom/path
```

## 工作流程

```
┌─────────────┐
│   app.apk   │
└──────┬──────┘
       │ decompile.py
       ▼
┌─────────────────────────┐
│ app-decompiled/         │
│  ├── smali-out/         │ ← 编辑 Smali 代码
│  └── apktool-out/       │ ← 编辑资源/Manifest
└──────┬──────────────────┘
       │ rebuild.py
       ▼
┌─────────────────────┐
│ app-rebuilt.apk     │
│ (已签名，可安装)     │
└─────────────────────┘
```

## 注意事项

1. **签名限制**：重新打包后使用调试密钥签名，与原应用签名不同
   - 无法覆盖安装原应用
   - 需要先卸载原应用

2. **完整性校验**：某些应用会校验签名或文件完整性
   - 需要额外处理绕过校验

3. **混淆代码**：ProGuard/R8 混淆后的代码：
   - 类名/方法名会被重命名
   - 需要手动分析理解逻辑

4. **法律风险**：仅供学习研究，请勿用于非法用途

## 环境要求

- Java 运行时 (JRE 8+)
- Python 3.6+
- unzip (通常已预装)
