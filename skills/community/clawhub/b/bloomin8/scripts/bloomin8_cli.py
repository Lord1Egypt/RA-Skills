#!/usr/bin/env python3
"""
BLOOMIN8 E-Ink Device CLI Tool

A command-line tool using bleak to control e-ink devices via BLE + HTTP.

Features:
- Get device info (BLE wake + HTTP /deviceInfo)
- Upload images (auto BLE wake if device offline)
- Get/Set upstream controller settings

Usage:
    python bloomin8_cli.py info --name "EINK-XXXX"
    python bloomin8_cli.py info --id "12345678"
    python bloomin8_cli.py upload --ip 192.168.1.100 --file image.jpg
    python bloomin8_cli.py upload --name "EINK-XXXX" --file image.jpg --show
    python bloomin8_cli.py upstream --ip 192.168.1.100

Requirements:
    pip install bleak aiohttp pillow
"""

import argparse
import asyncio
import json
import struct
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

# Device cache path
DEVICE_CACHE_PATH = Path.home() / ".bloomin8" / "device_cache.json"

try:
    from bleak import BleakClient, BleakScanner
    from bleak.backends.device import BLEDevice
    from bleak.backends.scanner import AdvertisementData
except ImportError:
    print("Error: bleak not installed. Run: pip install bleak")
    sys.exit(1)

try:
    import aiohttp
    from aiohttp import FormData
except ImportError:
    print("Error: aiohttp not installed. Run: pip install aiohttp")
    sys.exit(1)

try:
    from PIL import Image
    import io
except ImportError:
    Image = None


# BLE GATT UUIDs
SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
NOTIFY_CHAR_UUID = "0000fff1-0000-1000-8000-00805f9b34fb"
WRITE_CHAR_UUID = "0000fff2-0000-1000-8000-00805f9b34fb"
WAKE_SERVICE_UUID = "0000f000-0000-1000-8000-00805f9b34fb"
WAKE_CHAR_UUID = "0000f001-0000-1000-8000-00805f9b34fb"

# Manufacturer IDs to filter
TARGET_MANUFACTURER_IDS = [0x1ADF, 0x013F]

# HTTP timeouts
HTTP_TIMEOUT = aiohttp.ClientTimeout(total=10)


def load_device_cache() -> dict:
    """Load device cache from disk"""
    if DEVICE_CACHE_PATH.exists():
        try:
            return json.loads(DEVICE_CACHE_PATH.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_device_cache(cache: dict):
    """Save device cache to disk"""
    DEVICE_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    DEVICE_CACHE_PATH.write_text(json.dumps(cache, indent=2, ensure_ascii=False))


def cache_device(name: str, device_id: str, ip: str, screen_w: int, screen_h: int):
    """Cache device info after a successful info/upload"""
    cache = load_device_cache()
    key = name.lower().strip() if name else device_id.upper()
    cache[key] = {
        "name": name,
        "device_id": device_id,
        "ip": ip,
        "screen_width": screen_w,
        "screen_height": screen_h,
        "updated": datetime.now().isoformat(),
    }
    save_device_cache(cache)


def lookup_cached_device(name: Optional[str] = None, device_id: Optional[str] = None, ip: Optional[str] = None) -> Optional[dict]:
    """Lookup a device from cache by name, device_id, or IP address"""
    cache = load_device_cache()
    if name:
        key = name.lower().strip()
        # Exact match first
        if key in cache:
            return cache[key]
        # Partial match
        for k, v in cache.items():
            if key in k or key in v.get("name", "").lower():
                return v
    if device_id:
        uid = device_id.upper()
        for v in cache.values():
            if v.get("device_id", "").upper() == uid:
                return v
    if ip:
        for v in cache.values():
            if v.get("ip") == ip:
                return v
    return None


def dedup_scan_results(devices: list) -> list:
    """Deduplicate scan results by device_id, keeping the strongest RSSI"""
    seen = {}
    for device, adv in devices:
        dev_id = None
        for mfr_id, msd_data in adv.manufacturer_data.items():
            if mfr_id in TARGET_MANUFACTURER_IDS:
                dev_id = EinkDevice.extract_device_id_from_msd(msd_data)
                break
        key = dev_id or device.address
        if key not in seen or adv.rssi > seen[key][1].rssi:
            seen[key] = (device, adv)
    return list(seen.values())


@dataclass
class DeviceInfo:
    device_id: str
    name: str
    sta_ip: Optional[str]
    sta_ssid: Optional[str]
    mac: Optional[str]
    firmware: Optional[str]
    screen_width: Optional[int]
    screen_height: Optional[int]
    battery: Optional[int]

    @classmethod
    def from_dict(cls, data: dict) -> "DeviceInfo":
        return cls(
            device_id=data.get("sn", data.get("device_id", "")),
            name=data.get("name", ""),
            sta_ip=data.get("sta_ip"),
            sta_ssid=data.get("sta_ssid"),
            mac=data.get("mac"),
            firmware=data.get("firmware", data.get("version")),
            screen_width=data.get("screen_width", data.get("width")),
            screen_height=data.get("screen_height", data.get("height")),
            battery=data.get("battery"),
        )


class EinkDevice:
    """E-Ink device controller using BLE + HTTP"""

    def __init__(self, ble_device: Optional[BLEDevice] = None, ip: Optional[str] = None):
        self.ble_device = ble_device
        self.ip = ip
        self._client: Optional[BleakClient] = None
        self._device_info: Optional[dict] = None
        self._info_received = asyncio.Event()
        self._screen_size: Optional[tuple[int, int]] = None

    @staticmethod
    async def scan(timeout: float = 10.0) -> list[tuple[BLEDevice, AdvertisementData]]:
        """Scan for BLOOMIN8 e-ink devices"""
        devices = []

        def detection_callback(device: BLEDevice, adv: AdvertisementData):
            if adv.manufacturer_data:
                for mfr_id in adv.manufacturer_data.keys():
                    if mfr_id in TARGET_MANUFACTURER_IDS:
                        devices.append((device, adv))
                        break

        scanner = BleakScanner(detection_callback=detection_callback)
        await scanner.start()
        await asyncio.sleep(timeout)
        await scanner.stop()

        return devices

    @staticmethod
    def extract_device_id_from_msd(msd_data: bytes) -> Optional[str]:
        """Extract device ID suffix from manufacturer specific data"""
        if len(msd_data) < 6:
            return None
        device_id_bytes = msd_data[2:6]
        return device_id_bytes.hex().upper()

    @staticmethod
    def extract_battery_from_msd(msd_data: bytes) -> Optional[int]:
        """Extract battery percentage from MSD (new firmware only)"""
        if len(msd_data) < 14:
            return None
        tag = msd_data[6:10]
        if tag != b"BATT":
            return None
        try:
            digits = msd_data[10:14].decode("ascii")
            raw = int(digits)
            return raw // 10
        except (ValueError, UnicodeDecodeError):
            return None

    async def connect_ble(self, timeout: float = 10.0) -> bool:
        """Connect to device via BLE"""
        if not self.ble_device:
            print("Error: No BLE device set")
            return False

        try:
            self._client = BleakClient(self.ble_device.address, timeout=timeout)
            await self._client.connect()
            print(f"✅ BLE connected to {self.ble_device.name or self.ble_device.address}")
            return True
        except Exception as e:
            print(f"❌ BLE connection failed: {e}")
            return False

    async def disconnect_ble(self):
        """Disconnect BLE"""
        if self._client and self._client.is_connected:
            await self._client.disconnect()
            print("🔌 BLE disconnected")

    async def send_wake(self) -> bool:
        """Send wake command via BLE"""
        if not self._client or not self._client.is_connected:
            print("Error: Not connected via BLE")
            return False

        try:
            # Write 0x01 then 0x00 to wake characteristic
            await self._client.write_gatt_char(WAKE_CHAR_UUID, bytes([0x01]), response=False)
            await asyncio.sleep(0.001)
            await self._client.write_gatt_char(WAKE_CHAR_UUID, bytes([0x00]), response=False)
            print("⚡ Wake command sent")
            return True
        except Exception as e:
            print(f"❌ Wake command failed: {e}")
            return False

    async def subscribe_notifications(self):
        """Subscribe to BLE notifications (only once)"""
        if not self._client or not self._client.is_connected:
            return

        # Check if already subscribed
        if hasattr(self, '_notifications_subscribed') and self._notifications_subscribed:
            return

        def notification_handler(sender, data: bytearray):
            try:
                json_data = json.loads(data.decode("utf-8").strip())
                msg_type = json_data.get("msg")
                print(f"  📡 BLE Notification: {msg_type}")

                if msg_type == "greet" and "data" in json_data:
                    self._device_info = json_data["data"]
                    self._info_received.set()
                    print(f"  ✅ Received device info: {json_data['data'].get('sn', 'unknown')}")
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"  ⚠️ Failed to parse notification: {e}")

        try:
            await self._client.start_notify(NOTIFY_CHAR_UUID, notification_handler)
            self._notifications_subscribed = True
            print("  ✅ Notifications subscribed")
        except Exception as e:
            print(f"  ⚠️ Subscribe notification error: {e}")
            # If already subscribed, that's ok
            self._notifications_subscribed = True

    async def send_ble_command(self, command: dict) -> bool:
        """Send JSON command via BLE"""
        if not self._client or not self._client.is_connected:
            return False

        try:
            json_str = json.dumps(command) + "\r\n"
            await self._client.write_gatt_char(WRITE_CHAR_UUID, json_str.encode(), response=False)
            return True
        except Exception as e:
            print(f"❌ BLE command failed: {e}")
            return False

    async def get_info_via_ble(self, timeout: float = 10.0) -> Optional[dict]:
        """Get device info via BLE - just wait for the notification"""
        self._info_received.clear()
        self._device_info = None

        try:
            await asyncio.wait_for(self._info_received.wait(), timeout=timeout)
            return self._device_info
        except asyncio.TimeoutError:
            print(f"⏳ Timeout waiting for device info ({timeout}s)")
            return None

    async def check_device_online(self, ip: str, timeout: float = 5.0) -> bool:
        """Check if device is online via HTTP whistle"""
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
                async with session.get(f"http://{ip}/whistle") as resp:
                    return resp.status == 200
        except Exception:
            return False

    async def get_device_info_http(self, ip: str) -> Optional[dict]:
        """Get device info via HTTP"""
        try:
            async with aiohttp.ClientSession(timeout=HTTP_TIMEOUT) as session:
                async with session.get(f"http://{ip}/deviceInfo") as resp:
                    if resp.status == 200:
                        return await resp.json()
        except Exception as e:
            print(f"❌ HTTP deviceInfo failed: {e}")
        return None

    async def upload_image(
        self,
        ip: str,
        image_path: str,
        filename: Optional[str] = None,
        gallery: str = "default",
        show_now: bool = True,
        resize: Optional[tuple[int, int]] = None,
        resize_mode: str = "cover",
    ) -> bool:
        """Upload image to device via HTTP.

        The device only accepts JPEG baseline images with dimensions matching
        the screen exactly. This method always converts to JPEG baseline and
        resizes when a target size is provided.
        """
        path = Path(image_path)
        if not path.exists():
            print(f"❌ Image not found: {image_path}")
            return False

        filename = filename or path.name

        if not Image:
            print("❌ Pillow is required for image processing (pip install pillow)")
            return False

        # Device requires JPEG baseline at exact screen dimensions.
        # Always open with Pillow to guarantee format conversion.
        try:
            image_data = path.read_bytes()
            img = Image.open(io.BytesIO(image_data))
            img = img.convert("RGB")
        except Exception as e:
            print(f"❌ Failed to open image: {e}")
            return False

        if resize:
            try:
                target_w, target_h = resize
                orig_w, orig_h = img.size

                if resize_mode == "cover":
                    orig_ratio = orig_w / orig_h
                    target_ratio = target_w / target_h
                    if orig_ratio > target_ratio:
                        new_height = target_h
                        new_width = int(new_height * orig_ratio)
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        left = (new_width - target_w) // 2
                        img = img.crop((left, 0, left + target_w, target_h))
                    else:
                        new_width = target_w
                        new_height = int(new_width / orig_ratio)
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        top = (new_height - target_h) // 2
                        img = img.crop((0, top, target_w, top + target_h))
                    print(f"📐 Cover resize to {target_w}x{target_h} (center crop)")
                elif resize_mode == "contain":
                    img.thumbnail(resize, Image.Resampling.LANCZOS)
                    new_img = Image.new("RGB", resize, (255, 255, 255))
                    paste_x = (target_w - img.width) // 2
                    paste_y = (target_h - img.height) // 2
                    new_img.paste(img, (paste_x, paste_y))
                    img = new_img
                    print(f"📐 Contain resize to {target_w}x{target_h} (white background)")
                else:  # stretch
                    img = img.resize(resize, Image.Resampling.LANCZOS)
                    print(f"📐 Stretch resize to {target_w}x{target_h}")
            except Exception as e:
                print(f"❌ Image processing failed: {e}")
                return False

        # Always encode as JPEG baseline — device requirement
        try:
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=90, progressive=False)
            image_data = buffer.getvalue()
        except Exception as e:
            print(f"❌ JPEG encoding failed: {e}")
            return False

        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
                form = FormData()
                form.add_field("image", image_data, filename=filename, content_type="image/jpeg")

                params = {
                    "filename": filename,
                    "gallery": gallery,
                    "show_now": "1" if show_now else "0",
                }

                async with session.post(f"http://{ip}/upload", params=params, data=form) as resp:
                    if resp.status == 200:
                        print(f"✅ Image uploaded: {filename}")
                        return True
                    else:
                        text = await resp.text()
                        print(f"❌ Upload failed ({resp.status}): {text}")
                        return False
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return False

    async def get_upstream_settings(self, ip: str) -> Optional[dict]:
        """Get upstream controller settings"""
        try:
            async with aiohttp.ClientSession(timeout=HTTP_TIMEOUT) as session:
                async with session.get(f"http://{ip}/upstream/pull_settings") as resp:
                    if resp.status == 200:
                        return await resp.json()
        except Exception as e:
            print(f"❌ Get upstream settings failed: {e}")
        return None

    async def set_upstream_settings(
        self,
        ip: str,
        upstream_on: Optional[bool] = None,
        token: Optional[str] = None,
        upstream_url: Optional[str] = None,
        cron_time: Optional[str] = None,
    ) -> bool:
        """Set upstream controller settings"""
        data = {}
        if upstream_on is not None:
            data["upstream_on"] = upstream_on
        if token:
            data["token"] = token
        if upstream_url:
            data["upstream_url"] = upstream_url
        if cron_time:
            data["cron_time"] = cron_time

        if not data:
            print("No settings to update")
            return False

        try:
            async with aiohttp.ClientSession(timeout=HTTP_TIMEOUT) as session:
                async with session.put(f"http://{ip}/upstream/pull_settings", json=data) as resp:
                    if resp.status == 200:
                        print("✅ Upstream settings updated")
                        return True
                    else:
                        text = await resp.text()
                        print(f"❌ Update failed ({resp.status}): {text}")
                        return False
        except Exception as e:
            print(f"❌ Update upstream settings failed: {e}")
            return False


async def find_device(name: Optional[str] = None, device_id: Optional[str] = None, timeout: float = 10.0) -> Optional[tuple[BLEDevice, AdvertisementData]]:
    """Find device by name or device ID"""
    print(f"🔍 Scanning for devices ({timeout}s)...")
    devices = await EinkDevice.scan(timeout)

    if not devices:
        print("❌ No BLOOMIN8 devices found")
        return None

    for device, adv in devices:
        # Match by name
        if name and adv.local_name and name.lower() in adv.local_name.lower():
            print(f"✅ Found device: {adv.local_name}")
            return device, adv

        # Match by device ID from MSD
        if device_id:
            for mfr_id, msd_data in adv.manufacturer_data.items():
                if mfr_id in TARGET_MANUFACTURER_IDS:
                    extracted_id = EinkDevice.extract_device_id_from_msd(msd_data)
                    if extracted_id and device_id.upper() in extracted_id:
                        print(f"✅ Found device by ID: {adv.local_name or device.address}")
                        return device, adv

    # If no specific match, list all found (deduped) devices
    unique_devices = dedup_scan_results(devices)
    print(f"\n📋 Found {len(unique_devices)} unique device(s):")
    for device, adv in unique_devices:
        msd_info = ""
        for mfr_id, msd_data in adv.manufacturer_data.items():
            if mfr_id in TARGET_MANUFACTURER_IDS:
                dev_id = EinkDevice.extract_device_id_from_msd(msd_data)
                battery = EinkDevice.extract_battery_from_msd(msd_data)
                msd_info = f" [ID: {dev_id}]"
                if battery:
                    msd_info += f" [Battery: {battery}%]"
        print(f"  - {adv.local_name or 'Unknown'} ({device.address}){msd_info}")

    return None


def _cache_fallback(name: Optional[str], device_id: Optional[str], use_json: bool) -> Optional[dict]:
    """Try to get device info from cache when BLE fails"""
    cached = lookup_cached_device(name=name, device_id=device_id)
    if cached and cached.get("ip"):
        if not use_json:
            print(f"⚠️ BLE failed. Using cached info (last updated: {cached.get('updated', 'unknown')})")
        return {**cached, "ble_info": None, "source": "cache"}
    return None


async def discover_device_ip(
    name: Optional[str] = None,
    device_id: Optional[str] = None,
    scan_timeout: float = 10.0,
    use_json: bool = False,
) -> Optional[dict]:
    """Discover device via BLE scan + wake + getInfo, with cache fallback.

    Returns dict with keys: ip, screen_width, screen_height, device_name,
    device_id, ble_info (raw notification dict or None), source ("ble" or "cache").
    Returns None if all discovery methods fail.
    """
    result = await find_device(name=name, device_id=device_id, timeout=scan_timeout)
    if not result:
        return _cache_fallback(name, device_id, use_json)

    ble_device, adv = result
    eink = EinkDevice(ble_device=ble_device)

    try:
        if not await eink.connect_ble():
            return _cache_fallback(name, device_id, use_json)

        await eink.subscribe_notifications()
        await eink.send_wake()
        if not use_json:
            print("⏳ Waiting for device to wake up (8s)...")
        await asyncio.sleep(8)

        if not use_json:
            print("🔍 Sending getInfo command...")
        info = None
        for attempt in range(5):
            await eink.send_ble_command({"cmd": "getInfo"})
            if not use_json:
                print(f"  ⏳ Waiting for response (attempt {attempt + 1}/5)...")
            info = await eink.get_info_via_ble(timeout=5.0)
            if info:
                break
            await asyncio.sleep(2)

        if not info:
            return _cache_fallback(name, device_id, use_json)

        sta_ip = info.get("sta_ip")
        screen_w = info.get("w") or info.get("screen_width")
        screen_h = info.get("h") or info.get("screen_height")
        dev_name = adv.local_name or info.get("name", "")
        dev_sn = info.get("sn", "")

        if sta_ip and screen_w and screen_h:
            cache_device(dev_name, dev_sn, sta_ip, screen_w, screen_h)

        return {
            "ip": sta_ip,
            "screen_width": screen_w,
            "screen_height": screen_h,
            "device_name": dev_name,
            "device_id": dev_sn,
            "ble_info": info,
            "source": "ble",
        }
    finally:
        await eink.disconnect_ble()


async def cmd_info(args):
    """Get device info command"""
    use_json = getattr(args, 'json', False)
    discovery = await discover_device_ip(
        name=args.name, device_id=args.id,
        scan_timeout=args.scan_timeout, use_json=use_json,
    )

    if not discovery:
        if use_json:
            print(json.dumps({"error": "failed_to_get_device_info"}))
        else:
            print("❌ Failed to get device info")
        return

    if discovery["source"] == "cache":
        if use_json:
            print(json.dumps({"source": "cache", **{k: v for k, v in discovery.items() if k not in ("ble_info", "source")}}))
        else:
            print(json.dumps({k: v for k, v in discovery.items() if k not in ("ble_info", "source")}, indent=2, ensure_ascii=False))
        return

    # BLE discovery succeeded — show full info
    info = discovery["ble_info"]
    sta_ip = discovery["ip"]

    if use_json:
        combined = {"source": "ble", "ble": info}
        if sta_ip:
            http_info = await EinkDevice(ip=sta_ip).get_device_info_http(sta_ip)
            if http_info:
                combined["http"] = http_info
        print(json.dumps(combined))
    else:
        print("\n📱 Device Info (BLE):")
        print(json.dumps(info, indent=2, ensure_ascii=False))
        if sta_ip:
            print(f"\n🌐 Checking HTTP ({sta_ip})...")
            http_info = await EinkDevice(ip=sta_ip).get_device_info_http(sta_ip)
            if http_info:
                print("📱 Device Info (HTTP):")
                print(json.dumps(http_info, indent=2, ensure_ascii=False))


async def cmd_upload(args):
    """Upload image command"""
    use_json = getattr(args, 'json', False)
    ip = args.ip
    screen_size = None

    # --- Resolve IP and screen size ---
    if ip:
        # Direct IP — get screen size from cache or --resize
        if not args.resize:
            cached = lookup_cached_device(name=args.name, device_id=args.id, ip=ip)
            if cached and cached.get("screen_width") and cached.get("screen_height"):
                screen_size = (cached["screen_width"], cached["screen_height"])
                if not use_json:
                    print(f"📐 Using cached screen size: {screen_size[0]}x{screen_size[1]}")
            else:
                if use_json:
                    print(json.dumps({"error": "no_screen_size", "message": "Screen size required. Pass --resize WxH or run 'info' first to cache screen size."}))
                else:
                    print("❌ Screen size unknown. Device requires exact screen-size JPEG.")
                    print("   Pass --resize WxH or run 'info' first to cache screen size.")
                return
    else:
        # BLE discovery path
        discovery = await discover_device_ip(
            name=args.name, device_id=args.id,
            scan_timeout=args.scan_timeout, use_json=use_json,
        )
        if not discovery or not discovery.get("ip"):
            if use_json:
                print(json.dumps({"error": "device_not_found", "message": "BLE discovery failed and no cached IP available"}))
            else:
                print("❌ Could not find device")
            return
        ip = discovery["ip"]
        if not use_json:
            print(f"📍 Device IP: {ip}")
        if discovery.get("screen_width") and discovery.get("screen_height"):
            screen_size = (discovery["screen_width"], discovery["screen_height"])
            if not use_json:
                print(f"📐 Screen size: {screen_size[0]}x{screen_size[1]}")

    # --- Check device online, BLE re-wake if needed ---
    eink = EinkDevice(ip=ip)
    if not use_json:
        print(f"🔍 Checking device at {ip}...")
    device_online = False
    for check_attempt in range(3):
        if await eink.check_device_online(ip, timeout=10):
            device_online = True
            break
        if not use_json:
            print(f"⚠️ Device offline (attempt {check_attempt + 1}/3), waiting...")
        await asyncio.sleep(5)

    if not device_online:
        if not use_json:
            print("⚠️ Device offline, attempting BLE wake...")

        ble_device = None
        result = await find_device(name=args.name, device_id=args.id, timeout=args.scan_timeout)
        if not result:
            if use_json:
                print(json.dumps({"error": "device_offline", "ip": ip}))
            else:
                print("❌ Cannot find device to wake")
            return
        ble_device = result[0]

        wake_eink = EinkDevice(ble_device=ble_device)
        if await wake_eink.connect_ble():
            await wake_eink.send_wake()
            if not use_json:
                print("⏳ Waiting for device to connect to WiFi (10s)...")
            await asyncio.sleep(10)
            await wake_eink.disconnect_ble()

            for check_attempt in range(3):
                if await eink.check_device_online(ip, timeout=10):
                    device_online = True
                    break
                if not use_json:
                    print(f"⏳ Still waiting... (attempt {check_attempt + 1}/3)")
                await asyncio.sleep(5)

            if not device_online:
                if use_json:
                    print(json.dumps({"error": "device_offline_after_wake", "ip": ip}))
                else:
                    print("❌ Device still offline after wake")
                return
            if not use_json:
                print("✅ Device is now online")

    # --- Determine resize dimensions ---
    resize = None
    if args.resize:
        try:
            w, h = map(int, args.resize.split("x"))
            resize = (w, h)
        except ValueError:
            print(f"⚠️ Invalid resize format: {args.resize}, expected WxH")
    elif screen_size:
        resize = screen_size
        if not use_json:
            print(f"📐 Auto-resizing to fit screen: {resize[0]}x{resize[1]}")

    # --- Upload ---
    show_now = not args.no_show if args.no_show else args.show
    success = await eink.upload_image(
        ip=ip,
        image_path=args.file,
        filename=args.filename,
        gallery=args.gallery,
        show_now=show_now,
        resize=resize,
        resize_mode=getattr(args, 'mode', 'cover'),
    )

    if use_json:
        print(json.dumps({"success": success, "ip": ip, "resize": f"{resize[0]}x{resize[1]}" if resize else None}))
    elif success:
        print("🎉 Upload complete!")


async def cmd_upstream(args):
    """Get/Set upstream settings command"""
    ip = args.ip

    if not ip:
        discovery = await discover_device_ip(
            name=args.name, device_id=args.id,
            scan_timeout=args.scan_timeout, use_json=False,
        )
        if not discovery or not discovery.get("ip"):
            print("❌ Could not get device IP")
            return
        ip = discovery["ip"]

    eink = EinkDevice(ip=ip)

    # Get current settings
    settings = await eink.get_upstream_settings(ip)
    if settings:
        print("\n⚙️ Current Upstream Settings:")
        print(json.dumps(settings, indent=2, ensure_ascii=False))

    # Update if any flags provided
    if any([args.on, args.off, args.token, args.url, args.cron]):
        upstream_on = None
        if args.on:
            upstream_on = True
        elif args.off:
            upstream_on = False

        await eink.set_upstream_settings(
            ip=ip,
            upstream_on=upstream_on,
            token=args.token,
            upstream_url=args.url,
            cron_time=args.cron,
        )


async def cmd_scan(args):
    """Scan for devices command"""
    use_json = getattr(args, 'json', False)
    if not use_json:
        print(f"🔍 Scanning for BLOOMIN8 devices ({args.timeout}s)...")
    raw_devices = await EinkDevice.scan(args.timeout)

    if not raw_devices:
        if use_json:
            print(json.dumps({"devices": [], "raw_count": 0}))
        else:
            print("❌ No devices found")
        return

    devices = dedup_scan_results(raw_devices)

    if use_json:
        result = []
        for device, adv in devices:
            entry = {"name": adv.local_name or "Unknown", "address": device.address, "rssi": adv.rssi}
            for mfr_id, msd_data in adv.manufacturer_data.items():
                if mfr_id in TARGET_MANUFACTURER_IDS:
                    entry["device_id"] = EinkDevice.extract_device_id_from_msd(msd_data)
                    battery = EinkDevice.extract_battery_from_msd(msd_data)
                    if battery is not None:
                        entry["battery"] = battery
            result.append(entry)
        print(json.dumps({"devices": result, "unique_count": len(devices), "raw_count": len(raw_devices)}))
        return

    print(f"\n📋 Found {len(devices)} unique device(s) ({len(raw_devices)} raw advertisements):\n")

    for device, adv in devices:
        print(f"📱 {adv.local_name or 'Unknown'}")
        print(f"   Address: {device.address}")
        print(f"   RSSI: {adv.rssi} dBm")

        for mfr_id, msd_data in adv.manufacturer_data.items():
            if mfr_id in TARGET_MANUFACTURER_IDS:
                dev_id = EinkDevice.extract_device_id_from_msd(msd_data)
                battery = EinkDevice.extract_battery_from_msd(msd_data)
                print(f"   Device ID: {dev_id}")
                if battery is not None:
                    print(f"   Battery: {battery}%")
                else:
                    print(f"   Battery: N/A (firmware < 1.8.30)")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="BLOOMIN8 E-Ink Device CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan for nearby devices
  python bloomin8_cli.py scan

  # Get device info by name
  python bloomin8_cli.py info --name "EINK-1234"

  # Get device info by device ID
  python bloomin8_cli.py info --id "12345678"

  # Upload image directly to IP
  python bloomin8_cli.py upload --ip 192.168.1.100 --file image.jpg --show

  # Upload image by device name (auto BLE wake)
  python bloomin8_cli.py upload --name "EINK-1234" --file image.jpg --resize 480x800 --show

  # View upstream settings
  python bloomin8_cli.py upstream --ip 192.168.1.100

  # Enable upstream with token
  python bloomin8_cli.py upstream --ip 192.168.1.100 --on --token "your-token"
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan for nearby devices")
    scan_parser.add_argument("--timeout", type=float, default=10.0, help="Scan timeout in seconds")
    scan_parser.add_argument("--json", action="store_true", help="Output as JSON for programmatic use")

    # Info command
    info_parser = subparsers.add_parser("info", help="Get device info")
    info_parser.add_argument("--name", help="Device name (partial match)")
    info_parser.add_argument("--id", help="Device ID (from MSD)")
    info_parser.add_argument("--scan-timeout", type=float, default=10.0, help="BLE scan timeout")
    info_parser.add_argument("--json", action="store_true", help="Output as JSON for programmatic use")

    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload image to device")
    upload_parser.add_argument("--ip", help="Device IP address (skips BLE discovery)")
    upload_parser.add_argument("--name", help="Device name (for BLE discovery, or cache lookup when used with --ip)")
    upload_parser.add_argument("--id", help="Device ID (for BLE discovery)")
    upload_parser.add_argument("--file", required=True, help="Image file to upload")
    upload_parser.add_argument("--filename", help="Filename on device (default: same as local)")
    upload_parser.add_argument("--gallery", default="default", help="Gallery name")
    upload_parser.add_argument("--show", action="store_true", default=True, help="Show image immediately (default: True)")
    upload_parser.add_argument("--no-show", action="store_true", help="Disable auto-show after upload")
    upload_parser.add_argument("--resize", help="Resize to WxH (e.g., 480x800)")
    upload_parser.add_argument("--mode", default="cover", choices=["cover", "contain", "stretch"], help="Resize mode: cover (center crop fill), contain (fit with white bg), stretch (distort). Default: cover")
    upload_parser.add_argument("--scan-timeout", type=float, default=10.0, help="BLE scan timeout")
    upload_parser.add_argument("--json", action="store_true", help="Output as JSON for programmatic use")

    # Upstream command
    upstream_parser = subparsers.add_parser("upstream", help="Get/Set upstream settings")
    upstream_parser.add_argument("--ip", help="Device IP address")
    upstream_parser.add_argument("--name", help="Device name (for BLE discovery)")
    upstream_parser.add_argument("--id", help="Device ID (for BLE discovery)")
    upstream_parser.add_argument("--on", action="store_true", help="Enable upstream")
    upstream_parser.add_argument("--off", action="store_true", help="Disable upstream")
    upstream_parser.add_argument("--token", help="Upstream token")
    upstream_parser.add_argument("--url", help="Upstream URL")
    upstream_parser.add_argument("--cron", help="Cron time expression")
    upstream_parser.add_argument("--scan-timeout", type=float, default=10.0, help="BLE scan timeout")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Run async command
    if args.command == "scan":
        asyncio.run(cmd_scan(args))
    elif args.command == "info":
        if not args.name and not args.id:
            print("Error: --name or --id required")
            return
        asyncio.run(cmd_info(args))
    elif args.command == "upload":
        if not args.ip and not args.name and not args.id:
            print("Error: --ip, --name, or --id required")
            return
        asyncio.run(cmd_upload(args))
    elif args.command == "upstream":
        if not args.ip and not args.name and not args.id:
            print("Error: --ip, --name, or --id required")
            return
        asyncio.run(cmd_upstream(args))


if __name__ == "__main__":
    main()
