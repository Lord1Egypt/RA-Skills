#!/usr/bin/env python3
"""
日报反馈收集服务
- 静态文件服务：serve output/ 目录
- 反馈接收：POST /api/feedback → 写入 data/feedback/{date}.json
- 自动超时退出（profile.yaml server.timeout_hours，默认 24 小时）
- 端口冲突时明确报错，不静默漂移
- 忽略 SIGHUP，后台运行时不被终端关闭杀死
"""
import fcntl
import http.server
import hashlib
import json
import os
import re
import signal
import subprocess
import sys
import socket
import threading
import time
from pathlib import Path
from functools import partial

DEFAULT_PORT = 17890
DEFAULT_HOST = "0.0.0.0"


def resolve_root_dir():
    """优先从环境变量/工作目录推断 Skill 根目录，避免依赖固定层级。"""
    env_root = os.environ.get("DAILY_ROOT") or os.environ.get("AI_DAILY_ROOT")
    candidates = []
    if env_root:
        candidates.append(Path(env_root).expanduser())

    cwd = Path.cwd().resolve()
    candidates.extend([cwd, *cwd.parents])

    script_dir = Path(__file__).resolve().parent
    candidates.extend([script_dir, *script_dir.parents])

    seen = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if (
            (candidate / "SKILL.md").exists()
            and (candidate / "reference" / "daily_example.html").exists()
            and (candidate / "scripts" / "feedback_server.py").exists()
        ):
            return candidate

    return script_dir.parent


ROOT_DIR = resolve_root_dir()
OUTPUT_DIR = ROOT_DIR / "output"
FEEDBACK_DIR = ROOT_DIR / "data" / "feedback"
PORT_FILE = ROOT_DIR / "data" / ".server_port"
PID_FILE = ROOT_DIR / "data" / ".server_pid"


def normalize_feedback_payload(body):
    """仅落盘完整 session 结构；兼容旧版事件批量上报但不写入正式反馈文件。"""
    if not isinstance(body, dict):
        return None, "invalid"

    if "session" in body and "explicit_feedback" in body and "implicit_feedback" in body:
        normalized = dict(body)
        normalized.setdefault("date", time.strftime("%Y-%m-%d"))
        return normalized, "summary"

    if "events" in body:
        return None, "event_batch"

    return None, "invalid"


def _is_string_list(value):
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _is_article_feedback_list(value):
    if not isinstance(value, list):
        return False
    for item in value:
        if not isinstance(item, dict):
            return False
        if not isinstance(item.get("id"), str):
            return False
        if not isinstance(item.get("title"), str):
            return False
        tags = item.get("tags", [])
        if tags is not None and not _is_string_list(tags):
            return False
    return True


def _is_dwell_list(value):
    if not isinstance(value, list):
        return False
    for item in value:
        if not isinstance(item, dict):
            return False
        if not isinstance(item.get("articleId"), str):
            return False
        if not isinstance(item.get("title"), str):
            return False
        if not _is_string_list(item.get("tags", [])):
            return False
        if not isinstance(item.get("dwell_seconds"), int):
            return False
    return True


def _is_ai_detail_list(value):
    if not isinstance(value, list):
        return False
    for item in value:
        if not isinstance(item, dict):
            return False
        if not isinstance(item.get("tool"), str):
            return False
        if not isinstance(item.get("prompt_preview"), str):
            return False
    return True


def _is_tag_score_list(value):
    if not isinstance(value, list):
        return False
    for item in value:
        if not isinstance(item, dict):
            return False
        if not isinstance(item.get("tag"), str):
            return False
        if not isinstance(item.get("score"), (int, float)):
            return False
    return True


def validate_feedback_summary(summary):
    errors = []
    if not isinstance(summary, dict):
        return ["反馈 summary 必须是对象"]

    if not isinstance(summary.get("date"), str) or not summary["date"].strip():
        errors.append("date 缺失或不是有效字符串")

    session = summary.get("session")
    if not isinstance(session, dict):
        errors.append("session 缺失或不是对象")
    else:
        session_id = session.get("session_id")
        if session_id is not None and not isinstance(session_id, str):
            errors.append("session.session_id 必须是字符串")
        if not isinstance(session.get("total_time_seconds"), int):
            errors.append("session.total_time_seconds 必须是整数")
        if not isinstance(session.get("total_events"), int):
            errors.append("session.total_events 必须是整数")
        if not isinstance(session.get("page_load"), str):
            errors.append("session.page_load 必须是字符串")

    explicit_feedback = summary.get("explicit_feedback")
    if not isinstance(explicit_feedback, dict):
        errors.append("explicit_feedback 缺失或不是对象")
    else:
        if not _is_article_feedback_list(explicit_feedback.get("voted", [])):
            errors.append("explicit_feedback.voted 结构不合法")
        if not _is_article_feedback_list(explicit_feedback.get("bookmarked", [])):
            errors.append("explicit_feedback.bookmarked 结构不合法")
        if not _is_string_list(explicit_feedback.get("tags_followed", [])):
            errors.append("explicit_feedback.tags_followed 必须是字符串数组")
        if not _is_string_list(explicit_feedback.get("tags_unfollowed", [])):
            errors.append("explicit_feedback.tags_unfollowed 必须是字符串数组")

    implicit_feedback = summary.get("implicit_feedback")
    if not isinstance(implicit_feedback, dict):
        errors.append("implicit_feedback 缺失或不是对象")
    else:
        if not _is_dwell_list(implicit_feedback.get("dwell_ranking", [])):
            errors.append("implicit_feedback.dwell_ranking 结构不合法")
        if not _is_article_feedback_list(implicit_feedback.get("articles_clicked", [])):
            errors.append("implicit_feedback.articles_clicked 结构不合法")
        if not _is_article_feedback_list(implicit_feedback.get("articles_copied", [])):
            errors.append("implicit_feedback.articles_copied 结构不合法")

    ai_interaction = summary.get("ai_interaction")
    if not isinstance(ai_interaction, dict):
        errors.append("ai_interaction 缺失或不是对象")
    else:
        tools_used = ai_interaction.get("tools_used", {})
        if not isinstance(tools_used, dict) or not all(
            isinstance(key, str) and isinstance(value, int) for key, value in tools_used.items()
        ):
            errors.append("ai_interaction.tools_used 结构不合法")
        if not _is_ai_detail_list(ai_interaction.get("detail", [])):
            errors.append("ai_interaction.detail 结构不合法")

    interest_profile = summary.get("interest_profile")
    if not isinstance(interest_profile, dict):
        errors.append("interest_profile 缺失或不是对象")
    else:
        if not _is_tag_score_list(interest_profile.get("tag_scores", [])):
            errors.append("interest_profile.tag_scores 结构不合法")
        if not _is_string_list(interest_profile.get("top_interests", [])):
            errors.append("interest_profile.top_interests 必须是字符串数组")

    all_events = summary.get("all_events")
    if all_events is not None and not isinstance(all_events, list):
        errors.append("all_events 必须是数组")

    return errors


def feedback_fingerprint(summary):
    payload = json.dumps(summary, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def is_duplicate_session(existing_sessions, summary):
    incoming_session_id = summary.get("session", {}).get("session_id")
    if incoming_session_id:
        for existing in existing_sessions:
            if existing.get("session", {}).get("session_id") == incoming_session_id:
                return True

    incoming_fp = feedback_fingerprint(summary)
    for existing in existing_sessions:
        if feedback_fingerprint(existing) == incoming_fp:
            return True
    return False


def get_local_ip_addresses():
    """返回可用于局域网访问的本机 IPv4 地址。"""
    ips = set()
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, family=socket.AF_INET):
            ip = info[4][0]
            if not ip.startswith("127."):
                ips.add(ip)
    except socket.gaierror:
        pass

    # 通过 UDP 套接字获取默认出口地址，通常更接近实际可访问网卡
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            if ip and not ip.startswith("127."):
                ips.add(ip)
    except OSError:
        pass

    return sorted(ips)


class FeedbackHandler(http.server.SimpleHTTPRequestHandler):
    """处理静态文件 + 反馈 API"""

    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def do_POST(self):
        if self.path == "/api/feedback":
            self._handle_feedback()
        elif self.path == "/api/bookmark":
            self._handle_bookmark()
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    MAX_BODY_SIZE = 2 * 1024 * 1024  # 2 MB

    def _handle_feedback(self):
        length = int(self.headers.get("Content-Length", 0))
        if length > self.MAX_BODY_SIZE:
            self.send_response(413)
            self.send_header("Content-Type", "application/json")
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"ok":false,"error":"payload_too_large"}')
            return
        try:
            body = json.loads(self.rfile.read(length)) if length else {}
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"ok":false,"error":"invalid_json"}')
            return
        normalized, payload_type = normalize_feedback_payload(body)

        if payload_type == "event_batch":
            self.send_response(202)
            self.send_header("Content-Type", "application/json")
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"ok":true,"accepted":false,"reason":"event_batch_ignored"}')
            return

        if payload_type != "summary":
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"ok":false,"error":"invalid_feedback_payload"}')
            return

        errors = validate_feedback_summary(normalized)
        if errors:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self._cors_headers()
            self.end_headers()
            self.wfile.write(
                json.dumps(
                    {"ok": False, "error": "invalid_feedback_summary", "details": errors},
                    ensure_ascii=False,
                ).encode("utf-8")
            )
            return

        date = normalized.get("date", time.strftime("%Y-%m-%d"))
        filepath = FEEDBACK_DIR / f"{date}.json"

        FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)

        # 追加合并（文件锁保护并发写入）
        lock_path = filepath.with_suffix(".lock")
        with open(lock_path, "w") as lock_fh:
            fcntl.flock(lock_fh, fcntl.LOCK_EX)
            try:
                existing = {"sessions": []}
                if filepath.exists():
                    try:
                        existing = json.loads(filepath.read_text(encoding="utf-8"))
                    except (json.JSONDecodeError, IOError):
                        pass
                if not isinstance(existing, dict) or not isinstance(existing.get("sessions"), list):
                    existing = {"sessions": []}

                if is_duplicate_session(existing["sessions"], normalized):
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self._cors_headers()
                    self.end_headers()
                    self.wfile.write(b'{"ok":true,"deduped":true}')
                    return

                existing["sessions"].append(normalized)
                filepath.write_text(
                    json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8"
                )
            finally:
                fcntl.flock(lock_fh, fcntl.LOCK_UN)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self._cors_headers()
        self.end_headers()
        self.wfile.write(b'{"ok":true}')

    def _handle_bookmark(self):
        length = int(self.headers.get("Content-Length", 0))
        if length > 64 * 1024:
            self.send_response(413)
            self.send_header("Content-Type", "application/json")
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"ok":false,"error":"payload_too_large"}')
            return
        try:
            body = json.loads(self.rfile.read(length)) if length else {}
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"ok":false,"error":"invalid_json"}')
            return

        article_id = str(body.get("id", "")).strip()
        title = str(body.get("title", "")).strip()
        if not article_id or not title:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"ok":false,"error":"missing_id_or_title"}')
            return

        graphify_cfg = load_graphify_config()
        if not graphify_cfg.get("enabled", False):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"ok":true,"graphify":"disabled"}')
            return

        data_dir = Path(graphify_cfg.get("data_dir", "~/graphify-data")).expanduser()
        raw_dir = data_dir / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)

        safe_id = re.sub(r"[^\w-]", "-", article_id)[:30]
        id_hash = hashlib.md5(article_id.encode()).hexdigest()[:8]
        date = str(body.get("date", time.strftime("%Y-%m-%d"))).strip() or time.strftime("%Y-%m-%d")
        filename = f"{date}-{safe_id}-{id_hash}.md"
        filepath = raw_dir / filename

        tags = body.get("tags", [])
        if not isinstance(tags, list):
            tags = []
        summary = str(body.get("summary", "")).strip()
        source_url = str(body.get("source_url", "")).strip()
        priority = str(body.get("priority", "normal")).strip()

        lines = ["---"]
        lines.append(f'title: "{title}"')
        lines.append(f'source_url: "{source_url}"')
        lines.append(f'date: "{date}"')
        lines.append(f'priority: "{priority}"')
        lines.append(f'bookmarked_at: "{time.strftime("%Y-%m-%dT%H:%M:%S")}"')
        lines.append('from: "daily-producer-skill"')
        if tags:
            lines.append("tags:")
            for tag in tags:
                lines.append(f"  - {tag}")
        lines.append("---")
        lines.append("")
        lines.append(f"# {title}")
        lines.append("")
        if summary:
            lines.append(summary)
            lines.append("")
        if source_url:
            lines.append(f"来源：{source_url}")

        filepath.write_text("\n".join(lines), encoding="utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self._cors_headers()
        self.end_headers()
        self.wfile.write(
            json.dumps({"ok": True, "file": filename}, ensure_ascii=False).encode("utf-8")
        )

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format, *args):
        pass  # 静默


def find_port(base, host):
    """尝试绑定 base 端口。被占用时直接报错，不静默漂移。"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((host, base))
            return base, None
        except OSError as exc:
            return None, exc


def start_graphify_watch_if_enabled():
    """如果 graphify.enabled=true，检查并启动 graphify watch 进程。"""
    graphify_cfg = load_graphify_config()
    if not graphify_cfg.get("enabled", False):
        return
    data_dir = Path(graphify_cfg.get("data_dir", "~/graphify-data")).expanduser()
    data_dir.mkdir(parents=True, exist_ok=True)
    # 检查是否已在运行
    try:
        result = subprocess.run(
            ["pgrep", "-f", f"graphify.*--watch"],
            capture_output=True, text=True, timeout=2
        )
        if result.returncode == 0:
            print(f"   Graphify watch 已运行 (PID {result.stdout.strip().split()[0]})")
            return
    except Exception:
        pass
    # 启动 watch
    try:
        proc = subprocess.Popen(
            ["graphify", str(data_dir), "--watch"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        print(f"   Graphify watch 已启动 (PID {proc.pid}，数据目录: {data_dir})")
    except FileNotFoundError:
        print("   ⚠️  graphify 命令未找到，请先安装: pip install graphifyy", file=sys.stderr)
    except Exception as e:
        print(f"   ⚠️  启动 graphify watch 失败: {e}", file=sys.stderr)


def load_graphify_config():
    """从 profile.yaml 读取 graphify 配置"""
    config_path = ROOT_DIR / "config" / "profile.yaml"
    if not config_path.exists():
        return {}
    try:
        import yaml
        with open(config_path, encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        return cfg.get("graphify", {})
    except Exception:
        return {}


def load_server_config():
    """从 profile.yaml 读取 server 配置"""
    config_path = ROOT_DIR / "config" / "profile.yaml"
    if config_path.exists():
        try:
            import yaml

            with open(config_path, encoding="utf-8") as f:
                cfg = yaml.safe_load(f)
            return cfg.get("server", {})
        except ImportError:
            # 没有 pyyaml，用简单解析
            text = config_path.read_text(encoding="utf-8")
            cfg = {}
            for line in text.splitlines():
                line = line.strip()
                # 跳过纯注释行
                if not line or line.startswith("#"):
                    continue
                # 去掉行内注释（空格+#）
                if " #" in line:
                    line = line[: line.index(" #")].rstrip()
                if line.startswith("host:"):
                    cfg["host"] = line.split(":", 1)[1].strip().strip("'\"")
                elif line.startswith("port:"):
                    try:
                        cfg["port"] = int(line.split(":")[1].strip())
                    except ValueError:
                        pass
                elif line.startswith("timeout_hours:"):
                    try:
                        cfg["timeout_hours"] = float(line.split(":")[1].strip())
                    except ValueError:
                        pass
                elif line.startswith("public_url:"):
                    cfg["public_url"] = line.split(":", 1)[1].strip().strip("'\"")
            return cfg
    return {}


def stop_existing_server():
    """检查并关闭已在运行的服务进程。"""
    if not PID_FILE.exists():
        return
    try:
        old_pid = int(PID_FILE.read_text(encoding="utf-8").strip())
    except (ValueError, IOError):
        PID_FILE.unlink(missing_ok=True)
        return
    # 检查进程是否存活
    try:
        os.kill(old_pid, 0)
    except OSError:
        # 进程已不存在，清理残留文件
        PID_FILE.unlink(missing_ok=True)
        PORT_FILE.unlink(missing_ok=True)
        return
    # 进程存活，发送 SIGTERM 关闭
    print(f"发现已有服务进程 (PID {old_pid})，正在关闭...")
    try:
        os.kill(old_pid, 15)  # SIGTERM
        # 等待最多 3 秒
        for _ in range(30):
            time.sleep(0.1)
            try:
                os.kill(old_pid, 0)
            except OSError:
                break
        else:
            # 3 秒后仍存活，强制 kill
            os.kill(old_pid, 9)  # SIGKILL
    except OSError:
        pass
    PID_FILE.unlink(missing_ok=True)
    PORT_FILE.unlink(missing_ok=True)
    print("已关闭旧服务。")


def main():
    # 忽略 SIGHUP，防止终端关闭时杀死后台进程
    signal.signal(signal.SIGHUP, signal.SIG_IGN)

    stop_existing_server()
    start_graphify_watch_if_enabled()

    cfg = load_server_config()
    bind_host = cfg.get("host", DEFAULT_HOST)
    port_base = cfg.get("port", DEFAULT_PORT)
    timeout_hours = cfg.get("timeout_hours", 24)
    public_url = cfg.get("public_url", "").rstrip("/")

    port, port_error = find_port(port_base, bind_host)
    if not port:
        if isinstance(port_error, PermissionError):
            print(
                "ERROR: 当前环境不允许监听本地端口，反馈服务未启动。",
                file=sys.stderr,
            )
        else:
            print(
                f"ERROR: 端口 {port_base} 已被占用，反馈服务未启动。",
                file=sys.stderr,
            )
            print(
                f"       请先执行: kill $(lsof -ti:{port_base})",
                file=sys.stderr,
            )
            if port_error is not None:
                print(f"       错误详情: {port_error}", file=sys.stderr)
        sys.exit(1)

    # 启动服务（ThreadingHTTPServer 支持并发连接，避免单线程队列溢出）
    handler = partial(FeedbackHandler, directory=str(OUTPUT_DIR))
    server = http.server.ThreadingHTTPServer((bind_host, port), handler)

    PORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    PORT_FILE.write_text(str(port))
    PID_FILE.write_text(str(os.getpid()))

    # 自动超时退出
    def _auto_shutdown():
        print(f"\n⏰ 服务已运行 {timeout_hours} 小时，自动退出", flush=True)
        PORT_FILE.unlink(missing_ok=True)
        PID_FILE.unlink(missing_ok=True)
        server.shutdown()

    timer = threading.Timer(timeout_hours * 3600, _auto_shutdown)
    timer.daemon = True
    timer.start()

    today = time.strftime("%Y-%m-%d")
    print("✅ 日报服务已启动")
    print(f"   PID: {os.getpid()}")
    print(f"   监听地址: {bind_host}:{port}")
    if public_url:
        print(f"   🌐 公网地址: {public_url}")
        print(f"   访问日报: {public_url}/daily/{{DATE}}.html  （DATE 为当次运行日期）")
        print(f"   今日示例: {public_url}/daily/{today}.html")
    else:
        print(f"   本机访问: http://localhost:{port}/daily/{{DATE}}.html  （DATE 为当次运行日期）")
        print(f"   今日示例: http://localhost:{port}/daily/{today}.html")
        if bind_host in {"0.0.0.0", ""}:
            lan_ips = get_local_ip_addresses()
            if lan_ips:
                print("   局域网访问:")
                for ip in lan_ips:
                    print(f"   - http://{ip}:{port}/daily/{today}.html")
    print(f"   静态目录: {OUTPUT_DIR}")
    print(f"   反馈写入: {FEEDBACK_DIR}")
    print(f"   自动退出: {timeout_hours} 小时后")
    print(f"   按 Ctrl+C 手动停止")
    sys.stdout.flush()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 手动停止服务")
    finally:
        timer.cancel()
        PORT_FILE.unlink(missing_ok=True)
        PID_FILE.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
