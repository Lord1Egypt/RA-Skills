"""Brand name → che168 URL pinyin slug mapping.

che168.com uses pinyin brand slugs in URLs: /beijing/baoma/ (宝马/BMW).
Includes common aliases.
"""

CHE168_BRAND_SLUG: dict[str, str] = {
    # German
    "宝马": "baoma",
    "BMW": "baoma",
    "奔驰": "benchi",
    "梅赛德斯": "benchi",
    "奥迪": "aodi",
    "大众": "dazhong",
    "保时捷": "baoshijie",
    "迈巴赫": "maibaha",
    # Japanese
    "丰田": "fengtian",
    "本田": "bentian",
    "日产": "richan",
    "马自达": "mazida",
    "雷克萨斯": "leikesasi",
    "英菲尼迪": "yingfeinidi",
    "讴歌": "ouge",
    "斯巴鲁": "sibalu",
    "三菱": "sanling",
    "铃木": "lingmu",
    # American
    "福特": "fute",
    "雪佛兰": "xuefulan",
    "别克": "bieke",
    "凯迪拉克": "kaidilake",
    "Jeep": "jipu",
    "吉普": "jipu",
    "林肯": "linken",
    "特斯拉": "tesila",
    "克莱斯勒": "kelaisile",
    "道奇": "daoqi",
    "悍马": "hanma",
    # Korean
    "现代": "xiandai",
    "起亚": "qiya",
    # French / Italian
    "标致": "biaozhi",
    "雪铁龙": "xuetielong",
    "雷诺": "leinuo",
    "法拉利": "falali",
    "兰博基尼": "lanbojini",
    "玛莎拉蒂": "mashaladi",
    "阿尔法·罗密欧": "aerfalamiou",
    # British / Swedish
    "路虎": "luhu",
    "捷豹": "jiebao",
    "沃尔沃": "woerwo",
    "MINI": "mini",
    "劳斯莱斯": "laosikuaisi",
    "宾利": "binli",
    "阿斯顿马丁": "asidunmading",
    "迈凯伦": "maikailun",
    # Chinese — domestic
    "比亚迪": "biyadi",
    "BYD": "biyadi",
    "吉利": "jili",
    "长安": "changan",
    "长城": "changcheng",
    "哈弗": "hafu",
    "WEY": "wey",
    "魏牌": "wey",
    "奇瑞": "qirui",
    "红旗": "hongqi",
    "一汽": "yiqi",
    "广汽传祺": "chuanqi",
    "传祺": "chuanqi",
    "荣威": "rongwei",
    "名爵": "mingjue",
    "MG": "mingjue",
    "五菱": "wuling",
    "宝骏": "baojun",
    "东风": "dongfeng",
    "江淮": "jianghuai",
    "众泰": "zhongtai",
    "北汽": "beiqi",
    "北京": "beijingqc",
    "华晨": "huachen",
    "中华": "zhonghua",
    "猎豹": "liebao",
    "陆风": "lufeng",
    "海马": "haima",
    "力帆": "lifan",
    "观致": "guanzhi",
    "启辰": "qichen",
    "纳智捷": "nazhijie",
    "野马": "yema",
    # Chinese — new energy
    "蔚来": "weilai",
    "NIO": "weilai",
    "理想": "lixiang",
    "理想汽车": "lixiang",
    "小鹏": "xiaopeng",
    "小鹏汽车": "xiaopeng",
    "零跑": "lingpao",
    "哪吒": "nezha",
    "哪吒汽车": "nezha",
    "极氪": "jike",
    "极狐": "jihu",
    "岚图": "lantu",
    "阿维塔": "aweita",
    "智己": "zhiji",
    "飞凡": "feifan",
    "极越": "jiyue",
    "小米": "xiaomi",
    "小米汽车": "xiaomi",
    "问界": "wenjie",
    "华为": "wenjie",
    "仰望": "yangwang",
    "方程豹": "fangchengbao",
    "腾势": "tengshi",
    "深蓝": "shenlan",
    "启源": "qiyuan",
    "银河": "yinhe",
    "坦克": "tanke",
    "欧拉": "oula",
    "高合": "gaohe",
    "创维": "skyworth",
    "合创": "hechuang",
    "睿蓝": "ruilan",
    "远航": "yuanhang",
    "昊铂": "haopo",
    "埃安": "aion",
    "iCAR": "icar",
}


def get_brand_slug(brand: str) -> str | None:
    """Get che168 URL slug for a brand. None if not found."""
    if not brand:
        return None
    slug = CHE168_BRAND_SLUG.get(brand)
    if slug:
        return slug
    for name, s in CHE168_BRAND_SLUG.items():
        if brand.lower() == name.lower():
            return s
    return None
