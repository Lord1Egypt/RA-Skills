# Installation Guide

## Prerequisites

Before installing the etcd skill, ensure you have:

1. **etcdctl** (version 3.6.1 or higher)
   ```bash
   # Check if etcdctl is installed
   etcdctl version
   
   # Install etcdctl (if not installed)
   # On macOS:
   brew install etcd
   
   # On Ubuntu/Debian:
   sudo apt-get update
   sudo apt-get install etcd-client
   
   # On CentOS/RHEL:
   sudo yum install etcd
   ```

2. **bash** (version 4.0 or higher)
   ```bash
   bash --version
   ```

3. **jq** (optional, for JSON processing)
   ```bash
   jq --version
   ```

## Installation Methods

### Method 1: Using the Package (Recommended)

1. Download the package:
   ```bash
   # Download from your distribution source
   # Example:
   wget https://example.com/openclaw-skill-etcd-1.0.0.tar.gz
   ```

2. Extract the package:
   ```bash
   tar -xzf openclaw-skill-etcd-1.0.0.tar.gz
   ```

3. Install to OpenClaw skills directory:
   ```bash
   # Copy to system skills directory
   cp -r openclaw-skill-etcd-1.0.0 ~/workspace/test/openclaw/skills/etcd
   
   # Or copy to user skills directory
   cp -r openclaw-skill-etcd-1.0.0 ~/.openclaw/skills/etcd
   ```

### Method 2: Manual Installation

1. Create the skill directory:
   ```bash
   mkdir -p ~/workspace/test/openclaw/skills/etcd
   ```

2. Copy all files:
   ```bash
   cp SKILL.md ~/workspace/test/openclaw/skills/etcd/
   cp README.md ~/workspace/test/openclaw/skills/etcd/
   cp etcd_helper.sh ~/workspace/test/openclaw/skills/etcd/
   cp -r scripts ~/workspace/test/openclaw/skills/etcd/
   cp -r references ~/workspace/test/openclaw/skills/etcd/
   ```

3. Set execute permissions:
   ```bash
   chmod +x ~/workspace/test/openclaw/skills/etcd/etcd_helper.sh
   chmod +x ~/workspace/test/openclaw/skills/etcd/scripts/*.sh
   ```

## Verification

### Test the Installation

1. Check if skill is recognized:
   ```bash
   # The skill should appear in OpenClaw's skill list
   # This depends on your OpenClaw configuration
   ```

2. Test the helper script:
   ```bash
   cd ~/workspace/test/openclaw/skills/etcd
   ./etcd_helper.sh
   ```

3. Test connection (requires running etcd):
   ```bash
   ./scripts/test_connection.sh http://localhost:2379
   ```

### Test with OpenClaw

1. Start OpenClaw or reload skills
2. Test the skill with a simple command:
   ```
   请使用etcd技能：
   - 操作：list
   - 环境：dev
   - 端点：http://localhost:2379
   - 前缀：/
   ```

## Configuration

### Environment Variables

You can set these environment variables for convenience:

```bash
# Set default etcd endpoints
export ETCD_ENDPOINTS_DEV="http://localhost:2379"
export ETCD_ENDPOINTS_TEST="http://etcd-test:2379"
export ETCD_ENDPOINTS_PROD="https://etcd-prod:2379"

# Set TLS certificates (if needed)
export ETCD_CA_CERT="/path/to/ca.crt"
export ETCD_CLIENT_CERT="/path/to/client.crt"
export ETCD_CLIENT_KEY="/path/to/client.key"
```

### TLS Configuration

For TLS-enabled etcd clusters:

```bash
# Update etcd_helper.sh to include TLS options
# Add these flags to etcdctl commands:
# --cacert="$ETCD_CA_CERT" --cert="$ETCD_CLIENT_CERT" --key="$ETCD_CLIENT_KEY"
```

## Usage Examples

### Basic Usage
```bash
# List keys
./etcd_helper.sh list http://localhost:2379 /app/config/

# Get value
./etcd_helper.sh get http://localhost:2379 /app/config/database

# Put value
./etcd_helper.sh put http://localhost:2379 /test/key "test value"

# Delete key
./etcd_helper.sh delete http://localhost:2379 /test/old_key
```

### Through OpenClaw
```
请使用etcd技能：
- 操作：get
- 环境：prod
- 端点：https://etcd-prod:2379
- key：/app/config/api_key
```

## Troubleshooting

### Common Issues

1. **etcdctl not found**
   ```
   Error: command not found: etcdctl
   ```
   **Solution**: Install etcdctl as shown in prerequisites.

2. **Connection refused**
   ```
   Error: dial tcp 127.0.0.1:2379: connect: connection refused
   ```
   **Solution**: Ensure etcd is running and accessible.

3. **Permission denied**
   ```
   Error: permission denied
   ```
   **Solution**: Check etcd authentication and TLS certificates.

4. **Skill not recognized**
   ```
   Skill not found: etcd
   ```
   **Solution**: Ensure skill is in the correct directory and OpenClaw is reloaded.

### Debug Mode

Enable debug output by setting:
```bash
export ETCD_DEBUG=1
```

Then run commands to see detailed output.

## Upgrading

### From Previous Versions

1. Backup your current etcd skill:
   ```bash
   cp -r ~/workspace/test/openclaw/skills/etcd ~/etcd-backup
   ```

2. Remove old version:
   ```bash
   rm -rf ~/workspace/test/openclaw/skills/etcd
   ```

3. Install new version using Method 1 or 2 above.

4. Restore any custom configurations from backup.

## Uninstallation

To remove the etcd skill:

```bash
# Remove from system skills directory
rm -rf ~/workspace/test/openclaw/skills/etcd

# Remove from user skills directory
rm -rf ~/.openclaw/skills/etcd
```

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the references/ directory for documentation
3. Check OpenClaw logs for skill loading errors
4. Contact the skill maintainer

## License

This skill is released under the MIT License. See the LICENSE file for details.