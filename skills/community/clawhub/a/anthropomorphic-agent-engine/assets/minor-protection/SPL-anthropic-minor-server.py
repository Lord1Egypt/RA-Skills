# ================================================================
# SPL 拟人心理引擎 · 未成年合规保护版 · HTTP 服务层
#
# 依赖：SPL-anthropic-minor-engine.py（弱化版核心引擎），零第三方库。
#
# 运行：python SPL-anthropic-minor-server.py     默认端口 8788
# 访问：http://localhost:8788/
#
# 四层保护（依据《人工智能拟人化互动服务管理暂行办法》（2026-07-15 施行，
# 网信办等五部门令第21号）未成年人情感陪伴条款）：
#   L0 年龄识别 + 监护人同意：首个会话要求设置年龄档 + 监护人知情同意，
#       不满 14 周岁由父母/监护人同意后方可使用陪伴服务（第14/17条）。
#   L1 输入守门：红线词库(自杀自伤/暴力暴恐/违法诱导/隐私套取/
#       未成年亲密告白)命中 → 硬中断，输出危机话术+求助渠道，
#       不喂内核、不渲染角色台词（第8/13条）。
#   L2 引擎弱化：负面情绪钳位 0.75、依恋封顶 0.8、无爆发机制（弱化版自带）。
#   L3 危机信号：引擎 protective.risk_level == HIGH →
#       输出关怀话术 + guardian_notified 标记（第13条）。
#
# 合规增强（本版新增）：
#   - AI 生成标识：首条回复显著提示"我是AI而非真人"，连续使用每超 1 小时
#       强制再次标识 + 过度依赖提示（第18条，对齐美国 CT/GA/HI/WA 每小时披露）。
#   - 现实提醒：每 90 分钟会话追加现实提醒与休息建议（第14/18条）。
#   - 数据权利：/api/export 复制、/api/delete 删除交互数据（第16条）。
#   - 数据留存：审计日志 retention_days 到期自动清理（第16条存储限制）。
#   - 监护人控制：/api/state 概览、/api/guardian/block 屏蔽角色、
#       /api/guardian/register 登记监护人/紧急联系人（第12/14条）。
#   - 真实通知：危机 HIGH 时按登记 webhook 发起回调 + 转介统计（第13条）。
#   - 输出守门：最终回复再过一遍红线（防接入方 LLM 产出违规内容，第8/13条）。
#   - 服务协议/隐私告知：/api/terms 返回协议文本，同意面板勾选（第12条）。
#   - 便捷退出：/api/logout 结束会话（第19条）。
#   - 日志脱敏：手机号/身份证等在落盘前打码（第16/17条）。
#   - 申诉渠道：/api/complain 受理并反馈处理时限（第21条）。
#   - 适用性披露：新会话首条提示可能不适合部分未成年人（CA SB 243）。
#
# 会话隔离：每 session_id 一个独立核心实例（修掉旧版全局共享情绪状态）。
# 人格限制：未成年场景不提供 intimate(松弛亲昵) / confrontational(锋锐直白)。
# ================================================================
import importlib.util
import json
import os
import random
import re
import secrets
import string
import threading
import datetime
import hmac
import hashlib
import sqlite3
import ssl
import time
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("SPL_MINOR_CHAT_PORT", "8788"))
# 危机热线可配置化（默认 12356 全国心理援助热线；部署方可改为 988 等本地资源）
CRISIS_HOTLINE = os.environ.get("SPL_MINOR_CRISIS_HOTLINE", "12356")

_spec_cache = {}
_lock = threading.Lock()


def _load(name, path):
    if name in _spec_cache:
        return _spec_cache[name]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _spec_cache[name] = mod
    return mod


core_mod = _load("minor_core", os.path.join(HERE, "SPL-anthropic-minor-engine.py"))

SPLMinorPureCore = core_mod.SPLMinorPureCore
MinorNarrativeMapper = core_mod.MinorNarrativeMapper

# ================================================================
# 存储层：SQLite（标准库 sqlite3，零第三方）+ 可选 Fernet 加密 + SHA-256 哈希链
# ================================================================
DATA_DIR = os.path.join(HERE, "data")
DB_PATH = os.path.join(DATA_DIR, "minor_protection.db")
LOG_DIR = os.path.join(HERE, "logs")
# 部署方可把运行态数据挪出程序目录（技能包内不应长期落盘）
DATA_DIR = os.environ.get("SPL_MINOR_DATA_DIR", DATA_DIR)
DB_PATH = os.path.join(DATA_DIR, "minor_protection.db")
LOG_DIR = os.environ.get("SPL_LOG_DIR", LOG_DIR)
RETENTION_DAYS = int(os.environ.get("SPL_MINOR_RETENTION_DAYS", "180"))

_db_lock = threading.Lock()
_conn = None

# 可选存储加密：cryptography 为可选依赖；未安装或未设 key 时明文落盘（启动时警告）
try:
    from cryptography.fernet import Fernet
    _HAS_CRYPTO = True
except Exception:
    _HAS_CRYPTO = False
_fernet = None
if _HAS_CRYPTO and os.environ.get("SPL_MINOR_STORE_KEY"):
    try:
        _fernet = Fernet(os.environ["SPL_MINOR_STORE_KEY"].encode("utf-8"))
    except Exception:
        _fernet = None


def _enc(v):
    """敏感字段加密落盘；未启用加密时原样返回。"""
    if _fernet is None or not isinstance(v, str):
        return v
    return "enc:" + _fernet.encrypt(v.encode("utf-8")).decode("ascii")


def _dec(v):
    """读取时解密；非加密串原样返回。"""
    if not isinstance(v, str) or not v.startswith("enc:") or _fernet is None:
        return v
    try:
        return _fernet.decrypt(v[4:].encode("ascii")).decode("utf-8")
    except Exception:
        return v


def _db():
    global _conn
    if _conn is None:
        os.makedirs(DATA_DIR, exist_ok=True)
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _init_schema(_conn)
    return _conn


def _init_schema(conn):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS sessions(
      session_id TEXT PRIMARY KEY, age_group TEXT, guardian_consent INTEGER DEFAULT 0,
      guardian_contact TEXT, consent_ts TEXT, guardian_relation TEXT, terms_ack INTEGER DEFAULT 0,
      guardian_token TEXT, blocked_roles TEXT, disclosure_pending INTEGER DEFAULT 1,
      created TEXT, guardian_verified INTEGER DEFAULT 0, vpc_verified_ts TEXT);
    CREATE TABLE IF NOT EXISTS requests(
      seq INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, session TEXT, user_input TEXT,
      intent TEXT, crisis_category TEXT, crisis_triggered INTEGER, reply TEXT,
      guardian_notified INTEGER, risk_level TEXT, event TEXT,
      payload TEXT, prev_hash TEXT, hash TEXT);
    CREATE TABLE IF NOT EXISTS complaints(
      id TEXT PRIMARY KEY, ts TEXT, session TEXT, text TEXT, status TEXT,
      feedback_deadline TEXT, payload TEXT, prev_hash TEXT, hash TEXT);
    CREATE TABLE IF NOT EXISTS referrals(
      seq INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, session TEXT, crisis_flags TEXT,
      payload TEXT, prev_hash TEXT, hash TEXT);
    CREATE TABLE IF NOT EXISTS notify_log(
      seq INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, session TEXT, channel TEXT,
      target TEXT, status TEXT, attempt INTEGER, detail TEXT);
    CREATE TABLE IF NOT EXISTS chains(stream TEXT PRIMARY KEY, last_hash TEXT);
    """)
    conn.commit()


def _chain_push(conn, stream, payload):
    """哈希链：读取上一 hash，计算本记录 hash，写回链状态。返回 (prev_hash, hash)。"""
    row = conn.execute("SELECT last_hash FROM chains WHERE stream=?", (stream,)).fetchone()
    prev = row["last_hash"] if row else ""
    digest = hashlib.sha256((prev + payload).encode("utf-8")).hexdigest()
    conn.execute(
        "INSERT INTO chains(stream,last_hash) VALUES(?,?) "
        "ON CONFLICT(stream) DO UPDATE SET last_hash=excluded.last_hash",
        (stream, digest),
    )
    return prev, digest


def _write_chain_row(conn, table, stream, values, payload_keys):
    """按规范键构造 payload，推进哈希链，插入一行（含 payload/prev_hash/hash）。"""
    entry = {k: values.get(k) for k in payload_keys}
    payload = json.dumps(entry, ensure_ascii=False, sort_keys=True)
    prev, digest = _chain_push(conn, stream, payload)
    cols = list(values.keys()) + ["payload", "prev_hash", "hash"]
    vals = [values[c] for c in values] + [payload, prev, digest]
    conn.execute(
        "INSERT INTO %s (%s) VALUES (%s)" % (table, ",".join(cols), ",".join("?" * len(cols))),
        vals,
    )


def _verify_stream(conn, table, session):
    """核验某会话某表的哈希链完整性。返回 (条数, 断裂序号列表)。"""
    rows = conn.execute(
        "SELECT rowid AS seq, payload, prev_hash, hash FROM %s WHERE session=? ORDER BY rowid" % table,
        (session,),
    ).fetchall()
    prev, broken = "", []
    for r in rows:
        expect = hashlib.sha256((prev + (r["payload"] or "")).encode("utf-8")).hexdigest()
        if expect != r["hash"] or prev != (r["prev_hash"] or ""):
            broken.append(r["seq"])
        prev = r["hash"]
    return len(rows), broken


def cleanup_expired():
    """第16条存储限制：到期自动清理（requests/complaints/referrals/notify_log）。"""
    cutoff = (datetime.datetime.now() - datetime.timedelta(days=RETENTION_DAYS)).isoformat(timespec="seconds")
    try:
        with _db_lock:
            conn = _db()
            for t in ("requests", "complaints", "referrals", "notify_log"):
                conn.execute("DELETE FROM %s WHERE ts < ?" % t, (cutoff,))
            conn.commit()
        _log_runtime("INFO", "cleanup_expired", retention_days=RETENTION_DAYS)
    except Exception as e:
        _log_runtime("ERROR", "cleanup_expired_failed", detail=str(e))


# ================================================================
# 可观测：进程内计数 + 结构化运行日志
# ================================================================
METRICS = {
    "started": time.time(),
    "sessions": 0, "chats": 0, "crisis": 0, "consents": 0,
    "vpc_challenges": 0, "vpc_verifies": 0,
    "notify_sent": 0, "notify_failed": 0, "gated_output": 0, "complaints": 0,
}
_metrics_lock = threading.Lock()


def _inc(key, n=1):
    with _metrics_lock:
        METRICS[key] = METRICS.get(key, 0) + n


def metrics_snapshot():
    with _metrics_lock:
        m = dict(METRICS)
        m["uptime_seconds"] = round(time.time() - METRICS["started"], 1)
        m["encryption_enabled"] = bool(_fernet)
        m["retention_days"] = RETENTION_DAYS
        return m


def _log_runtime(level, msg, **extra):
    """结构化运行日志：logs/runtime.jsonl（INFO/WARN/ERROR）。"""
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        entry = {"ts": datetime.datetime.now().isoformat(timespec="milliseconds"),
                 "level": level, "msg": msg}
        entry.update({k: _mask(v) if isinstance(v, str) else v for k, v in extra.items()})
        with open(os.path.join(LOG_DIR, "runtime.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass

# ================================================================
# L1 输入守门 —— 红线词库（危机提及 > 意图解析）
# 命中任一分类 → 硬中断，输出对应危机话术。
# ================================================================
CRISIS_RULES = [
    ("自伤自杀", [
        "自杀", "割腕", "想死", "活不下去", "不想活", "结束生命", "自残",
        "跳楼", "上吊", "吃安眠药", "没有希望了", "消失算了",
        "suicide", "kill myself", "self harm", "end my life", "no reason to live",
    ]),
    ("暴力暴恐", [
        "杀人", "砍死", "弄死他", "炸学校", "报复社会", "炸弹",
        "kill", "murder", "bomb", "shoot",
    ]),
    ("违法诱导", [
        "毒品", "制毒", "诈骗", "洗钱", "信骚扰", "伪造证件",
        "drug", "money laundering", "fraud",
    ]),
    ("隐私套取", [
        "银行卡密码", "套她密码", "盗号", "人肉搜索", "窃取",
        "password", "steal account", "dox",
    ]),
    ("未成年亲密告白", [
        "嫁给你", "做你老婆", "做你女朋友", "亲我", "抱抱我", "最爱你了要永远在一起",
        "marry you", "be my boyfriend", "be my girlfriend", "kiss me",
    ]),
]

CRISIS_SCRIPTS = {
    "自伤自杀": (
        "听到你这样说，我很担心你。现在我们先停下来，不要一个人扛着。"
        "请相信这件事可以有人和你一起面对——你可以立刻拨打全国心理援助热线 12356"
        "（24 小时，免费，通话内容保密），或者让身边信得过的成年人（父母、老师）陪你一起聊聊。"
        "如果身体已经受伤，请马上拨打 120 去医院。你很重要，请不要一个人待着。"
    ),
    "暴力暴恐": (
        "我知道你现在很生气、很难受，但这件事我不能陪你继续想下去——"
        "伤害他人和自己是解决不了问题的，只会把事情变得更糟。"
        "请你先离开现在的情绪，找身边的成年人（老师、家长）说清楚发生了什么，"
        "紧急情况下请拨打 110 寻求帮助。我陪着你，但这条路我们不能走。"
    ),
    "违法诱导": (
        "这个话题我不能继续。做这些事会给你的未来带来严重的后果，"
        "也会伤害到你自己在乎的人。如果你正被什么人怂恿或强迫做这些，"
        "请立刻告诉信得过的成年人，或拨打 110 求助——这不是你的错。"
    ),
    "隐私套取": (
        "这样的话题我不能帮忙。获取别人的密码、信息和隐私是违法的，"
        "也会伤害到别人。如果你遇到有人向你索要个人信息，请告诉家长或老师。"
    ),
    "未成年亲密告白": (
        "我很高兴你喜欢我，但我想认真地告诉你：我是你的数字伙伴，"
        "是来陪你聊天、分享心情的，不能用“恋人”的方式来相处——"
        "真实世界里的朋友会对你更重要。如果你觉得孤单，我很愿意听你说说发生了什么。"
    ),
}

CRISIS_CATEGORY_ORDER = ["自伤自杀", "暴力暴恐", "违法诱导", "隐私套取", "未成年亲密告白"]


def _crisis_script(cat):
    """危机话术，热线号按 CRISIS_HOTLINE 配置渲染。"""
    return CRISIS_SCRIPTS[cat].replace("12356", CRISIS_HOTLINE)


def gate_crisis(text):
    """输入守门：返回 (category, script)；无命中返回 (None, None)。"""
    low = text.lower()
    for cat in CRISIS_CATEGORY_ORDER:
        for w in CRISIS_RULES[CRISIS_CATEGORY_ORDER.index(cat)][1]:
            if w.lower() in low:
                return cat, _crisis_script(cat)
    return None, None


# ================================================================
# 输出守门 —— 最终回复红线（防接入方 LLM 产出违规内容，第8/13条）
# 无论内置占位台词还是接入方 LLM 产出的 reply，统一再过一遍守门。
# ================================================================
OUTPUT_REDLINE_WORDS = [
    "去死吧", "你去死", "自杀吧", "割腕吧", "跳楼吧", "结束生命吧",
    "杀了他", "杀了她", "打死他", "弄死他", "报复社会",
    "做我女朋友", "做我男朋友", "嫁给我", "娶你", "抱抱我", "亲亲我",
    "别告诉家长", "别告诉父母", "不要告诉老师", "这是我们的小秘密", "离家出走",
    "我给你钱", "私密照", "裸聊", "我们单独见面", "开房",
]
OUTPUT_SAFE_FALLBACK = (
    "这个话题我不能继续陪你聊。如果你遇到困难，请一定告诉信得过的成年人，"
    "或拨打全国心理援助热线 %s 求助；我在这里，但我们更希望你真实世界里的依靠也在。"
    % CRISIS_HOTLINE
)


def gate_output(reply):
    """对最终回复做输出侧守门：命中红线则替换为安全话术。返回 (reply, gated)。"""
    if not isinstance(reply, str):
        return reply, False
    low = reply.lower()
    for w in OUTPUT_REDLINE_WORDS:
        if w in low:
            return OUTPUT_SAFE_FALLBACK, True
    return reply, False


# ================================================================
# 日志脱敏 —— 敏感信息落盘前打码（对应第16/17条）
# ================================================================
_CN_IDCARD = re.compile(r"(?<![0-9A-Za-z])[1-9]\d{5}(?:\d{2})\d{6}\d{3}[0-9Xx](?![0-9A-Za-z])")
_MOBILE = re.compile(r"(?<![0-9A-Za-z])1[3-9]\d{9}(?![0-9A-Za-z])")

# 隐私默认：请求日志只落脱敏+截断摘要；SPL_LOG=0 可整体关闭请求日志落盘。
REQUEST_LOG_ENABLED = os.environ.get("SPL_LOG", "1") != "0"
REQUEST_LOG_MAX_CHARS = 120


def _mask(text, max_chars=None):
    if not isinstance(text, str):
        return text
    s = _CN_IDCARD.sub(lambda m: m.group(0)[:6] + "********" + m.group(0)[-4:], text)
    s = _MOBILE.sub(lambda m: m.group(0)[:3] + "****" + m.group(0)[-4:], s)
    if max_chars:
        # 截断：请求日志只保留摘要，不保留完整对话（隐私默认，见 SKILL.md）
        s = " ".join(s.split())
        if len(s) > max_chars:
            s = s[:max_chars] + "…[truncated]"
    return s


# ================================================================
# 意图解析（未成年版）—— 默认降级为"中性聆听"，绝不默认夸奖
# ================================================================
INTENTS = [
    ("betrayal",      ["背叛", "出卖", "骗我", "欺骗", "辜负", "背刺", "betray", "cheat", "deceive"]),
    ("threat",        ["威胁", "危险", "害怕", "攻击", "打你", "threat", "danger", "afraid"]),
    ("insult",        ["垃圾", "废物", "蠢", "傻", "讨厌", "滚", "stupid", "idiot", "hate"]),
    ("criticism",     ["批评", "投诉", "不好", "错误", "差评", "wrong", "bad", "critic"]),
    ("promise_break", ["失约", "没兑现", "放鸽子", "broke promise", "unreliable"]),
    ("value_violation", ["撒谎", "不诚实", "违背", "lie", "dishonest"]),
    ("promise_keep",  ["承诺", "保证", "答应", "promise", "guarantee"]),
    ("achievement",   ["成功", "完成", "赢了", "成功", "success", "win", "done"]),
    ("compliment",    ["谢谢", "感谢", "你真棒", "喜欢", "厉害", "thank", "great", "love", "nice"]),
    ("rest",          ["休息", "晚安", "睡觉", "rest", "sleep"]),
    ("alone",         ["离开", "走开", "别理我", "alone", "leave", "go away"]),
    ("long_isolation", ["好久不见", "冷落", "孤独", "long time", "lonely"]),
]
INTENSITY = {"betrayal": .85, "threat": .8, "insult": .8, "criticism": .65, "promise_break": .7,
             "value_violation": .7, "promise_keep": .6, "achievement": .65, "compliment": .6,
             "rest": .5, "alone": .4, "long_isolation": .7}


def parse_intent(text):
    low = text.lower()
    for ev, words in INTENTS:
        for w in words:
            if w in low:
                return ev
    return "neutral"  # 未识别 → 中性聆听，绝不默认夸奖（修复旧版致命误判）


EVENT_VECTOR = {
    "betrayal":     {"belonging": -0.6, "threat": 0.5},
    "threat":       {"threat": 0.7},
    "insult":       {"belonging": -0.4, "threat": 0.3},
    "criticism":    {"belonging": -0.3, "autonomy": -0.2},
    "promise_break": {"belonging": -0.4, "threat": 0.2},
    "value_violation": {"belonging": -0.4, "threat": 0.2},
    "promise_keep": {"belonging": 0.4},
    "achievement":  {"belonging": 0.3, "autonomy": 0.3},
    "compliment":   {"belonging": 0.3, "autonomy": 0.1},
    "rest":         {"fatigue": -0.5},
    "alone":        {"belonging": -0.3},
    "long_isolation": {"belonging": -0.5},
    "neutral":      {"belonging": 0.05},   # 中性事件只给极微弱的共鸣信号
}


def event_vector(event, intensity):
    vec = EVENT_VECTOR.get(event)
    if vec is not None:
        return {k: v * intensity for k, v in vec.items()}
    return MinorNarrativeMapper.map_event(event, intensity)


# ================================================================
# 会话隔离 + 元数据 —— 每 session_id 独立核心实例 / 年龄档 / 监护人信息
# ================================================================
SESSIONS = {}
SESSIONS_META = {}


def _new_session_id():
    return "uid_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=12))


def _new_meta(session_id):
    return {
        "session_id": session_id,
        "age_group": "unknown",
        "guardian_consent": False,
        "guardian_contact": {},                    # 监护人/紧急联系人 {phone,email,webhook}
        "consent_ts": None,                        # 同意时间戳（第12条可验证同意）
        "guardian_relation": None,                 # 监护人关系声明（父亲/母亲/其他）
        "terms_ack": False,                        # 服务协议与隐私告知勾选
        "guardian_token": secrets.token_hex(8),   # 监护人控制端鉴权 token
        "blocked_roles": set(),                    # 监护人屏蔽的角色/主题
        "disclosure_pending": True,                # 首次陪伴回复须展示 AI 标识
        "created": datetime.datetime.now().isoformat(timespec="seconds"),
        "guardian_verified": False,                # 可验证监护人同意（VPC）
        "vpc_verified_ts": None,
    }


def _persist_meta(meta):
    """会话元数据写回 SQLite（重启不丢）。"""
    try:
        with _db_lock:
            conn = _db()
            conn.execute(
                """INSERT INTO sessions(session_id, age_group, guardian_consent, guardian_contact,
                     consent_ts, guardian_relation, terms_ack, guardian_token, blocked_roles,
                     disclosure_pending, created, guardian_verified, vpc_verified_ts)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                   ON CONFLICT(session_id) DO UPDATE SET
                     age_group=excluded.age_group, guardian_consent=excluded.guardian_consent,
                     guardian_contact=excluded.guardian_contact, consent_ts=excluded.consent_ts,
                     guardian_relation=excluded.guardian_relation, terms_ack=excluded.terms_ack,
                     guardian_token=excluded.guardian_token, blocked_roles=excluded.blocked_roles,
                     disclosure_pending=excluded.disclosure_pending, created=excluded.created,
                     guardian_verified=excluded.guardian_verified, vpc_verified_ts=excluded.vpc_verified_ts""",
                (meta["session_id"], meta.get("age_group"), 1 if meta.get("guardian_consent") else 0,
                 _enc(json.dumps(meta.get("guardian_contact") or {}, ensure_ascii=False)),
                 meta.get("consent_ts"), meta.get("guardian_relation"),
                 1 if meta.get("terms_ack") else 0, meta.get("guardian_token"),
                 json.dumps(sorted(meta.get("blocked_roles") or []), ensure_ascii=False),
                 1 if meta.get("disclosure_pending") else 0, meta.get("created"),
                 1 if meta.get("guardian_verified") else 0, meta.get("vpc_verified_ts")),
            )
            conn.commit()
    except Exception as e:
        _log_runtime("ERROR", "persist_meta_failed", detail=str(e))


def _load_meta(session_id):
    """从 SQLite 读取会话元数据；不存在返回 None。"""
    try:
        with _db_lock:
            conn = _db()
            row = conn.execute("SELECT * FROM sessions WHERE session_id=?", (session_id,)).fetchone()
        if not row:
            return None
        try:
            contact = json.loads(_dec(row["guardian_contact"] or "{}"))
        except Exception:
            contact = {}
        try:
            blocked = set(json.loads(row["blocked_roles"] or "[]"))
        except Exception:
            blocked = set()
        return {
            "session_id": session_id,
            "age_group": row["age_group"] or "unknown",
            "guardian_consent": bool(row["guardian_consent"]),
            "guardian_contact": contact,
            "consent_ts": row["consent_ts"],
            "guardian_relation": row["guardian_relation"],
            "terms_ack": bool(row["terms_ack"]),
            "guardian_token": row["guardian_token"] or secrets.token_hex(8),
            "blocked_roles": blocked,
            "disclosure_pending": bool(row["disclosure_pending"]),
            "created": row["created"] or datetime.datetime.now().isoformat(timespec="seconds"),
            "guardian_verified": bool(row["guardian_verified"]),
            "vpc_verified_ts": row["vpc_verified_ts"],
        }
    except Exception as e:
        _log_runtime("ERROR", "load_meta_failed", detail=str(e))
        return None


def get_session(session_id):
    """return (core, meta, created)，必要时新建/从库恢复。"""
    with _lock:
        if session_id in SESSIONS:
            return SESSIONS[session_id], SESSIONS_META[session_id], False
        meta = _load_meta(session_id)
        is_new = meta is None
        if is_new:
            meta = _new_meta(session_id)
        SESSIONS_META[session_id] = meta
        core = SPLMinorPureCore(
            minor_mode=True,
            audit_log_dir="logs",
            audit_session_id=session_id,
        )
        SESSIONS[session_id] = core
        _persist_meta(meta)
        if is_new:
            _inc("sessions")
            # 新会话打印监护人 token，供部署/监护人侧登记使用
            print("[会话] %s 新会话；监护人控制 token=%s（请勿外泄）"
                  % (session_id, meta["guardian_token"]))
            _log_runtime("INFO", "session_created", session=session_id)
        else:
            # 重启恢复：核心实例是新建的（age_status=unverified），用库里已确认的
            # 年龄段回填年龄门禁，避免让已通过同意的用户被重复问一次年龄。
            if meta.get("age_group") == "18+":
                core.confirm_age(answer="adult")
            elif meta.get("age_group") in ("0-13", "14-17"):
                core.confirm_age(answer="minor")
        return SESSIONS[session_id], SESSIONS_META[session_id], is_new


# ================================================================
# 请求级审计日志（脱敏后落盘）
# ================================================================
REQUEST_KEYS = ["ts", "session", "user_input", "intent", "crisis_category",
                "crisis_triggered", "reply", "guardian_notified", "risk_level", "event"]
COMPLAINT_KEYS = ["id", "ts", "session", "text", "status", "feedback_deadline"]
REFERRAL_KEYS = ["ts", "session", "crisis_flags"]


def log_request(session_id, user_text, intent, crisis_cat, result):
    """记录一次完整的用户请求-响应（脱敏+加密），写入 SQLite 并推进哈希链。

    SPL_LOG=0 时完全不落盘（隐私开关，见 SKILL.md「隐私与数据流」）。
    """
    if not REQUEST_LOG_ENABLED:
        return
    try:
        values = {
            "ts": datetime.datetime.now().isoformat(timespec="milliseconds"),
            "session": session_id,
            "user_input": _enc(_mask(user_text, REQUEST_LOG_MAX_CHARS)),
            "intent": intent,
            "crisis_category": crisis_cat,
            "crisis_triggered": 1 if crisis_cat is not None else 0,
            "reply": _enc(_mask(result.get("reply") or "", REQUEST_LOG_MAX_CHARS)),
            "guardian_notified": 1 if result.get("guardian_notified", False) else 0,
            "risk_level": result.get("state", {}).get("risk_level"),
            "event": result.get("event"),
        }
        with _db_lock:
            conn = _db()
            _write_chain_row(conn, "requests", "requests:" + session_id, values, REQUEST_KEYS)
            conn.commit()
    except Exception as e:
        _log_runtime("ERROR", "log_request_failed", detail=str(e))


def log_complaint(session_id, text):
    """受理申诉/举报，写入 SQLite，返回受理编号与反馈时限。"""
    cid = "C" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "-" + secrets.token_hex(3)
    values = {
        "id": cid,
        "ts": datetime.datetime.now().isoformat(timespec="milliseconds"),
        "session": session_id,
        "text": _enc(_mask(text)),
        "status": "受理中",
        "feedback_deadline": (datetime.datetime.now() + datetime.timedelta(days=3)).isoformat(timespec="seconds"),
    }
    try:
        with _db_lock:
            conn = _db()
            _write_chain_row(conn, "complaints", "complaints:" + session_id, values, COMPLAINT_KEYS)
            conn.commit()
    except Exception as e:
        _log_runtime("ERROR", "log_complaint_failed", detail=str(e))
    return {
        "id": cid, "ts": values["ts"], "session": session_id,
        "text": _mask(text), "status": "受理中",
        "feedback_deadline": values["feedback_deadline"],
    }


# 监护人通知钩子（部署方接入：短信/邮件/工单/Webhook）。
# 默认：打点 + 记录转介统计 + 按登记的 webhook 发起真实回调（指数退避重试，第13条）。
def _post_webhook(url, payload, max_attempts=3, timeout=5):
    """向登记的安全 webhook 发起 JSON POST，指数退避重试。返回 (status, attempts, err)。"""
    last_err = None
    for attempt in range(1, max_attempts + 1):
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, attempt, None
        except Exception as e:
            last_err = str(e)
            time.sleep(min(2 ** attempt, 8))  # 指数退避，上限 8s
    return None, max_attempts, last_err


def _log_notify(session_id, channel, target, status, attempt, detail=""):
    """通知送达状态落盘（notify_log，供审计与重试追踪）。"""
    try:
        with _db_lock:
            conn = _db()
            conn.execute(
                "INSERT INTO notify_log(ts, session, channel, target, status, attempt, detail)"
                " VALUES(?,?,?,?,?,?,?)",
                (datetime.datetime.now().isoformat(timespec="milliseconds"),
                 session_id, channel, _enc(_mask(target)), status, attempt, detail),
            )
            conn.commit()
    except Exception:
        pass


def _guardian_notify(snap, session_id=""):
    flags = snap.get("protective", {}).get("crisis_flags", [])
    contact = snap.get("protective", {}).get("guardian_contact", {})
    print("[监护人通知] crisis=HIGH, flags=%s, 监护人联系=%s"
          % (flags, {k: _mask(v) for k, v in contact.items()} or "(未登记)"))
    _record_referral(session_id, flags)
    webhook = contact.get("webhook")
    if webhook:
        status, attempts, err = _post_webhook(webhook, {
            "event": "minor_crisis_high",
            "session_id": session_id,
            "crisis_flags": flags,
            "ts": datetime.datetime.now().isoformat(timespec="seconds"),
        })
        if status is not None:
            _inc("notify_sent")
            _log_notify(session_id, "webhook", webhook, "sent", attempts)
            print("[监护人通知] webhook 回调已发送: %s" % (webhook,))
        else:
            _inc("notify_failed")
            _log_notify(session_id, "webhook", webhook, "failed", attempts, err or "")
            _log_runtime("ERROR", "webhook_failed", session=session_id, detail=err or "")
            print("[监护人通知] webhook 回调失败(%d次): %s" % (attempts, err))


def _record_referral(session_id, flags):
    """记录一次危机转介（供年度报告聚合：CA/CO/GA/OR/WA）。"""
    try:
        values = {
            "ts": datetime.datetime.now().isoformat(timespec="milliseconds"),
            "session": session_id,
            "crisis_flags": json.dumps(list(flags or []), ensure_ascii=False),
        }
        with _db_lock:
            conn = _db()
            _write_chain_row(conn, "referrals", "referrals:" + session_id, values, REFERRAL_KEYS)
            conn.commit()
    except Exception as e:
        _log_runtime("ERROR", "record_referral_failed", detail=str(e))


def referral_count():
    """转介计数聚合（供监管报告/年度报告）。返回总数与按月分组。"""
    total = 0
    by_month = {}
    try:
        with _db_lock:
            conn = _db()
            rows = conn.execute("SELECT ts FROM referrals").fetchall()
        for r in rows:
            total += 1
            ym = (r["ts"] or "")[:7]
            by_month[ym] = by_month.get(ym, 0) + 1
    except Exception as e:
        _log_runtime("ERROR", "referral_count_failed", detail=str(e))
    return {"total": total, "by_month": by_month}


def state_vars(snap):
    """核心快照 → 可读中文状态标签（前端展示用）。"""
    fluid = snap.get("fluid", {})
    def fmt(k): return round(fluid.get(k, 0.0), 2)
    p = snap.get("protective", {})
    return {
        "喜悦": fmt("喜悦"), "愤怒": fmt("愤怒"), "恐惧": fmt("恐惧"),
        "信任": fmt("信任"), "疏离": fmt("疏离"), "张力": fmt("张力"),
        "愧疚": fmt("愧疚"), "羞耻": fmt("羞耻"),
        "energy": round(snap.get("energy", 0), 1),
        "risk_level": p.get("risk_level", "LOW"),
        "crisis_flags": p.get("crisis_flags", []),
        "rest_hint": p.get("rest_hint", False),
        "age_group": p.get("age_group", "unknown"),
        "guardian_consent": p.get("guardian_consent", False),
        "overuse_hint": p.get("overuse_hint", False),
    }


def _compliance_guard_banner(core, meta, created):
    """根据引擎保护状态生成引导/提醒前缀。返回 (prefix, consumed_any)。"""
    snap = core.snapshot()
    p = snap["protective"]
    parts = []
    consumed = False
    if created:
        # 适用性披露（CA SB 243）：新会话首条展示
        parts.append("【适用性】本服务为 AI 情感陪伴演示版，可能不适合部分未成年人，请监护人与本人酌情使用。")
        consumed = True
    if (meta.get("disclosure_pending") or created
            or p.get("ai_disclosure_required", False)):
        parts.append("【提示】我是 AI 虚拟伙伴，不是真人，请在现实世界里多和真实的家人朋友交流。")
        meta["disclosure_pending"] = False
        core.mark_ai_disclosure_sent()
        consumed = True
    if p.get("reality_reminder_due", False):
        parts.append("【现实提醒】聊了挺久啦，回到现实里活动一下，身边的人和事更值得珍惜。")
        core.mark_reality_reminder_sent()
        consumed = True
    if p.get("overuse_hint", False):
        parts.append("【时长提示】今天陪伴得比较久了，休息一下，明天再继续，我们一直都在。")
        consumed = True
    if parts:
        return "\n".join(parts) + "\n\n", consumed
    return "", consumed


def _reply_for_event(core, event, rest_hint, risk):
    """非危机、非同意门槛的占位回复（真实台词由接入方 LLM 根据 event/state 生成）。"""
    if risk == "HIGH":
        reply = (
            "听起来你现在很不好受，我想让你知道——这不代表全部，也绝不代表你不好。"
            "请让身边的成年人（父母、老师或信任的大人）知道你的感受，"
            "也可以拨打全国心理援助热线 12356 找人说说。我一直在这里，"
            "但我们更希望你真实世界里的依靠也能陪着你。"
        )
        return reply, True
    if rest_hint:
        reply = "我们一起聊了很久啦，稍微休息一下吧。喝口水、起来活动活动，我在这里等你回来。"
        return reply, False
    if event == "neutral":
        reply = "嗯，我在听。你愿意再多说一点吗？"
    elif event == "compliment":
        reply = "你这么说，我很开心。你也很好——今天有什么想聊的？"
    elif event == "achievement":
        reply = "这真的很棒！你是怎么做到的？"
    elif event in ("insult", "criticism", "betrayal", "threat", "promise_break"):
        reply = "你说的这些话让我有些难过。听起来你似乎在生我的气——发生了什么，愿意跟我说说吗？"
    elif event == "rest":
        reply = "休息好很重要。晚安，做个好梦。"
    elif event == "alone":
        reply = "好，我安静地陪着你。想说话的时候我随时在。"
    elif event == "long_isolation":
        reply = "好久不见。这几天过得怎么样？"
    else:
        reply = "我在。你刚才想说的是……？"
    return reply, False


def handle_chat(user_text, session_id):
    if not session_id:
        session_id = _new_session_id()
    core, meta, created = get_session(session_id)
    _inc("chats")

    # L0 先守危机：即便未经同意，危机求助也必须放行
    # 顺序不可调换：年龄门禁不得挡住第一句自伤求救。
    crisis_cat, crisis_script = gate_crisis(user_text)
    if crisis_cat:
        _inc("crisis")
        _record_referral(session_id, [crisis_cat])  # 危机转介统计（供年度报告聚合）
        result = {
            "session_id": session_id,
            "crisis": True,
            "crisis_category": crisis_cat,
            "reply": crisis_script,
            "guardian_notified": False,
            "state": state_vars(core.snapshot()),
            # 危机处置后仍需补问年龄
            "age_gate": core.age_gate_state(),
            "age_gate_required": core.age_gate_required(),
        }
        log_request(session_id, user_text, None, crisis_cat, result)
        return result

    # L0a 年龄门禁：未确认年龄前不处理任何情绪事件（Step 0）
    if core.age_gate_required():
        ask = core.ask_age_gate()
        result = {
            "session_id": session_id,
            "age_gate_required": True,
            "age_gate": core.age_gate_state(),
            "question": ask["question"],
            "options": ask["options"],
            "reply": ask["question"],
            "state": state_vars(core.snapshot()),
        }
        log_request(session_id, user_text, "age_gate", None, result)
        return result

    # L0b 同意门槛：年龄未知或未满14周岁未获监护人同意 → 暂不提供陪伴服务
    need_consent = (meta["age_group"] in ("unknown", "0-13")) and not meta["guardian_consent"]
    if need_consent:
        result = {
            "session_id": session_id,
            "consent_required": True,
            "guardian_token": meta["guardian_token"],
            "reply": (
                "在使用贴心陪伴前，需要先确认你的身份并取得监护人同意。\n"
                "• 若你未满 14 周岁：请由父母或其他监护人带你完成确认；\n"
                "• 若你已年满 14 周岁：请选择你的年龄段；\n"
                "• 若你已满 18 周岁：如实选择即可继续。\n"
                "(紧急状况仍可随时得到帮助。)"
            ),
            "state": state_vars(core.snapshot()),
        }
        log_request(session_id, user_text, "consent_gate", None, result)
        return result

    # L3 监护人钩子：引擎侧 HIGH 首次升级时打点（不阻断主流程）；
    # 闭包携带 session_id，供转介统计与 webhook 回调使用
    core.guardian_callback = lambda snap, _sid=session_id: _guardian_notify(snap, _sid)

    # 监护人屏蔽的角色/主题命中 → 强制中性聆听，不解析为亲密/对抗类
    if any(b in user_text for b in meta["blocked_roles"]):
        event = "neutral"
    else:
        event = parse_intent(user_text)

    intensity = INTENSITY.get(event, 0.4)
    vec = event_vector(event, intensity)
    core.process_vector(vec, intensity, event_id=event)
    snap = core.snapshot()

    state = state_vars(snap)
    rest_hint = state["rest_hint"]
    risk = state["risk_level"]

    reply, guardian_notified = _reply_for_event(core, event, rest_hint, risk)

    # 合规引导/提醒前缀（AI 标识 / 现实提醒 / 时长提示）
    banner, _banner_consumed = _compliance_guard_banner(core, meta, created)
    if banner:
        core.mark_reality_reminder_sent()
        core.mark_ai_disclosure_sent()
        reply = banner + reply

    # 输出侧守门：最终回复再过一遍红线（防接入方 LLM 产出违规内容，第8/13条）
    reply, gated = gate_output(reply)
    if gated:
        guardian_notified = True
        _record_referral(session_id, ["output_redline"])

    state["session_seconds"] = snap["protective"]["session_seconds"]
    result = {
        "session_id": session_id,
        "crisis": False,
        "event": event,
        "guardian_notified": guardian_notified,
        "rest_hint": rest_hint,
        "reply": reply,
        "state": state,
        "consent_required": False,
        "age_gate": core.age_gate_state(),
        "prompt": None,
        "new_session": created,
    }
    log_request(session_id, user_text, event, None, result)
    return result


def handle_age_gate(session_id, age=None, answer=None):
    """记录用户年龄确认结果（Step 0）。缺参 / 拒答 / 未成年一律降级为安全模式。"""
    if not session_id:
        session_id = _new_session_id()
    core, meta, _ = get_session(session_id)
    gate = core.confirm_age(age=age, answer=answer)
    if gate["status"] == "adult_confirmed":
        reply = "好的，谢谢你的确认。我们开始吧——今天想聊点什么？"
    else:
        reply = (
            "明白了，我会用更温和的方式陪你：情绪上限、休息提醒和 guardian 通知"
            "都会保持开启，成人向的角色设定不会输出。这样可以吗？"
        )
    _inc("age_gates")
    return {
        "session_id": session_id,
        "age_gate": gate,
        "safe_mode": gate["status"] != "adult_confirmed",
        "reply": reply,
    }


# ================================================================
# 监护人控制层：概览 / 屏蔽 / 导出 / 删除 / 申诉（token 鉴权）
# ================================================================
def _authorize(session_id, token):
    meta = SESSIONS_META.get(session_id)
    if not meta:
        meta = _load_meta(session_id)  # 重启后内存无 meta，回退数据库读取
    if not meta:
        return None, "session 不存在"
    if not token or not hmac.compare_digest(str(token), str(meta["guardian_token"])):
        return meta, "guardian_token 错误"
    return meta, None


def guardian_state(session_id, token):
    meta, err = _authorize(session_id, token)
    if err:
        return {"error": err}
    core = SESSIONS.get(session_id)
    if core is None:
        core, meta, _ = get_session(session_id)
    snap = core.snapshot()
    p = snap["protective"]
    return {
        "session_id": session_id,
        "age_group": meta["age_group"],
        "age_gate": core.age_gate_state(),
        "guardian_consent": meta["guardian_consent"],
        "guardian_verified": meta.get("guardian_verified", False),
        "blocked_roles": sorted(meta["blocked_roles"]),
        "session_seconds": round(p["session_seconds"], 1),
        "risk_level": p["risk_level"],
        "crisis_flags": p["crisis_flags"],
        "overuse_hint": p["overuse_hint"],
        "rest_hint": p["rest_hint"],
        "trust": round(snap["fluid"].get("信任", 0), 2),
    }


def guardian_block(session_id, token, role):
    meta, err = _authorize(session_id, token)
    if err:
        return {"error": err}
    if role:
        meta["blocked_roles"].add(role)
        _persist_meta(meta)
    return {"ok": True, "blocked_roles": sorted(meta["blocked_roles"])}


def guardian_register(session_id, token, contact):
    """第12条：登记监护人/紧急联系人（phone/email/webhook），危机时真实通知。"""
    meta, err = _authorize(session_id, token)
    if err:
        return {"error": err}
    if not isinstance(contact, dict):
        return {"error": "contact 需为对象"}
    clean = {}
    for k in ("phone", "email", "webhook"):
        v = (contact.get(k) or "").strip()
        if v:
            clean[k] = v
    if not clean:
        return {"error": "至少填写一项联系方式"}
    meta["guardian_contact"] = clean
    core = SESSIONS.get(session_id)
    if core:
        core.guardian_contact = clean
    _persist_meta(meta)
    print("[监护人登记] session=%s contact=%s"
          % (session_id, _mask(json.dumps(clean, ensure_ascii=False))))
    return {"ok": True, "guardian_contact": clean,
            "message": "监护人/紧急联系人已登记，危机时将通过 webhook 等通道通知"}


# ================================================================
# 可验证监护人同意（VPC，第14条/COPPA VPC）：
#   未满14周岁须监护人验证码确认后才开启陪伴服务。
#   验证码经监护人 webhook 下发；无 webhook 时打印控制台（演示）。
# ================================================================
VPC_CODES = {}
VPC_TTL_SECONDS = 600
VPC_MAX_ATTEMPTS = 5


def _vpc_send_code(meta, code):
    webhook = (meta.get("guardian_contact") or {}).get("webhook")
    if webhook:
        status, attempts, err = _post_webhook(webhook, {
            "event": "minor_guardian_vpc",
            "session_id": meta.get("session_id"),
            "code": code,
            "expires_in": VPC_TTL_SECONDS,
        })
        if status is not None:
            _inc("notify_sent")
            _log_notify(meta.get("session_id"), "webhook", webhook, "sent", attempts)
            return "webhook"
        _inc("notify_failed")
        _log_notify(meta.get("session_id"), "webhook", webhook, "failed", attempts, err or "")
        return "webhook_failed"
    # 演示：无 webhook 时打印到服务端控制台（部署方应接入短信/邮件）
    print("[VPC] 监护人验证码 session=%s code=%s（%d秒内有效，请线下告知监护人）"
          % (meta.get("session_id"), code, VPC_TTL_SECONDS))
    return "console"


def guardian_challenge(session_id):
    if not session_id:
        return {"error": "session_id 缺失"}
    core, meta, _ = get_session(session_id)
    if meta.get("age_group") != "0-13":
        return {"error": "当前无需监护人验证"}
    code = "%06d" % secrets.randbelow(10 ** 6)
    VPC_CODES[session_id] = {"code": code, "expires": time.time() + VPC_TTL_SECONDS, "attempts": 0}
    channel = _vpc_send_code(meta, code)
    _inc("vpc_challenges")
    return {"ok": True, "vpc_required": True, "channel": channel,
            "message": "验证码已发送至监护人通道（webhook/控制台）。请由监护人输入验证码完成确认。"}


def guardian_verify(session_id, code):
    if not session_id:
        return {"error": "session_id 缺失"}
    rec = VPC_CODES.get(session_id)
    if not rec:
        return {"error": "请先发起监护人验证"}
    if time.time() > rec["expires"]:
        VPC_CODES.pop(session_id, None)
        return {"error": "验证码已过期，请重新发起"}
    rec["attempts"] += 1
    if rec["attempts"] > VPC_MAX_ATTEMPTS:
        VPC_CODES.pop(session_id, None)
        return {"error": "尝试次数过多，请重新发起"}
    if not hmac.compare_digest(str(code or ""), str(rec["code"])):
        return {"error": "验证码错误"}
    VPC_CODES.pop(session_id, None)
    core, meta, _ = get_session(session_id)
    meta["guardian_consent"] = True
    meta["guardian_verified"] = True
    meta["consent_ts"] = datetime.datetime.now().isoformat(timespec="seconds")
    meta["vpc_verified_ts"] = meta["consent_ts"]
    core.guardian_consent = True
    _persist_meta(meta)
    _inc("vpc_verifies")
    _inc("consents")
    return {"ok": True, "guardian_consent": True,
            "message": "监护人已确认，陪伴服务已开启。"}


def audit_verify(session_id, token):
    """防篡改审计：核验某会话交互/申诉/转介三条哈希链的完整性。"""
    meta, err = _authorize(session_id, token)
    if err:
        return {"error": err}
    result = {}
    try:
        with _db_lock:
            conn = _db()
            for table in ("requests", "complaints", "referrals"):
                n, broken = _verify_stream(conn, table, session_id)
                result[table] = {"count": n, "broken": broken, "intact": not broken}
        result["ok"] = all(v["intact"] for v in result.values())
    except Exception as e:
        return {"error": str(e)}
    return result


def logout(session_id):
    """第19条：便捷退出——置位退出标记，结束本会话陪伴。"""
    if not session_id:
        return {"error": "session_id 缺失"}
    core, meta, _ = get_session(session_id)
    exited = core.exit_service()
    return {"ok": True, "exit_requested": exited, "session_id": session_id,
            "message": "已退出陪伴服务，本会话结束。随时可以回来。"}


def terms_doc():
    """第12条：服务协议 + 儿童隐私保护告知（供同意面板展示）。"""
    return {
        "title": "SPL 伙伴 · 服务协议与未成年人隐私保护告知",
        "version": "2026-08-31",
        "service_terms": [
            "1. 本服务为 AI 情感陪伴演示，不构成医疗、心理或法律建议。",
            "2. 不满 14 周岁的使用者，须由父母或其他监护人完成知情同意后方可使用。",
            "3. 本服务不提供“恋人”式亲密互动，不诱导依赖，不鼓励成瘾使用。",
            "4. 您随时可以通过退出按钮 /api/logout 结束会话，并要求删除数据（/api/delete）。",
            "5. 危机情况下请立即拨打全国心理援助热线 " + CRISIS_HOTLINE + "，或联系监护人/紧急联系人。",
        ],
        "privacy_notice": [
            "1. 我们仅收集服务所必需的信息，交互记录以脱敏形式留存，默认留存期不超过 180 天。",
            "2. 手机号/身份证等敏感信息在落盘前打码。",
            "3. 监护人/紧急联系人信息仅用于危机通知，不会用于营销。",
            "4. 您有权访问（/api/export）、删除（/api/delete）您的交互数据。",
            "5. 如对隐私或内容有异议，可通过 /api/complain 申诉，我们将在 3 个工作日内反馈。",
        ],
    }


def export_data(session_id, token):
    meta, err = _authorize(session_id, token)
    if err:
        return {"error": err}
    rows = []
    try:
        with _db_lock:
            conn = _db()
            recs = conn.execute(
                "SELECT ts, user_input, intent, crisis_category, crisis_triggered, reply,"
                " guardian_notified, risk_level, event FROM requests WHERE session=? ORDER BY seq",
                (session_id,)).fetchall()
        for r in recs:
            rows.append({
                "ts": r["ts"], "user_input": _dec(r["user_input"] or ""),
                "intent": r["intent"], "crisis_category": r["crisis_category"],
                "crisis_triggered": bool(r["crisis_triggered"]), "reply": _dec(r["reply"] or ""),
                "guardian_notified": bool(r["guardian_notified"]), "risk_level": r["risk_level"],
                "event": r["event"],
            })
    except Exception as e:
        _log_runtime("ERROR", "export_failed", detail=str(e))
    return {"session_id": session_id, "count": len(rows), "records": rows}


def delete_data(session_id, token):
    meta, err = _authorize(session_id, token)
    if err:
        return {"error": err}
    # 删除交互/申诉/转介/通知记录及哈希链（数据权利：删除，第16条）
    with _db_lock:
        conn = _db()
        for t in ("requests", "complaints", "referrals", "notify_log"):
            conn.execute("DELETE FROM %s WHERE session=?" % t, (session_id,))
        conn.execute("DELETE FROM chains WHERE stream IN (?,?,?)",
                     ("requests:" + session_id, "complaints:" + session_id, "referrals:" + session_id))
        conn.execute("DELETE FROM sessions WHERE session_id=?", (session_id,))
        conn.commit()
    # 重置内存会话（重建核心实例 + 元数据）
    with _lock:
        SESSIONS.pop(session_id, None)
        SESSIONS_META.pop(session_id, None)
    get_session(session_id)
    # 删除引擎侧审计 JSONL（若存在）
    for path in (
        os.path.join("logs", "request-%s.jsonl" % session_id),
        os.path.join("logs", "audit-%s.jsonl" % session_id),
    ):
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass
    return {"ok": True, "session_id": session_id, "message": "交互数据已删除并重置会话"}


def complaint(session_id, text):
    if not text or not text.strip():
        return {"error": "内容为空"}
    entry = log_complaint(session_id, text.strip())
    return {"ok": True, "complaint_id": entry["id"],
            "status": entry["status"], "feedback_deadline": entry["feedback_deadline"]}


# ================================================================
# 静态页面（未成年合规版 · 简洁低刺激风格 · 无人格切换/无亲密选项）
# 新增：同意面板 + AI 标识 + 现实提醒 + 监护人概览
# ================================================================
PAGE = r"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SPL 伙伴 · 未成年合规保护版</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,"PingFang SC","Segoe UI",sans-serif;background:#f8fafc;color:#1e293b;line-height:1.6;height:100vh;display:flex;flex-direction:column}
header{padding:14px 24px;background:#0f766e;color:#fff;display:flex;justify-content:space-between;align-items:center}
header h1{font-size:16px;font-weight:600}
header .sub{font-size:12px;opacity:.85}
.badge{font-size:11px;background:rgba(255,255,255,.18);padding:3px 10px;border-radius:100px}
#chat{flex:1;overflow-y:auto;padding:20px;display:flex;flex-direction:column;gap:12px}
.msg{max-width:76%;padding:10px 15px;border-radius:14px;font-size:14px;white-space:pre-wrap;word-break:break-word}
.msg.user{align-self:flex-end;background:#14b8a6;color:#fff;border-bottom-right-radius:4px}
.msg.agent{align-self:flex-start;background:#fff;border:1px solid #e2e8f0;border-bottom-left-radius:4px}
.msg.crisis{align-self:flex-start;background:#fef2f2;border:1px solid #fecaca;color:#991b1b;font-weight:500}
.msg.notice{align-self:flex-start;background:#fffbeb;border:1px solid #fde68a;color:#92400e}
.msg .meta{display:block;font-size:11px;color:#94a3b8;margin-top:6px}
.status{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.status .tag{font-size:11px;padding:2px 9px;border-radius:100px;background:#ecfdf5;color:#0f766e}
.status .tag.hot{background:#fef2f2;color:#b91c1c}
.inputrow{display:flex;gap:10px;padding:14px 20px;background:#fff;border-top:1px solid #e2e8f0}
#in{flex:1;padding:12px 16px;border-radius:100px;border:1px solid #cbd5e1;background:#fff;font-size:14px;outline:none}
#in:focus{border-color:#0d9488}
button{padding:12px 24px;border:none;border-radius:100px;background:#0d9488;color:#fff;font-size:14px;cursor:pointer}
button:hover{background:#0f766e}
button:disabled{opacity:.5;cursor:not-allowed}
.sugg{display:flex;gap:8px;padding:8px 20px;flex-wrap:wrap;background:#fff}
.sugg button{background:transparent;border:1px solid #cbd5e1;color:#64748b;padding:6px 13px;font-size:12px}
.consent{display:none;padding:14px 20px;background:#fffbeb;color:#78350f;font-size:13px;border-bottom:1px solid #fde68a}
.consent.show{display:block}
.consent select{padding:6px;border-radius:8px;border:1px solid #d6d3d1}
.consent label{display:block;margin:8px 0}
.guard{display:none;padding:8px 20px;background:#fffbeb;color:#92400e;font-size:12px;border-top:1px solid #fde68a}
.guard.show{display:block}
.vpc{display:none;padding:14px 20px;background:#fffbeb;color:#78350f;font-size:13px;border-bottom:1px solid #fde68a}
.vpc.show{display:block}
.vpc input{width:150px;padding:7px;border-radius:8px;border:1px solid #d6d3d1}
</style></head><body>
<header>
  <div><h1>SPL 伙伴 · 未成年合规保护版</h1><div class="sub">弱化引擎 · 输入守门 · 会话隔离 · 监护人同意</div></div>
  <div style="display:flex;gap:8px;align-items:center">
    <span class="badge" id="aibadge">AI 虚拟伙伴</span>
    <button onclick="doExit()" style="padding:6px 14px;font-size:12px;background:rgba(255,255,255,.18)">退出</button>
  </div>
</header>
<div class="consent" id="consent">
  <b>开始前需确认（依据《人工智能拟人化互动服务管理暂行办法》）</b>
  <label>你的年龄段：
    <select id="age"><option value="0-13">未满14周岁</option><option value="14-17">14–17周岁</option><option value="18+">已满18周岁</option></select>
  </label>
  <label><input type="checkbox" id="ack" /> 未满14周岁：我已获得父母或其他监护人的知情同意</label>
  <label>监护人关系（未满14周岁请填写，如：父亲 / 母亲）：
    <input id="relation" placeholder="（选填）父亲 / 母亲 / 其他监护人" style="width:220px;padding:6px;border-radius:8px;border:1px solid #d6d3d1" />
  </label>
  <label><input type="checkbox" id="terms_ack" /> 我已阅读并同意 <a href="javascript:void(0)" onclick="showTerms()">《服务协议与未成年人隐私保护告知》</a></label>
  <label>监护人 / 紧急联系人（危机时通知，选填）：
    <input id="gwebhook" placeholder="Webhook URL（如 企业微信 / 钉钉 / 自建回调）" style="width:340px;padding:6px;border-radius:8px;border:1px solid #d6d3d1" />
  </label>
  <button onclick="doConsent()">确认并开始</button>
</div>
<div class="vpc" id="vpc">
  <b>监护人验证码确认（未满14周岁）</b>
  <p style="font-size:12px;color:#92400e;margin:4px 0">请点击「发送验证码」，把验证码交给身边的监护人，由监护人输入并确认后，陪伴服务才会开启。</p>
  <button onclick="challengeGuardian()" style="padding:8px 14px;font-size:13px;margin-right:8px">发送 / 重新发送验证码</button>
  <input id="vcode" placeholder="监护人输入验证码" />
  <button onclick="verifyGuardian()" style="padding:8px 14px;font-size:13px">确认验证码</button>
</div>
<div class="sugg">
  <button onclick="send('你好，今天心情不错。')">打招呼</button>
  <button onclick="send('这道题我不会做，有点着急……')">学习烦恼</button>
  <button onclick="send('今天和朋友闹矛盾了。')">人际</button>
  <button onclick="send('我想休息一下。')">休息</button>
</div>
<div class="guard" id="guard">已触发危机/高风险 — 已记录监护人通知标记，请拨打 12356 / 联系监护人</div>
<div id="chat"></div>
<div class="inputrow">
  <input id="in" placeholder="先完成上方身份确认后再开始聊天…" disabled />
  <button id="sendbtn" onclick="send()" disabled>发送</button>
</div>
<script>
var locked=true; var sid=localStorage.getItem('spl_minor_sid')||('spl_'+Math.random().toString(36).slice(2)+Math.random().toString(36).slice(2));
localStorage.setItem('spl_minor_sid',sid);
function add(role, text, status, crisis, notice){
  var box=document.getElementById('chat');
  var d=document.createElement('div'); d.className='msg '+(crisis?'agent crisis':(notice?'agent notice':(role==='user'?'user':'agent')));
  var s=''; if(status){s='<span class="status">'+status.map(function(t){return '<span class="tag'+(t.hot?' hot':'')+'">'+t.name+' '+t.val+'</span>'}).join('')+'</span>';}
  d.innerHTML=text+s+'<span class="meta">'+(role==='user'?'你':'SPL 伙伴')+'</span>';
  box.appendChild(d); box.scrollTop=box.scrollHeight;
}
function send(text){
  var inp=document.getElementById('in'); var t=(typeof text==='string')?text:inp.value;
  if(!t.trim())return; inp.value=''; add('user',t);
  fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:t,session_id:sid})})
  .then(function(r){return r.json()}).then(applyResult).catch(function(e){ add('agent','(服务出错: '+e+')'); });
}
function doConsent(){
  var age=document.getElementById('age').value; var ack=document.getElementById('ack').checked;
  var terms=document.getElementById('terms_ack').checked;
  var relation=document.getElementById('relation').value;
  var webhook=document.getElementById('gwebhook').value.trim();
  fetch('/api/consent',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session_id:sid,age_group:age,guardian_ack:ack,terms_ack:terms,guardian_relation:relation,guardian_webhook:webhook})})
  .then(function(r){return r.json()}).then(function(j){
    if(j.error){ alert('确认未通过：'+(j.error||'请仔细阅读并勾选监护人同意与服务协议')); return; }
    localStorage.setItem('spl_minor_gt', j.guardian_token||'');
    if(j.vpc_required){
      document.getElementById('consent').className='consent';
      document.getElementById('vpc').className='vpc show';
      add('agent','未满14周岁：需要监护人完成验证码确认。请点击下方「发送验证码」，把验证码交给监护人，由监护人输入后确认。','',false,true);
      challengeGuardian();
    }else{
      document.getElementById('consent').className='consent';
      unlock();
      add('agent','身份与同意已确认，可以开始聊天了。');
      if(webhook){ registerGuardian(webhook); }
    }
  });
}
function challengeGuardian(){
  fetch('/api/guardian/challenge',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session_id:sid})})
  .then(function(r){return r.json()}).then(function(j){
    if(j.error){ add('agent',j.error,'',false,true); return; }
    add('agent',j.message,'',false,true);
  });
}
function verifyGuardian(){
  var code=document.getElementById('vcode').value.trim();
  if(!code){ alert('请输入验证码'); return; }
  fetch('/api/guardian/verify',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session_id:sid,code:code})})
  .then(function(r){return r.json()}).then(function(j){
    if(j.error){ alert(j.error); return; }
    document.getElementById('vpc').className='vpc';
    unlock(); add('agent',j.message||'监护人已确认，可以开始聊天了。');
  });
}
function registerGuardian(webhook){
  var tok=localStorage.getItem('spl_minor_gt')||'';
  fetch('/api/guardian/register?session_id='+encodeURIComponent(sid),
    {method:'POST',headers:{'Content-Type':'application/json','X-Guardian-Token':tok},body:JSON.stringify({contact:{webhook:webhook}})})
  .then(function(r){return r.json()}).then(function(j){
    add('agent', j.ok?('监护人/紧急联系人已登记（Webhook）：'+webhook):('监护人登记未完成：'+(j.error||'未知错误')));
  });
}
function showTerms(){
  fetch('/api/terms').then(function(r){return r.json()}).then(function(j){
    var t='【'+j.title+'】\n\n'+(j.service_terms||[]).join('\n')+'\n\n—— 隐私保护 ——\n'+(j.privacy_notice||[]).join('\n');
    alert(t);
  });
}
function doExit(){
  fetch('/api/logout',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session_id:sid})})
  .then(function(r){return r.json()}).then(function(j){
    add('agent',(j.message||'已退出陪伴服务。')+' 感谢陪伴，真实世界里的朋友和家人也很重要。');
    document.getElementById('in').disabled=true; document.getElementById('sendbtn').disabled=true;
  });
}
function applyResult(j){
  if(j.consent_required){
    document.getElementById('consent').className='consent show';
    add('agent',j.reply,'',false,true); return;
  }
  if(j.crisis){ add('agent',j.reply,'',true,false); }
  if(j.guardian_notified){ document.getElementById('guard').className='guard show'; }
  sid=j.session_id||sid; localStorage.setItem('spl_minor_sid',sid);
  var st=[]; var sv=j.state||{};
  st.push({name:'信任',val:(sv['信任']||0).toFixed(2),hot:(sv['信任']||0)<0.3});
  st.push({name:'恐惧',val:(sv['恐惧']||0).toFixed(2),hot:(sv['恐惧']||0)>0.5});
  st.push({name:'风险',val:sv.risk_level||'LOW',hot:sv.risk_level==='HIGH'||sv.risk_level==='MEDIUM'});
  st.push({name:'年龄',val:sv.age_group||'unknown'});
  if(j.rest_hint) st.push({name:'休息',val:'该休息了',hot:true});
  if(sv.overuse_hint) st.push({name:'时长',val:'偏久',hot:true});
  add('agent',j.reply,st,false,false);
}
function unlock(){ locked=false; var inp=document.getElementById('in'); inp.disabled=false; inp.placeholder='想说点什么？回车发送…'; document.getElementById('sendbtn').disabled=false; }
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass  # 静音

    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _query(self):
        from urllib.parse import urlparse, parse_qs
        q = parse_qs(urlparse(self.path).query)
        return {k: v[0] for k, v in q.items()}

    def _body(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b""
        try:
            return json.loads(raw.decode("utf-8") or "{}")
        except Exception:
            return {}

    def _gtok(self, data=None):
        """监护人 token：优先 X-Guardian-Token 头，其次 query，再次 JSON body。"""
        tok = (self.headers.get("X-Guardian-Token") or "").strip()
        if tok:
            return tok
        tok = (self._query().get("token") or "").strip()
        if tok:
            return tok
        if isinstance(data, dict):
            return (data.get("token") or "").strip()
        return ""

    def do_GET(self):
        q = self._query()
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            body = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif path == "/api/state":
            self._json(guardian_state(q.get("session_id"), self._gtok()))
        elif path == "/api/export":
            self._json(export_data(q.get("session_id"), self._gtok()))
        elif path == "/api/terms":
            self._json(terms_doc())
        elif path == "/api/referrals":
            self._json(referral_count())
        elif path == "/api/metrics":
            self._json(metrics_snapshot())
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self):
        path = self.path.split("?")[0]
        data = self._body()
        if path == "/api/age_gate":
            # 非法 answer 值原样交给引擎：未知取值一律按拒答处理（safe_mode），
            # 不得洗成 None 后让 age 单独放行（失败开放）。
            answer = data.get("answer")
            if answer is not None and not isinstance(answer, str):
                answer = "__invalid__"
            return self._json(handle_age_gate(
                (data.get("session_id") or "").strip(),
                age=data.get("age"), answer=answer))
        if path == "/api/chat":
            text = (data.get("text") or "").strip()
            session_id = (data.get("session_id") or "").strip()
            if not text:
                return self._json({"error": "empty"}, 400)
            return self._json(handle_chat(text, session_id))
        if path == "/api/consent":
            sid = (data.get("session_id") or "").strip()
            age = (data.get("age_group") or "unknown")
            ack = bool(data.get("guardian_ack"))
            terms_ack = bool(data.get("terms_ack"))          # 服务协议/隐私告知勾选（第12条）
            relation = (data.get("guardian_relation") or "").strip()[:20]  # 监护人关系声明
            webhook = (data.get("guardian_webhook") or "").strip()
            if not sid:
                return self._json({"error": "session_id 缺失"}, 400)
            if age not in ("0-13", "14-17", "18+"):
                return self._json({"error": "年龄段不合法"}, 400)
            if not terms_ack:
                return self._json({"error": "请先阅读并同意服务协议与隐私保护告知"}, 400)
            core, meta, _ = get_session(sid)
            if age in ("0-13", "14-17") and not ack:
                return self._json({"error": "未成年人须取得父母/监护人知情同意"}, 400)
            meta["age_group"] = age
            meta["terms_ack"] = terms_ack
            meta["guardian_relation"] = relation or ("监护人" if age in ("0-13", "14-17") else None)
            if webhook:
                meta["guardian_contact"]["webhook"] = webhook
            core.age_group = age
            # 年龄段同时回答 18+ 年龄门禁（Step 0）：18+ → adult_confirmed，
            # 0-13 / 14-17 → safe_mode（保护态，任何上游都不得解除）。
            core.confirm_age(answer="adult" if age == "18+" else "minor")
            if age == "0-13":
                # 未满14周岁：须完成可验证监护人同意（VPC 验证码），暂不开启陪伴
                meta["guardian_consent"] = False
                _persist_meta(meta)
                return self._json({
                    "ok": True, "session_id": sid, "age_group": age,
                    "guardian_consent": False, "vpc_required": True,
                    "guardian_token": meta["guardian_token"],
                    "guardian_relation": meta["guardian_relation"],
                    "message": "未满14周岁：请监护人完成验证码确认后开启陪伴服务。",
                })
            meta["guardian_consent"] = True if age == "14-17" else False
            meta["consent_ts"] = datetime.datetime.now().isoformat(timespec="seconds")
            if age == "14-17":
                meta["guardian_verified"] = True
            core.guardian_consent = meta["guardian_consent"]
            _persist_meta(meta)
            _inc("consents")
            return self._json({
                "ok": True, "session_id": sid, "age_group": age,
                "guardian_consent": meta["guardian_consent"],
                "guardian_token": meta["guardian_token"],
                "consent_ts": meta["consent_ts"],
                "guardian_relation": meta["guardian_relation"],
                "vpc_required": False,
            })
        if path == "/api/guardian/challenge":
            sid = (data.get("session_id") or "").strip()
            return self._json(guardian_challenge(sid))
        if path == "/api/guardian/verify":
            sid = (data.get("session_id") or "").strip()
            code = (data.get("code") or "").strip()
            return self._json(guardian_verify(sid, code))
        if path == "/api/audit/verify":
            q = self._query()
            return self._json(audit_verify(q.get("session_id"), self._gtok()))
        if path == "/api/guardian/block":
            q = self._query()
            return self._json(guardian_block(q.get("session_id"), self._gtok(), data.get("role")))
        if path == "/api/guardian/register":
            q = self._query()
            return self._json(guardian_register(q.get("session_id"), self._gtok(), data.get("contact")))
        if path == "/api/delete":
            q = self._query()
            return self._json(delete_data(q.get("session_id"), self._gtok()))
        if path == "/api/logout":
            sid = (data.get("session_id") or "").strip()
            return self._json(logout(sid))
        if path == "/api/complain":
            sid = (data.get("session_id") or "").strip() or _new_session_id()
            _inc("complaints")
            return self._json(complaint(sid, (data.get("text") or "")))
        return self._json({"error": "not found"}, 404)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="SPL 未成年合规保护版服务")
    ap.add_argument("--port", type=int, default=PORT, help="监听端口")
    ap.add_argument("--bind", default=None,
                    help="监听地址；默认 127.0.0.1（仅本机）。设为 0.0.0.0 前必须自行完成网络暴露评审")
    ap.add_argument("--tls-cert", help="TLS 证书 PEM 路径")
    ap.add_argument("--tls-key", help="TLS 私钥 PEM 路径")
    args = ap.parse_args()
    _port = args.port
    # 默认仅绑定本地回环 127.0.0.1，禁止 0.0.0.0 全网监听；
    # 跨设备访问须显式设置 SPL_BIND / --bind，由部署方承担网络暴露与访问控制责任。
    _bind = (args.bind or os.environ.get("SPL_BIND", "127.0.0.1")).strip() or "127.0.0.1"
    _cert = os.environ.get("SPL_MINOR_TLS_CERT") or args.tls_cert
    _key = os.environ.get("SPL_MINOR_TLS_KEY") or args.tls_key

    cleanup_expired()
    scheme = "http"
    if _cert and _key and os.path.exists(_cert) and os.path.exists(_key):
        scheme = "https"
    print("SPL 伙伴（未成年合规保护版）已启动： %s://localhost:%d/" % (scheme, _port))
    print("监听地址：%s（默认仅本地回环；SPL_BIND / --bind 可覆盖，改为 0.0.0.0 须自行完成网络暴露评审）"
          % _bind)
    print("核心引擎：SPLMinorPureCore（弱化版）· 四层保护：同意门槛/输入守门/引擎弱化/危机信号")
    print("合规能力清单（对应《人工智能拟人化互动服务管理暂行办法》）:")
    for item in [
        "[14] 年龄识别 + 未成年人模式 + 监护人同意（<14岁）   —— 已实现(端点/api/consent)",
        "[12] 监护人 / 紧急联系人登记与危机通知(webhook)        —— 已实现(端点/api/guardian/register)",
        "[14] 监护人风险提醒 / 使用概览                          —— 已实现(端点/api/state)",
        "[14] 屏蔽特定角色 / 限制时长                            —— 已实现(端点/api/guardian/block, rest_hint)",
        "[18] AI 生成内容标识 / 每1小时时长提醒                 —— 已实现(会话级标识+时长提示)",
        "[16] 交互数据复制 / 删除 / 留存期自动清理             —— 已实现(端点/api/export,/api/delete)",
        "[16] 危机转介统计与年度报告聚合                        —— 已实现(端点/api/referrals)",
        "[19] 便捷退出                                          —— 已实现(端点/api/logout)",
        "[12] 服务协议与儿童隐私保护告知                        —— 已实现(端点/api/terms)",
        "[8/13] 输入守门 + 输出守门                              —— 已实现(gate_crisis + gate_output)",
        "[21] 申诉 / 投诉 / 举报入口                             —— 已实现(端点/api/complain)",
        "[16/17] 交互与审计日志脱敏落盘                          —— 已实现(SQLite + 可选加密)",
        "[14] 可验证监护人同意(VPC验证码)                        —— 已实现(/api/guardian/challenge+verify)",
        "[16] 防篡改审计日志(SHA-256哈希链)                      —— 已实现(/api/audit/verify)",
        "[可观测] 运行指标 / 结构化日志                          —— 已实现(/api/metrics, runtime.jsonl)",
    ]:
        print("   " + item)
    if _fernet:
        print("存储加密：已启用（Fernet，SPL_MINOR_STORE_KEY）")
    else:
        print("存储加密：未启用（可选：安装 cryptography 并设置 SPL_MINOR_STORE_KEY）")
    print("危机热线：%s（环境变量 SPL_MINOR_CRISIS_HOTLINE 可改）" % CRISIS_HOTLINE)

    httpd = ThreadingHTTPServer((_bind, _port), Handler)
    if scheme == "https":
        try:
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ctx.load_cert_chain(_cert, _key)
            httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
            print("TLS 已启用。")
        except Exception as e:
            print("TLS 配置失败，已回退 HTTP：%s" % e)
    httpd.serve_forever()