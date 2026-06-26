---
name: android-mobpush-integration
description: Interactive guide for integrating MobTech MobPush into Android projects with 6-step workflow. Use when user says "我要在app中增加推送能力", "MobPush集成", "Android推送功能", "配置推送通知", or asks about MobPush setup, Gradle configuration, vendor channels (Xiaomi, Huawei, OPPO, vivo, Meizu, Honor, FCM), push message handling, alias/tags management, or privacy compliance. Supports step-by-step interactive integration with user confirmation at each step.
tags:
  - android
  - mobpush
  - mobtech
  - push-notification
  - gradle
  - privacy
  - interactive-integration
  - vendor-channel
---

# Android MobPush 集成 Skill

## 适用场景

当用户提到以下任一主题时，使用本 skill：

- android mobpush
- MobPush 集成
- MobPush 推送 SDK 接入
- Android 推送通知配置
- MobPush 的 Gradle 配置
- MobPush appKey / appSecret 配置
- MobPush 隐私合规
- 厂商通道配置（小米、华为、OPPO、vivo、魅族、荣耀）
- FCM 推送集成
- 推送消息接收与处理
- 别名/标签设置
- **我要在app中增加推送能力**
- **我要在Android项目中接入推送功能**
- **帮我配置推送通知**
- **一键集成 MobPush**
- **快速接入 MobPush**
- **自动配置 MobPush**

如果用户问题明确与 Android 的 MobPush 接入、工程配置、推送功能、厂商通道、消息处理有关，应优先使用本 skill。

---

## 6 步交互式集成工作流

当用户表达集成 MobPush 的意图时，执行以下 6 步交互式流程。每步操作前都需要展示内容给用户确认，获得明确同意后再执行。

---

### 步骤 1：启动流程

#### 1-1 触发识别

用户可能通过以下方式表达集成意图：
- "我要在app中增加推送能力"
- "帮我集成 MobPush 到 Android 项目"
- "配置推送通知"
- "一键集成 MobPush"
- "Android 推送功能怎么接入"

#### 1-2 询问项目路径

**主动询问用户**：

```
我来帮你集成 MobPush 推送功能。

请提供需要集成的 Android 项目根路径，例如：
/Users/xxx/your-android-project

请确保项目包含 app/build.gradle 文件。
```

#### 1-3 验证路径合法性

**验证逻辑**：
1. 检查路径是否存在
2. 检查路径下是否有 `app/build.gradle` 或 `settings.gradle` 文件
3. 检查是否为有效的 Android 项目结构

**如果路径不合法**：
```
路径验证失败，可能原因：
- 路径不存在：{path}
- 未找到 app/build.gradle 文件，请确认这是 Android 项目根目录

请重新提供正确的项目路径。
```

**如果路径合法**：进入步骤 2

---

### 步骤 2：注册 MobPush 配置信息

#### 2-1 生成配置模板文件

**操作**：
1. 执行 `assets/generate_excel_template.py`，生成 `assets/MobPush_Config_Template.xlsx`
2. 将生成的 `assets/MobPush_Config_Template.xlsx` 复制到 `{path}` 下
3. 在 `{path}` 下命名为 `MobPush_Config.xlsx`

**告知用户**：
```
已在你项目的根目录生成 {path}/MobPush_Config.xlsx 配置文件。

请打开该文件，按以下步骤填写：
1. 在"基础信息"Sheet 中填写 MobTech 的 appKey 和 appSecret
   （从 https://www.mob.com/ 注册应用获取）
2. 填写 Android 包名和签名 MD5
3. 在各厂商通道 Sheet 中填写需要启用的通道配置
   （不需要的通道可留空或填写"否"）
4. "隐私合规"Sheet 中有隐私政策说明
5. "填写说明"Sheet 中有各 Sheet 的详细说明

填写完成后告诉我"填好了"，我将继续下一步。
```

#### 2-2 等待用户填写完成

等待用户回复"填好了"或类似表达。

#### 2-3 读取并验证配置

**操作**：读取用户项目根目录的 `MobPush_Config.xlsx` 文件

**验证规则**：

| 检查项 | 规则 | 不通过时的提示 |
|--------|------|---------------|
| appKey | 必填，不能为空字符串 | "基础信息 Sheet 中的 appKey 未填写，请从 MobTech 官网获取" |
| appSecret | 必填，不能为空字符串 | "基础信息 Sheet 中的 appSecret 未填写" |
| 包名 | 必填，格式应为 com.xxx.xxx | "包名格式不正确，应为 com.xxx.xxx 格式" |

**类型转换规则**：
- `appKey`、`appSecret`、`appId`、`appKey`、`appSecret`、`包名` 等标识符字段：**强制转为字符串**，即使 Excel 中填写的是数字，也要转为 `"字符串"`
- `启用` 字段：转为布尔值，`是`/`true` -> `true`，`否`/`false` -> `false`

**如果不合法**：
```
配置信息验证失败，请修正以下问题：

{具体问题列表}
- 第 1 条：{问题描述}
- 第 2 条：{问题描述}

请修改 Excel 文件后保存，然后重新告诉我"填好了"。
```

**如果合法**：提取配置信息，进入步骤 3

---

### 步骤 3：完成 SDK 集成

#### 3-1 项目级 Gradle 配置

根据项目 AGP 版本（通过检查 `gradle/wrapper/gradle-wrapper.properties` 中的 distributionUrl 判断），选择对应配置方式。

**【7.0及以上版本】**
1. 打开项目级 `settings.gradle` 文件，配置 Maven 仓地址，注意修改 `repositoriesMode` 为 `RepositoriesMode.PREFER_SETTINGS`。
```groovy
pluginManagement {
    repositories {
        gradlePluginPortal()
        google()
        mavenCentral()
        maven {
            url "https://mvn.zztfly.com/android"
        }
    }
}
dependencyResolutionManagement {
    // repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositoriesMode.set(RepositoriesMode.PREFER_SETTINGS)
    repositories {
        gradlePluginPortal()
        google()
        mavenCentral()
        maven {
            url "https://mvn.zztfly.com/android"
        }
    }
}
```
2. 打开项目级 `build.gradle` 文件，配置 FlySDK 插件地址：
```groovy
buildscript {
    dependencies {
        // 增加 FlySDK 插件配置
        classpath 'cn.fly.sdk:FlySDK:+'
        // 增加 google services 插件配置，用于集成 FCM（不集成 FCM 可不配置）
        classpath 'com.google.gms:google-services:4.3.14'
    }
}
```

**AGP 9.0+ 额外补充：**
如 AGP 版本 ≥ 9.0，需在 `gradle.properties` 文件中添加以下配置，否则可能遇到 SDK 配置信息失效的情况：
```properties
android.newDsl=false
```

**【7.0以下版本】**
1. 打开项目级 `build.gradle` 文件：
1.1 在 `allprojects -> repositories` 中配置 Maven 仓地址：
```groovy
   allprojects {
       repositories {
           maven {
               url "https://mvn.zztfly.com/android"
           }
       }
   }
```
1.2 在 `buildscript -> repositories` 中配置 Maven 仓地址：
```groovy
buildscript {
    repositories {
        maven {
            url "https://mvn.zztfly.com/android"
        }
    }
}
```
1.3 在 `buildscript -> dependencies` 中配置 FlySDK 插件：
```groovy
buildscript {
    dependencies {
        // 增加 FlySDK 插件配置
        classpath 'cn.fly.sdk:FlySDK:+'
    }
}
```


#### 3-2 应用级 build.gradle 配置

在 `app/build.gradle` 中添加插件和 FlySDK 配置块。

**生成规则**：
1. **类型转换**：`appKey`、`appSecret` 等标识符：**强制转为字符串**（加引号）
2. **已启用厂商通道**：根据 Excel 中填写的厂商生成完整配置块
3. **未启用厂商通道**：以注释形式填充到 `MobPush` 中，方便后续启用：
   ```groovy
   MobPush {
       // 已启用的厂商通道配置
       {已启用厂商配置块}

       // ========== 以下厂商通道未启用，取消注释并填写参数即可使用 ==========

       // HUAWEI {
       //     appId ""
       //     appSecret ""
       // }

       // XIAOMI {
       //     appId ""
       //     appKey ""
       //     appSecret ""
       // }

       // OPPO {
       //     appId ""
       //     appKey ""
       //     appSecret ""
       //     masterSecret ""
       // }

       // VIVO {
       //     appId ""
       //     appKey ""
       //     appSecret ""
       // }

       // MEIZU {
       //     appId ""
       //     appKey ""
       //     appSecret ""
       // }

       // HONOR {
       //     appId ""
       //     appSecret ""
       //     clientId ""
       //     clientSecret ""
       // }

       // FCM {
       //     // 需在 MobTech 后台上传 google-services.json 并配置
       // }
   }
   ```

**展示内容**（根据用户填写的 Excel 信息动态生成）：
```groovy
// 在文件开头添加插件
apply plugin: 'cn.fly.sdk'
// 或
// plugins {
//     id 'cn.fly.sdk'
// }

// 在文件末尾添加 FlySDK 配置
FlySDK {
    appKey "{用户填写的appKey}"
    appSecret "{用户填写的appSecret}"

    MobPush {
        // 已启用的厂商通道配置
        {已启用厂商配置块}

        // ========== 以下厂商通道未启用，取消注释并填写参数即可使用 ==========

        // 未启用的厂商通道（注释形式）
        {未启用厂商注释块}
    }
}
```

**询问**：`以上是要添加到 app/build.gradle 的内容，是否确认修改？`

#### 3-3 gradle.properties 配置

**主动询问用户**：
```
你的应用是否需要上架 Google Play？
- 是：将使用 GPP（Google Play Policy）合规版本
- 否：将使用 FP（Full Package）版本
```

如果开发者回答：**是 / YES**

```properties
MobSDK.spEdition=GPP
```

如果开发者回答：**否 / NO**
```properties
MobSDK.spEdition=FP
```

#### 3-4 混淆配置

在 `proguard-rules.pro` 中添加以下混淆规则：
```proguard
-keep class com.mob.** { *; }
-dontwarn com.mob.**
```

至此，Gradle 配置已全部完成。
---

#### 3-5 执行 Gradle Sync

**说明**：修改 build.gradle 后，需要同步 Gradle 配置才能生效：
- 命令行 `./gradlew`：下载依赖、编译代码
- Android Studio Sync：让 IDE 解析 build.gradle 配置，更新项目结构索引

两者作用不同，即使命令行成功，仍建议在 Android Studio 中执行 Sync。

**尝试自动执行**：
```bash
cd {project_path}
./gradlew --refresh-dependencies
```

**如果成功**：
```
命令行 Gradle Sync 成功，依赖已拉取。

⚠️ 如果你在 Android Studio 中开发，请再执行一次 IDE Sync：
1. 打开 Android Studio
2. 点击菜单栏 File -> Sync Project with Gradle Files
3. 或点击右上角大象图标（Sync Now）
```

**如果失败**：
```
自动 Gradle Sync 失败，可能原因：
- Gradle 未配置环境变量
- 网络问题无法下载依赖

请在 Android Studio 中手动执行：
1. 打开项目
2. 点击菜单栏 File -> Sync Project with Gradle Files
3. 或点击 Gradle 面板中的刷新按钮
```

进入步骤 4

---

### 步骤 4：日志调试

请在AndroidManifest.xml文件中 <application>下添加上面配置,在日志控制台即可查看到TAG为MobPushLog的相关日志：
```xml
<meta-data
      android:name="com.mob.mobpush.debugLevel"
      android:value="4" />
```

**询问**："是否需要在 AndroidManifest.xml 中添加以上配置？"

进入步骤 5

---

### 步骤 5：插入隐私授权回调

#### 5-1 说明合规原因

**向用户说明**：
```
根据 MobTech 隐私合规要求和中国区 App 上架规范，使用 MobPush 需要在用户同意隐私政策后才能初始化 SDK。

你需要在 App 中：
1. 首次启动时展示《隐私政策》弹窗
2. 用户点击"同意"按钮后，调用隐私授权代码
3. 用户点击"不同意"则不应调用

请告知我：用户点击隐私政策"同意"按钮的回调代码在哪个文件、哪个方法中？
例如：MainActivity.java 的 onPrivacyAgreed() 方法 或具体文件:行号如: com/mob/kit/app/MainActivity.java:64
```

#### 5-2 询问回调位置

等待用户告知具体的文件路径和方法名。

#### 5-3 展示并确认插入代码

**展示要插入的代码**：
```java
// 用户同意隐私政策后调用
MobSDK.submitPolicyGrantResult(true);
```

**完整示例**：
```java
public void onPrivacyAgreed() {
    // 用户点击同意按钮
    
    // === MobPush 隐私授权 ===
    com.mob.MobSDK.submitPolicyGrantResult(true);
    // =======================
    
    // 其他业务逻辑...
}
```

**询问**："以上代码将插入到 {文件} 的 {方法} 中，是否确认？"

#### 5-4 执行插入

用户确认后，将代码插入指定位置。

进入步骤 6

---
### 步骤6: SDK API接入


推送监听接口
添加推送监听
功能说明
添加推送监听，消息下发到设备，可根据推送监听进行业务逻辑操作
自定义消息到达(透传消息)、通知消息到达、通知栏消息点击、增删别名、增删标签事件。
参数说明
参数	类型	描述
mobPushReceiver	MobPushReceiver	注册推送监听
示例代码
```java
/**
 * import com.mob.pushsdk.MobPushReceiver;
 * import com.mob.pushsdk.PushReceiver;
 */
public static void addPushReceiver(MobPushReceiver mobPushReceiver)
PushReceiver mobPushReceiver = new PushReceiver() {

    @Override
    public void onCommandReceive(int type, Map<String, Object> map) {
        //接收MobPush内部消息
        //type   内部消息的类型
        //map    内部消息的数组
        map.get(PushReceiver.KEY_CHANNEL);//channel
        if (type == 1 || type == 2) {
            //Mob或者厂商 Token改变
            map.get(PushReceiver.KEY_TOKEN);//token
        } else if (type == 3) {
            //三方sdk初始化失败
            map.get(PushReceiver.KEY_MESSAGE);//失败原因
        }
    }

    @Override
    public void onCustomMessageReceive(Context context, MobPushCustomMessage message) {
        //接收到自定义消息（透传消息）
        message.getMessageId();//获取任务ID
        message.getContent();//获取推送内容
    }

    @Override
    public void onNotifyMessageReceive(Context context, MobPushNotifyMessage message) {
        //通知消息到达
        message.getMobNotifyId();//获取消息ID
        message.getMessageId();//获取任务ID
        message.getTitle();//获取推送标题
        message.getContent();//获取推送内容
    }

    @Override
    public void onNotifyMessageOpenedReceive(Context context, MobPushNotifyMessage message) {
        //通知被点击事件
        message.getMobNotifyId();//获取消息ID
        message.getMessageId();//获取任务ID
        message.getTitle();//获取推送标题
        message.getContent();//获取推送内容
    }

    @Override
    public void onTagsCallback(Context context, String[] tags, int operation, int errorCode) {
        //标签操作回调
        //tags    已添加的标签集合
        //operation    0:获取标签 1:设置标签 2:删除标签
        //errorCode    0:操作成功 其它:操作失败
    }

    @Override
    public void onAliasCallback(Context context, String alias, int operation, int errorCode) {
        //别名操作回调
        //alias    对应的别名
        //operation    0:获取别名 1:设置别名 2:删除别名
        //errorCode    0:操作成功 其它:操作失败
    }
};

MobPush.addPushReceiver(mobPushReceiver);
```
注销推送监听
功能说明
注销推送监听，在应用销毁时调用注销函数，注销已添加过的推送监听。
参数说明
|参数 | 类型 | 描述 |
| mobPushReceiver |	MobPushReceiver	| 注销推送监听 |
示例代码
```java
/**
 * import com.mob.pushsdk.MobPushReceiver;
 */
public static void removePushReceiver(MobPushReceiver mobPushReceiver)
MobPush.removePushReceiver(mobPushReceiver);

```
转发厂商消息
功能说明
MobPush 4.6.14+版本，对推送回调进行了整合，TCP消息和厂商均可以在MobPushReceiver处理，需要注意的是，解析intent位置需要进行消息转发, 也可以参考最佳实践模块
参数说明
|参数 |	类型 | 描述 |
| Intent | Intent | 厂商消息解析页面的Intent |
		
示例代码
public static void parseManufacturerMessage(final Intent var0)
MobPush.parseManufacturerMessage(getIntent());

进入步骤7

---

### 步骤 7：补充说明

#### 7-1 生成项目级 README

**操作**：在用户项目根目录生成 `MOBPUSH_README.md`，内容包含集成说明、关键文件位置、后续修改指引。

填充以下信息：
- 项目路径
- 集成的 SDK 配置（appKey、appSecret）
- 隐私回调文件和方法
- 配置的厂商通道列表
- 官方文档链接

#### 7-2 完成告知

**向用户说明**：
```
MobPush 集成已完成！

📁 生成的文件：
- {project_path}/MOBPUSH_README.md — 集成说明文档

📝 后续修改位置：
- 修改 SDK 配置：app/build.gradle 中的 `FlySDK { }` 块
- 修改隐私授权位置：{privacy_file} 的 {privacy_method} 方法
- 修改厂商通道配置：app/build.gradle 中的 `MobPush { }` 块
- 修改 Google Play 版本配置：`gradle.properties` 中的 `MobSDK.spEdition`

📖 更多帮助：
- 官方文档：https://www.mob.com/wiki/detailed?wiki=498&id=136
- 厂商通道配置：https://www.mob.com/wiki/detailed?wiki=517&id=136
- 合规指南：https://www.mob.com/wiki/detailed?wiki=421&id=717

⚠️ 重要提醒：
1. 确保包名与 MobTech 后台配置一致
2. 确保签名 MD5 与后台配置一致
3. 确保 App 有隐私政策并在用户同意后调用隐私授权代码
4. Android 13+ 需动态申请通知权限
5. 华为/荣耀通道需在厂商后台开启回执状态
```

---

## 附录：技术参考

### A. Gradle 配置参考

#### A.1 Gradle 插件 7.0 及以上

在 `settings.gradle` 第1行开始填充：

```groovy
pluginManagement {
    repositories {
        gradlePluginPortal()
        google()
        mavenCentral()
        maven { url "https://mvn.zztfly.com/android" }
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.PREFER_SETTINGS)
    repositories {
        gradlePluginPortal()
        google()
        mavenCentral()
        maven { url "https://mvn.zztfly.com/android" }
    }
}
```

在项目级 `build.gradle` 中：

```groovy
buildscript {
    dependencies {
        classpath 'cn.fly.sdk:FlySDK:+'
    }
}
```

#### A.2 Gradle 插件 7.0 以下

在项目级 `build.gradle` 中配置：

```groovy
allprojects {
    repositories {
        maven { url "https://mvn.zztfly.com/android" }
    }
}
buildscript {
    repositories {
        maven { url "https://mvn.zztfly.com/android" }
    }
    dependencies {
        classpath 'cn.fly.sdk:FlySDK:+'
    }
}
```

#### A.3 应用级启用插件

```groovy
apply plugin: 'cn.fly.sdk'
```

#### A.4 gradle.properties 配置

上架 Google Play 时使用：
```properties
MobSDK.spEdition=GPP
```

不上架 Google Play 时使用：
```properties
MobSDK.spEdition=FP
```

---

### B. 厂商通道详细配置

#### B.1 华为通道

1. 在华为开发者联盟注册应用，获取 **App ID** 和 **Client Secret**
2. 在华为后台配置 **SHA256 证书指纹**
3. 在 MobTech 后台配置华为参数
4. 在 Gradle 中添加 HUAWEI 配置块
5. 在华为后台开启 **回执状态**（否则无法统计送达数据）

```groovy
HUAWEI {
    appId "替换为华为AppID"
    appSecret "替换为华为Client Secret"
}
```

#### B.2 小米通道

1. 在小米开放平台注册应用，获取 **AppID**、**AppKey**、**AppSecret**
2. 在 MobTech 后台配置小米参数
3. 在 Gradle 中添加 XIAOMI 配置块

```groovy
XIAOMI {
    appId "替换为小米AppID"
    appKey "替换为小米AppKey"
    appSecret "替换为小米AppSecret"
}
```

#### B.3 OPPO 通道

1. 在 OPPO 开放平台注册应用，获取 **AppID**、**AppKey**、**AppSecret**、**MasterSecret**
2. 在 MobTech 后台配置 OPPO 参数
3. 在 Gradle 中添加 OPPO 配置块
4. **注意**：Android 8.0+ 必须适配通知渠道

```groovy
OPPO {
    appId "替换为OPPO AppID"
    appKey "替换为OPPO AppKey"
    appSecret "替换为OPPO AppSecret"
    masterSecret "替换为OPPO MasterSecret"
}
```

#### B.4 vivo 通道

1. 在 vivo 开放平台注册应用，获取 **AppID**、**AppKey**、**AppSecret**
2. 在 MobTech 后台配置 vivo 参数
3. 在 Gradle 中添加 VIVO 配置块

```groovy
VIVO {
    appId "替换为vivo AppID"
    appKey "替换为vivo AppKey"
    appSecret "替换为vivo AppSecret"
}
```

#### B.5 魅族通道

1. 在魅族开放平台注册应用，获取 **AppID**、**AppKey**、**AppSecret**
2. 在 MobTech 后台配置魅族参数
3. 在 Gradle 中添加 MEIZU 配置块

```groovy
MEIZU {
    appId "替换为魅族AppID"
    appKey "替换为魅族AppKey"
    appSecret "替换为魅族AppSecret"
}
```

#### B.6 荣耀通道

1. 在荣耀开发者平台注册应用，获取 **APP ID**、**APP Secret**、**Client ID**、**Client Secret**
2. 在荣耀后台配置回执状态
3. 在 MobTech 后台配置荣耀参数
4. 在 Gradle 中添加 HONOR 配置块
5. **注意**：仅支持 Magic UI 4.0 及以上版本

```groovy
HONOR {
    appId "替换为荣耀APP ID"
    appSecret "替换为荣耀APP Secret"
    clientId "替换为荣耀Client ID"
    clientSecret "替换为荣耀Client Secret"
}
```

#### B.7 FCM 通道

1. 在 Firebase 控制台创建项目
2. 下载 `google-services.json` 放入 app 模块
3. 生成服务账号私钥证书
4. 在 MobTech 后台上传私钥证书
5. 在 Gradle 中添加 FCM 配置块

```groovy
FCM {
    // 需在后台上传服务账号私钥证书
}
```

---

### C. 推送消息接收处理

创建自定义 Receiver implements `PushReceiver`：

```java
import com.mob.pushsdk.MobPushCustomMessage;
import com.mob.pushsdk.MobPushNotifyMessage;
import com.mob.pushsdk.PushReceiver;

public class MyPushReceiver implements PushReceiver {
    
     @Override
    public void onCommandReceive(int type, Map<String, Object> map) {
        //接收MobPush内部消息
        //type   内部消息的类型
        //map    内部消息的数组
        map.get(PushReceiver.KEY_CHANNEL);//channel
        if (type == 1 || type == 2) {
            //Mob或者厂商 Token改变
            map.get(PushReceiver.KEY_TOKEN);//token
        } else if (type == 3) {
            //三方sdk初始化失败
            map.get(PushReceiver.KEY_MESSAGE);//失败原因
        }
    }

    @Override
    public void onCustomMessageReceive(Context context, MobPushCustomMessage message) {
        //接收到自定义消息（透传消息）
        message.getMessageId();//获取任务ID
        message.getContent();//获取推送内容
    }

    @Override
    public void onNotifyMessageReceive(Context context, MobPushNotifyMessage message) {
        //通知消息到达
        message.getMobNotifyId();//获取消息ID
        message.getMessageId();//获取任务ID
        message.getTitle();//获取推送标题
        message.getContent();//获取推送内容
    }

    @Override
    public void onNotifyMessageOpenedReceive(Context context, MobPushNotifyMessage message) {
        //通知被点击事件
        message.getMobNotifyId();//获取消息ID
        message.getMessageId();//获取任务ID
        message.getTitle();//获取推送标题
        message.getContent();//获取推送内容
    }

    @Override
    public void onTagsCallback(Context context, String[] tags, int operation, int errorCode) {
        //标签操作回调
        //tags    已添加的标签集合
        //operation    0:获取标签 1:设置标签 2:删除标签
        //errorCode    0:操作成功 其它:操作失败
    }

    @Override
    public void onAliasCallback(Context context, String alias, int operation, int errorCode) {
        //别名操作回调
        //alias    对应的别名
        //operation    0:获取别名 1:设置别名 2:删除别名
        //errorCode    0:操作成功 其它:操作失败
    }
}
```

注册和注销 Receiver：

```java
// 注册推送监听
MobPushReceiver receiver = new MyPushReceiver();
MobPush.addPushReceiver(receiver);

// 在页面销毁时注销
MobPush.removePushReceiver(receiver);
```

---

### D. 别名与标签管理

#### D.1 别名设置

```java
// 设置别名（唯一标识，与 RegistrationId 一对一）
MobPush.setAlias("user_123");

// 获取别名
MobPush.getAlias();

// 删除别名
MobPush.deleteAlias();
```

#### D.2 标签管理

```java
// 添加标签
MobPush.addTags(new String[]{"vip", "beijing"});

// 删除指定标签
MobPush.deleteTags(new String[]{"vip"});

// 清空所有标签
MobPush.cleanTags();

// 获取所有标签
MobPush.getTags();
```

---

### E. 隐私合规要求

必须提醒用户：

1. App 需要有《隐私政策》
2. 首次冷启动展示隐私政策并获取用户同意
3. 同意后调用 `MobSDK.submitPolicyGrantResult(true)`
4. 不同意时不能调用该方法

在隐私政策中应包含：
- 使用了 MobTech MobPush 服务
- 用于消息推送、通知提醒等功能
- 可能会收集相关信息

完整合规指南：https://www.mob.com/wiki/detailed?wiki=421&id=717

---

### F. 混淆配置

在 `proguard-rules.pro` 中添加：

```proguard
# MobPush
-keep class com.mob.pushsdk.** { *; }
-keep class com.mob.** { *; }
-dontwarn com.mob.**

# 厂商通道
-keep class com.huawei.** { *; }
-keep class com.xiaomi.** { *; }
-keep class com.oppo.** { *; }
-keep class com.vivo.** { *; }
-keep class com.meizu.** { *; }
-keep class com.hihonor.** { *; }
-dontwarn com.huawei.**
-dontwarn com.xiaomi.**
-dontwarn com.oppo.**
-dontwarn com.vivo.**
-dontwarn com.meizu.**
-dontwarn com.hihonor.**
```

---

### G. 常见问题排查

| 问题 | 可能原因 |
|------|----------|
| 收不到推送 | 签名MD5不一致、包名不一致、appKey/appSecret错误 |
| 厂商推送失败 | 厂商参数错误、未配置回执状态 |
| Android 13+ 无通知 | 未动态申请 POST_NOTIFICATIONS 权限 |
| OPPO 无回调 | OPPO 不支持通知和打开通知的回调 |
| 荣耀推送失败 | 仅支持 Magic UI 4.0 及以上版本 |

---

## 回答边界

- 仅聚焦 Android MobPush 工程集成与合规
- 不扩展到 iOS、服务端、非 MobTech SDK
- 不伪造真实账号、密钥、签名值
