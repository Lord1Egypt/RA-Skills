#!/usr/bin/env bash
# Scaffold a minimal Android app (Gradle + Kotlin, one Activity) that is ready
# for this devkit: the aarch64 aapt2 override is applied by setup-aapt2-arm64.sh.
#
# Usage:
#   ./scripts/new-project.sh <target-dir> <package-id> [app-name]
#
# Example:
#   ./scripts/new-project.sh ~/apps/MyApp com.example.myapp "My App"
#
# Notes:
#   - Refuses to write into an existing path.
#   - minSdk is 26 so only an adaptive icon is needed (no binary PNGs).
#   - Creates the Gradle wrapper only if `gradle` is on PATH.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() { echo "usage: $0 <target-dir> <package-id> [app-name]" >&2; exit 2; }

[ $# -ge 2 ] || usage
DEST="$1"
PKG="$2"
NAME="${3:-$(basename "$DEST")}"

# --- validate the package id: dot-separated Java identifiers -----------------
case "$PKG" in
  *[!A-Za-z0-9._]*|*..*|.*|*.) echo "invalid package id: $PKG" >&2; exit 2 ;;
esac
OLDIFS="$IFS"; IFS='.'; set -- $PKG; IFS="$OLDIFS"
[ $# -ge 2 ] || { echo "package id needs at least two segments: $PKG" >&2; exit 2; }
for seg in "$@"; do
  case "$seg" in
    [A-Za-z_]*) ;;
    *) echo "invalid package segment: $seg" >&2; exit 2 ;;
  esac
done

if [ -e "$DEST" ]; then
  echo "refusing to overwrite existing path: $DEST" >&2
  exit 2
fi

PKG_PATH="$(printf '%s' "$PKG" | tr '.' '/')"
SAFE="$(printf '%s' "$NAME" | sed 's/[^A-Za-z0-9]//g')"
[ -n "$SAFE" ] || SAFE=App

echo "== scaffolding $NAME ($PKG) into $DEST =="
mkdir -p "$DEST/gradle" \
         "$DEST/app/src/main/java/$PKG_PATH" \
         "$DEST/app/src/main/res/values" \
         "$DEST/app/src/main/res/layout" \
         "$DEST/app/src/main/res/xml" \
         "$DEST/app/src/main/res/drawable" \
         "$DEST/app/src/main/res/mipmap-anydpi-v26"

cat > "$DEST/settings.gradle.kts" <<EOF
pluginManagement {
    repositories {
        google {
            content {
                includeGroupByRegex("com\\\\.android.*")
                includeGroupByRegex("com\\\\.google.*")
                includeGroupByRegex("androidx.*")
            }
        }
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

rootProject.name = "$NAME"
include(":app")
EOF

cat > "$DEST/build.gradle.kts" <<'EOF'
plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false
}
EOF

cat > "$DEST/gradle.properties" <<'EOF'
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
org.gradle.parallel=true
org.gradle.caching=true
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
EOF

cat > "$DEST/gradle/libs.versions.toml" <<'EOF'
[versions]
agp = "8.13.1"
kotlin = "2.2.21"
coreKtx = "1.10.1"
appcompat = "1.6.1"
material = "1.10.0"

[libraries]
androidx-core-ktx = { group = "androidx.core", name = "core-ktx", version.ref = "coreKtx" }
androidx-appcompat = { group = "androidx.appcompat", name = "appcompat", version.ref = "appcompat" }
material = { group = "com.google.android.material", name = "material", version.ref = "material" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
EOF

cat > "$DEST/.gitignore" <<'EOF'
.gradle/
build/
local.properties
*.iml
.idea/
EOF

cat > "$DEST/app/build.gradle.kts" <<EOF
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
}

android {
    namespace = "$PKG"
    compileSdk = 34

    defaultConfig {
        applicationId = "$PKG"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        release { isMinifyEnabled = false }
        getByName("debug") { isDebuggable = true }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.material)
}
EOF

cat > "$DEST/app/src/main/AndroidManifest.xml" <<EOF
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.$SAFE">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:label="@string/app_name"
            android:theme="@style/Theme.$SAFE">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
EOF

cat > "$DEST/app/src/main/java/$PKG_PATH/MainActivity.kt" <<EOF
package $PKG

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }
}
EOF

cat > "$DEST/app/src/main/res/values/strings.xml" <<EOF
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">$NAME</string>
    <string name="subtitle">Scaffolded by android-arm64-devkit-skill</string>
</resources>
EOF

cat > "$DEST/app/src/main/res/values/themes.xml" <<EOF
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.$SAFE" parent="Theme.MaterialComponents.DayNight.NoActionBar">
        <item name="colorPrimary">#2E7D32</item>
        <item name="colorOnPrimary">#FFFFFF</item>
    </style>
</resources>
EOF

cat > "$DEST/app/src/main/res/layout/activity_main.xml" <<'EOF'
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="32dp">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/app_name"
        android:textSize="28sp" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:paddingTop="12dp"
        android:text="@string/subtitle"
        android:textSize="16sp" />
</LinearLayout>
EOF

cat > "$DEST/app/src/main/res/xml/backup_rules.xml" <<'EOF'
<?xml version="1.0" encoding="utf-8"?>
<full-backup-content/>
EOF

cat > "$DEST/app/src/main/res/xml/data_extraction_rules.xml" <<'EOF'
<?xml version="1.0" encoding="utf-8"?>
<data-extraction-rules>
    <cloud-backup />
    <device-transfer />
</data-extraction-rules>
EOF

cat > "$DEST/app/src/main/res/drawable/ic_launcher_background.xml" <<'EOF'
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <solid android:color="#2E7D32" />
</shape>
EOF

cat > "$DEST/app/src/main/res/drawable/ic_launcher_foreground.xml" <<'EOF'
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#FFFFFF"
        android:pathData="M34,34 h40 v40 h-40 z" />
</vector>
EOF

cat > "$DEST/app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml" <<'EOF'
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
</adaptive-icon>
EOF

cp "$DEST/app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml" \
   "$DEST/app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml"

echo "== applying the aarch64 aapt2 override (single source: setup-aapt2-arm64.sh) =="
bash "$HERE/setup-aapt2-arm64.sh" --write-gradle-property "$DEST" >/dev/null

if [ -n "${ANDROID_HOME:-}" ]; then
  printf 'sdk.dir=%s\n' "$ANDROID_HOME" > "$DEST/local.properties"
  echo "  wrote local.properties (sdk.dir=$ANDROID_HOME)"
else
  echo "  ANDROID_HOME is not set: create local.properties yourself (sdk.dir=...)"
fi

if command -v gradle >/dev/null 2>&1; then
  echo "== gradle wrapper =="
  ( cd "$DEST" && gradle wrapper >/dev/null && echo "  created gradlew + gradle/wrapper/" )
else
  echo "  gradle not on PATH: run 'gradle wrapper' in the project, or add the wrapper files"
fi

cat <<EOF

== done: $DEST ==

next steps:
  1. cd "$DEST"
  2. ./gradlew clean assembleDebug        # require "M executed" with M > 0
  3. (devkit) scripts/adb-connect.sh      # with config.sh prepared
  4. (devkit) scripts/adb-install-verify.sh app/build/outputs/apk/debug/app-debug.apk
EOF
