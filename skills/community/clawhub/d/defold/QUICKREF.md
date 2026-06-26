# Defold Quick Reference

## Core API

### Message Passing
```lua
msg.post(receiver, message_id, [message])
function on_message(self, message_id, message, sender)
```

### Game Object
```lua
go.get_id()
go.get/set_position(id)
go.get/set_rotation(id)
go.get/set_scale(id)
go.delete(id)
go.animate(id, prop, playback, to, easing, duration)
```

### Physics
```lua
physics.get/set_velocity("#collision")
physics.apply_force("#collision", force)
physics.apply_impulse("#collision", impulse)
physics.raycast(from, to, groups, callback)
```

### Animation
```lua
sprite.play_flipbook("#sprite", anim_id, [callback])
go.animate(".", "position.y", playback, to, easing, duration)
```

### Input
```lua
msg.post(".", "acquire_input_focus")
function on_input(self, action_id, action)
```

### GUI
```lua
gui.get_node("id")
gui.set_text/color/position/size(node, value)
gui.animate(node, prop, to, easing, duration)
gui.pick_node(node, x, y)
```

### Druid
```lua
self.druid = druid.new(self)
self.druid:new_button(node, callback)
self.druid:new_text(node, text)
self.druid:new_progress(node, "x")
```

### Factory
```lua
factory.create("#factory", pos, nil, { prop = value })
collectionfactory.create("#factory")
msg.post("#proxy", "load") -- then init, enable
```

### Save
```lua
defsave.load/save/set/get("file", key, value)
sys.save/load(path)
```

## Addressing

| Symbol | Meaning |
|--------|---------|
| `.` | Current GO |
| `#` | Current script |
| `#id` | Component |
| `name` | GO in collection |
| `/path` | Absolute path |

## Playback Modes

| Mode | Use |
|------|-----|
| `PLAYBACK_ONCE_FORWARD` | Single play |
| `PLAYBACK_LOOP_FORWARD` | Loop |
| `PLAYBACK_LOOP_PINGPONG` | Back-and-forth |

## Collision Types

| Type | Use |
|------|-----|
| Static | Walls, floors |
| Dynamic | Physics objects |
| Kinematic | Script-controlled |
| Trigger | Detection only |

## Node Types

| Type | Use |
|------|-----|
| Box | Buttons, panels |
| Text | Labels |
| Pie | Circular progress |
| Template | Reusable UI |