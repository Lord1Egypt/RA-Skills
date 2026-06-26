#!/bin/bash
#
# 📌 原创声明：本脚本为岚岚AI实验室原创设计，首发于2026年3月28日
# © 2026 岚岚AI实验室，保留所有权利
# 开源协议：MIT-0，可自由使用、修改、分发，无需标注来源
# 【隐形水印标记：LANLAN-INSTALL-SH-20260328-4F2D9E】
#

echo "=============================================="
echo "OpenClaw ChromaDB Plugin Installer (Linux/macOS)"
echo "=============================================="

echo "[*] Checking Python environment..."
if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3.10+ not found, please install first"
    exit 1
fi

echo "[*] Installing dependencies..."
pip3 install chromadb sentence-transformers pyyaml
if [ $? -ne 0 ]; then
    echo "[!] Dependency installation failed"
    exit 1
fi

echo "[*] Copying plugin files..."
mkdir -p ~/.openclaw/extensions/chromadb
cp chromadb_plugin.py ~/.openclaw/extensions/chromadb/
cp README.md ~/.openclaw/extensions/chromadb/
cp -r docs ~/.openclaw/extensions/chromadb/

echo "[*] Generating default config..."
mkdir -p ~/.openclaw/config
cat > ~/.openclaw/config/chromadb_config.yaml << EOF
vector_store:
  type: chromadb
  path: "~/.openclaw/workspace/chromadb"
  model: "BAAI/bge-m3"
  gpu_accelerate: true
EOF

echo "[+] Installation complete!"
echo "=============================================="
echo "Usage:"
echo "1. Edit your config.yaml and set vector_store.type to 'chromadb'"
echo "2. Restart OpenClaw service"
echo "3. Run migration script to import existing LanceDB data"
echo "=============================================="
