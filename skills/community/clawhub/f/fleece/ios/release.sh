#!/usr/bin/env bash
# Usage: ./release.sh <TEAM_ID>
# Example: ./release.sh ABC123DEF4
# Run from the ios/ directory after enrolling in Apple Developer Program.

set -euo pipefail

TEAM_ID="${1:-}"
if [[ -z "$TEAM_ID" ]]; then
  echo "Usage: $0 <TEAM_ID>"
  echo "Find your Team ID at developer.apple.com/account → Membership details"
  exit 1
fi

SCHEME="FleeceApp"
ARCHIVE="build/FleeceApp.xcarchive"

echo "==> Regenerating project with Team ID $TEAM_ID"
sed -i '' "s/DEVELOPMENT_TEAM: \"\"/DEVELOPMENT_TEAM: \"$TEAM_ID\"/" project.yml
xcodegen generate

echo "==> Archiving (Release)"
xcodebuild archive \
  -project FleeceApp.xcodeproj \
  -scheme "$SCHEME" \
  -configuration Release \
  -archivePath "$ARCHIVE" \
  -destination "generic/platform=iOS" \
  DEVELOPMENT_TEAM="$TEAM_ID" \
  | xcpretty 2>/dev/null || true

echo "==> Exporting + uploading to App Store Connect"
xcodebuild -exportArchive \
  -archivePath "$ARCHIVE" \
  -exportOptionsPlist ExportOptions.plist \
  -exportPath build/export \
  DEVELOPMENT_TEAM="$TEAM_ID"

echo ""
echo "✅ Done. Check App Store Connect → TestFlight for your build."
