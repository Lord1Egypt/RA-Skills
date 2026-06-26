#!/usr/bin/env python3
"""
Flipper Zero SubGHz operations over BLE.

Uses app launch + screen reading + button navigation to perform SubGHz
operations wirelessly. This works around the limitation that SubGHz CLI
commands aren't available in the Protobuf RPC.

Usage:
    flipper_subghz_ble.py read [duration_sec]           - Open SubGHz Read mode and capture signals
    flipper_subghz_ble.py read_raw [duration_sec]        - Open SubGHz Read RAW mode
    flipper_subghz_ble.py frequency_analyzer [duration]  - Open Frequency Analyzer
    flipper_subghz_ble.py saved                          - List saved SubGHz signals
    flipper_subghz_ble.py transmit <filename>            - Transmit a saved .sub file
    flipper_subghz_ble.py navigate_to <menu_item>        - Navigate SubGHz menu to specific item
    flipper_subghz_ble.py status                         - Screenshot current SubGHz screen

Environment:
    FLIPPER_BLE_ADDRESS  - BLE address (skip scan)
    FLIPPER_BLE_NAME     - BLE name (default: Flipper)
"""

import asyncio
import sys
import os
import json
import time

# Import the screen module
sys.path.insert(0, os.path.dirname(__file__))
from flipper_screen import FlipperScreen

# SubGHz menu items in order (Momentum firmware)
SUBGHZ_MENU = [
    "Read",          # 0 - Read decoded signals
    "Read RAW",      # 1 - Read raw signals
    "Saved",         # 2 - Browse saved files
    "Add Manually",  # 3 - Manual signal entry
    "Frequency Analyzer",  # 4
    "Radio Settings",      # 5
]


class FlipperSubGhzBLE:
    def __init__(self):
        self.screen = FlipperScreen()
    
    async def connect(self):
        await self.screen.connect()
    
    async def disconnect(self):
        await self.screen.disconnect()
    
    async def _go_home(self):
        """Press back multiple times to ensure we're at the desktop."""
        for _ in range(5):
            await self.screen.send_input('back')
            await asyncio.sleep(0.15)
        await asyncio.sleep(0.3)
    
    async def _launch_subghz(self):
        """Navigate to and launch SubGHz app from desktop."""
        await self._go_home()
        await asyncio.sleep(0.3)
        
        # Press OK to enter main menu
        await self.screen.send_input('ok')
        await asyncio.sleep(0.5)
        
        # SubGHz is typically the first item in Momentum menu
        # But let's navigate up first to make sure we're at top
        await self.screen.send_input('up')
        await asyncio.sleep(0.2)
        await self.screen.send_input('up')
        await asyncio.sleep(0.2)
        await self.screen.send_input('up')
        await asyncio.sleep(0.2)
        await self.screen.send_input('up')
        await asyncio.sleep(0.2)
        await self.screen.send_input('up')
        await asyncio.sleep(0.2)
        
        # First item should be Sub-GHz, press OK
        await self.screen.send_input('ok')
        await asyncio.sleep(1.0)
        
        # Take a screenshot to verify we're in SubGHz
        result = await self.screen.ascii_screenshot()
        return result.get('ascii', '')
    
    async def _launch_subghz_direct(self):
        """Launch SubGHz app directly via protobuf app_start."""
        import flipper_pb2 as pb
        
        msg = pb.Main()
        msg.command_id = self.screen._next_id()
        msg.app_start_request.name = "Sub-GHz"
        msg.app_start_request.args = ""
        responses = await self.screen._send_and_wait(msg, timeout=5.0)
        
        if responses and responses[0].command_status != pb.OK:
            # Try alternate name
            msg2 = pb.Main()
            msg2.command_id = self.screen._next_id()
            msg2.app_start_request.name = "subghz"
            msg2.app_start_request.args = ""
            responses = await self.screen._send_and_wait(msg2, timeout=5.0)
        
        await asyncio.sleep(1.0)
        return responses
    
    async def _navigate_subghz_menu(self, target_index):
        """Navigate to a specific SubGHz menu item by index."""
        # Go to top of menu
        for _ in range(len(SUBGHZ_MENU)):
            await self.screen.send_input('up')
            await asyncio.sleep(0.15)
        
        # Navigate down to target
        for _ in range(target_index):
            await self.screen.send_input('down')
            await asyncio.sleep(0.15)
        
        # Select
        await self.screen.send_input('ok')
        await asyncio.sleep(0.5)
    
    async def read_signals(self, duration=15):
        """Open SubGHz Read mode and capture for duration seconds.
        
        Returns screenshots at intervals showing any decoded signals.
        """
        result = {
            "command": "subghz_read",
            "transport": "BLE",
            "duration": duration,
            "screenshots": []
        }
        
        # Launch SubGHz app
        await self._launch_subghz_direct()
        
        # Take a screenshot to see where we are
        screen_check = await self.screen.ascii_screenshot()
        ascii_text = screen_check.get('ascii', '')
        
        # Navigate to Read (first menu item)
        await self._navigate_subghz_menu(0)
        await asyncio.sleep(1.0)
        
        # Now we should be in Read mode — capture screens periodically
        start = time.time()
        interval = min(3, duration)
        frame_num = 0
        
        while time.time() - start < duration:
            # Capture screenshot
            screenshot = await self.screen.screenshot(
                f"/tmp/flipper_subghz_read_{frame_num:03d}.png"
            )
            ascii_shot = await self.screen.ascii_screenshot()
            
            result["screenshots"].append({
                "time": round(time.time() - start, 1),
                "file": screenshot.get("file"),
                "ascii": ascii_shot.get("ascii", "")
            })
            
            frame_num += 1
            
            remaining = duration - (time.time() - start)
            if remaining > 0:
                await asyncio.sleep(min(interval, remaining))
        
        # Press back to exit Read mode
        await self.screen.send_input('back')
        await asyncio.sleep(0.3)
        await self.screen.send_input('back')
        
        result["status"] = "ok"
        result["frames_captured"] = frame_num
        return result
    
    async def read_raw(self, duration=15):
        """Open SubGHz Read RAW mode."""
        result = {
            "command": "subghz_read_raw",
            "transport": "BLE",
            "duration": duration,
            "screenshots": []
        }
        
        await self._launch_subghz_direct()
        await self._navigate_subghz_menu(1)  # Read RAW
        await asyncio.sleep(1.0)
        
        # Press OK to start recording
        await self.screen.send_input('ok')
        await asyncio.sleep(0.5)
        
        start = time.time()
        frame_num = 0
        
        while time.time() - start < duration:
            ascii_shot = await self.screen.ascii_screenshot()
            screenshot = await self.screen.screenshot(
                f"/tmp/flipper_subghz_raw_{frame_num:03d}.png"
            )
            result["screenshots"].append({
                "time": round(time.time() - start, 1),
                "file": screenshot.get("file"),
                "ascii": ascii_shot.get("ascii", "")
            })
            frame_num += 1
            remaining = duration - (time.time() - start)
            if remaining > 0:
                await asyncio.sleep(min(3, remaining))
        
        # Press OK to stop recording, then back out
        await self.screen.send_input('ok')
        await asyncio.sleep(0.5)
        await self.screen.send_input('back')
        await asyncio.sleep(0.3)
        await self.screen.send_input('back')
        
        result["status"] = "ok"
        result["frames_captured"] = frame_num
        return result
    
    async def frequency_analyzer(self, duration=10):
        """Open Frequency Analyzer to see what's transmitting nearby."""
        result = {
            "command": "frequency_analyzer",
            "transport": "BLE",
            "duration": duration,
            "screenshots": []
        }
        
        await self._launch_subghz_direct()
        await self._navigate_subghz_menu(4)  # Frequency Analyzer
        await asyncio.sleep(1.0)
        
        start = time.time()
        frame_num = 0
        
        while time.time() - start < duration:
            ascii_shot = await self.screen.ascii_screenshot()
            screenshot = await self.screen.screenshot(
                f"/tmp/flipper_freqanalyzer_{frame_num:03d}.png"
            )
            result["screenshots"].append({
                "time": round(time.time() - start, 1),
                "file": screenshot.get("file"),
                "ascii": ascii_shot.get("ascii", "")
            })
            frame_num += 1
            remaining = duration - (time.time() - start)
            if remaining > 0:
                await asyncio.sleep(min(2, remaining))
        
        await self.screen.send_input('back')
        await asyncio.sleep(0.3)
        await self.screen.send_input('back')
        
        result["status"] = "ok"
        result["frames_captured"] = frame_num
        return result
    
    async def list_saved(self):
        """Navigate to Saved menu and capture the file list."""
        result = {
            "command": "subghz_saved",
            "transport": "BLE",
            "screenshots": []
        }
        
        await self._launch_subghz_direct()
        await self._navigate_subghz_menu(2)  # Saved
        await asyncio.sleep(1.0)
        
        # Capture several pages of the file browser
        for page in range(3):
            ascii_shot = await self.screen.ascii_screenshot()
            screenshot = await self.screen.screenshot(
                f"/tmp/flipper_subghz_saved_{page}.png"
            )
            result["screenshots"].append({
                "page": page,
                "file": screenshot.get("file"),
                "ascii": ascii_shot.get("ascii", "")
            })
            # Scroll down for next page
            for _ in range(5):
                await self.screen.send_input('down')
                await asyncio.sleep(0.1)
            await asyncio.sleep(0.3)
        
        await self.screen.send_input('back')
        await asyncio.sleep(0.3)
        await self.screen.send_input('back')
        
        result["status"] = "ok"
        return result
    
    async def transmit_file(self, filename):
        """Navigate to a saved file and transmit it.
        
        ⚠️ HIGH RISK - Requires explicit user confirmation before calling.
        
        filename: just the name, no path (e.g., "Home_Garage")
        """
        result = {
            "command": "subghz_transmit",
            "transport": "BLE",
            "risk": "high",
            "file": filename
        }
        
        await self._launch_subghz_direct()
        await self._navigate_subghz_menu(2)  # Saved
        await asyncio.sleep(1.0)
        
        # Take screenshot of file list
        ascii_shot = await self.screen.ascii_screenshot()
        result["file_list"] = ascii_shot.get("ascii", "")
        
        # TODO: OCR-based file finding would be ideal here
        # For now, user needs to know the position
        # We could scroll through and match, but that's fragile
        
        result["status"] = "ok"
        result["note"] = "File browser opened. Use navigate commands to select the file and press OK to open, then hold OK to transmit."
        
        return result
    
    async def take_status_screenshot(self):
        """Just take a screenshot of whatever's on screen."""
        screenshot = await self.screen.screenshot("/tmp/flipper_status.png")
        ascii_shot = await self.screen.ascii_screenshot()
        return {
            "status": "ok",
            "file": screenshot.get("file"),
            "ascii": ascii_shot.get("ascii", "")
        }


async def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    subghz = FlipperSubGhzBLE()
    
    try:
        await subghz.connect()
        
        if command == 'read':
            duration = int(args[0]) if args else 15
            result = await subghz.read_signals(duration)
        
        elif command == 'read_raw':
            duration = int(args[0]) if args else 15
            result = await subghz.read_raw(duration)
        
        elif command == 'frequency_analyzer':
            duration = int(args[0]) if args else 10
            result = await subghz.frequency_analyzer(duration)
        
        elif command == 'saved':
            result = await subghz.list_saved()
        
        elif command == 'transmit':
            if not args:
                print(json.dumps({"status": "error", "message": "transmit requires <filename>"}))
                return
            result = await subghz.transmit_file(args[0])
        
        elif command == 'status':
            result = await subghz.take_status_screenshot()
        
        else:
            result = {"status": "error", "message": f"Unknown command: {command}"}
        
        # Print JSON but handle ascii art specially
        print(json.dumps(result, indent=2, default=str))
    
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e), "type": type(e).__name__}))
        sys.exit(1)
    finally:
        await subghz.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
