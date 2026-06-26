# Ai-Thinker-Coder

Hermes Agent skill for Ai-Thinker IoT module development.

## Overview

This is a comprehensive skill collection for Ai-Thinker IoT modules, covering WiFi, BLE, LoRa, Radar, NB-IoT, and NearLink modules. Sub-skills are organized by chip platform.

## Installation

### Method 1: Via Hermes Agent (Recommended)

```
/skill install Ai-Thinker-Coder
```

### Method 2: Manual Installation

```bash
# Clone the skill repository to your Hermes skills directory
git clone <repo-url> ~/.hermes/profiles/<YOUR_PROFILE>/skills/hardware/Ai-Thinker-Coder

# Or copy the skill directory manually
cp -r Ai-Thinker-Coder ~/.hermes/profiles/<YOUR_PROFILE>/skills/hardware/
```

### Method 3: Install Sub-Skills Individually

```bash
# Install specific chip skill
/skill install Ai-Thinker-Coder-bl602    # Ai-WB2 (BL602)

# Or manually
cp -r Ai-Thinker-Coder-bl602 ~/.hermes/profiles/<YOUR_PROFILE>/skills/hardware/
```

## Usage

### Load Main Skill

```
/skill Ai-Thinker-Coder
```

Displays product overview and links to sub-skills.

### Load Chip-Specific Skill

First install the sub-skill, then load it:

```bash
# Install sub-skill
/skill install Ai-Thinker-Coder-bl602    # Ai-WB2 series (BL602 chip)

# Load sub-skill
/skill Ai-Thinker-Coder-bl602
```

### Available Sub-Skills

| Skill | Chip Platform | Product Series | Status |
|-------|-------------|----------------|--------|
| Ai-Thinker-Coder-bl602 | BL602 | Ai-WB2-01S/12F/32S | Available |
| Ai-Thinker-Coder-bl618 | BL616/BL618 | Ai-M61/M62 series | Coming soon |
| Ai-Thinker-Coder-lora | - | Ra-01/RA-01H LoRa | Coming soon |
| Ai-Thinker-Coder-radar | - | RD-01/03/04 Radar | Coming soon |

## Development Workflow

1. **Install main skill** - `/skill install Ai-Thinker-Coder`
2. **Install sub-skill** - `/skill install Ai-Thinker-Coder-bl602` (for your chip)
3. **Load sub-skill** - `/skill Ai-Thinker-Coder-bl602`
4. **Follow setup guide** - Configure development environment
5. **Build and flash** - Use provided Makefile and flash commands

## Quick Start Example (BL602/Ai-WB2)

```bash
# 1. Load the skill
/skill Ai-Thinker-Coder-bl602

# 2. Clone SDK
cd /home/seahi/workspase
git clone https://github.com/Ai-Thinker-Open/Ai-Thinker-WB2.git
cd Ai-Thinker-WB2
git submodule update --init --recursive

# 3. Build example
cd applications/get-started/helloworld
make

# 4. Flash firmware
make flash p=/dev/ttyUSB0 b=921600
```

## Documentation Structure

```
Ai-Thinker-Coder/
├── SKILL.md              # Main entry (Chinese)
├── README.md             # English installation guide
├── README_Zh.md         # Chinese installation guide
└── Ai-Thinker-Coder-bl602/
    └── SKILL.md          # BL602 detailed guide
```

## Requirements

- Hermes Agent with skill management enabled
- For hardware development: USB serial connection to module
- For WSL development: usbipd configured for device passthrough

## Troubleshooting

- **Skill not found**: Ensure skill is in `~/.hermes/profiles/<YOUR_PROFILE>/skills/hardware/`
- **Build errors**: Check git submodules are initialized (`git submodule update --init --recursive`)
- **Flash failures**: Verify BOOT pin pulled low and serial port correct

## Links

- **Ai-Thinker Website**: https://www.ai-thinker.com
- **Forum**: https://bbs.ai-thinker.com
- **Docs**: https://docs.ai-thinker.com
- **GitHub**: https://github.com/Ai-Thinker-Open/

## License

MIT-0 License - See [LICENSE](LICENSE) file for details.
