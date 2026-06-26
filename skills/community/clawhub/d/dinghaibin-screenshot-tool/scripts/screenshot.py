#!/usr/bin/env python3
"""
Screenshot Tool - Capture screenshots and screen recordings
Note: Uses platform-specific tools (gnome-screenshot, scrot, macOS screencapture)
"""

import argparse
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


def take_screenshot(output=None, window=None, area=None, delay=0, format='png'):
    """Take a screenshot."""
    
    # Delay if requested
    if delay > 0:
        print(f"Taking screenshot in {delay} seconds...")
        time.sleep(delay)
    
    # Determine output file
    if not output:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output = f"screenshot_{timestamp}.{format}"
    
    # Try different tools based on platform
    success = False
    
    # Linux: gnome-screenshot, scrot, import (ImageMagick)
    if sys.platform.startswith('linux'):
        # Try gnome-screenshot
        try:
            cmd = ['gnome-screenshot']
            if window:
                cmd.append('-w')
            elif area:
                cmd.extend(['-a'])
            if output:
                cmd.extend(['-f', output])
            subprocess.run(cmd, check=True)
            success = True
        except:
            pass
        
        # Try scrot
        if not success:
            try:
                cmd = ['scrot']
                if window:
                    cmd = ['scrot', '-u']
                elif area:
                    x, y, w, h = area.split(',')
                    cmd = ['scrot', '-a', f'{x},{y},{w},{h}']
                cmd.append(output)
                subprocess.run(cmd, check=True)
                success = True
            except:
                pass
        
        # Try ImageMagick
        if not success:
            try:
                cmd = ['import', '-window', 'root', output]
                subprocess.run(cmd, check=True)
                success = True
            except:
                pass
    
    # macOS: screencapture
    elif sys.platform == 'darwin':
        try:
            cmd = ['screencapture']
            if window:
                cmd.extend(['-w'])
            elif area:
                x, y, w, h = area.split(',')
                cmd.extend(['-R', f'{x},{y},{w},{h}'])
            cmd.append(output)
            subprocess.run(cmd, check=True)
            success = True
        except:
            pass
    
    # Windows: PowerShell
    elif sys.platform == 'win32':
        try:
            # Use PowerShell's Get-Screenshot
            ps_script = f'''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$screens = [System.Windows.Forms.Screen]::AllScreens
$screen = $screens[0]
$bitmap = New-Object System.Drawing.Bitmap($screen.Bounds.Width, $screen.Bounds.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screen.Bounds.Location, [System.Drawing.Point]::Empty, $screen.Bounds.Size)
$bitmap.Save("{output}")
$graphics.Dispose()
$bitmap.Dispose()
'''
            subprocess.run(['powershell', '-Command', ps_script], check=True)
            success = True
        except:
            pass
    
    if success:
        print(f"Screenshot saved: {output}")
        return 0
    else:
        print("Error: No screenshot tool available")
        print("Install: gnome-screenshot (Linux), or use macOS/Windows")
        return 1


def start_recording(output=None):
    """Start screen recording (limited platform support)."""
    if not output:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output = f"recording_{timestamp}.mp4"
    
    print("Screen recording started")
    print("Press Ctrl+C to stop")
    
    # Note: Full screen recording requires ffmpeg on Linux
    if sys.platform.startswith('linux'):
        try:
            cmd = ['ffmpeg', '-f', 'x11grab', '-s', '1920x1080', '-i', ':0.0', output]
            print(f"Run: {' '.join(cmd)}")
            print("Recording not implemented - install ffmpeg for full support")
            return 0
        except:
            pass
    
    print("Screen recording requires platform-specific setup")
    return 1


def main():
    parser = argparse.ArgumentParser(description='Screenshot Tool')
    parser.add_argument('--capture', action='store_true', help='Take screenshot')
    parser.add_argument('--record', action='store_true', help='Start recording')
    parser.add_argument('--stop', action='store_true', help='Stop recording')
    parser.add_argument('--window', help='Capture specific window')
    parser.add_argument('--area', help='Capture area (x,y,width,height)')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--delay', type=int, default=0, help='Delay in seconds')
    parser.add_argument('--format', default='png', choices=['png', 'jpg'], help='Format')
    
    args = parser.parse_args()
    
    # Capture screenshot
    if args.capture:
        return take_screenshot(
            args.output,
            args.window,
            args.area,
            args.delay,
            args.format
        )
    
    # Start recording
    if args.record:
        return start_recording(args.output)
    
    # Default: show help
    parser.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
