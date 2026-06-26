# Phase 3: Dynamic Objects

## Mechanism Comparison

| Feature | Factory | Collection Factory | Collection Proxy |
|---------|----------|---------------------|------------------|
| Spawns | Single GO | Multiple GOs | New world |
| Physics | Current world | Current world | Isolated world |
| Namespace | Current collection | Current collection | New socket |
| Memory | Low | Medium | High |
| Use | Bullets, items | Enemy+weapon groups | Level switching |

## Factory

```lua
local id = factory.create(url, [position], [rotation], [properties], [scale])

local enemy = factory.create("#enemy_factory")
local coin = factory.create("#coin_factory", pos, nil, { value = 100 })
local boss = factory.create("#boss_factory", pos, nil, nil, 2.0)
```

| Param | Type | Notes |
|-------|------|-------|
| url | string | Factory component ID |
| position | vector3 | World position |
| rotation | quat | World rotation |
| properties | table | Script property overrides |
| scale | float/vector3 | Uniform or non-uniform |

## Factory Properties

```lua
factory.create("#coin", pos, nil, { value = 100, color = "gold" })

go.property("value", 1)
go.property("color", "silver")
```

## Accessing Spawned GO

```lua
local id = factory.create("#enemy")
msg.post(id, "attack", { target = player_id })

local url = msg.url(nil, id, "weapon")
msg.post(url, "enable")

sprite.play_flipbook(msg.url(nil, id, "body"), hash("idle"))
```

## Tracking Spawned Objects

```lua
self.spawned = {}

function spawn()
    local id = factory.create("#enemy")
    table.insert(self.spawned, id)
end

function clear()
    go.delete(self.spawned)
    self.spawned = {}
end
```

## Passing Parent Reference

```lua
local id = factory.create("#drone", pos, nil, { parent = msg.url() })

go.property("parent", msg.url())

function final(self)
    msg.post(self.parent, "drone_dead")
end
```

## Collection Factory

```lua
local ids = collectionfactory.create(url, [position], [rotation], [properties], [scale])

local ids = collectionfactory.create("#team_factory")
local bean = ids[hash("/bean")]
local shield = ids[hash("/shield")]

go.set_scale(0.5, bean)
msg.post(shield, "activate")
```

| Return | Type | Notes |
|--------|------|-------|
| ids | table | Key: collection ID hash, Value: runtime ID |

## Collection Factory Properties

```lua
local props = {}
props[hash("/bean")] = { hp = 100 }
props[hash("/weapon")] = { damage = 50 }
local ids = collectionfactory.create("#team", pos, nil, props)
```

## Dynamic Loading

```lua
factory.load("#factory", function(self, url, result)
    local id = factory.create(url)
end)

factory.unload("#factory")

collectionfactory.load("#factory", function(self, url, result)
    local ids = collectionfactory.create(url)
end)

collectionfactory.unload("#factory")
```

## Dynamic Prototype

```lua
factory.unload("#factory")
factory.set_prototype("#factory", "/enemies/boss.go")
local id = factory.create("#factory")

collectionfactory.unload("#factory")
collectionfactory.set_prototype("#factory", "/levels/level2.collection")
local ids = collectionfactory.create("#factory")
```

## Collection Proxy

```lua
msg.post("#proxy", "load")

function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

## Collection Proxy Messages

| Message | Effect |
|---------|--------|
| `load` | Sync load collection |
| `async_load` | Async load |
| `init` | Call init() on all GOs |
| `enable` | Start rendering |
| `disable` | Stop rendering |
| `final` | Call final() on all GOs |
| `unload` | Remove from memory |

## Unload Sequence

```lua
msg.post("#proxy", "disable")
msg.post("#proxy", "final")
msg.post("#proxy", "unload")

-- Or single step
msg.post("#proxy", "unload")
```

## Cross-World Addressing

```lua
-- From loaded world to bootstrap
msg.post("main:/loader#script", "level_done")

-- From bootstrap to loaded world
msg.post("level:/player#script", "wake_up")
```

## Time Step Control

```lua
msg.post("#proxy", "set_time_step", { factor = 0, mode = 0 })  -- Pause
msg.post("#proxy", "set_time_step", { factor = 1, mode = 1 })  -- Normal
msg.post("#proxy", "set_time_step", { factor = 0.5, mode = 1 }) -- Half speed
```

| Mode | Effect |
|------|--------|
| 0 | Discrete (freeze) |
| 1 | Continuous (scaled) |

## Level Manager Pattern

```lua
function load_level(self, level_name)
    if self.current_level then
        msg.post("#proxy", "unload")
    end
    collectionproxy.set_prototype("#proxy", "/levels/" .. level_name .. ".collection")
    msg.post("#proxy", "async_load")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_unloaded") then
        msg.post("#proxy", "async_load")
    elseif message_id == hash("proxy_loaded") then
        msg.post(sender, "init")
        msg.post(sender, "enable")
        self.current_level = sender
    end
end
```

## Object Pooling

Defold engine handles pooling internally. Direct `go.delete()` and `factory.create()` is optimal.

```lua
local id = factory.create("#bullet")
go.delete(id)
-- Engine reuses memory automatically
```

## Instance Limits

game.project `max_instances` limits total GO count per world.

## Choosing Mechanism

| Need | Use |
|------|-----|
| Spawn single GO repeatedly | Factory |
| Spawn GO group with hierarchy | Collection Factory |
| Load entire level/world | Collection Proxy |
| Modal dialog/popup | Collection Factory or Proxy |

## Manual Links

- https://defold.com/manuals/factory
- https://defold.com/manuals/collection-factory
- https://defold.com/manuals/collection-proxy