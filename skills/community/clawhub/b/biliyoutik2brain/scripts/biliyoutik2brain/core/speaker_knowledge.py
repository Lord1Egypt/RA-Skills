"""
说话人知识库（v2.1）
真实身份是根，平台是分支。支持跨平台矩阵号映射。
自动积累UP主的交易体系知识，越用越准。

v2.1 新增:
  - 错题类型集: 按错误原因分类(同音/韵母/数字/外语), 非1:1订正
  - 声学特征档案: 语速/口音/口头禅/清晰度 → 反哺ASR
  - 反哺函数: format_asr_hints / format_llm_hints
"""

import os, json, time, copy
from typing import Dict, List, Optional

KNOWLEDGE_FILE = os.path.expanduser("~/.biliyoutik2brain_speakers.json")

_DEFAULT_PROFILE_TEMPLATE = {
    "real_name": "",
    "platforms": {},
    "aliases": [],
    "background": "",
    "domain": "",
    "trading_style": "",
    "common_topics": [],
    "known_patterns": [],
    "known_mistakes": {},
    # ── v2.1 错题类型集 ──
    "error_categories": {
        "homophone":      {"label": "术语同音替换", "count": 0, "examples": []},
        "rhyme_confusion": {"label": "韵母混淆",   "count": 0, "examples": []},
        "number_mishear": {"label": "数字序列误听", "count": 0, "examples": []},
        "bilingual_mix":  {"label": "外语词混合",   "count": 0, "examples": []},
        "filler_noise":   {"label": "口头禅误入",   "count": 0, "examples": []},
        "unknown":        {"label": "其他未分类",   "count": 0, "examples": []},
    },
    # ── v2.1 声学特征 ──
    "acoustic_profile": {
        "speech_rate": 0.0,
        "speech_rate_label": "",
        "accent_type": "",
        "clarity_score": 0.0,
        "filler_words": [],
        "pitch_pattern": "",
        "samples_processed": 0,
    },
    "processed_videos": [],
    "last_updated": "",
}


def _load() -> Dict:
    """加载说话人知识库"""
    if os.path.exists(KNOWLEDGE_FILE):
        try:
            with open(KNOWLEDGE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def _save(db: Dict):
    """保存说话人知识库"""
    os.makedirs(os.path.dirname(KNOWLEDGE_FILE), exist_ok=True)
    with open(KNOWLEDGE_FILE, "w") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def _normalize_speaker(uploader: str) -> str:
    """归一化说话人名称 → 返回数据库主键（real_name 或第一个别名）

    v2.0 查找顺序:
      1. uploader 本身就是数据库中的 key（real_name 或旧主名）
      2. uploader 出现在某个 profile 的 aliases 中
      3. uploader 出现在某个 profile 的 platforms 值中
      4. 都没找到 → 返回 uploader 本身（新UP主）
    """
    if not uploader:
        return ""
    db = _load()
    uploader = uploader.strip()

    # 1) 本身就是 key
    if uploader in db:
        return uploader

    # 2) 匹配 aliases（回溯兼容）
    for main_name, profile in db.items():
        if uploader in profile.get("aliases", []):
            return main_name

    # 3) 匹配 platforms 的值
    for main_name, profile in db.items():
        if uploader in profile.get("platforms", {}).values():
            return main_name

    # 4) 新UP主
    return uploader


def _rebuild_aliases(profile: Dict) -> None:
    """从 real_name + platforms 自动重建 aliases 列表"""
    all_names = set(profile.get("aliases", []))

    real = profile.get("real_name", "")
    if real:
        all_names.add(real)

    for platform_name in profile.get("platforms", {}).values():
        if platform_name:
            all_names.add(platform_name)

    # 去掉自己（如果 real_name 是 key，不要在 aliases 里出现）
    profile["aliases"] = sorted([a for a in all_names if a])


def _is_financial_term(word: str) -> bool:
    """判断一个词是否可能是金融/交易术语（用于过滤自动学习）"""
    financial_signals = [
        "交易", "止损", "止盈", "仓位", "杠杆", "做多", "做空", "点差",
        "均线", "K线", "趋势", "突破", "回调", "支撑", "阻力", "盘口",
        "缠论", "背离", "震荡", "量价", "主力", "机构", "多空", "持仓",
        "回撤", "加仓", "减仓", "开仓", "平仓", "挂单", "市价", "限价",
        "盈亏", "风险", "本金", "余额", "净值", "保证金", "强平", "爆仓",
        "形态", "指标", "信号", "周期", "级别", "段", "笔", "中枢",
        "孕线", "吞没", "锤子", "流星", "十字星", "顶分型", "底分型",
        "MT4", "MT5", "EA", "EA交易", "量化", "回测", "优化",
        "FVG", "ATR", "EMA", "SMA", "RSI", "MACD", "布林",
        "USD", "JPY", "EUR", "GBP", "外汇", "期货", "股票",
    ]
    lowered = word.lower()
    for sig in financial_signals:
        if sig.lower() in lowered or (len(sig) >= 2 and sig[0] + sig[1:].lower() == lowered):
            return True
    return False


def _guess_domain(video_title: str = "", keywords: List[str] = None, uploader: str = "") -> str:
    """根据视频标题、关键词和UP主名猜测领域标签"""
    if not video_title and not keywords and not uploader:
        return ""

    domain_keywords = {
        "trading": ["交易", "止损", "K线", "止盈", "仓位", "杠杆",
                     "股票", "期货", "外汇", "基金", "行情", "大盘",
                     "趋势", "突破", "回调", "支撑", "阻力", "均线",
                     "点数", "盈利", "亏损", "做多", "做空", "缠论",
                     "机构", "主力", "量价", "盘口"],
        "life": ["生活", "美食", "旅行", "vlog", "日常", "开箱"],
        "tech": ["编程", "教程", "技术", "代码", "开发者", "开源"],
    }

    text = (video_title or "") + " " + (uploader or "") + " " + " ".join(keywords or [])

    for domain, kws in domain_keywords.items():
        for kw in kws:
            if kw in text:
                return domain
    return "general"


def _estimate_clarity_from_text(text: str) -> float:
    """从文本估算说话清晰度

    简单启发式: 重复字率 + 断句频率 + 口头禅密度
    返回 0-1 分数（1=最清晰）
    """
    if not text or len(text) < 50:
        return 0.5

    # 断句频率: 标点密度
    punct_count = sum(1 for c in text if c in '。！？，、；')
    punct_density = punct_count / max(len(text), 1)

    # 重复字检测: 连续重复2次以上
    repeat_pattern = 0
    for i in range(len(text) - 1):
        if text[i] == text[i + 1] and text[i:i+2] not in {'好好', '慢慢', '刚刚'}:
            repeat_pattern += 1

    # 口头禅密度
    filler_hit = sum(1 for w in ['然后', '就是', '这个', '那个', '对吧', '你看']
                     if w in text)

    score = 0.8  # 起步分
    score += min(punct_density * 5, 0.15)   # 标点多=更有条理
    score -= min(repeat_pattern * 0.02, 0.15)  # 重复=不清晰
    score -= min(filler_hit * 0.02, 0.1)       # 口头禅多=不清晰

    return round(max(0.3, min(0.95, score)), 2)


def _learn_mistakes_from_corrections(speaker: str, corrections: List[Dict]) -> int:
    if not speaker or not corrections:
        return 0

    db = _load()
    main_name = _normalize_speaker(speaker)
    profile = db.setdefault(main_name, copy.deepcopy(_DEFAULT_PROFILE_TEMPLATE))
    existing = profile.setdefault("known_mistakes", {})

    noise_words = {"啊", "哦", "嗯", "这个", "那个", "对吧", "然后", "就是"}
    learned = 0

    for corr in corrections:
        original = corr.get("original", "").strip()
        corrected = corr.get("corrected", "").strip()
        conf = corr.get("confidence", 0)

        if not original or not corrected or original == corrected:
            continue
        if len(original) <= 1 or len(corrected) <= 1:
            continue
        if original in noise_words:
            continue
        if original in existing and existing[original] == corrected:
            continue
        if not _is_financial_term(corrected) and not _is_financial_term(original):
            continue
        if conf < 0.4:
            continue

        if original in existing:
            if conf > 0.7:
                existing[original] = corrected
                learned += 1
        else:
            existing[original] = corrected
            learned += 1

    if learned:
        profile["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
        # ── v2.1: 自动分类错题 ──
        _classify_mistakes(profile, existing, learned)
        _save(db)
        print(f"  [特征学习] 🧠 {speaker}: 自动记录了 {learned} 条误认修正")

    return learned


# ═══════════════════════════════════════════════════════════════
#  v2.1 错题类型集
# ═══════════════════════════════════════════════════════════════

def _classify_mistake(wrong: str, right: str) -> str:
    """将一条误认修正分类到错误类型

    分类规则（按优先级）:
      homophone:      同音/近音不同字 (韵母相同, 声母相近)
      rhyme_confusion: 韵母不同但声母相同 (前/后鼻音, 平/翘舌)
      number_mishear:  数字/数值
      bilingual_mix:   中英混合
      filler_noise:    口头禅/语气词
      unknown:         其他
    """
    if not wrong or not right:
        return "unknown"

    # 数字类
    if any(c.isdigit() for c in wrong) or any(c.isdigit() for c in right):
        return "number_mishear"

    # 中英混合
    has_en = any(ord(c) < 128 and c.isalpha() for c in wrong) or \
             any(ord(c) < 128 and c.isalpha() for c in right)
    has_cn = any('\u4e00' <= c <= '\u9fff' for c in wrong) or \
             any('\u4e00' <= c <= '\u9fff' for c in right)
    if has_en and has_cn:
        return "bilingual_mix"

    # 口头禅/语气词
    filler_patterns = {"啊", "哦", "嗯", "呢", "吧", "嘛", "啦", "哈", "唉",
                       "这个", "那个", "是吧", "对吧", "然后", "就是"}
    lower_wrong = wrong.strip()
    if lower_wrong in filler_patterns or len(wrong) <= 1:
        return "filler_noise"

    # 韵母混淆 (前后鼻音 an/ang, en/eng, in/ing)
    rhyme_pairs = [
        ('an', 'ang'), ('en', 'eng'), ('in', 'ing'),
        ('ian', 'iang'), ('uan', 'uang'),
        ('zhi', 'zi'), ('chi', 'ci'), ('shi', 'si'),
    ]
    for a, b in rhyme_pairs:
        has_a = a in wrong or a in right
        has_b = b in wrong or b in right
        if has_a != has_b:  # 一个有一个没有
            return "rhyme_confusion"

    # 默认为同音替换
    return "homophone"


def _classify_mistakes(profile: Dict, mistakes: Dict, new_count: int):
    """将新学的误认分类到错题类型集"""
    cats = profile.setdefault("error_categories", {
        "homophone": {"label": "术语同音替换", "count": 0, "examples": []},
        "rhyme_confusion": {"label": "韵母混淆", "count": 0, "examples": []},
        "number_mishear": {"label": "数字序列误听", "count": 0, "examples": []},
        "bilingual_mix": {"label": "外语词混合", "count": 0, "examples": []},
        "filler_noise": {"label": "口头禅误入", "count": 0, "examples": []},
        "unknown": {"label": "其他未分类", "count": 0, "examples": []},
    })

    for wrong, right in mistakes.items():
        cat = _classify_mistake(wrong, right)
        if cat in cats:
            cats[cat]["count"] += 1
            example = f"{wrong}→{right}"
            if example not in cats[cat]["examples"]:
                cats[cat]["examples"].append(example)
                cats[cat]["examples"] = cats[cat]["examples"][-10:]  # 保留最近10条


def format_asr_hints(speaker: str) -> str:
    """生成ASR引擎提示（根据说话人声学特征+错题类型）

    用于在转录前传递给声学模型，提高准确率。
    示例: "该UP主语速较快(5.2字/秒), 有浙江口音倾向, 常混淆前后鼻音"
    """
    profile = get_profile(speaker)
    if not profile:
        return ""

    hints = []
    acoustic = profile.get("acoustic_profile", {})

    # 语速提示
    rate = acoustic.get("speech_rate", 0)
    if rate > 5.0:
        hints.append(f"语速较快({rate:.1f}字/秒), 建议降低VAD敏感度")
    elif rate > 3.5:
        hints.append(f"语速中等({rate:.1f}字/秒)")
    elif rate > 0:
        hints.append(f"语速较慢({rate:.1f}字/秒)")

    # 口音提示
    accent = acoustic.get("accent_type", "")
    if accent:
        hints.append(f"有{accent}口音倾向, 注意韵母辨识")

    # 口头禅
    fillers = acoustic.get("filler_words", [])
    if fillers:
        hints.append(f"口头禅: {'、'.join(fillers[:5])}")

    # 错题类型提示
    cats = profile.get("error_categories", {})
    if cats:
        top_errors = sorted(cats.items(), key=lambda x: x[1]["count"], reverse=True)
        for cat_name, cat_data in top_errors[:2]:
            if cat_data["count"] >= 3:
                hints.append(f"{cat_data['label']}高发({cat_data['count']}次)")

    if not hints:
        return ""

    name = profile.get("real_name", speaker)
    return f"[{name}] " + "; ".join(hints)


def format_llm_hints(speaker: str) -> str:
    """生成LLM修正提示（根据错题类型集）

    用于在转录修正时传递给LLM，提供靶向修正线索。
    """
    profile = get_profile(speaker)
    if not profile:
        return ""

    hints = []
    cats = profile.get("error_categories", {})
    known = profile.get("known_mistakes", {})

    if cats:
        for cat_name, cat_data in cats.items():
            if cat_data["count"] >= 3:
                examples = cat_data.get("examples", [])[:5]
                ex_str = f"如 {' | '.join(examples)}"
                hints.append(f"【{cat_data['label']}】{cat_data['count']}次 {ex_str}")

    if known:
        top_mistakes = list(known.items())[:5]
        flat = " | ".join(f"{w}→{r}" for w, r in top_mistakes)
        hints.append(f"已知误认: {flat}")

    if not hints:
        return ""

    name = profile.get("real_name", speaker)
    return f"## {name} 的错题类型集\n" + "\n".join(hints)


# ═══════════════════════════════════════════════════════════════
#  v2.1 声学特征管理
# ═══════════════════════════════════════════════════════════════

def update_acoustic(
    speaker: str,
    speech_rate: float = 0.0,
    accent_type: str = "",
    clarity_score: float = 0.0,
    filler_words: List[str] = None,
    pitch_pattern: str = "",
):
    """更新说话人声学特征（加权移动平均）"""
    if not speaker:
        return

    db = _load()
    main_name = _normalize_speaker(speaker)
    profile = db.setdefault(main_name, copy.deepcopy(_DEFAULT_PROFILE_TEMPLATE))
    ac = profile.setdefault("acoustic_profile", {
        "speech_rate": 0.0, "speech_rate_label": "",
        "accent_type": "", "clarity_score": 0.0,
        "filler_words": [], "pitch_pattern": "",
        "samples_processed": 0,
    })

    n = ac.get("samples_processed", 0) + 1

    # 语速: 加权平均
    if speech_rate > 0:
        old = ac.get("speech_rate", 0)
        ac["speech_rate"] = round((old * (n - 1) + speech_rate) / n, 1)

    # 语速标签
    rate = ac["speech_rate"]
    ac["speech_rate_label"] = "快" if rate > 5.0 else ("慢" if rate < 3.0 else "中")

    # 清晰度
    if clarity_score > 0:
        old_c = ac.get("clarity_score", 0)
        ac["clarity_score"] = round((old_c * (n - 1) + clarity_score) / n, 1)

    # 口音、口头禅、语调 (直接覆盖，通常不变)
    if accent_type:
        ac["accent_type"] = accent_type
    if filler_words:
        for w in filler_words:
            if w not in ac.get("filler_words", []):
                ac.setdefault("filler_words", []).append(w)
    if pitch_pattern:
        ac["pitch_pattern"] = pitch_pattern

    ac["samples_processed"] = n
    profile["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    _save(db)
    print(f"  [声学] 🎤 {speaker}: 语速={ac['speech_rate']}字/秒({ac['speech_rate_label']}), "
          f"清晰度={ac['clarity_score']:.2f}, 样本={n}")


def add_filler_words(speaker: str, words: List[str]):
    """添加口头禅"""
    if not speaker or not words:
        return
    db = _load()
    main_name = _normalize_speaker(speaker)
    profile = db.setdefault(main_name, copy.deepcopy(_DEFAULT_PROFILE_TEMPLATE))
    ac = profile.setdefault("acoustic_profile", {})
    for w in words:
        if w not in ac.get("filler_words", []):
            ac.setdefault("filler_words", []).append(w)
    _save(db)


def _learn_patterns_from_analysis(speaker: str, analysis: Dict) -> int:
    """自动从分析结果中提取说话人常见的交易规律/观点模式"""
    if not speaker or not analysis:
        return 0

    db = _load()
    main_name = _normalize_speaker(speaker)
    profile = db.setdefault(main_name, copy.deepcopy(_DEFAULT_PROFILE_TEMPLATE))
    existing = set(profile.get("known_patterns", []))

    summary = analysis.get("summary", "")
    learned = 0

    pattern_indicators = ["核心", "框架", "体系", "一直", "每次", "始终", "坚持",
                          "原则", "纪律", "规则", "策略", "思路", "逻辑", "理念"]

    if summary:
        for line in summary.split("\n"):
            line = line.strip()
            if len(line) < 10 or len(line) > 120:
                continue
            if any(ind in line for ind in pattern_indicators):
                if line not in existing:
                    profile.setdefault("known_patterns", []).append(line)
                    existing.add(line)
                    learned += 1

    if learned:
        profile["known_patterns"] = profile["known_patterns"][:20]
        profile["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
        _save(db)
        print(f"  [规律学习] 🧠 {speaker}: 自动提取了 {learned} 条观点模式")

    return learned


# ═══════════════════════════════════════════════════════════════
#  v2.0 跨平台身份映射
# ═══════════════════════════════════════════════════════════════

def link_identity(real_name: str, platform: str, username: str):
    """建立跨平台映射：真实身份 ← 平台用户名

    示例:
      link_identity("张扬", "bilibili", "张聚贤")
      link_identity("张扬", "youtube", "tntsunrise")
      link_identity("张扬", "xiaohongshu", "胖杰克")

    - 如果 real_name 还不存在 → 自动创建 profile
    - 如果 username 已属于另一个 profile → 自动迁移并合并
    """
    if not real_name or not platform or not username:
        return

    db = _load()
    real_name = real_name.strip()
    platform = platform.strip().lower()
    username = username.strip()

    # 检查 username 是否已有独立 profile 或属于别人
    existing_owner = _normalize_speaker(username)

    # 张三在db里是个独立profile → 需要迁移
    if existing_owner in db and existing_owner != real_name:
        print(f"  [身份] ⚠️ {username} 当前独立 profile {existing_owner}，将迁移到 {real_name}")
        _migrate_platform_to(existing_owner, real_name, platform, username)
        return

    # 如果 _normalize_speaker 返回的人 ≠ real_name（属于别人的映射）
    if existing_owner not in db and existing_owner != real_name:
        # username 是新用户 → 正常注册
        pass

    # 正常流程：注册映射
    profile = db.setdefault(real_name, copy.deepcopy(_DEFAULT_PROFILE_TEMPLATE))

    if not profile.get("real_name"):
        profile["real_name"] = real_name

    # 注册平台映射
    profile.setdefault("platforms", {})
    old_val = profile["platforms"].get(platform)
    if old_val and old_val != username:
        print(f"  [身份] {real_name} 的 {platform} 平台: {old_val} → {username}")

    profile["platforms"][platform] = username

    # 自动维护 aliases
    _rebuild_aliases(profile)
    profile["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")

    _save(db)
    print(f"  [身份] ✅ 已关联: {real_name} ← {platform}:{username}")


def _migrate_platform_to(from_owner: str, to_real_name: str, platform: str, username: str):
    """将某个平台账号从旧 owner 迁移到新 real_name 下"""
    db = _load()

    sp = db.get(from_owner, {})
    tp = db.setdefault(to_real_name, copy.deepcopy(_DEFAULT_PROFILE_TEMPLATE))

    # 迁移 platform 映射
    if platform in sp.get("platforms", {}):
        del sp["platforms"][platform]
    tp.setdefault("platforms", {})[platform] = username

    # 迁移该用户名下的视频记录
    migrated_videos = 0
    for v in list(sp.get("processed_videos", [])):
        if _video_belongs_to(v, username, platform):
            existing_ids = {e.get("bvid") for e in tp.get("processed_videos", [])}
            if v.get("bvid") not in existing_ids:
                tp.setdefault("processed_videos", []).append(v)
                migrated_videos += 1

    sp["processed_videos"] = [v for v in sp.get("processed_videos", [])
                              if not _video_belongs_to(v, username, platform)]

    # 如果旧 owner 没有剩余平台了 → 完全合并
    if not sp.get("platforms"):
        # 把 sp 的全部知识合并到 tp
        for k in ["known_mistakes", "known_patterns", "common_topics", "background",
                   "trading_style", "domain", "aliases"]:
            _merge_field(sp, tp, k)
        # 合并剩余视频
        existing_ids = {e.get("bvid") for e in tp.get("processed_videos", [])}
        for v in sp.get("processed_videos", []):
            if v.get("bvid") not in existing_ids:
                tp["processed_videos"].append(v)
        del db[from_owner]
        print(f"  [身份] {from_owner} 已无剩余平台，完全合并到 {to_real_name}")

    _rebuild_aliases(tp)
    if from_owner in db:
        _rebuild_aliases(sp)

    tp["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    if not tp.get("real_name"):
        tp["real_name"] = to_real_name
    _save(db)
    print(f"  [身份] ✅ 迁移完成: {from_owner}.{platform} → {to_real_name} ({migrated_videos}条视频)")


def _merge_field(src: Dict, dst: Dict, key: str):
    """合并单个字段（dict合并，list去重追加，str非空覆盖）"""
    if key not in src:
        return
    sv = src[key]
    if isinstance(sv, dict):
        for k, v in sv.items():
            dst.setdefault(key, {})[k] = v
    elif isinstance(sv, list):
        exist = set(dst.get(key, []))
        for item in sv:
            if item not in exist:
                dst.setdefault(key, []).append(item)
                exist.add(item)
    elif isinstance(sv, str) and sv:
        if not dst.get(key):
            dst[key] = sv


def _video_belongs_to(video: Dict, username: str, platform: str) -> bool:
    """判断一条视频记录是否属于某个平台的某个用户名"""
    vp = video.get("platform", "")
    vu = video.get("uploader", "")
    return (vp and vp == platform) or (vu and vu == username)


def resolve_identity(username: str) -> Dict:
    """给定任意平台的用户名，返回该人的完整资料（含真实姓名）

    返回: {"real_name": "张扬", "profile": {...}, "platform_names": {"bilibili": "张聚贤", ...}}
    如果未找到 → 返回空 profile
    """
    main_key = _normalize_speaker(username)
    if main_key == username and username not in _load():
        return {"real_name": "", "profile": {}, "platform_names": {}}

    db = _load()
    profile = db.get(main_key, {})
    return {
        "real_name": profile.get("real_name", main_key),
        "profile": profile,
        "platform_names": profile.get("platforms", {}),
    }


# ═══════════════════════════════════════════════════════════════
#  公共API
# ═══════════════════════════════════════════════════════════════

def get_speakers_by_domain(domain: str) -> List[str]:
    """按领域查找所有说话人"""
    if not domain:
        return []
    db = _load()
    return [name for name, p in db.items() if p.get("domain") == domain]


def list_all_speakers() -> List[Dict]:
    """列出所有说话人（含跨平台信息）"""
    db = _load()
    result = []
    for key, p in db.items():
        result.append({
            "key": key,
            "real_name": p.get("real_name", key),
            "platforms": p.get("platforms", {}),
            "domain": p.get("domain", ""),
            "video_count": len(p.get("processed_videos", [])),
        })
    return sorted(result, key=lambda x: x["video_count"], reverse=True)


def merge_speakers(target: str, source: str):
    """将 source 说话人的全部知识合并到 target（合并后删除 source）

    用于手动指定：胖杰克→张聚贤（两个不同用户名实际同一人）
    v2.0: 也会合并 platforms 字段
    """
    if target == source:
        return

    db = _load()
    if source not in db:
        print(f"  [合并] {source} 不存在，跳过")
        return
    if target not in db:
        print(f"  [合并] {target} 不存在，直接改名")
        db[target] = db.pop(source)
        _save(db)
        return

    sp = db[source]
    tp = db[target]

    # 合并 platforms
    if sp.get("platforms"):
        tp.setdefault("platforms", {})
        for plat, uname in sp["platforms"].items():
            if plat not in tp["platforms"]:
                tp["platforms"][plat] = uname

    # 合并 real_name
    if sp.get("real_name") and not tp.get("real_name"):
        tp["real_name"] = sp["real_name"]

    # 合并 aliases
    for a in sp.get("aliases", []):
        if a not in tp.get("aliases", []):
            tp.setdefault("aliases", []).append(a)
    if source not in tp.get("aliases", []):
        tp.setdefault("aliases", []).append(source)

    # 合并其他字段
    _merge_field(sp, tp, "known_mistakes")
    _merge_field(sp, tp, "known_patterns")
    _merge_field(sp, tp, "common_topics")

    for f in ["background", "domain", "trading_style"]:
        if sp.get(f) and not tp.get(f):
            tp[f] = sp[f]

    # 合并视频记录
    existing_bvids = {v.get("bvid") for v in tp.get("processed_videos", [])}
    for v in sp.get("processed_videos", []):
        if v.get("bvid") not in existing_bvids:
            tp.setdefault("processed_videos", []).append(v)

    tp["processed_videos"] = sorted(tp["processed_videos"],
                                     key=lambda x: x.get("date", ""), reverse=True)[:20]
    tp["common_topics"] = tp["common_topics"][:30]
    _rebuild_aliases(tp)
    tp["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")

    del db[source]
    _save(db)
    print(f"  [合并] {source} → {target} 完成")
    print(f"  → 总视频: {len(tp['processed_videos'])} 条")
    print(f"  → 总话题: {len(tp['common_topics'])} 个")
    print(f"  → 总误认: {len(tp.get('known_mistakes', {}))} 条")
    print(f"  → 平台矩阵: {tp.get('platforms', {})}")


def get_profile(speaker: str) -> Dict:
    """获取说话人知识档案"""
    main_name = _normalize_speaker(speaker)
    db = _load()
    return db.get(main_name, {})


def format_context(speaker: str, video_title: str = "", domain: str = "") -> str:
    """生成供LLM注入的说话人上下文（含跨平台信息+wiki同领域知识）"""
    if not speaker:
        return ""

    profile = get_profile(speaker)
    if not profile:
        return ""

    real_name = profile.get("real_name", "")
    platforms = profile.get("platforms", {})

    # 标题：优先用真实姓名
    if real_name:
        lines = [f"## {real_name} 的知识档案"]
    else:
        lines = [f"## {speaker} 的知识档案"]

    # 跨平台矩阵
    if platforms:
        plat_list = [f"{p}:{u}" for p, u in platforms.items()]
        lines.append(f"平台矩阵：{' | '.join(plat_list)}")

    if profile.get("background"):
        lines.append(f"身份：{profile['background']}")

    if profile.get("domain"):
        lines.append(f"领域：{profile['domain']}")

    if profile.get("trading_style"):
        lines.append(f"交易风格：{profile['trading_style']}")

    if profile.get("common_topics"):
        lines.append(f"常讲内容：{'、'.join(profile['common_topics'][:8])}")

    if profile.get("known_patterns"):
        lines.append("已确认的交易规律/核心观点：")
        for p in profile["known_patterns"][:5]:
            lines.append(f"  • {p}")

    # 同主题历史视频（最近3条，排除当前）
    prev = [v for v in profile.get("processed_videos", [])
            if video_title not in v.get("title", "")]
    if prev:
        lines.append("历史视频参考：")
        for v in prev[-3:]:
            platform_tag = f"[{v.get('platform', '')}]" if v.get('platform') else ""
            lines.append(f"  - {platform_tag}《{v['title']}》→ {v.get('key_insight', '')[:40]}")

    if profile.get("known_mistakes"):
        lines.append("whisper转录常见误认（已积累修正）：")
        for wrong, right in list(profile["known_mistakes"].items())[:8]:
            lines.append(f"  - {wrong} → {right}")

    # wiki同领域关联知识
    try:
        from .wiki_bridge import wiki_query
        wiki_ctx = wiki_query(topic=video_title, uploader=speaker, domain=domain, top_n=2)
        if wiki_ctx:
            lines.append("")
            lines.append("Wiki同领域关联知识：")
            lines.append(wiki_ctx)
    except Exception:
        pass

    return "\n".join(lines)


def update_after_video(
    speaker: str,
    video_title: str,
    bvid: str,
    video_duration: int,
    analysis: Dict,
    corrected_text: str,
    corrections: Optional[List[Dict]] = None,
    platform: str = "",
):
    """处理完一条视频后更新知识库（含自动特征学习 + 跨平台解析）

    v2.0 新增:
      - platform: 视频来源平台（"bilibili" / "youtube" / "xiaohongshu" / "douyin"）
      - 自动识别跨平台身份，知识集中到真实身份下
    """
    if not speaker:
        return

    db = _load()
    main_name = _normalize_speaker(speaker)
    if main_name not in db:
        db[main_name] = copy.deepcopy(_DEFAULT_PROFILE_TEMPLATE)

    profile = db[main_name]

    # ── v2.0: 自动注册平台映射 ──
    if platform:
        profile.setdefault("platforms", {})
        existing_username = profile["platforms"].get(platform)
        if not existing_username:
            profile["platforms"][platform] = speaker
            print(f"  [平台] ✅ 自动注册: {speaker} → {platform}")
        elif existing_username != speaker:
            # 同一平台出现新用户名 — 可能是改名
            print(f"  [平台] ⚠️ {platform}平台: {existing_username} → {speaker}（可能是改名）")
            profile["platforms"][platform] = speaker
        _rebuild_aliases(profile)

    # 别名（向后兼容）
    if speaker not in profile["aliases"] and speaker != main_name:
        profile["aliases"].append(speaker)

    # 提取本次视频的核心洞察
    summary = analysis.get("summary", "")
    keywords = analysis.get("keywords", [])
    chapters = analysis.get("chapters", [])
    topics = analysis.get("topics", [])

    # 记录视频
    video_entry = {
        "bvid": bvid,
        "date": time.strftime("%Y-%m-%d"),
        "title": video_title,
        "duration": video_duration,
        "key_insight": summary[:80],
        "topics": topics[:3],
    }
    if platform:
        video_entry["platform"] = platform
        video_entry["uploader"] = speaker

    # 排重
    profile["processed_videos"] = [
        v for v in profile["processed_videos"]
        if v.get("bvid") != bvid
    ]
    profile["processed_videos"].append(video_entry)

    # 更新话题（去重合并）
    for t in topics + keywords:
        if t and t not in profile["common_topics"]:
            profile["common_topics"].append(t)

    # 设置/更新领域标签
    if not profile.get("domain"):
        profile["domain"] = _guess_domain(video_title, keywords + topics, speaker)

    # 自动推断背景（首条视频）
    if not profile["background"]:
        if keywords and "交易" in " ".join(keywords[:3]):
            profile["background"] = "交易领域内容创作者"

    profile["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")

    # 保留上限
    profile["processed_videos"] = profile["processed_videos"][-20:]
    profile["common_topics"] = profile["common_topics"][-30:]

    _save(db)

    # ── 自动特征学习 ──
    if corrections:
        _learn_mistakes_from_corrections(speaker, corrections)
    if analysis:
        _learn_patterns_from_analysis(speaker, analysis)

    # ── v2.1: 自动提取声学特征 ──
    if video_duration > 0:
        full_text = corrected_text if corrected_text else ""
        chinese_chars = sum(1 for c in full_text if '\u4e00' <= c <= '\u9fff')
        if chinese_chars > 50:
            speech_rate = chinese_chars / max(video_duration, 1)
            clarity = _estimate_clarity_from_text(full_text)
            update_acoustic(speaker, speech_rate=speech_rate, clarity_score=clarity)


def add_mistake(speaker: str, wrong: str, right: str):
    """添加一条已知whisper误认"""
    if not speaker or not wrong:
        return
    db = _load()
    main_name = _normalize_speaker(speaker)
    if main_name not in db:
        db[main_name] = copy.deepcopy(_DEFAULT_PROFILE_TEMPLATE)

    if "known_mistakes" not in db[main_name]:
        db[main_name]["known_mistakes"] = {}
    db[main_name]["known_mistakes"][wrong] = right
    _save(db)


def add_pattern(speaker: str, pattern: str):
    """添加一条交易规律"""
    if not speaker or not pattern:
        return
    db = _load()
    main_name = _normalize_speaker(speaker)
    if main_name not in db:
        db[main_name] = copy.deepcopy(_DEFAULT_PROFILE_TEMPLATE)

    if pattern not in db[main_name].get("known_patterns", []):
        db[main_name].setdefault("known_patterns", []).append(pattern)
    _save(db)


def set_background(speaker: str, bg: str):
    """手动设置说话人背景"""
    if not speaker or not bg:
        return
    db = _load()
    main_name = _normalize_speaker(speaker)
    if main_name not in db:
        db[main_name] = copy.deepcopy(_DEFAULT_PROFILE_TEMPLATE)
    db[main_name]["background"] = bg
    _save(db)


def set_trading_style(speaker: str, style: str):
    """手动设置交易风格"""
    if not speaker or not style:
        return
    db = _load()
    main_name = _normalize_speaker(speaker)
    if main_name not in db:
        db[main_name] = copy.deepcopy(_DEFAULT_PROFILE_TEMPLATE)
    db[main_name]["trading_style"] = style
    _save(db)


def set_real_name(speaker: str, real_name: str):
    """手动设置真实姓名"""
    if not speaker or not real_name:
        return
    db = _load()
    main_name = _normalize_speaker(speaker)
    if main_name not in db:
        db[main_name] = copy.deepcopy(_DEFAULT_PROFILE_TEMPLATE)
    db[main_name]["real_name"] = real_name
    _rebuild_aliases(db[main_name])
    _save(db)


def add_alias(speaker: str, alias: str):
    """添加别名（向后兼容，v2.0更推荐使用 link_identity）"""
    if not speaker or not alias:
        return
    db = _load()
    main_name = _normalize_speaker(speaker)
    if main_name not in db:
        db[main_name] = copy.deepcopy(_DEFAULT_PROFILE_TEMPLATE)
    if alias not in db[main_name].get("aliases", []):
        db[main_name].setdefault("aliases", []).append(alias)
    _save(db)


# ================================================================
# 移植自 ZIP v1.10.0: 高级错误分类+根本原因分析+自动调优
# ================================================================

ERROR_TYPE_MAP = {
    "E_VOICE_PRONOUNCE": "发音近似",       # 语音层：同音/近音
    "E_VOICE_SHRINK": "发音缩略",          # 语音层：吞音/缩略
    "E_VOICE_DIALECT": "方言影响",          # 语音层：方言口音
    "E_VOICE_HOMOPHONE": "同音误读",        # 语音层：完全同音但字不同
    "E_SEMANTIC_TERM": "术语混用",          # 语义层：领域术语误认
    "E_SEMANTIC_CONTEXT": "上下文歧义",      # 语义层：多义词选错
    "E_FORMAT_NUMBER": "数字单位错位",       # 格式层：数字/单位
    "E_FORMAT_STRUCT": "结构错误",           # 格式层：断句/分段
}


def auto_classify_mistake(wrong: str, right: str, hint_type: str = "") -> str:
    """自动归类错误到 Error Type ID（正则/关键词，不依赖LLM）

    输入：wrong="只是", right="知识"
    输出："E_VOICE_HOMOPHONE"
    """
    # 1. 完全同音（拼音相同）
    if _same_pinyin(wrong, right):
        return "E_VOICE_HOMOPHONE"

    # 2. 缩略/吞音（长度差>50%）
    if len(wrong) < len(right) * 0.5:
        return "E_VOICE_SHRINK"
    if len(right) < len(wrong) * 0.5:
        return "E_VOICE_SHRINK"

    # 3. 数字/单位涉及
    if re.search(r'\d|万|亿|千|百|%|点', wrong) or re.search(r'\d|万|亿|千|百|%|点', right):
        return "E_FORMAT_NUMBER"

    # 4. 领域术语判断
    trading_terms = ['损', '盈', '仓', '线', '均', '量', '价', '盘', '趋势', '突破', '回调']
    tech_terms = ['代码', '函数', '接口', '算法', '模块', '配置']
    if any(t in wrong or t in right for t in trading_terms):
        return "E_SEMANTIC_TERM"
    if any(t in wrong or t in right for t in tech_terms):
        return "E_SEMANTIC_TERM"

    # 5. 方言特征（特定音节模式）
    dialect_patterns = [
        (r'[zc]hi\b', r'[zc]i\b'),   # zh/z 混淆
        (r'[sh]eng\b', r'[sh]en\b'),  # 前后鼻音
        (r'\bn[^g]', r'\bl[^g]'),     # n/l 混淆
    ]
    for p1, p2 in dialect_patterns:
        if re.search(p1, wrong) or re.search(p1, right):
            return "E_VOICE_DIALECT"

    # 6. 默认：发音近似
    return "E_VOICE_PRONOUNCE"



def find_similar_mistakes(wrong: str, speaker: str = "", domain: str = "") -> List[Dict]:
    """查找同类错误模式（跨UP主、同领域）

    输入一个错误的词，在所有说话人/同领域中查找相似的错误模式。
    用于 Feedback Loop：碰到新错误时先查"有没有人犯过同类错"。
    """
    results = []
    db = _load()

    for name, profile in db.items():
        if speaker and name != speaker and speaker != "*":
            continue
        if domain and profile.get("domain") != domain:
            continue

        mist = profile.get("mistake_patterns", {})
        if isinstance(mist, dict):
            for type_id, entries in mist.items():
                if isinstance(entries, list):
                    for entry in entries:
                        entry_wrong = entry.get("wrong") if isinstance(entry, dict) else (
                            entry.split("→")[0] if isinstance(entry, str) else ""
                        )
                        # 相似度检查：同音/同模式
                        if entry_wrong and wrong and _phonetic_similarity(wrong, entry_wrong) > 0.7:
                            results.append({
                                "speaker": name,
                                "type_id": type_id,
                                "entry": entry,
                            })

    return results



def _same_pinyin(w1: str, w2: str) -> bool:
    """粗略判断两段文字是否同音（基于拼音模糊匹配）"""
    try:
        import pypinyin
        py1 = pypinyin.lazy_pinyin(w1, style=pypinyin.Style.NORMAL)
        py2 = pypinyin.lazy_pinyin(w2, style=pypinyin.Style.NORMAL)
        return py1 == py2
    except ImportError:
        # 无 pypinyin 时回退：按单字占比判断
        common = set(w1) & set(w2)
        return len(common) / max(len(set(w1 + w2)), 1) > 0.4



def _phonetic_similarity(w1: str, w2: str) -> float:
    """计算两个词的语音相似度（0-1）"""
    try:
        import pypinyin
        py1 = pypinyin.lazy_pinyin(w1, style=pypinyin.Style.NORMAL)
        py2 = pypinyin.lazy_pinyin(w2, style=pypinyin.Style.NORMAL)
        common = sum(1 for a, b in zip(py1, py2) if a == b)
        return common / max(len(py1), len(py2), 1)
    except ImportError:
        # 简单 Jaccard
        common = len(set(w1) & set(w2))
        return common / max(len(set(w1 + w2)), 1)



def _root_cause_label(type_id: str) -> str:
    """Error Type ID → 中文根因标签"""
    labels = {
        "E_VOICE_PRONOUNCE": "语音层_发音近似",
        "E_VOICE_SHRINK": "语音层_发音缩略",
        "E_VOICE_DIALECT": "语音层_方言影响",
        "E_VOICE_HOMOPHONE": "语音层_同音误读",
        "E_SEMANTIC_TERM": "语义层_术语混用",
        "E_SEMANTIC_CONTEXT": "语义层_上下文歧义",
        "E_FORMAT_NUMBER": "格式层_数字单位错位",
        "E_FORMAT_STRUCT": "格式层_结构错误",
    }
    return labels.get(type_id, "未知")


# ══════════════════════════════════════════════════════════════════════
# v1.16.0: 根因分析描述 — 将错误统计转为 LLM 可理解的语音/语义特征描述
# ══════════════════════════════════════════════════════════════════════


ROOT_CAUSE_DESCRIPTIONS = {
    "E_VOICE_PRONOUNCE": (
        "发音近似导致误认：该UP主某些音节的发音与标准发音有细微偏差（如声母混淆 n/l、zh/z，"
        "或韵母偏移 an/ang、en/eng），ASR容易把这些音映射到发音近似的日常词而非正确术语。"
        "在修正时请注意检查——如果转录出的词在上下文中语义不通、且读音与某个专业术语接近，"
        "大概率是发音偏差导致的误认。"
    ),
    "E_VOICE_SHRINK": (
        "发音缩略/吞音：该UP主语速较快或在连续讲话中省略了部分音节（如'不知道'→'不造'），"
        "ASR可能把缩略读音识别为完全不同的词。修正时需要根据上下文还原被吞掉的音节。"
    ),
    "E_VOICE_DIALECT": (
        "方言/口音影响：该UP主带有方言特征（如台湾腔、粤语腔、东北腔等），某些音节的发音"
        "与普通话标准发音不同。ASR在识别这些偏离标准的音节时容易出错。修正时请注意该口音特征"
        "会导致特定类别的音素误读。"
    ),
    "E_VOICE_HOMOPHONE": (
        "同音/近音字混淆：中文同音字极多，ASR在缺乏足够上下文时无法区分同音字。"
        "典型表现如'熊市→雄士'、'乖离→怪力'、'止损→只损'——发音完全正确但字选错了。"
        "这是ASR的通用弱点而非UP主特有，但在专业术语密集的语境中尤为突出。"
        "修正时优先检查：转录出的词在交易语境中是否合理？是否有同音的专业术语更合适？"
    ),
    "E_SEMANTIC_TERM": (
        "领域术语被误认为日常词：交易领域的专有名词（如'止损''盈亏比''孕线''乖离'）"
        "在whisper的通用词汇表中频率极低，模型倾向选择频率更高的日常词汇。"
        "这不是发音问题，而是语言模型的领域偏差——它在金融交易语料上的训练不足。"
        "修正时请注意：如果上下文明显是交易分析，但出现了看起来像普通词汇的表达，"
        "检查是否是领域术语被误认。"
    ),
    "E_SEMANTIC_CONTEXT": (
        "上下文歧义：某些词在交易语境中有特殊含义（如'多头''空头''持仓''回档'），"
        "但ASR按通用义项理解，导致选错词或歧义消解失败。修正时需要根据上下文判断正确含义。"
    ),
    "E_FORMAT_NUMBER": (
        "数字/单位错位：交易中频繁出现的数字、比率、价格等（如'3R''50%''120均线'），"
        "ASR容易把数字听成近音汉字（如'3R→三尔'、'50%→50啪'）。"
        "修正时特别注意转录中出现的不自然数字或单位表达，还原为正确的数值格式。"
    ),
    "E_FORMAT_STRUCT": (
        "结构错误：长句或复杂逻辑表达时，ASR可能在断句、标点、语序上出错。"
        "表现如两个分句被合并、标点位置错误导致语义改变。这是语音转写中的常见结构性问题。"
    ),
}



def _summarize_mistake_types_by_root_cause(mistake_patterns: dict) -> str:
    """将mistake_patterns的根因类型汇总为LLM友好的根因描述文本
    
    不是列出词对词映射，而是告诉LLM：
    - 这个UP主有哪些类型的ASR错误
    - 每种类型的根因是什么
    - 修正时应该注意什么
    
    Returns: 根因描述文本，或空字符串
    """
    if not mistake_patterns or not isinstance(mistake_patterns, dict):
        return ""
    
    # 统计每种类型的高频词条数
    active_types = set()
    for type_id, entries in mistake_patterns.items():
        if entries:
            active_types.add(type_id)
    
    if not active_types:
        return ""
    
    lines = ["## 该UP主的ASR错误类型（根因分析 → 指导LLM修正）", ""]
    
    for type_id in sorted(active_types):
        label = _root_cause_label(type_id)
        desc = ROOT_CAUSE_DESCRIPTIONS.get(type_id, "")
        entries = mistake_patterns[type_id]
        
        # 统计数据
        total_hits = sum(
            e.get("hit_count", 1) if isinstance(e, dict) else 1
            for e in entries
        )
        count = len(entries)
        
        # 提取典型样例（高命中的前3个）
        examples = []
        if isinstance(entries[0], dict):
            sorted_entries = sorted(
                entries, key=lambda x: x.get("hit_count", 0), reverse=True
            )
            for e in sorted_entries[:3]:
                w = e.get("wrong", "")
                r = e.get("right", "")
                if w and r:
                    examples.append(f"「{w}」→「{r}」")
        else:
            # 旧格式兼容
            for e in entries[:3]:
                if isinstance(e, str):
                    examples.append(e)
        
        lines.append(f"### {label}")
        lines.append(f"发生次数：{count}种模式，累计{total_hits}次命中")
        lines.append(f"根因：{desc}")
        if examples:
            lines.append(f"典型样例：{'、'.join(examples)}")
        lines.append("")
    
    return "\n".join(lines)



def _summarize_domain_patterns(domain_patterns: dict) -> str:
    """将领域错题集汇总为LLM友好的领域级根因描述
    
    不列词对词清单，而是分析领域共性问题的根因模式。
    """
    if not domain_patterns:
        return ""
    
    # 按类别汇总
    sem = domain_patterns.get("E_SEMANTIC_TERM", [])
    fmt = domain_patterns.get("E_FORMAT_NUMBER", [])
    all_patterns = sem + fmt
    if not all_patterns:
        return ""
    
    lines = ["## 交易领域ASR共性根因（跨UP主共享，指导LLM修正）", ""]
    
    if sem:
        high_terms = [p for p in sem if p.get("severity") == "high"]
        total_hits = sum(p.get("hit_count", 0) for p in sem)
        # 取 top 高频术语名称
        top_terms = sorted(sem, key=lambda x: x.get("hit_count", 0), reverse=True)
        top_names = [p["target_word"] for p in top_terms[:8]]
        
        lines.append(
            f"交易领域术语被ASR系统性误认。{len(sem)}个核心术语（累计{total_hits}次误认），"
            f"高频受害者：{'、'.join(top_names)}。"
        )
        lines.append("")
        lines.append(ROOT_CAUSE_DESCRIPTIONS["E_SEMANTIC_TERM"])
        lines.append("")
    
    if fmt:
        total_fmt = sum(p.get("hit_count", 0) for p in fmt)
        lines.append(
            f"数字/比率/单位表达在交易语境中极其频繁（{len(fmt)}种模式被误认，"
            f"累计{total_fmt}次），ASR常把数字听成近音汉字。"
        )
        lines.append(ROOT_CAUSE_DESCRIPTIONS["E_FORMAT_NUMBER"])
        lines.append("")
    
    return "\n".join(lines)



def _infer_trigger(wrong: str, right: str, type_id: str) -> str:
    """根据错误类型推断触发条件"""
    if type_id.startswith("E_VOICE"):
        return f"发音相似: '{wrong}' ≈ '{right}'"
    if type_id.startswith("E_SEMANTIC"):
        return f"领域混淆: '{wrong}' → '{right}'"
    if type_id.startswith("E_FORMAT"):
        return f"格式误判: '{wrong}' → '{right}'"
    return ""



def add_known_person(speaker: str, person: str):
    """确认某个提到的人物属于该UP主的体系
    
    例如：UP主"某交易员"的视频提到"吴江"，
    你确认后调用 add_known_person("某交易员", "吴江")
    这条视频入库时会被标记为关联吴江体系。
    """
    if not speaker or not person:
        return
    db = _load()
    main_name = _normalize_speaker(speaker)
    if main_name not in db:
        db[main_name] = dict(_DEFAULT_PROFILE_TEMPLATE)
    if person not in db[main_name].get("known_persons", []):
        db[main_name].setdefault("known_persons", []).append(person)
    if not db[main_name].get("main_person"):
        db[main_name]["main_person"] = person
    _save(db)
    print(f"  ✅ 已标记「{person}」→ {main_name} 体系")
    print(f"     该UP主提及「{person}」的视频会关联到 {person} 知识体系")



def set_main_person(speaker: str, person: str):
    """设置该UP主代言的核心人物
    
    例如：某个UP主专门传播吴江方法论，就设
    set_main_person("UP主名", "吴江")
    """
    if not speaker or not person:
        return
    db = _load()
    main_name = _normalize_speaker(speaker)
    if main_name not in db:
        db[main_name] = dict(_DEFAULT_PROFILE_TEMPLATE)
    db[main_name]["main_person"] = person
    if person not in db[main_name].get("known_persons", []):
        db[main_name].setdefault("known_persons", []).append(person)
    _save(db)


# ── v1.11.0: 知识提取与反哺 ──


def _update_core_knowledge(profile: Dict, analysis: Dict, corrected_text: str):
    """从LLM分析结果中提取三大维度内容，追加到 core_knowledge（自动去重）"""
    core = profile.setdefault("core_knowledge", {
        "底层认知": [],
        "自用方法论": [],
        "独家观点": [],
    })
    
    summary = analysis.get("summary", "")
    essence = analysis.get("essence", "")
    usages = analysis.get("usages", [])
    chapters = analysis.get("chapters", [])
    keywords = analysis.get("keywords", [])
    
    # ── 底层认知 ──
    if essence and len(essence) > 10:
        cognitive = essence[:200].strip()
    elif summary and len(summary) > 20:
        # 兜底：summary 前两句作为底层认知
        sentences = summary.split("。")
        cognitive = "。".join(sentences[:2])[:200].strip() + ("。" if len(sentences) >= 2 else "")
    else:
        cognitive = ""
    if cognitive and cognitive not in core["底层认知"]:
        core["底层认知"].append(cognitive)
        core["底层认知"] = core["底层认知"][-10:]
    
    # ── 自用方法论 ──
    if usages:
        for u in usages:
            if isinstance(u, str) and len(u) > 5 and u not in core["自用方法论"]:
                core["自用方法论"].append(u)
        core["自用方法论"] = core["自用方法论"][-15:]
    elif chapters:
        # 兜底：章节标题作为方法论条目
        for ch in chapters:
            title = ch.get("title", "") if isinstance(ch, dict) else str(ch)
            if len(title) > 3 and title not in core["自用方法论"]:
                core["自用方法论"].append(title)
        core["自用方法论"] = core["自用方法论"][-15:]
    
    # ── 独家观点 ──
    if summary and len(summary) > 20:
        sentences = summary.split("。")
        # 取前两句中较短的、判断性的一句
        candidates = [s.strip() + "。" for s in sentences[:3] if len(s) > 10]
        for cand in candidates:
            if cand not in core["独家观点"]:
                core["独家观点"].append(cand)
        core["独家观点"] = core["独家观点"][-10:]



def _update_skill_feedback(profile: Dict, analysis: Dict, corrected_text: str, speaker: str = ""):
    """收集 hotwords、error_mappings，自动归类错误类型写入 mistake_patterns，用于反哺 Whisper 和规则引擎 + LLM enhance 上下文"""
    fb = profile.setdefault("skill_feedback", {
        "hotwords": [],
        "error_mappings": {},
    })
    
    keywords = analysis.get("keywords", [])
    topics = analysis.get("topics", [])
    all_terms = keywords + topics
    
    # 提取≥3字的专业术语作为 hotwords
    from collections import Counter
    import re
    # 从 corrected_text 中提取高频中文词
    terms = re.findall(r'[\u4e00-\u9fff]{3,8}', corrected_text[:3000])
    term_counts = Counter(terms)
    # 筛选在关键词/话题中出现过的术语
    known_terms = set()
    for t in all_terms:
        if isinstance(t, str) and len(t) >= 2:
            known_terms.add(t)
    
    # 高频词 + 关键词交集 → hotwords
    hotwords = set(fb.get("hotwords", []))
    for word, count in term_counts.most_common(30):
        if count >= 3 and len(word) >= 2:
            # 只保留有意义的词（非停用词）
            if word not in ("我们可以", "一个非常", "实际上", "比如说", "以至于", 
                          "是不是", "之后呢", "那么呢", "所以呢"):
                hotwords.add(word)
    # 合并已知关键词
    for k in known_terms:
        if len(k) >= 2:
            hotwords.add(k)
    fb["hotwords"] = sorted(hotwords)[:30]  # 最多30个热词
    
    # error_mappings 从 analysis 的 corrections 字段获取
    corrections = analysis.get("corrections", {})
    if isinstance(corrections, dict):
        fb["error_mappings"].update(corrections)
        # 限制大小
        if len(fb["error_mappings"]) > 100:
            fb["error_mappings"] = dict(list(fb["error_mappings"].items())[-100:])

    # ── v1.13.0: 统一入口 → feedback_gateway 分发到 speaker + domain + dict ──
    if isinstance(corrections, dict) and corrections:
        feedback_gateway(corrections, speaker=speaker)


# ═══════════════════════════════════════════════════════════════
# v1.13.0: 统一错误反馈入口 — 所有校正层(L1-L5) + LLM enhance
# 都从这里进入，一条入口 → 三条出口
# ═══════════════════════════════════════════════════════════════


def feedback_gateway(corrections: Dict[str, str], speaker: str = "", bvid: str = ""):
    """
    统一错误反馈入管 — 不管校正来自 L1 规则引擎 / L2-L5 多层校正器 / LLM enhance，
    都从这里进入，自动分发到三条出口：
    
    1. speaker 错题集 (mistake_patterns) — UP主特有的发音/语音错误
    2. 领域错题集 (domain_errors.json) — 跨UP主共享的术语误认
    3. 旧 correction_dict (兼容) — 保留 stats + patterns 历史

    Args:
        corrections: {"错误词": "正确词", ...}
        speaker: UP主名（用于 speaker 级写入）
        bvid: 视频ID（可选，记录来源）
    """
    import json, os, fcntl
    if not corrections or not isinstance(corrections, dict):
        return
    
    main_name = _normalize_speaker(speaker) if speaker else ""

    # ── 出口1: speaker 错题集 ──
    speaker_written = 0
    if main_name:
        db = _load()
        if main_name not in db:
            db[main_name] = dict(_DEFAULT_PROFILE_TEMPLATE)
        profile = db[main_name]
        mist = profile.setdefault("mistake_patterns", {})
        if not isinstance(mist, dict):
            mist = {}
            profile["mistake_patterns"] = mist
        
        for wrong, right in corrections.items():
            if not isinstance(wrong, str) or not isinstance(right, str):
                continue
            if len(wrong) < 1 or len(right) < 1:
                continue
            type_id = auto_classify_mistake(wrong, right)
            root_cause = _root_cause_label(type_id)
            if type_id not in mist:
                mist[type_id] = []
            existing = next((e for e in mist[type_id] if isinstance(e, dict) and e.get("wrong") == wrong), None)
            if existing:
                existing["hit_count"] = existing.get("hit_count", 1) + 1
                if existing["hit_count"] >= 3:
                    existing["severity"] = "high"
            else:
                mist[type_id].append({
                    "wrong": wrong, "right": right,
                    "root_cause": root_cause, "severity": "medium",
                    "hit_count": 1,
                    "trigger_condition": _infer_trigger(wrong, right, type_id),
                    "generalization_rule": "",
                })
            speaker_written += 1
        _save(db)

    # ── 出口2: 领域错题集（只存语义层+格式层）──
    domain_written = 0
    semantic_format = {
        k: v for k, v in corrections.items()
        if auto_classify_mistake(k, v).startswith(("E_SEMANTIC", "E_FORMAT"))
    }
    if semantic_format:
        STORE_PATH = os.path.expanduser("~/.biliyoutik2brain_domain_errors.json")
        try:
            with open(STORE_PATH, 'r', encoding='utf-8') as f:
                store = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            store = {}
        
        for wrong, right in semantic_format.items():
            tid = auto_classify_mistake(wrong, right)
            if tid not in store:
                store[tid] = []
            existing = next((e for e in store[tid] if isinstance(e, dict) and e.get("wrong") == wrong), None)
            if existing:
                existing["hit_count"] = existing.get("hit_count", 1) + 1
                if existing["hit_count"] >= 3:
                    existing["severity"] = "high"
                if existing["right"] != right and right not in existing.get("alt_rights", []):
                    existing["alt_rights"].append(right)
            else:
                store[tid].append({
                    "wrong": wrong, "right": right,
                    "root_cause": _root_cause_label(tid),
                    "severity": "low", "hit_count": 1,
                    "trigger_condition": _infer_trigger(wrong, right, tid),
                    "alt_rights": [], "source": bvid if bvid else "auto",
                })
            domain_written += 1
        
        with open(STORE_PATH + ".tmp", 'w', encoding='utf-8') as f:
            json.dump(store, f, ensure_ascii=False, indent=2)
        os.replace(STORE_PATH + ".tmp", STORE_PATH)
        try:
            _rebuild_domain_patterns()
        except Exception:
            pass

    # ── 出口3: 旧 correction_dict (兼容 stats) ──
    from .corrector_dictionary import DOMAIN_CORRECTIONS
    dict_written = 0
    for wrong, right in corrections.items():
        if isinstance(wrong, str) and isinstance(right, str) and len(wrong) >= 1 and len(right) >= 1:
            DOMAIN_CORRECTIONS.setdefault(wrong, right)
            dict_written += 1

    # v1.14.0: 闭环回灌 — 累计足够新错题后自动触发
    _auto_backflush_check()

    return {
        "speaker": speaker_written,
        "domain": domain_written,
        "dict": dict_written,
    }


# ── 回灌触发计数 ──
_backflush_counter = 0

_BACKFLUSH_TRIGGER_EVERY = 10  # 每积累10条新domain错误触发一次回灌


def _auto_backflush_check():
    """自动检查是否需要触发闭环回灌"""
    global _backflush_counter
    _backflush_counter += 1
    if _backflush_counter >= _BACKFLUSH_TRIGGER_EVERY:
        _backflush_counter = 0
        try:
            backflush_to_correction_engine(min_hit_count=2)
        except Exception:
            pass



def _domain_error_feedback(corrections: Dict[str, str]) -> None:
    """
    将语义层/格式层错误写入领域错题集（~/.biliyoutik2brain_domain_errors.json）
    跨UP主共享，用于 format_context 中注入 LLM enhance prompt
    """
    import json, os, fcntl
    STORE_PATH = os.path.expanduser("~/.biliyoutik2brain_domain_errors.json")
    
    # 只写入语义层和格式层（E_SEMANTIC_*, E_FORMAT_*）
    # 发音层是 speaker 特有的，不写入领域集
    domain_entries = []
    for wrong, right in corrections.items():
        if not isinstance(wrong, str) or not isinstance(right, str):
            continue
        tid = auto_classify_mistake(wrong, right)
        if tid.startswith("E_SEMANTIC") or tid.startswith("E_FORMAT"):
            domain_entries.append((wrong, right, tid))
    
    if not domain_entries:
        return
    
    # 原子写入（加文件锁防并发冲突）
    try:
        with open(STORE_PATH, 'r', encoding='utf-8') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            store = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        store = {}
    
    for wrong, right, tid in domain_entries:
        if tid not in store:
            store[tid] = []
        
        existing = None
        for entry in store[tid]:
            if isinstance(entry, dict) and entry.get("wrong") == wrong:
                existing = entry
                break
        
        if existing:
            existing["hit_count"] = existing.get("hit_count", 1) + 1
            if existing["hit_count"] >= 3:
                existing["severity"] = "high"
            if existing["right"] != right and right not in existing.get("alt_rights", []):
                existing["alt_rights"].append(right)
        else:
            store[tid].append({
                "wrong": wrong,
                "right": right,
                "root_cause": _root_cause_label(tid),
                "severity": "low",
                "hit_count": 1,
                "trigger_condition": _infer_trigger(wrong, right, tid),
                "alt_rights": [],
                "source": "auto_feedback",
            })
    
    # 原子写入
    with open(STORE_PATH + ".tmp", 'w', encoding='utf-8') as f:
        json.dump(store, f, ensure_ascii=False, indent=2)
    os.replace(STORE_PATH + ".tmp", STORE_PATH)
    
    # 同时更新 pattern 缓存（异步不阻塞）
    try:
        _rebuild_domain_patterns()
    except Exception:
        pass  # pattern 重建失败不影响主流程



def _rebuild_domain_patterns() -> None:
    """从 domain_errors.json 重建 domain_patterns.json（类型→模式归并）"""
    import json, os
    STORE_PATH = os.path.expanduser("~/.biliyoutik2brain_domain_errors.json")
    PATTERN_PATH = os.path.expanduser("~/.biliyoutik2brain_domain_patterns.json")
    
    try:
        with open(STORE_PATH, 'r', encoding='utf-8') as f:
            store = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return
    
    patterns = {}
    for tid, entries in store.items():
        if tid == "E_SEMANTIC_TERM":
            # 按 right（正确词）分组
            groups = {}
            for e in entries:
                key = e["right"]
                groups.setdefault(key, []).append(e)
            
            plist = []
            for right_word, group in groups.items():
                wrongs = sorted(set(e["wrong"] for e in group))
                plist.append({
                    "pattern_name": f"ASR误认「{right_word}」",
                    "target_word": right_word,
                    "wrong_variants": wrongs,
                    "hit_count": sum(e.get("hit_count", 1) for e in group),
                    "severity": "high" if len(wrongs) >= 3 else "medium",
                    "trigger_rule": f"听到发音类似 {wrongs[0]}、{wrongs[1] if len(wrongs)>1 else wrongs[0]} 等 → 检查是否该是「{right_word}」",
                    "category": "语义层_术语混用",
                    "source_count": len(group),
                })
            patterns[tid] = sorted(plist, key=lambda x: -x["hit_count"])
        
        elif tid == "E_FORMAT_NUMBER":
            plist = []
            for e in entries:
                plist.append({
                    "pattern_name": f"数字/格式误认「{e['right']}」",
                    "target_word": e["right"],
                    "wrong_variants": [e["wrong"]],
                    "hit_count": e.get("hit_count", 1),
                    "severity": "low",
                    "trigger_rule": e.get("trigger_condition", ""),
                    "category": "格式层_数字单位错位",
                    "source_count": 1,
                })
            patterns[tid] = plist
    
    with open(PATTERN_PATH + ".tmp", 'w', encoding='utf-8') as f:
        json.dump(patterns, f, ensure_ascii=False, indent=2)
    os.replace(PATTERN_PATH + ".tmp", PATTERN_PATH)


# ═══════════════════════════════════════════════════════════════
# v1.14.0: 闭环回灌 — 高频错题模式 → 校正引擎规则优先级
# ═══════════════════════════════════════════════════════════════


def backflush_to_correction_engine(min_hit_count: int = 3) -> dict:
    """
    将高频错题模式回灌到校正引擎，实现闭环优化。
    
    实践→认识→再实践→再认识：
      - 转录实践产生了错题集（认识）
      - 将高频模式回灌到 DOMAIN_CORRECTIONS（再实践）
      - 下一次转录时校正引擎自动命中这些高频模式（更深的认识）
    
    回灌产物：
      1. ~/.biliyoutik2brain_backflush.json — 回灌记录（可审计可回滚）
      2. DOMAIN_CORRECTIONS 优先级加权 — 高频模式直接写入字典
      3. 输出回灌摘要报告
    
    Args:
        min_hit_count: 最小命中次数阈值（默认3次以上才回灌）
    
    Returns:
        {added: int, skipped: int, summary: [...]}
    """
    import json, os
    from .corrector_dictionary import DOMAIN_CORRECTIONS
    
    STORE_PATH = os.path.expanduser("~/.biliyoutik2brain_domain_errors.json")
    BACKFLUSH_PATH = os.path.expanduser("~/.biliyoutik2brain_backflush.json")
    
    result = {"added": 0, "skipped": 0, "summary": []}
    
    try:
        with open(STORE_PATH, 'r', encoding='utf-8') as f:
            store = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return result
    
    if not store:
        return result
    
    # 加载回灌历史
    try:
        with open(BACKFLUSH_PATH, 'r', encoding='utf-8') as f:
            backflush = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        backflush = {"history": [], "last_run": "", "total_added": 0}
    
    newly_added = {}
    
    for tid, entries in store.items():
        for entry in entries:
            wrong = entry.get("wrong", "").strip()
            right = entry.get("right", "").strip()
            hit_count = entry.get("hit_count", 1)
            severity = entry.get("severity", "low")
            
            if not wrong or not right:
                continue
            if len(wrong) < 1 or len(right) < 1:
                continue
            
            # 阈值过滤：只有高频错误才回灌
            if hit_count < min_hit_count and severity != "high":
                continue
            
            # 已存在则设标记
            if wrong in DOMAIN_CORRECTIONS:
                continue
            
            # 回灌到 DOMAIN_CORRECTIONS
            DOMAIN_CORRECTIONS[wrong] = right
            newly_added[wrong] = {"right": right, "hit_count": hit_count, "type": tid}
    
    result["added"] = len(newly_added)
    
    if newly_added:
        # 写入回灌记录
        record = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "added": newly_added,
            "trigger_threshold": min_hit_count,
        }
        backflush["history"].append(record)
        backflush["last_run"] = time.strftime("%Y-%m-%d %H:%M:%S")
        backflush["total_added"] += len(newly_added)
        
        with open(BACKFLUSH_PATH, 'w', encoding='utf-8') as f:
            json.dump(backflush, f, ensure_ascii=False, indent=2)
        
        # 摘要
        for wrong, info in sorted(newly_added.items(), key=lambda x: -x[1]["hit_count"]):
            result["summary"].append(f"{wrong}→{info['right']} (×{info['hit_count']}, {info['type']})")
        
        print(f"\n[闭环回灌] 高频错题模式 → DOMAIN_CORRECTIONS: {len(newly_added)}条")
        for s in result["summary"][:10]:
            print(f"  + {s}")
        if len(result["summary"]) > 10:
            print(f"  ... 还有 {len(result['summary']) - 10} 条")
    
    return result



def backflush_summary() -> dict:
    """查看回灌历史和统计"""
    import json, os
    BACKFLUSH_PATH = os.path.expanduser("~/.biliyoutik2brain_backflush.json")
    try:
        with open(BACKFLUSH_PATH, 'r', encoding='utf-8') as f:
            bf = json.load(f)
        return {
            "total_added": bf.get("total_added", 0),
            "last_run": bf.get("last_run", "never"),
            "history_count": len(bf.get("history", [])),
            "latest": bf["history"][-1] if bf.get("history") else None,
        }
    except (FileNotFoundError, json.JSONDecodeError):
        return {"total_added": 0, "last_run": "never", "history_count": 0, "latest": None}


# ═══════════════════════════════════════════════════════════════
# v1.15.0: 自动调参器 — 让技能自己调节关键参数
# ═══════════════════════════════════════════════════════════════


def auto_tune(speaker_name: str = None) -> dict:
    """
    基于错题集和转录质量统计数据，自动建议/执行参数调整。
    
    可调参数（skill内部不跨文件）：
    1. correction_priority — speaker级校正优先级
    2. word_boost_limit — ASR前置词上限
    3. model_suggestion — 转录模型升级/降级建议
    
    返回: {"adjustments": [...], "suggestions": [...]}
    """
    import json, os
    result = {"adjustments": [], "suggestions": []}
    
    db = _load()
    speakers = [speaker_name] if speaker_name else list(db.keys())
    
    for name in speakers:
        p = db.get(name)
        if not p or not p.get("processed_videos"):
            continue
        
        videos = p.get("processed_videos", [])
        
        # ── 统计0: 视频数量门槛 — 至少3个视频才有统计意义 ──
        if len(videos) < 3:
            continue
        
        # ── 统计1: 校正优先级（基于 error_mappings hit_count）──
        fb = p.get("skill_feedback", {})
        err_map = fb.get("error_mappings", {})
        # error_mappings 的 entries 里错误命中频率从 _update_skill_feedback 写入
        # 直接数error_mappings的条数：多→该speaker问题多→提高优先级
        err_count = len(err_map)
        current_prio = p.get("tuning_overrides", {}).get("correction_boost", 1.0)
        if err_count > 20 and current_prio < 1.5:
            p.setdefault("tuning_overrides", {})["correction_boost"] = 1.5
            result["adjustments"].append({
                "speaker": name,
                "type": "correction_boost",
                "old_value": 1.0,
                "new_value": 1.5,
                "reason": f"error_mappings超过{err_count}条，提高校正增强倍率",
            })
        
        # ── 统计2: word_boost_limit — 基于视频数量和文本质量估算 ──
        current_limit = p.get("tuning_overrides", {}).get("word_boost_limit", 15)
        # 估算：总视频数 > 5 且存在通用话题 → 扩大热词池
        topic_count = len(p.get("common_topics", []))
        if len(videos) >= 5 and topic_count >= 10 and current_limit < 25:
            new_limit = min(25, current_limit + 5)
            p.setdefault("tuning_overrides", {})["word_boost_limit"] = new_limit
            result["adjustments"].append({
                "speaker": name,
                "type": "word_boost_limit",
                "old_value": current_limit,
                "new_value": new_limit,
                "reason": f"{len(videos)}个视频+{topic_count}个话题，扩大ASR热词池",
            })
        
        # ── 统计3: 模型建议 — 基于领域分类和内容复杂度 ──
        current_model = p.get("tuning_overrides", {}).get("suggested_model", "tiny")
        domain = p.get("domain", "general")
        # trading 领域 + 多视频 → 建议 base
        if domain == "trading" and len(videos) >= 5 and current_model != "base":
            p.setdefault("tuning_overrides", {})["suggested_model"] = "base"
            result["suggestions"].append({
                "speaker": name,
                "type": "model_upgrade",
                "message": f"交易领域+{len(videos)}个视频，建议tiny→base提高术语准确率",
                "action": "建议确认后生效（修改配置或下次transcribe时自动采纳）",
            })
        
        # ── 统计4: speaker质量标记 — 基于已知错误模式数量 ──
        known_pats = p.get("known_patterns", [])
        if len(known_pats) >= 5 and "high_priority_correction" not in p.get("tuning_overrides", {}):
            p.setdefault("tuning_overrides", {})["high_priority_correction"] = True
            result["adjustments"].append({
                "speaker": name,
                "type": "high_priority_correction",
                "reason": f"已知{len(known_pats)}个错误模式，标记为高优先级校正speaker",
            })
    
    _save(db)
    
    if not result["adjustments"] and not result["suggestions"]:
        result["status"] = "no_changes"
    else:
        result["status"] = f"{len(result['adjustments'])}次调整, {len(result['suggestions'])}条建议"
    
    return result



def _trigger_auto_tune(speaker_name: str = None):
    """update_after_video 后自动触发，静默执行"""
    import json, os
    TUNE_LOG_PATH = os.path.expanduser("~/.biliyoutik2brain_tune_log.json")
    
    # v1.15.1: 如果 speaker_name 是某主号的别名，自动解析到主号
    db = _load()
    actual_speaker = speaker_name
    for name, p in db.items():
        if speaker_name and speaker_name in p.get("aliases", []):
            actual_speaker = name
            break
    
    result = auto_tune(actual_speaker)
    
    # 持久化调节日志
    try:
        with open(TUNE_LOG_PATH, 'r', encoding='utf-8') as f:
            log = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        log = {"runs": [], "total_adjustments": 0, "total_suggestions": 0}
    
    log["runs"].append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "speaker": speaker_name or "all",
        "adjustments": len(result.get("adjustments", [])),
        "suggestions": len(result.get("suggestions", [])),
        "details": result,
    })
    log["total_adjustments"] += len(result.get("adjustments", []))
    log["total_suggestions"] += len(result.get("suggestions", []))
    # 只保留最近50次
    log["runs"] = log["runs"][-50:]
    
    with open(TUNE_LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    
    if result["adjustments"] or result["suggestions"]:
        print(f"  [自动调参] {result['status']}")
        for adj in result["adjustments"][:5]:
            print(f"    🔧 {adj['speaker']} | {adj['type']}: {adj.get('old_value','?')}→{adj.get('new_value','?')} | {adj['reason']}")
    
    return result


# ═══════════════════════════════════════════════════════════════
# v2.2.0: teaching_patterns 自动推断 — 从视频行为数据推断教学类型
# ═══════════════════════════════════════════════════════════════

# 教学领域到默认 teaching_patterns 的映射

_DOMAIN_TEACHING_DEFAULTS = {
    "trading": {
        "indicator_style": "spatial_pointing",
        "indicator_triggers": {"type": "deictic_reference", "confidence_signal": "prosody_emphasis"},
        "visual_attention": "chart_annotation",
    },
    "tech": {
        "indicator_style": "live_demonstration",
        "indicator_triggers": {"type": "procedural", "confidence_signal": "word_pattern"},
        "visual_attention": "code_highlight",
    },
    "life": {
        "indicator_style": "static_explanation",
        "indicator_triggers": {"type": "none", "confidence_signal": "none"},
        "visual_attention": "none",
    },
    "general": {
        "indicator_style": "sequential_scroll",
        "indicator_triggers": {"type": "deictic_reference", "confidence_signal": "word_pattern"},
        "visual_attention": "slide_pointing",
    },
}


def infer_teaching_patterns(speaker_name: str, ocr_result: dict = None) -> dict:
    """
    自动推断/更新 UP 主的 teaching_patterns
    
    优先级：
    1. 已有 teaching_patterns → 保留（仅更新 visual_layout）
    2. 领域默认 → 交易→spatial_pointing, 技术→live_demonstration 等
    3. 从 OCR 结果反哺 → 如果有教学文字块，更新 visual_attention
    
    Args:
        speaker_name: UP主名称
        ocr_result: OCR v2 节点的输出（可选）
    
    Returns:
        更新后的 teaching_patterns
    """
    db = _load()
    if speaker_name not in db:
        # 新人：用领域默认
        return _DOMAIN_TEACHING_DEFAULTS.get("general", {})
    
    p = db[speaker_name]
    patterns = p.get("teaching_patterns", {})
    domain = p.get("domain", "general")
    
    # 步骤1: 如果完全没有 teaching_patterns，用领域默认填充
    if not patterns or not patterns.get("indicator_style"):
        defaults = _DOMAIN_TEACHING_DEFAULTS.get(domain, _DOMAIN_TEACHING_DEFAULTS["general"])
        for k, v in defaults.items():
            if k not in patterns or not patterns[k]:
                patterns[k] = v
    
    # 步骤2: 从 OCR 结果反哺 visual_layout
    if ocr_result and ocr_result.get("subtitle_region"):
        patterns.setdefault("visual_layout", {})
        patterns["visual_layout"]["subtitle_region"] = ocr_result["subtitle_region"]
    
    # 步骤3: 从 OCR 帧统计反哺 sampling_strategy
    stats = ocr_result.get("stats", {}) if ocr_result else {}
    if stats:
        patterns.setdefault("ocr_sampling_strategy", {})
        strat = patterns["ocr_sampling_strategy"]
        actual_frames = stats.get("frames_ocr", 0)
        scenes = stats.get("scenes_detected", 0)
        if actual_frames > 0 and scenes > 0:
            strat["dense_fps"] = max(1, int(actual_frames / max(scenes, 1)))
    
    # 保存
    p["teaching_patterns"] = patterns
    _save(db)
    
    return patterns



def get_teaching_patterns(speaker_name: str) -> dict:
    """获取 UP 主的 teaching_patterns（带领域默认回退）"""
    db = _load()
    p = db.get(speaker_name, {})
    patterns = p.get("teaching_patterns", {})
    
    if patterns and patterns.get("indicator_style"):
        return patterns
    
    # 回退：领域默认
    domain = p.get("domain", "general")
    return dict(_DOMAIN_TEACHING_DEFAULTS.get(domain, _DOMAIN_TEACHING_DEFAULTS["general"]))

