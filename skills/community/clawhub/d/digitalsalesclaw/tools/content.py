#!/usr/bin/env python3
"""
DigitalSalesClaw - content.py
内容创作 + 钩子生成 + 内容优化（优化版）

优化内容：
- batch_generate 循环内 import → 模块级 import + 合规工具调用
- 钩子库：每风格扩展至 ≥20 条，支持 topic/platform 索引
- 相似度检测：避免连续生成高度相似内容

输入: {"action": "create|hook|optimize|analyze_performance|batch", ...}
输出: {"action, result, content, suggestions}
"""

import sys
import json
import random
from pathlib import Path
from datetime import datetime
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent

# ─────────────────────────────────────────
# 钩子风格定义（5种）
# ─────────────────────────────────────────
HOOK_STYLES = {
    "提问式": "通过提出直击痛点的问题吸引注意力，引发用户思考和互动",
    "故事式": "通过讲述真实或虚构的故事场景，拉近与用户的距离",
    "数据式": "通过震撼的数据或研究发现建立权威性",
    "对比式": "通过对比揭示差异，激发用户好奇心",
    "情绪式": "通过强烈的情绪共鸣，让用户感同身受",
}

# ─────────────────────────────────────────
# 钩子库（每风格 ≥20 条，支持 topic 变量）
# 全部使用 {topic} 作为占位符，运行时替换
# ─────────────────────────────────────────
HOOK_LIBRARY = {
    "提问式": [
        "你知道{topic}的真相是什么吗？大多数人都错了！",
        "为什么你{topic}总是效果不好？问题出在这里→",
        "{topic}到底听谁的？专家和医生说的竟然不一样！",
        "关于{topic}，90%的人都在犯同一个错误！",
        "发现一个关于{topic}的惊天秘密，看完沉默了……",
        "{topic}这件事，90%的医生都不会告诉你！",
        "为什么{topic}越来越普遍？答案在这里",
        "关于{topic}，这是我见过最实用的建议",
        "出现{topic}症状怎么办？三甲医院主任这样说",
        "{topic}会遗传吗？最新研究给出了答案",
        "如果{topic}，一定要看！能救命！",
        "{topic}最怕什么？医生终于说出了真相",
        "关于{topic}，网上那些说法到底哪个是真的？",
        "为什么偏偏是你{topic}？看完终于明白了",
        "{topic}怎么判断？出现这些信号要注意",
        "关于{topic}的误区，90%的人都踩过",
        "一文读懂{topic}，建议收藏！",
        "{topic}和饮食的关系，绝大多数人不知道",
        "出现{topic}症状？别慌，先做这件事",
        "关于{topic}，这篇文章说得太清楚了",
        "同样是{topic}，为什么有人恢复快？",
        "{topic}反复发作？可能是这个原因",
    ],
    "故事式": [
        "昨天遇到一个患者，{topic}的问题让他后悔不已……",
        "我见过最严重的{topic}案例，教训太深刻了",
        "一个关于{topic}的真实故事，看完你会有所触动",
        "邻居张阿姨的{topic}经历，震惊了整个小区",
        "一个{topic}患者的自述：我差点错过了最佳治疗时机",
        "发生在医院里的真实故事，关于{topic}的教训",
        "三年前的一场误诊，让我对{topic}有了全新认识",
        "一位退休老医生的{topic}经历，看完沉默了",
        "这是我追踪了5年的{topic}患者，现在状态令人惊讶",
        "同事的真实经历：{topic}差点毁了他的生活",
        "一个关于{topic}的急救故事，结局出人意料",
        "婆婆的{topic}经历，婆媳关系因此改变",
        "一个{topic}患者的独白：那段日子太难熬了",
        "我身边最严重的{topic}案例，教训太深刻",
        "朋友的{topic}经历告诉我：这件事不能拖",
        "一位宝妈的{topic}经历，说出了无数妈妈的心声",
        "爷爷的{topic}故事，让我重新认识了这种疾病",
        "病房里真实的一幕，关于{topic}的生死抉择",
        "大学教授的{topic}经历，引发了整个学术界的讨论",
        "一个让人心疼的{topic}故事，转给身边人",
        "同事被{topic}折磨了三年，根源竟是……",
        "这是我听过最令人震惊的{topic}案例",
    ],
    "数据式": [
        "最新研究：90%的人对{topic}存在严重误解！",
        "数据说话了：关于{topic}，你必须知道的3个真相",
        "{topic}的最新数据曝光，数字触目惊心！",
        "震惊！最新研究显示{topic}发病率又创新高",
        "国家疾控中心最新数据：关于{topic}的真相",
        "最新调查：每5个{topic}患者中就有1个因此失业",
        "数据揭秘：关于{topic}，医生不会告诉你的10个秘密",
        "研究证明：{topic}与这个日常习惯高度相关",
        "最新研究数据：{topic}正在年轻化！",
        "WHO最新报告：全球{topic}患者已超过这个数字",
        "临床数据：{topic}患者的平均确诊时间让人意外",
        "大数据分析：{topic}最高发的季节终于找到了",
        "最新研究：控制{topic}只需要做好这件事",
        "一组关于{topic}的可怕数据，揭示了残酷真相",
        "医学期刊最新研究：关于{topic}的三大误区",
        "最新调查：超过50%的{topic}患者曾被误诊",
        "数据不会骗人：{topic}的真相令人警醒",
        "研究证实：{topic}与这个指标密切相关",
        "最新研究显示：做好这件事，{topic}风险降低80%",
        "CDC最新报告：关于{topic}的10个惊人事实",
        "临床数据证明：{topic}患者最常见的共同点",
        "医学研究重大发现：关于{topic}的新机制",
    ],
    "对比式": [
        "左边是错的，右边是对的！关于{topic}，一次说清楚",
        "普通人 vs 专业人士处理{topic}的区别，惊了！",
        "同样{topic}，为什么差距这么大？",
        "两代人的{topic}观念对比，完全不一样！",
        "有钱人和穷人的{topic}管理，差别太大了",
        "治疗{topic}：中医 vs 西医，哪个更靠谱？",
        "同一个{topic}，三甲医院和社区医院的处理差别",
        "关于{topic}：有人好了有人没好，区别在这",
        "前后对比：坚持做这件事的{topic}患者vs没做的",
        "协和 vs 普通医院：关于{topic}的正确做法",
        "关于{topic}，医生和患者的想法差距太大了",
        "有症状 vs 没症状：{topic}患者的真实对比",
        "老年人的{topic}观念vs年轻人的，结果很意外",
        "关于{topic}：三甲医院主任 vs 社区医生说法对比",
        "治疗前 vs 治疗后：{topic}的真实对比",
        "关于{topic}，这5个习惯决定了好与坏的差距",
        "城市 vs 农村：{topic}患者的认知差异有多大",
        "30岁 vs 50岁的{topic}管理，差别太大了",
        "懂医的人 vs 不懂医的人，处理{topic}有何不同",
        "关于{topic}：这三件事，做好了完全不一样",
        "保守治疗 vs 积极干预：{topic}患者的十年跟踪对比",
        "关于{topic}，这些误区99%的人都踩过",
    ],
    "情绪式": [
        "因为{topic}，我差点失去了最重要的人……",
        "崩溃！{topic}这个问题，困扰了我整整三年",
        "为什么没人早点告诉我这些？关于{topic}的血泪经验",
        "得了{topic}之后，我差点离婚……",
        "家人们，谁懂啊！{topic}这件事太折磨人了",
        "深夜emo：因为{topic}，我患上了焦虑症",
        "{topic}毁了我的婚礼，这个教训太深刻了",
        "哭死！关于{topic}，这些苦真的没人能理解",
        "被{topic}折磨了5年，终于找对方法控制了！",
        "因为我的无知，差点害了孩子！关于{topic}的教训",
        "确诊{topic}的那天，我感觉天都塌了",
        "关于{topic}，这是我人生中最黑暗的一段时光",
        "曾经因为{topic}自卑到不敢出门，现在终于走出来了",
        "崩溃边缘！{topic}反复发作，我已经绝望了",
        "亲历{topic}：那段时间，我差点放弃了自己",
        "写给所有{topic}患者：别放弃希望！",
        "因为{topic}，我辞掉了工作全职照顾家人",
        "太真实了！{topic}患者的心理状态，说出了心声",
        "{topic}患者家属的自白：太累了，但不能倒下",
        "关于{topic}，这些崩溃的瞬间你经历过吗？",
        "一位{topic}患者母亲的自述：看着孩子难受太心疼了",
        "如果你也经历过{topic}的低谷，这句话送给你",
    ],
}

# 确保每风格至少20条
for style, hooks in HOOK_LIBRARY.items():
    assert len(hooks) >= 20, f"风格「{style}」钩子数量不足20条"


# ─────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────

def get_time_context() -> dict:
    now = datetime.now()
    return {
        "current_date": now.strftime("%Y-%m-%d"),
        "current_month": now.strftime("%Y-%m"),
        "day_of_week": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][now.weekday()],
        "time_slot": f"{now.hour}:00-{now.hour+1}:00"
    }


def get_similarity_score(text1: str, text2: str) -> float:
    """简单词重叠相似度（0.0-1.0）"""
    if not text1 or not text2:
        return 0.0
    words1 = set(text1.replace("{topic}", "").split())
    words2 = set(text2.replace("{topic}", "").split())
    if not words1 or not words2:
        return 0.0
    intersection = words1 & words2
    union = words1 | words2
    return len(intersection) / len(union)


def generate_hook(topic: str, style: str = None, platform: str = "douyin",
                   recent_hooks: list[str] = None) -> dict:
    """
    生成开头钩子（支持相似度过滤）
    recent_hooks: 近期已生成的钩子列表，用于避免重复
    """
    if style is None:
        style = random.choice(list(HOOK_STYLES.keys()))

    library = HOOK_LIBRARY.get(style, HOOK_LIBRARY["提问式"])

    # 相似度过滤：如果候选钩子与近期钩子太相似，跳过
    candidates = library
    if recent_hooks:
        filtered = []
        for hook in candidates:
            too_similar = any(get_similarity_score(hook, recent) > 0.6
                             for recent in recent_hooks)
            if not too_similar:
                filtered.append(hook)
        if filtered:
            candidates = filtered

    # 随机选一条
    hook_template = random.choice(candidates)
    hook = hook_template.replace("{topic}", topic)

    return {
        "style": style,
        "hook": hook,
        "platform": platform,
        "usage_tip": HOOK_STYLES.get(style, ""),
        "suitable_for": f"{platform} 平台，前3秒/开头使用"
    }


def _get_db_conn():
    """获取数据库连接（MySQL 优先）"""
    try:
        import mysql.connector
        from mysql.connector import pooling
        pool = pooling.MySQLConnectionPool(
            host="localhost", port=3306, user="ontology", unix_socket="/tmp/mysql.sock",
            password="ontology", database="digitalsalesclaw",
            pool_name="dsc_content", pool_size=3, charset="utf8mb4"
        )
        conn = pool.get_connection()
        conn.autocommit = False
        return conn, False
    except Exception:
        conn = get_conn()
        return conn, True


def _call_compliance_tool(content: str) -> dict:
    """
    调用合规审核工具（替代直接 import compliance 模块）
    通过 subprocess 调用 digitalsalesclaw_compliance 工具
    """
    import subprocess, json

    tool_path = Path(__file__).parent / "compliance.py"
    params = {"action": "review", "content": content}

    try:
        result = subprocess.run(
            ["python3", str(tool_path)],
            input=json.dumps(params),
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(Path(__file__).parent),
        )
        if result.returncode == 0:
            try:
                output_lines = result.stdout.strip().split("\n")
                return json.loads(output_lines[-1])
            except json.JSONDecodeError:
                pass
    except Exception:
        pass

    return {"error": "compliance tool unavailable"}


def generate_content(topic: str, platform: str = "douyin", conn=None, ) -> dict:
    """生成完整内容脚本"""
    template = PLATFORM_TEMPLATES.get(platform, PLATFORM_TEMPLATES["douyin"])
    tc = get_time_context()

    related = []
    if conn:
        try:
            if is_sqlite:
                rows = conn.execute("""
                    SELECT topic, platform, status FROM content_topics
                    WHERE topic LIKE ? AND status = 'approved'
                    LIMIT 5
                """, (f"%{topic[:4]}%",)).fetchall()
            else:
                rows = conn.execute("""
                    SELECT topic, platform, status FROM content_topics
                    WHERE topic LIKE %s AND status = 'approved'
                    LIMIT 5
                """, (f"%{topic[:4]}%",)).fetchall()
            related = [r[0] for r in rows]
        except Exception:
            pass

    style_map = {"douyin": "提问式", "xiaohongshu": "情绪式", "wechat": "数据式"}
    hook_style = style_map.get(platform, "提问式")
    hook_text = generate_hook(topic, hook_style, platform)["hook"]

    if platform == "douyin":
        script = _build_douyin_script(topic, hook_text, tc)
    elif platform == "xiaohongshu":
        script = _build_xiaohongshu_script(topic, hook_text, tc)
    else:
        script = _build_wechat_script(topic, hook_text, tc)

    # 保存到数据库
    topic_id = None
    script_id = None
    if conn:
        try:
            now = datetime.now().isoformat()
            if is_sqlite:
                cursor = conn.execute("""
                    INSERT INTO content_topics (topic, platform, status, priority, created_at, updated_at)
                    VALUES (?, ?, 'approved', 'high', ?, ?)
                """, (topic, platform, now, now))
            else:
                cursor = conn.execute("""
                    INSERT INTO content_topics (topic, platform, status, priority, created_at, updated_at)
                    VALUES (%s, %s, 'approved', 'high', %s, %s)
                """, (topic, platform, now, now))
            topic_id = cursor.lastrowid
            conn.commit()

            fmt = "video" if platform == "douyin" else "article"
            if is_sqlite:
                cursor2 = conn.execute("""
                    INSERT INTO content_scripts (topic_id, title, content, platform, format, status, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, 'draft', ?, ?)
                """, (topic_id, f"{topic} - {platform}", script, platform, fmt, now, now))
            else:
                cursor2 = conn.execute("""
                    INSERT INTO content_scripts (topic_id, title, content, platform, format, status, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, 'draft', %s, %s)
                """, (topic_id, f"{topic} - {platform}", script, platform, fmt, now, now))
            script_id = cursor2.lastrowid
            conn.commit()
        except Exception:
            pass

    return {
        "topic": topic,
        "platform": platform,
        "script": script,
        "topic_id": topic_id,
        "script_id": script_id,
        "format": template["format"],
        "estimated_length": template["length"],
        "structure": template["structure"],
        "tips": template["tips"],
        "publish_suggestion": f"建议在{tc['day_of_week']} {tc['time_slot']}发布"
    }


def _build_douyin_script(topic: str, hook_text: str, tc: dict) -> str:
    return f"""【短视频脚本 | {tc['current_date']}】

🎬 开场钩子（前3秒）：
{hook_text}

📌 痛点引入（10秒）：
- {topic}是很多人都会遇到的问题
- 但网上信息太杂，不知道该信哪个
- 今天一次给你讲清楚

💡 核心内容（30秒）：
1. 关于{topic}的正确认知
2. 常见的3个误区
3. 正确的处理方法

🎯 行动号召（5秒）：
- 觉得有用就点个赞
- 关注我，每天分享实用的健康知识
- 有问题评论区见

---
📝 发布建议：
- 发布时间：{tc['day_of_week']} {tc['time_slot']}
- 添加标签：#{topic} #健康科普 #医药
- 前3秒必须说完开场钩子再切入正题
"""


def _build_xiaohongshu_script(topic: str, hook_text: str, tc: dict) -> str:
    return f"""【小红书图文笔记 | {tc['current_date']}】

📌 封面标题：
关于{topic}，这件事没人告诉你

💬 开头引导：
{hook_text}
（以下是纯干货，建议收藏）

📖 正文：
【什么是{topic}】
{topic}是...

【为什么重要】
1. ...
2. ...
3. ...

【正确做法】
✅ 步骤1：...
✅ 步骤2：...
✅ 步骤3：...

【常见问题Q&A】
Q: ...
A: ...

👏 结尾互动：
你关于{topic}有什么经历？欢迎评论区分享！
❤️ 如果有用记得收藏
"""


def _build_wechat_script(topic: str, hook_text: str, tc: dict) -> str:
    return f"""【微信公众号推文 | {tc['current_date']}】

📌 标题：
{hook_text}

💬 导语：
今天我们来聊聊{topic}这个话题。根据最新数据，很多人都存在认知偏差...

📖 正文：

一、{topic}的基本概念
...

二、关于{topic}的3个真相
1. ...
2. ...
3. ...

三、正确应对{topic}的方法
...

四、常见问题解答
...

📣 结尾：
如果觉得有用，欢迎转发给身边的朋友！
点击在看，让更多人看到
"""


PLATFORM_TEMPLATES = {
    "douyin": {
        "format": "短视频脚本",
        "length": "30-60秒",
        "structure": "开头钩子(3秒) → 痛点引入(10秒) → 解决方案(30秒) → 行动号召(5秒)",
        "tips": "前3秒必须有强钩子，语言口语化，多用祈使句"
    },
    "xiaohongshu": {
        "format": "图文笔记",
        "length": "300-800字",
        "structure": "封面标题(吸引眼球) → 开头(痛点共鸣) → 主体(实用干货) → 结尾(互动引导)",
        "tips": "标题要有悬念或数字，多用emoji，结尾引导评论"
    },
    "wechat": {
        "format": "微信公众号推文",
        "length": "1000-2000字",
        "structure": "标题(蹭热点或痛点) → 导语(引发共鸣) → 正文(逻辑清晰) → 结尾(转发引导)",
        "tips": "标题决定打开率，内容要有信息增量，结尾要有转发动力"
    }
}


def analyze_performance(content_id: str = None, conn=None, ) -> dict:
    """分析内容效果"""
    own_conn = False
    if conn is None:
        conn, is_sqlite = _get_db_conn()
        own_conn = True

    try:
        if content_id:
            if is_sqlite:
                m = conn.execute("""
                    SELECT cm.*, cc.name as campaign_name
                    FROM content_metrics cm
                    JOIN content_campaigns cc ON cc.id = cm.campaign_id
                    WHERE cm.id = ?
                """, (content_id,)).fetchone()
            else:
                m = conn.execute("""
                    SELECT cm.*, cc.name as campaign_name
                    FROM content_metrics cm
                    JOIN content_campaigns cc ON cc.id = cm.campaign_id
                    WHERE cm.id = %s
                """, (content_id,)).fetchone()

            if not m:
                return {"error": f"Content {content_id} not found"}
            cols = [d[0] for d in conn.execute("SELECT * FROM content_metrics LIMIT 0").description]
            m = dict(zip(cols, m))
        else:
            date_filter = "date('now', '-30 days')" if is_sqlite else "DATE_SUB(NOW(), INTERVAL 30 DAY)"
            if is_sqlite:
                agg = conn.execute(f"""
                    SELECT
                        COUNT(DISTINCT campaign_id) as campaign_count,
                        SUM(impressions) as total_impressions,
                        SUM(clicks) as total_clicks,
                        SUM(conversions) as total_conversions,
                        SUM(spend) as total_spend,
                        AVG(engagement_rate) as avg_engagement,
                        AVG(ctr) as avg_ctr
                    FROM content_metrics
                    WHERE date >= date({date_filter})
                """).fetchone()
            else:
                agg = conn.execute(f"""
                    SELECT
                        COUNT(DISTINCT campaign_id) as campaign_count,
                        SUM(impressions) as total_impressions,
                        SUM(clicks) as total_clicks,
                        SUM(conversions) as total_conversions,
                        SUM(spend) as total_spend,
                        AVG(engagement_rate) as avg_engagement,
                        AVG(ctr) as avg_ctr
                    FROM content_metrics
                    WHERE date >= {date_filter}
                """).fetchone()
            cols = [d[0] for d in conn.execute("SELECT * FROM content_metrics LIMIT 0").description]
            m = dict(zip(cols, agg))

        impressions = m.get("total_impressions") or m.get("impressions") or 0
        clicks = m.get("total_clicks") or m.get("clicks") or 0
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        eng_rate = m.get("avg_engagement") or m.get("engagement_rate") or 0

        if ctr >= 5 and eng_rate >= 3:
            rating, rating_text = "excellent", "优秀"
        elif ctr >= 2 and eng_rate >= 1:
            rating, rating_text = "good", "良好"
        elif ctr >= 1:
            rating, rating_text = "average", "一般"
        else:
            rating, rating_text = "poor", "需优化"

        suggestions = []
        if ctr < 2:
            suggestions.append("CTR偏低，建议优化开头钩子")
        if eng_rate < 1:
            suggestions.append("互动率低，建议增加互动引导")
        if not suggestions:
            suggestions.append("整体表现良好，可继续沿用当前策略")

        return {
            "impressions": impressions,
            "clicks": clicks,
            "ctr": round(ctr, 2),
            "engagement_rate": round(eng_rate, 2) if isinstance(eng_rate, float) else eng_rate,
            "rating": rating,
            "rating_text": rating_text,
            "suggestions": suggestions
        }
    finally:
        if own_conn:
            conn.close()


# ─────────────────────────────────────────
# 批量生成流水线（已修复：模块级 import + 合规工具调用）
# ─────────────────────────────────────────

def batch_generate(topics: list[str], platform: str = "douyin",
                   auto_compliance: bool = True, conn=None, ) -> dict:
    """
    批量内容生成流水线：选题 → 创作 → 合规审核（可选）

    优化点：
    - 合规审核通过 subprocess 调用 compliance.py 工具（不直接 import）
    - 支持 MySQL/SQLite 双引擎
    """
    pipeline_id = f"PIP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    results = []

    own_conn = False
    if conn is None:
        conn, is_sqlite = _get_db_conn()
        own_conn = True

    # 追踪近期钩子，用于相似度过滤
    recent_hooks = []

    try:
        for i, topic in enumerate(topics):
            item = {
                "step": i + 1,
                "topic": topic,
                "platform": platform,
                "status": "pending",
                "script": None,
                "compliance_check": None,
                "errors": [],
            }

            try:
                # Step 1: 创作（传入近期钩子列表用于相似度过滤）
                hook_result = generate_hook(topic, None, platform, recent_hooks)
                if recent_hooks is not None:
                    recent_hooks.append(hook_result["hook"])

                script_result = generate_content(topic, platform, conn)
                item["script"] = script_result.get("script", "")[:200] + "..."
                item["script_id"] = script_result.get("script_id")
                item["topic_id"] = script_result.get("topic_id")
                item["status"] = "script_created"

                # Step 2: 合规审核（通过工具调用，不直接 import）
                if auto_compliance and item["script"]:
                    compliance_result = _call_compliance_tool(
                        script_result.get("script", ""), conn, is_sqlite
                    )
                    item["compliance_check"] = {
                        "risk_level": compliance_result.get("risk_level"),
                        "violations": compliance_result.get("violations_count", 0),
                        "compliance_score": compliance_result.get("score"),
                        "passed": compliance_result.get("level") in ("pass", "warning"),
                    }
                    item["status"] = "compliance_checked"

                # Step 3: 更新 topic 状态
                if item.get("topic_id"):
                    new_status = ("approved"
                                 if not auto_compliance
                                 or item.get("compliance_check", {}).get("passed")
                                 else "pending")
                    if is_sqlite:
                        conn.execute("UPDATE content_topics SET status = ? WHERE id = ?",
                                     (new_status, item["topic_id"]))
                    else:
                        conn.execute("UPDATE content_topics SET status = %s WHERE id = %s",
                                     (new_status, item["topic_id"]))
                    conn.commit()

            except Exception as e:
                item["status"] = "failed"
                item["errors"].append(str(e))

            results.append(item)

        passed = len([r for r in results if r["status"] in ("script_created", "compliance_checked")])
        compliance_passed = len([r for r in results if r.get("compliance_check", {}).get("passed")])

        return {
            "pipeline_id": pipeline_id,
            "total_topics": len(topics),
            "created": passed,
            "compliance_passed": compliance_passed,
            "failed": len(topics) - passed,
            "platform": platform,
            "items": results,
            "suggestions": [
                f"批量生成完成：{passed}/{len(topics)} 条内容已创建",
                f"合规审核通过：{compliance_passed}/{passed} 条",
                "可使用 compliance 工具对未通过内容进行修改"
            ]
        }
    finally:
        if own_conn:
            conn.close()


def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {"action": "create", "topic": sys.argv[1]}
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {"action": "create", "topic": data}
    return {}


if __name__ == "__main__":
    args = _parse_args()
    action = args.get("action", "create")
    topic = args.get("topic", "健康科普")
    platform = args.get("platform", "douyin")
    content_id = args.get("content_id")

    conn, is_sqlite = _get_db_conn()

    try:
        if action == "hook":
            result = generate_hook(topic, args.get("style"), platform,
                                  args.get("recent_hooks"))
        elif action == "optimize":
            result = analyze_performance(content_id, conn)
            if "error" not in result:
                result["topic"] = topic
                result["platform"] = platform
        elif action == "analyze_performance":
            result = analyze_performance(content_id, conn)
        elif action == "batch":
            topics = args.get("topics", [topic])
            result = batch_generate(topics, platform,
                                     args.get("auto_compliance", True),
                                     conn)
        else:
            result = generate_content(topic, platform, conn)
    finally:
        close_conn(conn)

    print(json.dumps(result, ensure_ascii=False, indent=2))
