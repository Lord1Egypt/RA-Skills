#!/usr/bin/env python3
"""
Flipper Zero BLE Protobuf RPC client.
Connects to Flipper over Bluetooth and sends commands via the Protobuf RPC protocol.

Usage:
    flipper_ble.py <command> [args...]

Commands:
    scan                        - Scan for Flipper Zero devices
    ping                        - Ping the Flipper
    info                        - Device info (all properties)
    power_info                  - Battery/power info
    storage list <path>         - List files/dirs
    storage read <path>         - Read file contents
    storage write <path> <local_file> - Write file from local path
    storage mkdir <path>        - Create directory
    storage delete <path>       - Delete file/dir (⚠️ HIGH RISK)
    storage info <path>         - Storage stats
    storage md5 <path>          - MD5 checksum
    storage rename <old> <new>  - Rename/move
    gpio read <pin>             - Read GPIO pin (PC0,PC1,PC3,PB2,PB3,PA4,PA6,PA7)
    gpio write <pin> <0|1>      - Write GPIO pin
    gpio mode <pin> <input|output> - Set pin mode
    gpio otg <on|off>           - 5V OTG power (for Flux Capacitor)
    app start <name> [args]     - Start Flipper app
    app exit                    - Exit current app
    alert                       - Play audiovisual alert
    datetime                    - Get date/time
    reboot [os|dfu|update]      - Reboot (⚠️ HIGH RISK)
    protobuf_version            - Protocol version

Environment:
    FLIPPER_BLE_ADDRESS  - BLE address (skip scan)
    FLIPPER_BLE_NAME     - BLE name to search for (default: Flipper)
"""

import asyncio
import struct
import sys
import json
import os
import time

from bleak import BleakClient, BleakScanner

# Add proto dir to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'proto'))

import flipper_pb2 as pb
import storage_pb2 as storage_pb
import system_pb2 as system_pb
import gpio_pb2 as gpio_pb
import application_pb2 as app_pb

# Flipper BLE UUIDs
SERIAL_SERVICE = "8fe5b3d5-2e7f-4a98-2a48-7acc60fe0000"
RX_CHAR = "19ed82ae-ed21-4c9d-4145-228e62fe0000"   # Write TO Flipper
TX_CHAR = "19ed82ae-ed21-4c9d-4145-228e61fe0000"    # Read FROM Flipper (indications)
FLOW_CHAR = "19ed82ae-ed21-4c9d-4145-228e63fe0000"  # Flow control
RPC_CHAR = "19ed82ae-ed21-4c9d-4145-228e64fe0000"   # RPC status

KNOWN_NON_FLIPPER = set()  # Add your non-Flipper BLE device names here to skip during scan
DEFAULT_NAME = os.environ.get("FLIPPER_BLE_NAME", "Flipper")


class FlipperBLE:
    def __init__(self):
        self.client = None
        self.address = None
        self.command_id = 0
        self._response_data = bytearray()
        self._response_event = asyncio.Event()
        self._responses = {}  # command_id -> list of responses
        self._pending_id = None

    async def scan(self, timeout=10.0):
        """Scan for Flipper devices."""
        devices = await BleakScanner.discover(timeout=timeout, return_adv=True)
        flippers = []
        for addr, (dev, adv) in devices.items():
            name = dev.name or adv.local_name or ""
            if name in KNOWN_NON_FLIPPER:
                continue
            rssi = adv.rssi if adv else None
            svc = adv.service_uuids if adv else []
            # Match by name or service UUID
            if "flipper" in name.lower() or name == DEFAULT_NAME or \
               any("8fe5b3d5" in s for s in svc):
                flippers.append({"name": name, "address": addr, "rssi": rssi})
        return flippers

    async def connect(self, address=None, name=None):
        """Connect to Flipper."""
        if address:
            self.address = address
        else:
            # Scan and find
            target_name = name or DEFAULT_NAME
            devices = await self.scan()
            for d in devices:
                if d["name"].lower() == target_name.lower():
                    self.address = d["address"]
                    break
            # If exact name not found, take first Flipper device
            if not self.address and devices:
                self.address = devices[0]["address"]
            if not self.address:
                raise ConnectionError(f"Flipper '{target_name}' not found. Is BLE enabled?")

        self.client = BleakClient(self.address, timeout=15.0)
        await self.client.connect()

        # Start listening for indications on TX characteristic
        await self.client.start_notify(TX_CHAR, self._on_indication)

        # Also listen on flow control
        try:
            await self.client.start_notify(FLOW_CHAR, self._on_flow)
        except Exception:
            pass  # Flow control notifications may not be available

        # Small delay for BLE stack to settle
        await asyncio.sleep(0.3)

    async def disconnect(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()

    def _on_indication(self, sender, data):
        """Handle incoming data from Flipper."""
        self._response_data.extend(data)
        # Try to parse — protobuf messages are length-delimited
        self._try_parse_response()

    def _on_flow(self, sender, data):
        """Handle flow control notifications."""
        pass  # For now, we don't need to handle back-pressure

    def _try_parse_response(self):
        """Try to parse a complete protobuf response from accumulated data."""
        if len(self._response_data) < 2:
            return

        # Flipper BLE protocol: varint-length-delimited protobuf messages
        try:
            # Read varint length
            length, offset = _decode_varint(self._response_data, 0)
            if length is None:
                return
            total = offset + length
            if len(self._response_data) < total:
                return  # Not enough data yet

            # Extract the message bytes
            msg_bytes = bytes(self._response_data[offset:total])
            self._response_data = self._response_data[total:]

            # Parse the Main message
            msg = pb.Main()
            msg.ParseFromString(msg_bytes)

            cmd_id = msg.command_id
            if cmd_id not in self._responses:
                self._responses[cmd_id] = []
            self._responses[cmd_id].append(msg)

            if not msg.has_next:
                self._response_event.set()

            # Try to parse more if there's remaining data
            if len(self._response_data) > 1:
                self._try_parse_response()

        except Exception:
            # Incomplete message, wait for more data
            pass

    def _next_id(self):
        self.command_id += 1
        return self.command_id

    async def _send(self, msg):
        """Serialize and send a Main message."""
        data = msg.SerializeToString()
        # Length-delimited: varint length prefix + message
        framed = _encode_varint(len(data)) + data

        # Split into MTU-sized chunks if needed
        mtu = self.client.mtu_size - 3  # BLE overhead
        if mtu <= 0:
            mtu = 128

        for i in range(0, len(framed), mtu):
            chunk = framed[i:i + mtu]
            await self.client.write_gatt_char(RX_CHAR, chunk, response=False)
            if i + mtu < len(framed):
                await asyncio.sleep(0.01)  # Small delay between chunks

    async def _send_and_wait(self, msg, timeout=10.0):
        """Send a message and wait for the response(s)."""
        cmd_id = msg.command_id
        self._responses[cmd_id] = []
        self._response_event.clear()
        self._response_data.clear()

        await self._send(msg)

        try:
            await asyncio.wait_for(self._response_event.wait(), timeout=timeout)
        except asyncio.TimeoutError:
            pass

        responses = self._responses.pop(cmd_id, [])
        return responses

    # ---- High-level commands ----

    async def ping(self, data=b"ping"):
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.system_ping_request.data = data
        responses = await self._send_and_wait(msg)
        if responses and responses[0].command_status == pb.OK:
            return {"status": "ok", "pong_data": responses[0].system_ping_response.data.decode('utf-8', errors='replace')}
        return {"status": "error", "message": "No ping response", "raw": [str(r) for r in responses]}

    async def device_info(self):
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.system_device_info_request.CopyFrom(system_pb.DeviceInfoRequest())
        responses = await self._send_and_wait(msg, timeout=5.0)
        info = {}
        for r in responses:
            if r.HasField('system_device_info_response'):
                info[r.system_device_info_response.key] = r.system_device_info_response.value
        return info

    async def power_info(self):
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.system_power_info_request.CopyFrom(system_pb.PowerInfoRequest())
        responses = await self._send_and_wait(msg, timeout=5.0)
        info = {}
        for r in responses:
            if r.HasField('system_power_info_response'):
                info[r.system_power_info_response.key] = r.system_power_info_response.value
        return info

    async def protobuf_version(self):
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.system_protobuf_version_request.CopyFrom(system_pb.ProtobufVersionRequest())
        responses = await self._send_and_wait(msg)
        if responses:
            r = responses[0]
            return {"major": r.system_protobuf_version_response.major,
                    "minor": r.system_protobuf_version_response.minor}
        return None

    async def play_alert(self):
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.system_play_audiovisual_alert_request.CopyFrom(system_pb.PlayAudiovisualAlertRequest())
        responses = await self._send_and_wait(msg)
        return {"status": "ok" if responses and responses[0].command_status == pb.OK else "error"}

    async def get_datetime(self):
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.system_get_datetime_request.CopyFrom(system_pb.GetDateTimeRequest())
        responses = await self._send_and_wait(msg)
        if responses and responses[0].HasField('system_get_datetime_response'):
            dt = responses[0].system_get_datetime_response.datetime
            return {
                "year": dt.year, "month": dt.month, "day": dt.day,
                "hour": dt.hour, "minute": dt.minute, "second": dt.second,
                "weekday": dt.weekday
            }
        return None

    async def reboot(self, mode="os"):
        modes = {"os": 0, "dfu": 1, "update": 2}
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.system_reboot_request.mode = modes.get(mode, 0)
        await self._send(msg)  # Reboot won't get a response
        return {"status": "ok", "mode": mode}

    async def storage_list(self, path="/ext"):
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.storage_list_request.path = path
        responses = await self._send_and_wait(msg, timeout=10.0)
        files = []
        for r in responses:
            if r.HasField('storage_list_response'):
                for f in r.storage_list_response.file:
                    files.append({
                        "name": f.name,
                        "type": "dir" if f.type == storage_pb.File.DIR else "file",
                        "size": f.size
                    })
        return files

    async def storage_read(self, path):
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.storage_read_request.path = path
        responses = await self._send_and_wait(msg, timeout=10.0)
        data = b''
        for r in responses:
            if r.HasField('storage_read_response') and r.storage_read_response.file.data:
                data += r.storage_read_response.file.data
            if r.command_status != pb.OK:
                return {"status": "error", "code": r.command_status,
                        "message": pb.CommandStatus.Name(r.command_status)}
        return {"status": "ok", "data": data.decode('utf-8', errors='replace'), "size": len(data)}

    async def storage_write(self, path, data):
        """Write data to a file on Flipper. Data can be bytes or str."""
        if isinstance(data, str):
            data = data.encode('utf-8')

        CHUNK_SIZE = 256  # Safe chunk size for BLE
        offset = 0
        while offset < len(data):
            chunk = data[offset:offset + CHUNK_SIZE]
            msg = pb.Main()
            msg.command_id = self._next_id()
            msg.has_next = (offset + CHUNK_SIZE < len(data))
            msg.storage_write_request.path = path
            msg.storage_write_request.file.data = chunk
            if offset + CHUNK_SIZE >= len(data):
                # Last chunk — wait for response
                responses = await self._send_and_wait(msg)
                if responses and responses[0].command_status != pb.OK:
                    return {"status": "error", "code": responses[0].command_status}
            else:
                await self._send(msg)
                await asyncio.sleep(0.05)
            offset += CHUNK_SIZE

        return {"status": "ok", "bytes_written": len(data)}

    async def storage_mkdir(self, path):
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.storage_mkdir_request.path = path
        responses = await self._send_and_wait(msg)
        status = responses[0].command_status if responses else -1
        return {"status": "ok" if status == pb.OK else "error",
                "code": pb.CommandStatus.Name(status) if status != -1 else "NO_RESPONSE"}

    async def storage_delete(self, path, recursive=False):
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.storage_delete_request.path = path
        msg.storage_delete_request.recursive = recursive
        responses = await self._send_and_wait(msg)
        status = responses[0].command_status if responses else -1
        return {"status": "ok" if status == pb.OK else "error",
                "code": pb.CommandStatus.Name(status) if status != -1 else "NO_RESPONSE"}

    async def storage_info(self, path="/ext"):
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.storage_info_request.path = path
        responses = await self._send_and_wait(msg)
        if responses and responses[0].HasField('storage_info_response'):
            r = responses[0].storage_info_response
            return {"total_space": r.total_space, "free_space": r.free_space}
        return None

    async def storage_md5(self, path):
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.storage_md5sum_request.path = path
        responses = await self._send_and_wait(msg)
        if responses and responses[0].HasField('storage_md5sum_response'):
            return responses[0].storage_md5sum_response.md5sum
        return None

    async def storage_rename(self, old_path, new_path):
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.storage_rename_request.old_path = old_path
        msg.storage_rename_request.new_path = new_path
        responses = await self._send_and_wait(msg)
        status = responses[0].command_status if responses else -1
        return {"status": "ok" if status == pb.OK else "error"}

    async def gpio_read(self, pin_name):
        pin = _parse_pin(pin_name)
        if pin is None:
            return {"status": "error", "message": f"Unknown pin: {pin_name}"}

        # Set pin to input mode first
        mode_msg = pb.Main()
        mode_msg.command_id = self._next_id()
        mode_msg.gpio_set_pin_mode.pin = pin
        mode_msg.gpio_set_pin_mode.mode = gpio_pb.INPUT
        await self._send_and_wait(mode_msg)

        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.gpio_read_pin.pin = pin
        responses = await self._send_and_wait(msg)
        if responses and responses[0].HasField('gpio_read_pin_response'):
            return {"pin": pin_name, "value": responses[0].gpio_read_pin_response.value}
        return {"status": "error", "message": "No response"}

    async def gpio_write(self, pin_name, value):
        pin = _parse_pin(pin_name)
        if pin is None:
            return {"status": "error", "message": f"Unknown pin: {pin_name}"}

        # Set pin to output mode first
        mode_msg = pb.Main()
        mode_msg.command_id = self._next_id()
        mode_msg.gpio_set_pin_mode.pin = pin
        mode_msg.gpio_set_pin_mode.mode = gpio_pb.OUTPUT
        await self._send_and_wait(mode_msg)

        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.gpio_write_pin.pin = pin
        msg.gpio_write_pin.value = int(value)
        responses = await self._send_and_wait(msg)
        status = responses[0].command_status if responses else -1
        return {"status": "ok" if status == pb.OK else "error", "pin": pin_name, "value": int(value)}

    async def gpio_set_mode(self, pin_name, mode):
        pin = _parse_pin(pin_name)
        if pin is None:
            return {"status": "error", "message": f"Unknown pin: {pin_name}"}
        mode_val = gpio_pb.OUTPUT if mode.lower() == "output" else gpio_pb.INPUT
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.gpio_set_pin_mode.pin = pin
        msg.gpio_set_pin_mode.mode = mode_val
        responses = await self._send_and_wait(msg)
        status = responses[0].command_status if responses else -1
        return {"status": "ok" if status == pb.OK else "error"}

    async def gpio_otg(self, on=True):
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.gpio_set_otg_mode.mode = gpio_pb.ON if on else gpio_pb.OFF
        responses = await self._send_and_wait(msg)
        status = responses[0].command_status if responses else -1
        return {"status": "ok" if status == pb.OK else "error", "otg": "on" if on else "off"}

    async def app_start(self, name, args=""):
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.app_start_request.name = name
        msg.app_start_request.args = args
        responses = await self._send_and_wait(msg)
        status = responses[0].command_status if responses else -1
        return {"status": "ok" if status == pb.OK else "error",
                "code": pb.CommandStatus.Name(status) if status != -1 else "NO_RESPONSE"}

    async def app_exit(self):
        msg = pb.Main()
        msg.command_id = self._next_id()
        msg.app_exit_request.CopyFrom(app_pb.AppExitRequest())
        responses = await self._send_and_wait(msg)
        status = responses[0].command_status if responses else -1
        return {"status": "ok" if status == pb.OK else "error"}


def _parse_pin(name):
    """Parse GPIO pin name to enum value."""
    pins = {
        "PC0": gpio_pb.PC0, "PC1": gpio_pb.PC1, "PC3": gpio_pb.PC3,
        "PB2": gpio_pb.PB2, "PB3": gpio_pb.PB3,
        "PA4": gpio_pb.PA4, "PA6": gpio_pb.PA6, "PA7": gpio_pb.PA7,
    }
    return pins.get(name.upper())


def _encode_varint(value):
    """Encode an integer as a protobuf varint."""
    result = bytearray()
    while value > 0x7F:
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    result.append(value & 0x7F)
    return bytes(result)


def _decode_varint(data, offset):
    """Decode a varint from data at offset. Returns (value, new_offset) or (None, offset)."""
    result = 0
    shift = 0
    for i in range(offset, min(offset + 10, len(data))):
        byte = data[i]
        result |= (byte & 0x7F) << shift
        shift += 7
        if not (byte & 0x80):
            return result, i + 1
    return None, offset


async def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    flipper = FlipperBLE()
    result = {"command": command}

    try:
        if command == "scan":
            devices = await flipper.scan()
            result["status"] = "ok"
            result["devices"] = devices
            print(json.dumps(result, indent=2))
            return

        # Connect
        address = os.environ.get("FLIPPER_BLE_ADDRESS")
        await flipper.connect(address=address)
        result["transport"] = "BLE"
        result["address"] = flipper.address

        if command == "ping":
            r = await flipper.ping()
            result.update(r)

        elif command == "info":
            info = await flipper.device_info()
            result["status"] = "ok"
            result["device_info"] = info

        elif command == "power_info":
            info = await flipper.power_info()
            result["status"] = "ok"
            result["power"] = info

        elif command == "protobuf_version":
            ver = await flipper.protobuf_version()
            result["status"] = "ok"
            result["version"] = ver

        elif command == "alert":
            r = await flipper.play_alert()
            result.update(r)

        elif command == "datetime":
            dt = await flipper.get_datetime()
            result["status"] = "ok"
            result["datetime"] = dt

        elif command == "reboot":
            mode = args[0] if args else "os"
            r = await flipper.reboot(mode)
            result.update(r)

        elif command == "storage":
            if not args:
                result = {"status": "error", "message": "storage requires: list|read|write|mkdir|delete|info|md5|rename"}
            else:
                subcmd = args[0]
                if subcmd == "list":
                    path = args[1] if len(args) > 1 else "/ext"
                    files = await flipper.storage_list(path)
                    result["status"] = "ok"
                    result["path"] = path
                    result["files"] = files
                elif subcmd == "read":
                    path = args[1] if len(args) > 1 else ""
                    r = await flipper.storage_read(path)
                    result.update(r)
                elif subcmd == "write":
                    if len(args) < 3:
                        result = {"status": "error", "message": "storage write <flipper_path> <local_file>"}
                    else:
                        flipper_path = args[1]
                        local_file = args[2]
                        with open(local_file, 'rb') as f:
                            data = f.read()
                        r = await flipper.storage_write(flipper_path, data)
                        result.update(r)
                elif subcmd == "mkdir":
                    r = await flipper.storage_mkdir(args[1])
                    result.update(r)
                elif subcmd == "delete":
                    recursive = "--recursive" in args
                    r = await flipper.storage_delete(args[1], recursive=recursive)
                    result.update(r)
                elif subcmd == "info":
                    path = args[1] if len(args) > 1 else "/ext"
                    info = await flipper.storage_info(path)
                    result["status"] = "ok"
                    result["storage"] = info
                elif subcmd == "md5":
                    md5 = await flipper.storage_md5(args[1])
                    result["status"] = "ok"
                    result["md5"] = md5
                elif subcmd == "rename":
                    if len(args) < 3:
                        result = {"status": "error", "message": "storage rename <old> <new>"}
                    else:
                        r = await flipper.storage_rename(args[1], args[2])
                        result.update(r)

        elif command == "gpio":
            if not args:
                result = {"status": "error", "message": "gpio requires: read|write|mode|otg"}
            else:
                subcmd = args[0]
                if subcmd == "read":
                    r = await flipper.gpio_read(args[1])
                    result.update(r)
                elif subcmd == "write":
                    r = await flipper.gpio_write(args[1], args[2])
                    result.update(r)
                elif subcmd == "mode":
                    r = await flipper.gpio_set_mode(args[1], args[2])
                    result.update(r)
                elif subcmd == "otg":
                    on = args[1].lower() in ("on", "1", "true") if len(args) > 1 else True
                    r = await flipper.gpio_otg(on)
                    result.update(r)

        elif command == "app":
            if not args:
                result = {"status": "error", "message": "app requires: start|exit"}
            elif args[0] == "start":
                name = args[1] if len(args) > 1 else ""
                app_args = " ".join(args[2:]) if len(args) > 2 else ""
                r = await flipper.app_start(name, app_args)
                result.update(r)
            elif args[0] == "exit":
                r = await flipper.app_exit()
                result.update(r)

        else:
            result = {"status": "error", "message": f"Unknown command: {command}"}

        print(json.dumps(result, indent=2, default=str))

    except ConnectionError as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e), "type": type(e).__name__}))
        sys.exit(1)
    finally:
        await flipper.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
