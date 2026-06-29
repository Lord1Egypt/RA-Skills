"""
无障碍旅行助手 - Accessible Travel Guide
查询国内热门景点和酒店的无障碍设施信息，为轮椅使用者、视障听障人士、老年人和带婴儿车出行者提供出行建议。
"""
import json
import os
import ssl
import urllib.request
import urllib.parse

PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")
ALLOWED_DOMAINS = [
    "1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com",
    "1439498936-bl10af74fl.ap-guangzhou.tencentscf.com",
]

# ========== 景点无障碍数据库 ==========
SPOTS_DB = {
    "北京故宫": {
        "city": "北京",
        "level": "5A",
        "accessibility": {
            "wheelchair": {
                "accessible": True,
                "details": "午门入口有无障碍通道（东侧），太和门/中和殿/保和殿/御花园均可轮椅通行。乾清宫区域有少量台阶需绕行。珍宝馆和钟表馆有坡道入口。",
                "routes": "午门→太和门→中和殿→保和殿→乾清门→乾清宫(绕行)→御花园→神武门出，全程约2.5公里，坡度≤8°",
                "rental": "午门和神武门服务处可免费租借轮椅（押金500元），数量约20台/处",
                "restrooms": "太和门西侧、乾清门东侧、御花园北侧各有一处无障碍卫生间",
                "tips": "建议从东华门进入走无障碍通道，避开午门主入口人流高峰"
            },
            "visual": {
                "accessible": True,
                "details": "提供语音导览器（中英日韩），部分展馆有触摸式展品复制品。珍宝馆和钟表馆语音讲解最丰富。",
                "services": "服务处可申请志愿者陪同讲解（需提前1天预约）"
            },
            "hearing": {
                "accessible": True,
                "details": "语音导览器有字幕模式，钟表馆每日有文字版演示说明",
                "services": "可申请手语讲解志愿者（需提前3天预约，电话010-85007938）"
            },
            "stroller": {
                "accessible": True,
                "details": "与轮椅路线相同，午门无障碍通道可推婴儿车。部分门槛较高需抬车。御花园石板路颠簸建议慢行。"
            },
            "elderly": {
                "accessible": True,
                "details": "全程平缓无大坡，但面积大（72万㎡）步行距离长。建议乘坐电瓶车（珍宝馆-御花园段），票价10元。60岁以上半价门票。"
            }
        },
        "discount": "残疾人凭残疾证免票，60岁以上半价，70岁以上免票",
        "contact": "010-85007938（无障碍服务预约）"
    },
    "北京颐和园": {
        "city": "北京",
        "level": "5A",
        "accessibility": {
            "wheelchair": {
                "accessible": True,
                "details": "东宫门入口有无障碍通道。长廊全程平坦可轮椅通行。佛香阁有电梯可到二层平台（需工作人员开启）。苏州街区域有台阶不建议前往。",
                "routes": "东宫门→仁寿殿→长廊→排云殿(远观)→石舫→苏州街(外部)→北宫门出，全程约4公里",
                "rental": "东宫门和北宫门游客中心可免费租借轮椅",
                "restrooms": "仁寿殿东侧、长廊中段、石舫附近有无障碍卫生间",
                "tips": "昆明湖边步道平坦宽阔，适合轮椅游览。避免走万寿山后山"
            },
            "visual": {
                "accessible": True,
                "details": "提供语音导览，长廊彩画有语音描述版本"
            },
            "hearing": {
                "accessible": True,
                "details": "提供文字版导览手册"
            },
            "stroller": {
                "accessible": True,
                "details": "长廊和湖边步道推婴儿车很方便，佛香阁路段建议不推车"
            },
            "elderly": {
                "accessible": True,
                "details": "长廊段可全程坐轮椅或推车，建议避开万寿山爬坡路段。园内游船可坐轮椅。"
            }
        },
        "discount": "残疾人免票，60岁以上半价，70岁以上免票",
        "contact": "010-62881144"
    },
    "北京天坛": {
        "city": "北京",
        "level": "5A",
        "accessibility": {
            "wheelchair": {
                "accessible": True,
                "details": "各门均有无障碍通道。祈年殿有专用坡道（东侧），回音壁外圈可轮椅通行。丹陛桥长360米但坡度极缓。",
                "routes": "南门→圜丘→回音壁→丹陛桥→祈年殿→东门出，全程约2公里",
                "rental": "东门和南门游客中心可免费租借轮椅",
                "restrooms": "祈年殿东侧、回音壁北侧有无障碍卫生间",
                "tips": "圜丘台有三层台阶无坡道，轮椅无法上台，可在台下观赏"
            },
            "stroller": {
                "accessible": True,
                "details": "园区道路平坦，祈年殿有坡道可推车。丹陛桥长但缓。"
            },
            "elderly": {
                "accessible": True,
                "details": "天坛公园绿化好、道路平坦，适合老年人散步。建议春秋季游览，夏季遮阴少。"
            }
        },
        "discount": "残疾人免票，60岁以上半价，70岁以上免票",
        "contact": "010-67022617"
    },
    "西安兵马俑": {
        "city": "西安",
        "level": "5A",
        "accessibility": {
            "wheelchair": {
                "accessible": True,
                "details": "一号坑和三号坑有无障碍坡道入口，二号坑需从侧门进入。坑周边观景平台均可轮椅通行。秦始皇陵遗址公园有电瓶车。",
                "routes": "入口→一号坑(无障碍入口在南侧)→二号坑(侧门)→三号坑→文物陈列厅→电瓶车至丽山园",
                "rental": "游客服务中心可免费租借轮椅",
                "restrooms": "各坑之间休息区均设有无障碍卫生间",
                "tips": "建议先看一号坑（最大最壮观），再参观其他。丽山园较远建议坐电瓶车。"
            },
            "visual": {
                "accessible": True,
                "details": "提供语音导览器，陈列厅有触摸复制品"
            },
            "stroller": {
                "accessible": True,
                "details": "一号坑观景平台宽敞可推车，但人流大时拥挤"
            },
            "elderly": {
                "accessible": True,
                "details": "场馆内较平坦，但面积大步行距离长。建议坐电瓶车往返丽山园。65岁以上免票。"
            }
        },
        "discount": "残疾人免票，65岁以上免票",
        "contact": "029-81399001"
    },
    "杭州西湖": {
        "city": "杭州",
        "level": "5A",
        "accessibility": {
            "wheelchair": {
                "accessible": True,
                "details": "环湖步道大部分平坦可轮椅通行（苏堤/白堤/湖滨路）。断桥有缓坡可上。雷峰塔有无障碍电梯直达顶层。三潭印月游船可上轮椅。",
                "routes": "湖滨→断桥→白堤→孤山→苏堤→花港观鱼→雷峰塔→净慈寺，环湖约15公里",
                "rental": "湖滨游客中心、雷峰塔入口可租借轮椅",
                "restrooms": "湖滨、白堤中段、苏堤南北端、雷峰塔旁有无障碍卫生间",
                "tips": "苏堤较长（2.8公里），轮椅建议只走半程。西湖游船码头有无障碍登船设施。"
            },
            "stroller": {
                "accessible": True,
                "details": "环湖步道全程可推婴儿车，苏堤白堤平坦好走。游船可推车上船。"
            },
            "elderly": {
                "accessible": True,
                "details": "环湖有大量休息座椅，建议坐游船代替步行。雷峰塔有电梯。免费景区（西湖大景区免费）。"
            }
        },
        "discount": "西湖大景区免费，雷峰塔等小景点残疾人免票，70岁以上免票",
        "contact": "0571-87179603"
    },
    "上海外滩": {
        "city": "上海",
        "level": "4A",
        "accessibility": {
            "wheelchair": {
                "accessible": True,
                "details": "外滩观光平台全程平坦，无障碍通道从南京东路入口进入。观光隧道有专用通道。对岸陆家嘴滨江步道同样平坦。",
                "routes": "南京东路口→观光平台→陈毅广场→外白渡桥→折返，约1.5公里",
                "rental": "外滩游客中心不提供轮椅租借，建议自带",
                "restrooms": "陈毅广场附近有无障碍卫生间",
                "tips": "观光平台人多时轮椅通行需耐心，建议傍晚人少时前往"
            },
            "stroller": {
                "accessible": True,
                "details": "观光平台全程平坦，推婴儿车很方便"
            },
            "elderly": {
                "accessible": True,
                "details": "全程平坦无坡度，大量座椅可休息。夜景最美但人多注意安全。"
            }
        },
        "discount": "外滩观光平台免费开放",
        "contact": "021-63260300"
    },
    "上海迪士尼": {
        "city": "上海",
        "level": "5A",
        "accessibility": {
            "wheelchair": {
                "accessible": True,
                "details": "园区主要道路均可轮椅通行。多数游乐设施有轮椅专用通道（入口处告知工作人员）。花车巡游有轮椅观赏区。城堡前有坡道。",
                "routes": "入口→米奇大街→奇想花园→明日世界→梦幻世界→宝藏湾→探险岛",
                "rental": "入园处Guest Services可租借轮椅（90元/天），电动轮椅（380元/天）",
                "restrooms": "每个主题区域均设有无障碍卫生间",
                "tips": "热门项目可领取DAS（残障通行服务）卡，减少排队时间。需在Guest Services登记。"
            },
            "visual": {
                "accessible": True,
                "details": "提供音频描述设备，可在Guest Services领取"
            },
            "hearing": {
                "accessible": True,
                "details": "提供手语翻译预约服务，部分演出有字幕"
            },
            "stroller": {
                "accessible": True,
                "details": "推婴儿车游览方便，各项目入口有婴儿车停放区"
            },
            "elderly": {
                "accessible": True,
                "details": "园区面积大建议租轮椅代步。DAS卡同样适用行动不便老人。花车和烟花表演有座椅区。"
            }
        },
        "discount": "持残疾证可购买优惠票（约7.5折），需现场购买",
        "contact": "400-180-0000"
    },
    "成都大熊猫基地": {
        "city": "成都",
        "level": "5A",
        "accessibility": {
            "wheelchair": {
                "accessible": True,
                "details": "新建区域（熊猫塔/熊猫谷）全程无障碍。老区部分木栈道有台阶但可绕行。园区有电瓶车。",
                "routes": "南门→熊猫塔→太阳产房→月亮产房→熊猫谷→电瓶车返回",
                "rental": "南门游客中心可免费租借轮椅",
                "restrooms": "各休息区均有无障碍卫生间",
                "tips": "建议早上8点入园看熊猫活动（9点后熊猫多在睡觉），电瓶车20元/人"
            },
            "stroller": {
                "accessible": True,
                "details": "新区平坦好推车，老区部分木栈道需慢行"
            },
            "elderly": {
                "accessible": True,
                "details": "园区有大量遮阴区域，电瓶车可代步。60岁以上半价。"
            }
        },
        "discount": "残疾人免票，60岁以上半价，65岁以上免票",
        "contact": "028-83510033"
    },
    "南京中山陵": {
        "city": "南京",
        "level": "5A",
        "accessibility": {
            "wheelchair": {
                "accessible": False,
                "details": "中山陵主体392级台阶无坡道，轮椅无法登顶。但陵园路、音乐台、中山植物园区域可轮椅通行。陵前广场可远观。",
                "rental": "景区入口游客中心可租借轮椅",
                "restrooms": "入口处和音乐台有无障碍卫生间",
                "tips": "轮椅用户建议游览音乐台（平坦，白鸽互动）和中山植物园，放弃登陵"
            },
            "stroller": {
                "accessible": False,
                "details": "同轮椅，392级台阶无法推车。建议只逛陵前广场和音乐台。"
            },
            "elderly": {
                "accessible": True,
                "details": "392级台阶对体力要求高，建议量力而行。可只在广场和音乐台游览。景区观光车可到达入口处。"
            }
        },
        "discount": "免费景区（需预约），残疾人和70岁以上免预约",
        "contact": "025-84431991"
    },
    "厦门鼓浪屿": {
        "city": "厦门",
        "level": "5A",
        "accessibility": {
            "wheelchair": {
                "accessible": False,
                "details": "鼓浪屿全岛无机动车，道路多为石板路和坡道，轮椅通行困难。码头到商业街路段相对平坦可勉强通行，但多数景点需爬坡上台阶。建议慎重考虑。",
                "rental": "岛上无轮椅租借服务",
                "restrooms": "商业街区域有无障碍卫生间，景点内较少",
                "tips": "如必须前往，建议只在三丘田码头-商业街-菽庄花园一线活动，避免上坡路段"
            },
            "stroller": {
                "accessible": False,
                "details": "石板路颠簸，上下坡多，推婴儿车体验差"
            },
            "elderly": {
                "accessible": True,
                "details": "体力好的老人可慢行，有电瓶车（环岛线）可代步。建议只走商业街区域。"
            }
        },
        "discount": "残疾人凭残疾证船票半价，上岛免费",
        "contact": "0592-2060777"
    },
    "张家界国家森林公园": {
        "city": "张家界",
        "level": "5A",
        "accessibility": {
            "wheelchair": {
                "accessible": True,
                "details": "天门山玻璃栈道有轮椅专用段（A线），天门山索道可上轮椅。百龙天梯可乘轮椅。金鞭溪步道前段平坦可通行（约2公里后需原路返回）。",
                "routes": "天门山索道上山→玻璃栈道(A线)→天门洞广场→索道下山。金鞭溪走前段原路返回。",
                "rental": "天门山游客中心可租借轮椅",
                "restrooms": "天门山顶站和索道中站有无障碍卫生间",
                "tips": "天门山比森林公园更适合轮椅用户。十里画廊有小火车可坐。袁家界部分观景台可到但需绕行。"
            },
            "stroller": {
                "accessible": False,
                "details": "山区地形复杂，多数路段不适合推婴儿车。天门山可推车但人流密集时需注意安全。"
            },
            "elderly": {
                "accessible": True,
                "details": "天门山索道+山顶步道对老年人友好。百龙天梯省去大量台阶。景区有大量休息点。65岁以上免票。"
            }
        },
        "discount": "残疾人免票，65岁以上免票",
        "contact": "0744-5611198"
    },
    "桂林漓江": {
        "city": "桂林",
        "level": "5A",
        "accessibility": {
            "wheelchair": {
                "accessible": True,
                "details": "漓江游船可上轮椅（竹江码头/磨盘山码头有工作人员协助）。象鼻山公园平坦可轮椅通行。两江四湖夜游船也可上轮椅。",
                "rental": "桂林市区酒店多有轮椅租借服务",
                "restrooms": "游船上有无障碍卫生间（大型船），码头有",
                "tips": "游船是最好的观景方式，无需步行即可欣赏全程风光。建议选大型游船（设施更完善）。"
            },
            "stroller": {
                "accessible": True,
                "details": "游船可推婴儿车，象鼻山和市区步道平坦"
            },
            "elderly": {
                "accessible": True,
                "details": "游船观景最适合老年人，全程坐船无需步行。阳朔西街平坦适合散步。"
            }
        },
        "discount": "残疾人免景区门票，游船无优惠",
        "contact": "0773-2823874"
    },
    "苏州园林（拙政园）": {
        "city": "苏州",
        "level": "5A",
        "accessibility": {
            "wheelchair": {
                "accessible": True,
                "details": "拙政园东部和中部主要路线可轮椅通行，有专门的无障碍游览路线图（入口处领取）。西部部分区域有台阶需绕行。留园、狮子林同样部分可达。",
                "rental": "拙政园入口可租借轮椅",
                "restrooms": "园区入口附近有无障碍卫生间",
                "tips": "园林门槛较多但多数有临时坡板，需请工作人员协助。建议工作日前往人少时体验更好。"
            },
            "stroller": {
                "accessible": True,
                "details": "与轮椅路线相同，部分门槛需抬车。园林石子路颠簸建议慢行。"
            },
            "elderly": {
                "accessible": True,
                "details": "园林面积不大步行距离适中，大量亭台可休息。60岁以上半价，70岁以上免票。"
            }
        },
        "discount": "残疾人免票，60岁以上半价，70岁以上免票",
        "contact": "0512-67510286"
    },
    "广州长隆": {
        "city": "广州",
        "level": "5A",
        "accessibility": {
            "wheelchair": {
                "accessible": True,
                "details": "长隆野生动物世界全程可轮椅通行，有专用观光小火车和缆车（可上轮椅）。长隆欢乐世界多数项目有轮椅通道。水上乐园有专用更衣室。",
                "rental": "各园区入口可租借轮椅（100元/天，押金500元）",
                "restrooms": "各园区均设有无障碍卫生间",
                "tips": "野生动物世界最适合轮椅游览，小火车+缆车几乎覆盖全园。建议买多园套票。"
            },
            "stroller": {
                "accessible": True,
                "details": "推婴儿车非常方便，各项目有停放区。野生动物世界小火车可推车上去。"
            },
            "elderly": {
                "accessible": True,
                "details": "野生动物世界最轻松（坐小火车/缆车），欢乐世界刺激项目老人不适合。大马戏有对号入座。"
            }
        },
        "discount": "持残疾证可购优惠票（需现场咨询），65岁以上有长者票",
        "contact": "400-883-0083"
    },
    "三亚亚龙湾": {
        "city": "三亚",
        "level": "4A",
        "accessibility": {
            "wheelchair": {
                "accessible": True,
                "details": "亚龙湾沙滩有木质栈道可轮椅通行到海边观景平台。亚龙湾热带天堂森林公园有观光车。各高星级酒店到沙滩均有无障碍通道。",
                "rental": "星级酒店多提供轮椅租借",
                "restrooms": "酒店和商业区有无障碍卫生间",
                "tips": "选择有沙滩无障碍通道的酒店最重要。瑞吉/万豪/丽思卡尔顿等品牌无障碍设施较完善。"
            },
            "stroller": {
                "accessible": True,
                "details": "木质栈道推婴儿车方便，但沙地区域推不动"
            },
            "elderly": {
                "accessible": True,
                "details": "海边度假对老年人友好，酒店内活动为主。注意防晒和补水。"
            }
        },
        "discount": "热带天堂森林公园65岁以上半价",
        "contact": "0898-88568899"
    },
    "拉萨布达拉宫": {
        "city": "拉萨",
        "level": "5A",
        "accessibility": {
            "wheelchair": {
                "accessible": False,
                "details": "布达拉宫需爬大量台阶（从山脚到宫殿约900级），无电梯和坡道，轮椅无法到达。广场和药王山观景台可远观。",
                "rental": "不提供轮椅租借",
                "restrooms": "广场有无障碍卫生间",
                "tips": "轮椅用户可在布达拉宫广场和药王山观景台拍摄外观。八廓街部分路段可通行。"
            },
            "elderly": {
                "accessible": False,
                "details": "高海拔+大量台阶，对老年人和心肺功能弱者挑战极大。建议在广场远观。如必须进入，量力而行缓慢攀登，备好氧气。"
            }
        },
        "discount": "残疾人免票，60岁以上半价",
        "contact": "0891-6823366"
    },
    "重庆洪崖洞": {
        "city": "重庆",
        "level": "4A",
        "accessibility": {
            "wheelchair": {
                "accessible": True,
                "details": "洪崖洞有电梯连接各层（1F-11F），每层观景平台可轮椅通行。从千厮门大桥观景台可远观全景。内部街道平坦。",
                "rental": "不提供轮椅租借",
                "restrooms": "各层商场区域有无障碍卫生间",
                "tips": "建议从1F（嘉陵江边）进入乘电梯到4F（城市阳台）观景，避开人流高峰（19:00-21:00）"
            },
            "stroller": {
                "accessible": True,
                "details": "电梯连接各层，推婴儿车可在各层观景平台活动"
            },
            "elderly": {
                "accessible": True,
                "details": "有电梯不需爬楼，但人多拥挤时注意安全。建议白天前往人少。"
            }
        },
        "discount": "免费开放",
        "contact": "023-63039888"
    },
    "武汉黄鹤楼": {
        "city": "武汉",
        "level": "5A",
        "accessibility": {
            "wheelchair": {
                "accessible": True,
                "details": "黄鹤楼主楼有电梯可到各层（需在入口处登记使用）。公园区域平坦可轮椅通行。户部巷小吃街部分可达。",
                "rental": "南门游客中心可租借轮椅",
                "restrooms": "景区入口和主楼一层有无障碍卫生间",
                "tips": "主楼电梯需提前告知工作人员。公园内步行道平坦宽阔。"
            },
            "stroller": {
                "accessible": True,
                "details": "公园区域推车方便，主楼有电梯可到各层观景"
            },
            "elderly": {
                "accessible": True,
                "details": "有电梯登楼，公园散步舒适。65岁以上免票。长江大桥观景台也可远观。"
            }
        },
        "discount": "残疾人免票，65岁以上免票",
        "contact": "027-88875073"
    },
    "云南丽江古城": {
        "city": "丽江",
        "level": "5A",
        "accessibility": {
            "wheelchair": {
                "accessible": False,
                "details": "古城全部为石板路，凹凸不平，且有多处台阶和坡道，轮椅通行极困难。仅古城口广场和主街前段勉强可通行。",
                "rental": "无轮椅租借",
                "restrooms": "古城内无障碍卫生间很少",
                "tips": "如需前往，建议住古城外酒店，白天只在主街短途活动。束河古镇相对平坦些。"
            },
            "stroller": {
                "accessible": False,
                "details": "石板路推婴儿车非常颠簸，体验差"
            },
            "elderly": {
                "accessible": True,
                "details": "体力好的老人可慢行，古城内客栈多有台阶注意安全。海拔2400米注意高反。"
            }
        },
        "discount": "古城维护费残疾人免，70岁以上免",
        "contact": "0888-5111068"
    },
    "黄山": {
        "city": "黄山",
        "level": "5A",
        "accessibility": {
            "wheelchair": {
                "accessible": False,
                "details": "黄山核心景区台阶极多且陡峭，索道站到观景点仍需大量步行。轮椅几乎无法游览核心景点。慈光阁索道下站区域平坦可远观。",
                "rental": "不提供轮椅租借",
                "restrooms": "索道站和山顶酒店有无障碍卫生间",
                "tips": "轮椅用户不建议前往黄山。如想体验，可坐云谷索道到白鹅岭站，在站区短暂观景后原路返回。"
            },
            "elderly": {
                "accessible": True,
                "details": "体力好的老人可借助索道+手杖完成核心路线。建议住山顶酒店分两天游览。65岁以上半价。"
            }
        },
        "discount": "残疾人免票，65岁以上半价，70岁以上免票",
        "contact": "0559-5580244"
    },
    "青岛栈桥/八大关": {
        "city": "青岛",
        "level": "4A",
        "accessibility": {
            "wheelchair": {
                "accessible": True,
                "details": "栈桥有坡道可轮椅通行到回澜阁。八大关区域道路平坦宽阔，花石楼等景点入口有台阶但可观外观。海滨木栈道全程平坦。",
                "rental": "栈桥附近酒店可租借轮椅",
                "restrooms": "栈桥入口和八大关休息区有无障碍卫生间",
                "tips": "海滨木栈道是最佳轮椅游览路线，从栈桥到奥帆中心约5公里平坦无阻。"
            },
            "stroller": {
                "accessible": True,
                "details": "海滨木栈道推婴儿车非常方便，八大关林荫道也适合推车"
            },
            "elderly": {
                "accessible": True,
                "details": "海滨木栈道平坦舒适，大量座椅可休息。夏季避暑胜地。"
            }
        },
        "discount": "栈桥和八大关免费开放",
        "contact": "0532-82885918"
    },
    "敦煌莫高窟": {
        "city": "敦煌",
        "level": "5A",
        "accessibility": {
            "wheelchair": {
                "accessible": True,
                "details": "莫高窟数字展示中心全程无障碍。实体洞窟区域有专用无障碍参观路线（约4-5个洞窟），需提前预约无障碍服务。入口有坡道。",
                "rental": "数字展示中心可租借轮椅",
                "restrooms": "展示中心和洞窟入口有无障碍卫生间",
                "tips": "必须提前在官网预约无障碍服务（至少3天），普通参观路线台阶较多不适用。"
            },
            "stroller": {
                "accessible": False,
                "details": "洞窟内空间狭小且光线暗，不建议推婴儿车。数字展示中心可以。"
            },
            "elderly": {
                "accessible": True,
                "details": "无障碍路线避开了台阶，60岁以上半价。夏季高温注意防晒补水。"
            }
        },
        "discount": "残疾人免票，60岁以上半价，70岁以上免票",
        "contact": "0937-8825000"
    },
    "哈尔滨冰雪大世界": {
        "city": "哈尔滨",
        "level": "4A",
        "accessibility": {
            "wheelchair": {
                "accessible": False,
                "details": "冰雪路面湿滑，轮椅无法安全通行。室内冰雕馆有坡道可短途观览。极地馆和室内景区可轮椅通行。",
                "rental": "不提供轮椅租借",
                "restrooms": "室内区域有无障碍卫生间",
                "tips": "冬季不建议轮椅用户前往户外冰雪景区。可选择室内项目（极地馆/科技馆）。"
            },
            "stroller": {
                "accessible": False,
                "details": "冰面推婴儿车不安全，建议用背带"
            },
            "elderly": {
                "accessible": True,
                "details": "室内项目适合老人观赏，户外冰面注意防滑。建议白天参观（气温较高）。"
            }
        },
        "discount": "残疾人凭残疾证优惠，65岁以上有长者票",
        "contact": "0451-84884366"
    }
}

# ========== 酒店无障碍数据库 ==========
HOTELS_DB = {
    "万豪": {
        "brand_en": "Marriott",
        "category": "豪华",
        "accessibility": {
            "accessible_room": True,
            "details": "万豪品牌旗下酒店均提供无障碍客房，配备宽门（≥80cm）、浴室扶手、低位洗手台、视觉门铃、紧急呼叫按钮。部分酒店提供淋浴椅和床边扶手。",
            "room_types": "无障碍大床房/无障碍双人房，部分酒店有无障碍套房",
            "booking": "官网和APP筛选'无障碍客房'，或致电酒店前台预约。建议至少提前3天确认房型。",
            "facilities": "无障碍停车位（近入口）、大堂低位前台、电梯语音播报、无障碍泳池通道（部分门店）"
        }
    },
    "万怡": {
        "brand_en": "Courtyard",
        "category": "中高端",
        "accessibility": {
            "accessible_room": True,
            "details": "万怡品牌统一标准提供无障碍客房，配备浴室扶手、宽门、低位设施。设施标准与万豪一致但房间面积略小。",
            "room_types": "无障碍大床房",
            "booking": "万豪APP筛选无障碍房型，或电话预约",
            "facilities": "无障碍停车位、大堂无障碍通道、电梯"
        }
    },
    "喜来登": {
        "brand_en": "Sheraton",
        "category": "豪华",
        "accessibility": {
            "accessible_room": True,
            "details": "喜来登品牌提供无障碍客房，标准与万豪集团统一。部分门店有更宽敞的无障碍套房。",
            "room_types": "无障碍大床房/无障碍套房（部分门店）",
            "booking": "万豪APP或致电酒店，建议提前确认具体设施配置",
            "facilities": "无障碍停车位、无障碍大堂、电梯、部分门店有泳池升降机"
        }
    },
    "威斯汀": {
        "brand_en": "Westin",
        "category": "豪华",
        "accessibility": {
            "accessible_room": True,
            "details": "威斯汀品牌提供无障碍客房，配备标准无障碍设施。部分门店提供特殊床垫和淋浴座椅。",
            "room_types": "无障碍大床房/无障碍双人房",
            "booking": "万豪APP筛选或致电确认",
            "facilities": "无障碍停车位、大堂通道、电梯、健身房无障碍入口（部分门店）"
        }
    },
    "丽思卡尔顿": {
        "brand_en": "Ritz-Carlton",
        "category": "奢华",
        "accessibility": {
            "accessible_room": True,
            "details": "丽思卡尔顿提供高标准无障碍客房，面积更宽敞，配备完整无障碍设施+管家服务协助特殊需求。",
            "room_types": "无障碍豪华大床房/无障碍套房",
            "booking": "建议致电酒店礼宾部提前沟通需求，可定制服务",
            "facilities": "全程无障碍通道、专用停车位、泳池升降机、SPA无障碍入口"
        }
    },
    "如家": {
        "brand_en": "Home Inn",
        "category": "经济",
        "accessibility": {
            "accessible_room": True,
            "details": "如家部分门店（2018年后开业）提供无障碍客房，老门店可能无专用无障碍房但有低楼层房间。配备基本扶手和宽门。",
            "room_types": "无障碍大床房（部分门店）",
            "booking": "建议电话确认门店是否有无障碍房型，APP上不总是标注",
            "facilities": "一楼房间、电梯（多层门店）、基本无障碍卫生间"
        }
    },
    "全季": {
        "brand_en": "JI Hotel",
        "category": "中端",
        "accessibility": {
            "accessible_room": True,
            "details": "全季酒店统一设计标准，较新门店均配备无障碍客房。中式简约风格，房间宽敞。配备扶手、宽门、淋浴椅。",
            "room_types": "无障碍大床房",
            "booking": "华住APP可筛选无障碍房型，或致电门店确认",
            "facilities": "无障碍停车位、电梯、一楼大堂无障碍通道"
        }
    },
    "亚朵": {
        "brand_en": "Atour",
        "category": "中端",
        "accessibility": {
            "accessible_room": True,
            "details": "亚朵较新门店提供无障碍客房，服务口碑好可提前沟通需求。配备基本无障碍设施。",
            "room_types": "无障碍大床房（部分门店）",
            "booking": "建议电话联系门店确认无障碍房是否可用",
            "facilities": "电梯、基本无障碍卫生间、可提供额外协助"
        }
    },
    "希尔顿": {
        "brand_en": "Hilton",
        "category": "豪华",
        "accessibility": {
            "accessible_room": True,
            "details": "希尔顿品牌全球统一无障碍标准，提供完整无障碍客房设施。中国区门店标准一致。",
            "room_types": "无障碍大床房/无障碍双人房",
            "booking": "希尔顿APP可筛选Accessible Room，建议提前3天确认",
            "facilities": "无障碍停车位、低位前台、电梯语音播报、泳池通道（部分门店）"
        }
    },
    "洲际": {
        "brand_en": "InterContinental",
        "category": "奢华",
        "accessibility": {
            "accessible_room": True,
            "details": "洲际品牌提供高标准无障碍客房，设施完善。部分门店提供额外服务如机场轮椅接送。",
            "room_types": "无障碍豪华房/无障碍套房",
            "booking": "IHG APP筛选或致电酒店礼宾部",
            "facilities": "全程无障碍通道、专用停车位、泳池升降机（部分门店）"
        }
    },
    "维也纳": {
        "brand_en": "Vienna Hotel",
        "category": "中端",
        "accessibility": {
            "accessible_room": True,
            "details": "维也纳较新门店配备无障碍客房。老门店需电话确认。基本无障碍设施齐全。",
            "room_types": "无障碍大床房（部分门店）",
            "booking": "建议电话确认门店无障碍房情况",
            "facilities": "电梯、一楼房间、基本扶手设施"
        }
    }
}

# ========== 出行建议数据库 ==========
TIPS_DB = {
    "wheelchair": {
        "name": "轮椅出行",
        "general": [
            "出行前务必电话确认目的地的无障碍设施现状，避免临时变动",
            "国内航班：轮椅可免费托运，电动轮椅需提前24小时通知航司，电池容量有要求（不超过300Wh）",
            "高铁：每列车有1个轮椅位（4号车厢），建议提前购票选座，车站可申请轮椅服务和绿色通道",
            "酒店预订时直接致电前台确认无障碍房型可用，APP标注可能不准确",
            "携带轮椅维修工具包（内六角、扳手、打气筒），长途旅行必备",
            "目的地城市优先选择有地铁的城市（多数有无障碍电梯），避免公交为主的城市"
        ],
        "plane": [
            "提前24小时联系航司申请轮椅服务（值机柜台到登机口/机舱口）",
            "手动轮椅可托运（免费），也可推到机舱口再托运",
            "电动轮椅：电池≤300Wh可托运，需提前申报，轮椅需用防撞包装",
            "选座优先选过道位（方便进出），部分航机有轮椅可到达的机舱洗手间",
            "到达后轮椅服务会送到行李转盘/出口处"
        ],
        "train": [
            "12306APP可购买轮椅票（显示'无障碍座位'），每列车1个",
            "大站均有轮椅服务和绿色通道，需提前电话预约（车站服务热线）",
            "高铁车厢连接处宽80cm，标准轮椅（宽60-65cm）可通行",
            "车站无障碍电梯通常在站台两端，按指示标识行走"
        ],
        "self_drive": [
            "确认租用车辆有足够后备箱空间放置轮椅",
            "高速服务区多数有无障碍卫生间，但部分老服务区可能没有",
            "景区停车位：残疾证可使用无障碍停车位（通常在入口附近）"
        ],
        "equipment": "必备：轮椅维修工具、防雨罩、坐垫减压垫。建议：便携坡板（6kg铝合金款）"
    },
    "visual": {
        "name": "视障出行",
        "general": [
            "携带导盲犬出行：国内航班允许导盲犬登机（需提前48小时申请+疫苗证明），高铁同样允许",
            "景区语音导览是核心需求，出行前确认目的地是否有语音导览服务",
            "智能手机开启无障碍模式（读屏功能），提前下载离线地图和公交信息",
            "建议结伴出行，至少有一名视力正常者陪同",
            "部分城市（北京/上海/广州）地铁有无障碍引导服务，可提前预约"
        ],
        "plane": [
            "航司提供登机引导服务（值机到登机口到座位），提前申请",
            "导盲犬可随主人登机（免费），需疫苗证明+导盲犬工作证",
            "选靠窗位避免过道打扰，空乘会协助餐食"
        ],
        "train": [
            "12306可预约重点旅客服务（到站接+出站送）",
            "导盲犬可上高铁（需工作证+疫苗证明），建议选末端座位减少干扰"
        ],
        "equipment": "必备：导盲犬装备/盲杖、读屏手机。建议：骨传导耳机（听导航+环境声）"
    },
    "hearing": {
        "name": "听障出行",
        "general": [
            "航班信息关注机场大屏和APP推送，避免依赖广播",
            "酒店预订时备注听障需求，要求视觉门铃和震动闹钟",
            "高铁到站前看显示屏报站，避免坐过站",
            "景区手语服务需提前预约（多数景区需3天以上）",
            "手机开启震动提醒模式，安装实时字幕APP（如讯飞听见）"
        ],
        "plane": [
            "值机时告知听障情况，空乘会用文字卡沟通安全须知",
            "部分航机安全须知视频有字幕版",
            "登机口注意看显示屏，避免错过登机通知"
        ],
        "equipment": "必备：震动闹钟/手表。建议：实时字幕APP、助听器备用电池"
    },
    "stroller": {
        "name": "婴儿车出行",
        "general": [
            "伞车（轻便型）比大型婴儿车更适合旅行，可折叠登机",
            "飞机：伞车可推到登机口再托运（免费），到达后在行李转盘取",
            "高铁：车厢连接处可放婴儿车，但空间有限建议折叠",
            "景区石板路/石子路推车颠簸，考虑用背带替代",
            "选择有电梯的酒店（老式民宿可能无电梯）"
        ],
        "plane": [
            "婴儿车可免费托运（算额外行李），也可推到登机口托运",
            "2岁以下婴儿无座位（成人抱），可申请婴儿摇篮（靠窗位+隔板，需提前预约）",
            "带好婴儿耳塞或喂奶/安抚奶嘴，起降时缓解耳压"
        ],
        "equipment": "必备：轻便伞车（可单手折叠）、背带。建议：防晒罩、雨罩"
    },
    "elderly": {
        "name": "老年出行",
        "general": [
            "出行前体检，确认心肺功能适合目的地海拔和活动强度",
            "随身携带常用药+急救药（速效救心丸/降压药），分开存放",
            "选择节奏慢的行程，每天景点不超过2个，预留充足休息时间",
            "优先选择有电梯的酒店，避免爬楼",
            "购买旅游意外险，确认覆盖高龄人群（部分保险80岁以上不承保）",
            "国内多数5A景区对60-69岁半价、70岁以上免票，带好身份证"
        ],
        "plane": [
            "长途飞行建议每2小时起身活动，预防深静脉血栓",
            "选靠过道座位方便活动，压缩袜有助于血液循环",
            "提前申请机场轮椅服务（免费），即使能走也可以减少体力消耗"
        ],
        "train": [
            "高铁比飞机更适合中短途（1-6小时），活动空间大、无气压变化",
            "买下铺（卧铺）或过道座位，方便活动和如厕"
        ],
        "equipment": "必备：常用药（分两份存放）、身份证。建议：折叠手杖椅（可坐可走）、保温杯"
    }
}


def _make_request(url, data=None):
    """Make HTTPS request with proper SSL verification."""
    ctx = ssl.create_default_context()
    headers = {"Content-Type": "application/json"}
    if PROXY_TOKEN:
        headers["Authorization"] = f"Bearer {PROXY_TOKEN}"

    if data:
        req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
    else:
        req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}


def spot_accessibility(spot_name: str, need_type: str = "wheelchair") -> str:
    """查询景点无障碍设施信息"""
    # Search in local DB
    result = None
    search_key = spot_name.strip()
    for key, val in SPOTS_DB.items():
        if search_key in key or key in search_key:
            result = val
            break

    if not result:
        # Try city match
        for key, val in SPOTS_DB.items():
            if result:
                break
            city = val.get("city", "")
            if search_key in city:
                # Return all spots in that city
                spots_in_city = [k for k, v in SPOTS_DB.items() if v.get("city") == city]
                return json.dumps({
                    "found": False,
                    "message": f"未找到'{search_key}'的具体信息，但{city}有以下收录景点：{', '.join(spots_in_city)}。请尝试输入完整景点名称查询。"
                }, ensure_ascii=False)

    if not result:
        available = list(SPOTS_DB.keys())
        return json.dumps({
            "found": False,
            "message": f"暂未收录'{search_key}'的无障碍信息。目前收录{len(available)}个热门景区，包括：{', '.join(available[:10])}等。将持续更新更多景区。"
        }, ensure_ascii=False)

    need_type = need_type.lower().strip()
    type_map = {
        "wheelchair": "wheelchair", "轮椅": "wheelchair",
        "visual": "visual", "视障": "visual", "盲": "visual",
        "hearing": "hearing", "听障": "hearing", "聋": "hearing",
        "stroller": "stroller", "婴儿车": "stroller", "推车": "stroller",
        "elderly": "elderly", "老年": "elderly", "老人": "elderly",
    }
    mapped_type = type_map.get(need_type, "wheelchair")

    acc = result.get("accessibility", {})
    type_info = acc.get(mapped_type, {})

    output = {
        "found": True,
        "spot": spot_name,
        "city": result.get("city", ""),
        "level": result.get("level", ""),
        "need_type": mapped_type,
        "accessible": type_info.get("accessible", False),
        "details": type_info.get("details", "暂无详细信息"),
        "discount": result.get("discount", ""),
        "contact": result.get("contact", ""),
    }

    # Add type-specific fields
    for field in ["routes", "rental", "restrooms", "tips", "services"]:
        if field in type_info:
            output[field] = type_info[field]

    return json.dumps(output, ensure_ascii=False)


def hotel_accessibility(hotel_brand: str, city: str = "") -> str:
    """查询酒店无障碍设施信息"""
    search_key = hotel_brand.strip()
    result = None
    for key, val in HOTELS_DB.items():
        if search_key in key or key in search_key:
            result = val
            break
        # Also match English brand name
        brand_en = val.get("brand_en", "").lower()
        if search_key.lower() in brand_en or brand_en in search_key.lower():
            result = val
            break

    if not result:
        available = list(HOTELS_DB.keys())
        return json.dumps({
            "found": False,
            "message": f"暂未收录'{search_key}'的无障碍信息。目前收录{len(available)}个酒店品牌：{', '.join(available)}。"
        }, ensure_ascii=False)

    output = {
        "found": True,
        "brand": hotel_brand,
        "brand_en": result.get("brand_en", ""),
        "category": result.get("category", ""),
        "accessible_room": result.get("accessibility", {}).get("accessible_room", False),
        "details": result.get("accessibility", {}).get("details", ""),
        "room_types": result.get("accessibility", {}).get("room_types", ""),
        "booking": result.get("accessibility", {}).get("booking", ""),
        "facilities": result.get("accessibility", {}).get("facilities", ""),
    }

    if city:
        output["city_note"] = f"{city}地区建议致电具体门店确认无障碍房型可用性"

    return json.dumps(output, ensure_ascii=False)


def travel_tips(destination: str, accessibility_need: str, travel_mode: str = "") -> str:
    """根据出行类型和目的地提供无障碍旅行实用建议"""
    need_map = {
        "wheelchair": "wheelchair", "轮椅": "wheelchair",
        "visual": "visual", "视障": "visual",
        "hearing": "hearing", "听障": "hearing",
        "stroller": "stroller", "婴儿车": "stroller", "推车": "stroller",
        "elderly": "elderly", "老年": "elderly", "老人": "elderly",
    }
    mapped_need = need_map.get(accessibility_need.lower().strip(), "wheelchair")

    mode_map = {
        "plane": "plane", "飞机": "plane", "飞行": "plane",
        "train": "train", "火车": "train", "高铁": "train",
        "self_drive": "self_drive", "自驾": "self_drive", "开车": "self_drive",
    }

    tips_data = TIPS_DB.get(mapped_need, {})
    tips_name = tips_data.get("name", accessibility_need)

    # Collect tips
    general_tips = tips_data.get("general", [])
    specific_tips = []

    if travel_mode:
        mapped_mode = mode_map.get(travel_mode.lower().strip(), "")
        if mapped_mode and mapped_mode in tips_data:
            specific_tips = tips_data[mapped_mode]
    else:
        # Return all transport tips
        for mode in ["plane", "train", "self_drive"]:
            if mode in tips_data:
                specific_tips.extend(tips_data[mode])

    # Find matching spot info
    spot_info = None
    for key, val in SPOTS_DB.items():
        if destination in key or key in destination or destination in val.get("city", ""):
            spot_info = val
            break

    output = {
        "destination": destination,
        "need_type": tips_name,
        "general_tips": general_tips,
        "transport_tips": specific_tips if specific_tips else "请指定出行方式（飞机/火车/自驾）获取更具体建议",
        "equipment": tips_data.get("equipment", ""),
    }

    if spot_info:
        need_key = mapped_need
        acc = spot_info.get("accessibility", {}).get(need_key, {})
        output["spot_note"] = {
            "accessible": acc.get("accessible", None),
            "details": acc.get("details", ""),
            "discount": spot_info.get("discount", ""),
        }

    return json.dumps(output, ensure_ascii=False)


# ========== Tool Registry ==========
TOOLS = {
    "spot_accessibility": {
        "fn": spot_accessibility,
        "desc": "查询景点的无障碍设施信息"
    },
    "hotel_accessibility": {
        "fn": hotel_accessibility,
        "desc": "查询酒店品牌的无障碍房型和设施信息"
    },
    "travel_tips": {
        "fn": travel_tips,
        "desc": "根据出行类型和目的地提供无障碍旅行实用建议"
    }
}


def run(tool_name: str, **kwargs):
    """Execute a tool by name."""
    tool = TOOLS.get(tool_name)
    if not tool:
        return json.dumps({"error": f"Unknown tool: {tool_name}"}, ensure_ascii=False)
    try:
        result = tool["fn"](**kwargs)
        return result
    except TypeError as e:
        return json.dumps({"error": f"参数错误: {str(e)}"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"执行错误: {str(e)}"}, ensure_ascii=False)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <tool_name> [args...]")
        sys.exit(1)

    tool = sys.argv[1]
    args = {}
    i = 2
    while i < len(sys.argv) - 1:
        key = sys.argv[i].lstrip("-")
        args[key] = sys.argv[i + 1]
        i += 2

    print(run(tool, **args))
