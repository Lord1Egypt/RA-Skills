#!/usr/bin/env python3
"""
Base64 Toolkit - Encoding and decoding utility

Actions:
- encode: Encode text to Base64
- decode: Decode Base64 to text
- encode-url: URL-safe Base64 encoding
- decode-url: URL-safe Base64 decoding
- image-encode: Convert image to Base64 data URI
"""

import argparse
import base64
import json
import mimetypes
import os
import sys


def encode_text(text: str) -> dict:
    """Encode text to Base64."""
    try:
        encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        return {"success": True, "encoded": encoded, "input": text}
    except Exception as e:
        return {"success": False, "error": str(e)}


def decode_text(encoded: str) -> dict:
    """Decode Base64 to text."""
    try:
        # Remove any whitespace
        encoded = encoded.strip()
        decoded = base64.b64decode(encoded).decode('utf-8')
        return {"success": True, "decoded": decoded, "input": encoded}
    except Exception as e:
        return {"success": False, "error": f"Invalid Base64: {str(e)}"}


def encode_url_safe(text: str) -> dict:
    """URL-safe Base64 encoding."""
    try:
        encoded = base64.urlsafe_b64encode(text.encode('utf-8')).decode('utf-8')
        # Remove padding for cleaner URLs
        encoded = encoded.rstrip('=')
        return {"success": True, "encoded": encoded, "input": text, "note": "Padding removed for URL use"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def decode_url_safe(encoded: str) -> dict:
    """URL-safe Base64 decoding."""
    try:
        encoded = encoded.strip()
        # Add padding if needed
        padding = 4 - len(encoded) % 4
        if padding != 4:
            encoded += '=' * padding
        decoded = base64.urlsafe_b64decode(encoded).decode('utf-8')
        return {"success": True, "decoded": decoded, "input": encoded}
    except Exception as e:
        return {"success": False, "error": f"Invalid URL-safe Base64: {str(e)}"}


def encode_image(file_path: str) -> dict:
    """Convert image to Base64 data URI."""
    try:
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}
        
        # Detect MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type or not mime_type.startswith('image/'):
            mime_type = 'image/png'  # Default fallback
        
        # Read and encode
        with open(file_path, 'rb') as f:
            image_data = f.read()
        
        encoded = base64.b64encode(image_data).decode('utf-8')
        data_uri = f"data:{mime_type};base64,{encoded}"
        
        return {
            "success": True,
            "data_uri": data_uri,
            "mime_type": mime_type,
            "base64": encoded,
            "file_size": len(image_data),
            "file_path": file_path
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description='Base64 Toolkit')
    parser.add_argument('action', choices=['encode', 'decode', 'encode-url', 'decode-url', 'image-encode'],
                        help='Action to perform')
    parser.add_argument('--input', '-i', required=True, help='Input string or file path')
    parser.add_argument('--file', '-f', action='store_true', help='Treat input as file path')
    
    args = parser.parse_args()
    
    # Handle file input for non-image actions
    input_data = args.input
    if args.file and args.action != 'image-encode':
        try:
            with open(args.input, 'r') as f:
                input_data = f.read()
        except FileNotFoundError:
            result = {"success": False, "error": f"File not found: {args.input}"}
            print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(1)
    
    # Execute action
    if args.action == 'encode':
        result = encode_text(input_data)
    elif args.action == 'decode':
        result = decode_text(input_data)
    elif args.action == 'encode-url':
        result = encode_url_safe(input_data)
    elif args.action == 'decode-url':
        result = decode_url_safe(input_data)
    elif args.action == 'image-encode':
        result = encode_image(args.input)  # Always treat as file path
    else:
        result = {"success": False, "error": f"Unknown action: {args.action}"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result.get('success') else 1)


if __name__ == '__main__':
    main()
