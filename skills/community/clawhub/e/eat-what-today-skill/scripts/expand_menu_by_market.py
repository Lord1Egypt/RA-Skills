import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
MENU_FILE = BASE / "assets" / "menu_db.json"

existing = json.loads(MENU_FILE.read_text(encoding="utf-8"))
menu = {item["name"]: item for item in existing}

def upsert(name, cuisine, price, spicy, modes, city_tags, time_tags, moods, weather=None):
    menu[name] = {
        "name": name,
        "modes": modes,
        "moods": moods,
        "weather": weather or ["all"],
        "price": price,
        "spicy": spicy,
        "city_tags": city_tags,
        "time_tags": time_tags,
        "cuisine": cuisine,
    }

# Public-hot categories inspired by Meituan/Ele.me open trend summaries.
packs = {
    "川渝": [
        "宫保鸡丁盖饭", "回锅肉盖饭", "鱼香肉丝盖饭", "毛血旺", "口水鸡", "夫妻肺片", "冒菜", "钵钵鸡", "酸辣粉", "担担面", "肥肠粉", "串串香", "烤鱼", "冷锅串串", "川北凉粉"
    ],
    "湘菜": [
        "小炒黄牛肉", "剁椒鱼头", "农家小炒肉", "外婆菜炒饭", "辣椒炒鸡", "香辣虾", "湘西腊肉饭", "剁椒蒸茄子", "干锅花菜", "湘味口味虾"
    ],
    "粤式": [
        "豉汁排骨饭", "烧鸭饭", "叉烧饭", "双拼饭", "煲仔饭", "腊味煲仔饭", "云吞面", "鲜虾云吞", "白切鸡饭", "艇仔粥", "皮蛋瘦肉粥", "滑蛋牛肉饭"
    ],
    "粉面主食": [
        "兰州牛肉拉面", "番茄鸡蛋面", "炸酱面", "热干面", "刀削面", "酸汤肥牛米线", "花甲米线", "桂林米粉", "南昌拌粉", "重庆酸辣粉", "牛杂粉", "卤肉拌面"
    ],
    "盖饭快餐": [
        "番茄牛腩饭", "黑椒牛柳饭", "照烧鸡腿饭", "咖喱鸡排饭", "土豆牛肉饭", "青椒肉丝饭", "香菇滑鸡饭", "蜜汁叉烧饭", "台式鸡排饭", "卤肉双拼饭", "鸡腿便当", "香辣鸡丁饭"
    ],
    "轻食健康": [
        "鸡胸肉沙拉", "牛油果沙拉", "藜麦能量碗", "低脂鸡肉卷", "全麦三明治", "金枪鱼沙拉", "蔬菜豆腐碗", "水煮西兰花鸡胸", "燕麦酸奶碗", "低卡荞麦面"
    ],
    "早餐": [
        "豆浆油条", "手抓饼", "鸡蛋灌饼", "小笼包", "生煎包", "茶叶蛋套餐", "豆腐脑", "肉包子", "鲜肉锅贴", "紫米饭团"
    ],
    "夜宵": [
        "炒河粉", "炒面", "炒年糕", "烤串拼盘", "炸鸡桶", "炸鸡汉堡套餐", "砂锅土豆粉", "牛肉锅贴", "炸酱炒饭", "香辣小龙虾"
    ],
    "西式": [
        "意大利肉酱面", "奶油蘑菇意面", "黑椒牛排", "夏威夷披萨", "榴莲披萨", "培根披萨", "鸡肉卷", "美式热狗", "芝士焗饭", "烤鸡翅拼盘"
    ],
    "日式": [
        "照烧鳗鱼饭", "亲子丼", "咖喱猪排饭", "厚蛋烧便当", "三文鱼寿司拼盘", "牛肉乌冬面", "豚骨拉面", "炸虾天妇罗", "日式炸鸡块", "日式牛肉饭"
    ],
    "韩式": [
        "韩式拌饭", "石锅拌饭", "辣白菜五花肉", "韩式泡菜锅", "韩式年糕", "韩式鸡肉饭", "部队锅套餐", "辣炒年糕套餐", "韩式海鲜饼", "参鸡汤"
    ],
    "东北北方面食": [
        "锅包肉饭", "地三鲜盖饭", "东北大拉皮", "猪肉炖粉条", "葱爆羊肉饭", "羊肉泡馍", "臊子面", "胡辣汤", "驴肉火烧", "牛肉馅饼"
    ],
    "云贵": [
        "酸汤鱼", "豆花米线", "折耳根拌面", "菌菇鸡汤米线", "汽锅鸡", "小锅米线", "过桥米线套餐", "凉拌米线", "贵州酸汤牛肉", "云南小炒"
    ],
    "饮品": [
        "珍珠奶茶", "杨枝甘露", "芝士葡萄", "生椰拿铁", "美式咖啡", "拿铁咖啡", "抹茶拿铁", "柠檬茶", "鲜榨果汁", "冰粉"
    ],
    "甜品": [
        "葡式蛋挞", "提拉米苏", "黑森林蛋糕", "芝士蛋糕", "芋圆烧仙草", "双皮奶", "椰汁西米露", "布丁", "泡芙", "红豆奶冻"
    ],
    "素食": [
        "菌菇豆腐煲", "素炒三鲜", "地中海素食碗", "番茄豆腐饭", "香菇青菜面", "素春卷", "凉拌木耳", "清炒时蔬套餐", "素鸡盖饭", "香煎豆腐饭"
    ],
}

for group, dishes in packs.items():
    for name in dishes:
        if group in ("川渝", "湘菜"):
            upsert(name, "sichuan" if group == "川渝" else "hunan", "mid", "high", ["takeaway", "dine_in", "cook"], ["south", "all"] if group == "川渝" else ["hunan", "south", "all"], ["lunch", "dinner", "late_night"], ["adventurous", "happy", "focused"], ["all", "cold", "rainy"])
        elif group == "粤式":
            upsert(name, "cantonese", "mid", "low", ["takeaway", "dine_in", "cook"], ["guangdong", "south", "all"], ["breakfast", "lunch", "dinner"], ["comfort", "light", "neutral"], ["all", "hot", "humid"])
        elif group in ("粉面主食", "东北北方面食", "云贵"):
            upsert(name, "northern" if group == "东北北方面食" else "sichuan" if group == "云贵" else "fusion", "low", "mid", ["takeaway", "dine_in", "cook"], ["north", "all"] if group == "东北北方面食" else ["south", "all"], ["breakfast", "lunch", "dinner", "late_night"], ["busy", "focused", "comfort"], ["all", "cold", "rainy"])
        elif group == "盖饭快餐":
            upsert(name, "fusion", "mid", "low", ["takeaway", "dine_in", "cook"], ["all"], ["lunch", "dinner"], ["busy", "focused", "neutral"], ["all"])
        elif group == "轻食健康":
            upsert(name, "healthy", "mid", "low", ["takeaway", "dine_in", "cook"], ["all"], ["breakfast", "lunch", "dinner"], ["healthy", "light", "focused"], ["all", "hot", "sunny"])
        elif group == "早餐":
            upsert(name, "breakfast", "low", "low", ["takeaway", "dine_in", "cook"], ["all"], ["breakfast", "lunch"], ["busy", "neutral", "comfort"], ["all"])
        elif group == "夜宵":
            upsert(name, "late_night", "mid", "mid", ["takeaway", "dine_in", "cook"], ["all"], ["dinner", "late_night"], ["party", "happy", "late_night"], ["all", "cold", "rainy"])
        elif group == "西式":
            upsert(name, "western", "high", "low", ["takeaway", "dine_in", "cook"], ["all"], ["lunch", "dinner", "late_night"], ["happy", "party", "neutral"], ["all"])
        elif group == "日式":
            upsert(name, "japanese", "high", "low", ["takeaway", "dine_in", "cook"], ["all"], ["lunch", "dinner"], ["light", "happy", "focused"], ["all"])
        elif group == "韩式":
            upsert(name, "korean", "high", "mid", ["takeaway", "dine_in", "cook"], ["all"], ["lunch", "dinner", "late_night"], ["party", "happy", "adventurous"], ["all", "cold"])
        elif group == "饮品":
            upsert(name, "drink", "low", "low", ["takeaway", "dine_in"], ["all"], ["breakfast", "lunch", "dinner", "late_night"], ["happy", "light", "busy"], ["all", "hot", "sunny"])
        elif group == "甜品":
            upsert(name, "dessert", "mid", "low", ["takeaway", "dine_in", "cook"], ["all"], ["lunch", "dinner", "late_night"], ["happy", "comfort", "party"], ["all"])
        elif group == "素食":
            upsert(name, "vegetarian", "mid", "low", ["takeaway", "dine_in", "cook"], ["all"], ["lunch", "dinner"], ["healthy", "light", "neutral"], ["all"])

updated = sorted(menu.values(), key=lambda x: x["name"])
MENU_FILE.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Updated items:", len(updated))
