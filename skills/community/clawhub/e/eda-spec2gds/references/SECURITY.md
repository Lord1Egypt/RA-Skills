# Security and Safety Guide

**Version:** 1.0.0  
**Last Updated:** 2026-03-20

---

## Overview

This document provides detailed security guidance for the `eda-spec2gds` skill. The skill operates in two modes:

1. **Core Skill Operations** - File-based, safe operations (RTL generation, report collection)
2. **Optional Setup Scripts** - System-modifying operations (package installation, Docker setup)

Understanding this distinction is critical for safe deployment.

---

## Core Skill Operations (Safe)

The following operations are **file-based only** and do not modify system state:

| Operation | Description | Risk Level |
|-----------|-------------|------------|
| RTL Generation | Creates Verilog files in project directory | ✅ Safe |
| Testbench Creation | Creates testbench files | ✅ Safe |
| Spec Normalization | Reads/writes YAML/Markdown files | ✅ Safe |
| Lint/Simulation | Runs yosys/iverilog on local files | ✅ Safe |
| Synthesis | Runs yosys synthesis | ✅ Safe |
| Report Collection | Parses log files, generates summaries | ✅ Safe |
| Dashboard Serving | Local HTTP server on specified port | ✅ Safe |

These operations:
- Only read/write within the skill's project directories
- Do not require network access (except optional dashboard)
- Do not require elevated privileges
- Do not modify system configuration

---

## Optional Setup Scripts (Requires Review)

The following scripts **modify system state** and require careful review:

### `scripts/install_ubuntu_24_mvp.sh`

**What it does:**
```bash
# Installs system packages
sudo apt-get install yosys iverilog verilator gtkwave klayout docker.io python3-pip python3-venv

# Enables Docker service
sudo systemctl enable --now docker

# Adds user to Docker group (privilege escalation potential)
sudo usermod -aG docker $USER

# Creates Python virtual environment
python3 -m venv ~/.venvs/openlane
pip install openlane==2.3.10
```

**Security implications:**
- ⚠️ **Docker group membership**: Users in the `docker` group can effectively gain root access via container escapes
- ⚠️ **System package installation**: Modifies `/usr/bin`, `/etc`, system libraries
- ⚠️ **Network access**: Downloads packages from apt archives, PyPI, Docker Hub
- ⚠️ **Service enablement**: Starts Docker daemon (persistent background service)

**Recommended usage:**
- Run only in isolated VMs or development workstations
- Do NOT run on shared production systems without audit
- Consider manual installation with reviewed package versions

### `scripts/bootstrap_eda_demo.sh`

**What it does:**
- Runs the installation script above
- Initializes demo project directories
- Executes full EDA flow end-to-end
- Pulls OpenLane Docker image (~2-3GB)

**Security implications:**
- Inherits all risks from `install_ubuntu_24_mvp.sh`
- Additional network egress for Docker image pull
- Creates files in user's home directory and workspace

---

## Threat Model

### What Could Go Wrong

1. **Docker Privilege Escalation**
   - Adding a user to the `docker` group grants near-root privileges
   - Malicious containers could escape and access host filesystem
   - **Mitigation**: Use dedicated VM, not shared workstations

2. **Supply Chain Attacks**
   - Packages from apt/PyPI/Docker Hub could be compromised
   - **Mitigation**: Pin versions, use trusted mirrors, verify checksums

3. **Resource Exhaustion**
   - OpenLane runs can consume significant CPU/RAM/disk
   - Docker images can fill disk space
   - **Mitigation**: Set resource limits, monitor disk usage

4. **Network Exposure**
   - Dashboard server binds to local port (default 8765)
   - **Mitigation**: Bind to localhost only, use firewall rules

### What This Skill Does NOT Do

- ❌ No external API calls (except package downloads during setup)
- ❌ No telemetry or data exfiltration
- ❌ No persistent backdoors or scheduled tasks
- ❌ No modification of system security settings
- ❌ No access to user credentials or secrets

---

## Safe Deployment Patterns

### Pattern 1: Isolated VM (Recommended)

```bash
# Create disposable VM (e.g., Multipass, Vagrant, cloud VM)
multipass launch --name eda-sandbox --cpus 4 --memory 8G --disk 50G

# Install skill inside VM
# Run installation scripts
# Use for EDA work
# Destroy VM when done
multipass delete eda-sandbox
multipass purge
```

**Pros:** Complete isolation, easy to destroy/recreate  
**Cons:** Resource overhead, file sharing complexity

### Pattern 2: Docker-in-Docker

```bash
# Run OpenClaw inside Docker container with Docker socket mounted
docker run -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/workspace:/workspace \
  your-openclaw-image
```

**Pros:** Good isolation, portable  
**Cons:** Docker socket access still grants host access

### Pattern 3: Dedicated Workstation

```bash
# Use a dedicated development machine
# Not shared with production workloads
# Regular security updates
# Firewall rules limiting outbound connections
```

**Pros:** Full performance, easy debugging  
**Cons:** Hardware cost, maintenance overhead

### Pattern 4: Manual Installation (Most Secure)

```bash
# Review and install packages manually
sudo apt-get install yosys iverilog verilator

# Create virtualenv manually
python3 -m venv ~/.venvs/openlane
source ~/.venvs/openlane/bin/activate
pip install openlane==2.3.10  # Review package first

# Pull Docker image after review
docker pull efabless/openlane:latest

# Run skill without using install scripts
```

**Pros:** Full control, audited every step  
**Cons:** More effort, requires EDA knowledge

---

## Checklist Before Running Installation Scripts

- [ ] I am running this in an isolated/development environment
- [ ] I have reviewed `scripts/install_ubuntu_24_mvp.sh` line by line
- [ ] I understand Docker group membership implications
- [ ] I have verified network destinations (apt, PyPI, Docker Hub)
- [ ] I have sufficient disk space (~10GB for tools + images)
- [ ] I am not running on a production/shared system
- [ ] I have backups of important data
- [ ] I understand how to uninstall/remove the tools

---

## Uninstallation

To remove all EDA tools installed by this skill:

```bash
# Remove apt packages
sudo apt-get remove --purge yosys iverilog verilator gtkwave klayout docker.io

# Remove Python virtualenv
rm -rf ~/.venvs/openlane

# Remove Docker images
docker rmi efabless/openlane:latest

# Remove user from Docker group (optional)
sudo gpasswd -d $USER docker

# Remove skill files
rm -rf /path/to/eda-spec2gds
```

Note: Removing Docker group membership requires logout/login to take effect.

---

## Reporting Security Issues

If you discover a security vulnerability:

1. Do NOT run the skill until the issue is resolved
2. Report to the skill maintainer immediately
3. Provide details: affected scripts, potential impact, reproduction steps

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-20 | Initial security documentation |

---

**Remember:** When in doubt, review the scripts first and run in an isolated environment. The core skill operations are safe, but the optional installation scripts modify your system and should be treated with appropriate caution.
