# Optimization History

Documented fixes from production deployment (Feb-Mar 2026).

## Timeline

### Feb 13, 2026: Initial Deployment
- Default vidaio-subnet config
- Immediate issues: tasks timing out, low success rate

### Mar 7, 2026 04:16 UTC: Upscaler NVENC Fix
**Problem:** Upscaler using CPU libx265 encoding (slow)  
**Fix:** Switched to h264_nvenc GPU encoding  
**Result:** 5-10x speedup (50s → 20-35s)

### Mar 7, 2026 18:45 UTC: Compressor Timeout Fix
**Problem:** No timeout on encoding, some tasks took 150s+  
**Fix:** Added 45s subprocess timeout  
**Result:** Tasks complete or abort within 60s deadline

### Mar 9, 2026 05:25 UTC: Caddy Auth Fix
**Problem:** Validators getting 401 Unauthorized  
**Cause:** Caddy routing external ports with HTTP Basic Auth  
**Fix:** Removed auth from Caddyfile reverse_proxy blocks  
**Result:** Validators could finally connect

### Mar 11, 2026 05:33 UTC: Dynamic Upscaling
**Problem:** video2x trying 4x scale on 4K input → GPU OOM  
**Fix:** Dynamic scale factor (4K→2x, HD→2x, SD→4x)  
**Result:** 100% completion rate on all resolutions

### Mar 13, 2026 05:19 UTC: Network Timeout Fix
**Problem:** httpx ConnectTimeout on large video downloads  
**Fix:** Increased connect timeout 5s → 30s, read 120s  
**Result:** Downloads complete reliably

### Mar 14, 2026 06:34 UTC: AI Pipeline Optimization
**Problem:** Feature extraction taking 90s (missed deadline)  
**Fix:** Reduced analyzed frames 150 → 10  
**Result:** Insufficient (encoding was real bottleneck)

### Mar 14, 2026 20:55 UTC: Encoder Speed Fix
**Problem:** libsvtav1 preset 10 too slow (29-155s)  
**Fixes:**  
- AV1 preset 10 → 12 (fastest)
- HEVC preset fast → ultrafast
- 45s hard timeout on ffmpeg subprocess  
**Result:** All tasks <50s or abort cleanly

## Current Stable Config (Mar 15, 2026)

**Uptime:** 3+ days  
**Task completion:** ~95%+ (estimated from validator activity)  
**Response times:**  
- Upscaler: 20-50s
- Compressor: 15-45s

**Still investigating:** Zero incentive/emission despite active task processing
