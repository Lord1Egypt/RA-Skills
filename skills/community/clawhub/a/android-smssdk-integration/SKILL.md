---
name: android-smssdk-integration
description: Interactive guide for integrating MobTech SMSSDK (短信验证) into Android projects with 6-step workflow. Use when user says "我要在app中增加短信验证", "SMSSDK集成", "Android短信验证码", "配置短信验证", or asks about SMSSDK setup, Gradle configuration, SMS verification, MobSDK appKey, privacy compliance. Supports step-by-step interactive integration with user confirmation at each step.
tags:
  - android
  - smssdk
  - mobtech
  - sms-verification
  - mobile-verification
  - gradle
  - privacy
  - interactive-integration
---

# Android SMSSDK (短信验证) 集成 Skill

## 适用场景

当用户提到以下任一主题时，使用本 skill：

- android smssdk
- 短信验证集成
- 短信验证码
- 语音验证码
- SMSSDK SDK 接入
- **我要在app中增加短信验证**
- **我要在Android项目中接入短信验证码功能**
- **帮我配置短信验证**
- **一键集成 SMSSDK**
- **快速接入短信验证**
- **自动配置 SMSSDK**

如果用户问题明确与 Android 的短信验证接入、工程配置、验证码功能、自定义 UI 有关，应优先使用本 skill。

---

## 6 步交互式集成工作流

当用户表达集成 SMSSDK 的意图时，执行以下 6 步交互式流程。每步操作前都需要展示内容给用户确认，获得明确同意后再执行。

---

### 步骤 1：启动流程

#### 1-1 触发识别

用户可能通过以下方式表达集成意图：
- "我要在app中增加短信验证"
- "帮我集成 SMSSDK 到 Android 项目"
- "配置短信验证"
- "一键集成短信验证"
- "Android 短信验证码功能怎么接入"

#### 1-2 询问项目路径

**主动询问用户**：

```
我来帮你集成 SMSSDK 短信验证功能。

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

### 步骤 2：注册 SMSSDK 配置信息

#### 2-1 生成配置模板文件

**操作**：
1. 在 skill 目录中运行 Python 脚本生成 `SMSSDK_Config_Template.xlsx`
   ```bash
   python {skill_dir}/assets/generate_excel_template.py
   ```
2. 将生成的 `SMSSDK_Config_Template.xlsx` 复制到用户项目根目录，命名为 `SMSSDK_Config.xlsx`

**告知用户**：
```
已在你项目的根目录生成 {path}/SMSSDK_Config.xlsx 配置文件。

请打开该文件，按以下步骤填写：
1. 在"基础信息"Sheet 中填写 MobTech 的 appKey 和 appSecret
   （从 https://www.mob.com/ 注册应用获取）
2. 填写 Android 包名
3. "短信签名审核"Sheet 中填写短信签名信息（企业需审核，个人使用默认【掌淘科技】）
4. "填写说明"Sheet 中有详细说明

⚠️ 重要提醒：
- 短信签名审核通过后才能正常下发短信
- 请前往 MobTech 开发者工作台提交短信签名审核
- 国际短信签名无需审核，直接自行输入英文即可

填写完成后告诉我"填好了"，我将继续下一步。
```

#### 2-2 等待用户填写完成

等待用户回复"填好了"或类似表达。

#### 2-3 读取并验证配置

**操作**：读取用户项目根目录的 `SMSSDK_Config.xlsx` 文件

**验证规则**：

| 检查项 | 规则 | 不通过时的提示 |
|--------|------|---------------|
| appKey | 必填，不能为空字符串 | "基础信息 Sheet 中的 appKey 未填写，请从 MobTech 官网获取" |
| appSecret | 必填，不能为空字符串 | "基础信息 Sheet 中的 appSecret 未填写" |
| 包名 | 必填，格式应为 com.xxx.xxx | "包名格式不正确，应为 com.xxx.xxx 格式" |

**类型转换规则**：
- `appKey`、`appSecret`、`包名` 等标识符字段：**强制转为字符串**（加引号）

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

#### 3-1 Gradle 环境配置

根据项目 AGP 版本（通过检查 `gradle/wrapper/gradle-wrapper.properties` 中的 distributionUrl 判断），选择对应配置方式。

**【7.0及以上版本】**

##### 文件 1：settings.gradle（AGP 7.0+）

**展示内容**：
```groovy
pluginManagement {
    repositories {
        gradlePluginPortal()
        google()
        mavenCentral()
        maven { url "https://mvn.mob.com/android" }
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.PREFER_SETTINGS)
    repositories {
        gradlePluginPortal()
        google()
        mavenCentral()
        maven { url "https://mvn.mob.com/android" }
    }
}
```

##### 文件 2：项目级 build.gradle

**展示内容**：
```groovy
buildscript {
    dependencies {
        // 增加 MobSDK 插件配置
        classpath "com.mob.sdk:MobSDK2:+"
        // 如需集成 FCM，增加以下配置（非必须）
        classpath 'com.google.gms:google-services:4.3.14'
    }
}
```

**7.0以下版本**

在项目级 `build.gradle` 中配置：

```groovy
allprojects {
    repositories {
        maven { url "https://mvn.mob.com/android" }
    }
}

buildscript {
    repositories {
        maven { url "https://mvn.mob.com/android" }
    }
    dependencies {
        // 增加 MobSDK 插件配置
        classpath "com.mob.sdk:MobSDK2:+"
    }
}
```

##### 文件 3：gradle.properties

**主动询问是否上架googleplay**
如果开发者回答:是/YES 
则配置

```properties
MobSDK.spEdition=GPP
```

否则(否/NO): 则使用如下配置
```properties
MobSDK.spEdition=FP
```

##### 文件 4：app/build.gradle

**生成规则**：
1. **类型转换**：`appKey`、`appSecret` 等标识符：**强制转为字符串**（加引号）

**展示内容**：
```groovy
// 在文件开头添加插件（根据你的 plugins 块结构选择一种）

// 方式 A
apply plugin: 'com.mob.sdk'

// 方式 B
plugins {
    id 'com.android.application'
    id 'com.mob.sdk'
}

// 在文件末尾添加 MobSDK 配置代码
MobSDK {
    appKey "{用户填写的appKey}"
    appSecret "{用户填写的appSecret}"
    SMSSDK {}
}
```

**询问**："以上是要添加到 app/build.gradle 的内容，是否确认修改？"

#### 3-2 执行 Gradle Sync

**说明**：修改 build.gradle 后，需要同步 Gradle 配置才能生效：
- 命令行 `./gradlew`：下载依赖、编译代码
- Android Studio Sync：让 IDE 解析 build.gradle 配置，更新项目结构索引

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
至此，Gradle集成方式环境搭建已经完成。

进入步骤 4

---

### 步骤 4：补充隐私合规

#### 4-1 说明隐私授权

**向用户说明**：
```
根据工信部合规要求和 MobTech 隐私合规规范，使用 SMSSDK 需要在用户同意《隐私政策》后才能初始化 SDK。

你需要在 App 中：
1. 首次启动时展示《隐私政策》弹窗
2. 用户点击"同意"按钮后，调用隐私授权代码
3. 用户点击"不同意"则不应调用

请告知我：用户点击隐私政策"同意"按钮的回调代码在哪个文件、哪个方法中？
例如：MainActivity.java 的 onPrivacyAgreed() 方法
```

等待用户告知具体的文件路径和方法名。

**展示要插入的代码**：
```java
// 用户同意隐私政策后调用
MobSDK.submitPolicyGrantResult(true);
```

**完整示例**：
```java
public void onPrivacyAgreed() {
    // 用户点击同意按钮
    
    // === SMSSDK 隐私授权 ===
    MobSDK.submitPolicyGrantResult(true);
    // ==========================
    
    // 其他业务逻辑...
}
```

#### 4-2 确认隐私授权代码

**询问**：`"以上代码将插入到 {文件} 的 {方法} 中，是否确认？"`

#### 4-3 执行插入

用户确认后，将代码插入指定位置。

进入步骤 5

---

### 步骤 5：插入短信验证代码

#### 5-1 询问集成方式

**说明**：SMSSDK 支持两种使用方式：
1. **自带 UI 页面**（快速集成）：SDK 提供默认注册页面，一行代码拉起
2. **自定义集成**（灵活定制）：自己写 UI，调用 SDK 底层接口

**询问**：`"请选择集成方式：\n1. 自带 UI 页面（快速，一行代码拉起默认注册页）\n2. 自定义集成（灵活，自己写 UI + 调用底层接口）\n\n回复 1 或 2。"`

#### 5-2 方式一：自带 UI 页面

**等待用户告知**：要插入代码的文件路径和方法名。

**展示要插入的代码**：
```java
// === SMSSDK 自带 UI 页面 ===
RegisterPage page = new RegisterPage();
page.setTempCode(null); // 未申请模板编号时传 null
page.setRegisterCallback(new EventHandler() {
    @Override
    public void afterEvent(int event, int result, Object data) {
        if (result == SMSSDK.RESULT_COMPLETE) {
            // 成功回调
            if (event == SMSSDK.EVENT_SUBMIT_VERIFICATION_CODE) {
                // 提交验证码成功
            } else if (event == SMSSDK.EVENT_GET_VERIFICATION_CODE) {
                // 获取验证码成功
            }
        } else {
            // 失败回调
            ((Throwable) data).printStackTrace();
        }
    }
});
page.show(context);
// ==========================
```

**询问**：`"以上代码将插入到 {文件} 的 {方法} 中，是否确认？"`

用户确认后，将代码插入指定位置。

#### 5-3 方式二：自定义集成

**等待用户告知**：要插入代码的文件路径和方法名。

**展示要插入的代码**：

**注册 EventHandler**：
```java
// 注册短信回调（建议在 onCreate 中调用）
EventHandler eh = new EventHandler() {
    @Override
    public void afterEvent(int event, int result, Object data) {
        if (result == SMSSDK.RESULT_COMPLETE) {
            // 成功回调
            if (event == SMSSDK.EVENT_SUBMIT_VERIFICATION_CODE) {
                // 提交验证码成功
                // TODO 利用验证码进行后续操作
            } else if (event == SMSSDK.EVENT_GET_VERIFICATION_CODE) {
                // 获取验证码成功
                // TODO 提示用户查收短信
            } else if (event == SMSSDK.EVENT_GET_VOICE_VERIFICATION_CODE) {
                // 获取语音验证码成功
            } else if (event == SMSSDK.EVENT_GET_SUPPORTED_COUNTRIES) {
                // 返回支持发送验证码的国家列表
            }
        } else {
            // 失败回调
            ((Throwable) data).printStackTrace();
        }
    }
};
SMSSDK.registerEventHandler(eh);
```

**获取验证码**：
```java
// 请求文本验证码（不带模板编号）
SMSSDK.getVerificationCode("86", "手机号");

// 请求语音验证码（需先发送完文本验证码）
SMSSDK.getVoiceVerifyCode("86", "手机号");

// 提交验证码
SMSSDK.submitVerificationCode("86", "手机号", "验证码");
```

**注销监听**（建议在 Activity 的 onDestroy 中调用）：
```java
SMSSDK.unregisterEventHandler(eh);
```

**询问**：`"以上代码将插入到 {文件} 的 {方法} 中，是否确认？"`

用户确认后，将代码插入指定位置。

进入步骤 6

---

### 步骤 6：完成集成

#### 6-1 生成项目级 README

**操作**：在用户项目根目录生成 `SMSSDK_README.md`，内容包含集成说明、关键文件位置、后续修改指引。

#### 6-2 完成告知

**向用户说明**：
```
SMSSDK 集成已完成！

📁 生成的文件：
- {project_path}/SMSSDK_README.md — 集成说明文档

📝 后续修改位置：
- 修改 SDK 配置：app/build.gradle 中的 MobSDK { } 块
- 修改隐私授权位置：{privacy_file} 的 {privacy_method} 方法
- 修改短信回调：{callback_file} 的 {callback_method} 方法

📖 更多帮助：
- 短信验证集成指南：https://mob.com/wiki/detailed?wiki=440&id=23
- SDK API：https://mob.com/wiki/detailed?wiki=440&id=23
- 产品简介：https://mob.com/wiki/detailed?wiki=163&id=23
- 合规指南：https://mob.com/wiki/detailed?wiki=210&id=23
- 服务端验证 API：https://mob.com/wiki/detailed?wiki=112&id=23
- 短信设置：https://mob.com/wiki/detailed?wiki=452&id=23
- 常见问题：https://mob.com/wiki/detailed?wiki=123&id=23

⚠️ 重要提醒：
1. 确保短信签名审核已通过（否则无法正常下发短信）
2. 确保包名与 MobTech 后台配置一致
3. 必须配置《隐私政策》并在用户同意后调用 submitPolicyGrantResult
4. Android 9.0+ 如需 HTTP 请求需配置 usesCleartextTraffic="true"
5. 回调 afterEvent 在子线程，不可直接处理 UI，需传到主线程
```

---

## 附录：技术参考

### A. Gradle 配置参考

#### A.1 Gradle 插件 7.0 及以上

在 `settings.gradle` 中：

```groovy
pluginManagement {
    repositories {
        gradlePluginPortal()
        google()
        mavenCentral()
        maven { url "https://mvn.mob.com/android" }
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.PREFER_SETTINGS)
    repositories {
        gradlePluginPortal()
        google()
        mavenCentral()
        maven { url "https://mvn.mob.com/android" }
    }
}
```

在项目级 `build.gradle` 中：

```groovy
buildscript {
    dependencies {
        classpath "com.mob.sdk:MobSDK2:+"
    }
}
```

#### A.2 Gradle 插件 7.0 以下

在项目级 `build.gradle` 中配置：

```groovy
allprojects {
    repositories {
        maven { url "https://mvn.mob.com/android" }
    }
}
buildscript {
    repositories {
        maven { url "https://mvn.mob.com/android" }
    }
    dependencies {
        classpath "com.mob.sdk:MobSDK2:+"
    }
}
```

#### A.3 应用级启用插件

```groovy
// 方式 A
apply plugin: 'com.mob.sdk'

// 方式 B
plugins {
    id 'com.android.application'
    id 'com.mob.sdk'
}
```

#### A.4 gradle.properties 配置

```properties
MobSDK.spEdition=FP  // 上架 Google Play 则改为 GPP
```

---

### B. 短信 SDK API

#### B.1 注册回调

```java
EventHandler eh = new EventHandler() {
    @Override
    public void afterEvent(int event, int result, Object data) {
        if (result == SMSSDK.RESULT_COMPLETE) {
            // 成功
        } else {
            // 失败
            ((Throwable) data).printStackTrace();
        }
    }
};
SMSSDK.registerEventHandler(eh);
```

#### B.2 获取验证码

```java
// 文本验证码
SMSSDK.getVerificationCode("86", "手机号");

// 带模板编号
SMSSDK.getVerificationCode("模板编号", "86", "手机号");

// 语音验证码（需先发送完文本验证码）
SMSSDK.getVoiceVerifyCode("86", "手机号");
```

#### B.3 提交验证码

```java
SMSSDK.submitVerificationCode("86", "手机号", "验证码");
```

#### B.4 获取国家列表

```java
SMSSDK.getSupportedCountries();
```

#### B.5 注销监听

```java
SMSSDK.unregisterEventHandler(eh);
```

#### B.6 本机号码验证（可选）

```java
// 获取 token
SMSSDK.getToken();

// 验证本机号码
SMSSDK.login("手机号", new TokenVerifyResult("opToken", "token", "operator"));
```

> **注意**：当同时使用秒验（MSSDK）和短信（SMSSDK）时，默认支持本机号验证，**不需要**也**不能**通过开关打开。仅单独使用短信 SDK 时才需要配置 `mobileAuth true`。

---

### C. 隐私合规要求

必须提醒用户：

1. App 需要有《隐私政策》
2. 隐私政策中必须明确说明使用 MobTech 短信验证服务
3. 首次冷启动展示隐私政策并获取用户同意
4. 同意后调用 `MobSDK.submitPolicyGrantResult(true)`
5. 不同意时不能调用该方法

隐私政策参考条款：
> "我们使用了第三方（上海掌之淘信息技术有限公司，以下称"MobTech"）MobTech 短信验证服务为您提供短信验证功能。为了顺利实现该功能，您需要授权 MobTech SDK 提供对应的服务；在您授权后，MobTech 将收集您相关的个人信息。"

完整合规指南：https://mob.com/wiki/detailed?wiki=210&id=23

---

### D. 短信签名审核

SMSSDK 需要短信签名才能下发短信。

**签名类型要求**（自 2025-08-01 起）：
- **公司签名**（推荐）：与企业营业执照名称完全一致，或简称需包含在营业执照全称中
- **商标签名**：商标需已在中国商标网完成注册
- ~~网站/公众号/小程序签名~~（已不再支持）

**个人用户**：默认使用【掌淘科技】签名
**企业用户**：需上传营业执照审核

国际短信签名：无需审核，直接自行输入英文即可。

---

### E. 常见问题排查

| 问题 | 可能原因 |
|------|----------|
| 验证码发送失败 | 短信签名未审核通过、包名不一致、网络异常 |
| 验证码接收慢 | 运营商通道问题，可尝试语音验证码 |
| Gradle Sync 失败 | 仓库地址配置错误、网络问题 |
| 回调在子线程 | afterEvent 在子线程执行，处理 UI 需传到主线程 |
| 服务端验证失败 | 未开启服务端验证开关、IP 未加入白名单 |

---

## 回答边界

- 仅聚焦 Android SMSSDK 工程集成与合规
- 不扩展到 iOS、服务端（仅参考服务端验证 API 文档）、非 MobTech SDK
- 不伪造真实账号、密钥、签名值
