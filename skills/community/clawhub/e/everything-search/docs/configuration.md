# Configuration Guide

This guide walks you through configuring Everything HTTP Server for the Everything Search skill.

## Prerequisites

- Windows OS
- Everything 1.4+ installed
- Administrator access (optional, for installation)

## Step 1: Install Everything

1. Download Everything from: https://www.voidtools.com/
2. Run the installer
3. Choose installation location (recommended: `D:\Program Files\Everything\`)
4. Complete installation

## Step 2: Enable HTTP Server

**⚠️ Critical Step - Must be done manually in GUI**

1. **Open Everything**
   - Double-click Everything icon on desktop
   - Or search for "Everything" in Start menu

2. **Open Options**
   - Press `Ctrl+P` on keyboard
   - Or click menu: **Tools** → **Options**

3. **Navigate to HTTP Server**
   - In left panel, click **"HTTP Server"**

4. **Enable HTTP Server**
   - Check the box: **☑ Enable HTTP server**
   - Set **Port** to: `2853`
   - Leave other settings as default

5. **Save Settings**
   - Click **"OK"** button

## Step 3: Restart Everything

**Important:** Configuration changes require a full restart.

1. **Exit Everything completely**
   - Right-click Everything icon in system tray (bottom-right)
   - Select **"Exit"**
   - Wait for the icon to disappear

2. **Restart Everything**
   - Double-click Everything icon
   - Wait 3-5 seconds for full startup

## Step 4: Verify Configuration

### Method 1: Run Diagnostic Script

```bash
cd everything-search-skill
python scripts/check-config.py
```

Expected output:
```
✓ Everything process
✓ Port 2853
✓ HTTP server
✓ Search API
```

### Method 2: Manual Browser Test

1. Open web browser
2. Navigate to: `http://127.0.0.1:2853/`
3. You should see an HTML page with "Everything" title

### Method 3: Test Search

```bash
python examples/basic_search.py "test"
```

## Troubleshooting

### Problem: "Cannot connect to Everything HTTP Server"

**Solution:**
1. Verify Everything is running (check system tray)
2. Open Everything → Ctrl+P → HTTP Server
3. Confirm "Enable HTTP server" is CHECKED
4. Confirm port is 2853
5. Exit Everything completely
6. Restart Everything

### Problem: "Port 2853 is CLOSED"

**Solution:**
1. Check if another application is using port 2853
2. Try a different port (e.g., 8080)
3. Update port in all scripts and examples

### Problem: "API returns 404"

**Solution:**
- Use correct endpoint: `http://127.0.0.1:2853/?search=keyword&json=1`
- Do NOT use: `/everything/` or `/api/` prefixes

### Problem: "Chinese search returns no results"

**Solution:**
- Ensure URL encoding is applied
- The provided scripts handle this automatically
- For manual testing, use: `urllib.parse.quote("中文")`

## Configuration File Location

Everything configuration is stored at:
```
%APPDATA%\Everything\Everything.ini
```

Typical path:
```
C:\Users\<YourUsername>\AppData\Roaming\Everything\Everything.ini
```

**Note:** Editing this file directly does NOT enable HTTP server. You must use the GUI.

## Advanced Configuration

### Change Port

If port 2853 is unavailable:

1. Open Everything → Ctrl+P → HTTP Server
2. Change port to another value (e.g., 8080)
3. Update port in scripts:
   ```python
   search = EverythingSearch(port=8080)
   ```

### Enable Remote Access

**⚠️ Security Warning:** Only enable if needed and on trusted networks.

1. Open Everything → Ctrl+P → HTTP Server
2. Check "Allow remote access"
3. Configure firewall to allow incoming connections on port 2853

### Enable Authentication

For password protection:

1. Open Everything → Ctrl+P → HTTP Server
2. Check "Require authentication"
3. Set username and password
4. Update scripts to include authentication headers

## Next Steps

After successful configuration:

1. ✅ Run diagnostic: `python scripts/diagnose.py`
2. ✅ Try basic search: `python examples/basic_search.py "数据资产"`
3. ✅ Search photos: `python examples/search_photos.py "张三"`
4. ✅ Explore advanced features: `python examples/advanced_search.py --help`

## Support

- Documentation: See `SKILL.md` for detailed troubleshooting
- Issues: GitHub Issues
- Everything Help: https://www.voidtools.com/support/everything/
