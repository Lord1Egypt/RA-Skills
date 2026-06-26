#!/bin/bash
echo "🔍 VERIFYING ROOSTER'S CLAW CODE SKILLS"
echo "========================================"

# 1. Check directory exists
echo "1. Checking skill directory..."
if [ -d ~/.openclaw/skills/claw-code-master ]; then
    echo "   ✅ Directory exists"
    echo "   📁 Contents:"
    ls -la ~/.openclaw/skills/claw-code-master/
else
    echo "   ❌ Directory missing"
    exit 1
fi

# 2. Check executable
echo ""
echo "2. Checking executable..."
if [ -x ~/.openclaw/skills/claw-code-master/run.sh ]; then
    echo "   ✅ run.sh is executable"
else
    echo "   ❌ run.sh not executable"
    chmod +x ~/.openclaw/skills/claw-code-master/run.sh
    echo "   🔧 Fixed permissions"
fi

# 3. Test basic command
echo ""
echo "3. Testing basic command..."
cd ~/.openclaw/skills/claw-code-master
timeout 10 ./run.sh summary > /tmp/rooster_test.txt 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Command executed successfully"
    echo "   📊 First 3 lines of output:"
    head -3 /tmp/rooster_test.txt
else
    echo "   ❌ Command failed"
    echo "   📋 Error output:"
    cat /tmp/rooster_test.txt
fi

# 4. Check capability count
echo ""
echo "4. Checking capability counts..."
if grep -q "207" /tmp/rooster_test.txt && grep -q "184" /tmp/rooster_test.txt; then
    echo "   ✅ 207 commands and 184 tools confirmed"
else
    echo "   ⚠️  Counts not found in output"
    echo "   📋 Searching for counts..."
    grep -E "207|184" /tmp/rooster_test.txt || echo "   ❌ No counts found"
fi

# 5. Test all 6 commands
echo ""
echo "5. Testing all 6 commands..."
commands=("summary" "tools --limit 2" "commands --limit 2" "manifest" "subsystems" "parity-audit")
for cmd in "${commands[@]}"; do
    echo "   Testing: $cmd"
    timeout 5 ./run.sh $cmd > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "     ✅ Success"
    else
        echo "     ❌ Failed"
    fi
done

echo ""
echo "========================================"
echo "📋 VERIFICATION COMPLETE"
echo ""
echo "If all tests pass, ROOSTER has full access to:"
echo "✅ 207 Claw Code commands"
echo "✅ 184 Claw Code tools"
echo "✅ 6 harness commands"
echo "✅ Python port integration"
