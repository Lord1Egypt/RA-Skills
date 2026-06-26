#!/usr/bin/env python3
"""
Cross-platform browser opener script.
Supports Chrome, Firefox, Edge, Safari and default browser.
"""

import sys
import subprocess
import argparse
import webbrowser
import platform
import os
from typing import Optional, List

class BrowserOpener:
    """Cross-platform browser opener with support for multiple browsers."""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.browsers = {
            'chrome': {
                'windows': ['chrome', 'google-chrome', 'google-chrome-stable'],
                'darwin': ['google-chrome', 'google-chrome-stable', 'chrome'],
                'linux': ['google-chrome', 'google-chrome-stable', 'chrome']
            },
            'firefox': {
                'windows': ['firefox', 'mozilla-firefox'],
                'darwin': ['firefox', 'mozilla-firefox'],
                'linux': ['firefox', 'mozilla-firefox']
            },
            'edge': {
                'windows': ['edge', 'microsoft-edge'],
                'darwin': ['microsoft-edge'],
                'linux': ['microsoft-edge']
            },
            'safari': {
                'windows': [],
                'darwin': ['safari', 'apple-safari'],
                'linux': []
            }
        }
    
    def find_browser_executable(self, browser_name: str) -> Optional[str]:
        """Find the executable path for a given browser."""
        if browser_name == 'default':
            return None
        
        browser_key = browser_name.lower()
        if browser_key not in self.browsers:
            raise ValueError(f"Unsupported browser: {browser_name}")
        
        possible_names = self.browsers[browser_key].get(self.system, [])
        
        for name in possible_names:
            # Check if the browser is available in PATH
            try:
                result = subprocess.run(['where' if self.system == 'windows' else 'which', name], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    return name
            except FileNotFoundError:
                continue
        
        # Also check common installation paths
        common_paths = self._get_common_installation_paths(browser_key)
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        raise FileNotFoundError(f"Browser '{browser_name}' not found on {self.system}")
    
    def _get_common_installation_paths(self, browser_key: str) -> List[str]:
        """Get common installation paths for browsers."""
        paths = []
        
        if browser_key == 'chrome':
            if self.system == 'windows':
                paths.extend([
                    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
                ])
            elif self.system == 'darwin':
                paths.extend([
                    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
                ])
            elif self.system == 'linux':
                paths.extend([
                    '/usr/bin/google-chrome',
                    '/usr/bin/google-chrome-stable'
                ])
        
        elif browser_key == 'firefox':
            if self.system == 'windows':
                paths.extend([
                    r'C:\Program Files\Mozilla Firefox\firefox.exe',
                    r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'
                ])
            elif self.system == 'darwin':
                paths.extend([
                    '/Applications/Firefox.app/Contents/MacOS/firefox'
                ])
            elif self.system == 'linux':
                paths.extend([
                    '/usr/bin/firefox',
                    '/usr/bin/firefox-esr'
                ])
        
        elif browser_key == 'edge':
            if self.system == 'windows':
                paths.extend([
                    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
                    r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'
                ])
            elif self.system == 'darwin':
                paths.extend([
                    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
                ])
        
        elif browser_key == 'safari':
            if self.system == 'darwin':
                paths.extend([
                    '/Applications/Safari.app/Contents/MacOS/Safari'
                ])
        
        return paths
    
    def open_url(self, url: str, browser_name: str = 'default', 
                 new_window: bool = False, incognito: bool = False, 
                 headless: bool = False) -> bool:
        """Open a URL with the specified browser."""
        
        if not url:
            raise ValueError("URL is required")
        
        try:
            # Validate URL
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            browser_executable = None
            if browser_name != 'default':
                browser_executable = self.find_browser_executable(browser_name)
            
            # Build the command
            cmd = []
            
            if browser_executable:
                cmd.append(browser_executable)
                
                # Add browser-specific flags
                if browser_name.lower() == 'chrome':
                    if incognito:
                        cmd.append('--incognito')
                    if headless:
                        cmd.append('--headless')
                        cmd.append('--disable-gpu')
                    if new_window:
                        cmd.append('--new-window')
                
                elif browser_name.lower() == 'firefox':
                    if incognito:
                        cmd.append('--private-window')
                    if headless:
                        cmd.append('--headless')
                    if new_window:
                        cmd.append('--new-window')
                
                elif browser_name.lower() == 'edge':
                    if incognito:
                        cmd.append('--inprivate')
                    if headless:
                        cmd.append('--headless')
                    if new_window:
                        cmd.append('--new-window')
                
                elif browser_name.lower() == 'safari':
                    if new_window:
                        cmd.append('--new-window')
                    # Safari doesn't support headless or incognito via command line
            
            else:
                # Use system default browser
                if new_window:
                    # webbrowser.open_new() opens in new window/tab
                    webbrowser.open_new(url)
                    return True
                else:
                    webbrowser.open(url)
                    return True
            
            # Add URL
            cmd.append(url)
            
            # Execute command
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True
            else:
                print(f"Error opening browser: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error opening browser: {str(e)}")
            return False

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description='Open URL in specified browser')
    parser.add_argument('--url', required=True, help='URL to open')
    parser.add_argument('--browser', default='default', 
                       help='Browser to use (chrome, firefox, edge, safari, default)')
    parser.add_argument('--new-window', action='store_true', 
                       help='Open in new window')
    parser.add_argument('--incognito', action='store_true', 
                       help='Open in incognito/private mode')
    parser.add_argument('--headless', action='store_true', 
                       help='Open in headless mode')
    
    args = parser.parse_args()
    
    opener = BrowserOpener()
    success = opener.open_url(
        url=args.url,
        browser_name=args.browser,
        new_window=args.new_window,
        incognito=args.incognito,
        headless=args.headless
    )
    
    if success:
        print(f"Successfully opened {args.url} in {args.browser}")
        sys.exit(0)
    else:
        print(f"Failed to open {args.url} in {args.browser}")
        sys.exit(1)

if __name__ == '__main__':
    main()