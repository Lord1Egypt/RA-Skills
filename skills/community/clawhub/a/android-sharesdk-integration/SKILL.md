---
name: android-sharesdk-integration
description: Interactive guide for integrating MobTech ShareSDK into Android projects with 6-step workflow. Use when user says "我要在app中增加分享能力", "ShareSDK集成", "Android分享功能", "配置微信分享", or asks about ShareSDK setup, Gradle configuration, platform devInfo, privacy compliance, or social sharing SDK integration. Supports step-by-step interactive integration with user confirmation at each step.
tags:
  - android
  - sharesdk
  - mobtech
  - social-share
  - gradle
  - privacy
  - interactive-integration
---

# Android ShareSDK 集成 Skill

## 适用场景

当用户提到以下任一主题时，使用本 skill：

- android sharesdk
- ShareSDK 集成
- Mob ShareSDK 接入
- Android 社交分享 SDK 配置
- ShareSDK 的 Gradle 配置
- ShareSDK appKey / appSecret 配置
- ShareSDK 隐私合规
- 微信 / 微信朋友圈等平台在 ShareSDK 中的 devInfo 配置
- 微信分享集成
- **我要在app中增加分享能力**
- **我要在Android项目中接入分享功能**
- **帮我配置微信分享**
- **一键集成 ShareSDK**
- **快速接入 ShareSDK**
- **自动配置 ShareSDK**

如果用户问题明确与 Android 的 ShareSDK 接入、工程配置、平台参数、隐私合规有关，应优先使用本 skill。

---

## 6 步交互式集成工作流

当用户表达集成 ShareSDK 的意图时，执行以下 6 步交互式流程。每步操作前都需要展示内容给用户确认，获得明确同意后再执行。

---

### 步骤 1：启动流程

#### 1-1 触发识别

用户可能通过以下方式表达集成意图：
- "我要在app中增加分享能力"
- "帮我集成 ShareSDK 到 Android 项目"
- "配置微信分享"
- "一键集成 ShareSDK"
- "Android 分享功能怎么接入"

#### 1-2 询问项目路径

**主动询问用户**：

```
我来帮你集成 ShareSDK 分享功能。

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

### 步骤 2：注册社交平台信息

#### 2-1 生成配置模板文件

**操作**：
1. 执行 `assets/generate_excel_template.py`，生成 `assets/ShareSDK_Config_Template.xlsx`
2. 将生成的 `assets/ShareSDK_Config_Template.xlsx` 复制到 `{path}` 下
3. 在 `{path}` 下命名为 `ShareSDK_Config.xlsx`

**告知用户**：
```
已在你项目的根目录生成 {path}/ShareSDK_Config.xlsx 配置文件。

请打开该文件，按以下步骤填写：
1. 在"基础信息"Sheet 中填写 MobTech 的 appKey 和 appSecret
   （从 https://www.mob.com/ 注册应用获取）
2. 在相应平台的 Sheet 中填写需要启用的平台配置
   （如微信、QQ、微博等，不需要的平台可留空）
3. "平台申请地址"Sheet 中有各开放平台的申请链接

填写完成后告诉我"填好了"，我将继续下一步。
```

#### 2-2 等待用户填写完成

等待用户回复"填好了"或类似表达。

#### 2-3 读取并验证配置

**操作**：读取用户项目根目录的 `ShareSDK_Config.xlsx` 文件

**验证规则**：

| 检查项 | 规则 | 不通过时的提示 |
|--------|------|---------------|
| appKey | 必填，不能为空字符串 | "基础信息 Sheet 中的 appKey 未填写，请从 MobTech 官网获取" |
| appSecret | 必填，不能为空字符串 | "基础信息 Sheet 中的 appSecret 未填写" |
| 微信 appId | 如填写，必须以 `wx` 开头 | "微信 appId 格式不正确，应以 wx 开头（如 wx1234567890abcdef）" |
| 微信 appSecret | 如填写，长度应为 32 位 | "微信 appSecret 格式不正确，应为 32 位字符串" |
| QQ appId | 如填写，必须为纯数字 | "QQ appId 格式不正确，应为纯数字（如 100371282）" |
| QQ appKey | 如填写，长度应为 32 位 | "QQ appKey 格式不正确，应为 32 位字符串" |
| 微博 appKey | 如填写，不能为空 | "微博 appKey 未填写" |

**类型转换规则**：
- `appId`、`appKey`、`appSecret`、`userName`、`path` 等标识符字段：**强制转为字符串**，即使 Excel 中填写的是数字（如 `12345`），也要转为 `"12345"`
- `withShareTicket`、`bypassApproval`、`shareByAppClient` 等布尔字段：转为 `true`/`false`（不加引号）
- `miniprogramType` 等数字字段：转为整数（不加引号）

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

#### 3-1 gradle环境配置

根据项目 AGP 版本（通过检查 `gradle/wrapper/gradle-wrapper.properties` 中的 distributionUrl 判断），选择对应配置方式。

##### 文件 1：settings.gradle（AGP 7.0+）

**展示内容**：
```groovy
// 在文件开头添加以下内容
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
// 在 buildscript.dependencies 中添加
classpath "com.mob.sdk:MobSDK2:+"
```


##### 文件 3：gradle.properties

**展示内容**：
```properties
# MobSDK 配置
MobSDK.spEdition=FP
```


##### 文件 4：app/build.gradle

**生成规则**：

1. **类型转换**：
   - `appId`、`appKey`、`appSecret` 等标识符：**强制转为字符串**（加引号），即使 Excel 中填写的是数字（如 `12345` → `"12345"`）
   - `withShareTicket`、`bypassApproval` 等布尔字段：`true`/`false`（不加引号）
   - `miniprogramType` 等数字字段：整数（不加引号）

2. **已启用平台**：根据 Excel 中填写的平台生成完整配置块

3. **未启用平台**：以注释形式填充到 `devInfo` 中，方便后续启用：
   ```groovy
   devInfo {
       Wechat { ... }  // 已启用

       // ========== 以下平台未启用，取消注释并填写参数即可使用 ==========

       // SinaWeibo {
           // appKey ""
           // appSecret ""
           // redirectUri "https://api.weibo.com/oauth2/default.html"
           // shareByAppClient true
       // }
   }
   ```

4. **验证失败处理**：
   - 如果 Excel 数据有错误（如 appKey 为空、微信 appId 不以 wx 开头等），**不生成 build.gradle**，而是向用户展示错误列表，要求修正 Excel 后重新执行

**展示内容**（根据用户填写的 Excel 信息生成）：
```groovy
// 在文件开头添加插件
apply plugin: 'com.mob.sdk'

// 在文件末尾添加 MobSDK 配置
MobSDK {
    appKey "{用户填写的appKey}"
    appSecret "{用户填写的appSecret}"
    gui true

    ShareSDK {
        loopShare true

        devInfo {
            // 根据用户填写的平台动态生成
            {各平台配置块}
        }
    }
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

进入步骤 4

---

### 步骤 4：插入隐私授权回调

#### 4-1 说明合规原因

**向用户说明**：
```
根据 MobTech 隐私合规要求和中国区 App 上架规范，使用 ShareSDK 需要在用户同意隐私政策后才能初始化 SDK。

你需要在 App 中：
1. 首次启动时展示《隐私政策》弹窗
2. 用户点击"同意"按钮后，调用隐私授权代码
3. 用户点击"不同意"则不应调用

请告知我：用户点击隐私政策"同意"按钮的回调代码在哪个文件、哪个方法中？
例如：MainActivity.java 的 onPrivacyAgreed() 方法或者具体位置如:com/kit/app/MainActivity.java:80
```

#### 4-2 询问回调位置

等待用户告知具体的文件路径和方法名。

#### 4-3 展示并确认插入代码

**展示要插入的代码**：
```java
// 用户同意隐私政策后调用
MobSDK.submitPolicyGrantResult(true);
```

**完整示例**：
```java

public void onPrivacyAgreed() {
    // 用户点击同意按钮
    
    // === ShareSDK 隐私授权 ===
    com.mob.MobSDK.submitPolicyGrantResult(true);
    // =======================
    
    // 其他业务逻辑...
}
```

**询问**："以上代码将插入到 {文件} 的 {方法} 中，是否确认？"

#### 4-4 执行插入

用户确认后，将代码插入指定位置。

进入步骤 5

---

### 步骤 5：插入分享代码

#### 5-1 收集分享需求

**询问用户**：
```
现在来配置分享功能，请告诉我：

1. 希望在哪个位置执行分享？
   - 例如：MainActivity 的分享按钮点击事件
   - 或：ArticleDetailFragment 的 onShareClick() 方法

2. 分享内容是什么？
   - 标题：
   - 文本内容：
   - 链接URL：
   - 图片URL（可选）：

3. 分享方式：
   - A. 弹出分享面板让用户选择平台（一键分享）
   - B. 直接分享到指定平台（如微信）

4. 目标平台（如选择B）：
   - 根据用户在 Excel 中配置的平台动态显示
   - 例如：用户配置了微信和QQ，则显示"微信 / 微信朋友圈 / QQ"
   - 未配置的平台不显示，避免用户选择后分享失败
```

#### 5-2 生成并展示分享代码

根据用户需求生成代码：

**场景 A：一键分享面板**
```java
private void showShare() {
    OnekeyShare oks = new OnekeyShare();
    oks.disableSSOWhenAuthorize();
    
    oks.setTitle("{标题}");
    oks.setText("{文本内容}");
    oks.setUrl("{链接URL}");
    oks.setImageUrl("{图片URL}");
    
    oks.setCallback(new PlatformActionListener() {
        @Override
        public void onComplete(Platform platform, int i, HashMap<String, Object> hashMap) {
            Toast.makeText(MainActivity.this, "分享成功", Toast.LENGTH_SHORT).show();
        }
        
        @Override
        public void onError(Platform platform, int i, Throwable throwable) {
            Toast.makeText(MainActivity.this, "分享失败: " + throwable.getMessage(), Toast.LENGTH_SHORT).show();
        }
        
        @Override
        public void onCancel(Platform platform, int i) {
            Toast.makeText(MainActivity.this, "分享取消", Toast.LENGTH_SHORT).show();
        }
    });
    
    oks.show(this);
}
```

**场景 B：指定平台分享（微信示例）**
```java
private void shareToWechat() {
    Platform wechat = ShareSDK.getPlatform("Wechat");
    
    cn.sharesdk.wechat.friends.Wechat.ShareParams sp = 
        new cn.sharesdk.wechat.friends.Wechat.ShareParams();
    sp.setTitle("{标题}");
    sp.setText("{文本内容}");
    sp.setUrl("{链接URL}");
    sp.setShareType(Platform.SHARE_WEBPAGE);
    
    wechat.setPlatformActionListener(new PlatformActionListener() {
        @Override
        public void onComplete(Platform platform, int i, HashMap<String, Object> hashMap) {
            Toast.makeText(MainActivity.this, "微信分享成功", Toast.LENGTH_SHORT).show();
        }
        
        @Override
        public void onError(Platform platform, int i, Throwable throwable) {
            Toast.makeText(MainActivity.this, "微信分享失败", Toast.LENGTH_SHORT).show();
        }
        
        @Override
        public void onCancel(Platform platform, int i) {
            Toast.makeText(MainActivity.this, "微信分享取消", Toast.LENGTH_SHORT).show();
        }
    });
    
    wechat.share(sp);
}
```

**询问**："以上是生成的分享代码，将插入到 {位置}，是否确认？"

#### 5-3 执行插入

用户确认后，将代码插入指定位置。

进入步骤 6

---

### 步骤 6：补充说明

#### 6-1 生成项目级 README

**操作**：使用 `templates/SHARESDK_README.md` 模板，填充以下占位符后写入用户项目根目录：

| 占位符 | 填充内容 |
|--------|----------|
| `{date}` | 当前日期 |
| `{platforms_list}` | 用户启用的平台列表（如：微信、QQ、微博）|
| `{project_path}` | 用户项目路径 |
| `{privacy_file}` | 步骤 4 中用户指定的隐私回调文件 |
| `{privacy_method}` | 步骤 4 中用户指定的隐私回调方法 |
| `{share_file}` | 步骤 5 中插入分享代码的文件 |
| `{share_method}` | 步骤 5 中插入分享代码的方法名 |
| `{share_platforms}` | 步骤 5 中用户选择的分享平台 |

#### 6-2 完成告知

**向用户说明**：
```
ShareSDK 集成已完成！

📁 生成的文件：
- {project_path}/SHARESDK_README.md — 集成说明文档

📝 后续修改位置：
- 修改 SDK 配置：app/build.gradle 中的 MobSDK { } 块
- 修改隐私授权位置：{privacy_file} 的 {privacy_method} 方法
- 修改分享逻辑：{share_file} 的 {share_method} 方法

📖 更多帮助：
- 查看项目根目录的 SHARESDK_README.md
- 官方文档：https://www.mob.com/wiki/list
- 合规指南：https://www.mob.com/wiki/detailed?wiki=421&id=717

⚠️ 重要提醒：
1. 确保微信/QQ 等平台的签名 MD5 与开放平台配置一致
2. 确保 App 有隐私政策并在用户同意后调用隐私授权代码
3. 如需添加更多分享平台，修改 app/build.gradle 的 devInfo 块
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
        maven { url "https://mvn.zztfly.com/android" }
    }
}
buildscript {
    repositories {
        maven { url "https://mvn.zztfly.com/android" }
    }
    dependencies {
        classpath "com.mob.sdk:MobSDK2:+"
    }
}
```

#### A.3 应用级启用插件

```groovy
apply plugin: 'com.android.application'
apply plugin: 'com.mob.sdk'
```


#### A.4 gradle.properties 配置
**主动询问是否上架googleplay**
如果开发者回答:是/YES 
则配置

```properties
MobSDK.spEdition=GPP
```

否则(否/NO): 使用如下配置
```properties
MobSDK.spEdition=FP
```

---

### B. SDK API 参考

#### B.1 一键分享

```java
private void showShare() {
    OnekeyShare oks = new OnekeyShare();
    oks.disableSSOWhenAuthorize();
    oks.setTitle("ShareSDK测试分享");
    oks.setTitleUrl("http://sharesdk.cn");
    oks.setText("这是通过ShareSDK分享的测试内容");
    oks.setUrl("http://sharesdk.cn");
    oks.setImageUrl("https://www.mob.com/public/img/logo_black.png");
    
    oks.setCallback(new PlatformActionListener() {
        @Override
        public void onComplete(Platform platform, int i, HashMap<String, Object> hashMap) {
            Toast.makeText(MainActivity.this, "分享成功", Toast.LENGTH_SHORT).show();
        }
        
        @Override
        public void onError(Platform platform, int i, Throwable throwable) {
            Toast.makeText(MainActivity.this, "分享失败", Toast.LENGTH_SHORT).show();
        }
        
        @Override
        public void onCancel(Platform platform, int i) {
            Toast.makeText(MainActivity.this, "分享取消", Toast.LENGTH_SHORT).show();
        }
    });
    
    oks.show(this);
}
```

#### B.2 指定平台分享（微信）

```java
private void shareToWechat() {
    Platform wechat = ShareSDK.getPlatform("Wechat");
    
    cn.sharesdk.wechat.friends.Wechat.ShareParams sp = 
        new cn.sharesdk.wechat.friends.Wechat.ShareParams();
    sp.setTitle("微信分享测试");
    sp.setText("这是分享到微信的测试内容");
    sp.setUrl("http://sharesdk.cn");
    sp.setShareType(Platform.SHARE_WEBPAGE);
    
    wechat.setPlatformActionListener(new PlatformActionListener() {
        @Override
        public void onComplete(Platform platform, int i, HashMap<String, Object> hashMap) {
            Toast.makeText(MainActivity.this, "微信分享成功", Toast.LENGTH_SHORT).show();
        }
        
        @Override
        public void onError(Platform platform, int i, Throwable throwable) {
            Toast.makeText(MainActivity.this, "微信分享失败", Toast.LENGTH_SHORT).show();
        }
        
        @Override
        public void onCancel(Platform platform, int i) {
            Toast.makeText(MainActivity.this, "微信分享取消", Toast.LENGTH_SHORT).show();
        }
    });
    
    wechat.share(sp);
}
```

#### B.3 指定平台分享（QQ）

```java
private void shareToQQ() {
    Platform qq = ShareSDK.getPlatform("QQ");
    
    cn.sharesdk.tencent.qq.QQ.ShareParams sp = 
        new cn.sharesdk.tencent.qq.QQ.ShareParams();
    sp.setTitle("QQ分享测试");
    sp.setTitleUrl("http://sharesdk.cn");
    sp.setText("这是分享到QQ的测试内容");
    sp.setImageUrl("https://www.mob.com/public/img/logo_black.png");
    sp.setSite("ShareSDK");
    sp.setSiteUrl("http://sharesdk.cn");
    
    qq.setPlatformActionListener(new PlatformActionListener() {
        @Override
        public void onComplete(Platform platform, int i, HashMap<String, Object> hashMap) {
            Toast.makeText(MainActivity.this, "QQ分享成功", Toast.LENGTH_SHORT).show();
        }
        
        @Override
        public void onError(Platform platform, int i, Throwable throwable) {
            Toast.makeText(MainActivity.this, "QQ分享失败", Toast.LENGTH_SHORT).show();
        }
        
        @Override
        public void onCancel(Platform platform, int i) {
            Toast.makeText(MainActivity.this, "QQ分享取消", Toast.LENGTH_SHORT).show();
        }
    });
    
    qq.share(sp);
}
```

#### B.4 第三方登录

```java
Platform platform = ShareSDK.getPlatform(QQ.NAME);
platform.setPlatformActionListener(new PlatformActionListener() {
    @Override
    public void onComplete(Platform platform, int i, HashMap<String, Object> hashMap) {
        String userId = platform.getDb().getUserId();
        String token = platform.getDb().getToken();
    }
    
    @Override
    public void onError(Platform platform, int i, Throwable throwable) {
        // 登录失败
    }
    
    @Override
    public void onCancel(Platform platform, int i) {
        // 取消登录
    }
});
platform.showUser(null);
```

#### B.5 分享参数说明

| 方法 | 说明 |
|------|------|
| setTitle | 分享标题（微信、QQ空间等使用） |
| setTitleUrl | 标题链接（仅LinkedIn、QQ空间使用） |
| setText | 分享文本（所有平台都需要） |
| setImageUrl | 网络图片地址 |
| setUrl | 分享链接（微信、QQ等使用） |
| setShareType | 分享类型：WEBPAGE（网页）、IMAGE（图片）、TEXT（文本） |

---

### C. 隐私合规要求

必须提醒用户：

1. App 需要有《隐私政策》
2. 首次冷启动展示隐私政策并获取用户同意
3. 同意后调用 `MobSDK.submitPolicyGrantResult(true)`
4. 不同意时不能调用该方法

在隐私政策中应包含：
- 使用了 MobTech ShareSDK 服务
- 用于社交分享、第三方登录
- 可能会收集相关信息

完整合规指南：https://www.mob.com/wiki/detailed?wiki=421&id=717

---

### D. 常见问题排查

| 问题 | 可能原因 |
|------|----------|
| 微信分享失败 | 签名MD5不一致、包名不一致、appId错误 |
| QQ分享失败 | appId/appKey错误、未配置URL Scheme |
| 微博分享失败 | appKey/appSecret错误、回调地址不匹配 |
| 编译失败 | MobSDK插件未加载成功 |

---

### E. 平台申请地址汇总

| 平台 | 开放平台地址 |
|------|-------------|
| 微信/微信朋友圈/微信收藏 | https://open.weixin.qq.com |
| QQ / QZone | https://connect.qq.com |
| 新浪微博 | https://open.weibo.com |
| Facebook | https://developers.facebook.com |
| Twitter / X | https://developer.twitter.com |
| Instagram | https://developers.instagram.com |
| LinkedIn | https://www.linkedin.com/developers/apps |
| Line | https://developers.line.biz/console/ |
| KakaoTalk / KakaoStory | https://developers.kakao.com/console/app |
| 支付宝 | https://open.alipay.com/platform/home.htm |

---

## 回答边界

- 仅聚焦 Android ShareSDK 工程集成与合规
- 不扩展到 iOS、服务端、非 MobTech SDK
- 不伪造真实账号、密钥、签名值
