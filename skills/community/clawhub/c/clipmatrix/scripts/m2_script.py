"""
M2 文案内审 + 英文质量审核（阻断性）
- CTA完整性检查
- 句子长度 ≤32词
- 第一人称 ≥2次
- 场景重复检查（同账号历史）
- 视觉类型去重
"""
import json
import math
import re
import logging
from pathlib import Path
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)

# 场景 → 视觉类型
SCENE_TO_VISUAL_TYPE = {
    "夜景": "night_view", "天际线": "skyline", "灯火": "night_view",
    "雪山": "mountain", "山峰": "mountain", "山景": "mountain", "山峦": "mountain", "山脉": "mountain",
    "草原": "grassland", "牧场": "grassland", "花海": "grassland",
    "湖泊": "water", "湖面": "water", "江水": "water", "河流": "water", "江景": "water", "海子": "water",
    "藏寨": "village", "古镇": "village", "老街": "village",
    "茶馆": "culture", "寺庙": "religious", "佛塔": "religious", "经幡": "religious",
    "森林": "nature", "徒步": "nature", "峡谷": "nature", "竹林": "nature",
    "火锅": "food", "美食": "food", "小吃": "food",
    "酒店": "accommodation", "民宿": "accommodation",
    "街道": "street", "巷子": "street",
    "温泉": "wellness", "spa": "wellness",
    "索道": "transport", "高铁": "transport", "轻轨": "transport",
    "建筑": "architecture", "大桥": "architecture", "桥梁": "architecture",
    "日出": "sunrise_sunset", "日落": "sunrise_sunset", "夕阳": "sunrise_sunset",
    "星空": "night_view",
    "熊猫": "wildlife",
    "航拍": "aerial",
    "城市": "cityscape",
    "瀑布": "water",
}

# 英文→中文时间映射
EN_TO_CN_TIME = {
    "morning": "早晨", "dawn": "黎明", "sunrise": "日出",
    "day": "白天", "afternoon": "下午", "evening": "傍晚",
    "dusk": "黄昏", "night": "晚上", "midnight": "午夜",
}

# 英文→中文角度映射
EN_TO_CN_ANGLE = {
    "wide": "全景", "panorama": "全景", "panoramic": "全景",
    "close": "近景", "close-up": "近景", "macro": "微距",
    "aerial": "航拍", "drone": "航拍", "bird": "航拍",
    "travel": "旅拍", "vlog": "旅拍",
    "detail": "特写", "tracking": "跟拍",
}


def _scene_to_visual_type(scene: str) -> str:
    """提取场景的视觉类型"""
    for keyword, vtype in SCENE_TO_VISUAL_TYPE.items():
        if keyword in scene:
            return vtype
    return "general"


def _cn_time(en_time: str) -> str:
    """英文时间→中文"""
    return EN_TO_CN_TIME.get(en_time.lower(), en_time)


def _cn_angle(en_angle: str) -> str:
    """英文角度→中文"""
    return EN_TO_CN_ANGLE.get(en_angle.lower(), en_angle)


# ============================================================
# 方向地理区域定义（用于M2.5路线合理性校验）
# ============================================================
DIRECTION_ZONES = {
    "成都": {
        "city_center": ["文殊院", "宽窄巷子", "人民公园", "太古里", "春熙路",
                       "九眼桥", "安顺廊桥", "339电视塔", "锦江", "武侯祠",
                       "锦里", "杜甫草堂", "望江楼", "铁像寺水街", "玉林路",
                       "大慈寺"],
        "suburb": ["大熊猫基地", "西村大院", "麓湖"],
        "day_trip": ["都江堰", "青城山"],
        "far": ["乐山大佛", "峨眉山", "自贡"],
    },
    "重庆": {
        "city_center": ["解放碑", "洪崖洞", "来福士", "长江索道", "魁星楼",
                       "十八梯", "山城步道", "朝天门", "南滨路", "李子坝轻轨穿楼",
                       "鹅岭二厂"],
        "suburb": ["磁器口"],
        "day_trip": ["大足石刻", "武隆天生三桥", "南山一棵树"],
        "far": [],
    },
    "川西": {
        "gateway": ["康定"],
        "tagong_area": ["塔公草原", "墨石公园", "木雅大寺", "鱼子西", "格底拉姆"],
        "mountain": ["四姑娘山", "折多山"],
        "far": ["丹巴藏寨", "色达", "理塘", "稻城亚丁", "新都桥", "毕棚沟", "古尔沟", "海螺沟"],
    },
    "北川": {
        "jiuzhaigou": ["九寨沟"],
        "huanglong": ["黄龙"],
        "nearby": ["松潘古城", "牟尼沟", "达古冰川", "若尔盖"],
    },
    "川南": {
        "leshan": ["乐山大佛"],
        "emei": ["峨眉山"],
        "zigong": ["自贡"],
        "xichang": ["西昌邛海", "螺髻山"],
        "lugu": ["泸沽湖"],
        "dali": ["大理古城", "洱海", "沙溪古镇"],
    },
}


def get_scene_zone(scene_name: str, direction: str) -> str:
    """获取场景所属地理区域"""
    zones = DIRECTION_ZONES.get(direction, {})
    for zone, attractions in zones.items():
        for a in attractions:
            if a in scene_name:
                return zone
    return "unknown"


def check_route_logic(scenes: list, direction: str, style: str) -> (bool, list):
    """
    M2.5 路线合理性检查
    只抓最离谱的情况：同一场景名在列表中非相邻位置反复出现（纯AI幻觉），
    或相邻场景从郊区突跳回市中心但中间无过渡。
    """
    if not scenes or not direction:
        return True, []
    if style not in ("shadow_cut",):
        return True, []

    reasons = []

    # 检查1: 同样场景名在非相邻位置再次出现（A → ... → A, 间隔>1）
    for i, s1 in enumerate(scenes):
        for j in range(i + 2, len(scenes)):
            if scenes[j] == s1:
                reasons.append(f"场景'{s1}'在位置{i+1}和{j+1}重复出现，中间有{j-i-1}个其他场景，路线在绕圈。")

    # 检查2: 映射到区域后，检查city_center出现3次且被其他区域打断
    zone_seq = []
    for s in scenes:
        zone = get_scene_zone(s, direction)
        zone_seq.append((s, zone))

    if reasons:
        logger.warning(f"Route logic blocked: {'; '.join(reasons)}")
        return False, reasons
    return True, []


def check_cta(text: str) -> bool:
    """CTA质量检查 — 验证逻辑要素,不卡死不句式 (2026-06-01)
    
    三步验证:
    1. 排除垃圾CTA (comment below, follow for等)
    2. 确认有具体关键词/场景引用
    3. 确认有行动导向
    """
    t = text.lower().strip()
    
    # ❌ 一票否决: 垃圾CTA
    garbage = [
        r'\bcomment\s+below\b', r'\bfollow\s+for\s+more\b',
        r'\blet\s+us\s+know\b', r'\bwhat\s+do\s+you\s+think\b',
        r'\btell\s+us\b', r'\blike\s+and\s+subscribe\b',
        r'\bshare\s+this\b', r'\bdrop\s+a\s+comment\b',
    ]
    for pat in garbage:
        if re.search(pat, t, re.IGNORECASE):
            return False
    
    # ✅ 验证1: 有具体引用 (关键词、地名、场景)
    # 找ABC大写关键词
    has_keyword = bool(re.search(r'\b[A-Z]{2,}\b', text))  # DM us CHENGDU, message JIUZHAI
    # 或具体场景短语
    has_scenario = bool(re.search(
        r'\b(?:your|this|the|next|first|winter|summer|spring|autumn)\s+(?:\w+\s+){0,2}(?:trip|visit|adventure|journey|route|plan|guide|map|stay)\b',
        text, re.IGNORECASE))
    # 或具体交付物
    has_deliverable = bool(re.search(
        r'\b(?:itinerary|route|guide|map|checklist|plan|list|pin|secret|spot|timing|schedule|exact|full|complete)\b',
        text, re.IGNORECASE))
    
    if not (has_keyword or has_scenario or has_deliverable):
        return False
    
    # ✅ 验证2: 有行动导向
    action_patterns = [
        r'\bdm\b', r'\bsave\b', r'\bgrab\b', r'\bget\b', r'\bbook\b',
        r'\bmessage\b', r'\btap\b', r'\bclick\b', r'\bfind\b', r'\bcheck\b',
        r'\bdownload\b', r'\bkeep\b', r'\bpin\b', r'\bbookmark\b',
        r'\bsend\b', r'\b(?:reach|write)\s+(?:us|to)\b',
    ]
    has_action = any(re.search(pat, t) for pat in action_patterns)
    if not has_action:
        return False
    
    return True


def check_sentence_length(text: str) -> bool:
    """检查句子长度，所有句子≤40词（v10.0放宽，非阻断）"""
    sentences = re.split(r'[.!?]+', text)
    for s in sentences:
        words = s.strip().split()
        if len(words) > 40:
            logger.warning(f"Sentence too long ({len(words)} words): {s[:60]}...")
            return False
    return True


def check_first_person(text: str) -> bool:
    """检查第一人称出现次数≥2次（词边界匹配）"""
    count = len(re.findall(r'\b(I|We)\b', text))
    return count >= 2


def check_scene_duplicates(scenes: list, history_scenes: list, same_prefix_ok: bool = True) -> bool:
    """
    检查场景重复
    - 同账号最近3条历史：场景Jaccard≥60% → 拦截
    - 如果聚焦单景点（场景名相同前缀）放行
    """
    if not scenes or not history_scenes:
        return True  # No history → pass

    # 聚焦单景点：如果所有场景都以同一个前缀开头，放行
    if same_prefix_ok and len(scenes) >= 2:
        prefixes = set(s.split("_")[0] for s in scenes if "_" in s)
        if len(prefixes) <= 1:
            return True

    # Jaccard相似度
    current_set = set(s.lower().strip() for s in scenes)
    for hist in history_scenes:
        hist_set = set(s.lower().strip() for s in hist)
        if not current_set or not hist_set:
            continue
        jaccard = len(current_set & hist_set) / len(current_set | hist_set)
        if jaccard >= 0.6:
            logger.warning(f"Scene Jaccard too high: {jaccard:.2f}")
            return False

    return True


def check_visual_type_dedup(scenes: list, history_visual_types: list) -> bool:
    """
    视觉类型去重检查
    - 视觉类型重叠≥60% → 拦截
    """
    current_types = set(_scene_to_visual_type(s) for s in scenes)
    if not current_types or not history_visual_types:
        return True

    hist_types = set(history_visual_types)
    jaccard = len(current_types & hist_types) / len(current_types | hist_types)
    if jaccard >= 0.6:
        logger.warning(f"Visual type overlap too high: {jaccard:.2f}")
        return False

    return True


def check_speech_similarity(speech: str, history_speeches: list) -> bool:
    """检查口播文本相似度 ≥60% → 拦截(只对比最近1条历史)
    使用Jaccard相似度(交集/并集)，避免"day/drive/kilometers"等模板词误杀。
    """
    for hist in history_speeches[-1:]:
        if not hist:
            continue
        words_cur = set(speech.lower().split())
        words_hist = set(hist.lower().split())
        if not words_cur or not words_hist:
            continue
        # Jaccard: 交集 / 并集 （防止min分母过小导致模板词误杀）
        overlap = len(words_cur & words_hist)
        union = len(words_cur | words_hist)
        similarity = overlap / union if union > 0 else 0
        if similarity >= 0.6:
            logger.warning(f"Speech overlap too high: {similarity:.2f} (Jaccard)")
            return False
    return True


DEEPSEEK_API_KEY = None
DEEPSEEK_BASE_URL = "https://api.deepseek.com"


def get_api_key() -> str:
    global DEEPSEEK_API_KEY
    if DEEPSEEK_API_KEY:
        return DEEPSEEK_API_KEY
    auth_path = Path.home() / ".openclaw" / "agents" / "main" / "agent" / "auth-profiles.json"
    if auth_path.exists():
        try:
            with open(auth_path) as f:
                data = json.load(f)
            for val in data.get("profiles", {}).values():
                k = val.get("key", "") or val.get("api_key", "")
                if not k and "credentials" in val:
                    k = val["credentials"].get("api_key", "")
                if k:
                    DEEPSEEK_API_KEY = k
                    return k
        except:
            pass
    return os.environ.get("DEEPSEEK_API_KEY", "")


def generate_storyboard(speech_text, tts_duration, scene_input, account_info=None, history=None):
    """
    生成分镜 — 使用M1.5的scene_mapping
    scene_input: list[dict] (scene_mapping with scene/speech_segment/tags/effects)
               或 list[str] (场景名列表降级)
    """
    # 如果已经是mapping格式，直接用
    if scene_input and isinstance(scene_input[0], dict):
        mapping = scene_input
    else:
        # 降级：硬分配
        scenes = scene_input if isinstance(scene_input, list) else []
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', speech_text) if s.strip()]
        n_scene = min(len(scenes), 5) or 1
        sp = max(1, len(sentences) // n_scene) if sentences else 1
        mapping = []
        for i, sc in enumerate(scenes[:n_scene]):
            a = i * sp
            b = a + sp if i < n_scene - 1 else len(sentences)
            seg = " ".join(sentences[a:b]) if sentences else speech_text[:50]
            mapping.append({"scene":sc,"speech_segment":seg[:80],"tags":[sc],"effects":[]})

    # 去重：仅移除完全相同的条目（scene+speech_segment都相同才算重复）
    # 允许同名场景（如Velvet深挖模式所有scene用同一景点名）
    seen = set()
    unique = []
    for m in mapping:
        key = (m.get("scene",""), m.get("speech_segment","")[:20])
        if key not in seen:
            seen.add(key)
            unique.append(m)
    n_seg = len(unique)
    if n_seg < 2:
        unique = mapping[:min(2,len(mapping))]
        n_seg = len(unique)
    # 素材普遍不超过10s，单个分镜段控制在10s以内（盼哥2026-05-21指示）
    MAX_SEG_DUR = 10.0
    seg_time = tts_duration / n_seg
    if seg_time > MAX_SEG_DUR and n_seg > 1:
        # 需要更多段来消化时长
        needed = max(n_seg, math.ceil(tts_duration / MAX_SEG_DUR))
        if needed > n_seg:
            # 循环填充：不把额外段全堆在最后一个场景
            # 比如 [A,B,C,D] 需7段 → [A,B,C,D,A,B,C] 每场景最多2次
            for i in range(needed - n_seg):
                src = unique[i % n_seg]
                unique.append(src.copy() if isinstance(src, dict) else src)
            n_seg = len(unique)
        seg_time = tts_duration / n_seg
    sb = []
    for i, m in enumerate(unique):
        ts = round(i * seg_time, 1)
        te = round(tts_duration, 1) if i == n_seg - 1 else round((i + 1) * seg_time, 1)
        sb.append({"scene":m.get("scene",""),"start_sec":ts,"end_sec":te,
            "tags":m.get("tags",[m.get("scene","")]),"effects":m.get("effects",[]),
            "speech_snippet":m.get("speech_segment","")[:60],
            "visual_plan":m.get("visual_plan",{})})
    return {"storyboard":sb,"storyboard_id":f"sb_{hash(speech_text)%100000:05d}"}


def check_storyboard_similarity(storyboard, history):
    """分镜查重"""
    if not storyboard or not history: return True
    ct = set()
    for seg in storyboard:
        for t in seg.get("tags",[]): ct.add(str(t).lower())
    if not ct: return True
    for h in history:
        if not isinstance(h,dict): continue
        ht = set()
        for seg in h.get("storyboard",[]):
            for t in seg.get("tags",[]): ht.add(str(t).lower())
        if not ht: continue
        if len(ct&ht)/len(ct|ht) >= 0.6:
            logger.warning(f"Storyboard overlap: {(len(ct&ht)/len(ct|ht)):.2f}")
            return False
    return True


def check_script(script: dict, history: list = None,
                 direction: str = "", style: str = "") -> dict:
    """
    M2完整审核 + M2.5路线合理性
    返回: {"passed": bool, "reasons": [str], "checks": {...}}
    """
    speech_text = script.get("speech_text", "")
    caption = script.get("caption", "")
    scenes = script.get("scenes", [])

    checks = {}
    reasons = []

    # 1. CTA完整性（阻断性）
    cta_ok = check_cta(speech_text)
    checks["cta"] = cta_ok
    if not cta_ok:
        reasons.append("CTA not found in speech_text")
        logger.warning("CTA not found in speech_text")

    # 0. #pandajourneys 标签检查（非阻断，但记录警告）2026-05-31
    has_brand_tag = '#pandajourneys' in caption.lower()
    checks["brand_tag"] = has_brand_tag
    if not has_brand_tag:
        logger.warning("⚠️  #pandajourneys tag missing from caption (will be auto-injected)")

    # 0.5 文案/口播混淆检查（阻断）2026-05-31
    if caption and len(caption) > 20 and speech_text and len(speech_text) > 20:
        from difflib import SequenceMatcher
        sim = SequenceMatcher(None, caption.lower(), speech_text.lower()).ratio()
        # 触发条件: 整体相似度>0.55
        if sim > 0.55:
            reasons.append(f"Caption too similar to speech_text (sim={sim:.2f}) — write a DISTINCT social caption")
            checks["caption_distinct"] = False
            logger.warning(f"Caption overlaps speech_text: sim={sim:.2f}")
        else:
            checks["caption_distinct"] = True
    else:
        checks["caption_distinct"] = True

    # 2. 句子长度（非阻断，仅警告）
    length_ok = check_sentence_length(speech_text)
    checks["sentence_length"] = length_ok
    if not length_ok:
        logger.warning("Sentence exceeds 32 words (non-blocking)")

    # 3. 第一人称（不检查 — v10.0去掉强制要求）
    checks["first_person"] = True  # Always pass

    # 4. 场景重复（阻断性）
    scene_dup_ok = True
    if history:
        hist_scenes = [h.get("scenes", []) for h in history if isinstance(h, dict)]
        scene_dup_ok = check_scene_duplicates(scenes, hist_scenes)
        checks["scene_duplicate"] = scene_dup_ok
        if not scene_dup_ok:
            reasons.append("Scene duplicate with recent history (>60% Jaccard)")

    # 5. 口播相似度（阻断性）
    speech_sim_ok = True
    if history:
        hist_speeches = [h.get("speech_text", "") for h in history if isinstance(h, dict)]
        speech_sim_ok = check_speech_similarity(speech_text, hist_speeches)
        checks["speech_similarity"] = speech_sim_ok
        if not speech_sim_ok:
            reasons.append("Speech overlap >50% with history")

    # 6. 视觉类型去重
    visual_dup_ok = True
    if history:
        hist_visual = []
        for h in history:
            if isinstance(h, dict):
                hist_visual.extend(h.get("visual_types", []))
        visual_dup_ok = check_visual_type_dedup(scenes, hist_visual)
        checks["visual_type_dedup"] = visual_dup_ok
        if not visual_dup_ok:
            reasons.append("Visual type overlap >60% with history")

    # 7. M2.5 路线合理性检查（阻断性）
    route_ok, route_reasons = check_route_logic(scenes, direction, style)
    checks["route_logic"] = route_ok
    if not route_ok:
        reasons.extend(route_reasons)

    passed = all([
        cta_ok, scene_dup_ok, speech_sim_ok,
        visual_dup_ok, route_ok
    ])

    return {
        "passed": passed,
        "reasons": reasons,
        "checks": checks,
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    test_script = {
        "speech_text": "I just visited Wenshu Monastery in Chengdu. It was built in the Tang Dynasty. The architecture is incredible. The incense burners are massive. You need to see this for yourself. Follow me for more hidden gems in China.",
        "caption": "Hidden gem in Chengdu #ChinaTravel",
        "scenes": ["Chengdu_WenshuMonastery_courtyard", "Chengdu_WenshuMonastery_hall", "Chengdu_WenshuMonastery_garden"]
    }

    result = check_script(test_script)
    print(json.dumps(result, indent=2))
