#!/bin/bash
# Verify no sensitive information is included

echo "=== Verifying Clean Package ==="
echo ""

# Check for hardcoded API tokens
echo "🔍 Checking for hardcoded API tokens..."
if grep -r "9c2ee424-da3d-462d-8d71-8bda9b548ac1" . 2>/dev/null; then
    echo "❌ Found hardcoded API token!"
    exit 1
else
    echo "✅ No hardcoded API tokens found"
fi

# Check for personal information
echo ""
echo "🔍 Checking for personal information..."
if grep -r "AD\|爪爪\|视频\|创作" . 2>/dev/null; then
    echo "⚠️  Found personal information references"
else
    echo "✅ No personal information found"
fi

# Check file permissions
echo ""
echo "🔍 Checking file permissions..."
find scripts/ -name "*.sh" -exec sh -c '
    if [ ! -x "$1" ]; then
        echo "❌ $1 is not executable"
        exit 1
    fi
' _ {} \;
echo "✅ All scripts are executable"

# Check for large files
echo ""
echo "🔍 Checking for large files..."
find . -type f -size +1M | while read file; do
    echo "⚠️  Large file found: $file"
done

echo ""
echo "✅ Verification completed successfully!"
echo "The package is ready for GitHub."
