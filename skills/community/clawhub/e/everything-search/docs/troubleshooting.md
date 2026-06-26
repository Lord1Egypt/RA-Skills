# Troubleshooting Guide

Common issues and solutions for Everything Search skill.

## Table of Contents

- [Connection Issues](#connection-issues)
- [API Errors](#api-errors)
- [Search Problems](#search-problems)
- [Performance Issues](#performance-issues)
- [FAQ](#faq)

---

## Connection Issues

### Problem: "Cannot connect to Everything HTTP Server"

**Symptoms:**
```
✗ Connection failed: [WinError 10061] 由于目标计算机积极拒绝，无法连接
```

**Root Cause:**
- HTTP server is not enabled in Everything
- Everything is not running
- Wrong port number

**Solution:**

1. **Verify Everything is running**
   ```bash
   tasklist | findstr Everything
   ```
   Should show at least one `Everything.exe` process.

2. **Check HTTP Server is enabled**
   - Open Everything window
   - Press `Ctrl+P`
   - Click "HTTP Server"
   - Confirm `☑ Enable HTTP server` is CHECKED
   - Confirm Port is `2853`

3. **Restart Everything**
   - Right-click tray icon → Exit
   - Restart Everything
   - Wait 3-5 seconds

4. **Test connection**
   ```bash
   python scripts/check-config.py
   ```

---

### Problem: "Port 2853 is CLOSED"

**Symptoms:**
```python
✗ Port 2853 is CLOSED (error code: 10061)
```

**Root Cause:**
- HTTP server not enabled
- Port blocked by firewall
- Different port configured

**Solution:**

1. **Check if port is listening**
   ```bash
   netstat -ano | findstr "2853"
   ```
   If no output, port is not listening.

2. **Enable HTTP server** (see above)

3. **Check firewall**
   - Windows Defender Firewall → Advanced settings
   - Inbound Rules → Find Everything
   - Ensure port 2853 is allowed

4. **Try different port**
   - Change to 8080 or 8081
   - Update scripts: `EverythingSearch(port=8080)`

---

## API Errors

### Problem: "HTTP Error 404: Not Found"

**Symptoms:**
```
✗ Search failed: HTTP Error 404: Not Found
```

**Root Cause:**
- Wrong API endpoint URL
- Using incorrect path prefix

**Solution:**

**Correct endpoint:**
```
http://127.0.0.1:2853/?search=关键词&json=1
```

**Wrong endpoints (will return 404):**
```
http://127.0.0.1:2853/everything/?search=关键词&json=1
http://127.0.0.1:2853/api/search?query=关键词&json=1
```

**Fix in code:**
```python
# ✓ Correct
url = f"http://127.0.0.1:2853/?search={encoded}&json=1"

# ✗ Wrong
url = f"http://127.0.0.1:2853/everything/?search={encoded}&json=1"
```

---

### Problem: "Invalid JSON response"

**Symptoms:**
```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1
```

**Root Cause:**
- Server returned HTML instead of JSON
- Missing `json=1` parameter

**Solution:**

Ensure URL includes `json=1`:
```python
url = f"http://127.0.0.1:2853/?search={keyword}&json=1"
```

---

## Search Problems

### Problem: "File size shows as 0 B"

**Symptoms:**
All files show size as `0 B` even though they have actual size.

**Root Cause:**
- Missing `size=1` parameter in API request

**Solution:**

Add `size=1` to URL:
```python
url = f"http://127.0.0.1:2853/?search={keyword}&json=1&size=1"
```

The provided scripts handle this automatically.

---

### Problem: "Chinese search returns garbled text"

**Symptoms:**
- Search returns no results for Chinese keywords
- Or returns incorrect results

**Root Cause:**
- Chinese characters not URL-encoded

**Solution:**

Always encode Chinese keywords:
```python
import urllib.parse

keyword = "数据资产"
encoded = urllib.parse.quote(keyword)
url = f"http://127.0.0.1:2853/?search={encoded}&json=1"
```

The provided scripts handle encoding automatically.

---

### Problem: "Search returns too many results"

**Symptoms:**
- Search returns thousands of results
- Slow performance

**Solution:**

1. **Limit results**
   ```python
   results = search.search("keyword", max_results=20)
   ```

2. **Add filters**
   ```python
   # By file type
   results = search.search("报告", file_type="pdf")
   
   # By size
   results = search.search("视频", min_size="10mb")
   
   # By path
   results = search.search("文档", path="D:\\Documents")
   ```

3. **Use more specific keywords**
   ```python
   # Instead of "数据"
   results = search.search("数据资产 报告")
   ```

---

### Problem: "Search returns no results"

**Symptoms:**
```
Found 0 results
```

**Root Cause:**
- Keyword too specific
- File not indexed
- Wrong search syntax

**Solution:**

1. **Try simpler keyword**
   ```python
   # Instead of "数据资产（Data Catalog）"
   results = search.search("数据资产")
   ```

2. **Check file exists**
   - Open Everything GUI
   - Search manually to verify file exists

3. **Use wildcards**
   ```python
   results = search.search("*.pdf")
   ```

4. **Check Everything index**
   - Open Everything → Tools → Options → Indexes
   - Ensure drive/folder is indexed

---

## Performance Issues

### Problem: "Search is slow"

**Symptoms:**
- Search takes > 2 seconds
- High CPU usage

**Solution:**

1. **Reduce max_results**
   ```python
   results = search.search("keyword", max_results=10)
   ```

2. **Add filters to narrow search**
   ```python
   results = search.search("keyword", file_type="pdf")
   ```

3. **Check Everything database**
   - Open Everything → Tools → Options → Indexes
   - Rebuild index if needed

4. **Close other applications**
   - High system load can slow Everything

---

## FAQ

### Q: Can I use a different port?

**A:** Yes. Change port in Everything settings and update scripts:
```python
search = EverythingSearch(port=8080)
```

### Q: Does this work on Linux/Mac?

**A:** No. Everything is Windows-only. For Linux, consider `fd` or `locate`. For Mac, use `mdfind`.

### Q: Can I search network drives?

**A:** Yes, if network drives are indexed by Everything:
1. Open Everything → Tools → Options → Indexes
2. Add network drive to folders
3. Wait for indexing to complete

### Q: How do I search for files modified today?

**A:** Use date filter:
```python
results = search.search("文档", modified_after="today")
```

Or in Everything syntax:
```python
results = search.search("文档 dm:today")
```

### Q: Can I search file contents?

**A:** No. Everything only searches filenames and paths, not file contents. For content search, use `grep` or `ripgrep`.

### Q: How do I exclude certain folders?

**A:** Use exclude_path parameter:
```python
results = search.search("报告", exclude_path="C:\\Windows")
```

Or in Everything syntax:
```python
results = search.search("报告 !path:\"C:\\Windows\"")
```

### Q: Why are there two Everything processes?

**A:** One is a Windows service (for system-wide indexing), the other is the user interface. Both are normal.

### Q: HTTP server won't start after config change

**A:** You must completely exit and restart Everything:
1. Right-click tray icon → Exit
2. Wait for icon to disappear
3. Restart Everything
4. Wait 3-5 seconds

---

## Getting Help

If you still have issues:

1. **Run diagnostic**
   ```bash
   python scripts/diagnose.py
   ```

2. **Check logs**
   - Everything doesn't have detailed logs
   - Check Python error messages

3. **Verify configuration**
   - See `docs/configuration.md`
   - Follow step-by-step guide

4. **Report issue**
   - GitHub Issues
   - Include diagnostic output
   - Mention Everything version

---

**Last Updated:** 2024-04-02  
**Version:** 1.0.0
