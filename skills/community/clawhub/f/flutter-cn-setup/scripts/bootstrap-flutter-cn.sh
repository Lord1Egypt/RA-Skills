#!/usr/bin/env bash

set -euo pipefail

FLUTTER_DIR="${FLUTTER_DIR:-$HOME/development/flutter}"
SHELL_PROFILE="${SHELL_PROFILE:-$HOME/.zshrc}"
NEED_IOS="${NEED_IOS:-yes}" # yes|no
MIRROR_PUB_URL="${MIRROR_PUB_URL:-https://pub.flutter-io.cn}"
MIRROR_STORAGE_URL="${MIRROR_STORAGE_URL:-https://storage.flutter-io.cn}"

log() {
  printf "\n[%s] %s\n" "$(date '+%H:%M:%S')" "$*"
}

has_cmd() {
  command -v "$1" >/dev/null 2>&1
}

append_if_missing() {
  local line="$1"
  local file="$2"
  if [[ ! -f "$file" ]]; then
    touch "$file"
  fi
  if ! grep -Fqx "$line" "$file"; then
    printf "%s\n" "$line" >> "$file"
  fi
}

check_macos() {
  if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "This script is for macOS only."
    exit 1
  fi
}

install_base_tools() {
  if ! has_cmd brew; then
    cat <<'EOF'
Homebrew is not installed.
Install it first:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
Then re-run this script.
EOF
    exit 1
  fi

  log "Installing base tools with Homebrew"
  brew install git curl unzip xz
}

install_or_update_flutter() {
  mkdir -p "$(dirname "$FLUTTER_DIR")"
  if [[ -d "$FLUTTER_DIR/.git" ]]; then
    log "Flutter exists, updating stable branch"
    git -C "$FLUTTER_DIR" fetch --tags
    git -C "$FLUTTER_DIR" checkout stable
    git -C "$FLUTTER_DIR" pull --ff-only
  else
    log "Cloning Flutter stable to $FLUTTER_DIR"
    git clone https://github.com/flutter/flutter.git -b stable "$FLUTTER_DIR"
  fi
}

configure_shell_profile() {
  log "Configuring mirrors and PATH in $SHELL_PROFILE"
  append_if_missing "# Flutter CN mirrors" "$SHELL_PROFILE"
  append_if_missing "export PUB_HOSTED_URL=$MIRROR_PUB_URL" "$SHELL_PROFILE"
  append_if_missing "export FLUTTER_STORAGE_BASE_URL=$MIRROR_STORAGE_URL" "$SHELL_PROFILE"
  append_if_missing "# Flutter SDK PATH" "$SHELL_PROFILE"
  append_if_missing "export PATH=\"\$PATH:$FLUTTER_DIR/bin\"" "$SHELL_PROFILE"

  # Also export in current shell for immediate usage.
  export PUB_HOSTED_URL="$MIRROR_PUB_URL"
  export FLUTTER_STORAGE_BASE_URL="$MIRROR_STORAGE_URL"
  export PATH="$PATH:$FLUTTER_DIR/bin"
}

run_flutter_checks() {
  log "Running flutter precache and doctor"
  flutter --version
  flutter precache
  flutter doctor -v
}

handle_android_reminder() {
  log "Android next steps"
  cat <<'EOF'
1) Install Android Studio and open it once.
2) In SDK Manager, install:
   - Android SDK Platform
   - Android SDK Platform-Tools
   - Android SDK Command-line Tools
   - Android Emulator
3) Then run:
   flutter doctor --android-licenses
   flutter doctor -v
EOF
}

handle_ios_reminder() {
  if [[ "$NEED_IOS" != "yes" ]]; then
    log "Skipping iOS setup reminder (NEED_IOS=$NEED_IOS)"
    return 0
  fi

  log "iOS next steps"
  cat <<'EOF'
1) Install Xcode from App Store.
2) Run:
   sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
   sudo xcodebuild -runFirstLaunch
3) Install CocoaPods:
   brew install cocoapods
4) Verify:
   pod --version
   flutter doctor -v
EOF
}

create_smoke_project() {
  local project_dir="$HOME/hello_flutter_cn"
  if [[ -d "$project_dir" ]]; then
    log "Smoke project already exists: $project_dir"
    return 0
  fi

  log "Creating smoke test Flutter app at $project_dir"
  flutter create "$project_dir"
  (
    cd "$project_dir"
    flutter pub get
  )
}

main() {
  check_macos
  log "Starting Flutter CN bootstrap"
  log "Config: FLUTTER_DIR=$FLUTTER_DIR, SHELL_PROFILE=$SHELL_PROFILE, NEED_IOS=$NEED_IOS"

  install_base_tools
  install_or_update_flutter
  configure_shell_profile
  run_flutter_checks
  handle_android_reminder
  handle_ios_reminder
  create_smoke_project

  log "Done. Open a new terminal or run: source \"$SHELL_PROFILE\""
}

main "$@"
