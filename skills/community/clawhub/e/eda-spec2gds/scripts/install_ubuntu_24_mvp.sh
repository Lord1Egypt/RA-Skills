#!/usr/bin/env bash
set -euo pipefail

# Install MVP open-source EDA toolchain on Ubuntu 24.04.
# Run as a sudo-capable user: bash scripts/install_ubuntu_24_mvp.sh

if [[ "${EUID}" -eq 0 ]]; then
  echo "Please run as a regular user with sudo access, not root." >&2
  exit 1
fi

sudo apt-get update
sudo apt-get install -y \
  yosys \
  iverilog \
  verilator \
  gtkwave \
  klayout \
  docker.io \
  python3-pip \
  python3-venv

sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"

python3 -m venv "$HOME/.venvs/openlane"
# shellcheck disable=SC1091
source "$HOME/.venvs/openlane/bin/activate"
pip install --upgrade pip
pip install openlane==2.3.10

echo
echo "Installation finished. Next steps:"
echo "1. Re-login or run: newgrp docker"
echo "2. Pull image: docker pull efabless/openlane:latest"
echo "3. Verify env: skills/eda-spec2gds/scripts/check_env.sh"
