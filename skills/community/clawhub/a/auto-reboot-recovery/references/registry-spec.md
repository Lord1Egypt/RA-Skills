# Service Registry 規格

## 檔案位置

`~/.openclaw/workspace/service-registry.json`

## 結構

```json
{
  "machine": {
    "name": "機器名稱",
    "os": "macos",
    "description": "用途描述"
  },
  "proxy_chain": {
    "description": "特殊網路代理（如 Telegram 走 VPS）",
    "hops": [
      { "name": "名稱", "type": "http|socks5|ssh", "listen": ":port", "target": "描述" }
    ]
  },
  "tunnels": {
    "provider": "frp|ngrok|cloudflared",
    "config_path": "config 檔案路徑",
    "entries": [
      { "subdomain": "子域名", "local_port": 1234, "service": "服務名" }
    ]
  },
  "services": [
    {
      "name": "服務顯示名稱",
      "tier": 1,
      "type": "launchagent",
      "label": "com.xxx.yyy",
      "program": "/path/to/binary",
      "args": ["arg1", "arg2"],
      "keep_alive": true,
      "log_prefix": "服務名",
      "description": "用途"
    },
    {
      "name": "服務顯示名稱",
      "tier": 2,
      "type": "tmux-bootstrap",
      "session": "tmux session 名",
      "socket": "openclaw",
      "port": 8124,
      "workdir": "/path/to/workdir",
      "command": "啟動指令",
      "description": "用途"
    },
    {
      "name": "服務顯示名稱",
      "tier": 3,
      "type": "wrapper-daemon",
      "session": "tmux session 名",
      "socket": "default",
      "workdir": "/path/to/workdir",
      "command": "啟動指令（在 tmux 裡送的）",
      "wrapper_label": "LaunchAgent label",
      "wrapper_script": "script 路徑",
      "check_interval": 30,
      "max_failures": 3,
      "cooldown_seconds": 3600,
      "startup_wait": 25,
      "description": "用途"
    }
  ]
}
```

## 欄位說明

### service 通用欄位

| 欄位 | 必填 | 說明 |
|---|---|---|
| name | ✅ | 人看的名稱 |
| tier | ✅ | 1 / 2 / 3 |
| type | ✅ | `launchagent` / `tmux-bootstrap` / `wrapper-daemon` |
| description | ✅ | 用途 |
| port | ❌ | 服務 port（有的話填） |

### Tier 1 專屬

| 欄位 | 說明 |
|---|---|
| label | LaunchAgent label |
| program | 可執行檔路徑 |
| args | 參數陣列 |
| keep_alive | 是否 KeepAlive |
| log_prefix | log 檔案前綴（存在 `~/.openclaw/logs/`） |

### Tier 2 專屬

| 欄位 | 說明 |
|---|---|
| session | tmux session 名 |
| socket | `openclaw` 或 `default` |
| workdir | 啟動前 cd 到的目錄 |
| command | tmux 裡的啟動指令 |

### Tier 3 專屬

| 欄位 | 說明 |
|---|---|
| session | tmux session 名 |
| socket | `openclaw` 或 `default` |
| workdir | 啟動前 cd 到的目錄 |
| command | tmux 裡送的指令 |
| wrapper_label | wrapper daemon 的 LaunchAgent label |
| wrapper_script | wrapper script 路徑 |
| check_interval | 檢查間隔（秒） |
| max_failures | 最大連續失敗次數 |
| cooldown_seconds | cooldown 秒數 |
| startup_wait | 啟動後等幾秒再檢查 |
