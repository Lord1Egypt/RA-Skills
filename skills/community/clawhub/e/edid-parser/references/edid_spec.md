# EDID Specification Overview

## What is EDID?

EDID (Extended Display Identification Data) is a data structure that contains information about a display device. It's used to communicate display capabilities to a source device (like a computer, set-top box, or media player) so that the source can determine the optimal display settings.

## EDID Structure

### Version 1.3 (Most Common)

```
Offset  Size  Description
------  ----  -----------
0x00    8     Header: 00 FF FF FF FF FF FF 00
0x08    10    Vendor & Product Identification
0x12    4     EDID Version/Revision
0x14    16    Basic Display Parameters
0x24    10    Color Characteristics
0x2E    3     Established Timings I
0x31    2     Established Timings II / Reserved
0x33    16    Standard Timings
0x43    18    Detailed Timing Descriptor 1
0x55    18    Detailed Timing Descriptor 2
0x67    18    Detailed Timing Descriptor 3
0x79    18    Detailed Timing Descriptor 4
0x8B    1     Extension Flag
0x8C    1     Checksum
```

## Key Fields

### Header (0x00-0x07)
- Fixed bytes: `00 FF FF FF FF FF FF 00` (EDID marker)

### Vendor & Product Identification (0x08-0x11)
- **Manufacturer ID** (3 bytes): 3-character code (see manufacturer_codes.md)
- **Product Code** (2 bytes): Manufacturer-assigned product code
- **Serial Number** (4 bytes): Unique identifier
- **Week of Manufacture** (1 byte)
- **Year of Manufacture** (1 byte) - Year since 1990

### EDID Version (0x12-0x14)
- Version (typically 1)
- Revision (typically 3 or 4)

### Basic Display Parameters (0x14-0x23)
- **Video Input Definition**: Digital vs Analog
- **Max Horizontal Image Size** (cm)
- **Max Vertical Image Size** (cm)
- **Display Transfer Characteristic** (Gamma)
- **Power Management**: Standby, Suspend, Active Off
- **Color Format**: RGB, yCbCr, pseudo-color

### Color Characteristics (0x24-0x2D)
- Red, Green, Blue, White chromaticity coordinates
- Used for color profiling

### Established Timings (0x2E-0x33)
- Pre-defined timings like 640x480, 800x600, 1024x768, etc.

### Standard Timings (0x33-0x42)
- 16 slots for additional standard resolutions
- Format: 2 bytes per timing

### Detailed Timing Descriptors (0x43-0x6A)
- 4 descriptors, 18 bytes each
- Contains detailed timing information:
  - Pixel clock (kHz)
  - Horizontal active/blanking
  - Vertical active/blanking
  - Sync polarities
  - Sync widths

### Extension Blocks (0x8B+)
- Additional data blocks (e.g., CTA-861 for video timings, audio info)

## Common EDID Extensions

### CTA-861 Extension (Block 1)
Most common extension for modern displays:
- **Video Data Block**: Supported video formats (VICs)
- **Audio Data Block**: Audio capabilities
- **Speaker Allocation**: Speaker configuration
- **Vendor-Specific**: HDMI features, color spaces

## Common Problems

1. **Empty EDID**
   - No display connected
   - Display in sleep mode
   - Cable issue

2. **Corrupt EDID**
   - Invalid checksum
   - Hardware issue with display

3. **Missing Information**
   - Older displays may not report all capabilities
   - Some fields may be zero/undefined

4. **Outdated EDID**
   - Display firmware may have bugs
   - Workaround needed in driver

## Useful Commands

### Read EDID from DRM device
```bash
cat /sys/class/drm/card0-HDMI-A-1/edid
xxd /sys/class/drm/card0-HDMI-A-1/edid
```

### Decode EDID
```bash
edid-decode /sys/class/drm/card0-HDMI-A-1/edid
```

### Force read EDID
```bash
# Force kernel to re-read EDID
echo 1 > /sys/class/drm/card0-HDMI-A-1/edid
```

### Test EDID validity
```bash
# Check for valid header
head -c 8 /sys/class/drm/card0-HDMI-A-1/edid | xxd
# Should show: 00 ff ff ff ff ff ff 00

# Check checksum
edid-decode /sys/class/drm/card0-HDMI-A-1/edid 2>&1 | grep -i checksum
```

## References

- VESA E-EDID Standard: https://www.vesa.org/
- CTA-861 Standard: https://www.cta.tech/
- Linux DRM documentation: /usr/share/doc/linux-doc/gpu/drm-kms.rst