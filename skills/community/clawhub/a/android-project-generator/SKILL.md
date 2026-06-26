---
name: android-project-generator
description: Generate Android projects that compile on the first real build, including optional JNI/NDK/CMake native setup. Use when creating new Android apps, configuring Gradle and version compatibility, validating assembleDebug readiness, or adding native modules.
description_en: Generate Android projects that compile on the first real build, including optional JNI/NDK/CMake native setup. Use when creating new Android apps, configuring Gradle and version compatibility, validating assembleDebug readiness, or adding native modules.
description_zh: 生成以首次真实构建通过为目标的 Android 工程，并支持可选的 JNI/NDK/CMake Native 集成。当你需要创建新 Android 应用、配置 Gradle 与版本兼容性、验证 assembleDebug 可构建性，或接入 Native 模块时使用此技能。
license: MIT
metadata:
  author: oahcfly
  version: 1.3.0
  category: mobile
---

# Android Project Generator Skill

## Purpose

Ensure AI-generated Android projects compile successfully on the first attempt by providing:

1. **Version compatibility knowledge** — AGP/Gradle/JDK/Kotlin version matrices
2. **Standardized configuration templates** — Complete, working Gradle configurations
3. **Environment detection** — Adapt to local JDK/SDK versions
4. **Post-generation validation** — Verify compilation succeeds
5. **APK build orchestration** — Distinguish between scaffolding-only, build-failed, and compiled APK states
6. **Native integration guidance** — Detect native intent and scaffold JNI/NDK/CMake-compatible project configuration

## Runtime & Safety Requirements

Before using this skill on a production or sensitive machine, verify:

- Required binaries are present in PATH: `python`, `java`, and at least one of `gradle`/`gradlew`.
- Android tooling is installed on disk for real build validation: Android SDK (platforms/build-tools/cmdline-tools/licenses), and optional NDK+CMake for native flows.
- Environment variables are correctly scoped: `JAVA_HOME` (recommended), `ANDROID_HOME` or `ANDROID_SDK_ROOT`, optional `ANDROID_NDK_HOME` or `NDK_HOME` for native workflows.
- Local command execution is acceptable in the current host policy.
- Device interactions (`adb install`, `adb shell am start`) are allowed for connected devices/emulators.
- Build-time network access is acceptable (for Gradle wrapper/dependency resolution).

This skill runs local commands and may perform build/device operations; treat it as operational code, not documentation-only guidance. It does not request API keys, tokens, or cloud credentials by design.

## Credentials

This skill does not require cloud credentials, API keys, or tokens.

It does rely on local environment variables and installed binaries/tooling:

- Env vars inspected/used: `JAVA_HOME`, `ANDROID_HOME`/`ANDROID_SDK_ROOT`, and for native projects `ANDROID_NDK_HOME`/`NDK_HOME`.
- Binaries/tooling expected: `java`, `gradle`/`gradlew`, Android SDK/NDK on disk, and optional `adb` for install/launch verification.

The scripts do not intentionally exfiltrate data, but they do run subprocesses that may:

- access network resources (for Gradle wrapper/dependency downloads)
- interact with attached devices/emulators (`adb`)

## When to Use This Skill

Trigger this skill when:
- Creating a new Android project from scratch
- Generating Gradle configuration files (`build.gradle.kts`, `settings.gradle.kts`)
- Setting up Android project structure
- Adding or planning C/C++ native code (`JNI`, `NDK`, `CMake`, `externalNativeBuild`)
- User asks to "create an Android app" or "generate an Android project"
- Debugging Gradle version compatibility issues

## Workflow

### Phase 1: Audit the Build Environment First

If the project is meant to build on the current machine, do not generate files yet. Audit the environment first:

```bash
python scripts/detect_env.py
```

Treat this phase as mandatory for local project generation because most "AI generated Android project won't compile" failures are environment mismatches, not template mistakes.

This outputs:
- JDK version → determines AGP version range
- `JAVA_HOME` configuration and version
- `PATH` java executable and version
- Gradle CLI JDK source (`JAVA_HOME` vs `PATH`)
- Android SDK path and build-tools versions
- Installed Android platforms
- cmdline-tools / licenses readiness
- NDK version (if present)
- Recommended configuration for the detected environment
- Environment assessment with blocking issues and warnings

If `ready_for_build` is false:
- Explain the blocking issues clearly
- Prefer fixing the environment before generating a "build-ready" project
- If the user still wants files generated, say the project is scaffolding-only until the environment issues are fixed

If the environment status is `degraded`:
- Explain why the build is risky rather than blocked
- Most commonly this means JDK 17 exists but `JAVA_HOME` is missing, so Gradle is falling back to `PATH`
- Recommend aligning Android Studio, CLI Gradle, and project-level JDK configuration before claiming the build setup is stable

### Phase 2: Select Configuration Profile

Base the profile on audited environment data, not guesswork:

| Profile | AGP | Gradle | JDK | Use Case |
|---------|-----|--------|-----|----------|
| stable | 8.7.0 | 8.9 | 17+ | Recommended for most projects |
| latest | 9.1.0 | 9.3.1 | 17+ | New features, Android 16+ |
| legacy | 7.4.2 | 7.5 | 11+ | Older environments |

**Default to "stable" profile only when the environment is ready for it.**

Use this decision order:
1. If JDK 17+, `platforms/android-35`, and build-tools are present → use `stable`
2. If user explicitly wants Android 16 / newest APIs and the environment supports it → use `latest`
3. If JDK is 11-16 → use `legacy`
4. If the environment is incomplete → stop and surface what is missing before claiming the project is build-ready

Native 触发策略（`native_enabled`）：
- 默认 `native_enabled = false`
- 如果提示词命中强信号（如 `JNI`、`NDK`、`CMake`、`externalNativeBuild`、`C++`、`native library`、`原生模块`）→ 自动切到 `native_enabled = true`
- 如果只命中弱信号（如 `native`、`底层`、`性能优化`）→ 先标记候选并二次确认，再决定是否开启
- 若用户显式指定（例如 `native_enabled=true/false`），显式配置优先于关键词推断

Additional JDK rules:
- Prefer a clearly configured `JAVA_HOME` over an accidental `PATH` java
- If `JAVA_HOME` and `PATH` java disagree, treat that as a reproducibility risk and explain it
- Prefer a project-level Gradle JDK setting for long-term consistency

### Phase 3: Generate Project Structure

Always create the complete file structure:

```
ProjectName/
├── settings.gradle.kts
├── build.gradle.kts
├── gradle.properties
├── gradle/
│   └── wrapper/
│       └── gradle-wrapper.properties
├── gradlew
├── gradlew.bat
├── app/
│   ├── build.gradle.kts
│   ├── src/
│   │   └── main/
│   │       ├── AndroidManifest.xml
│   │       ├── java/com/example/project/
│   │       │   └── MainActivity.kt
│   │       └── res/
│   │           ├── layout/
│   │           │   └── activity_main.xml
│   │           ├── values/
│   │           │   ├── strings.xml
│   │           │   └── themes.xml
│   │           └── mipmap-*/
│   │               ├── ic_launcher.png
│   │               └── ic_launcher_round.png
│   └── proguard-rules.pro
└── local.properties (create when sdk path is known and immediate CLI build is expected)
```

Important:
- Do not stop at "mostly complete"
- The generated project is not considered ready until wrapper files and validation are in place
- If SDK path is known and the goal is immediate command-line build, create `local.properties` with `sdk.dir=...` to reduce local environment ambiguity
- If the machine has JDK 17 but no stable project-level JDK selection, recommend `GRADLE_LOCAL_JAVA_HOME` or equivalent project-scoped JDK binding

### Phase 4: Use Configuration Templates

Load templates from `references/config-templates.md`:

- Use the "Golden Configuration: Stable" section for the "stable" profile
- Use the "China Mirror" variant for users in China (detected by locale or explicit request)
- Replace placeholders: `MyApp`, `com.example.myapp`, `com.example.myapp.MainActivity`
- Keep `namespace`, `applicationId`, source package path, and theme names aligned
- If generating a project that must build immediately, prefer the template path that includes `local.properties`

### Phase 5: Make Gradle Wrapper Real, Not Placeholder

Before reporting the project as buildable, ensure the wrapper is genuinely usable:

- Required files:
  - `gradlew`
  - `gradlew.bat`
  - `gradle/wrapper/gradle-wrapper.properties`
  - `gradle/wrapper/gradle-wrapper.jar`
- A `gradle-wrapper.properties` file alone is not enough
- Placeholder scripts are not acceptable for a claimed "first build succeeds" result

Use one of these approaches:
1. Copy wrapper files from a known-good template project
2. Generate them with `gradle wrapper --gradle-version <target-version>` if Gradle is installed
3. If neither is possible, explicitly say wrapper generation is incomplete and do not claim the project is ready for `assembleDebug`

You can use `scripts/project_validator.py` logic as the acceptance bar:
- invalid package name => block
- missing wrapper jar => block
- placeholder wrapper scripts => block

### Phase 6: Validate Compilation with a Real Build Loop

After generating all files, **MUST** run:

```bash
./gradlew assembleDebug
```

If compilation fails:
1. Read the error message carefully
2. Check version compatibility in `references/version-matrix.md`
3. Check whether the failure is really caused by environment readiness, wrapper incompleteness, or template/config mismatch
4. Fix one root cause at a time and retry
5. Do not report success until `assembleDebug` passes with the generated project

If the wrapper is unavailable or the environment is missing mandatory SDK components:
- Do not present the project as "verified buildable"
- Say exactly which prerequisite prevented real verification

### Phase 7: Confirm APK Output and Runtime Readiness

After `assembleDebug`, verify that the debug APK really exists:

```text
app/build/outputs/apk/debug/app-debug.apk
```

Use `scripts/build_flow.py` concepts as the final status model:

- `scaffolding_only`
  - Files were generated
  - Build was not attempted because the environment was blocked
- `build_failed`
  - Gradle ran, but `assembleDebug` failed or no APK was produced
- `compiled`
  - `assembleDebug` succeeded and the debug APK exists

If a device or emulator is available, continue one more step:

- install the debug APK
- launch the main activity
- only then classify the project as `runnable`

Additional final states:

- `install_failed`
  - APK exists
  - installation to device/emulator failed
- `launch_failed`
  - APK installed
  - main activity launch failed
- `runnable`
  - APK built
  - APK installed
  - main activity launched successfully

Only the `compiled` state should be described as:
- environment normal
- project buildable
- APK produced

Only the `runnable` state should be described as:
- environment normal
- project buildable
- app installable
- app launch verified on device or emulator

## Reference Files

### Version Compatibility Matrix

See `references/version-matrix.md` for:
- AGP 9.x / 8.x / 7.x version requirements
- Kotlin compatibility with AGP
- Gradle Wrapper configuration

Key rules:
- AGP 8.0+ requires JDK 17 (non-negotiable)
- AGP 9.x requires Gradle 9.1+
- Always check the matrix when in doubt

### Configuration Templates

See `references/config-templates.md` for:
- Complete `settings.gradle.kts` template
- Project-level and module-level `build.gradle.kts`
- `gradle.properties` defaults
- `gradle-wrapper.properties` format
- Minimal `MainActivity.kt` and `AndroidManifest.xml`
- China mirror configuration

## Environment Detection Script

`scripts/detect_env.py` provides:

- JDK version detection (parses `java -version` output)
- Android SDK path discovery (ANDROID_HOME, ANDROID_SDK_ROOT, common paths)
- Build-tools version listing
- NDK version detection
- Recommended configuration based on detected JDK

Run this script to adapt the generated project to the user's actual environment.

## Critical Rules

1. **Never skip the validation step** — Always run `./gradlew assembleDebug`
2. **JDK 17 is mandatory for AGP 8.x+** — Do not generate AGP 8.x config if JDK < 17
3. **Use Kotlin DSL (.kts)** — Groovy DSL is legacy, prefer `build.gradle.kts`
4. **Set correct namespace** — AGP 8.0+ requires namespace in build.gradle, not manifest
5. **A real wrapper is mandatory for build claims** — Do not rely on placeholder scripts
6. **Create `local.properties` when immediate local CLI build is required and sdk path is known**
7. **Prefer explicit JDK selection** — Align `JAVA_HOME`, Android Studio Gradle JDK, and project-level Gradle JDK settings
8. **Use Java toolchains** — Declare the required Java toolchain instead of relying only on machine defaults
9. **Use Version Catalog for complex projects** — Consider `gradle/libs.versions.toml` for larger projects

## Common Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| Missing `namespace` in app/build.gradle.kts | Add `namespace = "com.example.myapp"` in `android {}` block |
| Wrong JDK version for AGP 8.x | Use AGP 7.x if JDK < 17, or instruct user to install JDK 17 |
| Inconsistent AGP/Gradle versions | Check `version-matrix.md`, use recommended pairs |
| Missing or fake Gradle Wrapper files | Always include `gradlew`, `gradlew.bat`, `gradle-wrapper.properties`, and `gradle-wrapper.jar` |
| Wrong `compileSdk` for AGP version | AGP 8.7+ requires `compileSdk = 35`, AGP 9.x requires `compileSdk = 36` |
| Missing SDK platform or build-tools | Check environment audit before generation; install missing SDK components first |
| Build verified only in theory | Do not claim success without a real `assembleDebug` run |
| `JAVA_HOME` missing but PATH java exists | Treat as degraded, not fully stable; recommend explicit JDK configuration |
| `JAVA_HOME` and PATH java point to different JDKs | Explain that Gradle CLI will prefer `JAVA_HOME`, which can differ from shell expectations |
| `assembleDebug` succeeded but no APK found | Treat as build verification failure until `app-debug.apk` is confirmed |
| APK exists but install fails | Treat as `install_failed`; do not claim the app is runnable |
| Install succeeds but launch fails | Treat as `launch_failed`; do not claim runtime verification passed |

## Example Usage

**User:** "Create a new Android project called TodoApp"

**AI Response:**

1. Load this skill
2. Run `detect_env.py` (if possible)
3. Check the environment assessment and confirm it is ready for a stable build
4. Select "stable" profile (AGP 8.7.0, Gradle 8.9)
5. Generate complete project structure from templates
6. Replace placeholders: `MyApp` → `TodoApp`, `com.example.myapp` → `com.example.todoapp`
7. Ensure real wrapper files exist, not placeholders
8. Run `./gradlew assembleDebug`
9. Confirm `app/build/outputs/apk/debug/app-debug.apk` exists
10. If a device or emulator is available, install the APK and launch the main activity
11. Report `compiled` only if build + APK verification pass
12. Report `runnable` only if build + install + launch all pass

---

This skill transforms Android project generation from a guessing game into an audited, verifiable build process.
