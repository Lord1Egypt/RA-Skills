---
name: dlna-control
description: Use when controlling DLNA/UPnP media renderers (smart TVs, speakers) on a local network - discovering devices, playing media URLs, controlling playback (play/pause/stop), querying transport status, and setting default devices.
---

# DLNA/UPnP Control

## Overview

Control DLNA/UPnP MediaRenderer devices (smart TVs, speakers) on the local network. Uses `async_upnp_client` library for SSDP discovery and SOAP-based device control.

## When to Use

- Need to discover and list DLNA devices on LAN
- Play media URLs on smart TVs or DLNA speakers
- Control playback (play, pause, stop, seek)
- Query current transport/position status
- Set default device for simplified operations
- Build CLI or Python API for DLNA device control

## Core Pattern

### 1. Device Discovery

```python
from async_upnp_client import SsdpListener

async def discover_media_renderers(timeout: float = 5.0) -> list[DeviceInfo]:
    """Discover all MediaRenderer devices on network"""
    listener = SsdpListener()
    await listener.async_start()
    await asyncio.sleep(timeout)

    devices = []
    for usn, location in listener.unique_locations():
        device = await listener.async_get_device(location)
        if device and "MediaRenderer" in device.device_type:
            devices.append(DeviceInfo(
                name=device.friendly_name,
                udn=device.udn,
                location=location
            ))

    await listener.async_stop()
    return devices
```

### 2. Media Playback Control

```python
from async_upnp_client import AsyncUPnPClient, AVTransport

async def play_media(device_url: str, media_url: str, title: str = None):
    """Play media URL on DLNA device"""
    async with httpx.AsyncClient() as client:
        device = await UPnPDevice.async_get_device(device_url, client=client)
        av_transport = device.service("urn:schemas-upnp-org:service:AVTransport:1")

        # Build DIDL-Lite metadata
        metadata = f'''<?xml version="1.0" encoding="utf-8"?>
        <DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/"
                   xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/">
          <item id="0" parentID="0" restricted="0">
            <dc:title>{title or 'Media'}</dc:title>
            <res protocolInfo="http-get:*:video/mp4:*">{media_url}</res>
          </item>
        </DIDL-Lite>'''

        await av_transport.action("Stop", InstanceID=0)
        await av_transport.action("SetAVTransportURI", InstanceID=0, CurrentURI=media_url, CurrentURIMetaData=metadata)
        await av_transport.action("Play", InstanceID=0, Speed="1")
```

### 3. Transport Status Query

```python
async def get_playback_status(av_transport) -> dict:
    """Query current playback state"""
    info = await av_transport.action("GetTransportInfo", InstanceID=0)
    position = await av_transport.action("GetPositionInfo", InstanceID=0)
    return {
        "state": info.get("CurrentTransportState"),  # PLAYING, PAUSED, STOPPED
        "position": position.get("RelTime"),
        "duration": position.get("TrackDuration")
    }
```

## Quick Reference

| Action | Method |
|--------|--------|
| Discover devices | `SsdpListener().unique_locations()` |
| Play | `AVTransport.action("Play", InstanceID=0, Speed="1")` |
| Pause | `AVTransport.action("Pause", InstanceID=0)` |
| Stop | `AVTransport.action("Stop", InstanceID=0)` |
| Seek | `AVTransport.action("Seek", InstanceID=0, Unit="REL_TIME", Target="01:00:00")` |
| Volume | `RenderingControl.action("SetVolume", InstanceID=0, DesiredVolume=50)` |
| Status | `AVTransport.action("GetTransportInfo", InstanceID=0)` |

## Common Mistakes

| Issue | Fix |
|-------|-----|
| SSDP timeout | Increase timeout to 5-10s; check firewall allows UDP 1900 |
| Play fails silently | Verify media URL is accessible from TV network; check content type |
| Wrong content type | Match `protocolInfo` to actual MIME type (video/mp4, audio/wav) |
| Device not found | Use exact UDN or IP:port from discovery; check device supports MediaRenderer |

## CLI Framework

Use **Click** for CLI:

```python
import click
import asyncio

@click.group()
def cli():
    """DLNA/UPnP Media Controller"""
    pass

@cli.command()
@click.option("--timeout", "-t", default=5)
def discover(timeout):
    """Discover DLNA devices on network"""
    ...

@cli.command()
@click.argument("media_url")
@click.option("--device", "-d")
def play(media_url, device):
    """Play media URL"""
    ...
```

## Dependencies

```toml
dependencies = [
    "async_upnp_client>=0.36.0",
    "click>=8.0.0",
    "httpx>=0.25.0",
]
```
