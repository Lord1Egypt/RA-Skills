"""
Linux Desktop Control - safe mouse/keyboard/screen automation for OpenClaw.
"""

import os
import time
import logging
import subprocess
from typing import Tuple, Optional, List

try:
    import pyautogui
except Exception as e:  # pragma: no cover
    pyautogui = None
    _pyautogui_import_error = e

try:
    import pytesseract
    from PIL import Image
    import numpy as np
    _ocr_available = True
except Exception:
    pytesseract = None
    Image = None
    np = None
    _ocr_available = False

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DesktopControllerLinux:
    """
    Safe desktop automation controller for Linux.
    - Approval mode enabled by default
    - Failsafe supported (move mouse to corner)
    - Environment checks (X11/Wayland)
    """

    def __init__(self, failsafe: bool = True, require_approval: bool = True, log_path: Optional[str] = None):
        if pyautogui is None:
            # Attempt to recover when DISPLAY was missing at import time
            err = str(_pyautogui_import_error)
            if "DISPLAY" in err:
                detected = self._auto_detect_display()
                if detected:
                    os.environ["DISPLAY"] = detected
                    try:
                        import importlib
                        globals()["pyautogui"] = importlib.import_module("pyautogui")
                    except Exception:
                        pass
            if pyautogui is None:
                raise ImportError(
                    f"pyautogui not available: {_pyautogui_import_error}. "
                    "Install: pip install pyautogui pillow"
                )

        self.failsafe = failsafe
        self.require_approval = require_approval
        self.log_path = log_path
        self.presets = {}
        pyautogui.FAILSAFE = failsafe

        # Speed tweaks
        pyautogui.MINIMUM_DURATION = 0
        pyautogui.MINIMUM_SLEEP = 0
        pyautogui.PAUSE = 0

        self._check_environment()
        self.screen_width, self.screen_height = pyautogui.size()
        logger.info(
            f"DesktopControllerLinux initialized. Screen: {self.screen_width}x{self.screen_height} | "
            f"failsafe={failsafe} approval={require_approval}"
        )

    # -------- Environment --------
    def _check_environment(self) -> None:
        session = os.environ.get("XDG_SESSION_TYPE", "unknown")
        display = os.environ.get("DISPLAY")
        wayland = os.environ.get("WAYLAND_DISPLAY")

        if not display and not wayland:
            # Attempt auto-detect X11 DISPLAY via /tmp/.X11-unix
            detected = self._auto_detect_display()
            if detected:
                os.environ["DISPLAY"] = detected
                display = detected
                logger.info(f"Auto-detected DISPLAY={detected}")
            else:
                logger.warning("No DISPLAY/WAYLAND_DISPLAY detected. GUI automation may fail.")

        if session == "wayland":
            logger.warning(
                "Wayland session detected. Many distros restrict input control/screenshot; "
                "X11 is recommended for full functionality."
            )

    def _auto_detect_display(self) -> Optional[str]:
        try:
            if os.path.isdir("/tmp/.X11-unix"):
                for name in sorted(os.listdir("/tmp/.X11-unix")):
                    if name.startswith("X"):
                        return f":{name[1:]}"
        except Exception:
            return None
        return None

    def _check_approval(self, action: str) -> bool:
        if not self.require_approval:
            return True
        response = input(f"Allow: {action}? [y/n]: ").strip().lower()
        approved = response in ("y", "yes")
        if not approved:
            logger.warning(f"Action declined: {action}")
        return approved

    # -------- Mouse --------
    def move_mouse(self, x: int, y: int, duration: float = 0, smooth: bool = True) -> None:
        if self._check_approval(f"move mouse to ({x}, {y})"):
            if smooth and duration > 0:
                pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeInOutQuad)
            else:
                pyautogui.moveTo(x, y, duration=duration)

    def move_relative(self, x_offset: int, y_offset: int, duration: float = 0) -> None:
        if self._check_approval(f"move mouse relative ({x_offset}, {y_offset})"):
            pyautogui.move(x_offset, y_offset, duration=duration)

    def click(self, x: Optional[int] = None, y: Optional[int] = None,
              button: str = "left", clicks: int = 1, interval: float = 0.1) -> None:
        position_str = f"at ({x}, {y})" if x is not None else "at current position"
        if self._check_approval(f"{button} click {position_str}"):
            pyautogui.click(x=x, y=y, clicks=clicks, interval=interval, button=button)

    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int,
             duration: float = 0.5, button: str = "left") -> None:
        if self._check_approval(f"drag from ({start_x}, {start_y}) to ({end_x}, {end_y})"):
            pyautogui.moveTo(start_x, start_y)
            time.sleep(0.05)
            pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration, button=button)

    def scroll(self, clicks: int, direction: str = "vertical",
               x: Optional[int] = None, y: Optional[int] = None) -> None:
        if x is not None and y is not None:
            pyautogui.moveTo(x, y)

        if direction == "vertical":
            pyautogui.scroll(clicks)
        else:
            pyautogui.hscroll(clicks)

    def get_mouse_position(self) -> Tuple[int, int]:
        pos = pyautogui.position()
        return (pos.x, pos.y)

    # -------- Keyboard --------
    def type_text(self, text: str, interval: float = 0, wpm: Optional[int] = None) -> None:
        if wpm is not None:
            chars_per_second = (wpm * 5) / 60
            interval = 1.0 / chars_per_second
        if self._check_approval(f"type text: '{text[:50]}...'" ):
            pyautogui.write(text, interval=interval)

    def press(self, key: str, presses: int = 1, interval: float = 0.1) -> None:
        if self._check_approval(f"press '{key}' {presses}x"):
            pyautogui.press(key, presses=presses, interval=interval)

    def hotkey(self, *keys, interval: float = 0.05) -> None:
        keys_str = "+".join(keys)
        if self._check_approval(f"hotkey: {keys_str}"):
            pyautogui.hotkey(*keys, interval=interval)

    # -------- Convenience --------
    def wait(self, seconds: float = 15) -> None:
        """Default wait for app launches or heavy UI updates."""
        time.sleep(seconds)

    def launch_app(self, app_name: str, wait_seconds: float = 15, window_title: Optional[str] = None,
                   auto_detect_window: bool = True) -> Optional[str]:
        """Open start menu, type app name, press enter, then wait.
        If window_title is set, retry wait/check. If auto_detect_window, return new window title.
        """
        baseline = self.get_all_windows() if auto_detect_window else []
        self.press('win')
        time.sleep(0.2)
        self.type_text(app_name)
        time.sleep(0.2)
        self.press('enter')
        if window_title:
            if not self.wait_retry_window(window_title, wait_seconds=wait_seconds):
                raise RuntimeError(f"Window '{window_title}' not detected after waiting")
            return window_title
        if auto_detect_window:
            neww = self.wait_retry_new_window(baseline, wait_seconds=wait_seconds)
            if not neww:
                raise RuntimeError("No new window detected after waiting")
            return neww
        self.wait(wait_seconds)
        return None

    def open_url(self, url: str, wait_seconds: float = 15) -> None:
        """Focus address bar and open URL, then wait."""
        self.hotkey('ctrl', 'l')
        self.type_text(url)
        self.press('enter')
        self.wait(wait_seconds)

    def _window_exists(self, title_substring: str) -> bool:
        try:
            return any(title_substring.lower() in w.lower() for w in self.get_all_windows())
        except Exception:
            return False

    def _wait_retry_predicate(self, predicate, wait_seconds: float = 15) -> bool:
        """Wait, check predicate; if false, wait again and re-check."""
        self.wait(wait_seconds)
        if predicate():
            return True
        self.wait(wait_seconds)
        return predicate()

    def smart_retry(self, action_fn, check_fn, wait_seconds: float = 15, retries: int = 2) -> bool:
        """Run action, wait->check, retry with wait. Avoid rapid loops."""
        for attempt in range(retries):
            action_fn()
            self.wait(wait_seconds)
            if check_fn():
                return True
        return False

    def wait_retry_window(self, title_substring: str, wait_seconds: float = 15) -> bool:
        return self._wait_retry_predicate(lambda: self._window_exists(title_substring), wait_seconds)

    def wait_retry_new_window(self, baseline: List[str], wait_seconds: float = 15) -> Optional[str]:
        """Wait for any new window title not in baseline; retry once."""
        def _new_window():
            now = self.get_all_windows()
            diff = [w for w in now if w not in baseline]
            return diff[0] if diff else None
        first = _new_window()
        if first:
            return first
        if self._wait_retry_predicate(lambda: bool(_new_window()), wait_seconds):
            return _new_window()
        return None

    def open_chrome(self, url: Optional[str] = None, wait_seconds: float = 15) -> None:
        """Launch Chrome and optionally open URL. Waits 15s; retries once if not found."""
        try:
            self.launch_app('chrome', wait_seconds=wait_seconds, window_title='Chrome')
        except RuntimeError:
            # fallback: try auto-detect window without title
            self.launch_app('chrome', wait_seconds=wait_seconds, window_title=None, auto_detect_window=True)
        if url:
            self.open_url(url, wait_seconds=wait_seconds)

    # -------- Multi-monitor Support --------
    def get_monitors(self) -> List[dict]:
        """Return list of monitors with position and size."""
        import subprocess
        import re
        try:
            out = subprocess.check_output(['xrandr'], text=True)
            monitors = []
            for line in out.split('\n'):
                # Match: "HDMI-0 connected primary 1920x1080+1366+0"
                match = re.match(r'^(\S+)\s+connected\s+(?:primary\s+)?(\d+)x(\d+)\+(\d+)\+(\d+)', line)
                if match:
                    name = match.group(1)
                    width = int(match.group(2))
                    height = int(match.group(3))
                    x = int(match.group(4))
                    y = int(match.group(5))
                    monitors.append({'name': name, 'x': x, 'y': y, 'width': width, 'height': height})
            if monitors:
                return monitors
            return [{'name': 'primary', 'x': 0, 'y': 0, 'width': self.screen_width, 'height': self.screen_height}]
        except Exception as e:
            logger.warning(f"Failed to get monitors: {e}")
            return [{'name': 'primary', 'x': 0, 'y': 0, 'width': self.screen_width, 'height': self.screen_height}]

    def click_monitor(self, monitor_index: int, relative_x: int, relative_y: int) -> None:
        """Click on a specific monitor using relative coordinates (0-1 range)."""
        monitors = self.get_monitors()
        if monitor_index >= len(monitors):
            raise ValueError(f"Monitor {monitor_index} not found")
        mon = monitors[monitor_index]
        x = mon['x'] + int(relative_x * mon['width'])
        y = mon['y'] + int(relative_y * mon['height'])
        self.click(x=x, y=y)

    # -------- State Detection --------
    def wait_for_text(self, text: str, timeout: float = 30, confidence: float = 0.7) -> bool:
        """Wait for text to appear on screen (OCR). Returns True if found."""
        if not _ocr_available:
            logger.warning("OCR not available - install pytesseract and tesseract-ocr")
            return False
        from PIL import Image
        import numpy as np
        
        start = time.time()
        while time.time() - start < timeout:
            try:
                img = self.screenshot()
                gray = img.convert('L')
                arr = np.array(gray)
                config = '--psm 6'
                extracted = pytesseract.image_to_string(Image.fromarray(arr), config=config)
                if text.lower() in extracted.lower():
                    self.log_action(f"Text found: {text}")
                    return True
            except Exception as e:
                logger.debug(f"OCR check failed: {e}")
            self.wait(2)
        self.log_action(f"Text not found: {text}")
        return False

    def detect_state(self, expected_text: str, timeout: float = 10) -> bool:
        """Quick check if text exists on screen."""
        return self.wait_for_text(expected_text, timeout=timeout)

    # -------- OCR Helpers --------
    def read_text_on_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> str:
        """Read text from entire screen or specific region (x, y, w, h)."""
        if not _ocr_available:
            logger.warning("OCR not available - install pytesseract and tesseract-ocr")
            return ""
        from PIL import Image
        
        img = self.screenshot()
        if region:
            x, y, w, h = region
            img = img.crop((x, y, x + w, y + h))
        gray = img.convert('L')
        text = pytesseract.image_to_string(gray)
        self.log_action(f"OCR read: {len(text)} chars")
        return text

    # -------- Enhanced Logging --------
    def log_action(self, message: str) -> None:
        """Log action with timestamp (no secrets)."""
        if not self.log_path:
            return
        try:
            ts = time.strftime('%Y-%m-%d %H:%M:%S')
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(f"[{ts}] {message}\n")
        except Exception:
            pass

    # -------- Robust Retry (Stabilitas) --------
    def robust_click(self, x: int, y: int, retries: int = 2) -> bool:
        """Click with retry on failure."""
        for attempt in range(retries + 1):
            try:
                self.click(x=x, y=y)
                self.wait(1)
                return True
            except Exception as e:
                logger.warning(f"Click failed (attempt {attempt + 1}): {e}")
                if attempt < retries:
                    self.wait(2)
        return False

    def robust_type(self, text: str, retries: int = 2) -> bool:
        """Type text with retry on failure."""
        for attempt in range(retries + 1):
            try:
                self.type_text(text)
                self.wait(0.5)
                return True
            except Exception as e:
                logger.warning(f"Type failed (attempt {attempt + 1}): {e}")
                if attempt < retries:
                    self.wait(2)
        return False

    # -------- Smart Wait (Loading Detection) --------
    def smart_wait(self, check_fn, timeout: float = 30, interval: float = 1) -> bool:
        """Wait until check_fn returns True or timeout. Unlike simple sleep, this polls."""
        start = time.time()
        while time.time() - start < timeout:
            if check_fn():
                return True
            time.sleep(interval)
        return False

    def wait_for_window_stable(self, title_substring: str, wait_seconds: float = 15) -> bool:
        """Wait for window to appear and stabilize (no resize for 2s)."""
        if not self.wait_retry_window(title_substring, wait_seconds=wait_seconds):
            return False
        # wait for stability
        time.sleep(2)
        return True

    # -------- Drag & Drop --------
    def drag_drop(self, from_x: int, from_y: int, to_x: int, to_y: int, duration: float = 0.5) -> None:
        """Drag from (x1, y1) to (x2, y2)."""
        pyautogui.moveTo(from_x, from_y, duration=0.2)
        pyautogui.mouseDown()
        pyautogui.moveTo(to_x, to_y, duration=duration)
        pyautogui.mouseUp()

    def drag_file_to_app(self, file_path: str, target_x: int, target_y: int) -> None:
        """Drag a file to a specific position (e.g., drop file to app)."""
        self.drag_drop(0, 0, target_x, target_y, duration=1)

    # -------- Window Manager --------
    def resize_window(self, title_substring: str, width: int, height: int) -> bool:
        import subprocess
        try:
            # Get window ID
            out = subprocess.check_output(['wmctrl', '-l'], text=True)
            for line in out.split('\n'):
                if title_substring.lower() in line.lower():
                    win_id = line.split()[0]
                    subprocess.run(['wmctrl', '-ir', win_id, '-e', f'0,-1,-1,{width},{height}'])
                    return True
            return False
        except Exception as e:
            logger.warning(f"Resize failed: {e}")
            return False

    def minimize_window(self, title_substring: str) -> bool:
        import subprocess
        try:
            out = subprocess.check_output(['wmctrl', '-l'], text=True)
            for line in out.split('\n'):
                if title_substring.lower() in line.lower():
                    win_id = line.split()[0]
                    subprocess.run(['xdotool', 'windowminimize', win_id])
                    return True
            return False
        except Exception as e:
            logger.warning(f"Minimize failed: {e}")
            return False

    def maximize_window(self, title_substring: str) -> bool:
        import subprocess
        try:
            out = subprocess.check_output(['wmctrl', '-l'], text=True)
            for line in out.split('\n'):
                if title_substring.lower() in line.lower():
                    win_id = line.split()[0]
                    subprocess.run(['wmctrl', '-ir', win_id, '-b', 'add,maximized_vert,maximized_horz'])
                    return True
            return False
        except Exception as e:
            logger.warning(f"Maximize failed: {e}")
            return False

    # -------- Multi-Browser Support --------
    def open_firefox(self, url: Optional[str] = None, wait_seconds: float = 15) -> None:
        """Open Firefox and optionally navigate to URL."""
        self.launch_app('firefox', wait_seconds=wait_seconds, window_title='Firefox')
        if url:
            self.open_url(url, wait_seconds=wait_seconds)

    def open_edge(self, url: Optional[str] = None, wait_seconds: float = 15) -> None:
        """Open Microsoft Edge and optionally navigate to URL."""
        self.launch_app('edge', wait_seconds=wait_seconds, window_title='Microsoft Edge')
        if url:
            self.open_url(url, wait_seconds=wait_seconds)

    # -------- Keyboard Layout Auto-detect --------
    def detect_keyboard_layout(self) -> str:
        """Detect current keyboard layout (returns: qwerty, qwertz, azerty, unknown)."""
        try:
            import subprocess
            out = subprocess.check_output(['setxkbmap', '-query'], text=True)
            layout = out.get('layout', '')
            if 'us' in layout:
                return 'qwerty'
            elif 'de' in layout:
                return 'qwertz'
            elif 'fr' in layout:
                return 'azerty'
        except Exception:
            pass
        return 'qwerty'  # default

    # -------- AI Element Detection (OpenCV) --------
    def find_element_by_color(self, target_color: tuple, tolerance: int = 30) -> Optional[Tuple[int, int]]:
        """Find element by color RGB. Returns (x, y) center or None."""
        try:
            from PIL import Image
            import numpy as np
            
            img = self.screenshot()
            arr = np.array(img)
            
            # Simple color matching
            r, g, b = target_color
            mask = (
                (np.abs(arr[:,:,0] - r) <= tolerance) &
                (np.abs(arr[:,:,1] - g) <= tolerance) &
                (np.abs(arr[:,:,2] - b) <= tolerance)
            )
            
            coords = np.where(mask)
            if len(coords[0]) > 0:
                y_center = int(np.mean(coords[0]))
                x_center = int(np.mean(coords[1]))
                return (x_center, y_center)
        except Exception as e:
            logger.warning(f"Color detection failed: {e}")
        return None

    def find_button_vision(self, template_path: str, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
        """Find button/image on screen and return center coordinates."""
        try:
            loc = self.find_on_screen(template_path, confidence=confidence)
            if loc:
                return (loc.left + loc.width // 2, loc.top + loc.height // 2)
        except Exception:
            pass
        return None

    # -------- Flow Recorder --------
    _recorded_actions: List[dict] = []
    
    def start_recording(self) -> None:
        """Start recording actions."""
        self._recorded_actions = []
        self.log_action("Recording started")

    def record_action(self, action_type: str, **kwargs) -> None:
        """Record an action for replay."""
        self._recorded_actions.append({'type': action_type, 'params': kwargs, 'time': time.time()})

    def stop_recording(self) -> List[dict]:
        """Stop recording and return recorded actions."""
        self.log_action(f"Recording stopped: {len(self._recorded_actions)} actions")
        return self._recorded_actions.copy()

    def replay_actions(self, actions: Optional[List[dict]] = None, delay_multiplier: float = 1.0) -> None:
        """Replay recorded actions with optional speed control."""
        if actions is None:
            actions = self._recorded_actions
        for i, action in enumerate(actions):
            action_type = action.get('type')
            params = action.get('params', {})
            
            if action_type == 'click':
                self.click(x=params.get('x'), y=params.get('y'))
            elif action_type == 'type':
                self.type_text(params.get('text', ''))
            elif action_type == 'press':
                self.press(params.get('key', 'enter'))
            elif action_type == 'hotkey':
                self.hotkey(*params.get('keys', []))
            elif action_type == 'wait':
                self.wait(params.get('seconds', 1) * delay_multiplier)
            
            # delay between actions
            time.sleep(0.5 * delay_multiplier)

    # -------- UI Helpers --------
    def click_image(self, image_path: str, confidence: float = 0.8) -> bool:
        try:
            loc = self.find_on_screen(image_path, confidence=confidence)
        except Exception:
            loc = None
        if loc is None:
            return False
        x, y = loc.left + loc.width // 2, loc.top + loc.height // 2
        self.click(x=x, y=y)
        return True

    def click_image_or(self, image_path: str, fallback_x: int, fallback_y: int, confidence: float = 0.8) -> bool:
        """Try click by image; fallback to coordinates."""
        if self.click_image(image_path, confidence=confidence):
            return True
        self.click(x=fallback_x, y=fallback_y)
        return False

    def login_form(self, email: str, password: str, submit: bool = True,
                   click_x: Optional[int] = None, click_y: Optional[int] = None,
                   wait_seconds: float = 15) -> None:
        """Simple login helper: click (optional), type email, tab, type password, enter."""
        if click_x is not None and click_y is not None:
            self.click(x=click_x, y=click_y)
        self.type_text(email)
        self.press('tab')
        self.type_text(password)
        if submit:
            self.press('enter')
        self.wait(wait_seconds)

    # -------- State verification --------
    def ensure_window(self, title_substring: str, wait_seconds: float = 15) -> bool:
        """Ensure a window exists by title substring with wait+retry."""
        return self.wait_retry_window(title_substring, wait_seconds=wait_seconds)

    def active_window_contains(self, title_substring: str) -> bool:
        title = self.get_active_window() or ""
        return title_substring.lower() in title.lower()

    # -------- Error recovery --------
    def recover_reload(self, wait_seconds: float = 5) -> None:
        self.hotkey('ctrl', 'r')
        self.wait(wait_seconds)

    def recover_back(self, wait_seconds: float = 5) -> None:
        self.hotkey('alt', 'left')
        self.wait(wait_seconds)

    def retry_with_recovery(self, action_fn, check_fn, wait_seconds: float = 15, retries: int = 1) -> bool:
        """Run action -> wait -> check; on fail, reload+retry (with wait)."""
        for attempt in range(retries + 1):
            action_fn()
            self.wait(wait_seconds)
            if check_fn():
                return True
            if attempt < retries:
                self.recover_reload(wait_seconds=5)
        return False

    # -------- Workflow DSL --------
    def run_steps(self, steps: List[dict], default_wait: float = 15) -> None:
        """Run a list of step dicts. Supported actions: wait, click, type, press, hotkey,
        open_url, launch_app, open_chrome, login_form, click_image, click_image_or,
        ensure_window, screenshot, back, reload.
        """
        for step in steps:
            action = step.get('action')
            if action == 'wait':
                self.wait(step.get('seconds', default_wait))
            elif action == 'click':
                self.click(x=step.get('x'), y=step.get('y'))
            elif action == 'type':
                self.type_text(step.get('text', ''))
            elif action == 'press':
                self.press(step.get('key', 'enter'))
            elif action == 'hotkey':
                self.hotkey(*step.get('keys', []))
            elif action == 'open_url':
                self.open_url(step.get('url', ''), wait_seconds=step.get('wait', default_wait))
            elif action == 'launch_app':
                self.launch_app(step.get('app', ''), wait_seconds=step.get('wait', default_wait),
                                window_title=step.get('window_title'),
                                auto_detect_window=step.get('auto_detect_window', True))
            elif action == 'open_chrome':
                self.open_chrome(step.get('url'), wait_seconds=step.get('wait', default_wait))
            elif action == 'login_form':
                self.login_form(step.get('email', ''), step.get('password', ''),
                                submit=step.get('submit', True),
                                click_x=step.get('x'), click_y=step.get('y'),
                                wait_seconds=step.get('wait', default_wait))
            elif action == 'click_image':
                self.click_image(step.get('image', ''), confidence=step.get('confidence', 0.8))
            elif action == 'click_image_or':
                self.click_image_or(step.get('image', ''), step.get('x', 0), step.get('y', 0),
                                    confidence=step.get('confidence', 0.8))
            elif action == 'ensure_window':
                ok = self.ensure_window(step.get('title', ''), wait_seconds=step.get('wait', default_wait))
                if not ok:
                    raise RuntimeError(f"Window not found: {step.get('title','')}")
            elif action == 'screenshot':
                self.screenshot_to(step.get('path', '/tmp/screen.png'))
            elif action == 'back':
                self.recover_back(wait_seconds=step.get('wait', 5))
            elif action == 'reload':
                self.recover_reload(wait_seconds=step.get('wait', 5))
            else:
                raise ValueError(f"Unknown action: {action}")

    # -------- Presets --------
    def register_preset(self, name: str, func) -> None:
        self.presets[name] = func

    def run_preset(self, name: str, *args, **kwargs):
        if name not in self.presets:
            raise ValueError(f"Preset '{name}' not found")
        return self.presets[name](*args, **kwargs)

    # -------- Screen --------
    def screenshot(self, region: Optional[Tuple[int, int, int, int]] = None,
                   filename: Optional[str] = None):
        img = pyautogui.screenshot(region=region)
        if filename:
            img.save(filename)
        else:
            return img

    def screenshot_to(self, filename: str, region: Optional[Tuple[int, int, int, int]] = None) -> str:
        """Take a screenshot and save to filename. Returns filename."""
        self.screenshot(region=region, filename=filename)
        return filename

    def record_screen(self, output_path: str, seconds: int = 30, fps: int = 25,
                      display: Optional[str] = None, resolution: Optional[str] = None) -> str:
        """Record screen using ffmpeg. Requires ffmpeg installed."""
        if display is None:
            display = os.environ.get("DISPLAY", ":0")
        if resolution is None:
            resolution = f"{self.screen_width}x{self.screen_height}"
        cmd = [
            "ffmpeg", "-y",
            "-f", "x11grab",
            "-video_size", resolution,
            "-i", f"{display}.0",
            "-t", str(seconds),
            "-r", str(fps),
            output_path
        ]
        subprocess.run(cmd, check=True)
        return output_path

    def get_pixel_color(self, x: int, y: int) -> Tuple[int, int, int]:
        return pyautogui.pixel(x, y)

    def find_on_screen(self, image_path: str, confidence: float = 0.8,
                       region: Optional[Tuple[int, int, int, int]] = None):
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence, region=region)
            return location
        except Exception as e:
            logger.error(f"Error finding image: {e}")
            return None

    def get_screen_size(self) -> Tuple[int, int]:
        return (self.screen_width, self.screen_height)

    # -------- Window ops --------
    def get_all_windows(self) -> List[str]:
        """
        Get list of open window titles.
        Uses wmctrl on Linux for reliable support.
        """
        try:
            import subprocess
            out = subprocess.check_output(["wmctrl", "-l"], text=True)
            titles = []
            for line in out.splitlines():
                parts = line.split(None, 3)
                if len(parts) == 4:
                    title = parts[3].strip()
                    if title:
                        titles.append(title)
            return titles
        except FileNotFoundError:
            logger.error("wmctrl not found. Install: sudo apt-get install wmctrl")
            return []
        except Exception as e:
            logger.error(f"Error getting windows: {e}")
            return []

    def activate_window(self, title_substring: str) -> bool:
        """
        Activate a window by title substring using wmctrl.
        """
        try:
            env = os.environ.copy()
            if not env.get("DISPLAY"):
                detected = self._auto_detect_display()
                if detected:
                    env["DISPLAY"] = detected
            subprocess.check_call(["wmctrl", "-a", title_substring], env=env)
            return True
        except FileNotFoundError:
            logger.error("wmctrl not found. Install: sudo apt-get install wmctrl")
            return False
        except Exception as e:
            logger.error(f"Error activating window: {e}")
            return False

    def focus_window_or_click(self, title_substring: str, fallback_x: int, fallback_y: int) -> None:
        """Try to focus window; fallback to clicking a coordinate."""
        if not self.activate_window(title_substring):
            self.click(x=fallback_x, y=fallback_y)

    def get_active_window(self) -> Optional[str]:
        """
        Get active window title using xdotool if available.
        """
        try:
            import subprocess
            out = subprocess.check_output(["xdotool", "getactivewindow", "getwindowname"], text=True)
            return out.strip() if out else None
        except FileNotFoundError:
            logger.warning("xdotool not found. Install: sudo apt-get install xdotool")
            return None
        except Exception as e:
            logger.error(f"Error getting active window: {e}")
            return None

    # -------- Clipboard --------
    def copy_to_clipboard(self, text: str) -> None:
        try:
            import pyperclip
            pyperclip.copy(text)
        except Exception as e:
            logger.error(f"Clipboard copy error: {e}")

    def get_from_clipboard(self) -> Optional[str]:
        try:
            import pyperclip
            return pyperclip.paste()
        except Exception as e:
            logger.error(f"Clipboard paste error: {e}")
            return None


# Convenience export
__all__ = ["DesktopControllerLinux"]
