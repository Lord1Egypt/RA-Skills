# Setup Guide

Use this reference when the environment is missing dependencies or an API key.

## Required dependency

The workflow requires Node.js 18 or newer.

Check it with:

```bash
node --version
```

## Install Node.js

### Windows

With winget:

```powershell
winget install OpenJS.NodeJS.LTS
```

Or download it from the official site:

- https://nodejs.org/

### macOS

With Homebrew:

```bash
brew install node
```

Or download it from the official site:

- https://nodejs.org/

### Ubuntu or Debian

```bash
sudo apt-get update
sudo apt-get install -y nodejs npm
```

If the distro package is too old, install the current LTS from the official Node.js distribution site.

## SiliconFlow API key

If the workflow needs ASR and `SILICONFLOW_API_KEY` is missing, tell the user to create a key here:

- https://cloud.siliconflow.cn/me/account/ak

Then set it before retrying.

### Windows PowerShell

```powershell
$env:SILICONFLOW_API_KEY="your_key_here"
```

### Windows CMD

```cmd
set SILICONFLOW_API_KEY=your_key_here
```

### macOS or Linux

```bash
export SILICONFLOW_API_KEY="your_key_here"
```

## Retry rule

After the user installs Node.js or sets the API key, rerun the same `node scripts/bilibili_pipeline.mjs ...` command.