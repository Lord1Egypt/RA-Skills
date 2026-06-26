#!/usr/bin/env python3
"""
深智智预习课件生成 CLI

Usage:
    deepaistudy-prep <command> [options]

Commands:
    config      查看/设置配置
    list        预习列表
    upload      上传图片生成预习
    analyze     AI分析PDF并自动生成预习
    batch       批量从PDF生成（整本书）
    status      查看状态
    result      获取生成结果
"""

import argparse
import configparser
import json
import os
import sys
import time
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

# 尝试导入 requests
try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# ---------------------------------------------------------------------------
# 配置管理
# ---------------------------------------------------------------------------

CONFIG_DIR = Path.home() / ".config" / "deepaistudy-prep"
CONFIG_FILE = CONFIG_DIR / "config.ini"


def get_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        config.read(CONFIG_FILE)
    if not config.has_section("default"):
        config.add_section("default")
    return config


def save_config(config: configparser.ConfigParser) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        config.write(f)


def get_config_value(key: str, default: str = "") -> str:
    config = get_config()
    return config.get("default", key, fallback=default)


def set_config_value(key: str, value: str) -> None:
    config = get_config()
    config.set("default", key, value)
    save_config(config)


# ---------------------------------------------------------------------------
# API 客户端
# ---------------------------------------------------------------------------


class DeepAIStudyClient:
    """深智智 API 客户端"""

    def __init__(self, server: str, username: str = "", password: str = ""):
        self.server = server.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "deepaistudy-prep-cli/1.0"})
        self.jwt_token: Optional[str] = None
        self.csrf_token: Optional[str] = None
        self.username = username
        self.password = password

    def _url(self, path: str) -> str:
        return f"{self.server}{path}"

    # ── 认证 ────────────────────────────────────────────────────────────────

    def login(self) -> bool:
        """通过移动端 API 登录获取 JWT"""
        if not self.username or not self.password:
            # 尝试从环境变量或配置获取
            self.username = get_config_value("username")
            self.password = get_config_value("password")

        if not self.username or not self.password:
            print("错误: 请先设置用户名和密码")
            print("  deepaistudy-prep config set username <email>")
            print("  deepaistudy-prep config set password <password>")
            return False

        resp = self.session.post(
            self._url("/api/mobile/login"),
            json={"username": self.username, "password": self.password},
            timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success"):
                self.jwt_token = data["data"]["token"]
                self.session.headers.update({"Authorization": f"Bearer {self.jwt_token}"})
                print(f"✓ 登录成功: {data['data']['user'].get('username', self.username)}")
                return True

        print(f"错误: 登录失败 ({resp.status_code})")
        if resp.status_code == 401:
            print("  用户名或密码错误")
        return False

    def ensure_auth(self) -> bool:
        """确保已认证"""
        if self.jwt_token:
            return True
        return self.login()

    # ── 核心 API ─────────────────────────────────────────────────────────────

    def get_csrf_token(self) -> Optional[str]:
        """从页面获取 CSRF token"""
        try:
            resp = self.session.get(self._url("/"), timeout=10)
            # 查找 csrf_token 或 csrfToken
            import re

            match = re.search(r'(?:csrf_token|csrfToken|csrf)[^"]*"([^"]+)"', resp.text)
            if match:
                return match.group(1)
        except Exception:
            pass
        return None

    def list_preps(
        self,
        page: int = 1,
        per_page: int = 20,
        subject: str = "",
        status: str = "",
    ) -> Dict[str, Any]:
        """获取预习列表"""
        if not self.ensure_auth():
            return {"success": False, "error": "认证失败"}

        params = {"page": page, "per_page": per_page}
        if subject:
            params["subject"] = subject
        if status:
            params["status"] = status

        resp = self.session.get(self._url("/api/preps"), params=params, timeout=15)
        if resp.status_code == 200:
            return resp.json()
        return {"success": False, "error": f"请求失败 ({resp.status_code})"}

    def get_prep(self, prep_id: int) -> Dict[str, Any]:
        """获取预习详情"""
        if not self.ensure_auth():
            return {"success": False, "error": "认证失败"}

        resp = self.session.get(self._url(f"/api/prep/{prep_id}"), timeout=15)
        if resp.status_code == 200:
            return resp.json()
        if resp.status_code == 404:
            return {"success": False, "error": "预习不存在或无权访问"}
        return {"success": False, "error": f"请求失败 ({resp.status_code})"}

    def create_prep(
        self,
        image_paths: List[str],
        subject: str = "",
        grade_level: str = "",
        topic: str = "",
        difficulty: str = "medium",
        subject_mode: str = "auto",
    ) -> Dict[str, Any]:
        """创建预习任务（上传图片）"""
        if not self.ensure_auth():
            return {"success": False, "error": "认证失败"}

        # 如果服务器是本地，尝试获取 CSRF token
        if "127.0.0.1" in self.server or "localhost" in self.server:
            self.csrf_token = self.get_csrf_token()

        files = []
        for i, path in enumerate(image_paths):
            path = Path(path).expanduser()
            if not path.exists():
                return {"success": False, "error": f"文件不存在: {path}"}
            files.append(("images", (path.name, open(path, "rb"), "image/jpeg")))

        data = {
            "subject": subject,
            "grade_level": grade_level,
            "topic": topic,
            "difficulty": difficulty,
            "subject_mode": subject_mode,
        }
        if self.csrf_token:
            data["csrf_token"] = self.csrf_token

        resp = self.session.post(
            self._url("/api/prep"),
            files=files,
            data=data,
            timeout=60,
        )

        # 关闭所有打开的文件句柄
        for _, (_, fh, _) in files:
            fh.close()

        if resp.status_code == 202:
            return resp.json()
        if resp.status_code == 400:
            try:
                return resp.json()
            except Exception:
                return {"success": False, "error": resp.text}
        return {"success": False, "error": f"请求失败 ({resp.status_code}): {resp.text}"}

    def create_prep_from_urls(
        self,
        image_urls: List[str],
        subject: str = "",
        grade_level: str = "",
        topic: str = "",
        difficulty: str = "medium",
    ) -> Dict[str, Any]:
        """通过图片 URL 创建预习任务"""
        if not self.ensure_auth():
            return {"success": False, "error": "认证失败"}

        self.csrf_token = self.get_csrf_token()

        payload = {
            "image_urls": image_urls,
            "subject": subject,
            "grade_level": grade_level,
            "topic": topic,
            "difficulty": difficulty,
            "subject_mode": "auto" if not subject else "manual",
        }
        if self.csrf_token:
            payload["csrf_token"] = self.csrf_token

        resp = self.session.post(
            self._url("/api/prep"),
            json=payload,
            timeout=30,
        )
        if resp.status_code in (200, 202):
            return resp.json()
        return {"success": False, "error": f"请求失败 ({resp.status_code})"}

    def retry_prep(self, prep_id: int) -> Dict[str, Any]:
        """重试失败的预习"""
        if not self.ensure_auth():
            return {"success": False, "error": "认证失败"}

        resp = self.session.post(
            self._url(f"/api/prep/{prep_id}/retry"),
            timeout=15,
        )
        if resp.status_code == 200:
            return resp.json()
        return {"success": False, "error": f"请求失败 ({resp.status_code})"}

    def get_batch_prep(self, batch_id: str) -> Dict[str, Any]:
        """获取批量预习详情"""
        if not self.ensure_auth():
            return {"success": False, "error": "认证失败"}

        resp = self.session.get(
            self._url(f"/api/prep/batch/{batch_id}"),
            timeout=15,
        )
        if resp.status_code == 200:
            return resp.json()
        return {"success": False, "error": f"请求失败 ({resp.status_code})"}

    def poll_prep(
        self,
        prep_id: int,
        interval: int = 5,
        timeout: int = 300,
        silent: bool = False,
    ) -> Dict[str, Any]:
        """轮询预习状态直到完成"""
        start = time.time()
        while True:
            result = self.get_prep(prep_id)
            if not result.get("success"):
                return result

            data = result.get("data", {})
            status = data.get("status", "")

            if not silent:
                print(f"  状态: {status}", end="")
                if status == "failed":
                    print(f" - {data.get('error_message', '未知错误')}")
                else:
                    print()

            if status == "completed":
                return result
            if status == "failed":
                return {
                    "success": False,
                    "error": data.get("error_message", "生成失败"),
                    "data": data,
                }

            elapsed = time.time() - start
            if elapsed > timeout:
                return {"success": False, "error": f"超时（{timeout}秒）"}

            time.sleep(interval)


# ---------------------------------------------------------------------------
# PDF 处理
# ---------------------------------------------------------------------------


def extract_pdf_images(
    pdf_path: str,
    output_dir: Optional[str] = None,
    max_pages: int = 20,
) -> List[str]:
    """从 PDF 提取图片页面"""
    try:
        from pdf2image import convert_from_path

        pages = convert_from_path(pdf_path, dpi=150, first_page=1, last_page=max_pages)
    except ImportError:
        try:
            import subprocess

            # 尝试用 pdftoppm
            if output_dir is None:
                output_dir = tempfile.mkdtemp()
            result = subprocess.run(
                ["pdftoppm", "-r", "150", "-png", pdf_path, "page"],
                capture_output=True,
                cwd=output_dir,
            )
            if result.returncode != 0:
                raise ImportError("pdf2image 和 pdftoppm 都不可用")
            import glob

            pages = sorted(glob.glob(os.path.join(output_dir, "page*.png")))
            return pages
        except Exception as e:
            raise ImportError(f"无法提取 PDF 图片: {e}")

    if output_dir is None:
        output_dir = tempfile.mkdtemp()

    image_paths = []
    for i, page in enumerate(pages):
        img_path = os.path.join(output_dir, f"page_{i+1:03d}.jpg")
        page.save(img_path, "JPEG", quality=85)
        image_paths.append(img_path)

    return image_paths


def detect_pdf_info(pdf_path: str) -> Dict[str, Any]:
    """检测 PDF 基本信息（页数、目录等）"""
    try:
        import PyPDF2

        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            total_pages = len(reader.pages)
        return {"success": True, "total_pages": total_pages}
    except ImportError:
        try:
            import subprocess

            result = subprocess.run(
                ["pdfinfo", pdf_path],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if line.startswith("Pages:"):
                        total_pages = int(line.split(":")[1].strip())
                        return {"success": True, "total_pages": total_pages}
        except Exception:
            pass
        return {"success": True, "total_pages": 0}


# ---------------------------------------------------------------------------
# 交互式 AI 分析（调用外部 AI 服务）
# ---------------------------------------------------------------------------


def analyze_pdf_ai(
    pdf_path: str,
    client: DeepAIStudyClient,
) -> Dict[str, Any]:
    """调用 AI 自动分析 PDF（识别目录、学科、年级）"""
    # 先尝试本地 AI 分析脚本
    ai_script = Path.home() / "clawd" / "scripts" / "pdf-analyze.sh"
    if ai_script.exists():
        import subprocess

        result = subprocess.run(
            [str(ai_script), pdf_path],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0:
            try:
                return json.loads(result.stdout)
            except Exception:
                pass

    # 使用 MiniMax MCP（如果可用）
    # 这里作为后备，返回空让用户手动指定
    return {
        "success": False,
        "error": "需要手动指定 --subject 和 --grade 参数，或安装 pdf-analyze.sh 脚本",
    }


# ---------------------------------------------------------------------------
# 命令实现
# ---------------------------------------------------------------------------


def cmd_config_list():
    config = get_config()
    print("当前配置:")
    print(f"  server:   {get_config_value('server', 'http://127.0.0.1:5000')}")
    print(f"  username: {get_config_value('username', '(未设置)')}")
    print(f"  password: {'***' if get_config_value('password') else '(未设置)'}")
    print()
    print("设置方法:")
    print("  deepaistudy-prep config set server   https://www.deepaistudy.com")
    print("  deepaistudy-prep config set username your@email.com")
    print("  deepaistudy-prep config set password xxxxx")


def cmd_config_set(key: str, value: str):
    valid_keys = {"server", "username", "password"}
    if key not in valid_keys:
        print(f"错误: 无效的配置项 '{key}'")
        print(f"可选: {', '.join(valid_keys)}")
        return

    if key == "server":
        if not value.startswith("http"):
            print("错误: server 必须以 http:// 或 https:// 开头")
            return
        if not value.endswith("/"):
            value += "/"

    set_config_value(key, value)
    print(f"✓ 已设置 {key} = {value if key != 'password' else '***'}")


def cmd_list(args):
    server = get_config_value("server", "http://127.0.0.1:5000")
    username = get_config_value("username")
    password = get_config_value("password")

    client = DeepAIStudyClient(server, username, password)
    result = client.list_preps(
        page=args.page,
        per_page=args.per_page,
        subject=args.subject,
        status=args.status,
    )

    if not result.get("success"):
        print(f"错误: {result.get('error')}")
        return

    items = result.get("data", {}).get("items", [])
    total = result.get("data", {}).get("total", 0)
    page = result.get("data", {}).get("current_page", 1)

    print(f"\n预习列表 (共 {total} 条, 第 {page} 页)")
    print("-" * 70)
    for item in items:
        status_icon = {"completed": "✓", "processing": "⟳", "queued": "⏳", "failed": "✗"}.get(
            item.get("status", ""), "?"
        )
        title = item.get("title") or item.get("chapter") or "(无标题)"
        subject = item.get("subject", "")
        print(f"  [{item['id']}] {status_icon} {title}")
        print(f"         学科: {subject} | 状态: {item.get('status')} | 创建: {item.get('created_at', '')[:10]}")


def cmd_status(args):
    server = get_config_value("server", "http://127.0.0.1:5000")
    username = get_config_value("username")
    password = get_config_value("password")

    client = DeepAIStudyClient(server, username, password)
    result = client.get_prep(args.prep_id)

    if not result.get("success"):
        print(f"错误: {result.get('error')}")
        return

    data = result.get("data", {})
    print(f"\n预习详情 (ID: {args.prep_id})")
    print("=" * 60)
    print(f"  标题:   {data.get('title') or data.get('chapter')}")
    print(f"  学科:   {data.get('subject')}")
    print(f"  年级:   {data.get('grade_level')}")
    print(f"  状态:   {data.get('status')}")

    meta = data.get("meta") or {}
    if meta.get("animation_slide_count"):
        print(f"  幻灯片: {meta['animation_slide_count']} 页")

    if data.get("status") == "failed":
        print(f"  错误:   {data.get('error_message')}")


def cmd_result(args):
    server = get_config_value("server", "http://127.0.0.1:5000")
    username = get_config_value("username")
    password = get_config_value("password")

    client = DeepAIStudyClient(server, username, password)
    result = client.get_prep(args.prep_id)

    if not result.get("success"):
        print(f"错误: {result.get('error')}")
        return

    data = result.get("data", {})
    meta = data.get("meta") or {}

    print(f"\n预习结果 (ID: {args.prep_id})")
    print("=" * 60)

    # 基本信息
    print(f"标题: {data.get('title') or data.get('chapter')}")
    print(f"学科: {data.get('subject')} | 年级: {data.get('grade_level')}")
    print(f"状态: {data.get('status')}")

    # OCR 原文
    if data.get("ocr_text"):
        lines = data["ocr_text"].splitlines()
        preview = "\n".join(lines[:10])
        if len(lines) > 10:
            preview += f"\n  ... (+{len(lines)-10} 行)"
        print(f"\n--- 课文原文 (OCR) ---")
        print(preview)

    # SVG 幻灯片
    if meta.get("animation_svg"):
        svg_len = len(meta["animation_svg"])
        print(f"\n--- 互动幻灯片 ---")
        print(f"  SVG 大小: {svg_len:,} 字符")
        print(f"  幻灯片数: {meta.get('animation_slide_count', '?')} 页")
        print(f"  生成方式: {meta.get('processing_method', 'unknown')}")

        if args.output:
            output_path = Path(args.output)
            svg_path = output_path.with_suffix(".svg")
            svg_path.write_text(meta["animation_svg"])
            print(f"  已保存: {svg_path}")

    # 小测
    quiz = meta.get("interactive_preview", {}).get("quiz", {})
    if quiz.get("questions"):
        questions = quiz["questions"]
        print(f"\n--- 预习小测 ({len(questions)} 题) ---")
        for i, q in enumerate(questions[:5], 1):
            print(f"  {i}. [{q.get('type', 'unknown')}] {q.get('stem', q.get('question', ''))[:60]}")
        if len(questions) > 5:
            print(f"  ... (+{len(questions)-5} 题)")

        progress = meta.get("interactive_preview", {}).get("progress", {})
        print(f"\n  小测进度: {progress.get('status', '未开始')}")
        if progress.get("last_score") is not None:
            print(f"  上次得分: {progress['last_score']}分")


def cmd_upload(args):
    if not args.images:
        print("错误: 请指定要上传的图片文件")
        return

    server = get_config_value("server", "http://127.0.0.1:5000")
    username = get_config_value("username")
    password = get_config_value("password")

    # 检查文件
    image_paths = []
    for p in args.images:
        path = Path(p).expanduser()
        if not path.exists():
            print(f"错误: 文件不存在: {path}")
            return
        image_paths.append(str(path))

    print(f"准备上传 {len(image_paths)} 张图片...")
    print(f"服务器: {server}")

    client = DeepAIStudyClient(server, username, password)

    # 创建预习
    result = client.create_prep(
        image_paths=image_paths,
        subject=args.subject or "",
        grade_level=args.grade or "",
        topic=args.topic or "",
        difficulty=args.difficulty or "medium",
    )

    if not result.get("success"):
        print(f"错误: {result.get('error')}")
        return

    prep_id = result.get("prep_id")
    task_id = result.get("task_id")
    print(f"✓ 预习任务已创建 (ID: {prep_id})")
    if task_id:
        print(f"  任务ID: {task_id}")

    if args.no_wait:
        print("（使用 --no-wait 跳过等待）")
        return

    # 轮询等待完成
    print("\n正在生成预习内容，请稍候...")
    done = client.poll_prep(prep_id, interval=5, timeout=args.timeout)

    if done.get("success"):
        data = done.get("data", {})
        meta = data.get("meta") or {}
        slide_count = meta.get("animation_slide_count", 0)
        print(f"\n✓ 生成完成！")
        print(f"  幻灯片: {slide_count} 页")
        print(f"  查看结果: deepaistudy-prep result {prep_id}")
        if args.open and server == "http://127.0.0.1:5000":
            import subprocess

            subprocess.run(["open", f"http://127.0.0.1:5000/preps/detail/{prep_id}"])
    else:
        print(f"\n✗ 生成失败: {done.get('error')}")


def cmd_analyze(args):
    """AI 自动分析 PDF 并生成预习"""
    pdf_path = Path(args.pdf).expanduser()
    if not pdf_path.exists():
        print(f"错误: PDF 文件不存在: {pdf_path}")
        return

    server = get_config_value("server", "http://127.0.0.1:5000")
    username = get_config_value("username")
    password = get_config_value("password")

    print(f"分析 PDF: {pdf_path}")
    print(f"服务器: {server}")

    # 检测 PDF 信息
    info = detect_pdf_info(str(pdf_path))
    total_pages = info.get("total_pages", 0)
    print(f"PDF 总页数: {total_pages}")

    # 提取图片
    print("提取图片页面...")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            image_paths = extract_pdf_images(str(pdf_path), output_dir=tmpdir, max_pages=args.max_pages or 20)
            print(f"提取了 {len(image_paths)} 张图片")

            client = DeepAIStudyClient(server, username, password)

            print("创建预习任务...")
            result = client.create_prep(
                image_paths=image_paths,
                subject=args.subject or "",
                grade_level=args.grade or "",
                topic=args.topic or "",
                difficulty=args.difficulty or "medium",
            )

            if not result.get("success"):
                print(f"错误: {result.get('error')}")
                return

            prep_id = result.get("prep_id")
            print(f"✓ 预习任务已创建 (ID: {prep_id})")

            if args.no_wait:
                print("（使用 --no-wait 跳过等待）")
                return

            print("\n正在生成预习内容，请稍候...")
            done = client.poll_prep(prep_id, interval=5, timeout=args.timeout or 300)

            if done.get("success"):
                data = done.get("data", {})
                meta = data.get("meta") or {}
                print(f"\n✓ 生成完成！")
                print(f"  幻灯片: {meta.get('animation_slide_count', 0)} 页")
                print(f"  查看结果: deepaistudy-prep result {prep_id}")
            else:
                print(f"\n✗ 生成失败: {done.get('error')}")

    except ImportError as e:
        print(f"错误: {e}")
        print("\n请安装依赖:")
        print("  pip install pdf2image pillow PyPDF2 requests")
        if sys.platform == "darwin":
            print("  brew install poppler  # macOS 需要先安装 poppler")


def cmd_batch(args):
    """批量从 PDF 生成预习（整本书，每课一个）"""
    pdf_path = Path(args.pdf).expanduser()
    if not pdf_path.exists():
        print(f"错误: PDF 文件不存在: {pdf_path}")
        return

    server = get_config_value("server", "http://127.0.0.1:5000")
    username = get_config_value("username")
    password = get_config_value("password")

    client = DeepAIStudyClient(server, username, password)

    print(f"批量生成: {pdf_path}")
    print(f"服务器: {server}")
    print(f"学科: {args.subject or 'AI自动识别'}")
    print(f"年级: {args.grade or 'AI自动识别'}")

    import subprocess

    # 预览拆分
    print("\n预览目录拆分...")
    result = subprocess.run(
        ["curl", "-s", "-X", "POST",
         f"{server}/api/prep/batch/preview",
         "-F", f"pdf_file=@{pdf_path}",
         "-F", f"subject={args.subject or ''}",
         "-F", f"grade_level={args.grade or ''}",
         "-F", f"auto_split={str(args.auto_split).lower()}",
         "-F", f"toc_pdf_pages={args.toc_pages or ''}",
         "-F", f"first_lesson_pdf_page={args.first_lesson_page or ''}",
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )

    try:
        preview_data = json.loads(result.stdout)
        if preview_data.get("success"):
            lessons = preview_data["data"]["lessons"]
            print(f"\n目录识别结果: {len(lessons)} 个课时")
            for les in lessons[:10]:
                print(f"  {les['lesson_number']:2d}. {les['title']} (页 {les['start_page']}-{les['end_page']})")
            if len(lessons) > 10:
                print(f"  ... (+{len(lessons)-10} 课)")

            if not args.confirm:
                response = input("\n确认生成全部课时? (y/n): ")
                if response.lower() != "y":
                    print("已取消")
                    return
        else:
            print(f"预览失败: {preview_data.get('error')}")
            return
    except Exception as e:
        print(f"预览失败: {e}")
        return

    # 实际批量创建
    print("\n创建批量预习任务...")
    result = subprocess.run(
        ["curl", "-s", "-X", "POST",
         f"{server}/api/prep/batch",
         "-F", f"pdf_file=@{pdf_path}",
         "-F", f"subject={args.subject or ''}",
         "-F", f"grade_level={args.grade or ''}",
         "-F", f"auto_split={str(args.auto_split).lower()}",
         "-F", f"toc_pdf_pages={args.toc_pages or ''}",
         "-F", f"first_lesson_pdf_page={args.first_lesson_page or ''}",
         "-F", f"batch_title={args.title or pdf_path.stem}",
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )

    try:
        batch_data = json.loads(result.stdout)
        if batch_data.get("success"):
            batch_id = batch_data["batch_id"]
            total = batch_data["total_count"]
            print(f"✓ 批量任务已创建 (批次ID: {batch_id})")
            print(f"  共 {total} 个课时")
            print(f"  查看进度: 访问 http://127.0.0.1:5000/study/batch-progress/{batch_id}")
        else:
            print(f"错误: {batch_data.get('error')}")
    except Exception as e:
        print(f"批量创建失败: {e}")
        print(f"原始响应: {result.stdout[:500]}")


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------


def main():
    if not HAS_REQUESTS:
        print("错误: 需要 requests 库")
        print("安装: pip install requests")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="深智智预习课件生成工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # config
    config_parser = subparsers.add_parser("config", help="查看/设置配置")
    config_parser.add_argument("action", nargs="?", choices=["list", "set"], default="list")
    config_parser.add_argument("key", nargs="?")
    config_parser.add_argument("value", nargs="?")
    config_parser.set_defaults(func=lambda a: cmd_config_set(a.key, a.value) if a.action == "set" else cmd_config_list())

    # list
    list_parser = subparsers.add_parser("list", help="预习列表")
    list_parser.add_argument("--page", type=int, default=1)
    list_parser.add_argument("--per-page", type=int, dest="per_page", default=20)
    list_parser.add_argument("--subject", default="")
    list_parser.add_argument("--status", default="")
    list_parser.set_defaults(func=cmd_list)

    # status
    status_parser = subparsers.add_parser("status", help="查看状态")
    status_parser.add_argument("prep_id", type=int)
    status_parser.set_defaults(func=cmd_status)

    # result
    result_parser = subparsers.add_parser("result", help="获取结果")
    result_parser.add_argument("prep_id", type=int)
    result_parser.add_argument("--output", "-o", dest="output", help="保存 SVG 到文件")
    result_parser.set_defaults(func=cmd_result)

    # upload
    upload_parser = subparsers.add_parser("upload", help="上传图片生成预习")
    upload_parser.add_argument("images", nargs="+", help="图片文件路径")
    upload_parser.add_argument("--subject", "-s", default="", help="学科")
    upload_parser.add_argument("--grade", "-g", default="", dest="grade", help="年级")
    upload_parser.add_argument("--topic", "-t", default="", help="章节/课题")
    upload_parser.add_argument("--difficulty", "-d", default="medium", choices=["low", "medium", "high"])
    upload_parser.add_argument("--no-wait", action="store_true", dest="no_wait", help="不等待生成完成")
    upload_parser.add_argument("--timeout", type=int, default=300, help="超时秒数")
    upload_parser.add_argument("--open", action="store_true", help="完成后在浏览器打开")
    upload_parser.set_defaults(func=cmd_upload)

    # analyze
    analyze_parser = subparsers.add_parser("analyze", help="AI分析PDF并生成预习")
    analyze_parser.add_argument("pdf", help="PDF 文件路径")
    analyze_parser.add_argument("--subject", "-s", default="", help="学科")
    analyze_parser.add_argument("--grade", "-g", default="", dest="grade", help="年级")
    analyze_parser.add_argument("--topic", "-t", default="", help="章节/课题")
    analyze_parser.add_argument("--difficulty", "-d", default="medium", choices=["low", "medium", "high"])
    analyze_parser.add_argument("--ai", action="store_true", help="使用 AI 自动识别目录和课文结构")
    analyze_parser.add_argument("--max-pages", type=int, dest="max_pages", help="最多提取页数")
    analyze_parser.add_argument("--no-wait", action="store_true", dest="no_wait", help="不等待生成完成")
    analyze_parser.add_argument("--timeout", type=int, default=300, help="超时秒数")
    analyze_parser.set_defaults(func=cmd_analyze)

    # batch
    batch_parser = subparsers.add_parser("batch", help="批量从PDF生成整本书预习")
    batch_parser.add_argument("pdf", help="PDF 文件路径")
    batch_parser.add_argument("--subject", "-s", default="", help="学科")
    batch_parser.add_argument("--grade", "-g", default="", dest="grade", help="年级")
    batch_parser.add_argument("--title", default="", help="批次标题")
    batch_parser.add_argument("--auto-split", action="store_true", dest="auto_split", default=True, help="AI自动识别目录")
    batch_parser.add_argument("--toc-pages", dest="toc_pages", default="", help="目录页码，如 3-5 或 3,4,5")
    batch_parser.add_argument("--first-lesson-page", dest="first_lesson_page", type=int, help="第一课起始页码")
    batch_parser.add_argument("--no-wait", action="store_true", dest="no_wait", help="不等待生成完成")
    batch_parser.add_argument("--confirm", action="store_true", help="跳过确认直接生成")
    batch_parser.set_defaults(func=cmd_batch)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "config" and args.action == "list":
        cmd_config_list()
        return

    if args.command == "config" and args.action == "set":
        if not args.key or not args.value:
            print("用法: deepaistudy-prep config set <key> <value>")
            return
        cmd_config_set(args.key, args.value)
        return

    # 调用对应的命令函数
    args.func(args)


if __name__ == "__main__":
    main()
