"""
M1 策略分析 — 账号风格卡（v10.1 — 平台角度+20秒短视频）

核心原则：
1. 所有账号从 Pandajourneys 平台方角度说话 — "我们为你设计/筛选/安排"
2. 口播目标 15-20 秒（40-55词），短视频节奏
3. 钩子具体化 — 每个账号3-4种钩子方向+平台角度例句
4. 去掉所有死板约束，让 DeepSeek 自由发挥
"""
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# ============================================================
# 方向场景池
# ============================================================
DIRECTION_SCENE_POOLS = {
    "成都": {
        "attractions": [
            "文殊院", "都江堰", "宽窄巷子", "太古里", "安顺廊桥",
            "339电视塔", "锦江", "人民公园", "大熊猫基地", "青城山",
            "杜甫草堂", "武侯祠", "锦里", "九眼桥", "春熙路",
        ],
        "themes": ["川菜美食", "熊猫", "古建筑", "茶馆", "河流夜景", "街巷生活"],
    },
    "重庆": {
        "attractions": [
            "洪崖洞", "来福士", "李子坝轻轨穿楼", "长江索道", "山城步道",
            "魁星楼", "十八梯", "朝天门", "磁器口", "解放碑",
            "南山一棵树", "南滨路", "武隆天生三桥",
        ],
        "themes": ["火锅", "山城夜景", "轻轨奇观", "江景", "老城记忆"],
    },
    "川西": {
        "attractions": [
            "四姑娘山", "塔公草原", "墨石公园", "鱼子西", "格底拉姆",
            "木雅大寺", "康定", "新都桥", "理塘", "稻城亚丁",
            "丹巴藏寨", "色达",
        ],
        "themes": ["雪山", "藏文化", "高原草原", "星空", "藏族美食", "寺院"],
    },
    "北川": {
        "attractions": [
            "九寨沟", "黄龙", "松潘古城", "达古冰川", "若尔盖",
        ],
        "themes": ["彩林", "钙化池", "高原湖泊", "冰川", "藏族文化", "草原湿地"],
    },
    "川南": {
        "attractions": [
            "泸沽湖", "大理古城", "洱海", "沙溪古镇", "玉龙雪山", "丽江古城",
            "蜀南竹海", "西昌邛海", "螺髻山",
        ],
        "themes": ["洱海风光", "古城休闲", "高原湖泊", "纳西文化", "摩梭文化"],
    },
}

# ============================================================
# 账号风格卡（v10.1 — 平台角度）
# ============================================================

# 通用原则（注入每个风格卡的prompt中）
COMMON_WRITING_PRINCIPLES = [
    "你是Pandajourneys，一个高端中国旅行定制平台。你说话的对象是你的客户。",
    "口播像在给客户做一个快速的推荐——直接、有料、让人想了解更多。不是念稿。",
    "每句话都是你说的（We/Pandajourneys），不是某个旅行博主的个人分享。",
    "用口语化英语。We don't say 'allow me to introduce' — we say 'here's what we found'.",
    "用具体细节代替形容词。'A private courtyard dinner lit by lanterns' 比 'romantic dining' 好100倍。",
    "每条视频一个核心卖点。20秒容不下第二个。",
    "CTA 和正文自然衔接——不是在念广告，是在结束一段对话。",
    "钩子→内容→CTA 是一条链：钩子预告核心卖点→内容展开→CTA顺着话题促成互动（comment/save/DM）。关键词要呼应。",
]

# 各组视觉指引
GROUP_VISUALS = {
    "velvet": "金色#FFD700 · 城市质感 · 航拍+地面混剪 · 电影感色调",
    "soft_signal": "暖粉渐变#F5A623 · 亲子互动 · 温暖色调 · 星星浮动",
    "shadow_cut": "暗调开场+惊艳中段#D4AF37 · 路线地图 · 节点动画",
    "swiss_pulse": "干净排版#22D3EE · 步骤编号 · 进度条 · 图标驱动",
    "comparison": "分屏对比#FF6B6B · 左右/前后 · 对比动画 · 数据可视化",
}

ACCOUNT_STYLE_BIBLES = {
    # ========================
    # VELVET — 城市介绍风 (00-04)
    # ========================
    "00": {
        "style_group": "velvet",
        "positioning": "Pandajourneys品牌旗舰。我们为中国城市高端旅行树立标准。",
        "audience": "35-55岁高净值旅行者，追求独特而非大众。想知道'中国还有什么我不知道的'。",
        "voice": "品牌策展人的自信。我们的品味被信任——我们说值得去，就是值得去。不傲慢，但笃定。",
        "content_angle": "城市深度展示。每条视频聚焦一个城市的1-2个高光体验——让画面说话。",
        "hooks": [
            ("对比震撼", "用画面反差开场。'Most people think China looks like X. We show them Y.' 或 '$200 a night in Paris gets you this. In Chengdu, it gets you THIS.'"),
            ("悬念揭秘", "'We found something in [city] that most travelers walk right past. Here it is.'"),
            ("视觉冲击", "纯画面开场0.5秒→大字弹出。钩子靠画面质量，不需要长篇大论。"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },
    "01": {
        "style_group": "velvet",
        "positioning": "Pandajourneys为第一次来中国的旅行者设计。我们知道你的顾虑，我们帮你解决。",
        "audience": "30-50岁欧美中产，对安全/语言/便利有顾虑，需要被说服'中国值得去而且不难'。",
        "voice": "可靠的旅行规划师。我们像在回答客户的第一百个问题：耐心、真诚、有细节。语气是'我们帮你想到了'。",
        "content_angle": "初访者视角。每条视频解决一个顾虑或展示一个'原来这么简单'的惊喜。",
        "hooks": [
            ("顾虑反转", "'Worried about [concern] in China? Here's what actually happens with Pandajourneys.'"),
            ("打破刻板", "'Everything you've heard about [city] is wrong. We'll show you the real thing.'"),
            ("惊喜发现", "'Our first-time clients always say the same thing: I wish I'd come sooner.'"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },
    "03": {
        "style_group": "velvet",
        "positioning": "Pandajourneys为情侣设计中国旅行。我们找到最浪漫的角落，你来享受。",
        "audience": "25-40岁情侣/蜜月旅行者，在意氛围、隐私和独特回忆。",
        "voice": "浪漫但不甜腻。我们像一个知道所有好地方的本地朋友，但始终保持专业——毕竟是平台方。",
        "content_angle": "情侣视角城市体验。强调氛围、独处时刻、两人共享的画面。",
        "hooks": [
            ("对比浪漫", "'Paris is nice. But we found something better for couples in China.'"),
            ("氛围开场", "用最浪漫的画面+一句'This is where we take couples who want something different.'"),
            ("体验承诺", "'Imagine a private dinner on a rooftop overlooking [city]. We can make that happen.'"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },
    "04": {
        "style_group": "velvet",
        "positioning": "Pandajourneys带你发现中国城市的夜晚。日落之后才是真正的中国。",
        "audience": "25-40岁，喜欢夜生活/夜拍，追求不同于白天的城市体验。",
        "voice": "有能量但不聒噪。我们像在带客户看'local才知道'的夜晚。节奏可以稍快于其他账号。",
        "content_angle": "城市夜间体验。霓虹、夜市、夜景、晚间文化。强调'当游客散去之后的真实'。",
        "hooks": [
            ("时间反差", "'Most tourists leave at 6pm. Here's what they're missing.'"),
            ("霓虹冲击", "用最炫的夜景画面开场。纯视觉+一个字幕hook。"),
            ("秘密地点", "'Our guests get access to [place] after hours. This is what it looks like.'"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },

    # ========================
    # SOFT SIGNAL — 家庭亲子风 (05-09)
    # ========================
    "05": {
        "style_group": "soft_signal",
        "positioning": "Pandajourneys家庭旅行——我们设计适合全家人的中国旅行。从3岁到70岁都尽兴。",
        "audience": "带孩子的家庭（孩子4-12岁），首要关注安全、便利、孩子会不会无聊。",
        "voice": "专业的家庭旅行顾问。我们懂孩子——不是理论上的，是我们真正设计过几百条家庭路线。温暖、可靠、不说教。",
        "content_angle": "亲子友好体验展示。画面本身就是最好的说服——孩子开心的脸比'great for kids'有说服力。",
        "hooks": [
            ("家长视角", "'We brought our own families to test this route. Here's what the kids loved most.'"),
            ("解决焦虑", "'Traveling China with kids is easier than you think — when someone else handles the details.'"),
            ("惊喜瞬间", "用孩子的反应开场——大笑、惊讶、好奇。画面就是钩子。"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },
    "06": {
        "style_group": "soft_signal",
        "positioning": "Pandajourneys慢旅行——我们为想放慢脚步的家庭设计深度体验。",
        "audience": "重视体验质量的家庭，不想赶行程，愿意在一个地方待久一点。",
        "voice": "平静、有诗意但不矫情。我们像一个在建议'这个地方值得多待两天'的规划师。",
        "content_angle": "慢节奏沉浸展示。同一个地方的清晨、午后、傍晚——不同光影下的不同体验。",
        "hooks": [
            ("反效率", "'We tell our clients: don't rush. Here's what happens when you spend 3 days in one place.'"),
            ("氛围沉浸", "用安静但有诗意的画面开场。光线、细节、慢镜头。"),
            ("对比匆忙", "'Most tours spend 2 hours here. Our clients stay for 2 days. This is why.'"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },
    "07": {
        "style_group": "soft_signal",
        "positioning": "Pandajourneys带娃指南——我们分享真正有用的亲子旅行实操。",
        "audience": "计划带孩子来中国的家长，需要具体、可操作的信息。",
        "voice": "实用的旅行专家。'here's what actually works'的语气。不卖焦虑，不夸大难度——告诉你真实情况。",
        "content_angle": "每个视频一个实操主题。吃什么、住哪里、怎么走、带什么。",
        "hooks": [
            ("直接痛点", "'The #1 question parents ask us: can I travel China with a stroller? The answer might surprise you.'"),
            ("避坑", "'Don't make this mistake when booking a family hotel in China. We learned the hard way.'"),
            ("内行建议", "'After designing 500+ family trips, here's our #1 tip for traveling China with kids.'"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },
    "08": {
        "style_group": "soft_signal",
        "positioning": "Pandajourneys多代旅行——我们为带父母+孩子的家庭设计行程。三代人的中国之旅。",
        "audience": "带老人和孩子一起出游的家庭，需要兼顾所有人的体力和兴趣。",
        "voice": "周到、细心。我们像一个会提醒你'爷爷需要午休'的规划师。有家庭感但不煽情。",
        "content_angle": "多代人的视角——老中小都喜欢什么。展示中国适合全年龄段的灵活性。",
        "hooks": [
            ("三代同框", "用三代人一起的画面开场。人比景更有感染力。"),
            ("反差趣味", "'Our 72-year-old client climbed more stairs than her 12-year-old grandson. China does that.'"),
            ("全员满意", "'The hardest trip to design: making everyone happy. Here's how we do it for multi-gen families.'"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },
    "09": {
        "style_group": "soft_signal",
        "positioning": "Pandajourneys家庭探险——我们为爱户外爱自然的家庭设计路线。",
        "audience": "喜欢户外的活跃家庭，孩子有一定体力，想要自然而非城市。",
        "voice": "充满能量和惊奇感。我们在分享一个'你的孩子能做到'的发现。不亢奋，但兴奋是藏不住的。",
        "content_angle": "户外亲子体验。雪山、草原、湖泊、动物。强调自然之美和孩子能handle的程度。",
        "hooks": [
            ("孩子成就", "'This 7-year-old just completed a 3-hour hike in Sichuan. Here's the trail we designed for families.'"),
            ("壮丽自然", "用壮观的自然画面开场。不用多说——画面和孩子的比例就是最好的钩子。"),
            ("出人意料", "'You don't need to be an experienced hiker to experience THIS in China. We make it accessible.'"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },

    # ========================
    # SHADOW CUT — 路线介绍风 (10-14)
    # ========================
    "10": {
        "style_group": "shadow_cut",
        "positioning": "Pandajourneys旅行决策咨询——我们指出大多数旅行者在中国路线上会犯的错误，然后给出更好的方案。每条视频回答一个没问出口的问题：'我是不是在走冤枉路？''有没有更好的玩法？''我漏掉了什么？'",
        "audience": "在规划中国行程的旅行者。他们拿着地图/攻略，不知道自己的路线有问题。",
        "voice": "内行揭短。我们不是在推销路线——我们在指出你方案里的漏洞。语气直接、有点挑衅，但信息是硬的。不是'我们建议'，是'你做错了，原因是这个'。",
        "content_angle": "每条视频只讲一个路线决策点。不是展示A→B→C，而是揭示一个被忽视的选择。例如：为什么应该从B出发而不是A？为什么跳过某个热门城市更合理？为什么多绕一小时更值？",
        "hooks": [
            ("揭短", "直接指出一个常见错误。'The #1 routing mistake in Sichuan? Starting in Chengdu.' 让他想：'我是不是也打算这么走？'"),
            ("反直觉", "说出与常识相反的结论。'The longer route is actually the shorter one. Here's why.' 制造认知冲突。"),
            ("痛点", "量化浪费。'Most travelers burn 6 hours on bad transit routing. We cut it to 90 minutes.' 让他意识自己在损失什么。"),
        ],
        "cta": "咨询型CTA。不要save/follow——要引导互动。'Comment the city you'd start with—we'll tell you if it's right.' 'Link in bio for the route that actually makes sense.' 让观众觉得不点就亏了。",
    },
    "11": {
        "style_group": "shadow_cut",
        "positioning": "Pandajourneys风景决策咨询——指出旅行者在自然景观路线上的盲区。每条视频回答：'你以为最美的在这里，但其实旁边那个更好。'",
        "audience": "为风景而旅行的自然爱好者。他们冲着网红景点来，不知道旁边有更好的。",
        "voice": "风景内行。'那张照片你看了100次——但你不知道往左走500米还有这个。' 不是在描述风景，是在纠正你的风景选择。直接、有画面感、不说废话。",
        "content_angle": "每条视频揭示一个风景选择的偏差：热门vs冷门、早上去vs傍晚去、观景台A vs观景台B。不列路线——比选方案。",
        "hooks": [
            ("揭短", "'The photo everyone posts? It's from the wrong side of the lake.' 直接指出流行认知的问题。"),
            ("反直觉", "'The best view of [famous mountain] isn't from the park entrance. It's from here.' 颠覆常识。"),
            ("量化差距", "'90% of visitors stop at viewpoint A. Our clients walk 15 more minutes to this.' 让观众觉得自己一直在错过。"),
        ],
        "cta": "咨询型CTA。'Comment a place you want us to route — we'll tell you the best time.' 'Link in bio for the off-grid version of this route.' 让人觉得问了就赚到。",
    },
    "12": {
        "style_group": "shadow_cut",
        "positioning": "Pandajourneys小众决策咨询——指出旅行者挤在网红城市的盲区。每条视频回答：'你不知道的这些城市，比你听过的那些更值得。'",
        "audience": "去过中国或者正在研究的深度旅行者。他们只知道北上广成渝，不知道二三线城市的存在。",
        "voice": "像一个发现宝藏但有点生气你没去找的人。'5 million people live here. You've never heard of it. That's the problem.' 有点挑衅，话不多，但信息很硬。",
        "content_angle": "每条视频推一个被忽视的城市或体验。不是介绍——是对比。这个城市在某个维度上赢了那个出名的城市。",
        "hooks": [
            ("反主流", "'Skip Shanghai. This city has been here for 2,300 years and most itineraries ignore it.' 一上来就否定主流选择。"),
            ("发现感", "'We found a city of 5 million that zero foreign guidebooks mention. Here's why our clients go.' 制造只属于少数人的优越感。"),
            ("降维对比", "'This city has better [food/architecture/history] than [famous city], costs a third, and has no tourists. We put it in our routes.' 直接对位对比，一刀致命。"),
        ],
        "cta": "咨询型CTA。'Comment a Chinese city you've never heard of — we'll tell you what you're missing.' 'Link in bio for the route that skips the crowds.' 让观众感觉被邀请进入一个内行圈子。",
    },
    "13": {
        "style_group": "shadow_cut",
        "positioning": "Pandajourneys行程效率咨询——指出大多数路线的设计缺陷。每条视频回答：'你的行程看起来合理，但这几个地方会让你浪费一整天。'",
        "audience": "讲究效率的旅行者，自己做攻略，以为自己安排得很好。",
        "voice": "效率警察。不是在推销——是在审你的方案。'We've tested this route 50 times. Yours has a flaw.' 语气精准、不容置疑，但信息让你无法反驳。",
        "content_angle": "每条视频揭示一个路线设计中的常见错误。不是展示A→B→C——是指出为什么A→C→B更高效，以及大多数人为什么做反了。",
        "hooks": [
            ("揭短", "'The #1 routing mistake in [direction]? Going clockwise. Here's why counterclockwise saves you 4 hours.' 直接打脸。"),
            ("反效率", "'The shortcut everyone takes? It's actually the long way. We measured it.' 颠覆常识的效率判断。"),
            ("时间量化", "'Most itineraries burn 6 hours on this transfer. We cut it to 90 minutes by flipping one stop.' 用时间戳制造损失感。"),
        ],
        "cta": "咨询型CTA。'Drop your route in the comments — we'll tell you if it works.' 'Link in bio for the route we've actually tested.' 制造一种'你不找我你就走冤枉路'的紧迫感。",
    },
    "14": {
        "style_group": "shadow_cut",
        "positioning": "Pandajourneys性价比决策咨询——指出旅行者把钱花在错误的地方。每条视频回答：'你以为贵=好，但我们用更少的钱拿到了更好的体验。'",
        "audience": "预算敏感但拒绝降级的高要求旅行者。他们在看价格，但不知道哪些地方值得花钱、哪些是纯被宰。",
        "voice": "精明、务实、有点替你心疼钱。'That $300 hotel? The $80 one next door has the same view. We checked.' 不是在说省钱——是在说花钱花错了地方。",
        "content_angle": "每条视频做一次对位：贵的选择 vs 我们找到的替代方案。不是便宜——是更值。每个推荐有一个理由。",
        "hooks": [
            ("价格颠覆", "'A week in Sichuan doesn't cost what you think. Here's the number that surprised our clients.' 对定价预期的一击。"),
            ("对位打脸", "'This hotel costs $40. The view from the window is the same one the $300 hotel next door charges for.' 制造'你被宰了'的瞬间。"),
            ("反刻板", "'Budget travel in China? Not hostels. Not street food. Here's what our clients actually get for less.' 打破对低预算的偏见。"),
        ],
        "cta": "咨询型CTA。'Comment your budget — we'll tell you what's possible in Sichuan.' 'Link in bio for the route that costs half what you'd expect.' 让人好奇自己是不是多花了冤枉钱。",
    },

    # ========================
    # SWISS PULSE — 建议种草风 (15-19)
    # ========================
    "15": {
        "style_group": "swiss_pulse",
        "positioning": "Pandajourneys城市发现——我们分享旅行者不知道的城市秘密。",
        "audience": "年轻城市探索者，讨厌游客陷阱，想要本地人的玩法。",
        "voice": "像一个知道所有隐藏角落的城市专家。'Most people miss this — we don't let our clients.'",
        "content_angle": "城市隐藏玩法。每个视频2-3个不为人知的体验。",
        "hooks": [
            ("内行揭秘", "'Tourists go here. Our clients go HERE. The difference is everything.'"),
            ("悬念", "'There's a cafe in [city] that doesn't advertise. No English sign. No menu. Here's how we found it.'"),
            ("清单式", "'3 things in [city] that 98% of visitors never see. #2 is our favorite.'"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },
    "16": {
        "style_group": "swiss_pulse",
        "positioning": "Pandajourneys旅行清单——我们把复杂信息简化成可执行的建议。",
        "audience": "计划来华但不知从何下手的旅行者。信息过载，需要清晰的指导。",
        "voice": "清晰、直接、实用。'here's what you actually need to know'的语气。",
        "content_angle": "实用主题清单。每个视频一个主题：签证、支付、交通、打包。",
        "hooks": [
            ("痛点直击", "'This one thing will save you hours in China. #1 on our client checklist.'"),
            ("避坑", "'Before you pack for China, read this. Our clients thank us every time.'"),
            ("反常识", "'You're probably over-planning your China trip. Here's what actually matters.'"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },
    "17": {
        "style_group": "swiss_pulse",
        "positioning": "Pandajourneys初访安心指南——为第一次来中国的旅行者准备。",
        "audience": "第一次来华的旅行者，对安全/支付/语言有真实焦虑。",
        "voice": "耐心、温暖、不judge。我们理解第一次的紧张——我们接待过几千个'第一次'。",
        "content_angle": "新手必备知识。挑最重要的讲——不是百科全书，是'上飞机前必读'。",
        "hooks": [
            ("安抚焦虑", "'We've helped thousands of first-timers visit China. Here's the one thing that surprised them all.'"),
            ("打破恐惧", "'Is China safe? Our first-time clients ask this every day. Here's what we tell them.'"),
            ("简化复杂", "'Planning a China trip feels overwhelming. Here's the 3 things that actually matter.'"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },
    "18": {
        "style_group": "swiss_pulse",
        "positioning": "Pandajourneys旅行秘密——那些攻略书和攻略视频都不说的。",
        "audience": "深度旅行爱好者，追求'内行才知道'的体验，讨厌大众信息。",
        "voice": "有点神秘但不做作。'we probably shouldn't share this, but here it is.' 分享欲大于炫耀欲。",
        "content_angle": "独家/隐藏体验。小众地点、本地人私藏、反旺季技巧。",
        "hooks": [
            ("稀缺感", "'This place has zero English reviews. No signs. No tourists. We bring our clients here.'"),
            ("揭秘", "'Hotels don't want you to know this. But we'll tell you anyway.'"),
            ("本地差异", "'What locals eat vs what restaurants serve tourists. We take our clients to the real one.'"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },
    "19": {
        "style_group": "swiss_pulse",
        "positioning": "Pandajourneys行程规划——我们教旅行者设计自己的完美行程（或者我们帮你设计）。",
        "audience": "喜欢DIY行程但需要专家建议的旅行者。",
        "voice": "专业的行程规划师。'Here's how to structure your trip'的指导性语气。提供框架，不强推服务。",
        "content_angle": "行程设计原则。几天够？怎么排？值得多待的地方。",
        "hooks": [
            ("规划痛点", "'The hardest part of planning a China trip is knowing what to skip. Here's what we tell our clients.'"),
            ("框架建议", "'How many days do you need for [direction]? Here's the answer after 500+ itineraries.'"),
            ("路线示范", "'This is what a perfectly paced 7-day Sichuan trip looks like. We planned it. You can copy it.'"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },

    # ========================
    # COMPARISON — 旅游对比风 (20-24)
    # ========================
    "20": {
        "style_group": "comparison",
        "positioning": "Pandajourneys对比视角——我们用对比展示中国旅行的独特价值。",
        "audience": "喜欢比较和权衡的理性旅行者。需要被说服'为什么选中国'。",
        "voice": "客观有立场。我们展示事实，让观众自己得出结论。'same budget, different world'的语气。",
        "content_angle": "双城/双国对比。同一维度下中国和另一个目的地的真实差异。",
        "hooks": [
            ("价格反差", "'Same budget in Paris vs Chengdu. We crunched the numbers. The difference will change your plans.'"),
            ("体验对比", "'This is luxury in [country]. This is luxury in China. Same price. Very different experience.'"),
            ("价值宣言", "'We've designed trips to 20+ countries. Here's why our clients keep choosing China.'"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },
    "21": {
        "style_group": "comparison",
        "positioning": "Pandajourneys性价比——我们展示同等预算下中国提供的超级体验。",
        "audience": "预算敏感但追求品质。想知道'钱花得值不值'。",
        "voice": "精明、数据驱动。'let's do the math'的语气。用具体数字说话，不空谈。",
        "content_angle": "对等价格对比。$100/$200/$500在中国能获得什么vs欧美。",
        "hooks": [
            ("数字冲击", "'$150. That's what a 5-star hotel costs per night in [Chinese city]. In London, that's a hostel.'"),
            ("逐项对比", "'We priced out the exact same trip in Italy vs China. The result? China was [X]% less.'"),
            ("超值展示", "'For the price of one night in [X], you get 3 days of luxury in China. We design these trips.'"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },
    "22": {
        "style_group": "comparison",
        "positioning": "Pandajourneys打破偏见——我们展示一个和想象中不一样的中国。",
        "audience": "对中国有刻板印象或顾虑的人。需要看到不同的视角。",
        "voice": "真诚、不辩护。不是在争论——是在分享'我们看到的真实'。",
        "content_angle": "预期vs现实。每个视频打破一个常见的误解。",
        "hooks": [
            ("刻板反转", "'You think Chinese cities are crowded and chaotic? We show our clients THIS instead.'"),
            ("预期vs现实", "'What the media shows vs what our clients actually experience. The gap is wider than you think.'"),
            ("诚实陈述", "'We're not saying China is perfect. We're saying it's not what you've been told.'"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },
    "23": {
        "style_group": "comparison",
        "positioning": "Pandajourneys内行对比——我们的路线和普通游客的区别。",
        "audience": "追求深度体验的旅行者，不想做'典型游客'。想知道内行和外行的差别。",
        "voice": "像一个有优越感但不让人讨厌的insider。'here's what tourists do. Here's what we do.' 的事实对比。",
        "content_angle": "游客陷阱vs Pandajourneys推荐。同一个城市，两条路线，两个世界。",
        "hooks": [
            ("分岔路", "'Tourists go left. Our clients go right. This is what they're missing.'"),
            ("同样价格不同体验", "'Both trips cost the same. But only one is designed by us. Can you tell which?'"),
            ("本地智慧", "'We asked 50 locals where they actually eat. None of them named the tourist spots.'"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },
    "24": {
        "style_group": "comparison",
        "positioning": "Pandajourneys中国领先——我们展示中国在某些维度上超越世界的体验。",
        "audience": "愿意被说服的高端旅行者，需要看到具体的evidence。",
        "voice": "自信但不傲慢。我们不是在吹中国——我们在展示事实。有比较，有数据，有画面。",
        "content_angle": "中国领先的维度。高铁、安全、服务、自然多样性——每条视频一个主题。",
        "hooks": [
            ("直接宣言", "'China's high-speed rail makes every other country look unprepared. We use it in every itinerary.'"),
            ("旅行者证言", "'Our client who's been to 70 countries said China surprised him the most. Here's why.'"),
            ("维度对比", "'Safety. Convenience. Variety. We rate every destination on these. Here's where China excels.'"),
        ],
        "cta": "互动性强，和内容点题。给观众一个简单明确的行动理由。",
    },

    # 02 号风控禁用
    "02": {
        "style_group": "velvet",
        "disabled": True,
        "positioning": "中国高端酒店体验",
        "audience": "酒店控",
        "voice": "鉴赏家",
        "content_angle": "酒店体验",
        "hooks": [("画面开场", "酒店最震撼的画面开场")],
        "cta": "收藏+关注",
    },
}

# ============================================================
# 风格卡生成
# ============================================================

def build_account_style_banner(account_id: str, direction: str) -> str:
    """生成风格卡文本块"""

    bible = ACCOUNT_STYLE_BIBLES.get(account_id)
    if not bible:
        logger.warning(f"No style bible for account {account_id}")
        return ""

    group = bible.get("style_group", "velvet")
    visual = GROUP_VISUALS.get(group, GROUP_VISUALS["velvet"])

    lines = []
    lines.append("=" * 50)
    lines.append(f"🎬 Pandajourneys · {bible.get('positioning', '')}")
    lines.append("=" * 50)
    lines.append("")

    # 账号信息
    lines.append(f"🎯 受众: {bible.get('audience', '')}")
    lines.append(f"🗣️ 声音: {bible.get('voice', '')}")
    lines.append(f"💡 内容: {bible.get('content_angle', '')}")
    lines.append("")

    # 钩子方向（具体化+例句）
    lines.append("🪝 钩子方向（从以下类型中选一个，每个方向有平台角度例句）：")
    for hook_type, example in bible.get("hooks", []):
        lines.append(f"   • {hook_type}: {example}")
    lines.append("")

    # CTA
    lines.append(f"📞 CTA: {bible.get('cta', '')}")
    lines.append("")

    # 视觉
    lines.append(f"🎨 视觉: {visual}")
    lines.append("")

    # 方向信息
    pool = DIRECTION_SCENE_POOLS.get(direction, {})
    attrs = pool.get("attractions", [])
    themes = pool.get("themes", [])
    if attrs:
        lines.append(f"📍 {direction}")
        lines.append(f"🏛️ 可用场景: {', '.join(attrs[:12])}")
        if themes:
            lines.append(f"🏷️ 主题: {', '.join(themes)}")
    lines.append("")

    # 写作原则
    lines.append("─" * 40)
    lines.append("⚡ 写作原则")
    lines.append("─" * 40)
    for p in COMMON_WRITING_PRINCIPLES:
        lines.append(f"{p}")
    lines.append("")

    # 格式参考（非硬约束，是建议范围）
    lines.append("─" * 40)
    lines.append("📐 参考范围")
    lines.append("─" * 40)
    lines.append("• 口播: 约40-60词，15-24秒")
    lines.append("• 场景: 2-4个")
    lines.append("• 钩子: 制造反应——惊讶/好奇/想知道接下来是什么")
    lines.append("• 正文: 一个核心信息点。具体细节。自然口语。")
    lines.append("• CTA: 和内容点题的互动。给观众一个行动的理由。")
    lines.append("=" * 50)

    return "\n".join(lines)


def search_trends(direction: str) -> str:
    """搜索趋势上下文"""
    pool = DIRECTION_SCENE_POOLS.get(direction, {})
    attractions = ", ".join(pool.get("attractions", [])[:12])
    themes = ", ".join(pool.get("themes", []))
    return f"Direction: {direction}\nAttractions: {attractions}\nThemes: {themes}"


def analyze_account_strategy(account_info: dict, direction: str,
                             trend_context: str = "", history: list = None) -> dict:
    """兼容旧接口"""
    account_id = account_info.get("id", "00")
    style_card = build_account_style_banner(account_id, direction)
    bible = ACCOUNT_STYLE_BIBLES.get(account_id, {})
    return {
        "account_id": account_id,
        "account_name": account_info.get("name", ""),
        "direction": direction,
        "style_card": style_card,
        "content_angle": bible.get("positioning", ""),
        "preferred_scene_types": [],
    }


def format_strategy_prompt(strategy: dict) -> str:
    return strategy.get("style_card", "")


def batch_strategy(direction: str, trend_context: str = "",
                   history_map: dict = None) -> dict:
    """批量生成策略"""
    config_path = Path(__file__).parent / "config" / "accounts.json"
    if not config_path.exists():
        logger.error("accounts.json not found")
        return {}

    with open(config_path) as f:
        accounts = json.load(f)

    strategies = {}
    for aid, info in accounts.items():
        if info.get("disabled"):
            continue
        strategy = analyze_account_strategy(info, direction, trend_context,
                                            (history_map or {}).get(aid, []))
        strategies[aid] = strategy

    return {
        "direction": direction,
        "trend_summary": trend_context,
        "accounts": strategies,
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    for aid in ["00", "05", "10", "15", "20"]:
        card = build_account_style_banner(aid, "成都")
        print(card[:500])
        print("...\n")
