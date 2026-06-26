# File Upload CLI Tool

Upload files to the litterbox.catbox.moe file sharing service from the command line using curl.

## Installation

### Prerequisites

- **Node.js v14.0.0 or higher**
  - Windows: Download from [nodejs.org](https://nodejs.org)
  - macOS: `brew install node` or download from [nodejs.org](https://nodejs.org)
  - Linux: `sudo apt install nodejs npm` (Ubuntu/Debian) or use your package manager

- **curl**
  - Windows: Included with Windows 10+ (curl.exe)
  - macOS: Pre-installed
  - Linux: `sudo apt install curl` (Ubuntu/Debian) or use your package manager

### Install Dependencies

```bash
cd file-upload-cli
npm install
```

No external npm packages required - uses native Node.js modules and system curl.

## Usage

Upload a file and get a shareable URL:

```bash
node file-upload-cli.js <filePath>
```

### Examples

```bash
# Upload a text file
node file-upload-cli.js document.txt

# Upload an image
node file-upload-cli.js photo.jpg

# Upload with absolute path
node file-upload-cli.js /path/to/file.pdf

# Upload file with spaces in name
node file-upload-cli.js "my file.txt"
```

## Output

**Success**:
```
Uploading...
File uploaded successfully!
URL: https://litter.catbox.moe/abc123.txt
Note: File will be available for 72 hours.
```

**Error**:
```
Error: File not found - document.txt
Please check the file path and try again.
```

## Features

- ✅ Simple one-command upload
- ✅ Progress indication for large files
- ✅ Clear error messages
- ✅ Cross-platform (Windows, macOS, Linux)
- ✅ Supports files up to 1GB
- ✅ Files available for 72 hours
- ✅ No external npm dependencies (uses system curl)

## Exit Codes

- `0` - Success
- `1` - General error
- `2` - Network error
- `3` - Service error
- `4` - Validation error (file not found, too large, etc.)

## Limitations

- Maximum file size: 1GB (litterbox.catbox.moe service limit)
- Files are uploaded to a public service (URLs are publicly accessible)
- Files expire after 72 hours
- No authentication required
- Single file upload per command
- Requires curl to be installed on the system

## Troubleshooting

### Common Issues

**"curl command not found"**
- **Solution**: Install curl on your system
  - Windows: curl.exe is included in Windows 10+
  - macOS: Pre-installed
  - Linux: `sudo apt install curl`

**"Permission denied" error**
- **Windows**: Check file permissions in File Explorer → Properties → Security
- **macOS/Linux**: Run `chmod +r <file>` to grant read permission

**"Connection timeout" error**
- Check your internet connection
- Verify firewall allows HTTPS connections
- Try with a smaller file first
- The 0x0.st service may be experiencing issues

**"File too large" from service (413)**
- File exceeds 1GB limit
- Compress the file or split into smaller parts

**"Network error - Cannot connect to litterbox.catbox.moe"**
- Check internet connection
- Verify DNS resolution: `ping litterbox.catbox.moe`
- Check if firewall is blocking the connection
- Try again later (service may be down)

### Platform-Specific Notes

**Windows**:
- Use quotes for paths with spaces: `node file-upload-cli.js "my file.txt"`
- Both forward slash and backslash work: `C:/path/file.txt` or `C:\path\file.txt`
- PowerShell and Command Prompt both supported

**macOS/Linux**:
- Use quotes for paths with spaces: `node file-upload-cli.js "my file.txt"`
- Tilde (`~`) expansion not supported - use absolute paths
- Symlinks are followed automatically

### Getting Help

- Check the SKILL.md file for detailed documentation
- Review quickstart.md in specs/001-file-upload-cli/ for test scenarios
- Verify Node.js version: `node --version` (should be v14+)

## License

MIT
