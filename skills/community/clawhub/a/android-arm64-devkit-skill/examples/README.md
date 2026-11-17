# Examples

## Demo — build toolchain + project scaffold on ARM64

Captured on an **aarch64 Linux** host (NVIDIA DGX Spark), run from the
repository root. Paths are shortened (`$ANDROID_SDK`).

### 1. Diagnose the toolchain

```console
$ bash scripts/setup-aapt2-arm64.sh
== host ==
  arch: aarch64

== candidates on PATH / SDK ==
  $ANDROID_SDK/build-tools/34.0.0/aapt2   x86-64
    -> NOT runnable here (expected on this host)
  $ANDROID_SDK/build-tools/35.0.0/aapt2   x86-64
    -> NOT runnable here (expected on this host)
  $ANDROID_SDK/build-tools/36.0.0/aapt2   x86-64
    -> NOT runnable here (expected on this host)
  /usr/bin/aapt2                          symbolic link to ../lib/android-sdk/build-tools/debian/aapt2
    -> NOT runnable here (expected on this host)
  /usr/lib/android-sdk/build-tools/debian/aapt2   ARM aarch64
    -> runs? Android Asset Packaging Tool (aapt) 2.19-debian

== Debian aarch64 build-tools ==
  found: /usr/lib/android-sdk/build-tools/debian/aapt2
  arch : ARM aarch64
```

Google's SDK `aapt2` are **x86-64** and die with `Exec format error` on aarch64;
the Debian **aarch64** build runs.

### 2. Scaffold an app (already wired to the native aapt2)

```console
$ bash scripts/new-project.sh /tmp/demo-app com.example.demo "Demo App"
== scaffolding Demo App (com.example.demo) into /tmp/demo-app ==
== applying the aarch64 aapt2 override (single source: setup-aapt2-arm64.sh) ==
  wrote local.properties (sdk.dir=$ANDROID_SDK)
== gradle wrapper ==
  created gradlew + gradle/wrapper/

== done: /tmp/demo-app ==
```

Project tree (abridged):

```text
app/build.gradle.kts
app/src/main/AndroidManifest.xml
app/src/main/java/com/example/demo/MainActivity.kt
app/src/main/res/...
build.gradle.kts
gradle.properties
gradle/wrapper/gradle-wrapper.properties
gradlew
settings.gradle.kts
```

`gradle.properties` gets the override appended (idempotently):

```properties
android.aapt2FromMavenOverride=/usr/lib/android-sdk/build-tools/debian/aapt2
```

### 3. Self-test suite

```console
$ bash tests/run-tests.sh
...
TOTAL: 36 passed, 0 failed
```

> Building (`./gradlew clean assembleDebug`) additionally needs the Android SDK
> and a JDK, so it is not part of this example. The deploy/verify branch needs a
> real device; it is exercised by `tests/run-tests.sh` through stub `adb`/`ssh`.
