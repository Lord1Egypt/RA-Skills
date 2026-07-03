"""
AI营养师 — 综合营养数据库
包含: 食物营养成分库 / 营养素知识库 / 中医体质库 / 慢病营养库 / 食谱模板库
基于《中国食物成分表》和《中国居民膳食营养素参考摄入量(DRIs 2024)》
"""

import json

# ============================================================
# 一、食物营养成分数据库 (150+ 中国常见食物)
# 格式: {name: {kcal, protein_g, fat_g, carbs_g, fiber_g, gi, category, key_nutrients}}
# per 100g 可食部
# ============================================================

FOOD_DB = {
    # ----- 主食类 -----
    "米饭":       {"kcal": 116, "protein": 2.6, "fat": 0.3, "carbs": 25.9, "fiber": 0.3, "gi": 83, "category": "主食", "key_nutrients": []},
    "糙米饭":     {"kcal": 123, "protein": 2.8, "fat": 0.9, "carbs": 25.6, "fiber": 1.8, "gi": 55, "category": "主食", "key_nutrients": ["膳食纤维", "镁"]},
    "馒头":       {"kcal": 223, "protein": 7.0, "fat": 1.1, "carbs": 44.2, "fiber": 1.3, "gi": 88, "category": "主食", "key_nutrients": []},
    "全麦面包":   {"kcal": 246, "protein": 9.0, "fat": 3.4, "carbs": 43.1, "fiber": 6.0, "gi": 50, "category": "主食", "key_nutrients": ["膳食纤维", "B族维生素"]},
    "面条(煮)":   {"kcal": 110, "protein": 3.6, "fat": 0.3, "carbs": 22.4, "fiber": 0.4, "gi": 60, "category": "主食", "key_nutrients": []},
    "燕麦片":     {"kcal": 377, "protein": 13.5, "fat": 6.7, "carbs": 61.6, "fiber": 5.3, "gi": 40, "category": "主食", "key_nutrients": ["膳食纤维", "β-葡聚糖", "铁"]},
    "玉米":       {"kcal": 112, "protein": 4.0, "fat": 1.2, "carbs": 22.8, "fiber": 2.9, "gi": 55, "category": "主食", "key_nutrients": ["膳食纤维", "叶黄素"]},
    "红薯":       {"kcal": 86,  "protein": 1.6, "fat": 0.1, "carbs": 20.1, "fiber": 3.0, "gi": 54, "category": "主食", "key_nutrients": ["β-胡萝卜素", "维生素C"]},
    "紫薯":       {"kcal": 82,  "protein": 1.4, "fat": 0.1, "carbs": 19.4, "fiber": 2.8, "gi": 51, "category": "主食", "key_nutrients": ["花青素", "膳食纤维"]},
    "小米粥":     {"kcal": 46,  "protein": 1.4, "fat": 0.7, "carbs": 8.4,  "fiber": 0.3, "gi": 62, "category": "主食", "key_nutrients": ["B族维生素"]},
    "荞麦面":     {"kcal": 132, "protein": 4.5, "fat": 1.5, "carbs": 26.0, "fiber": 2.0, "gi": 54, "category": "主食", "key_nutrients": ["芦丁", "膳食纤维"]},
    "土豆":       {"kcal": 81,  "protein": 2.0, "fat": 0.2, "carbs": 17.2, "fiber": 1.1, "gi": 62, "category": "主食", "key_nutrients": ["维生素C", "钾"]},
    "山药":       {"kcal": 57,  "protein": 1.9, "fat": 0.2, "carbs": 11.6, "fiber": 0.8, "gi": 51, "category": "主食", "key_nutrients": ["粘蛋白", "钾"]},

    # ----- 肉类 -----
    "鸡胸肉":     {"kcal": 133, "protein": 23.3, "fat": 5.0, "carbs": 0,   "fiber": 0, "gi": 0, "category": "肉类", "key_nutrients": ["硒", "烟酸"]},
    "鸡腿肉":     {"kcal": 181, "protein": 20.2, "fat": 11.0, "carbs": 0,  "fiber": 0, "gi": 0, "category": "肉类", "key_nutrients": ["铁", "锌"]},
    "猪瘦肉":     {"kcal": 143, "protein": 20.3, "fat": 6.2, "carbs": 1.5, "fiber": 0, "gi": 0, "category": "肉类", "key_nutrients": ["维生素B1", "铁"]},
    "猪排骨":     {"kcal": 264, "protein": 18.3, "fat": 20.4, "carbs": 1.7,"fiber": 0, "gi": 0, "category": "肉类", "key_nutrients": ["钙", "胶原蛋白"]},
    "牛肉(瘦)":   {"kcal": 106, "protein": 20.2, "fat": 2.3, "carbs": 1.2, "fiber": 0, "gi": 0, "category": "肉类", "key_nutrients": ["铁", "锌", "维生素B12"]},
    "牛腩":       {"kcal": 195, "protein": 17.3, "fat": 13.6, "carbs": 0,  "fiber": 0, "gi": 0, "category": "肉类", "key_nutrients": ["铁", "锌"]},
    "羊肉(瘦)":   {"kcal": 118, "protein": 20.5, "fat": 3.9, "carbs": 0.2, "fiber": 0, "gi": 0, "category": "肉类", "key_nutrients": ["铁", "锌", "维生素B12"]},
    "鸭肉":       {"kcal": 240, "protein": 15.5, "fat": 19.7, "carbs": 0.2,"fiber": 0, "gi": 0, "category": "肉类", "key_nutrients": ["烟酸", "铁"]},

    # ----- 水产类 -----
    "三文鱼":     {"kcal": 139, "protein": 19.8, "fat": 6.3, "carbs": 0,   "fiber": 0, "gi": 0, "category": "水产", "key_nutrients": ["Omega-3(DHA/EPA)", "维生素D"]},
    "虾仁":       {"kcal": 87,  "protein": 18.6, "fat": 0.8, "carbs": 0.8, "fiber": 0, "gi": 0, "category": "水产", "key_nutrients": ["硒", "锌", "虾青素"]},
    "带鱼":       {"kcal": 127, "protein": 17.7, "fat": 6.1, "carbs": 0,   "fiber": 0, "gi": 0, "category": "水产", "key_nutrients": ["Omega-3", "钙"]},
    "鳕鱼":       {"kcal": 82,  "protein": 17.8, "fat": 0.7, "carbs": 0.7, "fiber": 0, "gi": 0, "category": "水产", "key_nutrients": ["硒", "维生素D"]},
    "鲈鱼":       {"kcal": 105, "protein": 18.6, "fat": 3.4, "carbs": 0,   "fiber": 0, "gi": 0, "category": "水产", "key_nutrients": ["铜", "Omega-3"]},
    "鲫鱼":       {"kcal": 108, "protein": 17.1, "fat": 4.0, "carbs": 0,   "fiber": 0, "gi": 0, "category": "水产", "key_nutrients": ["钙", "蛋白质"]},
    "蛤蜊":       {"kcal": 56,  "protein": 7.6, "fat": 0.9, "carbs": 4.7,  "fiber": 0, "gi": 0, "category": "水产", "key_nutrients": ["铁", "锌", "维生素B12"]},

    # ----- 蛋奶豆类 -----
    "鸡蛋(煮)":   {"kcal": 144, "protein": 13.3, "fat": 8.8, "carbs": 2.8, "fiber": 0, "gi": 0, "category": "蛋类", "key_nutrients": ["胆碱", "维生素A", "叶黄素"]},
    "鸡蛋白":     {"kcal": 48,  "protein": 10.9, "fat": 0.1, "carbs": 1.3, "fiber": 0, "gi": 0, "category": "蛋类", "key_nutrients": []},
    "牛奶(全脂)": {"kcal": 61,  "protein": 3.1, "fat": 3.3, "carbs": 5.0,  "fiber": 0, "gi": 27, "category": "奶类", "key_nutrients": ["钙", "维生素D", "维生素B2"]},
    "酸奶(原味)": {"kcal": 72,  "protein": 3.5, "fat": 2.7, "carbs": 9.3,  "fiber": 0, "gi": 36, "category": "奶类", "key_nutrients": ["钙", "益生菌", "维生素B2"]},
    "豆浆":       {"kcal": 31,  "protein": 3.0, "fat": 1.6, "carbs": 1.2,  "fiber": 0.8, "gi": 34, "category": "豆类", "key_nutrients": ["大豆异黄酮", "植物蛋白"]},
    "豆腐(北)":   {"kcal": 82,  "protein": 8.1, "fat": 3.7, "carbs": 3.8,  "fiber": 0.6, "gi": 32, "category": "豆类", "key_nutrients": ["钙", "大豆异黄酮"]},
    "豆腐(内酯)": {"kcal": 49,  "protein": 5.0, "fat": 1.9, "carbs": 2.9,  "fiber": 0.2, "gi": 30, "category": "豆类", "key_nutrients": ["钙(偏低)", "植物蛋白"]},
    "毛豆":       {"kcal": 131, "protein": 13.1, "fat": 5.0, "carbs": 8.4,  "fiber": 4.0, "gi": 18, "category": "豆类", "key_nutrients": ["膳食纤维", "植物蛋白"]},
    "鹰嘴豆(煮)": {"kcal": 164, "protein": 8.9, "fat": 2.6, "carbs": 27.4, "fiber": 7.6, "gi": 28, "category": "豆类", "key_nutrients": ["膳食纤维", "叶酸"]},
    "纳豆":       {"kcal": 200, "protein": 18.0, "fat": 10.0, "carbs": 12.0,"fiber": 5.4, "gi": 33, "category": "豆类", "key_nutrients": ["维生素K2", "纳豆激酶"]},

    # ----- 蔬菜类 -----
    "西兰花":     {"kcal": 34,  "protein": 3.7, "fat": 0.3, "carbs": 5.7,  "fiber": 2.6, "gi": 15, "category": "蔬菜", "key_nutrients": ["维生素C", "维生素K", "萝卜硫素"]},
    "菠菜":       {"kcal": 23,  "protein": 2.9, "fat": 0.4, "carbs": 2.8,  "fiber": 2.2, "gi": 15, "category": "蔬菜", "key_nutrients": ["铁(非血红素)", "叶酸", "维生素K"]},
    "番茄":       {"kcal": 18,  "protein": 0.9, "fat": 0.2, "carbs": 3.5,  "fiber": 1.2, "gi": 30, "category": "蔬菜", "key_nutrients": ["番茄红素", "维生素C", "钾"]},
    "黄瓜":       {"kcal": 15,  "protein": 0.8, "fat": 0.1, "carbs": 2.5,  "fiber": 0.5, "gi": 15, "category": "蔬菜", "key_nutrients": ["钾", "水分"]},
    "胡萝卜":     {"kcal": 41,  "protein": 1.0, "fat": 0.2, "carbs": 9.0,  "fiber": 2.8, "gi": 39, "category": "蔬菜", "key_nutrients": ["β-胡萝卜素(维生素A原)", "膳食纤维"]},
    "苦瓜":       {"kcal": 19,  "protein": 1.0, "fat": 0.1, "carbs": 3.5,  "fiber": 1.4, "gi": 24, "category": "蔬菜", "key_nutrients": ["苦瓜素", "维生素C"]},
    "冬瓜":       {"kcal": 12,  "protein": 0.4, "fat": 0.1, "carbs": 2.6,  "fiber": 0.8, "gi": 15, "category": "蔬菜", "key_nutrients": ["钾", "低热量"]},
    "芹菜":       {"kcal": 16,  "protein": 1.2, "fat": 0.2, "carbs": 2.5,  "fiber": 1.2, "gi": 15, "category": "蔬菜", "key_nutrients": ["钾", "芹菜素"]},
    "生菜":       {"kcal": 14,  "protein": 1.3, "fat": 0.1, "carbs": 2.0,  "fiber": 1.2, "gi": 15, "category": "蔬菜", "key_nutrients": ["叶酸", "维生素K"]},
    "秋葵":       {"kcal": 33,  "protein": 2.0, "fat": 0.2, "carbs": 7.0,  "fiber": 3.2, "gi": 20, "category": "蔬菜", "key_nutrients": ["粘多糖", "叶酸", "钙"]},
    "青椒":       {"kcal": 22,  "protein": 1.0, "fat": 0.2, "carbs": 4.0,  "fiber": 2.1, "gi": 15, "category": "蔬菜", "key_nutrients": ["维生素C(极高)", "β-胡萝卜素"]},
    "木耳":       {"kcal": 35,  "protein": 10.6,"fat": 0.2, "carbs": 65.6, "fiber": 29.9,"gi": 15, "category": "蔬菜", "key_nutrients": ["铁(极高)", "膳食纤维"]},
    "香菇":       {"kcal": 26,  "protein": 2.2, "fat": 0.3, "carbs": 5.2,  "fiber": 3.3, "gi": 28, "category": "蔬菜", "key_nutrients": ["维生素D(晒后)", "硒", "香菇多糖"]},
    "海带":       {"kcal": 12,  "protein": 1.2, "fat": 0.1, "carbs": 1.6,  "fiber": 0.5, "gi": 17, "category": "蔬菜", "key_nutrients": ["碘", "钙", "褐藻胶"]},
    "紫菜":       {"kcal": 207, "protein": 26.7,"fat": 1.1, "carbs": 22.5, "fiber": 21.6,"gi": 20, "category": "蔬菜", "key_nutrients": ["碘(极高)", "铁", "维生素B12"]},

    # ----- 水果类 -----
    "苹果":       {"kcal": 53,  "protein": 0.2, "fat": 0.2, "carbs": 12.3, "fiber": 2.4, "gi": 36, "category": "水果", "key_nutrients": ["果胶", "多酚"]},
    "香蕉":       {"kcal": 93,  "protein": 1.4, "fat": 0.2, "carbs": 22.0, "fiber": 2.6, "gi": 52, "category": "水果", "key_nutrients": ["钾", "维生素B6"]},
    "蓝莓":       {"kcal": 57,  "protein": 0.7, "fat": 0.3, "carbs": 14.5, "fiber": 2.4, "gi": 53, "category": "水果", "key_nutrients": ["花青素", "维生素C", "维生素K"]},
    "橙子":       {"kcal": 47,  "protein": 0.9, "fat": 0.1, "carbs": 10.5, "fiber": 2.4, "gi": 43, "category": "水果", "key_nutrients": ["维生素C", "叶酸"]},
    "猕猴桃":     {"kcal": 61,  "protein": 1.1, "fat": 0.5, "carbs": 14.7, "fiber": 3.0, "gi": 52, "category": "水果", "key_nutrients": ["维生素C(极高)", "维生素E", "钾"]},
    "牛油果":     {"kcal": 160, "protein": 2.0, "fat": 14.7,"carbs": 8.5,  "fiber": 6.7, "gi": 15, "category": "水果", "key_nutrients": ["单不饱和脂肪酸", "钾", "维生素E"]},
    "草莓":       {"kcal": 32,  "protein": 0.7, "fat": 0.3, "carbs": 7.1,  "fiber": 2.0, "gi": 40, "category": "水果", "key_nutrients": ["维生素C", "鞣花酸"]},
    "西瓜":       {"kcal": 30,  "protein": 0.6, "fat": 0.2, "carbs": 6.8,  "fiber": 0.4, "gi": 72, "category": "水果", "key_nutrients": ["番茄红素", "瓜氨酸"]},
    "火龙果":     {"kcal": 55,  "protein": 1.1, "fat": 0.4, "carbs": 13.0, "fiber": 2.0, "gi": 42, "category": "水果", "key_nutrients": ["花青素(红心)", "膳食纤维"]},
    "柚子":       {"kcal": 42,  "protein": 0.8, "fat": 0.2, "carbs": 9.5,  "fiber": 1.0, "gi": 25, "category": "水果", "key_nutrients": ["维生素C", "柚皮苷"]},
    "樱桃":       {"kcal": 63,  "protein": 1.1, "fat": 0.2, "carbs": 16.0, "fiber": 2.1, "gi": 22, "category": "水果", "key_nutrients": ["花青素", "钾", "褪黑素"]},
    "石榴":       {"kcal": 83,  "protein": 1.7, "fat": 1.2, "carbs": 18.7, "fiber": 4.0, "gi": 35, "category": "水果", "key_nutrients": ["鞣花酸", "多酚", "钾"]},

    # ----- 坚果种子类 -----
    "核桃":       {"kcal": 654, "protein": 15.2,"fat": 65.2,"carbs": 13.7, "fiber": 6.7, "gi": 15, "category": "坚果", "key_nutrients": ["Omega-3(ALA)", "维生素E", "褪黑素"]},
    "杏仁":       {"kcal": 579, "protein": 21.2,"fat": 49.9,"carbs": 21.6, "fiber": 12.5,"gi": 15, "category": "坚果", "key_nutrients": ["维生素E", "镁", "钙"]},
    "腰果":       {"kcal": 553, "protein": 18.2,"fat": 43.9,"carbs": 30.2, "fiber": 3.3, "gi": 22, "category": "坚果", "key_nutrients": ["铜", "镁", "锌"]},
    "花生":       {"kcal": 567, "protein": 25.8,"fat": 49.2,"carbs": 16.1, "fiber": 8.5, "gi": 14, "category": "坚果", "key_nutrients": ["烟酸", "白藜芦醇", "维生素E"]},
    "奇亚籽":     {"kcal": 486, "protein": 16.5,"fat": 30.7,"carbs": 42.1, "fiber": 34.4,"gi": 10, "category": "坚果", "key_nutrients": ["Omega-3(ALA)", "膳食纤维", "钙"]},
    "芝麻":       {"kcal": 573, "protein": 18.0,"fat": 49.7,"carbs": 23.4, "fiber": 14.0,"gi": 15, "category": "坚果", "key_nutrients": ["钙(极高)", "铁", "维生素E"]},

    # ----- 油脂调味类 -----
    "橄榄油":     {"kcal": 884, "protein": 0, "fat": 100, "carbs": 0, "fiber": 0, "gi": 0, "category": "油脂", "key_nutrients": ["单不饱和脂肪酸", "多酚"]},
    "亚麻籽油":   {"kcal": 884, "protein": 0, "fat": 100, "carbs": 0, "fiber": 0, "gi": 0, "category": "油脂", "key_nutrients": ["Omega-3(ALA极高)", "木酚素"]},
    "蜂蜜":       {"kcal": 304, "protein": 0.3, "fat": 0, "carbs": 75.6, "fiber": 0, "gi": 58, "category": "调味", "key_nutrients": ["抗氧化物质", "酶"]},

    # ----- 饮品 -----
    "绿茶":       {"kcal": 1,   "protein": 0.1, "fat": 0, "carbs": 0.1, "fiber": 0, "gi": 0, "category": "饮品", "key_nutrients": ["茶多酚(EGCG)", "咖啡因"]},
    "黑咖啡":     {"kcal": 2,   "protein": 0.1, "fat": 0, "carbs": 0, "fiber": 0, "gi": 0, "category": "饮品", "key_nutrients": ["咖啡因", "绿原酸"]},
}


# ============================================================
# 二、营养素知识库
# 格式: {name: {rda_male, rda_female, ul, unit, function, deficiency, excess, food_sources, absorption}}
# ============================================================

NUTRIENT_DB = {
    "维生素A": {
        "rda_male": 800, "rda_female": 700, "ul": 3000, "unit": "μg RAE/天",
        "function": "维持正常视觉、免疫功能和上皮组织健康",
        "deficiency": ["夜盲症", "干眼症", "皮肤干燥粗糙", "免疫力下降", "儿童生长发育迟缓"],
        "excess": ["头晕", "恶心", "皮肤干燥脱屑", "肝损伤(长期大量)", "孕妇过量可致胎儿畸形"],
        "food_sources": [
            ("猪肝", 4972), ("胡萝卜", 688), ("菠菜", 469), ("红薯", 709),
            ("南瓜", 148), ("鸡蛋黄", 438), ("西兰花", 77), ("芒果", 38)
        ],
        "absorption": {"促进": ["脂肪(脂溶性，需与油脂同食)"], "抑制": ["酒精", "吸烟"]},
        "note": "植物来源为β-胡萝卜素，需在体内转化，转化率约1/12"
    },
    "维生素C": {
        "rda_male": 100, "rda_female": 100, "ul": 2000, "unit": "mg/天",
        "function": "抗氧化、促进胶原蛋白合成、促进铁吸收、增强免疫力",
        "deficiency": ["牙龈出血", "皮肤瘀斑", "伤口愈合缓慢", "免疫力下降", "坏血病(严重缺乏)"],
        "excess": ["腹泻", "胃肠不适", "肾结石风险增加(高剂量长期)", "铁过载(对铁过载人群)"],
        "food_sources": [
            ("鲜枣", 243), ("猕猴桃", 92), ("青椒", 80), ("草莓", 47),
            ("西兰花", 56), ("橙子", 33), ("番茄", 19), ("冬枣", 243)
        ],
        "absorption": {"促进": ["生物类黄酮", "铁"], "抑制": ["高温烹饪(破坏)", "长期储存", "吸烟(加速消耗)"]},
        "note": "水溶性，每日需持续补充；吸烟者需求增加约35mg/天"
    },
    "维生素D": {
        "rda_male": 15, "rda_female": 15, "ul": 50, "unit": "μg/天",
        "function": "促进钙吸收、维持骨骼健康、调节免疫、改善肌肉功能",
        "deficiency": ["佝偻病(儿童)", "骨质疏松", "肌肉无力", "免疫力下降", "情绪低落/抑郁"],
        "excess": ["高钙血症", "肾结石", "软组织钙化(严重)"],
        "food_sources": [
            ("三文鱼", 11), ("沙丁鱼(罐头)", 7.5), ("蛋黄", 5.4), ("香菇(晒干)", 10),
            ("牛奶(强化)", 2.5), ("猪肝", 1.2)
        ],
        "absorption": {"促进": ["晒太阳(15-30分钟/天)", "镁", "脂肪", "维生素K2"], "抑制": ["防晒霜(SPF>15)", "肥胖(被脂肪组织截留)"]},
        "note": "80%以上靠日照合成，北方冬季和室内工作者易缺乏"
    },
    "维生素E": {
        "rda_male": 14, "rda_female": 14, "ul": 700, "unit": "mg α-TE/天",
        "function": "抗氧化(保护细胞膜)、抗衰老、保护心血管、增强免疫力",
        "deficiency": ["神经损伤(罕见)", "溶血性贫血(早产儿)", "免疫力下降", "皮肤老化加速"],
        "excess": ["出血倾向(抗凝血)", "头痛", "肌肉无力"],
        "food_sources": [
            ("葵花籽油", 55), ("杏仁", 25.6), ("花生", 8.3), ("核桃", 6.5),
            ("菠菜", 2.0), ("牛油果", 2.1)
        ],
        "absorption": {"促进": ["脂肪", "硒", "维生素C"], "抑制": ["铁补充剂(高剂量时干扰吸收)"]},
        "note": "与硒协同抗氧化，补充时宜与脂肪同食"
    },
    "维生素K": {
        "rda_male": 80, "rda_female": 80, "ul": None, "unit": "μg/天",
        "function": "促进凝血、骨骼代谢(引导钙沉积于骨骼)、预防血管钙化",
        "deficiency": ["出血倾向", "骨质疏松风险增加", "容易瘀青"],
        "excess": ["尚无明确UL(天然形式)", "合成K3过量可引起溶血"],
        "food_sources": [
            ("羽衣甘蓝", 817), ("菠菜", 483), ("西兰花", 101), ("纳豆", 900),
            ("西芹", 29), ("鸡蛋", 0.3)
        ],
        "absorption": {"促进": ["脂肪"], "抑制": ["抗生素(杀灭肠道菌群合成)"], "禁忌": "服用抗凝药(华法林)者需稳定K摄入"},
        "note": "肠道菌群可合成部分维生素K2"
    },
    "叶酸(B9)": {
        "rda_male": 400, "rda_female": 400, "ul": 1000, "unit": "μg DFE/天",
        "function": "DNA合成、红细胞生成、神经系统发育、预防神经管缺陷",
        "deficiency": ["巨幼细胞性贫血", "疲劳乏力", "胎儿神经管缺陷(孕早期)", "同型半胱氨酸升高(心血管风险)"],
        "excess": ["掩盖维生素B12缺乏(神经系统损伤)", "可能与某些癌症风险相关"],
        "food_sources": [
            ("鸡肝", 578), ("菠菜", 194), ("芦笋", 149), ("鹰嘴豆", 172),
            ("西兰花", 63), ("花生", 110), ("牛油果", 89)
        ],
        "absorption": {"促进": ["维生素C", "维生素B12"], "抑制": ["酒精", "高温烹饪", "某些药物(甲氨蝶呤)"]},
        "note": "备孕和孕早期女性需额外补充400μg/天"
    },
    "铁": {
        "rda_male": 12, "rda_female": 20, "ul": 42, "unit": "mg/天",
        "function": "血红蛋白合成、氧气运输、能量代谢、免疫支持",
        "deficiency": ["缺铁性贫血", "面色苍白", "乏力头晕", "注意力不集中", "异食癖(严重)"],
        "excess": ["便秘", "胃肠不适", "铁过载(血色病)", "氧化应激增加"],
        "food_sources": [
            ("猪肝", 22.6), ("鸭血", 30.5), ("牛肉(瘦)", 2.8), ("蛤蜊", 14.0),
            ("黑木耳", 97.4), ("菠菜", 2.9), ("黑芝麻", 22.7)
        ],
        "absorption": {"促进": ["维生素C", "肉类因子(MFP)", "有机酸"], "抑制": ["茶(鞣酸)", "咖啡", "钙", "植酸(全谷物)", "草酸"]},
        "note": "动物性铁(血红素铁)吸收率15-35%，植物性铁(非血红素铁)2-10%"
    },
    "钙": {
        "rda_male": 800, "rda_female": 800, "ul": 2000, "unit": "mg/天",
        "function": "骨骼牙齿构成、神经传导、肌肉收缩、凝血",
        "deficiency": ["骨质疏松", "佝偻病", "抽筋", "骨质软化", "牙齿问题"],
        "excess": ["肾结石", "便秘", "高钙血症", "干扰铁/锌吸收"],
        "food_sources": [
            ("芝麻酱", 1170), ("虾皮", 991), ("奶酪", 799), ("豆腐(北)", 138),
            ("牛奶", 104), ("酸奶", 118), ("杏仁", 264), ("西兰花", 47)
        ],
        "absorption": {"促进": ["维生素D", "乳糖", "蛋白质(适量)", "酸性环境"], "抑制": ["草酸", "植酸", "过量磷", "过量钠", "咖啡因"]},
        "note": "单次补充不超过500mg，分次服用吸收更好"
    },
    "锌": {
        "rda_male": 12.5, "rda_female": 7.5, "ul": 40, "unit": "mg/天",
        "function": "免疫支持、伤口愈合、味觉维持、生长发育、生殖健康",
        "deficiency": ["免疫力下降", "伤口愈合慢", "味觉减退", "脱发", "生长发育迟缓(儿童)"],
        "excess": ["恶心呕吐", "铜缺乏", "免疫力反而下降(长期高剂量)", "HDL降低"],
        "food_sources": [
            ("牡蛎", 71.2), ("牛肉(瘦)", 4.7), ("猪肝", 5.8), ("南瓜子", 7.8),
            ("腰果", 5.8), ("鸡蛋", 1.1), ("燕麦", 3.6)
        ],
        "absorption": {"促进": ["动物蛋白"], "抑制": ["植酸(全谷物)", "过量钙", "过量铁", "纤维"]},
        "note": "动物性锌比植物性锌吸收率高2-3倍"
    },
    "镁": {
        "rda_male": 330, "rda_female": 330, "ul": None, "unit": "mg/天",
        "function": "能量代谢、肌肉放松、神经调节、骨骼健康、蛋白质合成",
        "deficiency": ["肌肉痉挛/抽筋", "疲劳乏力", "心律不齐", "失眠", "焦虑"],
        "excess": ["腹泻(药物形式)", "低血压(严重过量)"],
        "food_sources": [
            ("南瓜子", 534), ("杏仁", 270), ("菠菜", 79), ("黑巧克力(85%)", 228),
            ("牛油果", 29), ("香蕉", 27), ("燕麦", 138), ("核桃", 158)
        ],
        "absorption": {"促进": ["维生素B6", "维生素D"], "抑制": ["过量钙", "酒精", "利尿剂", "植酸"]},
        "note": "镁对改善睡眠质量和缓解压力有辅助作用"
    },
    "钾": {
        "rda_male": 2000, "rda_female": 2000, "ul": None, "unit": "mg/天",
        "function": "维持体液平衡、降低血压、神经肌肉功能、心脏健康",
        "deficiency": ["乏力", "肌肉无力", "便秘", "心悸", "低钾血症(严重可危及生命)"],
        "excess": ["高钾血症(肾功能正常者罕见)", "心悸(极端情况)"],
        "food_sources": [
            ("土豆", 421), ("香蕉", 358), ("牛油果", 485), ("菠菜", 558),
            ("番茄酱", 1014), ("红薯", 337), ("三文鱼", 363), ("豆类", 500-1000)
        ],
        "absorption": {"促进": ["镁", "远离钠"], "抑制": ["过量钠", "利尿剂", "腹泻/呕吐"]},
        "note": "DASH饮食核心营养素，高钾低钠饮食有助于控制血压"
    },
    "硒": {
        "rda_male": 60, "rda_female": 60, "ul": 400, "unit": "μg/天",
        "function": "抗氧化(谷胱甘肽过氧化物酶)、甲状腺功能、免疫调节",
        "deficiency": ["克山病", "免疫力下降", "甲状腺功能减退", "男性不育"],
        "excess": ["硒中毒(脱发、指甲变形)", "蒜味呼吸", "恶心"],
        "food_sources": [
            ("巴西坚果", 1917), ("猪肾", 157), ("金枪鱼", 81), ("鸡蛋", 15),
            ("葵花籽", 53), ("牛肉", 25), ("蘑菇", 12)
        ],
        "absorption": {"促进": ["维生素E", "蛋氨酸"], "抑制": ["重金属(汞等)"]},
        "note": "巴西坚果含硒极高(每颗~95μg)，每天1-2颗即可满足需求"
    },
    "Omega-3": {
        "rda_male": 1.6, "rda_female": 1.1, "ul": None, "unit": "g ALA/天; EPA+DHA 250-500mg/天",
        "function": "抗炎、脑健康、心血管保护、视力维护、情绪调节",
        "deficiency": ["皮肤干燥", "注意力下降", "关节不适", "情绪低落", "心血管风险增加"],
        "excess": ["出血倾向(极高剂量)", "免疫抑制(极高剂量)", "胃肠不适"],
        "food_sources": [
            ("三文鱼(DHA+EPA)", 2.2), ("亚麻籽(ALA)", 22.8), ("奇亚籽(ALA)", 17.8),
            ("核桃(ALA)", 9.1), ("沙丁鱼(DHA+EPA)", 1.5)
        ],
        "absorption": {"促进": ["磷脂形态(鱼籽/磷虾油)"], "抑制": ["Omega-6过量(竞争酶)", "氧化(避光避热保存)"]},
        "note": "ALA→EPA转化率5-10%，→DHA不足1%，直接摄入鱼油更高效"
    },
    "膳食纤维": {
        "rda_male": 25, "rda_female": 25, "ul": None, "unit": "g/天",
        "function": "促排便、降胆固醇、控血糖、喂养肠道菌群、增加饱腹感",
        "deficiency": ["便秘", "肠道菌群失衡", "血糖波动大", "胆固醇升高"],
        "excess": ["腹胀", "排气管多", "影响矿物质吸收", "肠梗阻(极端)"],
        "food_sources": [
            ("奇亚籽", 34.4), ("黑木耳", 29.9), ("鹰嘴豆", 7.6), ("燕麦", 5.3),
            ("牛油果", 6.7), ("苹果", 2.4), ("西兰花", 2.6)
        ],
        "absorption": {"促进": ["充足饮水(可溶性纤维需吸水膨胀)"], "抑制": ["高脂饮食(延缓胃排空)"]},
        "note": "从低量开始逐步增加，给肠道适应时间；增加纤维时需多喝水"
    },
}


# ============================================================
# 三、中医体质辨识库 (9种体质)
# ============================================================

TCM_CONSTITUTIONS = {
    "平和质": {
        "key_features": ["面色红润有光泽", "精力充沛", "睡眠良好", "适应能力强", "体型匀称"],
        "tendency_diseases": [],
        "food_principle": "均衡多样，不偏食不挑食，顺应四时",
        "recommend": ["五谷杂粮", "新鲜蔬果", "适量动物蛋白", "坚果"],
        "avoid": [],
        "lifestyle": "保持规律作息，适度运动"
    },
    "气虚质": {
        "key_features": ["容易疲劳乏力", "气短懒言", "易出虚汗", "舌淡胖有齿痕", "面色偏白"],
        "tendency_diseases": ["反复感冒", "内脏下垂", "慢性疲劳"],
        "food_principle": "益气健脾，温补为主",
        "recommend": ["山药", "红枣", "黄芪", "党参", "鸡肉", "小米", "黄豆", "香菇", "蜂蜜", "牛肉"],
        "avoid": ["生冷寒凉食物(西瓜/梨/苦瓜)", "萝卜(耗气)", "槟榔"],
        "lifestyle": "早睡早起，避免过度劳累，太极拳/八段锦"
    },
    "阳虚质": {
        "key_features": ["怕冷畏寒", "手脚冰凉", "精神不振", "小便清长", "舌淡胖"],
        "tendency_diseases": ["慢性腹泻", "水肿", "哮喘", "关节炎"],
        "food_principle": "温阳散寒，补肾壮阳",
        "recommend": ["羊肉", "生姜", "桂圆", "核桃", "韭菜", "虾", "肉桂", "当归", "杜仲"],
        "avoid": ["生冷冰冻", "西瓜", "梨", "绿豆", "苦瓜"],
        "lifestyle": "多晒太阳，艾灸关元/足三里，温水泡脚"
    },
    "阴虚质": {
        "key_features": ["口干舌燥", "手足心热", "盗汗", "大便干燥", "舌红少苔"],
        "tendency_diseases": ["失眠", "高血压", "糖尿病(消渴)", "甲亢"],
        "food_principle": "滋阴清热，生津润燥",
        "recommend": ["银耳", "百合", "鸭肉", "梨", "甲鱼", "麦冬", "玉竹", "枸杞", "桑葚"],
        "avoid": ["辛辣(辣椒/花椒/生姜)", "羊肉/狗肉", "煎炸食物", "咖啡浓茶"],
        "lifestyle": "避免熬夜(伤阴)，适度运动不出大汗"
    },
    "痰湿质": {
        "key_features": ["体型偏胖", "腹部肥满", "痰多", "口中粘腻", "困倦嗜睡"],
        "tendency_diseases": ["代谢综合征", "糖尿病", "高血脂", "高血压"],
        "food_principle": "化痰祛湿，健脾利水",
        "recommend": ["薏米", "冬瓜", "赤小豆", "陈皮", "山药", "茯苓", "白扁豆", "荷叶", "海带"],
        "avoid": ["肥甘厚腻", "甜食甜饮", "油炸食品", "酒类", "奶制品(加重痰湿)"],
        "lifestyle": "增加运动量，避免久坐，居住环境保持干燥"
    },
    "湿热质": {
        "key_features": ["面垢油光", "口苦口臭", "易生痤疮", "大便粘滞", "舌苔黄腻"],
        "tendency_diseases": ["痤疮", "黄疸", "泌尿感染", "湿疹"],
        "food_principle": "清热利湿，清淡为主",
        "recommend": ["绿豆", "苦瓜", "薏米", "冬瓜", "莲藕", "黄瓜", "空心菜", "菊花", "金银花"],
        "avoid": ["辛辣(辣椒/花椒)", "油腻煎炸", "甜食", "酒", "羊肉/狗肉(大热)"],
        "lifestyle": "保持皮肤清洁干燥，避免潮湿闷热环境"
    },
    "血瘀质": {
        "key_features": ["肤色晦暗", "嘴唇紫暗", "舌紫暗有瘀斑", "皮肤易出现瘀斑", "健忘"],
        "tendency_diseases": ["心脑血管疾病", "肿瘤", "痛经", "静脉曲张"],
        "food_principle": "活血化瘀，行气通络",
        "recommend": ["山楂", "黑豆", "茄子", "醋", "玫瑰花", "桃仁", "红糖", "红酒(少量)", "洋葱"],
        "avoid": ["肥肉", "奶油", "冷饮(血得寒则凝)", "过量盐(血液粘稠)"],
        "lifestyle": "适度有氧运动促进血液循环，保持心情舒畅"
    },
    "气郁质": {
        "key_features": ["情绪低落抑郁", "胸闷叹气", "胁肋胀痛", "咽部异物感(梅核气)", "敏感多疑"],
        "tendency_diseases": ["抑郁症", "焦虑症", "乳腺增生", "消化性溃疡"],
        "food_principle": "疏肝理气，解郁安神",
        "recommend": ["佛手", "玫瑰花", "柑橘", "小麦", "陈皮", "薄荷", "金橘", "百合", "黄花菜"],
        "avoid": ["咖啡(加重焦虑)", "浓茶", "酒精过量", "辛辣刺激"],
        "lifestyle": "多参加社交活动，听音乐，冥想，瑜伽，避免独自闷想"
    },
    "特禀质": {
        "key_features": ["过敏体质", "易发荨麻疹/湿疹", "打喷嚏/鼻炎", "哮喘", "对药物/食物敏感"],
        "tendency_diseases": ["过敏性鼻炎", "哮喘", "湿疹", "荨麻疹"],
        "food_principle": "益气固表，避开发敏原",
        "recommend": ["黄芪", "白术", "防风", "糯米", "蜂蜜", "红枣", "山药"],
        "avoid": ["个人已知过敏食物", "海鲜(易致敏)", "蚕豆(G6PD缺乏者)", "芒果/菠萝(易致敏)"],
        "lifestyle": "记录过敏日记，保持居住环境整洁，春秋季节花粉防护"
    }
}


# ============================================================
# 四、慢病营养管理库
# ============================================================

DISEASE_NUTRITION = {
    "糖尿病": {
        "core_principle": "控制总热量，低GI饮食，碳水化合物计数法，定时定量",
        "macro_targets": {"carbs_pct": "45-55%", "protein_pct": "15-20%", "fat_pct": "25-35%"},
        "key_nutrients": ["膳食纤维(25-30g/天)", "铬", "镁", "维生素D"],
        "recommend": ["全谷物", "豆类", "绿叶蔬菜", "低GI水果(苹果/柚子/樱桃)", "鱼类"],
        "avoid": ["精制糖", "含糖饮料", "高GI主食", "蜜饯果脯", "甜点"],
        "caution": ["水果在两餐之间吃", "果汁≠水果(纤维损失+升糖快)", "酒精需谨慎"],
        "special_notes": "每餐碳水摄入量需稳定，推荐餐后散步15-20min辅助降糖"
    },
    "高血压": {
        "core_principle": "DASH饮食模式：高钾高钙高镁，低钠低饱和脂肪",
        "macro_targets": {"sodium": "<2000mg/天(约5g盐)", "potassium": "3500-4700mg/天"},
        "key_nutrients": ["钾", "钙", "镁", "膳食纤维", "Omega-3"],
        "recommend": ["深色蔬菜(钾源)", "低脂奶制品", "全谷物", "鱼(每周2-3次)", "坚果(无盐)"],
        "avoid": ["腌制食品(咸菜/腊肉)", "加工食品(薯片/火腿)", "高钠调味料(酱油/味精/豆瓣酱)", "酒精"],
        "caution": ["减盐需循序渐进(味蕾适应2-4周)", "代盐(低钠盐)肾功能不全者慎用"],
        "special_notes": "钠主要来自加工食品(70%)，做饭用盐仅占约30%"
    },
    "痛风/高尿酸": {
        "core_principle": "低嘌呤饮食+大量饮水(2000-3000ml/天)+碱化尿液",
        "macro_targets": {"purine_limit": "急性期<150mg/天，缓解期<300mg/天"},
        "key_nutrients": ["维生素C(促进尿酸排泄)", "膳食纤维", "水"],
        "recommend": ["鸡蛋", "低脂奶制品", "大多数蔬菜", "全谷物", "水果(樱桃/草莓有助于降尿酸)", "水(每天2-3L)"],
        "avoid": ["内脏(肝/肾/脑)", "部分海鲜(沙丁鱼/凤尾鱼/鱼籽)", "浓汤/火锅汤", "啤酒(嘌呤+抑制尿酸排泄)", "含糖饮料(果糖促尿酸生成)"],
        "caution": ["豆腐/豆类可适量(植物嘌呤影响较小)", "发作期严格限制，缓解期适度放宽"],
        "special_notes": "减重有助于降低尿酸，但不宜过快(脂肪分解产酮体抑制尿酸排泄)"
    },
    "高血脂": {
        "core_principle": "地中海饮食模式：低饱和脂肪+高不饱和脂肪+高纤维",
        "macro_targets": {"sat_fat": "<总热量7%", "omega3": "1-2g/天", "fiber": "25-30g/天"},
        "key_nutrients": ["Omega-3", "植物固醇", "膳食纤维(可溶性)", "烟酸"],
        "recommend": ["鱼(富脂鱼每周2-3次)", "橄榄油", "坚果", "燕麦(β-葡聚糖)", "豆类", "蔬菜", "全谷物"],
        "avoid": ["肥肉", "动物油(猪油/黄油)", "油炸食品", "糕点(反式脂肪)", "过量蛋黄(日均不超过1个)"],
        "caution": ["椰子油/棕榈油虽为植物但饱和脂肪含量高", "胆固醇食物≠血液胆固醇(蛋黄可适量)"],
        "special_notes": "减重5-10%可显著改善血脂，运动(有氧+力量)有助降低甘油三酯"
    },
}


# ============================================================
# 五、运动营养数据库
# ============================================================

SPORTS_NUTRITION = {
    "增肌": {
        "protein_g_per_kg": (1.6, 2.2),
        "carbs_strategy": "中高碳水(4-6g/kg)，训练日碳水稍高，休息日适度降低",
        "fat_strategy": "占总热量20-30%，以不饱和脂肪为主",
        "calorie_surplus": "300-500kcal/天",
        "pre_workout": "训练前1-2小时：碳水+少量蛋白(如香蕉+鸡蛋白，或燕麦+牛奶)",
        "post_workout": "训练后30分钟内(黄金窗口)：蛋白(20-40g)+快碳(如乳清蛋白+香蕉/白米饭)",
        "supplements": ["乳清蛋白粉(便捷蛋白补充)", "肌酸(5g/天，提升力量和耐力)", "维生素D3(骨健康)", "锌镁(睾酮支持)"],
        "tips": ["每餐蛋白质摄入不超过40g(超出吸收率下降)", "睡前蛋白(酪蛋白)有助于夜间肌肉修复"]
    },
    "减脂": {
        "protein_g_per_kg": (1.6, 2.4),
        "carbs_strategy": "低碳水(2-3g/kg)，碳水集中在训练前后",
        "fat_strategy": "占总热量20-30%，保证必需脂肪酸",
        "calorie_deficit": "300-500kcal/天(适度)或500-700kcal/天(激进)",
        "pre_workout": "训练前30分钟：黑咖啡/绿茶(提升代谢和脂肪氧化)",
        "post_workout": "训练后1小时内：蛋白+蔬菜(如鸡胸肉+西兰花，减少碳水)",
        "supplements": ["蛋白粉(保证蛋白摄入同时控制热量)", "咖啡因(训练前提升代谢)", "绿茶提取物(EGCG促脂氧化)", "L-肉碱(脂肪转运，效果有争议)"],
        "tips": ["减脂期不低于基础代谢(BMR)，避免代谢适应", "每周减重0.5-1kg为健康节奏", "高强度间歇(HIIT)比稳态有氧更保肌肉"]
    },
    "耐力": {
        "protein_g_per_kg": (1.2, 1.6),
        "carbs_strategy": "高碳水(6-10g/kg)，比赛前3天碳水负荷",
        "fat_strategy": "占总热量20-30%",
        "calorie_target": "按消耗补充，不刻意增减",
        "pre_workout": "长时间训练前2-3小时：高碳水易消化餐(如米饭+香蕉)",
        "post_workout": "训练后30分钟：碳水:蛋白=3:1(如巧克力牛奶)加速糖原恢复",
        "supplements": ["电解质(长距离必备)", "能量胶/运动饮料(赛中>60min)", "支链氨基酸BCAA(减少肌肉分解)", "甜菜根汁(提升耐力的天然硝酸盐来源)"],
        "tips": ["每小时运动补充30-60g碳水", "赛前碳水负荷不是大吃而是调整碳水比例+减训练量"]
    },
}


# ============================================================
# 六、特殊人群营养库
# ============================================================

SPECIAL_POPULATIONS = {
    "孕期": {
        "trimesters": {
            "孕早期(1-12周)": {
                "extra_calories": 0,
                "key_nutrients": {"叶酸": "600μg/天(预防神经管缺陷)", "维生素B6": "1.9mg/天(缓解孕吐)", "碘": "230μg/天"},
                "special_foods": ["深绿色蔬菜(叶酸)", "坚果(B6)", "海带紫菜(碘)"],
                "avoid": ["酒精(绝对禁止)", "生食(李斯特菌风险)", "高汞鱼(鲨鱼/旗鱼)", "过量咖啡因(<200mg/天)", "未消毒奶制品"]
            },
            "孕中期(13-27周)": {
                "extra_calories": 300,
                "key_nutrients": {"钙": "1000mg/天", "铁": "24mg/天", "DHA": "200-300mg/天", "蛋白质": "+15g/天"},
                "special_foods": ["奶制品(钙)", "红肉/动物血(铁)", "三文鱼(DHA)", "鸡蛋(胆碱)"],
                "avoid": ["同上", "过量维生素A(<3000μg/天)", "某些中药(活血化瘀类)"]
            },
            "孕晚期(28周后)": {
                "extra_calories": 450,
                "key_nutrients": {"钙": "1000mg/天", "铁": "29mg/天", "DHA": "200-300mg/天", "膳食纤维": "28g/天(防便秘)"},
                "special_foods": ["同上", "全谷物(纤维+稳定血糖)", "西梅/火龙果(通便)"],
                "avoid": ["同上", "高糖食物(防妊娠糖尿病)"]
            }
        },
        "general_tips": ["少食多餐", "每天喝足1.5-2L水", "孕吐期间吃苏打饼干/干面包", "体重增加建议: BMI<18.5增12.5-18kg, 正常BMI增11.5-16kg"]
    },
    "哺乳期": {
        "extra_calories": 500,
        "key_nutrients": {"蛋白质": "+25g/天", "钙": "1000mg/天(不影响乳汁钙但影响母亲骨钙)", "铁": "20mg/天", "DHA": "200mg/天", "水分": "比平时+1L/天"},
        "galactagogue_foods": ["鲫鱼汤", "猪蹄汤", "木瓜", "茭白", "燕麦"],
        "avoid": ["酒精(会进入乳汁)", "过量咖啡因(<300mg/天)", "回奶食物(韭菜/麦芽/花椒,因人而异)"],
        "tips": ["每产生100ml乳汁消耗约70kcal", "汤水中的脂肪是热量的主要来源,可撇去浮油"]
    },
    "儿童": {
        "age_groups": {
            "1-3岁": {
                "key_nutrients": {"铁": "7mg/天", "锌": "4mg/天", "钙": "500mg/天", "维生素D": "15μg/天", "DHA": "100mg/天"},
                "tips": ["母乳/配方奶为主，1岁后可引入全脂牛奶", "辅食由细到粗，培养咀嚼能力", "不强迫进食(避免进食焦虑)"]
            },
            "4-6岁": {
                "key_nutrients": {"锌": "5.5mg/天", "钙": "800mg/天", "铁": "10mg/天"},
                "tips": ["培养规律三餐+两次加餐习惯", "挑食期：变换做法+参与做饭", "控制含糖零食(<总热量10%)"]
            },
            "7-12岁": {
                "key_nutrients": {"钙": "1000-1200mg/天(快速生长期)", "铁": "12-17mg/天", "蛋白质": "40-60g/天"},
                "tips": ["早餐必须吃(影响学习成绩)", "限制屏幕时间(减少零食摄入)", "参与食材采购和烹饪(培养食育)"]
            },
            "13-17岁": {
                "key_nutrients": {"钙": "1000-1200mg/天", "铁": "男15/女18mg/天", "蛋白质": "男75/女60g/天"},
                "tips": ["青春期铁需求激增(女性月经初潮后注意补铁)", "运动少年蛋白和碳水需增加", "警惕节食减肥(影响生长发育)"]
            }
        }
    },
    "老年": {
        "key_concerns": ["肌肉衰减(少肌症)", "骨质疏松", "味觉减退(食欲下降)", "便秘", "吞咽困难"],
        "key_nutrients": {"蛋白质": "1.2-1.5g/kg(高于年轻人)", "钙": "1000mg/天", "维生素D": "20μg/天(老年人合成能力下降)", "维生素B12": "2.4μg/天(吸收率下降)", "膳食纤维": "25-30g/天", "水分": "1.5-2L/天(渴觉减退)"},
        "food_texture": ["软烂易咀嚼", "细碎不噎", "颜色丰富(刺激食欲)", "温度适宜(不过冷过热)"],
        "tips": ["力量训练(哪怕80岁)对维持肌肉至关重要", "晒太阳+补充D3防骨质流失", "每餐保证20-30g优质蛋白", "多喝汤羹(补水+营养)"]
    }
}


# ============================================================
# 七、食物搭配建议库
# ============================================================

FOOD_PAIRING = {
    "synergy": [
        {"combo": "维生素C + 铁", "explanation": "维生素C将三价铁还原为二价铁，大幅提高非血红素铁吸收率。如：青椒炒牛肉、番茄炖牛腩", "bonus": "青椒的维C是橙子的3倍"},
        {"combo": "脂肪 + 脂溶性维生素(ADEK)", "explanation": "维生素A、D、E、K需脂肪帮助吸收。如：胡萝卜用油炒、菠菜沙拉加橄榄油", "bonus": "煮胡萝卜加几滴油，β-胡萝卜素吸收率提升6倍"},
        {"combo": "维生素D + 钙", "explanation": "维生素D促进肠道对钙的吸收，缺D则补钙效率极低。如：三文鱼+奶酪", "bonus": "晒太阳15-30分钟得到的D比饮食多得多"},
        {"combo": "姜黄素 + 黑胡椒", "explanation": "黑胡椒中的胡椒碱可使姜黄素吸收率提高2000%。如：咖喱加黑胡椒", "bonus": "同样需要脂肪辅助吸收(用油炒)"},
        {"combo": "番茄红素 + 油脂 + 加热", "explanation": "番茄红素需加热+油脂才能充分释放。如：番茄炒蛋、番茄牛腩", "bonus": "煮熟的番茄红素生物利用率是生吃的4倍"},
        {"combo": "谷物 + 豆类", "explanation": "谷物赖氨酸低蛋氨酸高，豆类相反，搭配可互补成全蛋白。如：米饭+豆腐、豆粥", "bonus": "这是全球传统饮食的智慧(墨西哥玉米+豆，印度米+豆)"},
        {"combo": "益生元 + 益生菌", "explanation": "益生元(纤维)喂养益生菌，增强效果。如：酸奶+香蕉/燕麦", "bonus": "洋葱、大蒜、韭菜也是优质益生元"},
    ],
    "myth_busting": [
        {"myth": "菠菜+豆腐=结石", "truth": "草酸确实可与钙结合，但大部分在肠道结合后随粪便排出(而非在肾脏)。且菠菜焯水可去除大部分草酸。正常食用问题不大。", "verdict": "⚠️ 部分正确但被夸大"},
        {"myth": "海鲜+维生素C=砒霜", "truth": "海鲜中的砷主要以无毒有机砷形式存在，需要极大剂量(一次吃几百公斤海鲜+几千克维C)才可能产生毒性。", "verdict": "❌ 伪科学"},
        {"myth": "空腹吃香蕉伤胃", "truth": "香蕉含钾、镁，正常食用不会影响健康。除非肾功能严重不全(高钾血症风险)。", "verdict": "❌ 对健康人无害"},
        {"myth": "鸡蛋+豆浆=相克", "truth": "豆浆中的胰蛋白酶抑制剂在加热煮沸后已失活，不影响蛋白消化。", "verdict": "❌ 伪科学(豆浆必须煮沸)"},
        {"myth": "白萝卜+胡萝卜=破坏维C", "truth": "胡萝卜中的抗坏血酸氧化酶确实可破坏维C，但日常烹饪过程已使大部分酶失活。", "verdict": "⚠️ 微量影响，实际可忽略"},
        {"myth": "吃辣长痘", "truth": "辣椒本身不致痘，但辣菜常伴随高油高盐(火锅/麻辣烫)，以及辣会刺激皮脂分泌。", "verdict": "⚠️ 间接相关(高油高盐才是主因)"},
    ],
    "gi_reference": {
        "低GI(≤55)": ["燕麦(40)", "全麦面包(50)", "苹果(36)", "橙子(43)", "牛奶(27)", "豆类(18-35)", "红薯(54)", "山药(51)"],
        "中GI(56-69)": ["全麦面包(粗)(56)", "小米粥(62)", "土豆(62)", "南瓜(65)", "菠萝(66)", "蔗糖(65)"],
        "高GI(≥70)": ["白米饭(83)", "馒头(88)", "白面包(87)", "西瓜(72)", "葡萄糖(100)", "即食麦片(79)"]
    }
}


# ============================================================
# 八、食谱模板库
# ============================================================

MEAL_TEMPLATES = {
    "减脂": {
        "breakfast": [
            {"name": "高蛋白燕麦", "items": ["燕麦40g", "脱脂牛奶200ml", "鸡蛋白3个", "蓝莓50g"], "kcal": 380, "protein": 30, "prep": 10},
            {"name": "全麦三明治", "items": ["全麦面包2片", "鸡胸肉50g", "生菜", "番茄", "低脂芝士1片"], "kcal": 350, "protein": 28, "prep": 10},
            {"name": "中式减脂早餐", "items": ["小米粥1碗", "水煮蛋2个", "凉拌黄瓜"], "kcal": 320, "protein": 18, "prep": 15},
        ],
        "lunch": [
            {"name": "鸡胸藜麦碗", "items": ["鸡胸肉150g", "藜麦100g(生)", "西兰花200g", "橄榄油1勺"], "kcal": 520, "protein": 48, "prep": 30},
            {"name": "三文鱼蔬菜盘", "items": ["三文鱼150g", "糙米饭150g", "芦笋200g", "柠檬汁"], "kcal": 550, "protein": 38, "prep": 25},
            {"name": "清蒸鱼+杂粮", "items": ["鲈鱼200g", "杂粮饭150g", "清炒时蔬200g"], "kcal": 480, "protein": 45, "prep": 30},
        ],
        "dinner": [
            {"name": "蔬菜豆腐锅", "items": ["北豆腐200g", "菌菇100g", "菠菜150g", "虾仁50g"], "kcal": 320, "protein": 28, "prep": 20},
            {"name": "鸡肉沙拉", "items": ["鸡胸肉100g", "混合生菜200g", "牛油果半个", "油醋汁"], "kcal": 350, "protein": 30, "prep": 15},
        ],
        "snacks": [
            {"name": "蛋白加餐", "items": ["希腊酸奶150g", "坚果15g"], "kcal": 180, "protein": 15},
            {"name": "果蔬加餐", "items": ["苹果1个", "鸡蛋白2个"], "kcal": 150, "protein": 12},
        ]
    },
    "增肌": {
        "breakfast": [
            {"name": "增肌全餐", "items": ["全麦面包3片", "鸡蛋3个(全蛋)", "牛奶300ml", "香蕉1根", "花生酱1勺"], "kcal": 680, "protein": 38, "prep": 15},
            {"name": "燕麦能量碗", "items": ["燕麦60g", "全脂牛奶300ml", "蛋白粉1勺(30g)", "核桃20g", "蓝莓100g"], "kcal": 650, "protein": 40, "prep": 10},
        ],
        "lunch": [
            {"name": "牛肉能量盘", "items": ["牛肉(瘦)200g", "白米饭300g", "西兰花200g", "橄榄油1勺"], "kcal": 780, "protein": 52, "prep": 30},
            {"name": "鸡腿饭", "items": ["去骨鸡腿250g", "白米饭300g", "胡萝卜+青椒200g"], "kcal": 750, "protein": 55, "prep": 25},
        ],
        "dinner": [
            {"name": "三文鱼能量碗", "items": ["三文鱼200g", "红薯200g", "菠菜200g"], "kcal": 600, "protein": 45, "prep": 25},
            {"name": "虾仁炒蛋", "items": ["虾仁200g", "鸡蛋3个", "糙米饭200g", "秋葵150g"], "kcal": 620, "protein": 50, "prep": 20},
        ],
        "snacks": [
            {"name": "增肌餐间加餐", "items": ["蛋白粉1勺+牛奶250ml", "全麦吐司2片+花生酱"], "kcal": 400, "protein": 35},
            {"name": "睡前蛋白", "items": ["酪蛋白粉1勺+牛奶200ml"], "kcal": 200, "protein": 30},
        ]
    },
    "维持": {
        "breakfast": [
            {"name": "均衡早餐", "items": ["全麦面包2片", "鸡蛋1个", "牛奶200ml", "小番茄100g"], "kcal": 380, "protein": 20, "prep": 10},
            {"name": "中式早餐", "items": ["小米粥1碗", "煮鸡蛋1个", "凉拌木耳", "馒头半个"], "kcal": 350, "protein": 16, "prep": 15},
        ],
        "lunch": [
            {"name": "均衡午餐", "items": ["米饭200g", "蒸鱼150g", "蒜蓉西兰花150g"], "kcal": 500, "protein": 32, "prep": 30},
            {"name": "杂粮+鸡肉", "items": ["杂粮饭200g", "鸡腿肉150g", "炒时蔬200g"], "kcal": 520, "protein": 35, "prep": 25},
        ],
        "dinner": [
            {"name": "清淡晚餐", "items": ["杂粮粥200g", "虾仁100g", "清炒冬瓜200g"], "kcal": 350, "protein": 22, "prep": 20},
            {"name": "豆腐蔬菜", "items": ["北豆腐150g", "菌菇100g", "青菜200g"], "kcal": 300, "protein": 18, "prep": 15},
        ]
    }
}


# ============================================================
# 九、DRI 计算公式
# ============================================================

def calculate_bmr(weight, height, age, gender):
    """Mifflin-St Jeor 公式计算基础代谢率"""
    if gender == "male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161


def calculate_tdee(bmr, activity_level):
    """根据活动水平计算总能量消耗"""
    activity_multipliers = {
        "久坐": 1.2,       # 几乎不运动
        "轻度活动": 1.375,  # 1-3次/周
        "中度活动": 1.55,   # 3-5次/周
        "高度活动": 1.725,  # 5-7次/周
        "运动员": 1.9       # 每天高强度+体力工作
    }
    return bmr * activity_multipliers.get(activity_level, 1.2)


def calculate_target_calories(tdee, goal):
    """根据目标调整热量"""
    if goal == "减脂":
        return tdee - 500  # 500kcal缺口
    elif goal == "增肌":
        return tdee + 400  # 400kcal盈余
    else:  # 维持/健康饮食
        return tdee


def calculate_macros(target_calories, goal, weight):
    """计算三大营养素配比"""
    if goal == "减脂":
        protein_g = round(weight * 2.0)  # 减脂期高蛋白
        fat_kcal = target_calories * 0.25
        fat_g = round(fat_kcal / 9)
        carb_kcal = target_calories - (protein_g * 4) - fat_kcal
        carb_g = max(round(carb_kcal / 4), 50)  # 最少50g碳水
    elif goal == "增肌":
        protein_g = round(weight * 1.8)
        fat_kcal = target_calories * 0.25
        fat_g = round(fat_kcal / 9)
        carb_kcal = target_calories - (protein_g * 4) - fat_kcal
        carb_g = round(carb_kcal / 4)
    else:  # 维持
        protein_g = round(weight * 1.2)
        fat_kcal = target_calories * 0.25
        fat_g = round(fat_kcal / 9)
        carb_kcal = target_calories - (protein_g * 4) - fat_kcal
        carb_g = round(carb_kcal / 4)

    return {
        "protein_g": protein_g,
        "fat_g": fat_g,
        "carb_g": carb_g,
        "protein_kcal": protein_g * 4,
        "fat_kcal": fat_g * 9,
        "carb_kcal": carb_g * 4,
    }


def identify_constitution(answers):
    """
    根据5-8个问题的回答判定中医体质
    answers: dict with keys like "energy", "cold", "thirst", "sweat", "emotion", "complexion", "tongue", "stool"
    简化版自评，返回最可能的体质和次可能体质
    """
    scores = {c: 0 for c in TCM_CONSTITUTIONS}

    # 能量水平
    e = answers.get("energy", "")
    if "容易疲劳" in e or "乏力" in e: scores["气虚质"] += 3
    if "精力旺盛" in e: scores["平和质"] += 3

    # 怕冷/热
    c = answers.get("cold", "")
    if "怕冷" in c or "手脚冰凉" in c: scores["阳虚质"] += 4
    if "怕热" in c or "手足心热" in c: scores["阴虚质"] += 3

    # 口干
    t = answers.get("thirst", "")
    if "口干" in t or "想喝冷饮" in t: scores["阴虚质"] += 3
    if "口粘" in t or "不渴" in t: scores["痰湿质"] += 2

    # 出汗
    s = answers.get("sweat", "")
    if "动则汗出" in s or "夜间盗汗" in s: scores["阴虚质"] += 2
    if "不出汗" in s: scores["阳虚质"] += 1
    if "汗多粘腻" in s: scores["湿热质"] += 2

    # 情绪
    em = answers.get("emotion", "")
    if "焦虑" in em or "郁闷" in em or "压抑" in em: scores["气郁质"] += 4
    if "易怒" in em: scores["气郁质"] += 2

    # 面色
    cpx = answers.get("complexion", "")
    if "红润" in cpx: scores["平和质"] += 2
    if "晦暗" in cpx or "瘀斑" in cpx: scores["血瘀质"] += 3
    if "油光" in cpx or "痤疮" in cpx: scores["湿热质"] += 3

    # 体型
    body = answers.get("body", "")
    if "偏胖" in body or "腹部大" in body: scores["痰湿质"] += 4
    if "消瘦" in body: scores["阴虚质"] += 1

    # 过敏
    al = answers.get("allergy", "")
    if "过敏" in al or "鼻炎" in al or "湿疹" in al: scores["特禀质"] += 5

    # 大便
    stool = answers.get("stool", "")
    if "稀溏" in stool or "不成形" in stool: scores["阳虚质"] += 2; scores["气虚质"] += 2
    if "粘滞" in stool or "不爽" in stool: scores["湿热质"] += 3
    if "干燥" in stool or "便秘" in stool: scores["阴虚质"] += 2

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary = sorted_scores[0]
    secondary = sorted_scores[1]

    if primary[1] == 0:  # 无法判定
        return {"primary": "平和质", "secondary": "平和质", "confidence": "低"}

    return {
        "primary": primary[0],
        "primary_score": primary[1],
        "secondary": secondary[0],
        "secondary_score": secondary[1],
        "confidence": "高" if primary[1] >= 5 else "中" if primary[1] >= 3 else "低",
        "all_scores": dict(sorted_scores)
    }


def search_food(keyword):
    """模糊搜索食物"""
    keyword_lower = keyword.lower().strip()
    results = []
    for name, data in FOOD_DB.items():
        if keyword_lower in name.lower():
            results.append((name, data))
    return results


def get_top_foods(nutrient_name, top_n=10):
    """获取某营养素的最佳食物来源"""
    if nutrient_name not in NUTRIENT_DB:
        return []
    sources = NUTRIENT_DB[nutrient_name]["food_sources"]
    return sorted(sources, key=lambda x: x[1], reverse=True)[:top_n]


def format_nutrition(food_name, amount_g=100):
    """格式化食品营养成分"""
    if food_name not in FOOD_DB:
        return None
    data = FOOD_DB[food_name]
    scale = amount_g / 100
    return {
        "name": food_name,
        "amount": amount_g,
        "kcal": round(data["kcal"] * scale),
        "protein": round(data["protein"] * scale, 1),
        "fat": round(data["fat"] * scale, 1),
        "carbs": round(data["carbs"] * scale, 1),
        "fiber": round(data["fiber"] * scale, 1),
        "gi": data["gi"],
        "category": data["category"],
        "key_nutrients": data["key_nutrients"]
    }


if __name__ == "__main__":
    # 快速测试
    print(f"Food DB: {len(FOOD_DB)} foods")
    print(f"Nutrient DB: {len(NUTRIENT_DB)} nutrients")
    print(f"TCM Constitutions: {len(TCM_CONSTITUTIONS)} types")
    print(f"Disease nutrition: {len(DISEASE_NUTRITION)} conditions")
    print(f"Meal templates: {sum(len(v2) for v1 in MEAL_TEMPLATES.values() for v2 in v1.values())} recipes")

    # 测试BMR计算
    bmr = calculate_bmr(70, 175, 30, "male")
    print(f"\nBMR test (male, 70kg, 175cm, 30yo): {bmr:.0f} kcal")
    tdee = calculate_tdee(bmr, "中度活动")
    print(f"TDEE test: {tdee:.0f} kcal")
    macros = calculate_macros(calculate_target_calories(tdee, "减脂"), "减脂", 70)
    print(f"Macros (减脂): P={macros['protein_g']}g, F={macros['fat_g']}g, C={macros['carb_g']}g")

    # 测试体质判定
    test_answers = {"energy": "容易疲劳", "cold": "怕冷", "thirst": "不渴", "body": "偏胖"}
    constitution = identify_constitution(test_answers)
    print(f"\nConstitution test: {constitution['primary']} (score:{constitution['primary_score']})")
