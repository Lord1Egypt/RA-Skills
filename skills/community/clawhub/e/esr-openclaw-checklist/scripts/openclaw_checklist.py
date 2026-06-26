import os
import json
import subprocess
import re
from datetime import datetime

# =========================
# 常量定义
# =========================
OPENCLAW_PORT = 18789
HOME = os.path.expanduser("~")
CONFIG_PATH = os.path.join(HOME, ".openclaw", "openclaw.json")
SKILL_PATH = os.path.join(HOME, ".openclaw", "skills")

HIGH = 3
MEDIUM = 2
LOW = 1

issues = []
results = []
check_counter = 0

# =========================
# 工具函数
# =========================
def run_command(cmd):
    """执行终端命令，只返回 stdout，不打印 stderr"""
    try:
        return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
    except:
        return ""

def add_issue(category, description, severity, recommendation):
    issues.append({
        "category": category,
        "description": description,
        "severity": severity,
        "recommendation": recommendation
    })

def print_check(title, detail, risk_flag=False, recommendation=""):
    global check_counter
    check_counter += 1

    status = "配置安全" if not risk_flag else "存在风险"

    # 终端输出
    print(f"\n检查项{check_counter}: {title}")
    print(f"检查详情: {detail}")
    if risk_flag and recommendation:
        print(f"修复建议: {recommendation}")
    print(f"安全状态: {status}")
    print("-" * 60)

    # 写入 JSON 结构
    results.append({
        "check_id": check_counter,
        "title": title,
        "detail": detail,
        "status": status,
        "risk": risk_flag,
        "recommendation": recommendation if risk_flag else ""
    })


# =========================
# L1 网络暴露面
# =========================
def check_default_port():
    title = "默认端口使用情况"
    risk_flag = False
    recommendation = "修改默认端口为 17999-18999 之间，不使用默认端口"

    CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
    DEFAULT_PORT = 18789
    SAFE_MIN = 17999
    SAFE_MAX = 18999

    if not os.path.exists(CONFIG_PATH):
        risk_flag = True
        detail = "未检测到 openclaw.json 配置文件"
        add_issue("Network", detail, LOW, recommendation)
        print_check(title, detail, risk_flag, recommendation)
        return

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)

        # 🔥 关键修复：读取 gateway.port
        gateway = config.get("gateway", {})
        port = gateway.get("port")

        # 未设置端口
        if port is None:
            risk_flag = True
            detail = f"未配置 gateway.port（可能默认使用 {DEFAULT_PORT}）"
            add_issue("Network", detail, LOW, recommendation)

        # 类型异常
        elif not isinstance(port, int):
            risk_flag = True
            detail = f"端口类型异常: {port}"
            add_issue("Network", detail, LOW, recommendation)

        # 使用默认端口
        elif port == DEFAULT_PORT:
            risk_flag = True
            detail = f"使用默认端口 {DEFAULT_PORT}"
            add_issue("Network", detail, LOW, recommendation)

        # 不在建议区间
        elif not (SAFE_MIN <= port <= SAFE_MAX):
            risk_flag = True
            detail = f"端口 {port} 不在建议区间 {SAFE_MIN}-{SAFE_MAX}"
            add_issue("Network", detail, LOW, recommendation)

        # 合规
        else:
            detail = f"已使用合规自定义端口 {port}"

    except json.JSONDecodeError:
        risk_flag = True
        detail = "openclaw.json 格式错误"
        add_issue("Network", detail, LOW, recommendation)

    except Exception as e:
        risk_flag = True
        detail = f"读取配置异常: {str(e)}"
        add_issue("Network", detail, LOW, recommendation)

    print_check(title, detail, risk_flag, recommendation if risk_flag else None)

def check_listening_address():
    title = "服务监听地址检查"
    risk_flag = False
    recommendation = "绑定服务到 127.0.0.1，仅允许本地访问"

    # 方法1: 尝试使用lsof
    output = run_command(f"lsof -i :{OPENCLAW_PORT}")
    
    # 如果lsof不可用，尝试其他方法
    if "command not found" in output or output == "":
        # 方法2: 使用curl测试连接
        curl_output = run_command(f"curl -s -o /dev/null -w '%{{http_code}}' http://127.0.0.1:{OPENCLAW_PORT}/ 2>/dev/null || echo 'FAIL'")
        
        if curl_output == "200":
            # 方法3: 检查OpenClaw服务状态
            status_output = run_command("openclaw gateway status 2>/dev/null || echo ''")
            
            if "127.0.0.1" in status_output and f"port={OPENCLAW_PORT}" in status_output:
                detail = "仅监听 127.0.0.1（本地安全）"
            elif "0.0.0.0" in status_output:
                risk_flag = True
                detail = "监听地址为 0.0.0.0（存在公网暴露风险）"
                add_issue("Network", detail, HIGH, recommendation)
            else:
                risk_flag = True
                detail = "服务状态检测异常"
                add_issue("Network", detail, MEDIUM, recommendation)
        else:
            risk_flag = True
            detail = "未检测到端口监听（需人工确认）"
            add_issue("Network", detail, HIGH, recommendation)
    
    elif "0.0.0.0" in output:
        risk_flag = True
        detail = "监听地址为 0.0.0.0（存在公网暴露风险）"
        add_issue("Network", detail, HIGH, recommendation)
    elif "127.0.0.1" in output or "localhost" in output:
        detail = "仅监听 127.0.0.1（本地安全）"
    elif output == "":
        risk_flag = True
        detail = "未检测到端口监听（需人工确认）"
        add_issue("Network", detail, HIGH, recommendation)
    else:
        risk_flag = True
        detail = "检测到异常监听信息"
        add_issue("Network", detail, MEDIUM, recommendation)

    print_check(title, detail, risk_flag, recommendation)

def check_tunneling_tools():
    title = "内网穿透工具检测"
    risk_flag = False
    recommendation = "卸载未授权内网穿透工具"

    # 扩充后的穿透工具关键字（单行定义，便于维护）
    TUNNEL_KEYWORDS = (
        "ngrok", "frpc", "frps", "cloudflared",
        "nps", "npc", "natapp",
        "localtunnel", "lt --port",
        "serveo", "sish",
        "gost", "rathole",
        "boringproxy", "telebit",
        "pagekite", "zrok",
        "tailscale", "zerotier",
        "inlets", "chisel"
    )

    processes = run_command("ps aux").lower()

    detected = [tool for tool in TUNNEL_KEYWORDS if tool in processes]

    if detected:
        risk_flag = True
        detail = f"检测到穿透工具: {', '.join(set(detected))}"
        add_issue("Network", detail, HIGH, recommendation)
    else:
        detail = "未检测到内网穿透工具"

    print_check(title, detail, risk_flag, recommendation if risk_flag else None)

# =========================
# L2 应用安全
# =========================
def check_node_version():
    title = "Node.js 版本检查"
    risk_flag = False
    recommendation = "升级 Node.js 至 >=18 LTS"

    output = run_command("node -v")
    match = re.search(r"v(\d+)", output)

    if match:
        version = int(match.group(1))
        if version < 18:
            risk_flag = True
            detail = f"Node.js 版本过低: {version}"
            add_issue("Application", detail, MEDIUM, recommendation)
        else:
            detail = f"Node.js 版本正常: {version}"
    else:
        risk_flag = True
        detail = "未检测到 Node.js"
        add_issue("Application", detail, HIGH, recommendation)

    print_check(title, detail, risk_flag, recommendation)

def check_password_mode():
    title = "密码登录模式检查"
    risk_flag = False
    recommendation = "配置 mode: password，启用密码登录"

    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
            if config.get("mode") == "password":
                detail = "已启用密码登录模式"
            else:
                risk_flag = True
                detail = "未启用密码登录模式"
                add_issue("Application", detail, HIGH, recommendation)
    else:
        risk_flag = True
        detail = "未找到 openclaw.json"

    print_check(title, detail, risk_flag, recommendation)

# =========================
# L3 供应链
# =========================
def check_skill_inventory():
    title = "Skill 数量及官方来源检查"
    risk_flag = False
    recommendation = "仅使用官方来源 Skill，核实非官方 Skill 来源"

    cli_output = run_command("openclaw skills list")
    total_skills = len([line for line in cli_output.split("\n") if line.strip()]) if cli_output else 0

    unofficial = []
    if os.path.exists(SKILL_PATH):
        for skill in os.listdir(SKILL_PATH):
            meta_path = os.path.join(SKILL_PATH, skill, "skill.json")
            if os.path.exists(meta_path):
                with open(meta_path, "r") as f:
                    meta = json.load(f)
                    if meta.get("source") != "ClawHub":
                        unofficial.append(skill)
            else:
                unofficial.append(skill)

    if unofficial:
        risk_flag = True
        detail = f"共安装 {total_skills} 个 Skill，非官方: {', '.join(unofficial)}"
        add_issue("SupplyChain", detail, MEDIUM, recommendation)
    else:
        detail = f"共安装 {total_skills} 个 Skill，均为官方来源"

    print_check(title, detail, risk_flag, recommendation)

def check_config_permission():
    title = "配置文件权限检查"
    risk_flag = False
    recommendation = "执行 chmod 600 ~/.openclaw/openclaw.json"

    if os.path.exists(CONFIG_PATH):
        mode = oct(os.stat(CONFIG_PATH).st_mode)[-3:]
        if mode != "600":
            risk_flag = True
            detail = f"openclaw.json 权限为 {mode}"
            add_issue("SupplyChain", detail, HIGH, recommendation)
        else:
            detail = "openclaw.json 权限为 600（安全）"
    else:
        risk_flag = True
        detail = "未找到 openclaw.json"

    print_check(title, detail, risk_flag, recommendation)

# =========================
# 检查项8: OpenClawd 深度安全审计（仅 Sandbox）
# =========================
def check_openclawd_deep_security():
    title = "OpenClawd 深度安全审计"
    risk_flag = False

    output = run_command("openclaw security audit --deep")

    if not output:
        detail = "未获取到审计输出"
        recommendation = "确认 openclaw 命令可用"
        risk_flag = True
        add_issue("Application", detail, HIGH, recommendation)

    elif "sandbox=off" in output:
        detail = "检测到 sandbox=off（未启用沙箱隔离）"
        recommendation = "开启 sandbox，建议设置 agents.defaults.sandbox.mode='all'"
        risk_flag = True
        add_issue("Application", "Sandbox 未启用", HIGH, recommendation)

    else:
        detail = "已启用 Sandbox 隔离模式"

    # ===== 输出格式统一 =====
    print(f"\n检查项8: {title}")
    print(f"检查详情: {detail}")

    if risk_flag:
        print(f"修复建议: {recommendation}")

    status = "配置安全" if not risk_flag else "存在风险"
    print(f"安全状态: {status}")
    print("-" * 60)
# =========================
# 主程序
# =========================
def main():
    check_default_port()
    check_listening_address()
    check_tunneling_tools()
    check_node_version()
    check_password_mode()
    check_skill_inventory()
    check_config_permission()
    check_openclawd_deep_security()

    # 最终报告
    report_status = "存在风险" if issues else "配置安全"

    report = {
    "scan_time": datetime.now().isoformat(),
    "status": report_status,
    "total_checks": check_counter,
    "checks": results,
    "issues": issues
    }

    # 时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scan_result_{timestamp}.json"

    # 获取脚本目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)

    with open(filepath, "w") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    print("\n========== 最终审计结果 ==========")
    print(f"安全状态: {report_status}")
    print(f"问题总数: {len(issues)}")
    print(f"结果已保存：{filepath}")
    
    # ========== V1.2 新增：信息安全部门提示 ==========
    print("\n" + "="*60)
    print("信息安全部门提示：")
    print("="*60)
    print("1. 权限管理：")
    print("   - 不得授予系统高权限，禁止使用root权限运行")
    print("   - 关闭高危系统权限，实行分级授权")
    print("   - 每月清理权限，确保最小权限原则")
    print()
    print("2. 功能禁用：")
    print("   - 禁用OpenClaw内置的支付、商城产品发布等相关功能")
    print("   - 防止产生费用或滥用风险")
    print("="*60)

if __name__ == "__main__":
    main()