#!/data/data/com.termux/files/usr/bin/bash
# phone_node_setup.sh — run this in Termux to make any Android a compute node.
# After this runs, Pi can route inference jobs to this phone.
#
# Usage: paste this URL in Termux browser, or:
#   curl -s http://albionwakes.com/phone_setup.sh | bash

set -e

echo "=== Albion Phone Node Setup ==="
echo "Installing packages..."
pkg update -y -q
pkg install -y curl wget python3 openssh 2>/dev/null

echo "Installing Ollama..."
ARCH=$(uname -m)
if [ "$ARCH" = "aarch64" ]; then
    OLLAMA_URL="https://github.com/ollama/ollama/releases/latest/download/ollama-linux-arm64"
else
    OLLAMA_URL="https://github.com/ollama/ollama/releases/latest/download/ollama-linux-amd64"
fi

mkdir -p $HOME/bin
wget -q -O $HOME/bin/ollama "$OLLAMA_URL"
chmod +x $HOME/bin/ollama
export PATH="$HOME/bin:$PATH"

# Persist PATH
grep -q 'albion-node' $HOME/.bashrc 2>/dev/null || echo '# albion-node' >> $HOME/.bashrc
grep -q '$HOME/bin' $HOME/.bashrc 2>/dev/null || echo 'export PATH="$HOME/bin:$PATH"' >> $HOME/.bashrc

echo "Pulling default model (qwen2.5:0.5b — 394MB)..."
$HOME/bin/ollama pull qwen2.5:0.5b

# Write a startup script
cat > $HOME/start_node.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
export PATH="$HOME/bin:$PATH"
export OLLAMA_HOST=0.0.0.0:11434
echo "Starting Ollama node on port 11434..."
ollama serve
EOF
chmod +x $HOME/start_node.sh

echo ""
echo "=== Done ==="
echo ""
echo "To start the node:"
echo "  bash ~/start_node.sh"
echo ""
echo "Then tell Albion your phone's IP address."
echo "  (Settings > WiFi > tap your network > IP address)"
echo ""
echo "Albion registers it with:"
echo "  python3 albion_phone_nodes.py register <name> <phone-ip>"
