#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大乐透系统 — 回归 / 冒烟测试 (Regression & Smoke Test)

设计目标: 在**不联网、不生成完整报告、不污染生产状态**的前提下,
对核心管线做一次"快而狠"的回归体检, 抓出改动后可能静默引入的破坏:

  1) 全量模块可导入  —— 抓出 `import re` 缺失 / 语法错误 / 模块级未定义名
                        (历史上第21项 AST 闸门抓过的那类事故)
  2) AST 未定义名网关 —— 复用 check_undefined_names.py, 退出码断言
  3) 9 项过滤器单测   —— passes_filters 已知 in/out 用例, 抓逻辑回退
  4) 穷举组合数确定性 —— exhaustive_combos() 重算数 == 缓存 dlt_valid_combos.json
                        数(抓 9 过滤器或缓存任一方漂移)
  5) 端到端预测生成   —— 用离线历史数据跑通 generate_predictions, 断言 5 组结构
                        合法(前5后2范围正确 / 过 9 过滤器 / 互不相同)

任何一项失败 -> 进程退出码 1(供 build_dist.py / CI 作为回归闸门)。

零网络依赖: 仅读取本地 dlt_history.json / dlt_valid_combos.json /
dlt_expert_picks.json。预测生成阶段在临时目录隔离, 不写回生产状态文件。
"""
import os
import sys
import json
import glob
import shutil
import tempfile
import contextlib
import subprocess
import py_compile

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

PY = sys.executable

# 需要离线喂给预测生成的本地数据(只读, 不修改)
NEEDED_DATA = [
    "dlt_history.json",
    "dlt_valid_combos.json",
    "dlt_expert_picks.json",
    "dlt_power_baseline.json",
    "dlt_winner_stats.json",
    "dlt_data_source.json",
]

failures = []
checks_run = 0


def record(name, ok, detail=""):
    global checks_run
    checks_run += 1
    mark = "✅" if ok else "❌"
    try:
        print(f"  {mark} [{checks_run:02d}] {name}" + (f"  -> {detail}" if detail else ""))
    except Exception:
        # stdout 偶发被关(某些模块 import 副作用), 不因此中断测试
        pass
    if not ok:
        failures.append((name, detail))


# ============================================================
# 1) 全量模块编译 (抓语法错误 / import 解析失败)
#    —— 用 py_compile 而非 import, 避免 dlt_cross_validate 等模块
#       在 import 时执行模块级主逻辑(污染 stdout / 副作用)。
#    —— 运行期未定义名(如漏 import re)由第 2 项 AST 网关专门抓。
# ============================================================
def test_compile():
    print("\n[1] 全量模块编译 (py_compile, 抓语法/import 解析错误)")
    files = sorted(glob.glob(os.path.join(ROOT, "*.py")))
    # 排除自身与一次性探查脚本
    skip = {"dlt_smoke_test.py", "_inspect_schema.py"}
    files = [f for f in files if os.path.basename(f) not in skip]
    bad = []
    for fp in files:
        try:
            py_compile.compile(fp, doraise=True)
        except py_compile.PyCompileError as e:
            bad.append((os.path.basename(fp), str(e).strip().splitlines()[-1]))
    if bad:
        for name, msg in bad:
            record(f"compile {name}", False, msg)
    else:
        record(f"全部 {len(files)} 个 .py 编译通过", True)


# ============================================================
# 2) AST 未定义名网关
# ============================================================
def test_ast_gate():
    print("\n[2] AST 未定义名网关 (check_undefined_names.py)")
    gate = os.path.join(ROOT, "check_undefined_names.py")
    if not os.path.exists(gate):
        record("AST 网关脚本存在", False, "check_undefined_names.py 缺失")
        return
    try:
        r = subprocess.run([PY, gate], cwd=ROOT,
                            capture_output=True, text=True, timeout=120,
                            encoding="utf-8", errors="replace")
        ok = r.returncode == 0
        record("AST 网关返回 0", ok,
               (r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[:120]))
    except Exception as e:
        record("AST 网关执行", False, f"{type(e).__name__}: {e}")


# ============================================================
# 3) 9 项过滤器单测
# ============================================================
def test_filters():
    print("\n[3] passes_filters 单测 (9 项过滤器逻辑)")
    try:
        import dlt_auto
    except Exception as e:
        record("导入 dlt_auto", False, str(e))
        return
    # 已知合法组合(取自 dlt_valid_combos.json 样本)
    record("合法组合过 9 过滤器",
           dlt_auto.passes_filters([1, 2, 18, 28, 31]) is True,
           "预期 True")
    # 全奇数 -> odd_count=5 不在 [2,3]
    record("全奇数被拒 (奇偶过滤)",
           dlt_auto.passes_filters([1, 3, 5, 7, 9]) is False,
           "预期 False")
    # 和值过低 -> sum=15 < 80
    record("和值过低被拒 (和值过滤)",
           dlt_auto.passes_filters([1, 2, 3, 4, 5]) is False,
           "预期 False")
    # 重号超过 2 个 -> 第9项过滤
    record("重号>2 被拒 (重号过滤)",
           dlt_auto.passes_filters([1, 2, 3, 4, 5], prev_front=[1, 2, 3, 4, 5]) is False,
           "预期 False")
    # 连号组过多: 1,2,3,4,5 连续 -> consecutive_groups 应为 1(整组一段)
    # 故意构造两组连号: 1,2, 4,5, 7 -> 两组连号 -> >1 应被拒
    record("连号组>1 被拒 (连号过滤)",
           dlt_auto.passes_filters([1, 2, 4, 5, 7]) is False,
           "预期 False")


# ============================================================
# 4) 穷举组合数确定性
# ============================================================
def test_exhaustive_determinism():
    print("\n[4] exhaustive_combos() 重算 == 缓存 (9 过滤器漂移闸门)")
    try:
        import dlt_auto
        vc_path = os.path.join(ROOT, "dlt_valid_combos.json")
        if not os.path.exists(vc_path):
            record("缓存文件存在", False, "dlt_valid_combos.json 缺失")
            return
        cached = json.load(open(vc_path, encoding="utf-8"))
        got = dlt_auto.exhaustive_combos()
        ok = (len(got) == len(cached))
        record("穷举数 == 缓存数", ok,
               f"重算={len(got):,}  缓存={len(cached):,}")
    except Exception as e:
        record("穷举重算", False, f"{type(e).__name__}: {e}")


# ============================================================
# 5) 端到端预测生成 (临时目录隔离)
# ============================================================
def test_end_to_end_predict():
    print("\n[5] generate_predictions 端到端 (离线数据, 临时目录隔离)")
    try:
        import dlt_auto
    except Exception as e:
        record("导入 dlt_auto", False, str(e))
        return

    # 准备离线数据(只读, 复制到临时目录以隔离写入)
    missing = [n for n in NEEDED_DATA if not os.path.exists(os.path.join(ROOT, n))]
    if missing:
        record("离线数据齐全", False, f"缺失: {missing}")
        return

    draws = json.load(open(os.path.join(ROOT, "dlt_history.json"), encoding="utf-8"))
    valid_combos = json.load(open(os.path.join(ROOT, "dlt_valid_combos.json"), encoding="utf-8"))
    # 与生产 dlt_auto.main() 完全一致: 转成 (expert, front, back) 元组列表
    ep_data = json.load(open(os.path.join(ROOT, "dlt_expert_picks.json"), encoding="utf-8"))
    expert_picks = [(e["expert"], e["front"], e.get("back", []))
                    for e in ep_data.get("experts", [])]

    # 数据基本健全性
    if not (isinstance(draws, list) and len(draws) >= 100):
        record("历史数据量充足", False, f"仅 {len(draws)} 期")
        return
    if not (isinstance(valid_combos, list) and len(valid_combos) > 1000):
        record("合法组合缓存充足", False, f"仅 {len(valid_combos)} 个")
        return

    td = tempfile.mkdtemp(prefix="dlt_smoke_")
    try:
        for n in NEEDED_DATA:
            shutil.copy(os.path.join(ROOT, n), os.path.join(td, n))
        old_cwd = os.getcwd()
        os.chdir(td)
        try:
            # 计算模型(纯内存, 离线)
            models = dlt_auto.compute_models(draws)
            # 抑制冗长打印
            with contextlib.redirect_stdout(open(os.devnull, "w", encoding="utf-8")):
                groups, dantuo = dlt_auto.generate_predictions(
                    draws, models, valid_combos, expert_picks)
        finally:
            os.chdir(old_cwd)

        # 结构断言
        record("返回 5 组推荐", isinstance(groups, list) and len(groups) == 5,
               f"len(groups)={len(groups) if isinstance(groups, list) else 'N/A'}")

        if isinstance(groups, list) and len(groups) == 5:
            all_ok = True
            seen = set()
            bad = []
            for gi, g in enumerate(groups):
                f = g.get("front"); b = g.get("back")
                if not (isinstance(f, list) and len(f) == 5 and len(set(f)) == 5
                        and all(isinstance(x, int) and 1 <= x <= 35 for x in f)):
                    all_ok = False; bad.append(f"组{gi+1}前区非法:{f}"); continue
                # 后区为复式(4 码, C(4,2)=6 注), 范围 1..12 互不相同
                if not (isinstance(b, list) and len(b) == 4 and len(set(b)) == 4
                        and all(isinstance(x, int) and 1 <= x <= 12 for x in b)):
                    all_ok = False; bad.append(f"组{gi+1}后区非法:{b}"); continue
                if not dlt_auto.passes_filters(f):
                    all_ok = False; bad.append(f"组{gi+1}未过9过滤器:{f}")
                seen.add(dlt_auto._combo_str(f, b))
            record("每组前5后2合法且过过滤器", all_ok,
                   ("; ".join(bad[:3]) if bad else "5 组全部合法"))
            record("5 组互不相同 (跨期唯一性闸门)", len(seen) == 5,
                   f"去重后 {len(seen)} 组")

        # 胆拖结构最小断言
        if isinstance(dantuo, dict) and dantuo.get("standard"):
            std = dantuo["standard"]
            ok_struct = all(k in std for k in ("dan", "tuo", "back"))
            record("胆拖方案结构完整", ok_struct,
                   "dan/tuo/back 齐备" if ok_struct else f"缺键: {[k for k in ('dan','tuo','back') if k not in std]}")
        else:
            record("胆拖方案(可选)", True, "本数据下走降级路径, 不强制")
    except Exception as e:
        record("端到端预测生成", False, f"{type(e).__name__}: {e}")
    finally:
        shutil.rmtree(td, ignore_errors=True)


# ============================================================
# 6) 开奖核对 CLI 运行时冒烟 (subprocess 真实执行)
#    —— 覆盖静态 AST 闸门盲区: 当 `if __name__=="__main__": main()` 守卫
#       写在某个 def 之前时, 以脚本方式运行时 main() 会先于该 def 执行,
#       触发运行时 NameError。import / AST 检查都抓不到, 只有"真正以脚本
#       方式执行"才能暴露。本条直接在离线、临时目录下跑通业务 CLI。
# ============================================================
def test_runtime_cli():
    print("\n[6] 开奖核对 CLI 运行时冒烟 (subprocess 真实执行, 覆盖 __main__ 顺序盲区)")
    # 找一个既有预测文件又有开奖结果的期号 -> 离线且完整走到 export 路径
    preds = sorted(glob.glob(os.path.join(ROOT, "dlt_prediction_*_v8.json")))
    if not preds:
        record("存在预测文件", False, "无 dlt_prediction_*_v8.json")
        return
    hist_path = os.path.join(ROOT, "dlt_history.json")
    hist = {}
    if os.path.exists(hist_path):
        try:
            hist = {str(d.get('period')): d
                    for d in json.load(open(hist_path, encoding='utf-8'))}
        except Exception:
            hist = {}
    target = None
    for pf in preds:
        P = next((p for p in os.path.basename(pf).split('_') if p.isdigit()), None)
        if not P:
            continue
        d = hist.get(P)
        if not d:
            continue
        f = d.get('front'); b = d.get('back')
        if isinstance(f, str):
            f = [int(x) for x in f.split(',') if x.strip()]
        if isinstance(b, str):
            b = [int(x) for x in b.split(',') if x.strip()]
        if (isinstance(f, (list, tuple)) and isinstance(b, (list, tuple))
                and len(f) >= 5 and len(b) >= 2):
            target = (P, [int(x) for x in f[:5]], [int(x) for x in b[:2]])
            break
    if not target:
        record("找到可核对期号(预测+开奖齐全)", False, "无匹配期号")
        return
    P, front, back = target
    fr = ",".join(str(x) for x in front)
    bk = ",".join(str(x) for x in back)
    # 不传 --out-dir: 强制 export_to_desktop 走到 cands 分支(调用 _detect_real_desktop),
    # 以真覆盖"守卫写在 def 之前"那类运行时顺序缺陷。用环境变量把桌面重定向到临时目录,
    # 避免污染真实用户桌面(真实报告路径由 REPORT_DESKTOP_PATH 输出断言)。
    td = tempfile.mkdtemp(prefix="dlt_drawcheck_")
    desk = os.path.join(td, "Desktop")
    os.makedirs(desk, exist_ok=True)
    try:
        env = dict(os.environ)
        env['PYTHONUTF8'] = '1'
        env['PYTHONIOENCODING'] = 'utf-8'
        env['SystemDrive'] = 'X:'        # 让 _detect_real_desktop 扫描不到真实用户目录 -> None
        env['USERPROFILE'] = td          # 回退桌面 = td/Desktop
        r = subprocess.run(
            [PY, os.path.join(ROOT, "dlt_draw_check.py"),
             "--period", P, "--front", fr, "--back", bk],
            cwd=ROOT, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=300, env=env)
        ok = r.returncode == 0 and "REPORT_DESKTOP_PATH" in r.stdout
        detail = (r.stdout.strip().splitlines()[-1] if r.stdout.strip()
                  else (r.stderr.strip()[:200] if r.stderr.strip() else f"rc={r.returncode}"))
        record(f"draw_check CLI 退出0且生成报告(期{P})", ok, detail)
        written = [f for f in os.listdir(desk) if f.endswith('.html')]
        record("报告落入临时桌面(未污染真实桌面)", len(written) == 1,
               f"临时桌面报告数={len(written)}")
    finally:
        shutil.rmtree(td, ignore_errors=True)


def main():
    # 控制台编码自适应(Windows GBK 下打印 emoji 会抛 UnicodeEncodeError)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    print("=" * 64)
    print("  大乐透系统 — 回归 / 冒烟测试")
    print(f"  时间: {__import__('datetime').datetime.now():%Y-%m-%d %H:%M:%S}")
    print(f"  根目录: {ROOT}")
    print("=" * 64)

    test_compile()
    test_ast_gate()
    test_filters()
    test_exhaustive_determinism()
    test_end_to_end_predict()
    test_runtime_cli()

    print("\n" + "=" * 64)
    if failures:
        print(f"  ❌ 冒烟测试失败 {len(failures)}/{checks_run} 项:")
        for n, d in failures:
            print(f"     - {n}  {d}")
        print("  ⛔ 存在回归, 请勿交付!")
        return 1
    print(f"  ✅ 全部 {checks_run} 项通过, 核心管线健康 (回归安全网有效)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
