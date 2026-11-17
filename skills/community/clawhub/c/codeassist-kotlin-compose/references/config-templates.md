# Config File Templates

All config files that must be present in every CodeAssist project.

## manifest.json (ZIP root)

```json
{
  "format": 1,
  "kind": "project",
  "name": "{APP_NAME}",
  "description": "",
  "author": "",
  "createdBy": "CodeAssist",
  "isAndroid": true,
  "packageName": "{PACKAGE_NAME}",
  "moduleCount": 1,
  "modules": ["app"],
  "hasBundledDeps": true,
  "iconEntry": null,
  "store": null
}
```

Replace `{APP_NAME}` with the project name (lowercase, no spaces).
Replace `{PACKAGE_NAME}` with `com.example.{name}`.

## module.toml (project/app/module.toml)

```toml
version = 2

[module]
type = "android-app"
name = "app"
languageLevel = "JAVA_8"
output = "build/classes"

[sourceSets.debug]
scope = "IMPLEMENTATION"
assets = ["src/debug/assets"]
java = ["src/debug/java", "src/debug/kotlin"]
jniLibs = ["src/debug/jniLibs"]
res = ["src/debug/res"]
resources = ["src/debug/resources"]

[sourceSets.main]
scope = "IMPLEMENTATION"
assets = ["src/main/assets"]
java = ["src/main/java", "src/main/kotlin"]
jniLibs = ["src/main/jniLibs"]
res = ["src/main/res"]
resources = ["src/main/resources"]

[sourceSets.release]
scope = "IMPLEMENTATION"
assets = ["src/release/assets"]
java = ["src/release/java", "src/release/kotlin"]
jniLibs = ["src/release/jniLibs"]
res = ["src/release/res"]
resources = ["src/release/resources"]

[dependencies]
implementation = ["kotlin-stdlib", "androidx.activity:activity-compose:1.9.3", "androidx.compose.ui:ui:1.7.5", "androidx.compose.foundation:foundation:1.7.5", "androidx.compose.material3:material3:1.3.1", "androidx.compose.ui:ui-tooling-preview:1.7.5"]

[android]
namespace = "{PACKAGE_NAME}"
compileSdk = 34
minSdk = 21
targetSdk = 34
manifest = "src/main/AndroidManifest.xml"
versionCode = 1
versionName = "1.0"
isApplication = true
buildTypes = [{ name = "debug", debuggable = true, minifyEnabled = false, shrinkResources = false }, { name = "release", debuggable = false, minifyEnabled = false, shrinkResources = false, proguardFiles = ["proguard-android-optimize.txt", "proguard-rules.pro"] }]
compose = true
```

## workspace.json (project/.platform/workspace.json)

```json
{
  "version": 1,
  "projects": [
    {
      "id": "{APP_NAME}",
      "name": "{APP_NAME}",
      "root": "",
      "buildSystem": "native",
      "settings": {},
      "modules": [
        {
          "id": "app",
          "name": "app",
          "dir": "app"
        }
      ],
      "libraries": []
    }
  ]
}
```

## AndroidManifest.xml (project/app/src/main/AndroidManifest.xml)

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="{PACKAGE_NAME}">
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.App">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>
```

Add permissions before `<application>`:
```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
```

## proguard-rules.pro (project/app/proguard-rules.pro)

```pro
# Add project-specific ProGuard/R8 keep rules here.
# These are applied on top of the bundled defaults (proguard-android-optimize.txt) when the
# build type has minifyEnabled = true.
#
# Keep a class that is referenced only by reflection / from XML, e.g.:
# -keep class com.example.SomeClass { *; }
#
# Preserve line numbers for readable crash stack traces, then hide the original file name:
# -keepattributes SourceFile,LineNumberTable
# -renamesourcefileattribute SourceFile
```

## Resource Files

### res/values/colors.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">#3DDC84</color>
</resources>
```

### res/values/strings.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{APP_DISPLAY_NAME}</string>
</resources>
```

### res/values/themes.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.App" parent="android:Theme.Material.Light.NoActionBar"/>
</resources>
```

### res/drawable/ic_launcher_background.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp"
    android:viewportWidth="108" android:viewportHeight="108">
    <path android:fillColor="@color/ic_launcher_background" android:pathData="M0,0h108v108h-108z"/>
</vector>
```

### res/drawable/ic_launcher_foreground.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp"
    android:viewportWidth="108" android:viewportHeight="108">
    <path android:strokeColor="#FFFFFF" android:strokeWidth="2" android:strokeLineCap="round" android:pathData="M45,45L40,37"/>
    <path android:strokeColor="#FFFFFF" android:strokeWidth="2" android:strokeLineCap="round" android:pathData="M63,45L68,37"/>
    <path android:fillColor="#FFFFFF" android:pathData="M38,72L38,58A16,16 0 0 1 70,58L70,72Z"/>
    <path android:fillColor="@color/ic_launcher_background" android:pathData="M45,54a2,2 0 1 0 4,0a2,2 0 1 0 -4,0"/>
    <path android:fillColor="@color/ic_launcher_background" android:pathData="M59,54a2,2 0 1 0 4,0a2,2 0 1 0 -4,0"/>
</vector>
```

### res/mipmap/ic_launcher.xml & ic_launcher_round.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@drawable/ic_launcher_background"/>
    <item android:drawable="@drawable/ic_launcher_foreground"/>
</layer-list>
```

### res/mipmap-anydpi-v26/ic_launcher.xml & ic_launcher_round.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background"/>
    <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>
```

## settings.properties (project/.platform/settings.properties)

```properties
#CodeAssist project settings
```

## open-tabs.txt (project/.platform/open-tabs.txt)

```
#v2
0
```

## Complete Directory Structure

```
{app_name}/
├── manifest.json
├── deps/
│   └── libraries.json
└── project/
    ├── .platform/
    │   ├── open-tabs.txt
    │   ├── settings.properties
    │   └── workspace.json
    └── app/
        ├── module.toml
        ├── proguard-rules.pro
        └── src/main/
            ├── AndroidManifest.xml
            └── kotlin/com/example/{name}/
            │   ├── MainActivity.kt
            │   └── (other .kt files)
            └── res/
                ├── drawable/
                │   ├── ic_launcher_background.xml
                │   └── ic_launcher_foreground.xml
                ├── mipmap/
                │   ├── ic_launcher.xml
                │   └── ic_launcher_round.xml
                ├── mipmap-anydpi-v26/
                │   ├── ic_launcher.xml
                │   └── ic_launcher_round.xml
                └── values/
                    ├── colors.xml
                    ├── strings.xml
                    └── themes.xml
```
