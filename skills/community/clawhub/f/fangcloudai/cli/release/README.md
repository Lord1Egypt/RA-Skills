# Fangcloud CLI Release

Use the binary that matches the user's OS and CPU architecture.

## Download Base URL

- `https://app.fangcloud.com/sync/vv25/knowclaw/release/`

## Platform Mapping

- Windows `amd64`:
  - `https://app.fangcloud.com/sync/vv25/knowclaw/release/fangcloud-windows-amd64.exe`
- Windows `arm64`:
  - `https://app.fangcloud.com/sync/vv25/knowclaw/release/fangcloud-windows-arm64.exe`
- macOS Intel `amd64`:
  - `https://app.fangcloud.com/sync/vv25/knowclaw/release/fangcloud-macos-amd64.zip`
- macOS Apple Silicon `arm64`:
  - `https://app.fangcloud.com/sync/vv25/knowclaw/release/fangcloud-macos-arm64.zip`
- Linux `amd64`:
  - `https://app.fangcloud.com/sync/vv25/knowclaw/release/fangcloud-linux-amd64.zip`
- Linux `arm64`:
  - `https://app.fangcloud.com/sync/vv25/knowclaw/release/fangcloud-linux-arm64.zip`

## Environment Variables

- `FANGCLOUD_USER_TOKEN`
- `FANGCLOUD_ADMIN_TOKEN` when calling admin URLs

## Auto Detect And Download

- Preferred:
  - macOS / Linux: `./cli/scripts/download_release_binary.sh`
  - Windows (PowerShell): `.\cli\scripts\download_release_binary.ps1`
- macOS / Linux:
  - download script saves the source zip into `cli/release/`
  - extracted binary is saved into `cli/bin/`
- macOS / Linux (`bash`):
  - `os="$(uname -s)"; arch="$(uname -m)"; base="https://app.fangcloud.com/sync/vv25/knowclaw/release"; case "$os" in Darwin) [ "$arch" = "arm64" ] && file="fangcloud-macos-arm64.zip" || file="fangcloud-macos-amd64.zip" ;; Linux) [ "$arch" = "aarch64" ] && file="fangcloud-linux-arm64.zip" || file="fangcloud-linux-amd64.zip" ;; *) echo "unsupported os: $os"; exit 1 ;; esac; curl -fL "$base/$file" -o "$file"`
- Windows (PowerShell):
  - `$base="https://app.fangcloud.com/sync/vv25/knowclaw/release"; $arch=$env:PROCESSOR_ARCHITECTURE; if ($arch -eq "ARM64") { $file="fangcloud-windows-arm64.exe" } else { $file="fangcloud-windows-amd64.exe" }; Invoke-WebRequest "$base/$file" -OutFile "$file"`

## Run

- macOS / Linux:
  - `./cli/scripts/download_release_binary.sh`
  - `./cli/bin/fangcloud-macos-arm64 --help`
  - `./cli/bin/fangcloud-macos-arm64 api GET /v2/user/info`
  - optional: `export PATH="$(pwd)/cli/bin:$PATH"` then run `fangcloud-macos-arm64 ...`
- Windows PowerShell:
  - `.\cli\scripts\run_release_binary.ps1 --help`
  - `.\cli\scripts\run_release_binary.ps1 api GET /v2/user/info`
