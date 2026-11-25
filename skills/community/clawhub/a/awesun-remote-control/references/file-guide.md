# Remote File Management & Transfer Guide

Detailed file exploration, manipulation, and asynchronous file transfer operations for `awesun-cli`.

---

## 1. Prerequisites

All file management commands require an active `type=file` session.

```bash
awesun-cli session connect --type file --remote-id 1738789907
# Returns session_id: file_session_001
```

---

## 2. Remote Directory Operations

### Browse Remote Files (`file ls`)
```bash
# List desktop files (default path when --path is omitted is "#desktop")
awesun-cli file ls file_session_001

# List specific remote path with limit and keyword filter
awesun-cli file ls file_session_001 --path /var/log --limit 50 --keyword "app"
```

### Create Remote Directory (`file mkdir`)
```bash
awesun-cli file mkdir file_session_001 --path /home/user/work --name "backup"
```

### Rename Remote File or Directory (`file mv`)
> [!NOTE]
> `file mv` performs **in-place rename only**. Moving files to a different directory path is not supported.

```bash
awesun-cli file mv file_session_001 --path /home/user/work/data.csv --new-name "data_v2.csv"
```

### Delete Remote File or Directory (`file rm`)
```bash
# Delete file
awesun-cli file rm file_session_001 --path /home/user/work/temp.log

# Recursively delete directory
awesun-cli file rm file_session_001 --path /home/user/work/temp_folder -r
```

---

## 3. File Transfer (`file transfer`)

File transfers are executed asynchronously in the background.

### Upload File (Local -> Remote)
```bash
awesun-cli file transfer file_session_001 \
  --type up \
  --local /local/path/app.zip \
  --remote /home/user/downloads/app.zip \
  --override
```

### Download File (Remote -> Local)
> [!IMPORTANT]
> **`--local` MUST be an existing local DIRECTORY, NOT a full file path.**
> The CLI automatically saves the remote file into the target directory with its original filename. Passing a non-existent directory or a file path will cause transfer failure.

```bash
# Ensure the local destination directory exists first
mkdir -p ~/Downloads

awesun-cli file transfer file_session_001 \
  --type down \
  --remote /home/user/reports/annual.pdf \
  --local ~/Downloads/
```

### Polling Transfer Status
Transfers generate a `transfer-id`. You must poll `file transfer status` until the status reaches `finished`:

```bash
# Polling loop example
while true; do
  STATE=$(awesun-cli file transfer status file_session_001 --transfer-id <transfer_id>)
  if echo "$STATE" | grep -q "finished"; then
    echo "Transfer completed!"
    break
  fi
  sleep 3
done
```

### Cancel Transfer
```bash
awesun-cli file transfer cancel file_session_001 --transfer-id <transfer_id>
```

---

## 4. Key Rules & Path Pitfalls

1. **Path format**:
   - On macOS/Linux targets, use absolute paths (e.g., `/Users/<username>/Downloads`, `/home/<username>/documents`). Do not use `~` shorthand in remote paths as it may not expand correctly.
   - On Windows targets, use backslashes or quoted paths (e.g., `C:\Users\Admin\Desktop`).
2. **Pre-check paths**:
   - Always run `awesun-cli file ls` to verify the parent directory and remote file existence before issuing deletion or transfer commands.
