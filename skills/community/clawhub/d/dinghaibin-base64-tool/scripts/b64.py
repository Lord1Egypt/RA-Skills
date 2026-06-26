#!/usr/bin/env python3
"""Base64 Tool - Encode and decode Base64."""

import argparse
import base64
import sys


def encode_string(text: str, url_safe: bool = False, wrap: int = 0) -> str:
    """Encode a string to Base64."""
    data = text.encode('utf-8')
    
    if url_safe:
        result = base64.urlsafe_b64encode(data).decode('ascii')
    else:
        result = base64.b64encode(data).decode('ascii')
    
    if wrap > 0:
        # Wrap at specified width
        lines = [result[i:i+wrap] for i in range(0, len(result), wrap)]
        result = '\n'.join(lines)
    
    return result


def decode_string(text: str, url_safe: bool = False) -> bytes:
    """Decode a Base64 string."""
    text = text.strip()
    
    try:
        if url_safe:
            return base64.urlsafe_b64decode(text)
        else:
            return base64.b64decode(text)
    except Exception as e:
        raise ValueError(f"Invalid Base64: {e}")


def encode_file(input_path: str, output_path: str = None, url_safe: bool = False) -> str:
    """Encode a file to Base64."""
    with open(input_path, 'rb') as f:
        data = f.read()
    
    if url_safe:
        result = base64.urlsafe_b64encode(data).decode('ascii')
    else:
        result = base64.b64encode(data).decode('ascii')
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(result)
        print(f"Encoded {input_path} -> {output_path}")
    
    return result


def decode_file(input_path: str, output_path: str = None, url_safe: bool = False) -> bytes:
    """Decode a Base64 file."""
    with open(input_path, 'r') as f:
        data = f.read()
    
    try:
        if url_safe:
            result = base64.urlsafe_b64decode(data)
        else:
            result = base64.b64decode(data)
        
        if output_path:
            with open(output_path, 'wb') as f:
                f.write(result)
            print(f"Decoded {input_path} -> {output_path}")
        
        return result
    except Exception as e:
        raise ValueError(f"Invalid Base64 file: {e}")


def main():
    parser = argparse.ArgumentParser(description='Base64 encode/decode tool')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--encode', action='store_true', help='Encode to Base64')
    group.add_argument('--decode', action='store_true', help='Decode from Base64')
    
    parser.add_argument('--string', '-s', help='String to encode/decode')
    parser.add_argument('--file', '-f', help='File to encode/decode')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--url', action='store_true', help='Use URL-safe Base64')
    parser.add_argument('--wrap', type=int, default=0, help='Wrap output at N characters')
    
    args = parser.parse_args()
    
    try:
        if args.string:
            if args.encode:
                result = encode_string(args.string, args.url, args.wrap)
                if args.output:
                    with open(args.output, 'w') as f:
                        f.write(result)
                    print(f"Encoded to: {args.output}")
                else:
                    print(result)
            else:
                result = decode_string(args.string, args.url)
                if args.output:
                    with open(args.output, 'wb') as f:
                        f.write(result)
                    print(f"Decoded to: {args.output}")
                else:
                    print(result.decode('utf-8', errors='replace'))
        
        elif args.file:
            if args.encode:
                encode_file(args.file, args.output, args.url)
            else:
                decode_file(args.file, args.output, args.url)
        
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
