#!/usr/bin/env python3
"""Generate COS presigned URLs for accessing private bucket objects.

腾讯云 COS 预签名 URL 生成工具
用于为私有 bucket 中的图片生成带签名的临时访问 URL
"""

import os
import sys
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cos_uploader import _fetch_sts_credentials, _get_cos_client
from qcloud_cos.cos_exception import CosServiceError


def extract_cos_key_from_url(cos_url: str) -> tuple:
    """Extract bucket, region, and key from COS URL.
    
    URL format: https://{bucket}.cos.{region}.myqcloud.com/{key}
    """
    parsed = urlparse(cos_url)
    host = parsed.netloc
    
    # Parse bucket.cos.region.myqcloud.com
    parts = host.split('.')
    if len(parts) >= 5 and parts[1] == 'cos':
        bucket = parts[0]
        region = parts[2]
    else:
        raise ValueError(f"Invalid COS URL format: {cos_url}")
    
    key = parsed.path.lstrip('/')
    return bucket, region, key


def generate_presigned_url(cos_url: str, expired: int = 3600) -> str:
    """Generate presigned URL for COS object.
    
    Args:
        cos_url: Original COS URL (e.g., https://bucket.cos.region.myqcloud.com/key)
        expired: URL expiration time in seconds (default: 3600 = 1 hour)
    
    Returns:
        Presigned URL with query parameters
    """
    bucket, region, key = extract_cos_key_from_url(cos_url)
    
    # Get COS client with STS credentials
    client, _, _ = _get_cos_client()
    
    # Generate presigned URL
    presigned_url = client.get_presigned_url(
        Method='GET',
        Bucket=bucket,
        Key=key,
        Expired=expired
    )
    
    return presigned_url


def generate_presigned_url_with_custom_domain(cos_url: str, custom_domain: str = None, expired: int = 3600) -> str:
    """Generate presigned URL with optional custom CDN domain.
    
    If custom_domain is provided, the signature will be generated for the COS URL
    but the returned URL will use the custom domain (for CDN acceleration).
    """
    presigned = generate_presigned_url(cos_url, expired)
    
    if custom_domain:
        # Replace the COS domain with custom CDN domain
        parsed = urlparse(cos_url)
        original_host = parsed.netloc
        presigned_parsed = urlparse(presigned)
        
        # Build new URL with custom domain but keep query params (signature)
        new_url = f"https://{custom_domain}{parsed.path}?{presigned_parsed.query}"
        return new_url
    
    return presigned


def batch_generate_presigned_urls(cos_urls: list, expired: int = 3600) -> dict:
    """Generate presigned URLs for multiple COS objects.
    
    Args:
        cos_urls: List of COS URLs
        expired: URL expiration time in seconds
    
    Returns:
        Dict mapping original URLs to presigned URLs
    """
    results = {}
    for url in cos_urls:
        try:
            presigned = generate_presigned_url(url, expired)
            results[url] = {
                "success": True,
                "presigned_url": presigned,
                "expired": expired
            }
        except Exception as e:
            results[url] = {
                "success": False,
                "error": str(e)
            }
    return results


if __name__ == "__main__":
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Generate COS presigned URLs")
    parser.add_argument("url", help="COS URL to sign")
    parser.add_argument("--expired", type=int, default=3600, help="Expiration time in seconds (default: 3600)")
    parser.add_argument("--cdn-domain", type=str, default=None, help="Custom CDN domain (optional)")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()
    
    try:
        if args.cdn_domain:
            result = generate_presigned_url_with_custom_domain(args.url, args.cdn_domain, args.expired)
        else:
            result = generate_presigned_url(args.url, args.expired)
        
        if args.json:
            print(json.dumps({
                "original_url": args.url,
                "presigned_url": result,
                "expired": args.expired
            }, indent=2))
        else:
            print(result)
    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
