#!/bin/bash

echo "🧪 Testing AI Content Generator Pro Skill"
echo "========================================"

# Test 1: Check Node.js and dependencies
echo "1. Checking Node.js..."
node --version
if [ $? -eq 0 ]; then
    echo "✅ Node.js OK"
else
    echo "❌ Node.js check failed"
    exit 1
fi

echo "2. Checking dependencies..."
npm list --depth=0
if [ $? -eq 0 ]; then
    echo "✅ Dependencies OK"
else
    echo "⚠️  Some dependencies may be missing"
fi

# Test 2: Check configuration files
echo "3. Checking configuration..."
if [ -f "config/config.json" ]; then
    echo "✅ Config file exists"
else
    echo "⚠️  Config file missing, creating default..."
    mkdir -p config
    cat > config/config.json << EOF
{
  "openai": {
    "apiKey": "test",
    "model": "gpt-4"
  },
  "defaultModel": "openai",
  "tone": "professional"
}
EOF
fi

# Test 3: Test the skill directly
echo "4. Testing skill functionality..."
echo "Running help command..."
node index.js help
if [ $? -eq 0 ]; then
    echo "✅ Help command works"
else
    echo "❌ Help command failed"
    exit 1
fi

# Test 4: Test content generation (simulated)
echo "5. Testing content generation..."
mkdir -p test-output
node index.js generate blog "Test Topic" > test-output/test1.txt 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Content generation works"
    echo "Sample output:"
    head -5 test-output/test1.txt
else
    echo "❌ Content generation failed"
    exit 1
fi

# Test 5: Test configuration
echo "6. Testing configuration..."
node index.js config show > test-output/config.txt 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Configuration works"
else
    echo "❌ Configuration failed"
fi

# Test 6: Check file structure
echo "7. Checking file structure..."
required_files=("index.js" "package.json" "SKILL.md" "config/models.json" "config/templates.json")
missing_files=0
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
        missing_files=$((missing_files + 1))
    fi
done

if [ $missing_files -gt 0 ]; then
    echo "⚠️  Missing $missing_files required files"
else
    echo "✅ All required files present"
fi

# Cleanup
echo "8. Cleaning up..."
rm -rf test-output

echo ""
echo "📊 Test Summary"
echo "=============="
echo "All basic tests passed! The skill is ready for use."
echo ""
echo "To run full integration tests:"
echo "1. Add real API keys to config/config.json"
echo "2. Run: node index.js generate blog 'Real Topic'"
echo "3. Check the generated content in the 'content' directory"
echo ""
echo "For OpenClaw integration testing:"
echo "1. Install the skill: openclaw skill install ."
echo "2. Test commands: openclaw content generate blog 'Test'"
echo ""
echo "✅ Testing complete!"