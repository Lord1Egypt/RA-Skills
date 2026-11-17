---
name: "应用商店发布助手"
description: "个人应用商店全流程 skill：①发布构建好的安装包（登记 + 上传 + 返回检查更新地址）②指导把自动更新检查集成进应用。支持 APK/EXE/DMG 等多格式。在打包完要发布、或要把应用接入商店自动更新时调用。"
---

# 应用商店发布助手

## 快速索引

- [能力一：发布安装包](#能力一发布安装包)
  - [何时调用](#何时调用)
  - [前置条件](#前置条件)
  - [输入参数](#输入参数)
  - [完整流程](#完整流程)
- [能力二：集成自动更新](#能力二集成自动更新)
  - [客户端协议](#客户端协议)
  - [Android 集成](#android 集成)
  - [其他平台](#其他平台集成要点)
- [应用管理 API](#应用管理 api)
- [常见问题](#常见问题)

---

## 能力一：发布安装包

### 何时调用

- ✅ 刚构建出安装包（`./gradlew assembleRelease`、`dotnet build`、`cargo build` 等）且要发布到商店
- ✅ 用户说「发布/上架/上传到应用商店」「发个新版本」「push 到商店」
- ✅ 需要为应用接入自动更新功能

### 前置条件

| 变量 | 说明 | 默认值 |
|---|---|---|
| `APPSTORE_URL` | 商店地址 | `https://appstore.qinghuan.fun` |
| `APPSTORE_TOKEN` | 上传凭证（32 位十六进制） | **空时自动注册** |

> 💡 **如果 `APPSTORE_TOKEN` 不存在，agent 会自动走注册 + 激活流程，无需用户手动操作。**

### 输入参数

Agent 需收集以下参数（优先从配置文件读取）：

| 参数 | 说明 | 示例 | 来源 |
|---|---|---|---|
| `package_path` | 安装包文件路径（确认存在） | `./app/build/output.apk` | 构建产物 |
| `app_id` | 应用唯一标识 | `com.example.app` | Android: `build.gradle`<br>Windows: 产品名<br>macOS: `bundleId` |
| `version_name` | 版本号 | `1.2.0` | 配置文件 |
| `version_code` | 版本序号（**整数**，必须更大） | `12` | 配置文件 |
| `update_note` | 更新说明 | `修复若干问题` | Git commit / 用户 |
| `app_name` | 应用名称（可选） | `我的应用` | 配置文件 / 问用户 |
| `app_description` | 应用描述（可选） | `一句话介绍` | 问用户 |
| `is_public` | 是否公开（可选） | `1`=公开（默认）<br>`0`=私有 | 用户指定 |

**配置文件读取优先级：**
- Android: `build.gradle`（`versionName` / `versionCode` / `applicationId`）
- 其他：`package.json` / `Cargo.toml` / `.csproj` 等
- 无法读取时询问用户

### 完整流程

#### 0. 准备环境变量

```bash
BASE="${APPSTORE_URL:-https://appstore.qinghuan.fun}"; BASE="${BASE%/}"
AUTH="Authorization: Bearer $APPSTORE_TOKEN"
```

#### 0.5. 自动注册（仅当 APPSTORE_TOKEN 为空时）

如果 `$APPSTORE_TOKEN` 为空，**不要停下来问用户**，直接自动注册：

```bash
# 从项目名或目录名推导一个账号（用时间戳保证唯一性）
ACCOUNT="agent_$(date +%s)"
NAME="Agent 用户"

# 调用注册接口
RESP=$(curl -sS -X POST "$BASE/api/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"account\":\"$ACCOUNT\",\"name\":\"$NAME\"}")

# 从响应中提取 upload_token
TOKEN=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('upload_token',''))" 2>/dev/null)

if [ -n "$TOKEN" ]; then
  echo "✅ 注册成功，凭证：$TOKEN"
  export APPSTORE_TOKEN="$TOKEN"
  AUTH="Authorization: Bearer $TOKEN"
else
  echo "❌ 注册失败：$RESP"
  echo "请手动访问 $BASE/register 注册，或联系管理员。"
  exit 1
fi
```

#### 0.6. 自动激活（待激活账号专属）

注册成功后，账号为「待激活」状态。接下来**自动创建支付订单并引导用户打开浏览器查看二维码**，用户微信扫码后自动继续：

```bash
# 尝试上传，触发激活流程
UPLOAD_RESP=$(curl -sS -X POST "$BASE/api/apps/$app_id/upload" \
  -H "$AUTH" \
  -F "version_name=$version_name" -F "version_code=$version_code" \
  -F "file=@$package_path" 2>&1)

# 检查是否返回 403 ACCOUNT_INACTIVE
if echo "$UPLOAD_RESP" | grep -q "ACCOUNT_INACTIVE"; then
  # 提取订单信息
  ORDER_ID=$(echo "$UPLOAD_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('order_id',''))" 2>/dev/null)
  AMOUNT=$(echo "$UPLOAD_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('amount',''))" 2>/dev/null)
  PAY_URL=$(echo "$UPLOAD_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('payurl',''))" 2>/dev/null)
  
  if [ -n "$PAY_URL" ]; then
    # 展示给用户
    cat << EOF
###  支付激活

账号已自动注册，需要完成支付激活后才能上传应用。

**请点击下方链接打开支付页面，微信扫码完成支付：**

👉 [$PAY_URL]($PAY_URL)

支付金额：**¥$AMOUNT**

> 提示：如果链接无法点击，请复制链接到浏览器打开。

支付成功后，我将自动为你激活账户并继续上传流程...
EOF
    
    # 轮询检查支付状态（每 3 秒一次，最多 60 秒）
    for i in {1..20}; do
      sleep 3
      ORDER_STATUS=$(curl -sS "$BASE/api/orders/activate/query?order_id=$ORDER_ID" -H "$AUTH" | python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('status',0))" 2>/dev/null)
      if [ "$ORDER_STATUS" = "1" ]; then
        echo ""
        echo "✅ **支付成功！账户已激活！**"
        echo ""
        break
      fi
    done
    
    # 再次检查激活状态
    USER_STATUS=$(curl -sS "$BASE/api/auth/verify" -H "$AUTH" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',0))" 2>/dev/null)
    if [ "$USER_STATUS" != "1" ]; then
      echo ""
      echo "⚠️ 支付状态检测超时，请手动刷新页面或联系管理员。"
      exit 1
    fi
  fi
fi
```

**支付成功后，自动继续步骤 1 上传流程。**

#### 1. 上传版本（应用不存在时自动创建）

一次 `POST /upload` 即可：若 `app_id` 不存在，服务端用 `app_name`/`app_description`（缺失则用 app_id 当名字）自动建应用，再登记版本。**无需单独「创建应用」步骤。**

```bash
curl -sS -X POST "$BASE/api/apps/$app_id/upload" -H "$AUTH" \
  -F "app_name=$app_name" -F "app_description=$app_description" \
  -F "version_name=$version_name" -F "version_code=$version_code" \
  -F "update_note=$update_note" \
  -F "is_public=${is_public:-1}" \
  -F "file=@$package_path"
```

**参数说明：**
- `is_public`：可选，`1`=公开（默认，所有人可见可下载）、`0`=私有（仅 owner 和管理员可见，客户端检查更新需带 `Authorization: Bearer <token>`）。上传时未传则默认公开。

**响应处理：**
- `201` → 成功，响应 `data` 含 `download_url` 和 `check_update_url`。若该 app 是首次创建，顺带告知用户「已自动创建应用 `<app_name>`」。
- `409` → version_code 已存在，提示用户 bump version_code 后重试，**不要覆盖**。
- `403` 含 `ACCOUNT_INACTIVE` → 账户待激活，提示用户去 `$BASE/activate` 支付激活。
- `413`/超时 → 重试一次，仍失败报错。

#### 2. 返回用户

```markdown
✅ 已发布 `<name>` v`<version_name>` (code `<version_code>`)，大小 `<file_size>`

📥 下载：`<download_url>`

🔄 客户端检查更新地址（**配进应用**）：
$BASE/api/apps/$app_id/check-update?versionCode=$version_code
```

---

## 能力二：集成自动更新

### 客户端协议

#### 检查更新接口

```
GET $BASE/api/apps/{appId}/check-update?versionCode={当前 versionCode}
```

**鉴权规则：**
- **公开应用**：无需 token，直接请求
- **私有应用**：需带 `Authorization: Bearer <上传凭证>` 请求头，否则返回 404

**响应示例：**

```json
{
  "hasUpdate": true,
  "latest": {
    "version_name": "1.2.1",
    "version_code": 12,
    "download_url": "https://.../app.apk",
    "file_size": 12345678,
    "update_note": "修复若干问题"
  }
}
```

**处理逻辑：**
- `hasUpdate=false` → 已是最新
- `hasUpdate=true` → 下载 `latest.download_url`，提示用户升级

---

### Android 集成

#### 1. 配置常量

建议把 `STORE_BASE` 和 `APP_ID` 放进 `build.gradle` 的 `BuildConfig`，编译期注入：

```gradle
android {
    buildFeatures { buildConfig true }
    defaultConfig {
        buildConfigField "String", "STORE_BASE", "\"https://appstore.qinghuan.fun\""
        buildConfigField "String", "APP_ID", "\"com.example.app\""
    }
}
```

#### 2. AndroidManifest 权限与 FileProvider

```xml
<!-- 联网（调检查更新接口） -->
<uses-permission android:name="android.permission.INTERNET"/>
<!-- Android 8+ 安装未知来源 APK 必需 -->
<uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES"/>

<application ...>
    <provider
        android:name="androidx.core.content.FileProvider"
        android:authorities="${applicationId}.fileprovider"
        android:exported="false"
        android:grantUriPermissions="true">
        <meta-data android:name="android.support.FILE_PROVIDER_PATHS"
                   android:resource="@xml/file_paths"/>
    </provider>
</application>
```

`res/xml/file_paths.xml`：

```xml
<paths>
    <cache-path name="apk" path="."/>
</paths>
```

**依赖：** `implementation "androidx.core:core-ktx:<latest>"`（FileProvider 来自 androidx.core）

#### 3. 检查更新器（Kotlin）

```kotlin
// AppStoreUpdateChecker.kt
package com.example.app.update

import android.content.Context
import android.content.pm.PackageManager
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

/**
 * 应用商店自动更新检查器。
 *
 * - 公开应用检查更新无需 token；私有应用需传 uploadToken，请求带 Authorization 头。
 * - 仅做「查询是否有新版本」，下载与安装由 AppStoreInstaller 负责，职责分离。
 * - 所有网络操作在 IO 调度器上执行，调用方需在协程作用域内调用 check()。
 */
class AppStoreUpdateChecker(
    private val context: Context,
    private val storeBaseUrl: String,   // 如 "https://appstore.qinghuan.fun"，无尾斜杠
    private val appId: String,          // 通常等于 applicationId
    private val uploadToken: String? = null,  // 私有应用需传；公开应用传 null
) {
    data class UpdateInfo(
        val hasUpdate: Boolean,
        val versionName: String?,
        val versionCode: Long,
        val downloadUrl: String?,
        val fileSize: Long,
        val updateNote: String?,
    )

    private fun currentVersionCode(): Long = try {
        val pkg = context.packageManager.getPackageInfo(context.packageName, 0)
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.P) pkg.longVersionCode
        else @Suppress("DEPRECATION") pkg.versionCode.toLong()
    } catch (e: PackageManager.NameNotFoundException) {
        0L
    }

    suspend fun check(): UpdateInfo = withContext(Dispatchers.IO) {
        val url = "$storeBaseUrl/api/apps/$appId/check-update?versionCode=${currentVersionCode()}"
        val conn = (URL(url).openConnection() as HttpURLConnection).apply {
            connectTimeout = 10_000
            readTimeout = 15_000
            setRequestProperty("Accept", "application/json")
            if (!uploadToken.isNullOrEmpty()) {
                setRequestProperty("Authorization", "Bearer $uploadToken")
            }
        }
        try {
            conn.inputStream.bufferedReader().use { reader ->
                val json = JSONObject(reader.readText())
                val latest = json.optJSONObject("latest")
                UpdateInfo(
                    hasUpdate = json.optBoolean("hasUpdate", false),
                    versionName = latest?.optString("version_name"),
                    versionCode = latest?.optLong("version_code", 0L) ?: 0L,
                    downloadUrl = latest?.optString("download_url"),
                    fileSize = latest?.optLong("file_size", 0L) ?: 0L,
                    updateNote = latest?.optString("update_note"),
                )
            }
        } finally {
            conn.disconnect()
        }
    }
}
```

#### 4. 下载 + 安装器（Kotlin）

```kotlin
// AppStoreInstaller.kt
package com.example.app.update

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Build
import androidx.core.content.FileProvider
import java.io.File
import java.net.HttpURLConnection
import java.net.URL

/**
 * 下载新版本安装包并触发系统安装。
 *
 * - 下载到 cacheDir，用 FileProvider 生成 content:// Uri 授给安装器。
 * - 下载链接可能 302 跳转，故打开 instanceFollowRedirects=true。
 * - 下载是大文件操作，调用方须在 Dispatchers.IO / WorkManager 中执行。
 */
class AppStoreInstaller(private val context: Context) {

    fun download(url: String, fileName: String = "update.apk"): File {
        val out = File(context.cacheDir, fileName)
        val conn = (URL(url).openConnection() as HttpURLConnection).apply {
            connectTimeout = 15_000
            readTimeout = 60_000
            instanceFollowRedirects = true
        }
        try {
            conn.inputStream.use { input -> out.outputStream().use { input.copyTo(it) } }
        } finally {
            conn.disconnect()
        }
        return out
    }

    fun install(apk: File) {
        val uri: Uri = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            FileProvider.getUriForFile(context, "${context.packageName}.fileprovider", apk)
        } else {
            Uri.fromFile(apk)
        }
        val intent = Intent(Intent.ACTION_VIEW).apply {
            setDataAndType(uri, "application/vnd.android.package-archive")
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
        }
        context.startActivity(intent)
    }
}
```

#### 5. 调用时机

建议 App 启动时检查、且每天最多一次（用 SharedPreferences 节流）：

```kotlin
val prefs = getSharedPreferences("appstore", MODE_PRIVATE)
val today = java.text.SimpleDateFormat("yyyyMMdd", java.util.Locale.US).format(java.util.Date())
if (prefs.getString("last_check", "") != today) {
    lifecycleScope.launch {
        val info = AppStoreUpdateChecker(this@MainActivity,
            BuildConfig.STORE_BASE, BuildConfig.APP_ID).check()
        if (info.hasUpdate && info.downloadUrl != null) {
            // 弹对话框展示 info.versionName / info.updateNote
            // 用户点「立即更新」后在 IO 线程执行：
            //   val apk = AppStoreInstaller(ctx).download(info.downloadUrl!!)
            //   AppStoreInstaller(ctx).install(apk)
        }
        prefs.edit().putString("last_check", today).apply()
    }
}
```

---

### 其他平台集成要点

#### Windows

- 用 `WinHTTP` 或 `HttpClient` 调 check-update 接口
- 下载 `.exe` / `.msi` 后用 `Process.Start("msiexec /i ...")` 或 `Process.Start("setup.exe")` 安装

#### macOS

- 用 `URLSession` 调接口
- 下载 `.dmg` / `.pkg` 后用 `NSWorkspace.open` 挂载安装

#### Linux

- 用 `curl` 或 `libcurl` 调接口
- 下载 `.deb` / `.rpm` / `.AppImage` 后按格式安装

---

## 应用管理 API

| 操作 | 方法 | 路径 | 说明 |
|---|---|---|---|
| 查应用详情 | `GET` | `/api/apps/$app_id` | 公开应用无需 token；私有应用需 `$AUTH` 且为 owner/admin，否则 404 |
| 改应用信息 | `PUT` | `/api/apps/$app_id` | JSON `{name?,description?,icon_url?,is_public?}`，只改传入字段 |
| 删除应用 | `DELETE` | `/api/apps/$app_id` | 连带删除其全部版本元数据 |
| 删除单个版本 | `DELETE` | `/api/versions/$version_id` | 清掉历史版本表里某一条 |

> ⚠️ 删除不可恢复，调用前最好让用户确认。`version_id` 可从 `GET /api/apps/$app_id` 的 `versions[].id` 取。

---

## 常见问题

### Q: 上传时提示 version_code 已存在？

A: version_code 必须单调递增且唯一。解决方法：
1. 查看当前最大 version_code：`GET /api/apps/$app_id`
2. bump version_code（+1 或更大）
3. 重试上传

### Q: 如何设置应用为私有？

A: 上传时加 `-F "is_public=0"`，或上传后调用：
```bash
curl -X PUT "$BASE/api/apps/$app_id" -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{"is_public": false}'
```

### Q: 私有应用如何在客户端检查更新？

A: **不要硬编码 token 在客户端**（会被反编译泄露）。建议方案：
1. 通过自有后端中转，后端存 token，客户端请求后端
2. 后端调用商店接口，返回检查结果给客户端

### Q: 下载链接为什么会 302 跳转？

A: 安装包存储在 GitHub Release，商店返回的下载链接会 302 跳转到 GitHub CDN。HTTP 客户端需允许重定向：
- Java `HttpURLConnection`: `instanceFollowRedirects = true`
- OkHttp: 默认允许
- Python `requests`: 默认允许

### Q: 支持哪些安装包格式？

A: 支持所有常见安装包格式：
- Android: `.apk`, `.aab`
- Windows: `.exe`, `.msi`
- macOS: `.dmg`, `.pkg`, `.app`, `.zip`
- Linux: `.deb`, `.rpm`, `.AppImage`, `.snap`, `.flatpak`
- iOS: `.ipa`
- 其他：`.zip`, `.7z`, `.rar`, `.tar.gz`

### Q: 如何删除已发布的版本？

A: 
1. 获取 version_id：`GET /api/apps/$app_id`
2. 删除版本：`DELETE /api/versions/$version_id`
3. 确认：再次 `GET /api/apps/$app_id` 查看版本列表

### Q: 账号激活后能否退款？

A: 支付激活是自动化的，一旦支付成功无法自动退款。如有问题请联系管理员。

---

## 附录：完整示例

### 发布一个 Android 应用

```bash
# 0. 准备
export APPSTORE_URL="https://appstore.qinghuan.fun"
export APPSTORE_TOKEN=""  # 空时自动注册

# 1. 构建
./gradlew assembleRelease

# 2. 读取配置
APK_PATH="./app/build/outputs/apk/release/app-release.apk"
APP_ID="com.example.app"
VERSION_NAME="1.2.0"
VERSION_CODE=12
UPDATE_NOTE="修复登录闪退问题"

# 3. 自动注册 + 激活（如需要）+ 上传
# agent 自动执行，无需手动干预

# 4. 返回结果
✅ 已发布 com.example.app v1.2.0 (code 12)，大小 12.3 MB
📥 下载：https://github.com/.../app-release.apk
🔄 检查更新：https://appstore.qinghuan.fun/api/apps/com.example.app/check-update?versionCode=12
```

### 集成到 Android 应用

```kotlin
// 在 Application 或 MainActivity 中初始化
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        
        // 每天检查一次更新
        checkUpdateIfNeeded()
    }
    
    private fun checkUpdateIfNeeded() {
        val prefs = getSharedPreferences("appstore", MODE_PRIVATE)
        val today = java.text.SimpleDateFormat("yyyyMMdd", Locale.US).format(Date())
        
        if (prefs.getString("last_check", "") != today) {
            lifecycleScope.launch {
                val info = AppStoreUpdateChecker(
                    this@MyApplication,
                    BuildConfig.STORE_BASE,
                    BuildConfig.APP_ID
                ).check()
                
                if (info.hasUpdate) {
                    // 显示更新对话框
                    showUpdateDialog(info)
                }
                
                prefs.edit().putString("last_check", today).apply()
            }
        }
    }
}
```
