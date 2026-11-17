---
name: bearware-teamtalk
description: "Complete knowledge base for BearWare.dk's TeamTalk 5 Conferencing System. Use when working with TeamTalk audio/video conferencing, the TeamTalk 5 SDK (C-API, .NET, Java, Python, Rust), TeamTalk server administration, TeamTalk client development, building TeamTalk from source, or any TeamTalk-related task including cloning, building, detecting installed SDK, API usage, and configuring servers."
---

# BearWare.dk / TeamTalk 5 Skill

## Overview

BearWare.dk is a Danish software company (founded 2005 by Bjørn D. Rasmussen) that develops the TeamTalk 5 Conferencing System - a self-hosted audio/video conferencing platform with a standalone server, multiple clients, and a full SDK. The entire source code is open on GitHub.

## Quick Actions

### Check if SDK is installed

Run `scripts/check_sdk.py` to detect TeamTalk SDK on the current system. It checks common install paths and reports the version if found.

### Build from Source

Run `scripts/build_from_source.sh` to clone, build, and set up the TeamTalk 5 SDK from GitHub source. Supports Linux, macOS, and cross-compilation for Android/iOS/Raspberry Pi.

### Detect Platform

Run `scripts/check_sdk.py --detect-only` to print the current platform string.

## Building TeamTalk 5 from Source

The full source is at `https://github.com/BearWare/TeamTalk5`. Build using CMake or the provided Makefile.

### Prerequisites

- CMake 3.10+
- C++17 compiler (GCC 9+, Clang 10+, MSVC 2019+)
- Qt 5.15+ (for the client GUI)
- OpenSSL (for encryption support)
- ALSA / PulseAudio development headers (Linux)

### Build with Makefile (Linux/macOS)

The Build directory contains a Makefile for common targets:

```bash
git clone https://github.com/BearWare/TeamTalk5.git
cd TeamTalk5

# Install dependencies then build
sudo make -C Build depend-ubuntu24
make -C Build ubuntu24

# macOS
brew install qt openssl
make -C Build depend-mac
make -C Build mac

# Build all Android targets
make -C Build android-all

# Build for Raspberry Pi OS
make -C Build raspios12
```

### Build with Docker

```bash
git clone https://github.com/BearWare/TeamTalk5.git
cd TeamTalk5

docker compose run --rm ubuntu24 make -C /TeamTalk5/Build ubuntu24
docker compose run --rm android make -C /TeamTalk5/Build android-all
```

### Build with CMake (Advanced)

```bash
git clone https://github.com/BearWare/TeamTalk5.git
cd TeamTalk5/Library/TeamTalkLib
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
```

### Build Individual Components

| Component | Directory | Dependency |
|---|---|---|
| C-API DLL | `Library/TeamTalk_DLL` | TeamTalkLib |
| .NET Wrapper | `Library/TeamTalk.NET` | TeamTalk_DLL |
| Java JNI | `Library/TeamTalkJNI` | TeamTalk_DLL |
| Python Bindings | `Library/TeamTalkPy` | TeamTalk_DLL |
| Rust Bindings | `Library/teamtalk_rust` | TeamTalk_DLL |
| Qt Client | `Client/qtTeamTalk` | TeamTalk_DLL |
| MFC Client | `Client/TeamTalkClassic` | TeamTalk_DLL |
| .NET Client | `Client/TeamTalkApp.NET` | TeamTalk.NET |
| iOS Client | `Client/iTeamTalk` | TeamTalk_DLL |
| Android Client | `Client/TeamTalkAndroid` | TeamTalkJNI |
| C++ Server | `Server/TeamTalkServer` | TeamTalk_DLL (Pro) |
| .NET Server | `Server/TeamTalkServer.NET` | TeamTalk.NET (Pro) |
| Java Server | `Server/jTeamTalkServer` | TeamTalkJNI (Pro) |
| PHP Admin | `Client/ttphpadmin` | PHP CLI |

## SDK Structure (after build)

```
TeamTalk5/
├── Library/
│   ├── TeamTalkLib/         # Core library source
│   ├── TeamTalk_DLL/        # C-API DLL project
│   │   ├── TeamTalk5.h      # C-API header (main API)
│   │   └── TeamTalk5.def    # DLL exports
│   ├── TeamTalk.NET/        # .NET wrapper source
│   ├── TeamTalkJNI/         # Java JNI wrapper source
│   ├── TeamTalkPy/          # Python bindings
│   └── teamtalk_rust/       # Rust bindings
├── Client/
│   ├── qtTeamTalk/          # Qt-based client
│   ├── TeamTalkClassic/     # Accessible MFC client
│   ├── TeamTalkApp.NET/     # C# .NET client
│   ├── iTeamTalk/           # iOS Swift client
│   ├── TeamTalkAndroid/     # Android Java client
│   └── ttphpadmin/          # PHP admin script
├── Server/
│   ├── TeamTalkServer/      # C++ server example
│   ├── TeamTalkServer.NET/  # C# server example
│   └── jTeamTalkServer/     # Java server example
├── Build/
│   ├── Makefile             # Unified build targets
│   └── Docker/              # Docker build environments
└── Setup/                   # Installer scripts
```

## TeamTalk 5 SDK Editions

| Feature | Standard | Professional |
|---|---|---|
| Client DLL API | Yes | Yes |
| Encryption (TLS/AES) | Optional | Yes |
| Standalone server | Yes (unencrypted) | Yes (encrypted) |
| Server DLL API | No | Yes |

The source builds both editions. Professional features are enabled at compile time.

## TeamTalk 5 Pro Server

Encrypted TeamTalk server with Web-Login authentication. Built from source with Professional Edition flags.

Features:
- TLS/AES encrypted connections
- BearWare.dk Web-Login authentication
- SpamBot (auto-kick foul language, block VPN/proxies)
- Available for Ubuntu 22/24, Windows, Raspbian 12

## Supported Platforms

- **Windows**: 10/11, 32-bit and 64-bit
- **macOS**: 10.13+, 64-bit
- **Linux**: Ubuntu 22/24, x86_64 (Debian 9+ variants)
- **Android**: v5.0+ (ARMv7, ARM64, x86, x86_64)
- **iOS**: v7.0+ (Universal)
- **Raspberry Pi**: Raspbian 12, arm64

## SDK API Reference

See `references/api_reference.md` for the complete SDK API overview including all structs, enums, events, and methods.

See `references/changelog.md` for the full change history from v5.0a to v5.22a.

### Language Bindings

All bindings wrap the same C-API DLL:

- **C-API**: `TeamTalk5.h` - the native interface
- **.NET**: `TeamTalk.NET` - C# wrapper
- **Java**: `TeamTalkJNI` - Java JNI wrapper
- **Python**: `TeamTalkPy` - Python bindings
- **Rust**: `teamtalk_rust` - bindgen-generated Rust bindings

## Key SDK Concepts

### Client Workflow

1. Create instance: `TT_InitTeamTalk()` or `TT_InitTeamTalkEx()`
2. Set sound devices: `TT_InitSoundDevices()` or `TT_InitSoundDuplexDevices()`
3. Connect: `TT_Connect()` with IP, TCP port, UDP port
4. Login: `TT_DoLogin()` with username, password
5. Join/create channel: `TT_DoJoinChannel()` / `TT_DoMakeChannel()`
6. Transmit audio/video: `TT_EnableVoiceTransmission()` / `TT_StartVideoCaptureTransmission()`
7. Cleanup: `TT_CloseTeamTalk()` and `TT_DeleteInstance()`

### Server Workflow

1. Create instance: `TTS_InitTeamTalkServer()` or `TTS_InitTeamTalkServerEx()`
2. Load config: `TTS_LoadConfiguration()` from `tt5srv.xml`
3. Run: `TTS_RunServer()` (blocking)
4. Handle callbacks from registered events
5. Shutdown: `TTS_CloseServer()`

### Key Data Structures

- **`TTInstance`** - opaque handle to a client instance
- **`Channel`** - channel properties (name, password, topic, codec, disk quota, etc.)
- **`User`** - user properties (ID, username, IP, status, etc.)
- **`UserAccount`** - server-side user account (username, password, user type, user rights, etc.)
- **`TextMessage`** - text message (from user, to user/channel, content, etc.)
- **`AudioCodec`** / **`VideoCodec`** - codec configuration for audio/video streams
- **`SoundDevice`** - sound device properties
- **`ServerProperties`** - server config (max users, motd, etc.)

### Audio Codecs

- **OPUS** - primary VoIP codec
- **Speex** - legacy codec
- **AudioFileFormat** - WAV, MP3, OGG (OPUS), WMA

### Video Codecs

- **WebM** (VP8) - primary video codec, supports VBR and CBR
- Capture via DirectShow (Windows), AVFoundation (macOS), V4L2 (Linux)

### Stream Types

- `STREAMTYPE_VOICE` - microphone audio
- `STREAMTYPE_VIDEOCAPTURE` - webcam video
- `STREAMTYPE_DESKTOP` - desktop sharing
- `STREAMTYPE_MEDIAFILE_AUDIO` - streamed audio files
- `STREAMTYPE_MEDIAFILE_VIDEO` - streamed video files
- `STREAMTYPE_CHANNELMSG` - channel text messages
- `STREAMTYPE_LOCALMEDIAPLAYBACK_AUDIO` - local media playback

### Channel Types

- `CHANNEL_DEFAULT` - normal channel
- `CHANNEL_CLASSROOM` - teacher controls who transmits
- `CHANNEL_SOLO_TRANSMIT` - only one user transmits at a time
- `CHANNEL_FREEFORALL` - override classroom restrictions
- `CHANNEL_HIDDEN` - invisible without `USERRIGHT_VIEW_HIDDEN_CHANNELS`

### User Rights

- `USERRIGHT_DEFAULT` - basic access
- `USERRIGHT_VIEW_HIDDEN_CHANNELS` - see hidden channels
- `USERRIGHT_TEXTMESSAGE_USER` - send private messages
- `USERRIGHT_TEXTMESSAGE_CHANNEL` - send channel messages
- `USERRIGHT_MODIFY_CHANNELS` - create/rename permanent channels
- `USERRIGHT_MULTI_LOGIN` - allow multiple logins from same account

### Encryption

- TLS for control channel, AES-256 for media streams
- Configure via `EncryptionContext` struct
- Peer verification supported (client and server)

## Public Test Servers

- `tt://tt5us.bearware.dk?tcpport=10335&udpport=10335&username=bearware&channel=/` (unencrypted)
- `tt://tt5us.bearware.dk?tcpport=10443&udpport=10443&username=bearware&channel=/&encrypted=1` (encrypted)

Press F2 in the TeamTalk client for more public servers.

## GitHub

- Repository: `https://github.com/BearWare/TeamTalk5`
- 377 stars, 184 forks
- 49 releases (latest: v5.22, April 2026)
- Languages: C++ (61%), Java (13%), C# (11%), C (6%), Swift (3%), CMake (3%)
- 8,635 commits
- Topics: voip, video-streaming, conferencing, desktop-sharing

## License

The TeamTalk 5 SDK source code is on GitHub under the TeamTalk 5 SDK License Agreement: `https://github.com/BearWare/TeamTalk5/blob/master/LICENSE.txt`

## Consulting & Custom Development

BearWare.dk offers consulting for custom TeamTalk integrations. Email `contact@bearware.dk`. Customers span: entertainment, defense, radio communications, medical, education, space agencies, emergency services.

## News

- **April 6, 2026**: TeamTalk v5.22 released
- **November 13, 2025**: TeamTalk Pro Server v5.21.1 released
- **September 29, 2025**: TeamTalk v5.21 released
