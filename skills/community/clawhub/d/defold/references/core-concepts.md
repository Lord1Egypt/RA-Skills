# Phase 1: Core Concepts

## Building Blocks

| Type | Description | File | Runtime Object |
|------|-------------|------|----------------|
| Collection | Container for GOs and nested collections | `.collection` | No (namespace only) |
| Game Object | Entity with position/rotation/scale | `.go` | Yes |
| Component | Behavior attached to GO | In `.go` or file ref | Yes |

## Component Types

| Type | API | Use Case |
|------|-----|----------|
| Sprite | `sprite.*` | 2D image/flipbook |
| Script | `go.*, physics.*` | Logic |
| GUI | `gui.*` | Interface |
| Factory | `factory.*` | Spawn GO |
| Collection Factory | `collectionfactory.*` | Spawn collection |
| Collection Proxy | `collectionproxy.*` | Load world |
| Collision Object | `physics.*` | Physics |
| Sound | `sound.*` | Audio |
| Camera | `camera.*` | Viewport |

## Addressing

```
[socket:][path][#fragment]
```

| Symbol | Meaning | Example |
|--------|---------|---------|
| `.` | Current GO | `msg.post(".", "disable")` |
| `#` | Current script | `msg.post("#", "reset")` |
| `#id` | Component in GO | `msg.post("#sprite", "play_flipbook", ...)` |
| `go_id` | GO in collection | `msg.post("enemy", "attack")` |
| `/path` | Absolute path | `msg.post("/manager#script", "hello")` |
| `socket:` | World identifier | `msg.post("level:/player", "wake")` |

```lua
local url = msg.url("main", "/manager", "controller")
print(url.socket, url.path, url.fragment)

local id = go.get_id()
local other = hash("/path/to/object")
```

## Message Passing

```lua
msg.post(receiver, message_id, [message])
```

| Param | Type | Notes |
|-------|------|-------|
| receiver | string/hash/URL | Target component/GO |
| message_id | string/hash | Message name |
| message | table | Data payload (max 2KB) |

```lua
msg.post("enemy#script", "attack")
msg.post("/hud#gui", "update_score", { score = 100 })

function on_message(self, message_id, message, sender)
    if message_id == hash("attack") then
        self.hp = self.hp - message.damage
    end
end
```

## System Messages

| Message | Target | Effect |
|---------|--------|--------|
| `enable` | Component | Activate |
| `disable` | Component | Deactivate |
| `acquire_input_focus` | GO/script | Receive input |
| `release_input_focus` | GO/script | Stop receiving |
| `set_parent` | GO | Change parent |
| `delete` | GO | Remove |

## Script Lifecycle

```lua
function init(self) end
function final(self) end
function fixed_update(self, dt) end
function update(self, dt) end
function late_update(self, dt) end
function on_message(self, message_id, message, sender) end
function on_input(self, action_id, action) end
function on_reload(self) end
```

| Callback | When | Use |
|----------|------|-----|
| `init` | Spawn | Initialize state |
| `final` | Delete | Cleanup |
| `fixed_update` | Physics step | Physics logic |
| `update` | Every frame | Game logic |
| `late_update` | After update | Post-processing |
| `on_message` | Message received | Handle events |
| `on_input` | Input event | User interaction |

## Script Types

| Type | Extension | API Access |
|------|-----------|------------|
| GO Script | `.script` | `go.*, physics.*` |
| GUI Script | `.gui_script` | `gui.*` |
| Render Script | `.render_script` | `render.*` |

## Self Variable

```lua
self.health = 100
self.speed = 5

local pos = go.get_position()
go.set_position(pos + vmath.vector3(self.speed, 0, 0))
```

## Properties

```lua
go.property("speed", 5)
go.property("max_hp", 100)

local speed = go.get("#", "speed")
go.set("#", "speed", 10)

go.animate("#", "speed", go.PLAYBACK_LOOP_PINGPONG, 15, go.EASING_LINEAR, 1.0)
```

## GO Functions

```lua
go.get_id()
go.get_position([id])
go.set_position(pos, [id])
go.get_rotation([id])
go.set_rotation(rot, [id])
go.get_scale([id])
go.set_scale(scale, [id])
go.delete([id], [recursive])
go.animate(id, property, playback, to, easing, duration, [delay], [callback])
```

## Playback Modes

| Mode | Behavior |
|------|----------|
| `PLAYBACK_ONCE_FORWARD` | Play once |
| `PLAYBACK_ONCE_BACKWARD` | Reverse once |
| `PLAYBACK_ONCE_PINGPONG` | Forward then back |
| `PLAYBACK_LOOP_FORWARD` | Loop forward |
| `PLAYBACK_LOOP_BACKWARD` | Loop reverse |
| `PLAYBACK_LOOP_PINGPONG` | Loop ping-pong |

## Easing Functions

| Function | Curve |
|----------|-------|
| `EASING_LINEAR` | Linear |
| `EASING_INQUAD` | Accelerate |
| `EASING_OUTQUAD` | Decelerate |
| `EASING_INOUTQUAD` | Smooth |
| `EASING_OUTELASTIC` | Elastic |
| `EASING_INBACK` | Anticipate |

## Timer Module

```lua
timer.delay(seconds, repeat, callback)
timer.cancel(timer_id)

timer.delay(2, false, function()
    msg.post("enemy", "spawn")
end)
```

## Parent-Child Hierarchy

```lua
local parent = go.get_id("parent_go")
msg.post("child", "set_parent", { parent_id = parent })
```

Transform propagates: parent position/rotation/scale affects children.

## Lua Performance

```lua
local pos = vmath.vector3()
function update(self, dt)
    pos.x = 0
    pos.y = 0
end

print(collectgarbage("count") * 1024)
```

## Lua Scope

| Scope | Syntax | Visibility |
|-------|--------|------------|
| Global | `var = value` | All scripts |
| File-local | `local var = value` | Same file instances |
| Instance | `self.var = value` | Current instance |
| Function-local | `local var` in function | Function only |

## Vmath

```lua
local v = vmath.vector3(x, y, z)
local q = vmath.quat_rotation_z(angle)
local m = vmath.matrix4()
local d = vmath.length(v)
local n = vmath.normalize(v)
local dot = vmath.dot(a, b)
local cross = vmath.cross(a, b)
local lerp = vmath.lerp(t, a, b)
```

## Application Lifecycle

1. **Init**: Load bootstrap collection, call `init()`
2. **Update Loop**: Input → fixed_update → update → late_update → render
3. **Final**: `final()`, cleanup

## Collection vs Parent

| Concept | Effect | Changeable |
|---------|--------|------------|
| Collection hierarchy | Addressing namespace | Static |
| Parent-child | Transform propagation | Runtime |

## In-place vs File Reference

| Type | Use For | Notes |
|------|---------|-------|
| In-place | Unique instances | Edit affects only this |
| File reference | Shared prototypes | Required: Script, GUI, ParticleFX, Tilemap |

## Manual Links

- https://defold.com/manuals/building-blocks
- https://defold.com/manuals/addressing
- https://defold.com/manuals/message-passing
- https://defold.com/manuals/script
- https://defold.com/manuals/lua