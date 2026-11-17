---
name: codeassist-kotlin-compose
description: >-
  Gera projetos Android completos em Kotlin + Jetpack Compose + Material 3 no formato do CodeAssist (com.tyron.code), prontos para importar e compilar direto no celular. Use quando o usuário pedir para criar app Android, app Kotlin, app Compose, projeto CodeAssist, ou qualquer combinação de "cria um app", "faz um aplicativo", "monta um projeto" — exceto quando pedir Rust no backend (use kotlin-rust-app) ou JStudio (use jstudio-android-dev).
metadata:
  execution_mode: sandbox
---

# CodeAssist Kotlin + Jetpack Compose App Generator

Generate complete Android app projects in CodeAssist format (module.toml, no Gradle) with Kotlin + Jetpack Compose + Material 3 ultra-modern design.

## Target Environment

- **IDE**: CodeAssist (`com.tyron.code`) — mobile IDE that compiles on-device
- **Build system**: Native (NOT Gradle) — uses `module.toml` instead of `build.gradle`
- **Language**: Kotlin (latest) + Jetpack Compose
- **UI Framework**: Material 3 (`androidx.compose.material3`)
- **Min SDK**: 21 | **Target/Compile SDK**: 34

## CRITICAL Rules

1. **NEVER use Gradle files** — no `build.gradle`, `build.gradle.kts`, `settings.gradle`, or `libs.versions.toml`
2. **ALWAYS use `module.toml`** for build configuration
3. **Source files go in `src/main/kotlin/`** (NOT `src/main/java/`)
4. **Package structure**: `com.example.{appname}` (or user-specified)
5. **ALL resource files required** — drawable, mipmap, mipmap-anydpi-v26, values (colors, strings, themes)
6. **Design MUST be ultra-modern** — Material 3, rounded corners, gradients, animations, dark/light theme
7. **Only use available dependencies** — see dependency list in `references/dependencies.md`
8. **ZIP format MUST match CodeAssist export format exactly**
9. **NEVER include `.exmu-cfg1.data`** binary files — they are IDE-internal and auto-generated
10. **NEVER add `exportedAt` or `fileCount` or `uncompressedSize`** to manifest.json — they are export-only metadata

## Workflow

### Step 1: Understand the Request

Parse what the user wants: app name, features, screens, permissions. If the request is clear, skip questions and proceed directly.

### Step 2: Create Project Skeleton

Run the packager script to scaffold the base structure:

```bash
python scripts/package_project.py --name "{app_name}" --package "com.example.{name}"
```

This creates all config files (manifest.json, module.toml, workspace.json, libraries.json, AndroidManifest.xml, proguard-rules.pro) and the resource templates (colors.xml, strings.xml, themes.xml, icons).

### Step 3: Write Kotlin Source Code

Write all `.kt` files under the generated path: `{name}/project/app/src/main/kotlin/com/example/{name}/`

**Design rules (MANDATORY):**
- Material 3 theme — use `MaterialTheme` with custom `ColorScheme`
- `Surface` and `Scaffold` as root composables
- `TopAppBar` (Material 3 `CenterAlignedTopAppBar` or `MediumTopAppBar`)
- Rounded corners: `RoundedCornerShape(16.dp)` on cards/containers
- Padding: `16.dp` standard, `24.dp` for sections
- `Card` composables for content blocks with `elevation`
- `LazyColumn` / `LazyRow` for scrollable content
- State with `remember { mutableStateOf(...) }` and `by remember`
- Screen navigation via state enum (NO Navigation library)
- One file per screen/feature for complex apps
- `Column`, `Row`, `Box` for layout composition
- `Icon` with `Icons.Default.*` or `Icons.Outlined.*`
- `AnimatedVisibility`, `animateContentSize()` for smooth transitions
- Custom color palette in a `Theme.kt` or inside `MainActivity.kt`

**Available APIs** — see `references/dependencies.md`

**NOT available (NEVER use):**
- `androidx.navigation` — Navigation component
- `androidx.room` — Room database
- `retrofit2` / `okhttp3` — networking
- `coil` / `glide` — image loading
- `hilt` / `dagger` — dependency injection
- `com.google.accompanist` — Accompanist
- Any library NOT in the dependency list

### Step 4: Customize Resources

Edit the generated resource files:
- `colors.xml` — set app-specific Material 3 color palette
- `strings.xml` — set `app_name` and add UI strings
- `ic_launcher_foreground.xml` — customize vector icon for the app
- Keep all other resource files as generated

### Step 5: Update AndroidManifest.xml

Add permissions as needed:
- `INTERNET` — if the app uses networking
- `ACCESS_NETWORK_STATE` — if checking network status
- `WRITE_EXTERNAL_STORAGE` / `READ_EXTERNAL_STORAGE` — if accessing files
- Add `android:usesCleartextTraffic="true"` for HTTP

Add extra `<activity>` entries only if needed (rare — most Compose apps are single-activity).

### Step 6: Package and Deliver

Package the project into a ZIP:

```bash
cd {name} && zip -r ../output/{name}.zip . && cd ..
```

Upload via `upload_file` and present to the user with:
- App name and what it does
- List of screens/features
- How to import into CodeAssist (just open the ZIP)

## Validation Checklist

Before delivering, verify:

- [ ] `manifest.json` exists at ZIP root with correct `name` and `packageName`
- [ ] `deps/libraries.json` exists with all 5 dependency entries
- [ ] `project/.platform/workspace.json` exists with `buildSystem: "native"`
- [ ] `project/app/module.toml` exists with `compose = true` and correct namespace
- [ ] `project/app/src/main/AndroidManifest.xml` exists with correct package
- [ ] At least one `.kt` file exists in correct package directory
- [ ] All 9 resource files exist (2 drawable, 2 mipmap, 2 mipmap-anydpi-v26, 3 values)
- [ ] `proguard-rules.pro` exists
- [ ] NO Gradle files anywhere
- [ ] NO `.exmu-cfg1.data` files
- [ ] Code only uses available dependencies (no Room, Retrofit, Navigation, etc.)

## References

- **Dependencies & APIs**: See `references/dependencies.md`
- **Config templates**: See `references/config-templates.md`
