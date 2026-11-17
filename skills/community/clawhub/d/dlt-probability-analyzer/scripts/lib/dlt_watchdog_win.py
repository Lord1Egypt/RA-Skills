# -*- coding: utf-8 -*-
"""
大乐透系统 · 独立 Windows 看门狗 (Standalone Watchdog)
======================================================

不依赖 WorkBuddy 的 OS 级看门狗: 即便 WorkBuddy 停用/重装,
只要本机 Windows 计划任务还在, 失败告警仍能触达用户。

复用 dlt_healthcheck_all.py 第22项(排程真实运行结果)的四项检查:
  (A) 上次结果 LastTaskResult 必须为 0
  (B) 排程无"主动杀任务"反模式(DisallowStartIfOnBatteries 等)
  (C) 上次排程日志无"开跑即中断"特征(^C / 行数过少)
  (D) 未处理告警文件 dlt_run_alert.txt 不得比最新产物更新

异常时(任一检查不过):
  - 写 dlt_run_alert.txt (首行 ALERT, 供 WorkBuddy 看门狗/体检复用)
  - 写 dlt_watchdog_status.txt (首行 ALERT + 时间戳|原因, 与现状格式兼容)
  - 追加 dlt_watchdog_alerts.log (持久化, 跨重启可见)
  - (可选) 弹 Windows 原生提示: 仅当显式传 --toast 时(BurntToast, 否则回退 msg *)
    默认不弹窗 —— 因为本看门狗通常以 SYSTEM 账户在后台运行(无论是否登录都跑),
    后台会话无桌面, 弹窗既无意义也易吊死; 告警以文件落盘为准。

正常时:
  - 删除陈旧 dlt_run_alert.txt
  - 写 dlt_watchdog_status.txt (首行 OK + 时间戳|说明)

始终 exit 0 (看门狗自身失败不应让排程任务报错)。

用法
----
  python dlt_watchdog_win.py            # 真实检查; 异常则写告警文件(默认不弹窗)
  python dlt_watchdog_win.py --toast   # 额外弹 Windows 原生提示(仅交互会话有意义)
  python dlt_watchdog_win.py --dry     # 只评估并打印, 不写告警/不弹窗(用于验证检测逻辑)
"""
import sys
import os
import io
import json
import glob
import subprocess
import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# 是否弹 Windows 原生提示。默认 False: 后台(SYSTEM)运行时不弹窗, 只写告警文件。
# 仅当显式传 --toast 才弹(交互会话手动跑时有用)。
TOAST = "--toast" in sys.argv[1:]

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
# 顶层目录(lib/ 的父级): Root 部署下是工程根, SKILL 包下是 scripts/。
# dlt_run_v8.bat 用 `cd /d "%~dp0"` 在**顶层**写日志/告警, 用户与 22 项护栏也在顶层读。
# 路径修正(2026-08-07): 旧代码把告警/状态写进 lib/, 导致
#   (1) bat 的 `if exist dlt_run_alert.txt del` 只清顶层 → lib/ 内陈旧告警**永不清除**(永久假警报);
#   (2) 用户与护栏在顶层读到的状态与看门狗实写的 lib/ 版本**账实不符**;
#   (3) 读排程日志恒落空 → "开跑即被杀"检测静默失效。
SCRIPTS_DIR = os.path.dirname(WORK_DIR)
TASK_NAME = "DLT_V8_Smart"
ALERT_FILE = os.path.join(SCRIPTS_DIR, "dlt_run_alert.txt")
STATUS_FILE = os.path.join(SCRIPTS_DIR, "dlt_watchdog_status.txt")
ALERTS_LOG = os.path.join(SCRIPTS_DIR, "dlt_watchdog_alerts.log")


def _pick_runtime_file(name):
    """在顶层(优先)与 lib/ 两处定位 bat 写出的运行态文件; 都存在取 mtime 最新, 都无返回 None。"""
    found = [p for p in (os.path.join(SCRIPTS_DIR, name), os.path.join(WORK_DIR, name))
             if os.path.exists(p)]
    return max(found, key=os.path.getmtime) if found else None

RESULT_MEANING = {
    0: "成功", 267008: "就绪", 267009: "正在运行", 267010: "已禁用",
    267011: "从未运行", 267012: "无更多运行", 267013: "未计划",
    267014: "任务被中止(SCHED_S_TASK_TERMINATED)", 267015: "无有效触发器",
}


def _now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def evaluate():
    """返回 (problems:list[str], notes:list[str], reachable:bool)。"""
    problems, notes = [], []
    reachable = False

    # (A) 上次结果码
    try:
        r = subprocess.run(
            ["schtasks", "/query", "/tn", TASK_NAME, "/fo", "list", "/v"],
            capture_output=True, timeout=30,
        )
        out = (r.stdout or b"").decode("gbk", errors="replace")
        if r.returncode == 0 and (TASK_NAME in out or "任务名" in out):
            reachable = True
            last_res, last_run = None, ""
            for line in out.splitlines():
                if "上次结果" in line or "Last Result" in line:
                    try:
                        last_res = int(line.split(":", 1)[-1].strip())
                    except Exception:
                        pass
                elif "上次运行时间" in line or "Last Run Time" in line:
                    last_run = line.split(":", 1)[-1].strip()
            if last_res is None:
                notes.append("未能解析『上次结果』字段")
            elif last_res == 0:
                notes.append(f"上次结果=0 成功 (于 {last_run})")
            elif last_res == 267011:
                notes.append("上次结果=267011 从未运行(新建任务尚未到点, 非故障)")
            else:
                problems.append(
                    f"上次排程运行未成功: 结果码 {last_res} "
                    f"({RESULT_MEANING.get(last_res, '未知')}), 时间 {last_run}"
                )
    except Exception as e:
        notes.append(f"schtasks 不可达({type(e).__name__}), 跳过运行结果校验")

    # (B) 反模式设置
    if reachable:
        try:
            rx = subprocess.run(
                ["schtasks", "/query", "/tn", TASK_NAME, "/xml"],
                capture_output=True, timeout=30,
            )
            raw = rx.stdout or b""
            xml = raw.decode("utf-16", errors="replace") if raw[:2] in (b"\xff\xfe", b"\xfe\xff") \
                else raw.decode("gbk", errors="replace")
            anti = []
            if "<DisallowStartIfOnBatteries>true" in xml:
                anti.append("DisallowStartIfOnBatteries=true(电池供电时根本不启动)")
            if "<StopIfGoingOnBatteries>true" in xml:
                anti.append("StopIfGoingOnBatteries=true(跑到一半切电池即被杀)")
            if "<StopOnIdleEnd>true" in xml:
                anti.append("StopOnIdleEnd=true(用户一动鼠标/空闲结束即被杀)")
            if anti:
                problems.append(
                    "排程存在会主动杀任务的反模式: " + "; ".join(anti)
                    + " -> 以管理员运行 一键修复排程.bat 修复"
                )
            else:
                notes.append("排程 Settings 无杀任务反模式")
        except Exception as e:
            notes.append(f"读取排程 XML 失败: {type(e).__name__}")

    # (C) 上次排程日志"开跑即中断"特征
    # 日志由 bat 写在顶层, 须双路径查找(旧代码只查 lib/ → 恒落空, 本项静默失效)。
    slog = _pick_runtime_file("dlt_scheduler_run.log")
    if slog:
        try:
            txt = open(slog, encoding="utf-8", errors="replace").read()
            lines = [l for l in txt.splitlines() if l.strip()]
            tail = "\n".join(lines[-3:])
            aborted = ("^C" in tail) or ("KeyboardInterrupt" in txt) or ("终止批处理操作" in txt)
            if aborted:
                problems.append(f"上次排程日志呈中断特征(尾部含 ^C/中断标记), 仅 {len(lines)} 行, 流水线未跑完")
            elif len(lines) < 8:
                problems.append(f"上次排程日志仅 {len(lines)} 行, 疑似开跑即退出(正常完整运行应有数十行)")
            else:
                notes.append(f"上次排程日志 {len(lines)} 行, 无中断特征")
        except Exception as e:
            notes.append(f"读取排程日志失败: {type(e).__name__}")
    else:
        notes.append("无 dlt_scheduler_run.log(尚未由排程真实驱动过)")

    # (D) 未处理告警
    if os.path.exists(ALERT_FILE):
        try:
            # 产物在 lib/(最新期) 与顶层(历史副本) 都可能存在, 两层都 glob 取全局最新,
            # 否则"告警是否比产物新"的基准会偏小 → 误判为未处理告警。
            reports = []
            for _d in (WORK_DIR, SCRIPTS_DIR):
                reports += glob.glob(os.path.join(_d, "*增强版*.html"))
                reports += glob.glob(os.path.join(_d, "dlt_prediction_*_v8.json"))
            newest = max((os.path.getmtime(p) for p in reports), default=0)
            if os.path.getmtime(ALERT_FILE) > newest:
                problems.append("dlt_run_alert.txt 比最新产物还新 -> 存在未处理的排程失败告警")
            else:
                notes.append("告警文件早于最新产物(历史遗留, 已被新一次成功运行覆盖)")
        except Exception as e:
            notes.append(f"告警文件比对失败: {type(e).__name__}")

    # (E) 模块自完整性守卫: 关键文件被改坏/篡改/损坏 -> 自动发现
    # 基线首次运行自动生成(dlt_integrity_manifest.json); 之后哈希比对。
    try:
        if os.path.basename(WORK_DIR) == "lib":
            sys.path.insert(0, WORK_DIR)
        import dlt_self_integrity as SI
        si = SI.check_self_integrity()
        if si.get("initialized"):
            notes.append(f"自完整性: {si['note']}")
        elif not si["ok"]:
            bad = []
            if si["tampered"]:
                bad.append(f"哈希变化={si['tampered']}")
            if si["missing"]:
                bad.append(f"缺失={si['missing']}")
            problems.append("模块自完整性异常 -> " + "; ".join(bad)
                            + " (疑似被改坏/篡改/损坏, 需从发布副本重建)")
        else:
            notes.append("自完整性: 关键文件哈希一致(38个)")
    except Exception as e:
        notes.append(f"自完整性检查失败: {type(e).__name__}")

    # (F) 数据真实性校验(非致命, 两层):
    #   1) 零网络比对: 实时主源最新一期 vs 本地已验证历史(同期号码不同 -> 篡改信号)
    #   2) 尽力跨源: 主源 vs 官方 cwl / 500, 同一期号号码不同 -> 篡改信号
    try:
        import importlib
        hi = importlib.import_module("dlt_huiniao_api")
        live = hi.fetch_latest_huiniao(limit=3)
        if not live:
            notes.append("数据真实性: 主源取数失败, 跳过比对(非致命)")
        else:
            latest = live[-1]
            # 1) 零网络: 本地历史中同期的记录(本地历史已手工比对过外部权威源)
            hist = None
            for _p in (os.path.join(SCRIPTS_DIR, "dlt_history.json"),
                       os.path.join(WORK_DIR, "dlt_history.json")):
                if os.path.exists(_p):
                    try:
                        hist = json.load(open(_p, encoding="utf-8"))
                        break
                    except Exception:
                        hist = None
            if hist:
                rec = next((x for x in hist if str(x["period"]) == str(latest["period"])), None)
                if rec and (rec["front"] != latest["front"] or rec["back"] != latest["back"]):
                    problems.append(
                        f"数据真实性告警: 实时主源第{latest['period']}期与本地已验证历史号码不一致 "
                        f"(实时 {latest['front']}+{latest['back']} vs 本地 {rec['front']}+{rec['back']}) "
                        f"-> 疑似主源被篡改, 需人工核查数据源"
                    )
                else:
                    notes.append(f"数据真实性: 实时主源第{latest['period']}期与本地历史一致 ✅")
            else:
                notes.append("数据真实性: 无本地历史可比(首次)")
            # 2) 尽力跨源(官方, 非致命): 仅当期号相同且号码不同才告警
            au = importlib.import_module("dlt_auto")
            for srcname, fn in (("cwl", au._fetch_from_cwl), ("500", au._fetch_from_500)):
                try:
                    ext = fn()
                except Exception:
                    continue
                if not ext:
                    continue
                ep = ext[-1]
                if ep["period"] == latest["period"]:
                    if ep["front"] != latest["front"] or ep["back"] != latest["back"]:
                        problems.append(
                            f"数据真实性告警: 主源与{srcname}第{latest['period']}期号码不一致 "
                            f"-> 疑似数据被篡改"
                        )
                    else:
                        notes.append(f"数据真实性: 主源与{srcname}第{latest['period']}期一致 ✅")
                    break
    except Exception as e:
        notes.append(f"数据真实性比对失败: {type(e).__name__} (非致命)")

    return problems, notes, reachable


def _ps_escape(s):
    return s.replace("'", "''")


def raise_os_alert(reasons, toast=TOAST):
    """持久化告警日志 + (可选)Windows 原生提示。不依赖 WorkBuddy/管理员。"""
    msg = "大乐透排程异常: " + reasons[0][:180]
    # 持久化告警日志(跨重启可见, 最可靠, 始终写)
    try:
        with open(ALERTS_LOG, "a", encoding="utf-8") as f:
            f.write(f"[{_now()}] ALERT\n")
            for r in reasons:
                f.write(f"  - {r}\n")
    except Exception:
        pass
    # Windows 原生提示: 默认不弹(后台 SYSTEM 会话无桌面); 仅 --toast 时弹。
    #   优先 BurntToast, 回退 msg *
    if not toast:
        return
    ps = (
        f"$m='{_ps_escape(msg)}';"
        "try{"
        "if(Get-Module -ListAvailable BurntToast){"
        "Import-Module BurntToast;New-BurntToastNotification -Text '大乐透排程告警',$m}"
        "else{msg * $m}"
        "}catch{msg * $m}"
    )
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30,
        )
    except Exception:
        pass


def write_status(kind, line):
    try:
        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            f.write(f"{kind}\n{_now()} | {line}\n")
    except Exception:
        pass


def main():
    dry = "--dry" in sys.argv[1:]
    problems, notes, reachable = evaluate()

    print("=" * 64)
    print("  大乐透系统 · 独立看门狗 (Standalone Watchdog)")
    print(f"  时间: {_now()}")
    if dry:
        print("  [DRY-RUN] 只评估并打印, 不写告警/不弹窗")
    print("=" * 64)
    for n in notes:
        print(f"  · {n}")
    for p in problems:
        print(f"  ❌ {p}")

    if problems:
        print(f"\n  ⚠️ 发现问题 {len(problems)} 项, 触发告警")
        if dry:
            print("  (dry) 未写 dlt_run_alert.txt / 未弹窗")
            write_status("ALERT", "[DRY] " + "; ".join(problems))
        else:
            # 写告警文件(供 WorkBuddy 看门狗 + 体检第22项复用)
            try:
                with open(ALERT_FILE, "w", encoding="utf-8") as f:
                    f.write(f"ALERT\n{_now()} | 大乐透排程异常:\n")
                    for p in problems:
                        f.write(f"  - {p}\n")
            except Exception:
                pass
            write_status("ALERT", "; ".join(problems))
            raise_os_alert(problems)
        print("=" * 64)
        print("  看门狗判定: 异常(已告警), 但看门狗自身 exit 0")
        print("=" * 64)
        return 0

    # 正常
    if os.path.exists(ALERT_FILE):
        try:
            os.remove(ALERT_FILE)
        except Exception:
            pass
    if not reachable and not problems:
        print("\n  ⚠️ schtasks 不可达(非 Windows 部署), 仅基于本地日志/告警文件判断")
    else:
        print("\n  ✅ 排程运行态正常 (LastTaskResult=0, 无中断/无未处理告警)")
    if not dry:
        write_status("OK", "排程运行态正常 (LastTaskResult=0, 无中断/无未处理告警)")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
