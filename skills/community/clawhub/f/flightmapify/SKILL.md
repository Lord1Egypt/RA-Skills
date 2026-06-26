---
name: flightmapify
version: 1.4.6
description: Find cheapest flights and create interactive flight route maps with real-time flight search.
author: rudy2steiner
license: MIT
tags: [flights, maps, routing, flyai, travel, interactive]
---

# FlightMapify Skill

## Overview
FlightMapify creates interactive flight route maps that allow users to search for flights between cities and visualize flight paths on an interactive map. Unlike TravelMapify which focuses on ground travel routes, FlightMapify is specifically designed for air travel planning.

## Features
- **Optimized server management** with automatic port conflict resolution
- **Flask-based flight search server** for robust API handling
- Interactive flight search between origin and destination cities
- Real-time flight data from FlyAI (Fliggy MCP)
- **Support for both direct and connecting flights** with complete route information
- Visual flight path display on Amap maps with animated markers
- Direct booking links to Fliggy
- Support for both domestic and international flights
- Single-date input for simple flight queries
- **Enhanced UX** with loading states, notifications, and auto-hiding messages
- **Professional error handling** with user-friendly feedback
- **Environment variable configuration** for API Key management
- **Complete connecting flight details** including transfer cities, prices, and durations

## Usage

### Environment Setup
FlightMapify is an OpenClaw skill that supports optional user-configurable FlyAI API Key.

**Configuration Options:**

1. **User-provided API Key** (Recommended - avoids rate limiting)
   
   Get your API key from: https://flyai.open.fliggy.com/console
   
   ```bash
   export FLYAI_API_KEY=your_api_key_here
   ```

2. **FlyAI Built-in API Key** (Default)
   - If `FLYAI_API_KEY` is not configured, FlyAI will use its built-in default API key
   - Built-in key may have rate limits for frequent requests
   - No configuration required for basic usage

**Environment Variables:**
- `FLYAI_API_KEY`: Your FlyAI API key for flight search (optional, recommended to avoid rate limits)
- `FLYAI_API_TOKEN`: Alternative API token variable (optional)
- `FLYAI_TOKEN`: Another API token variable for compatibility (optional)

**Note:** `FLYAI_API_KEY` is optional. If not set, FlyAI will use its built-in default API key, but this may be subject to rate limiting for frequent requests.

### Generate Flight Map
```bash
# Generate a flight map between two cities
flightmapify --origin "北京" --destination "上海" --date "2026-04-22" --output flight-beijing-shanghai.html
```

## Parameters
- `--origin`: Departure city (required)
- `--destination`: Arrival city (required)  
- `--date`: Travel date in YYYY-MM-DD format (required)
- `--output`: Output HTML file name (required)
- `--port`: HTTP server port (default: 9000)

## Integration
FlightMapify integrates with the existing FlyAI skill for real-time flight search and booking capabilities. It uses Amap for map visualization and provides a clean, focused interface for flight planning.

### API Keys
- **Amap API Key**: Uses built-in default API key (no user key required)
- **Custom Amap Key**: Set `AMAP_API_KEY` environment variable to use your own key

### Local Server Architecture
- Flight search server runs locally on dynamic ports
- HTTP server serves from OpenClaw workspace directory
- All URLs use localhost for security and simplicity

## Technical Details

### Server Architecture
- **Flight Search Server**: Flask-based server on configurable port (default: 8790)
- **HTTP Server**: Lightweight server for map display (default: 9000)
- **Port Management**: Automatic port conflict resolution and server health checks

### Flight Data
- **Direct Flights**: Non-stop flights with price, duration, and booking links
- **Connecting Flights**: Multi-segment flights with transfer cities, complete pricing, and duration
- **Route Visualization**: Interactive map showing flight paths with animated markers
- **Real-time Data**: Live search results from FlyAI API

### Environment Variables
- `FLYAI_API_KEY`: Your FlyAI API key for flight search (optional, recommended to avoid rate limits)
- `FLYAI_API_TOKEN`: Alternative API token variable (optional)
- `FLYAI_TOKEN`: Another API token variable for compatibility (optional)

**Note:** `FLYAI_API_KEY` is optional. If not set, FlyAI will use its built-in default API key, but this may be subject to rate limiting for frequent requests. Setting your own API key is recommended for production use or high-volume requests.

## Changelog

### Version 1.4.0 (2026-04-16)
- ✅ Reverted to optional API Key configuration
- ✅ Support for FlyAI built-in default API key (may have rate limits)
- ✅ User-provided API Key recommended to avoid rate limiting
- ✅ Updated documentation with clear configuration options
- ✅ Enhanced input box width optimization for better UI
- ✅ Fixed city suggestion box width for better UX

### Version 1.3.0 (2026-04-16)
- ✅ Removed default API Key - now requires explicit user configuration
- ✅ Added clear error message when FLYAI_API_KEY is not set
- ✅ Updated documentation to reflect required API Key configuration
- ✅ Improved security by removing hardcoded API keys

### Version 1.2.0 (2026-04-16)
- ✅ Fixed connecting flight search functionality
- ✅ Added complete connecting flight details (route cities, prices, durations)
- ✅ Implemented OpenClaw skill configuration with user-configurable API Key
- ✅ Added automatic fallback to default FlyAI API Key when not configured
- ✅ Updated server manager to use Flask-based server
- ✅ Enhanced server management with .env file support
- ✅ Fixed API Key configuration issues (trial limit errors)
- ✅ Improved error handling and user feedback
- ✅ Removed flight-search-server-simple.py (now using Flask-based server exclusively)

### Version 1.1.0
- Initial release with basic flight search and map visualization

## Examples
```bash
# Basic flight map
flightmapify --origin "北京" --destination "阿克苏" --date "2026-04-22" --output beijing-aksu-flight.html

# With custom port
flightmapify --origin "上海" --destination "乌鲁木齐" --date "2026-05-01" --output shanghai-urumqi-flight.html --port 8080
```

## Troubleshooting Common Problems

### 🔴 **"No flights found" or Empty Results**

**Possible Causes:**
- **API Rate Limits**: Built-in FlyAI API key has trial limits
- **Route Availability**: Remote destinations may have limited flight options
- **Date Too Far**: Airlines may not have published schedules for distant dates

**Solutions:**
1. **Get your own FlyAI API key** from https://flyai.open.fliggy.com/console
   ```bash
   export FLYAI_API_KEY=your_api_key_here
   ```
2. **Try closer dates** (within 3-6 months)
3. **Test with major city pairs** first (Beijing-Shanghai, Guangzhou-Shenzhen)

### 🔴 **404 File Not Found Error**

**Cause:** HTML file generated in wrong directory

**Solution:**
- The skill now uses **dynamic workspace detection**
- Files are always generated in your OpenClaw workspace directory
- Check that your workspace contains `AGENTS.md` or `SOUL.md`

### 🔴 **Character Encoding Issues (乱码)**

**Symptoms:** Chinese cities show as garbled text like "阿克苯"

**Cause:** URL parameter double-decoding

**Solution:**
- This is **fixed in version 1.4.0**
- Ensure you're using the latest version from ClawHub
- If issues persist, restart your terminal session

### 🔴 **Flight Search Server Won't Start**

**Symptoms:** "Failed to start flight search server on port XXXX"

**Causes & Solutions:**
1. **Port already in use**: Server automatically finds next available port
2. **Missing dependencies**: Ensure `flyai` CLI is installed
   ```bash
   npm install -g @openclaw/flyai
   ```
3. **Permission issues**: Run with appropriate permissions

### 🔴 **API Key Configuration Issues**

**Problem:** Still getting rate limits after setting API key

**Solutions:**
1. **Verify key is set correctly**:
   ```bash
   echo $FLYAI_API_KEY
   ```
2. **Check FlyAI config file**:
   ```bash
   cat ~/.flyai/config.json
   ```
3. **Use environment variable method** (more reliable):
   ```bash
   export FLYAI_API_KEY=sk_your_actual_key
   flightmapify --origin "北京" --destination "上海" --date "2026-04-25" --output test.html
   ```

### 🔴 **Map Not Loading or JavaScript Errors**

**Causes:**
- Amap API key issues
- Network connectivity problems
- Browser security restrictions

**Solutions:**
1. **Amap key is built-in** - no user configuration needed
2. **Open HTML file via HTTP server** (not file:// protocol)
3. **Check browser console** for specific error messages

### 🟡 **Performance Issues with Many Flights**

**Symptoms:** Slow loading with routes having many connecting options

**Solutions:**
- The system shows **top 20 flights** by default
- Use **direct flights only** for faster results if needed
- Close other browser tabs to free memory

### 🔧 **Debugging Tips**

1. **Check server logs**:
   ```bash
   # Look for Python server output in your terminal
   ```

2. **Test FlyAI CLI directly**:
   ```bash
   flyai search-flight --origin "北京" --destination "上海" --dep-date "2026-04-25"
   ```

3. **Verify file locations**:
   ```bash
   ls -la ~/.openclaw/workspace/*.html
   ```

4. **Check port availability**:
   ```bash
   lsof -i :9000  # Replace with your port
   ```

### 📞 **When to Contact Support**

Contact the skill maintainer if:
- You've tried all troubleshooting steps above
- The issue persists with major city pairs (Beijing-Shanghai)
- You see consistent errors across different dates/routes
- The HTML file generates but shows completely blank map

**Include in your report:**
- OpenClaw version (`openclaw --version`)
- Skill version (check SKILL.md)
- Exact command used
- Error messages from terminal
- Screenshot of the HTML page (if applicable)