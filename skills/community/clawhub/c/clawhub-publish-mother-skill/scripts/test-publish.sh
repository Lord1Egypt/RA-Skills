#!/bin/bash
echo "=== CLAWHUB PUBLISH TEST ==="
echo "Testing the publishing workflow..."
echo ""

# Check authentication
echo "1. Authentication check:"
clawhub whoami 2>&1
echo ""

# Check if in skill directory
echo "2. Directory check:"
if [ -f "SKILL.md" ]; then
    echo "✅ In skill directory (SKILL.md found)"
else
    echo "❌ Not in skill directory"
    echo "Run this from inside your skill directory"
    exit 1
fi

# Dry run
echo ""
echo "3. Dry run publish:"
echo "Command: clawhub publish . --dry-run"
echo ""
clawhub publish . --dry-run 2>&1 | head -20

echo ""
echo "=== TEST COMPLETE ==="
echo "If dry run succeeds, you can publish with:"
echo "clawhub publish . --slug your-slug --name "Your Skill" --version 1.0.0"
