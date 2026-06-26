---
name: edid-parser
description: |
  Parse and analyze EDID (Extended Display Identification Data) from monitors and displays.
  
  USE WHEN: (1) User wants to read/parse display EDID information; (2) Checking display capabilities 
  and supported modes; (3) Debugging display/HDMI/CEC issues; (4) Listing available video outputs; 
  (5) Validating EDID data and generating diagnostic reports; (6) Batch processing multiple EDID files;
  (7) Working with DRM/KMS/display subsystems.
  
  SUPPORTS: Linux sysfs (/sys/class/drm/*/edid), binary EDID files (.bin), raw hex data.
  OUTPUT: Human-readable reports, JSON data, validation results.
---

# EDID Parser

Comprehensive EDID parsing and analysis skill for Linux systems.

## Quick Start

### 1. Parse a single EDID file

```bash
# From sysfs (Linux)
edid-decode /sys/class/drm/card0-HDMI-A-1/edid

# Or use our script
python3 scripts/parse_edid.py /sys/class/drm/card0-HDMI-A-1/edid
```

### 2. List all display outputs

```bash
bash scripts/list_outputs.sh
```

### 3. Validate and generate diagnostic report

```bash
bash scripts/validate_edid.sh /path/to/edid.bin
```

### 4. Extract key information (JSON)

```bash
python3 scripts/extract_info.py /path/to/edid.bin
```

### 5. Batch process multiple EDID files

```bash
python3 scripts/batch_validate.py /path/to/edid/directory/
```

## Features

### Feature 1: EDID Validity Check ✅

Validates if EDID is:
- Present and non-empty
- Has valid header (00 FF FF FF FF FF FF 00)
- Has valid checksum
- Can be decoded by edid-decode

**Usage:**
```bash
bash scripts/validate_edid.sh /sys/class/drm/card0-HDMI-A-1/edid
```

### Feature 2: Diagnostic Report

Generates human-readable diagnostic report with:
- Basic information (manufacturer, model, year)
- Display capabilities (resolution, refresh rate, screen size)
- Feature support (audio, YCbCr, HDR, VRR)
- Warnings and issues

**Usage:**
```bash
python3 scripts/diagnostic_report.py /path/to/edid.bin
```

### Feature 3: Human-Readable Report

Converts technical EDID data to easy-to-understand Chinese report.

**Usage:**
```bash
python3 scripts/extract_info.py /path/to/edid.bin
```

Output example:
```
📺 Display Info
   Manufacturer: Samsung (SAM)
   Model: FTV
   Production Date: Week 4, 2020
   
🖥️ Display Capabilities
   Max Resolution: 1920x1080 @ 60Hz
   Screen Size: 32 inches
   Audio: Supported (2-channel PCM)
   
🎨 Color Space
   RGB: Supported
   YCbCr 4:4:4: Supported
   YCbCr 4:2:2: Supported

⚠️ Issues/Warnings
   - Only 60Hz supported, no high refresh rate
```

### Feature 4: Batch Processing

Process multiple EDID files and generate summary report.

**Usage:**
```bash
python3 scripts/batch_validate.py ~/Downloads/edid/test-samples/Digital/
```

Output:
```
=== Batch EDID Validation ===
Total: 10 | Valid: 9 | Invalid: 1 | Warnings: 3

Invalid:
  - Digital/Sony/MS_0003/F19C835333F6 (128 bytes - Too small)

With Warnings:
  - Digital/Goldstar/GSM0000/A36298C521A5
  - Digital/TCL/TCL0000/0067660D05BD
```

## Scripts

| Script | Description |
|--------|-------------|
| `list_outputs.sh` | List all available display outputs on Linux |
| `parse_edid.sh` | Parse and display EDID in detail |
| `extract_info.py` | Extract key info as JSON |
| `validate_edid.sh` | Validate EDID and check for issues |
| `diagnostic_report.py` | Generate human-readable diagnostic report |
| `batch_validate.py` | Batch process multiple EDID files |

## Prerequisites

- `edid-decode` must be installed:
  ```bash
  sudo apt-get install edid-decode
  ```

## Common EDID File Locations

### Linux
```bash
# Find all EDID files
find /sys/class/drm -name "edid" -type f

# Typical paths
/sys/class/drm/card0-HDMI-A-1/edid
/sys/class/drm/card0-DP-1/edid
/sys/class/drm/card0-DVI-D-1/edid
```

### Extract from file
```bash
# Extract binary from text file
cat EDID.txt | grep -E '^([a-f0-9]{32}|[a-f0-9 ]{47})$' | tr -d '[:space:]' | xxd -r -p > EDID.bin
```

## Examples

### Example 1: Check monitor capabilities

**User says:** "What resolutions and refresh rates does my monitor support?"

**Action:**
```bash
python3 scripts/extract_info.py /path/to/edid.bin
# Or use built-in test sample:
python3 scripts/extract_info.py samples/test_tv_4k.bin
```

### Example 2: Use built-in test samples

The skill includes sample EDID files for testing:

```bash
# 4K TV sample (3840x2160 @ 30Hz)
python3 scripts/extract_info.py samples/test_tv_4k.bin

# 1080p Monitor sample (1920x1080 @ 60Hz)  
python3 scripts/extract_info.py samples/test_monitor_1080p.bin

# 4K Streaming stick sample (3840x2160 @ 60Hz)
python3 scripts/extract_info.py samples/test_stick_4k.bin
```

### Example 3: Validate all EDID files in a directory

**User says:** "Check if all EDID files in this directory have any issues"

**Action:**
```bash
python3 scripts/batch_validate.py ~/Downloads/edid/test-samples/Digital/
```

### Example 4: Debug display issue

**User says:** "Monitor not displaying, is it an EDID issue?"

**Action:**
```bash
bash scripts/validate_edid.sh /sys/class/drm/card0-HDMI-A-1/edid
```

Check for:
- Empty EDID (no display connected)
- Invalid checksum (corrupted)
- Missing DTD (no detailed timing)

## Troubleshooting

### EDID is empty
- Monitor may be in sleep mode or disconnected
- Try waking the monitor
- Check cable connections

### EDID decode errors
- EDID may be corrupted
- Monitor may not support standard EDID

### No display detected
- Check `/sys/class/drm/` for available outputs
- Try different port (HDMI/DP/DVI)

## References

- `references/manufacturer_codes.md` - EDID manufacturer codes
- `references/edid_spec.md` - EDID specification overview
- `references/feature_plan.md` - Feature roadmap