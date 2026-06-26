# Brother DCP-T426W Printer Project

## Overview

Printing skill for the **Brother DCP-T426W** inkjet printer. Primary method uses CUPS + IPP driverless for full format support. TCP direct available as text-only fallback.

**Supported platforms:** Any device with CUPS + `driverless` (NAS, Linux, macOS) or Python 3 with TCP access (fallback).

## Printer Details

| Field | Value |
|-------|-------|
| Model | Brother DCP-T426W |
| IP Address | 192.168.50.232 |
| Protocol | IPP (`ipp://192.168.50.232:631/ipp/print`) — primary; TCP 9100 fallback |
| Type | Color Inkjet MFP |

## Quick Commands

```bash
# Print text (IPP/CUPS, default)
python scripts/print.py --text "Hello World"

# Print file (text, image, PDF)
python scripts/print.py --file document.txt
python scripts/print.py --file photo.jpg
python scripts/print.py --file report.pdf

# Print text with receipt formatting
python scripts/print.py --text "Invoice #123" --mode receipt

# Print test page
python scripts/print.py --test

# Check printer status
python scripts/print.py --status

# Use TCP fallback (text only, no CUPS)
python scripts/print.py --file document.txt --method tcp
```

## Architecture

- `scripts/print.py` — Main CLI entrypoint (IPP/CUPS primary, TCP fallback)

## Print Methods

### IPP + driverless (default)

1. Calls CUPS `lp` command
2. CUPS converts input to PWG-raster using the driverless PPD
3. Data sent to printer via IPP protocol
4. Full support for text, images, PDFs

### TCP direct (fallback, `--method tcp`)

1. Opens TCP socket to printer at 192.168.50.232:9100
2. Wraps text in PJL (Printer Job Language) commands
3. Sends data directly to printer
4. Text only — images/PDFs need CUPS conversion

## Key Technical Notes

### CUPS Setup (one-time)

```bash
# Install CUPS + driverless
sudo apt install cups cups-filters ipp-usb
sudo systemctl enable --now cups

# Generate PPD and add printer
driverless "ipp://192.168.50.232:631/ipp/print" > ~/brother.ppd
sudo lpadmin -p Brother_DCP-T426W \
  -v "ipp://192.168.50.232:631/ipp/print" \
  -E \
  -P ~/brother.ppd
```

### PJL Protocol (TCP fallback)

The TCP direct method uses PJL (Printer Job Language) to wrap text data:
- `\x1b%-12345X` — Universal Exit Language (UEL)
- `@PJL ENTER LANGUAGE = PLAINTEXT` — Switch to plain text mode
- `\x0c` — Form feed (eject page)

### Platform Differences

| Concern | macOS | Linux |
|---------|-------|-------|
| CUPS service | `launchctl` | `systemctl` |
| PPD path | `/Library/Printers/PPDs/Contents/Resources/` | `/usr/share/ppd/` or `~/brother.ppd` |
| Driver install | `.dmg` / `.pkg` | `driverless` (IPP) or `.deb` / `.rpm` |
| `lp` / `lpstat` | Same commands | Same commands |

### PDL Limitations

The DCP-T426W is a **consumer inkjet** — it does NOT support:
- Native PostScript
- Native PCL
- Direct PDF printing (without CUPS conversion)
- IPP Everywhere / AirPrint

CUPS driverless handles all format conversion to PWG-raster.

## Troubleshooting

- **`driverless: command not found`**: `sudo apt install cups-filters ipp-usb`
- **IPP connection refused**: Verify printer supports IPP: `driverless` (list available printers)
- **No paper output**: Check paper tray, ink levels, printer not in error state
- **TCP prints garbled text**: Use IPP method — PJL PLAINTEXT may not be fully supported
- **CUPS printer not found**: Run `lpstat -p`; re-run lpadmin setup
