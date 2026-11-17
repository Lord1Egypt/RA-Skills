#!/usr/bin/env python3
"""
CodeAssist Kotlin + Compose project scaffolder.
Generates the complete project skeleton (module.toml, no Gradle) ready for CodeAssist import.

Usage:
    python package_project.py --name "myapp" [--package "com.example.myapp"]

Note: this is a functional reconstruction of the original scaffolder that ships
with the codeassist-kotlin-compose skill. It produces the same output structure.
"""
import argparse
import json
import os
import shutil
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DIRECT_DEPS = [
    "kotlin-stdlib",
    "androidx.activity:activity-compose:1.9.3",
    "androidx.compose.ui:ui:1.7.5",
    "androidx.compose.foundation:foundation:1.7.5",
    "androidx.compose.material3:material3:1.3.1",
    "androidx.compose.ui:ui-tooling-preview:1.7.5",
]

MANIFEST_JSON = """{
  "format": 1,
  "kind": "project",
  "name": "{name}",
  "description": "",
  "author": "",
  "createdBy": "CodeAssist",
  "isAndroid": true,
  "packageName": "{package}",
  "moduleCount": 1,
  "modules": ["app"],
  "hasBundledDeps": true,
  "iconEntry": null,
  "store": null
}
"""

MODULE_TOML = """version = 2

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
namespace = "{package}"
compileSdk = 34
minSdk = 21
targetSdk = 34
manifest = "src/main/AndroidManifest.xml"
versionCode = 1
versionName = "1.0"
isApplication = true
buildTypes = [{ name = "debug", debuggable = true, minifyEnabled = false, shrinkResources = false }, { name = "release", debuggable = false, minifyEnabled = false, shrinkResources = false, proguardFiles = ["proguard-android-optimize.txt", "proguard-rules.pro"] }]
compose = true
"""

WORKSPACE_JSON = """{
  "version": 1,
  "projects": [
    {
      "id": "{name}",
      "name": "{name}",
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
"""

ANDROID_MANIFEST = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="{package}">
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
"""

PROGUARD = """# Add project-specific ProGuard/R8 keep rules here.
# These are applied on top of the bundled defaults (proguard-android-optimize.txt) when the
# build type has minifyEnabled = true.
#
# Keep a class that is referenced only by reflection / from XML, e.g.:
# -keep class com.example.SomeClass { *; }
#
# Preserve line numbers for readable crash stack traces, then hide the original file name:
# -keepattributes SourceFile,LineNumberTable
# -renamesourcefileattribute SourceFile
"""

MAIN_ACTIVITY = """package {package}

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    App()
                }
            }
        }
    }
}

@Composable
fun App() {
    Text(text = "Hello, CodeAssist!")
}

@Preview(showBackground = true)
@Composable
fun AppPreview() {
    App()
}
"""

COLORS_XML = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">#3DDC84</color>
</resources>
"""

STRINGS_XML = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{display_name}</string>
</resources>
"""

THEMES_XML = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.App" parent="android:Theme.Material.Light.NoActionBar"/>
</resources>
"""

DRAWABLE_BG = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp"
    android:viewportWidth="108" android:viewportHeight="108">
    <path android:fillColor="@color/ic_launcher_background" android:pathData="M0,0h108v108h-108z"/>
</vector>
"""

DRAWABLE_FG = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp"
    android:viewportWidth="108" android:viewportHeight="108">
    <path android:strokeColor="#FFFFFF" android:strokeWidth="2" android:strokeLineCap="round" android:pathData="M45,45L40,37"/>
    <path android:strokeColor="#FFFFFF" android:strokeWidth="2" android:strokeLineCap="round" android:pathData="M63,45L68,37"/>
    <path android:fillColor="#FFFFFF" android:pathData="M38,72L38,58A16,16 0 0 1 70,58L70,72Z"/>
    <path android:fillColor="@color/ic_launcher_background" android:pathData="M45,54a2,2 0 1 0 4,0a2,2 0 1 0 -4,0"/>
    <path android:fillColor="@color/ic_launcher_background" android:pathData="M59,54a2,2 0 1 0 4,0a2,2 0 1 0 -4,0"/>
</vector>
"""

MIPMAP_LAYER = """<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@drawable/ic_launcher_background"/>
    <item android:drawable="@drawable/ic_launcher_foreground"/>
</layer-list>
"""

MIPMAP_ADAPTIVE = """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background"/>
    <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>
"""

SETTINGS_PROPERTIES = """#CodeAssist project settings
"""

OPEN_TABS = """#v2
0
"""


def write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def sub(template: str, **kw) -> str:
    """Token replace que nao conflita com chaves de JSON/TOML."""
    out = template
    for key, val in kw.items():
        out = out.replace("{" + key + "}", str(val))
    return out


def build_libraries_json(out_path: str) -> None:
    """Copy the bundled templates/libraries.json; generate a minimal one if missing."""
    bundled = os.path.join(SCRIPT_DIR, "..", "templates", "libraries.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    if os.path.isfile(bundled):
        shutil.copyfile(bundled, out_path)
        return
    # Fallback: minimal manifest with the 5 direct dependencies
    libs = [
        {
            "name": dep,
            "scope": "IMPLEMENTATION",
            "type": "android-library" if ":" in dep else "java-library",
        }
        for dep in DIRECT_DEPS
    ]
    write(out_path, json.dumps({"format": 1, "libraries": libs}, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a CodeAssist Kotlin+Compose project")
    parser.add_argument("--name", required=True, help="Project name (lowercase, no spaces)")
    parser.add_argument("--package", dest="package_name", default=None, help="Android package name")
    parser.add_argument("--output", default=".", help="Base output directory")
    args = parser.parse_args()

    name = args.name.strip().lower().replace(" ", "-")
    if not name.replace("-", "").isalnum() or not name:
        print(f"ERROR: invalid project name '{args.name}'", file=sys.stderr)
        return 1

    package = args.package_name or f"com.example.{name.replace('-', '')}"
    display_name = name.replace("-", " ").title()

    root = os.path.join(args.output, name)
    app = os.path.join(root, "project", "app")
    src = os.path.join(app, "src", "main")
    res = os.path.join(src, "res")
    pkg_path = os.path.join(src, "kotlin", *package.split("."))

    # Root + platform files
    write(os.path.join(root, "manifest.json"), sub(MANIFEST_JSON, name=name, package=package))
    build_libraries_json(os.path.join(root, "deps", "libraries.json"))
    platform = os.path.join(root, "project", ".platform")
    write(os.path.join(platform, "workspace.json"), sub(WORKSPACE_JSON, name=name))
    write(os.path.join(platform, "settings.properties"), SETTINGS_PROPERTIES)
    write(os.path.join(platform, "open-tabs.txt"), OPEN_TABS)

    # Module config
    write(os.path.join(app, "module.toml"), sub(MODULE_TOML, package=package))
    write(os.path.join(app, "proguard-rules.pro"), PROGUARD)
    write(os.path.join(src, "AndroidManifest.xml"), sub(ANDROID_MANIFEST, package=package))

    # Kotlin starter
    write(os.path.join(pkg_path, "MainActivity.kt"), sub(MAIN_ACTIVITY, package=package))

    # Resources (9 files)
    write(os.path.join(res, "values", "colors.xml"), COLORS_XML)
    write(os.path.join(res, "values", "strings.xml"), sub(STRINGS_XML, display_name=display_name))
    write(os.path.join(res, "values", "themes.xml"), THEMES_XML)
    write(os.path.join(res, "drawable", "ic_launcher_background.xml"), DRAWABLE_BG)
    write(os.path.join(res, "drawable", "ic_launcher_foreground.xml"), DRAWABLE_FG)
    write(os.path.join(res, "mipmap", "ic_launcher.xml"), MIPMAP_LAYER)
    write(os.path.join(res, "mipmap", "ic_launcher_round.xml"), MIPMAP_LAYER)
    write(os.path.join(res, "mipmap-anydpi-v26", "ic_launcher.xml"), MIPMAP_ADAPTIVE)
    write(os.path.join(res, "mipmap-anydpi-v26", "ic_launcher_round.xml"), MIPMAP_ADAPTIVE)

    print(f"Project skeleton created at ./{name}")
    print(f"  Package: {package}")
    print(f"  Kotlin source: ./{name}/project/app/src/main/kotlin/{package.replace('.', '/')}/")
    print(f"  Resources: ./{name}/project/app/src/main/res/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
