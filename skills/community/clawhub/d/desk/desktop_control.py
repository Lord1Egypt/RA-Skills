"""
Desktop Control - Optimized Desktop Automation
Advanced Mouse, Keyboard, and Screen Automation for OpenClaw

Optimized for:
- Minimal latency on hot paths
- Lazy loading of optional dependencies
- Robust error handling with retry logic
- Context manager support
"""

from __future__ import annotations

import functools
import logging
import math
import time
from typing import TYPE_CHECKING, Callable, List, Optional, Tuple, Union

if TYPE_CHECKING:
    from PIL import Image

# Configure logging with lazy evaluation
logger = logging.getLogger(__name__)

# Lazy imports for optional modules - only load when needed
_gw = None
_perclip = None


def _get_pygetwindow():
    """Lazy load pygetwindow module."""
    global _gw
    if _gw is None:
        try:
            import pygetwindow as gw
            _gw = gw
        except ImportError:
            logger.warning("pygetwindow not available. Window operations disabled.")
            raise
    return _gw


def _get_pyperclip():
    """Lazy load pyperclip module."""
    global _perclip
    if _perclip is None:
        try:
            import pyperclip
            _perclip = pyperclip
        except ImportError:
            logger.warning("pyperclip not available. Clipboard operations disabled.")
            raise
    return _perclip


# Retry decorator for flaky operations
def retry_on_error(max_retries: int = 3, delay: float = 0.1, exceptions: tuple = (Exception,)):
    """Decorator to retry operations on failure."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (2 ** attempt))  # Exponential backoff
                        logger.debug(f"Retry {attempt + 1}/{max_retries} for {func.__name__}")
                    else:
                        raise last_exception
            return None
        return wrapper
    return decorator


class DesktopController:
    """
    Optimized desktop automation controller with minimal overhead.

    Features:
    - Context manager support for automatic cleanup
    - Lazy loading of heavy dependencies
    - Retry logic for flaky operations
    - Configurable logging levels
    - Bounds checking for all coordinate operations
    """

    __slots__ = ('failsafe', 'require_approval', 'screen_width', 'screen_height',
                 '_corner_tolerance', '_last_mouse_pos', '_log_debug')

    def __init__(
        self,
        failsafe: bool = True,
        require_approval: bool = False,
        log_level: int = logging.INFO
    ) -> None:
        """
        Initialize desktop controller.

        Args:
            failsafe: Enable failsafe (move mouse to corner to abort)
            require_approval: Require user confirmation for actions
            log_level: Logging level (use logging.DEBUG for verbose output)
        """
        self.failsafe = failsafe
        self.require_approval = require_approval
        self._corner_tolerance = 5
        self._last_mouse_pos: Optional[Tuple[int, int]] = None

        # Cache screen size (assume single monitor for most operations)
        self.screen_width, self.screen_height = self._get_screen_size()

        # Configure logging based on level
        logger.setLevel(log_level)
        self._log_debug = log_level <= logging.DEBUG

        if failsafe:
            logger.info(
                f"DesktopController ready. Screen: {self.screen_width}x{self.screen_height}. "
                f"Failsafe enabled (move to corner to abort)."
            )

    def __enter__(self) -> DesktopController:
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit with cleanup."""
        self.cleanup()

    def cleanup(self) -> None:
        """Release resources and ensure clean state."""
        try:
            # Release any held keys
            import pyautogui
            pyautogui.keyUp('ctrl')
            pyautogui.keyUp('shift')
            pyautogui.keyUp('alt')
            pyautogui.keyUp('win')
        except Exception:
            pass
        logger.debug("DesktopController cleanup complete")

    # ========== INTERNAL UTILITIES ==========

    def _check_failsafe(self) -> None:
        """Check if mouse is in corner (failsafe position)."""
        if not self.failsafe:
            return

        x, y = self.get_mouse_position()
        corners = (
            (0, 0),
            (self.screen_width - 1, 0),
            (0, self.screen_height - 1),
            (self.screen_width - 1, self.screen_height - 1)
        )

        for cx, cy in corners:
            if abs(x - cx) <= self._corner_tolerance and abs(y - cy) <= self._corner_tolerance:
                raise pyautogui.FailSafeException("Failsafe triggered - mouse in corner")

    def _check_approval(self, action: str) -> bool:
        """Check if user approves action when approval mode is enabled."""
        if not self.require_approval:
            return True

        response = input(f"Allow: {action}? [y/n]: ").strip().lower()
        approved = response in ('y', 'yes')

        if not approved:
            logger.warning(f"Action declined: {action}")
        return approved

    def _clamp_coordinates(self, x: int, y: int) -> Tuple[int, int]:
        """Clamp coordinates to screen bounds."""
        return (
            max(0, min(x, self.screen_width - 1)),
            max(0, min(y, self.screen_height - 1))
        )

    @staticmethod
    def _get_screen_size() -> Tuple[int, int]:
        """Get screen size (static method for initialization)."""
        import pyautogui
        return pyautogui.size()

    def _wpm_to_interval(self, wpm: int) -> float:
        """Convert WPM to keystroke interval (assuming 5 chars/word)."""
        return 60.0 / (wpm * 5)

    # ========== MOUSE OPERATIONS ==========

    def move_mouse(
        self,
        x: int,
        y: int,
        duration: float = 0,
        smooth: bool = True
    ) -> None:
        """
        Move mouse to absolute coordinates with optional smoothing.

        Args:
            x: X coordinate (pixels from left)
            y: Y coordinate (pixels from top)
            duration: Movement time in seconds (0 = instant)
            smooth: Use easing for natural movement
        """
        self._check_failsafe()
        x, y = self._clamp_coordinates(x, y)

        if self._check_approval(f"move mouse to ({x}, {y})"):
            import pyautogui

            if smooth and duration > 0:
                pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeInOutQuad)
            else:
                pyautogui.moveTo(x, y, duration=duration)

            self._last_mouse_pos = (x, y)
            if self._log_debug:
                logger.debug(f"Moved to ({x}, {y}) in {duration}s")

    def move_relative(self, dx: int, dy: int, duration: float = 0) -> None:
        """Move mouse relative to current position."""
        self._check_failsafe()

        if self._check_approval(f"move mouse relative ({dx}, {dy})"):
            import pyautogui
            pyautogui.move(dx, dy, duration=duration)
            if self._log_debug:
                logger.debug(f"Moved relative ({dx}, {dy})")

    @retry_on_error(max_retries=2, delay=0.05)
    def click(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        button: str = 'left',
        clicks: int = 1,
        interval: float = 0.05
    ) -> None:
        """
        Perform mouse click with retry logic.

        Args:
            x, y: Coordinates (None = current position)
            button: 'left', 'right', 'middle'
            clicks: Number of clicks (1-3 supported efficiently)
            interval: Delay between clicks
        """
        self._check_failsafe()

        if x is not None and y is not None:
            x, y = self._clamp_coordinates(x, y)

        pos_str = f"at ({x}, {y})" if x is not None else "at current position"
        if self._check_approval(f"{button} click {pos_str}"):
            import pyautogui

            # Optimize for common cases
            if clicks == 1 and interval <= 0.01:
                # Single fast click
                if x is not None and y is not None:
                    pyautogui.click(x, y, button=button)
                else:
                    pyautogui.click(button=button)
            else:
                pyautogui.click(x, y, clicks=clicks, interval=interval, button=button)

            logger.info(f"{button} click {pos_str} x{clicks}")

    def double_click(self, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """Optimized double-click."""
        self.click(x, y, clicks=2, interval=0.01)

    def right_click(self, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """Optimized right-click."""
        self.click(x, y, button='right')

    def middle_click(self, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """Optimized middle-click."""
        self.click(x, y, button='middle')

    def drag(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        duration: float = 0.3,
        button: str = 'left'
    ) -> None:
        """
        Drag from point A to point B.

        Args:
            x1, y1: Start coordinates
            x2, y2: End coordinates
            duration: Drag duration
            button: Mouse button to hold
        """
        self._check_failsafe()
        x1, y1 = self._clamp_coordinates(x1, y1)
        x2, y2 = self._clamp_coordinates(x2, y2)

        if self._check_approval(f"drag ({x1},{y1}) to ({x2},{y2})"):
            import pyautogui

            # Move to start first
            pyautogui.moveTo(x1, y1)
            time.sleep(0.02)  # Minimal delay for stability

            # Perform drag
            pyautogui.dragTo(x2, y2, duration=duration, button=button)

            self._last_mouse_pos = (x2, y2)
            logger.info(f"Dragged from ({x1},{y1}) to ({x2},{y2})")

    def scroll(
        self,
        amount: int,
        x: Optional[int] = None,
        y: Optional[int] = None,
        horizontal: bool = False
    ) -> None:
        """
        Scroll mouse wheel.

        Args:
            amount: Scroll clicks (+ = up/left, - = down/right)
            x, y: Position to scroll at
            horizontal: Scroll horizontally instead of vertically
        """
        self._check_failsafe()

        if x is not None and y is not None:
            self.move_mouse(x, y, duration=0)

        import pyautogui
        if horizontal:
            pyautogui.hscroll(amount)
        else:
            pyautogui.scroll(amount)

        if self._log_debug:
            logger.debug(f"Scrolled {'horizontal' if horizontal else 'vertical'} {amount}")

    def get_mouse_position(self) -> Tuple[int, int]:
        """Get current mouse coordinates."""
        import pyautogui
        pos = pyautogui.position()
        return (pos.x, pos.y)

    # ========== KEYBOARD OPERATIONS ==========

    def type_text(
        self,
        text: str,
        interval: Optional[float] = None,
        wpm: Optional[int] = None
    ) -> None:
        """
        Type text with configurable speed.

        Args:
            text: Text to type
            interval: Delay between keystrokes (None = instant)
            wpm: Words per minute (overrides interval)
        """
        self._check_failsafe()

        if not text:
            return

        # Calculate interval
        if wpm is not None:
            interval = self._wpm_to_interval(wpm)
        elif interval is None:
            interval = 0

        display_text = text[:50] + '...' if len(text) > 50 else text
        if self._check_approval(f"type: '{display_text}'"):
            import pyautogui
            pyautogui.write(text, interval=interval)
            logger.info(f"Typed '{display_text}' (interval={interval:.3f}s)")

    def press(self, key: str, presses: int = 1, interval: float = 0.05) -> None:
        """Press and release a key."""
        self._check_failsafe()

        if self._check_approval(f"press '{key}' x{presses}"):
            import pyautogui
            pyautogui.press(key, presses=presses, interval=interval)
            logger.info(f"Pressed '{key}' {presses}x")

    def hotkey(self, *keys: str, interval: float = 0.01) -> None:
        """Execute keyboard shortcut."""
        self._check_failsafe()

        keys_str = '+'.join(keys)
        if self._check_approval(f"hotkey: {keys_str}"):
            import pyautogui
            pyautogui.hotkey(*keys, interval=interval)
            logger.info(f"Hotkey: {keys_str}")

    def key_down(self, key: str) -> None:
        """Hold a key down."""
        self._check_failsafe()
        import pyautogui
        pyautogui.keyDown(key)
        if self._log_debug:
            logger.debug(f"Key down: {key}")

    def key_up(self, key: str) -> None:
        """Release a held key."""
        import pyautogui
        pyautogui.keyUp(key)
        if self._log_debug:
            logger.debug(f"Key up: {key}")

    @contextmanager
    def hold_keys(self, *keys: str):
        """Context manager for holding keys.

        Example:
            with dc.hold_keys('ctrl', 'shift'):
                dc.click(100, 100)
        """
        import pyautogui
        for key in keys:
            pyautogui.keyDown(key)
        try:
            yield self
        finally:
            for key in reversed(keys):
                pyautogui.keyUp(key)

    # ========== SCREEN OPERATIONS ==========

    @retry_on_error(max_retries=2, delay=0.1)
    def screenshot(
        self,
        region: Optional[Tuple[int, int, int, int]] = None,
        filename: Optional[str] = None
    ) -> Optional['Image.Image']:
        """
        Capture screenshot with retry logic.

        Args:
            region: (left, top, width, height) for partial capture
            filename: Path to save image

        Returns:
            PIL Image if filename not provided, None otherwise
        """
        import pyautogui

        img = pyautogui.screenshot(region=region)

        if filename:
            img.save(filename)
            logger.info(f"Screenshot saved: {filename}")
            return None

        if self._log_debug:
            logger.debug(f"Screenshot captured (region={region})")
        return img

    def screenshot_to_file(self, filename: str, region: Optional[Tuple[int, int, int, int]] = None) -> str:
        """Capture and save screenshot (convenience method)."""
        self.screenshot(region=region, filename=filename)
        return filename

    def get_pixel(self, x: int, y: int) -> Tuple[int, int, int]:
        """Get RGB color at coordinates."""
        import pyautogui
        return pyautogui.pixel(x, y)

    def get_pixel_region(
        self,
        x: int,
        y: int,
        width: int,
        height: int
    ) -> List[List[Tuple[int, int, int]]]:
        """
        Get all pixel colors in a region efficiently.

        Returns 2D list of RGB tuples.
        """
        import pyautogui

        # Use screenshot for efficiency on larger regions
        if width * height > 100:
            img = pyautogui.screenshot(region=(x, y, width, height))
            return [[img.getpixel((px, py)) for px in range(width)] for py in range(height)]
        else:
            # Individual pixel access for small regions
            return [
                [pyautogui.pixel(x + px, y + py) for px in range(width)]
                for py in range(height)
            ]

    def find_on_screen(
        self,
        image_path: str,
        confidence: float = 0.9,
        region: Optional[Tuple[int, int, int, int]] = None,
        grayscale: bool = True
    ) -> Optional[Tuple[int, int, int, int]]:
        """
        Find image on screen with optimized settings.

        Args:
            image_path: Path to template image
            confidence: Match threshold 0-1
            region: Search region (left, top, width, height)
            grayscale: Convert to grayscale for faster matching

        Returns:
            (x, y, width, height) of match, or None
        """
        import pyautogui

        try:
            location = pyautogui.locateOnScreen(
                image_path,
                confidence=confidence,
                region=region,
                grayscale=grayscale
            )
            if location:
                logger.info(f"Found '{image_path}' at {location}")
                return (location.left, location.top, location.width, location.height)
            return None
        except Exception as e:
            logger.error(f"Find image error: {e}")
            return None

    def find_all_on_screen(
        self,
        image_path: str,
        confidence: float = 0.9,
        region: Optional[Tuple[int, int, int, int]] = None
    ) -> List[Tuple[int, int, int, int]]:
        """Find all occurrences of an image on screen."""
        import pyautogui

        try:
            locations = pyautogui.locateAllOnScreen(
                image_path,
                confidence=confidence,
                region=region
            )
            return [(loc.left, loc.top, loc.width, loc.height) for loc in locations]
        except Exception as e:
            logger.error(f"Find all error: {e}")
            return []

    def wait_for_image(
        self,
        image_path: str,
        timeout: float = 10.0,
        interval: float = 0.5,
        confidence: float = 0.9
    ) -> Optional[Tuple[int, int, int, int]]:
        """
        Wait for image to appear on screen.

        Args:
            image_path: Path to image to wait for
            timeout: Maximum wait time in seconds
            interval: Check interval
            confidence: Match confidence

        Returns:
            Location tuple if found, None if timeout
        """
        start = time.time()
        while time.time() - start < timeout:
            result = self.find_on_screen(image_path, confidence)
            if result:
                return result
            time.sleep(interval)
        logger.warning(f"Timeout waiting for image: {image_path}")
        return None

    # ========== WINDOW OPERATIONS ==========

    def get_all_windows(self) -> List[str]:
        """Get all open window titles."""
        try:
            gw = _get_pygetwindow()
            return [w for w in gw.getAllTitles() if w.strip()]
        except ImportError:
            logger.error("pygetwindow not installed")
            return []
        except Exception as e:
            logger.error(f"Window list error: {e}")
            return []

    def get_active_window(self) -> Optional[str]:
        """Get currently focused window title."""
        try:
            gw = _get_pygetwindow()
            window = gw.getActiveWindow()
            return window.title if window else None
        except ImportError:
            return None
        except Exception as e:
            logger.error(f"Active window error: {e}")
            return None

    def activate_window(self, title: str, partial: bool = True) -> bool:
        """
        Bring window to front.

        Args:
            title: Window title or substring
            partial: Match partial title

        Returns:
            True if activated successfully
        """
        try:
            gw = _get_pygetwindow()

            if partial:
                windows = gw.getWindowsWithTitle(title)
                if windows:
                    windows[0].activate()
                    logger.info(f"Activated: {windows[0].title}")
                    return True
            else:
                for window in gw.getAllWindows():
                    if window.title == title:
                        window.activate()
                        logger.info(f"Activated: {title}")
                        return True

            logger.warning(f"Window not found: {title}")
            return False
        except ImportError:
            return False
        except Exception as e:
            logger.error(f"Activate error: {e}")
            return False

    def find_window(self, title_substring: str) -> Optional[str]:
        """Find window by partial title match."""
        try:
            gw = _get_pygetwindow()
            windows = gw.getWindowsWithTitle(title_substring)
            return windows[0].title if windows else None
        except ImportError:
            return None
        except Exception:
            return None

    # ========== CLIPBOARD OPERATIONS ==========

    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to clipboard."""
        try:
            pc = _get_pyperclip()
            pc.copy(text)
            logger.debug(f"Copied to clipboard: {text[:50]}...")
            return True
        except ImportError:
            return False
        except Exception as e:
            logger.error(f"Clipboard copy error: {e}")
            return False

    def get_clipboard(self) -> Optional[str]:
        """Get text from clipboard."""
        try:
            pc = _get_pyperclip()
            return pc.paste()
        except ImportError:
            return None
        except Exception as e:
            logger.error(f"Clipboard paste error: {e}")
            return None

    # ========== UTILITY ==========

    def sleep(self, seconds: float) -> None:
        """Sleep for specified duration."""
        time.sleep(seconds)

    def wait_for_key(self, key: str, timeout: Optional[float] = None) -> bool:
        """Wait for specific key press."""
        import pyautogui

        start = time.time()
        while True:
            if pyautogui.isPressed(key):
                return True
            if timeout and (time.time() - start) > timeout:
                return False
            time.sleep(0.05)

    def alert(self, text: str = '', title: str = 'Alert') -> None:
        """Show alert dialog."""
        import pyautogui
        pyautogui.alert(text=text, title=title, button='OK')

    def confirm(self, text: str = '', title: str = 'Confirm') -> bool:
        """Show confirmation dialog. Returns True if OK clicked."""
        import pyautogui
        result = pyautogui.confirm(text=text, title=title, buttons=['OK', 'Cancel'])
        return result == 'OK'


# Import contextmanager here for type checking
from contextlib import contextmanager


# ========== CONVENIENCE FUNCTIONS ==========

# Global controller with lazy initialization
_controller: Optional[DesktopController] = None


def get_controller(**kwargs) -> DesktopController:
    """Get or create global controller instance."""
    global _controller
    if _controller is None:
        _controller = DesktopController(**kwargs)
    return _controller


def reset_controller() -> None:
    """Reset global controller. Useful for changing settings."""
    global _controller
    if _controller is not None:
        _controller.cleanup()
    _controller = None


# Quick access functions
def move(x: int, y: int, duration: float = 0) -> None:
    """Quick mouse move."""
    get_controller().move_mouse(x, y, duration)


def click(x: Optional[int] = None, y: Optional[int] = None, button: str = 'left') -> None:
    """Quick click."""
    get_controller().click(x, y, button=button)


def typewrite(text: str, interval: Optional[float] = None) -> None:
    """Quick text typing."""
    get_controller().type_text(text, interval=interval)


def hotkey(*keys: str) -> None:
    """Quick hotkey."""
    get_controller().hotkey(*keys)


def screenshot(filename: Optional[str] = None) -> Optional['Image.Image']:
    """Quick screenshot."""
    return get_controller().screenshot(filename=filename)


if __name__ == "__main__":
    # Quick test
    logging.basicConfig(level=logging.INFO)

    with DesktopController() as dc:
        print(f"Screen: {dc.screen_width}x{dc.screen_height}")
        print(f"Mouse: {dc.get_mouse_position()}")
        print(f"Windows: {len(dc.get_all_windows())} open")
