# Defold Game Engine Skill

Build 2D games with Defold - from business simulation to platformers.

## Why This Skill

Defold is a free, open-source game engine optimized for 2D mobile games. This skill provides comprehensive knowledge for AI agents to develop Defold games efficiently:

- **9 core domains**: Core concepts, GUI, physics, animation, input, dynamic objects, data storage, and game patterns
- **Code-first approach**: Every pattern includes working code examples
- **Agent-optimized**: Concise format (170-280 lines per reference), API tables, no冗余解释
- **Battle-tested patterns**: Real game logic for customers, shops, upgrades, collisions

## When This Skill Triggers

User says:
- "Defold" / "Defold引擎"
- "Defold project" / "Defold项目"
- "Lua game" / "Lua游戏"
- "Mobile game" / "手机游戏"
- "Build a game" / "构建游戏"
- "Game engine" / "游戏引擎"
- "Sprite animation" / "精灵动画"
- "Physics collision" / "物理碰撞"
- "Game save" / "游戏保存"

## Supported Game Types

| Type | Coverage |
|------|----------|
| Business Simulation | ★★★★★ |
| Platformer | ★★★★☆ |
| Casual Physics | ★★★★☆ |
| Idle/Clicker | ★★★★★ |
| Tower Defense | ★★★★☆ |
| Card/Board | ★★★★★ |

## Quick Start

### Install Dependencies
```
https://github.com/Insality/druid/archive/refs/tags/1.2.2.zip
https://github.com/subsoap/defsave/archive/refs/tags/v1.2.6.zip
```

### Core Pattern
```lua
-- Message passing
msg.post("target#script", "event", { data = value })

-- Spawn dynamically
local id = factory.create("#factory", pos)

-- Physics collision
physics.apply_force("#collision", force)

-- Animation
sprite.play_flipbook("#sprite", "idle")

-- Input
function on_input(self, action_id, action)
    if action_id == hash("jump") and action.pressed then jump() end
end
```

## Skill Contents

| Reference | Lines | Coverage |
|-----------|-------|----------|
| core-concepts.md | ~180 | GO, components, messaging, addressing, lifecycle |
| gui-system.md | ~230 | Nodes, layouts, templates, Druid framework |
| physics-system.md | ~250 | Collision types, forces, raycast, triggers |
| animation-system.md | ~270 | Flipbook, Spine, property animation, easing |
| input-system.md | ~280 | Binding, focus, touch, gamepad, multi-touch |
| dynamic-objects.md | ~180 | Factory, Collection Factory, Proxy |
| data-storage.md | ~170 | sys.save, DefSave, io.*, Custom/Bundle |
| business-patterns.md | ~200 | Customers, shops, upgrades, economy |

## Installation

Copy `defold.skill` to your skill directory, or install via ClawHub.

## Technical Stack

- **Engine**: Defold (LuaJIT-based)
- **UI Framework**: Druid (MIT)
- **Save System**: DefSave (CC0)
- **Screen Manager**: Monarch (optional)
- **Language**: Lua 5.1 compatible

## Platform Targets

| Platform | Package Size |
|----------|--------------|
| iOS | ~2MB |
| Android | ~1.5MB |
| HTML5 | ~3MB |
| Steam | ~5MB |

## License

Skill content is free to use. Defold engine is free with perpetual license.

## References

- [Defold Manual](https://defold.com/manuals)
- [Druid Framework](https://github.com/Insality/druid)
- [DefSave](https://github.com/subsoap/defsave)
- [Defold Asset Portal](https://defold.com/assets)