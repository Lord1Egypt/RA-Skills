#!/bin/bash
# Quick status check for SN85 miners

set -e

echo "=== PM2 Status ==="
pm2 list | grep video

echo -e "\n=== Recent Upscaler Activity ==="
pm2 logs video-miner --lines 20 --nostream 2>/dev/null | grep -E '(Receiving|Completed)' | tail -5

echo -e "\n=== Recent Compressor Activity ==="
pm2 logs video-miner-compress --lines 20 --nostream 2>/dev/null | grep -E '(Receiving|Completed)' | tail -5

echo -e "\n=== Uptime ==="
uptime

echo -e "\n=== Disk Usage ==="
df -h / | tail -1

echo -e "\n=== Port Bindings ==="
netstat -tuln | grep -E ':19000|:19001' || echo "WARNING: No miners bound to ports!"

echo -e "\n=== External Access Check ==="
PUBLIC_IP=$(curl -s ifconfig.me)
echo "Upscaler: http://$PUBLIC_IP:26565"
echo "Compressor: http://$PUBLIC_IP:26833"
