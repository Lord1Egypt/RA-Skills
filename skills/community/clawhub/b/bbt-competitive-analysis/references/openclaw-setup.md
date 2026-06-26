# OpenClaw Setup

When migrating this skill into OpenClaw, prefer OpenClaw-managed environment injection instead of `.env`.

## Placement

Place this directory under the OpenClaw workspace at `skills/competitive_analysis/`.

OpenClaw will automatically discover the skill from the workspace `skills/` directory.

## `openclaw.json` 示例

Add the following to `~/.openclaw/openclaw.json` or the workspace config:

```json5
{
  skills: {
    entries: {
      competitive_analysis: {
        enabled: true,
        env: {
          COMPETITIVE_ANALYSIS_DSN: "postgresql://postgres:password@127.0.0.1:5432/bbt",
          DINGTALK_WEBHOOK: "https://oapi.dingtalk.com/robot/send?access_token=your_access_token",
          DINGTALK_SECRET: "",
          OSS_ENDPOINT: "oss-cn-hangzhou.aliyuncs.com",
          OSS_BUCKET: "your-bucket-name",
          OSS_ACCESS_KEY_ID: "your-access-key-id",
          OSS_ACCESS_KEY_SECRET: "your-access-key-secret",
          OSS_PREFIX: "bbt-skills/competitive-analysis",
          OSS_PUBLIC_BASE_URL: "",
          COMPETITIVE_ANALYSIS_CATEGORY: "",
          COMPETITIVE_ANALYSIS_SINCE_MONTHS: "6",
          COMPETITIVE_ANALYSIS_LIMIT: "20",
          COMPETITIVE_ANALYSIS_BRAND: "BUBBLETREE",
          COMPETITIVE_ANALYSIS_REPORTER: "自动分析任务"
        }
      }
    }
  }
}
```

Notes:

- The config key must match the skill name: `competitive_analysis`.
- OpenClaw injects these environment variables at agent runtime.
- If the database password contains special characters, URL-encode it first.

## Reload

After changing the skill or `openclaw.json`, start a new session or restart the gateway:

```bash
/new
```

Or:

```bash
openclaw gateway restart
```

## Check Visibility

```bash
openclaw skills list
```

## Execution

Invoke the script from OpenClaw or an external scheduler:

```bash
python3 {baseDir}/scripts/run_report.py
```

## Agent Allowlist

If your OpenClaw agent uses a skills allowlist, include `competitive_analysis`.

Example:

```json5
{
  agents: {
    defaults: {
      skills: ["competitive_analysis"]
    }
  }
}
```
