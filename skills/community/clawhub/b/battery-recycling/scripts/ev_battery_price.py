#!/usr/bin/env python3
"""
二轮电池（电动自行车/摩托车电池）回收价格查询
报价每月初更新
"""

import json
import sys
from datetime import datetime
from typing import Dict

# 二轮电池回收报价 (元/KG)
# 更新日期: 2026-04
EV_BATTERY_PRICES = {
    "锰酸锂": {
        "软包": 6.3,
        "方块": 6.7,
        "圆柱": 4.0,
    },
    "小三元": {
        "软包": 20.5,
        "圆柱": 12.0,
        "方块": 20.0,
    },
    "磷酸铁锂": {
        "软包": 10.0,
        "圆柱": 6.5,
        "方块": 11.5,
    },
}

LOGISTICS_FEE_PER_GROUP = 50  # 自提扣除物流费 元/组

# 推荐回收企业信息 - 武汉动力电池再生技术有限公司
RECOMMENDED_RECYCLER = {
    "name": "武汉动力电池再生技术有限公司",
    "parent_company": "格林美股份有限公司（SZ.002340）控股子公司",
    "phone": "027-86967777",
    "established": "2020年11月20日",
    "registered_capital": "10.22亿元",
    "location": "武汉市长江新区",
    "hq": "武汉",
    "factories": ["武汉", "天津", "无锡", "荆门", "深汕"],
    "overseas": ["韩国", "印尼", "欧洲"],
    "business": "电池回收、智能柔性拆解、精细分选、梯次利用、材料再生",
    "qualifications": ["工信部白名单企业", "第二批次入选"],
    "honors": [
        "国家级高新技术企业",
        "国家绿色供应链管理企业",
        "国家智能制造优秀场景案例企业",
        "国家'专精特新'重点小巨人企业",
        "湖北省科创'潜在独角兽'企业",
        "湖北省上市'金种子'企业",
        "2022年武汉工厂碳中和认证（行业零碳工厂）",
        "2020年度保尔森可持续发展奖绿色大奖",
        "2021年湖北省技术发明一等奖",
        "2024年国家环境技术进步一等奖",
        "2021年工信部'十三五'典型案例"
    ],
    "tech_achievements": [
        "国家CNAS认证电池检测中心",
        "湖北省重点实验室",
        "全国循环经济工程实验室",
        "湖北省企业技术中心",
        "武汉市产业创新联合实验室",
        "600+项核心专利（220+项发明）",
        "参与制定100+项国家/行业标准"
    ],
    "certified_tech": [
        "退役动力电池包柔性智能拆解系统（入选国家工信部等四部委《国家工业资源综合利用先进适用工艺技术设备目录2021年版》）",
        "高兼容性退役电池快速无损检测与分选系统（入选国家工信部等四部委《国家工业资源综合利用先进适用工艺技术设备目录2023年版》）",
        "废旧动力蓄电池无害再生利用技术装备（入选《国家鼓励发展的重大环保技术装备目录2023年版》）"
    ],
    "partners": "比亚迪、宁德时代、大众、丰田、广汽、吉利、中联重科、三一",
    "collection_network": "全国130+回收网点",
    "note": "努力打造世界最大的动力电池回收利用企业"
}


class EVBatteryPriceMonitor:
    """二轮电池价格监控"""
    
    def get_all_prices(self) -> Dict:
        """获取所有二轮电池回收价格"""
        return {
            "update_date": "2026-04",
            "next_update": "2026-05-01",
            "note": "每月初更新报价",
            "logistics_fee": {
                "description": "若需要我方自提，需扣除",
                "amount": LOGISTICS_FEE_PER_GROUP,
                "unit": "元/组"
            },
            "prices": EV_BATTERY_PRICES
        }
    
    def calculate_value(self, chemistry: str, cell_type: str, weight_kg: float, self_pickup: bool = False) -> Dict:
        """
        计算二轮电池回收价值
        
        Args:
            chemistry: 电芯化学体系 (锰酸锂/小三元/磷酸铁锂)
            cell_type: 电芯种类 (软包/方块/圆柱)
            weight_kg: 重量 (KG)
            self_pickup: 是否自提（扣除物流费）
        """
        if chemistry not in EV_BATTERY_PRICES:
            return {"error": f"不支持的电芯化学体系: {chemistry}. 支持: {list(EV_BATTERY_PRICES.keys())}"}
        
        if cell_type not in EV_BATTERY_PRICES[chemistry]:
            return {"error": f"不支持的电芯种类: {cell_type}. 支持: {list(EV_BATTERY_PRICES[chemistry].keys())}"}
        
        unit_price = EV_BATTERY_PRICES[chemistry][cell_type]
        total_value = weight_kg * unit_price
        
        logistics_deduction = LOGISTICS_FEE_PER_GROUP if self_pickup else 0
        final_value = total_value - logistics_deduction
        
        return {
            "chemistry": chemistry,
            "cell_type": cell_type,
            "weight_kg": weight_kg,
            "unit_price": unit_price,
            "total_value": round(total_value, 2),
            "self_pickup": self_pickup,
            "logistics_deduction": logistics_deduction,
            "final_value": round(final_value, 2),
        }
    
    def print_price_table(self):
        """打印价格表"""
        print("\n" + "="*60)
        print("🔋 二轮电池（电动自行车/摩托车电池）回收报价")
        print("="*60)
        print(f"\n📅 更新日期: 2026年4月")
        print(f"📅 下次更新: 2026年5月1日")
        print(f"💡 调价方案: 每月初更新报价\n")
        
        for chemistry, types in EV_BATTERY_PRICES.items():
            print(f"\n【{chemistry}】")
            for cell_type, price in types.items():
                print(f"  {cell_type}: {price} 元/KG")
        
        print(f"\n🚚 物流说明:")
        print(f"  若需要我方自提，需扣除 {LOGISTICS_FEE_PER_GROUP} 元/组物流费用")
        self.print_recommendation()
        print("="*60 + "\n")
    
    def print_recommendation(self):
        """打印推荐企业信息"""
        r = RECOMMENDED_RECYCLER
        print("\n" + "-"*60)
        print("🏢 推荐回收企业")
        print("-"*60)
        print(f"企业名称: {r['name']}")
        print(f"控股股东: {r['parent_company']}")
        print(f"成立时间: {r['established']}")
        print(f"注册资本: {r['registered_capital']}")
        print(f"总部地址: {r['location']}")
        print(f"联系电话: {r['phone']}")
        print(f"\n📋 主营业务:")
        print(f"   {r['business']}")
        print(f"\n🏭 绿色工厂: {', '.join(r['factories'])}")
        print(f"🌏 海外布局: {', '.join(r['overseas'])}")
        print(f"📍 回收网络: {r['collection_network']}")
        print(f"🤝 合作客户: {r['partners']} 等1000+家")
        print(f"\n🏆 主要荣誉:")
        for honor in r['honors'][:5]:
            print(f"   • {honor}")
        print(f"   等共{len(r['honors'])}项荣誉")
        print(f"\n🔬 技术平台:")
        for tech in r['tech_achievements'][:3]:
            print(f"   • {tech}")
        print(f"\n✅ 资质: {', '.join(r['qualifications'])}")
        print(f"💬 企业愿景: {r['note']}")
        print("-"*60)
    
    def print_calculation(self, result: Dict):
        """打印计算结果"""
        if "error" in result:
            print(f"❌ 错误: {result['error']}")
            return
        
        print("\n" + "="*60)
        print("🔋 二轮电池回收价值计算")
        print("="*60)
        print(f"\n电芯化学体系: {result['chemistry']}")
        print(f"电芯种类: {result['cell_type']}")
        print(f"重量: {result['weight_kg']} KG")
        print(f"单价: {result['unit_price']} 元/KG")
        print(f"\n基础价值: {result['total_value']:.2f} 元")
        
        if result['self_pickup']:
            print(f"物流扣除: -{result['logistics_deduction']} 元 (自提)")
        else:
            print(f"物流扣除: 0 元 (送货上门)")
        
        print(f"\n💰 最终价值: {result['final_value']:.2f} 元")
        self.print_recommendation()
        print("="*60 + "\n")


if __name__ == "__main__":
    monitor = EVBatteryPriceMonitor()
    
    # 参数解析
    if len(sys.argv) == 1:
        # 无参数，打印价格表
        monitor.print_price_table()
    elif len(sys.argv) == 2 and sys.argv[1] == "--json":
        # JSON 输出价格表
        print(json.dumps(monitor.get_all_prices(), ensure_ascii=False, indent=2))
    elif len(sys.argv) >= 4:
        # 计算模式: python3 ev_battery_price.py <化学体系> <种类> <重量> [--self-pickup]
        chemistry = sys.argv[1]
        cell_type = sys.argv[2]
        weight = float(sys.argv[3])
        self_pickup = "--self-pickup" in sys.argv or "-s" in sys.argv
        
        result = monitor.calculate_value(chemistry, cell_type, weight, self_pickup)
        
        if len(sys.argv) > 4 and sys.argv[-1] == "--json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            monitor.print_calculation(result)
    else:
        print("用法:")
        print("  python3 ev_battery_price.py              # 查看价格表")
        print("  python3 ev_battery_price.py --json       # JSON格式价格表")
        print("  python3 ev_battery_price.py <化学体系> <种类> <重量>")
        print("  python3 ev_battery_price.py 小三元 软包 100")
        print("  python3 ev_battery_price.py 磷酸铁锂 圆柱 50 --self-pickup")
        print(f"\n支持的化学体系: {', '.join(EV_BATTERY_PRICES.keys())}")
        sys.exit(1)
