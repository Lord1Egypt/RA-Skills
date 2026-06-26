#!/usr/bin/env python3
"""
Agent Browser - Browser automation CLI for AI agents

Fast, Python-based browser automation using Playwright.
"""

import sys
from src.browser import BrowserAgent


def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: agent-browser <command> [args]")
        print("\nCommands:")
        print("  open <url>              Open a URL")
        print("  snapshot [-i] [-c] [-d] Get accessibility tree")
        print("  click <selector>        Click element")
        print("  fill <sel> <text>       Fill input field")
        print("  type <sel> <text>       Type text")
        print("  screenshot [path]       Take screenshot")
        print("  get_text <sel>          Get text content")
        print("  get_html <sel>          Get HTML")
        print("  get_url                 Get current URL")
        print("  get_title               Get page title")
        print("  is_visible <sel>        Check visibility")
        print("  wait [options]          Wait for element/text/url")
        print("  find [options]          Find elements")
        print("  press <sel> <key>       Press key")
        print("  hover <sel>             Hover element")
        print("  check <sel>             Check checkbox")
        print("  uncheck <sel>           Uncheck checkbox")
        print("  select <sel> <val>      Select option")
        print("  scroll [dir] [px]       Scroll page")
        print("  upload <sel> <files>    Upload files")
        print("  get_value <sel>         Get input value")
        print("  get_attr <sel> <attr>   Get attribute")
        print("  get_box <sel>           Get bounding box")
        print("  count <sel>             Count elements")
        print("  eval <js>               Execute JavaScript")
        print("  close                   Close browser")
        print("  install                 Install browsers")
        print("\nOptions:")
        print("  --headless              Run in headless mode (default)")
        print("  --headed                Show browser window")
        print("  --viewport <WxH>        Set viewport size")
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    # Parse global options
    headless = True
    viewport = "1280x720"
    
    i = 0
    while i < len(args):
        if args[i] == '--headless':
            headless = True
            args.pop(i)
        elif args[i] == '--headed':
            headless = False
            args.pop(i)
        elif args[i] == '--viewport':
            viewport = args[i + 1] if i + 1 < len(args) else "1280x720"
            args.pop(i)
            if i < len(args) and not args[i].startswith('-'):
                args.pop(i)
        else:
            i += 1
    
    try:
        agent = BrowserAgent(headless=headless, viewport=viewport)
        
        if command == 'open':
            if not args:
                print("Error: open requires URL argument")
                sys.exit(1)
            agent.open(args[0])
            print(f"✓ Opened: {args[0]}")
        
        elif command == 'snapshot':
            interactive = '-i' in args or '--interactive' in args
            compact = '-c' in args or '--compact' in args
            depth = None
            for i, arg in enumerate(args):
                if arg == '-d' and i + 1 < len(args):
                    depth = int(args[i + 1])
            tree = agent.snapshot(interactive=interactive, compact=compact, depth=depth)
            print(tree)
        
        elif command == 'click':
            if not args:
                print("Error: click requires selector argument")
                sys.exit(1)
            agent.click(args[0])
            print(f"✓ Clicked: {args[0]}")
        
        elif command == 'fill':
            if len(args) < 2:
                print("Error: fill requires selector and text arguments")
                sys.exit(1)
            agent.fill(args[0], args[1])
            print(f"✓ Filled: {args[0]}")
        
        elif command == 'type':
            if len(args) < 2:
                print("Error: type requires selector and text arguments")
                sys.exit(1)
            agent.fill(args[0], args[1])
            print(f"✓ Typed: {args[1]} into {args[0]}")
        
        elif command == 'screenshot':
            path = args[0] if args else 'screenshot.png'
            full = '--full' in args
            agent.screenshot(path, full_page=full)
            print(f"✓ Screenshot saved: {path}")
        
        elif command == 'get_text':
            if not args:
                print("Error: get_text requires selector argument")
                sys.exit(1)
            text = agent.get_text(args[0])
            print(text)
        
        elif command == 'get_html':
            if not args:
                print("Error: get_html requires selector argument")
                sys.exit(1)
            html = agent.get_html(args[0])
            print(html)
        
        elif command == 'get_url':
            agent._ensure_browser()
            print(agent.page.url)
        
        elif command == 'get_title':
            agent._ensure_browser()
            print(agent.page.title())
        
        elif command == 'is_visible':
            if not args:
                print("Error: is_visible requires selector argument")
                sys.exit(1)
            visible = agent.is_visible(args[0])
            print(f"{'✓ Visible' if visible else '✗ Hidden'}")
        
        elif command == 'close':
            agent.close()
            print("✓ Browser closed")
        
        elif command == 'install':
            import subprocess
            print("Installing Playwright browsers...")
            result = subprocess.run([sys.executable, '-m', 'playwright', 'install'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Playwright browsers installed successfully")
            else:
                print(f"✗ Installation failed: {result.stderr}")
                sys.exit(1)
        
        else:
            print(f"Error: Unknown command '{command}'")
            print("Run 'agent-browser' without arguments to see available commands")
            sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    finally:
        if 'agent' in locals():
            agent.close()


if __name__ == '__main__':
    main()
