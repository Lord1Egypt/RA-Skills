import difflib

province_all = ["北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海", "江苏", "浙江", "安徽",
                "福建", "江西",
                "山东", "河南", "湖北", "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州", "云南", "陕西", "甘肃",
                "青海", "宁夏"]

courses_all = ["物理", "化学", "生物", "历史", "地理", "政治", "技术"]

major_all = ["哲学类", "经济学类", "财政学类", "金融学类", "经济与贸易类", "法学类", "政治学类", "社会学类", "民族学类",
             "马克思主义理论类", "公安学类", "教育学类", "体育学类", "中国语言文学类", "外国语言文学类",
             "新闻传播学类", "历史学类", "数学类", "物理学类", "化学类", "天文学类", "地理科学类", "大气科学类",
             "海洋科学类", "地球物理学类", "地质学类", "生物科学类", "心理学类", "统计学类", "力学类", "机械类",
             "仪器类", "材料类", "能源动力类", "电气类", "电子信息类", "自动化类", "计算机类", "土木类", "水利类",
             "测绘类", "化工与制药类", "地质类", "矿业类", "纺织类", "轻工类", "交通运输类", "海洋工程类", "航空航天类",
             "兵器类", "核工程类", "农业工程类", "林业工程类", "环境科学与工程类", "生物医学工程类", "食品科学与工程类",
             "建筑类", "安全科学与工程类", "生物工程类", "公安技术类", "交叉工程类", "植物生产类",
             "自然保护与环境生态类", "动物生产类", "动物医学类", "林学类", "水产类", "草学类", "基础医学类",
             "临床医学类", "口腔医学类", "公共卫生与预防医学类", "中医学类", "中西医结合类", "药学类", "中药学类",
             "法医学类", "医学技术类", "护理学类", "管理科学与工程类", "工商管理类", "农业经济管理类", "公共管理类",
             "图书情报与档案管理类", "物流管理与工程类", "工业工程类", "电子商务类", "旅游管理类",
             "艺术学理论类", "音乐与舞蹈学类", "戏剧与影视学类", "美术学类", "设计学类"]


def verify_correct_info(province, courses, score, rank, majors):
    # 校验省市
    if province not in province_all:
        return {"code": "failed", "msg": "找不到该省市，请确认省市是否正确并且是目前支持的省市"}
    # 校验选科
    courses_lst = courses.replace("[", "").replace("]", "").split(',')
    if len(courses_lst) == 0:
        return {"code": "failed", "msg": "选科信息为空"}
    for course in courses_lst:
        if course not in courses_all:
            return {"code": "failed", "msg": "选科信息错误，请确认选科信息是否正确"}
    # 校验分数
    if score < 0 or score > 2000:
        return {"code": "failed", "msg": "分数错误，不能小于0或者大于总分"}
    # 校验分数
    if rank < 0:
        return {"code": "failed", "msg": "位次错误，不能小于0"}
    # 校验倾向专业大类
    majors_lst = majors.replace("[", "").replace("]", "").split(',')
    majors_lst_correct = []
    for major in majors_lst:
        major = major.strip()
        if not major:
            continue
        # 优先精确匹配
        if major in major_all:
            majors_lst_correct.append(major)
            continue
        # 模糊匹配
        best_match = None
        max_diff_score = -1.0
        for candidate in major_all:
            diff_score = difflib.SequenceMatcher(None, major, candidate).ratio()
            # 只取最相似的那个 (不需要阈值，强制更新最大值)
            if diff_score > max_diff_score:
                max_diff_score = diff_score
                best_match = candidate
        if best_match:
            majors_lst_correct.append(best_match)

    return {
        "code": "success",
        "msg": "校验成功",
        "data": {
            "province": province,
            "courses": courses,
            "score": score,
            "rank": rank,
            "majors": ",".join(majors_lst_correct)
        }
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--province", type=str, required=True, help="省份")
    parser.add_argument("--courses", type=str, required=True, help="选科组合")
    parser.add_argument("--score", type=int, required=True, help="高考分数")
    parser.add_argument("--rank", type=int, required=False, help="高考位次")
    parser.add_argument("--majors", type=str, required=True, help="专业大类")
    args = parser.parse_args()

    print(verify_correct_info(province=args.province,
                              courses=args.courses,
                              score=args.score,
                              rank=args.rank,
                              majors=args.majors))
