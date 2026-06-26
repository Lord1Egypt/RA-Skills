#!/usr/bin/env python3
"""
DeepTask Command Line Interface
提供命令行工具用于管理项目和任务
"""

import argparse
import sys
import os
import subprocess
import shutil
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db_manager import DeepTaskDB, DEFAULT_DB_PATH


def cmd_create_project(args):
    """创建新项目"""
    db = DeepTaskDB(args.db)
    project_id = db.create_project(
        name=args.name,
        description=args.desc or "",
        summary=args.summary or ""
    )
    print(f"✅ 项目已创建：{project_id}")
    print(f"   名称：{args.name}")
    if args.desc:
        print(f"   描述：{args.desc}")
    if args.summary:
        print(f"   摘要：{args.summary}")
    db.close()


def cmd_list_projects(args):
    """列出所有项目"""
    db = DeepTaskDB(args.db)
    projects = db.get_all_projects()
    
    if not projects:
        print("暂无项目")
        db.close()
        return
    
    print(f"\n=== 项目列表 ({len(projects)}) ===\n")
    for p in projects:
        print(f"{p['id']}: {p['name']}")
        if p['description']:
            print(f"   描述：{p['description']}")
        if p['summary']:
            print(f"   摘要：{p['summary']}")
        print(f"   创建时间：{p['created_at']}")
        print()
    
    db.close()


def cmd_show_project(args):
    """显示项目详情"""
    db = DeepTaskDB(args.db)
    project = db.get_project(args.project)
    
    if not project:
        print(f"❌ 项目不存在：{args.project}")
        db.close()
        return
    
    print(f"\n=== 项目：{project['id']} ===\n")
    print(f"名称：{project['name']}")
    print(f"描述：{project['description'] or '无'}")
    print(f"摘要：{project['summary'] or '无'}")
    print(f"创建时间：{project['created_at']}")
    
    sessions = db.get_sessions_by_project(args.project)
    if sessions:
        print(f"\n--- 会话 ({len(sessions)}) ---")
        for s in sessions:
            status_icon = {"pending": "⏳", "in_progress": "🔄", "completed": "✅", "review_pending": "🔍"}.get(s['status'], "❓")
            print(f"  {status_icon} {s['id']}: {s['summary']} [{s['status']}]")
    
    db.close()


def cmd_review(args):
    """人工审核"""
    db = DeepTaskDB(args.db)
    
    if args.session:
        entity_type = "session"
        entity_id = args.session
    elif args.subtask:
        entity_type = "subtask"
        entity_id = args.subtask
    elif args.muf:
        entity_type = "muf"
        entity_id = args.muf
    else:
        print("❌ 请指定审核对象：--session, --subtask, 或 --muf")
        db.close()
        return
    
    review_id = db.add_review_record(
        entity_type=entity_type,
        entity_id=entity_id,
        reviewer=args.reviewer or "admin",
        status=args.status,
        comments=args.comments or ""
    )
    
    if args.status == "approved":
        if entity_type == "session":
            db.update_status("sessions", entity_id, "in_progress")
            print(f"✅ 会话 {entity_id} 已批准，状态更新为 in_progress")
        elif entity_type == "muf":
            db.update_status("mufs", entity_id, "pending")
            print(f"✅ MUF {entity_id} 已批准，状态重置为 pending（可重试）")
    elif args.status == "rejected":
        if entity_type == "session":
            db.update_status("sessions", entity_id, "pending")
            print(f"⚠️  会话 {entity_id} 已拒绝，状态重置为 pending")
    
    print(f"审查记录 ID: {review_id}")
    if args.comments:
        print(f"意见：{args.comments}")
    
    db.close()


def cmd_status(args):
    """显示系统状态"""
    db = DeepTaskDB(args.db)
    
    print("\n=== DeepTask 系统状态 ===\n")
    
    projects = db.get_all_projects()
    print(f"📁 项目总数：{len(projects)}")
    
    cursor = db.conn.cursor()
    cursor.execute("SELECT status, COUNT(*) FROM sessions GROUP BY status")
    print("\n📋 会话状态:")
    for row in cursor.fetchall():
        icon = {"pending": "⏳", "in_progress": "🔄", "completed": "✅", "review_pending": "🔍"}.get(row[0], "❓")
        print(f"  {icon} {row[0]}: {row[1]}")
    
    cursor.execute("SELECT status, COUNT(*) FROM subtasks GROUP BY status")
    print("\n📝 子任务状态:")
    for row in cursor.fetchall():
        icon = {"pending": "⏳", "in_progress": "🔄", "completed": "✅", "review_pending": "🔍"}.get(row[0], "❓")
        print(f"  {icon} {row[0]}: {row[1]}")
    
    cursor.execute("SELECT status, COUNT(*) FROM mufs GROUP BY status")
    print("\n🔧 MUF 状态:")
    for row in cursor.fetchall():
        icon = {"pending": "⏳", "in_progress": "🔄", "completed": "✅", "failed": "🔴"}.get(row[0], "❓")
        print(f"  {icon} {row[0]}: {row[1]}")
    
    review_pending = db.get_review_pending_sessions()
    if review_pending:
        print(f"\n⚠️  待审核会话：{len(review_pending)}")
        for s in review_pending[:5]:
            print(f"  - {s['id']}: {s['summary']}")
    
    failed = db.get_failed_mufs()
    if failed:
        print(f"\n🔴 失败的 MUF: {len(failed)}")
        for m in failed[:5]:
            print(f"  - {m['id']}: {m['summary']}")
    
    db.close()


def cmd_init(args):
    """初始化数据库"""
    db = DeepTaskDB(args.db)
    print(f"✅ 数据库已初始化：{args.db}")
    db.close()


def cmd_check_env(args):
    """检查环境"""
    tool = args.tool
    
    print(f"\n=== 检查 {tool} 环境 ===\n")
    
    tool_path = shutil.which(tool)
    if not tool_path:
        print(f"❌ {tool} 未安装")
        print(f"   提示：请安装 {tool} 后重试")
        return
    
    print(f"✅ {tool} 已安装：{tool_path}")
    
    try:
        result = subprocess.run([tool, "--version"], 
                                capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ 版本：{result.stdout.strip().split(chr(10))[0]}")
        else:
            print(f"⚠️  版本检查失败：{result.stderr.strip()}")
    except Exception as e:
        print(f"⚠️  版本检查异常：{e}")
    
    if tool == "moon":
        print("\n--- Hello World 测试 ---")
        _test_hello_moon()
    elif tool in ["python3", "python"]:
        print("\n--- Hello World 测试 ---")
        _test_hello_python()
    elif tool == "node":
        print("\n--- Hello World 测试 ---")
        _test_hello_node()


def _test_hello_moon():
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            os.makedirs(os.path.join(tmpdir, "src", "test"))
            with open(os.path.join(tmpdir, "moon.mod.json"), "w") as f:
                f.write('{"name":"test","version":"0.1.0"}')
            with open(os.path.join(tmpdir, "src", "test", "moon.pkg.json"), "w") as f:
                f.write('{"is-main":true}')
            with open(os.path.join(tmpdir, "src", "test", "main.mbt"), "w") as f:
                f.write('fn main { println("hello") }')
            
            result = subprocess.run(["moon", "build"], cwd=tmpdir, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print("✅ MoonBit Hello World 编译通过")
            else:
                print(f"❌ MoonBit Hello World 编译失败")
        except Exception as e:
            print(f"⚠️  编译异常：{e}")


def _test_hello_python():
    try:
        result = subprocess.run(["python3", "-c", "print('hello')"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and "hello" in result.stdout:
            print("✅ Python Hello World 运行通过")
        else:
            print(f"❌ Python Hello World 运行失败")
    except Exception as e:
        print(f"⚠️  Python 运行异常：{e}")


def _test_hello_node():
    try:
        result = subprocess.run(["node", "-e", "console.log('hello')"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and "hello" in result.stdout:
            print("✅ Node.js Hello World 运行通过")
        else:
            print(f"❌ Node.js Hello World 运行失败")
    except Exception as e:
        print(f"⚠️  Node.js 运行异常：{e}")


def cmd_reset_project(args):
    """重置项目状态"""
    db = DeepTaskDB(args.db)
    
    project_id = args.project
    reason = args.reason or "用户请求重置"
    
    print(f"\n=== 重置项目 {project_id} ===\n")
    
    project = db.get_project(project_id)
    if not project:
        print(f"❌ 项目不存在：{project_id}")
        db.close()
        return
    
    print(f"项目名称：{project['name']}")
    print(f"重置原因：{reason}")
    
    sessions = db.get_sessions_by_project(project_id)
    for session in sessions:
        db.update_status("sessions", session['id'], "pending")
        print(f"  重置会话：{session['id']} → pending")
    
    for session in sessions:
        subtasks = db.get_subtasks_by_session(session['id'])
        for subtask in subtasks:
            db.update_status("subtasks", subtask['id'], "pending")
            print(f"    重置子任务：{subtask['id']} → pending")
    
    for session in sessions:
        subtasks = db.get_subtasks_by_session(session['id'])
        for subtask in subtasks:
            mufs = db.get_mufs_by_subtask(subtask['id'])
            for muf in mufs:
                db.update_status("mufs", muf['id'], "pending")
                print(f"      重置 MUF: {muf['id']} → pending")
    
    db.add_review_record(
        entity_type="project",
        entity_id=project_id,
        reviewer="admin",
        status="rejected",
        comments=f"项目重置：{reason}"
    )
    
    print(f"\n✅ 项目 {project_id} 已重置")
    db.close()


def cmd_git_log(args):
    """查看 Git Commit 历史"""
    project_id = args.project
    muf_id = args.muf if args.muf else None
    verify = args.verify if hasattr(args, 'verify') else False
    
    workspace = os.path.expanduser("~/.openclaw/workspace")
    project_dir = os.path.join(workspace, f"project_{project_id}")
    
    if not os.path.exists(project_dir):
        print(f"❌ 项目目录不存在：{project_dir}")
        return
    
    if not os.path.exists(os.path.join(project_dir, ".git")):
        print(f"❌ 项目未初始化 Git: {project_dir}")
        return
    
    print(f"\n=== Git Commit 历史：{project_id} ===\n")
    
    cmd = ["git", "log", "--oneline"]
    if muf_id:
        cmd.extend(["--grep", f"MUF_ID:{muf_id}"])
    else:
        cmd.extend(["--grep", "SE_ID:"])
    
    try:
        result = subprocess.run(cmd, cwd=project_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            if result.stdout.strip():
                print(result.stdout.strip())
                print(f"\n共 {len(result.stdout.strip().split(chr(10)))} 个 commit")
                
                if verify:
                    print("\n=== 验证 Commit 格式 ===")
                    for line in result.stdout.strip().split(chr(10)):
                        if "SE_ID:" in line and "MUF_ID:" in line:
                            print(f"  ✅ {line}")
                        else:
                            print(f"  ⚠️  格式可能不正确：{line}")
            else:
                print("暂无 commit 记录")
        else:
            print(f"❌ Git log 失败：{result.stderr}")
    except Exception as e:
        print(f"❌ 执行失败：{e}")


def main():
    parser = argparse.ArgumentParser(description="DeepTask - AI 自动拆解需求与任务管理工具")
    parser.add_argument("--db", default=DEFAULT_DB_PATH, help=f"数据库路径 (默认：{DEFAULT_DB_PATH})")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    p_create = subparsers.add_parser("create_project", help="创建新项目")
    p_create.add_argument("--name", required=True, help="项目名称")
    p_create.add_argument("--desc", help="项目描述")
    p_create.add_argument("--summary", help="项目摘要")
    p_create.set_defaults(func=cmd_create_project)
    
    p_list = subparsers.add_parser("list_projects", help="列出所有项目")
    p_list.set_defaults(func=cmd_list_projects)
    
    p_show = subparsers.add_parser("show_project", help="显示项目详情")
    p_show.add_argument("--project", required=True, help="项目 ID")
    p_show.set_defaults(func=cmd_show_project)
    
    p_review = subparsers.add_parser("review", help="人工审核")
    p_review.add_argument("--session", help="会话 ID")
    p_review.add_argument("--subtask", help="子任务 ID")
    p_review.add_argument("--muf", help="MUF ID")
    p_review.add_argument("--status", required=True, choices=["approved", "rejected"], help="审核结果")
    p_review.add_argument("--reviewer", help="审核者名称")
    p_review.add_argument("--comments", help="审核意见")
    p_review.set_defaults(func=cmd_review)
    
    p_status = subparsers.add_parser("status", help="显示系统状态")
    p_status.set_defaults(func=cmd_status)
    
    p_init = subparsers.add_parser("init", help="初始化数据库")
    p_init.set_defaults(func=cmd_init)
    
    p_check = subparsers.add_parser("check_env", help="检查环境")
    p_check.add_argument("--tool", required=True, help="工具名称 (moon/python/node/rust)")
    p_check.set_defaults(func=cmd_check_env)
    
    p_reset = subparsers.add_parser("reset_project", help="重置项目状态")
    p_reset.add_argument("--project", required=True, help="项目 ID")
    p_reset.add_argument("--reason", help="重置原因")
    p_reset.set_defaults(func=cmd_reset_project)
    
    p_git_log = subparsers.add_parser("git_log", help="查看 Git Commit 历史")
    p_git_log.add_argument("--project", required=True, help="项目 ID")
    p_git_log.add_argument("--muf", help="MUF ID（可选）")
    p_git_log.add_argument("--verify", action="store_true", help="验证 commit 格式")
    p_git_log.set_defaults(func=cmd_git_log)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
