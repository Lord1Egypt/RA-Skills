#!/bin/bash
set -e

echo "Testing FRITZ!Box Skill..."

# Check python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi

echo "✅ Python 3 found ($(python3 --version))"

# Check fritzbox.py exists
if [ ! -f "fritzbox.py" ]; then
    echo "❌ fritzbox.py not found"
    exit 1
fi

# Check syntax
python3 -m py_compile fritzbox.py && echo "✅ fritzbox.py syntax OK" || { echo "❌ Syntax error in fritzbox.py"; exit 1; }

# Check required files
for f in SKILL.md README.md requirements.txt _meta.json; do
    if [ ! -f "$f" ]; then
        echo "❌ $f not found"
        exit 1
    fi
done
echo "✅ All required files present"

# Check SKILL.md frontmatter
if ! head -1 SKILL.md | grep -q "^---$"; then
    echo "❌ SKILL.md missing YAML frontmatter"
    exit 1
fi
if ! grep -q "^name:" SKILL.md; then
    echo "❌ SKILL.md missing 'name' field"
    exit 1
fi
if ! grep -q "^description:" SKILL.md; then
    echo "❌ SKILL.md missing 'description' field"
    exit 1
fi
echo "✅ SKILL.md frontmatter valid"

# Check .env.example exists and has no real credentials
if [ ! -f ".env.example" ]; then
    echo "❌ .env.example not found"
    exit 1
fi
if grep -qiE "password\s*=\s*[^y]" .env.example; then
    echo "⚠️  Warning: .env.example may contain real credentials"
fi
echo "✅ .env.example present"

echo ""
echo "✅ All checks passed"
echo "✅ Ready to use"

if [ -z "$FRITZBOX_HOST" ]; then
    echo "⚠️  Note: Set FRITZBOX_HOST and FRITZBOX_PASSWORD for live testing"
else
    echo "✅ FRITZBOX_HOST is set"
fi
