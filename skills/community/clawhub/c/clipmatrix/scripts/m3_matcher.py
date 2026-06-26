"""
M3 素材匹配 — 场景名→关键词→素材库匹配
- 场景名转中文关键词（EN_TO_CN映射+中文提取）
- 扫素材库选打分最高者
- 素材缺口直接阻断，通知盼哥补
- 素材时长检查：太短的素材降分，让更长的素材优先
"""
import os
import re
import random
import logging
from config_loader import get_path
from pathlib import Path

logger = logging.getLogger(__name__)

LIBRARY_DIR = Path(get_path("library_dir"))

# 中文场景同义词（盼哥2026-05-21补充）
CN_SYNONYMS = {
    "安顺廊桥": ["九眼桥"],
    "九眼桥": ["安顺廊桥"],
    "锦江": ["九眼桥", "安顺廊桥"],
    "西昌邛海": ["邛海"],
    "邛海": ["西昌邛海"],
    "大理古城": ["大理古镇"],
    "大理古镇": ["大理古城"],
    # 春熙路商圈 (2026-06-01)
    "春熙路": ["IFS熊猫", "太古里"],
    "IFS熊猫": ["春熙路", "太古里"],
    "太古里": ["春熙路", "IFS熊猫"],
}

# 🔴 短素材黑名单 — 素材绝对时长<7s，M3拒绝选用（盼哥2026-05-24标注）
# 格式：文件名（不含路径），匹配时会跳过这些文件
SHORT_MATERIALS = {
    "重庆_洪崖洞_晚上_旅拍_3.mp4",  # 仅6.6s，不够任何场景
    "重庆_解放碑_晚上_旅拍.mp4",  # 仅6.8s，不够任何场景
    "北川_九寨沟_夏天_旅拍_2.mp4",  # 仅9.6s，临界时长易黑帧
}

# 英文→中文场景映射
EN_TO_CN_SCENE = {
    # 川南
    "shuxi": "蜀西竹海", "shuxi bamboo": "蜀西竹海",
    "shaxi": "沙溪古镇", "shaxi ancient": "沙溪古镇",
    # 成都
    "wenshu": "文殊院", "wenshu monastery": "文殊院", "monastery": "寺庙",
    "dujiangyan": "都江堰", "irrigation": "都江堰",
    "wide alley": "宽窄巷子", "narrow alley": "宽窄巷子", "kuanzhai": "宽窄巷子",
    "taikoo": "太古里", "taikoo li": "太古里",
    "chunxi": "春熙路", "chunxi road": "春熙路", "ifs": "IFS熊猫", "ifs panda": "IFS熊猫",
    "an shun": "安顺廊桥", "an shun bridge": "安顺廊桥",
    "339 tower": "339电视塔", "339 tv": "339电视塔",
    "jinjiang": "锦江", "jin river": "锦江",
    "bamboo": "竹林小径", "bamboo path": "竹林小径",
    "teahouse": "茶馆",
    # 重庆
    "hongya": "洪崖洞", "hongya cave": "洪崖洞",
    "raffles": "来福士",
    "liziba": "李子坝轻轨", "light rail": "李子坝轻轨",
    "yangtze cable": "长江索道", "cable car": "长江索道",
    "mountain city": "山城步道", "mountain steps": "山城步道",
    "kuixing": "魁星楼",
    "18 stairs": "十八梯", "shibati": "十八梯", "shitbati": "十八梯",
    "erling": "鹅岭二厂",
    "shancheng": "山城", "mountaincity": "山城",
    "yangtze": "长江",
    "chaotian": "朝天门", "chaotianmen": "朝天门",
    "nantai": "南山一棵树", "nantai temple": "南山一棵树",
    "nanbin": "南滨路",
    # 川西
    "sister mountain": "四姑娘山", "siguniang": "四姑娘山", "four girls": "四姑娘山",
    "tagong": "塔公草原", "tagong grassland": "塔公草原", "yak": "塔公草原",
    "moshi": "墨石公园", "black rock": "墨石公园", "moxi": "墨石公园",
    "yuzi": "鱼子西", "yuzi west": "鱼子西",
    "gedilamu": "格底拉姆",
    "muyadasi": "木雅大寺",
    "guergou": "古尔沟",
    "bipeng": "毕棚沟",
    "kangding": "康定",
    "grassland": "草原",
    "snow mountain": "雪山", "snowmountain": "雪山",
    "tibetan": "藏寨",
    # 北川
    "jiuzhai": "九寨沟", "jiuzhaigou": "九寨沟",
    "huanglong": "黄龙",
    "songpan": "松潘古城",
    "munigou": "牟尼沟",
    "dagu": "达古冰川",
    # 川南
    "xichang": "西昌",
    "qionghai": "邛海",
    "luoji": "螺髻山", "luojishan": "螺髻山",
    "panzhihua": "攀枝花",
    "lugu": "泸沽湖", "luguhu": "泸沽湖",
    "dali": "大理", "dali old town": "大理古城",
    "erhai": "洱海",
    "zigong": "自贡",
    "zigong dinosaur": "自贡恐龙博物馆", "dinosaur museum": "自贡恐龙博物馆",
    "lijiang": "丽江", "lijiang old town": "丽江古城",
    "yulong": "玉龙雪山", "jade dragon": "玉龙雪山",
    "cangshan": "苍山",
    "shuanglang": "双廊",
    "xizhou": "喜洲",
    "shuhe": "束河",
    "shangri": "香格里拉", "shangri-la": "香格里拉",
    "hutiao": "虎跳峡", "tiger leaping": "虎跳峡",
    # 通用
    "night": "夜景", "night view": "夜景",
    "sunset": "日落", "sunrise": "日出",
    "river": "江景",
    "lake": "湖面",
    "aerial": "航拍",
    "street": "街道",
}

# 英文→中文时间映射
EN_TO_CN_TIME = {
    "morning": "早晨", "dawn": "黎明", "sunrise": "日出",
    "day": "白天", "afternoon": "下午", "evening": "傍晚",
    "dusk": "黄昏", "night": "晚上", "midnight": "午夜",
    "spring": "春天", "summer": "夏天", "autumn": "秋天", "winter": "冬天",
}

# 英文→中文角度映射
EN_TO_CN_ANGLE = {
    "wide": "全景", "panorama": "全景", "panoramic": "全景",
    "close": "近景", "close-up": "近景", "macro": "微距",
    "aerial": "航拍", "drone": "航拍", "bird eye": "航拍",
    "travel": "旅拍", "vlog": "旅拍",
    "detail": "特写", "tracking": "跟拍",
    "selfie": "自拍", "selfie stick": "自拍",
    "mix": "混剪",
}


def load_all_materials(orientation: str = None) -> list:
    """加载所有素材文件
    orientation: 'portrait'(竖屏) | 'landscape'(横屏) | None(全部)
    """
    if not LIBRARY_DIR.exists():
        logger.warning(f"Library dir not found: {LIBRARY_DIR}")
        return []

    materials = []
    search_dirs = []
    
    if orientation == 'portrait':
        search_dirs = [LIBRARY_DIR / '竖屏']
    elif orientation == 'landscape':
        search_dirs = [LIBRARY_DIR / '横屏']
    else:
        search_dirs = [LIBRARY_DIR, LIBRARY_DIR / '竖屏', LIBRARY_DIR / '横屏']
    
    for d in search_dirs:
        if d.exists():
            for f in d.iterdir():
                if f.suffix.lower() in (".mp4", ".mov", ".MP4", ".MOV"):
                    materials.append(str(f))
    return sorted(materials)


def scene_to_cn_keywords(scene_desc: str) -> list:
    """将英文场景描述转为中文关键词列表"""
    keywords = []
    desc_lower = scene_desc.lower()

    # 直接映射
    for en_key, cn_val in EN_TO_CN_SCENE.items():
        if en_key in desc_lower:
            keywords.append(cn_val)

    # 提取_中的中文部分（如果场景是 mix 格式）
    parts = scene_desc.split("_")
    for p in parts:
        if re.search(r'[\u4e00-\u9fff]', p):
            keywords.append(p)

    # 对长中文场景名做简称提取（素材文件名可能用简称）
    short_names = {
        "李子坝轻轨穿楼": "李子坝",
        "大理古城": "大理",
        "大熊猫基地": "熊猫",
        "339电视塔": "339",
        "天府广场": "成都",
        "武隆天生三桥": "武隆",
        "南山一棵树": "南山",
        "乐山大佛": "乐山",
    }
    for full, short in short_names.items():
        if full in scene_desc and short not in keywords:
            keywords.append(short)

    # 中文同义词扩展（安顺廊桥→九眼桥等）
    for keyword in list(keywords):
        if keyword in CN_SYNONYMS:
            for syn in CN_SYNONYMS[keyword]:
                if syn not in keywords:
                    keywords.append(syn)

    return list(set(keywords))


def _get_material_duration(path: str) -> float:
    """获取素材时长（秒），失败返回999"""
    import subprocess, json
    try:
        r = subprocess.run([
            'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
            '-of', 'json', path
        ], capture_output=True, text=True, timeout=10)
        data = json.loads(r.stdout)
        return float(data.get('format', {}).get('duration', 999))
    except:
        return 999


# 分辨率缓存，避免重复ffprobe
_material_width_cache = {}

def _get_material_width(path: str) -> int:
    """获取素材宽度（像素），带缓存，失败返回0"""
    if path in _material_width_cache:
        return _material_width_cache[path]
    import subprocess, json
    try:
        r = subprocess.run([
            'ffprobe', '-v', 'quiet', '-select_streams', 'v:0',
            '-show_entries', 'stream=width', '-of', 'json', path
        ], capture_output=True, text=True, timeout=10)
        data = json.loads(r.stdout)
        w = int(data['streams'][0]['width'])
    except:
        w = 0
    _material_width_cache[path] = w
    return w


def find_best_match(scene_desc: str, exclude_files: set = None,
                    orientation: str = None,
                    required_duration: float = None) -> dict:
    """
    为场景找最佳素材
    exclude_files: 同视频已用的素材文件，不允许重复
    orientation: 'portrait'(竖屏) | 'landscape'(横屏) | None(全部)
    required_duration: 场景需要的时长（秒），素材太短则降分
    返回: {"path": str, "confidence": str, "reason": str}
    """
    if exclude_files is None:
        exclude_files = set()

    materials = load_all_materials(orientation)
    if not materials:
        if orientation:
            materials = load_all_materials()
        if not materials:
            return {"path": "", "confidence": "none", "reason": "no materials"}

    cn_keywords = scene_to_cn_keywords(scene_desc)
    candidates = []

    for mat in materials:
        bn = os.path.basename(mat)
        if bn in exclude_files:
            continue
        if bn in SHORT_MATERIALS:
            continue  # 🔴 短素材黑名单，盼哥标注

        mat_name_lower = mat.lower()
        mat_bn_lower = bn.lower()

        score = 0
        matched_keywords = []

        # 关键词匹配
        for kw in cn_keywords:
            if kw.lower() in mat_name_lower or kw.lower() in mat_bn_lower:
                score += 10
                matched_keywords.append(kw)

        # 精确场景名映射匹配
        scene_lower = scene_desc.lower()
        for en_key, cn_val in EN_TO_CN_SCENE.items():
            if en_key in scene_lower:
                cn_match = cn_val.lower()
                if cn_match in mat_name_lower or cn_match in mat_bn_lower:
                    score += 20
                    if cn_val not in matched_keywords:
                        matched_keywords.append(cn_val)

        if score > 0:
            # 🔧 素材时长检查：太短则降分，极短则拒绝
            if required_duration:
                mat_dur = _get_material_duration(mat)
                if mat_dur < required_duration * 0.5:
                    logger.info(f"  {bn} duration {mat_dur:.1f}s < "
                                f"50% of required {required_duration:.1f}s, REJECTED")
                    continue  # 拒绝太短的素材，防黑帧
                elif mat_dur < required_duration * 0.7:
                    score -= 5
                    logger.info(f"  {bn} duration {mat_dur:.1f}s < "
                                f"required {required_duration:.1f}s, score penalty")
            # 🔧 分辨率优先：同分时1080p+/4K素材赢过720p
            mat_w = _get_material_width(mat)
            if mat_w >= 3000:
                score += 4  # 4K+
            elif mat_w >= 1900:
                score += 2  # 1080p+
            elif mat_w <= 1290:
                score -= 1  # 720p，轻微惩罚
            candidates.append({"path": mat, "score": score, "keywords": matched_keywords})

    if candidates:
        candidates.sort(key=lambda x: x["score"], reverse=True)
        top_score = candidates[0]["score"]
        top_tier = [c for c in candidates if c["score"] >= top_score * 0.8]
        chosen = random.choice(top_tier)
        logger.info(f"Matched: {scene_desc} → {os.path.basename(chosen['path'])} "
                    f"(score={chosen['score']}, kw={chosen['keywords']})")
        return {"path": chosen["path"], "confidence": "high" if chosen["score"] >= 15 else "medium",
                "reason": f"matched keywords: {chosen['keywords']}"}

    return {"path": "", "confidence": "none", "reason": f"no match for: {scene_desc}"}


def match_scenes(scenes: list, orientation: str = 'portrait',
                 scene_durations: list = None) -> list:
    """
    为所有场景匹配素材，同视频内不重复使用同一素材文件
    盼哥铁律：同一视频内同一素材文件不可复用
    scene_durations: 每个场景所需时长列表，与scenes一一对应
    返回: [{"scene": str, "path": str, "confidence": str}, ...]
    """
    exclude_files = set()
    results = []
    for i, scene in enumerate(scenes):
        req_dur = scene_durations[i] if scene_durations and i < len(scene_durations) else None
        result = find_best_match(scene, exclude_files, orientation=orientation,
                                 required_duration=req_dur)
        if result["path"]:
            exclude_files.add(os.path.basename(result["path"]))
        results.append({
            "scene": scene,
            "path": result["path"],
            "confidence": result.get("confidence", "none"),
            "reason": result.get("reason", ""),
        })

    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    test_scenes = ["Chengdu_WenshuMonastery_courtyard", "Chengdu_BambooPath_morning"]
    results = match_scenes(test_scenes)
    for r in results:
        print(f"  {r['scene']} → {r['path'][:50]} ({r['confidence']})")
