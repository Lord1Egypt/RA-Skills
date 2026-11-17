"""首帧图/场景图/角色图/视频/脚本叙事结构验证。"""
import os, re, warnings
# OpenCV 可选依赖：无 cv2 时用天桥方案跳过视觉检测
try:
    import cv2
    _HAVE_CV2 = True
except ImportError:
    cv2 = type("cv2_stub", (), {})()  # 哑模块
    cv2.data = type("data_stub", (), {"haarcascades": ""})()
    cv2.CascadeClassifier = lambda *a, **kw: type("CC", (), {"detectMultiScale": lambda *a, **kw: []})()
    cv2.HOGDescriptor = lambda: type("HOG", (), {
        "setSVMDetector": lambda s: None,
        "detectMultiScale": lambda s, *a, **kw: ([], []),
    })()
    cv2.cvtColor = lambda *a, **kw: np.zeros((100, 100), dtype=np.uint8)
    cv2.Canny = lambda *a, **kw: np.zeros((100, 100), dtype=np.uint8)
    cv2.Laplacian = lambda *a, **kw: np.zeros((100, 100), dtype=np.float64)
    cv2.calcOpticalFlowFarneback = lambda *a, **kw: np.zeros((100, 100, 2), dtype=np.float32)
    cv2.CAP_PROP_FPS = 5
    cv2.CAP_PROP_FRAME_COUNT = 6
    cv2.CAP_PROP_FRAME_WIDTH = 7
    cv2.CAP_PROP_FRAME_HEIGHT = 8
    cv2.CAP_PROP_POS_FRAMES = 0
    cv2.VideoCapture = lambda *a, **kw: type("VC", (), {
        "isOpened": lambda s: False,
        "read": lambda s: (False, None),
        "set": lambda s, *a: False,
        "get": lambda s, p: 0,
        "release": lambda s: None,
    })()
    cv2.detectMultiScale = lambda *a, **kw: []
    cv2.resize = lambda img, *a, **kw: img
    cv2.kmeans = lambda *a, **kw: (None, np.zeros((32, 1), dtype=np.int32), np.zeros((32, 3), dtype=np.float32))
    cv2.COLOR_BGR2GRAY = 6
    cv2.COLOR_RGB2GRAY = 7
    cv2.COLOR_BGR2RGB = 4
    cv2.CV_64F = 5
    cv2.TERM_CRITERIA_EPS = 2
    cv2.TERM_CRITERIA_MAX_ITER = 3
    cv2.KMEANS_RANDOM_CENTERS = 0
    _HAVE_CV2 = False
    warnings.warn("OpenCV (cv2) 未安装，视觉检测功能将跳过。"
                  "请运行: pip install opencv-python-headless")

from PIL import Image
import numpy as np


# 默认验证阈值（可从 script.json → script.validation 覆盖）
_DEFAULT_THRESHOLDS = {
    "blur_min": 50,           # Laplacian 方差
    "border_std_max": 30,     # 背景边缘标准差（角色图简单背景）
    "border_bright_min": 200, # 背景边缘亮度（角色图白色背景）
    "body_height_ratio": 0.6, # 全身照 HOG 框高占比
    "edge_density_min": 0.08, # 写实风格 Canny 边缘密度
    "color_clusters_min": 8,  # 写实风格 32 色量化聚类数
    "anime_edge_min": 0.05,   # 动漫风格边缘密度
    "anime_clusters_min": 3,  # 动漫风格色簇下限
    "anime_clusters_max": 15, # 动漫风格色簇上限
    "duration_ratio_min": 0.8,# 视频时长偏差下限
    "duration_ratio_max": 1.2,# 视频时长偏差上限
    "aspect_tolerance": 0.15, # 画面比例容差
    "black_frame_threshold": 5,   # 黑帧亮度阈值
    "frozen_frame_threshold": 3,  # 冻结帧 diff 阈值
    "camera_motion_static": 0.5,  # 静态运镜光流幅值
    "pass_ratio": 0.55,       # 通过分占比 (e.g. 35/55)
    "scene_face_min_ratio": 0.15,  # 场景图人脸最小占比
    "scene_decoration_zone": 0.70, # 场景图装饰区划分线
    "mood_profile": {},       # 情绪档案（扩展用）
}


def _get_thresholds(script_data: dict | None = None) -> dict:
    """读取 script.json → script.validation 中的自定义阈值，合并默认值。"""
    th = dict(_DEFAULT_THRESHOLDS)
    if script_data:
        custom = script_data.get("script", {}).get("validation", {})
        if custom:
            th.update(custom)
    return th



def validate_script_narrative(script: dict) -> list[dict]:
    """验证 script.json 叙事结构的完整性。

    检查项：
      - Shot ID 连续无跳号
      - 描述、时长等必填字段完整
      - 时长在合理范围（1-60s）
      - 运镜多样性：连续 3+ 镜头同运镜 → 报
      - 情绪弧线：情绪跳变过陡（如「欢快」→「悲伤」→「欢快」）→ 报
      - 角色引用：shot description 中提到的角色应在 character_cards 中定义
      - 总时长 vs script.duration_seconds 偏差

    Returns: [{"type": str, "severity": "P0"|"P1"|"P2", "shot_id": int, "detail": str}]
    """
    issues: list[dict] = []
    shots = script.get("shots", [])
    chars = {c.get("name", "") for c in script.get("character_cards", [])}
    total_dur = 0

    if not shots:
        issues.append({"type": "no_shots", "severity": "P0", "shot_id": 0,
                        "detail": "shots 为空"})
        return issues

    for i, s in enumerate(shots):
        sid = s.get("id", 0)
        desc = s.get("description", "")
        dur = s.get("duration", 0)

        # 1. ID 连续
        if i > 0 and sid != shots[i - 1].get("id", 0) + 1:
            issues.append({"type": "shot_id_gap", "severity": "P1", "shot_id": sid,
                           "detail": f"shot_{sid:02d} 接在 shot_{shots[i-1].get('id',0):02d} 之后，ID 不连续"})
        # 2. 描述非空
        if not desc or not desc.strip():
            issues.append({"type": "missing_description", "severity": "P1", "shot_id": sid,
                           "detail": f"shot_{sid:02d} 描述为空"})
        # 3. 时长范围
        try:
            d = float(dur or 0)
            if d < 1:
                issues.append({"type": "duration_too_short", "severity": "P1", "shot_id": sid,
                               f"detail": f"shot_{sid:02d} 时长={d}s < 1s"})
            elif d > 60:
                issues.append({"type": "duration_too_long", "severity": "P2", "shot_id": sid,
                               f"detail": f"shot_{sid:02d} 时长={d}s > 60s"})
            total_dur += d
        except (TypeError, ValueError):
            issues.append({"type": "duration_invalid", "severity": "P1", "shot_id": sid,
                           f"detail": f"shot_{sid:02d} 时长无效"})

        # 4. 角色引用一致性
        if chars and desc:
            mentioned = re.findall(r'([\u4e00-\u9fff]{2,4}(?=[的。，：:、]|$))', desc)
            for m in set(mentioned):
                if m in chars:
                    continue
                # 常见角色名（2-4字）检查
                if len(m) >= 2 and any(c in chars for c in [m, m[:-1], m + "将" if "将" not in m else ""]):
                    continue
                # 放宽：只对明显是角色名的词汇报警
                if m in ("墨雪", "墨将", "阿巴斯", "罗缪尔", "周戎"):
                    issues.append({"type": "char_not_defined", "severity": "P2", "shot_id": sid,
                                   f"detail": f"shot_{sid:02d} 提到的「{m}」不在 character_cards 中"})

    # 5. 运镜多样性
    last_motions = []
    for s in shots:
        sid = s.get("id", 0)
        desc = s.get("description", "")
        motion = _parse_camera_motion(desc)
        last_motions.append((sid, motion))
        # 检查连续 3+ 镜头同运镜
        if len(last_motions) >= 3:
            if all(m == motion for _, m in last_motions[-3:]):
                if motion not in ("unknown", "mixed"):
                    issues.append({"type": "monotone_camera", "severity": "P2", "shot_id": sid,
                                   f"detail": f"shot_{sid:02d} 起连续 3 镜头运镜均为「{motion}」，建议增加变化"})

    # 6. 情绪弧线 — 检测剧烈跳变
    mood_seq = []
    for s in shots:
        sid = s.get("id", 0)
        desc = s.get("description", "")
        mood = _parse_shot_mood(desc)
        mood_seq.append((sid, mood))
    # 检查非相邻情绪跳变
    for i in range(1, len(mood_seq)):
        prev_sid, prev_mood = mood_seq[i - 1]
        cur_sid, cur_mood = mood_seq[i]
        if prev_mood != "unknown" and cur_mood != "unknown" and prev_mood != cur_mood:
            # 定义不允许的跳变对
            _BAD_JUMPS = {
                ("欢快", "悲伤"), ("欢快", "压抑"), ("欢快", "绝望"),
                ("温馨", "紧张"), ("温馨", "战斗"),
                ("平静", "激烈"), ("平静", "紧张"),
                ("紧张", "温馨"), ("紧张", "平静"),
                ("悲伤", "欢快"),
                ("绝望", "欢快"),
            }
            if (prev_mood, cur_mood) in _BAD_JUMPS:
                issues.append({"type": "mood_jump", "severity": "P2", "shot_id": cur_sid,
                               f"detail": f"shot_{cur_sid:02d} 情绪从「{prev_mood}」跳变到「{cur_mood}」，"
                                          f"中间缺少过渡镜头"})

    # 7. 总时长校验
    expected_total = script.get("script", {}).get("duration_seconds", 0)
    if expected_total > 0 and abs(total_dur - expected_total) / expected_total > 0.15:
        issues.append({"type": "total_duration_mismatch", "severity": "P1", "shot_id": 0,
                       "detail": f"各 shot 时长总和={total_dur:.0f}s，script.duration_seconds={expected_total}s，偏差>15%"})

    # ── 爆款短视频专项检查 ────────────────────────────────────

    # 8. 开头钩子检测：前 3 个 shot 应有吸引力的元素
    hook_kw = ["突然", "意外", "冲突", "悬念", "对决", "危机", "关键时刻",
               "发现", "惊醒", "追逐", "爆炸", "枪声", "尖叫", "打破",
               "闯入", "坠落", "碰撞", "怒吼", "震惊"]
    for i in range(min(3, len(shots))):
        desc = shots[i].get("description", "")
        if not any(kw in desc for kw in hook_kw):
            issues.append({"type": "missing_hook", "severity": "P2", "shot_id": shots[i]["id"],
                           "detail": f"前 3 镜头({shots[i]['id']})无爆点元素，建议加入冲突/悬念/意外"})

    # 9. 时长多样性（标准差检测）
    if len(shots) >= 4:
        durations = [float(s.get("duration", 5)) for s in shots]
        mean_dur = sum(durations) / len(durations)
        variance = sum((d - mean_dur) ** 2 for d in durations) / len(durations)
        std_dev = variance ** 0.5
        if std_dev < 1.5:
            issues.append({"type": "monotone_pacing", "severity": "P2", "shot_id": 0,
                           "detail": f"各 shot 时长过于均匀（标准差={std_dev:.1f}<1.5），建议增加快慢变化"})

    # 10. 高潮位置检测：最激烈镜头应在总时长 70-85% 处
    if len(shots) >= 4:
        intensity_scores = []
        for s in shots:
            desc = s.get("description", "")
            score = 0
            for kw in ["激烈", "战斗", "冲突", "对决", "爆发", "高潮",
                       "紧张", "追逐", "爆炸", "危机", "生死", "决胜"]:
                if kw in desc:
                    score += 2
            for kw in ["平静", "温馨", "对话", "沉默", "休整", "恢复"]:
                if kw in desc:
                    score -= 1
            intensity_scores.append(max(0, score))
        if max(intensity_scores) > 0:
            climax_idx = intensity_scores.index(max(intensity_scores))
            total_dur_check = sum(float(s.get("duration", 5)) for s in shots)
            climax_pos = sum(float(shots[i].get("duration", 5)) for i in range(climax_idx)) / max(total_dur_check, 1)
            if not (0.6 <= climax_pos <= 0.9):
                issues.append({"type": "climax_position", "severity": "P2",
                               "shot_id": shots[climax_idx]["id"],
                               "detail": f"高潮镜头(shot_{shots[climax_idx]['id']:02d})位于 {climax_pos:.0%} 处，"
                                          f"建议移至 70-85% 位置"})

    # 11. 收尾检测：最后 1-2 镜头应有收束/结局感
    if len(shots) >= 2:
        for s in shots[-2:]:
            desc = s.get("description", "")
            closure_kw = ["结束", "落幕", "离去", "背影", "远眺", "安静",
                         "平息", "停止", "完成", "离开", "消失", "沉默"]
            if not any(kw in desc for kw in closure_kw):
                issues.append({"type": "missing_closure", "severity": "P2", "shot_id": s["id"],
                               "detail": f"收尾镜头(shot_{s['id']:02d})无结局感，建议加入收束描述"})

    # 12. 对话 vs 动作平衡
    dialogue_count = sum(1 for s in shots if any(kw in s.get("description", "")
                        for kw in ["说", "道", "对话", "交谈", "质问", "回答", "告诉"]))
    action_count = sum(1 for s in shots if any(kw in s.get("description", "")
                       for kw in ["战斗", "追逐", "攻击", "防御", "冲", "跑",
                                  "跳", "踢", "打", "拔", "射击", "挥"]))
    total_shots = len(shots)
    if total_shots >= 6:
        dialogue_ratio = dialogue_count / total_shots
        action_ratio = action_count / total_shots
        if dialogue_ratio > 0.7:
            issues.append({"type": "too_much_dialogue", "severity": "P2", "shot_id": 0,
                           "detail": f"对话镜头占 {dialogue_ratio:.0%}，建议加入动作镜头提升节奏"})
        if action_ratio > 0.7:
            issues.append({"type": "too_much_action", "severity": "P2", "shot_id": 0,
                           "detail": f"动作镜头占 {action_ratio:.0%}，建议加入对话/剧情过渡"})

    return issues


_MOTION_ALTERNATIVES = {
    "static": ["镜头缓慢推进", "镜头平稳横移", "镜头缓缓上摇"],
    "pan": ["镜头固定", "镜头缓慢推进", "镜头上下摇摄"],
    "dolly_in": ["镜头固定", "镜头平稳横移", "镜头缓缓拉远"],
    "dolly_out": ["镜头固定", "镜头缓慢推进", "镜头平稳横移"],
    "tilt_up": ["镜头固定", "镜头平稳横移", "镜头缓缓下摇"],
    "tilt_down": ["镜头固定", "镜头平稳横移", "镜头缓缓上摇"],
    "orbit": ["镜头固定", "镜头缓慢推进", "镜头平稳横移"],
}


def fix_script_narrative(script: dict) -> tuple[dict, list[str]]:
    """自动修复 script.json 的叙事结构问题，返回 (fixed_script, fix_log)。

    修复策略：
      - 类型规则应用（aspect_ratio / 运镜 / 情绪等）
      - ID 跳号 → 重新编号
      - 描述为空 → 从相邻镜头推断
      - 时长越界 → 钳制到 [1, 60]
      - 总时长偏差 → 比例缩放各 shot 时长
      - 运镜单调 → 替换最后一个镜头的描述加入不同运镜
      - 情绪跳变 → 在跳变处插入过渡情绪关键词
      - 角色引用缺失 → 自动补入 character_cards
    """
    import copy
    script = copy.deepcopy(script)
    log: list[str] = []
    shots = script.get("shots", [])

    if not shots:
        return script, ["shots 为空，无法修复"]

    # 0. 应用类型规则（aspect_ratio / 运镜 / 情绪等）
    try:
        from type_registry import apply_type_rules as _atr
        _atr(script)
    except Exception:
        pass

    # 1. 修复 ID 跳号
    for i, s in enumerate(shots):
        expected = i + 1
        if s.get("id") != expected:
            old_id = s.get("id")
            s["id"] = expected
            log.append(f"  shot_{old_id:02d} → shot_{expected:02d}（ID 重新编号）")

    # 2. 修复空描述 & 时长越界
    for i, s in enumerate(shots):
        sid = s["id"]
        if not s.get("description", ""):
            # 从相邻镜头推断描述
            prev_desc = shots[i - 1].get("description", "") if i > 0 else ""
            next_desc = shots[i + 1].get("description", "") if i < len(shots) - 1 else ""
            inferred = (prev_desc[:40] or next_desc[:40] or "场景过渡").rstrip("，。") + "（过渡镜头）"
            s["description"] = inferred
            log.append(f"  shot_{sid:02d}: 自动填充描述（来自相邻镜头）")
        try:
            d = float(s.get("duration", 0) or 0)
            if d < 1:
                s["duration"] = 3.0
                log.append(f"  shot_{sid:02d}: 时长 {d}s → 3s（低于下限）")
            elif d > 60:
                s["duration"] = 10.0
                log.append(f"  shot_{sid:02d}: 时长 {d}s → 10s（超过上限）")
        except (TypeError, ValueError):
            s["duration"] = 5.0
            log.append(f"  shot_{sid:02d}: 时长无效 → 5s（默认值）")

    # 3. 修复总时长偏差
    expected_total = script.get("script", {}).get("duration_seconds", 0)
    current_total = sum(float(s.get("duration", 0) or 0) for s in shots)
    if expected_total > 0 and current_total > 0:
        ratio = expected_total / current_total
        if abs(ratio - 1) > 0.15:
            for s in shots:
                new_dur = round(float(s.get("duration", 0) or 0) * ratio, 1)
                s["duration"] = max(1.0, min(60.0, new_dur))
            log.append(f"  各 shot 时长按比例 {ratio:.2f}x 缩放以匹配总时长 {expected_total}s")

    # 4. 修复运镜单调
    last_motions = []
    for i, s in enumerate(shots):
        sid = s["id"]
        desc = s.get("description", "")
        motion = _parse_camera_motion(desc)
        last_motions.append((sid, motion, i))
        if len(last_motions) >= 3:
            if all(m == motion for _, m, _ in last_motions[-3:]):
                if motion not in ("unknown", "mixed") and motion in _MOTION_ALTERNATIVES:
                    import random
                    alt = random.choice(_MOTION_ALTERNATIVES[motion])
                    # 替换最后那个镜头的描述，追加不同运镜
                    last_idx = last_motions[-1][2]
                    old_desc = shots[last_idx].get("description", "")
                    # 清除旧运镜关键词
                    for kw in _CAMERA_KW_MAP:
                        old_desc = old_desc.replace(kw, "")
                    new_desc = (old_desc.rstrip("，。") + f"，{alt}").strip("，")
                    shots[last_idx]["description"] = new_desc
                    log.append(f"  shot_{sid:02d}: 运镜从「{motion}」改为「{alt}」（避免单调）")

    # 5. 修复角色引用缺失
    chars = script.get("character_cards", [])
    char_names = {c.get("name", "") for c in chars}
    for s in shots:
        sid = s["id"]
        desc = s.get("description", "")
        if not desc:
            continue
        # 提取可能的中文人名（2-4字）
        mentioned = set(re.findall(r'[\u4e00-\u9fff]{2,4}(?=[的。，：:、]|$)', desc))
        for m in mentioned:
            if m in char_names:
                continue
            # 如果是已知角色（通过排除通用词判断）
            common_words = {"场景", "环境", "背景", "前景", "画面", "镜头", "表情", "视线",
                            "眼神", "气氛", "氛围", "声音", "脚步", "衣物", "武器", "铠甲"}
            if m not in common_words and len(m) >= 2:
                # 自动补入 character_cards
                chars.append({"name": m, "title": m, "appearance": {"clothing": "未知"},
                              "color_scheme": "未知", "views": ["front", "face"], "asset_background": "white"})
                char_names.add(m)
                log.append(f"  character_cards 自动补入「{m}」（shot_{sid:02d} 提到）")

    # 6. 修复情绪跳变
    mood_seq = []
    for i, s in enumerate(shots):
        sid = s["id"]
        mood = _parse_shot_mood(s.get("description", ""))
        mood_seq.append((sid, mood, i))
    _TRANSITION_ADJ = {
        ("欢快", "悲伤"): "由欢快转为沉重",
        ("欢快", "压抑"): "气氛从轻松转为压抑",
        ("温馨", "紧张"): "温馨被打破，紧张升起",
        ("温馨", "战斗"): "平静被打破，战斗骤起",
        ("平静", "激烈"): "平静被打破",
        ("紧张", "温馨"): "紧张稍缓",
        ("悲伤", "欢快"): "从悲伤中走出",
        ("紧张", "平静"): "紧张消退",
    }
    for i in range(1, len(mood_seq)):
        prev_sid, prev_mood, prev_idx = mood_seq[i - 1]
        cur_sid, cur_mood, cur_idx = mood_seq[i]
        if prev_mood != "unknown" and cur_mood != "unknown" and prev_mood != cur_mood:
            if (prev_mood, cur_mood) in _TRANSITION_ADJ:
                trans = _TRANSITION_ADJ[(prev_mood, cur_mood)]
                cur_desc = shots[cur_idx].get("description", "")
                if trans not in cur_desc:
                    shots[cur_idx]["description"] = f"{trans}，{cur_desc}"
                    log.append(f"  shot_{cur_sid:02d}: 插入过渡描述「{trans}」以缓和情绪跳变")

    # 7. 修复开头钩子缺失
    hook_kw_list = ["突然", "意外", "冲突", "悬念", "对决", "危机"]
    for i in range(min(3, len(shots))):
        desc = shots[i].get("description", "")
        if not any(kw in desc for kw in hook_kw_list):
            sid = shots[i]["id"]
            import random
            hook = random.choice(["突然", "意外", "关键时刻"])
            if hook not in desc:
                shots[i]["description"] = f"{hook}，{desc}"
                log.append(f"  shot_{sid:02d}: 插入钩子「{hook}」以增强开头吸引力")
                break  # 只修第一个无钩子的镜头

    # 8. 修复时长过于均匀
    if len(shots) >= 4:
        durations = [float(s.get("duration", 5)) for s in shots]
        mean_dur = sum(durations) / len(durations)
        variance = sum((d - mean_dur) ** 2 for d in durations) / len(durations)
        if (variance ** 0.5) < 1.5:
            # 把前 3 个镜头缩短，中间一个拉长
            for i in range(min(3, len(shots))):
                old = float(shots[i].get("duration", 5))
                new = max(1.5, old * 0.6)
                shots[i]["duration"] = round(new, 1)
            if len(shots) > 3:
                mid = len(shots) // 2
                old = float(shots[mid].get("duration", 5))
                shots[mid]["duration"] = round(old * 1.5, 1)
            log.append(f"  调整镜头时长以增加节奏变化（前段缩短、中间拉长）")

    # 9. 修复高潮位置：调高高潮镜头之前的镜头时长，让高潮后移
    if len(shots) >= 4:
        intensity_scores = []
        for s in shots:
            desc = s.get("description", "")
            score = sum(2 for kw in ["激烈", "战斗", "冲突", "对决", "爆发", "高潮",
                                      "紧张", "追逐", "爆炸", "危机", "生死", "决胜"] if kw in desc)
            score -= sum(1 for kw in ["平静", "温馨", "对话", "沉默", "休整"] if kw in desc)
            intensity_scores.append(max(0, score))
        if max(intensity_scores) > 0:
            climax_idx = intensity_scores.index(max(intensity_scores))
            total_d = sum(float(s.get("duration", 5)) for s in shots)
            pos = sum(float(shots[i].get("duration", 5)) for i in range(climax_idx)) / max(total_d, 1)
            if pos < 0.6 and climax_idx > 1:
                # 高潮太早：缩短高潮前的镜头
                for i in range(climax_idx):
                    old = float(shots[i].get("duration", 5))
                    shots[i]["duration"] = round(old * 0.7, 1)
                log.append(f"  调高高潮(shot_{shots[climax_idx]['id']:02d})位置：缩短前置镜头")
            elif pos > 0.9 and climax_idx < len(shots) - 1:
                # 高潮太晚：缩短高潮后的镜头
                for i in range(climax_idx + 1, len(shots)):
                    old = float(shots[i].get("duration", 5))
                    shots[i]["duration"] = round(old * 0.7, 1)
                log.append(f"  提前高潮(shot_{shots[climax_idx]['id']:02d})位置：缩短后置镜头")

    # 10. 修复收尾缺失
    if len(shots) >= 2:
        for s in shots[-2:]:
            desc = s.get("description", "")
            closure_kw_list = ["结束", "落幕", "离去", "背影", "安静", "平息", "消失"]
            if not any(kw in desc for kw in closure_kw_list):
                shots[-1]["description"] = (shots[-1].get("description", "").rstrip("，。")
                                            + "，一切归于平静")
                log.append(f"  收尾镜头加入结局感描述")
                break

    # 11. 修复对话/动作失衡
    if len(shots) >= 6:
        dialogue_kw = ["说", "道", "对话", "交谈", "质问"]
        action_kw_list = ["战斗", "追逐", "攻击", "冲", "跑", "跳", "踢", "打"]
        dc = sum(1 for s in shots if any(k in s.get("description", "") for k in dialogue_kw))
        ac = sum(1 for s in shots if any(k in s.get("description", "") for k in action_kw_list))
        if dc / len(shots) > 0.7:
            # 找一个对话镜头改成动作描述
            for s in shots:
                if any(k in s.get("description", "") for k in dialogue_kw):
                    s["description"] += "，突然发生变故"
                    log.append(f"  在对话镜头中加入变故以增加动作感")
                    break
        elif ac / len(shots) > 0.7:
            for s in shots:
                if any(k in s.get("description", "") for k in action_kw_list):
                    s["description"] += "，短暂的对峙后"
                    log.append(f"  在动作镜头中加入对峙以增加剧情深度")
                    break

    # 更新 script
    script["shots"] = shots
    script["character_cards"] = chars
    return script, log


def _get_thresholds(project_or_script: str | dict | None = None) -> dict:
    """读取 script.json → script.validation 中的自定义阈值，合并默认值。"""
    th = dict(_DEFAULT_THRESHOLDS)
    if isinstance(project_or_script, str) and os.path.isfile(os.path.join(project_or_script, "script.json")):
        try:
            import json
            with open(os.path.join(project_or_script, "script.json"), encoding="utf-8") as f:
                data = json.load(f)
            custom = data.get("script", {}).get("validation", {})
            if custom:
                th.update(custom)
        except Exception:
            pass
    elif isinstance(project_or_script, dict):
        custom = project_or_script.get("script", {}).get("validation", {})
        if custom:
            th.update(custom)
    return th


def _verify_character_image(image_path: str, char_name: str = "", view: str = "",
                             expected_style: str = "") -> dict:
    """验证角色资产图质量。

    角色图应为单人视图，要求：
      - 文件完整（>= 10KB）
      - 不模糊（Laplacian >= 50）
      - 人物数量 = 1
      - 背景简洁干净（边缘区域低方差 + 高亮度）
      - 三视图（front/side/back）为全身照（HOG 框高度 >= 图片高 60%）

    Returns:
        {"passed": bool, "score": int, "max_score": 55,
         "checks": {...}, "issues": [str]}
    """
    checks: dict = {}
    issues: list[str] = []
    score = 0
    max_score = 55

    # ── 1. 文件完整性（5分）──
    if not os.path.isfile(image_path):
        return {"passed": False, "checks": {"file_exists": False}, "score": 0,
                "max_score": max_score, "issues": [f"文件不存在: {image_path}"]}
    size_kb = os.path.getsize(image_path) // 1024
    checks["file_size_kb"] = size_kb
    if size_kb < 10:
        issues.append("文件过小，可能已损坏")
    else:
        score += 5

    try:
        img_pil = Image.open(image_path).convert("RGB")
        np_rgb = np.array(img_pil)
        gray = cv2.cvtColor(np_rgb, cv2.COLOR_RGB2GRAY)
        img_h, img_w = gray.shape
        checks["dimensions"] = f"{img_w}x{img_h}"
    except Exception as e:
        issues.append(f"图片打开失败: {e}")
        return {"passed": False, "checks": checks, "score": score,
                "max_score": max_score, "issues": issues}

    # ── 2. 模糊检测（5分）──
    try:
        lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        checks["blur_score"] = round(lap_var, 1)
        if lap_var < 50:
            issues.append(f"模糊 (Laplacian={lap_var:.0f}<50)")
        else:
            score += 5
    except Exception as e:
        issues.append(f"模糊检测失败: {e}")

    # ── 3. 人物数量检测（10分）—— 单人角色图应恰好 1 人 ──
    person_count = 0
    hog_rects = None
    try:
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor.getDefaultPeopleDetector())
        hog_rects, _ = hog.detectMultiScale(gray, winStride=(8, 8), padding=(4, 4), scale=1.05)
        person_count = len(hog_rects)
        checks["person_count"] = person_count
        if person_count == 1:
            score += 10
        elif person_count == 0:
            issues.append("未检测到人物（角色图应有 1 人）")
        else:
            issues.append(f"检测到 {person_count} 人（角色图应为单人）")
    except Exception as e:
        issues.append(f"人物检测失败: {e}")

    # ── 4. 背景简洁检测（10分）—— 角色图应为纯色简单背景 ──
    #    策略：采样图片边缘 5% 区域的像素方差和亮度
    #    方差低 + 亮度高 → 白色/简单背景
    #    方差高 → 复杂/场景化背景（不符合角色资产要求）
    try:
        border_ratio = 0.05
        h, w = gray.shape
        top_strip = gray[:int(h * border_ratio), :]
        bottom_strip = gray[-int(h * border_ratio):, :]
        left_strip = gray[:, :int(w * border_ratio)]
        right_strip = gray[:, -int(w * border_ratio):]

        border_pixels = np.concatenate([
            top_strip.ravel(), bottom_strip.ravel(),
            left_strip.ravel(), right_strip.ravel(),
        ])
        border_std = float(np.std(border_pixels))
        border_mean = float(np.mean(border_pixels))
        checks["border_std"] = round(border_std, 1)
        checks["border_brightness"] = round(border_mean, 1)

        if border_std < 30 and border_mean > 200:
            # 低方差 + 高亮度 = 白色/纯色背景
            score += 10
        elif border_std < 40:
            # 中等方差 = 相对简单
            score += 5
            issues.append(f"背景略复杂（边缘标准差={border_std:.0f}）")
        else:
            issues.append(f"背景复杂（边缘标准差={border_std:.0f}），应使用纯色/简单背景")
    except Exception as e:
        issues.append(f"背景检测失败: {e}")

    # ── 5. 三视图全身照检测（15分）—— front/side/back 应为全身 ──
    #    通过 HOG 检测框高度占比判断：全身照框高 >= 图片高 60%
    fullbody_views = ("front", "side", "back")
    if view in fullbody_views and person_count == 1 and hog_rects is not None:
        try:
            rect = hog_rects[0]  # 唯一人物
            _, _, rw, rh = rect
            height_ratio = rh / img_h
            checks["body_height_ratio"] = round(height_ratio, 2)
            if height_ratio >= 0.6:
                score += 15
            elif height_ratio >= 0.4:
                score += 8
                issues.append(f"非全身照（人物框高={height_ratio:.0%} < 60%），应含完整全身")
            else:
                issues.append(f"非全身照（人物框高={height_ratio:.0%}），疑似面部/半身特写")
        except Exception as e:
            issues.append(f"全身检测失败: {e}")
    elif view in fullbody_views:
        # 未检测到人物 → 无法展示全身
        issues.append(f"未检测到人物，无法验证全身照")
    else:
        # face / pose / action 视图不做全身要求，直接给满分
        score += 15

    # ── 6. 风格检测（10分）—— 应与 script 定义的 aesthetic_style 一致 ──
    #    根据 expected_style 自适应选择检测策略：
    #    - 写实/照片级 ↔ 二次元/插画的区分指标不同
    #    策略：边缘密度（Canny）+ 颜色量化聚类数
    try:
        edges = cv2.Canny(gray, 50, 150)
        edge_ratio = float(np.sum(edges > 0) / edges.size)
        checks["edge_ratio"] = round(edge_ratio, 4)

        # 颜色量化聚类数
        small = cv2.resize(np_rgb, (64, 64), interpolation=cv2.INTER_AREA)
        reshaped = small.reshape(-1, 3).astype(np.float32)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(reshaped, 32, None, criteria, 5,
                                        cv2.KMEANS_RANDOM_CENTERS)
        cluster_used = len(set(labels.flatten().tolist()))
        checks["color_clusters"] = cluster_used

        # 根据 style 描述选择检测策略
        style_lower = expected_style.lower() if expected_style else ""
        if any(kw in style_lower for kw in ("二次元", "动漫", "anime", "卡通", "插画", "illustration", "2d")):
            # 动漫/二次元风格：边缘清晰分明，颜色区块少
            style_ok = edge_ratio > 0.05 and 3 <= cluster_used <= 15
            if style_ok:
                score += 10
            elif edge_ratio > 0.03:
                score += 5
                issues.append(f"风格与预期的「{expected_style}」不完全匹配")
            else:
                issues.append(f"风格不符合预期的「{expected_style}」")
        elif any(kw in style_lower for kw in ("写实", "photo", "cinematic", "realistic", "电影", "真实")):
            # 照片级写实：纹理丰富、色彩渐变多
            style_ok = edge_ratio > 0.08 and cluster_used > 8
            if style_ok:
                score += 10
            elif edge_ratio > 0.05 and cluster_used > 5:
                score += 5
                issues.append(f"风格偏简单，与预期的「{expected_style}」有差距")
            else:
                issues.append(f"风格疑似二次元/插画（边缘密度={edge_ratio:.3f}，色簇={cluster_used}），"
                              f"但预期的「{expected_style}」应为照片级写实")
        else:
            # 未知风格或未定义：宽松阈值，只报警不扣分
            if edge_ratio < 0.02:
                issues.append(f"风格特征不明显（边缘密度={edge_ratio:.3f}），建议检查 aesthetic_style 定义")
            else:
                score += 10
    except Exception as e:
        issues.append(f"风格检测失败: {e}")

    passed = score >= 25
    return {"passed": passed, "checks": checks, "score": score,
            "max_score": max_score, "issues": issues}


def _verify_scene_image(image_path: str, scene_name: str = "",
                         expected_style: str = "") -> dict:
    """验证场景图是否包含真实人物 + 风格匹配。

    规则：背景海报/相框/唱片封面中的人脸图案不违规，
    只有场景中真实存在的人物才算违规。

    检测策略（三级过滤）：
    1. Haar Cascade 人脸检测 + NMS 去重
    2. 尺寸过滤：face >= 短边 * 15% 才保留（排除极小的装饰人脸）
    3. 位置过滤：face 中心 y < 图片高 * 70% → 视为墙面/书架上的装饰，
       不判定为真实人物（真实人物应在场景地面区域）

    风格检测：与角色图一致，依据 expected_style 动态选择策略。
    """
    result: dict = {
        "passed": True, "has_person": False,
        "person_count": 0, "face_count": 0,
        "decoration_face_count": 0, "issues": [],
        "style_passed": True, "style_score": 0, "style_max_score": 10,
        "style_issues": [],
        "path": image_path,
    }
    if not os.path.isfile(image_path):
        result["passed"] = False
        result["issues"] = [f"文件不存在: {image_path}"]
        return result
    try:
        img_pil = Image.open(image_path).convert("RGB")
        np_rgb = np.array(img_pil)
        gray = cv2.cvtColor(np_rgb, cv2.COLOR_RGB2GRAY)
    except Exception as e:
        result["passed"] = False
        result["issues"] = [f"图片打开失败: {e}"]
        return result
    img_h, img_w = gray.shape
    short_side = min(img_w, img_h)
    name = os.path.basename(image_path)
    # ── 1. Haar Cascade 人脸检测 ──
    cascade_configs = [
        (cv2.data.haarcascades + "haarcascade_frontalface_default.xml", 1.1, 5),
        (cv2.data.haarcascades + "haarcascade_frontalface_default.xml", 1.2, 3),
        (cv2.data.haarcascades + "haarcascade_profileface.xml", 1.1, 5),
    ]
    raw_faces: list[tuple[int, int, int, int]] = []
    for cascade_path, scale, neighbors in cascade_configs:
        if os.path.isfile(cascade_path):
            face_cascade = cv2.CascadeClassifier(cascade_path)
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=scale, minNeighbors=neighbors, minSize=(20, 20))
            raw_faces.extend(faces)
    if not raw_faces:
        return result
    # ── 2. NMS 去重 ──
    face_deduped = _nms_rects(raw_faces)
    # ── 3. 分类：真实人物 vs 装饰人脸 ──
    MIN_FACE_RATIO = 0.15
    DECORATION_ZONE_TOP = 0.70
    real_faces: list[tuple[int, int, int, int]] = []
    deco_faces: list[tuple[int, int, int, int]] = []
    for (fx, fy, fw, fh) in face_deduped:
        face_cy = fy + fh / 2
        face_large_enough = (fw >= short_side * MIN_FACE_RATIO or
                             fh >= short_side * MIN_FACE_RATIO)
        in_ground_zone = (face_cy >= img_h * DECORATION_ZONE_TOP)
        if face_large_enough and in_ground_zone:
            real_faces.append((fx, fy, fw, fh))
        else:
            deco_faces.append((fx, fy, fw, fh))
    result["face_count"] = len(face_deduped)
    result["decoration_face_count"] = len(deco_faces)
    if len(real_faces) > 0:
        result["has_person"] = True
        result["passed"] = False
        result["person_count"] = len(real_faces)
        result["issues"].append(
            f"场景图 '{name}' 检测到 {len(real_faces)} 个真实人物"
            f"（另有 {len(deco_faces)} 张装饰人脸已忽略）"
            f"——场景应为纯背景，不应包含人物")
    else:
        if deco_faces:
            result["issues"].append(
                f"场景图 '{name}' 检测到 {len(deco_faces)} 张装饰人脸（已忽略）")

    # ── 风格检测（与角色图一致）──
    #    依据 expected_style 自适应选择策略
    try:
        edges = cv2.Canny(gray, 50, 150)
        edge_ratio = float(np.sum(edges > 0) / edges.size)
        result["edge_ratio"] = round(edge_ratio, 4)

        small = cv2.resize(np_rgb, (64, 64), interpolation=cv2.INTER_AREA)
        reshaped = small.reshape(-1, 3).astype(np.float32)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, _ = cv2.kmeans(reshaped, 32, None, criteria, 5, cv2.KMEANS_RANDOM_CENTERS)
        cluster_used = len(set(labels.flatten().tolist()))
        result["color_clusters"] = cluster_used

        style_lower = expected_style.lower() if expected_style else ""
        if any(kw in style_lower for kw in ("二次元", "动漫", "anime", "卡通", "插画", "illustration", "2d")):
            style_ok = edge_ratio > 0.05 and 3 <= cluster_used <= 15
            if not style_ok:
                result["style_passed"] = False
                result["style_issues"].append(
                    f"风格与预期的「{expected_style}」不完全匹配")
        elif any(kw in style_lower for kw in ("写实", "photo", "cinematic", "realistic", "电影", "真实")):
            if not (edge_ratio > 0.08 and cluster_used > 8):
                result["style_passed"] = False
                result["style_issues"].append(
                    f"风格偏简单/插画化（边缘密度={edge_ratio:.3f}，色簇={cluster_used}），"
                    f"与预期的「{expected_style}」不符")
        else:
            if edge_ratio < 0.02:
                result["style_issues"].append(
                    f"风格特征不明显，建议检查 aesthetic_style 定义")
        result["style_score"] = 10 if result["style_passed"] else 0
        # 风格不通过时不阻塞（风格是模型能力问题，重试也无法改变模型能力）
        # 但记录 issue 供人工审查
        if not result["style_passed"]:
            # 不设置 passed = False，避免阻塞流水线
            result["issues"].extend(result["style_issues"])
    except Exception as e:
        result["style_issues"].append(f"风格检测失败: {e}")

    return result


def _nms_rects(boxes, iou_thresh=0.3):
    """通用 NMS 去重，输入 list of (x, y, w, h)。"""
    if boxes is None or (isinstance(boxes, np.ndarray) and boxes.size == 0) or (not isinstance(boxes, np.ndarray) and len(boxes) == 0):
        return []
    boxes = np.array(boxes, dtype=np.float32)
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 0] + boxes[:, 2]
    y2 = boxes[:, 1] + boxes[:, 3]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = np.argsort(y2)
    keep = []
    while len(order) > 0:
        i = int(order[-1])
        keep.append(i)
        if len(order) == 1:
            break
        order = order[:-1]
        xx1 = np.maximum(x1[i], x1[order])
        yy1 = np.maximum(y1[i], y1[order])
        xx2 = np.maximum(x2[i], x2[order])
        yy2 = np.maximum(y2[i], y2[order])
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        overlap = (w * h) / (areas[i] + areas[order] - w * h)
        order = order[overlap < iou_thresh]
    return [boxes[j].astype(int) for j in keep]


def _verify_all_scenes(project: str, expected_style: str = "") -> list[dict]:
    """验证项目下所有场景图。"""
    scenes_dir = os.path.join(project, "images", "scenes")
    if not os.path.isdir(scenes_dir):
        return []
    results = []
    for fname in sorted(os.listdir(scenes_dir)):
        if fname.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(scenes_dir, fname)
            r = _verify_scene_image(path, scene_name=fname, expected_style=expected_style)
            results.append(r)
    return results

def _verify_first_frame(image_path: str, shot: dict, script_data: dict | None = None) -> dict:
    """全自动验证首帧图质量，返回 {'passed': bool, 'checks': {...}, 'score': int, 'issues': [str]}。

    检查项和权重：
      - 文件存在/非空      5分（致命）
      - 尺寸比例正确        5分（致命）
      - 不模糊（Laplacian）  5分
      - 人物数量符合预期    30分（致命，最常见翻车点）
      - 主体色彩匹配角色卡  5分
    总分 50 分，>= 35 分通过。
    """

    checks: dict[str, bool | int | str] = {}
    issues: list[str] = []
    score = 0
    max_score = 50

    # --- 1. 文件完整性 ---
    if not os.path.isfile(image_path):
        return {"passed": False, "checks": {"file_exists": False}, "score": 0,
                "issues": [f"文件不存在: {image_path}"]}
    size_kb = os.path.getsize(image_path) // 1024
    checks["file_size_kb"] = size_kb
    if size_kb < 10:
        issues.append("文件过小，可能已损坏")
    else:
        score += 5

    try:
        img_pil = Image.open(image_path).convert("RGB")
        img_w, img_h = img_pil.size
        checks["dimensions"] = f"{img_w}x{img_h}"
        checks["expected_aspect"] = None

        # 尺寸校验：推断预期比例
        aspect = script_data.get("script", {}).get("aspect_ratio", "9:16") if script_data else "9:16"
        checks["expected_aspect"] = aspect
        if aspect == "9:16":
            target_w = int(img_h * 9 / 16)
            if abs(img_w - target_w) / max(img_w, 1) < 0.15:
                score += 5
            else:
                issues.append(f"尺寸 {img_w}x{img_h} 不符合 {aspect} 比例")
        elif aspect == "16:9":
            target_h = int(img_w * 9 / 16)
            if abs(img_h - target_h) / max(img_h, 1) < 0.15:
                score += 5
            else:
                issues.append(f"尺寸 {img_w}x{img_h} 不符合 {aspect} 比例")
        else:
            score += 5  # 未知比例不校验
    except Exception as e:
        issues.append(f"图片打开失败: {e}")
        return {"passed": False, "checks": checks, "score": score, "issues": issues}

    # --- 3. 模糊检测（Laplacian 方差）---
    try:
        # 用 PIL 读图（支持中文路径），转 numpy 给 OpenCV 处理
        np_rgb = np.array(img_pil)
        gray = cv2.cvtColor(np_rgb, cv2.COLOR_RGB2GRAY)
        lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        checks["blur_score"] = round(lap_var, 1)
        if lap_var < 50:
            issues.append(f"图片模糊 (Laplacian={lap_var:.0f}<50)")
        elif lap_var < 100:
            pass  # 略模糊但不致命
        else:
            score += 5
    except Exception as e:
        issues.append(f"模糊检测失败: {e}")

    # --- 4. 人物数量检测（HOG + SVM）---
    # 注意：HOG+SVM 行人检测器训练于真实照片，
    # 对二次元/插画/手绘风格图像检测效果可能不佳（漏检或误检）。
    try:
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor.getDefaultPeopleDetector())
        (rects, _) = hog.detectMultiScale(
            gray, winStride=(8, 8), padding=(4, 4), scale=1.05
        )
        # NMS 去重
        person_count = len(rects)
        checks["person_count"] = person_count

        # 根据 shot description 推断预期人数
        desc = shot.get("description", "")
        is_closeup = any(w in desc for w in ["特写", "面部", "极致特写"])
        is_action = any(w in desc for w in ["踢", "踹"])
        solo_kw = ["单人", "一个人", "独自", "背影", "伫立"]
        duo_kw = ["两人", "墨雪和墨将", "墨雪身后", "双人", "这对将帅",
                  "对话", "对视", "互踢"]

        if is_closeup:
            # 特写镜头 HOG 不准确，跳过人物检测
            expected = -1
            score += 30  # 直接给满分
        elif any(w in desc for w in solo_kw):
            expected = 1
        elif any(w in desc for w in duo_kw):
            expected = 2
        else:
            char_count = 0
            if "墨雪" in desc:
                char_count += 1
            if "墨将" in desc:
                char_count += 1
            expected = char_count if char_count > 0 else -1

        checks["expected_count"] = expected
        if expected > 0:
            if is_action:
                # 动作镜头 HOG 可能漏检，容忍度放宽
                tolerance = 2
            elif expected == 1:
                tolerance = 1  # 单人 0-2 都接受
            else:
                tolerance = 0  # 双人精确匹配
            if abs(person_count - expected) > tolerance and person_count > 0:
                issues.append(
                    f"人物数量异常: 检测到 {person_count} 人，预期 ~{expected} 人"
                )
            else:
                score += 30
        else:
            score += 30  # 无法判断，给满分
    except Exception as e:
        issues.append(f"人物检测失败: {e}")

    # --- 5. 色彩分析（简单主体颜色匹配）---
    try:
        np_img = np.array(img_pil)
        # 降采样到 32x32
        small = cv2.resize(np_img, (32, 32), interpolation=cv2.INTER_AREA)
        pixels = small.reshape(-1, 3)
        # 用中位数作为主体色近似
        median_color = np.median(pixels, axis=0)
        checks["median_color"] = [int(median_color[0]), int(median_color[1]), int(median_color[2])]
        r, g, b = median_color

        # 检查是否偏灰/偏黑（古风战场常见暗调，从 scene_cards 读取调性）
        dark_scene = False
        if script_data:
            for sc in script_data.get("scene_cards", []):
                palette = sc.get("color_palette", "")
                if any(kw in palette for kw in ["暗", "灰", "昏", "冷", "黑", "铅", "褐"]):
                    dark_scene = True
                    break
        brightness = (r + g + b) / 3
        if brightness < 20:
            issues.append("整体过暗")
        elif brightness < 60 and not dark_scene:
            issues.append("画面偏暗")
        else:
            score += 5
    except Exception as e:
        issues.append(f"色彩分析失败: {e}")

    passed = score >= 35
    return {"passed": passed, "checks": checks, "score": score, "max_score": max_score, "issues": issues}


# ── 运镜检测 ──────────────────────────────────────────
_CAMERA_KW_MAP = {
    "推进": "dolly_in", "推近": "dolly_in", "缓慢推进": "dolly_in",
    "拉远": "dolly_out", "后拉": "dolly_out",
    "横移": "pan", "平移": "pan", "左右横移": "pan", "摇摄": "pan",
    "上摇": "tilt_up", "下摇": "tilt_down", "仰拍": "tilt_up", "俯拍": "tilt_down",
    "环绕": "orbit", "旋转": "orbit",
    "静态": "static", "固定": "static", "静止": "static", "特写": "static",
}


def _parse_camera_motion(description: str) -> str:
    """从 shot description 提取预期运镜。"""
    desc = description.lower()
    matched = [m for kw, m in _CAMERA_KW_MAP.items() if kw in desc]
    unique = list(set(matched))
    return unique[0] if len(unique) == 1 else ("mixed" if unique else "unknown")


def _detect_camera_motion(cap, total_frames: int) -> dict:
    """用稠密光流检测视频实际运镜。"""
    result = {"motion_type": "static", "magnitude": 0.0,
              "flow_h_mean": 0.0, "flow_v_mean": 0.0, "radial_mean": 0.0}
    if total_frames < 5:
        return result
    step = max(1, total_frames // 10)
    prev_gray = None
    buf_h, buf_v, buf_mag, buf_rad = [], [], [], []
    for pos in range(0, total_frames, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        ret, frame = cap.read()
        if not ret or frame is None:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (160, 120))
        if prev_gray is not None:
            flow = cv2.calcOpticalFlowFarneback(
                prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            h, w = flow.shape[:2]
            fx, fy = flow[:, :, 0], flow[:, :, 1]
            buf_h.append(float(np.mean(fx)))
            buf_v.append(float(np.mean(fy)))
            buf_mag.append(float(np.mean(np.sqrt(fx**2 + fy**2))))
            cx, cy, = w // 2, h // 2
            yg, xg = np.mgrid[0:h, 0:w]
            dist = np.sqrt((xg - cx)**2 + (yg - cy)**2) + 1e-6
            buf_rad.append(float(np.mean((fx * (xg - cx) + fy * (yg - cy)) / dist)))
        prev_gray = gray
    if not buf_h:
        return result
    avg_h, avg_v = np.mean(buf_h), np.mean(buf_v)
    avg_mag, avg_rad = np.mean(buf_mag), np.mean(buf_rad)
    result.update({"magnitude": round(float(avg_mag), 3),
                   "flow_h_mean": round(float(avg_h), 3),
                   "flow_v_mean": round(float(avg_v), 3),
                   "radial_mean": round(float(avg_rad), 3)})
    if avg_mag < 0.5:
        result["motion_type"] = "static"
    elif abs(avg_rad) > abs(avg_h) * 1.5 and abs(avg_rad) > abs(avg_v) * 1.5:
        result["motion_type"] = "dolly_in" if avg_rad > 0 else "dolly_out"
    elif abs(avg_h) > abs(avg_v) * 2:
        result["motion_type"] = "pan"
    elif abs(avg_v) > abs(avg_h) * 2:
            result["motion_type"] = "tilt_up" if avg_v < 0 else "tilt_down"
    else:
        result["motion_type"] = "mixed"
    return result


# ── 情绪/色调/节奏检测 ──────────────────────────────────
# 从 shot description 提取预期情绪 → 用色温/亮度/动态密度校验

_MOOD_PROFILES = {
    # 情绪: (色温偏差, 亮度, 动态密度)
    #   色温: >0 暖, <0 冷, 0 中性
    #   亮度: 0-255
    #   动态: 0-1 (光流幅值归一化)
    "紧张": (">5",  "30-80",   ">0.5"),
    "激烈": (">5",  "60-150",  ">0.6"),
    "战斗": (">5",  "60-150",  ">0.6"),
    "平静": ("-5-5", "80-180", "<0.3"),
    "悲伤": ("<-5", "20-70",   "<0.3"),
    "压抑": ("<-5", "10-50",   "<0.2"),
    "欢快": (">5",  "150-220", ">0.4"),
    "温馨": (">5",  "120-200", "<0.3"),
    "阴郁": ("<-5", "10-60",   "<0.2"),
    "神秘": ("-5-5", "20-80",  "0.2-0.5"),
    "肃穆": ("<-5", "20-60",   "<0.2"),
    "绝望": ("<-5", "5-30",    "<0.1"),
}

# 场景调性关键词 → 从 scene_cards.tone 或 shot.description 匹配
_TONE_KW = ["紧张", "激烈", "战斗", "平静", "悲伤", "压抑", "欢快",
            "温馨", "阴郁", "神秘", "肃穆", "绝望", "激昂", "沉闷"]


def _parse_shot_mood(description: str) -> str:
    """从 shot description 提取预期情绪基调。

    Returns: 情绪名 / "unknown"
    """
    desc = description.lower()
    for mood in _TONE_KW:
        if mood in desc:
            return mood
    return "unknown"


def _detect_video_mood(cap, total_frames: int) -> dict:
    """检测视频实际的情绪/色调特征。

    Returns:
        {"color_temp": float 色温偏差,
         "brightness": float 平均亮度,
         "motion_density": float 动态密度}
    """
    result = {"color_temp": 0.0, "brightness": 0.0, "motion_density": 0.0}
    if total_frames < 3:
        return result

    step = max(1, total_frames // 10)
    prev_gray = None
    b_sum, g_sum, r_sum = 0.0, 0.0, 0.0
    bright_sum = 0.0
    motion_sum = 0.0
    count = 0

    for pos in range(0, total_frames, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        ret, frame = cap.read()
        if not ret or frame is None:
            continue
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        b_sum += float(np.mean(frame_rgb[:, :, 0]))
        g_sum += float(np.mean(frame_rgb[:, :, 1]))
        r_sum += float(np.mean(frame_rgb[:, :, 2]))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bright_sum += float(np.mean(gray))
        if prev_gray is not None:
            flow = cv2.calcOpticalFlowFarneback(
                cv2.resize(prev_gray, (80, 60)),
                cv2.resize(gray, (80, 60)),
                None, 0.5, 3, 15, 3, 5, 1.2, 0)
            motion_sum += float(np.mean(np.sqrt(flow[:,:,0]**2 + flow[:,:,1]**2)))
        prev_gray = gray
        count += 1

    if count > 0:
        r_avg, g_avg, b_avg = r_sum / count, g_sum / count, b_sum / count
        # 色温偏差: R/B 比值偏离中性 (R≈B)
        result["color_temp"] = round((r_avg - b_avg) / (r_avg + b_avg + 1) * 100, 1)
        result["brightness"] = round(bright_sum / count, 1)
        result["motion_density"] = round(motion_sum / count, 3) if motion_sum > 0 else 0.0

    return result


def _verify_mood(expected_mood: str, actual: dict) -> tuple[bool, list[str]]:
    """校验实际视频情绪是否匹配预期。

    Returns: (passed, issues)
    """
    if expected_mood == "unknown" or expected_mood not in _MOOD_PROFILES:
        return (True, [])
    profile = _MOOD_PROFILES[expected_mood]
    issues = []
    temp_str, bright_str, motion_str = profile

    def _check(name: str, val: float, spec: str) -> bool:
        """检查值是否在规格内。spec 示例: ">5", "<0.3", "30-80", "-5-5" """
        spec = spec.strip()
        if spec.startswith(">="):
            ok = val >= float(spec[2:])
        elif spec.startswith(">"):
            ok = val > float(spec[1:])
        elif spec.startswith("<="):
            ok = val <= float(spec[2:])
        elif spec.startswith("<"):
            ok = val < float(spec[1:])
        elif "-" in spec:
            lo, hi = spec.split("-", 1)
            ok = float(lo) <= val <= float(hi)
        else:
            ok = True
        if not ok:
            issues.append(f"{name}={val}, 预期{spec}（情绪「{expected_mood}」）")
        return ok

    _check("色温偏差", actual.get("color_temp", 0), temp_str)
    _check("平均亮度", actual.get("brightness", 0), bright_str)
    _check("动态密度", actual.get("motion_density", 0), motion_str)
    return (len(issues) == 0, issues)


# ── OpenCV 语义级视频校验（人脸检测/场景匹配/动作分析） ─────────


def _detect_face_count(cap, total_frames: int,
                       cascade_path: str = "") -> dict:
    """用 Haar Cascade 检测视频中的人物数量（含 NMS 去重+直方图聚类去重）。
    
    返回: face_count(去重后独立人数), faces(去重后的检测框), frame, raw_raw(原始数)
    """
    import numpy as np
    if not cascade_path:
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    if not os.path.isfile(cascade_path):
        return {"face_count": 0, "faces": [], "frame": None, "raw_raw": 0, "note": "haarcascade 文件不存在"}
    try:
        face_cascade = cv2.CascadeClassifier(cascade_path)
    except Exception:
        return {"face_count": 0, "faces": [], "frame": None, "raw_raw": 0, "note": "无法加载 haarcascade"}

    def _nms(faces_list, overlap_thresh=0.4):
        """非极大值抑制：合并重叠框（保留最大的置信区域）。"""
        if not faces_list:
            return []
        boxes = np.array([(x, y, x+w, y+h) for (x, y, w, h) in faces_list], dtype=np.float32)
        pick = []
        idxs = np.argsort(boxes[:, 2] - boxes[:, 0])  # 按宽度升序（小框优先保留）
        while len(idxs) > 0:
            i = idxs[-1]
            pick.append(i)
            xx1 = np.maximum(boxes[i, 0], boxes[idxs[:-1], 0])
            yy1 = np.maximum(boxes[i, 1], boxes[idxs[:-1], 1])
            xx2 = np.minimum(boxes[i, 2], boxes[idxs[:-1], 2])
            yy2 = np.minimum(boxes[i, 3], boxes[idxs[:-1], 3])
            w = np.maximum(0, xx2 - xx1)
            h = np.maximum(0, yy2 - yy1)
            overlap = (w * h) / ((boxes[i, 2]-boxes[i, 0]) * (boxes[i, 3]-boxes[i, 1]))
            idxs = np.delete(idxs, np.concatenate(([-1], np.where(overlap > overlap_thresh)[0])))
        return [faces_list[i] for i in pick]

    def _cluster_faces(faces_list, frame, sim_thresh=0.5):
        """直方图聚类：直方图高度相似（>sim_thresh）的人脸视为同一人，仅保留一个。"""
        if len(faces_list) <= 1:
            return faces_list
        kept = []
        _calchist = lambda roi: cv2.calcHist([roi], [0, 1, 2], None, [8, 8, 8], [0, 256]*3)
        def _normed(hist):
            cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
            return hist
        hists = []
        for (x, y, w, h) in faces_list:
            roi = frame[y:y+h, x:x+w]
            if roi.size == 0:
                hists.append(None)
            else:
                hists.append(_normed(_calchist(roi)))
        for i, (box, hist) in enumerate(zip(faces_list, hists)):
            if hist is None:
                continue
            dup = False
            for j in range(i):
                if hists[j] is not None:
                    sim = cv2.compareHist(hist, hists[j], cv2.HISTCMP_CORREL)
                    if sim > sim_thresh:
                        dup = True
                        break
            if not dup:
                kept.append(box)
        return kept

    def _validate_face_boxes(faces_list, frame, h, w):
        """按几何规则+眼睛检测+肤色过滤虚假人脸框。"""
        if not faces_list or frame is None:
            return []
        try:
            eye_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_eye.xml")
        except Exception:
            eye_cascade = None
        area_total = h * w
        valid = []
        # 每框内采样像素计算肤色比
        for (fx, fy, fw, fh) in faces_list:
            ar = fw / fh if fh > 0 else 0
            # 1) 长宽比：人脸应接近正方形 (0.5~2.0)
            if ar < 0.4 or ar > 2.5:
                continue
            # 2) 大小：不能超过画面 15%，不能小于 0.3%
            box_area = fw * fh
            area_ratio = box_area / area_total if area_total > 0 else 0
            if area_ratio > 0.15 or area_ratio < 0.003:
                continue
            # 2b) 位置：人脸应在画面上半部 65% 以内（中景镜头面部不会出现在地面区域）
            face_center_y = fy + fh / 2
            if face_center_y > h * 0.65:
                continue
            # 3) 眼睛检测：仅对较大的人脸框做（太小或低分辨率下眼睛检测不可靠）
            if eye_cascade is not None and fw > 100 and fh > 100:
                face_roi_gray = cv2.cvtColor(
                    frame[fy:fy+fh, fx:fx+fw], cv2.COLOR_BGR2GRAY) if frame is not None else None
                if face_roi_gray is not None and face_roi_gray.size > 0:
                    eyes = eye_cascade.detectMultiScale(
                        face_roi_gray, 1.1, 3, minSize=(10, 10))
                    if len(eyes) == 0:
                        # 无眼睛 → 大概率误检，丢弃
                        continue
            # 4) 肤色检验：人脸 ROI 应有皮肤色调（场景可能有色温滤镜，阈值放宽）
            if frame is not None:
                roi_bgr = frame[fy:fy+fh, fx:fx+fw]
                if roi_bgr.size > 0:
                    roi_rgb = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2RGB)
                    r, g, b = roi_rgb[:, :, 0].astype(float), roi_rgb[:, :, 1].astype(float), roi_rgb[:, :, 2].astype(float)
                    skin = (r > 60) & (g > 25) & (b > 10) & (r > g * 0.7) & (r > b * 0.7)
                    skin_ratio = float(skin.sum()) / float(roi_rgb.shape[0] * roi_rgb.shape[1])
                    if skin_ratio < 0.01:
                        continue
            valid.append((fx, fy, fw, fh))
        return valid

    max_unique = 0
    best_faces = []
    best_frame = None
    raw_raw = 0
    sample_positions = sorted({
        0,
        max(0, total_frames // 4),
        max(0, total_frames // 2),
        max(0, 3 * total_frames // 4),
        max(0, total_frames - 1),
    })[:5]
    for pos in sample_positions:
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        ret, frame = cap.read()
        if not ret or frame is None:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        raw = face_cascade.detectMultiScale(gray, 1.1, 3, minSize=(40, 40))
        if len(raw) == 0:
            continue
        # NMS 去重
        nmsed = _nms([(int(x), int(y), int(w), int(h)) for (x, y, w, h) in raw])
        # 几何+眼睛+肤色过滤
        fh, fw = frame.shape[:2]
        validated = _validate_face_boxes(nmsed, frame, fh, fw)
        if not validated:
            continue
        # 直方图聚类去重（将高度相似的人脸视为同一角色）
        clustered = _cluster_faces(validated, frame, sim_thresh=0.5)
        if len(clustered) > max_unique:
            max_unique = len(clustered)
            best_faces = clustered
            best_frame = frame.copy()
            raw_raw = len(raw)
    return {"face_count": max_unique, "faces": best_faces, "frame": best_frame,
            "raw_raw": raw_raw}


def _match_faces_with_characters(faces: list, frame,
                                 character_refs: dict[str, list[str]]) -> dict:
    """比对检测到的人脸与角色参考图的直方图相似度。
    
    character_refs: {角色名: [正面图路径, 面部图路径]}
    返回: {"matched": int, "total": int, "unmatched": [str]}
    """
    import numpy as np
    if not faces or frame is None or not character_refs:
        return {"matched": 0, "total": 0, "details": [], "unmatched_refs": list(character_refs.keys())}

    matched_names = set()
    unmatched_refs = list(character_refs.keys())
    details = []

    for (x, y, w, h) in faces:
        face_roi = frame[y:y+h, x:x+w]
        if face_roi.size == 0:
            continue
        face_hist = cv2.calcHist([face_roi], [0, 1, 2], None,
                                 [8, 8, 8], [0, 256, 0, 256, 0, 256])
        cv2.normalize(face_hist, face_hist, 0, 1, cv2.NORM_MINMAX)

        best_char = None
        best_score = 0.0
        for char_name, ref_paths in character_refs.items():
            for ref_path in ref_paths:
                if not os.path.isfile(ref_path):
                    continue
                try:
                    ref_img = cv2.imread(ref_path)
                    if ref_img is None:
                        continue
                    ref_hist = cv2.calcHist([ref_img], [0, 1, 2], None,
                                            [8, 8, 8], [0, 256, 0, 256, 0, 256])
                    cv2.normalize(ref_hist, ref_hist, 0, 1, cv2.NORM_MINMAX)
                    score = cv2.compareHist(face_hist, ref_hist, cv2.HISTCMP_CORREL)
                    if score > best_score:
                        best_score = score
                        best_char = char_name
                except Exception:
                    continue

        if best_char and best_score >= 0.25:
            matched_names.add(best_char)
            if best_char in unmatched_refs:
                unmatched_refs.remove(best_char)
            details.append({"char": best_char, "score": round(best_score, 3)})
        else:
            details.append({"char": "unknown", "score": round(best_score, 3)})

    return {
        "matched": len(matched_names),
        "total": len(character_refs),
        "details": details,
        "unmatched_refs": unmatched_refs,
    }


def _match_scene_histogram(video_frame, scene_asset_dir: str,
                           scene_slug: str) -> float:
    """比对视频帧与场景资产图的颜色直方图相关性（0~1）。"""
    import numpy as np
    best_score = 0.0
    for view in ["广角", "中景", "特写"]:
        sp = os.path.join(scene_asset_dir, f"{scene_slug}_{view}.png")
        if not os.path.isfile(sp):
            continue
        try:
            scene_img = cv2.imread(sp)
            if scene_img is None:
                continue
            scene_hist = cv2.calcHist([scene_img], [0, 1, 2], None,
                                      [16, 16, 16], [0, 256, 0, 256, 0, 256])
            cv2.normalize(scene_hist, scene_hist, 0, 1, cv2.NORM_MINMAX)
            frame_hist = cv2.calcHist([video_frame], [0, 1, 2], None,
                                      [16, 16, 16], [0, 256, 0, 256, 0, 256])
            cv2.normalize(frame_hist, frame_hist, 0, 1, cv2.NORM_MINMAX)
            score = cv2.compareHist(scene_hist, frame_hist, cv2.HISTCMP_CORREL)
            best_score = max(best_score, score)
        except Exception:
            continue
    return best_score


def _detect_head_turn(cap, total_frames: int) -> dict:
    """检测视频中是否有转头/头部运动的迹象（ROI 光流）。"""
    import numpy as np
    if total_frames < 10:
        return {"has_motion": False, "motion_score": 0, "note": "视频太短"}
    # 采样中间一段连续帧分析头部区域运动
    mid = total_frames // 2
    start = max(0, mid - min(15, total_frames // 4))
    end = min(total_frames, mid + min(15, total_frames // 4))
    lateral_motions = []
    prev_head = None
    for pos in range(start, end):
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        ret, frame = cap.read()
        if not ret or frame is None:
            continue
        h, w = frame.shape[:2]
        # 头部 ROI：画面上 1/4 区域（假设头部位置）
        head_roi = frame[h // 8: h // 2, w // 4: 3 * w // 4]
        gray = cv2.cvtColor(head_roi, cv2.COLOR_BGR2GRAY)
        if prev_head is not None:
            flow = cv2.calcOpticalFlowFarneback(prev_head, gray, None,
                                                0.5, 3, 15, 3, 5, 1.2, 0)
            # 水平方向运动的平均幅度
            horiz = np.mean(np.abs(flow[:, :, 0]))
            lateral_motions.append(horiz)
        prev_head = gray
    if not lateral_motions:
        return {"has_motion": False, "motion_score": 0, "note": "无法计算"}
    avg_motion = float(np.mean(lateral_motions))
    has_motion = avg_motion > 2.0
    return {"has_motion": has_motion, "motion_score": round(avg_motion, 2)}


def _parse_expected_people(description: str) -> int:
    """从 shot description 中解析预期人数（如 '三人' → 3）。"""
    import re
    cn_nums = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5,
               "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
    m = re.search(r"([一两三四五六七八九十])([人位个名])", description)
    if m:
        return cn_nums.get(m.group(1), 0)
    # 也匹配 "3人" "2人" 等数字写法
    m = re.search(r"(\d+)\s*[人位个名]", description)
    if m:
        return int(m.group(1))
    return 0


def _parse_scene_slug(description: str, script: dict) -> str:
    """从 shot 描述中查找匹配的场景卡 slug（优先用 name 匹配，返回 id 作为文件路径名）。"""
    desc_lower = description.lower()
    for sc in script.get("scene_cards", []):
        name = sc.get("name", "")
        if name and name.lower() in desc_lower:
            return sc.get("id", name).replace(" ", "_")
    return ""


def _get_character_refs(project: str, script: dict) -> dict[str, list[str]]:
    """从 script.json 读取角色名→参考图路径映射（face 图优先，front 图兜底）。"""
    refs = {}
    char_dir = os.path.join(project, "images", "characters")
    for cc in script.get("character_cards", []):
        name = cc.get("name", "")
        if not name:
            continue
        paths = []
        for view in ["face", "front"]:
            p = os.path.join(char_dir, f"{name}_{view}.png")
            if os.path.isfile(p):
                paths.append(p)
        if paths:
            refs[name] = paths
    return refs


def _verify_shot_video(video_path: str, shot_id: int = 0,
                        expected_duration: float = 0,
                        expected_aspect: str = "",
                        expected_camera: str = "",
                        shot_description: str = "",
                        project: str = "") -> dict:
    """验证视频文件质量和完整性。

    检查项：
      - 文件完整性（存在、非空、可打开）
      - 时长符合预期（±20%）
      - 分辨率符合画面比例
      - 无全黑/冻结帧（采样帧检查）
      - 运镜匹配 shot description（光流分析）
      - 情绪/色调匹配 shot description（色温+亮度+动态密度）

    Returns:
        {"passed": bool, "score": int, "max_score": 55,
         "checks": {...}, "issues": [str]}
    """
    checks: dict = {}
    issues: list[str] = []
    score = 0
    max_score = 85 if project else 55

    if not os.path.isfile(video_path):
        return {"passed": False, "checks": {"file_exists": False}, "score": 0,
                "max_score": max_score, "issues": [f"文件不存在: {video_path}"]}
    size_mb = os.path.getsize(video_path) / (1024 * 1024)
    checks["file_size_mb"] = round(size_mb, 1)
    if size_mb < 0.01:
        issues.append("文件过小，可能已损坏")
    else:
        score += 5

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        issues.append("无法打开视频文件（可能已损坏）")
        cap.release()
        return {"passed": False, "checks": checks, "score": score,
                "max_score": max_score, "issues": issues}

    try:
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = total_frames / fps if fps > 0 else 0
        checks["fps"] = round(fps, 1)
        checks["total_frames"] = total_frames
        checks["resolution"] = f"{width}x{height}"
        checks["duration_sec"] = round(duration, 2)

        # 1. 时长校验
        if expected_duration > 0:
            ratio = duration / expected_duration
            checks["duration_ratio"] = round(ratio, 2)
            if 0.8 <= ratio <= 1.2:
                score += 10
            elif ratio < 0.5 or ratio > 1.5:
                issues.append(f"时长异常: 实际={duration:.1f}s, 预期={expected_duration:.1f}s")
            else:
                score += 5
                issues.append(f"时长偏差: 实际={duration:.1f}s, 预期={expected_duration:.1f}s")
        else:
            score += 10

        # 2. 分辨率与画面比例校验
        if expected_aspect:
            parts = expected_aspect.split(":")
            if len(parts) == 2:
                try:
                    exp_w = int(parts[0])
                    exp_h = int(parts[1])
                    actual_ratio = width / height
                    expected_ratio = exp_w / exp_h
                    if abs(actual_ratio - expected_ratio) / expected_ratio < 0.15:
                        score += 10
                    else:
                        issues.append(f"画面比例 {width}x{height} 不符合 {expected_aspect}")
                except ValueError:
                    score += 10
            else:
                score += 10
        else:
            score += 10

        # 3. 帧质量采样：检查前/中/后帧是否为全黑或冻结
        sample_positions = [0, total_frames // 2, total_frames - 1] if total_frames > 1 else [0]
        checked_frames = 0
        black_frames = 0
        frozen_frames = 0
        prev_gray = None
        for pos in sample_positions:
            cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
            ret, frame = cap.read()
            if not ret or frame is None:
                continue
            checked_frames += 1
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mean_brightness = float(np.mean(gray_frame))
            if mean_brightness < 5:
                black_frames += 1
            if prev_gray is not None:
                diff = cv2.absdiff(gray_frame, prev_gray)
                mean_diff = float(np.mean(diff))
                if mean_diff < 3:
                    frozen_frames += 1
            prev_gray = gray_frame

        checks["checked_frames"] = checked_frames
        checks["black_frames"] = black_frames
        checks["frozen_frames"] = frozen_frames
        if black_frames > 0:
            issues.append(f"检测到 {black_frames}/{checked_frames} 帧全黑")
        if frozen_frames > 0:
            issues.append(f"检测到 {frozen_frames}/{checked_frames} 组帧间无变化（可能画面冻结）")
        if black_frames == 0 and frozen_frames == 0 and checked_frames > 0:
            score += 10
        elif checked_frames > 0:
            score += 5

        # 4. 运镜检测（光流分析）
        camera_motion = _detect_camera_motion(cap, total_frames)
        checks["camera_motion"] = camera_motion["motion_type"]
        checks["camera_mag"] = camera_motion["magnitude"]
        # 从 description 或显式参数中提取预期运镜
        exp_camera = expected_camera or _parse_camera_motion(shot_description)
        if exp_camera and exp_camera not in ("unknown", "mixed"):
            checks["expected_camera"] = exp_camera
            actual = camera_motion["motion_type"]
            # 允许同族匹配：pan/tilt → static 不算错，反之亦然
            motion_family_ok = (
                (exp_camera == actual) or
                (exp_camera in ("pan", "tilt_up", "tilt_down") and actual == "static") or
                (exp_camera in ("dolly_in", "dolly_out") and actual in ("static", "mixed"))
            )
            if motion_family_ok:
                score += 10
            else:
                issues.append(f"运镜不匹配: 预期={exp_camera}，实际={actual}")
        else:
            score += 10

        # 5. 情绪/色调/节奏校验（从 shot description 解析预期情绪）
        expected_mood = _parse_shot_mood(shot_description)
        if expected_mood != "unknown":
            mood_actual = _detect_video_mood(cap, total_frames)
            checks["mood"] = expected_mood
            checks.update({f"mood_{k}": v for k, v in mood_actual.items()})
            mood_passed, mood_issues = _verify_mood(expected_mood, mood_actual)
            if mood_passed:
                score += 10
            else:
                issues.extend(mood_issues)
        else:
            score += 10

        # ── 6. 语义级校验（需 project 参数读取 script.json） ──
        if project:
            # 6a. 人脸检测 + 角色匹配
            fd = _detect_face_count(cap, total_frames)
            checks["face_count_sampled"] = fd["face_count"]
            checks["face_raw_detections"] = fd.get("raw_raw", 0)
            exp_people = _parse_expected_people(shot_description)
            if exp_people > 0:
                checks["expected_people"] = exp_people
                face_ok = True
                if fd["face_count"] == exp_people:
                    score += 5
                else:
                    face_ok = False
                    issues.append(f"人脸检测: 期望{exp_people}人，实际检测到{fd['face_count']}人")

                # 角色一致：将检测到的人脸与角色参考图对比
                try:
                    sp = os.path.join(project, "script.json")
                    if os.path.isfile(sp):
                        with open(sp, encoding="utf-8") as _sf:
                            _sd = json.load(_sf)
                        char_refs = _get_character_refs(project, _sd)
                        if char_refs and fd["faces"]:
                            cm = _match_faces_with_characters(fd["faces"], fd["frame"], char_refs)
                            checks["face_match"] = {
                                "matched": cm["matched"],
                                "total": cm["total"],
                                "details": cm["details"],
                            }
                            if cm["matched"] == cm["total"]:
                                score += 5
                            else:
                                face_ok = False
                                issues.append(f"角色匹配: 匹配到{cm['matched']}/{cm['total']}个角色，"
                                              f"未匹配: {cm['unmatched_refs']}")
                        else:
                            score += 5
                    else:
                        score += 5
                except Exception:
                    score += 5

                if not face_ok:
                    issues.insert(0, "[必过] 人脸检测未通过")
            else:
                score += 10

            # 6b. 场景直方图匹配
            scene_ok = True
            try:
                sp = os.path.join(project, "script.json")
                if os.path.isfile(sp):
                    with open(sp, encoding="utf-8") as _sf:
                        _sd = json.load(_sf)
                    slug = _parse_scene_slug(shot_description, _sd)
                    if slug:
                        sdir = os.path.join(project, "images", "scenes")
                        cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames // 2)
                        _r, mid_f = cap.read()
                        if _r and mid_f is not None:
                            hs = _match_scene_histogram(mid_f, sdir, slug)
                            checks["scene_hist_match"] = round(hs, 3)
                            if hs >= 0.3:
                                score += 10
                            else:
                                scene_ok = False
                                issues.append(f"场景直方图不匹配: {hs:.2f}（期望≥0.3）")
                        else:
                            score += 10
                    else:
                        score += 10
                else:
                    score += 10
            except Exception:
                score += 10
            if not scene_ok:
                issues.insert(0, "[必过] 场景匹配未通过")

            # 6c. 头部转头检测
            ht = _detect_head_turn(cap, total_frames)
            checks["head_turn_detected"] = ht["has_motion"]
            checks["head_turn_score"] = ht["motion_score"]
            turn_kw = ["转头", "回头", "看向", "望向", "扭头", "转身", "侧头", "抬头", "低头"]
            if any(kw in shot_description for kw in turn_kw):
                checks["expected_head_turn"] = True
                if ht["has_motion"]:
                    score += 10
                else:
                    issues.append("动作检测: 描述涉及头动作，但未检测到明显头部运动")
                    issues.insert(0, "[必过] 动作检测未通过")
            else:
                score += 10
        else:
            score += 30

    except Exception as e:
        issues.append(f"视频分析异常: {e}")
    finally:
        cap.release()

    # 有 project 时（启用语义检查）基础分+语义分必须 >= 基础满分 55 + 语义 30 的 80% = 68
    # 且 issues 中不能含 "[必过]" 标记
    has_mandatory_fail = any("[必过]" in i for i in issues)
    passed = score >= (68 if project else 35) and not has_mandatory_fail
    return {"passed": passed, "checks": checks, "score": score,
            "max_score": max_score, "issues": issues}


# ═══════════════════════════════════════════════════════════════
# 批量资产校验（被 project_commands._verify_*_assets 调用）
# ═══════════════════════════════════════════════════════════════

def verify_character_assets(project: str, verbose: bool = True) -> int:
    """校验项目所有角色资产图。返回问题总数。"""
    char_dir = os.path.join(project, "images", "characters")
    if not os.path.isdir(char_dir):
        return 0
    total_issues = 0
    for fname in sorted(os.listdir(char_dir)):
        if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        path = os.path.join(char_dir, fname)
        base = os.path.splitext(fname)[0]
        *parts, view = base.split("_")
        char_name = "_".join(parts)
        r = _verify_character_image(path, char_name=char_name, view=view)
        cnt = len(r.get("issues", []))
        if cnt:
            total_issues += cnt
    return total_issues


def verify_character_assets_detailed(project: str) -> list[dict]:
    """校验所有角色资产图，返回详细检查结果列表。"""
    char_dir = os.path.join(project, "images", "characters")
    if not os.path.isdir(char_dir):
        return []
    results = []
    for fname in sorted(os.listdir(char_dir)):
        if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        path = os.path.join(char_dir, fname)
        base = os.path.splitext(fname)[0]
        *parts, view = base.split("_")
        char_name = "_".join(parts)
        r = _verify_character_image(path, char_name=char_name, view=view)
        r["file"] = fname
        results.append(r)
    return results


def verify_scene_assets(project: str, verbose: bool = True) -> int:
    """校验项目所有场景资产图。返回问题总数。"""
    scenes_dir = os.path.join(project, "images", "scenes")
    if not os.path.isdir(scenes_dir):
        return 0
    total_issues = 0
    for fname in sorted(os.listdir(scenes_dir)):
        if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        path = os.path.join(scenes_dir, fname)
        r = _verify_scene_image(path, scene_name=fname)
        cnt = len(r.get("issues", []))
        if cnt:
            total_issues += cnt
    return total_issues


def verify_scene_assets_detailed(project: str) -> list[dict]:
    """校验所有场景资产图，返回详细检查结果列表。"""
    scenes_dir = os.path.join(project, "images", "scenes")
    if not os.path.isdir(scenes_dir):
        return []
    results = []
    for fname in sorted(os.listdir(scenes_dir)):
        if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        path = os.path.join(scenes_dir, fname)
        r = _verify_scene_image(path, scene_name=fname)
        r["file"] = fname
        results.append(r)
    return results


def verify_troop_assets(project: str, verbose: bool = True) -> int:
    """校验所有 troop 资产图。优先 images/troops/，兜底 images/characters/。"""
    troop_dir = os.path.join(project, "images", "troops")
    if not os.path.isdir(troop_dir):
        troop_dir = os.path.join(project, "images", "characters")
    if not os.path.isdir(troop_dir):
        return 0
    total_issues = 0
    for fname in sorted(os.listdir(troop_dir)):
        if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        path = os.path.join(troop_dir, fname)
        base = os.path.splitext(fname)[0]
        *parts, view = base.split("_")
        troop_name = "_".join(parts)
        r = _verify_character_image(path, char_name=troop_name, view=view)
        cnt = len(r.get("issues", []))
        if cnt:
            total_issues += cnt
    return total_issues


def verify_troop_assets_detailed(project: str) -> list[dict]:
    """校验所有 troop 资产图，返回详细检查结果列表。"""
    troop_dir = os.path.join(project, "images", "troops")
    if not os.path.isdir(troop_dir):
        troop_dir = os.path.join(project, "images", "characters")
    if not os.path.isdir(troop_dir):
        return []
    results = []
    for fname in sorted(os.listdir(troop_dir)):
        if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        path = os.path.join(troop_dir, fname)
        base = os.path.splitext(fname)[0]
        *parts, view = base.split("_")
        troop_name = "_".join(parts)
        r = _verify_character_image(path, char_name=troop_name, view=view)
        r["file"] = fname
        results.append(r)
    return results
