#!/usr/bin/env python3
"""
Flipper Zero BLE Screen & Input Control.

Captures the Flipper's 128x64 monochrome display and provides D-pad input.
Can render as PNG image or ASCII art.

Usage:
    flipper_screen.py screenshot [output.png]   - Capture screen as PNG
    flipper_screen.py ascii                      - Capture screen as ASCII art
    flipper_screen.py press <key>                - Press a button (up/down/left/right/ok/back)
    flipper_screen.py press <key> long           - Long press
    flipper_screen.py navigate <key1> <key2> ... - Press sequence of keys
    flipper_screen.py watch <seconds> [dir]      - Stream screenshots for N seconds
    flipper_screen.py app_control <app> [actions...] - Launch app then execute button sequence

Environment:
    FLIPPER_BLE_ADDRESS  - BLE address (skip scan)
    FLIPPER_BLE_NAME     - BLE name (default: Flipper)
"""

import asyncio
import sys
import os
import json
import time
import struct

from bleak import BleakClient, BleakScanner
from PIL import Image

# Add proto dir
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'proto'))
import flipper_pb2 as pb
import gui_pb2 as gui_pb

# BLE UUIDs
SERIAL_SERVICE = "8fe5b3d5-2e7f-4a98-2a48-7acc60fe0000"
RX_CHAR = "19ed82ae-ed21-4c9d-4145-228e62fe0000"
TX_CHAR = "19ed82ae-ed21-4c9d-4145-228e61fe0000"
FLOW_CHAR = "19ed82ae-ed21-4c9d-4145-228e63fe0000"

KNOWN_NON_FLIPPER = set()  # Add your non-Flipper BLE device names here to skip during scan
DEFAULT_NAME = os.environ.get("FLIPPER_BLE_NAME", "Flipper")

# Flipper display: 128x64 pixels, 1 bit per pixel, MSB first
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
SCREEN_BYTES = SCREEN_WIDTH * SCREEN_HEIGHT // 8  # 1024 bytes

# ASCII rendering chars
PIXEL_CHARS = {
    (0, 0): ' ',   # both empty
    (1, 0): '▀',   # top filled
    (0, 1): '▄',   # bottom filled
    (1, 1): '█',   # both filled
}

# Input key mapping
KEY_MAP = {
    'up': gui_pb.UP, 'down': gui_pb.DOWN,
    'left': gui_pb.LEFT, 'right': gui_pb.RIGHT,
    'ok': gui_pb.OK, 'back': gui_pb.BACK,
    'u': gui_pb.UP, 'd': gui_pb.DOWN,
    'l': gui_pb.LEFT, 'r': gui_pb.RIGHT,
    'o': gui_pb.OK, 'b': gui_pb.BACK,
}

INPUT_TYPE_MAP = {
    'press': gui_pb.PRESS, 'release': gui_pb.RELEASE,
    'short': gui_pb.SHORT, 'long': gui_pb.LONG,
    'repeat': gui_pb.REPEAT,
}


def _encode_varint(value):
    result = bytearray()
    while value > 0x7F:
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    result.append(value & 0x7F)
    return bytes(result)


def _decode_varint(data, offset):
    result = 0
    shift = 0
    for i in range(offset, min(offset + 10, len(data))):
        byte = data[i]
        result |= (byte & 0x7F) << shift
        shift += 7
        if not (byte & 0x80):
            return result, i + 1
    return None, offset


def frame_to_pixels(data):
    """Convert Flipper screen frame bytes to 2D pixel array.
    
    Flipper uses a column-major format: data is organized in 8-pixel-tall columns.
    Each byte represents 8 vertical pixels, LSB = top pixel.
    """
    if len(data) < SCREEN_BYTES:
        # Pad if short
        data = data + b'\x00' * (SCREEN_BYTES - len(data))
    
    pixels = [[0] * SCREEN_WIDTH for _ in range(SCREEN_HEIGHT)]
    
    for page in range(SCREEN_HEIGHT // 8):  # 8 pages of 8 rows each
        for x in range(SCREEN_WIDTH):
            byte = data[page * SCREEN_WIDTH + x]
            for bit in range(8):
                y = page * 8 + bit
                if y < SCREEN_HEIGHT:
                    pixels[y][x] = 1 if (byte >> bit) & 1 else 0
    
    return pixels


def pixels_to_png(pixels, output_path, scale=4):
    """Convert pixel array to scaled PNG."""
    w = SCREEN_WIDTH * scale
    h = SCREEN_HEIGHT * scale
    img = Image.new('1', (w, h), 0)  # 1-bit image, black background
    
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            if pixels[y][x]:
                for sy in range(scale):
                    for sx in range(scale):
                        img.putpixel((x * scale + sx, y * scale + sy), 1)
    
    # Convert to RGB for orange-on-black Flipper look
    img_rgb = Image.new('RGB', (w, h), (0, 0, 0))
    for y in range(h):
        for x in range(w):
            if img.getpixel((x, y)):
                img_rgb.putpixel((x, y), (255, 140, 0))  # Flipper orange
    
    img_rgb.save(output_path)
    return output_path


def pixels_to_ascii(pixels):
    """Convert pixel array to ASCII art using half-block characters.
    Each output row represents 2 pixel rows."""
    lines = []
    for y in range(0, SCREEN_HEIGHT, 2):
        line = ''
        for x in range(SCREEN_WIDTH):
            top = pixels[y][x] if y < SCREEN_HEIGHT else 0
            bottom = pixels[y + 1][x] if y + 1 < SCREEN_HEIGHT else 0
            line += PIXEL_CHARS[(top, bottom)]
        lines.append(line.rstrip())
    return '\n'.join(lines)


class FlipperScreen:
    def __init__(self):
        self.client = None
        self.address = None
        self.command_id = 0
        self._rx_buffer = bytearray()
        self._response_event = asyncio.Event()
        self._responses = {}
        self._screen_frames = []
        self._streaming = False
    
    async def connect(self, address=None):
        if address:
            self.address = address
        else:
            target = os.environ.get("FLIPPER_BLE_ADDRESS")
            if target:
                self.address = target
            else:
                devices = await BleakScanner.discover(timeout=10.0, return_adv=True)
                name_target = DEFAULT_NAME
                for addr, (dev, adv) in devices.items():
                    name = dev.name or adv.local_name or ""
                    if name in KNOWN_NON_FLIPPER:
                        continue
                    if name.lower() == name_target.lower():
                        self.address = addr
                        break
                if not self.address:
                    # Take first non-Apple device with Flipper service
                    for addr, (dev, adv) in devices.items():
                        name = dev.name or adv.local_name or ""
                        if name in KNOWN_NON_FLIPPER:
                            continue
                        svc = adv.service_uuids if adv else []
                        if any("8fe5b3d5" in s for s in svc):
                            self.address = addr
                            break
                    
        if not self.address:
            raise ConnectionError("Flipper not found")
        
        self.client = BleakClient(self.address, timeout=15.0)
        await self.client.connect()
        await self.client.start_notify(TX_CHAR, self._on_data)
        try:
            await self.client.start_notify(FLOW_CHAR, lambda s, d: None)
        except Exception:
            pass
        await asyncio.sleep(0.3)
    
    async def disconnect(self):
        if self._streaming:
            await self._stop_screen_stream()
        if self.client and self.client.is_connected:
            await self.client.disconnect()
    
    def _on_data(self, sender, data):
        self._rx_buffer.extend(data)
        self._try_parse()
    
    def _try_parse(self):
        while len(self._rx_buffer) > 1:
            try:
                length, offset = _decode_varint(self._rx_buffer, 0)
                if length is None:
                    return
                total = offset + length
                if len(self._rx_buffer) < total:
                    return
                
                msg_bytes = bytes(self._rx_buffer[offset:total])
                self._rx_buffer = self._rx_buffer[total:]
                
                msg = pb.Main()
                msg.ParseFromString(msg_bytes)
                
                # Screen frames come as gui_screen_frame with no command_id
                if msg.HasField('gui_screen_frame'):
                    self._screen_frames.append(msg.gui_screen_frame)
                    if not self._streaming:
                        self._response_event.set()
                
                cmd_id = msg.command_id
                if cmd_id:
                    if cmd_id not in self._responses:
                        self._responses[cmd_id] = []
                    self._responses[cmd_id].append(msg)
                    if not msg.has_next:
                        self._response_event.set()
                        
            except Exception:
                return
    
    def _next_id(self):
        self.command_id += 1
        return self.command_id
    
    async def _send(self, msg):
        data = msg.SerializeToString()
        framed = _encode_varint(len(data)) + data
        mtu = self.client.mtu_size - 3
        if mtu <= 0:
            mtu = 128
        for i in range(0, len(framed), mtu):
            chunk = framed[i:i + mtu]
            await self.client.write_gatt_char(RX_CHAR, chunk, response=False)
            if i + mtu < len(framed):
                await asyncio.sleep(0.01)
    
    async def _send_and_wait(self, msg, timeout=10.0):
        cmd_id = msg.command_id
        self._responses[cmd_id] = []
        self._response_event.clear()
        
        await self._send(msg)
        
        try:
            await asyncio.wait_for(self._response_event.wait(), timeout=timeout)
        except asyncio.TimeoutError:
            pass
        
        return self._responses.pop(cmd_id, [])
    
    async def _start_screen_stream(self):
        """Start receiving screen frames."""
        self._streaming = True
        self._screen_frames.clear()
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.gui_start_screen_stream_request.CopyFrom(gui_pb.StartScreenStreamRequest())
        await self._send(msg)
        # Give it a moment to start sending frames
        await asyncio.sleep(0.5)
    
    async def _stop_screen_stream(self):
        """Stop screen stream."""
        self._streaming = False
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.gui_stop_screen_stream_request.CopyFrom(gui_pb.StopScreenStreamRequest())
        await self._send(msg)
        await asyncio.sleep(0.2)
    
    async def capture_frame(self, timeout=3.0):
        """Capture a single screen frame."""
        self._screen_frames.clear()
        self._response_event.clear()
        
        await self._start_screen_stream()
        
        # Wait for at least one frame
        start = time.time()
        while not self._screen_frames and time.time() - start < timeout:
            await asyncio.sleep(0.1)
        
        await self._stop_screen_stream()
        
        if self._screen_frames:
            return self._screen_frames[-1]  # Return most recent frame
        return None
    
    async def screenshot(self, output_path=None, scale=4):
        """Capture screen and save as PNG."""
        frame = await self.capture_frame()
        if not frame or not frame.data:
            return {"status": "error", "message": "No frame received"}
        
        pixels = frame_to_pixels(frame.data)
        
        if not output_path:
            output_path = f"/tmp/flipper_screen_{int(time.time())}.png"
        
        pixels_to_png(pixels, output_path, scale=scale)
        
        return {
            "status": "ok",
            "file": output_path,
            "size": f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}",
            "orientation": gui_pb.ScreenOrientation.Name(frame.orientation),
            "data_bytes": len(frame.data)
        }
    
    async def ascii_screenshot(self):
        """Capture screen and return ASCII art."""
        frame = await self.capture_frame()
        if not frame or not frame.data:
            return {"status": "error", "message": "No frame received"}
        
        pixels = frame_to_pixels(frame.data)
        art = pixels_to_ascii(pixels)
        
        return {
            "status": "ok",
            "ascii": art,
            "size": f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}",
            "orientation": gui_pb.ScreenOrientation.Name(frame.orientation)
        }
    
    async def send_input(self, key, input_type="short"):
        """Send a button press to the Flipper."""
        key_enum = KEY_MAP.get(key.lower())
        if key_enum is None:
            return {"status": "error", "message": f"Unknown key: {key}. Use: up/down/left/right/ok/back"}
        
        type_enum = INPUT_TYPE_MAP.get(input_type.lower(), gui_pb.SHORT)
        
        if input_type.lower() == "short":
            # Short press = PRESS + SHORT + RELEASE
            for t in [gui_pb.PRESS, gui_pb.SHORT, gui_pb.RELEASE]:
                msg = pb.Main()
                msg.command_id = self._next_id()
                msg.gui_send_input_event_request.key = key_enum
                msg.gui_send_input_event_request.type = t
                await self._send(msg)
                await asyncio.sleep(0.05)
        elif input_type.lower() == "long":
            # Long press = PRESS + LONG + RELEASE
            for t in [gui_pb.PRESS, gui_pb.LONG, gui_pb.RELEASE]:
                msg = pb.Main()
                msg.command_id = self._next_id()
                msg.gui_send_input_event_request.key = key_enum
                msg.gui_send_input_event_request.type = t
                await self._send(msg)
                if t == gui_pb.PRESS:
                    await asyncio.sleep(0.8)  # Hold for long press
                else:
                    await asyncio.sleep(0.05)
        else:
            msg = pb.Main()
            msg.command_id = self._next_id()
            msg.gui_send_input_event_request.key = key_enum
            msg.gui_send_input_event_request.type = type_enum
            await self._send(msg)
        
        await asyncio.sleep(0.15)  # Let the UI settle
        
        return {"status": "ok", "key": key, "type": input_type}
    
    async def navigate(self, keys):
        """Press a sequence of keys with brief pauses."""
        results = []
        for key in keys:
            # Support "key:type" syntax (e.g., "ok:long")
            if ':' in key:
                k, t = key.split(':', 1)
            else:
                k, t = key, 'short'
            r = await self.send_input(k, t)
            results.append(r)
            await asyncio.sleep(0.2)
        return {"status": "ok", "actions": results}
    
    async def watch(self, duration, output_dir=None):
        """Capture screen frames for a duration, save as PNGs."""
        if not output_dir:
            output_dir = f"/tmp/flipper_watch_{int(time.time())}"
        os.makedirs(output_dir, exist_ok=True)
        
        self._screen_frames.clear()
        await self._start_screen_stream()
        
        start = time.time()
        frame_count = 0
        while time.time() - start < duration:
            await asyncio.sleep(0.2)
            while self._screen_frames:
                frame = self._screen_frames.pop(0)
                if frame.data:
                    pixels = frame_to_pixels(frame.data)
                    path = os.path.join(output_dir, f"frame_{frame_count:04d}.png")
                    pixels_to_png(pixels, path, scale=2)
                    frame_count += 1
        
        await self._stop_screen_stream()
        
        return {
            "status": "ok",
            "frames_captured": frame_count,
            "output_dir": output_dir,
            "duration": round(time.time() - start, 1)
        }
    
    async def app_control(self, app_name, actions):
        """Launch an app and execute button sequences.
        
        Actions can be:
        - Button names: up, down, left, right, ok, back
        - Long press: ok:long, back:long
        - Wait: wait:1.0 (seconds)
        - Screenshot: screenshot (captures current frame)
        """
        # Launch the app via protobuf
        import application_pb2 as app_pb_mod
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.app_start_request.name = app_name
        msg.app_start_request.args = ""
        responses = await self._send_and_wait(msg, timeout=5.0)
        
        if responses and responses[0].command_status != pb.OK:
            return {"status": "error", "message": f"Failed to start {app_name}: {pb.CommandStatus.Name(responses[0].command_status)}"}
        
        await asyncio.sleep(1.0)  # Let app load
        
        results = []
        for action in actions:
            if action.startswith('wait:'):
                wait_time = float(action.split(':')[1])
                await asyncio.sleep(wait_time)
                results.append({"action": "wait", "seconds": wait_time})
            elif action == 'screenshot':
                r = await self.screenshot()
                results.append({"action": "screenshot", **r})
            elif action == 'ascii':
                r = await self.ascii_screenshot()
                results.append({"action": "ascii", **r})
            else:
                if ':' in action:
                    k, t = action.split(':', 1)
                else:
                    k, t = action, 'short'
                r = await self.send_input(k, t)
                results.append(r)
                await asyncio.sleep(0.3)
        
        return {"status": "ok", "app": app_name, "actions": results}


async def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    screen = FlipperScreen()
    
    try:
        await screen.connect()
        
        if command == 'screenshot':
            output = args[0] if args else None
            result = await screen.screenshot(output)
            print(json.dumps(result, indent=2))
        
        elif command == 'ascii':
            result = await screen.ascii_screenshot()
            if result.get('ascii'):
                print(result['ascii'])
                print(f"\n[{result['size']}, {result['orientation']}]")
            else:
                print(json.dumps(result, indent=2))
        
        elif command == 'press':
            if not args:
                print(json.dumps({"status": "error", "message": "press requires: up/down/left/right/ok/back"}))
                return
            key = args[0]
            input_type = args[1] if len(args) > 1 else 'short'
            result = await screen.send_input(key, input_type)
            print(json.dumps(result, indent=2))
        
        elif command == 'navigate':
            if not args:
                print(json.dumps({"status": "error", "message": "navigate requires key sequence"}))
                return
            result = await screen.navigate(args)
            print(json.dumps(result, indent=2))
        
        elif command == 'watch':
            duration = float(args[0]) if args else 5.0
            output_dir = args[1] if len(args) > 1 else None
            result = await screen.watch(duration, output_dir)
            print(json.dumps(result, indent=2))
        
        elif command == 'app_control':
            if not args:
                print(json.dumps({"status": "error", "message": "app_control requires <app_name> [actions...]"}))
                return
            app_name = args[0]
            actions = args[1:] if len(args) > 1 else ['wait:1', 'screenshot']
            result = await screen.app_control(app_name, actions)
            print(json.dumps(result, indent=2))
        
        else:
            print(json.dumps({"status": "error", "message": f"Unknown command: {command}"}))
    
    except ConnectionError as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e), "type": type(e).__name__}))
        sys.exit(1)
    finally:
        await screen.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
