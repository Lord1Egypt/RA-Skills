import os
import re
from typing import Dict, List, Any, Optional
# import logging
# from logging.handlers import TimedRotatingFileHandler
import pandas as pd
import datetime
import json
import requests


GTS_AUTHORIZATION_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".authorization")
GTS_ACCESS_KEY = os.getenv("GTS_ACCESS_KEY", None)
GTS_SECRET_KEY = os.getenv("GTS_SECRET_KEY", None)

# 通过 ak/sk 获取 临时 authorization
AUTHORIZATION_URL = f"https://open.gangtise.com/application/auth/oauth/open/loginV2"

def get_authorization(ak: str, sk: str):
    payload = {
        "accessKey": ak,
        "secretAccessKey": sk
    }
    response = requests.post(AUTHORIZATION_URL, json=payload)
    if response.status_code != 200:
        return None
    try:
        return response.json()["data"]["accessToken"]
    except Exception as e:
        return None

GTS_AUTHORIZATION = None
if GTS_ACCESS_KEY and GTS_SECRET_KEY:
    GTS_AUTHORIZATION = get_authorization(GTS_ACCESS_KEY, GTS_SECRET_KEY)
elif os.path.exists(GTS_AUTHORIZATION_PATH):
    with open(GTS_AUTHORIZATION_PATH, "r", encoding="utf-8") as f:
        content = json.load(f)
        if content.get("accessKey", None) and content.get("secretAccessKey", None):
            GTS_AUTHORIZATION = get_authorization(content["accessKey"], content["secretAccessKey"])
        else:
            GTS_AUTHORIZATION = None

GTS_SAVE_FILE = os.getenv("GTS_SAVE_FILE", False)
GTS_SAVE_EXTENSION = os.getenv("GTS_SAVE_EXTENSION", "md")

GANGTISE_DATA_DOMAIN = "https://open.gangtise.com/application/open-ai/agent"
# 与 /agent/* 并列的 open-ai 能力（如热点话题列表），默认不含末尾 /agent
GANGTISE_OPENAI_ROOT = "https://open.gangtise.com/application/open-ai"

def _find_openclaw_root():
    """向上遍历目录直到找到 .openclaw，返回其上级目录作为执行目录"""
    path = os.path.abspath(os.path.dirname(__file__))
    openclaw_dir_got = False
    while path != os.path.dirname(path):
        dir_name = os.path.basename(path)
        if dir_name in (".openclaw"):
            openclaw_dir_got = True
            return os.path.abspath(path)
        path = os.path.dirname(path)
    path = os.path.abspath(os.path.dirname(__file__))
    if not openclaw_dir_got:
        openclaw_dir_got = False
        while path != os.path.dirname(path):
            dir_name = os.path.basename(path)
            if dir_name in (".agent"):
                openclaw_dir_got = True
                return os.path.abspath(path)
            path = os.path.dirname(path)
    path = os.path.abspath(os.path.dirname(__file__))
    if not openclaw_dir_got:
        openclaw_dir_got = False
        while path != os.path.dirname(path):
            dir_name = os.path.basename(path)
            if dir_name in ("workspace"):
                openclaw_dir_got = True
                return os.path.abspath(path)
            path = os.path.dirname(path)
    path = os.path.abspath(os.path.dirname(__file__))
    if not openclaw_dir_got:
        openclaw_dir_got = False
        while path != os.path.dirname(path):
            dir_name = os.path.basename(path)
            if dir_name in ("skills"):
                openclaw_dir_got = True
                return os.path.abspath(os.path.dirname(path))
            path = os.path.dirname(path)
    return os.path.abspath(os.getcwd())

openclaw_root = _find_openclaw_root()
if openclaw_root.endswith("workspace"):
    gangtise_workspace_path = os.path.join(openclaw_root, "gangtise")
else:
    gangtise_workspace_path = os.path.join(openclaw_root, "workspace", "gangtise")
if not os.path.exists(gangtise_workspace_path):
    os.makedirs(gangtise_workspace_path, exist_ok=True)

usage_dir = os.path.join(gangtise_workspace_path, ".usage")
if not os.path.exists(usage_dir):
    os.makedirs(usage_dir, exist_ok=True)

file_dir = os.path.join(gangtise_workspace_path, "files")
if not os.path.exists(file_dir):
    os.makedirs(file_dir, exist_ok=True)

def data_to_md(data: pd.DataFrame, range: List[int]=None, max_cell_length: int=None):
    data_copy = data.copy()
    if "metadata" in data_copy.columns:
        data_copy = data_copy.drop(columns=["metadata"])
    content = "| " + " | ".join(data_copy.columns) + " |\n"
    content += "| " + " | ".join(["-" for _ in data_copy.columns]) + " |\n"
    omitted = False
    for i, row in enumerate(data_copy.to_dict(orient="records")):
        if range:
            if i in range:
                if max_cell_length:
                    content += "| " + " | ".join([re.sub(r"\s+", " ", str(row[key]).replace("\n"," ")).replace("|", "")[:max_cell_length]+"..." if len(re.sub(r"\s+", " ", str(row[key])).replace("|", "")) > max_cell_length else re.sub(r"\s+", " ", str(row[key])).replace("|", "") for key in row.keys()]) + " |\n"
                else:
                    content += "| " + " | ".join([re.sub(r"\s+", " ", str(row[key]).replace("\n"," ")).replace("|", "") for key in row.keys()]) + " |\n"
            elif not omitted:
                content += "| ... |\n"
                omitted = True
        else:
            if max_cell_length:
                content += "| " + " | ".join([re.sub(r"\s+", " ", str(row[key]).replace("\n"," ")).replace("|", "")[:max_cell_length]+"..." if len(re.sub(r"\s+", " ", str(row[key])).replace("|", "")) > max_cell_length else re.sub(r"\s+", " ", str(row[key])).replace("|", "") for key in row.keys()]) + " |\n"
            else:
                content += "| " + " | ".join([re.sub(r"\s+", " ", str(row[key]).replace("\n"," ")).replace("|", "") for key in row.keys()]) + " |\n"
    content = content[:-1]
    return content.strip()

def add_usages(usages_list: List[Dict[str, Any]]):
    usages = {}
    for usages_item in usages_list:
        if len(usages_item) == 0:
            continue
        for k,v in usages_item.items():
            if k not in usages:
                usages[k] = v
            else:
                usages[k] = usages[k] + v
    return usages
    
_THEME_ID_NAME_ROWS = """
121000002 核电
121000003 风电
121000004 氢能源
121000006 高温合金
121000008 折叠屏
121000009 储能
121000016 配网
121000019 固态电池
121000021 锂电池
121000026 HJT
121000030 钙钛矿
121000031 镍
121000032 锂
121000038 特斯拉电动车
121000039 华为智选车
121000041 充换电
121000044 整车
121000052 黄金
121000055 半导体设备
121000059 电子特气
121000060 光刻胶
121000061 功率半导体
121000062 先进封装
121000183 光模块
121000063 疫苗
121000064 mRNA疫苗
121000072 造船
121000073 物流快递
121000076 氟化工
121000077 钾肥
121000087 游戏
121000093 信创
121000094 网络安全
121000096 数据中心
121000101 AI应用
121000102 虚拟数字人
121000103 数据要素
121000110 数据加密
121000113 智慧矿山
121000116 动力电池回收
121000126 教育
121000129 工业母机
121000130 机器人
121000131 商业航天
121000133 CCER
121000136 宠物
121000137 电子烟
121000139 预制菜
121000141 大飞机
121000142 两机
121000143 军工
121000158 华为圈
121000163 医疗新基建
121000164 医美
121000167 中药
121000171 CXO
121000179 数字货币
121000185 3D打印
120101004 中概股
121000196 脑机接口
121000197 减肥药
121000198 绿电运营
121000200 核污染
121000205 光刻机
121000207 5.5G
121000210 转基因
121000214 自动驾驶
121000215 华为昇腾
121000217 创新药
121000222 阿尔兹海默
121000224 小米汽车
121000225 流感
121000227 MR
121000230 养老
121000236 化妆品
121000240 低空经济
121000242 合成生物学
121000253 AI PC
121000261 墨脱水电站
121000264 铜连接
121000262 磷化工
121000267 锂电设备
121000288 鸿蒙系统
121000284 AI手机
121000285 跨境电商
121000313 EDA
121000324 光伏
121000318 轮胎
121000332 存储
121000336 AI算力
121000337 维生素
121000297 液冷
121000342 白酒
121000345 新零售
121000346 生物质能源
121000348 激光雷达
121000349 旅游
121000356 生猪养殖
121000359 铜
121000362 HBM
121000365 果链
121000418 氨纶
121000420 涤纶
121000421 钛白粉
121000416 锦纶
121000422 证券
121000378 城中村
121000382 国货品牌
121000415 深海经济
121000375 汽车零配件
121000381 理想汽车
121000372 黑科技
121000369 铝
121000374 中国优势
121000367 设备更新
121000379 骨科
121000398 饮料
121000391 医疗服务
121000370 小金属
121000423 餐饮连锁
121000424 乳业
121000384 煤炭
121000385 石油
121000407 燃气
121000392 火电
121000412 物业管理
121000405 建材
121000376 房地产
121000394 肝病
121000386 工业大麻
121000371 国产替代
121000387 AI眼镜
121000389 消费降级
121000395 户外体育
121000425 化工白马
121000410 新疆
121000404 高股息
121000414 核心资产
121000400 粮食安全
121000409 人民币国际化
121000403 微盘股精选
121000419 服装家纺
121000426 芳纶
121000427 粘胶
121000366 家电
121000373 家居
121000388 科学仪器仪表
121000380 农机
121000393 生命科学上游
121000469 珠宝
121000470 美国大选
121000471 新疆煤化工
121000472 谷子经济
121000473 字节算力
121000474 微信小店
121000475 铁路改革
121000476 零食
121000477 首发经济
121000478 小红书
121000479 冰雪经济
121000481 算力租赁
121000480 云计算
121000487 AI玩具
121000489 乌克兰重建
121000491 阿里算力
121000490 腾讯算力
121000492 生育
121000493 核聚变
121000494 量子科技
121000496 新材料
121000495 碳纤维
121000498 消费品出海
121000497 免税
121000499 会展经济
121000500 烯草酮
121000502 保健品
121000504 新消费
121000503 低度酒
121000505 硝化棉
121000506 共价有机框架材料(COFs)
121000507 草甘膦
121000508 氮肥
121000509 氯虫苯甲酰胺
121000511 稳定币
121000510 外骨骼机器人
121000512 区块链
121000513 PEEK材料
121000514 军贸
121000515 活性染料
121000516 短剧
121000517 维生素D3
121000518 稀土永磁材料
121000519 溴素
121000520 模拟芯片
121000521 无人机
121000525 疫情医疗
121000522 MiniLED
121000526 NFT
121000527 VR/AR应用
121000523 元宇宙
121000524 3D视觉
121000535 正极材料
121000532 电磁&电子对抗
121000533 辅助生殖
121000537 猴痘
121000531 反制裁
121000538 口腔
121000534 负极材料
121000530 灾害防治
121000539 婴童
121000529 BC电池
121000542 ASIC
121000545 体温检测
121000541 干细胞
121000546 医用氧
121000544 PLA
121000547 基因测序
121000540 超导
121000550 玻璃
121000553 制冷剂
121000558 芬太尼
121000548 化肥
121000560 肝素
121000561 医废处理
121000557 蚂蚁金服
121000555 机器视觉
121000563 硅料
121000552 土地流转
121000556 上海自贸区
121000562 草铵膦
121000559 乙醇燃料
121000554 农药
121000551 PTA
121000549 玻璃基板
121000565 车路云
121000564 4680电池
121000566 种植业
121000568 超级电容器
121000569 蛋氨酸
121000571 分散染料
121000570 棉花
121000567 油气改革
121000575 锌
121000583 白糖
121000584 DeepSeek
121000582 螺纹钢
121000585 星闪
121000574 可燃冰
121000576 全息投影
121000577 钴
121000572 纯碱
121000580 赛马
121000573 博彩
121000581 鸡肉
121000578 种业
121000599 动漫
121000604 印染
121000587 白银
121000596 智慧政务
121000601 卡牌
121000586 超硬材料
121000603 醋酸
121000588 钼
121000594 露营经济
121000589 电商
121000590 智能家居
121000592 C2M
121000593 MCN
121000605 乙二醇
121000602 数据确权
121000600 生鲜电商
121000597 造纸
121000598 机场航空
121000591 玻纤
121000619 固收
121000620 kimi
121000608 调味品
121000617 智能手表
121000612 保险
121000607 甜味剂
121000614 影视院线
121000616 兽药
121000622 房屋检测
121000611 银行
121000606 铁路基建
121000613 地摊经济
121000609 啤酒
121000615 水产品
121000618 烟草
121000621 跨境支付CIPS
121000610 垃圾发电
121000624 CPO
121000623 高速公路
121000625 海工装备
121000629 有机硅
121000630 磷肥
121000633 无人物流车
121000628 分拆上市
121000638 海南自贸
121000627 知识产权
121000641 重卡
121000637 消防器材
121000626 颗粒硅
121000634 西部大开发
121000636 水利建设
121000640 汽车后市场
121000643 POE胶膜
121000635 新三板精选层
121000632 毫米波雷达
121000642 AI基础设施
121000631 复合肥
121000639 冷链物流
121000644 电子雷管
121000650 低市净率
121000654 海绵城市
121000655 水务
121000647 乡村振兴
121000656 reits
121000645 向量数据库
121000651 中俄贸易
121000646 上海本地股
121000652 股权转让
121000653 并购重组预案
121000649 复合铜箔
121000648 军工信息化
121000657 大股东定增
121000658 回购
121000659 消费升级
121000661 成飞
121000660 工程机械
121000662 PCB
121000664 充电桩
121000663 燃料电池
121000667 高压快充
121000665 钠离子电池
121000666 储能热管理
121000668 铜箔
121000669 新型电力系统
121000671 面板
121000670 眼科
121000672 人力资源
121000673 变压器
121000674 虚拟电厂
121000675 TDI
121000676 民爆
121000677 SOC
121000678 柴油发电机
121000679 PVC
121000680 先进制程
121000681 交换机
121000682 乙烯
121000683 反内卷
121000684 服务器电源
121000685 含能材料
121000686 基孔肯雅热
121000687 eSIM
121000688 新藏铁路
121000690 光学元件
121000689 光热发电
121000691 固废处理
121000692 化学工程
121000693 磷化铟
121000697 军工AI
121000696 水下军工
121000695 半导体材料
121000694 摩托车
121000698 军用机器人
121000699 GPU
121000700 聚醚多元醇
121000701 血制品
121000703 薄膜铌酸锂
121000702 物联网
121000704 尼龙
121000705 碳化硅
121000707 钠电池
121000706 水泥
121000708 工业硅
121000711 镁铝合金
121000710 绿色甲醇
121000709 杀菌剂
121000712 HVDC
121000713 MEMS
121000714 深地经济
121000715 自主可控
121000716 十五五规划
121000717 海峡两岸
121000718 芳香胺
121000719 SOFC
121000720 AI能源
121000721 燃气轮机
121000722 太空算力
121000723 反制日本
121000724 算力元器件
121000725 电子布
121000726 谷歌AI
121000727 氮化镓
121000728 互联网金融
121000729 洁净室
121000730 小核酸药物
121000731 太空光伏
121000732 电感
121000733 OpenClaw
121000734 算电协同
"""

THEME_NAME_TO_ID = {}
for line in _THEME_ID_NAME_ROWS.strip().splitlines():
    theme_id, theme_name = line.strip().split(maxsplit=1)
    THEME_NAME_TO_ID[theme_name] = theme_id

def format_response(response: dict, method_name: str, output: Optional[str] = None, additional_message: str = ""):
    # 保存 usage
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    now = datetime.datetime.now().strftime("%H%M%S")
    usage_path = os.path.join(usage_dir, f"{today}.json")
    if response.get("usage", None):
        if os.path.exists(usage_path):
            with open(usage_path, "r", encoding="utf-8") as f:
                usage = json.load(f)
            if now in usage:
                now_usage = add_usages([response["usage"], usage[now]])
            else:
                now_usage = response["usage"]
            usage.update({now: now_usage})
        else:
            usage = {now: response["usage"]}
        with open(usage_path, "w", encoding="utf-8") as f:
            json.dump(usage, f, ensure_ascii=False)

    method_name_map = {
        "one_pager": "公司一页通",
        "investment_logic": "投资逻辑",
        "peer_comparison": "公司同业对比",
        "earnings_review_getid": "绩点评ID",
        "earnings_review_getcontent": "绩点评内容",
        "theme_tracking": "主题跟踪",
        "research_outline": "公司调研提纲",
        "hot_topic_list": "热点话题报告",
        "security_clue_list": "投研线索列表",
        "agent": "Agent",
    }
    display_name = method_name_map.get(method_name, method_name)

    if response.get("state") != "success":
        return_message = "调用gangtise服务端失败，错误信息：" + response.get("message", "")
        if additional_message:
            return_message += "\n" + additional_message
        return return_message

    sections: List[str] = []
    for item in response.get("data", []):
        data_list = item.get("data", [])
        module_name = item.get("module", "agent")
        type_name = item.get("type", "result")

        if GTS_SAVE_FILE:
            if output:
                process_path = output
                if os.path.exists(process_path):
                    return "错误信息：文件已存在"
            else:
                extension = GTS_SAVE_EXTENSION
                process_dir = os.path.join(gangtise_workspace_path, method_name)
                if not os.path.exists(process_dir):
                    os.makedirs(process_dir, exist_ok=True)
                file_index = 1
                process_path = os.path.join(process_dir, f"{module_name}_{file_index}.{extension}")
                max_retries = 20
                while os.path.exists(process_path) and max_retries > 0:
                    file_index += 1
                    process_path = os.path.join(process_dir, f"{module_name}_{file_index}.{extension}")
                    max_retries -= 1
                if max_retries == 0:
                    return "错误信息：文件存储系统繁忙，请稍后再试"

            if GTS_SAVE_EXTENSION == "json":
                with open(process_path, "w", encoding="utf-8") as f:
                    json.dump(data_list, f, ensure_ascii=False, indent=2)
            else:
                with open(process_path, "w", encoding="utf-8") as f:
                    for i, row in enumerate(data_list):
                        f.write(f"### 查询结果 {i + 1}\n")
                        if row.get("date"):
                            f.write(f"日期：{row['date']}\n")
                        if row.get("type"):
                            f.write(f"类型：{row['type']}\n")
                        if row.get("dataId"):
                            f.write(f"dataId：{row['dataId']}\n")
                        if row.get("content"):
                            content = row["content"].strip()
                            f.write(f"内容：\"\"\"\n{content}\n\"\"\"\n")
                        elif row.get("markdown"):
                            f.write(row["markdown"].strip() + "\n")
                        if i < len(data_list) - 1:
                            f.write("\n---\n\n")

            sections.append(
                f"### {display_name} 查询结果（{module_name}/{type_name}）\n\n"
                + _render_agent_items(data_list, type_name=type_name)
                + f"\n所有查询结果已保存到{GTS_SAVE_EXTENSION}：\"{os.path.abspath(process_path)}\""
            )
        else:
            sections.append(
                f"### {display_name} 查询结果（{module_name}/{type_name}）\n\n"
                + _render_agent_items(data_list, type_name=type_name)
            )

    return_message = response.get("message", "")
    if sections:
        return_message += "\n\n" + "\n\n".join(sections)
    if additional_message:
        return_message += "\n" + additional_message
    return return_message.strip()


def _render_agent_items(data_list: List[Dict[str, Any]], type_name: str = "") -> str:
    if not data_list:
        return "无可展示数据。"
    parts: List[str] = []
    for row in data_list:
        if type_name in ("hot-topic-list", "security-clue-list") and row.get("markdown"):
            parts.append(str(row["markdown"]).strip())
            parts.append("---")
            continue
        if row.get("date"):
            parts.append(f"日期：{row['date']}")
        if row.get("type"):
            parts.append(f"类型：{row['type']}")
        if row.get("dataId"):
            parts.append(f"dataId：{row['dataId']}")
        if row.get("content"):
            content = row["content"].strip()
            parts.append(f"内容：\"\"\"\n{content}\n\"\"\"")
        parts.append("---")
    return "\n".join(parts[:-1] if parts and parts[-1] == "---" else parts)

def load_securities_from_file(path: str) -> List[str]:
    full_path = path
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"证券文件不存在: {path}")
    df = pd.read_csv(full_path)
    if "security_abbr" in df.columns:
        return [str(x) for x in df["security_abbr"].dropna().tolist()]
    if "security_code" in df.columns:
        return [str(x) for x in df["security_code"].dropna().tolist()]
    raise ValueError("证券文件必须包含 security_code 或 security_abbr 列")

OPENAPI_SKILL_VERSION = "1.4.4"
SKILL_CHECK_URL = "https://open.gangtise.com/application/skills-backend/version?skill=openapi"

def check_version(large_version: bool = True):
    response = requests.get(SKILL_CHECK_URL)
    if response.status_code == 200 and large_version:
        return response.json()["state"] == "success" and response.json()["version"].split(".")[0] == OPENAPI_SKILL_VERSION.split(".")[0] and response.json()["version"].split(".")[1] == OPENAPI_SKILL_VERSION.split(".")[1]
    elif response.status_code == 200 and not large_version:
        return response.json()["state"] == "success" and response.json()["version"] == OPENAPI_SKILL_VERSION
    else:
        return False

if __name__ == "__main__":
    print("检查 gangtise-kb 相关配置")
    if not os.path.exists(GTS_AUTHORIZATION_PATH):
        print("  无法检测到gangtise授权文件, gangtise-kb 无法正常工作")
    elif GTS_AUTHORIZATION is None:
        print("  授权文件存在, 但无法获取gangtise授权, gangtise-kb 无法正常工作")
    else:
        print("  检测到gangtise授权文件, gangtise-kb 可以正常工作")
    if GTS_SAVE_FILE is None:
        print("  环境变量 GTS_SAVE_FILE 未配置, 默认值为 False, gangtise服务端 将不保存查询结果到文件中")
    elif GTS_SAVE_FILE == "True":
        print("  环境变量 GTS_SAVE_FILE 为 True, gangtise服务端 将保存查询结果到文件中")
    else:
        print("  环境变量 GTS_SAVE_FILE 为 False, gangtise服务端 将不保存查询结果到文件中")
    if check_version(large_version=False):
        print("  gangtise-kb 版本为最新")
    else:
        print("  gangtise-kb 版本不是最新, 建议进行更新")
    print(f"  gangtise-kb 工作文件目录: {gangtise_workspace_path}")