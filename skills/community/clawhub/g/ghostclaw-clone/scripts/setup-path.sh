#!/usr/bin/env bash
# scripts/setup-path.sh — Ensures ~/.local/bin is in the user's PATH (where ghostclaw binary lives)

TARGET_DIR="$HOME/.local/bin"
BINARY_NAME="ghostclaw"

# Detect default shell profile
if [ -n "$ZSH_VERSION" ]; then
    PROFILE_FILE="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    PROFILE_FILE="$HOME/.bashrc"
else
    PROFILE_FILE="$HOME/.profile"
fi

if [[ ":$PATH:" == *":$TARGET_DIR:"* ]]; then
    echo "=> $TARGET_DIR is already in your PATH. Nothing to do."
else
    # shellcheck disable=SC2016  # single quotes are intentional: %s is a printf format, not a shell expansion
    printf '\n# Added by Ghostclaw Installer\nexport PATH="$PATH:%s"\n' "$TARGET_DIR" >> "$PROFILE_FILE"
    echo "=> Added $TARGET_DIR to $PROFILE_FILE"
    echo "=> Run 'source $PROFILE_FILE' or restart your terminal to use '$BINARY_NAME' from anywhere."
fi
