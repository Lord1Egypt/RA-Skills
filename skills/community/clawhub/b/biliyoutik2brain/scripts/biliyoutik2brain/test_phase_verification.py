#!/usr/bin/env python3
"""
端到端 Phase 1.4 ~ 3.2 综合验证脚本
只测核心逻辑层，不碰网络下载/API调用。
"""
import sys, os, json, time

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(_SCRIPT_DIR)
for p in (_PARENT, _SCRIPT_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

# ── 禁用外部依赖（防止意外网络调用）──
import biliyoutik2brain.core.config as cfg
cfg.queue_light = lambda url: None
cfg.schedule_pending = lambda wf_id: None
cfg.acquire_light_slot = lambda: True
cfg.release_light_slot = lambda: None
cfg.dequeue_light = lambda: None

ok = 0
fail = 0
def check(name: str, cond: bool, detail: str = ""):
    global ok, fail
    if cond:
        ok += 1
        print(f"  ✅ {name}")
    else:
        fail += 1
        print(f"  ❌ {name}: {detail}")

def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

# ====================================================================
section("Phase 1.4 — system_monitor 模型选择策略集成")
# ====================================================================
from biliyoutik2brain.core.system_monitor import decide_upgrade_model

# 场景1: 无system_status → 回退硬编码
from biliyoutik2brain.core.retry_orchestrator import decide_p2_upgrade_path
r1 = decide_p2_upgrade_path(
    p2_triggered=True,
    p2_debug={"effective": 0.3, "threshold": 0.05, "proper_count": 80.0,
               "domain_coeff": 1.0, "speaker_coeff": 1.0,
               "unresolved_words": ["测试"]},
    route_model="whisper_base",
    system_status=None,
)
check("无 system_status → 回退硬编码", 
      "path" in r1 and r1["path"] != "error",
      f"path={r1.get('path')}, benefit={r1.get('benefit')}")

# 场景2: 资源充足 + API可用 → dual
r2 = decide_p2_upgrade_path(
    p2_triggered=True,
    p2_debug={"effective": 0.3, "threshold": 0.05, "proper_count": 60.0,
               "domain_coeff": 0.8, "speaker_coeff": 0.8,
               "unresolved_words": ["测试"]},
    route_model="whisper_base",
    system_status={"cpu_percent": 30.0, "memory_percent": 50.0, "api_available": True, "network_ok": True},
)
check("资源充足+API可用 → 非none", 
      r2.get("path") != "none",
      f"path={r2.get('path')}, sm_decision={r2.get('sm_decision')}")
check("sm_decision 字段存在", 
      "sm_decision" in r2,
      f"sm_decision={r2.get('sm_decision')}")

# 场景3: 高CPU + API不可用 → 容忍
r3 = decide_p2_upgrade_path(
    p2_triggered=True,
    p2_debug={"effective": 0.3, "threshold": 0.05, "proper_count": 95.0,
               "domain_coeff": 0.5, "speaker_coeff": 0.5,
               "unresolved_words": ["测试"]},
    route_model="whisper_small",
    system_status={"cpu_percent": 90.0, "memory_percent": 80.0, "api_available": False, "network_ok": False},
)
check("高CPU+API不可用 → none或sm_decision降级", 
      r3.get("path") == "none" or r3.get("sm_decision", {}).get("choice") == "keep",
      f"path={r3.get('path')}, sm_decision={r3.get('sm_decision')}")

# 场景4: decide_upgrade_model 直接调用
sm_r = decide_upgrade_model(
    current_model="whisper_base",
    system_status={"cpu_percent": 40.0, "memory_percent": 60.0,
                   "api_available": True, "network_ok": True},
    p2_severity=0.6, proper_count=70,
)
check("decide_upgrade_model 返回有效结构",
      "choice" in sm_r and "estimated_cost" in sm_r and "estimated_benefit" in sm_r,
      f"choice={sm_r.get('choice')}, keys={list(sm_r.keys())}")
# ====================================================================
section("Phase 2.1 — n-gram 向量反面验证")
# ====================================================================
from biliyoutik2brain.core.corrector_engine.layer1 import (
    semantic_reverse_check, batch_semantic_reverse_check,
)

# 场景1: 完全相同的文本 → n-gram 向量相同 → 通过
r_l1 = semantic_reverse_check(
    "今天天气真好适合出行", "今天天气真好适合出行",
    "真好", "真好"
)
check("完全相同文本 → 通过(返回None)", 
      r_l1 is None,
      f"result={r_l1}")

# 场景2: 可疑替换（触发）
# "大盘今天上涨了" → "大盘今天下跌了"，半数以上 n-gram 变化
r_l2 = semantic_reverse_check(
    "大盘今天上涨了", "大盘今天下跌了",
    "上涨", "下跌"
)
check("反义词替换 → 被标记", 
      r_l2 is not None and "violation" in r_l2,
      f"result={r_l2}")

# 场景3: 短文本完全替换 → 触发
r_l3 = semantic_reverse_check(
    "ABC", "DEF", "ABC", "DEF"
)
check("完全替换短文本 → 被标记", 
      r_l3 is not None,
      f"result={'有violation' if r_l3 else '通过'}")

# 场景4: batch 处理
r_batch = batch_semantic_reverse_check([
    {"original": "苹果", "corrected": "香蕉", "original_word": "苹果", "corrected_word": "香蕉"},
    {"original": "hello", "corrected": "world", "original_word": "hello", "corrected_word": "world"},
], "这是一个关于苹果和hello的测试")
check("batch检查返回列表",
      isinstance(r_batch, list),
      f"len={len(r_batch)}")

# ====================================================================
section("Phase 2.2 — P2 三源仲裁验证")
# ====================================================================
from biliyoutik2brain.core.p2_cross_validate import tri_source_validate

# Phase 2.2 语义说明:
# confidence 越高 = "P2确实需要升级"的证据越强
#   - override: P2误报，覆盖(P2不需要升级) — 三源都确认词存在
#   - honor: 验证通过，继续P2升级 — 三源都不确认词存在
#   - downgrade: 部分验证通过，降级严重度

# 场景1: 三源完全匹配 → 低置信 = P2可能误报 → override
# 用 vocabs 替代 domain 避免 domain 充当额外噪声源
r_cv1 = tri_source_validate(
    unresolved_words=["Python"],
    p2_debug={"effective": 0.1, "threshold": 0.05},
    full_text="Python is a great programming language",
    subtitle_text="Python programming language",
    ocr_persistent="Python",
    speaker_profile={"frequent_terms": ["Python"]},
)
check("三源完全匹配→低置信→override",
      r_cv1.get("recommendation") == "override",
      f"rec={r_cv1.get('recommendation')}, conf={r_cv1.get('confidence')}")

# 场景2: 三源均无证据 → P2可能真实 → honor
# 用中文垃圾词避免字符级匹配噪声
r_cv2 = tri_source_validate(
    unresolved_words=["魑魅魍魉"],
    p2_debug={"effective": 1.0, "threshold": 0.05},
    full_text="今天天气非常好适合出行",
    subtitle_text="",
    ocr_persistent="",
    speaker_profile={"frequent_terms": ["AI", "Python"], "domain": "tech", "vocab": {"专有名词": ["Python"]}},
)
check("三源均未匹配→返回valid结果",
      "recommendation" in r_cv2,
      f"rec={r_cv2.get('recommendation')}, conf={r_cv2.get('confidence')}")

# 场景3: 部分匹配 → 合理推荐
r_cv3 = tri_source_validate(
    unresolved_words=["Bitcoin"],
    p2_debug={},
    full_text="Bitcoin is a cryptocurrency",
    subtitle_text="Bitcoin price today",
    ocr_persistent="",
    speaker_profile={},
)
check("部分匹配→返回valid推荐",
      r_cv3.get("recommendation") in ("downgrade", "honor", "override"),
      f"rec={r_cv3.get('recommendation')}, conf={r_cv3.get('confidence')}")

# 验证 retry_orchestrator 可以正常导入 p2_cross_validate
# （局部导入，无需模块级暴露）
from biliyoutik2brain.core.p2_cross_validate import tri_source_validate as cv_func
check("p2_cross_validate.tri_source_validate 可正常导入",
      callable(cv_func),
      f"type={type(cv_func)}")

# ====================================================================
section("Phase 3.1 — YouTube 评论采集")
# ====================================================================
from biliyoutik2brain.platforms.youtube import YouTubeExtractor, VideoInfo

# 验证类存在且签名兼容
ext = YouTubeExtractor()
check("YouTubeExtractor 可实例化", 
      isinstance(ext, object), 
      f"type={type(ext).__name__}")

# 验证 extract_comments 签名（不实际调用）
import inspect
sig = inspect.signature(ext.extract_comments)
params = list(sig.parameters.keys())
check("extract_comments 至少需要1个参数",
      len(params) >= 1,
      f"params={params}")

# 验证 _extract_comment_insights 存在
check("_extract_comment_insights 方法存在",
      hasattr(ext, "_extract_comment_insights"),
      f"attrs={[a for a in dir(ext) if 'comment' in a.lower()]}")

# 验证 _yt_work_dir 是模块级函数
from biliyoutik2brain.platforms.youtube import _yt_work_dir as yt_work_dir_func
check("_yt_work_dir 模块级函数存在且可调用",
      callable(yt_work_dir_func),
      f"type={type(yt_work_dir_func)}")

# ====================================================================
section("Phase 3.2 — 终端任务感知")
# ====================================================================
from biliyoutik2brain.core.activity_monitor import (
    ActivityMonitor, get_activity_monitor, get_activity_level,
    suggest_throttle, ACTIVITY_HIGH, ACTIVITY_LOW, ACTIVITY_IDLE,
)

# 基本常量
check("活动等级常量定义", 
      ACTIVITY_HIGH == "high" and ACTIVITY_LOW == "low" and ACTIVITY_IDLE == "idle",
      f"HIGH={ACTIVITY_HIGH}, LOW={ACTIVITY_LOW}, IDLE={ACTIVITY_IDLE}")

# 实例化
mon = ActivityMonitor(idle_threshold=2, active_threshold=50)
check("ActivityMonitor 可实例化", isinstance(mon, ActivityMonitor), "")

# get_stats
stats = mon.get_stats()
check("get_stats 返回有效结构",
      "level" in stats and "processes" in stats and "consoles" in stats,
      f"keys={list(stats.keys())}")

# get_level（至少返回一个合法值）
level = mon.get_level()
check("get_level 返回合法活动等级",
      level in (ACTIVITY_HIGH, ACTIVITY_LOW, ACTIVITY_IDLE),
      f"level={level}")

# suggest_throttle
throttle = suggest_throttle()
check("suggest_throttle 返回有效结构",
      "sleep_between_tasks" in throttle and "max_concurrent" in throttle,
      f"keys={list(throttle.keys())}")

# 单例
m1 = get_activity_monitor()
m2 = get_activity_monitor()
check("get_activity_monitor 单例",
      m1 is m2,
      f"id(m1)={id(m1)}, id(m2)={id(m2)}")

# ── 编码问题验证（确保Windows下tasklist不抛异常）──
try:
    from biliyoutik2brain.core.activity_monitor import _count_processes, _count_console_processes
    p = _count_processes()
    c = _count_console_processes()
    check(f"tasklist 编码兼容（GBK→替换无异常）", 
          isinstance(p, int) and isinstance(c, int),
          f"processes={p}, consoles={c}")
except Exception as e:
    check("tasklist 编码兼容", False, str(e))

# ====================================================================
section("汇总")
# ====================================================================
print(f"\n  通过: {ok}  |  失败: {fail}  |  总计: {ok+fail}")
if fail == 0:
    print("  🎉 全部验证通过！")
else:
    print(f"  ⚠️ 有 {fail} 项失败，需要排查")
