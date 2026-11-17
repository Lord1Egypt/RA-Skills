# -*- coding: utf-8 -*-
"""
模块自完整性守卫 (dlt_self_integrity.py)  V8.9.7 新增 (看门狗加固)

目的: 弥补"三体一致性只靠手动比对"的缺口——一旦 lib 内模块或根目录关键文件
被意外改坏 / 被篡改 / 损坏，应能被自动发现并告警，而不是等排程跑挂才暴露。

机制:
  - 首次运行生成基线清单 (dlt_integrity_manifest.json, SHA256)。
  - 之后每次运行比对: 任何关键文件哈希变化 -> 判定 tamper/corruption -> 告警。
  - 关键文件 = lib/ 下全部 dlt_*.py(守卫自身除外) + 根目录 run_dlt.py / dlt_run_v8.bat
    / dlt_history.json(数据完整性基线, 篡改意味着历史被污染)。

用法:
  python dlt_self_integrity.py            # 检查(缺失清单则先初始化)
  python dlt_self_integrity.py --init      # 强制重建基线
看门狗 dlt_watchdog_win.py 每日运行时会调用 check_self_integrity()。
"""
import hashlib
import json
import os
import sys

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.dirname(WORK_DIR)
MANIFEST = os.path.join(WORK_DIR, "dlt_integrity_manifest.json")


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _targets():
    """(稳定名, [候选路径按优先级]) —— 名字跨环境稳定，路径运行时解析。"""
    t = []
    for f in sorted(os.listdir(WORK_DIR)):
        if f.startswith("dlt_") and f.endswith(".py") and f != "dlt_self_integrity.py":
            t.append((f, [os.path.join(WORK_DIR, f)]))
    for f in ("run_dlt.py", "dlt_run_v8.bat", "dlt_history.json"):
        t.append((f, [os.path.join(SCRIPTS_DIR, f), os.path.join(WORK_DIR, f)]))
    return t


def generate_manifest():
    files = {}
    resolved = {}
    for name, cands in _targets():
        for p in cands:
            if os.path.exists(p):
                files[name] = _sha256(p)
                resolved[name] = p
                break
    manifest = {
        "generated": os.path.basename(WORK_DIR),
        "note": "SHA256 基线, 由 dlt_self_integrity 自动生成",
        "files": files,
    }
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return manifest, resolved


def check_self_integrity():
    """返回 dict: ok / initialized / tampered[] / missing[] / note。"""
    if not os.path.exists(MANIFEST):
        # 首次运行: 建立基线
        generate_manifest()
        return {
            "ok": True,
            "initialized": True,
            "tampered": [],
            "missing": [],
            "note": "完整性清单不存在, 已初始化基线(首次运行)",
        }
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    baseline = manifest.get("files", {})
    tampered, missing = [], []
    for name, cands in _targets():
        if name not in baseline:
            continue  # 基线未涵盖的文件不判失败(避免误报新增合法文件)
        path = next((p for p in cands if os.path.exists(p)), None)
        if path is None:
            missing.append(name)
            continue
        if _sha256(path) != baseline[name]:
            tampered.append(name)
    ok = (len(tampered) == 0 and len(missing) == 0)
    return {
        "ok": ok,
        "initialized": False,
        "tampered": tampered,
        "missing": missing,
        "note": ("✅ 全部关键文件哈希一致" if ok else
                 f"⚠ 检测到异常: 篡改={tampered} 缺失={missing}"),
    }


# ============================================================
# 扩展能力 (深度升级): 数据过期检测 / 运行一致性 / 篡改自愈引导
# ============================================================
import datetime
import glob as _glob


def _history_path():
    for p in (os.path.join(WORK_DIR, "dlt_history.json"),
              os.path.join(SCRIPTS_DIR, "dlt_history.json")):
        if os.path.exists(p):
            return p
    return os.path.join(WORK_DIR, "dlt_history.json")


def check_data_freshness(attempt_refresh=True):
    """检测开奖数据是否过期 (mtime 过旧 / 最新开奖日期落后), 并尽力自动刷新。

    返回 dict: stale / age_days / latest_date / refreshed / note。
    设计: 数据陈旧属'可自愈'类问题 —— 重新拉取数据是非破坏性的(只更新数据, 不碰代码),
    且流水线本就在每次运行下载, 此处作为安全网。刷新仅在'拉取成功且数据合理'时才替换,
    失败则降级为告警(绝不让刷新失败阻断检查)。
    """
    hp = _history_path()
    if not os.path.exists(hp):
        return {"stale": True, "age_days": None, "latest_date": None,
                "refreshed": False, "note": "dlt_history.json 不存在"}
    try:
        age_days = (datetime.datetime.now() - datetime.datetime.fromtimestamp(
            os.path.getmtime(hp))).days
    except Exception:
        age_days = None
    latest_date = None
    try:
        hist = json.load(open(hp, encoding="utf-8"))
        dates = [d.get("date") for d in hist if isinstance(d, dict) and d.get("date")]
        if dates:
            latest_date = max(dates)
    except Exception:
        pass
    stale = False
    reasons = []
    if age_days is not None and age_days > 2:
        stale = True
        reasons.append(f"数据文件 {age_days} 天未更新")
    if latest_date:
        try:
            gap = (datetime.date.today() - datetime.date.fromisoformat(latest_date)).days
            if gap > 3:
                stale = True
                reasons.append(f"最新开奖 {latest_date} 已落后 {gap} 天")
        except Exception:
            pass
    refreshed = False
    if stale and attempt_refresh:
        try:
            import dlt_huiniao_api as api
            new_data = api.fetch_all_huiniao()
            if new_data and len(new_data) >= len(hist):
                json.dump(new_data, open(hp, "w", encoding="utf-8"),
                          ensure_ascii=False, indent=2)
                refreshed = True
                reasons.append("已自动重新拉取最新数据")
        except Exception as e:
            reasons.append(f"自动刷新失败(降级为告警): {e}")
    note = ("; ".join(reasons) if reasons else
            f"数据新鲜 (mtime {age_days}天前, 最新开奖 {latest_date})")
    return {"stale": stale and not refreshed, "age_days": age_days,
            "latest_date": latest_date, "refreshed": refreshed, "note": note}


def _latest_backup_dir():
    """定位最近一次备份目录(供篡改自愈引导)。"""
    try:
        import dlt_restore
        return dlt_restore._latest_backup()
    except Exception:
        return None


def self_heal(heal=False):
    """篡改自愈。

    设计(安全优先): 代码文件被篡改是高风险事件, **默认不盲目自覆盖** —— 因为基线清单可能在
    一次合法升级后未重初始化, 误判为'篡改'时盲目恢复会把刚写的新代码覆盖掉。故:
      - 检测到篡改 → 定位最近备份, 报告'篡改文件 + 备份位置 + 恢复命令'(自主诊断 + 引导)。
      - 仅当显式 heal=True (操作员确认) 才调用 dlt_restore 真正恢复并重建基线。
    数据过期(safe)的自愈在 check_data_freshness 内已自动完成; 此处专管代码完整性。
    """
    r = check_self_integrity()
    if r["ok"] or r.get("initialized"):
        return {"tampered": [], "backed_up": None, "healed": False,
                "note": "关键文件哈希一致, 无需自愈"}
    bak = _latest_backup_dir()
    if not heal:
        return {"tampered": r["tampered"], "backed_up": bak, "healed": False,
                "note": (f"检测到篡改 {r['tampered']}; 备份位于 {bak or '无'}; "
                          f"确认后运行 `python dlt_self_integrity.py --heal` 恢复")}
    # 显式恢复: 调用 dlt_restore 把关键文件从备份还原, 并重建基线
    try:
        import dlt_restore
        dlt_restore.restore_files(WORK_DIR, force=True)
        generate_manifest()
        return {"tampered": r["tampered"], "backed_up": bak, "healed": True,
                "note": "已从备份恢复被篡改文件并重建完整性基线"}
    except Exception as e:
        return {"tampered": r["tampered"], "backed_up": bak, "healed": False,
                "note": f"自动恢复失败: {e}; 请手动从备份 {bak} 恢复"}


def check_operational_consistency():
    """运行一致性: 抓'预测了却从未核对'的静默漏洞 + 孤儿验证记录。

    返回 dict: unverified(已开奖但未被核对的历史预测期) / orphans(验证记录引用了不存在的期) / ok。
    """
    hp = _history_path()
    perf_path = os.path.join(WORK_DIR, "dlt_performance.json")
    unverified, orphans = [], []
    try:
        hist = json.load(open(hp, encoding="utf-8"))
        periods = set(str(d.get("period")) for d in hist if isinstance(d, dict))
        latest = max(int(p) for p in periods)
    except Exception:
        return {"unverified": [], "orphans": [], "ok": True,
                "note": "历史数据不可读, 跳过一致性校验"}
    # 已生成的预测文件(期号)
    pred_periods = set()
    for f in _glob.glob(os.path.join(WORK_DIR, "dlt_prediction_*_v8.json")):
        m = __import__("re").search(r"dlt_prediction_(\d+)_v8\.json", f)
        if m:
            pred_periods.add(m.group(1))
    # 验证记录已覆盖的期号
    verified = set()
    if os.path.exists(perf_path):
        try:
            data = json.load(open(perf_path, encoding="utf-8"))
            verified = {str(r.get("period")) for r in data.get("records", [])}
        except Exception:
            pass
    # 已预测 且 已开奖(期号<=最新) 但 未出现在验证记录 → 静默漏洞
    for p in pred_periods:
        try:
            pi = int(p)
        except ValueError:
            continue
        if pi <= latest and p not in verified:
            unverified.append(p)
    # 验证记录引用了不存在于历史的期 → 孤儿
    for p in verified:
        if p not in periods:
            orphans.append(p)
    ok = (len(unverified) == 0 and len(orphans) == 0)
    return {"unverified": sorted(unverified, key=lambda x: int(x)),
            "orphans": sorted(orphans, key=lambda x: int(x)),
            "ok": ok,
            "note": ("OK" if ok else
                     f"未核对历史预测 {unverified or '无'}; 孤儿记录 {orphans or '无'}")}


def diagnose(heal=False):
    """综合诊断 (供健康护栏 #24 调用): 完整性 + 数据新鲜度 + 运行一致性 + (可选)自愈。

    返回 dict: integrity / freshness / consistency / heal / ok。
    """
    integrity = check_self_integrity()
    freshness = check_data_freshness()
    consistency = check_operational_consistency()
    heal_r = self_heal(heal=heal) if (not integrity["ok"]) else None
    ok = (integrity["ok"] and not freshness["stale"] and consistency["ok"]
          and (heal_r is None or heal_r["healed"] or not heal_r["tampered"]))
    return {"integrity": integrity, "freshness": freshness,
            "consistency": consistency, "heal": heal_r, "ok": ok}


def main():
    init = "--init" in sys.argv
    if init:
        m, _ = generate_manifest()
        print(f"✓ 已重建基线, 覆盖 {len(m['files'])} 个关键文件")
        return 0
    if "--heal" in sys.argv:
        r = self_heal(heal=True)
        print(f"自愈结果: {r['note']}")
        return 0 if r["healed"] or not r["tampered"] else 1
    if "--diagnose" in sys.argv:
        d = diagnose(heal=False)
        print("=== 综合诊断 ===")
        print(f"  完整性: {'✅' if d['integrity']['ok'] else '⚠ '+str(d['integrity'].get('tampered'))}")
        print(f"  数据新鲜度: {d['freshness']['note']}")
        print(f"  运行一致性: {d['consistency']['note']}")
        print(f"  综合: {'✅ 健康' if d['ok'] else '⚠ 存在问题'}")
        return 0 if d["ok"] else 1
    r = check_self_integrity()
    if r.get("initialized"):
        print(f"✓ {r['note']} (覆盖 {len(json.load(open(MANIFEST,encoding='utf-8'))['files'])} 个文件)")
    elif r["ok"]:
        print(f"✅ 自完整性检查通过 (关键文件 {len(json.load(open(MANIFEST,encoding='utf-8'))['files'])} 个, 哈希一致)")
    else:
        print(f"⚠ 自完整性异常:")
        if r["tampered"]:
            print(f"   篡改: {r['tampered']}")
        if r["missing"]:
            print(f"   缺失: {r['missing']}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
