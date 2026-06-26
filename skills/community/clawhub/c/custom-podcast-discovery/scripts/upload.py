#!/usr/bin/env python3
"""
upload.py — Upload podcast episode to storage

Supports S3 and local file storage based on config.

Usage:
    upload.py --file episode.mp3 --config config.yaml [--title "Episode Title"]
"""
import sys
import os
import re
import argparse
import subprocess
from pathlib import Path
from datetime import datetime


def load_config(config_path: str) -> dict:
    """Load config (simplified YAML parser)"""
    with open(config_path) as f:
        content = f.read()
    
    config = {"storage": {}}
    
    # Parse storage section
    storage_match = re.search(r'storage:\s*\n((?:  \w+:.*\n?)*)', content)
    if storage_match:
        for line in storage_match.group(1).split('\n'):
            if ':' in line:
                key, val = line.strip().split(':', 1)
                config["storage"][key.strip()] = val.strip()
    
    return config


def slugify(text: str) -> str:
    """Convert text to URL-safe slug"""
    slug = text.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    return slug[:50]  # Limit length


def _validate_s3_param(value: str, param_name: str) -> str:
    """Validate S3 config values — reject shell metacharacters"""
    if not value or not re.match(r'^[a-zA-Z0-9._\-/]+$', value):
        print(f"ERROR: Invalid {param_name}: {value!r} — only alphanumerics, dots, hyphens, underscores, slashes allowed")
        sys.exit(1)
    return value


def upload_to_s3(file_path: str, bucket: str, key: str, region: str) -> str:
    """Upload file to S3 and return public URL"""
    # Validate all config-derived values before passing to subprocess
    bucket = _validate_s3_param(bucket, "bucket")
    key = _validate_s3_param(key, "key")
    region = _validate_s3_param(region, "region")

    cmd = [
        "aws", "s3", "cp", file_path, f"s3://{bucket}/{key}",
        "--content-type", "audio/mpeg",
        "--region", region
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        url = f"https://{bucket}.s3.{region}.amazonaws.com/{key}"
        
        # Verify accessible
        import urllib.request
        req = urllib.request.Request(url, method='HEAD')
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    return url
        except:
            pass
        
        return url
    except subprocess.CalledProcessError as e:
        print(f"ERROR: S3 upload failed: {e.stderr.decode()}")
        sys.exit(1)


def copy_to_local(file_path: str, dest_dir: str, filename: str) -> str:
    """Copy file to local directory and return path"""
    dest_path = Path(dest_dir) / filename
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    import shutil
    shutil.copy2(file_path, dest_path)
    
    return str(dest_path.absolute())


def main():
    """Main entry point for episode upload"""
    parser = argparse.ArgumentParser(description="Upload podcast episode to storage")
    parser.add_argument("--file", required=True, help="Audio file to upload")
    parser.add_argument("--config", required=True, help="Config YAML file")
    parser.add_argument("--title", help="Episode title (for filename)")
    args = parser.parse_args()
    
    if not Path(args.file).exists():
        print(f"ERROR: File not found: {args.file}")
        sys.exit(1)
    
    # Load config
    config = load_config(args.config)
    storage = config.get("storage", {})
    
    storage_type = storage.get("type", "local")
    
    # Generate filename
    date = datetime.now().date().isoformat()
    if args.title:
        slug = slugify(args.title)
        filename = f"episode-{date}-{slug}.mp3"
    else:
        filename = f"episode-{date}.mp3"
    
    print(f"=== UPLOADING EPISODE ===")
    print(f"File: {args.file}")
    print(f"Storage: {storage_type}")
    print(f"Filename: {filename}")
    print()
    
    if storage_type == "s3":
        bucket = storage.get("bucket")
        region = storage.get("region", "us-east-1")
        prefix = storage.get("prefix", "podcast/")
        
        if not bucket:
            print("ERROR: S3 bucket not configured")
            sys.exit(1)
        
        key = prefix + filename
        print(f"S3 bucket: {bucket}")
        print(f"S3 key: {key}")
        print(f"Region: {region}")
        print()
        
        url = upload_to_s3(args.file, bucket, key, region)
        print(f"✅ Uploaded to S3")
        print(f"   URL: {url}")
        print()
        print(f"PUBLIC_URL={url}")
        
    elif storage_type == "local":
        dest_dir = storage.get("path", "./output")
        url = copy_to_local(args.file, dest_dir, filename)
        print(f"✅ Copied to local storage")
        print(f"   Path: {url}")
        print()
        print(f"PUBLIC_URL=file://{url}")
        
    else:
        print(f"ERROR: Unknown storage type: {storage_type}")
        sys.exit(1)


if __name__ == "__main__":
    main()
