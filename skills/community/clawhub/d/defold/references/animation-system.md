# Phase 8: Animation System

## Flipbook Animation

Animated sprite using atlas with animation frames.

### Atlas Setup

| Property | Value |
|----------|-------|
| Images | Animation frames |
| Animations | Named sequences |
| Fps | Frames per second |
| Play Mode | Once/Loop |

### Animation Definition

```lua
-- In atlas file
animations = {
    idle = { start = 0, end = 4, fps = 10 },
    walk = { start = 5, end = 12, fps = 15 },
    attack = { start = 13, end = 20, fps = 20, mode = "once" }
}
```

### Play Flipbook

```lua
sprite.play_flipbook("#sprite", hash("idle"))
sprite.play_flipbook("#sprite", "walk")

-- With callback
sprite.play_flipbook("#sprite", "attack", function(self, sprite_id, animation_id)
    print("Attack complete")
    sprite.play_flipbook("#sprite", "idle")
end)
```

## Sprite Flipbook API

```lua
sprite.play_flipbook(url, animation_id, [callback])
sprite.set_flipbook(url, animation_id)
sprite.get_flipbook(url)
```

## Flipbook Properties

| Property | API |
|----------|-----|
| Animation | `sprite.play_flipbook()` |
| Current frame | Internal only |
| Scale | `go.set_scale()` |

## State Machine Pattern

```lua
function init(self)
    self.state = "idle"
    sprite.play_flipbook("#sprite", "idle")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("move") then
        if self.state ~= "walk" then
            self.state = "walk"
            sprite.play_flipbook("#sprite", "walk")
        end
    elseif message_id == hash("stop") then
        self.state = "idle"
        sprite.play_flipbook("#sprite", "idle")
    elseif message_id == hash("attack") then
        self.state = "attack"
        sprite.play_flipbook("#sprite", "attack", function()
            self.state = "idle"
            sprite.play_flipbook("#sprite", "idle")
        end)
    end
end
```

## Property Animation

Animate any GO property using go.animate().

```lua
go.animate(id, property, playback, to, easing, duration, [delay], [callback])

go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, 100, go.EASING_OUTQUAD, 1.0)
go.animate("#", "scale", go.PLAYBACK_LOOP_PINGPONG, 2.0, go.EASING_LINEAR, 0.5)
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

| Constant | Curve |
|----------|-------|
| `EASING_LINEAR` | Linear |
| `EASING_INQUAD` | Quad accelerate |
| `EASING_OUTQUAD` | Quad decelerate |
| `EASING_INOUTQUAD` | Quad smooth |
| `EASING_INCUBIC` | Cubic accelerate |
| `EASING_OUTCUBIC` | Cubic decelerate |
| `EASING_INOUTCUBIC` | Cubic smooth |
| `EASING_INELASTIC` | Elastic start |
| `EASING_OUTELASTIC` | Elastic end |
| `EASING_INOUTELASTIC` | Elastic both |
| `EASING_INBACK` | Anticipate |
| `EASING_OUTBACK` | Overshoot |
| `EASING_INOUTBACK` | Both |
| `EASING_INBOUNCE` | Bounce start |
| `EASING_OUTBOUNCE` | Bounce end |
| `EASING_INOUTBOUNCE` | Bounce both |

## Animate Position

```lua
go.animate(".", "position", go.PLAYBACK_ONCE_FORWARD, vmath.vector3(100, 50, 0), go.EASING_LINEAR, 1.0)

go.animate(".", "position.x", go.PLAYBACK_ONCE_FORWARD, 100, go.EASING_OUTQUAD, 0.5)
go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, 50, go.EASING_OUTQUAD, 0.5)
```

## Animate Rotation

```lua
go.animate(".", "rotation", go.PLAYBACK_ONCE_FORWARD, vmath.quat_rotation_z(math.pi), go.EASING_LINEAR, 1.0)

-- Rotate around axis
go.animate(".", "euler.z", go.PLAYBACK_LOOP_FORWARD, 360, go.EASING_LINEAR, 2.0)
```

## Animate Scale

```lua
go.animate(".", "scale", go.PLAYBACK_ONCE_FORWARD, vmath.vector3(2, 2, 1), go.EASING_OUTELASTIC, 0.5)

-- Uniform scale
go.animate(".", "scale", go.PLAYBACK_ONCE_PINGPONG, 1.5, go.EASING_INOUTQUAD, 0.3)
```

## Animate Properties

```lua
go.property("opacity", 1.0)

go.animate("#", "opacity", go.PLAYBACK_ONCE_FORWARD, 0, go.EASING_LINEAR, 1.0, function()
    go.delete()
end)
```

## Cancel Animation

```lua
go.cancel_animations(id, [property])

go.cancel_animations(".")  -- All animations
go.cancel_animations(".", "position.x")  -- Specific property
```

## Animation Completion

```lua
go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, 100, go.EASING_LINEAR, 1.0, 0, function(self, id, property)
    print("Animation done")
    msg.post("manager", "jump_complete")
end)
```

## Spine Animation

Spine skeletal animation support (2D).

### Setup

1. Import `.skel` file (Spine JSON/binary)
2. Add Model component
3. Set Spine model resource

### Spine API

```lua
spine.play_anim(url, animation_id, [playback], [blend_duration], [callback])

spine.play_anim("#model", "walk", go.PLAYBACK_LOOP_FORWARD)
spine.play_anim("#model", "jump", go.PLAYBACK_ONCE_FORWARD, 0.2, function()
    spine.play_anim("#model", "idle")
end)
```

## Spine Playback

| Mode | Use |
|------|-----|
| `PLAYBACK_ONCE_FORWARD` | Single animation |
| `PLAYBACK_LOOP_FORWARD` | Looping animation |

## Spine Properties

```lua
spine.set_skin(url, skin_id)
spine.set_anim_time_ratio(url, ratio)
spine.get_anim_time_ratio(url)
spine.get_anim(url)
```

## Spine Mixing

```lua
spine.play_anim("#model", "walk", go.PLAYBACK_LOOP_FORWARD)
spine.play_anim("#model", "attack", go.PLAYBACK_ONCE_FORWARD, 0.2)
-- Blends 0.2 seconds from walk to attack
```

## GUI Animation

See Phase 2. Summary:

```lua
gui.animate(node, "position.x", 100, gui.EASING_LINEAR, 1.0)
gui.animate(node, "color", vmath.vector4(0, 0, 0, 1), gui.EASING_INQUAD, 0.5)
gui.cancel_animation(node, "position.x")
```

## Particle FX

Particle effects animation.

```lua
particlefx.play(url, [emitter_id], [callback])
particlefx.stop(url, [emitter_id])

particlefx.play("#particles")
particlefx.play("#particles", hash("smoke"), function()
    print("Particles done")
end)
```

## Complex Animation Pattern

```lua
function play_sequence(animations)
    local i = 1
    
    local function play_next()
        if i > #animations then return end
        
        local anim = animations[i]
        i = i + 1
        
        sprite.play_flipbook("#sprite", anim, function()
            play_next()
        end)
    end
    
    play_next()
end

play_sequence({ "ready", "attack", "recover", "idle" })
```

## Directional Animation

```lua
function update(self, dt)
    local vel = physics.get_velocity("#collision")
    
    if vel.x > 0 then
        sprite.set_hflip("#sprite", true)
    elseif vel.x < 0 then
        sprite.set_hflip("#sprite", false)
    end
    
    if vmath.length(vel) > 0.1 then
        sprite.play_flipbook("#sprite", "walk")
    else
        sprite.play_flipbook("#sprite", "idle")
    end
end
```

## Manual Links

- https://defold.com/manuals/sprite
- https://defold.com/manuals/animation
- https://defold.com/manuals/spine
- https://defold.com/manuals/particlefx
- https://defold.com/ref/sprite
- https://defold.com/ref/spine