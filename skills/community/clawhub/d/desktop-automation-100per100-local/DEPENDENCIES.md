# Dependencies — Desktop Automation Skill

This document explains each dependency and its purpose.

## Core (Required)

| Package | Version | Purpose |
|---------|---------|---------|
| `pyautogui` | 0.9.54 | Main automation library: mouse moves, clicks, keyboard typing, screenshots, scrolling |
| `pygetwindow` | 0.0.9 | Window management: get active window, list windows, activate by title |
| `Pillow` | 10.4.0 | Image handling (used by pyautogui for screenshots) |
| `pynput` | 1.7.6 | Low-level input listeners for macro recording (keyboard + mouse events) |

## Optional — Vision (Image & OCR)

| Package | Version | Purpose | Required for actions |
|---------|---------|---------|---------------------|
| `opencv-python` | 4.10.0.84 | Computer vision: template matching, image recognition | `find_image`, `wait_for_image` |
| `pytesseract` | 0.3.10 | Optical Character Recognition (OCR) | `find_text_on_screen`, `extract_screen_data` |

**Note on pytesseract**: You also need the [Tesseract binary](https://github.com/tesseract-ocr/tesseract) installed on your system (not just the Python package). On Windows, download the installer and add it to PATH.

## Optional — Clipboard

| Package | Version | Purpose | Required for actions |
|---------|---------|---------|---------------------|
| `pyperclip` | 1.9.0 | Cross-platform clipboard access | `copy_to_clipboard`, `paste_from_clipboard` |

**Platform notes**:
- Windows/macOS: usually works out of the box
- Linux: may require `xclip` or `xsel` system packages

## Optional — Data Integration (Excel/CSV)

| Package | Version | Purpose | Required for actions |
|---------|---------|---------|---------------------|
| `openpyxl` | 3.1.5 | Read/write Excel `.xlsx` files | `excel_read`, `excel_write` |
| `pandas` | 2.2.3 | DataFrames, CSV I/O | `data_to_csv` (and used inside excel functions) |

---

## Installing Selectively

You can install only the dependencies you need:

```bash
# Minimal: basic automation only
pip install pyautogui pygetwindow Pillow pynput

# + Image recognition
pip install opencv-python

# + OCR
pip install pytesseract

# + Clipboard
pip install pyperclip

# + Excel/CSV
pip install openpyxl pandas
```

The skill will automatically detect which dependencies are available and enable the corresponding actions. Missing optional dependencies will cause the related actions to return an error with a clear message (e.g., "openpyxl not installed").

---

## Full Install

To install everything at once:

```bash
pip install -r requirements.txt
```

The `requirements.txt` in this skill pins the versions that have been tested together.

---

## Troubleshooting

- **ImportError: No module named 'cv2'** → `opencv-python` not installed. Install it or avoid using `find_image`.
- **pytesseract.pytesseract.TesseractNotFoundError** → Tesseract binary missing. Install from https://github.com/tesseract-ocr/tesseract and add to PATH.
- **pyperclip.PyperclipException** on Linux → install `xclip` (`sudo apt-get install xclip`) or `xsel`.

---

**Last updated**: 2026-03-15
