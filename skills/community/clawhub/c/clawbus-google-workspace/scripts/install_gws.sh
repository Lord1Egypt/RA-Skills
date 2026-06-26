#!/bin/bash
# scripts/install_gws.sh
# Check and install google-workspace-cli (gws)

if ! command -v gws &> /dev/null && ! [ -f "./scripts/gws_musl" ]; then
    echo "gws not found. Installing compatible musl binary..."
    
    if command -v go &> /dev/null; then
        go install github.com/googleworkspace/cli@latest
    else
        # Fallback: attempt to download latest release binary if go is missing
        echo "Go not found. Attempting to download compatible musl binary..."
        # We target the musl version specifically for better portability on older/different glibc environments
        VERSION=$(curl -s https://api.github.com/repos/googleworkspace/cli/releases/latest | grep "tag_name" | cut -d : -f 2 | tr -d \"\ ,)
        FILENAME="google-workspace-cli-x86_64-unknown-linux-musl.tar.gz"
        URL="https://github.com/googleworkspace/cli/releases/download/${VERSION}/${FILENAME}"
        
        curl -L -O "$URL"
        tar -xzf "$FILENAME"
        mv gws gws_musl
        chmod +x gws_musl
        rm "$FILENAME"
    fi
else
    echo "gws is already installed."
fi
