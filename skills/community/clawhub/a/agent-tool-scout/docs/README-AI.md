# CLAM — CLI / MCP / Lobster Reference

CLAM 把 macOS 应用变成 CLI 命令，你可以直接在终端调用 `clam-<app>` 来控制应用。

> **Agent 集成**：可作为 OpenClaw Skill / Lobster pipeline step / Claude Code MCP Server / 或任何能调用 shell 的 Agent 框架使用。

## CLI 命令

```bash
clam --json scan                      # 发现可控应用
clam --json info music                # 查看 Music 的全部能力
clam install music                    # 安装（如果还没装的话）
clam-music --json get-current-track   # 调用
```

## 完整示例：控制 Music

```bash
# 播放控制
clam-music play
clam-music pause
clam-music next-track

# 读取属性
clam-music get-sound-volume             # → 73
clam-music get-player-state             # → playing

# 写入属性
clam-music set-sound-volume 50

# 嵌套对象（当前曲目的详细信息）
clam-music get-current-track-name       # → Slow Devotion
clam-music get-current-track-artist     # → Leon Vynehall
clam-music --json get-current-track     # → 全部属性 JSON
```

## JSON API

所有 `clam` 和 `clam-<app>` 命令都支持 `--json` 输出

### `clam --json scan`

```json
[
  {
    "name": "Music",
    "app_id": "music",
    "commands": 19,
    "properties": 19,
    "nested_groups": 6,
    "installed": true,
    "mode": "full"
  },
  {
    "name": "Figma",
    "app_id": "figma",
    "commands": 0,
    "properties": 0,
    "mode": "ui"
  }
]
```

`mode`: `"full"` = 完整 AppleScript 支持, `"ui"` = UI Scripting (菜单点击)

### `clam --json info <app_id>`

返回完整能力清单，**调用前先读这个，了解有哪些命令可用**

App ID 支持模糊匹配：`chrome` → `google-chrome`，`word` → `microsoft-word`

```json
{
  "app_id": "music",
  "app_name": "Music",
  "entry_point": "clam-music",
  "commands": [
    {
      "name": "play",
      "description": "play the current track or the specified track or file.",
      "has_direct_param": true,
      "params": [{"name": "--once", "description": "If true, play this track once and then stop."}]
    }
  ],
  "properties": [
    {
      "name": "sound-volume",
      "access": "rw",
      "type": "int",
      "get_command": "get-sound-volume",
      "set_command": "set-sound-volume"
    }
  ],
  "nested_groups": [
    {
      "name": "current-track",
      "compound_command": "get-current-track",
      "properties": [
        {"name": "name", "access": "rw", "get_command": "get-current-track-name"}
      ]
    }
  ]
}
```

### `clam --json install <app_id>`

```json
{"app_id": "music", "entry_point": "clam-music", "commands": 19, "properties": 19, "mode": "full"}
```

## 命令模式

```bash
clam-music play                         # 动作命令
clam-music play "some file"             # 带位置参数
clam-music export "playlist" --as m3u   # 带命名参数

clam-music get-sound-volume             # 读属性 → 73
clam-music set-sound-volume 50          # 写属性

clam-music get-current-track-name       # 读嵌套对象属性
clam-music --json get-current-track     # 读嵌套对象全部属性
```

## 错误处理

非零退出码 + stderr 输出，常见错误：

- `permission denied` → 需要在系统设置中授权自动化权限
- `accessibility access denied` → 需要辅助功能权限（UI Scripting 模式）
- `object not available` → 对象不存在（如没有正在播放的曲目）

## 注意事项

- 命令通过 `osascript` 执行，超时 30 秒
- 属性类型：`str`/`int`/`float`/`bool`，布尔值接受 `true`/`false`
- UI Scripting 模式需要目标应用正在运行
- 用 `clam-<app> api` 可以快速查看某个应用的全部可用命令
