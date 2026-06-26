---
name: file-to-link
description: Uploads a local file to Qiniu Cloud Storage and returns a shareable URL.
---

# File to Link Skill

This skill provides a professional and reliable way to take a local file and get a publicly accessible URL for it. It uses **Qiniu Kodo Cloud Storage** as the backend.

This skill was upgraded from a previous version that used a less reliable, temporary hosting service. It now uses a robust cloud storage provider and correctly handles file paths with special characters (e.g., Chinese, spaces).

## SECURITY WARNING

**Do not use this skill for sensitive, private, or confidential files.**

Files uploaded using this skill may become **publicly accessible** depending on the bucket's configuration. Use this tool only for non-sensitive data that you are comfortable sharing.

## Core Functionality

The skill takes a local file path as input, uploads the file to a pre-configured Qiniu Kodo bucket, and prints the resulting public URL to standard output.

## Prerequisites

This skill requires the `qiniu` Python package to be installed. If it's not present, the skill will fail with an import error.

```sh
pip install qiniu
```

## Usage Example

To upload a file and get its link, execute the core Python script with the `--file` parameter.

```powershell
# Example usage
& "F:\python 3.10\python.exe" "C:\Users\EDY\.openclaw\skills\file-to-link\scripts\create_link.py" --file "F:\周明慧\资料\clawhub_skill\违规·素材\违规视频1.mp4"
```

### Parameters
*   `--file` (required): The full, absolute local path to the file you want to upload.

### Output

If the upload is successful, the script will print **only the URL** to its standard output. For example:

```
http://tbbc24uef.hn-bkt.clouddn.com/%E8%BF%9D%E8%A7%84%E8%A7%86%E9%A2%911.mp4_1772527755
```

If there is an error (e.g., file not found, Qiniu credentials incorrect), an error message will be printed to standard error, and the standard output will be empty.
