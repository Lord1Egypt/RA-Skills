# 🛠️ Installation Guide for CXM (ContextMachine)

CXM is a powerful tool, but it relies on some system-level libraries for clipboard support and AI embeddings. Follow these instructions for your specific Operating System.

## 🐧 Linux (Ubuntu, Debian, Fedora, Arch)

### 1. System Prerequisites
CXM uses `pyperclip` for clipboard integration, which requires a system clipboard manager.

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv xclip git
```

**Fedora:**
```bash
sudo dnf install python3-pip xclip git
```

**Arch Linux:**
```bash
sudo pacman -S python-pip xclip git
```

### 2. Setting up the Project
```bash
# Clone the repository
git clone https://github.com/Joeavaib/partner.git
cd partner

# Create and activate a virtual environment (Recommended)
python3 -m venv partnerenv
source partnerenv/bin/activate

# Install CXM in editable mode
pip install -e meta-orchestrator
```

---

## 🪟 Windows (10/11)

### 1. Prerequisites
- **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/). Ensure you check "Add Python to PATH" during installation.
- **Git for Windows**: Download from [git-scm.com](https://git-scm.com/).

### 2. C++ Build Tools (Important for FAISS)
The `faiss-cpu` library (which handles the "memory" of CXM) sometimes requires the C++ Build Tools on Windows. 
If you encounter errors during `pip install`, download and install the **"Desktop development with C++"** workload from the [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

### 3. Setting up the Project (PowerShell)
```powershell
# Clone the repository
git clone https://github.com/Joeavaib/partner.git
cd partner

# Create and activate a virtual environment
python -m venv partnerenv
.\partnerenv\Scripts\Activate.ps1

# Install CXM in editable mode
pip install -e meta-orchestrator
```

---

## ⚙️ Post-Installation Setup

### Initial Configuration
Run CXM for the first time to generate the default configuration file:
```bash
cxm
```
This will create a config folder at `~/.cxm/` (Linux) or `%USERPROFILE%\.cxm` (Windows).

### Verify Installation
Check if the tool can see your environment:
```bash
cxm ctx
```

## 🐞 Troubleshooting

- **Clipboard issues on Linux:** Ensure `xclip` is installed and you are in a graphical session (X11 or Wayland with XWayland).
- **FAISS Installation Errors:** On Windows, ensure you have the latest `pip` and `setuptools`:
  ```powershell
  pip install --upgrade pip setuptools
  ```
- **Path Issues:** If the `cxm` command is not found after installation, ensure your virtual environment is active.
