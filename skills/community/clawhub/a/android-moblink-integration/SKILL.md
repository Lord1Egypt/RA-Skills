---
name: android-moblink-integration
description: Interactive guide for integrating MobTech MobLink into Android projects with step-by-step workflow. Use when user says "MobLink集成", "Link集成", "Android深度链接", "场景还原", "一键集成 MobLink", or asks about MobLink Gradle configuration, uriScheme, AppLink Host, getMobID, scene restore, SceneRestorable, privacy compliance, or MobCustomController setup.
tags:
  - android
  - moblink
  - mobtech
  - deep-link
  - scene-restore
  - gradle
  - privacy
  - interactive-integration
---

# Android MobLink 集成 Skill

## 适用场景

当用户提到以下任一主题时，使用本 skill：

- android moblink
- MobLink 集成
- Link 集成
- MobTech MobLink 接入
- Android 深度链接 / Deeplink
- 场景还原
- MobLink 的 Gradle 配置
- MobLink uriScheme / AppLink Host 配置
- getMobID / setRestoreSceneListener / SceneRestorable
- MobLink 隐私合规
- MobCustomController 扩展业务功能控制
- **我要在app中增加深度链接能力**
- **我要在Android项目中接入MobLink**
- **帮我配置场景还原**
- **一键集成 MobLink**
- **自动配置 MobLink**

如果用户问题明确与 Android 的 MobLink 接入、工程配置、场景还原、隐私合规有关，应优先使用本 skill。

## 官方文档依据

使用以下官方文档作为事实来源：

- 文档入口：https://www.mob.com/wiki/detailed?wiki=661&id=34
- Android 集成指南：https://www.mob.com/wiki/detailed?wiki=115&id=34
- Android SDK API：https://www.mob.com/wiki/detailed?wiki=116&id=34
- Android 合规指南：https://www.mob.com/wiki/detailed?wiki=222&id=34
- MobLink 扩展业务功能设置：https://www.mob.com/wiki/detailed?wiki=660&id=34

关键事实：

- 官方 Android 集成方式：Android Studio + Gradle 在线集成。
- Android 最低版本：`minSdkVersion 19`。
- Maven 地址：`https://mvn.mob.com/android`。
- MobSDK 插件：`classpath "com.mob.sdk:MobSDK2:+"`。
- app 模块需要应用 `com.mob.sdk` 插件。
- `MobSDK { appKey "..."; appSecret "..."; MobLink { uriScheme "..."; appLinkHost "..." } }` 是核心配置。
- Google Play 版本使用 `MobSDK.spEdition=GPP`。
- 文档集成指南中出现 `MobSDK.spEdition=IZNAO`；合规指南中说明隐私协议适配版本为 `MobSDK.spEdition=FP`。生成时必须向用户确认上架渠道与版本选择。
- 用户同意隐私政策后调用 `MobSDK.submitPolicyGrantResult(true)`，或使用 `MobSDK.submitPolicyGrantResult(MobCustomController cont, true)`。

## 6 步交互式集成工作流

每步操作前都需要展示内容给用户确认，获得明确同意后再执行。

### 步骤 1：启动流程

#### 1-1 询问项目路径

```
我来帮你集成 MobLink 场景还原功能。

请提供需要集成的 Android 项目根路径，例如：
/path/to/your-android-project

请确保项目包含 settings.gradle 或 app/build.gradle 文件。
```

#### 1-2 验证路径合法性

验证逻辑：

1. 检查路径是否存在。
2. 检查路径下是否有 `settings.gradle` 或 `settings.gradle.kts`。
3. 检查是否存在 app 模块 Gradle 文件，例如 `app/build.gradle` 或 `app/build.gradle.kts`。
4. 检查是否为有效 Android 项目结构。

如果路径不合法：

```
路径验证失败，可能原因：
- 路径不存在：{path}
- 未找到 settings.gradle / settings.gradle.kts
- 未找到 app/build.gradle / app/build.gradle.kts

请重新提供正确的 Android 项目根路径。
```

如果路径合法：进入步骤 2。

### 步骤 2：注册 MobLink 配置信息

#### 2-1 生成配置模板文件

**操作**：

1. 执行 `assets/generate_excel_template.py`，生成 `assets/MobLink_Config_Template.xlsx`
2. 将生成的 `assets/MobLink_Config_Template.xlsx` 复制到 `{path}` 下
3. 在 `{path}` 下命名为 `MobLink_Config.xlsx`

**告知用户**：

```
已在你项目的根目录生成 {path}/MobLink_Config.xlsx 配置文件。

请打开该文件，按以下步骤填写：
1. 在"基础信息"Sheet 中填写 MobTech 的 appKey、appSecret、包名和签名 MD5
2. 在"MobLink配置"Sheet 中填写 uriScheme、appLinkHost 和默认场景路径
3. 在"隐私合规"Sheet 中确认隐私政策、授权回调和扩展采集控制配置
4. "填写说明"Sheet 中有官方文档链接和字段说明

填写完成后告诉我"填好了"，我将继续下一步。
```

#### 2-2 等待用户填写完成

等待用户回复“填好了”“已填写”或类似表达。

#### 2-3 读取并验证配置

**操作**：读取 `{path}/MobLink_Config.xlsx`。

验证规则：

| 检查项 | 规则 | 不通过时的提示 |
|--------|------|---------------|
| appKey | 必填，不能为空字符串 | "基础信息 Sheet 中的 appKey 未填写，请从 MobTech 官网获取" |
| appSecret | 必填，不能为空字符串 | "基础信息 Sheet 中的 appSecret 未填写" |
| packageName | 必填，建议符合 `com.xxx.xxx` 格式 | "包名格式不正确，应类似 com.example.app" |
| uriScheme | 建议填写，来自 MobLink 后台配置 | "MobLink uriScheme 未填写，可能影响 scheme 唤醒" |
| appLinkHost | 建议填写，来自 MobLink 后台开启 AppLink 时生成的 Host | "MobLink appLinkHost 未填写，可能影响 AppLink 唤醒" |
| defaultScenePath | 如填写，建议以 `/` 开头 | "场景路径建议以 / 开头，例如 /demo/a" |
| useGooglePlayEdition | 转为布尔值 | "是否上架 Google Play 请填写 是/否 或 true/false" |
| 隐私合规布尔项 | 转为布尔值 | "隐私合规配置请填写 是/否 或 true/false" |

类型转换规则：

- `appKey`、`appSecret`、`packageName`、`signatureMD5`、`uriScheme`、`appLinkHost`、`defaultScenePath`、`restoreActivity` 等标识符字段强制转为字符串。
- `useGooglePlayEdition`、`privacyPolicyReady`、`useMobCustomController`、`allowLocationData`、`allowDeviceIdData`、`allowAppListData`、`allowNetworkData` 转为 `true` / `false`。

如果不合法：

```
配置信息验证失败，请修正以下问题：

{具体问题列表}

请修改 Excel 文件后保存，然后重新告诉我"填好了"。
```

如果合法：提取配置信息，进入步骤 3。

### 步骤 3：完成 SDK 集成

#### 3-1 Gradle 仓库与插件配置

根据项目 AGP 版本和 Gradle 文件类型选择 Groovy 或 Kotlin DSL。修改前必须展示将要添加的内容并询问确认。

AGP 7.0+ 的 `settings.gradle` 示例：

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

项目级 `build.gradle`：

```groovy
buildscript {
    dependencies {
        classpath "com.mob.sdk:MobSDK2:+"
    }
}
```

AGP 7.0 以下项目还需要在项目级 `build.gradle` 的 `allprojects.repositories` 和 `buildscript.repositories` 中加入：

```groovy
maven { url "https://mvn.mob.com/android" }
```

#### 3-2 gradle.properties 配置

根据 Excel 的 `useGooglePlayEdition` 和用户确认决定：

- 上架 Google Play：`MobSDK.spEdition=GPP`
- 非 Google Play：中国区合规优先建议 `MobSDK.spEdition=FP`

#### 3-3 app 模块配置

Groovy DSL 示例：

```groovy
apply plugin: 'com.mob.sdk'

MobSDK {
    appKey "{appKey}"
    appSecret "{appSecret}"

    MobLink {
        uriScheme "{uriScheme}"
        appLinkHost "{appLinkHost}"
    }
}
```

如果项目使用 `plugins {}`：

```groovy
plugins {
    id 'com.android.application'
    id 'com.mob.sdk'
}
```

Kotlin DSL 项目需要按现有风格生成等价配置。若无法确认 MobSDK 插件在 Kotlin DSL 下的准确语法，先向用户展示建议并要求确认。

#### 3-4 ProGuard / R8 配置

如果项目启用了混淆，在混淆文件中加入：

```proguard
-keep class com.mob.**{*;}
-dontwarn com.mob.**
```

### 步骤 4：插入隐私授权回调

#### 4-1 说明合规原因

```
根据 MobTech 合规要求，MobLink 需要在用户同意隐私政策后才能提交授权结果并使用 SDK 功能。

请告知用户点击隐私政策"同意"按钮的回调代码在哪个文件、哪个方法中？
例如：MainActivity.java 的 onPrivacyAgreed() 方法，或具体位置如 app/src/main/java/.../MainActivity.java:80
```

#### 4-2 展示并确认插入代码

普通方案：

```java
com.mob.MobSDK.submitPolicyGrantResult(true);
```

如果用户启用 `MobCustomController`，展示：

```java
com.mob.MobSDK.submitPolicyGrantResult(new MyMobLinkCustomController(), true);
```

如需在启动时更新控制器，可展示：

```java
com.mob.MobSDK.updateMobCustomController(new MyMobLinkCustomController());
```

注意：官方扩展业务文档说明，使用 `submitPolicyGrantResult(controller, true)` 设置控制器时，必须每次启动 APP 时均调用；如果并非每次启动都会调用隐私提交接口，可以通过 `MobSDK.updateMobCustomController()` 设置。

用户确认后再执行插入。

### 步骤 5：插入场景还原与制链代码

#### 5-1 收集业务信息

询问用户：

```
现在配置 MobLink 场景还原，请告诉我：

1. 需要在哪个 Activity 承接还原后的场景？
2. 场景路径是什么？例如 /demo/a
3. 需要携带哪些业务参数？例如 articleId、userId、source
4. 是否需要生成 mobID 并拼接到分享链接？
5. 是否已有 Application 类？如果有，请提供路径。
```

#### 5-2 设置全局场景还原监听器

官方建议放到 Application 的 `onCreate` 中。若 Application 未继承 `MobApplication`，在设置监听前需要确认是否调用：

```java
MobSDK.init(this, "{appKey}", "{appSecret}");
```

监听器示例：

```java
MobLink.setRestoreSceneListener(new RestoreSceneListener() {
    @Override
    public Class<? extends Activity> willRestoreScene(Scene scene) {
        return MainActivity.class;
    }

    @Override
    public void notFoundScene(Scene scene) {
        // 未找到处理 scene 的 Activity
    }

    @Override
    public void completeRestore(Scene scene) {
        // 场景还原完成
    }
});
```

#### 5-3 修改承接 Activity

让需要场景还原的 Activity 实现 `SceneRestorable`，并添加：

```java
@Override
public void onReturnSceneData(Scene scene) {
    // 处理场景还原数据
}

@Override
protected void onNewIntent(Intent intent) {
    super.onNewIntent(intent);
    setIntent(intent);
    MobLink.updateNewIntent(getIntent(), this);
}
```

#### 5-4 生成 mobID 示例

```java
HashMap<String, Object> sceneParams = new HashMap<>();
sceneParams.put("key1", "value1");

Scene scene = new Scene();
scene.path = "{defaultScenePath}";
scene.params = sceneParams;

MobLink.getMobID(scene, new ActionListener() {
    @Override
    public void onResult(String mobID) {
        // 根据 mobID 拼接分享链接，例如：url + "&mobid=" + mobID
    }

    @Override
    public void onError(Throwable throwable) {
        // 处理错误
    }
});
```

所有代码修改前先展示完整 diff 计划，用户确认后再写入。

### 步骤 6：生成集成说明

**操作**：在 `{path}` 下生成 `MOBLINK_README.md`。

内容应包含：

- 已修改文件列表。
- MobSDK / MobLink Gradle 配置位置。
- `uriScheme` 和 `appLinkHost` 来源。
- 隐私授权回调位置。
- 场景还原监听器位置。
- 承接 Activity 和 `SceneRestorable` 实现位置。
- `getMobID` 使用方式。
- Google Play / FP / IZNAO 版本选择说明。
- 常见问题和官方文档链接。

生成前展示内容，用户确认后写入。
