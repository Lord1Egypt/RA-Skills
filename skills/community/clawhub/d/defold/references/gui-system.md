# Phase 2: GUI System

## GUI Component

| Property | Type | Use |
|----------|------|-----|
| Script | `.gui_script` | Logic |
| Material | Material | Rendering |
| Adjust Reference | Enum | Layout mode |
| Max Nodes | int | Node limit |

GUI renders in screen space, independent of camera.

## Node Types

| Type | Use | Key Properties |
|------|-----|----------------|
| Box | Panels, buttons | Texture, color, size |
| Text | Labels | Font, text, line_break |
| Pie | Circular progress | Perimeter, inner_radius |
| Template | Reusable UI | Gui file reference |
| ParticleFX | Effects | Particle file |

## Node Properties

| Property | Type | API |
|----------|------|-----|
| Position | vector3 | `gui.set_position(node, pos)` |
| Size | vector3 | `gui.set_size(node, size)` |
| Scale | vector3 | `gui.set_scale(node, scale)` |
| Rotation | quat | `gui.set_rotation(node, rot)` |
| Color | vector4 | `gui.set_color(node, color)` |
| Alpha | float | `gui.set_alpha(node, alpha)` |
| Visible | bool | `gui.set_visible(node, bool)` |
| Enabled | bool | `gui.set_enabled(node, bool)` |
| Pivot | enum | `gui.set_pivot(node, pivot)` |

## Pivot Values

| Pivot | Anchor Point |
|-------|--------------|
| `PIVOT_CENTER` | Center |
| `PIVOT_N` | Top center |
| `PIVOT_S` | Bottom center |
| `PIVOT_E` | Right center |
| `PIVOT_W` | Left center |
| `PIVOT_NE` | Top right |
| `PIVOT_NW` | Top left |
| `PIVOT_SE` | Bottom right |
| `PIVOT_SW` | Bottom left |

## Anchor Modes

| Anchor | Effect |
|--------|--------|
| `None` | Relative to center |
| `Left/Right` | Fixed to edge |
| `Top/Bottom` | Fixed to edge |

## Adjust Modes

| Mode | Scaling |
|------|---------|
| `Fit` | Fit within bounds (min scale) |
| `Zoom` | Cover bounds (max scale) |
| `Stretch` | Fill bounds |

## Blend Modes

| Mode | Use |
|------|-----|
| `Alpha` | Normal |
| `Add` | Glow |
| `Multiply` | Darken |
| `Screen` | Lighten |

## Node Operations

```lua
local node = gui.get_node("button")
gui.set_text(node, "Click")
gui.set_color(node, vmath.vector4(1, 0, 0, 1))
gui.set_enabled(node, false)

local clone = gui.clone(node)
local nodes = gui.clone_tree(node)
gui.delete_node(node)
```

## Dynamic Node Creation

```lua
local box = gui.new_box_node(vmath.vector3(100, 100, 0), vmath.vector3(50, 50, 0))
gui.set_color(box, vmath.vector4(0.5, 0.5, 0.5, 1))

local text = gui.new_text_node(vmath.vector3(100, 100, 0), "Hello")
gui.set_font(text, "main_font")
gui.set_size(text, vmath.vector3(200, 50, 0))
```

## GUI Animation

```lua
gui.animate(node, "position.x", 100, gui.EASING_LINEAR, 1.0)
gui.animate(node, "color", vmath.vector4(1, 0, 0, 1), gui.EASING_INQUAD, 0.5)
gui.animate(node, "scale", vmath.vector3(2, 2, 1), gui.EASING_OUTELASTIC, 0.3, 0, function()
    print("Done")
end)
```

## Easing

| Constant | Curve |
|----------|-------|
| `EASING_LINEAR` | Linear |
| `EASING_INQUAD` | Accelerate |
| `EASING_OUTQUAD` | Decelerate |
| `EASING_INOUTQUAD` | Smooth |
| `EASING_OUTELASTIC` | Elastic bounce |

## Input Handling

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local node = gui.get_node("button")
        if gui.pick_node(node, action.x, action.y) then
            print("Clicked")
        end
    end
end
```

## Action Properties

| Property | Type | Use |
|----------|------|-----|
| `pressed` | bool | Just pressed |
| `released` | bool | Just released |
| `repeated` | bool | Held down |
| `value` | float | Analog value |
| `x, y` | float | Position |
| `dx, dy` | float | Delta movement |

## Layouts

```lua
gui.get_layouts()
gui.set_layout("Portrait")

function on_message(self, message_id, message, sender)
    if message_id == hash("layout_changed") then
        if message.id == hash("Portrait") then
            -- Handle portrait
        end
    end
end
```

## Templates

```lua
local button = gui.get_node("template_id/button")
gui.set_text(gui.get_node("template_id/label"), "Buy")
```

Template nodes prefixed with `template_id/node_id`.

## Clipping

```lua
gui.set_clipping_mode(node, gui.CLIPPING_MODE_STENCIL)
gui.set_clipping_visible(node, true)
gui.set_clipping_inverted(node, false)
```

## Draw Order

Nodes render by outline order (top first). Use `gui.move_above()`, `gui.move_below()` to reorder.

```lua
gui.get_index(node)
gui.move_above(node, reference_node)
gui.move_below(node, reference_node)
```

## Layers

Optimize draw calls by grouping nodes with same atlas/blend mode.

## Druid Framework

Install: `https://github.com/Insality/druid/archive/refs/tags/1.2.2.zip`

```lua
local druid = require("druid.druid")

function init(self)
    self.druid = druid.new(self)
    self.btn = self.druid:new_button("btn_node", function()
        print("Clicked")
    end)
    self.text = self.druid:new_text("text_node", "Hello")
    self.progress = self.druid:new_progress("bar_node", "x")
end

function update(self, dt)
    self.druid:update(dt)
end

function on_input(self, action_id, action)
    return self.druid:on_input(action_id, action)
end

function on_message(self, message_id, message, sender)
    self.druid:on_message(message_id, message, sender)
end
```

## Druid Components

| Component | Create | Use |
|-----------|--------|-----|
| Button | `new_button(node, callback)` | Click handling |
| Text | `new_text(node, text)` | Text display |
| Progress | `new_progress(node, "x")` | Progress bar |
| Slider | `new_slider(node, "x")` | Slider control |
| Scroll | `new_scroll(view, content)` | Scroll view |
| Grid | `new_static_grid(node)` | Grid layout |
| Checkbox | `new_checkbox(node, callback)` | Checkbox |
| Input | `new_input(node, callback)` | Text input |
| Drag | `new_drag(node)` | Drag handling |

## Druid Button Events

```lua
local btn = self.druid:new_button("btn", on_click)
btn.on_long_click:subscribe(function() print("Long") end)
btn.on_double_click:subscribe(function() print("Double") end)
btn.on_pressed:subscribe(function() print("Down") end)
```

## Druid Progress

```lua
local progress = self.druid:new_progress("bar", "x")
progress:to(0.75)
progress:set_steps({0, 0.25, 0.5, 0.75, 1.0})
```

## Druid Scroll

```lua
local scroll = self.druid:new_scroll("view", "content")
scroll:scroll_to(vmath.vector3(0, 100, 0))
scroll:scroll_to_percent(0.5)
```

## Manual Links

- https://defold.com/manuals/gui
- https://defold.com/manuals/gui-script
- https://defold.com/manuals/gui-box
- https://defold.com/manuals/gui-text
- https://defold.com/manuals/gui-layouts
- https://github.com/Insality/druid