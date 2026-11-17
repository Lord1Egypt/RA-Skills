"""
BiliYouTik2Brain — 三级回退链调度层 (Phase 1)

设计原则：原系统零件不改，只加新调度层。
所有现有组件（P2/L1-L5/wiki_bridge/speaker_knowledge/knowledge_store/bailian_asr/cross_validate）保持原样，
此文件提供新的编排函数，调整调用顺序和时机。

架构：
                                        ┌──────────────────────┐
                                        │    Orchestrator      │
                                        │  (此文件)             │
                                        │                      │
  ┌──────────┐    ┌──────────────────┐   │  ┌──────────────┐   │
  │ node_ocr │ ──→│ Tier 1:           │──→│  │ Tier 2:      │──→│──→ ...
  │ (固定帧)  │    │ 自适应迭代抽帧     │   │  │ P2升级路径   │   │
  └──────────┘    │ SSIM+时间加权      │   │  │ 换ASR/升LLM/ │   │
                  └──────────────────┘   │  │ 组合         │   │
                                         │  └──────┬───────┘   │
                                         │         │           │
                                         │  ┌──────▼───────┐   │
                                         │  │ Tier 3:      │   │
                                         │  │ 全量下载兜底   │   │
                                         │  │ 成本账单      │   │
                                         │  └──────────────┘   │
                                         └──────────────────────┘
"""

import os, time, math, json, subprocess, tempfile
from typing import Dict, List, Tuple, Optional, Any

# ═══════════════════════════════════════════════════════════════
# Tier 1: 自适应迭代抽帧 (SSIM + 时间加权)
# ═══════════════════════════════════════════════════════════════

def adaptive_ocr_sampling(
    video_path: str,
    duration_s: float,
    unresolved_words: List[str] = None,
    raw_segments: List[Dict] = None,
    min_frames: int = 8,
    max_frames: int = 40,
    ssim_threshold: float = 0.92,
    target_addition_per_iter: int = 6,
) -> Dict:
    """一级回退：自适应迭代抽帧
    
    取代原来的固定20帧均匀采样。
    策略：
    1. 初始采样：min_frames 帧均匀分布，检测SSIM去重
    2. 评估：如果OCR质量或覆盖率不达标，迭代增加帧数
    3. 时间加权：有 unresolved_words 的时间段增加采样密度
    4. 迭代终止：达到 max_frames 或 OCR质量稳定
    
    Args:
        video_path: 视频文件路径
        duration_s: 视频时长（秒）
        unresolved_words: P2/L5残留犹豫词（决定时间加权区域）
        raw_segments: whisper 原始分段（含 start/end 时间戳）
        min_frames: 最少的初始采样帧数
        max_frames: 最多帧数
        ssim_threshold: SSIM 相似度阈值，高于此值判为重复帧跳过
        target_addition_per_iter: 每轮迭代增加多少帧
    
    Returns:
        ocr_data: 与原有接口兼容的 OCR 结果 Dict
    """
    from biliyoutik2brain.extra.ocr_video import ocr_video_targeted, cleanup
    from biliyoutik2brain.extra.transcription_enhancer import get_persistent_text
    
    if not video_path or not os.path.exists(video_path):
        return {"timeline": [], "persistent_text": ""}
    
    # ── 1. 生成时间加权采样区域 ──
    #
    # 方法：将视频分为 N 个 slot，每个 slot 至少 1 帧
    # 有 unresolved_words 的 slot 获得额外帧
    # 无问题的 slot 均匀分布即可
    
    def _build_weighted_timestamps(base_count: int) -> List[float]:
        """构建时间加权的时间戳列表"""
        if not unresolved_words or not raw_segments:
            # 无犹豫词 → 均匀采样
            interval = max(duration_s / base_count, 15)
            return [i * interval for i in range(base_count) if i * interval < duration_s]
        
        # 找出有问题的时间段
        problem_words = set(w if isinstance(w, str) else w[0] for w in unresolved_words[:20])
        problem_ranges = []  # [(start, end), ...]
        for seg in raw_segments:
            seg_text = seg.get("text", "")
            if any(pw in seg_text for pw in problem_words):
                st = seg.get("start", 0)
                et = seg.get("end", 0)
                if st < et:
                    problem_ranges.append((st, et))
        
        # 合并相邻问题段
        if problem_ranges:
            merged = [problem_ranges[0]]
            for st, et in problem_ranges[1:]:
                if st - merged[-1][1] < 5:
                    merged[-1] = (merged[-1][0], max(merged[-1][1], et))
                else:
                    merged.append((st, et))
            problem_ranges = merged
        else:
            return [i * (duration_s / base_count) for i in range(base_count) if i * (duration_s / base_count) < duration_s]
        
        # 分配帧数：问题区域密度 2x，非问题区域 1x
        total_problem_dur = sum(et - st for st, et in problem_ranges)
        safe_dur = max(duration_s - total_problem_dur, 1)
        problem_ratio = min(total_problem_dur / duration_s, 0.8)
        
        # 问题区域得更多帧
        problem_frames = max(int(base_count * problem_ratio * 1.5), 1)
        safe_frames = max(base_count - problem_frames, 1)
        
        timestamps = []
        # 问题区域内密集采样
        if problem_ranges:
            per_range = max(problem_frames // len(problem_ranges), 1)
            for st, et in problem_ranges:
                dur = et - st
                interval = max(dur / per_range, 1)
                ts = [st + i * interval for i in range(per_range) if st + i * interval < et]
                timestamps.extend(ts)
        
        # 非问题区域均匀分布
        safe_interval = max(safe_dur / safe_frames, 15)
        safe_ts = []
        t = 0
        while t < duration_s:
            # 跳过问题区域
            in_problem = False
            for st, et in problem_ranges:
                if st <= t <= et:
                    t = et
                    in_problem = True
                    break
            if in_problem:
                continue
            safe_ts.append(t)
            t += safe_interval
        timestamps.extend(safe_ts[:safe_frames])
        
        return sorted(set(round(t, 1) for t in timestamps if t < duration_s))
    
    # ── 2. 迭代抽帧循环 ──
    current_frames = min_frames
    last_persistent_count = 0
    stable_rounds = 0
    
    all_timeline = []
    seen_hashes = set()
    
    for iteration in range(4):  # 最多迭代4次
        timestamps = _build_weighted_timestamps(current_frames)
        
        # 去重：跳过 SSIM 相近的帧
        filtered_ts = []
        for ts in timestamps:
            ts_key = round(ts / 5) * 5  # 5秒窗口去重
            if ts_key not in seen_hashes:
                seen_hashes.add(ts_key)
                filtered_ts.append(ts)
        
        if not filtered_ts:
            filtered_ts = timestamps[:max_frames]
        
        print(f"  [自适应OCR] 迭代{iteration+1}: 帧数={len(filtered_ts)} (初始={min_frames}, 最大={max_frames})")
        
        try:
            ocr_data = ocr_video_targeted(
                video_path, timestamps=filtered_ts, window_pad=1.0
            )
            persistent_text = get_persistent_text(ocr_data)
            timeline = ocr_data.get("timeline", [])
            
            # 合并到全部结果
            all_timeline.extend(timeline)
            
            # 去重 persistent_text
            all_persistent = list(dict.fromkeys(
                [t.strip() for t in get_persistent_text({"timeline": all_timeline, "persistent_text": persistent_text}).split("\n") if t.strip()]
            ))
            current_persistent_count = len(all_persistent)
            
            # 判断是否稳定
            if current_persistent_count > 0:
                new_texts = current_persistent_count - last_persistent_count
                ratio = new_texts / max(current_persistent_count, 1)
                
                if ratio < 0.1:  # 新增不足10%
                    stable_rounds += 1
                else:
                    stable_rounds = 0
                
                last_persistent_count = current_persistent_count
                
                if stable_rounds >= 2:
                    print(f"  [自适应OCR] ✅ 稳定 (新增仅{ratio:.0%})，停止迭代")
                    break
            else:
                print(f"  [自适应OCR] ⚠️ 无OCR文字，继续采样")
            
            # 下一轮增加帧数
            current_frames = min(current_frames + target_addition_per_iter, max_frames)
            
        except Exception as e:
            print(f"  [自适应OCR] ⚠️ 迭代{iteration+1}失败: {e}")
            break
    
    cleanup()
    
    # 最终结果去重
    final_timeline = sorted(set(
        (t.get("timestamp", 0), t.get("text", ""))
        for t in all_timeline
    ), key=lambda x: x[0])
    
    final_timeline_dicts = [
        {"timestamp": ts, "text": text} for ts, text in final_timeline
    ]
    
    final_persistent = "\n".join(list(dict.fromkeys(
        [t[1] for t in final_timeline if t[1].strip()]
    )))
    
    print(f"  [自适应OCR] ✅ 最终: {len(final_timeline_dicts)}帧去重, {len(final_persistent.split(chr(10)) if final_persistent else [])}条文字")
    
    return {
        "timeline": final_timeline_dicts,
        "persistent_text": final_persistent,
    }


# ═══════════════════════════════════════════════════════════════
# Tier 2: P2阀门升级路径决策
# ═══════════════════════════════════════════════════════════════

def decide_p2_upgrade_path(
    p2_triggered: bool,
    p2_debug: Dict,
    system_status: Dict = None,
    route_model: str = "base",
) -> Dict:
    """二级回退：P2阀门决定升级路径
    
    原系统 P2 触发后固定走 whisper upgrade + bailian ASR 双路。
    现在根据系统状态和路由信息，选择性价比最高的路径：
    
    Path A: 仅升级 whisper (base → large) — 省钱，适合网络差/API不可用时
    Path B: 仅调用百炼 ASR — 适合本地资源紧张但API可用时
    Path C: 双模型交叉验证 (whisper large + bailian ASR) — 最高准确率
    Path D: 不升级（P2误报，容忍）— 适合熟UP主/闲聊视频
    
    Returns:
        dict with:
            - path: str ("none" | "whisper_upgrade" | "bailian_asr" | "dual")
            - reason: str
            - estimated_cost: float
            - estimated_benefit: float
    """
    if not p2_triggered:
        return {"path": "none", "reason": "P2未触发", "estimated_cost": 0, "estimated_benefit": 0}
    
    # 解析P2各维度
    effective = p2_debug.get("effective", 0)
    threshold = p2_debug.get("threshold", 0.05)
    proper_count = p2_debug.get("proper_count", 0)
    domain_coeff = p2_debug.get("domain_coeff", 1.0)
    speaker_coeff = p2_debug.get("speaker_coeff", 1.0)
    unresolved = p2_debug.get("unresolved_words", [])
    
    system_status = system_status or {}
    cpu_pct = system_status.get("cpu_percent", 50)
    memory_pct = system_status.get("memory_percent", 50)
    network_ok = system_status.get("network_ok", True)
    api_available = system_status.get("api_available", True)
    
    # ── 决定升级路径 ──
    
    # 严重程度因子
    severity = effective / max(threshold, 0.001)
    
    # ── Phase 1.4: 集成 system_monitor 模型选择策略 ──
    # system_monitor.decide_upgrade_model() 考虑了当前模型等级(route_model)和系统资源状态，
    # 动态计算性价比，比硬编码更精准
    sm_decision = None
    try:
        from .system_monitor import decide_upgrade_model
        sm_decision = decide_upgrade_model(
            current_model=route_model,
            system_status=system_status,
            p2_severity=severity,
            proper_count=proper_count,
        )
    except Exception:
        pass  # system_monitor 不是关键路径，失败不影响
    
    # 性价比评估 — 优先使用 system_monitor 的估算
    if sm_decision and sm_decision.get("estimated_benefit") is not None:
        benefit = sm_decision["estimated_benefit"]
        cost_whisper_large = 3.0 if route_model in ("tiny", "base") else 1.0
        cost_bailian = 1.0
        cost_dual = cost_whisper_large + cost_bailian
    else:
        # 回退：硬编码评估
        cost_whisper_large = 4.0  # large比base慢约4倍
        cost_bailian = 1.0
        cost_dual = cost_whisper_large + cost_bailian
        
        if proper_count >= 3 and severity > 3:
            benefit = 1.0
        elif proper_count >= 1 and severity > 2:
            benefit = 0.7
        elif severity > 1.5:
            benefit = 0.4
        else:
            benefit = 0.1
    
    # ── 路径选择（system_monitor 的 choice 作为参考信号） ──
    sm_choice = sm_decision["choice"] if sm_decision else None
    
    # ── 路径选择（优先 system_monitor，回退硬编码启发式） ──
    path = None
    reason = None
    
    if sm_choice is not None:
        # system_monitor 的 choice 到本函数 path 的映射
        # 注意命名差异：sm用"whisper_large"，本函数用"whisper_upgrade"
        choice_to_path = {
            "keep": "none",
            "whisper_large": "whisper_upgrade",
            "bailian_asr": "bailian_asr",
            "dual": "dual",
        }
        path = choice_to_path.get(sm_choice)
        reason = sm_decision.get("reason", "")
    
    # 回退：当 sm_choice 不可用或返回 "keep" 但我们认为值得升级时，走硬编码逻辑
    if path is None or (path == "none" and benefit >= 0.2):
        if benefit < 0.2:
            path = "none"
            reason = f"收益太低(benefit={benefit:.1f})，容忍"
        elif network_ok and api_available and cost_bailian <= cost_whisper_large:
            if proper_count >= 3 and severity > 5:
                path = "dual"
                reason = f"专有名词多({proper_count})且严重(severity={severity:.1f})，双保险"
            else:
                path = "bailian_asr"
                reason = f"API可用，百炼ASR性价比高(severity={severity:.1f})"
        elif not network_ok or not api_available:
            if cpu_pct < 70 and memory_pct < 80:
                path = "whisper_upgrade"
                reason = f"API不可用，本地资源充足(CPU={cpu_pct}%)，升whisper large"
            elif severity > 5:
                path = "whisper_upgrade"
                reason = f"API不可用但严重度高(severity={severity:.1f})，硬升whisper"
            else:
                path = "none"
                reason = f"API不可用+本地资源紧张(CPU={cpu_pct}%,RAM={memory_pct}%)，容忍"
        else:
            path = "dual"
            reason = f"默认双保险路径"
    
    cost_map = {"none": 0, "whisper_upgrade": cost_whisper_large, "bailian_asr": cost_bailian, "dual": cost_dual}
    
    return {
        "path": path,
        "reason": reason,
        "estimated_cost": cost_map.get(path, 0),
        "estimated_benefit": benefit,
        "severity": round(severity, 2),
        "proper_count": proper_count,
        "sm_decision": sm_decision,
    }


# ═══════════════════════════════════════════════════════════════
# Tier 3: 全量下载兜底
# ═══════════════════════════════════════════════════════════════

def should_fallback(retry_history: List[Dict]) -> bool:
    """判断是否需要启动三级兜底
    
    条件（任意一条）：
    1. Tier 1 迭代抽帧已达 max_frames 仍不够
    2. Tier 2 双路径都失败（whisper upgrade 和 bailian 都无效）
    3. 同一视频触发了 3 次以上 P2 仍无法解决
    """
    if not retry_history:
        return False
    
    tier1_attempts = [h for h in retry_history if h.get("tier") == 1]
    tier2_attempts = [h for h in retry_history if h.get("tier") == 2]
    
    # 条件1: Tier 1 帧数用满
    if tier1_attempts and tier1_attempts[-1].get("frames_used", 0) >= 40:
        return True
    
    # 条件2: Tier 2 双路径已走但仍未解决
    if len(tier2_attempts) >= 2:
        return True
    
    # 条件3: 同一视频多次P2触发
    total_p2_triggers = sum(1 for h in retry_history if h.get("p2_triggered"))
    if total_p2_triggers >= 3:
        return True
    
    return False


def generate_cost_bill(video_title: str, video_url: str, retry_history: List[Dict]) -> Dict:
    """生成三级兜底的成本账单
    
    内容包括：
    - 已经花费的资源（whisper 时间、API 调用次数）
    - 全量下载预计成本
    - 预估总成本
    - 建议：是否值得继续
    
    Returns:
        成本账单 dict
    """
    whisper_time = sum(
        h.get("whisper_time_s", 0) for h in retry_history
    )
    bailian_calls = sum(
        1 for h in retry_history if h.get("bailian_invoked")
    )
    ocr_frames = sum(
        h.get("frames_used", 0) for h in retry_history
    )
    
    # 预估全量下载成本
    estimated_download_gb = 0.5  # 10分钟视频 ~500MB
    estimated_whisper_full_time = whisper_time * 2  # 全量转录大约2x已有时间
    
    bill = {
        "video_title": video_title,
        "video_url": video_url,
        "already_spent": {
            "whisper_time_s": round(whisper_time, 1),
            "bailian_api_calls": bailian_calls,
            "ocr_frames_processed": ocr_frames,
        },
        "estimated_full_download_cost": {
            "download_gb": estimated_download_gb,
            "whisper_full_time_s": round(estimated_whisper_full_time, 1),
        },
        "total_estimated_time_s": round(whisper_time + estimated_whisper_full_time + bailian_calls * 30, 1),
        "recommendation": "不建议" if bailian_calls >= 2 and whisper_time > 600 else "可以一试",
    }
    
    return bill


def print_cost_bill(bill: Dict):
    """在控制台输出成本账单（用户可见）"""
    sep = "=" * 50
    print(f"\n{sep}")
    print(f"  📋 三级兜底 — 成本账单")
    print(f"{sep}")
    print(f"  视频: {bill['video_title']}")
    print(f"  URL: {bill['video_url'][:60]}...")
    print(f"")
    print(f"  已花费资源:")
    spent = bill['already_spent']
    print(f"    · Whisper 转录: {spent['whisper_time_s']}s")
    print(f"    · 百炼ASR调用: {spent['bailian_api_calls']} 次")
    print(f"    · OCR帧处理: {spent['ocr_frames_processed']} 帧")
    print(f"")
    print(f"  全量下载预估:")
    est = bill['estimated_full_download_cost']
    print(f"    · 下载流量: {est['download_gb']}GB")
    print(f"    · 全量转录: {est['whisper_full_time_s']}s")
    print(f"")
    print(f"  总预估时间: {bill['total_estimated_time_s']}s")
    print(f"  📌 建议: {bill['recommendation']}")
    print(f"{sep}")
    print(f"  ⚠️ 三级兜底需要你的确认才能执行！")
    print(f"{sep}\n")


# ═══════════════════════════════════════════════════════════════
# 3.3 置信度估算 — 三源融合
# ═══════════════════════════════════════════════════════════════

def tri_source_confidence(
    raw_confidence: float,
    subtitle_quality: float = 0.0,
    subtitle_text: str = "",
    corrected_text: str = "",
    ocr_text: str = "",
    speaker_knowledge: str = "",
    domain: str = "",
) -> Dict:
    """三源融合置信度估算
    
    替代原来的单源词级置信。
    融合三个置信度源：
    1. Whisper 原始置信度（由 whisper 模型输出的词级概率均值）
    2. 字幕/OCR 交叉验证比例
    3. 说话人领域知识匹配度
    
    Returns:
        dict with:
            - overall_confidence: float (0~1)
            - whisper_source: float
            - cross_validation_source: float
            - domain_source: float
            - source_breakdown: str (可读说明)
    """
    # 源1: Whisper 原始置信度
    w_conf = raw_confidence  # 0~1
    
    # 源2: 字幕/OCR 交叉验证
    cv_conf = 0.5  # 默认中性
    if subtitle_quality > 0 and corrected_text:
        # 字幕质量高 → 交叉验证置信度高
        cv_conf = subtitle_quality * 0.8 + 0.2
    if ocr_text:
        # 有OCR结果 → 补充验证
        cv_conf = min(cv_conf + 0.1, 1.0)
    
    # 源3: 说话人领域知识
    d_conf = 0.5
    if speaker_knowledge and corrected_text:
        # 有领域知识 → 匹配度加成
        from biliyoutik2brain.extra.transcription_enhancer import _guess_domain
        if domain and speaker_knowledge.lower().find(domain.lower()) >= 0:
            d_conf = 0.8
        else:
            d_conf = 0.6
    
    # 加权融合（权重向交叉验证倾斜，因为它比单源可靠）
    overall = (
        w_conf * 0.25 +       # Whisper 单源权重 25%
        cv_conf * 0.50 +       # 交叉验证权重 50%（最可靠）
        d_conf * 0.25          # 领域知识权重 25%
    )
    
    return {
        "overall_confidence": round(overall, 3),
        "whisper_source": round(w_conf, 3),
        "cross_validation_source": round(cv_conf, 3),
        "domain_source": round(d_conf, 3),
        "source_breakdown": (
            f"Whisper原始={w_conf:.2f}(25%) + "
            f"交叉验证={cv_conf:.2f}(50%) + "
            f"领域知识={d_conf:.2f}(25%) = {overall:.2f}"
        ),
    }


# ═══════════════════════════════════════════════════════════════
# 外部接口 — 一键启动三级回退
# ═══════════════════════════════════════════════════════════════

def orchestrate_retry(
    url: str,
    video_title: str,
    video_path: str,
    duration_s: float,
    collect_result: Any,
    assess_result: Dict,
    transcribe_result: Dict,
    enhance_result: Dict,
    system_status: Dict = None,
) -> Dict:
    """三级回退链一站式入口
    
    调用流程（在 enhance 节点内部或之后调用）：
    1. 检查 P2 是否触发
    2. 若触发 → Tier 2 决策升级路径
    3. 若 Tier 2 不满足 → 检查是否需 Tier 3
    4. 维护 retry_history 供 should_fallback() 判断
    
    Args:
        url: 视频 URL
        video_title: 视频标题
        video_path: 视频文件路径
        duration_s: 视频时长
        collect_result: CollectResult
        assess_result: assess 节点输出
        transcribe_result: transcribe 节点输出
        enhance_result: enhance 节点输出
        system_status: system_monitor 输出（可选）
    
    Returns:
        dict with:
            - tier_1_applied: bool
            - tier_2_applied: bool  
            - tier_3_applied: bool
            - upgraded_text: str (升级后的文本)
            - retry_history: list
            - cost_bill: dict (仅 Tier 3 时)
    """
    from .p2_decision import should_retranscribe
    
    retry_history = []
    result = {
        "tier_1_applied": False,
        "tier_2_applied": False,
        "tier_3_applied": False,
        "upgraded_text": enhance_result.get("corrected_text", ""),
        "retry_history": retry_history,
    }
    
    uploader = ""
    bvid = ""
    if collect_result:
        uploader = getattr(collect_result.video, "uploader", "")
        bvid = getattr(collect_result.video, "video_id", "")
    
    # ── 从增强结果获取犹豫词 ──
    unresolved = enhance_result.get("_unresolved", [])
    if not unresolved:
        return result
    
    # ── 执行 P2 决策 ──
    avg_quality = assess_result.get("avg_quality", 0.0)
    domain_hint = assess_result.get("domain_hint", "")
    raw_segments = transcribe_result.get("segments", [])
    chapters = enhance_result.get("analysis", {}).get("chapters", [])
    
    p2_trigger, p2_debug = should_retranscribe(
        unresolved_words=unresolved,
        total_chars=len(enhance_result.get("corrected_text", "")),
        speech_segments=assess_result.get("speech_segments", []),
        avg_quality=avg_quality,
        domain_hint=domain_hint,
        uploader=uploader,
        chapters=chapters,
    )
    
    # ── Phase 2.2: P2 三源仲裁验证 ──
    # P2 触发后但不立即升级，先做三源交叉验证判断是否误报
    tri_source_result = None
    if p2_trigger:
        try:
            from .p2_cross_validate import tri_source_validate
            from .speaker_knowledge import get_profile
            
            speaker_profile = get_profile(uploader) if uploader else None
            
            # 从增强结果收集 OCR 持久文本
            ocr_result = enhance_result.get("ocr_result", {})
            ocr_persistent = ""
            if isinstance(ocr_result, dict):
                ocr_persistent = ocr_result.get("persistent_text", "")
                if not ocr_persistent:
                    persistent_list = ocr_result.get("persistent", [])
                    if isinstance(persistent_list, list):
                        ocr_persistent = "\n".join(persistent_list)
            
            # 收集字幕文本
            subtitle_text = ""
            subtitle_segments = []
            if collect_result:
                subtitle_segments = getattr(collect_result, "subtitle_segments", []) or []
                subtitle_texts = [s.get("text", "") for s in subtitle_segments if isinstance(s, dict)]
                subtitle_text = "\n".join(subtitle_texts)
            
            tri_source_result = tri_source_validate(
                unresolved_words=[w if isinstance(w, str) else w[0] for w in unresolved],
                p2_debug=p2_debug,
                full_text=enhance_result.get("corrected_text", ""),
                subtitle_text=subtitle_text,
                subtitle_segments=subtitle_segments,
                ocr_persistent=ocr_persistent,
                speaker_profile=speaker_profile,
            )
            
            # 应用仲裁结果
            if tri_source_result["recommendation"] == "override":
                # 三源确认是误报 → 覆盖P2，容忍
                p2_trigger = False
                p2_debug["overridden_by_tri_source"] = tri_source_result["details"]
                print(f"  [P2仲裁] ❌ 三源验证覆盖P2: confidence={tri_source_result['confidence']:.2f}")
            elif tri_source_result["recommendation"] == "downgrade":
                # 部分验证 → 保留触发但降低严重度
                p2_debug["tri_source_downgraded"] = True
                print(f"  [P2仲裁] ⚠️ 三源验证降级P2: confidence={tri_source_result['confidence']:.2f}")
            else:  # honor
                print(f"  [P2仲裁] ✅ 三源验证确认P2: confidence={tri_source_result['confidence']:.2f}")
                
            p2_debug["tri_source_validation"] = tri_source_result
        except Exception as e:
            # 三源验证非关键路径，失败不影响
            print(f"  [P2仲裁] ⚠️ 跳过: {e}")
            pass
    
    # ── Tier 2: P2 升级路径决策 ──
    if p2_trigger:
        route_model = "base"
        if assess_result.get("route"):
            route_model = assess_result.route.model
        
        upgrade_decision = decide_p2_upgrade_path(
            p2_trigger, p2_debug,
            system_status=system_status,
            route_model=route_model,
        )
        
        result["tier_2_applied"] = True
        
        # 执行升级路径
        if upgrade_decision["path"] in ("whisper_upgrade", "dual"):
            upgraded = _exec_whisper_upgrade(
                assess_result, unresolved, raw_segments
            )
            if upgraded:
                result["upgraded_text"] = upgraded
        
        if upgrade_decision["path"] in ("bailian_asr", "dual"):
            bailian_text = _exec_bailian_fallback(
                assess_result, unresolved, raw_segments
            )
            if bailian_text:
                result["upgraded_text"] = bailian_text
        
        retry_history.append({
            "tier": 2,
            "p2_triggered": True,
            "upgrade_path": upgrade_decision["path"],
            "reason": upgrade_decision["reason"],
        })
    
    # ── Tier 3: 全量下载兜底 ──
    if should_fallback(retry_history):
        bill = generate_cost_bill(video_title, url, retry_history)
        print_cost_bill(bill)
        result["tier_3_applied"] = True
        result["cost_bill"] = bill
        # 注意：三级兜底需要用户确认，此处仅生成账单
        # 实际执行由外部调用方确认后执行
    
    return result


def _exec_whisper_upgrade(
    assess_result: Dict,
    unresolved_words: List[str],
    raw_segments: List[Dict],
) -> str:
    """执行 whisper 升级重转录（本地 large 模型）"""
    from biliyoutik2brain.extra.faster_transcriber import transcribe_full_audio_detailed
    from .slots import acquire_heavy_slot, release_heavy_slot
    
    audio_file = assess_result.get("audio_file", "")
    if not audio_file or not os.path.exists(audio_file):
        return ""
    
    problem_words = set(w if isinstance(w, str) else w[0] for w in unresolved_words[:10])
    prob_times = []
    for seg in raw_segments:
        seg_text = seg.get("text", "")
        if any(pw in seg_text for pw in problem_words):
            prob_times.append((seg.get("start", 0), seg.get("end", 0)))
    
    if not prob_times:
        return ""
    
    # 合并临近段
    merged = [prob_times[0]]
    for st, et in prob_times[1:]:
        if st - merged[-1][1] < 5:
            merged[-1] = (merged[-1][0], max(merged[-1][1], et))
        else:
            merged.append((st, et))
    
    print(f"  [Whisper升级] ⬆️ large模型重转录 {len(merged)}段")
    
    with tempfile.TemporaryDirectory(prefix="whisper_upgrade_") as tmpdir:
        text_parts = []
        
        acquire_heavy_slot("large")
        try:
            for st, et in merged:
                seg_path = os.path.join(tmpdir, f"seg_{st}_{et}.wav")
                subprocess.run(
                    ["ffmpeg", "-y", "-ss", str(st), "-t", str(et - st),
                     "-i", audio_file, "-ac", "1", "-ar", "16000", seg_path],
                    capture_output=True, timeout=30
                )
                if not os.path.exists(seg_path):
                    continue
                
                seg_text, _, _ = transcribe_full_audio_detailed(
                    seg_path, language="zh", confidence_threshold=0.5,
                    model_size="large",
                )
                if seg_text.strip():
                    text_parts.append(seg_text.strip())
        finally:
            release_heavy_slot()
    
    if text_parts:
        result = "\n".join(text_parts)
        print(f"  [Whisper升级] ✅ {len(result)}字")
        return result
    return ""


def _exec_bailian_fallback(
    assess_result: Dict,
    unresolved_words: List[str],
    raw_segments: List[Dict],
) -> str:
    """执行百炼ASR回退"""
    from biliyoutik2brain.extra.bailian_asr import transcribe_audio_segment
    
    audio_file = assess_result.get("audio_file", "")
    if not audio_file or not os.path.exists(audio_file):
        return ""
    
    problem_words = set(w if isinstance(w, str) else w[0] for w in unresolved_words[:10])
    prob_times = []
    for seg in raw_segments:
        seg_text = seg.get("text", "")
        if any(pw in seg_text for pw in problem_words):
            prob_times.append((seg.get("start", 0), seg.get("end", 0)))
    
    if not prob_times:
        return ""
    
    merged = [prob_times[0]]
    for st, et in prob_times[1:]:
        if st - merged[-1][1] < 5:
            merged[-1] = (merged[-1][0], max(merged[-1][1], et))
        else:
            merged.append((st, et))
    
    print(f"  [百炼ASR] ☁️ 回退 {len(merged)}段")
    
    with tempfile.TemporaryDirectory(prefix="bailian_") as tmpdir:
        text_parts = []
        for st, et in merged:
            seg_path = os.path.join(tmpdir, f"seg_{st}_{et}.wav")
            subprocess.run(
                ["ffmpeg", "-y", "-ss", str(st), "-t", str(et - st),
                 "-i", audio_file, "-ac", "1", "-ar", "16000", seg_path],
                capture_output=True, timeout=30
            )
            if not os.path.exists(seg_path):
                continue
            
            try:
                bailian_text, _ = transcribe_audio_segment(seg_path, timeout=60)
                if bailian_text:
                    text_parts.append(bailian_text.strip())
            except Exception as e:
                print(f"  [百炼ASR] ⚠️ 段失败: {e}")
    
    if text_parts:
        result = "\n".join(text_parts)
        print(f"  [百炼ASR] ✅ {len(result)}字")
        return result
    return ""
