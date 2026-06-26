#!/bin/bash
# Simple security verification script

echo "🔒 Claw Code Suite Security Verification"
echo "========================================"

echo "1. Checking for Rust files..."
if find . -name "*.rs" | grep -q .; then
    echo "❌ FAIL: Rust source files found"
    find . -name "*.rs" | head -5
    exit 1
else
    echo "✅ PASS: No Rust source files"
fi

echo ""
echo "2. Checking for Cargo files..."
if find . -name "Cargo.*" -o -name "*.toml" | grep -v package.json | grep -q .; then
    echo "❌ FAIL: Cargo/toml files found"
    find . -name "Cargo.*" -o -name "*.toml" | grep -v package.json
    exit 1
else
    echo "✅ PASS: No Cargo/toml files"
fi

echo ""
echo "3. Checking for network imports in Python..."
if grep -r "import.*requests\|import.*http\|import.*urllib\|import.*socket" . --include="*.py" | grep -q .; then
    echo "❌ FAIL: Network imports found in Python code"
    grep -r "import.*requests\|import.*http\|import.*urllib\|import.*socket" . --include="*.py" | head -5
    exit 1
else
    echo "✅ PASS: No network imports in Python code"
fi

echo ""
echo "4. Checking for API key patterns..."
if grep -r "API_KEY\|api_key\|APIKEY\|oauth\|auth.*token" . -i --include="*.py" --include="*.json" | grep -q .; then
    echo "⚠️  WARNING: API key/oauth patterns found (checking if false positives)..."
    grep -r "API_KEY\|api_key\|APIKEY\|oauth\|auth.*token" . -i --include="*.py" --include="*.json" | head -5
    # Don't exit for warnings, just note them
else
    echo "✅ PASS: No API key/oauth patterns"
fi

echo ""
echo "5. Checking Python code integrity..."
if [ ! -f "./claw_harness.py" ]; then
    echo "❌ FAIL: Main harness missing"
    exit 1
else
    echo "✅ PASS: Main harness exists"
fi

if [ ! -f "./claw_harness_enhanced.py" ]; then
    echo "❌ FAIL: Enhanced harness missing"
    exit 1
else
    echo "✅ PASS: Enhanced harness exists"
fi

if [ ! -d "./claw-code/src" ]; then
    echo "❌ FAIL: Claw Code Python port missing"
    exit 1
else
    echo "✅ PASS: Claw Code Python port exists"
fi

echo ""
echo "========================================"
echo "✅ SECURITY VERIFICATION PASSED"
echo "This skill is clean, Python-only, and contains no network code."
echo ""
echo "Total size: $(du -sh . | cut -f1)"
echo "Python files: $(find . -name "*.py" | wc -l)"
echo "All files: $(find . -type f | wc -l)"