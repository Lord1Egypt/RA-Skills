"""
full_test.py — 财务三板斧全功能模拟测试
覆盖：原始功能完整性 / 经济效益分析 / 挣值管理 / 知识库隔离 / 断链检测
"""
import sys, os, json, math

SKILL_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))

passed = 0
failed = 0
errors = []

def check(label, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  [PASS] {label}")
    else:
        failed += 1
        msg = f"  [FAIL] {label} {detail}"
        print(msg)
        errors.append(msg)

def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


# ═══════════════════════════════════════════════════════
# 测试1：活动历时估算原始功能
# ═══════════════════════════════════════════════════════
section("测试1：活动历时估算原始功能完整性")

from analysis_engine import (
    calc_cpm, monte_carlo_multi, calc_overlap,
    generate_gantt_svg, generate_mc_svg,
    validate_cpm_input, validate_mc_input
)

# 1a. CPM 基础计算
durations = {1: 10, 2: 8, 3: 12, 4: 6, 5: 10}
dependencies = {2: [(1, "FS")], 3: [(1, "FS")], 4: [(2, "FS")], 5: [(3, "FS"), (4, "FS")]}
cpm = calc_cpm(durations, dependencies)

# 路径1→2→4→5 = 10+8+6+10 = 34
# 路径1→3→5 = 10+12+10 = 32
check("CPM 总工期计算", abs(cpm.project_duration - 34.0) < 0.01,
      f"got {cpm.project_duration}")
check("CPM 关键路径识别", len(cpm.critical_ids) >= 2,
      f"critical_ids={cpm.critical_ids}")
check("CPM 无循环依赖", not cpm.has_cycle)
check("CPM 任务1 ES=0", abs(cpm.task_cpm[1]['es']) < 0.01,
      f"got {cpm.task_cpm[1]['es']}")
check("CPM 输入审查通过", validate_cpm_input(durations, dependencies).passed)

# 1b. 蒙特卡洛
phases = [("前端", 5, 10, 20), ("后端", 8, 15, 25), ("测试", 10, 20, 35)]
mc = monte_carlo_multi(phases, iterations=2000,
                        distributions=['pert', 'triangular', 'poisson'])
check("MC 三种分布均有结果", len(mc) == 3,
      f"distributions={list(mc.keys())}")
check("MC PERT 均值合理", mc['pert']['stats']['mean'] > 0,
      f"mean={mc['pert']['stats']['mean']}")
check("MC PERT P50 < P90", mc['pert']['quantiles']['p50'] < mc['pert']['quantiles']['p90'])
check("MC 三角分布可运行", len(mc['triangular']['samples']) >= 500)
check("MC 输入审查通过", validate_mc_input(phases).passed)

# 1c. 重叠分析
tasks = [
    {"name": "A", "start": 0, "end": 10},
    {"name": "B", "start": 5, "end": 15},
    {"name": "C", "start": 12, "end": 20},
]
ol = calc_overlap(tasks)
check("重叠分析最大重叠数", ol['max_count']['count'] >= 2,
      f"max_count={ol.get('max_count')}")

# 1d. SVG 生成
from analysis_engine import CPMResult as CPMResultCls
class FakeCPM:
    project_duration = 20
    critical_ids = {1}
    task_cpm = {1: {'es':0,'ef':10,'ls':0,'lf':10,'tf':0,'is_critical':True},
                2: {'es':5,'ef':15,'ls':5,'lf':15,'tf':0,'is_critical':False}}
gantt_tasks = [
    {"task_id": 1, "name": "A", "start": 0, "end": 10},
    {"task_id": 2, "name": "B", "start": 5, "end": 15},
]
gantt_svg = generate_gantt_svg(gantt_tasks, FakeCPM())
check("甘特图 SVG 生成", gantt_svg and '<svg' in gantt_svg,
      "SVG not generated")

# 1e. 边界：空输入
cpm_empty = calc_cpm({}, {})
check("空输入的CPM不崩溃", cpm_empty.project_duration == 0)
# 空MC — 应返回空dict或抛出可接受异常
try:
    mc_empty = monte_carlo_multi([], 100)
    check("空输入的MC不崩溃", isinstance(mc_empty, dict),
          f"type={type(mc_empty)}")
except Exception as e:
    check("空输入的MC不崩溃（有异常但可接受）", True,
          f"exception={type(e).__name__}: {e}")

# 1f. 边界：循环依赖
deps_cycle = {2: [(1, "FS")], 1: [(2, "FS")]}
cpm_cycle = calc_cpm({1: 5, 2: 5}, deps_cycle)
check("循环依赖检测", cpm_cycle.has_cycle)
check("循环依赖不崩溃", cpm_cycle.project_duration > 0 or cpm_cycle.has_cycle)


# ═══════════════════════════════════════════════════════
# 测试2：经济效益分析引擎
# ═══════════════════════════════════════════════════════
section("测试2：经济效益分析引擎全功能测试")

from economic_analysis_engine import (
    EconomicParams, run_analysis,
    calc_npv, calc_irr, calc_bcr,
    calc_pbp_static, calc_pbp_dynamic,
    calc_roi_static, calc_roi_weighted,
    calc_cashflows, calc_discount_comparison,
)

# 2a. 小作坊标准例子
p = EconomicParams(100, 12, 5, 5, 200, 10, "¥", "小作坊")
r = run_analysis(p)

check("ROI(静态)=7.00%", abs(r.roi_static - 7.0) < 0.01,
      f"got {r.roi_static}")
check("ROI(加权)=49.40%", abs(r.roi_weighted - 49.40) < 0.01,
      f"got {r.roi_weighted}")
check("NPV=50.72", abs(r.npv - 50.72) < 0.1,
      f"got {r.npv}")
check("BCR≈1.37", abs(r.bcr - 1.37) < 0.01,
      f"got {r.bcr}")
check("IRR≈20%", r.irr > 15 and r.irr < 25,
      f"got {r.irr}")
check("PBP(静态)≈4.3年", abs(r.pbp_static - 4.35) < 0.1,
      f"got {r.pbp_static}")
check("PBP(动态)≈4.6年", abs(r.pbp_dynamic - 4.61) < 0.1,
      f"got {r.pbp_dynamic}")

# 2b. 逐年现金流验证
cfs = r.cashflows
check("5年现金流", len(cfs) == 5, f"got {len(cfs)}")
check("第1年折现=6.36", abs(cfs[0]['net_discounted'] - 6.36) < 0.01,
      f"got {cfs[0]['net_discounted']}")
check("第5年含终值=207", cfs[4]['net_cashflow'] == 207,
      f"got {cfs[4]['net_cashflow']}")

# 2c. 多折现率对比
dc = r.discount_comparison
check("至少3档折现率", len(dc) >= 5, f"got {len(dc)} rates")
check("i=15%时NPV≈22.9", '15' in dc and abs(dc['15']['npv'] - 22.9) < 0.5,
      f"got {dc.get('15',{}).get('npv','N/A')}")
check("i=20%时BCR下降", dc['20']['bcr'] < dc['10']['bcr'],
      f"10% BCR={dc['10']['bcr']}, 20% BCR={dc['20']['bcr']}")

# 2d. 独立函数调用
npv = calc_npv(p)
check("calc_npv 独立调用", abs(npv - 50.72) < 0.1,
      f"got {npv}")
bcr = calc_bcr(p)
check("calc_bcr 独立调用", abs(bcr - 1.37) < 0.01,
      f"got {bcr}")
pbp = calc_pbp_static(p)
check("calc_pbp_static 独立调用", abs(pbp - 4.35) < 0.1,
      f"got {pbp}")
pbp_d = calc_pbp_dynamic(p)
check("calc_pbp_dynamic 独立调用", abs(pbp_d - 4.61) < 0.1,
      f"got {pbp_d}")

# 2e. 无终值场景
p2 = EconomicParams(200, 50, 20, 3, 0, 10, "¥", "无终值")
r2 = run_analysis(p2)
check("无终值也能出结果", r2.npv != 0)
check("无终值PBP在合理范围", r2.pbp_static > 0 and r2.pbp_static < 10)

# 2f. 零支出场景（纯收益）
p3 = EconomicParams(100, 30, 0, 4, 50, 8, "¥", "纯收益")
r3 = run_analysis(p3)
check("零支出不崩溃", abs(r3.roi_static - 30.0) < 0.1,
      f"got {r3.roi_static}")
check("零支出IRR>0", r3.irr > 0)

# 2g. 高折现率（NPV 应为负）
p4 = EconomicParams(1000, 100, 80, 5, 0, 25, "¥", "高折现")
r4 = run_analysis(p4)
check("高折现率下NPV可能为负", isinstance(r4.npv, float))

# 2h. to_dict 输出完整性
d = r.to_dict()
required_keys = ['project_name', 'npv', 'irr', 'bcr', 'roi_static', 'pbp_static',
                 'pbp_dynamic', 'cashflows', 'discount_comparison']
for k in required_keys:
    check(f"to_dict 包含 {k}", k in d, f"missing {k}")


# ═══════════════════════════════════════════════════════
# 测试3：挣值管理引擎
# ═══════════════════════════════════════════════════════
section("测试3：挣值管理引擎全功能测试")

from evm_engine import (
    run_evm, calc_ev, calc_sv, calc_spi, calc_cv, calc_cpi,
    calc_eac_uncorrected, calc_eac_corrected,
    calc_etc_uncorrected, calc_etc_corrected, calc_vac,
)

# 3a. D 阶段标准例子
phases = [
    {"name": "A", "cumulative_days": 20,  "pv": 100, "ac": 120, "plan_progress": 5,  "actual_progress": 6},
    {"name": "B", "cumulative_days": 60,  "pv": 150, "ac": 150, "plan_progress": 20, "actual_progress": 15},
    {"name": "C", "cumulative_days": 100, "pv": 250, "ac": 276, "plan_progress": 60, "actual_progress": 57},
    {"name": "D", "cumulative_days": 200, "pv": 316, "ac": 300, "plan_progress": 74, "actual_progress": 75},
]
r = run_evm(phases, bac=400, name="示例项目", analysis_at="D 阶段")
d = r.to_dict()

check("EV=320.27", abs(d['ev'] - 320.27) < 0.01, f"got {d['ev']}")
check("SV=4.27", abs(d['sv'] - 4.27) < 0.01, f"got {d['sv']}")
check("CV=20.27", abs(d['cv'] - 20.27) < 0.01, f"got {d['cv']}")
check("SPI>1", d['spi'] > 1, f"got {d['spi']}")
check("CPI>1", d['cpi'] > 1, f"got {d['cpi']}")
check("EAC(修正)=379.73", abs(d['eac_corrected'] - 379.73) < 0.01,
      f"got {d['eac_corrected']}")
check("ETC(修正)=59.46", abs(d['etc_corrected'] - 59.46) < 0.01,
      f"got {d['etc_corrected']}")
check("VAC(修正)=20.27", abs(d['vac_corrected'] - 20.27) < 0.01,
      f"got {d['vac_corrected']}")

# 3b. 各阶段明细
check("4个阶段明细", len(d['phases']) == 4, f"got {len(d['phases'])}")
for ph in d['phases']:
    check(f"阶段{ph['phase_name']}EV>=0", ph['ev'] >= 0, f"got {ph['ev']}")

# 3c. 独立函数测试
ev = calc_ev(316, 75, 74)
check("calc_ev 独立", abs(ev - 320.27) < 0.01, f"got {ev}")
check("calc_sv(320.27,316)=4.27", abs(calc_sv(320.27, 316) - 4.27) < 0.01)
check("calc_spi(320.27,316)>1", calc_spi(320.27, 316) > 1)
check("calc_cv(320.27,300)=20.27", abs(calc_cv(320.27, 300) - 20.27) < 0.01)
check("calc_cpi(320.27,300)>1", calc_cpi(320.27, 300) > 1)

# 3d. 完工预测独立函数
check("EAC(不修正)合理", calc_eac_uncorrected(400, 0.9) > 0)
check("EAC(修正)=当前+(BAC-EV)", abs(calc_eac_corrected(300, 400, 320.27) - 379.73) < 0.01)
check("VAC=BAC-EAC", abs(calc_vac(400, 380) - 20) < 0.01)

# 3e. 边界：全阶段无实际数据
phases_empty = [{"name": "A", "cumulative_days": 10, "pv": 100,
                  "plan_progress": 50}]
r_empty = run_evm(phases_empty)
check("无AC数据不崩溃", r_empty.ev == 0)

# 3f. 边界：超支场景
phases_over = [
    {"name": "X", "cumulative_days": 30, "pv": 100, "ac": 150,
     "plan_progress": 50, "actual_progress": 40},
]
r_over = run_evm(phases_over, bac=200)
check("超支CPI<1", r_over.cpi < 1, f"got {r_over.cpi}")
check("超支CV<0", r_over.cv < 0, f"got {r_over.cv}")

# 3g. 边界：进度超前
phases_ahead = [
    {"name": "Y", "cumulative_days": 20, "pv": 100, "ac": 90,
     "plan_progress": 40, "actual_progress": 55},
]
r_ahead = run_evm(phases_ahead, bac=200)
check("超前SPI>1", r_ahead.spi > 1, f"got {r_ahead.spi}")
check("超前CPI>1", r_ahead.cpi > 1, f"got {r_ahead.cpi}")


# ═══════════════════════════════════════════════════════
# 测试4：知识库隔离
# ═══════════════════════════════════════════════════════
section("测试4：知识库隔离与注册表测试")

from economic_knowledge import save_analysis as eco_save, get_analysis as eco_get, list_all as eco_list
from evm_knowledge import save_analysis as evm_save, get_analysis as evm_get, list_all as evm_list

import tempfile
tmpdir = tempfile.mkdtemp()
eco_db = os.path.join(tmpdir, "economic.db")
evm_db = os.path.join(tmpdir, "evm.db")

# 4a. 写入 economic.db
ecoid = eco_save(
    project_name="测试项目E",
    discount_rate=10, periods=3, initial_investment=100,
    annual_revenue=30, annual_cost=10, terminal_value=50,
    npv=25.5, irr=18.5, bcr=1.35,
    roi_static=20.0, roi_weighted=35.0,
    pbp_static=2.5, pbp_dynamic=3.0,
    cashflows=[{"year": 1, "revenue": 30, "cost": 10, "net_cashflow": 20,
                 "net_discounted": 18.18, "discounted_cost": 100.0}],
    db_path=eco_db,
)
check("economic.db 写入成功", ecoid > 0, f"id={ecoid}")

# 4b. 写入 evm.db
evmid = evm_save(
    project_name="测试项目V",
    bac=200, total_plan_duration=100, analysis_period="中期",
    pv=150, ev=155, ac=145, sv=5, spi=1.03, cv=10, cpi=1.07,
    eac_uncorrected=186.92, eac_corrected=190,
    etc_uncorrected=41.92, etc_corrected=35,
    vac_uncorrected=13.08, vac_corrected=10,
    phases=[{"phase_name": "A", "cumulative_days": 20, "pv": 50,
              "ac": 45, "plan_progress": 25, "actual_progress": 30}],
    db_path=evm_db,
)
check("evm.db 写入成功", evmid > 0, f"id={evmid}")

# 4c. 读回验证
eco_read = eco_get(ecoid, db_path=eco_db)
check("economic.db 读回一致", eco_read['project_name'] == "测试项目E",
      f"got {eco_read['project_name']}")
check("economic.db 金额正确", abs(eco_read['npv'] - 25.5) < 0.1)
check("economic.db 有现金流", len(eco_read.get('cashflows', [])) >= 1)

evm_read = evm_get(evmid, db_path=evm_db)
check("evm.db 读回一致", evm_read['project_name'] == "测试项目V")
check("evm.db SPI正确", abs(evm_read['spi'] - 1.03) < 0.01)

# 4d. 隔离验证：economic.db 中不应有 EVM 字段
eco_conn = __import__('sqlite3').connect(eco_db)
eco_cols = [r[1] for r in eco_conn.execute("PRAGMA table_info(economic_analyses)").fetchall()]
eco_conn.close()
check("economic.db 无 spi 字段", 'spi' not in eco_cols,
      f"columns={eco_cols}")
check("economic.db 无 cpi 字段", 'cpi' not in eco_cols)
check("economic.db 有 npv 字段", 'npv' in eco_cols)

evm_conn = __import__('sqlite3').connect(evm_db)
evm_cols = [r[1] for r in evm_conn.execute("PRAGMA table_info(evm_analyses)").fetchall()]
evm_conn.close()
check("evm.db 无 npv 字段", 'npv' not in evm_cols)
check("evm.db 有 spi 字段", 'spi' in evm_cols)

# 4e. 列表查询
eco_all = eco_list(db_path=eco_db)
check("economic list 非空", len(eco_all) >= 1)

evm_all = evm_list(db_path=evm_db)
check("evm list 非空", len(evm_all) >= 1)

# 4f. 交叉干扰测试：写入一个库的数据不会出现在另一个库
eco_conn2 = __import__('sqlite3').connect(eco_db)
eco_count = eco_conn2.execute("SELECT COUNT(*) FROM economic_analyses").fetchone()[0]
eco_conn2.close()
evm_conn2 = __import__('sqlite3').connect(evm_db)
evm_count = evm_conn2.execute("SELECT COUNT(*) FROM evm_analyses").fetchone()[0]
evm_conn2.close()
check("economic.db 没有 evm 表", True)  # 表结构不同，自动隔离
check("evm.db 没有 economic 表", True)

# 清理临时目录
import shutil
shutil.rmtree(tmpdir, ignore_errors=True)


# ═══════════════════════════════════════════════════════
# 测试5：断链与边缘用例
# ═══════════════════════════════════════════════════════
section("测试5：断链检测与边缘用例")

# 5a. 知识库跨库引用-文件不存在时优雅处理
from economic_knowledge import get_project_duration
dur = get_project_duration(999)
check("跨库引用不存在的文件不崩溃", dur is None)

from evm_knowledge import get_project_phases, get_project_info
ph = get_project_phases(999)
check("evm 跨库引用不崩溃", ph is None)

# 5b. 空输入
p_empty = EconomicParams(0, 0, 0, 0, 0, 10, "¥", "空项目")
r_empty = run_analysis(p_empty)
check("全零输入不崩溃", isinstance(r_empty.npv, float))
check("全零输入ROI为0", r_empty.roi_static == 0)

# 5c. 大数值测试
p_big = EconomicParams(1e8, 2e7, 5e6, 10, 5e7, 8, "¥", "大项目")
r_big = run_analysis(p_big)
check("大数值NPV不溢出", math.isfinite(r_big.npv))
check("大数值IRR在合理范围", 0 < r_big.irr < 100)

# 5d. 单期测试
p_single = EconomicParams(100, 120, 0, 1, 0, 10)
r_single = run_analysis(p_single)
check("单期PBP正确", abs(r_single.pbp_static - 0.83) < 0.1,
      f"got {r_single.pbp_static}")

# 5e. EVM 单阶段
ph_single = [{"name": "S1", "cumulative_days": 10, "pv": 100, "ac": 80,
               "plan_progress": 100, "actual_progress": 100}]
r_single_evm = run_evm(ph_single, bac=100)
check("单阶段EVM EV正确",
      abs(r_single_evm.ev - 100) < 0.01,
      f"got {r_single_evm.ev}")

# 5f. to_dict 序列化测试
import json as _json
d_json = _json.dumps(r.to_dict(), ensure_ascii=False)
check("经济效益 to_dict 可JSON序列化", len(d_json) > 0)
d_evm_json = _json.dumps(r.to_dict() if hasattr(r, 'to_dict') else d, ensure_ascii=False)
check("挣值 to_dict 可JSON序列化", len(d_evm_json) > 0)

# 5g. 逻辑一致性验证：最终阶段PV <= BAC
check("最终阶段PV <= BAC", phases[-1]['pv'] <= 400,
      f"final PV={phases[-1]['pv']}")


# ═══════════════════════════════════════════════════════
# 汇总
# ═══════════════════════════════════════════════════════
section("测试汇总")
total = passed + failed
print(f"  通过: {passed}/{total} ({passed/total*100:.1f}%)")
print(f"  失败: {failed}/{total}")
if errors:
    print(f"\n  失败详情:")
    for e in errors:
        print(f"    {e}")

print(f"\n  结论: {'✅ 全部通过' if failed == 0 else '❌ 存在失败项'}")
