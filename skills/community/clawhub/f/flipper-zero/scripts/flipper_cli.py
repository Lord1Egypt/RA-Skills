#!/usr/bin/env python3
"""
Flipper Zero CLI interface over USB serial.
Designed for OpenClaw to control a Flipper Zero via natural language.

Usage:
    flipper_cli.py <command> [args...]

Commands:
    info                        - Device info (firmware, battery, storage)
    storage list <path>         - List files/dirs
    storage read <path>         - Read file contents
    storage write <path> <data> - Write data to file
    storage mkdir <path>        - Create directory
    storage remove <path>       - Delete file/dir
    storage copy <src> <dst>    - Copy file
    storage move <src> <dst>    - Move/rename file
    storage info <path>         - Storage stats
    subghz rx <freq> [device]   - Receive SubGHz (device: 0=internal, 1=external/Flux)
    subghz tx <key> <freq> <te> <repeat> [device] - Transmit SubGHz
    subghz tx_from_file <path> [repeat] [device]  - Transmit from .sub file
    subghz rx_raw <freq>        - Receive raw SubGHz
    subghz decode_raw <path>    - Decode raw capture
    subghz chat <freq> [device] - SubGHz chat mode
    ir tx <path>                - Transmit IR from file
    nfc emulate <path>          - Emulate NFC
    rfid emulate <path>         - Emulate RFID
    badusb run <path>           - Execute BadUSB script
    gpio set <pin> <0|1>        - Set GPIO pin
    gpio read <pin>             - Read GPIO pin
    led <r> <g> <b>             - Set LED color
    vibro <0|1>                 - Vibration motor
    bt info                     - Bluetooth info
    power off                   - Shutdown
    power reboot                - Reboot
    power 5v <0|1>              - Enable/disable 5V on GPIO (for Flux Capacitor)
    raw <command>               - Send raw CLI command
    scan_subghz <freq> <duration_sec> [device] - Listen for signals for N seconds

Environment:
    FLIPPER_PORT    - Serial port (default: auto-detect)
    FLIPPER_BAUD    - Baud rate (default: 230400)
"""

import serial
import serial.tools.list_ports
import sys
import time
import json
import os
import signal
import re

DEFAULT_BAUD = 230400
READ_TIMEOUT = 2
CMD_WAIT = 1.5  # seconds to wait after sending command
LONG_CMD_WAIT = 5  # for rx/scan operations


def find_flipper_port():
    """Auto-detect Flipper Zero USB serial port."""
    port = os.environ.get('FLIPPER_PORT')
    if port:
        return port
    
    for p in serial.tools.list_ports.comports():
        if 'flip' in p.device.lower() or 'flip' in (p.description or '').lower():
            return p.device
    
    # Fallback: check for common macOS pattern
    import glob
    matches = glob.glob('/dev/cu.usbmodemflip_*')
    if matches:
        return matches[0]
    
    return None


class FlipperCLI:
    def __init__(self, port=None, baud=None):
        self.port = port or find_flipper_port()
        self.baud = baud or int(os.environ.get('FLIPPER_BAUD', DEFAULT_BAUD))
        self.ser = None
    
    def connect(self):
        if not self.port:
            raise ConnectionError("No Flipper Zero found. Is it plugged in via USB?")
        self.ser = serial.Serial(self.port, self.baud, timeout=READ_TIMEOUT)
        time.sleep(0.3)
        # Clear any pending data and get to a clean prompt
        self.ser.write(b'\r\n')
        time.sleep(0.3)
        self._flush()
    
    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
    
    def _flush(self):
        while self.ser.in_waiting:
            self.ser.read(self.ser.in_waiting)
            time.sleep(0.05)
    
    def send_command(self, cmd, wait=CMD_WAIT, read_until_prompt=True):
        """Send a CLI command and return the output."""
        self._flush()
        self.ser.write((cmd + '\r\n').encode())
        time.sleep(wait)
        
        output = b''
        while self.ser.in_waiting:
            output += self.ser.read(self.ser.in_waiting)
            time.sleep(0.1)
        
        text = output.decode('utf-8', errors='replace')
        
        # Remove the echoed command and trailing prompt
        lines = text.split('\r\n')
        # First line is usually the echoed command
        if lines and cmd in lines[0]:
            lines = lines[1:]
        # Last line is usually the prompt ">: "
        cleaned = []
        for line in lines:
            stripped = line.strip()
            if stripped == '>:' or stripped == '>: ':
                continue
            cleaned.append(line.rstrip())
        
        return '\n'.join(cleaned).strip()
    
    def send_command_streaming(self, cmd, duration_sec, callback=None):
        """Send a command and read output for a duration (for rx/scan)."""
        self._flush()
        self.ser.write((cmd + '\r\n').encode())
        
        output = b''
        start = time.time()
        while time.time() - start < duration_sec:
            if self.ser.in_waiting:
                chunk = self.ser.read(self.ser.in_waiting)
                output += chunk
                if callback:
                    callback(chunk.decode('utf-8', errors='replace'))
            time.sleep(0.1)
        
        # Send Ctrl+C to stop
        self.ser.write(b'\x03')
        time.sleep(0.5)
        while self.ser.in_waiting:
            output += self.ser.read(self.ser.in_waiting)
            time.sleep(0.1)
        
        return output.decode('utf-8', errors='replace')


# Risk classification (from V3SP3R)
RISK_LEVELS = {
    'low': [
        'device_info', 'storage list', 'storage read', 'storage info',
        'bt hci_info', 'power info', 'gpio read',
    ],
    'medium': [
        'storage write', 'storage mkdir', 'storage copy', 'storage move',
        'ir tx', 'subghz rx', 'subghz rx_raw', 'subghz decode_raw',
        'gpio set', 'led', 'vibro', 'power 5v',
        'nfc emulate', 'rfid emulate', 'badusb',
    ],
    'high': [
        'storage remove', 'subghz tx', 'subghz tx_from_file',
        'power off', 'power reboot',
    ],
}

def classify_risk(cmd):
    cmd_lower = cmd.lower()
    for level, patterns in RISK_LEVELS.items():
        for pattern in patterns:
            if cmd_lower.startswith(pattern):
                return level
    return 'medium'  # unknown = medium


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    flipper = FlipperCLI()
    
    try:
        flipper.connect()
        result = {"status": "ok", "command": command, "port": flipper.port}
        
        if command == 'info':
            info = flipper.send_command('device_info', wait=2)
            result['device_info'] = info
            
            storage = flipper.send_command('storage info /ext')
            result['storage'] = storage
            
        elif command == 'detect':
            # Just check connection
            info = flipper.send_command('device_info', wait=2)
            # Parse firmware
            for line in info.split('\n'):
                if 'firmware_version' in line:
                    result['firmware'] = line.split(':')[-1].strip()
                elif 'firmware_origin_fork' in line:
                    result['fork'] = line.split(':')[-1].strip()
            result['message'] = f"Flipper Zero connected on {flipper.port}"
            
        elif command == 'storage':
            if not args:
                print(json.dumps({"status": "error", "message": "storage requires: list|read|write|mkdir|remove|copy|move|info"}))
                return
            
            subcmd = args[0]
            
            if subcmd == 'list':
                path = args[1] if len(args) > 1 else '/ext'
                output = flipper.send_command(f'storage list {path}')
                result['path'] = path
                result['contents'] = output
                
            elif subcmd == 'read':
                path = args[1] if len(args) > 1 else ''
                if not path:
                    result = {"status": "error", "message": "storage read requires a path"}
                else:
                    output = flipper.send_command(f'storage read {path}', wait=2)
                    result['path'] = path
                    result['data'] = output
                    
            elif subcmd == 'write':
                if len(args) < 3:
                    result = {"status": "error", "message": "storage write requires <path> <data>"}
                else:
                    path = args[1]
                    data = ' '.join(args[2:])
                    risk = classify_risk(f'storage write')
                    result['risk'] = risk
                    output = flipper.send_command(f'storage write {path}')
                    # Writing via CLI requires streaming data then Ctrl+Z
                    flipper.ser.write(data.encode() + b'\x1a')
                    time.sleep(1)
                    while flipper.ser.in_waiting:
                        output += flipper.ser.read(flipper.ser.in_waiting).decode('utf-8', errors='replace')
                    result['output'] = output
                    
            elif subcmd == 'mkdir':
                path = args[1] if len(args) > 1 else ''
                output = flipper.send_command(f'storage mkdir {path}')
                result['output'] = output
                
            elif subcmd == 'remove':
                path = args[1] if len(args) > 1 else ''
                risk = classify_risk('storage remove')
                result['risk'] = risk
                output = flipper.send_command(f'storage remove {path}')
                result['output'] = output
                
            elif subcmd == 'copy':
                if len(args) < 3:
                    result = {"status": "error", "message": "storage copy requires <src> <dst>"}
                else:
                    output = flipper.send_command(f'storage copy {args[1]} {args[2]}')
                    result['output'] = output
                    
            elif subcmd == 'move':
                if len(args) < 3:
                    result = {"status": "error", "message": "storage move requires <src> <dst>"}
                else:
                    output = flipper.send_command(f'storage move {args[1]} {args[2]}')
                    result['output'] = output
                    
            elif subcmd == 'info':
                path = args[1] if len(args) > 1 else '/ext'
                output = flipper.send_command(f'storage info {path}')
                result['output'] = output
                
            else:
                result = {"status": "error", "message": f"Unknown storage command: {subcmd}"}
                
        elif command == 'subghz':
            if not args:
                result = {"status": "error", "message": "subghz requires: rx|tx|tx_from_file|rx_raw|decode_raw|chat"}
                print(json.dumps(result))
                return
            
            subcmd = args[0]
            
            if subcmd == 'rx':
                freq = args[1] if len(args) > 1 else '433920000'
                device = args[2] if len(args) > 2 else '0'
                duration = int(args[3]) if len(args) > 3 else 10
                result['frequency'] = freq
                result['device'] = 'external (Flux Capacitor)' if device == '1' else 'internal'
                result['duration'] = duration
                output = flipper.send_command_streaming(
                    f'subghz rx {freq} {device}', duration
                )
                result['captures'] = output
                
            elif subcmd == 'tx':
                if len(args) < 5:
                    result = {"status": "error", "message": "subghz tx requires <key_hex> <freq> <te_us> <repeat>"}
                else:
                    device = args[5] if len(args) > 5 else '0'
                    risk = classify_risk('subghz tx')
                    result['risk'] = risk
                    cmd = f'subghz tx {args[1]} {args[2]} {args[3]} {args[4]} {device}'
                    output = flipper.send_command(cmd, wait=3)
                    result['output'] = output
                    
            elif subcmd == 'tx_from_file':
                if len(args) < 2:
                    result = {"status": "error", "message": "subghz tx_from_file requires <path>"}
                else:
                    path = args[1]
                    repeat = args[2] if len(args) > 2 else '1'
                    device = args[3] if len(args) > 3 else '0'
                    risk = classify_risk('subghz tx_from_file')
                    result['risk'] = risk
                    result['file'] = path
                    cmd = f'subghz tx_from_file {path} {repeat} {device}'
                    output = flipper.send_command(cmd, wait=3)
                    result['output'] = output
                    
            elif subcmd == 'rx_raw':
                freq = args[1] if len(args) > 1 else '433920000'
                duration = int(args[2]) if len(args) > 2 else 10
                output = flipper.send_command_streaming(f'subghz rx_raw {freq}', duration)
                result['captures'] = output
                
            elif subcmd == 'decode_raw':
                path = args[1] if len(args) > 1 else ''
                output = flipper.send_command(f'subghz decode_raw {path}', wait=3)
                result['output'] = output
                
        elif command == 'ir':
            # IR commands via CLI are limited; mostly file-based
            subcmd = args[0] if args else ''
            if subcmd == 'tx' and len(args) > 1:
                output = flipper.send_command(f'ir tx {args[1]}', wait=2)
                result['output'] = output
            else:
                result = {"status": "error", "message": "ir requires: tx <file_path>"}
                
        elif command == 'gpio':
            subcmd = args[0] if args else ''
            if subcmd == 'set' and len(args) >= 3:
                output = flipper.send_command(f'gpio set {args[1]} {args[2]}')
                result['output'] = output
            elif subcmd == 'read' and len(args) >= 2:
                output = flipper.send_command(f'gpio read {args[1]}')
                result['output'] = output
            elif subcmd == 'mode' and len(args) >= 3:
                output = flipper.send_command(f'gpio mode {args[1]} {args[2]}')
                result['output'] = output
            else:
                result = {"status": "error", "message": "gpio requires: set <pin> <0|1> | read <pin> | mode <pin> <0|1>"}
                
        elif command == 'led':
            # Momentum firmware: led <r|g|b|bl> <0-255> (one channel at a time)
            if len(args) >= 2:
                output = flipper.send_command(f'led {args[0]} {args[1]}')
                result['output'] = output
            elif len(args) == 1 and args[0] == 'off':
                # Turn all LEDs off
                for ch in ['r', 'g', 'b', 'bl']:
                    flipper.send_command(f'led {ch} 0', wait=0.3)
                result['output'] = 'All LEDs off'
            else:
                result = {"status": "error", "message": "led requires <r|g|b|bl> <0-255> or 'off'"}
                
        elif command == 'vibro':
            val = args[0] if args else '1'
            output = flipper.send_command(f'vibro {val}')
            result['output'] = output
            
        elif command == 'bt':
            subcmd = args[0] if args else 'hci_info'
            output = flipper.send_command(f'bt {subcmd}')
            result['output'] = output
            
        elif command == 'power':
            if not args:
                result = {"status": "error", "message": "power requires: off|reboot|reboot2dfu|5v"}
            else:
                subcmd = args[0]
                risk = classify_risk(f'power {subcmd}')
                result['risk'] = risk
                if subcmd == '5v' and len(args) > 1:
                    output = flipper.send_command(f'power 5v {args[1]}')
                else:
                    output = flipper.send_command(f'power {subcmd}')
                result['output'] = output
                
        elif command == 'raw':
            raw_cmd = ' '.join(args)
            risk = classify_risk(raw_cmd)
            result['risk'] = risk
            result['raw_command'] = raw_cmd
            output = flipper.send_command(raw_cmd, wait=2)
            result['output'] = output
            
        elif command == 'scan_subghz':
            freq = args[0] if args else '433920000'
            duration = int(args[1]) if len(args) > 1 else 10
            device = args[2] if len(args) > 2 else '0'
            result['frequency'] = freq
            result['duration'] = duration
            result['device'] = 'external (Flux Capacitor)' if device == '1' else 'internal'
            output = flipper.send_command_streaming(
                f'subghz rx {freq} {device}', duration
            )
            result['captures'] = output
            
        else:
            result = {"status": "error", "message": f"Unknown command: {command}. Run without args for help."}
        
        print(json.dumps(result, indent=2))
        
    except ConnectionError as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
    except serial.SerialException as e:
        print(json.dumps({"status": "error", "message": f"Serial error: {e}"}))
        sys.exit(1)
    finally:
        flipper.disconnect()


if __name__ == '__main__':
    main()
