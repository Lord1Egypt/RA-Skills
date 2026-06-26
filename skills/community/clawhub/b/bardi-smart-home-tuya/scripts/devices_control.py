#!/usr/bin/env python3
"""Tuya/Bardi Smart Device Controller via Cloud API.

Controls any Tuya smart device — lights, plugs, sensors, meters, and more.
Includes Bardi-specific features: color presets, brightness preservation, HSV control.

Usage:
    python3 devices_control.py <device_id> <command> [args...]
    python3 devices_control.py discover

Environment Variables:
    TUYA_ACCESS_ID      — Cloud project access ID
    TUYA_ACCESS_SECRET  — Cloud project access secret
    TUYA_API_REGION     — Region code: sg, cn, us, eu, in (default: sg)
"""

import json
import os
import sys
import time
import tinytuya

# Color presets: name -> (hue, saturation, value)
COLOR_PRESETS = {
    "red":    (0, 1000, 1000),
    "orange": (30, 1000, 1000),
    "yellow": (60, 1000, 1000),
    "green":  (120, 1000, 1000),
    "cyan":   (180, 1000, 1000),
    "blue":   (240, 1000, 1000),
    "purple": (280, 1000, 1000),
    "mauve":  (300, 350, 1000),
    "pink":   (330, 1000, 1000),
    "warm":   (30, 300, 1000),
    "cool":   (210, 300, 1000),
}


class DeviceController:
    """Tuya cloud device controller with Bardi smart bulb support."""

    def __init__(self):
        access_id = os.environ.get("TUYA_ACCESS_ID")
        access_secret = os.environ.get("TUYA_ACCESS_SECRET")
        region = os.environ.get("TUYA_API_REGION", "sg")

        if not access_id or not access_secret:
            print("ERROR: Missing Tuya credentials.")
            print("Set TUYA_ACCESS_ID and TUYA_ACCESS_SECRET in environment.")
            sys.exit(1)

        self.cloud = tinytuya.Cloud(
            apiRegion=region,
            apiKey=access_id,
            apiSecret=access_secret
        )

    # ─── Core Methods ───

    def discover(self):
        """List all devices in the account."""
        return self.cloud.getdevices()

    def status(self, device_id):
        """Get device status."""
        return self.cloud.getstatus(device_id)

    def detail(self, device_id):
        """Get full device detail."""
        return self.cloud.getdevicedetail(device_id)

    def model(self, device_id):
        """Get device Thing Model (supported DPs)."""
        return self.cloud.getdps(device_id)

    def send(self, device_id, commands):
        """Send commands to device."""
        start = time.time()
        result = self.cloud.sendcommand(device_id, {"commands": commands})
        elapsed = time.time() - start
        return result, elapsed

    # ─── Switch Control ───

    def _get_switch_code(self, device_id):
        """Return correct switch property based on device type."""
        if device_id == "a343f3ea1a921b3df2qanr":
            return "switch"
        return "switch_led"

    def on(self, device_id, switch_code=None):
        """Turn device on."""
        code = switch_code or self._get_switch_code(device_id)
        return self.send(device_id, [{"code": code, "value": True}])

    def off(self, device_id, switch_code=None):
        """Turn device off."""
        code = switch_code or self._get_switch_code(device_id)
        return self.send(device_id, [{"code": code, "value": False}])

    # ─── Light Control ───

    def white(self, device_id, temp=None, brightness=None):
        """Set white mode with optional temperature (0-1000) and brightness (1-100%)."""
        cmds = [{"code": "work_mode", "value": "white"}]
        if temp is not None:
            cmds.append({"code": "temp_value", "value": max(0, min(1000, temp))})
        if brightness is not None:
            cmds.append({"code": "bright_value", "value": max(10, min(1000, brightness * 10))})
        return self.send(device_id, cmds)

    def brightness(self, device_id, pct):
        """Set brightness (1-100%), preserving color mode if active."""
        value = max(10, min(1000, int(pct * 10)))
        try:
            status = self.cloud.getstatus(device_id)
            mode = colour_hex = None
            for item in status.get("result", []):
                if item.get("code") == "work_mode":
                    mode = item.get("value")
                if item.get("code") == "colour_data":
                    colour_hex = item.get("value")
            if mode == "colour" and colour_hex and len(colour_hex) == 12:
                h, s = colour_hex[0:4], colour_hex[4:8]
                return self.send(device_id, [
                    {"code": "work_mode", "value": "colour"},
                    {"code": "colour_data", "value": f"{h}{s}{value:04x}"}
                ])
        except Exception:
            pass
        return self.send(device_id, [{"code": "bright_value", "value": value}])

    def color(self, device_id, h, s=None, v=None):
        """Set color by HSV values or preset name."""
        if isinstance(h, str):
            name = h.lower()
            if name not in COLOR_PRESETS:
                return None, f"Unknown preset: {name}"
            h, s, v = COLOR_PRESETS[name]
        s = s if s is not None else 1000
        v = v if v is not None else 1000
        return self.send(device_id, [
            {"code": "work_mode", "value": "colour"},
            {"code": "colour_data", "value": f"{h:04x}{s:04x}{v:04x}"}
        ])

    def preset(self, device_id, name, brightness_pct=None):
        """Apply a named preset with optional brightness override."""
        name = name.lower()
        if name not in COLOR_PRESETS:
            return None, f"Available presets: {', '.join(sorted(COLOR_PRESETS.keys()))}"
        if name in ("warm", "cool"):
            temp = 500 if name == "warm" else 1000
            cmds = [
                {"code": "work_mode", "value": "white"},
                {"code": "temp_value", "value": temp}
            ]
            if brightness_pct is not None:
                cmds.append({"code": "bright_value", "value": max(10, min(1000, brightness_pct * 10))})
            return self.send(device_id, cmds)
        h, s, v = COLOR_PRESETS[name]
        if brightness_pct is not None:
            v = max(10, min(1000, brightness_pct * 10))
        return self.send(device_id, [
            {"code": "work_mode", "value": "colour"},
            {"code": "colour_data", "value": f"{h:04x}{s:04x}{v:04x}"}
        ])

    def raw(self, device_id, code, value):
        """Send raw DP command to any device."""
        try:
            value = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            pass
        return self.send(device_id, [{"code": code, "value": value}])

    def batch(self, device_id, commands):
        """Send multiple commands in a single API call."""
        return self.send(device_id, commands)

    def set_white(self, device_id, temp=None, brightness=None, turn_on=False):
        """Set white mode, optionally with on command, in one API call."""
        cmds = []
        if turn_on:
            cmds.append({"code": self._get_switch_code(device_id), "value": True})
        cmds.append({"code": "work_mode", "value": "white"})
        if temp is not None:
            cmds.append({"code": "temp_value", "value": max(0, min(1000, temp))})
        if brightness is not None:
            cmds.append({"code": "bright_value", "value": max(10, min(1000, brightness * 10))})
        return self.send(device_id, cmds)

    def set_color(self, device_id, name_or_h, s=None, v=None, brightness=None, turn_on=False):
        """Set color mode, optionally with on and brightness, in one API call."""
        if isinstance(name_or_h, str):
            preset = name_or_h.lower()
            if preset not in COLOR_PRESETS:
                return None, f"Unknown preset: {preset}"
            h, s, v = COLOR_PRESETS[preset]
        else:
            h = name_or_h
            s = s if s is not None else 1000
            v = v if v is not None else 1000
        if brightness is not None:
            v = max(10, min(1000, brightness * 10))
        cmds = []
        if turn_on:
            cmds.append({"code": self._get_switch_code(device_id), "value": True})
        cmds.append({"code": "work_mode", "value": "colour"})
        cmds.append({"code": "colour_data", "value": f"{h:04x}{s:04x}{v:04x}"})
        return self.send(device_id, cmds)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    ctrl = DeviceController()
    arg1 = sys.argv[1]

    # Discovery mode
    if arg1 == "discover":
        result = ctrl.discover()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # Device control mode
    device_id = arg1
    command = sys.argv[2] if len(sys.argv) > 2 else "status"
    args = sys.argv[3:]

    if command == "status":
        result = ctrl.status(device_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif command == "detail":
        result = ctrl.detail(device_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif command == "model":
        result = ctrl.model(device_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif command == "on":
        code = args[0] if args else None
        result, elapsed = ctrl.on(device_id, code)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"latency: {elapsed:.3f}s")

    elif command == "off":
        code = args[0] if args else None
        result, elapsed = ctrl.off(device_id, code)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"latency: {elapsed:.3f}s")

    elif command == "white":
        temp = int(args[0]) if args else None
        bri = int(args[1]) if len(args) > 1 else None
        result, elapsed = ctrl.white(device_id, temp, bri)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"latency: {elapsed:.3f}s")

    elif command == "brightness":
        pct = int(args[0]) if args else 50
        result, elapsed = ctrl.brightness(device_id, pct)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"latency: {elapsed:.3f}s")

    elif command == "color":
        if not args:
            print("Usage: color <name|h> [s] [v]")
            sys.exit(1)
        if args[0].isdigit():
            h = int(args[0])
            s = int(args[1]) if len(args) > 1 else 1000
            v = int(args[2]) if len(args) > 2 else 1000
            result, elapsed = ctrl.color(device_id, h, s, v)
        else:
            result, elapsed = ctrl.color(device_id, args[0])
        if result is None:
            print(elapsed)
            sys.exit(1)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"latency: {elapsed:.3f}s")

    elif command == "preset":
        name = args[0] if args else ""
        bri = int(args[1]) if len(args) > 1 and args[1].isdigit() else None
        result, msg = ctrl.preset(device_id, name, bri)
        if result is None:
            print(msg)
            sys.exit(1)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"latency: {msg:.3f}s")

    elif command == "send":
        if len(args) < 2:
            print("Usage: send <code> <value>")
            sys.exit(1)
        result, elapsed = ctrl.raw(device_id, args[0], args[1])
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"latency: {elapsed:.3f}s")

    elif command == "batch":
        if not args:
            print("Usage: batch '<json array of commands>'")
            sys.exit(1)
        try:
            commands = json.loads(" ".join(args))
            if not isinstance(commands, list):
                raise ValueError("Must be a JSON array")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"ERROR: Invalid JSON: {e}")
            sys.exit(1)
        result, elapsed = ctrl.batch(device_id, commands)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"latency: {elapsed:.3f}s")

    elif command == "set":
        if not args:
            print("Usage: set <mode> [options]")
            print("  set white [temp] [bri%] [--on]")
            print("  set color <name|H> [S] [V] [bri%] [--on]")
            sys.exit(1)
        mode = args[0].lower()
        remaining = args[1:]
        turn_on = "--on" in remaining
        remaining = [a for a in remaining if a != "--on"]

        if mode == "white":
            temp = int(remaining[0]) if remaining else None
            bri = int(remaining[1]) if len(remaining) > 1 else None
            result, elapsed = ctrl.set_white(device_id, temp, bri, turn_on)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print(f"latency: {elapsed:.3f}s")

        elif mode == "colour" or mode == "color":
            if not remaining:
                print("Usage: set color <name|H> [S] [V] [bri%] [--on]")
                sys.exit(1)
            bri = None
            if remaining[0].isdigit():
                h = int(remaining[0])
                s = int(remaining[1]) if len(remaining) > 1 and remaining[1].isdigit() else 1000
                v = int(remaining[2]) if len(remaining) > 2 and remaining[2].isdigit() else 1000
                if len(remaining) > 3 and remaining[3].isdigit():
                    bri = int(remaining[3])
            else:
                name = remaining[0]
                h, s, v = None, None, None
                if len(remaining) > 1 and remaining[1].isdigit():
                    bri = int(remaining[1])
            if h is not None:
                result, elapsed = ctrl.set_color(device_id, h, s, v, bri, turn_on)
            else:
                result, elapsed = ctrl.set_color(device_id, name, brightness=bri, turn_on=turn_on)
            if result is None:
                print(elapsed)
                sys.exit(1)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print(f"latency: {elapsed:.3f}s")
        else:
            print(f"Unknown set mode: {mode}. Use 'white' or 'color'.")

    elif command == "help":
        print(__doc__)
        print("Commands:")
        print("  status                    Get device status")
        print("  detail                    Get full device detail")
        print("  model                     Get device Thing Model (supported DPs)")
        print("  on [switch_code]          Turn on")
        print("  off [switch_code]         Turn off")
        print("  white [temp] [bri%]       White mode (temp: 0-1000, brightness: 1-100%)")
        print("  brightness <1-100>        Set brightness percentage")
        print("  color <name|H S V>        Set color by preset or HSV values")
        print("  preset <name> [bri%]      Set preset with optional brightness")
        print("  send <code> <value>       Send raw DP command")
        print("  batch '<json>'            Send multiple commands in one API call")
        print("  set white [t] [b] [--on]  Set white mode in one call (optional --on)")
        print("  set color <n> [b] [--on]  Set color mode in one call (optional --on)")
        print("  discover                  List all devices")
        print(f"\nPresets: {', '.join(sorted(COLOR_PRESETS.keys()))}")

    else:
        print(f"Unknown command: {command}. Use 'help' for usage.")


if __name__ == "__main__":
    main()
