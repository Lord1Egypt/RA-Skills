---
name: game-dev-setup-engine
description: >
  Engine configuration wizard for Godot 4.6, Unity 7, and UE 5.6. Handles
  project creation, version control, renderer settings, and platform-specific
  setup with version-aware references.
triggers:
  - "set up my engine"
  - "configure Unity project"
  - "setup Godot"
  - "Unreal project setup"
  - "initialize project"
  - "engine configuration"
---

# Game Dev Setup Engine — Engine Configuration Wizard

## 🎯 Purpose

Guide users through configuring a game engine project from scratch. Handles
Godot 4.6, Unity 7, and Unreal Engine 5.6 with version-aware settings,
renderer selection, and platform target configuration.

## 🤖 Multi-Platform Notes

| Platform | Notes |
|----------|-------|
| **OpenClaw** | Can read/write engine config files directly. Best for generating correct file content and writing it to the right location. |
| **Claude Code** | Can run engine CLI commands (`godot --headless`, `Unity -projectPath`, etc.) and edit config files. Run detection commands to verify installs. |
| **Cursor/Windsurf** | Good for editing config files in the project. May have LSP support for GDScript/C#. |
| **GitHub Copilot** | Can suggest config file content. Let the user paste or review. |
| **Generic LLM Chat** | Output config file content as code blocks. User must paste into correct locations. |
| **Any AI** | Can guide through manual setup steps. Always state: "I can tell you the steps OR write the files for you — which do you prefer?" |

---

## 🔍 Phase 1: Engine Detection

### Step 1.1 — Ask

> **"Which engine are you using?"**
>
> ```
> 1) Godot 4.6
> 2) Unity 7
> 3) Unreal Engine 5.6
> 4) Other (specify)
> ```

### Step 1.2 — Check Installed Version

If on a terminal-capable platform, run:

**Godot:**
```bash
godot --version
# Expected: 4.6.stable or similar
```

**Unity:**
```bash
# Check Unity Hub for installed versions, or:
find /Applications/Unity -name "Unity" -type f 2>/dev/null
# Windows:
where Unity 2>/dev/null
```

**Unreal:**
```bash
# Check Engine association (Windows)
# Look in: C:\Program Files\Epic Games\UE_5.6\
```

### Step 1.3 — Version-Aware Config Reference

| Setting | Godot 4.6 | Unity 7 | UE 5.6 |
|---------|-----------|---------|--------|
| **Renderer** | Forward+ (3D), Compatibility (low-end) | URP (default), HDRP (high-end) | Deferred (default), Forward (VR) |
| **Script** | GDScript, C# (.NET 8) | C# (.NET 8) | C++, Blueprints |
| **Build Target** | Windows, Mac, Linux, Web, Android, iOS | Windows, Mac, Linux, Web, Android, iOS, Consoles | Windows, Mac, Linux, Android, iOS, Consoles |
| **Version Control** | Git (`.gitignore` provided) | Unity Version Control or Git | Perforce (recommended) or Git |
| **Plugin/Market** | Asset Library | Asset Store | Fab / Marketplace |

---

## ⚙️ Phase 2: Project Initialization

### Godot 4.6

Create `project.godot`:

```gdscript
[application]
config/name="My Game"
config/description="A game made with Godot 4.6"
config/icon="res://icon.png"
run/main_scene="res://scenes/main.tscn"

[rendering]
renderer/rendering_method="forward_plus"  # or "mobile" or "compatibility"
renderer/anti_aliasing/quality="high"     # or "medium", "low", "disabled"
```

Then ask:
> **"Create the standard folder structure?"**

```
res://
├── assets/        # Raw assets (sprites, models, audio)
│   ├── art/
│   ├── audio/
│   └── fonts/
├── scenes/        # .tscn files
├── scripts/       # .gd / .cs files
├── resources/     # .tres / .res files
├── addons/        # Plugins
├── levels/        # Level scenes
└── tests/         # Unit tests (GDScript 2.0 unit test)
```

**Render pipeline:** Forward+ default. Switch to Compatibility for 2D-only.
Switch to Mobile for mobile targets.

### Unity 7

Create project with Unity Hub, then set up:

```
Assets/
├── _Project/
│   ├── Scripts/
│   ├── Scenes/
│   ├── Prefabs/
│   ├── Art/
│   ├── Audio/
│   ├── Resources/
│   └── Settings/
├── ThirdParty/
└── Plugins/
```

**Render Pipeline Selection:**
- **URP** (Universal Render Pipeline) — default for most projects. Good for
  mobile, cross-platform, 2D, and mid-range 3D.
- **HDRP** (High Definition RP) — high-end PC/console 3D only.
- **Built-in RP** — legacy. Only use for existing projects.

> Ask: *"URP or HDRP? If you're not sure, pick URP."*

**Input System:**
- New Input System Package (recommended for all new projects)
- Legacy Input Manager (existing projects)

**Version Control:**
- Generate `.gitignore` for Unity
- Default meta file tracking
- Ask about Unity Version Control if on a team

### Unreal Engine 5.6

Create via Epic Games Launcher or manually:

```
Project/
├── Content/
│   ├── Characters/
│   ├── Environments/
│   ├── UI/
│   ├── Audio/
│   └── Blueprints/
├── Source/
│   └── [ProjectName]/
│       ├── [ProjectName].h
│       ├── [ProjectName].cpp
│       └── [ProjectName].Build.cs
├── Config/
└── [ProjectName].uproject
```

**Render Pipeline:** Deferred Renderer (default).
Switch to Forward for VR or high-framerate targets.

**Startup settings:**
- Ask: *"Blueprint-only or C++ ?"*
- Ask: *"Template? (Blank, Third Person, Top Down, etc.)"*

---

## 🔧 Phase 3: Platform Configuration

### Step 3.1 — Target Platforms

Ask:
> **"Which platforms will you target?"**
>
> ```
> 1) Windows/Mac/Linux (desktop)
> 2) Web (HTML5/WebGL)
> 3) Mobile (Android/iOS)
> 4) Console (requires approval)
> 5) All of the above
> ```

### Step 3.2 — Platform-Specific Settings

| Engine | Windows | Mac/Linux | Web | Mobile |
|--------|---------|-----------|-----|--------|
| Godot | Default | Default | `texture/force_keep_filtered` off, audio → `use_mobile_for_hq` | `rendering/texture/vram_compression` on |
| Unity | IL2CPP, DX11/12 | Mono, Metal | WebGL 2.0 | IL2CPP, Vulkan (Android), Metal (iOS) |
| UE | DX12/11 | Vulkan/Metal | N/A | Vulkan |

### Step 3.3 — Version Control Setup

Generate `.gitignore` based on engine:

- **Godot:** https://github.com/github/gitignore/blob/main/Godot.gitignore
- **Unity:** https://github.com/github/gitignore/blob/main/Unity.gitignore
- **UE:** https://github.com/github/gitignore/blob/main/UnrealEngine.gitignore

> Ask: *"Initialize a git repo and create .gitignore?"*

---

## ✅ Phase 4: Verification

### Step 4.1 — Build Test

Ask:
> **"Should I try to build an empty project to verify the setup?"**

If terminal-capable:

**Godot:**
```bash
godot --headless --build-solutions --quit
```

**Unity:**
```bash
# Requires Unity CLI path setup
Unity -projectPath . -buildTarget StandaloneWindows64 -quit -batchmode -logFile build.log
```

**UE:**
```bash
# Generate project files
# Windows:
"[Epic Games]\UE_5.6\Engine\Build\BatchFiles\Build.bat" [ProjectName]Editor Win64 Development -project="[full path]"
```

### Step 4.2 — Basic Scene

Create a default scene with:
- A camera
- A light (for 3D)
- A test object (cube or sprite)
- Attach a script that prints "Hello, World!"

> Ask: *"Want me to create a test scene to verify everything works?"*

---

## 📋 Setup Summary

After completing, output a setup summary:

```markdown
# Engine Setup Complete

## Project
- **Project:** [project name]
- **Engine:** [engine + version]
- **Location:** [path]
- **Renderer:** [renderer name]

## Configuration
- [ ] Folder structure created
- [ ] Version control initialized
- [ ] Platform targets set: [list]
- [ ] Test scene created and verified

## Next Steps
- Run `game-design-doc` to write the GDD
- Run `architecture` for system design
- Run `sprint-dev` to start development
```

## 🚨 Troubleshooting

### Godot
- GDScript not highlighting? Install Godot extension for your editor.
- .NET not detected? Install .NET 8 SDK.
- Export templates missing? Install via Godot → Editor → Manage Export Templates.

### Unity
- Package errors? Re-import from Package Manager → My Assets.
- Scripts not compiling? Check .NET profile and API compatibility level.
- "No Unity version associated" — open with Unity Hub.

### Unreal
- Visual Studio not detected? Install Game Development with C++ workload.
- Shader compilation errors? Update GPU drivers.
- Slow startup? This is normal for first launch.
