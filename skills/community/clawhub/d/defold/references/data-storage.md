# Phase 4: Data Storage

## File Access APIs

| API | Use | Platform |
|-----|-----|----------|
| `io.*` | Full file control | All (virtual FS on HTML5) |
| `sys.save/load` | Lua table persistence | All |
| `sys.load_resource` | Custom resources (archive) | All |
| `http.request` | Bundle resources (HTML5) | HTML5 |

## sys.save / sys.load

```lua
local path = sys.get_save_file("mygame", "savefile")

sys.save(path, { coins = 100, level = 5 })
local data = sys.load(path)
print(data.coins)
```

## io.* Operations

```lua
local f, err = io.open(path, "wb")
if f then
    f:write("data")
    f:close()
end

local f = io.open(path, "rb")
if f then
    local content = f:read("*a")
    f:close()
end

os.rename("old.txt", "new.txt")
os.remove("file.txt")
```

## Save File Paths

| Platform | Path |
|----------|------|
| Windows | `C:\Users\[User]\AppData\Roaming\[game]\` |
| macOS | `~/Library/Application Support/[game]/` |
| iOS | `Documents/[game]/` |
| Android | `/data/data/[package]/files/` |
| HTML5 | IndexedDB (virtual) |

## Custom Resources

Files packed in main archive. Read-only.

```lua
local data = sys.load_resource("/data/levels.json")
local levels = json.decode(data)
```

game.project: `Custom Resources: /assets/data`

## Bundle Resources

Files copied to app bundle. Read-write.

```lua
local app_path = sys.get_application_path()
local f = io.open(app_path .. "/config.txt", "rb")
local content = f:read("*a")
f:close()
```

game.project: `Bundle Resources: /res`

## Resource Comparison

| Feature | Custom | Bundle |
|---------|--------|--------|
| Load speed | Fast (archive) | Slow (filesystem) |
| Partial read | No | Yes |
| Modify runtime | No | Yes |
| Security | High | Low |

## Bundle Resource Structure

```
res/
├── common/         # All platforms
├── win32/          # Windows only
├── android/        # Android only
├── ios/            # iOS only
└── web/            # HTML5 only
```

## HTML5 Bundle Access

```lua
http.request("GET", "/config.txt", function(self, id, response)
    if response.status == 200 then
        print(response.response)
    end
end)
```

## DefSave

Install: `https://github.com/subsoap/defsave/archive/refs/tags/v1.2.6.zip`

```lua
local defsave = require("defsave.defsave")

defsave.load("game_save")
defsave.set("game_save", "coins", 1000)
defsave.set("game_save", "level", 5)
defsave.set("game_save", "items", { "sword", "shield" })

local coins = defsave.get("game_save", "coins")
local has_key = defsave.has_key("game_save", "coins")

defsave.save("game_save")
defsave.clear("game_save")
```

## DefSave Multi-File

```lua
defsave.load("config")
defsave.set("config", "sound", 0.8)

defsave.load("progress")
defsave.set("progress", "chapter", 3)

defsave.load("player")
defsave.set("player", "xp", 500)
```

Auto-saves on app exit.

## JSON Storage

```lua
local json = require("defold.utils.json")

local state = {
    player = { hp = 100, pos = { x = 10, y = 20 } },
    world = { level = "forest" }
}

local path = sys.get_save_file("game", "state")
local f = io.open(path, "wb")
f:write(json.encode(state))
f:close()

local f = io.open(path, "rb")
local loaded = json.decode(f:read("*a"))
f:close()
```

## Data Validation

```lua
local data = sys.load(path)
if not data.version or data.version < CURRENT_VERSION then
    data = default_data
    sys.save(path, data)
end

if not data.player then
    data.player = { hp = 100, coins = 0 }
end
```

## Auto-Save Pattern

```lua
function update(self, dt)
    self.save_timer = self.save_timer + dt
    if self.save_timer > 30 then
        defsave.save("game_save")
        self.save_timer = 0
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("critical_event") then
        defsave.save("game_save")
    end
end
```

## Data Separation

| Category | File | Example |
|----------|------|---------|
| System config | config.json | Sound/music volume |
| Player progress | progress.json | Level, unlocked items |
| Session state | Memory only | Current HP, position |

## HTML5 Notes

- `io.*` uses IndexedDB virtual filesystem
- Bundle resources require `http.request`
- localStorage not used by Defold

## Manual Links

- https://defold.com/manuals/file-access
- https://defold.com/ref/sys
- https://defold.com/ref/io
- https://defold.com/assets/defsave