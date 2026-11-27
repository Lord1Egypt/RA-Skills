#!/usr/bin/env python3
"""宝宝成长数据 CLI - Skill 的数据层与计算引擎。

纯本地运行，不依赖 Flutter App、不联网、不调用任何后端。
数据默认存于 ~/.workbuddy/baby-growth/data.json，可用 --data 或
环境变量 BABY_GROWTH_DATA 覆盖。每次写入前自动生成 .bak 备份。
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import date, datetime
from pathlib import Path

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS = SKILL_DIR / "assets"
DEFAULT_DATA = Path.home() / ".workbuddy" / "baby-growth" / "data.json"

NUTRIENTS = ["kcal", "protein", "iron", "calcium", "vitaminA", "vitaminC"]
LABELS = {
    "kcal": "热量", "protein": "蛋白质", "iron": "铁",
    "calcium": "钙", "vitaminA": "维生素A", "vitaminC": "维生素C",
}
UNITS = {
    "kcal": "kcal", "protein": "g", "iron": "mg",
    "calcium": "mg", "vitaminA": "μg", "vitaminC": "mg",
}
MEAL_TYPES = ["breakfast", "lunch", "dinner", "snack"]
TYPE_LABELS = {"breakfast": "早餐", "lunch": "午餐", "dinner": "晚餐", "snack": "加餐"}
SIZE_LABELS = {"small": "偏小（低于P3）", "normal": "正常（P3~P97）", "large": "偏大（高于P97）"}
FOOD_SUGGESTIONS = {
    "kcal": "可适当增加主食（米饭/面条）或红薯",
    "protein": "建议加个鸡蛋或一点瘦肉、鱼",
    "iron": "建议搭配瘦肉、猪肝（每周1-2次）或菠菜",
    "calcium": "建议增加牛奶、酸奶、豆腐",
    "vitaminA": "建议吃胡萝卜、南瓜、西兰花",
    "vitaminC": "建议吃橙子、猕猴桃、草莓",
}
DISCLAIMER = "数据为常见食材近似值，建议由本地规则生成，仅供参考，不构成医疗诊断；特殊情况请咨询医生或营养师。"


# ---------- 基础工具 ----------

def resolve_data_path(args):
    return Path(args.data) if getattr(args, "data", None) else Path(
        os.environ.get("BABY_GROWTH_DATA", str(DEFAULT_DATA))
    )


def empty_doc():
    return {
        "app": "baby_growth_skill",
        "formatVersion": 1,
        "exportedAt": datetime.now().isoformat(timespec="seconds"),
        "babies": [],
        "meals": [],
        "growthRecords": [],
        "favoriteCombos": [],
        "reminders": [],
        "settings": [],
    }


def load_doc(path, required=True):
    if not path.exists():
        if required:
            raise RuntimeError(
                f"数据文件不存在：{path}\n先执行 init 创建，或用 import-backup 从 App 备份迁移。"
            )
        return empty_doc()
    return json.loads(path.read_text(encoding="utf-8"))


def save_doc(doc, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        shutil.copy2(path, path.with_suffix(".json.bak"))
    doc["exportedAt"] = datetime.now().isoformat(timespec="seconds")
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def load_assets():
    foods = json.loads((ASSETS / "food_table.json").read_text(encoding="utf-8"))
    growth = json.loads((ASSETS / "growth_standards.json").read_text(encoding="utf-8"))
    return foods, growth


def food_index(food_doc):
    return {f["id"]: f for f in food_doc["foods"]}


def parse_dt(value):
    s = str(value).strip().replace("Z", "")
    return datetime.fromisoformat(s)


def parse_day(value):
    if not value:
        return date.today()
    return date.fromisoformat(value)


def day_of(meal):
    return parse_dt(meal["date"]).date().isoformat()


def iso_dt(day, use_now=False):
    t = datetime.now().time().replace(microsecond=0) if use_now else datetime.min.time().replace(hour=12)
    return datetime.combine(day, t).isoformat(timespec="milliseconds")


def fmt(value):
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.1f}"


def zeros():
    return {k: 0.0 for k in NUTRIENTS}


def next_id(items):
    return max((int(x.get("id") or 0) for x in items), default=0) + 1


def get_setting(doc, key, default=None):
    for row in doc.get("settings", []):
        if row.get("key") == key:
            return row.get("value")
    return default


def set_setting(doc, key, value):
    for row in doc.get("settings", []):
        if row.get("key") == key:
            row["value"] = str(value)
            return
    doc.setdefault("settings", []).append({"key": key, "value": str(value)})


def active_baby_id(doc):
    raw = get_setting(doc, "activeBabyId")
    try:
        return int(raw)
    except (TypeError, ValueError):
        return doc["babies"][0]["id"] if doc.get("babies") else None


def get_baby(doc, baby_id=None):
    bid = baby_id or active_baby_id(doc)
    for b in doc.get("babies", []):
        if int(b["id"]) == int(bid):
            return b
    return None


def require_baby(doc, baby_id=None):
    b = get_baby(doc, baby_id)
    if b is None:
        raise RuntimeError("没有找到宝宝档案。先执行 add-baby，或 import-backup 迁移数据。")
    return b


def age_in_months(baby, at=None):
    at = at or date.today()
    birth = parse_dt(baby["birthDate"]).date()
    months = (at.year - birth.year) * 12 + at.month - birth.month
    if at.day < birth.day:
        months -= 1
    return max(0, months)


# ---------- 计算引擎 ----------

def base_target(months):
    if months < 24:
        return dict(kcal=1100.0, protein=35.0, iron=10.0, calcium=600.0, vitaminA=400.0, vitaminC=40.0)
    return dict(kcal=1250.0, protein=40.0, iron=12.0, calcium=600.0, vitaminA=400.0, vitaminC=45.0)


def target_for(baby, at=None):
    t = base_target(age_in_months(baby, at))
    if baby.get("sizeStatus") == "small":
        t["kcal"] *= 1.10
        t["protein"] *= 1.10
    elif baby.get("sizeStatus") == "large":
        t["kcal"] *= 0.95
    weight = float(baby.get("weightKg") or 0)
    if weight < 10:
        t["kcal"] *= 1.05
    elif weight > 16:
        t["kcal"] *= 0.95
    if int(baby.get("ironRisk") or 0):
        t["iron"] *= 1.20
    return t


def decode_foods(meal):
    raw = meal.get("foodsJson") or "[]"
    try:
        data = json.loads(raw) if isinstance(raw, str) else raw
    except (json.JSONDecodeError, TypeError):
        return []
    out = []
    for item in data:
        try:
            out.append((str(item["foodId"]), float(item["grams"])))
        except (KeyError, TypeError, ValueError):
            continue
    return out


def nutrient_of_meal(meal, index):
    n = zeros()
    for fid, grams in decode_foods(meal):
        f = index.get(fid)
        if f is None or grams <= 0:
            continue
        for k in NUTRIENTS:
            n[k] += float(f[k]) * grams / 100.0
    n["vitaminA"] += float(meal.get("vitaminASupplement") or 0)
    n["vitaminC"] += float(meal.get("vitaminCSupplement") or 0)
    return n


def meals_on(doc, day, baby_id):
    key = day.isoformat()
    return [
        m for m in doc.get("meals", [])
        if day_of(m) == key and int(m.get("babyId") or 1) == int(baby_id)
    ]


def intake_on(doc, day, baby_id, index):
    total = zeros()
    for m in meals_on(doc, day, baby_id):
        part = nutrient_of_meal(m, index)
        for k in NUTRIENTS:
            total[k] += part[k]
    return total


def level_of(ratio):
    if ratio < 0.6:
        return "low"
    if ratio > 1.3:
        return "high"
    return "good"


def allergy_warnings(baby):
    raw = str(baby.get("allergies") or "").strip()
    if not raw:
        return []
    parts = [s for s in re.split(r"[,，、\s]+", raw) if s]
    return [f"已标记过敏：{s}，制作辅食时请避开" for s in parts]


def who_range(growth, gender, month, metric):
    prefix = "girl" if gender == "female" else "boy"
    suffix = "Height" if metric == "height" else "Weight"
    m = max(0, min(36, int(month)))
    return (
        growth["series"][f"{prefix}{suffix}P3"][m],
        growth["series"][f"{prefix}{suffix}P97"][m],
    )


def classify_size(growth, gender, month, height, weight):
    hp3, hp97 = who_range(growth, gender, month, "height")
    wp3, wp97 = who_range(growth, gender, month, "weight")
    if height < hp3 or weight < wp3:
        return "small"
    if height > hp97 or weight > wp97:
        return "large"
    return "normal"


# ---------- 命令 ----------

def cmd_init(args, doc, path, foods, growth, index):
    if path.exists() and not args.force:
        raise RuntimeError(f"数据文件已存在：{path}（如需重建加 --force，旧文件会先备份为 .bak）")
    save_doc(empty_doc(), path)
    print(f"已创建空数据文件：{path}")
    print("下一步：add-baby 新建档案，或 import-backup 从 App 备份迁移。")


def cmd_import_backup(args, doc, path, foods, growth, index):
    src = Path(args.file)
    had_existing = path.exists()
    incoming = json.loads(src.read_text(encoding="utf-8"))
    if not isinstance(incoming, dict) or not isinstance(incoming.get("babies"), list):
        raise RuntimeError("备份格式不合法：应为含 babies 数组的 JSON 对象")
    if incoming.get("app") not in ("baby_nutrition", "baby_growth_skill"):
        print(f"提示：app 标识为 {incoming.get('app')!r}，仍按兼容格式导入。")
    incoming["app"] = "baby_growth_skill"
    for key in ("meals", "growthRecords", "favoriteCombos", "reminders", "settings"):
        incoming.setdefault(key, [])
    if path.exists() and not args.replace:
        existing = load_doc(path)
        for key in ("babies", "meals", "growthRecords", "favoriteCombos"):
            seen = {int(x.get("id") or 0) for x in existing.get(key, [])}
            added = 0
            for row in incoming.get(key, []):
                if int(row.get("id") or 0) not in seen:
                    existing.setdefault(key, []).append(row)
                    seen.add(int(row.get("id") or 0))
                    added += 1
            print(f"合并 {key}: 新增 {added} 条")
        save_doc(existing, path)
    else:
        save_doc(incoming, path)
        print(f"已导入：{len(incoming.get('babies', []))} 个宝宝 / "
              f"{len(incoming.get('meals', []))} 条餐次 / "
              f"{len(incoming.get('growthRecords', []))} 条成长记录")
    print(f"数据文件：{path}" + ("（旧文件已备份为 .bak）" if had_existing else ""))


def cmd_status(args, doc, path, foods, growth, index):
    print(f"数据文件：{path}")
    print(f"app={doc.get('app')}  formatVersion={doc.get('formatVersion')}  更新于 {doc.get('exportedAt')}")
    print(f"宝宝 {len(doc.get('babies', []))} 个 | 餐次 {len(doc.get('meals', []))} 条 | "
          f"成长记录 {len(doc.get('growthRecords', []))} 条 | 提醒 {len(doc.get('reminders', []))} 条")
    b = get_baby(doc)
    if b:
        print(f"当前宝宝：#{b['id']} {b['name']}（{b.get('gender', 'male')}，"
              f"{age_in_months(b)} 月龄，{fmt(float(b['heightCm']))}cm / {fmt(float(b['weightKg']))}kg）")
    else:
        print("当前宝宝：无（先 add-baby）")


def cmd_babies(args, doc, path, foods, growth, index):
    if not doc.get("babies"):
        print("暂无宝宝档案。")
        return
    cur = active_baby_id(doc)
    for b in doc["babies"]:
        mark = " ←当前" if int(b["id"]) == cur else ""
        print(f"#{b['id']} {b['name']}{mark} | {b.get('gender', 'male')} | "
              f"生日 {str(b['birthDate'])[:10]} | {age_in_months(b)} 月龄 | "
              f"{fmt(float(b['heightCm']))}cm / {fmt(float(b['weightKg']))}kg | "
              f"个头 {SIZE_LABELS.get(b.get('sizeStatus', 'normal'), b.get('sizeStatus'))} | "
              f"缺铁风险 {'是' if int(b.get('ironRisk') or 0) else '否'} | "
              f"过敏 {b.get('allergies') or '无'}")


def cmd_add_baby(args, doc, path, foods, growth, index):
    birth = date.fromisoformat(args.birth)
    baby = {
        "id": next_id(doc.get("babies", [])),
        "name": args.name,
        "gender": args.gender,
        "birthDate": iso_dt(birth),
        "heightCm": float(args.height),
        "weightKg": float(args.weight),
        "allergies": args.allergies or "",
        "sizeStatus": args.size_status,
        "sizeStatusManual": 1 if args.manual_size else 0,
        "ironRisk": 1 if args.iron_risk else 0,
    }
    doc.setdefault("babies", []).append(baby)
    set_setting(doc, "activeBabyId", baby["id"])
    save_doc(doc, path)
    print(f"已建档 #{baby['id']} {baby['name']}，并设为当前宝宝。")


def cmd_switch(args, doc, path, foods, growth, index):
    b = get_baby(doc, args.id)
    if b is None:
        raise RuntimeError(f"不存在宝宝 #{args.id}")
    set_setting(doc, "activeBabyId", b["id"])
    save_doc(doc, path)
    print(f"已切换到 #{b['id']} {b['name']}")


def cmd_foods(args, doc, path, foods, growth, index):
    print("食材营养表（每 100g）：kcal / 蛋白质g / 铁mg / 钙mg / 维Aμg / 维Cmg")
    for f in foods["foods"]:
        if args.category and f["category"] != args.category:
            continue
        if args.search and args.search not in f["id"] and args.search not in f["name"]:
            continue
        print(f"{f['id']:<14} {f['name']:<8} {f['category']:<5} "
              f"{fmt(f['kcal']):>5} / {fmt(f['protein']):>5} / {fmt(f['iron']):>5} / "
              f"{fmt(f['calcium']):>5} / {fmt(f['vitaminA']):>6} / {fmt(f['vitaminC']):>4}")


def cmd_add_meal(args, doc, path, foods, growth, index):
    baby = require_baby(doc, args.baby_id)
    day = parse_day(args.date)
    items = []
    for raw in args.food or []:
        if ":" not in raw:
            raise RuntimeError(f"食物格式应为 id:克重，收到 {raw!r}（用 foods 查 id）")
        fid, grams = raw.rsplit(":", 1)
        if fid not in index:
            raise RuntimeError(f"未知食物 id {fid!r}，用 foods 查可用 id")
        grams = float(grams)
        if grams <= 0:
            raise RuntimeError("克重必须大于 0")
        items.append({"foodId": fid, "grams": grams})
    va = float(args.va or 0)
    vc = float(args.vc or 0)
    if not items and va <= 0 and vc <= 0:
        raise RuntimeError("至少要有一种食物或补充剂")
    if va < 0 or vc < 0:
        raise RuntimeError("补充剂不能为负数")
    meal = {
        "id": next_id(doc.get("meals", [])),
        "babyId": baby["id"],
        "mealType": args.type,
        "date": iso_dt(day, use_now=(args.date is None)),
        "foodsJson": json.dumps(items, ensure_ascii=False, separators=(",", ":")),
        "photoPath": None,
        "note": args.note or "",
        "vitaminASupplement": va,
        "vitaminCSupplement": vc,
    }
    doc.setdefault("meals", []).append(meal)
    save_doc(doc, path)
    detail = "、".join(f"{index[i['foodId']]['name']} {fmt(i['grams'])}g" for i in items) or "无食物"
    print(f"已记录 #{meal['id']} {day.isoformat()} {TYPE_LABELS[args.type]}：{detail}")
    if va or vc:
        print(f"额外补充剂：维A {fmt(va)}μg / 维C {fmt(vc)}mg")
    if args.note:
        print(f"备注：{args.note}")


def cmd_meals(args, doc, path, foods, growth, index):
    baby = require_baby(doc, args.baby_id)
    rows = meals_on(doc, parse_day(args.date), baby["id"])
    print(f"{baby['name']} · {parse_day(args.date).isoformat()} 共 {len(rows)} 餐")
    for m in rows:
        items = decode_foods(m)
        detail = "、".join(
            f"{index.get(fid, {}).get('name', fid)} {fmt(g)}g" for fid, g in items
        ) or "无食物"
        print(f"#{m['id']} {TYPE_LABELS.get(m['mealType'], m['mealType'])} | {detail}")
        if float(m.get("vitaminASupplement") or 0) or float(m.get("vitaminCSupplement") or 0):
            print(f"    补充剂 维A {fmt(float(m.get('vitaminASupplement') or 0))}μg / "
                  f"维C {fmt(float(m.get('vitaminCSupplement') or 0))}mg")
        if m.get("note"):
            print(f"    备注：{m['note']}")


def cmd_del_meal(args, doc, path, foods, growth, index):
    before = len(doc.get("meals", []))
    doc["meals"] = [m for m in doc.get("meals", []) if int(m["id"]) != args.id]
    if len(doc["meals"]) == before:
        raise RuntimeError(f"不存在餐次 #{args.id}")
    save_doc(doc, path)
    print(f"已删除餐次 #{args.id}（删除前数据已备份为 .bak）")


def cmd_add_growth(args, doc, path, foods, growth, index):
    baby = require_baby(doc, args.baby_id)
    day = parse_day(args.date)
    rec = {
        "id": next_id(doc.get("growthRecords", [])),
        "babyId": baby["id"],
        "date": iso_dt(day),
        "heightCm": float(args.height),
        "weightKg": float(args.weight),
        "note": args.note or "",
    }
    if rec["heightCm"] <= 0 or rec["weightKg"] <= 0:
        raise RuntimeError("身高体重必须大于 0")
    doc.setdefault("growthRecords", []).append(rec)
    months = age_in_months(baby, day)
    status = classify_size(growth, baby.get("gender", "male"), months, rec["heightCm"], rec["weightKg"])
    if not int(baby.get("sizeStatusManual") or 0):
        baby["sizeStatus"] = status
    baby["heightCm"] = rec["heightCm"]
    baby["weightKg"] = rec["weightKg"]
    save_doc(doc, path)
    hp3, hp97 = who_range(growth, baby.get("gender", "male"), months, "height")
    wp3, wp97 = who_range(growth, baby.get("gender", "male"), months, "weight")
    print(f"已记录 #{rec['id']} {day.isoformat()}：身高 {fmt(rec['heightCm'])}cm / 体重 {fmt(rec['weightKg'])}kg")
    print(f"WHO {months} 月龄参考：身高 P3~P97 {fmt(hp3)}~{fmt(hp97)}cm，"
          f"体重 {fmt(wp3)}~{fmt(wp97)}kg → 判定 {SIZE_LABELS[status]}")
    if int(baby.get("sizeStatusManual") or 0):
        print("个头偏差为手动指定，未自动覆盖。")


def cmd_growth(args, doc, path, foods, growth, index):
    baby = require_baby(doc, args.baby_id)
    records = [r for r in doc.get("growthRecords", []) if int(r.get("babyId") or 1) == int(baby["id"])]
    records.sort(key=lambda r: str(r["date"]))
    latest = records[-1] if records else None
    h = float(latest["heightCm"]) if latest else float(baby["heightCm"])
    w = float(latest["weightKg"]) if latest else float(baby["weightKg"])
    months = age_in_months(baby)
    hp3, hp97 = who_range(growth, baby.get("gender", "male"), months, "height")
    wp3, wp97 = who_range(growth, baby.get("gender", "male"), months, "weight")
    status = classify_size(growth, baby.get("gender", "male"), months, h, w)
    print(f"{baby['name']}（{'女' if baby.get('gender') == 'female' else '男'}，{months} 月龄）")
    print(f"最新：身高 {fmt(h)}cm / 体重 {fmt(w)}kg"
          + (f"（{str(latest['date'])[:10]}）" if latest else "（来自档案）"))
    print(f"身高 P3~P97：{fmt(hp3)}~{fmt(hp97)}cm | 体重 P3~P97：{fmt(wp3)}~{fmt(wp97)}kg")
    print(f"自动判型：{SIZE_LABELS[status]} | 档案记录：{SIZE_LABELS.get(baby.get('sizeStatus', 'normal'))}")
    print(f"历史测量 {len(records)} 条：")
    for r in records[-10:]:
        print(f"  {str(r['date'])[:10]}  {fmt(float(r['heightCm']))}cm / {fmt(float(r['weightKg']))}kg"
              + (f"  {r['note']}" if r.get("note") else ""))
    print("注：WHO 标准适用于足月儿；早产儿需矫正月龄。仅供观察趋势，不是医学诊断。")


def cmd_intake(args, doc, path, foods, growth, index):
    baby = require_baby(doc, args.baby_id)
    day = parse_day(args.date)
    total = intake_on(doc, day, baby["id"], index)
    target = target_for(baby, day)
    print(f"{baby['name']} · {day.isoformat()} 摄入 vs 全天目标（目标为全天总量，不是累计到当前时刻）")
    print(f"{'营养素':<10}{'摄入':>10}{'目标':>10}{'达成率':>10}  等级")
    for k in NUTRIENTS:
        ratio = total[k] / target[k] if target[k] > 0 else 0
        lv = {"low": "偏低", "good": "达标", "high": "偏高"}[level_of(ratio)]
        over = f" 超出{round((ratio - 1) * 100)}%" if ratio > 1 else ""
        print(f"{LABELS[k]:<10}{fmt(total[k]) + UNITS[k]:>10}{fmt(target[k]) + UNITS[k]:>10}"
              f"{f'{ratio * 100:.0f}%':>10}  {lv}{over}")


def cmd_advice(args, doc, path, foods, growth, index):
    baby = require_baby(doc, args.baby_id)
    day = parse_day(args.date)
    total = intake_on(doc, day, baby["id"], index)
    target = target_for(baby, day)
    day_meals = meals_on(doc, day, baby["id"])
    lines = []
    for w in allergy_warnings(baby):
        lines.append(f"[提醒] {w}")
    if not day_meals:
        lines.append("[提醒] 今天还没有记录，先记一餐再来看建议吧")
    for k in NUTRIENTS:
        value, goal = total[k], target[k]
        ratio = value / goal if goal > 0 else 0
        head = f"{LABELS[k]}（{fmt(value)}/{fmt(goal)}{UNITS[k]}）"
        if ratio < 0.6:
            lines.append(f"[偏低] {head}偏少，{FOOD_SUGGESTIONS[k]}")
        elif ratio > 1.3:
            lines.append(f"[偏高] {head}偏高，注意别过量")
        else:
            lines.append(f"[达标] {head}达标")
    print(f"{baby['name']} · {day.isoformat()} 营养建议（阈值：<60% 提示补充，>130% 提示减量）")
    for line in lines:
        print(line)
    print(f"\n{DISCLAIMER}")


def cmd_sources(args, doc, path, foods, growth, index):
    baby = require_baby(doc, args.baby_id)
    day = parse_day(args.date)
    key = args.nutrient
    rows = meals_on(doc, day, baby["id"])
    grams_by_food, supplements = {}, 0.0
    for m in rows:
        for fid, grams in decode_foods(m):
            grams_by_food[fid] = grams_by_food.get(fid, 0.0) + grams
        if key == "vitaminA":
            supplements += float(m.get("vitaminASupplement") or 0)
        elif key == "vitaminC":
            supplements += float(m.get("vitaminCSupplement") or 0)
    items = []
    for fid, grams in grams_by_food.items():
        f = index.get(fid)
        if f is None:
            continue
        amount = float(f[key]) * grams / 100.0
        if amount > 0:
            items.append((f["name"], amount, f"吃了 {fmt(grams)}g"))
    if supplements > 0:
        items.append(("维生素补充剂", supplements, "额外补充（非食物）"))
    items.sort(key=lambda x: -x[1])
    total = sum(x[1] for x in items)
    print(f"{baby['name']} · {day.isoformat()} {LABELS[key]} 的今日实际来源（共 {fmt(total)}{UNITS[key]}）")
    if not items:
        print("今天还没有记录含该营养素的食物。")
        return
    for name, amount, detail in items:
        pct = amount / total * 100 if total else 0
        print(f"  {name:<12} {fmt(amount):>7}{UNITS[key]:<4} 占今日 {pct:.0f}%  {detail}")


def cmd_report(args, doc, path, foods, growth, index):
    baby = require_baby(doc, args.baby_id)
    days = args.days
    today = date.today()
    start = today.fromordinal(today.toordinal() - days + 1)
    target = target_for(baby, today)
    per_day, available = [], 0
    sums = zeros()
    for offset in range(days):
        day = date.fromordinal(start.toordinal() + offset)
        n = intake_on(doc, day, baby["id"], index)
        has = any(n[k] > 0 for k in ("kcal", "protein", "iron", "calcium"))
        if has:
            available += 1
            for k in NUTRIENTS:
                sums[k] += n[k]
        per_day.append((day, n, has))
    denom = available or 1
    avg = {k: sums[k] / denom for k in NUTRIENTS}
    lines = [
        f"# {baby['name']} 近 {days} 天营养报告",
        "",
        f"统计区间：{start.isoformat()} ~ {today.isoformat()}｜有记录天数：{available}/{days} 天",
        f"目标口径：{age_in_months(baby)} 月龄全天推荐量（含个头/体重/缺铁微调）",
        "",
        "| 营养素 | 日均摄入 | 全天目标 | 日均达成率 |",
        "|---|---:|---:|---:|",
    ]
    for k in NUTRIENTS:
        ratio = avg[k] / target[k] if target[k] > 0 else 0
        lines.append(f"| {LABELS[k]} | {fmt(avg[k])}{UNITS[k]} | {fmt(target[k])}{UNITS[k]} | {ratio * 100:.0f}% |")
    lines += ["", "| 日期 | 热量 | 蛋白质 | 铁 | 钙 |", "|---|---:|---:|---:|---:|"]
    for day, n, has in per_day:
        mark = "" if has else "（无记录）"
        lines.append(f"| {day.isoformat()}{mark} | {fmt(n['kcal'])} | {fmt(n['protein'])} | "
                     f"{fmt(n['iron'])} | {fmt(n['calcium'])} |")
    lines += ["", f"> {DISCLAIMER}", ""]
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"报告已写入：{Path(args.out).resolve()}")
    else:
        print(text)


def cmd_export(args, doc, path, foods, growth, index):
    out = Path(args.out) if args.out else Path.cwd() / f"baby_growth_backup_{datetime.now():%Y%m%d_%H%M}.json"
    copy = json.loads(json.dumps(doc, ensure_ascii=False))
    copy["app"] = "baby_nutrition" if args.for_app else "baby_growth_skill"
    copy["exportedAt"] = datetime.now().isoformat(timespec="seconds")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(copy, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已导出：{out.resolve()}")
    if args.for_app:
        print("格式已设为 App 备份（app=baby_nutrition），可在 App 的「数据管理」里导入。")
    else:
        print("这是 Skill 数据备份，可用于版本管理或二次导入。")


COMMANDS = {
    "init": (cmd_init, "创建空数据文件"),
    "import-backup": (cmd_import_backup, "从 App 备份 JSON 迁移数据"),
    "status": (cmd_status, "查看数据文件与当前宝宝"),
    "babies": (cmd_babies, "列出宝宝档案"),
    "add-baby": (cmd_add_baby, "新建宝宝档案"),
    "switch": (cmd_switch, "切换当前宝宝"),
    "foods": (cmd_foods, "查询食材表与食物 id"),
    "add-meal": (cmd_add_meal, "记录一餐"),
    "meals": (cmd_meals, "查看某日餐次"),
    "del-meal": (cmd_del_meal, "删除餐次"),
    "add-growth": (cmd_add_growth, "记录身高体重"),
    "growth": (cmd_growth, "WHO 生长曲线判型"),
    "intake": (cmd_intake, "当日摄入 vs 推荐量"),
    "advice": (cmd_advice, "生成营养建议"),
    "sources": (cmd_sources, "查看某营养素的今日食物来源"),
    "report": (cmd_report, "生成近 7/30 天报告"),
    "export": (cmd_export, "导出 JSON 备份"),
}


def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--data", help="数据文件路径（默认 ~/.workbuddy/baby-growth/data.json）")
    p = argparse.ArgumentParser(
        prog="baby.py",
        description="宝宝成长数据维护 CLI（纯本地，无 App 依赖）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="cmd", required=True, metavar="命令")
    parsers = {}
    for name, (_, help_text) in COMMANDS.items():
        parsers[name] = sub.add_parser(name, parents=[common], help=help_text)

    parsers["init"].add_argument("--force", action="store_true", help="已存在时重建（旧文件先备份）")
    parsers["import-backup"].add_argument("--file", required=True, help="App 导出的 JSON 备份路径")
    parsers["import-backup"].add_argument("--replace", action="store_true", help="覆盖现有数据（默认按 id 合并）")

    parsers["add-baby"].add_argument("--name", required=True)
    parsers["add-baby"].add_argument("--birth", required=True, help="出生日期 YYYY-MM-DD")
    parsers["add-baby"].add_argument("--height", required=True, type=float, help="身高 cm")
    parsers["add-baby"].add_argument("--weight", required=True, type=float, help="体重 kg")
    parsers["add-baby"].add_argument("--gender", choices=["male", "female"], default="male")
    parsers["add-baby"].add_argument("--allergies", default="", help="过敏食物，逗号分隔")
    parsers["add-baby"].add_argument("--iron-risk", action="store_true")
    parsers["add-baby"].add_argument("--size-status", choices=["small", "normal", "large"], default="normal")
    parsers["add-baby"].add_argument("--manual-size", action="store_true", help="手动指定个头，禁止自动覆盖")
    parsers["switch"].add_argument("--id", required=True, type=int)

    parsers["foods"].add_argument("--category", help="按分类过滤，如 谷物 / 蛋奶 / 肉鱼 / 豆类 / 蔬菜 / 水果")
    parsers["foods"].add_argument("--search", help="按 id 或名称搜索")

    for name in ("add-meal", "meals", "intake", "advice", "sources"):
        parsers[name].add_argument("--date", help="日期 YYYY-MM-DD，默认今天")
        parsers[name].add_argument("--baby-id", type=int, help="默认当前宝宝")
    parsers["add-meal"].add_argument("--type", required=True, choices=MEAL_TYPES)
    parsers["add-meal"].add_argument("--food", action="append", metavar="ID:克重", help="可重复，如 --food rice:100")
    parsers["add-meal"].add_argument("--va", type=float, default=0, help="维生素A 补充剂 μg")
    parsers["add-meal"].add_argument("--vc", type=float, default=0, help="维生素C 补充剂 mg")
    parsers["add-meal"].add_argument("--note", default="")
    parsers["del-meal"].add_argument("--id", required=True, type=int)

    for name in ("add-growth", "growth"):
        parsers[name].add_argument("--baby-id", type=int, help="默认当前宝宝")
    parsers["add-growth"].add_argument("--height", required=True, type=float)
    parsers["add-growth"].add_argument("--weight", required=True, type=float)
    parsers["add-growth"].add_argument("--date", help="测量日期 YYYY-MM-DD，默认今天")
    parsers["add-growth"].add_argument("--note", default="")

    parsers["sources"].add_argument("--nutrient", required=True, choices=NUTRIENTS)
    parsers["report"].add_argument("--days", type=int, choices=[7, 30], default=7)
    parsers["report"].add_argument("--baby-id", type=int)
    parsers["report"].add_argument("--out", help="输出 Markdown 文件路径，不传则打印")
    parsers["export"].add_argument("--out", help="输出文件路径")
    parsers["export"].add_argument("--for-app", action="store_true", help="输出成 App 可导入的备份格式")
    return p


def main():
    args = build_parser().parse_args()
    path = resolve_data_path(args)
    try:
        foods, growth = load_assets()
        index = food_index(foods)
        doc = load_doc(path, required=False)
        COMMANDS[args.cmd][0](args, doc, path, foods, growth, index)
    except (RuntimeError, ValueError, KeyError, json.JSONDecodeError, OSError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
