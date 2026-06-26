#!/usr/bin/env python3
"""QR Tool - Generate and read QR codes."""

import argparse
import sys
import os


def generate_qr(data: str, output: str = None, size: int = 256, error_level: str = 'M'):
    """Generate QR code."""
    try:
        import qrcode
    except ImportError:
        print("Error: qrcode not installed", file=sys.stderr)
        print("Install with: pip install qrcode[pil]", file=sys.stderr)
        sys.exit(1)
    
    # Error correction levels
    error_correction = {
        'L': qrcode.constants.ERROR_CORRECT_L,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'H': qrcode.constants.ERROR_CORRECT_H
    }
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction.get(error_level, qrcode.constants.ERROR_CORRECT_M),
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    if output:
        img.save(output)
        print(f"QR code saved to: {output}")
    else:
        img.show()


def read_qr(image_path: str):
    """Read QR code from image."""
    try:
        from PIL import Image
        from pyzbar.pyzbar import decode
    except ImportError:
        print("Error: Required libraries not installed", file=sys.stderr)
        print("Install with: pip install pillow pyzbar", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.exists(image_path):
        print(f"Error: File not found: {image_path}", file=sys.stderr)
        sys.exit(1)
    
    img = Image.open(image_path)
    decoded = decode(img)
    
    if decoded:
        for obj in decoded:
            print(obj.data.decode('utf-8'))
    else:
        print("No QR code found in image")


def main():
    parser = argparse.ArgumentParser(description='QR code tool')
    parser.add_argument('data', nargs='?', help='Text or URL to encode')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-s', '--size', type=int, default=256, help='QR size')
    parser.add_argument('-r', '--read', help='Read QR from image')
    parser.add_argument('--error', default='M', choices=['L', 'M', 'Q', 'H'], 
                       help='Error correction level')
    
    args = parser.parse_args()
    
    if args.read:
        read_qr(args.read)
    elif args.data:
        generate_qr(args.data, args.output, args.size, args.error)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
