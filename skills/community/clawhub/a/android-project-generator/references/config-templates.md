# Android 项目配置模板

> 标准化的 Gradle 配置文件模板

## 项目文件结构

```
MyApp/
├── settings.gradle.kts          # 项目设置
├── build.gradle.kts             # 项目级构建配置
├── gradle.properties            # Gradle 属性
├── gradle/
│   └── wrapper/
│       └── gradle-wrapper.properties
├── gradlew                      # Unix 启动脚本
├── gradlew.bat                  # Windows 启动脚本
├── app/
│   ├── build.gradle.kts         # 模块级构建配置
│   └── src/
│       └── main/
│           ├── AndroidManifest.xml
│           ├── java/
│           └── res/
└── local.properties             # 当已知 sdk 路径且需要立即 CLI 构建时生成
```

## 黄金配置：稳定版 (AGP 8.7.0)

### settings.gradle.kts

```kotlin
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "MyApp"
include(":app")
```

### build.gradle.kts (项目级)

```kotlin
// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {
    id("com.android.application") version "8.7.0" apply false
    id("org.jetbrains.kotlin.android") version "2.0.21" apply false
}
```

### app/build.gradle.kts (模块级)

```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.example.myapp"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.example.myapp"
        minSdk = 24
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

kotlinOptions {
    jvmTarget = "17"
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(17))
    }
}

buildFeatures {
    viewBinding = true
}
}

dependencies {
    implementation("androidx.core:core-ktx:1.15.0")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
    implementation("androidx.constraintlayout:constraintlayout:2.2.0")
    
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.2.1")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.6.1")
}
```

### gradle.properties

```properties
# Project-wide Gradle settings.
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
org.gradle.parallel=true
org.gradle.caching=true

# Android settings
android.useAndroidX=true
android.nonTransitiveRClass=true
```

### gradle-wrapper.properties

```properties
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-8.9-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
```

### local.properties

如果检测脚本已经拿到 SDK 路径，并且目标是让当前机器马上执行 `assembleDebug`，补上：

```properties
sdk.dir=C\:\\Users\\<user>\\AppData\\Local\\Android\\Sdk
```

说明：
- Windows 路径中的反斜杠需要转义
- 如果不知道本机 SDK 路径，不要瞎猜
- 如果依赖 `ANDROID_SDK_ROOT` 而不写 `local.properties`，要在最终说明里明确这一点

## 项目级 JDK 绑定建议

根据 Android 官方建议，尽量不要只依赖 shell 当前环境里的 `PATH` java。

推荐顺序：

1. 项目级 Gradle JDK 绑定
2. 明确配置的 `JAVA_HOME`
3. 最后才是 `PATH` 中碰巧存在的 `java`

如果机器已经安装了合适的 JDK，但没有配置 `JAVA_HOME`，应将环境标记为“可运行但不稳定”。

对于需要长期稳定构建的项目，建议使用项目级 Gradle JDK 配置（例如 `GRADLE_LOCAL_JAVA_HOME` / `.gradle/config.properties` 中的 `java.home`）来固定构建所用 JDK。

## 国内镜像配置

### settings.gradle.kts (国内镜像版)

```kotlin
pluginManagement {
    repositories {
        maven { url = uri("https://maven.aliyun.com/repository/gradle-plugin") }
        maven { url = uri("https://maven.aliyun.com/repository/google") }
        maven { url = uri("https://maven.aliyun.com/repository/public") }
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        maven { url = uri("https://maven.aliyun.com/repository/google") }
        maven { url = uri("https://maven.aliyun.com/repository/public") }
    }
}

rootProject.name = "MyApp"
include(":app")
```

## 最小可运行模板

### AndroidManifest.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.MyApp">
        
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
```

### MainActivity.kt

```kotlin
package com.example.myapp

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }
}
```

### activity_main.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
```

## 必需资源文件

### res/values/strings.xml

```xml
<resources>
    <string name="app_name">MyApp</string>
</resources>
```

### res/values/themes.xml

```xml
<resources>
    <style name="Theme.MyApp" parent="Theme.Material3.DayNight.NoActionBar">
        <!-- Customize your theme here. -->
    </style>
</resources>
```

## 编译验证清单

生成项目后，必须执行以下验证：

1. [ ] 检查 JDK 版本: `java -version` (需要 17+)
2. [ ] 检查 SDK 组件: `platforms/android-35`、`build-tools`、`licenses`
3. [ ] 检查 wrapper 完整性: `gradlew`、`gradlew.bat`、`gradle-wrapper.properties`、`gradle-wrapper.jar`
4. [ ] 首次构建: `./gradlew assembleDebug`
5. [ ] 确认无编译错误
6. [ ] 确认生成的 APK 路径: `app/build/outputs/apk/debug/app-debug.apk`

## 构建状态建议

建议将最终结果明确分成三类：

- `scaffolding_only`
  - 仅代表工程结构已生成
  - 环境阻断导致未执行真正构建
- `build_failed`
  - 已执行 Gradle，但构建失败或未找到 APK
- `compiled`
  - `assembleDebug` 成功
  - `app/build/outputs/apk/debug/app-debug.apk` 已确认存在

如有设备或模拟器，可继续扩展为：

- `install_failed`
  - APK 已产出
  - `adb install -r` 失败
- `launch_failed`
  - APK 安装成功
  - 主 Activity 启动失败
- `runnable`
  - APK 已产出
  - APK 安装成功
  - 主 Activity 启动成功

只有 `runnable` 才能被描述为“环境正常、可编译、可运行准备完成”。

## Gradle Wrapper 获取与提交

如果目标是“首次真实构建成功”，以下文件都必须存在：

- `gradlew`
- `gradlew.bat`
- `gradle/wrapper/gradle-wrapper.properties`
- `gradle/wrapper/gradle-wrapper.jar`

只有 `gradle-wrapper.properties` 不够；占位脚本也不够。

可选获取方式：

1. 从已知可用的 Android / Gradle 项目复制完整 wrapper 文件
2. 如果本机已安装 Gradle，执行：

```bash
gradle wrapper --gradle-version 8.9
```

3. 如需最新版配置，可使用相应 Gradle 版本重新生成 wrapper

建议：

- 稳定版配置：Gradle `8.9`
- 最新版配置：Gradle `9.3.1`

提交规则：

- `gradlew`、`gradlew.bat`、`gradle-wrapper.jar` 应提交到版本控制
- 如果当前无法提供完整 wrapper，只能把项目标记为“脚手架已生成，尚未验证可构建”，不能标记为“首次编译成功”
