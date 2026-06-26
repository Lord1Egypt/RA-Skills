"""
M1.5 文案生成 — v10.0 简化版（去掉死板约束）

核心变革:
  1. 风格卡只提供方向引导（定位/声音/角度），不再有硬性模板
  2. 不再强制第一人称次数、句子长度、禁用词列表
  3. 不再强制 visual_plan 格式
  4. 不再做字数截断和第一人称注入
  5. 让 DeepSeek 自由发挥，只给原则不给模板
"""
import json
import os
import re
import random
import logging

# 🔧 (2026-05-31) 中→英场景名映射，用于fallback
_CN_TO_EN = {
    "成都": "Chengdu", "重庆": "Chongqing", "川西": "West Sichuan",
    "北川": "Northern Sichuan", "川南": "Southern Sichuan",
    "都江堰": "Dujiangyan", "文殊院": "Wenshu Temple",
    "宽窄巷子": "Kuanzhai Alley", "太古里": "Taikoo Li",
    "大熊猫基地": "Panda Base", "人民公园": "People's Park",
    "洪崖洞": "Hongya Cave", "解放碑": "Liberation Monument",
    "李子坝轻轨穿楼": "Liziba Metro", "长江索道": "Yangtze Cableway",
    "山城步道": "Mountain City Trail", "南山一棵树": "Nanshan Viewpoint",
    "南滨路": "Nanbin Road", "九寨沟": "Jiuzhaigou", "黄龙": "Huanglong",
    "泸沽湖": "Lugu Lake", "西昌邛海": "Xichang Qionghai",
    "四姑娘山": "Four Sisters Mountain", "塔公草原": "Tagong Grassland",
    "康定": "Kangding", "稻城亚丁": "Daocheng Yading",
    "乐山": "Leshan", "峨眉山": "Emeishan",
    "沙溪古镇": "Shaxi Old Town", "螺髻山": "Luoji Mountain",
}

def _cn_en(name: str) -> str:
    if name in _CN_TO_EN: return _CN_TO_EN[name]
    for cn, en in _CN_TO_EN.items():
        if cn in name or name in cn: return en
    return name
from pathlib import Path

logger = logging.getLogger(__name__)

# DeepSeek API configuration — 从 config_loader 读，环境变量优先
import os
from config_loader import get as cfg_get
DEEPSEEK_API_KEY = None
DEEPSEEK_BASE_URL = cfg_get("api.deepseek.base_url", "https://api.deepseek.com")

# ============================================================
# 方向场景池（中文名，给M3素材匹配用）
# ============================================================
DIRECTION_SCENES_V4 = {
    "成都": {
        "attractions": [
            "文殊院", "都江堰", "宽窄巷子", "太古里", "安顺廊桥",
            "339电视塔", "锦江", "人民公园", "大熊猫基地", "青城山",
            "杜甫草堂", "武侯祠", "锦里", "望江楼", "九眼桥",
            "春熙路", "铁像寺水街", "麓湖", "西村大院", "玉林路",
        ],
        "detail_scenes": {
            "文殊院": ["文殊院_大门", "文殊院_香炉", "文殊院_庭院", "文殊院_茶馆", "文殊院_红墙"],
            "都江堰": ["都江堰_鱼嘴", "都江堰_飞沙堰", "都江堰_宝瓶口", "都江堰_索桥", "都江堰_远眺"],
            "宽窄巷子": ["宽窄巷子_入口", "宽窄巷子_青砖墙", "宽窄巷子_茶馆", "宽窄巷子_庭院", "宽窄巷子_夜景"],
            "太古里": ["太古里_现代建筑", "太古里_Gucci", "太古里_大慈寺", "太古里_街景", "太古里_夜景"],
            "安顺廊桥": ["安顺廊桥_全景", "安顺廊桥_夜景", "安顺廊桥_桥下", "安顺廊桥_锦江"],
            "339电视塔": ["339电视塔_全景", "339电视塔_夜景", "339电视塔_顶楼", "339电视塔_俯瞰"],
            "锦江": ["锦江_日景", "锦江_夜景", "锦江_两岸", "锦江_游船"],
            "大熊猫基地": ["熊猫基地_熊猫", "熊猫基地_竹林", "熊猫基地_幼崽", "熊猫基地_户外"],
            "青城山": ["青城山_山门", "青城山_古道", "青城山_道观", "青城山_远眺", "青城山_绿荫"],
            "九眼桥": ["九眼桥_日景", "九眼桥_夜景", "九眼桥_酒吧街", "九眼桥_桥下"],
        },
    },
    "重庆": {
        "attractions": [
            "洪崖洞", "来福士", "李子坝轻轨穿楼", "长江索道", "山城步道",
            "魁星楼", "十八梯", "鹅岭二厂", "朝天门", "磁器口",
            "南山一棵树", "解放碑", "南滨路", "武隆天生三桥", "大足石刻",
        ],
        "detail_scenes": {
            "洪崖洞": ["洪崖洞_全景夜景", "洪崖洞_内部", "洪崖洞_顶层", "洪崖洞_千厮门大桥"],
            "来福士": ["来福士_全景", "来福士_底部", "来福士_顶部观景台", "来福士_朝天门广场"],
            "李子坝轻轨穿楼": ["李子坝_轻轨穿楼", "李子坝_站台", "李子坝_观景台", "李子坝_列车进站"],
            "长江索道": ["索道_车厢", "索道_长江之上", "索道_站台", "索道_全景"],
            "山城步道": ["山城步道_台阶", "山城步道_老建筑", "山城步道_俯瞰", "山城步道_转角"],
            "十八梯": ["十八梯_入口", "十八梯_老街道", "十八梯_夜景", "十八梯_茶馆"],
            "武隆天生三桥": ["武隆_天生三桥全景", "武隆_天龙桥", "武隆_青龙桥", "武隆_黑龙桥"],
        },
    },
    "川西": {
        "attractions": [
            "四姑娘山", "塔公草原", "墨石公园", "鱼子西", "格底拉姆",
            "木雅大寺", "古尔沟", "毕棚沟", "康定", "新都桥",
            "理塘", "稻城亚丁", "海螺沟", "色达", "丹巴藏寨",
        ],
        "detail_scenes": {
            "四姑娘山": ["四姑娘山_全景", "四姑娘山_幺妹峰", "四姑娘山_草甸", "四姑娘山_海子"],
            "塔公草原": ["塔公草原_全景", "塔公草原_雅拉雪山", "塔公草原_木雅大寺", "塔公草原_经幡"],
            "墨石公园": ["墨石公园_全景", "墨石公园_石林", "墨石公园_栈道", "墨石公园_异域"],
            "鱼子西": ["鱼子西_日落", "鱼子西_雪山", "鱼子西_星空", "鱼子西_秋千"],
            "丹巴藏寨": ["丹巴_碉楼", "丹巴_藏寨", "丹巴_山谷", "丹巴_梯田"],
        },
    },
    "北川": {
        "attractions": [
            "九寨沟", "黄龙", "松潘古城", "牟尼沟", "达古冰川", "若尔盖",
        ],
        "detail_scenes": {
            "九寨沟": ["九寨沟_五花海", "九寨沟_长海", "九寨沟_诺日朗瀑布", "九寨沟_五彩池", "九寨沟_树正群海"],
            "黄龙": ["黄龙_五彩池", "黄龙_金沙铺地", "黄龙_飞瀑", "黄龙_远眺", "黄龙_栈道"],
            "松潘古城": ["松潘古城_城门", "松潘古城_城墙", "松潘古城_老街", "松潘古城_远眺"],
            "达古冰川": ["达古冰川_冰川", "达古冰川_索道", "达古冰川_山顶", "达古冰川_云海"],
        },
    },
    "川南": {
        "attractions": [
            "西昌邛海", "螺髻山", "泸沽湖", "大理古城", "洱海", "沙溪古镇",
        ],
        "detail_scenes": {
            "泸沽湖": ["泸沽湖_全景", "泸沽湖_猪槽船", "泸沽湖_走婚桥", "泸沽湖_里格半岛", "泸沽湖_日落"],
            "洱海": ["洱海_全景", "洱海_骑行", "洱海_日落", "洱海_海鸥"],
            "大理古城": ["大理古城_城门", "大理古城_人民路", "大理古城_洋人街", "大理古城_苍山"],
            "沙溪古镇": ["沙溪_古戏台", "沙溪_寺登街", "沙溪_玉津桥", "沙溪_田野"],
        },
    },
}


def get_api_key() -> str:
    """获取DeepSeek API Key"""
    global DEEPSEEK_API_KEY
    if DEEPSEEK_API_KEY:
        return DEEPSEEK_API_KEY

    auth_path = Path.home() / ".openclaw" / "agents" / "main" / "agent" / "auth-profiles.json"
    if not auth_path.exists():
        auth_path = Path(__file__).parent.parent / ".openclaw" / "agents" / "main" / "agent" / "auth-profiles.json"

    if auth_path.exists():
        try:
            with open(auth_path) as f:
                data = json.load(f)
            profiles = data.get("profiles", {})
            for profile_name, val in profiles.items():
                k = val.get("key", "") or val.get("api_key", "")
                if not k and "credentials" in val:
                    k = val["credentials"].get("api_key", "")
                if k:
                    DEEPSEEK_API_KEY = k
                    logger.info(f"Loaded API key from {auth_path}")
                    return DEEPSEEK_API_KEY
        except Exception as e:
            logger.warning(f"Failed to load auth-profiles: {e}")

    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if api_key:
        DEEPSEEK_API_KEY = api_key
        return api_key

    logger.warning("No DeepSeek API key found")
    return ""


def _search_real_info(direction: str, account_info: dict = None) -> str:
    """搜索实时信息 + 知识库 → 注入M1.5 prompt"""
    style = (account_info or {}).get("style", "")
    is_family = style == "soft_signal"

    DIRECTION_FACTS = {
        "成都": (
            "Chengdu, capital of Sichuan, has 21 million people. "
            "Dujiangyan irrigation system (built 256 BC). Wenshu Monastery (Tang Dynasty). "
            "Giant Panda Breeding Research Base. Jinli, Wuhou Shrine, Du Fu Thatched Cottage. "
            "Known for Sichuan cuisine, tea culture, 3,000-year history.\n\n"
            "GEOGRAPHIC: CITY CENTER (walkable): 文殊院, 宽窄巷子, 人民公园, 太古里, 春熙路, 九眼桥, 安顺廊桥, 武侯祠, 锦里. "
            "SUBURB (30min): 大熊猫基地. DAY TRIP (1-1.5hr): 都江堰(60km), 青城山(70km). "
            "RULE: Don't mix city center + day trip in single scene. Distances: Chengdu→Dujiangyan 60km/1hr, Chengdu→Leshan 140km/2hr."
        ),
        "重庆": (
            "Chongqing has 32 million people. Built on mountains at Yangtze-Jialing confluence. "
            "Hongya Cave, Yangtze River Cableway (1,166m), hot pot culture. "
            "GEOGRAPHIC: CITY CENTER (2km): 解放碑, 洪崖洞, 来福士, 长江索道, 魁星楼, 十八梯, 山城步道. "
            "NEARBY: 李子坝(20min), 鹅岭二厂, 磁器口(20km). FULL DAY: 武隆天生三桥(170km)."
        ),
        "川西": (
            "West Sichuan high-altitude Tibetan landscapes. Gongga Shan (7,556m). "
            "ROUTE: 成都→康定(330km/4-5hr)→塔公草原(100km/2hr, 3,730m)→墨石公园(15km)→丹巴藏寨(120km). "
            "High altitude warnings above 3,000m."
        ),
        "北川": (
            "Jiuzhaigou Valley UNESCO — 114 lakes, 17 waterfalls at 2,000m+. Huanglong travertine pools. "
            "ROUTE: Chengdu→Jiuzhaigou 410km/6-7hr. Jiuzhaigou→Huanglong 100km/2hr."
        ),
        "川南": (
            "Leshan Giant Buddha (71m, built 713-803 AD). Emeishan (3,099m). Lugu Lake (2,685m). "
            "ROUTE: Chengdu→Leshan 140km/2hr. Chengdu→Xichang 450km/5hr. Xichang→Lugu Lake 260km/5hr."
        ),
    }

    facts = DIRECTION_FACTS.get(direction, "")
    output = f"=== KEY FACTS about {direction} ===\n{facts}"

    # 亲子注入
    if is_family:
        family_tips = {
            "成都": "FAMILY: Panda Base before 10am, stroller-friendly. Dujiangyan flat paths. Altitude 500m safe.",
            "川西": "FAMILY (HIGH ALTITUDE!): 3,000m+, kids under 5 caution. Oxygen available 20-30 RMB. Private car essential.",
        }
        tip = family_tips.get(direction, "")
        if tip:
            output += f"\n\n{tip}"
    logger.info(f"  Knowledge base injected")
    return output


def _build_direction_scene_context(direction: str) -> str:
    """构建方向场景上下文"""
    pool = DIRECTION_SCENES_V4.get(direction)
    if not pool:
        return ""
    attractions = pool.get("attractions", [])
    return (
        f"Available ATTRACTIONS in {direction} (use these exact Chinese names for scene names):\n"
        + ", ".join(attractions)
        + "\nNOTE: Scene names MUST be at ATTRACTION level only, e.g. '都江堰' not '都江堰_鱼嘴'."
    )


def _get_voice_profile(style_group: str, account_info: dict) -> str:
    """v11.0: 按风格组返回独特声音配置 — 5种声音，各不相同"""
    profiles = {
        "velvet": (
            "VOICE: Curator, not tour guide. You've seen it all and you're selectively sharing the best.\n"
            "• Confidence, not arrogance. 'This is worth your time' — not 'this is the best in the world.'\n"
            "• Rich sensory details: the sound of temple bells at 6am, the texture of ancient stone under your hand.\n"
            "• You speak less than other accounts — let the images do the heavy lifting.\n"
            "• Hook flavor: IMAGINE or PROVOCATION work best. Avoid CONFESSION (not vulnerable, you're the expert)."
        ),
        "soft_signal": (
            "VOICE: The mom/dad friend who's been there. Warm, real, never preachy.\n"
            "• You're speaking from experience: tried it with your own kids, learned the hard way.\n"
            "• Emotion first: the look on a child's face, the relief of a smooth travel day.\n"
            "• Not 'this is great for kids' — show WHY through a specific moment.\n"
            "• Hook flavor: CONFESSION or IMAGINE work best. 'I brought my own kids here' hits different."
        ),
        "shadow_cut": (
            "VOICE: The insider who knows the map better than anyone. Direct, slightly provocative.\n"
            "• You're not selling — you're correcting a mistake. 'Your route has a flaw. Here's the fix.'\n"
            "• Concrete and quantifiable: minutes saved, kilometers skipped, dollars wasted.\n"
            "• That slight arrogance is intentional — you've tested this 50 times. You're right.\n"
            "• Hook flavor: PROVOCATION or QUESTION work best. Make them doubt their own plan."
        ),
        "swiss_pulse": (
            "VOICE: The practical expert. Clear, useful, no fluff. Like a really good checklist in human form.\n"
            "• One actionable takeaway per video. 'Here's the one thing you need to know about X.'\n"
            "• Clean language: short sentences, active verbs, zero adjectives that don't carry weight.\n"
            "• The 'I wish someone told me this before my first trip' energy.\n"
            "• Hook flavor: QUESTION or REVERSE work best. Open their eyes to what they're missing."
        ),
        "comparison": (
            "VOICE: The savvy value-hunter who's done the math. Smart, playful, not bitter.\n"
            "• Every claim is backed by a number or comparison. No vague 'great value' — show the spread.\n"
            "• The fun is in the reveal: 'They paid THIS. We paid THIS. Same view.'\n"
            "• Not cheap — clever. You're not cutting corners, you're cutting waste.\n"
            "• Hook flavor: PROVOCATION or REVERSE work best. Price shocks or expectation flips."
        ),
    }
    return profiles.get(style_group, profiles["velvet"])


def _generate_prompt(account_info: dict, direction: str,
                     style_card: str, history: list = None) -> str:
    """构建文案生成prompt — v10.0 简化版"""

    account_id = account_info.get("id", "00")
    account_name = account_info.get("name", "China Unbounded")
    brand_name = account_info.get("brand_name", "Pandajourneys")
    style_group = account_info.get("style", "velvet")

    # 场景上下文
    scene_context = _build_direction_scene_context(direction)

    # 历史去重
    history_context = ""
    if history:
        recent = history[-5:] if len(history) > 5 else history
        captions = [h.get("caption", "") for h in recent if isinstance(h, dict) and h.get("caption")]
        if captions:
            history_context = (
                "\nRECENTLY PUBLISHED (avoid repeating these topics):\n"
                + "\n".join(f"  - \"{c[:100]}...\"" for c in captions[-3:])
            )

    # 视觉指引
    visual_guide = ""
    if style_group == "velvet":
        visual_guide = "Visual: Gold #FFD700, city showcase, cinematic cuts. Focus on 1-2 core city experiences per video."
    elif style_group == "soft_signal":
        visual_guide = "Visual: Warm pink gradients, family moments, floating stars. Show activities through a family lens."
    elif style_group == "shadow_cut":
        visual_guide = "Visual: Dark open + stunning reveals, #D4AF37 gold. Route map, nodes, timeline. If multi-day route, include itinerary_data in output."
    elif style_group == "swiss_pulse":
        visual_guide = "Visual: Clean layout, teal #22D3EE, step numbers, progress bars. Each scene is one actionable tip."
    elif style_group == "comparison":
        visual_guide = "Visual: Split-screen or before/after, coral #FF6B6B. Show contrast between two sides. Each scene highlights a dimension of comparison."

    # 内容方向指引（轻量风格原则，不绑定模板）
    content_direction = ""
    if style_group == "swiss_pulse":
        content_direction = "Content angle: You're sharing advice/insider knowledge, not telling a destination story. Each scene delivers one specific, actionable point grounded in real details (app names, prices, times, real numbers). The 'gap' in your hook is a traveler friction point they haven't solved — not a city they haven't seen."
    elif style_group == "comparison":
        content_direction = "Content angle: Compare two sides. Each scene highlights one dimension of contrast — price, experience, crowd level, value. The 'gap' is: 'I've been comparing wrong.'"

    # --- v11.0: 声音注入 + 钩子多样化 ---
    voice_profile = _get_voice_profile(style_group, account_info)

    prompt = f"""{style_card}

---

🎬 THIS VIDEO

Brand: Pandajourneys • {direction}

Available Scenes: {scene_context}
{history_context}
{visual_guide}
{f"Content Direction: {content_direction}" if content_direction else ""}

---

🗣️ VOICE PROFILE — THIS ACCOUNT

{voice_profile}

---

🎬 HOW TO WRITE THIS

You are Pandajourneys. "We" = Pandajourneys. "You" = the traveler.
15-24 second short video. 40-60 words. 2-4 scenes.

🎲 HOOK — Pick ONE of these 5 types. DO NOT default to just one type across videos:

1. REVERSE — "What if [common belief] is wrong?" Flips a traveler assumption.
   Ex: "What if the best time to visit Jiuzhaigou isn't morning?"
   Ex: "What if skipping Chengdu on your Sichuan trip is the right call?"

2. IMAGINE — Drops the viewer into a sensory moment. No facts, just feeling.
   Ex: "6AM. Mist rising off Lugu Lake. A Mosuo fisherman sings as he paddles past your window."
   Ex: "Your first bite of real mapo tofu. The numbing hits, then the fire, then the craving."

3. CONFESSION — Something we learned the hard way. Personal, vulnerable.
   Ex: "We designed this route wrong 3 times before we got it right. Here's what we changed."
   Ex: "We used to tell clients to skip this city. Then one of them went anyway and proved us wrong."

4. PROVOCATION — A bold, specific claim that demands a reaction.
   Ex: "That $400 hotel and the $50 guesthouse face the same mountain. We checked."
   Ex: "40,000 people leave Jiuzhaigou at 5pm. They're missing the best part."

5. QUESTION — One sharp question the viewer hasn't asked themselves yet.
   Ex: "Would you pay $300 for a view you can get for $50?"
   Ex: "How many hours of your vacation are you willing to spend in transit?"

⛔ FORBIDDEN HOOK OPENERS — These will be REJECTED:
"Most people [do X]..." ❌ (used 600+ times, viewers scroll past)
"Most travelers [do X]..." ❌
"Most families/tourists/couples [do X]..." ❌
"Everyone [does X]..." ❌
Any sentence starting with "Most" ❌

📖 BODY — One moment, not one fact. Don't explain — make them feel it.
Give one specific, sensory detail that proves your hook. A time. A price. A sound. A taste.
Natural spoken English. Contractions. Short sentences. No lists.

🔗 CTA — Two-part closer: brand tagline → soft action. Vary your approach:

The video's final two sentences follow this flow:

BRAND CLOSER (pick one, adapt naturally):
• "That's how we plan it."
• "We customize your private trip."
• "That's the Pandajourneys difference."
• "This is how we do it."
• "We handle the details — you take the trip."

SOFT CTA — immediately after brand closer, pick one type:
TYPE A — DELIVERABLE: "DM us CHENGDU for our exact itinerary"
TYPE B — CURIOSITY: "Link in bio for the route we actually tested"
TYPE C — SOCIAL: "200+ families have taken this route — DM us to join"
TYPE D — SAVE: "Bookmark this for your trip planning"
TYPE E — IMPLIED: "We'll send you the full route" (no explicit DM, implied)

❌ NEVER use bare "DM us" alone — always pair with brand closer.
❌ NEVER "Comment below" / "Follow for more" / "What do you think?"

🧩 THE CHAIN — Hook opens → One moment delivers → Brand closer → CTA closes.

Scene names: Chinese attraction names from the Available Scenes list.

OUTPUT FORMAT (valid JSON only, no markdown):

⚠️ speech_text MUST end with: brand closer → CTA. Two sentences. Videos without both will be REJECTED.

{{
  "speech_text": "40-60 word voiceover. Hook→Body→CTA. Pandajourneys platform voice. ALL ENGLISH — NO Chinese characters.",
  "caption": "Social media description (DISITNCT from speech_text — NOT a copy of voiceover). Under 220 chars. Must include #pandajourneys. 3-5 hashtags total.",
  "hook_text": "On-screen hook — 3-5 words, stops the scroll",
  "cta_text": "Call to action phrase",
  "scenes": ["中文场景名1", "中文场景名2"],
  "scene_mapping": [
    {{
      "scene": "都江堰",
      "speech_segment": "What is said during this scene",
      "tags": ["city", "都江堰", "白天", "航拍"],
      "effects": [],
      "visual_plan": {{
        "type": "hook",
        "headline": "2-5 word grabber",
        "subtitle": "10-15 word detail",
        "accent": "gold"
      }}
    }}
  ]
}}

visual_plan.accent by style: velvet=gold, soft_signal=sunset, shadow_cut=amber, swiss_pulse=teal, comparison=coral.

Generate ONLY valid JSON."""

    return prompt


def call_llm(prompt: str, model: str = "deepseek-v4-pro", max_tokens: int = 3000) -> str:
    """调用LLM — DeepSeek优先, 失败自动切MiMo V2.5 (2026-05-31)"""
    
    # === 方案1: DeepSeek V4 Pro ===
    ds_key = get_api_key()
    if ds_key:
        try:
            import urllib.request
            url = f"{DEEPSEEK_BASE_URL}/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {ds_key}",
                "Content-Type": "application/json",
            }
            data = json.dumps({
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.8,
                "thinking": {"type": "disabled"},
            }).encode()
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=180) as resp:
                result = json.loads(resp.read())
                content = result["choices"][0]["message"].get("content", "")
                if content.strip():
                    logger.info("  ✅ DeepSeek V4 Pro")
                    return content
        except Exception as e:
            logger.warning(f"  DeepSeek failed: {e}")
    
    # === 方案2: MiMo V2.5 Pro 兜底 (动态读取API key) ===
    mimo_key = _get_mimo_key()
    if mimo_key:
        try:
            import urllib.request
            url = "https://token-plan-cn.xiaomimimo.com/v1/chat/completions"
            headers = {
                "api-key": mimo_key,
                "Content-Type": "application/json",
            }
            data = json.dumps({
                "model": "mimo-v2.5",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 6000,  # MiMo推理模型需要更多token
            }).encode()
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=180) as resp:
                result = json.loads(resp.read())
                content = result["choices"][0]["message"].get("content", "") or \
                         result["choices"][0]["message"].get("reasoning_content", "")
                if content.strip():
                    logger.info("  🔄 DeepSeek降级 → MiMo V2.5 Pro")
                    return content
        except Exception as e:
            logger.warning(f"  MiMo also failed: {e}")
    
    # === 全部失败 — 不降级到fallback，直接报错 ===
    logger.error("  ❌ 所有LLM方案均失败，停止生产")
    return None


def _get_mimo_key() -> str:
    """从auth-profiles动态读取MiMo API key (2026-05-31)"""
    try:
        auth_path = Path.home() / ".openclaw" / "agents" / "main" / "agent" / "auth-profiles.json"
        if not auth_path.exists():
            auth_path = Path(__file__).parent.parent / ".openclaw" / "agents" / "main" / "agent" / "auth-profiles.json"
        if auth_path.exists():
            with open(auth_path) as f:
                data = json.load(f)
            for name, prof in data.get("profiles", {}).items():
                if "xiaomi" in name.lower() or "mimo" in name.lower():
                    key = prof.get("key", "")
                    if key:
                        return key
    except Exception as e:
        logger.warning(f"Failed to load MiMo key: {e}")
    return ""


def parse_script_response(response_text: str) -> dict:
    """解析LLM返回的JSON"""
    if not response_text:
        return None

    text = response_text.strip()

    # 匹配 ```json ... ``` 代码块
    code_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
    if code_match:
        text = code_match.group(1).strip()

    # 找到第一个{作为JSON起点
    brace_start = text.find('{')
    if brace_start >= 0:
        depth = 0
        end = -1
        for i in range(brace_start, len(text)):
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end > brace_start:
            json_str = text[brace_start:end+1]
            try:
                data = json.loads(json_str)
                required = ["speech_text", "caption", "scenes"]
                if all(k in data for k in required):
                    return data
            except json.JSONDecodeError:
                pass

    logger.warning("Failed to parse LLM response as JSON")
    return None


def generate_script(account_info: dict, direction: str, history: list = None,
                    m1_strategy_prompt: str = "",
                    m2_feedback: str = "") -> dict:
    """生成完整文案"""

    # 风格卡为空时的默认提示
    if not m1_strategy_prompt:
        m1_strategy_prompt = (
            "=== M1 风格卡 ===\n"
            "账号定位: 高端中国旅行内容\n"
            "目标受众: 国际旅行者\n"
            "声音: 自然口语化英语，像朋友聊天\n"
            "=== END ===\n"
        )

    # 搜索真实信息
    real_data = _search_real_info(direction, account_info)
    if real_data:
        logger.info(f"✅ 搜索数据注入")

    # 构建prompt
    raw_prompt = _generate_prompt(account_info, direction, m1_strategy_prompt, history)

    # M2反馈注入（简化版，不强制要求格式）
    if m2_feedback:
        raw_prompt += f"\n\n=== QUALITY FEEDBACK (fix these) ===\n{m2_feedback}\n\nAddress the above issues in your new output. Focus on natural English and avoiding repeated content.\n"
        logger.info(f"  🔧 M2反馈: {m2_feedback[:60]}...")

    # 搜索数据追加
    if real_data:
        raw_prompt += f"\n\n=== REAL DATA ===\n{real_data}\n\nUse these facts for accuracy. Don't invent numbers."

    # 调用LLM (DeepSeek → MiMo兜底)
    response = call_llm(raw_prompt, max_tokens=3000)
    if response is None:
        logger.error("❌ 所有LLM方案均失败，无法生成文案")
        return None  # 上游会处理None → 停止生产
    
    script = parse_script_response(response)

    if not script:
        logger.warning("LLM response parse failed, retrying...")
        response = call_llm(raw_prompt, max_tokens=3000)
        script = parse_script_response(response)
    
    if not script:
        logger.error("❌ LLM response parse failed twice, abort")
        return None

    # 基础后处理（不强制修改内容）
    speech_text = script.get("speech_text", "")

    # 解析scene_mapping
    scene_mapping = script.get("scene_mapping", [])
    if scene_mapping:
        logger.info(f"  scene_mapping: {len(scene_mapping)} entries")
    else:
        scene_mapping = _build_fallback_mapping(script.get("scenes", []), speech_text)
    script["scene_mapping"] = scene_mapping

    # 确保visual_plan存在（降级补全）
    for m in scene_mapping:
        if "visual_plan" not in m:
            m["visual_plan"] = {
                "type": "detail",
                "headline": m.get("scene", ""),
                "subtitle": m.get("speech_segment", "")[:80],
                "accent": "gold",
            }

    # 注入账号元数据
    script["account_id"] = account_info.get("id", "00")
    script["account_name"] = account_info.get("name", "")
    script["direction"] = direction

    # 字数截断：超过60词裁到最后一个句号
    MAX_WORDS = 60
    wc = len(speech_text.split())
    if wc > MAX_WORDS:
        words = speech_text.split()
        truncated = " ".join(words[:MAX_WORDS])
        last_period = truncated.rfind(".")
        if last_period > len(truncated) * 0.6:
            speech_text = truncated[:last_period + 1]
        else:
            speech_text = truncated + "."
        script["speech_text"] = speech_text
        wc_new = len(speech_text.split())
        logger.info(f"  ✂️ 字数截断: {wc}→{wc_new}词")
        wc = wc_new
    sc = len(script.get("scenes", []))
    logger.info(f"  ✅ 文案: {wc}词 / {sc}场景")
    script["word_stats"] = {"word_count": wc, "scene_count": sc}

    return script


def _build_fallback_mapping(scenes: list, speech_text: str) -> list:
    """降级：按 scenes 顺序分段 speech_text"""
    if not scenes or not speech_text:
        return []
    sentences = re.split(r'(?<=[.!?])\s+', speech_text)
    n = len(scenes)
    per_scene = max(1, len(sentences) // n) if n else 1
    mapping = []
    for i, scene_name in enumerate(scenes):
        start = i * per_scene
        end = start + per_scene if i < n - 1 else len(sentences)
        segment = " ".join(sentences[start:end])
        mapping.append({
            "scene": scene_name,
            "speech_segment": segment,
            "tags": ["city", scene_name, "白天", "旅拍"],
            "visual_plan": {"type": "detail", "headline": scene_name, "subtitle": segment[:80], "accent": "gold"},
        })
    return mapping


def _has_cta(text: str) -> bool:
    """检查CTA — 双档位: DM us 或 Save this for (2026-05-31)"""
    if re.search(r'\bDM\s+us\s+\w+', text, re.I):
        return True
    if re.search(r'\bSave\s+this\s+for\s+your\s+\w+', text, re.I):
        return True
    return False


def _fallback_script_v2(account_info: dict, direction: str) -> dict:
    """降级模板 — 纯英文输出 (2026-05-31 修复)"""
    aid = account_info.get("id", "00")
    account_name = account_info.get("name", "China Travel")

    pool = DIRECTION_SCENES_V4.get(direction, {})
    attractions = pool.get("attractions", ["attraction"])[:4]
    # 全部转英文
    en_attractions = [_cn_en(a) for a in attractions]
    en_direction = _cn_en(direction)

    scenes = attractions[:4]
    en_scene_info = ", ".join(en_attractions)

    script = {
        "speech_text": (
            f"Discover {en_direction} in a way most travelers never experience. "
            f"From {en_attractions[0] if len(en_attractions) > 0 else 'the old city'} "
            f"to {en_attractions[-1] if len(en_attractions) > 1 else 'hidden gems'}, "
            f"every corner tells a story. "
            f"Visit {en_scene_info} — each one will change how you see China. "
            f"Save this for your {en_direction} itinerary, and follow {account_name} for more luxury China travel guides."
        ),
        "caption": f"Discover the real {en_direction} 🇨🇳 #ChinaTravel #{en_direction.replace(' ','')} #LuxuryTravel",
        "hook_text": f"This is {en_direction}",
        "cta_text": f"DM us {en_direction.upper().replace(' ','')} for your custom itinerary",
        "scenes": scenes,
        "scene_mapping": [
            {"scene": s, "speech_segment": f"Discover {_cn_en(s)}...", "tags": ["city", s, "白天", "旅拍"],
             "visual_plan": {"type": "detail", "headline": s, "subtitle": f"Exploring {s}", "accent": "gold"}}
            for s in scenes
        ],
    }
    return script
