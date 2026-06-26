# Aliyun CLI — Setup & Authentication

## Installation

### macOS (Homebrew)
```bash
brew install aliyun-cli
```

### Linux (Ubuntu / Debian / CentOS / RHEL)
```bash
# Option 1: snap
sudo snap install aliyun-cli --classic

# Option 2: manual binary install (amd64)
curl -Lo aliyun-cli.tgz https://github.com/aliyun/aliyun-cli/releases/latest/download/aliyun-cli-linux-latest-amd64.tgz
tar xzf aliyun-cli.tgz
sudo mv aliyun /usr/local/bin/

# For arm64
curl -Lo aliyun-cli.tgz https://github.com/aliyun/aliyun-cli/releases/latest/download/aliyun-cli-linux-latest-arm64.tgz
tar xzf aliyun-cli.tgz
sudo mv aliyun /usr/local/bin/
```

### Windows
```powershell
# Scoop
scoop install aliyun

# Or download the MSI installer from:
# https://github.com/aliyun/aliyun-cli/releases
```

### Verify Installation
```bash
aliyun version
# Expected output: 3.x.x
```

---

## Authentication Methods

Alibaba Cloud supports three authentication methods. Choose based on context:

### 1. AccessKey (most common for local dev)

Create an AccessKey in the [RAM console](https://ram.console.aliyun.com/manage/ak):
- Use a **RAM user** AccessKey, not the root account
- The RAM user needs appropriate policies attached (e.g., `AliyunECSFullAccess`)

```bash
aliyun configure
# Prompts:
# Aliyun Access Key ID: LTAI5t...
# Aliyun Access Key Secret: xxxxx
# Default Region Id: cn-hangzhou
# Default output format [json]: json
# Default Language: en
```

Configuration is stored at `~/.aliyun/config.json`.

### 2. ECS RAM Role (recommended for scripts running on ECS)

If running on an ECS instance with a RAM role attached, no explicit credentials are needed:

```bash
# The CLI auto-detects the instance metadata endpoint
aliyun ecs DescribeInstances --RegionId cn-hangzhou
```

To configure explicitly:
```bash
aliyun configure set --mode EcsRamRole --ram-role-name <role-name>
```

### 3. STS Token (temporary credentials, CI/CD, cross-account)

```bash
aliyun configure set \
  --access-key-id ASIA... \
  --access-key-secret xxx \
  --sts-token xxx \
  --region cn-hangzhou
```

Or use environment variables (preferred for CI):
```bash
export ALIBABACLOUD_ACCESS_KEY_ID=ASIA...
export ALIBABACLOUD_ACCESS_KEY_SECRET=xxx
export ALIBABACLOUD_SECURITY_TOKEN=xxx
export ALIBABACLOUD_REGION_ID=cn-hangzhou
```

---

## Multiple Profiles

The CLI supports named profiles for switching between accounts or environments:

```bash
# Create a profile
aliyun configure --profile prod
aliyun configure --profile staging

# Use a specific profile for one command
aliyun ecs DescribeInstances --profile prod --RegionId cn-hangzhou

# Set default profile
aliyun configure set --profile prod

# List all profiles
aliyun configure list

# Show current profile settings
aliyun configure get
```

---

## Useful Global Flags

These work with all commands:

| Flag | Description |
|------|-------------|
| `--region <id>` | Override the configured default region |
| `--profile <name>` | Use a specific named credential profile |
| `--output cols=X,Y,Z` | Tabular output with selected columns |
| `--output table` | Aligned table format |
| `--timeout <seconds>` | Override default request timeout |
| `-d` or `--debug` | Show raw HTTP request/response for debugging |
| `--version` | Show CLI version |

---

## Checking Available Commands

```bash
# List all supported products
aliyun --help

# List all operations for a product
aliyun ecs --help
aliyun oss --help
aliyun vpc --help

# Get help for a specific operation
aliyun ecs DescribeInstances --help
```

---

## Troubleshooting

**Problem: `command not found: aliyun`**
- Ensure the binary is in your `$PATH`
- Try `echo $PATH` and check that `/usr/local/bin` is included

**Problem: `InvalidAccessKeyId`**
- Run `aliyun configure get` to verify the configured key ID
- Check that the key hasn't been disabled in the RAM console

**Problem: `Forbidden.RAM` or `NoPermission`**
- The RAM user/role is missing the required policy
- Attach the relevant policy (e.g., `AliyunECSReadOnlyAccess`) in RAM console
- Use `--debug` to see the exact API action being called, then grant that action

**Problem: Slow API responses or timeouts**
- Try specifying `--region` explicitly to avoid region auto-detection
- Check Alibaba Cloud service status at status.aliyun.com
