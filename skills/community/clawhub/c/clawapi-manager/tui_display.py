#!/usr/bin/env python3
"""
API Cockpit - TUI Display
Text-based UI with colors, progress bars, and ASCII art
"""

import os
import sys
import json
from datetime import datetime

# ANSI color codes
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'

def clear_screen():
    """Clear terminal screen"""
    print('\033[2J\033[H', end='')

def draw_box(title, content, width=60):
    """Draw a box with title"""
    print(f"{Colors.CYAN}{'═' * width}{Colors.RESET}")
    print(f"{Colors.CYAN}║ {Colors.BOLD}{title:^{width-4}}{Colors.RESET} {Colors.CYAN}║")
    print(f"{Colors.CYAN}{'═' * width}{Colors.RESET}")
    for line in content:
        print(f"{Colors.CYAN}║ {line:<{width-4}} {Colors.CYAN}║")
    print(f"{Colors.CYAN}{'═' * width}{Colors.RESET}")

def progress_bar(current, total, width=30, color=Colors.GREEN):
    """Draw a progress bar"""
    percent = min(current / total, 1.0)
    filled = int(width * percent)
    bar = '█' * filled + '░' * (width - filled)
    return f"{color}{bar}{Colors.RESET} {percent*100:.1f}%"

def draw_header():
    """Draw the header with ASCII art"""
    header = f"""
{Colors.CYAN}
   ██████╗ ██╗  ██╗ ██████╗ ███████╗██████╗ ████████╗██╗ ██████╗ ███ ██╗╗  
  ██╔════╝ ██║  ██║██╔═══██╗██╔════╝██╔══██╗╚══██╔══╝██║██╔════╝ ████╗  ██║
  ██║  ███╗███████║██║   ██║█████╗  ██████╔╝   ██║   ██║██║  ███╗██╔██╗ ██║
  ██║   ██║██╔══██║██║   ██║██╔══╝  ██╔══██╗   ██║   ██║██║   ██║██║╚██╗██║
  ╚██████╔╝██║  ██║╚██████╔╝██║     ██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
{Colors.RESET}
{Colors.BOLD}     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
     █   API Cockpit - Multi-Node Management System   █
     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{Colors.RESET}
"""
    print(header)

def draw_status():
    """Draw status section"""
    status_lines = [
        f"{Colors.GREEN}●{Colors.RESET} Central   {Colors.GREEN}ONLINE{Colors.RESET}  |  CPU: 23%  |  MEM: 1.2GB",
        f"{Colors.GREEN}●{Colors.RESET} Silicon   {Colors.GREEN}ONLINE{Colors.RESET}  |  CPU: 45%  |  MEM: 2.8GB",
        f"{Colors.GREEN}●{Colors.RESET} Tokyo     {Colors.GREEN}ONLINE{Colors.RESET}  |  CPU: 12%  |  MEM: 0.8GB",
    ]
    draw_box("SYSTEM STATUS", status_lines)

def draw_cost():
    """Draw cost section"""
    cost_lines = [
        f"Today:    {Colors.YELLOW}$12.50{Colors.RESET}",
        f"This Month: {Colors.YELLOW}$342.80{Colors.RESET}",
        f"",
        f"{Colors.BOLD}By Model:{Colors.RESET}",
        f"  claude-opus-4-6  {progress_bar(120, 200)}  $120.00",
        f"  gpt-4            {progress_bar(80, 200)}   $80.00",
        f"  deepseek-chat   {progress_bar(45, 200)}   $45.00",
        f"  kimix            {progress_bar(25, 200)}   $25.00",
    ]
    draw_box("COST MONITORING", cost_lines)

def draw_quota():
    """Draw quota section"""
    quota_lines = [
        f"Antigravity  {progress_bar(75, 100, color=Colors.GREEN)}  75%",
        f"Codex        {progress_bar(45, 100, color=Colors.GREEN)}  45%",
        f"Copilot      {progress_bar(90, 100, color=Colors.YELLOW)}  90%",
        f"Windsurf     {progress_bar(20, 100, color=Colors.GREEN)}  20%",
    ]
    draw_box("API QUOTA", quota_lines)

def draw_alerts():
    """Draw alerts section"""
    alert_lines = [
        f"{Colors.YELLOW}⚠{Colors.RESET} Copilot quota at 90% - consider rotation",
        f"{Colors.GREEN}✓{Colors.RESET} All nodes healthy",
        f"{Colors.GREEN}✓{Colors.RESET} No failed cron jobs",
    ]
    draw_box("RECENT ALERTS", alert_lines)

def draw_footer():
    """Draw footer"""
    print(f"""
{Colors.DIM}
  Commands: {Colors.CYAN}health{Colors.RESET} | {Colors.CYAN}cost{Colors.RESET} | {Colors.CYAN}quota{Colors.RESET} | {Colors.CYAN}alert{Colors.RESET} | {Colors.CYAN}refresh{Colors.RESET} | {Colors.CYAN}quit{Colors.RESET}
  Press 'q' to exit
{Colors.RESET}
""")

def demo():
    """Run TUI demo"""
    clear_screen()
    draw_header()
    draw_status()
    draw_cost()
    draw_quota()
    draw_alerts()
    draw_footer()

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        demo()
    else:
        print("Run with --demo to see TUI preview")
        print("")
        print("This TUI provides:")
        print("  • ASCII art header")
        print("  • Colored status indicators (green/yellow/red)")
        print("  • Progress bars with Unicode characters")
        print("  • Box-drawing characters for layout")
        print("  • Real-time node monitoring")
        print("  • Cost breakdown by model")

if __name__ == '__main__':
    main()
