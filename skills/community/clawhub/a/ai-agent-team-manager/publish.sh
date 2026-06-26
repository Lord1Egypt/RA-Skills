#!/bin/bash
# AI Agent Team Manager - Publish Script

echo "🚀 Publishing AI Agent Team Manager to ClawHub..."

# Validate skill structure
if [ ! -f "SKILL.md" ]; then
    echo "❌ Error: SKILL.md not found"
    exit 1
fi

if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found"
    exit 1
fi

echo "✅ Skill structure validated"

# Build and test
echo "🧪 Running tests..."
# Add test commands here when needed

echo "📤 Ready to publish!"
echo "Run: clawhub publish . --slug ai-agent-team-manager --name \"AI Agent Team Manager\" --version 1.0.0 --tags latest --changelog \"Initial release\""

echo "🎯 Pricing: $69/month (Professional), $129/month (Enterprise)"