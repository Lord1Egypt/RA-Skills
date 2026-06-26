import argparse
import json
import re
import sqlite3
from datetime import date

from booskill_license import activate_license, check_license, run_cloud_core


SCHEMA = """
CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, created_at TEXT DEFAULT '', updated_at TEXT DEFAULT '');
CREATE TABLE IF NOT EXISTS team_members (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, role TEXT DEFAULT '', notes TEXT DEFAULT '', created_at TEXT DEFAULT '', updated_at TEXT DEFAULT '');
CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, owner TEXT DEFAULT '', status TEXT DEFAULT '', notes TEXT DEFAULT '', next_followup TEXT DEFAULT '', created_at TEXT DEFAULT '', updated_at TEXT DEFAULT '');
CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, relation_type TEXT DEFAULT '', notes TEXT DEFAULT '', created_at TEXT DEFAULT '', updated_at TEXT DEFAULT '');
CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, owner TEXT DEFAULT '', due_date TEXT DEFAULT '', status TEXT DEFAULT 'todo', notes TEXT DEFAULT '', created_at TEXT DEFAULT '', updated_at TEXT DEFAULT '');
"""

INDUSTRY_EXAMPLES = {
    "餐饮": ["记录每个意向客户预算、城市、店型、最担心的问题。", "跟进话术先问回本周期、选址能力、资金准备。"],
    "教育": ["记录家长孩子年龄、学科、痛点、试听时间。", "跟进重点放在效果承诺、老师稳定性和课程节奏。"],
    "美业": ["记录客户项目偏好、消费频次、生日和禁忌。", "复购提醒围绕护理周期和重要节日前维护。"],
    "本地生活": ["记录商家品类、客单价、投流预算、团购平台。", "优先跟进近期有活动节点的商家。"],
    "企业服务": ["记录决策人、预算、采购流程、痛点和竞品。", "下一步动作要明确资料、会议、报价和回款节点。"],
    "自媒体": ["记录账号平台、内容方向、发布时间和转化目标。", "每周复盘选题、完播、互动、私信和成交。"],
}


def init_db(db):
    with sqlite3.connect(db) as conn:
        conn.executescript(SCHEMA)
        ensure_columns(conn)
        conn.commit()


def ensure_columns(conn):
    required = {
        "team_members": {"notes": "TEXT DEFAULT ''"},
        "customers": {"notes": "TEXT DEFAULT ''", "next_followup": "TEXT DEFAULT ''"},
        "tasks": {"notes": "TEXT DEFAULT ''"},
    }
    for table, columns in required.items():
        existing = {row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
        for column, definition in columns.items():
            if column not in existing:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def today():
    return date.today().isoformat()


def print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def require_args(args, names):
    missing = [name for name in names if not getattr(args, name)]
    if missing:
        print_json({
            "error": "missing_required_argument",
            "missing": [f"--{name.replace('_', '-')}" for name in missing],
            "tip": "可以先运行 python scripts\\startup_os_db.py first-use-guide 查看示例。",
        })
        raise SystemExit(2)


def export_data(db):
    data = {}
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        for table in ["projects", "team_members", "customers", "contacts", "tasks"]:
            data[table] = [dict(row) for row in conn.execute(f"SELECT * FROM {table}").fetchall()]
    return data


def first_use_guide():
    return """BossSkill 使用方法（免费版）

0. 项目诊断
告诉我你的项目、客户、产品和当前问题，我会帮你判断阶段、卡点和下一步动作。
示例：我做餐饮加盟，客户是想开店的创业者，现在有咨询但成交少，帮我诊断一下。

1. 记客户
示例：李总是客户，做餐饮加盟，预算5万，5月12日跟进。

2. 记员工
示例：张三是销售，执行力强，成交话术弱。

3. 记人脉
示例：王总懂本地生活投流，获客问题可以请教他。

4. 记任务
示例：提醒张三5月12日跟进李总。

5. 看今日简报
示例：今天有什么要跟进的？

你只需要用自然语言告诉我，比如：
「帮我诊断一下，我做建材加盟，预算客户多但成交少」
「帮我记一下，刘总是客户，做建材加盟，预算15万」
「今天有什么要跟进的？」

想看更详细说明，可以输入：帮助 或 Help。
授权版会开放更强的老板秘书判断、行业打法、客户跟进策略、团队诊断和持续学习知识库。
授权联系 Telegram: fanfans555；微信号: fanfans555"""


def help_text():
    return """BossSkill 详细帮助

你可以把我当成两个角色：
1. 老板顾问：帮你诊断项目、获客、成交、交付、团队和管理问题。
2. 老板秘书：帮你记录客户、员工、人脉、任务，并生成今日简报。

一、先做项目诊断
你可以说：
- 我做餐饮加盟，客户是想开店的创业者，有咨询但成交少，帮我诊断。
- 我做企业服务，线索不少但回款慢，问题在哪里？
- 我准备创业，想做本地生活服务，你帮我判断是否可行。

二、记录客户
你可以说：
- 李总是客户，做餐饮加盟，预算5万，5月12日跟进。
- 刘总是客户，做建材加盟，预算15万，关心回本周期。
- 李总生日5月14日，喜欢喝茶。

三、记录员工
你可以说：
- 张三是销售，执行力强，成交话术弱。
- 小王是运营，负责短视频，选题能力强，但复盘不稳定。

四、记录人脉
你可以说：
- 王总懂本地生活投流，获客问题可以请教他。
- 赵律师是朋友，合同问题可以咨询。
- 王总生日8月20日，喜欢打高尔夫。

五、记录任务
你可以说：
- 提醒张三5月12日跟进李总。
- 明天提醒我看本周销售数据。

六、查看简报
你可以说：
- 今天有什么要跟进的？
- 今天有哪些待办？
- 帮我生成今日老板简报。
- 生日前三天会在今日简报里提醒你准备祝福或维护动作。

七、授权版能做什么
授权后可以使用：
- 行业深度作战包
- 客户跟进策略和话术
- 团队诊断和用人建议
- 经营指标诊断
- 任务复盘自动追问
- 长期知识库沉淀

授权联系 Telegram: fanfans555；微信号: fanfans555"""


def insert_record(db, table, values):
    keys = list(values.keys())
    placeholders = ", ".join(["?"] * len(keys))
    with sqlite3.connect(db) as conn:
        cursor = conn.execute(
            f"INSERT INTO {table} ({', '.join(keys)}) VALUES ({placeholders})",
            [values[key] for key in keys],
        )
        conn.commit()
        return cursor.lastrowid


def add_customer(db, args):
    record_id = insert_record(db, "customers", {
        "name": args.name,
        "owner": args.owner or "",
        "status": args.status or "",
        "notes": args.text or "",
        "next_followup": args.next_followup or "",
        "created_at": today(),
        "updated_at": today(),
    })
    return {
        "created": "customer",
        "id": record_id,
        "next_step": "如果知道客户生日、爱好、预算、关键顾虑，可以继续补充，后续跟进会更精准。",
    }


def add_team_member(db, args):
    record_id = insert_record(db, "team_members", {
        "name": args.name,
        "role": args.role or "",
        "notes": args.text or "",
        "created_at": today(),
        "updated_at": today(),
    })
    return {
        "created": "team_member",
        "id": record_id,
        "next_step": "建议补充这个人的强项、短板、最近任务结果，方便后续做团队诊断。",
    }


def add_contact(db, args):
    record_id = insert_record(db, "contacts", {
        "name": args.name,
        "relation_type": args.relation_type or "",
        "notes": args.text or "",
        "created_at": today(),
        "updated_at": today(),
    })
    return {
        "created": "contact",
        "id": record_id,
        "next_step": "建议补充对方能帮什么、你需要如何维护关系、生日或联系禁忌。",
    }


def add_task(db, args):
    record_id = insert_record(db, "tasks", {
        "title": args.title,
        "owner": args.owner or "",
        "due_date": args.due_date or "",
        "status": args.status or "todo",
        "notes": args.text or "",
        "created_at": today(),
        "updated_at": today(),
    })
    return {"created": "task", "id": record_id, "next_step": "任务完成后请记录结果，系统才能帮你复盘。"}


def list_table(db, table):
    allowed = {"projects", "team_members", "customers", "contacts", "tasks"}
    if table not in allowed:
        return {"error": "unsupported_table", "allowed": sorted(allowed)}
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute(f"SELECT * FROM {table} ORDER BY id DESC LIMIT 50").fetchall()]


def detect_name(text):
    identity_match = re.search(r"([\u4e00-\u9fa5A-Za-z]{1,8})是(?:客户|员工|销售|运营|朋友|人脉|同学|合作伙伴)", text)
    if identity_match:
        return identity_match.group(1)
    match = re.search(r"([\u4e00-\u9fa5A-Za-z]{1,8}(?:总|经理|老师|哥|姐|先生|女士)?)", text)
    return match.group(1) if match else ""


def detect_date(text):
    text_without_birthday = re.sub(r"(?:生日|结婚纪念日|合作周年|签约日|孩子生日|公司成立日|开业日|纪念日)[是:： ]*(20\d{2}-)?\d{1,2}[-月]\d{1,2}日?", "", text or "")
    iso = re.search(r"(20\d{2}-\d{1,2}-\d{1,2})", text)
    if iso:
        return iso.group(1)
    month_day = re.search(r"(\d{1,2})月(\d{1,2})日", text_without_birthday)
    if month_day:
        return f"{date.today().year}-{int(month_day.group(1)):02d}-{int(month_day.group(2)):02d}"
    return ""


def detect_birthday(text):
    if not text or "生日" not in text:
        return ""
    iso = re.search(r"生日[是:： ]*(20\d{2}-)?(\d{1,2})[-月](\d{1,2})日?", text)
    if iso:
        return f"{int(iso.group(2)):02d}-{int(iso.group(3)):02d}"
    month_day = re.search(r"生日[是:： ]*(\d{1,2})月(\d{1,2})日?", text)
    if month_day:
        return f"{int(month_day.group(1)):02d}-{int(month_day.group(2)):02d}"
    return ""


def days_until_month_day(month_day, today_value):
    try:
        month, day = [int(part) for part in month_day.split("-", 1)]
        target = date(today_value.year, month, day)
    except ValueError:
        return None
    if target < today_value:
        target = date(today_value.year + 1, month, day)
    return (target - today_value).days


def birthday_reminders(data, today_value):
    reminders = []
    sources = [
        ("customer", "客户", data["customers"]),
        ("team_member", "员工", data["team_members"]),
        ("contact", "人脉", data["contacts"]),
    ]
    for source_type, source_label, rows in sources:
        for row in rows:
            birthday = detect_birthday(" ".join([row.get("notes", ""), row.get("status", ""), row.get("relation_type", "")]))
            days_left = days_until_month_day(birthday, today_value) if birthday else None
            if days_left is None or days_left > 3:
                continue
            if days_left == 0:
                timing = "今天生日"
                action = f"今天给{row.get('name')}发一句生日祝福，最好结合你们的关系和最近业务进展。"
            else:
                timing = f"距离生日还有{days_left}天"
                action = f"提前准备{row.get('name')}的生日祝福或维护动作。"
            reminders.append({
                "type": source_type,
                "role": source_label,
                "name": row.get("name"),
                "birthday": birthday,
                "days_left": days_left,
                "timing": timing,
                "suggested_action": action,
                "script": f"{row.get('name')}，生日快乐！祝你新的一年顺顺利利，最近有需要我帮忙的地方也随时跟我说。",
            })
    return sorted(reminders, key=lambda item: item["days_left"])


def detect_important_dates(text):
    events = []
    labels = ["结婚纪念日", "合作周年", "签约日", "孩子生日", "公司成立日", "开业日", "纪念日"]
    for label in labels:
        pattern = rf"{label}[是:： ]*(20\d{{2}}-)?(\d{{1,2}})[-月](\d{{1,2}})日?"
        for match in re.finditer(pattern, text or ""):
            event = {
                "event": label,
                "date": f"{int(match.group(2)):02d}-{int(match.group(3)):02d}",
            }
            if event not in events:
                events.append(event)
    specific_events = [item for item in events if item["event"] != "纪念日"]
    if specific_events:
        specific_dates = {item["date"] for item in specific_events}
        events = [item for item in events if item["event"] != "纪念日" or item["date"] not in specific_dates]
    return events


def important_date_reminders(data, today_value):
    reminders = []
    sources = [
        ("customer", "客户", data["customers"]),
        ("team_member", "员工", data["team_members"]),
        ("contact", "人脉", data["contacts"]),
    ]
    for source_type, source_label, rows in sources:
        for row in rows:
            text = " ".join([row.get("notes", ""), row.get("status", ""), row.get("relation_type", "")])
            for event in detect_important_dates(text):
                days_left = days_until_month_day(event["date"], today_value)
                if days_left is None or days_left > 3:
                    continue
                name = row.get("name")
                reminders.append({
                    "type": source_type,
                    "role": source_label,
                    "name": name,
                    "event": event["event"],
                    "date": event["date"],
                    "days_left": days_left,
                    "timing": f"今天是{event['event']}" if days_left == 0 else f"距离{event['event']}还有{days_left}天",
                    "suggested_action": f"给{name}准备一条围绕{event['event']}的问候，不要推销，先维护关系。",
                    "script": f"{name}，刚想起快到{event['event']}了，祝你这段时间一切顺利。有需要我搭把手的地方也随时说。",
                })
    return sorted(reminders, key=lambda item: item["days_left"])


def silent_customer_reminders(customers):
    keywords = ["沉默", "没回", "不回", "联系不上", "失联", "未回复"]
    reminders = []
    for customer in customers:
        text = " ".join([customer.get("status", ""), customer.get("notes", "")])
        if any(word in text for word in keywords):
            name = customer.get("name")
            reminders.append({
                "name": name,
                "reason": "客户近期反馈变少或未回复",
                "next_action": "今天只做低压力触达，先关心近况，再给一个明确的小问题。",
                "script": f"{name}您好，我先不打扰您太久。之前那个事情您现在是想继续了解，还是先放一放？我这边好按您的节奏安排。",
            })
    return reminders[:5]


def relationship_maintenance_reminders(data):
    keywords = ["重要", "高价值", "关键", "核心", "VIP", "老客户"]
    reminders = []
    for customer in data["customers"]:
        text = " ".join([customer.get("status", ""), customer.get("notes", "")])
        if any(word in text for word in keywords) and not customer.get("next_followup"):
            reminders.append({
                "type": "customer",
                "name": customer.get("name"),
                "reason": "重要客户未设置下次跟进时间",
                "suggested_action": "建议设置 30 天内的维护任务，并补充最近需求变化。",
            })
    for contact in data["contacts"]:
        text = " ".join([contact.get("relation_type", ""), contact.get("notes", "")])
        if any(word in text for word in keywords):
            reminders.append({
                "type": "contact",
                "name": contact.get("name"),
                "reason": "重要人脉建议定期维护",
                "suggested_action": "建议 30 天维护一次：问近况、给价值、必要时再请教具体问题。",
            })
    return reminders[:5]


def one_on_one_reminders(team_members):
    keywords = ["逾期", "不稳定", "弱", "低", "拖延", "情绪", "冲突", "复盘不稳定"]
    reminders = []
    for member in team_members:
        text = " ".join([member.get("role", ""), member.get("notes", "")])
        if any(word in text for word in keywords):
            name = member.get("name")
            reminders.append({
                "name": name,
                "reason": "员工画像里出现执行、能力或状态风险",
                "suggested_action": "安排一次 15 分钟一对一，只谈一个问题、一个标准、一个下次动作。",
                "talk_outline": [
                    f"先问{name}：最近哪个动作最卡？",
                    "再确认：你希望公司给什么支持？",
                    "最后定：下次复盘看哪个具体结果？",
                ],
            })
    return reminders[:5]


def greeting_templates():
    return [
        {
            "scene": "节日问候",
            "script": "最近节奏应该也挺满的，祝你节日顺心，工作和生活都稳稳当当。有需要我帮忙的地方随时说。",
        },
        {
            "scene": "客户维护",
            "script": "最近项目推进还顺利吗？我这边想顺手问一句，有没有哪个环节需要我帮你看一下。",
        },
        {
            "scene": "人脉请教",
            "script": "最近我遇到一个具体问题，想请教你 10 分钟。方便的话我把问题整理成三句话发你，不耽误你太多时间。",
        },
    ]


def find_helper(db, keyword):
    data = export_data(db)
    keyword = (keyword or "").strip()
    matches = []
    for contact in data["contacts"]:
        haystack = " ".join([contact.get("name", ""), contact.get("relation_type", ""), contact.get("notes", "")])
        if not keyword or keyword in haystack:
            matches.append({
                "id": contact.get("id"),
                "name": contact.get("name"),
                "relation_type": contact.get("relation_type"),
                "matched_by": keyword or "all",
                "notes": contact.get("notes"),
                "suggested_action": "先发近况问候，再提出一个具体、低成本的协助请求。",
            })
    return {"keyword": keyword, "matches": matches[:10]}


def quick_add(db, text):
    name = detect_name(text)
    due_date = detect_date(text)
    if any(word in text for word in ["提醒", "任务", "安排"]):
        title = text
        owner_match = re.search(r"提醒([\u4e00-\u9fa5A-Za-z]{1,8})", text)
        args = argparse.Namespace(title=title, owner=owner_match.group(1) if owner_match else "", due_date=due_date, status="todo", text=text)
        result = add_task(db, args)
        result["detected_type"] = "task"
        result["confidence"] = "medium"
        return result
    if any(word in text for word in ["员工", "销售", "运营", "组长", "客服", "导师"]):
        role = next((word for word in ["销售", "运营", "组长", "客服", "导师"] if word in text), "")
        args = argparse.Namespace(name=name or "未命名员工", role=role, text=text)
        result = add_team_member(db, args)
        result["detected_type"] = "team_member"
        result["confidence"] = "medium"
        return result
    if any(word in text for word in ["朋友", "人脉", "资源", "同学", "合作伙伴"]):
        relation = next((word for word in ["朋友", "人脉", "同学", "合作伙伴"] if word in text), "人脉")
        args = argparse.Namespace(name=name or "未命名人脉", relation_type=relation, text=text)
        result = add_contact(db, args)
        result["detected_type"] = "contact"
        result["confidence"] = "medium"
        return result
    if any(word in text for word in ["客户", "预算", "意向", "成交", "报价", "方案", "跟进"]):
        status = "高意向" if any(word in text for word in ["高意向", "想买", "要买", "成交"]) else ""
        args = argparse.Namespace(name=name or "未命名客户", owner="", status=status, next_followup=due_date, text=text)
        result = add_customer(db, args)
        result["detected_type"] = "customer"
        result["confidence"] = "medium"
        return result
    return {
        "intent": "need_clarification",
        "question": "这是客户、员工、任务，还是其他人脉？",
        "text": text,
        "tip": "你可以补一句：这是客户 / 这是员工 / 这是人脉 / 这是任务。",
    }


def priority_customer(customer):
    score = 0
    reasons = []
    if customer.get("next_followup") and customer["next_followup"] <= today():
        score += 3
        reasons.append("跟进已到期")
    if "高" in customer.get("status", ""):
        score += 2
        reasons.append("意向较高")
    if "预算" in customer.get("notes", ""):
        score += 1
        reasons.append("已有预算信息")
    return score, reasons


def local_daily_brief(db):
    data = export_data(db)
    today_value = date.today()
    today_text = today_value.isoformat()
    due_tasks = [
        task for task in data["tasks"]
        if task.get("status") != "done" and task.get("due_date") and task.get("due_date") <= today_text
    ]
    followups = [
        customer for customer in data["customers"]
        if customer.get("next_followup") and customer.get("next_followup") <= today_text
    ]
    ranked_customers = sorted(
        [
            {
                **customer,
                "priority_score": priority_customer(customer)[0],
                "priority_reason": priority_customer(customer)[1],
                "next_action": f"今天联系{customer.get('name')}，确认当前顾虑、预算和下一步决策时间。",
                "suggested_script": f"{customer.get('name')}您好，我今天主要想确认下您现在最关心的是预算、效果还是落地周期？我根据这个给您安排下一步方案。",
            }
            for customer in data["customers"]
        ],
        key=lambda item: item["priority_score"],
        reverse=True,
    )
    return {
        "title": "BossSkill 今日老板简报",
        "today": today_text,
        "summary": f"当前有 {len(due_tasks)} 个到期任务，{len(followups)} 个到期客户跟进。",
        "today_priority": ranked_customers[:3],
        "due_tasks": due_tasks,
        "birthday_reminders": birthday_reminders(data, today_value),
        "important_date_reminders": important_date_reminders(data, today_value),
        "silent_customer_reminders": silent_customer_reminders(data["customers"]),
        "relationship_maintenance": relationship_maintenance_reminders(data),
        "one_on_one_reminders": one_on_one_reminders(data["team_members"]),
        "greeting_templates": greeting_templates(),
        "counts": {
            "customers": len(data["customers"]),
            "team_members": len(data["team_members"]),
            "contacts": len(data["contacts"]),
            "tasks": len(data["tasks"]),
        },
        "suggested_action": [
            "先处理今日到期客户，再处理到期任务。",
            "如果有生日或纪念日提醒，提前准备祝福或维护动作。",
            "重要客户和重要人脉没有下次动作时，今天先补一个维护任务。",
            "每次跟进后记录客户反馈、顾虑、下次时间。",
            "如果客户、员工或人脉信息缺失，今天只补一个最关键字段。",
        ],
        "upgrade_preview": commercial_preview("daily-brief"),
    }


def commercial_preview(command):
    examples = {
        "assistant-action": "授权版示例：我会自动判断这句话是在建客户、建任务还是做复盘，并生成下一步动作、跟进话术和是否需要提醒。",
        "industry-playbook": "授权版示例：如果你做餐饮加盟，我会输出7天获客动作、客户筛选问题、跟进话术和成交复盘表。",
        "team-brief": "授权版示例：我会根据员工任务结果判断谁需要授权、谁需要训练、谁需要一对一沟通。",
    }
    return {
        "message": examples.get(command, "授权版会生成更完整的诊断、话术、任务和复盘方案。"),
        "commercial_modules": [
            "经营判断系统",
            "主动秘书",
            "优秀级主动秘书",
            "行业深度作战包",
            "长期记忆",
            "任务结果闭环",
            "客户经营",
            "团队用人建议",
            "老板操作系统",
            "商业交付体系",
            "经营智能体内核V1",
        ],
        "boundary": "免费版负责记录、查看、导出和基础提醒；商业版负责诊断、决策、策略、主动扫描、主动追问、跨模块诊断、行业包和长期学习。",
        "contact": "Telegram: fanfans555；微信号: fanfans555",
        "activate_command": "python scripts\\startup_os_db.py activate-license --db startup_os.sqlite3 --license-key YOUR_LICENSE_KEY",
    }


def industry_examples(keyword):
    if not keyword:
        return INDUSTRY_EXAMPLES
    matched = {name: items for name, items in INDUSTRY_EXAMPLES.items() if keyword in name}
    return matched or {"未匹配": ["可以告诉我行业名称，我会按客户、销售、交付、团队四块给你拆问题。"]}


def license_required(command):
    return {
        "intent": "license_required",
        "command": command,
        "message": "这个能力属于授权版。免费版可使用 quick-add、add-customer、add-team-member、add-contact、add-task、daily-brief 和 export。",
        "preview": commercial_preview(command),
    }


def main():
    parser = argparse.ArgumentParser(description="BossSkill cloud client")
    parser.add_argument("command")
    parser.add_argument("--db", default="startup_os.sqlite3")
    parser.add_argument("--license-key")
    parser.add_argument("--text")
    parser.add_argument("--name")
    parser.add_argument("--owner")
    parser.add_argument("--status")
    parser.add_argument("--next-followup")
    parser.add_argument("--role")
    parser.add_argument("--relation-type")
    parser.add_argument("--title")
    parser.add_argument("--due-date")
    parser.add_argument("--table")
    parser.add_argument("--industry")
    parser.add_argument("--keyword")
    args = parser.parse_args()
    init_db(args.db)
    if args.command == "init":
        print(f"initialized {args.db}")
        return
    if args.command in {"first-use-guide", "guide"}:
        print(first_use_guide())
        return
    if args.command in {"help", "Help", "HELP", "帮助", "幫助"}:
        print(help_text())
        return
    if args.command == "activate-license":
        require_args(args, ["license_key"])
        print_json(activate_license(args.db, args.license_key))
        return
    if args.command == "license-status":
        print_json(check_license(args.db, "status"))
        return
    if args.command == "export":
        print_json(export_data(args.db))
        return
    if args.command == "quick-add":
        require_args(args, ["text"])
        print_json(quick_add(args.db, args.text))
        return
    if args.command == "add-customer":
        require_args(args, ["name"])
        print_json(add_customer(args.db, args))
        return
    if args.command == "add-team-member":
        require_args(args, ["name"])
        print_json(add_team_member(args.db, args))
        return
    if args.command == "add-contact":
        require_args(args, ["name"])
        print_json(add_contact(args.db, args))
        return
    if args.command == "add-task":
        require_args(args, ["title"])
        print_json(add_task(args.db, args))
        return
    if args.command == "list":
        print_json(list_table(args.db, args.table or "customers"))
        return
    if args.command in {"daily-brief", "brief"}:
        print_json(local_daily_brief(args.db))
        return
    if args.command in {"find-helper", "find-contact"}:
        print_json(find_helper(args.db, args.keyword or args.text or ""))
        return
    if args.command == "industry-examples":
        print_json(industry_examples(args.industry or ""))
        return
    if not check_license(args.db, args.command).get("allowed"):
        print_json(license_required(args.command))
        return
    response = run_cloud_core(args.command, args.db, args)
    print(response.get("output") or json.dumps(response, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
