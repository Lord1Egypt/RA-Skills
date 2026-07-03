# Setup Guide

Use this reference when the environment is missing dependencies or an API key.

## Required dependencies

### Node.js 18+

Check it with:

```bash
node --version
```

#### Install

- **Windows**: `winget install OpenJS.NodeJS.LTS` or download from https://nodejs.org/
- **macOS**: `brew install node`
- **Ubuntu/Debian**: `sudo apt-get install -y nodejs npm`

### yt-dlp

Check it with:

```bash
yt-dlp --version
```

#### Install

```bash
pip3 install yt-dlp
```

Or download from https://github.com/yt-dlp/yt-dlp

## SiliconFlow API key

If the workflow needs ASR and `SILICONFLOW_API_KEY` is missing, create a key here:

- https://cloud.siliconflow.cn/me/account/ak

Then set it before retrying:

```bash
export SILICONFLOW_API_KEY="your_key_here"
```

## Retry rule

After the user installs missing dependencies or sets the API key, rerun the same `node scripts/bilibili_pipeline.mjs ...` command.
