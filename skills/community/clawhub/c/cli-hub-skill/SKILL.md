---
name: cli-hub
description: >-
  Browse and install 102+ CLI tools for GUI software and popular platforms.
  Covers image editing, 3D, video, audio, office, diagrams, AI, communication, devops, and more.
---

# CLI-Anything Hub

Agent-native CLI interfaces for 102 applications — 80 harness CLIs (stateful, `--json`, REPL) plus 22 public/third-party CLIs (npm, uv, brew, and more).

## Quick Install

```bash
# First, install the CLI Hub package manager
pip install cli-hub-py

# Browse available CLIs
cli-hub list

# Install any CLI by name
cli-hub install gimp
cli-hub install blender
cli-hub install generate-veo-video

# Search by category or keyword
cli-hub search image
cli-hub search ai

# Launch an installed CLI
cli-hub launch <name> [args...]
```

## CLI Matrices

`cli-hub` also ships 5 curated cross-tool matrices: install one name to pull in a whole workflow kit and read its dedicated SKILL.md.

```bash
# Browse curated matrices
cli-hub matrix list

# Inspect one matrix
cli-hub matrix info video-creation

# Check which providers are available locally
cli-hub matrix preflight video-creation --json

# Install the whole matrix
cli-hub matrix install video-creation
```

## CLI-Anything Harness CLIs

Stateful, agent-native wrappers for 80 GUI applications. All support `--json` output, REPL mode, and undo/redo.

### 3D

| Name | Description | Install |
|------|-------------|---------|
| **ACloudViewer** | 3D point cloud and mesh processing via ACloudViewer binary CLI and JSON-RPC | `cli-hub install acloudviewer` |
| **Blender** | 3D modeling, animation, and rendering via blender --background --python | `cli-hub install blender` |
| **FreeCAD** | Parametric 3D CAD modeling via FreeCAD CLI (258 commands: Part, Sketcher, PartDesign, Assembly, Mesh, TechDraw, Draft, FEM, CAM, and more) | `cli-hub install freecad` |

### Ai

| Name | Description | Install |
|------|-------------|---------|
| **ComfyUI** | AI image generation workflow management via ComfyUI REST API | `cli-hub install comfyui` |
| **Dify Workflow** | CLI-Anything wrapper for the Dify workflow DSL editor covering create, inspect, validate, edit, export, and layout operations | `cli-hub install dify-workflow` |
| **Magnific** | Agent-native CLI harness for Magnific's remote MCP media-generation server — generate and upscale images and video via mcpc OAuth without loading the full MCP schema each turn | `cli-hub install magnific` |
| **MiniMax** | Chat and TTS via MiniMax AI API — MiniMax-M3 chat models and speech-2.8-hd TTS | `cli-hub install minimax` |
| **NotebookLM** | Experimental NotebookLM harness scaffold wrapping the installed notebooklm CLI for notebook, source, chat, artifact, download, and sharing workflows | `cli-hub install notebooklm` |
| **Novita** | Access AI models via Novita's OpenAI-compatible API (DeepSeek, GLM, MiniMax) | `cli-hub install novita` |
| **Ollama** | Local LLM inference and model management via Ollama REST API | `cli-hub install ollama` |
| **OpenWebUI** | Operate a running OpenWebUI backend through an agent-friendly CLI | `cli-hub install openwebui` |

### Audio

| Name | Description | Install |
|------|-------------|---------|
| **Audacity** | Audio editing and processing via sox | `cli-hub install audacity` |
| **WaveTone** | Prepare WaveTone 2.61 audio transcription manifests, probe audio files, and launch the real Windows WaveTone executable | `cli-hub install wavetone` |

### Automation

| Name | Description | Install |
|------|-------------|---------|
| **EEZ Studio** | EEZ Studio project, LVGL UI, and SCPI command automation via native .eez-project JSON and real EEZ Studio backend hooks | `cli-hub install eez-studio` |
| **MacroCLI** | Layered macro runtime that converts GUI workflows into parameterized, agent-callable macros — record once, run anywhere via CLI with backend routing across native APIs, file transforms, accessibility controls, and visual template matching | `cli-hub install macrocli` |
| **n8n** | Workflow automation via n8n REST API — 55+ commands | `cli-hub install n8n` |

### Communication

| Name | Description | Install |
|------|-------------|---------|
| **VE Twini** | Unified Twitter/X CLI bridging bird (GraphQL API) and opencli (browser automation) | `cli-hub install ve-twini` |
| **Zoom** | Meeting management via Zoom REST API (OAuth2) | `cli-hub install zoom` |

### Database

| Name | Description | Install |
|------|-------------|---------|
| **ChromaDB** | Vector database operations — collections, documents, semantic search via ChromaDB HTTP API | `cli-hub install chromadb` |
| **OpenRefine** | Agent-native CLI for OpenRefine import, operation-history cleaning, row inspection, export, and session undo/redo through the real local HTTP API. | `cli-hub install openrefine` |

### Debugging

| Name | Description | Install |
|------|-------------|---------|
| **LLDB** | Stateful native debugging via LLDB with JSON CLI workflows and a stdio Debug Adapter Protocol server | `cli-hub install lldb` |
| **Unreal Insights** | Windows-first Unreal trace capture, background session control, engine-matched UnrealInsights builds, and headless Timing Insights export workflows | `cli-hub install unrealinsights` |

### Design

| Name | Description | Install |
|------|-------------|---------|
| **Ink/Stitch** | Machine-embroidery digitization — set stitch params, validate, preview, and export to DST/PES/JEF/VP3 via Ink/Stitch | `cli-hub install inkstitch` |
| **Sketch** | Generate Sketch design files (.sketch) from JSON design specifications via sketch-constructor | `cli-hub install sketch` |

### Devops

| Name | Description | Install |
|------|-------------|---------|
| **CC Switch** | Manage AI coding tool configurations - inspect providers, skills, MCP servers, usage stats, and proxy settings | `cli-hub install cc-switch` |
| **ETH2 QuickStart** | Hardened Ethereum node deployment and operations via the eth2-quickstart automation scripts | `cli-hub install eth2-quickstart` |
| **iTerm2** | Control a running iTerm2 instance — manage windows, tabs, split panes, send text, read output, run tmux -CC, broadcast keystrokes, and configure preferences. | `cli-hub install iterm2` |
| **JumpServer** | Bastion host management — manage assets, users, permissions, sessions, accounts, and audit logs via JumpServer REST API | `cli-hub install jumpserver` |
| **NSLogger** | Capture, parse, filter, export, and mirror NSLogger iOS/macOS logs from the CLI | `cli-hub install nslogger` |
| **PM2** | Node.js process management — list, start, stop, restart, logs, and metrics via PM2 CLI | `cli-hub install pm2` |

### Diagrams

| Name | Description | Install |
|------|-------------|---------|
| **Draw.io** | Diagram creation and export via draw.io CLI | `cli-hub install drawio` |
| **Mermaid** | Mermaid Live Editor state files and renderer URLs | `cli-hub install mermaid` |

### Finance

| Name | Description | Install |
|------|-------------|---------|
| **Firefly III** | Personal finance management via the Firefly III REST API | `cli-hub install firefly-iii` |

### Game

| Name | Description | Install |
|------|-------------|---------|
| **Slay the Spire 2** | Control the real Slay the Spire 2 game via local STS2_Bridge HTTP API | `cli-hub install slay_the_spire_ii` |

### Gamedev

| Name | Description | Install |
|------|-------------|---------|
| **Godot Engine** | Game engine project management, scene editing, export and GDScript execution via Godot 4 headless mode | `cli-hub install godot` |
| **s&box** | Game engine project management for s&box (Source 2): scenes, prefabs, materials, sounds, codegen, asset graph, project validation | `cli-hub install sbox` |
| **UEAtelier** | Unreal Editor 5.6/5.7 MCP self-extension workbench - editor automation, build diagnostics, Task Atlas workflows, PIE smoke verification, scaffold pipeline | `cli-hub install ueatelier` |

### Generation

| Name | Description | Install |
|------|-------------|---------|
| **AnyGen** | Generate docs, slides, websites and more via AnyGen cloud API | `cli-hub install anygen` |

### Graphics

| Name | Description | Install |
|------|-------------|---------|
| **3MF** | Mesh geometry editor for 3D printing files — detect and resize cylindrical holes, repair meshes, compare 3MF files | `cli-hub install 3mf` |
| **CloudAnalyzer** | Point cloud and trajectory QA: Chamfer/AUC/F1, ATE/RPE/drift, ground segmentation metrics, config-driven quality gates, baseline evolution — harness wraps the CloudAnalyzer Python API | `cli-hub install cloudanalyzer` |
| **CloudCompare** | 3D point cloud and mesh processing: load/save, color ops, normal estimation, Delaunay meshing, noise filtering, ICP registration, connected component segmentation | `cli-hub install cloudcompare` |
| **Live2D Cubism** | Inspect, validate, edit, lint, diff, batch-manage, and deploy Live2D Cubism models (.model3.json, .moc3, .motion3.json, .exp3.json) from the command line — 42 commands covering the full model lifecycle | `cli-hub install live2d` |
| **MeerK40t** | Laser cutting/engraving job preparation via the real MeerK40t kernel — elements, operations, SVG/G-code export with --json output | `cli-hub install meerk40t` |
| **Nsight Graphics CLI** | Windows-first Nsight Graphics CLI for Graphics/OpenGL capture, GPU Trace summary, Generate C++ Capture, and ngfx-replay analysis | `cli-hub install nsight-graphics` |
| **RenderDoc** | GPU frame capture analysis: pipeline state, shader export, texture inspection, draw call browsing | `cli-hub install renderdoc` |

### Image

| Name | Description | Install |
|------|-------------|---------|
| **GIMP** | Raster image processing via gimp -i -b (batch mode) | `cli-hub install gimp` |
| **Inkscape** | SVG vector graphics with export via inkscape --export-filename | `cli-hub install inkscape` |
| **Krita** | Digital painting and raster image editing via Krita CLI export pipeline | `cli-hub install krita` |

### Knowledge

| Name | Description | Install |
|------|-------------|---------|
| **Joplin** | Note-taking and to-do automation — manage notebooks, notes, to-dos, tags, attachments, search, sync, and import/export via the Joplin terminal CLI | `cli-hub install joplin` |
| **Obsidian** | Knowledge management and note-taking — manage notes, search vault, execute commands via Obsidian Local REST API | `cli-hub install obsidian` |

### Knowledge-Management

| Name | Description | Install |
|------|-------------|---------|
| **SiYuan CLI** | Knowledge management and note-taking via SiYuan HTTP API — manage notebooks, documents, blocks, and search content from the command line | `cli-hub install siyuan` |

### Music

| Name | Description | Install |
|------|-------------|---------|
| **MuseScore** | CLI for music notation — transpose, export PDF/audio/MIDI, extract parts, manage instruments | `cli-hub install musescore` |

### Network

| Name | Description | Install |
|------|-------------|---------|
| **AdGuardHome** | DNS ad-blocking and network infrastructure management via AdGuardHome REST API | `cli-hub install adguardhome` |
| **Teltonika RMS** | Device management and monitoring via Teltonika RMS REST API | `cli-hub install rms` |

### Office

| Name | Description | Install |
|------|-------------|---------|
| **Calibre** | E-book library management — list, search, metadata editing, format conversion via calibredb, ebook-convert, ebook-meta | `cli-hub install calibre` |
| **LibreOffice** | Create and manipulate ODF documents, export to PDF/DOCX/XLSX/PPTX via headless mode | `cli-hub install libreoffice` |
| **Mubu** | Knowledge management and outlining via local Mubu desktop data | `cli-hub install mubu` |
| **Zotero** | CLI & MCP server for Zotero 7/8 — 52 MCP tools + 70+ CLI commands for search, import, PDF, BibTeX, notes, and more | `cli-hub install zotero` |

### Osint

| Name | Description | Install |
|------|-------------|---------|
| **Intelwatch** | Competitive intelligence, M&A due diligence, and OSINT directly from your terminal. | `cli-hub install intelwatch` |

### Project-Management

| Name | Description | Install |
|------|-------------|---------|
| **SeaClip** | Kanban board, 6-agent AI pipeline, and issue management via SeaClip-Lite FastAPI + SQLite | `cli-hub install seaclip` |

### Science

| Name | Description | Install |
|------|-------------|---------|
| **Stata** | Run Stata do-files, batch jobs, and reproducible econometric projects from the terminal with JSON output, log parsing, project scaffolding, and security guard | `cli-hub install stata` |
| **Uni-Mol Tools** | Molecular property prediction — train and predict with 5 task types (classification, regression, multiclass, multilabel) for drug discovery | `cli-hub install unimol_tools` |

### Scientific

| Name | Description | Install |
|------|-------------|---------|
| **QGIS** | Geospatial project authoring, layout export, and processing via PyQGIS and qgis_process | `cli-hub install qgis` |

### Search

| Name | Description | Install |
|------|-------------|---------|
| **Exa** | AI-powered web search and content extraction via the Exa API | `cli-hub install exa` |
| **Hacker Feeds CLI** | CLI for GitHub Trending, Hacker News, Reddit, Product Hunt, DEV.to, Lobsters, EchoJS, and V2EX feeds | `cli-hub install hacker-feeds-cli` |

### Storage

| Name | Description | Install |
|------|-------------|---------|
| **Tigris** | Object storage management — buckets, objects, presigned URLs, snapshots, IAM, scoped access keys. Wraps the official `tigris` CLI (S3-compatible, globally distributed, no egress fees) | `cli-hub install tigris` |

### Streaming

| Name | Description | Install |
|------|-------------|---------|
| **OBS Studio** | Create and manage streaming/recording scenes via command line | `cli-hub install obs-studio` |

### Testing

| Name | Description | Install |
|------|-------------|---------|
| **WireMock** | HTTP mock server management — create stubs, inspect requests, record traffic, and manage scenarios via WireMock REST API | `cli-hub install wiremock` |

### Video

| Name | Description | Install |
|------|-------------|---------|
| **Kdenlive** | Video editing and rendering via melt | `cli-hub install kdenlive` |
| **Openscreen** | Screen recording editor — zoom, speed ramps, trim, crop, annotations, backgrounds, and polished exports via ffmpeg | `cli-hub install openscreen` |
| **Palmier Pro** | Agent-native CLI harness for the Palmier Pro local MCP video editor — drive timeline editing, media, captions, and AI generation from the command line | `cli-hub install palmier` |
| **QuietShrink** | Compress macOS screen recordings on Apple Silicon — 70-90% smaller files at visually lossless quality, hardware-encoded, computer stays silent | `cli-hub install quietshrink` |
| **Shotcut** | Video editing and rendering via melt/ffmpeg | `cli-hub install shotcut` |
| **VideoCaptioner** | AI-powered video captioning — transcribe speech, optimize/translate subtitles, burn styled subtitles into video | `cli-hub install videocaptioner` |

### Web

| Name | Description | Install |
|------|-------------|---------|
| **Browser** | Browser automation via DOMShell MCP server. Maps Chrome's Accessibility Tree to a virtual filesystem for agent-native navigation. | `cli-hub install browser` |
| **clibrowser** | Zero-dependency CLI browser for AI agents with search, extraction, forms, RSS, crawling, auth, and WebMCP support | `cli-hub install clibrowser` |
| **Mailchimp** | Mailchimp Marketing API v3.0 — manage audiences, campaigns, reports, automations, ecommerce, templates, and more from an agent-native CLI | `cli-hub install mailchimp` |
| **Safari** | Native macOS Safari browser automation via safari-mcp — 84 tools for navigation, DOM, forms, network capture, and screenshots | `cli-hub install safari` |
| **TinyFish Web Agent** | All four TinyFish products from the terminal: web search, clean page extraction, natural-language browser automation, and remote CDP browser sessions — via the REST APIs. | `cli-hub install tinyfish` |
| **Web Yu-pri** | Japan Post Web Yu-pri browser workflow automation for login, inspection, screenshots, dry-run planning, and contents-form filling | `cli-hub install web-yu-pri` |

## Public & Third-Party CLIs

Official and community CLIs for popular platforms, managed via npm, uv, brew, and other installers. 22 CLIs available.

### Ai

| Name | Description | Entry Point | Install | Skill |
|------|-------------|-------------|---------|-------|
| **Generate Veo Video** | CLI for generating videos with Google Veo 3.1 via Vertex AI/Gemini — text-to-video, image-to-video, reference images, frame morphing, and video extension | `generate-veo` | `cli-hub install generate-veo-video` | https://github.com/charles-forsyth/generate-veo-video |
| **Jimeng / Dreamina CLI** | Official ByteDance AI image and video generation CLI — text-to-image, text-to-video, image-to-video, digital human, and intelligent canvas; domestic brand is Jimeng (即梦), international brand is Dreamina | `dreamina` | `cli-hub install jimeng` | https://bytedance.larkoffice.com/wiki/FVTwwm0bGiishxkKOoScdHR2nsg |
| **MiniMax CLI** | MiniMax AI platform CLI for managing tokens, models, and API interactions from the command line | `minimax-cli` | `cli-hub install minimax-cli` | https://platform.minimax.io/docs/token-plan/minimax-cli |

### Audio

| Name | Description | Entry Point | Install | Skill |
|------|-------------|-------------|---------|-------|
| **ElevenLabs CLI** | Official ElevenLabs CLI for managing voice agents as code with local configs, templates, auth, push/pull sync, tests, widgets, and branch-aware workflows | `elevenlabs` | `cli-hub install elevenlabs` | https://github.com/elevenlabs/cli |

### Communication

| Name | Description | Entry Point | Install | Skill |
|------|-------------|-------------|---------|-------|
| **Feishu/Lark CLI** | Official Lark (Feishu) CLI for managing Lark apps, bots, and cloud resources from the terminal | `lark-cli` | `cli-hub install feishu` | `npx skills add larksuite/cli -y -g` |
| **WeCom CLI** | Official WeCom open-platform CLI for contacts, todos, meetings, messages, calendars, docs, and smart sheets | `wecom-cli` | `cli-hub install wecom` | `npx skills add WeComTeam/wecom-cli -y -g` |

### Data-Science

| Name | Description | Entry Point | Install | Skill |
|------|-------------|-------------|---------|-------|
| **TraceCSR / Py4CSR CLI** | GxP-compliant agent harness for CDISC Clinical Study Report (CSR) and Tables/Figures/Listings (TFL) generation | `tracecsr` | `cli-hub install py4csr` | https://github.com/yanmingyu92/py4csr |

### Devops

| Name | Description | Entry Point | Install | Skill |
|------|-------------|-------------|---------|-------|
| **1Password CLI** | Official 1Password CLI for vault access, secrets retrieval, item automation, and desktop-app-backed authentication | `op` | `cli-hub install 1password-cli` | https://developer.1password.com/docs/cli/get-started/ |
| **DeployHQ CLI** | Deploy code, manage projects/servers, run and monitor deployments via the DeployHQ platform — for humans and AI agents | `dhq` | `cli-hub install deployhq` | https://github.com/deployhq/deployhq-cli/blob/main/skills/deployhq/SKILL.md |
| **Sentry CLI** | Official Sentry CLI for releases, sourcemaps, debug files, monitors, and org/project automation | `sentry-cli` | `cli-hub install sentry` | https://docs.sentry.io/cli/ |

### Devtools

| Name | Description | Entry Point | Install | Skill |
|------|-------------|-------------|---------|-------|
| **SmithUE CLI** | CLI tool for controlling Unreal Engine editor via SmithUE plugin. Enables AI agents to execute editor commands, list tools, search capabilities, and monitor editor status. | `smithue-cli` | `cli-hub install smithue-cli` | https://raw.githubusercontent.com/123dx-svg/smithue-cli/970f4b86b8b0671728585979b3c974829b4f47d0/skills/SKILL.md |

### Knowledge

| Name | Description | Entry Point | Install | Skill |
|------|-------------|-------------|---------|-------|
| **Obsidian CLI** | Official Obsidian command line interface for vault automation, developer tools, screenshots, search, history, and plugin workflows | `obsidian` | `cli-hub install obsidian-cli` | https://obsidian.md/help/cli |

### Mobile

| Name | Description | Entry Point | Install | Skill |
|------|-------------|-------------|---------|-------|
| **Android CLI** | Official Android terminal interface for SDK setup, project creation, emulator/device management, app run/deploy workflows, docs access, and skill management for any agent | `android` | `cli-hub install android-cli` | https://developer.android.com/tools/agents/android-skills |

### Music

| Name | Description | Entry Point | Install | Skill |
|------|-------------|-------------|---------|-------|
| **Suno CLI** | CLI for generating music with Suno AI from lyrics and style prompts, with batch generation, status polling, downloads, and automatic MP3 tagging | `suno` | `cli-hub install suno` | https://github.com/slauger/suno-cli/blob/main/docs/USAGE.md |

### Productivity

| Name | Description | Entry Point | Install | Skill |
|------|-------------|-------------|---------|-------|
| **Obsidian CLI** | Full-featured CLI for Obsidian — manage notes, canvases, Excalidraw diagrams, Kanban boards, periodic notes, git, tasks, and more. Includes an AI agent skill for persistent knowledge capture and project memory. | `obsidian-agent` | `cli-hub install obsidian-agent-cli` | https://github.com/ProxyLandLLC/obsidian-agent-cli/blob/v0.1.1/SKILL.md |
| **Pieces OS CLI** | Agent-native CLI for Pieces OS — persistent long-term memory for developers. Search, create, and manage memory assets, snippets, and models via Pieces OS REST API. | `cli-anything-pieces` | `cli-hub install pieces` | https://github.com/goddardoven110907/cli-anything-pieces/blob/master/README.md |

### Scientific

| Name | Description | Entry Point | Install | Skill |
|------|-------------|-------------|---------|-------|
| **ArcGIS Pro** | Agent-native CLI for ArcGIS Pro (ArcPy): professional cartography (layouts + map series), geoprocessing, and feature query/edit — plus a live-Pro MCP bridge that drives the open session. | `cli-anything-arcgis-pro` | `cli-hub install arcgis-pro` | https://github.com/Jasper0122/CLI-Anything-Arcgis-Pro/blob/v0.1.0/SKILL.md |

### Web

| Name | Description | Entry Point | Install | Skill |
|------|-------------|-------------|---------|-------|
| **Browser CDP** | Browser automation via raw Chrome DevTools Protocol — connects to YOUR existing Chrome, no extensions, no new browser, inherits all cookies and sessions | `cli-anything-browser-cdp` | `cli-hub install browser-cdp` | https://raw.githubusercontent.com/Uname58/cdp-agent-kit/master/contrib/cli-anything-harness/agent-harness/SKILL.md |
| **CloakBrowser CLI** | Agent-friendly CLI for CloakBrowser — stealth Chromium that passes every bot detection test. Covers fingerprint flags, humanize behaviors, page operations, content extraction, cookies, storage, network, multi-page sessions, and CDP gateway. | `cloak` | `cli-hub install cloakbrowser` | https://github.com/dreamor/cloakbrowser-cli/blob/main/SKILL.md |
| **Contentful CLI** | Official Contentful CLI for spaces, migrations, imports, exports, seeding, and environment management | `contentful` | `cli-hub install contentful` | https://github.com/contentful/contentful-cli/tree/main/docs |
| **Sanity CLI** | Official Sanity CLI for studios, datasets, schemas, imports, exports, and structured content workflows | `sanity` | `cli-hub install sanity` | https://www.sanity.io/docs/apis-and-sdks/cli |
| **Shopify CLI** | Official Shopify CLI for apps, themes, functions, extensions, and Hydrogen storefront workflows | `shopify` | `cli-hub install shopify` | https://github.com/Shopify/cli/blob/main/packages/cli/README.md#commands |

## Curated Matrices

Each matrix is a curated multi-CLI workflow pulled from the CLI Matrix. Installing a matrix installs all member CLIs and points you at a matrix-specific SKILL.md.

| Matrix | Description | CLIs | Install | Skill |
|--------|-------------|------|---------|-------|
| **3D & CAD** | Capability-based matrix for 3D modeling, parametric CAD, sculpting, point clouds, photogrammetry, PBR texturing, preview/offline rendering, GPU frame debugging, fabrication (slicing and CAM), and game-engine export. Mostly offline-capable; providers include harness CLIs, Python libs, native binaries, and cloud APIs. | 6 | `cli-hub matrix install 3d-cad` | `cli-hub-matrix/3d-cad/SKILL.md` |
| **Game Development** | Capability-based matrix for game development: engine authoring (Godot-first), 3D/2D/audio/notation assets, AI-generated assets, agent-driven playtesting, build packaging, store publishing, and telemetry/crash reporting. Providers include harness CLIs, public CLIs, Python libs, native binaries, and cloud APIs. | 9 | `cli-hub matrix install game-development` | `cli-hub-matrix/game-development/SKILL.md` |
| **Image & Graphic Design** | Capability-based matrix for image and graphic design: AI image generation, raster/vector editing, UI mockups/wireframes, diagrams, super-resolution upscaling, photo library management, RAW development, and CMS publishing. GIMP/Krita/Inkscape/ComfyUI cover most work offline; cloud APIs escalate quality. | 7 | `cli-hub matrix install image-design` | `cli-hub-matrix/image-design/SKILL.md` |
| **Knowledge / Office / Research** | Capability-based matrix for research, note-taking, document authoring, and publishing: web/literature search, article retrieval, citations/references, notes/PKM, outlining, multi-doc synthesis, office document authoring (DOCX/XLSX/PPTX/PDF), format conversion, PDF manipulation, diagrams, web publishing, and LaTeX builds. Providers include harness CLIs, public CLIs, Python libs, native binaries, and cloud APIs. | 13 | `cli-hub matrix install knowledge-research` | `cli-hub-matrix/knowledge-research/SKILL.md` |
| **Video Creation & Editing** | Capability-based matrix for end-to-end video production: storyboard planning, story/audio direction, internet video/music search/download with source triage, capture, generation, voice/music, sound design, footage analysis, transcription, high-end caption design, assembly, overlay, thumbnail, encode, and quality review with render-doctor investigation. Providers include harness CLIs, public CLIs, Python libs, native binaries, bundled scripts, agent skills, and cloud APIs. | 14 | `cli-hub matrix install video-creation` | `cli-hub-matrix/video-creation/SKILL.md` |

## How It Works

`cli-hub` is a unified package manager for both harness CLIs and public CLIs:

- **Harness CLIs**: installed via `pip` as `cli-anything-<name>` packages
- **npm CLIs**: installed via `npm install -g`
- **uv CLIs**: installed via `uv tool install`
- **brew/script CLIs**: installed via the tool's native installer
- **bundled CLIs**: detected from PATH (pre-installed with the host app)
- **Matrices**: install a curated set of harness and public CLIs in one command

## Harness CLI Usage Pattern

All harness CLIs follow the same pattern:

```bash
# Interactive REPL
cli-anything-<name>

# One-shot command
cli-anything-<name> <group> <command> [options]

# JSON output for agents
cli-anything-<name> --json <group> <command>
```

## For AI Agents

1. Install the hub: `pip install cli-hub-py`
2. Install the CLI you need: `cli-hub install <name>`
3. Run the CLI directly via its entry point, or use `cli-hub launch <name> [args...]`
4. For harness CLIs: use `--json` flag for machine-readable output; check exit codes (0=success)
5. Read each harness CLI's full SKILL.md at the repo path shown in registry.json

## More Info

- Repository: https://github.com/Asher-1/CLI-Anything
- Web Hub: https://asher-1.github.io/CLI-Anything
- Last Updated: 2026-06-19
