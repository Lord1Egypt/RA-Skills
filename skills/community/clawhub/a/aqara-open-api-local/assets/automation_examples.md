# Automation JSON Configuration Examples

This document shows complete conversion examples from natural language to JSON configuration, covering a variety of common scenarios.

---

## Example 1: Turn On the Light When the Switch Turns On

**User Input**: "Turn on the LED light bulb when the switch turns on"

**Analysis**:
- Trigger: the switch `OnOff` trait becomes `true`
- Action: set the light bulb `OnOff` trait to `true`
- Device matching: "switch" -> `lumi.4cf8cdf3c7b3c26` endpoint 2 (Switch 1); "LED light bulb" -> `lumi.158d0002c660dc` endpoint 2

```json
{
    "metadata": {
        "name": "Switch-Controlled Lighting",
        "description": "Automatically turn on the light when the switch turns on"
    },
    "automations": [
        {
            "name": "Switch Turns On Light",
            "starters": [
                {
                    "type": "property.event",
                    "source": {
                        "type": "device.property",
                        "deviceId": "lumi.4cf8cdf3c7b3c26",
                        "endpointId": 2,
                        "functionCode": "Output",
                        "traitCode": "OnOff"
                    },
                    "is": true
                }
            ],
            "actions": [
                {
                    "type": "device.trait.write",
                    "functionCode": "Output",
                    "traitCode": "OnOff",
                    "targets": [
                        { "deviceId": "lumi.158d0002c660dc", "endpointIds": [2] }
                    ],
                    "value": true
                }
            ]
        }
    ]
}
```

---

## Example 2: Switch Linkage (Complementary Scenarios Split Automatically)

**User Input**: "Turn on the light when the switch turns on, and turn it off when the switch turns off"

**Analysis**: This needs to be split into two automations, one for `on` and one for `off`.

```json
{
    "metadata": {
        "name": "Switch-Linked Light Bulb",
        "description": "Turn the light on when the switch turns on, and off when the switch turns off"
    },
    "automations": [
        {
            "name": "Turn On Light When Switch Turns On",
            "starters": [
                {
                    "type": "property.event",
                    "source": {
                        "type": "device.property",
                        "deviceId": "lumi.4cf8cdf3c7b3c26",
                        "endpointId": 2,
                        "functionCode": "Output",
                        "traitCode": "OnOff"
                    },
                    "is": true
                }
            ],
            "actions": [
                {
                    "type": "device.trait.write",
                    "functionCode": "Output",
                    "traitCode": "OnOff",
                    "targets": [
                        { "deviceId": "lumi.158d0002c660dc", "endpointIds": [2] }
                    ],
                    "value": true
                }
            ]
        },
        {
            "name": "Turn Off Light When Switch Turns Off",
            "starters": [
                {
                    "type": "property.event",
                    "source": {
                        "type": "device.property",
                        "deviceId": "lumi.4cf8cdf3c7b3c26",
                        "endpointId": 2,
                        "functionCode": "Output",
                        "traitCode": "OnOff"
                    },
                    "is": false
                }
            ],
            "actions": [
                {
                    "type": "device.trait.write",
                    "functionCode": "Output",
                    "traitCode": "OnOff",
                    "targets": [
                        { "deviceId": "lumi.158d0002c660dc", "endpointIds": [2] }
                    ],
                    "value": false
                }
            ]
        }
    ]
}
```

---

## Example 3: Button Event Trigger (Event Type)

**User Input**: "Turn on the light bulb when the Z1 Pro button is double-pressed"

**Analysis**:
- Trigger: `ButtonEvent`, `is: "1"` (double press)
- Device matching: Z1 Pro -> `virtual.99426645927213` endpoint 2, `ButtonEvent`, `valueType=event`

```json
{
    "metadata": {
        "name": "Double Press Turns On Light",
        "description": "Turn on the light bulb when the Z1 Pro button is double-pressed"
    },
    "automations": [
        {
            "name": "Double Press Turns On Light",
            "starters": [
                {
                    "type": "property.event",
                    "source": {
                        "type": "device.property",
                        "deviceId": "virtual.99426645927213",
                        "endpointId": 2,
                        "functionCode": "Button",
                        "traitCode": "ButtonEvent"
                    },
                    "is": "0"
                }
            ],
            "actions": [
                {
                    "type": "device.trait.write",
                    "functionCode": "Output",
                    "traitCode": "OnOff",
                    "targets": [
                        { "deviceId": "lumi.158d0002c660dc", "endpointIds": [2] }
                    ],
                    "value": true
                }
            ]
        }
    ]
}
```

> Note: The `enumRange` of Z1 Pro `ButtonEvent` only contains `{"value":"0","key":"Single Press"}`, so only the single-press event is supported. If a device's `ButtonEvent` also contains `0=Single Press, 1=Double Press, 2=Long Press`, then single press, double press, and long press can be distinguished.

---

## Example 4: Scheduled + Conditional Trigger

**User Input**: "Every day at 10 PM, if the door/window is closed, turn off all lights and switches"

**Analysis**:
- Trigger: scheduled time `22:00`
- Condition: door/window sensor `ContactSensorState = false`
- Action: turn off all `Light` and `Switch` devices

```json
{
    "metadata": {
        "name": "Nightly Auto Shutdown",
        "description": "Every day at 10 PM, turn off all lights and switches if the door/window is closed"
    },
    "automations": [
        {
            "name": "Scheduled All-Off",
            "starters": [
                {
                    "type": "time.schedule",
                    "at": "22:00",
                    "timezone": "Asia/Shanghai"
                }
            ],
            "condition": {
                "type": "property.state",
                "source": {
                    "type": "device.property",
                    "deviceId": "matt.519d1fb013d1688ca9a4a000",
                    "endpointId": 2,
                    "functionCode": "Contact",
                    "traitCode": "ContactSensorState"
                },
                "is": false
            },
            "actions": [
                {
                    "type": "device.trait.write",
                    "functionCode": "Output",
                    "traitCode": "OnOff",
                    "targets": [
                        { "deviceId": "lumi.158d0002c660dc", "endpointIds": [2] },
                        { "deviceId": "lumi.4cf8cdf3c7b3c26", "endpointIds": [2, 3, 4] },
                        { "deviceId": "virtual.99426645927213", "endpointIds": [2] },
                        { "deviceId": "matt.519d1fb01378a56387aea000", "endpointIds": [2] }
                    ],
                    "value": false
                }
            ]
        }
    ]
}
```

---

## Example 5: Door/Window Left Open Reminder

**User Input**: "Flash a light as a reminder when the door/window has been open for more than 5 minutes"

**Analysis**:
- Trigger: `ContactSensorState = true` for 5 minutes (`for`)
- Action: light off -> wait 1 second -> light on (simulate a flash)

```json
{
    "metadata": {
        "name": "Door/Window Left Open Reminder",
        "description": "Flash a light when the door/window has been open for more than 5 minutes"
    },
    "automations": [
        {
            "name": "Door/Window Open Reminder",
            "starters": [
                {
                    "type": "property.event",
                    "source": {
                        "type": "device.property",
                        "deviceId": "matt.519d1fb013d1688ca9a4a000",
                        "endpointId": 2,
                        "functionCode": "Contact",
                        "traitCode": "ContactSensorState"
                    },
                    "is": true,
                    "for": "5min"
                }
            ],
            "actions": [
                {
                    "type": "device.trait.write",
                    "functionCode": "Output",
                    "traitCode": "OnOff",
                    "targets": [{ "deviceId": "lumi.158d0002c660dc", "endpointIds": [2] }],
                    "value": false
                },
                { "type": "delay", "for": "1sec" },
                {
                    "type": "device.trait.write",
                    "functionCode": "Output",
                    "traitCode": "OnOff",
                    "targets": [{ "deviceId": "lumi.158d0002c660dc", "endpointIds": [2] }],
                    "value": true
                }
            ]
        }
    ]
}
```

---

## Example 6: Automation With Compound Conditions

**User Input**: "When the switch turns on, if the door/window is closed and it is between 5 PM and 11 PM, turn on the light"

**Analysis**:
- Trigger: switch `OnOff = true`
- Condition: `AND` (door/window closed + time range `17:00-23:00`)
- Action: turn on the light

```json
{
    "metadata": {
        "name": "Conditional Smart Automation",
        "description": "When the switch turns on, only turn on the light if the door/window is closed and the time is within the specified range"
    },
    "automations": [
        {
            "name": "Conditional Light-On Automation",
            "starters": [
                {
                    "type": "property.event",
                    "source": {
                        "type": "device.property",
                        "deviceId": "matt.519d1fb01378a56387aea000",
                        "endpointId": 2,
                        "functionCode": "Output",
                        "traitCode": "OnOff"
                    },
                    "is": true
                }
            ],
            "condition": {
                "type": "and",
                "conditions": [
                    {
                        "type": "property.state",
                        "source": {
                            "type": "device.property",
                            "deviceId": "matt.519d1fb013d1688ca9a4a000",
                            "endpointId": 2,
                            "functionCode": "Contact",
                            "traitCode": "ContactSensorState"
                        },
                        "is": false
                    },
                    {
                        "type": "time.between",
                        "after": "17:00",
                        "before": "23:00"
                    }
                ]
            },
            "actions": [
                {
                    "type": "device.trait.write",
                    "functionCode": "Output",
                    "traitCode": "OnOff",
                    "targets": [
                        { "deviceId": "lumi.158d0002c660dc", "endpointIds": [2] }
                    ],
                    "value": true
                }
            ]
        }
    ]
}
```

---

## Example 7: Using a Scope Variable + Multiple References

**User Input**: "When the light bulb brightness changes and is greater than 30%, if the brightness is also greater than 50%, set the color temperature to 300"

**Analysis**: The light bulb brightness is used in both the starter and the condition, so use `scope`.

```json
{
    "metadata": {
        "name": "Brightness-Driven Color Temperature",
        "description": "Adjust color temperature when brightness exceeds the threshold",
        "scope": [
            {
                "name": "brightness",
                "type": "device.property",
                "deviceId": "lumi.158d0002c660dc",
                "endpointId": 2,
                "functionCode": "LevelControl",
                "traitCode": "CurrentLevel"
            }
        ]
    },
    "automations": [
        {
            "name": "Brightness-Driven Color Temperature",
            "starters": [
                {
                    "type": "property.event",
                    "source": {
                        "type": "data.ref",
                        "select": { "by": "name", "value": "brightness" }
                    },
                    "greaterThan": 30
                }
            ],
            "condition": {
                "type": "property.state",
                "source": {
                    "type": "data.ref",
                    "select": { "by": "name", "value": "brightness" }
                },
                "greaterThan": 50
            },
            "actions": [
                {
                    "type": "device.trait.write",
                    "functionCode": "ColorControl",
                    "traitCode": "ColorTemperature",
                    "targets": [
                        { "deviceId": "lumi.158d0002c660dc", "endpointIds": [2] }
                    ],
                    "value": 300
                }
            ]
        }
    ]
}
```

---

## Example 8: Manual Trigger + Delay + Batch Control

**User Input**: "Create an away mode that manually turns off all lights and switches"

```json
{
    "metadata": {
        "name": "One-Tap Away Mode",
        "description": "Manually trigger turning off all lights and switches"
    },
    "automations": [
        {
            "name": "Away Mode Turns Everything Off",
            "starters": [
                { "type": "manual", "name": "Away Mode" }
            ],
            "actions": [
                {
                    "type": "device.trait.write",
                    "functionCode": "Output",
                    "traitCode": "OnOff",
                    "targets": [
                        { "deviceId": "lumi.158d0002c660dc", "endpointIds": [2] }
                    ],
                    "value": false
                },
                { "type": "delay", "for": "1sec" },
                {
                    "type": "device.trait.write",
                    "functionCode": "Output",
                    "traitCode": "OnOff",
                    "targets": [
                        { "deviceId": "lumi.4cf8cdf3c7b3c26", "endpointIds": [2, 3, 4] },
                        { "deviceId": "virtual.99426645927213", "endpointIds": [2] },
                        { "deviceId": "matt.519d1fb01378a56387aea000", "endpointIds": [2] }
                    ],
                    "value": false
                }
            ]
        }
    ]
}
```

---

## Example 9: Power Overload Protection

**User Input**: "When the power of Z1 Pro exceeds 2000W, automatically turn it off"

```json
{
    "metadata": {
        "name": "Power Overload Protection",
        "description": "Automatically turn off the switch when power exceeds 2000W"
    },
    "automations": [
        {
            "name": "Turn Off On Power Overload",
            "starters": [
                {
                    "type": "property.event",
                    "source": {
                        "type": "device.property",
                        "deviceId": "virtual.99426645927213",
                        "endpointId": 1,
                        "functionCode": "EnergyManagement",
                        "traitCode": "CurrentPower"
                    },
                    "greaterThan": 2000
                }
            ],
            "actions": [
                {
                    "type": "device.trait.write",
                    "functionCode": "Output",
                    "traitCode": "OnOff",
                    "targets": [
                        { "deviceId": "virtual.99426645927213", "endpointIds": [2] }
                    ],
                    "value": false
                }
            ]
        }
    ]
}
```

---

## Example 10: Sunset Trigger + Dimming + Color Temperature (Night Mode)

**User Input**: "Turn on the light automatically 30 minutes after sunset, brightness 30%, warm color temperature"

```json
{
    "metadata": {
        "name": "Sunset Night Light Mode",
        "description": "Turn on the light 30 minutes after sunset and adjust it to night light mode"
    },
    "automations": [
        {
            "name": "Sunset Night Light",
            "starters": [
                {
                    "type": "time.schedule",
                    "at": "sunset+30min",
                    "timezone": "Asia/Shanghai"
                }
            ],
            "actions": [
                {
                    "type": "device.trait.write",
                    "functionCode": "Output",
                    "traitCode": "OnOff",
                    "targets": [{ "deviceId": "lumi.158d0002c660dc", "endpointIds": [2] }],
                    "value": true
                },
                {
                    "type": "device.trait.write",
                    "functionCode": "LevelControl",
                    "traitCode": "CurrentLevel",
                    "targets": [{ "deviceId": "lumi.158d0002c660dc", "endpointIds": [2] }],
                    "value": 30
                },
                {
                    "type": "device.trait.write",
                    "functionCode": "ColorControl",
                    "traitCode": "ColorTemperature",
                    "targets": [{ "deviceId": "lumi.158d0002c660dc", "endpointIds": [2] }],
                    "value": 370
                }
            ]
        }
    ]
}
```

> Note: A color temperature of `370` mired is approximately `2700K` (warm), and `153` mired is approximately `6500K` (cool). The range is `153-370` (from `valueRange`).
