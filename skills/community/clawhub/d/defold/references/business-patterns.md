# Phase 5: Business Game Patterns

## Architecture

```
main.collection
├── game_manager.go       # State, coins, level
├── customer_manager.go   # Spawn customers
├── shop_system.go        # Shop instances
├── inventory.go          # Stock display
├── upgrade_system.go     # Unlockables
└── ui.go                 # HUD
```

## Game State

```lua
local game_state = {
    coins = 0,
    level = 1,
    unlocked_shops = { "fruit" },
    upgrades = {},
    achievements = {}
}
```

## Game Manager

```lua
function init(self)
    self.coins = defsave.get("game_save", "coins") or 0
    self.level = defsave.get("game_save", "level") or 1
end

function on_message(self, message_id, message, sender)
    if message_id == hash("sale") then
        self.coins = self.coins + message.amount
        update_ui()
        check_level_up()
    elseif message_id == hash("spend") then
        self.coins = self.coins - message.amount
        update_ui()
    end
end

function update_ui()
    msg.post("/ui#gui", "update_coins", { coins = self.coins })
end
```

## Customer Manager

```lua
function init(self)
    self.spawn_timer = 0
    self.spawn_interval = 5
end

function update(self, dt)
    self.spawn_timer = self.spawn_timer + dt
    if self.spawn_timer >= self.spawn_interval then
        local pos = get_spawn_point()
        factory.create("#customer_factory", pos)
        self.spawn_timer = 0
    end
end
```

## Customer Script

```lua
function init(self)
    self.state = "entering"
    self.target_shop = nil
    self.patience = 100
end

function update(self, dt)
    if self.state == "entering" then
        move_to(go.get_position("entrance"))
        if at_target() then self.state = "shopping" end
    elseif self.state == "shopping" then
        if not self.target_shop then
            self.target_shop = random_shop()
        else
            move_to(go.get_position(self.target_shop))
            if at_target() then
                msg.post(self.target_shop, "purchase", { amount = 1 })
                self.state = "paying"
            end
        end
    elseif self.state == "paying" then
        move_to(go.get_position("counter"))
        if at_target() then self.state = "leaving" end
    elseif self.state == "leaving" then
        move_to(go.get_position("exit"))
        if at_target() then go.delete() end
    end
    
    self.patience = self.patience - dt
    if self.patience <= 0 then
        self.state = "leaving"
        msg.post("/game_manager", "customer_left_unhappy")
    end
end
```

## Shop Script

```lua
go.property("shop_type", "fruit")
go.property("max_stock", 50)
go.property("production_rate", 1.0)

function init(self)
    self.stock = 0
    self.price = PRICES[self.shop_type] or 10
end

function update(self, dt)
    if self.stock < self.max_stock then
        self.stock = self.stock + self.production_rate * dt
    end
    update_visuals()
end

function on_message(self, message_id, message, sender)
    if message_id == hash("purchase") then
        if self.stock >= message.amount then
            self.stock = self.stock - message.amount
            local total = message.amount * self.price
            msg.post("/game_manager", "sale", { amount = total })
            msg.post(sender, "purchase_ok", { item = self.shop_type })
        else
            msg.post(sender, "purchase_fail")
        end
    end
end
```

## Upgrade System

```lua
local UPGRADES = {
    fruit_speed = { shop = "fruit", cost = 100, prop = "production_rate", mult = 1.5 },
    fruit_cap = { shop = "fruit", cost = 200, prop = "max_stock", mult = 2 },
    fruit_price = { shop = "fruit", cost = 150, prop = "price", add = 5 }
}

function can_upgrade(upgrade_id)
    local u = UPGRADES[upgrade_id]
    return get_coins() >= u.cost
end

function apply_upgrade(upgrade_id)
    local u = UPGRADES[upgrade_id]
    if not can_upgrade(upgrade_id) then return false end
    
    spend_coins(u.cost)
    
    local shop = get_shop(u.shop)
    if u.mult then
        local current = go.get(shop, u.prop)
        go.set(shop, u.prop, current * u.mult)
    elseif u.add then
        local current = go.get(shop, u.prop)
        go.set(shop, u.prop, current + u.add)
    end
    
    mark_unlocked(upgrade_id)
    return true
end
```

## Shop Unlocking

```lua
local SHOP_UNLOCK = {
    bakery = { cost = 500, level = 3 },
    electronics = { cost = 1000, level = 5 }
}

function can_unlock_shop(shop_type)
    local req = SHOP_UNLOCK[shop_type]
    return get_coins() >= req.cost and get_level() >= req.level
end

function unlock_shop(shop_type)
    if not can_unlock_shop(shop_type) then return false end
    
    local req = SHOP_UNLOCK[shop_type]
    spend_coins(req.cost)
    
    local pos = get_shop_position(shop_type)
    factory.create("#shop_factory", pos, nil, { shop_type = shop_type })
    
    add_unlocked_shop(shop_type)
    return true
end
```

## Level System

```lua
function check_level_up()
    local threshold = self.level * 1000
    if self.coins >= threshold then
        self.level = self.level + 1
        msg.post("/ui#gui", "level_up", { level = self.level })
        show_unlock_notification()
        defsave.set("game_save", "level", self.level)
    end
end
```

## UI HUD

```lua
local druid = require("druid.druid")

function init(self)
    self.druid = druid.new(self)
    self.coins_text = self.druid:new_text("coins", "0")
    self.level_text = self.druid:new_text("level", "Lv.1")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("update_coins") then
        self.coins_text:set_text(format_coins(message.coins))
    elseif message_id == hash("level_up") then
        self.level_text:set_text("Lv." .. message.level)
    end
end

function format_coins(n)
    if n >= 1000000 then return string.format("%.1fM", n/1000000)
    elseif n >= 1000 then return string.format("%.1fK", n/1000)
    else return tostring(n) end
end
```

## Shelf Visuals

```lua
function update_visuals(self)
    local display_count = math.min(self.stock, 10)
    for i = 1, 10 do
        local node = gui.get_node("item_" .. i)
        gui.set_enabled(node, i <= display_count)
    end
end
```

## Input Handling

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        -- Tap shelf to restock
        for _, shelf in ipairs(self.shelves) do
            local node = gui.get_node(shelf.node)
            if gui.pick_node(node, action.x, action.y) then
                msg.post(shelf.id, "restock")
                break
            end
        end
        
        -- Tap customer to serve
        for _, customer in ipairs(self.customers) do
            local node = gui.get_node(customer.node)
            if gui.pick_node(node, action.x, action.y) then
                msg.post(customer.id, "serve")
                break
            end
        end
    end
end
```

## Recommended Libraries

| Library | Install | Use |
|---------|---------|-----|
| Druid | `https://github.com/Insality/druid/archive/1.2.2.zip` | UI |
| DefSave | `https://github.com/subsoap/defsave/archive/v1.2.6.zip` | Save |
| Monarch | `https://github.com/insality/defold-monarch/archive/1.0.zip` | Screens |
| A* | `https://github.com/defold/a-star/archive/1.0.zip` | Pathfinding |

## Performance Tips

- Atlas all sprites
- Limit spawned customers (pool pattern)
- Cache data in memory, don't read every frame
- Use message-driven, avoid polling in update()

## Manual Links

- https://defold.com/manuals/gui
- https://github.com/Insality/druid
- https://github.com/subsoap/defsave