#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
招投标商机全周期追踪工具 - Skill 入口

提供 CLI 和函数调用两种方式，统一权限控制：
- CLI 模式：通过命令行参数调用
- 函数模式：通过 bid_project_manager() 调用（OpenClaw Skill）

用法:
    python -m bidding_tracker.skill --help
    python -m bidding_tracker.skill init --name "王总监"
    python -m bidding_tracker.skill register --json '{...}' --manager-name "张经理"
"""

import argparse
import json
import os
import sqlite3
import subprocess
import sys
from bidding_tracker.config import get_db_path, load_env, get_evaluate_prompt, get_profiles

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')

HELP_TEXT = """招投标商机全周期追踪工具

用法:
    bidding-tracker init --name "姓名"           初始化系统（首次使用，总监注册）
    bidding-tracker register                     注册新项目（交互式）
    bidding-tracker register --json '...'        注册新项目（JSON 参数）
    bidding-tracker status                       查看项目列表
    bidding-tracker status --keyword "关键词"    按关键词搜索项目
    bidding-tracker purchased "项目名"            确认已购买标书
    bidding-tracker seal "项目名"                 确认已封标
    bidding-tracker result "项目名" --won         录入中标结果
    bidding-tracker result "项目名" --lost        录入未中标结果
    bidding-tracker cancel "项目名"               取消项目
    bidding-tracker users                         查看团队成员
    bidding-tracker adduser --new-user-id xxx --name "姓名"  添加负责人
    bidding-tracker stats                         查看统计（默认按月）
    bidding-tracker stats --by-manager           按负责人统计
    bidding-tracker stats --by-month --period 2026-Q1  按季度统计
    bidding-tracker evaluate --file /path/to/tender.pdf    解析招标文件（胜算评估）
    bidding-tracker bind-eval "项目名" --probability 0.75  绑定胜算到项目
    bidding-tracker bind-eval "项目名" --probability 0.75 --report "技术优势明显"

示例:
    bidding-tracker init --name "王总监"
    bidding-tracker status
    bidding-tracker result "XX系统采购" --won --our-price 980000 --winning-price 950000
    bidding-tracker stats --by-month
"""

# 权限常量
DIRECTOR_ONLY = {'register', 'adduser', 'users', 'stats'}


def get_conn():
    """获取数据库连接"""
    conn = sqlite3.connect(os.path.abspath(get_db_path()), timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def get_user(conn, user_id: str) -> dict | None:
    """查询用户身份"""
    row = conn.execute(
        "SELECT role, name FROM users WHERE wecom_userid = ?",
        (user_id,)).fetchone()
    return dict(row) if row else None


def check_permission(user_id: str, action: str) -> tuple[bool, str, str]:
    """
    检查用户权限，返回 (允许, 错误信息, 用户角色)
    """
    conn = get_conn()
    try:
        if action == 'init':
            # init 操作：检查是否已有总监
            director = conn.execute(
                "SELECT name FROM users WHERE role = 'director'"
            ).fetchone()
            if director:
                return False, f"系统已初始化，总监：{director['name']}", ""
            # init 无需用户存在，可直接注册
            return True, "", "director"

        # 非 init 操作：检查系统是否已初始化
        director = conn.execute(
            "SELECT wecom_userid, name FROM users WHERE role = 'director'"
        ).fetchone()

        if not director:
            return False, "系统尚未初始化，请先执行 init", ""

        # 查询当前用户
        user = get_user(conn, user_id)
        if not user:
            return False, "您尚未被添加为系统用户", ""

        role, name = user['role'], user['name']

        # 命令级权限校验
        if action in DIRECTOR_ONLY and role != 'director':
            return False, "仅总监可执行此操作", role

        return True, "", role
    finally:
        conn.close()


def check_project_access(user_id: str, keyword: str, role: str) -> tuple[int | None, str]:
    """
    检查项目访问权限，返回 (project_id, 错误信息)
    """
    if not keyword:
        return None, "缺少项目标识"

    conn = get_conn()
    try:
        if role == 'director':
            row = conn.execute(
                "SELECT id FROM projects WHERE project_no = ? OR project_name LIKE ?",
                (keyword, f"%{keyword}%")).fetchone()
        else:
            row = conn.execute(
                "SELECT p.id FROM projects p "
                "JOIN users u ON u.name = p.project_manager "
                "WHERE u.wecom_userid = ? AND (p.project_no = ? OR p.project_name LIKE ?)",
                (user_id, keyword, f"%{keyword}%")).fetchone()

        if not row:
            msg = "项目不存在" if role == 'director' else "该项目不在您的负责范围内"
            return None, msg
        return row['id'], ""
    finally:
        conn.close()


def run_script(script_name: str, args: list[str], db_path: str = None) -> subprocess.CompletedProcess:
    """运行 scripts/ 下的脚本"""
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    cmd = [sys.executable, script_path] + args
    env = os.environ.copy()
    env['DB_PATH'] = db_path or get_db_path()
    # 确保子进程能够导入 bidding_tracker 包
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    existing_pp = env.get('PYTHONPATH', '')
    env['PYTHONPATH'] = f"{project_root}:{existing_pp}" if existing_pp else project_root
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return result


def extract_document_text(file_path: str) -> tuple[str, str]:
    """提取文档文本，返回 (文本内容, 错误信息)。支持 PDF、Word、纯文本。"""
    path = os.path.abspath(file_path)
    if not os.path.exists(path):
        return "", f"文件不存在：{path}"
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        try:
            from pypdf import PdfReader
            reader = PdfReader(path)
            pages = [page.extract_text() or "" for page in reader.pages]
            return "\n".join(pages), ""
        except ImportError:
            return "", "缺少依赖：请执行 pip install pypdf"
        except Exception as e:
            return "", f"PDF 解析失败：{e}"
    elif ext == '.docx':
        try:
            import docx
            doc = docx.Document(path)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n".join(paragraphs), ""
        except ImportError:
            return "", "缺少依赖：请执行 pip install python-docx"
        except Exception as e:
            return "", f"Word 文档解析失败：{e}"
    else:
        try:
            with open(path, encoding='utf-8') as f:
                return f.read(), ""
        except Exception as e:
            return "", f"文件读取失败：{e}"


# ========== 命令处理函数 ==========

def cmd_init(args, user_id: str):
    """初始化系统（注册总监）"""
    # 检查是否已有总监
    conn = get_conn()
    try:
        director = conn.execute(
            "SELECT name FROM users WHERE role = 'director'"
        ).fetchone()
        if director:
            return {"status": "error", "message": f"系统已初始化，总监：{director['name']}"}
    finally:
        conn.close()

    result = run_script('manage_users.py', ['--bootstrap', '--user-id', user_id, '--name', args.name])

    if result.returncode == 0:
        return {"status": "ok", "message": f"总监注册成功：{args.name}"}
    else:
        return {"status": "error", "message": json.loads(result.stderr).get("error", "注册失败")}


def cmd_register(args, user_id: str):
    """注册新项目"""
    if not args.json and not args.interactive:
        return {"status": "error", "message": "需要提供 --json 或使用交互模式"}

    if not args.manager_name:
        return {"status": "error", "message": "需要提供 --manager-name 参数"}

    travel_days = args.travel_days or 2
    cmd_args = ['--json', args.json or '{}', '--manager-name', args.manager_name, '--travel-days', str(travel_days)]

    if args.file:
        cmd_args.extend(['--announcement-file', args.file])

    result = run_script('register_project.py', cmd_args)

    if result.returncode == 0:
        data = json.loads(result.stdout)
        return {"status": "ok", "message": f"项目注册成功: {data.get('project_no')}", "data": data}
    else:
        return {"status": "error", "message": json.loads(result.stderr).get("error", "注册失败")}


def cmd_status(args, user_id: str, role: str):
    """查看项目列表"""
    cmd_args = []
    if args.keyword:
        cmd_args.extend(['--keyword', args.keyword])
    if args.active_only:
        cmd_args.append('--active-only')
    if args.upcoming_days:
        cmd_args.extend(['--upcoming-days', str(args.upcoming_days)])

    # 非总监需要传递 user-id 进行过滤
    if role == 'manager':
        cmd_args.extend(['--user-id', user_id])

    result = run_script('query_projects.py', cmd_args)

    if result.returncode == 0:
        projects = json.loads(result.stdout)
        return {"status": "ok", "data": projects}
    else:
        return {"status": "error", "message": json.loads(result.stderr).get("error", "查询失败")}


def _update_project_status(user_id: str, keyword: str, status_value: str, role: str) -> dict:
    """更新项目状态"""
    project_id, err = check_project_access(user_id, keyword, role)
    if err:
        return {"status": "error", "message": err}

    result = run_script('update_project.py', ['--id', str(project_id), '--field', 'status', '--value', status_value])

    if result.returncode == 0:
        return {"status": "ok", "message": f"项目状态已更新为 {status_value}"}
    else:
        return {"status": "error", "message": json.loads(result.stderr).get("error", "更新失败")}


def cmd_purchased(args, user_id: str, role: str):
    """确认标书已购买"""
    if not args.keyword:
        return {"status": "error", "message": "需要提供项目名称"}
    return _update_project_status(user_id, args.keyword, 'doc_purchased', role)


def cmd_seal(args, user_id: str, role: str):
    """确认已封标"""
    if not args.keyword:
        return {"status": "error", "message": "需要提供项目名称"}
    return _update_project_status(user_id, args.keyword, 'sealed', role)


def cmd_result(args, user_id: str, role: str):
    """录入开标结果"""
    if not args.keyword:
        return {"status": "error", "message": "需要提供项目名称"}

    if not args.won and not args.lost:
        return {"status": "error", "message": "需要指定 --won 或 --lost"}

    project_id, err = check_project_access(user_id, args.keyword, role)
    if err:
        return {"status": "error", "message": err}

    cmd_args = ['--project-id', str(project_id), '--won', 'true' if args.won else 'false']

    if args.our_price:
        cmd_args.extend(['--our-price', str(args.our_price)])
    if args.winning_price:
        cmd_args.extend(['--winning-price', str(args.winning_price)])
    if args.winner:
        cmd_args.extend(['--winner', args.winner])
    if args.notes:
        cmd_args.extend(['--notes', args.notes])

    result = run_script('record_result.py', cmd_args)

    if result.returncode == 0:
        return {"status": "ok", "message": "开标结果已录入"}
    else:
        return {"status": "error", "message": json.loads(result.stderr).get("error", "录入失败")}


def cmd_cancel(args, user_id: str, role: str):
    """取消项目"""
    if not args.keyword:
        return {"status": "error", "message": "需要提供项目名称"}
    return _update_project_status(user_id, args.keyword, 'cancelled', role)


def cmd_users(args, user_id: str):
    """查看用户列表"""
    cmd_args = ['--list']
    if args.role:
        cmd_args.extend(['--role', args.role])

    result = run_script('manage_users.py', cmd_args)

    if result.returncode == 0:
        users = json.loads(result.stdout)
        return {"status": "ok", "data": users}
    else:
        return {"status": "error", "message": json.loads(result.stderr).get("error", "查询失败")}


def cmd_adduser(args, user_id: str):
    """添加用户"""
    if not args.new_user_id or not args.name:
        return {"status": "error", "message": "需要提供 --new-user-id 和 --name 参数"}

    cmd_args = ['--add', '--caller-id', user_id, '--user-id', args.new_user_id, '--name', args.name]

    if args.contact:
        cmd_args.extend(['--contact', args.contact])

    result = run_script('manage_users.py', cmd_args)

    if result.returncode == 0:
        return {"status": "ok", "message": f"用户添加成功：{args.name}"}
    else:
        return {"status": "error", "message": json.loads(result.stderr).get("error", "添加失败")}


def cmd_stats(args, user_id: str):
    """查看统计"""
    if args.by_manager and args.by_month:
        return {"status": "error", "message": "--by-manager 和 --by-month 不能同时使用"}

    cmd_args = []
    if args.by_manager:
        cmd_args.append('--by-manager')
    elif args.by_month:
        cmd_args.append('--by-month')
    else:
        cmd_args.append('--by-month')

    if args.period:
        cmd_args.extend(['--period', args.period])

    result = run_script('stats.py', cmd_args)

    if result.returncode == 0:
        stats = json.loads(result.stdout)
        return {"status": "ok", "data": stats}
    else:
        return {"status": "error", "message": json.loads(result.stderr).get("error", "统计失败")}


def cmd_evaluate(args, user_id: str):
    """解析招标文件并组装分析 prompt（供 OpenClaw LLM 消费）"""
    if not args.file:
        return {"status": "error", "message": "需要提供 --file 参数指定招标文件路径"}
    text, err = extract_document_text(args.file)
    if err:
        return {"status": "error", "message": err}
    if not text.strip():
        return {"status": "error", "message": "文档内容为空，无法解析"}
    prompt = get_evaluate_prompt()
    file_name = os.path.basename(args.file)
    return {
        "status": "ok",
        "message": f"招标文件《{file_name}》已解析（{len(text)} 字），请按分析框架进行深度博弈评估",
        "data": {
            "analysis_prompt": prompt,
            "profiles": get_profiles(),
            "document_text": text,
            "file_name": file_name,
        }
    }


def cmd_bind_eval(args, user_id: str, role: str):
    """将评估结果绑定到项目"""
    if not args.keyword:
        return {"status": "error", "message": "需要提供项目名称或编号"}
    if args.probability is None:
        return {"status": "error", "message": "需要提供 --probability 参数"}
    if not (0.0 <= args.probability <= 1.0):
        return {"status": "error", "message": "--probability 取值范围 0.0~1.0"}
    project_id, err = check_project_access(user_id, args.keyword, role)
    if err:
        return {"status": "error", "message": err}
    from datetime import datetime
    eval_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = run_script('update_project.py', ['--id', str(project_id), '--field', 'win_probability', '--value', str(args.probability)])
    if result.returncode != 0:
        return {"status": "error", "message": json.loads(result.stderr).get("error", "更新胜率失败")}
    if args.report:
        result2 = run_script('update_project.py', ['--id', str(project_id), '--field', 'win_prediction', '--value', args.report])
        if result2.returncode != 0:
            return {"status": "error", "message": json.loads(result2.stderr).get("error", "更新预测报告失败")}
    run_script('update_project.py', ['--id', str(project_id), '--field', 'win_eval_at', '--value', eval_at])
    prob_pct = f"{args.probability * 100:.0f}%"
    report_preview = f"，报告：{args.report[:50]}..." if args.report and len(args.report) > 50 else (f"，报告：{args.report}" if args.report else "")
    return {"status": "ok", "message": f"胜算评估已绑定：{prob_pct}{report_preview}"}


# ========== CLI 入口 ==========

def main():
    """CLI 入口函数"""
    parser = argparse.ArgumentParser(
        description='招投标商机全周期追踪工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=HELP_TEXT
    )
    parser.add_argument('--user-id', help='用户 ID（CLI 模式下使用环境变量）')

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # init
    p_init = subparsers.add_parser('init', help='初始化系统（首次使用，总监注册）')
    p_init.add_argument('--name', required=True, help='总监显示名称')

    # register
    p_reg = subparsers.add_parser('register', help='注册新项目')
    p_reg.add_argument('--json', help='项目信息 JSON 字符串')
    p_reg.add_argument('--manager-name', help='项目负责人姓名')
    p_reg.add_argument('--travel-days', type=int, default=2, help='运输天数')
    p_reg.add_argument('--file', help='招标公告文件路径')
    p_reg.add_argument('--interactive', action='store_true', help='交互式输入')

    # status
    p_status = subparsers.add_parser('status', help='查看项目列表')
    p_status.add_argument('--keyword', help='搜索关键词')
    p_status.add_argument('--active-only', action='store_true', help='仅显示活跃项目')
    p_status.add_argument('--upcoming-days', type=int, help='显示 N 天内有关键节点的项目')

    # purchased
    p_purchased = subparsers.add_parser('purchased', help='确认已购买标书')
    p_purchased.add_argument('keyword', nargs='?', help='项目名称或编号')

    # seal
    p_seal = subparsers.add_parser('seal', help='确认已封标')
    p_seal.add_argument('keyword', nargs='?', help='项目名称或编号')

    # result
    p_result = subparsers.add_parser('result', help='录入开标结果')
    p_result.add_argument('keyword', nargs='?', help='项目名称或编号')
    p_result.add_argument('--won', action='store_true', help='中标')
    p_result.add_argument('--lost', action='store_true', help='未中标')
    p_result.add_argument('--our-price', type=int, help='我方报价')
    p_result.add_argument('--winning-price', type=int, help='中标价')
    p_result.add_argument('--winner', help='中标单位')
    p_result.add_argument('--notes', help='备注')

    # cancel
    p_cancel = subparsers.add_parser('cancel', help='取消项目')
    p_cancel.add_argument('keyword', nargs='?', help='项目名称或编号')

    # users
    p_users = subparsers.add_parser('users', help='查看团队成员')
    p_users.add_argument('--role', choices=['director', 'manager'], help='按角色过滤')

    # adduser
    p_adduser = subparsers.add_parser('adduser', help='添加负责人')
    p_adduser.add_argument('--new-user-id', required=True, help='新用户 ID')
    p_adduser.add_argument('--name', required=True, help='用户显示名称')
    p_adduser.add_argument('--contact', help='联系方式')

    # stats
    p_stats = subparsers.add_parser('stats', help='查看统计')
    p_stats.add_argument('--by-manager', action='store_true', help='按负责人统计')
    p_stats.add_argument('--by-month', action='store_true', help='按月份统计')
    p_stats.add_argument('--period', help='统计周期')

    # evaluate
    p_eval = subparsers.add_parser('evaluate', help='解析招标文件，生成胜算评估所需内容')
    p_eval.add_argument('--file', required=True, help='招标文件路径 (PDF/Word/TXT)')

    # bind-eval
    p_bind = subparsers.add_parser('bind-eval', help='将评估胜率绑定到项目')
    p_bind.add_argument('keyword', nargs='?', help='项目名称或编号')
    p_bind.add_argument('--probability', type=float, required=True, help='胜率 0.0-1.0')
    p_bind.add_argument('--report', help='预测报告摘要')

    args = parser.parse_args()

    # 确保数据目录存在
    load_env()
    os.makedirs(os.path.dirname(os.path.abspath(get_db_path())), exist_ok=True)

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # 获取用户 ID
    user_id = args.user_id or os.environ.get('USER', 'cli_user')

    # 检查权限
    ok, err_msg, role = check_permission(user_id, args.command)
    if not ok:
        print(json.dumps({"status": "error", "message": err_msg}, ensure_ascii=False))
        sys.exit(1)

    # 执行命令
    result = None
    if args.command == 'init':
        result = cmd_init(args, user_id)
    elif args.command == 'register':
        result = cmd_register(args, user_id)
    elif args.command == 'status':
        result = cmd_status(args, user_id, role)
    elif args.command == 'purchased':
        result = cmd_purchased(args, user_id, role)
    elif args.command == 'seal':
        result = cmd_seal(args, user_id, role)
    elif args.command == 'result':
        result = cmd_result(args, user_id, role)
    elif args.command == 'cancel':
        result = cmd_cancel(args, user_id, role)
    elif args.command == 'users':
        result = cmd_users(args, user_id)
    elif args.command == 'adduser':
        result = cmd_adduser(args, user_id)
    elif args.command == 'stats':
        result = cmd_stats(args, user_id)
    elif args.command == 'evaluate':
        result = cmd_evaluate(args, user_id)
    elif args.command == 'bind-eval':
        result = cmd_bind_eval(args, user_id, role)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result.get('status') == 'ok' else 1)


# ========== OpenClaw Skill 函数入口 ==========

def bid_project_manager(action_type: str, project_data: dict = None, **kwargs) -> dict:
    """
    OpenClaw Skill Tool 函数入口

    Args:
        action_type: 操作类型
            项目生命周期: init / register / status / purchased / seal / result / cancel
            团队管理:     users / adduser
            统计分析:     stats
            胜算评估:     evaluate / bind-eval
        project_data: 业务参数 dict
        **kwargs: OpenClaw 引擎注入，含 __context__

    Returns:
        {"status": "ok"|"error", "message": "...", "data": {...}}
    """
    project_data = project_data or {}

    # 从上下文获取用户身份
    try:
        user_id = kwargs['__context__']['body']['from']['userid']
    except (KeyError, TypeError):
        return {"status": "error", "message": "无法识别您的企业微信身份"}

    # 附件路径处理
    if action_type == 'register':
        try:
            attachments = kwargs['__context__']['body'].get('attachments', [])
            if attachments:
                project_data['_attachment_path'] = attachments[0].get('local_path')
        except (KeyError, TypeError, IndexError):
            pass

    # 检查权限
    ok, err_msg, role = check_permission(user_id, action_type)
    if not ok:
        return {"status": "error", "message": err_msg}

    # 构建 args 对象
    class Args:
        pass

    args = Args()
    if action_type == 'init':
        args.name = project_data.get('name', user_id)
    elif action_type == 'register':
        args.json = json.dumps(project_data.get('fields', {}), ensure_ascii=False)
        args.manager_name = project_data.get('manager_name', '')
        args.travel_days = project_data.get('travel_days', 2)
        args.file = project_data.get('_attachment_path')
        args.interactive = False
    elif action_type in ('status', 'purchased', 'seal', 'result', 'cancel'):
        args.keyword = project_data.get('keyword')
        if action_type == 'status':
            args.active_only = project_data.get('active_only', False)
            args.upcoming_days = project_data.get('upcoming_days')
        if action_type == 'result':
            args.won = project_data.get('is_won')
            args.lost = not project_data.get('is_won') if 'is_won' in project_data else False
            args.our_price = project_data.get('our_price')
            args.winning_price = project_data.get('winning_price')
            args.winner = project_data.get('winner')
            args.notes = project_data.get('notes')
    elif action_type == 'users':
        args.role = project_data.get('role')
    elif action_type == 'adduser':
        args.new_user_id = project_data.get('user_id', '')
        args.name = project_data.get('name', '')
        args.contact = project_data.get('contact')
    elif action_type == 'stats':
        args.by_manager = project_data.get('by_manager')
        args.by_month = project_data.get('by_month')
        args.period = project_data.get('period')
    elif action_type == 'evaluate':
        try:
            attachments = kwargs['__context__']['body'].get('attachments', [])
            if attachments:
                project_data['file'] = attachments[0].get('local_path', '')
        except (KeyError, TypeError, IndexError):
            pass
        args.file = project_data.get('file', '')
    elif action_type == 'bind-eval':
        args.keyword = project_data.get('keyword', '')
        args.probability = project_data.get('probability')
        args.report = project_data.get('report', '')

    # 执行命令
    if action_type == 'init':
        return cmd_init(args, user_id)
    elif action_type == 'register':
        return cmd_register(args, user_id)
    elif action_type == 'status':
        return cmd_status(args, user_id, role)
    elif action_type == 'purchased':
        return cmd_purchased(args, user_id, role)
    elif action_type == 'seal':
        return cmd_seal(args, user_id, role)
    elif action_type == 'result':
        return cmd_result(args, user_id, role)
    elif action_type == 'cancel':
        return cmd_cancel(args, user_id, role)
    elif action_type == 'users':
        return cmd_users(args, user_id)
    elif action_type == 'adduser':
        return cmd_adduser(args, user_id)
    elif action_type == 'stats':
        return cmd_stats(args, user_id)
    elif action_type == 'evaluate':
        return cmd_evaluate(args, user_id)
    elif action_type == 'bind-eval':
        return cmd_bind_eval(args, user_id, role)
    else:
        return {"status": "error", "message": f"未知操作类型：{action_type}"}


if __name__ == '__main__':
    main()