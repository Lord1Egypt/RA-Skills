# Ubuntu 24.04 Setup Guide

This guide covers installing the MVP toolchain using apt and pip.

## Required for MVP

- yosys
- iverilog
- vvp (provided by iverilog package)
- docker.io
- python3-pip / venv support

## Optional but Useful

- verilator
- gtkwave
- klayout
- openlane (Python package + Docker image)

## Recommended Install Order

1. Install apt packages for synthesis/simulation/runtime
2. Enable Docker service
3. Create Python virtualenv for OpenLane
4. Pull Docker image for OpenLane
5. Run `scripts/check_env.sh` to verify
6. Perform smoke test with `assets/examples/simple-fifo/`

## APT Package Installation

```bash
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
```

## Docker Setup

```bash
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
```

**Note:** If `newgrp docker` is inconvenient in automation scripts, log out and log back in after adding the user to the docker group.

## OpenLane Setup

Use a dedicated virtual environment:

```bash
python3 -m venv ~/.venvs/openlane
source ~/.venvs/openlane/bin/activate
pip install --upgrade pip
pip install openlane==2.3.10
```

Then pull the Docker image:

```bash
docker pull efabless/openlane:latest
```

## Risk Signals and Caveats

- OpenLane depends on Docker; if the Docker daemon is unavailable, backend runs will fail.
- GUI tools (`gtkwave`, `klayout`) are optional and may not be useful on headless servers.
- `newgrp docker` changes the current shell group context; some environments still require a full relogin.
- The `openlane` package version may evolve; pin a tested version for reproducibility.
