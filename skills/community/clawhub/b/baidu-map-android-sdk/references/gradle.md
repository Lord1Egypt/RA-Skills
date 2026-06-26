# Gradle 集成 SDK

Android 推荐通过 Gradle 依赖集成百度地图 SDK（国内版）。Google 渠道等需使用一体化包时请从官网下载后按「本地依赖」方式集成。

**版本**：以下以 7.6.x / 9.6.x 为例，实际以官网更新为准。不写版本号可改为 `+` 或具体版本号；API 以工程内依赖版本为准，类/方法不存在时提示更新依赖，见 [SKILL.md](../SKILL.md) 规则 6。

## 1. 配置仓库

在 **Project** 的 `build.gradle` 中配置 `repositories`，添加 mavenCentral：

```gradle
allprojects {
    repositories {
        mavenCentral()
    }
}
```

若项目已使用 `dependencyResolutionManagement`（Gradle 7+），在 `settings.gradle` 或对应块中为百度 SDK 提供 mavenCentral 即可。

## 2. 主工程依赖（app/build.gradle）

在 **app** 的 `build.gradle` 的 `dependencies` 中按需添加。常用组合示例：

| SDK | 依赖 |
|-----|------|
| 地图组件 | `implementation 'com.baidu.lbsyun:BaiduMapSDK_Map:7.6.7'` |
| 检索组件 | `implementation 'com.baidu.lbsyun:BaiduMapSDK_Search:7.6.7'` |
| 工具组件 | `implementation 'com.baidu.lbsyun:BaiduMapSDK_Util:7.6.7'` |
| 步骑行导航组件 | `implementation 'com.baidu.lbsyun:BaiduMapSDK_Map-BWNavi:7.6.7'` |
| 基础定位组件 | `implementation 'com.baidu.lbsyun:BaiduMapSDK_Location:9.6.6'` |
| 全量定位组件 | `implementation 'com.baidu.lbsyun:BaiduMapSDK_Location_All:9.6.6'` |
| 驾车导航组件 | `implementation 'com.baidu.lbsyun:BaiduMapSDK_Map-Navi:7.6.7'` |
| 驾车+步骑行导航 | `implementation 'com.baidu.lbsyun:BaiduMapSDK_Map-AllNavi:7.6.7'` |
| TTS 组件 | `implementation 'com.baidu.lbsyun:NaviTts:3.2.13'` |
| 全景组件 | `implementation 'com.baidu.lbsyun:BaiduMapSDK_Panorama:2.9.0'` |

**仅地图+检索+工具**示例：

```gradle
dependencies {
    implementation 'com.baidu.lbsyun:BaiduMapSDK_Map:7.6.7'
    implementation 'com.baidu.lbsyun:BaiduMapSDK_Search:7.6.7'
    implementation 'com.baidu.lbsyun:BaiduMapSDK_Util:7.6.7'
}
```

## 3. 组件冲突说明

以下各组内**只能选其一**，不能同时引入：

| 组 | 可选依赖 |
|----|----------|
| 定位 | 基础定位 `BaiduMapSDK_Location` **或** 全量定位 `BaiduMapSDK_Location_All` |
| 地图/导航 | 地图 `BaiduMapSDK_Map`、步骑行 `BaiduMapSDK_Map-BWNavi`、驾车导航 `BaiduMapSDK_Map-Navi`、全部导航 `BaiduMapSDK_Map-AllNavi` 中选一（后三者已含地图） |

按需求选：仅展示地图+检索用 Map+Search+Util；要步骑行实时导航用 Map-BWNavi；要驾车导航用 Map-Navi 或 Map-AllNavi。

## 4. NDK 架构（abiFilters）

在 app 的 `build.gradle` 的 `android.defaultConfig` 中配置 so 架构，按需保留：

```gradle
android {
    defaultConfig {
        ndk {
            abiFilters "armeabi-v7a", "arm64-v8a", "x86", "x86_64"
        }
    }
}
```

说明：官方文档曾包含 "armeabi"，目前新包多已不再提供，以实际 SDK 为准。

## 5. 注意事项

- **Gradle 仅支持国内版**：若需 Google 渠道或其它定制包，请到官网下载一体化包，采用「下载 SDK 本地依赖」方式（jar + so 放入 libs/jniLibs，并在 build.gradle 中配置 sourceSets 与 implementation fileTree）。
- 集成完成后需配置 **AndroidManifest**（AK、权限、定位 Service）与 **混淆规则**，见 [project-config.md](project-config.md)；Application 初始化与隐私见 [overview.md](overview.md)。

## 6. 环境与镜像（集成经验）

以下为实际构建时的常见问题与处理，便于 Sync / 运行一次通过。

| 问题 | 处理 |
|------|------|
| **Java 21 与 Gradle 8.2 不兼容** | 升级到 Gradle 8.7（或 8.5+），并同步升级 Android Gradle Plugin（如 8.5.2）。在 `gradle-wrapper.properties` 中设置 `distributionUrl=.../gradle-8.7-bin.zip`。 |
| **Downloading gradle-8.7-bin.zip timeout** | 国内网络可将 `distributionUrl` 改为腾讯云镜像：`https://mirrors.cloud.tencent.com/gradle/gradle-8.7-bin.zip`；并把 `networkTimeout=10000` 改为 `60000`。 |
| **NoClassDefFoundError: org/gradle/wrapper/IDownload** | 工程里的 `gradle-wrapper.jar` 与 Gradle 版本不一致（如仍为 8.2 的 jar 却用 8.7 的 distribution）。需替换为与 8.7 对应的 [官方 gradle-wrapper.jar](https://raw.githubusercontent.com/gradle/gradle/v8.7.0/gradle/wrapper/gradle-wrapper.jar)，校验 SHA-256 见 [Gradle release-checksums](https://gradle.org/release-checksums/)。 |
| **无法定位 Java Runtime** | 终端/IDE 需能找到 JDK。macOS 下可把 Android Studio 自带 JDK 写入 `~/.zshrc`：`export JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"` 与 `export PATH="$JAVA_HOME/bin:$PATH"`。 |
