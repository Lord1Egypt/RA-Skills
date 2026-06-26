# Bittensor SN85 VidAIo Miner Skill

Deploy and optimize video compression/upscaling miners on Bittensor Subnet 85 (VidAIo).

## Overview

**Subnet:** 85 (VidAIo/Vibe)  
**Task:** Video compression (HEVC/AV1) and upscaling (SD→HD, HD→4K)  
**Repo:** https://github.com/Cazure8/vidaio-subnet  
**GPU Required:** RTX 3090+ (4090 recommended)  
**Platform:** Vast.ai recommended (cheap GPU rentals)

## Architecture

SN85 runs **dual miners** (compression + upscaling) with separate backend services:

```
Validator → Miner (axon) → Backend Service (Flask) → ffmpeg/video2x
```

**4 PM2 Processes:**
1. `video-miner` — Upscaling axon (receives SD2HD/HD24K tasks)
2. `video-miner-compress` — Compression axon (receives HEVC/AV1 tasks)
3. `video-upscaler` — Backend service (port 19000)
4. `video-compressor` — Backend service (port 19001)

## Prerequisites

```bash
# Bittensor wallet with at least 0.4τ for registration
btcli wallet create --wallet.name moltypython
btcli wallet new_hotkey --wallet.name moltypython --hotkey mining
btcli wallet new_hotkey --wallet.name moltypython --hotkey mining2

# Register both hotkeys
btcli subnet register --netuid 85 --wallet.name moltypython --wallet.hotkey mining
btcli subnet register --netuid 85 --wallet.name moltypython --wallet.hotkey mining2
```

## Vast.ai Setup

### 1. Launch Instance

**Requirements:**
- RTX 4090 (24GB VRAM)
- 64GB+ disk
- Ubuntu 24.04 (NVENC support verified)
- **At least 4 open TCP ports** (SSH + 3 miner ports)

**Template:**
```
Image: nvidia/cuda:13.0.2-cudnn9-devel-ubuntu24.04
Disk: 64GB
GPU: RTX 4090
```

### 2. Critical Port Configuration

⚠️ **Vast.ai occupies ports 8080, 11111, 18384 by default** (Jupyter, Portal, Syncthing). Do NOT use these!

**Recommended mapping:**
```
Internal → External (Vast assigns)
19000    → 26565  (upscaler backend)
19001    → 26833  (compressor backend)
22       → XXXXX  (SSH)
```

Vast.ai routes external ports through Caddy reverse proxy. You MUST configure Caddy to forward without auth:

```bash
# Edit /etc/caddy/Caddyfile
sudo tee /etc/caddy/Caddyfile << 'EOF'
:8384 {
    reverse_proxy localhost:19000
}

:1111 {
    reverse_proxy localhost:19001
}
EOF

sudo systemctl reload caddy
```

**Verify external access:**
```bash
curl -I http://<VAST_PUBLIC_IP>:<EXTERNAL_PORT>
# Should return 404 from Bittensor axon, NOT 401 Unauthorized
```

## Installation

```bash
# Clone repo
cd /root
git clone https://github.com/Cazure8/vidaio-subnet.git
cd vidaio-subnet

# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Copy wallets from local machine
scp -P <VAST_SSH_PORT> -r ~/.bittensor/wallets/moltypython root@<VAST_IP>:/root/.bittensor/wallets/
```

### Install Optimized ffmpeg

System ffmpeg lacks NVENC. Use BtbN static build:

```bash
cd /tmp
wget https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz
tar xf ffmpeg-master-latest-linux64-gpl.tar.xz
sudo cp ffmpeg-master-latest-linux64-gpl/bin/* /usr/local/bin/
ffmpeg -version | grep libsvtav1  # Verify AV1 support
```

### Install video2x for Upscaling

```bash
pip install video2x==6.3.1
# Downloads NCNN models automatically on first run
```

## PM2 Startup (Critical!)

⚠️ **MUST set PYTHONPATH or imports fail!**

```bash
cd /root/vidaio-subnet

# Upscaler miner (UID 165 in our case)
PYTHONPATH=/root/vidaio-subnet pm2 start venv/bin/python --name video-miner --interpreter none \
  -- neurons/miner.py --netuid 85 --subtensor.network finney \
  --wallet.name moltypython --wallet.hotkey mining \
  --axon.port 19000 --axon.external_port 26565 --logging.debug

# Compressor miner (UID 78 in our case)
PYTHONPATH=/root/vidaio-subnet pm2 start venv/bin/python --name video-miner-compress --interpreter none \
  -- neurons/miner_compress.py --netuid 85 --subtensor.network finney \
  --wallet.name moltypython --wallet.hotkey mining2 \
  --axon.port 19001 --axon.external_port 26833 --logging.debug

# Upscaler backend
PYTHONPATH=/root/vidaio-subnet pm2 start venv/bin/python --name video-upscaler --interpreter none \
  -- services/upscaling/server.py

# Compressor backend
PYTHONPATH=/root/vidaio-subnet pm2 start venv/bin/python --name video-compressor --interpreter none \
  -- services/compress/server.py

pm2 save
pm2 startup  # Auto-start on reboot
```

**Verify ports match registration:**
```bash
pm2 logs video-miner --lines 50 --nostream | grep "AxonInfo.*26565"
pm2 logs video-miner-compress --lines 50 --nostream | grep "AxonInfo.*26833"
# If wrong port appears, kill and restart with correct --axon.external_port
```

## Optimizations (Production-Ready)

### 1. Upscaler Speed Fix

**Problem:** Default config tries 4x upscaling on 4K input → GPU OOM/truncation.

**Fix:** Dynamic scaling based on input resolution.

Edit `/root/vidaio-subnet/services/upscaling/server.py`:

```python
# Around line 60, replace hardcoded scale=4 with:
input_width = int(probe['streams'][0]['width'])
if input_width >= 3840:  # 4K input
    scale = 2  # 4K → 8K
elif input_width >= 1920:  # HD input
    scale = 2  # HD → 4K
else:  # SD input
    scale = 4  # SD → HD
```

**Restart:** `pm2 restart video-upscaler`

### 2. Compressor Speed Optimization

**Problem:** AV1 encoding takes 90-155s (validator timeout is ~60s).

**Fixes:**

#### A. Use fastest AV1 preset
Edit `/root/vidaio-subnet/services/compress/utils/encoder_configs.py`:

```python
# Line ~40, change preset for all scene types:
"preset": "12",  # Was 10, now 12 (fastest)
```

#### B. Add encoding timeout
Edit `/root/vidaio-subnet/services/compress/utils/encode_video.py`:

```python
# Around line 80, add timeout to subprocess.run():
result = subprocess.run(
    cmd,
    capture_output=True,
    text=True,
    timeout=45  # Kill if exceeds 45s
)
```

#### C. Skip VMAF validation (trust lookup table)
Edit `/root/vidaio-subnet/services/compress/compression_optimized.py`:

```python
# Line ~120, set:
skip_vmaf = True  # Saves 5-10s per task
```

**Restart:** `pm2 restart video-compressor`

### 3. Network Timeout Fix

**Problem:** Large video downloads timeout with default 5s httpx connect timeout.

Edit `/root/vidaio-subnet/vidaio_subnet_core/utilities/file_handler.py`:

```python
# Line ~30, replace httpx.AsyncClient() with:
async with httpx.AsyncClient(
    timeout=httpx.Timeout(30.0, read=120.0, write=30.0, pool=None)
) as client:
```

**Restart:** `pm2 restart video-miner video-miner-compress`

### 4. DNS Fix (Docker resolver issue)

```bash
echo -e "nameserver 8.8.8.8\nnameserver 1.1.1.1" | sudo tee /etc/resolv.conf
```

## Monitoring

### Check Registration Status

```bash
btcli wallet overview --wallet.name moltypython --wallet.hotkey mining --subtensor.network finney
btcli wallet overview --wallet.name moltypython --wallet.hotkey mining2 --subtensor.network finney
```

Look for:
- UID assigned (e.g., 165, 78)
- INCENTIVE > 0 (means earning)
- EMISSION > 0 (τ per day)

### Check Task Activity

```bash
# Upscaler
pm2 logs video-miner --lines 50 | grep "Receiving"

# Compressor
pm2 logs video-miner-compress --lines 50 | grep "Receiving"
```

Healthy output:
```
✅✅✅ Receiving SD2HD Request from validator: 5EUq... with uid: 1
🛜🛜🛜 Receiving CompressionRequest from validator: 5EUq... with uid: 1 | VMAF: 89.0 | Codec: hevc
```

### Backend Response Times

```bash
# Check upscaler timing
pm2 logs video-upscaler --lines 100 | grep "Completed\|took"

# Check compressor timing
pm2 logs video-compressor --lines 100 | grep "Completed\|took"
```

Target: <50s per task (validator timeout ~60s)

## Troubleshooting

### 1. Zero Incentive Despite Tasks

**Symptoms:** Receiving validator requests but INCENTIVE = 0.00

**Causes:**
- Tasks timing out (>60s)
- Output quality below threshold (VMAF, resolution)
- Tasks failing silently (check backend logs)

**Debug:**
```bash
pm2 logs video-compressor --lines 200 | grep -i "error\|timeout\|failed"
pm2 logs video-upscaler --lines 200 | grep -i "error\|timeout\|failed"
```

### 2. "ModuleNotFoundError: No module named 'services'"

**Cause:** Missing PYTHONPATH

**Fix:** Kill all PM2 processes and restart with PYTHONPATH set (see PM2 Startup section)

### 3. Port Already in Use

**Cause:** Stale axon binding after restart

**Fix:**
```bash
pm2 kill  # Nuclear option
# Wait 10 seconds
# Restart all processes with PYTHONPATH
```

### 4. Validators Not Connecting (401 Unauthorized)

**Cause:** Caddy reverse proxy blocking with HTTP Basic Auth

**Fix:** Edit Caddyfile to remove auth (see Port Configuration section above)

### 5. "UnknownSynapseError" in Logs

**Normal!** Validators probe all UIDs with various synapse types. Ignore unless frequent.

## Expected Performance

**Upscaler (video2x + NVENC):**
- SD→HD: 20-35s
- HD→4K: 30-50s

**Compressor:**
- HEVC: 15-30s
- AV1: 25-45s (with preset 12)

Both should complete within 60s validator deadline.

## Costs

**Vast.ai RTX 4090:** ~$0.30-0.50/hour (~$220-360/month)  
**Registration:** 0.19τ per hotkey (0.38τ total)  
**SN85 emissions:** Variable (depends on competition/performance)

## Maintenance

### Daily Checks
```bash
ssh -p <PORT> root@<VAST_IP> "pm2 list && uptime"
```

### Weekly
- Check wallet balance growth
- Review PM2 restart counts (high = instability)
- Update vidaio-subnet repo if new commits

### If Deregistered
- Check balance (need 0.19τ to re-register)
- Review logs for errors before last known task
- Re-register: `btcli subnet register --netuid 85 --wallet.name moltypython --wallet.hotkey <HOTKEY>`

## References

- **VidAIo Subnet:** https://github.com/Cazure8/vidaio-subnet
- **Bittensor Docs:** https://docs.bittensor.com
- **Vast.ai:** https://vast.ai
- **VibeMiner (Ridges collab):** https://github.com/maxquick/VibeMiner

## Version History

- **2.1.0** (Mar 15, 2026): Added compression optimizations, network timeout fix, verified 3+ day stable deployment
- **2.0.0** (Mar 7, 2026): NVENC optimizations, dynamic upscaling, Caddy auth fix
- **1.0.0** (Feb 13, 2026): Initial deployment
