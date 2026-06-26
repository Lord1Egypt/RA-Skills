"""
刑冲合害分析模块
分析命盘四柱之间的地支关系和天干关系
"""

# 六合
LIU_HE = {
    "子": "丑", "丑": "子",
    "寅": "亥", "亥": "寅",
    "卯": "戌", "戌": "卯",
    "辰": "酉", "酉": "辰",
    "巳": "申", "申": "巳",
    "午": "未", "未": "午",
}

# 六合结果
LIU_HE_RESULT = {
    ("子", "丑"): "子丑合土", ("丑", "子"): "子丑合土",
    ("寅", "亥"): "寅亥合木", ("亥", "寅"): "寅亥合木",
    ("卯", "戌"): "卯戌合火", ("戌", "卯"): "卯戌合火",
    ("辰", "酉"): "辰酉合金", ("酉", "辰"): "辰酉合金",
    ("巳", "申"): "巳申合水", ("申", "巳"): "巳申合水",
    ("午", "未"): "午未合土", ("未", "午"): "午未合土",
}

# 三合局
SAN_HE = [
    ({"申", "子", "辰"}, "申子辰合水局"),
    ({"亥", "卯", "未"}, "亥卯未合木局"),
    ({"寅", "午", "戌"}, "寅午戌合火局"),
    ({"巳", "酉", "丑"}, "巳酉丑合金局"),
]

# 六冲
LIU_CHONG = {
    frozenset(["子", "午"]): "子午冲",
    frozenset(["丑", "未"]): "丑未冲",
    frozenset(["寅", "申"]): "寅申冲",
    frozenset(["卯", "酉"]): "卯酉冲",
    frozenset(["辰", "戌"]): "辰戌冲",
    frozenset(["巳", "亥"]): "巳亥冲",
}

# 三刑
SAN_XING = [
    ({"寅", "巳", "申"}, "寅巳申无恩之刑"),
    ({"丑", "戌", "未"}, "丑戌未恃势之刑"),
]

# 两两相刑（包括部分三刑的两两组合）
XING_PAIRS = {
    frozenset(["寅", "巳"]): "寅巳刑",
    frozenset(["巳", "申"]): "巳申刑",
    frozenset(["寅", "申"]): "寅申刑",
    frozenset(["丑", "戌"]): "丑戌刑",
    frozenset(["戌", "未"]): "戌未刑",
    frozenset(["丑", "未"]): "丑未刑",
    frozenset(["子", "卯"]): "子卯无礼之刑",
}

# 自刑
ZI_XING = {"辰", "午", "酉", "亥"}

# 六害
LIU_HAI = {
    frozenset(["子", "未"]): "子未害",
    frozenset(["丑", "午"]): "丑午害",
    frozenset(["寅", "巳"]): "寅巳害",
    frozenset(["卯", "辰"]): "卯辰害",
    frozenset(["申", "亥"]): "申亥害",
    frozenset(["酉", "戌"]): "酉戌害",
}

# 天干五合
TIAN_GAN_HE = {
    frozenset(["甲", "己"]): "甲己合土",
    frozenset(["乙", "庚"]): "乙庚合金",
    frozenset(["丙", "辛"]): "丙辛合水",
    frozenset(["丁", "壬"]): "丁壬合木",
    frozenset(["戊", "癸"]): "戊癸合火",
}

# 天干冲
TIAN_GAN_CHONG = {
    frozenset(["甲", "庚"]): "甲庚冲",
    frozenset(["乙", "辛"]): "乙辛冲",
    frozenset(["丙", "壬"]): "丙壬冲",
    frozenset(["丁", "癸"]): "丁癸冲",
}

# 四柱位置名
POS_NAMES = {
    "year": "年", "month": "月", "day": "日", "hour": "时"
}


def analyze_relationships(pillars):
    """
    分析命盘四柱之间的所有关系（刑冲合害）
    
    Args:
        pillars: dict with year/month/day/hour, each having stem and branch
    
    Returns:
        list of dict: [{"type": "六合", "positions": [...], "result": "..."}]
    """
    results = []
    positions = ["year", "month", "day", "hour"]
    
    # 提取地支和天干
    branches = {pos: pillars[pos]["branch"] for pos in positions}
    stems = {pos: pillars[pos]["stem"] for pos in positions}
    
    branch_list = list(branches.values())
    
    # --- 地支关系分析 ---
    
    # 六合（两两检查）
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            b1, b2 = branches[positions[i]], branches[positions[j]]
            key = (b1, b2)
            if key in LIU_HE_RESULT:
                results.append({
                    "type": "六合",
                    "positions": [f"{POS_NAMES[positions[i]]}支{b1}", f"{POS_NAMES[positions[j]]}支{b2}"],
                    "result": LIU_HE_RESULT[key],
                })
    
    # 三合（需要三个地支齐全）
    branch_set = set(branch_list)
    for required, result_str in SAN_HE:
        matched = required & branch_set
        if len(matched) >= 3:
            # 找到所有匹配的位置
            pos_strs = []
            for pos in positions:
                if branches[pos] in required:
                    pos_strs.append(f"{POS_NAMES[pos]}支{branches[pos]}")
            results.append({
                "type": "三合",
                "positions": pos_strs,
                "result": result_str,
            })
    
    # 六冲
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            b1, b2 = branches[positions[i]], branches[positions[j]]
            key = frozenset([b1, b2])
            if key in LIU_CHONG:
                results.append({
                    "type": "六冲",
                    "positions": [f"{POS_NAMES[positions[i]]}支{b1}", f"{POS_NAMES[positions[j]]}支{b2}"],
                    "result": LIU_CHONG[key],
                })
    
    # 三刑（需要三个齐全）
    for required, result_str in SAN_XING:
        matched = required & branch_set
        if len(matched) >= 3:
            pos_strs = []
            for pos in positions:
                if branches[pos] in required:
                    pos_strs.append(f"{POS_NAMES[pos]}支{branches[pos]}")
            results.append({
                "type": "三刑",
                "positions": pos_strs,
                "result": result_str,
            })
    
    # 两两相刑（如果没有形成三刑）
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            b1, b2 = branches[positions[i]], branches[positions[j]]
            key = frozenset([b1, b2])
            if key in XING_PAIRS:
                # 检查是否已经包含在三刑结果中
                already_in_sanxing = False
                for r in results:
                    if r["type"] == "三刑":
                        already_in_sanxing = True
                        break
                if not already_in_sanxing:
                    results.append({
                        "type": "相刑",
                        "positions": [f"{POS_NAMES[positions[i]]}支{b1}", f"{POS_NAMES[positions[j]]}支{b2}"],
                        "result": XING_PAIRS[key],
                    })
    
    # 自刑
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            if branches[positions[i]] == branches[positions[j]] and branches[positions[i]] in ZI_XING:
                b = branches[positions[i]]
                results.append({
                    "type": "自刑",
                    "positions": [f"{POS_NAMES[positions[i]]}支{b}", f"{POS_NAMES[positions[j]]}支{b}"],
                    "result": f"{b}{b}自刑",
                })
    
    # 六害
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            b1, b2 = branches[positions[i]], branches[positions[j]]
            key = frozenset([b1, b2])
            if key in LIU_HAI:
                results.append({
                    "type": "六害",
                    "positions": [f"{POS_NAMES[positions[i]]}支{b1}", f"{POS_NAMES[positions[j]]}支{b2}"],
                    "result": LIU_HAI[key],
                })
    
    # --- 天干关系分析 ---
    
    # 天干五合
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            s1, s2 = stems[positions[i]], stems[positions[j]]
            key = frozenset([s1, s2])
            if key in TIAN_GAN_HE:
                results.append({
                    "type": "天干合",
                    "positions": [f"{POS_NAMES[positions[i]]}干{s1}", f"{POS_NAMES[positions[j]]}干{s2}"],
                    "result": TIAN_GAN_HE[key],
                })
    
    # 天干冲
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            s1, s2 = stems[positions[i]], stems[positions[j]]
            key = frozenset([s1, s2])
            if key in TIAN_GAN_CHONG:
                results.append({
                    "type": "天干冲",
                    "positions": [f"{POS_NAMES[positions[i]]}干{s1}", f"{POS_NAMES[positions[j]]}干{s2}"],
                    "result": TIAN_GAN_CHONG[key],
                })
    
    return results
