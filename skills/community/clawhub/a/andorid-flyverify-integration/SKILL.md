---
name: android-flyverify-integration
description: Interactive guide for integrating MobTech FlyVerify (SecVerify) into Android projects with 5-step workflow. Use when user says "我要在app中增加一键登录", "秒验集成", "FlyVerify集成", "Android一键登录", or asks about FlyVerify setup, Gradle configuration, pre-verification, one-click login, custom UI, or privacy compliance. Supports step-by-step interactive integration with user confirmation at each step.
tags:
  - android
  - flyverify
  - secverify
  - mobtech
  - one-click-login
  - mobile-verification
  - gradle
  - privacy
  - interactive-integration
---

# Android FlyVerify (秒验) 集成 Skill

## 适用场景

当用户提到以下任一主题时，使用本 skill：

- android flyverify
- android secverify
- 秒验集成
- 一键验证/一键登录
- 手机号免密验证
- 运营商网关认证
- FlyVerify SDK 接入
- **我要在app中增加一键登录**
- **我要在Android项目中接入秒验功能**
- **帮我配置一键登录**
- **一键集成 FlyVerify**
- **快速接入秒验**
- **自动配置 FlyVerify**

如果用户问题明确与 Android 的秒验接入、工程配置、一键验证功能、自定义 UI 有关，应优先使用本 skill。

---

## 5 步交互式集成工作流

当用户表达集成 FlyVerify 的意图时，执行以下 5 步交互式流程。每步操作前都需要展示内容给用户确认，获得明确同意后再执行。

---

### 步骤 1：启动流程

#### 1-1 触发识别

用户可能通过以下方式表达集成意图：
- "我要在app中增加一键登录"
- "帮我集成 FlyVerify 到 Android 项目"
- "配置一键登录"
- "一键集成秒验"
- "Android 一键登录功能怎么接入"

#### 1-2 询问项目路径

**主动询问用户**：

```
我来帮你集成 FlyVerify 一键登录功能。

请提供需要集成的 Android 项目根路径，例如：
/Users/xxx/your-android-project

请确保项目包含 app/build.gradle 文件。

⚠️ 注意：FlyVerify所集成的项目 需要在 MobTech 后台提交秒验审核并通过后才能正常使用。
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

### 步骤 2：注册 FlyVerify 配置信息

#### 2-1 生成配置模板文件

**操作**：
1. 执行 `assets/generate_excel_template.py`，生成 `assets/FlyVerify_Config_Template.xlsx`
2. 将生成的 `assets/FlyVerify_Config_Template.xlsx` 复制到 `{path}` 下
3. 在 `{path}` 下命名为 `FlyVerify_Config.xlsx`

**告知用户**：
```
已在你项目的根目录生成 {path}/FlyVerify_Config.xlsx 配置文件。

请打开该文件，按以下步骤填写：
1. 在"基础信息"Sheet 中填写 MobTech 的 appKey 和 appSecret
   （从 https://www.mob.com/ 注册应用获取）
2. 填写 Android 包名和签名 MD5
3. 确认秒验审核是否已通过
4. "隐私合规"Sheet 中有隐私政策说明
5. "填写说明"Sheet 中有详细说明

⚠️ 重要提醒：
- 秒验审核通过后才能正常使用一键验证功能
- 请前往 MobTech 后台提交秒验审核

填写完成后告诉我"填好了"，我将继续下一步。
```

#### 2-2 等待用户填写完成

等待用户回复"填好了"或类似表达。

#### 2-3 读取并验证配置

**操作**：读取用户项目根目录的 `FlyVerify_Config.xlsx` 文件

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
        maven { url "https://mvn.zztfly.com/android" }
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.PREFER_SETTINGS)
    repositories {
        maven { url "https://mvn.zztfly.com/android" }
    }
}
```

##### 文件 2：项目级 build.gradle

**展示内容**：
```groovy
buildscript {
    dependencies {
        classpath 'cn.fly.sdk:FlySDK:+'
    }
}
```
**7.0以下版本**
1. 打开Android Studio项目级build.gradle文件。
2. 在allprojects ->repositories里面配置maven仓地址。
```groovy
   allprojects {
       repositories {
           maven {
               url "https://mvn.zztfly.com/android"
           }
       }
   }
```
3. 在buildscript->repositories中配置maven仓地址。
```groovy
   buildscript {
       repositories {
           maven {
               url "https://mvn.zztfly.com/android"
           }
       }
   }
```
4. 在buildscript->dependencies中配置AppGallery Connect插件地址
```groovy
   buildscript {
       dependencies {
           //增加SDK插件配置
           classpath 'cn.fly.sdk:FlySDK:+'
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
// 在文件开头添加插件
apply plugin: 'cn.fly.sdk'

// 在文件末尾添加 FlySDK 配置
FlySDK {
    appKey "{用户填写的appKey}"
    appSecret "{用户填写的appSecret}"
    FlyVerify {}
}
```

**询问**："以上是要添加到 app/build.gradle 的内容，是否确认修改？"

#### 3-2 执行 Gradle Sync

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
至此，Gradle集成方式环境搭建已经完成。

进入步骤 4

---

### 步骤 4：补充说明

#### 4-1 说明隐私授权

**向用户说明**：
```
根据 MobTech 隐私合规要求，使用 FlyVerify 需要在用户同意隐私政策后才能初始化 SDK。

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
FlySDK.submitPolicyGrantResult(true, null);
```

**完整示例**：
```java
public void onPrivacyAgreed() {
    // 用户点击同意按钮
    
    // === FlyVerify 隐私授权 ===
    cn.fly.FlySDK.submitPolicyGrantResult(true, null);
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

### 步骤 5：插入手机号一键验证代码

#### 5-1 询问是否使用预登录功能

**说明**：预登录（preVerify）可以提前检测网络环境并获取临时凭证，建议在登录页面打开前调用。

**询问**：`"是否需要在项目中添加预登录功能？"`

如果开发者回答：**否/NO** → 跳过 5-2 和 5-3，直接进入 5-4

如果开发者回答：**是/YES** → 继续 5-2

#### 5-2 展示并插入预登录代码

**等待用户告知**：要插入预登录代码的文件路径和方法名。

**展示要插入的代码**：
```java
// 建议提前调用预登录接口，可以加快免密登录过程，提高用户的体验。
FlyVerify.preVerify(new PreVerifyCallback() {
    @Override
    public void onComplete(Void data) {
        // TODO 处理成功的结果
    }
    @Override
    public void onFailure(VerifyException e) {
        // TODO 处理失败的结果
        // 获取错误码
        int errCode = e.getCode();
        // 获取SDK返回的错误信息
        String errMsg = e.getMessage();
        // 更详细的网络错误信息可以通过t查看，注：t有可能为null,也可用于获取运营商返回的错误信息
        Throwable t = e.getCause();
        String errDetail = null;
        if (t != null) {
            errDetail = t.getMessage();
        }
    }
});
```

**完整示例**：
```java
public void initLogin() {
    // === FlyVerify 预登录 ===
    FlyVerify.preVerify(new PreVerifyCallback() {
        @Override
        public void onComplete(Void data) {
            // TODO 处理成功的结果
        }
        @Override
        public void onFailure(VerifyException e) {
            // TODO 处理失败的结果
        }
    });
    // =======================
    
    // 其他登录相关逻辑...
}
```

**询问**：`"以上代码将插入到 {文件} 的 {方法} 中，是否确认？"`

用户确认后，将代码插入指定位置。

#### 5-3 询问是否使用一键登录功能

**说明**：一键登录（verify）将拉起运营商授权页面，用户授权后获取 token。

**询问**：`"是否需要添加一键登录功能？"`

如果开发者回答：**否/NO** → 跳过 5-4 和 5-5，直接进入步骤 6

如果开发者回答：**是/YES** → 继续 5-4

#### 5-4 展示并插入登录代码

**等待用户告知**：要插入登录代码的文件路径和方法名。

**展示要插入的代码**：
```java
FlyVerify.verify(new VerifyCallback() {
    @Override
    public void onOtherLogin() {
        // 用户点击"其他登录方式"，处理自己的逻辑
    }
    @Override
    public void onUserCanceled() {
        // 用户点击"关闭按钮"或"物理返回键"取消登录，处理自己的逻辑
    }
    @Override
    public void onComplete(VerifyResult verifyResult) {
        // 获取授权码成功，将token信息传给应用服务端，再由应用服务端进行登录验证，此功能需由开发者自行实现
        // opToken
        String opToken = verifyResult.getOpToken();
        // token
        String token = verifyResult.getToken();
        // 运营商类型，[CMCC:中国移动，CUCC：中国联通，CTCC：中国电信]
        String operator = verifyResult.getOperator();
    }
    @Override
    public void onFailure(VerifyException e) {
        // TODO 处理失败的结果
    }
});
```

**完整示例**：
```java
public void doLogin() {
    // === FlyVerify 一键登录 ===
    FlyVerify.verify(new VerifyCallback() {
        @Override
        public void onOtherLogin() {
            // 用户点击"其他登录方式"
        }
        @Override
        public void onUserCanceled() {
            // 用户取消登录
        }
        @Override
        public void onComplete(VerifyResult verifyResult) {
            String token = verifyResult.getToken();
            // 将 token 传给服务端进行登录验证
        }
        @Override
        public void onFailure(VerifyException e) {
            // TODO 处理失败的结果
        }
    });
    // =======================
}
```

**询问**：`"以上代码将插入到 {文件} 的 {方法} 中，是否确认？"`

用户确认后，将代码插入指定位置。

---

### 步骤 6：完成集成

#### 6-1 生成项目级 README

**操作**：在用户项目根目录生成 `FLYVERIFY_README.md`，内容包含集成说明、关键文件位置、后续修改指引。

#### 6-2 完成告知

**向用户说明**：
```
FlyVerify 集成已完成！

📁 生成的文件：
- {project_path}/FLYVERIFY_README.md — 集成说明文档

📝 后续修改位置：
- 修改 SDK 配置：app/build.gradle 中的 FlySDK { } 块
- 修改隐私授权位置：{privacy_file} 的 {privacy_method} 方法

📖 更多帮助：
- 官方文档：https://www.mob.com/wiki/detailed?wiki=551&id=78
- SDK API：https://www.mob.com/wiki/detailed?wiki=297&id=78
- 合规指南：https://www.mob.com/wiki/detailed?wiki=421&id=717

⚠️ 重要提醒：
1. 确保秒验审核已通过（否则无法正常使用）
2. 确保包名与 MobTech 后台配置一致
3. 确保签名 MD5 与后台配置一致
4. 必须使用移动蜂窝网络（WiFi 下可能无法取号）
5. Android 9.0+ 需配置 usesCleartextTraffic="true"
6. App 有隐私政策并在用户同意后调用隐私授权代码
```

---

## 附录：技术参考

### A. Gradle 配置参考

#### A.1 Gradle 插件 7.0 及以上

在 `settings.gradle` 第1行开始填充：

```groovy
pluginManagement {
    repositories {
        maven { url "https://mvn.zztfly.com/android" }
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.PREFER_SETTINGS)
    repositories {
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
**主动询问是否上架googleplay**
如果开发者回答:是/YES 
则配置

```properties
MobSDK.spEdition=GPP
```

否则(否/NO)
```properties
MobSDK.spEdition=FP
```


---

### B. 预取号接口

预取号可以提前获取一键登录的临时凭证，优化用户体验。建议在页面打开前或网络空闲时调用。

```java
// 建议提前调用预登录接口，可以加快免密登录过程，提高用户的体验。
FlyVerify.preVerify(new PreVerifyCallback() {
    @Override
    public void onComplete(Void data) {
        // TODO处理成功的结果
    }
    @Override
    public void onFailure(VerifyException e) {
        // TODO处理失败的结果
        // 获取错误码
        int errCode = e.getCode();
        //获取SDK返回的错误信息
        String errMsg = e.getMessage();   
        // 更详细的网络错误信息可以通过t查看
        Throwable t = e.getCause();
        String errDetail = null;
        if (t != null) {
            errDetail = t.getMessage();
        }
    }
});
```

---

### C. 一键验证/登录

调用验证接口拉起运营商授权页：

```java
FlyVerify.verify(new VerifyCallback() {
    @Override
    public void onOtherLogin() {
        // 用户点击"其他登录方式"，处理自己的逻辑
    }
    @Override
    public void onUserCanceled() {
        // 用户点击"关闭按钮"或"物理返回键"取消登录
    }
    @Override
    public void onComplete(VerifyResult verifyResult) {
        // 获取授权码成功，将token信息传给应用服务端
        // opToken
        String opToken = verifyResult.getOpToken();   
        // token
        String token = verifyResult.getToken();   
        // 运营商类型，[CMCC:中国移动，CUCC：中国联通，CTCC：中国电信]
        String operator = verifyResult.getOperator();   
    }
    @Override
    public void onFailure(VerifyException e) {
        //TODO处理失败的结果
    }
});
```

---

### D. SDK API 补充

#### D.1 设置调试模式

```java
FlySDK.setDebugMode(true);
```

#### D.2 超时设置

```java
// 超时时间，单位ms，取值1000-10000，默认5000ms
FlySDK.setTimeOut(5000);
```

#### D.3 关闭自带loading

```java
CommonProgressDialog.dismissProgressDialog();
```

#### D.4 主动关闭授权页面

```java
FlySDK.finishOAuthPage();
```

---

### E. 自定义 UI 配置

#### E.1 竖屏UI

```java
UiSettings uiSettings = new UiSettings.Builder()
    // 导航栏配置
    .setNavColor(Color.parseColor("#FFFFFF"))
    .setNavTextColor(Color.parseColor("#000000"))
    // Logo配置
    .setLogoResId(R.drawable.ic_logo)
    // 手机号配置
    .setNumberColor(Color.parseColor("#333333"))
    // 登录按钮配置
    .setLoginBtnText("本机号码一键登录")
    .setLoginBtnColor(Color.parseColor("#1677FF"))
    // 协议配置
    .addAgreement("https://example.com/privacy", "《隐私政策》")
    .build();

FlyVerify.setUiSettings(uiSettings);
```

#### E.2 横屏UI

```java
LandUiSettings landUiSettings = new LandUiSettings.Builder()
    // 横屏UI配置
    .build();

FlyVerify.setLandUiSettings(landUiSettings);
```

---

### F. 隐私合规要求

必须提醒用户：

1. App 需要有《隐私政策》
2. 隐私政策中必须明确说明使用秒验 SDK 进行一键验证/登录
3. 首次冷启动展示隐私政策并获取用户同意
4. 同意后调用 `FlySDK.submitPolicyGrantResult(true, null)`
5. 不同意时不能调用该方法

在隐私政策中应包含：
- 使用了 MobTech 秒验服务
- 用于一键验证/登录功能
- 涉及运营商网关认证和手机号验证
- 可能会收集相关信息

完整合规指南：https://www.mob.com/wiki/detailed?wiki=421&id=717

---

### G. 常见问题排查

| 问题 | 可能原因 |
|------|----------|
| 取号失败 | 秒验审核未通过、签名MD5不一致、包名不一致 |
| 无法拉起授权页 | 未开启移动蜂窝网络、Android 9.0+未配置usesCleartextTraffic |
| WiFi下无法取号 | 秒验必须使用移动蜂窝网络 |
| 授权页拉起失败 | 运营商不支持、网络异常 |



---

## 回答边界

- 仅聚焦 Android FlyVerify 工程集成与合规
- 不扩展到 iOS、服务端、非 MobTech SDK
- 不伪造真实账号、密钥、签名值
