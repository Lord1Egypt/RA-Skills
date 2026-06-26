# Phase 7: Physics System

## Collision Object Types

| Type | Shape | Use |
|------|-------|-----|
| Static | Box/Sphere/Poly | Walls, floors |
| Dynamic | Box/Sphere/Poly | Moving objects |
| Kinematic | Box/Sphere/Poly | Script-controlled |
| Trigger | Box/Sphere/Poly | Detection only |

## Collision Properties

| Property | Type | Use |
|----------|------|-----|
| Type | Enum | Static/Dynamic/Kinematic/Trigger |
| Shape | Enum | Box/Sphere/Poly |
| Friction | float | Surface resistance |
| Restitution | float | Bounciness |
| Mass | float | Dynamic mass (kg) |
| Group | string | Collision group name |
| Mask | table | Groups to collide with |
| Linear Damping | float | Velocity decay |
| Angular Damping | float | Rotation decay |
| Locked Rotation | bool | Prevent rotation |

## Collision Groups

game.project: `physics collision_groups`

```lua
-- Define groups
collision_groups = {
    "player",
    "enemy",
    "bullet",
    "wall",
    "pickup"
}
```

## Collision Filtering

```lua
-- In collision object
Group: "player"
Mask: ["enemy", "bullet", "wall"]

-- Player collides with enemy, bullet, wall
-- Does NOT collide with pickup (trigger needed)
```

## Physics Functions

```lua
physics.get_position(collision_object)
physics.get_velocity(collision_object)
physics.set_velocity(collision_object, velocity)
physics.get_gravity()
physics.set_gravity(gravity)

-- Apply force
physics.apply_force(collision_object, force, [position])

-- Apply impulse (instant velocity change)
physics.apply_impulse(collision_object, impulse, [position])

-- Raycast
physics.raycast(from, to, groups, callback)
physics.raycast_async(from, to, groups, callback)
```

## Velocity Operations

```lua
local vel = physics.get_velocity("#collision")
physics.set_velocity("#collision", vmath.vector3(100, 0, 0))

-- Add velocity
local vel = physics.get_velocity("#collision")
vel.x = vel.x + 50
physics.set_velocity("#collision", vel)
```

## Apply Force/Impulse

```lua
function update(self, dt)
    physics.apply_force("#collision", vmath.vector3(0, 100, 0))
end

function on_input(self, action_id, action)
    if action_id == hash("jump") and action.pressed then
        physics.apply_impulse("#collision", vmath.vector3(0, 500, 0))
    end
end
```

## Collision Response

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("collision_response") then
        local other_id = message.other_id
        local other_group = message.other_group
        local own_group = message.group
        local position = message.position
        local normal = message.normal
        local relative_velocity = message.relative_velocity
        
        if other_group == hash("enemy") then
            self.hp = self.hp - 10
        elseif other_group == hash("pickup") then
            msg.post(other_id, "collect")
        end
    end
end
```

## Collision Response Fields

| Field | Type | Meaning |
|-------|------|---------|
| `other_id` | hash | Colliding GO ID |
| `other_group` | hash | Colliding object's group |
| `group` | hash | Own collision group |
| `position` | vector3 | Collision point |
| `normal` | vector3 | Collision normal |
| `relative_velocity` | vector3 | Velocity difference |

## Trigger Detection

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("trigger_response") then
        if message.enter then
            print("Entered trigger")
        elseif message.exit then
            print("Exited trigger")
        end
    end
end
```

## Contact Point Response

```lua
if message_id == hash("contact_point_response") then
    local normal = message.normal
    local distance = message.distance
    local position = message.position
    
    -- Push out of collision
    local pos = go.get_position()
    pos = pos + normal * distance
    go.set_position(pos)
end
```

## Raycast

```lua
-- Sync raycast (blocks until complete)
physics.raycast(start_pos, end_pos, { "enemy", "wall" }, function(self, hit)
    if hit then
        print(hit.id, hit.position, hit.normal, hit.group)
        msg.post(hit.id, "damage", { amount = 50 })
    end
end)

-- Async raycast
physics.raycast_async(start_pos, end_pos, { "enemy" }, function(self, raycast_id, hit)
    if hit then
        -- Handle hit
    end
end)
```

## Raycast Hit Fields

| Field | Type | Meaning |
|-------|------|---------|
| `id` | hash | Hit GO ID |
| `position` | vector3 | Hit point |
| `normal` | vector3 | Surface normal |
| `group` | hash | Hit collision group |

## Kinematic Movement

```lua
function update(self, dt)
    local pos = go.get_position()
    pos.x = pos.x + self.speed * dt
    
    -- Check collision manually
    local vel = vmath.vector3(self.speed, 0, 0)
    physics.set_velocity("#collision", vel)
    
    -- Or use contact_point_response to slide
end
```

## Dynamic Physics

```lua
-- Falling object
go.property("gravity", -500)

function init(self)
    physics.set_gravity(vmath.vector3(0, self.gravity, 0))
end

function update(self, dt)
    physics.apply_force("#collision", vmath.vector3(0, self.gravity, 0))
end
```

## Sleeping Dynamic Objects

Dynamic objects sleep when stationary. Wake with:

```lua
physics.wake("#collision")
```

## Physics Debug

game.project: `physics debug = 1`

Visualizes collision shapes and contacts.

## 2D Physics Notes

- Z-axis ignored for 2D collision
- Use Box/Sphere shapes for 2D
- Poly shapes: custom convex polygons

## 3D Physics Notes

- Full 3D collision detection
- Use Sphere/Box for 3D
- Capsule shape for characters

## Joint Constraints

Not built-in. Use external library or manual constraint.

## Performance Tips

- Use trigger for detection, not collision_response for non-physics
- Limit collision groups in mask
- Use static for immovable objects
- Sleep distant dynamic objects

## Collision Shape Properties

### Box
```
Width, Height, Depth (for 3D)
```

### Sphere
```
Radius
```

### Poly (Convex)
```
Vertices: { {x,y}, {x,y}, ... }
```

## Common Patterns

### Platformer Physics
```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("contact_point_response") then
        if message.normal.y > 0.7 then
            self.on_ground = true
        end
    end
end
```

### Bullet Collision
```lua
go.property("damage", 10)

function on_message(self, message_id, message, sender)
    if message_id == hash("collision_response") then
        msg.post(message.other_id, "damage", { amount = self.damage })
        go.delete()
    end
end
```

### Trigger Zone
```lua
-- Type: Trigger
-- Group: "zone"
-- Mask: ["player"]

function on_message(self, message_id, message, sender)
    if message_id == hash("trigger_response") then
        if message.enter then
            msg.post(message.other_id, "enter_zone", { zone_id = go.get_id() })
        end
    end
end
```

## Manual Links

- https://defold.com/manuals/physics
- https://defold.com/manuals/physics-objects
- https://defold.com/ref/physics