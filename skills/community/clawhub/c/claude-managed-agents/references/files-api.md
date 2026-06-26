# Files API workflows

Use this reference when the task involves uploading local files and mounting them into Managed Agents sessions.

## Upload a file

The helper now supports a dedicated upload path:

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  file upload \
  --file-path ./data.csv
```

Return only the file ID:

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  file upload \
  --file-path ./data.csv \
  --only-id
```

Override filename or MIME type when needed:

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  file upload \
  --file-path ./blob.bin \
  --filename dataset.parquet \
  --mime-type application/octet-stream
```

## Mount uploaded files into a session

```bash
FILE_ID=$(python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  file upload \
  --file-path ./data.csv \
  --only-id)

python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session create \
  --agent-id agent_123 \
  --environment-id env_123 \
  --resource-json "{\"type\":\"file\",\"file_id\":\"${FILE_ID}\",\"mount_path\":\"/workspace/data.csv\"}"
```

## Multiple file mounts

```bash
FILE_A=$(python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py file upload --file-path ./data.csv --only-id)
FILE_B=$(python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py file upload --file-path ./config.json --only-id)

python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session create \
  --agent-id agent_123 \
  --environment-id env_123 \
  --resource-json "{\"type\":\"file\",\"file_id\":\"${FILE_A}\",\"mount_path\":\"/workspace/data.csv\"}" \
  --resource-json "{\"type\":\"file\",\"file_id\":\"${FILE_B}\",\"mount_path\":\"/workspace/config.json\"}"
```

## List files

List all files, or only the files scoped to a session:

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  file list

python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  file list \
  --scope-id sesn_abc123
```

## Download a file

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  file download \
  --file-id file_abc123 \
  --output ./output.txt
```

Note: uploaded source files commonly return `downloadable: false` and are not valid inputs to `/content`. The download path is mainly for downloadable artifacts created by tools or session outputs.

## Delete a file

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  file delete \
  --file-id file_abc123
```

## Manage session resources after session creation

Add a resource to a running session:

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session resource add \
  --session-id sess_123 \
  --file-id file_abc123 \
  --mount-path /workspace/data.csv
```

List resources on a session:

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session resource list \
  --session-id sess_123
```

Delete a session resource by resource ID:

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session resource delete \
  --session-id sess_123 \
  --resource-id sesrsc_abc123
```

## Notes

- Upload and delete use the Files API beta header: `files-api-2025-04-14`
- File list/download for session-scoped workflows use the Managed Agents beta header
- Session creation and session resource operations use the Managed Agents beta header
- Uploaded source files may be listed but not downloadable. Check the `downloadable` field before calling `file download`.
- Mounted files are read-only copies inside the session container
- The platform may normalize mount paths into a session upload mount under `/mnt/session/uploads/...`
- Use absolute mount paths
