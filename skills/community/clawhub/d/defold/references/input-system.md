# Phase 9: Input System

## Input Binding

File: `.input_binding`

```yaml
-- game.input_binding
input: {
  LEFT:   { KEY: ["A", "LEFT"] }
  RIGHT:  { KEY: ["D", "RIGHT"] }
  UP:     { KEY: ["W", "UP"] }
  DOWN:   { KEY: ["S", "DOWN"] }
  JUMP:   { KEY: "SPACE" }
  ATTACK: { KEY: ["J", "X"], MOUSE_BUTTON: 1 }
  TOUCH:  { MOUSE_BUTTON: 1, TOUCH: 0 }
  MOVE:   { TOUCH_MULTITOUCH: true }
}
```

## Action Types

| Type | Triggers |
|------|----------|
| `KEY` | Keyboard key press/release |
| `MOUSE_BUTTON` | Mouse button click |
| `MOUSE_MOVEMENT` | Mouse move/scroll |
| `TOUCH` | Touch screen tap |
| `TOUCH_MULTITOUCH` | Multi-touch gesture |
| `GAMEPAD` | Controller button |
| `GAMEPAD_AXIS` | Controller stick |

## Action Properties

| Property | Type | Use |
|----------|------|-----|
| `pressed` | bool | Just pressed |
| `released` | bool | Just released |
| `repeated` | bool | Held down (interval) |
| `value` | float | Analog value (axis/buttons) |
| `x, y` | float | Screen position |
| `dx, dy` | float | Movement delta |
| `screen_x, screen_y` | float | Window position |
| `id` | int | Multi-touch ID |
| `acc_x, acc_y, acc_z` | float | Accelerometer |

## Input Focus

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end

function final(self)
    msg.post(".", "release_input_focus")
end
```

## on_input Callback

```lua
function on_input(self, action_id, action)
    if action_id == hash("JUMP") and action.pressed then
        jump()
    end
    
    if action_id == hash("MOVE") then
        local x = action.x
        local y = action.y
    end
    
    return false  -- Pass to next consumer
end
```

## Input Return Value

| Return | Effect |
|--------|--------|
| `false` | Pass to next focus |
| `true` | Consume, stop propagation |

## Multiple Focus Objects

Objects with focus receive input in order of acquiring. First acquired = first to receive.

```lua
-- Player script
function init(self)
    msg.post(".", "acquire_input_focus")
end

-- GUI script
function init(self)
    msg.post(".", "acquire_input_focus")
end

-- Both receive, order depends on acquire order
```

## Input Priority Pattern

```lua
-- Manager controls priority
function on_message(self, message_id, message, sender)
    if message_id == hash("pause") then
        msg.post("/player", "release_input_focus")
        msg.post("/pause_menu", "acquire_input_focus")
    elseif message_id == hash("resume") then
        msg.post("/pause_menu", "release_input_focus")
        msg.post("/player", "acquire_input_focus")
    end
end
```

## Keyboard Input

```lua
function on_input(self, action_id, action)
    if action_id == hash("LEFT") then
        if action.pressed then
            self.moving_left = true
        elseif action.released then
            self.moving_left = false
        end
    end
    
    -- Or use value for analog keys
    if action_id == hash("MOVE") and action.value > 0.5 then
        move()
    end
end
```

## Movement Pattern

```lua
function update(self, dt)
    local speed = 100
    
    if self.moving_left then
        go.set_position(go.get_position() - vmath.vector3(speed * dt, 0, 0))
    end
    if self.moving_right then
        go.set_position(go.get_position() + vmath.vector3(speed * dt, 0, 0))
    end
end

function on_input(self, action_id, action)
    if action_id == hash("LEFT") then
        self.moving_left = action.pressed or action.repeated
    elseif action_id == hash("RIGHT") then
        self.moving_right = action.pressed or action.repeated
    end
end
```

## Mouse/Touch Input

```lua
function on_input(self, action_id, action)
    if action_id == hash("TOUCH") then
        if action.pressed then
            print("Pressed at", action.x, action.y)
        elseif action.released then
            print("Released")
        end
    end
    
    if action_id == hash("ATTACK") and action.pressed then
        local target = screen_to_world(action.x, action.y)
        attack(target)
    end
end
```

## GUI Input

GUI scripts also use on_input. Use gui.pick_node for detection.

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    if action_id == hash("TOUCH") and action.pressed then
        local button = gui.get_node("button")
        if gui.pick_node(button, action.x, action.y) then
            on_click()
            return true  -- Consume
        end
    end
    return false
end
```

## Scroll/Wheel Input

```lua
function on_input(self, action_id, action)
    if action_id == nil and action.MOUSE_MOVEMENT then
        -- Mouse move
        local dx = action.dx
        local dy = action.dy
        
        -- Scroll wheel
        if action.value > 0 then
            zoom_in()
        elseif action.value < 0 then
            zoom_out()
        end
    end
end
```

## Gamepad Input

```lua
function on_input(self, action_id, action)
    -- Button
    if action_id == hash("A") and action.pressed then
        jump()
    end
    
    -- Axis (sticks)
    if action_id == hash("LEFT_STICK_X") then
        self.move_x = action.value  -- -1 to 1
    end
    if action_id == hash("LEFT_STICK_Y") then
        self.move_y = action.value
    end
end
```

## Multi-Touch

```lua
function on_input(self, action_id, action)
    if action_id == hash("MOVE") then
        for i, touch in ipairs(action.touches) do
            print("Touch", touch.id, "at", touch.x, touch.y)
            print("Phase:", touch.pressed, touch.released)
        end
    end
end
```

## Touch Properties

| Property | Type |
|----------|------|
| `id` | int |
| `x, y` | float |
| `dx, dy` | float |
| `pressed` | bool |
| `released` | bool |
| `tap_count` | int |

## Input Binding File

game.project: `Input: default.input_binding`

```lua
-- default.input_binding
local bindings = {
    { action_id = "jump", triggers = { key = "space" } },
    { action_id = "attack", triggers = { key = "x", mouse_button = 1 } },
}
```

## Dynamic Input Binding

Not built-in. Store mapping in save data:

```lua
function load_bindings()
    local data = sys.load(sys.get_save_file("game", "bindings"))
    -- Apply to config
end
```

## Repeat Rate

game.project: `input repeat_interval = 0.5`

Controls `action.repeated` frequency.

## Text Input

Not built-in. Use Druid input component:

```lua
local input = self.druid:new_input("input_node", function(self, text)
    print("Input:", text)
end)
```

## Screen to World

```lua
function screen_to_world(screen_x, screen_y)
    local camera = go.get_position("/camera")
    local viewport = go.get("/camera#camera", "viewport")
    
    local world_x = camera.x + screen_x - viewport.width/2
    local world_y = camera.y + screen_y - viewport.height/2
    
    return vmath.vector3(world_x, world_y, 0)
end
```

## Input Debug

```lua
function on_input(self, action_id, action)
    pprint(action)
end
```

## Common Patterns

### Tap vs Hold
```lua
function init(self)
    self.hold_timer = 0
    self.is_holding = false
end

function on_input(self, action_id, action)
    if action_id == hash("TOUCH") then
        if action.pressed then
            self.hold_timer = 0
            self.is_holding = true
        elseif action.released then
            if self.hold_timer < 0.5 then
                on_tap(action.x, action.y)
            else
                on_hold_complete()
            end
            self.is_holding = false
        end
    end
end

function update(self, dt)
    if self.is_holding then
        self.hold_timer = self.hold_timer + dt
        if self.hold_timer > 0.5 then
            on_hold_start()
        end
    end
end
```

### Drag Movement
```lua
function init(self)
    self.dragging = false
    self.start_pos = nil
end

function on_input(self, action_id, action)
    if action_id == hash("DRAG") then
        if action.pressed then
            self.dragging = true
            self.start_pos = vmath.vector3(action.x, action.y, 0)
        elseif action.released then
            self.dragging = false
        end
    end
end

function update(self, dt)
    if self.dragging then
        local delta = vmath.vector3(action.dx, action.dy, 0)
        go.set_position(go.get_position() + delta)
    end
end
```

## Manual Links

- https://defold.com/manuals/input
- https://defold.com/manuals/input-binding
- https://defold.com/ref/go (acquire_input_focus)
- https://github.com/Insality/druid (input component)