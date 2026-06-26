---
name: defold
description: Defold game engine development. Triggers: "Defold", "Defold project", "Defold engine", "Lua game", "mobile game development", "build a game", "game engine", "create game", "sprite animation", "physics collision", "game save system". Covers: GO/components/message passing, GUI/Druid, physics/collision/forces, animation/flipbook/Spine, input/binding, Factory/CollectionProxy, DefSave, game patterns. Use for any Defold-based game project.
---

# Defold Game Engine

## Quick Start

### Install Dependencies
```
https://github.com/Insality/druid/archive/refs/tags/1.2.2.zip
https://github.com/subsoap/defsave/archive/refs/tags/v1.2.6.zip
https://github.com/insality/defold-monarch/archive/1.0.zip
```

### Project Structure
```
main.collection
├── game_manager.go
├── player.go
└── ui.go
```

## Core Patterns

### Message Passing
```lua
msg.post("target#script", "event", { data = value })

function on_message(self, message_id, message, sender)
    if message_id == hash("event") then handle(message) end
end
```

### Dynamic Objects
```lua
local id = factory.create("#factory", pos, nil, { prop = value })
local ids = collectionfactory.create("#collection_factory")
msg.post("#proxy", "load")  -- Wait for proxy_loaded, then init+enable
```

### GUI (Druid)
```lua
self.druid = druid.new(self)
self.btn = self.druid:new_button("node", callback)
self.text = self.druid:new_text("node", "text")
```

### Physics
```lua
physics.apply_force("#collision", force)
physics.set_velocity("#collision", velocity)

function on_message(self, message_id, message, sender)
    if message_id == hash("collision_response") then
        handle_collision(message.other_id, message.normal)
    end
end
```

### Animation
```lua
sprite.play_flipbook("#sprite", "idle", callback)
go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, 100, go.EASING_OUTQUAD, 1.0)
```

### Input
```lua
msg.post(".", "acquire_input_focus")

function on_input(self, action_id, action)
    if action_id == hash("jump") and action.pressed then jump() end
end
```

### Save/Load
```lua
defsave.load("game")
defsave.set("game", "coins", 100)
local coins = defsave.get("game", "coins")
```

## References

- **Core Concepts**: [core-concepts.md](references/core-concepts.md) - GO, components, addressing, lifecycle
- **GUI System**: [gui-system.md](references/gui-system.md) - Nodes, layouts, Druid
- **Dynamic Objects**: [dynamic-objects.md](references/dynamic-objects.md) - Factory, Collection Factory, Proxy
- **Data Storage**: [data-storage.md](references/data-storage.md) - sys.save, DefSave, io.*
- **Physics**: [physics-system.md](references/physics-system.md) - Collision, forces, raycast
- **Animation**: [animation-system.md](references/animation-system.md) - Flipbook, Spine, go.animate
- **Input**: [input-system.md](references/input-system.md) - Binding, focus, on_input
- **Game Patterns**: [business-patterns.md](references/business-patterns.md) - Customers, shops, upgrades

## Performance

- Atlas all sprites
- Message-driven logic, avoid polling
- Reuse vectors/tables
- Engine handles object pooling