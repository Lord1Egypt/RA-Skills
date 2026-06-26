# CFGPU API Skill for OpenClaw

A comprehensive OpenClaw skill for managing GPU cloud instances on CFGPU platform.

## Features

- **Resource Management**: List available regions, GPU types, and system images
- **Instance Lifecycle**: Create, start, stop, release GPU instances
- **Image Management**: List and manage system/user images
- **Interactive Wizard**: User-friendly command-line interface
- **API Integration**: Full CFGPU API coverage

## Installation

### Option 1: Install via ClawHub
```bash
# Once published to ClawHub
clawhub install cfgpu-api
```

### Option 2: Manual Installation
1. Clone this repository
2. Copy the `cfgpu-api` folder to your OpenClaw skills directory:
   ```bash
   cp -r cfgpu-api ~/.openclaw/workspace/skills/
   ```

## Quick Start

### 1. Get API Token
Obtain your API token from [CFGPU Platform](https://cfgpu.com).

### 2. Configure Authentication
```bash
# Set environment variable
export CFGPU_API_TOKEN="YOUR_API_TOKEN"

# Or create token file
echo "YOUR_API_TOKEN" > ~/.cfgpu/token
chmod 600 ~/.cfgpu/token
```

### 3. Basic Usage
```bash
# List available regions
./scripts/cfgpu-helper.sh list-regions

# List available GPU types
./scripts/cfgpu-helper.sh list-gpus

# Interactive instance creation
./scripts/cfgpu-helper.sh quick-create
```

## Scripts Overview

| Script | Description |
|--------|-------------|
| `cfgpu-helper.sh` | Main CLI tool for all operations |
| `setup-env.sh` | Interactive environment setup |
| `check-config.sh` | Configuration validation |
| `example-usage.sh` | Usage examples |

## API Coverage

This skill supports the full CFGPU API:

- ✅ Region management
- ✅ GPU type listing
- ✅ Image management (system/user)
- ✅ Instance lifecycle (create/start/stop/release)
- ✅ Instance status monitoring
- ✅ Paginated instance queries

## Security Notes

- **Never commit API tokens** to version control
- **Use environment variables** or secure token files
- **Set appropriate permissions** on token files (`chmod 600`)
- **Regularly rotate API tokens** for security

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- [CFGPU Platform](https://cfgpu.com)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [GitHub Issues](https://github.com/yourusername/cfgpu-api-skill/issues)

## Acknowledgments

- CFGPU for providing the GPU cloud platform
- OpenClaw community for the skill ecosystem
- Contributors and users
