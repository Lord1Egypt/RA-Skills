"""
Desktop Control Demo - Optimized Examples
Quick demonstrations of the optimized desktop control skill
"""

import logging
import sys
import time
from pathlib import Path

# Add parent to path for development
sys.path.insert(0, str(Path(__file__).parent.parent))

from desktop_control import DesktopController


def demo_mouse_control():
    """Demo: Mouse movement and clicking"""
    print("\n🖱️  === MOUSE CONTROL DEMO ===")

    with DesktopController(failsafe=True) as dc:
        print(f"Current position: {dc.get_mouse_position()}")

        # Smooth movement to center
        print("\n1. Moving to center smoothly...")
        screen_w, screen_h = dc.screen_width, dc.screen_height
        center_x, center_y = screen_w // 2, screen_h // 2
        dc.move_mouse(center_x, center_y, duration=0.5)

        # Relative movement
        print("2. Moving 100px right, 50px down...")
        dc.move_relative(100, 50, duration=0.3)

        # Click at current position
        print("3. Clicking...")
        dc.click()

        print(f"Final position: {dc.get_mouse_position()}")
        print("✅ Mouse demo complete!")


def demo_keyboard_control():
    """Demo: Keyboard typing with speed control"""
    print("\n⌨️  === KEYBOARD CONTROL DEMO ===")

    with DesktopController() as dc:
        print("\n⚠️  In 3 seconds, I'll type in the active window")
        print("Switch to a text editor NOW!")
        time.sleep(3)

        # Type with human-like speed (80 WPM)
        dc.type_text("Hello from OpenClaw! ", wpm=80)

        # Instant typing for code
        dc.type_text("import fast", interval=0)
        dc.press('return')

        # Using hotkey context manager for selection
        with dc.hold_keys('ctrl'):
            dc.press('a')  # Select all

        print("\n✅ Keyboard demo complete!")


def demo_screen_operations():
    """Demo: Screenshot and pixel operations"""
    print("\n📸 === SCREEN OPERATIONS DEMO ===")

    with DesktopController() as dc:
        # Fast screenshot to file
        print("\n1. Capturing full screen...")
        dc.screenshot_to_file("demo_screenshot.png")
        print("   Saved: demo_screenshot.png")

        # Region screenshot
        print("\n2. Capturing center region...")
        w, h = dc.screen_width, dc.screen_height
        region = ((w - 800) // 2, (h - 600) // 2, 800, 600)
        dc.screenshot_to_file("demo_region.png", region=region)
        print("   Saved: demo_region.png")

        # Get pixel color
        print("\n3. Getting pixel color at center...")
        r, g, b = dc.get_pixel(w // 2, h // 2)
        print(f"   RGB({r}, {g}, {b})")

        print("\n✅ Screen operations complete!")


def demo_window_management():
    """Demo: Window operations"""
    print("\n🪟 === WINDOW MANAGEMENT DEMO ===")

    with DesktopController() as dc:
        print(f"\n1. Active window: {dc.get_active_window()}")

        windows = dc.get_all_windows()
        print(f"\n2. Found {len(windows)} windows:")
        for i, title in enumerate(windows[:10], 1):
            print(f"   {i}. {title}")

        print("\n✅ Window demo complete!")


def demo_clipboard():
    """Demo: Clipboard operations"""
    print("\n📋 === CLIPBOARD DEMO ===")

    with DesktopController() as dc:
        # Save original
        original = dc.get_clipboard()

        # Copy new content
        test_text = "OpenClaw Desktop Control!"
        dc.copy_to_clipboard(test_text)
        print(f"Copied: '{test_text}'")

        # Verify
        result = dc.get_clipboard()
        print(f"Verified: '{result}'")

        # Restore original
        if original:
            dc.copy_to_clipboard(original)
            print("Restored original clipboard")

        print("✅ Clipboard demo complete!")


def demo_drag_and_drop():
    """Demo: Drag and drop with visual feedback"""
    print("\n🎯 === DRAG & DROP DEMO ===")

    with DesktopController() as dc:
        print("\n⚠️  This demo will drag from center-left to center-right")
        print("Press Enter to continue...")
        input()

        w, h = dc.screen_width, dc.screen_height

        # Drag from left to right of center
        start = (w // 2 - 200, h // 2)
        end = (w // 2 + 200, h // 2)

        print(f"Dragging from {start} to {end}...")
        dc.drag(start[0], start[1], end[0], end[1], duration=1.0)

        print("✅ Drag demo complete!")


def demo_advanced_features():
    """Demo: Advanced features like image finding"""
    print("\n🔍 === ADVANCED FEATURES DEMO ===")

    with DesktopController() as dc:
        print("\n1. Using hold_keys context manager...")
        print("   (Simulating Ctrl+Shift+End)")

        with dc.hold_keys('ctrl', 'shift'):
            dc.press('end')

        print("\n2. Scroll operations...")
        dc.scroll(-5)  # Scroll down
        time.sleep(0.2)
        dc.scroll(3)   # Scroll up

        print("\n✅ Advanced features demo complete!")


def run_menu():
    """Interactive demo menu"""
    demos = [
        ("Mouse Control", demo_mouse_control),
        ("Keyboard Control", demo_keyboard_control),
        ("Screen Operations", demo_screen_operations),
        ("Window Management", demo_window_management),
        ("Clipboard", demo_clipboard),
        ("Drag & Drop", demo_drag_and_drop),
        ("Advanced Features", demo_advanced_features),
    ]

    while True:
        print("\n" + "=" * 50)
        print("🎮 DESKTOP CONTROL - OPTIMIZED DEMO")
        print("=" * 50)

        for i, (name, _) in enumerate(demos, 1):
            print(f"  {i}. {name}")
        print(f"  {len(demos) + 1}. Run All")
        print("  0. Exit")

        choice = input("\nEnter choice: ").strip()

        if choice == '0':
            print("\n👋 Goodbye!")
            break
        elif choice == str(len(demos) + 1):
            for name, func in demos:
                print(f"\n{'=' * 50}")
                try:
                    func()
                    time.sleep(1)
                except Exception as e:
                    print(f"❌ Error in {name}: {e}")
            print(f"\n{'=' * 50}")
            print("🎉 All demos complete!")
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            try:
                demos[int(choice) - 1][1]()
            except Exception as e:
                print(f"\n❌ Error: {e}")
        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try:
        run_menu()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
