# Browser Support Details

This document provides detailed information about browser support across different platforms.

## Supported Browsers

### Chrome
- **Windows**: Chrome, Google Chrome
- **macOS**: Google Chrome
- **Linux**: Google Chrome, google-chrome-stable
- **Command**: `--browser chrome`
- **Installation Paths**:
  - Windows: `C:\Program Files\Google\Chrome\Application\chrome.exe`
  - macOS: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
  - Linux: `/usr/bin/google-chrome`, `/usr/bin/google-chrome-stable`

### Firefox
- **Windows**: Firefox, Mozilla Firefox
- **macOS**: Firefox
- **Linux**: Firefox, firefox-esr
- **Command**: `--browser firefox`
- **Installation Paths**:
  - Windows: `C:\Program Files\Mozilla Firefox\firefox.exe`
  - macOS: `/Applications/Firefox.app/Contents/MacOS/firefox`
  - Linux: `/usr/bin/firefox`, `/usr/bin/firefox-esr`

### Edge
- **Windows**: Edge, Microsoft Edge
- **macOS**: Microsoft Edge
- **Linux**: Microsoft Edge
- **Command**: `--browser edge`
- **Installation Paths**:
  - Windows: `C:\Program Files\Microsoft\Edge\Application\msedge.exe`
  - macOS: `/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge`

### Safari
- **macOS**: Safari, Apple Safari
- **Windows/Linux**: Not supported
- **Command**: `--browser safari`
- **Installation Paths**:
  - macOS: `/Applications/Safari.app/Contents/MacOS/Safari`

## Platform-Specific Notes

### Windows
- Uses `where` command to find browser executables
- Supports both 32-bit and 64-bit program paths
- Edge is pre-installed on Windows 10 and later

### macOS
- Uses `which` command to find browser executables
- Applications are typically in `/Applications/`
- Safari is the default browser and pre-installed

### Linux
- Uses `which` command to find browser executables
- Distribution-specific paths may vary
- Some distributions may require additional packages

## Browser Flags and Options

### Chrome
- `--incognito`: Incognito mode
- `--headless`: Headless mode (no GUI)
- `--new-window`: Open in new window
- `--disable-gpu`: Disable GPU acceleration (useful with headless)

### Firefox
- `--private-window`: Private browsing mode
- `--headless`: Headless mode
- `--new-window`: Open in new window

### Edge
- `--inprivate`: InPrivate mode
- `--headless`: Headless mode
- `--new-window`: Open in new window

### Safari
- `--new-window`: Open in new window
- Note: Safari doesn't support headless or incognito via command line

## Error Handling

The script includes comprehensive error handling for:

### Common Errors
1. **Browser Not Found**: Returns error if browser executable is not found
2. **Invalid URL**: Validates URL format and adds https:// if missing
3. **Permission Issues**: Handles permission errors when trying to launch browsers
4. **Platform-Specific Issues**: Handles OS-specific error conditions

### Troubleshooting
1. **Browser not found**: Install the browser or specify the correct path
2. **Permission denied**: Run script with appropriate permissions
3. **URL not opening**: Check URL format and network connectivity
4. **Platform issues**: Verify browser installation on your platform

## Testing

To test the browser opener:

```bash
# Test with default browser
python scripts/open_browser.py --url https://www.google.com

# Test with specific browser
python scripts/open_browser.py --url https://www.google.com --browser chrome

# Test with different options
python scripts/open_browser.py --url https://www.google.com --browser firefox --new-window --incognito
```