# -*- coding: utf-8 -*-
"""
大乐透智能预测系统 — 主控脚本
=====================================

一个命令完成全部流程:
  python dlt_smart.py

智能特性:
  1. 自动检测开奖日 (周一/三/六)
  2. 多源数据下载 (huiniao主→体彩网→500.com备)
  3. 数据新鲜度校验 + 异常检测
  4. 自动验证上期预测 vs 实际开奖
  5. 性能追踪 (历史命中率统计)
  6. 运行V8基础预测 (dlt_auto.py)
  7. 运行V8.5增强 (ML模型+冷热图+专家汇总)
  8. 三方交叉验证 (52项检查)
  9. 生成统一摘要

用法:
  python dlt_smart.py            # 完整运行 (开奖日自动检测)
  python dlt_smart.py --force    # 强制运行 (非开奖日也执行)
  python dlt_smart.py --verify-only  # 仅验证上期结果
"""
import sys
import os
import json
import subprocess
from datetime import datetime, timedelta
from dlt_period import next_period as next_period_func  # 统一期号计算

# Python路径: 使用当前解释器本身, 杜绝"换机/重装即崩" (不再写死绝对路径)
PYTHON = sys.executable
WORK_DIR = os.path.dirname(os.path.abspath(__file__))


def is_draw_day():
    """检测今天是否是开奖日 (周一=0, 三=2, 六=5)"""
    today = datetime.now().weekday()
    return today in [0, 2, 5]


def get_next_draw_info(draws):
    """获取下次开奖信息
    
    Returns:
        dict: {next_period, days_until_draw, is_draw_day}
    """
    if not draws:
        return None
    
    latest = draws[-1]
    latest_period = int(latest['period'])
    latest_date = latest.get('date', '')
    
    # 计算下期期号
    next_period = next_period_func(latest_period, latest_date)
    
    # 计算下次开奖日
    today = datetime.now()
    today_weekday = today.weekday()
    draw_days = [0, 2, 5]  # 周一, 周三, 周六
    
    days_until = 7
    for d in draw_days:
        diff = (d - today_weekday) % 7
        if diff == 0:
            days_until = 0  # 今天就是开奖日
            break
        elif diff < days_until:
            days_until = diff
    
    next_draw_date = today + timedelta(days=days_until)
    
    return {
        'next_period': next_period,
        'latest_period': latest['period'],
        'latest_date': latest_date,
        'is_draw_day': days_until == 0,
        'days_until_draw': days_until,
        'next_draw_date': next_draw_date.strftime('%Y-%m-%d'),
        'today': today.strftime('%Y-%m-%d %H:%M'),
    }


def check_data_freshness(draws):
    """检查数据新鲜度
    
    Returns:
        dict: {is_fresh, days_since_last_draw, warning}
    """
    if not draws:
        return {'is_fresh': False, 'warning': '无数据'}
    
    latest = draws[-1]
    latest_date = latest.get('date', '')
    
    if not latest_date:
        return {'is_fresh': True, 'warning': '无日期信息，跳过新鲜度检查', 'days_since': -1}
    
    try:
        latest_dt = datetime.strptime(latest_date[:10], '%Y-%m-%d')
        days_since = (datetime.now() - latest_dt).days
        
        if days_since > 7:
            return {'is_fresh': False, 'warning': f'数据过期: 最近一期是{days_since}天前', 'days_since': days_since}
        elif days_since > 4:
            return {'is_fresh': True, 'warning': f'数据稍旧: {days_since}天前', 'days_since': days_since}
        else:
            return {'is_fresh': True, 'warning': None, 'days_since': days_since}
    except:
        return {'is_fresh': True, 'warning': '日期解析失败，跳过新鲜度检查', 'days_since': -1}


# Windows 满载后偶发『进程启动失败/资源枯竭』(典型 0xC0000142 = 3221225794),
# 表现为特定返回码; 属间歇性环境现象(非逻辑 bug, 代码本身正确), 重试一次通常即可通过。
# 仅对这类码自动重试, 真正的逻辑失败(返回码 1 等)不重试。
_RESOURCE_EXHAUST_CODES = frozenset({3221225794, -1073741502, 3221225786, -1073741510})
_MAX_RETRY = 2


def run_script(script_name, description, timeout=300):
    """运行Python脚本（带资源枯竭自动重试）。

    Returns:
        (success, output)
    """
    last_out = ''
    for attempt in range(1, _MAX_RETRY + 1):
        ok, out, rc = _run_script_once(script_name, description, timeout, attempt)
        last_out = out
        if ok:
            return True, out
        # 资源枯竭类(间歇性) -> 延时避让后重试
        if rc in _RESOURCE_EXHAUST_CODES and attempt < _MAX_RETRY:
            import time
            print(f"  ⚠ {description} 疑似资源枯竭(返回码={rc}), {attempt}秒后自动重试 ...")
            time.sleep(attempt)
            continue
        return False, out
    return False, last_out


def _run_script_once(script_name, description, timeout, attempt):
    """单次执行, 返回 (ok, output, returncode)。"""
    tag = f" (重试 {attempt})" if attempt > 1 else ""
    print(f"\n{'=' * 70}")
    print(f"  >> {description}{tag}")
    print(f"{'=' * 70}")

    cmd = [PYTHON, script_name]
    try:
        result = subprocess.run(
            cmd,
            cwd=WORK_DIR,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8',
            errors='replace'
        )

        # 打印输出
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"  [STDERR] {result.stderr}")

        if result.returncode == 0:
            print(f"  >> {description}{tag} -- 成功")
            return True, result.stdout, result.returncode
        else:
            print(f"  >> {description}{tag} -- 失败 (返回码={result.returncode})")
            return False, result.stdout + result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        print(f"  >> {description}{tag} -- 超时({timeout}秒)")
        return False, 'TIMEOUT', None
    except Exception as e:
        print(f"  >> {description}{tag} -- 异常: {e}")
        return False, str(e), None


def archive_expert_picks(target_period):
    """将当期专家推荐带期号存档，为未来真实 ECI 回测积累历史数据。

    读取 dlt_expert_picks.json 中的 experts 数组，追加带 period 字段的
    记录到 dlt_expert_history.json。下一期起即可对"上一期真实专家推荐"
    做回测，N 期后形成完整的历史 ECI 回测能力。
    """
    print("\n" + "=" * 70)
    print("【Phase 5.5: 历史专家推荐存档】")
    print("=" * 70)
    if not target_period:
        print("  ⚠ 无目标期号，跳过存档")
        return

    try:
        with open('dlt_expert_picks.json', 'r', encoding='utf-8') as f:
            picks = json.load(f)
    except Exception as e:
        print(f"  ⚠ 读取专家推荐失败: {e}")
        return

    experts = picks.get('experts', [])
    if not experts:
        print("  ⚠ 无专家推荐数据，跳过存档")
        return

    # 读取已有历史
    history = []
    try:
        with open('dlt_expert_history.json', 'r', encoding='utf-8') as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    except Exception as e:
        print(f"  ⚠ 读取历史失败，重建: {e}")
        history = []

    # 避免重复写入同一期
    if any(h.get('period') == target_period for h in history):
        print(f"  ✓ 期号 {target_period} 已存档，跳过")
        return

    record = {
        'period': target_period,
        'experts': experts,
        'timestamp': datetime.now().isoformat(),
    }
    history.append(record)
    # 按期号排序
    history.sort(key=lambda h: h.get('period', ''))

    try:
        with open('dlt_expert_history.json', 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        print(f"  ✓ 已存档 {target_period} 期专家推荐 ({len(experts)}位)")
        print(f"  ✓ 历史存档累计: {len(history)} 期")
        print(f"  ✓ 说明: 下一期起即可对上一期真实专家推荐做 ECI 回测")
    except Exception as e:
        print(f"  ⚠ 存档失败: {e}")


def _detect_real_desktop():
    """SYSTEM 排程语境下 ~ 指向 systemprofile 虚拟桌面, 报告会落到用户看不到的位置。
    动态扫描系统用户目录定位真实交互用户桌面, 不写死用户名(换机也能正确投递)。"""
    users_root = os.path.expandvars(r"%SystemDrive%\Users")
    if not os.path.isdir(users_root):
        return None
    skip = ("public", "default", "default user", "defaultuser0", "all users",
            "systemprofile", "network service", "local service")
    try:
        for name in os.listdir(users_root):
            nl = name.lower()
            if nl in skip or nl.startswith("systemprofile"):
                continue
            d = os.path.join(users_root, name, "Desktop")
            if os.path.isdir(d):
                return d
    except Exception:
        pass
    return None


def _resolve_desktop():
    """解析真实用户桌面目录(中英文系统兼容, 兜底到用户主目录)。
    SYSTEM 语境动态定位真实交互用户桌面, 不再写死本机用户名。"""
    real = _detect_real_desktop()
    for c in (real,
              os.path.expanduser("~/Desktop"),
              os.path.expanduser("~/桌面"),
              os.path.expanduser("~/Documents"),
              os.path.expanduser("~")):
        if c and os.path.isdir(c):
            return c
    return None


def ensure_report_delivery():
    """预测+增强跑完后：保证增强版(优先)报告一定落到用户真实桌面 + 打印清晰绝对路径。

    根治"调出技能/排程运行后看不到报告"的反复问题：
      - 桌面文件是保底：用户总能双击用浏览器打开, 不依赖预览面板。
      - 增强版缺失时自动回退补跑 dlt_enhance.py, 确保'完整报告'一定产出。
      - 打印 REPORT_DESKTOP_PATH: (增强版绝对路径), 供调用模型 present_files 渲染预览面板。

    四体协同: 本函数与 SKILL 副本 run_dlt.py 的 _ensure_report_delivery 同源行为, 使
    根/Windows/自动化 三体与 SKILL 第四体在"报告投递"上完全一致 —— 这是此前唯一不对等
    的缺口(根链路只被动依赖 dlt_enhance.py 的桌面拷贝, 无补跑保底)。现已统一。
    """
    import glob
    import shutil
    pats = ("大乐透*V85_增强版.html", "大乐透*预测报告_V8_全面修复.html")
    cands = []
    for pat in pats:
        cands += glob.glob(os.path.join(WORK_DIR, pat))
    cands = sorted(set(cands), key=os.path.getmtime, reverse=True)
    enhanced = next((p for p in cands if "V85_增强版" in os.path.basename(p)), None)
    base = next((p for p in cands if "V85_增强版" not in os.path.basename(p)), None)

    # 增强版缺失 -> 补跑 dlt_enhance.py (幂等), 再重新定位
    if not enhanced and base:
        print("  ⚠ 未检测到增强版报告, 尝试补跑 dlt_enhance.py ...")
        try:
            subprocess.run([PYTHON, "dlt_enhance.py"], cwd=WORK_DIR,
                           capture_output=True, text=True, timeout=180,
                           encoding='utf-8', errors='replace')
        except Exception as e:
            print(f"  ⚠ 补跑增强失败(非致命): {e}")
        cands = []
        for pat in pats:
            cands += glob.glob(os.path.join(WORK_DIR, pat))
        cands = sorted(set(cands), key=os.path.getmtime, reverse=True)
        enhanced = next((p for p in cands if "V85_增强版" in os.path.basename(p)), None)
        base = next((p for p in cands if "V85_增强版" not in os.path.basename(p)), None)

    if not cands:
        print("  ⚠ 未找到任何预测报告, 无法交付报告文件")
        return

    desktop = _resolve_desktop()
    enhanced_desktop = base_desktop = None
    if desktop:
        for src, holder in ((enhanced, "enhanced_desktop"), (base, "base_desktop")):
            if not src:
                continue
            try:
                dest = os.path.join(desktop, os.path.basename(src))
                shutil.copy2(src, dest)
                if holder == "enhanced_desktop":
                    enhanced_desktop = os.path.abspath(dest)
                else:
                    base_desktop = os.path.abspath(dest)
            except Exception as e:
                print(f"  ⚠ 复制 {os.path.basename(src)} 到桌面失败: {e}")
    else:
        print("  ⚠ 未找到桌面目录, 跳过桌面复制(报告仍在项目目录)")

    print("=" * 64)
    print("REPORT_DESKTOP_PATH: " + (enhanced_desktop or base_desktop or ""))
    print("REPORT_ABS_PATH: " + os.path.abspath(enhanced or base))
    if base_desktop and base_desktop != enhanced_desktop:
        print("REPORT_BASE_DESKTOP_PATH: " + base_desktop)
    # 四体一致: 写入确定性文件 REPORT_PATH.txt (与 run_dlt.py 同源行为), 供调用模型
    # 直接读取绝对路径并 present_files, 无需从 stdout 解析带中文期号的路径。
    try:
        chosen_abs = os.path.abspath(enhanced or base or "")
        with open(os.path.join(WORK_DIR, "REPORT_PATH.txt"), "w", encoding="utf-8") as f:
            f.write(chosen_abs)
        print("REPORT_PATH_FILE: " + os.path.join(WORK_DIR, "REPORT_PATH.txt"))
    except Exception:
        pass
    # 四体一致: 把刚生成的最新一期产物镜像到其它安装副本, 根治 item19 护栏漂移
    # 防御性: 镜像属"锦上添花", 任何异常都不得让已成功的预测投递失败(曾因 glob 未导入
    # 抛 NameError 把整条流水线拖成退出码1)。失败只告警, 由 item19 护栏兜底暴露。
    try:
        sync_products_to_peers(WORK_DIR)
    except Exception as _e:
        print(f"  ⚠ 产物自动镜像失败(不影响本次预测投递): {type(_e).__name__}: {_e}")
    print("=" * 64)


def _iter_real_user_profiles():
    """生成真实交互用户 profile 根目录(跳过 Public/Default/systemprofile 等系统伪账户)。"""
    root = os.path.expandvars(r"%SystemDrive%\Users")
    if os.path.isdir(root):
        skip = ("public", "default", "default user", "defaultuser0", "all users",
                "systemprofile", "network service", "local service")
        try:
            for name in os.listdir(root):
                nl = name.lower()
                if nl in skip or nl.startswith("systemprofile"):
                    continue
                d = os.path.join(root, name)
                if os.path.isdir(d):
                    yield d
        except Exception:
            pass


def _candidate_peer_libs(work_dir):
    """返回『另一安装』的 lib/ 候选(动态, 不写死用户名/时间戳目录)。
    - SKILL 副本: <profile>/.workbuddy/skills/dlt-probability-analyzer/scripts/lib
    - Root 体    : <profile>/WorkBuddy/<含 lib/dlt_smart.py 的目录>/lib (扫描定位, 时间戳目录不写死)
    """
    cands = []
    for p in _iter_real_user_profiles():
        cands.append(os.path.join(p, ".workbuddy", "skills", "dlt-probability-analyzer", "scripts", "lib"))
        wb = os.path.join(p, "WorkBuddy")
        if os.path.isdir(wb):
            try:
                for sub in os.listdir(wb):
                    rp = os.path.join(wb, sub)
                    if os.path.isdir(rp) and os.path.exists(os.path.join(rp, "lib", "dlt_smart.py")):
                        cands.append(os.path.join(rp, "lib"))
            except Exception:
                pass
    return cands


def sync_products_to_peers(work_dir):
    """四体一致性 · 产物自动镜像 (根治 item19 护栏漂移)。

    预测产物(预测JSON + 基础/增强HTML)与模块一同落在各安装的 lib/ 子目录:
      根目录  : <Root>/lib/
      SKILL   : <SKILL>/scripts/lib/   (run_dlt.py 设 cwd=lib; item19 也优先查 scripts/lib)
    本函数把"当前安装" lib/ 的最新一期产物镜像到"另一个安装"的 lib/, 使四体产物
    永远一致, 护栏恒绿。双向: 根运行→镜像到 SKILL; SKILL 运行→镜像到根。

    注意: 仅同步"产物", 不同步代码(.py 由 build_dist 单向 SYNC)与离线数据(item20 校验)。
    防御性: 镜像属"锦上添花", 任何异常都不得让已成功的预测投递失败。
    """
    import shutil as _sh
    import re as _re
    import glob as _glob          # 注意: 模块顶层未导入 glob(仅第247行函数内局部导入), 必须本地导入
    # 两个已知安装各自的 lib/ 子目录(产物与模块同在此处)。归一化去重, 排除自身安装。
    # 动态扫描真实用户 profile 定位(不写死用户名/时间戳目录, 跨机可移植)。
    _self = os.path.normcase(os.path.realpath(work_dir))
    candidates = _candidate_peer_libs(work_dir)
    peers = []
    for c in candidates:
        if not os.path.isdir(c):
            continue
        key = os.path.normcase(os.path.realpath(c))
        if key == _self or key in {os.path.normcase(os.path.realpath(p)) for p in peers}:
            continue
        peers.append(c)
    if not peers:
        return
    preds = sorted(_glob.glob(os.path.join(work_dir, "dlt_prediction_*_v8.json")),
                   key=os.path.getmtime)
    if not preds:
        return
    latest = preds[-1]
    m = _re.search(r'dlt_prediction_(\d+)_v8\.json', os.path.basename(latest))
    period = m.group(1) if m else None
    files = [latest]
    if period:
        for pat in (f"大乐透{period}*预测报告_V8_全面修复.html",
                    f"大乐透{period}*_V85_增强版.html"):
            files += _glob.glob(os.path.join(work_dir, pat))
    files = list(dict.fromkeys(files))  # 去重保持顺序
    for peer in peers:
        ok = 0
        for src in files:
            try:
                _sh.copy2(src, os.path.join(peer, os.path.basename(src)))
                ok += 1
            except Exception as e:
                print(f"  ⚠ 镜像产物到 {peer} 失败 {os.path.basename(src)}: {e}")
        if ok:
            print(f"  ✅ 已自动镜像 {ok} 个最新期产物 -> {peer} (四体产物一致)")


def generate_smart_summary(draws, draw_info, freshness, verify_result):
    """生成智能摘要"""
    print("\n" + "=" * 70)
    print("【智能分析摘要】")
    print("=" * 70)
    
    # 数据状态
    print(f"\n  数据状态:")
    print(f"    历史期数: {len(draws)}")
    print(f"    最新期号: {draw_info['latest_period']} ({draw_info['latest_date']})")
    print(f"    目标期号: {draw_info['next_period']}")
    
    # 新鲜度
    if freshness['warning']:
        print(f"    数据新鲜度: {freshness['warning']}")
    else:
        print(f"    数据新鲜度: 正常 ({freshness['days_since']}天前)")
    
    # 开奖日信息
    if draw_info['is_draw_day']:
        print(f"\n  开奖日: 今天是开奖日!")
        print(f"    投注窗口: 现在 - 21:00")
        print(f"    开奖时间: 21:00")
    else:
        print(f"\n  开奖日: 距下次开奖还有{draw_info['days_until_draw']}天")
        print(f"    下次开奖: {draw_info['next_draw_date']}")
    
    # 验证结果
    if verify_result and verify_result.get('results'):
        print(f"\n  上期验证:")
        print(f"    验证期号: {verify_result['period']}")
        best = max(verify_result['results'], key=lambda x: x.get('total_hits', 0))
        print(f"    最佳表现: {best['name']} 命中{best['total_hits']}球 ({best['prize']})")
    elif verify_result and verify_result.get('skipped'):
        print(f"\n  上期验证: 跳过 ({verify_result.get('reason', 'no_prediction_files')})")
    else:
        print(f"\n  上期验证: 无待验证预测")
    
    # 性能追踪
    try:
        from dlt_result_verify import print_performance_summary
        print_performance_summary()
    except:
        pass
    
    # 投注建议
    print(f"\n  投注建议:")
    if draw_info['is_draw_day']:
        now = datetime.now()
        if now.hour < 21:
            print(f"    今天开奖! 请在21:00前完成投注")
            print(f"    推荐: 5组单式 + 标准胆拖 = 23注 = 46元(基本)/69元(含追加)")
        else:
            print(f"    今日开奖已结束，请等待结果")
    else:
        print(f"    非开奖日，可提前准备选号")
    
    # 文件位置
    print(f"\n  输出文件:")
    print(f"    V8基础报告: 大乐透*V8_全面修复.html")
    print(f"    V8.5增强报告: 大乐透*V85_增强版.html")
    print(f"    预测JSON: dlt_prediction_{draw_info['next_period']}_v8.json")
    print(f"    性能追踪: dlt_performance.json")


def main():
    import io
    # 锚定工作目录到本模块所在目录(lib/), 使所有相对路径文件读写与调用方 cwd 解耦。
    # 排程 bat 以 cd %~dp0 (Root) 启动本脚本, cwd=Root, 但 dlt_history.json 等数据在 lib/;
    # 不锚定会导致数据加载失败→draw_info=None→摘要生成 TypeError 崩溃(20:10 排程即此因)。
    # 仅 main() 运行期生效, 被 import 时不触发。
    os.chdir(WORK_DIR)
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # 四体一致性: 运行前先把最新产物镜像到其它安装副本, 确保 Phase 0.5 的
    # item19「根↔SKILL产物同步」护栏在"自然滚期"导致的期号漂移下也能通过。
    # 否则 Root 已滚到新一期(如26088)而 SKILL 副本仍是上期(26087),
    # item19 会误判为"未同步"并阻断本次预测(鸡生蛋问题: 不预测就没产物可同步)。
    # 防御性: 任何异常都不得阻断主流程(镜像只是锦上添花, 由 item19 兜底暴露)。
    try:
        sync_products_to_peers(WORK_DIR)
    except Exception as _e:
        print(f"  ⚠ 运行前产物镜像失败(不影响主流程): {type(_e).__name__}: {_e}")

    force = '--force' in sys.argv
    verify_only = '--verify-only' in sys.argv
    
    print("=" * 70)
    print(f"  大乐透智能预测系统 V8.5")
    print(f"  运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  工作目录: {WORK_DIR}")
    print("=" * 70)
    
    # Phase 0: 开奖日检测
    draw_today = is_draw_day()
    print(f"\n  开奖日检测: {'今天是开奖日' if draw_today else '今天不是开奖日'}")

    # Phase 0.5: 永久回归自检 (系统自身健康, 不通过则拒绝交付)
    print("\n" + "=" * 70)
    print("【Phase 0.5: 一键永久自检 / 回归护栏】")
    print("=" * 70)
    health_ok = False
    try:
        # 护栏含 22 项检查、15+ 子进程调用; 普通会话 ~155s,
        # SYSTEM 语境下 Python 冷启动+CPU调度差异可膨胀至 ~600s。
        # 排程任务自身 ExecutionTimeLimit=PT2H 足够容纳。
        r = subprocess.run([PYTHON, "dlt_healthcheck_all.py"],
                           cwd=WORK_DIR, capture_output=True, text=True,
                           timeout=900, encoding='utf-8', errors='replace')
        print(r.stdout[-2000:] if r.stdout else "")
        if r.stderr:
            print(f"  [STDERR] {r.stderr[-500:]}")
        health_ok = (r.returncode == 0)
    except Exception as e:
        print(f"  ⚠ 自检运行异常: {e}")
    if not health_ok:
        print("\n  ⛔ 永久自检未通过! 系统可能存在回归, 终止预测并报警。")
        print("  ⛔ 请勿交付未经自检的结果!")
        return

    # Phase 0.6: 专家推荐自动抓取 (非致命：专家仅为辅助参考，失败不阻断预测)
    print("\n" + "=" * 70)
    print("【Phase 0.6: 专家推荐自动抓取 (自动/非致命)】")
    print("=" * 70)
    expert_ok = True
    try:
        r = subprocess.run([PYTHON, "dlt_expert_scraper.py", "--auto"],
                           cwd=WORK_DIR, capture_output=True, text=True,
                           timeout=120, encoding='utf-8', errors='replace')
        print(r.stdout[-900:] if r.stdout else "  (无输出)")
        if r.stderr:
            print(f"  [STDERR] {r.stderr[-300:]}")
        expert_ok = (r.returncode == 0)
    except Exception as e:
        print(f"  ⚠ 专家抓取异常(非致命，专家仅为辅助): {e}")
        expert_ok = False

    # Phase 0.7: 专家战绩自算 + 随机基线对照 (非致命)
    # V8.9.8 新增: 每期开奖后用系统自身抓到的专家推荐 vs 实际开奖独立打分,
    # 同时生成机选基线, 杜绝采信平台注水战绩。不阻断预测。
    print("\n" + "=" * 70)
    print("【Phase 0.7: 专家战绩自算 / 随机基线对照 (非致命)】")
    print("=" * 70)
    tracker_ok = True
    try:
        r = subprocess.run([PYTHON, "dlt_expert_tracker.py"],
                           cwd=WORK_DIR, capture_output=True, text=True,
                           timeout=120, encoding='utf-8', errors='replace')
        print(r.stdout[-760:] if r.stdout else "  (无输出)")
    except Exception as e:
        print(f"  ⚠ 战绩自算异常(非致命): {e}")
        tracker_ok = False

    if not draw_today and not force and not verify_only:
        print("  非开奖日，跳过预测。使用 --force 强制运行。")
        print("  开奖日: 周一、周三、周六")
        return
    
    # 加载现有数据用于预检
    draws = []
    try:
        with open('dlt_history.json', 'r', encoding='utf-8') as f:
            draws = json.load(f)
        print(f"  现有数据: {len(draws)}期")
    except:
        print("  现有数据: 无 (将从网络下载)")
    
    draw_info = get_next_draw_info(draws) if draws else None
    
    if draw_info:
        print(f"  最新期号: {draw_info['latest_period']}")
        print(f"  目标期号: {draw_info['next_period']}")
    
    # 仅验证模式
    if verify_only:
        if draws:
            from dlt_result_verify import check_and_verify, print_performance_summary
            result = check_and_verify(draws)
            if result is None:
                print("\n  开奖数据不足, 无法验证。")
            elif result.get('skipped'):
                print(f"\n  无待验证预测 ({result.get('reason')})。")
            print_performance_summary()
        return
    
    # Phase 1: 上期预测验证
    print("\n" + "=" * 70)
    print("【Phase 1: 上期预测自动验证】")
    print("=" * 70)
    
    verify_result = None
    verify_ok = True  # 阶段是否无异常完成(成功后置判据, 不因病态"无文件可验"误判失败)
    if draws and len(draws) > 0:
        try:
            from dlt_result_verify import check_and_verify
            verify_result = check_and_verify(draws)
            if verify_result is None:
                print("  ⚠ 开奖数据不足, 跳过验证")
            elif verify_result.get('skipped'):
                _reason = verify_result.get('reason', 'no_prediction_files')
                if _reason == 'no_prediction_files':
                    print("  ℹ 上期预测验证: 未发现可验的上期预测文件(多为历史失败运行未产出, 非致命), 跳过")
                else:
                    print("  ℹ 上期预测验证: 最近期均已验证, 无待验证项")
            else:
                print("  ✓ 上期预测验证完成, 已更新性能追踪")
        except Exception as e:
            print(f"  ⚠ 验证模块异常: {e}")
            verify_ok = False
    else:
        verify_ok = False
    
    # Phase 2: V8基础预测 (含数据下载)
    success_v8, output_v8 = run_script('dlt_auto.py', 'V8基础预测 (数据下载→校验→穷举→选号→报告)', timeout=300)
    
    if not success_v8:
        print("\n  ✗ V8基础预测失败! 尝试使用 --skip-download 模式重试...")
        success_v8, output_v8 = run_script('dlt_auto.py', 'V8基础预测 (跳过下载)', timeout=300)
        if not success_v8:
            print("  ✗ V8基础预测再次失败，终止流程")
            return
    
    # 重新加载数据 (dlt_auto.py可能更新了)
    try:
        with open('dlt_history.json', 'r', encoding='utf-8') as f:
            draws = json.load(f)
    except:
        pass
    
    # 数据新鲜度检查
    freshness = check_data_freshness(draws)
    if not freshness['is_fresh']:
        print(f"\n  ⚠ 数据新鲜度警告: {freshness['warning']}")
    
    draw_info = get_next_draw_info(draws) if draws else draw_info
    
    # Phase 3: V8.5增强预测 (ML模型+冷热图+专家汇总)
    # V2.1.12 优化: 若 Phase2 的 dlt_auto.py 已补跑增强版(增强版报告已存在), 则跳过,
    # 避免与 dlt_auto 内部增强重复跑; 否则这里补跑兜底 —— 保证增强版一定产出。
    _tp = draw_info.get('next_period') if draw_info else None
    _enh_expected = f"大乐透{_tp}期预测报告_V8_全面修复_V85_增强版.html" if _tp else None
    # 2.1.20 修复: 增强版依赖基础版, 若比基础版旧则视为陈旧必须重算(兜底; 主逻辑在 dlt_auto)
    _base_html = f"大乐透{_tp}期预测报告_V8_全面修复.html" if _tp else None
    _base_mtime = os.path.getmtime(_base_html) if _base_html and os.path.exists(_base_html) else 0
    _enh_stale = bool(_enh_expected) and os.path.exists(_enh_expected) and os.path.getmtime(_enh_expected) < _base_mtime
    if _enh_expected and os.path.exists(_enh_expected) and not _enh_stale:
        print("  ℹ 增强版报告已由 Phase2(dlt_auto.py)产出且最新, Phase3 跳过重复补跑")
        success_v85, output_v85 = True, "skipped (already generated by dlt_auto)"
    else:
        success_v85, output_v85 = run_script('dlt_enhance.py', 'V8.5增强预测 (ML模型+冷热图+专家汇总)', timeout=180)

    if not success_v85:
        print("  ⚠ V8.5增强失败，但V8基础预测已完成")
    
    # Phase 4: 三方交叉验证
    success_verify, output_verify = run_script('dlt_cross_validate_v84_final.py', '三方交叉验证 (52项检查)', timeout=120)
    
    if not success_verify:
        print("  ⚠ 交叉验证发现问题，请检查输出")

    # Phase 6: 强化引擎 (样本外滚动回测 + 蒙特卡洛成本仿真 + 诚实闸门) — 非致命
    print("\n" + "=" * 70)
    print("【Phase 6: 强化引擎 / 科学严谨性自检 (非致命)】")
    print("=" * 70)
    success_power = True
    try:
        r = subprocess.run([PYTHON, "dlt_power_engine.py"],
                           cwd=WORK_DIR, capture_output=True, text=True,
                           timeout=200, encoding='utf-8', errors='replace')
        print(r.stdout[-1200:] if r.stdout else "(无输出)")
        if r.stderr:
            print(f"  [STDERR] {r.stderr[-300:]}")
        success_power = (r.returncode == 0)
    except Exception as e:
        print(f"  ⚠ 强化引擎异常(非致命): {e}")
        success_power = False

    # Phase 5: 智能摘要
    generate_smart_summary(draws, draw_info, freshness, verify_result)

    # Phase 5.5: 历史专家推荐存档 (为未来真实 ECI 回测积累数据)
    target_period = draw_info['next_period'] if draw_info else None
    archive_expert_picks(target_period)

    # Phase 7: ML 模型样本外自评 (量化"模型是否有用", 非致命)
    print("\n" + "=" * 70)
    print("【Phase 7: ML 模型样本外自评 (非致命)】")
    print("=" * 70)
    success_mlcheck = True
    try:
        r = subprocess.run([PYTHON, "dlt_ml_selfcheck.py"],
                           cwd=WORK_DIR, capture_output=True, text=True,
                           timeout=300, encoding='utf-8', errors='replace')
        print(r.stdout[-1000:] if r.stdout else "(无输出)")
        if r.stderr:
            print(f"  [STDERR] {r.stderr[-300:]}")
        success_mlcheck = (r.returncode == 0)
    except Exception as e:
        print(f"  ⚠ ML自评异常(非致命): {e}")
        success_mlcheck = False

    # Phase 8: 报告投递保底 (确保增强版报告落到真实用户桌面, 四体协同一致)
    # 放在所有预测阶段之后, 无论关键步骤是否通过都尽量交付报告(用户总想看到结果)
    ensure_report_delivery()

    # 最终状态
    print("\n" + "=" * 70)
    print("【全流程完成】")
    print("=" * 70)

    steps = [
        ("0. 开奖日检测", draw_today or force),
        ("0.5 永久自检/回归护栏", health_ok),
        ("0.6 专家自动抓取", expert_ok),
        ("0.7 专家战绩自算/追踪回填", tracker_ok),
        ("1. 上期预测验证", verify_ok),
        ("2. V8基础预测", success_v8),
        ("3. V8.5增强预测", success_v85),
        ("4. 三方交叉验证", success_verify),
        ("6. 强化引擎(严谨自检)", success_power),
        ("7. ML样本外自评", success_mlcheck),
        ("5. 智能摘要", True),
        ("5.5 专家存档", target_period is not None),
    ]
    
    for name, done in steps:
        print(f"  {'✅' if done else '❌'} {name}")

    success_count = sum(1 for _, d in steps if d)
    print(f"\n  智能化得分: {success_count}/{len(steps)}")

    # V8.9.8: 专家智慧总览(常驻名录 + 战绩自算状态), 诚实提示不提升中选可能
    try:
        from dlt_expert_roster import catalog_summary
        cs = catalog_summary()
        print(f"\n  🧠 专家智慧总览: 常驻名录 {cs['总计专家']} 位"
              f"(权威 {cs['权威']} / 野路子 {cs['野路子']}) + 官方数据源 {cs['官方数据源']} 个")
        acc = json.load(open('dlt_expert_accuracy.json', encoding='utf-8')) if os.path.exists('dlt_expert_accuracy.json') else {}
        recs = acc.get('records', [])
        if recs:
            last = recs[-1]
            print(f"     战绩自算: 已覆盖 {len(recs)} 期; 最新 {last['period']} 期"
                  f"随机基线前区均命中 {last['baseline']['front_hits']}"
                  f"(专家排名仅相对基线有意义, 不提升中选可能)")
        else:
            print(f"     战绩自算: 暂无(需先累积 dlt_expert_history.json 且对应期已开奖)")
    except Exception as e:
        print(f"\n  🧠 专家智慧总览: 读取失败(非致命): {e}")

    # 关键步骤校验: V8基础预测 与 三方交叉验证 必须同时通过, 否则结果不可信
    critical_ok = success_v8 and success_verify
    if not critical_ok:
        print(f"\n  ⛔ 关键步骤失败 (V8基础={success_v8}, 交叉验证={success_verify})")
        print(f"  ⛔ 本次输出未经完整验证, 请勿直接用于投注!")
    
    if draw_info and draw_info['is_draw_day']:
        print(f"\n  ⏰ 今天开奖! 投注窗口: 现在 - 21:00")
        if critical_ok:
            print(f"  📄 请查看报告: 大乐透*V85_增强版.html")
        else:
            print(f"  ⛔ 关键步骤失败, 本次报告不可信, 请勿据此投注")

    return critical_ok


if __name__ == '__main__':
    import sys
    try:
        ok = main()
    except KeyboardInterrupt:
        print("\n⚠️ 已手动中断。未生成报告，无需处理。")
        sys.exit(130)
    except Exception as e:
        # 顶层兜底：把任何意外变成友好提示，而非一串技术报错
        # 技术细节写入日志文件(供开发者排查)，不向普通用户展示原始异常
        import traceback as _tb
        _log = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dlt_error_log.txt")
        try:
            with open(_log, "a", encoding="utf-8") as _f:
                _f.write("\n%s\n%s\n" % ("=" * 40, _tb.format_exc()))
        except Exception:
            _log = "(日志写入失败，不影响本次提示)"
        print("=" * 64)
        print("⚠️ 预测流程意外中断，本次报告未能正常生成。")
        print("  这通常源于网络不通、数据文件缺失或运行环境差异，不是你操作有误。")
        print("  可尝试：① 重试一次；② 用 run_dlt.py --skip-download 离线跑；")
        print("          ③ 查看 references/faq.md 的「运行报错」章节。")
        print("  技术细节已自动记录到日志文件：")
        print("    %s" % _log)
        print("  如需进一步排查，可把这个文件发给开发者，无需自行解读。")
        print("=" * 64)
        sys.exit(1)
    # 关键: 关键步骤(v8基础预测 + 三方交叉验证)未通过时, 必须非零退出,
    # 否则 bat / 系统任务会把"带病交付"误判为成功, 导致静默错误。
    sys.exit(0 if ok else 1)
