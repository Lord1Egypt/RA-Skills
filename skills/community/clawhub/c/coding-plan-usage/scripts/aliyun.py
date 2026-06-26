import os
import re
import json
import subprocess
from typing import Any, Optional, Tuple, List, Dict

class AgentBrowserSession:
    DEFAULT_AGENT_BROWSER_PATH = "agent-browser"
    DEFAULT_SESSION_NAME = "jeayapp"
    ENV_KEY_PATH = "AGENT_BROWSER_PATH"
    ENV_KEY_DEV_MODE = "AGENT_BROWSER_DEV_MODE"
    ENV_KEY_SESSION_NAME = "AGENT_BROWSER_SESSION_NAME"

    def __init__(self, target_url: str):
        self.target_url = target_url.strip()
        if not self.target_url:
            raise ValueError("target url is required")
        self.config = self.load_agent_browser_config()
        self.opened = False

    def load_agent_browser_config(self) -> Dict[str, Any]:
        path = self.non_empty_or_default(self.resolve_env_value(self.ENV_KEY_PATH), self.DEFAULT_AGENT_BROWSER_PATH)
        session_name = self.non_empty_or_default(self.resolve_env_value(self.ENV_KEY_SESSION_NAME), self.DEFAULT_SESSION_NAME)
        dev_mode = self.is_dev_mode(self.resolve_env_value(self.ENV_KEY_DEV_MODE))

        # 仅在开发模式下输出调试信息
        if dev_mode:
            print(f"DEBUG: AGENT_BROWSER_PATH from env: {self.resolve_env_value(self.ENV_KEY_PATH)}")
            print(f"DEBUG: Final agent-browser path: {path}")

        return {
            "path": path,
            "session_name": session_name,
            "dev_mode": dev_mode
        }

    def resolve_env_value(self, key: str) -> str:
        for env_path in self.env_file_candidates():
            values = self.parse_env_file(env_path)
            if key in values:
                return values[key]
        env_value = os.environ.get(key, "")
        return env_value

    def env_file_candidates(self) -> List[str]:
        candidates = []
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            script_sibling_env_path = os.path.join(os.path.dirname(script_dir), ".env")
            if os.path.exists(script_sibling_env_path):
                candidates.append(script_sibling_env_path)
                return candidates
        except:
            pass

        try:
            working_dir = os.getcwd()
            working_dir_env_path = os.path.join(working_dir, ".env")
            candidates.append(working_dir_env_path)
        except:
            pass

        return candidates

    def parse_env_file(self, env_file_path: str) -> Dict[str, str]:
        values = {}
        try:
            with open(env_file_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split("=", 1)
                    if len(parts) != 2:
                        continue
                    key = parts[0].strip()
                    value = parts[1].strip()
                    value = value.strip('"\'')
                    if key and value:
                        values[key] = value
        except:
            pass
        return values

    def is_dev_mode(self, value: str) -> bool:
        lower_value = value.strip().lower()
        return lower_value in ["1", "true", "yes", "y", "on", "是"]

    def non_empty_or_default(self, value: str, default_value: str) -> str:
        if value.strip():
            return value
        return default_value

    def run(self, args: List[str]) -> Tuple[str, Optional[Exception]]:
        try:
            # 尝试使用系统PATH查找agent-browser
            import shutil
            agent_browser_path = shutil.which(self.config["path"])
            if agent_browser_path:
                # 仅在开发模式下输出调试信息
                if self.config.get("dev_mode", False):
                    print(f"DEBUG: Found agent-browser in PATH: {agent_browser_path}")
                cmd = [agent_browser_path] + args
            else:
                # 仅在开发模式下输出调试信息
                if self.config.get("dev_mode", False):
                    print(f"DEBUG: agent-browser not found in PATH, using: {self.config['path']}")
                cmd = [self.config["path"]] + args

            # 仅在开发模式下输出调试信息
            if self.config.get("dev_mode", False):
                print(f"DEBUG: Executing command: {cmd}")
                print(f"DEBUG: PATH environment variable: {os.environ.get('PATH', '')}")

            # 使用utf-8编码避免UnicodeDecodeError
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', check=True)
            return result.stdout, None
        except subprocess.CalledProcessError as e:
            # 输出错误信息，无论是否在开发模式下
            try:
                print(f"Error executing agent-browser: {e}")
                if e.stderr:
                    print(f"Stderr: {e.stderr}")
            except UnicodeEncodeError:
                # 处理编码错误
                print("Error executing agent-browser: Command failed")
                if e.stderr:
                    try:
                        print(f"Stderr: {e.stderr}")
                    except UnicodeEncodeError:
                        print("Stderr: (contains non-ASCII characters)")
            # 仅在开发模式下输出额外的调试信息
            if self.config.get("dev_mode", False):
                try:
                    print(f"DEBUG: CalledProcessError: {e}")
                    print(f"DEBUG: Stderr: {e.stderr}")
                except UnicodeEncodeError:
                    print("DEBUG: CalledProcessError: Command failed")
                    print("DEBUG: Stderr: (contains non-ASCII characters)")
            return e.stdout, e
        except Exception as e:
            # 输出错误信息，无论是否在开发模式下
            try:
                print(f"Error executing agent-browser: {e}")
            except UnicodeEncodeError:
                # 处理编码错误
                print("Error executing agent-browser: An error occurred")
            # 仅在开发模式下输出额外的调试信息
            if self.config.get("dev_mode", False):
                try:
                    print(f"DEBUG: Exception: {e}")
                except UnicodeEncodeError:
                    print("DEBUG: Exception: (contains non-ASCII characters)")
            return "", e

    def open(self) -> Tuple[str, Optional[Exception]]:
        args = ["--session-name", self.config["session_name"]]
        if self.config["dev_mode"]:
            args.append("--headed")
        args.extend(["open", self.target_url])
        output, err = self.run(args)
        if err is None:
            self.opened = True
        return output, err

    def close(self) -> Tuple[str, Optional[Exception]]:
        if not self.opened:
            return "", None
        args = ["--session-name", self.config["session_name"], "close"]
        output, err = self.run(args)
        if err is None:
            self.opened = False
        return output, err

class AliyunCodingLoginClient:
    ALIYUN_HOME_URL = "https://cn.aliyun.com/"
    ALIYUN_DIRECT_LOGIN_URL = "https://account.aliyun.com/login/login.htm"
    CODING_PLAN_DETAIL_URL = "https://bailian.console.aliyun.com/cn-beijing/?tab=coding-plan#/efm/detail"
    PAGE_WAIT_MS = 15000
    LOGIN_QR_WAIT_MS = 8000
    LOGIN_QR_WAIT_RETRIES = 3

    def __init__(self, session: AgentBrowserSession):
        self.session = session

    def close(self) -> Tuple[str, Optional[Exception]]:
        if not self.session:
            return "", None
        return self.session.close()

    def run(self) -> Tuple[Dict[str, Any], str, Optional[Exception]]:
        result = {
            "AlreadyLoggedIn": False,
            "EnteredLogin": False,
            "ScreenshotPath": "",
            "ScanCompleted": False,
            "Hours5ResetTime": "",
            "Hours5Usage": "",
            "WeekResetTime": "",
            "WeekUsage": "",
            "MonthResetTime": "",
            "MonthUsage": ""
        }
        logs = []

        wait_output, err = self.wait_window_ready()
        if wait_output.strip():
            logs.append(wait_output)
        if err:
            return result, "\n".join(logs), err

        snapshot_output, err = self.snapshot_interactive()
        if self.should_print_snapshot_output() and snapshot_output.strip():
            logs.append(snapshot_output)
        if err:
            return result, "\n".join(logs), err

        result["AlreadyLoggedIn"] = self.is_logged_in_from_snapshot(snapshot_output)
        if result["AlreadyLoggedIn"]:
            open_output, open_err = self.open_coding_plan_detail()
            if open_output.strip():
                logs.append(open_output)
            if open_err:
                return result, "\n".join(logs), open_err
            detail_snapshot, detail_err = self.snapshot_all()
            if self.should_print_snapshot_output() and detail_snapshot.strip():
                logs.append(detail_snapshot)
            if detail_err:
                return result, "\n".join(logs), detail_err
            self.fill_usage_from_snapshot(result, detail_snapshot)
            if not (result["Hours5Usage"] or result["WeekUsage"] or result["MonthUsage"]):
                fallback_snapshot, fallback_err = self.snapshot_interactive()
                if self.should_print_snapshot_output() and fallback_snapshot.strip():
                    logs.append(fallback_snapshot)
                if not fallback_err:
                    self.fill_usage_from_snapshot(result, fallback_snapshot)
            result["ScanCompleted"] = True
            return result, "\n".join(logs), None

        login_ref, err = self.find_login_ref(snapshot_output)
        if err:
            direct_login_output, direct_login_err = self.open_direct_login_page()
            if direct_login_output.strip():
                logs.append(direct_login_output)
            if direct_login_err:
                return result, "\n".join(logs), Exception(f"{err}; direct login fallback failed: {direct_login_err}")
            qr_wait_output, qr_wait_err = self.wait_for_login_qr_ready()
            if qr_wait_output.strip():
                logs.append(qr_wait_output)
            if qr_wait_err:
                return result, "\n".join(logs), qr_wait_err
            screenshot_path, screenshot_output, screenshot_err = self.capture_screenshot_in_cwd()
            if screenshot_output.strip():
                logs.append(screenshot_output)
            if screenshot_err:
                return result, "\n".join(logs), screenshot_err
            result["EnteredLogin"] = True
            result["ScreenshotPath"] = to_script_based_abs_path(screenshot_path)
            result["ScanCompleted"] = False
            return result, "\n".join(logs), None

        click_output, err = self.click_login_by_ref(login_ref)
        if click_output.strip():
            logs.append(click_output)
        if err:
            return result, "\n".join(logs), err
        result["EnteredLogin"] = True

        ready_output, err = self.wait_window_ready()
        if ready_output.strip():
            logs.append(ready_output)
        if err:
            return result, "\n".join(logs), err
        qr_wait_output, qr_wait_err = self.wait_for_login_qr_ready()
        if qr_wait_output.strip():
            logs.append(qr_wait_output)
        if qr_wait_err:
            return result, "\n".join(logs), qr_wait_err

        screenshot_path, screenshot_output, err = self.capture_screenshot_in_cwd()
        if screenshot_output.strip():
            logs.append(screenshot_output)
        if err:
            return result, "\n".join(logs), err
        result["ScreenshotPath"] = to_script_based_abs_path(screenshot_path)
        result["ScanCompleted"] = False

        return result, "\n".join(logs), None

    def snapshot_interactive(self) -> Tuple[str, Optional[Exception]]:
        output, err = self.run_session_command(["snapshot", "-i"])
        if err:
            return output or "", Exception(f"failed to snapshot aliyun home page: {err}")
        return output or "", None

    def should_print_snapshot_output(self) -> bool:
        if not self.session:
            return False
        return self.session.config.get("dev_mode", False)

    def snapshot_all(self) -> Tuple[str, Optional[Exception]]:
        output, err = self.run_session_command(["snapshot"])
        if err:
            return output, Exception(f"failed to snapshot aliyun page: {err}")
        return output, None

    def open_coding_plan_detail(self) -> Tuple[str, Optional[Exception]]:
        logs = []
        output, err = self.run_session_command(["open", self.CODING_PLAN_DETAIL_URL])
        if output.strip():
            logs.append(output)
        if err:
            return "\n".join(logs), Exception(f"failed to open coding plan detail page: {err}")
        wait_output, wait_err = self.wait_window_ready()
        if wait_output.strip():
            logs.append(wait_output)
        if wait_err:
            return "\n".join(logs), wait_err
        return "\n".join(logs), None

    def open_direct_login_page(self) -> Tuple[str, Optional[Exception]]:
        logs = []
        output, err = self.run_session_command(["open", self.ALIYUN_DIRECT_LOGIN_URL])
        if output.strip():
            logs.append(output)
        if err:
            return "\n".join(logs), Exception(f"failed to open direct login page: {err}")
        wait_output, wait_err = self.wait_window_ready()
        if wait_output.strip():
            logs.append(wait_output)
        if wait_err:
            return "\n".join(logs), wait_err
        return "\n".join(logs), None

    def wait_for_login_qr_ready(self) -> Tuple[str, Optional[Exception]]:
        logs = []
        for _ in range(self.LOGIN_QR_WAIT_RETRIES):
            wait_output, wait_err = self.wait_window_ready(self.LOGIN_QR_WAIT_MS)
            if wait_output.strip():
                logs.append(wait_output)
            if wait_err:
                return "\n".join(logs), wait_err
            snapshot_output, snapshot_err = self.snapshot_interactive()
            if self.should_print_snapshot_output() and snapshot_output.strip():
                logs.append(snapshot_output)
            if snapshot_err:
                continue
            if self.has_login_qr(snapshot_output):
                return "\n".join(logs), None
        return "\n".join(logs), None

    def fill_usage_from_snapshot(self, result: Dict[str, Any], snapshot_output: str):
        result["Hours5ResetTime"], result["Hours5Usage"] = self.extract_usage_by_marker(snapshot_output, "近一周用量")
        result["WeekResetTime"], result["WeekUsage"] = self.extract_usage_by_marker(snapshot_output, "近一月用量")
        result["MonthResetTime"], result["MonthUsage"] = self.extract_usage_by_marker(snapshot_output, "套餐专属API Key")
        if not result["MonthUsage"]:
            result["MonthResetTime"], result["MonthUsage"] = self.extract_usage_by_marker(snapshot_output, "套餐专属API")
        if not (result["Hours5Usage"] and result["WeekUsage"] and result["MonthUsage"]):
            sequence = self.extract_usage_by_sequence(snapshot_output)
            if len(sequence) >= 3:
                if not result["Hours5Usage"]:
                    result["Hours5ResetTime"], result["Hours5Usage"] = sequence[0][0], sequence[0][1]
                if not result["WeekUsage"]:
                    result["WeekResetTime"], result["WeekUsage"] = sequence[1][0], sequence[1][1]
                if not result["MonthUsage"]:
                    result["MonthResetTime"], result["MonthUsage"] = sequence[2][0], sequence[2][1]

    def is_logged_in_from_snapshot(self, snapshot_output: str) -> bool:
        content = snapshot_output.lower()
        not_logged_in_markers = [
            "登录阿里云",
            "立即登录",
            "快捷注册",
            "sign in",
            "log in",
        ]
        for marker in not_logged_in_markers:
            if marker.lower() in content:
                return False

        logged_in_markers = [
            "退出登录",
            "sign out",
            "账号中心",
            "accesskey",
        ]
        for marker in logged_in_markers:
            if marker.lower() in content:
                return True

        return False

    def has_login_qr(self, snapshot_output: str) -> bool:
        content = snapshot_output.lower()
        qr_markers = [
            "扫码登录",
            "二维码",
            "阿里云 app",
            "aliyun app",
            "scan",
        ]
        for marker in qr_markers:
            if marker.lower() in content:
                return True
        return False

    def find_login_ref(self, snapshot_output: str) -> Tuple[str, Optional[Exception]]:
        login_refs = self.extract_login_ref_candidates(snapshot_output)
        if not login_refs:
            return "", Exception("failed to find login ref from snapshot")
        return "@" + login_refs[0], None

    def click_login_by_ref(self, login_ref: str) -> Tuple[str, Optional[Exception]]:
        login_ref = login_ref.strip()
        if not login_ref:
            return "", Exception("login ref is required")
        if not login_ref.startswith("@"):
            login_ref = "@" + login_ref

        logs = []
        scroll_output, scroll_err = self.run_session_command(["scrollintoview", login_ref])
        if scroll_output.strip():
            logs.append(scroll_output)
        if scroll_err:
            click_output, click_err = self.run_session_command(["click", login_ref])
            if click_output.strip():
                logs.append(click_output)
            if click_err:
                return "\n".join(logs), Exception(f"failed to click login ref {login_ref}: {click_err}")
            return "\n".join(logs), None

        click_output, click_err = self.run_session_command(["click", login_ref])
        if click_output.strip():
            logs.append(click_output)
        if click_err:
            return "\n".join(logs), Exception(f"failed to click login ref {login_ref}: {click_err}")
        return "\n".join(logs), None

    def wait_window_ready(self, milliseconds: int = PAGE_WAIT_MS) -> Tuple[str, Optional[Exception]]:
        output, err = self.run_session_command(["wait", str(milliseconds)])
        if err:
            return output, Exception(f"failed to wait {milliseconds}ms: {err}")
        return output, None

    def capture_screenshot_in_cwd(self) -> Tuple[str, str, Optional[Exception]]:
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.abspath(os.path.join(script_dir, "aliyu-login.png"))
        except Exception as e:
            return "", "", Exception(f"failed to build screenshot path: {e}")

        output, err = self.run_session_command(["screenshot", file_path])
        if err:
            return "", output, Exception(f"failed to save login screenshot: {err}")
        return file_path, output, None

    def run_session_command(self, args: List[str]) -> Tuple[str, Optional[Exception]]:
        command_args = ["--session-name", self.session.config["session_name"]] + args
        output, err = self.session.run(command_args)
        return output or "", err

    def extract_login_ref_candidates(self, snapshot: str) -> List[str]:
        login_ref_regex = re.compile(r"\[ref=(e\d+)\]")
        lines = snapshot.split("\n")
        priority0 = []
        priority1 = []
        priority2 = []
        seen = set()

        for line in lines:
            if "[ref=" not in line or "登录" not in line:
                continue
            if "合作伙伴" in line or "管理后台" in line:
                continue
            matches = login_ref_regex.findall(line)
            if not matches:
                continue
            ref = matches[0]
            if ref in seen:
                continue
            seen.add(ref)

            if '"登录"' in line:
                priority0.append(ref)
                continue
            if '"登录阿里云"' in line:
                priority1.append(ref)
                continue
            priority2.append(ref)

        candidates = priority0 + priority1 + priority2
        return candidates

    def extract_usage_by_marker(self, snapshot_output: str, marker: str) -> Tuple[str, str]:
        line_pattern = re.compile(r"(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s*重置\s*([0-9]+%)")
        lines = snapshot_output.split("\n")
        for line in lines:
            if marker not in line:
                continue
            matches = line_pattern.findall(line)
            if matches:
                return matches[0][0], matches[0][1]
        return "", ""

    def extract_usage_by_sequence(self, snapshot_output: str) -> List[Tuple[str, str]]:
        pattern = re.compile(r"(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s*重置\s*([0-9]+%)")
        matches = pattern.findall(snapshot_output)
        result = []
        for match in matches:
            result.append((match[0], match[1]))
            if len(result) == 3:
                break
        return result

def should_print_agent_browser_output(client: AliyunCodingLoginClient) -> bool:
    return False

def to_script_based_abs_path(path: str) -> str:
    normalized = path.strip()
    if not normalized:
        return ""
    if os.path.isabs(normalized):
        return os.path.abspath(normalized)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(script_dir, normalized))

def main():
    try:
        session = AgentBrowserSession(AliyunCodingLoginClient.ALIYUN_HOME_URL)
        output, err = session.open()
        if err:
            if output.strip():
                print(output)
            print(f"Error executing command: {err}")
            return 1
        client = AliyunCodingLoginClient(session)
        if should_print_agent_browser_output(client) and output.strip():
            print(output)

        result, run_output, err = client.run()
        if should_print_agent_browser_output(client) and run_output.strip():
            print(run_output)
        if err:
            print(f"Error running aliyun login flow: {err}")
            return 1

        has_usage = bool(result.get("Hours5Usage", "").strip() or result.get("WeekUsage", "").strip() or result.get("MonthUsage", "").strip())
        if has_usage:
            response = {
                "hours5": {
                    "usage": result.get("Hours5Usage", ""),
                    "resetTime": result.get("Hours5ResetTime", "")
                },
                "week": {
                    "usage": result.get("WeekUsage", ""),
                    "resetTime": result.get("WeekResetTime", "")
                },
                "month": {
                    "usage": result.get("MonthUsage", ""),
                    "resetTime": result.get("MonthResetTime", "")
                }
            }
            payload = json.dumps(response, indent=2, ensure_ascii=False)
            print(payload)

            close_output, close_err = client.close()
            if should_print_agent_browser_output(client) and close_output.strip():
                print(close_output)
            if close_err:
                print(f"Error closing session: {close_err}")
                return 1
        else:
            print(f"Already logged in: {result.get('AlreadyLoggedIn', False)}")
            print(f"Entered login page: {result.get('EnteredLogin', False)}")
            screenshot_path = to_script_based_abs_path(result.get("ScreenshotPath", ""))
            if screenshot_path:
                print("请使用阿里云 App 扫码完成登录后，再次执行此程序以查询用量。")
                print(f"Login screenshot: {screenshot_path}")
            print(f"Scan completed: {result.get('ScanCompleted', False)}")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())
