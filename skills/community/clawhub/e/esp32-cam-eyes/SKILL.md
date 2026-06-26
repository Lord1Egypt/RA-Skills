---
name: esp32-cam-eyes
description: Set up ESP32-S3-CAM modules as visual sensors (eyes) for OpenClaw agents. Covers hardware identification, firmware flashing, WiFi configuration, and HTTP camera server deployment using PlatformIO + Arduino framework. Use when the user wants to give their agent physical vision, set up ESP32-CAM, connect a camera module, flash camera firmware, or troubleshoot ESP32-S3 camera issues. Supports Hiwonder/Freenove boards with GC2145, OV2640, and OV5640 sensors.
---

# ESP32-CAM Eyes

Give your OpenClaw agent physical eyes using ESP32-S3-CAM modules.

## Overview

Each ESP32-CAM module runs a lightweight HTTP server exposing `/capture` (single JPEG snapshot) and `/stream` (MJPEG live stream). Once connected to WiFi, the agent can grab images via `curl` for vision analysis.

## Prerequisites

- **Hardware**: ESP32-S3 development board with camera sensor (Hiwonder, Freenove, or similar)
- **Software**: macOS or Linux with Python 3 installed
- **Tools**: PlatformIO CLI (`pip3 install platformio`), pyserial (`pip3 install pyserial`)

## Quick Start

1. Plug in the ESP32-CAM via USB
2. Identify the serial port: `ls /dev/cu.usb*` (macOS) or `ls /dev/ttyUSB*` (Linux)
3. Identify the sensor model (critical — determines firmware config)
4. Create PlatformIO project, flash firmware
5. Connect to WiFi, test with `curl -o photo.jpg http://<IP>/capture`

For the complete step-by-step guide with firmware code, pin definitions, performance benchmarks, and troubleshooting: read [references/setup-guide.md](references/setup-guide.md).

## Key Decision: Sensor Type

The sensor model determines your firmware strategy:

| Sensor | PID | Hardware JPEG | Recommended Format |
|--------|-----|---------------|-------------------|
| OV2640 | 0x2640 | ✅ Yes | `PIXFORMAT_JPEG` directly |
| OV5640 | 0x5640 | ✅ Yes | `PIXFORMAT_JPEG` directly |
| GC2145 | 0x2145 | ❌ No | `PIXFORMAT_RGB565` + software `frame2jpg()` |

If buying new boards, prefer **OV2640** — hardware JPEG is significantly faster.

## API Endpoints

Once flashed and connected:

| Path | Function |
|------|----------|
| `/capture` | Single JPEG snapshot |
| `/stream` | MJPEG live stream |
| `/` | Web UI with stream viewer |

## Multi-Camera Deployment

Multiple ESP32-CAMs can join the same WiFi network for multi-angle coverage. Bind fixed IPs via router DHCP reservation to avoid IP changes on reboot.

## Common Pitfalls

- **Wrong sensor ID**: Always verify PID before choosing firmware config
- **Upload speed**: Use 460800 baud, not 921600 (causes flash verification failures on many boards)
- **WiFi band**: ESP32 only supports 2.4GHz — ensure your router has a 2.4GHz SSID available
- **QQVGA is slower than VGA**: Counter-intuitive but true due to PSRAM DMA buffer efficiency; use XGA (1024×768) for best speed/quality balance
