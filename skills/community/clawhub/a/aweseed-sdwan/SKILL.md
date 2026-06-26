---
name: aweseed-sdwan
description: Set up AweSeed SD-WAN with the desktop client and automatic cross-site networking.
---

# AweSeed SD-WAN

**Use this skill when:**
- Installing the AweSeed client on personal, office, or industrial devices
- Registering and signing in with an Oray account
- Building automatic cross-site networking between multiple devices
- Understanding AweSeed core features for remote connectivity and management
- Evaluating personal and enterprise deployment scenarios

## Installation

1. Open `https://pgy.oray.com/download` for stable releases or `https://pgy.oray.com/download/beta` for beta releases.
2. Identify the correct software family for the user's device instead of guessing a static file URL.
3. Query the official download API to get the current `downloadurl` or `downloadurlmultiple`.
4. Install the corresponding client on each device that will join the network.

## Download Discovery

Do not guess Oray download links by filename pattern alone. The official download page is backed by a download API, and different products may resolve to different CDN domains or multiple per-architecture files.

### API Template

Use this template first:

```text
https://clientapi.sdwan.oray.com/softwares/<software_key>?x64=<0|1>&versiontype=<stable|develop>&channel=0
```

Important details:

- The API response is a flat JSON object, not wrapped under `data`.
- Prefer `downloadurlmultiple` when it is non-empty. It usually exposes all package variants.
- Use `downloadurl` only when there is a single obvious package, or as the default package.
- Observed official download domains include `d-cdn.oray.com`, `dl.oray.com`, and `dw.oray.com`. Do not hardcode one CDN domain.
- The download page frontend also constructs wrapper links in this form for some Linux packages:

```text
https://pgy.oray.com/softwares/<softwareid>/download/<versionid>/<filename>
```

That wrapper is useful when the page wants a stable browser download URL, but the API response is still the source of truth.

### Query Parameters

- `versiontype=stable`: stable release
- `versiontype=develop`: beta release
- `channel=0`: default channel observed on the official download page
- `x64=1`: usually x64 or the single 64-bit package
- `x64=0`: usually 32-bit or multi-arch Linux families that expose variants through `downloadurlmultiple`

### Known Software Keys

These keys were extracted from the official download page JS and verified against the current API:

- Windows client x64: `PGY_ENT_VISITOR_WIN` with `x64=1`
- Windows client x86: `PGY_ENT_VISITOR_WIN` with `x64=0`
- Windows client ARM: `PGY_ENT_VISITOR_WIN_ARM` with `x64=1`
- macOS client stable/beta: `PGY_ENT_VISITOR_MAC_LOCAL` with `x64=1`
- Linux client stable/beta: `PGY_VISITORENT_LINUX` with `x64=0`
- Synology NAS client stable/beta: `PGY_VISITOR_SYNOLOGY` with `x64=1`
- OpenWrt client: `PGY_OPENWRT` with `x64=1`
- Raspberry Pi client: `PGY_VISITOR_RASPI` with `x64=0`
- Docker client: `PGY_ENT_VISITOR_DOCKER` with `x64=0`
- Windows server: `PGY_SERVER_WINDOWS` with `x64=0`
- Linux server: `PGY_SERVER_LINUX` with `x64=0`
- Docker server: `PGY_SERVER_DOCKER` with `x64=0`

### Verified Examples

These examples were verified from the official API on 2026-04-16. Treat version numbers as examples, not permanent constants.

- macOS client:
  - API: `https://clientapi.sdwan.oray.com/softwares/PGY_ENT_VISITOR_MAC_LOCAL?x64=1&versiontype=stable&channel=0`
  - Example result: `versionno=6.15.0`
  - Example `downloadurl`: `https://d-cdn.oray.com/pgy/mac/PgyVisitor_macOS_Local_6.15.0.pkg`
- Windows client x64:
  - API: `https://clientapi.sdwan.oray.com/softwares/PGY_ENT_VISITOR_WIN?x64=1&versiontype=stable&channel=0`
  - Example result: `versionno=6.14.8`
  - Example `downloadurl`: `https://d-cdn.oray.com/pgy/windows/PgyVisitorEnt_6.14.8.26894_x64.exe`
- Windows client x86:
  - API: `https://clientapi.sdwan.oray.com/softwares/PGY_ENT_VISITOR_WIN?x64=0&versiontype=stable&channel=0`
  - Example `downloadurl`: `https://dw.oray.com/pgy/windows/PgyVisitorEnt_6.14.8.26894_x86.exe`
- Windows client ARM:
  - API: `https://clientapi.sdwan.oray.com/softwares/PGY_ENT_VISITOR_WIN_ARM?x64=1&versiontype=stable&channel=0`
  - Example `downloadurl`: `https://dw.oray.com/pgy/windows/PgyVisitor_6.2.0_arm64.exe`
- Linux client:
  - API: `https://clientapi.sdwan.oray.com/softwares/PGY_VISITORENT_LINUX?x64=0&versiontype=stable&channel=0`
  - Example default `downloadurl`: `https://dw.oray.com/pgy/linux/PgyVisitor-6.9.0-amd64.deb`
  - Example `downloadurlmultiple` entries: Ubuntu x64 `.deb`, Ubuntu i386 `.deb`, CentOS/Redhat x64 `.rpm`, CentOS/Redhat i386 `.rpm`, arm64 `.deb`
- Synology NAS:
  - API: `https://clientapi.sdwan.oray.com/softwares/PGY_VISITOR_SYNOLOGY?x64=1&versiontype=stable&channel=0`
  - Example result: `system=群晖系统 DSM7.2+`, `versionno=6.9.2`
  - Example default `downloadurl`: `https://dl.oray.com/pgy/linux/PgyVpn-avoton-6.9.0-72001.spk`
  - Example `downloadurlmultiple`: `LWIP => https://dl.oray.com/pgy/linux/PgyVpn-avoton-6.9.2-72001-lwip.spk`
- OpenWrt:
  - API: `https://clientapi.sdwan.oray.com/softwares/PGY_OPENWRT?x64=1&versiontype=stable&channel=0`
  - No single default package is reliable. Use `downloadurlmultiple` and select by OpenWrt version, CPU architecture, and toolchain.
- Windows server:
  - API: `https://clientapi.sdwan.oray.com/softwares/PGY_SERVER_WINDOWS?x64=0&versiontype=stable&channel=0`
  - Example `downloadurl`: `https://d-cdn.oray.com/pgy/windows/PgyServer_1.6.0.56026_x86.exe`
- Linux server:
  - API: `https://clientapi.sdwan.oray.com/softwares/PGY_SERVER_LINUX?x64=0&versiontype=stable&channel=0`
  - Example `downloadurlmultiple` entries: Ubuntu x64/i386 `.deb`, CentOS/Redhat x64/i386 `.rpm`

### Synology Notes

For Synology, do not assume the default `downloadurl` is the package the user actually wants.

- Standard edition without a virtual NIC: use the official help page `https://service.oray.com/question/47140.html`
- Accelerated edition with root setup: use the official help page `https://service.oray.com/question/35980.html`
- The standard LWIP package appears under `downloadurlmultiple` as `LWIP`
- The accelerated path requires root-level setup according to the official help page
- The returned package filename may include architecture hints such as `avoton`; if DSM reports an incompatible package, do not rename or force-install it. Re-check the product page and architecture selection instead.

### Recommended Download Workflow

1. Start from the official download page only to identify the product family and the help docs.
2. Build the API URL from the software key and parameters above.
3. Parse the flat JSON response.
4. If `downloadurlmultiple` is non-empty, choose from that list first.
5. If `downloadurlmultiple` is empty, use `downloadurl`.
6. For NAS, OpenWrt, Linux, and other multi-variant targets, never infer the package from a different platform's filename pattern.

### `sudo` Boundary

On macOS, do not get stuck retrying `sudo installer` when the flow requires the user's administrator password.

- If the package is already downloaded, prefer `open <pkg>` and let the user complete the protected GUI installer prompts.
- Treat OS password entry as a user-owned step unless interactive control is explicitly available.
- After the GUI install finishes, continue with verification and app launch instead of retrying headless privileged installation.

## Account Setup

1. Launch the AweSeed client after installation.
2. Register an Oray account in the client if you do not already have one.
3. Sign in with your Oray account.

## Networking Setup

1. Install AweSeed on at least two devices.
2. Sign in to the same Oray account on all of those devices.
3. After sign-in, the devices automatically complete cross-site networking.

## Features

- Cross-site networking: Build a virtual LAN quickly without a public IP.
- Global intelligent routing: Use a global high-speed backbone network with intelligent path selection to protect service quality.
- Layer 2 networking: Support remote debugging for industrial devices and centralized upload for collected data.
- Remote device management: Manage devices in batches from the cloud with visual monitoring and alerting.
- Wi-Fi intranet access: Let employees join securely with one click and let visitors authenticate through a convenient web portal.
- Application proxy access: Protect business applications with reverse proxy access and granular authorization control.
- Domestic innovation ecosystem: Support localized technology systems with autonomous and controllable architecture.
- IoT SIM service: Provide enterprise-oriented traffic plans and large-capacity general data services.
- Operations channel edition: Discover remote devices automatically and manage PLC maintenance permissions with fine-grained control.
- SDK and API embedding: Enable lightweight development and fast integration into existing products or platforms.

## Use Cases

### Personal

- Remote multiplayer gaming
- Access to private personal devices
- Remote NAS access
- Remote file access

### Enterprise

- Enterprise office networking
- Remote operations and maintenance
- Branch and chain-store connectivity
- Industrial IoT scenarios
- Video surveillance connectivity
- Remote healthcare scenarios
