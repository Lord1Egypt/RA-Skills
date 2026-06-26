# CtrlZ Skill Test Cases

## Quick Demo

```bash
bash ~/.openclaw/skills/ctrlz/scripts/demo.sh
```

## Test Case 1: Basic File Edit Undo

**Scenario**: Modify config file then regret

```bash
# 1. Create original file
echo "port: 8080" > config.yaml

# 2. Start session
SESSION=$(ctrlz start "Change port" | jq -r '.session_id')

# 3. Record operation
ctrlz record $SESSION file_edit config.yaml

# 4. Execute modification
echo "port: 3000" > config.yaml

# 5. Found error, execute undo
ctrlz undo

# 6. Verify
# config.yaml should be restored to port: 8080
```

**Expected Result**: ✓ Port restored to 8080

---

## Test Case 2: Multiple Files Undo

**Scenario**: Modified multiple files in one conversation

```bash
# 1. Create multiple original files
echo "v1.0" > version.txt
echo "debug: false" > settings.json

# 2. Start session
SESSION=$(ctrlz start "Update version and settings" | jq -r '.session_id')

# 3. Record multiple operations
ctrlz record $SESSION file_edit version.txt
ctrlz record $SESSION file_edit settings.json

# 4. Execute multiple modifications
echo "v2.0" > version.txt
echo '{"debug": true, "feature": "new"}' > settings.json

# 5. Undo all modifications at once
ctrlz undo

# 6. Verify both files restored
```

**Expected Result**: ✓ version.txt restored to v1.0, settings.json restored to debug: false

---

## Test Case 3: Stack Size Limit

**Scenario**: Default keeps 1 undo, set to 3

```bash
# Set stack to 3
ctrlz set-stack 3

# Execute 5 modifications
for i in {1..5}; do
  echo "content $i" > file.txt
  SESSION=$(ctrlz start "Modify $i" | jq -r '.session_id')
  ctrlz record $SESSION file_edit file.txt
  echo "new $i" > file.txt
done

# Check undoable count
ctrlz stats
# Should show active_sessions: 3 (not 5)

# Restore default
ctrlz set-stack 1
```

**Expected Result**: ✓ Only keeps recent 3 sessions, old ones auto-cleanup

---

## Test Case 4: New File Creation Undo

**Scenario**: Created wrong file and want to delete

```bash
# 1. Start session
SESSION=$(ctrlz start "Create temp file" | jq -r '.session_id')

# 2. Create file and record
touch wrong_file.txt
ctrlz record $SESSION file_write wrong_file.txt

# 3. Undo (will delete the file)
ctrlz undo

# 4. Verify file doesn't exist
ls wrong_file.txt  # Should show not exists
```

**Expected Result**: ✓ wrong_file.txt deleted

---

## Test Case 5: No More Undo

**Scenario**: No operation records when trying to undo

```bash
# Clear all records
ctrlz clear

# Try to undo
ctrlz undo
```

**Expected Result**: ✓ Shows error: "No more operations to undo"

---

## Test Case 6: Multiple Undo (undo 3)

**Scenario**: Undo recent 3 conversation rounds at once

```bash
# Execute 3 modifications
for i in 1 2 3; do
  echo "original $i" > "file$i.txt"
  SESSION=$(ctrlz start "Modify file$i" | jq -r '.session_id')
  ctrlz record $SESSION file_edit "file$i.txt"
  echo "changed $i" > "file$i.txt"
done

# Undo 3 at once
ctrlz undo 3

# Verify all files restored
```

**Expected Result**: ✓ All 3 files restored to original content

---

## Test Case 7: Directory Creation Undo

**Scenario**: Created wrong directory then delete

```bash
# 1. Start session
SESSION=$(ctrlz start "Create project directory" | jq -r '.session_id')

# 2. Create directory and record
mkdir -p /tmp/wrong_project/src
ctrlz record $SESSION dir_create /tmp/wrong_project

# 3. Create some files in directory
echo "code" > /tmp/wrong_project/src/main.js

# 4. Undo (entire directory deleted)
ctrlz undo

# 5. Verify
ls /tmp/wrong_project  # Should not exist
```

**Expected Result**: ✓ /tmp/wrong_project entire directory deleted

---

## Test Case 8: Package Installation Record

**Scenario**: Installed packages and recorded (cannot auto-remove)

```bash
# 1. Start session
SESSION=$(ctrlz start "Install lodash" | jq -r '.session_id')

# 2. Record installation
ctrlz record $SESSION exec_install "npm:lodash"

# 3. Actual installation
npm install lodash

# 4. Undo will show warning
ctrlz undo
# Output: "📦 The following package installations cannot be auto-undone:"
```

**Expected Result**: ⚠️ Shows warning and manual removal commands

---

## Integration Test

### Complete Workflow

```bash
# Scenario: Set up AI News Agent but config wrong, want to revert everything

# 1. Create original file
cp ~/.openclaw/cron/jobs.json ~/.openclaw/cron/jobs.json.bak

# 2. Start a big session
SESSION=$(ctrlz start "Setup AI News Agent" | jq -r '.session_id')

# 3. Modify cron config
ctrlz record $SESSION file_edit ~/.openclaw/cron/jobs.json
# ... modify json ...

# 4. Create database
ctrlz record $SESSION dir_create ~/.openclaw/agents/ai-news-agent
echo "CREATE TABLE..." | sqlite3 ~/.openclaw/agents/ai-news-agent/news.db

# 5. Found whole setup wrong, undo all
ctrlz undo

# 6. Verify
# - jobs.json restored
# - ai-news-agent directory deleted
```

**Expected Result**: ✓ All modifications reverted

---

## Performance Test

### Large Batch Test

```bash
# Create 100 files
SESSION=$(ctrlz start "Batch create files" | jq -r '.session_id')

for i in {1..100}; do
  echo "content $i" > "/tmp/batch/file$i.txt"
  ctrlz record $SESSION file_write "/tmp/batch/file$i.txt"
done

# Measure undo time
time ctrlz undo
```

**Expected Result**: ✓ 100 files undone within 2 seconds

---

## Edge Cases

### Empty File
```bash
touch empty.txt
SESSION=$(ctrlz start "Modify empty file" | jq -r '.session_id')
ctrlz record $SESSION file_edit empty.txt
echo "content" > empty.txt
ctrlz undo
# Should restore to empty file
```

### Large File
```bash
dd if=/dev/urandom of=large.bin bs=1M count=10
SESSION=$(ctrlz start "Modify large file" | jq -r '.session_id')
ctrlz record $SESSION file_edit large.bin
echo "new" > large.bin
ctrlz undo
# Should restore 10MB original content
```

### Special Characters Filename
```bash
echo "test" > "file with spaces.txt"
echo "test" > "file'with'quotes.txt"
# Verify these files can be undone normally
```

---

## Automated Test Execution

```bash
# Run all tests
bash ~/.openclaw/skills/ctrlz/scripts/test_ctrlz.sh

# Or run quick demo
bash ~/.openclaw/skills/ctrlz/scripts/demo.sh
```
