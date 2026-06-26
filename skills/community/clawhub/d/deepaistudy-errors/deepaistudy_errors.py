#!/usr/bin/env python3
"""
深智智错题本 CLI

与 deepaistudy-prep 共用同一套认证和配置。

Usage:
    deepaistudy-errors <command> [options]

Commands:
    config      查看/设置配置（共用 deepaistudy-prep 的配置）
    add         添加错题（上传图片）
    list        查看错题列表
    analyze     提交 AI 分析（异步，返回 task_id）
    status      轮询分析状态
    master      标记为已掌握
    unmaster    取消已掌握标记
    variation   生成变式题
    delete      删除错题
    export      导出 PDF
"""

import argparse
import configparser
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ---------------------------------------------------------------------------
# 配置管理（与 deepaistudy-prep 共用）
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
        self.server = server.rstrip("/")  # 移除末尾斜杠避免双斜杠
        self.username = username
        self.password = password
        self.token = None
        self._login()

    def _login(self) -> None:
        """登录获取 JWT token"""
        if not self.username or not self.password:
            raise ValueError("未配置用户名或密码，请先运行: deepaistudy-errors config set username <邮箱>")
        resp = requests.post(
            f"{self.server}/api/mobile/login",
            json={"username": self.username, "password": self.password},
            timeout=30,
        )
        print(f"DEBUG login: status={resp.status_code} url={resp.url}", file=sys.stderr)
        if resp.status_code != 200:
            raise ValueError(f"登录失败: {resp.status_code} {resp.text}")
        data = resp.json()
        # token 在 data.token（标准）或根级 token（兼容）
        self.token = (data.get("data") or {}).get("token") or data.get("token") or data.get("access_token")
        if not self.token:
            raise ValueError(f"登录响应中未找到 token: {resp.text}")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _refresh_token_if_needed(self, resp: requests.Response) -> bool:
        """如果 token 过期，自动重新登录"""
        if resp.status_code in (401, 403):
            self._login()
            return True
        return False

    # ---------------------------------------------------------------------------
    # 错题本 API
    # ---------------------------------------------------------------------------

    def list_error_books(
        self,
        subject: str = "",
        page: int = 1,
        per_page: int = 20,
        search: str = "",
        sort: str = "latest",
    ) -> Dict[str, Any]:
        """获取错题本列表"""
        params = {"page": page, "per_page": per_page, "sort": sort}
        if subject:
            params["subject"] = subject
        if search:
            params["search"] = search

        resp = requests.get(
            f"{self.server}/api/mobile/error-book",
            headers=self._headers(),
            params=params,
            timeout=30,
        )
        if self._refresh_token_if_needed(resp):
            resp = requests.get(
                f"{self.server}/api/mobile/error-book",
                headers=self._headers(),
                params=params,
                timeout=30,
            )
        if resp.status_code != 200:
            raise ValueError(f"获取错题列表失败: {resp.status_code} {resp.text}")
        return resp.json()

    def get_error_book(self, note_id: int) -> Dict[str, Any]:
        """获取错题详情"""
        resp = requests.get(
            f"{self.server}/api/mobile/error-book/{note_id}",
            headers=self._headers(),
            timeout=30,
        )
        if self._refresh_token_if_needed(resp):
            resp = requests.get(
                f"{self.server}/api/mobile/error-book/{note_id}",
                headers=self._headers(),
                timeout=30,
            )
        if resp.status_code != 200:
            raise ValueError(f"获取错题详情失败: {resp.status_code} {resp.text}")
        return resp.json()

    def add_error_with_ai(
        self,
        images: List[str],
        subject: str = "综合",
        title: str = "",
    ) -> Dict[str, Any]:
        """添加错题并自动 AI 分析（异步，返回 task_id）"""
        files = []
        for i, img_path in enumerate(images):
            if not os.path.exists(img_path):
                raise ValueError(f"图片文件不存在: {img_path}")
            files.append(
                ("images", (os.path.basename(img_path), open(img_path, "rb"), "image/jpeg"))
            )

        data = {"subject": subject}
        if title:
            data["title"] = title

        resp = requests.post(
            f"{self.server}/api/mobile/breakthrough/ingest-analyze",
            headers={
                "Authorization": f"Bearer {self.token}",
            },
            data=data,
            files=files,
            timeout=60,
        )
        # 关闭文件句柄
        for _, (_, fobj, _) in files:
            fobj.close()

        if self._refresh_token_if_needed(resp):
            files = []
            for i, img_path in enumerate(images):
                files.append(
                    ("images", (os.path.basename(img_path), open(img_path, "rb"), "image/jpeg"))
                )
            resp = requests.post(
                f"{self.server}/api/mobile/breakthrough/ingest-analyze",
                headers={"Authorization": f"Bearer {self.token}"},
                data=data,
                files=files,
                timeout=60,
            )
            for _, (_, fobj, _) in files:
                fobj.close()

        if resp.status_code not in (200, 201):
            raise ValueError(f"添加错题失败: {resp.status_code} {resp.text}")
        return resp.json()

    def submit_error_analysis(
        self,
        images: List[str],
        subject: str = "综合",
        title: str = "",
    ) -> str:
        """提交 AI 分析，返回 task_id 或 sync:note_ids"""
        result = self.add_error_with_ai(images, subject, title)
        if result.get("success"):
            task_id = result.get("data", {}).get("task_id")
            if task_id:
                return task_id
            # 同步模式：直接返回了 note_id 或 note_ids
            data = result.get("data", {})
            note_ids = data.get("note_ids", [])
            if note_ids:
                return "sync:" + ",".join(str(n) for n in note_ids)
            note_id = data.get("note_id")
            if note_id:
                return f"sync:{note_id}"
        raise ValueError(f"提交失败: {result}")

    def poll_analysis_status(self, task_id: str, interval: int = 5, timeout: int = 300) -> Dict[str, Any]:
        """轮询 AI 分析状态"""
        start = time.time()
        while time.time() - start < timeout:
            if task_id.startswith("sync:"):
                # 同步模式
                note_ids_str = task_id.split(":", 1)[1]
                note_ids = [int(n) for n in note_ids_str.split(",")]
                if len(note_ids) == 1:
                    result = self.get_error_book(note_ids[0])
                    return {"success": True, "data": result.get("data", {}), "task_id": task_id, "note_ids": note_ids}
                # 多题：逐个获取详情
                notes = []
                for nid in note_ids:
                    r = self.get_error_book(nid)
                    if r.get("success"):
                        notes.append(r.get("data", {}))
                return {"success": True, "data": notes, "task_id": task_id, "note_ids": note_ids, "count": len(note_ids)}

            resp = requests.get(
                f"{self.server}/api/mobile/breakthrough/ingest-analyze/status/{task_id}",
                headers=self._headers(),
                timeout=30,
            )
            if resp.status_code == 401:
                self._login()
                resp = requests.get(
                    f"{self.server}/api/mobile/breakthrough/ingest-analyze/status/{task_id}",
                    headers=self._headers(),
                    timeout=30,
                )
            if resp.status_code != 200:
                print(f"状态查询失败: {resp.status_code}，{interval}秒后重试...")
            else:
                data = resp.json()
                status_data = data.get("data", {})
                status = status_data.get("status", "")
                progress = status_data.get("progress", 0)
                message = status_data.get("message", "")

                print(f"\r[{progress:3d}%] {message}", end="", flush=True)

                if status == "completed":
                    print()  # 换行
                    result_obj = status_data.get("result", {})
                    note_ids = result_obj.get("note_ids", [])
                    count = result_obj.get("count", len(note_ids) if note_ids else 1)
                    return {"success": True, "data": result_obj, "task_id": task_id, "note_ids": note_ids, "count": count}
                elif status == "failed":
                    print()
                    raise ValueError(f"AI 分析失败: {status_data.get('error', '未知错误')}")

            time.sleep(interval)

        raise TimeoutError(f"等待分析超时（{timeout}秒）")

    def mark_mastered(self, note_id: int) -> Dict[str, Any]:
        """标记为已掌握"""
        resp = requests.put(
            f"{self.server}/api/mobile/error-book/{note_id}/master",
            headers=self._headers(),
            timeout=30,
        )
        if self._refresh_token_if_needed(resp):
            resp = requests.put(
                f"{self.server}/api/mobile/error-book/{note_id}/master",
                headers=self._headers(),
                timeout=30,
            )
        if resp.status_code != 200:
            raise ValueError(f"标记已掌握失败: {resp.status_code} {resp.text}")
        return resp.json()

    def mark_unmastered(self, note_id: int) -> Dict[str, Any]:
        """取消已掌握标记"""
        resp = requests.put(
            f"{self.server}/api/mobile/error-book/{note_id}/unmaster",
            headers=self._headers(),
            timeout=30,
        )
        if self._refresh_token_if_needed(resp):
            resp = requests.put(
                f"{self.server}/api/mobile/error-book/{note_id}/unmaster",
                headers=self._headers(),
                timeout=30,
            )
        if resp.status_code != 200:
            raise ValueError(f"取消已掌握标记失败: {resp.status_code} {resp.text}")
        return resp.json()

    def generate_variation(
        self,
        note_id: int,
        difficulty: str = "medium",
        count: int = 3,
    ) -> Dict[str, Any]:
        """生成变式题"""
        resp = requests.post(
            f"{self.server}/api/mobile/error-book/{note_id}/variation",
            headers=self._headers(),
            json={"difficulty": difficulty, "count": count},
            timeout=60,
        )
        if self._refresh_token_if_needed(resp):
            resp = requests.post(
                f"{self.server}/api/mobile/error-book/{note_id}/variation",
                headers=self._headers(),
                json={"difficulty": difficulty, "count": count},
                timeout=60,
            )
        if resp.status_code != 200:
            raise ValueError(f"生成变式题失败: {resp.status_code} {resp.text}")
        return resp.json()

    def delete_error_book(self, note_id: int) -> Dict[str, Any]:
        """删除错题"""
        resp = requests.delete(
            f"{self.server}/api/mobile/error-book/{note_id}",
            headers=self._headers(),
            timeout=30,
        )
        if self._refresh_token_if_needed(resp):
            resp = requests.delete(
                f"{self.server}/api/mobile/error-book/{note_id}",
                headers=self._headers(),
                timeout=30,
            )
        if resp.status_code != 200:
            raise ValueError(f"删除错题失败: {resp.status_code} {resp.text}")
        return resp.json()


# ---------------------------------------------------------------------------
# CLI 命令
# ---------------------------------------------------------------------------

def cmd_config(args: argparse.Namespace) -> None:
    """配置命令"""
    if args.subcommand == "set":
        if not args.key or not args.value:
            print("用法: deepaistudy-errors config set <key> <value>")
            sys.exit(1)
        set_config_value(args.key, args.value)
        print(f"✓ 已设置 {args.key} = {args.value}")
    elif args.subcommand == "list":
        config = get_config()
        print("当前配置:")
        for key in config.options("default"):
            val = config.get("default", key)
            if key == "password":
                val = "****"
            print(f"  {key}: {val}")
    else:
        print("用法: deepaistudy-errors config set <key> <value>")


def cmd_add(args: argparse.Namespace) -> None:
    """添加错题"""
    client = _get_client()

    images = args.images
    if not images:
        print("错误: 请指定图片路径")
        sys.exit(1)

    for img in images:
        if not os.path.exists(img):
            print(f"错误: 图片不存在: {img}")
            sys.exit(1)

    subject = args.subject or "综合"
    title = args.title or ""

    print(f"正在提交 {len(images)} 张图片到 AI 分析...")
    task_id = client.submit_error_analysis(images, subject, title)
    print(f"任务ID: {task_id}")
    print("正在等待 AI 分析完成...")

    result = client.poll_analysis_status(task_id, interval=5, timeout=300)

    note_ids = result.get("note_ids", [])
    count = result.get("count", len(note_ids))

    print(f"\n✓ AI 分析完成，共识别出 {count} 道错题!")

    # 兼容单题和多题两种 data 格式
    data = result.get("data", {})
    if isinstance(data, list):
        # 多题：data 是笔记列表
        for i, note in enumerate(data, 1):
            mastery = note.get("mastery_status", "未掌握")
            status_icon = "✓" if mastery == "已掌握" else "✗"
            print(f"\n  【第{i}题】")
            print(f"  ID: {note.get('id')}")
            print(f"  学科: {note.get('subject', subject)}")
            print(f"  标题: {note.get('title', '未命名')}")
            print(f"  掌握状态: {status_icon} {mastery}")
    else:
        # 单题：data 是单个笔记
        note_id = data.get("id")
        mastery = data.get("mastery_status", "未掌握")
        print(f"\n✓ 错题添加成功!")
        print(f"  ID: {note_id}")
        print(f"  学科: {data.get('subject', subject)}")
        print(f"  标题: {data.get('title', title) or '未命名'}")
        print(f"  掌握状态: {mastery}")


def cmd_list(args: argparse.Namespace) -> None:
    """列出错题"""
    client = _get_client()

    result = client.list_error_books(
        subject=args.subject or "",
        page=args.page or 1,
        per_page=args.per_page or 20,
        search=args.search or "",
        sort=args.sort or "latest",
    )

    if not result.get("success"):
        print(f"获取失败: {result.get('message')}")
        sys.exit(1)

    items = result.get("data", [])
    pagination = result.get("pagination", {})

    print(f"\n错题列表 (共 {pagination.get('total', 0)} 条)")
    print("-" * 60)
    for item in items:
        status = "✓" if item.get("mastery_status") == "已掌握" else "✗"
        print(f"{status} [{item.get('id')}] {item.get('subject', '')} | {item.get('title', '未命名')[:30]}")
    print("-" * 60)
    print(f"第 {pagination.get('page', 1)}/{pagination.get('pages', 1)} 页")


def cmd_status(args: argparse.Namespace) -> None:
    """查看分析状态"""
    client = _get_client()
    result = client.poll_analysis_status(args.task_id, interval=args.interval or 5, timeout=args.timeout or 300)
    note = result.get("data", {})
    print(f"\n✓ 分析完成!")
    print(f"  ID: {note.get('id')}")
    print(f"  学科: {note.get('subject')}")
    print(f"  标题: {note.get('title', '未命名')}")


def cmd_master(args: argparse.Namespace) -> None:
    """标记已掌握"""
    client = _get_client()
    result = client.mark_mastered(args.note_id)
    if result.get("success"):
        print(f"✓ 笔记 {args.note_id} 已标记为已掌握")
    else:
        print(f"标记失败: {result.get('message')}")
        sys.exit(1)


def cmd_unmaster(args: argparse.Namespace) -> None:
    """取消已掌握"""
    client = _get_client()
    result = client.mark_unmastered(args.note_id)
    if result.get("success"):
        print(f"✓ 笔记 {args.note_id} 已取消已掌握标记")
    else:
        print(f"取消失败: {result.get('message')}")
        sys.exit(1)


def cmd_variation(args: argparse.Namespace) -> None:
    """生成变式题"""
    client = _get_client()
    print(f"正在为笔记 {args.note_id} 生成 {args.count} 道变式题...")
    result = client.generate_variation(args.note_id, args.difficulty, args.count)
    if result.get("success"):
        items = result.get("data", {}).get("items", [])
        print(f"\n✓ 生成成功，共 {len(items)} 道变式题:")
        for i, item in enumerate(items, 1):
            q = item.get("question", item.get("stem", ""))
            print(f"\n{i}. {q[:100]}")
            answer = item.get("correct_answer", item.get("answer", ""))
            if answer:
                print(f"   答案: {answer}")
    else:
        print(f"生成失败: {result.get('message')}")
        sys.exit(1)


def cmd_delete(args: argparse.Namespace) -> None:
    """删除错题"""
    client = _get_client()
    result = client.delete_error_book(args.note_id)
    if result.get("success"):
        print(f"✓ 错题 {args.note_id} 已删除")
    else:
        print(f"删除失败: {result.get('message')}")
        sys.exit(1)


def _get_client() -> DeepAIStudyClient:
    server = get_config_value("server")
    username = get_config_value("username")
    password = get_config_value("password")

    if not server:
        raise ValueError("未配置服务器地址，请运行:\n  deepaistudy-errors config set server https://www.deepaistudy.com")
    if not username or not password:
        raise ValueError("未配置用户名或密码，请运行:\n  deepaistudy-errors config set username <邮箱>\n  deepaistudy-errors config set password <密码>")

    return DeepAIStudyClient(server, username, password)


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def main() -> None:
    if not HAS_REQUESTS:
        print("错误: 需要安装 requests 库: pip install requests")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="深智智错题本 CLI")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # config
    config_sp = subparsers.add_parser("config", help="配置管理")
    config_sp.add_argument("subcommand", nargs="?", choices=["set", "list"], help="子命令")
    config_sp.add_argument("key", nargs="?", help="配置项")
    config_sp.add_argument("value", nargs="?", help="配置值")

    # add
    add_sp = subparsers.add_parser("add", help="添加错题（上传图片 + AI 分析）")
    add_sp.add_argument("images", nargs="+", help="作业/试卷图片路径（可多张）")
    add_sp.add_argument("--subject", "-s", default="", help="学科，如：数学、语文、英语（AI会自动识别）")
    add_sp.add_argument("--title", "-t", default="", help="标题")
    add_sp.add_argument("--auto-add", action="store_true", help="自动添加识别出的所有错题（默认）")
    add_sp.add_argument("--preview", action="store_true", help="仅预览识别结果，不保存到错题本")
    add_sp.add_argument("--count", "-n", type=int, default=0, help="最多添加多少道错题（0=全部）")

    # list
    list_sp = subparsers.add_parser("list", help="查看错题列表")
    list_sp.add_argument("--subject", "-s", default="", help="按学科筛选")
    list_sp.add_argument("--page", "-p", type=int, help="页码")
    list_sp.add_argument("--per-page", type=int, help="每页数量")
    list_sp.add_argument("--search", default="", help="搜索关键词")
    list_sp.add_argument("--sort", default="latest", choices=["latest", "oldest"], help="排序")

    # status
    status_sp = subparsers.add_parser("status", help="查看/轮询 AI 分析状态")
    status_sp.add_argument("task_id", help="任务 ID")
    status_sp.add_argument("--interval", type=int, default=5, help="轮询间隔（秒）")
    status_sp.add_argument("--timeout", type=int, default=300, help="超时时间（秒）")

    # master
    master_sp = subparsers.add_parser("master", help="标记为已掌握")
    master_sp.add_argument("note_id", type=int, help="笔记 ID")

    # unmaster
    unmaster_sp = subparsers.add_parser("unmaster", help="取消已掌握标记")
    unmaster_sp.add_argument("note_id", type=int, help="笔记 ID")

    # variation
    var_sp = subparsers.add_parser("variation", help="生成变式题")
    var_sp.add_argument("note_id", type=int, help="笔记 ID")
    var_sp.add_argument("--count", "-n", type=int, default=3, help="生成数量")
    var_sp.add_argument("--difficulty", "-d", default="medium", choices=["easy", "medium", "hard"], help="难度")

    # delete
    del_sp = subparsers.add_parser("delete", help="删除错题")
    del_sp.add_argument("note_id", type=int, help="笔记 ID")

    args = parser.parse_args()

    if args.command == "config":
        cmd_config(args)
    elif args.command == "add":
        cmd_add(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "master":
        cmd_master(args)
    elif args.command == "unmaster":
        cmd_unmaster(args)
    elif args.command == "variation":
        cmd_variation(args)
    elif args.command == "delete":
        cmd_delete(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
