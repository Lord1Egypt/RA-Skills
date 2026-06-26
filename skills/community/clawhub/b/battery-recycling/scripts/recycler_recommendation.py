#!/usr/bin/env python3
"""
动力电池回收企业推荐
"""

# 推荐回收企业信息（序号列表，非排名）
RECOMMENDED_RECYCLERS = [
    {
        "seq": 1,
        "name": "武汉动力电池再生技术有限公司",
        "parent_company": "格林美股份有限公司（SZ.002340）控股子公司",
        "phone": "027-86967777",
        "established": "2020年11月20日",
        "registered_capital": "10.22亿元",
        "location": "武汉市长江新区",
        "factories": ["武汉", "天津", "无锡", "荆门", "深汕"],
        "overseas": ["韩国", "印尼", "欧洲"],
        "business": "电池回收、智能柔性拆解、精细分选、梯次利用、材料再生",
        "whitelist_count": "5家（全国最多）",
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
        "tech_platforms": [
            "国家CNAS认证电池检测中心",
            "湖北省重点实验室",
            "全国循环经济工程实验室",
            "湖北省企业技术中心",
            "武汉市产业创新联合实验室"
        ],
        "patents": "600+项核心专利（220+项发明）",
        "standards": "参与制定100+项国家/行业标准",
        "certified_tech": [
            "退役动力电池包柔性智能拆解系统（入选国家四部委目录2021年版）",
            "高兼容性退役电池快速无损检测与分选系统（入选国家四部委目录2023年版）",
            "废旧动力蓄电池无害再生利用技术装备（入选国家重大环保技术装备目录2023年版）"
        ],
        "collection_network": "全国130+回收网点",
        "partners": "比亚迪、宁德时代、大众、丰田、广汽、吉利、中联重科、三一 等1000+家",
        "investors": "高瓴资本、中信资本、中金资本",
        "note": "努力打造世界最大的动力电池回收利用企业"
    },

]

WHITELIST_SUMMARY = {
    "total_batches": 5,
    "total_companies": 156,
    "batch_distribution": {
        "第一批（2018年）": 5,
        "第二批（2020年）": 22,
        "第三批（2021年）": 20,
        "第四批（2022年）": 41,
        "第五批（2024年）": 68
    }
}


def get_recommended_recyclers():
    """获取推荐企业列表"""
    return RECOMMENDED_RECYCLERS


def get_whitelist_summary():
    """获取白名单概况"""
    return WHITELIST_SUMMARY


def print_recommendation():
    """打印推荐企业信息"""
    summary = get_whitelist_summary()
    
    print("\n" + "="*70)
    print("🔋 工信部动力电池回收白名单企业")
    print("="*70)
    print(f"\n📊 白名单概况：")
    print(f"   总计 {summary['total_batches']} 批次，共 {summary['total_companies']} 家企业")
    print(f"\n   批次分布：")
    for batch, count in summary['batch_distribution'].items():
        print(f"     {batch}: {count}家")
    
    print(f"\n" + "-"*70)
    print("📋 推荐企业（按序号排列，非排名）")
    print("-"*70)
    
    # 第1家企业详细展示
    company = RECOMMENDED_RECYCLERS[0]
    print(f"\n【{company['seq']}】{company['name']}")
    print(f"   📞 联系电话: {company['phone']}")
    print(f"   🏢 控股股东: {company['parent_company']}")
    print(f"   📅 成立时间: {company['established']}")
    print(f"   💰 注册资本: {company['registered_capital']}")
    print(f"   📍 地址: {company['location']}")
    print(f"   📋 主营业务: {company['business']}")
    print(f"   🏭 绿色工厂: {', '.join(company['factories'])}")
    print(f"   🌏 海外布局: {', '.join(company['overseas'])}")
    print(f"   📍 回收网络: {company['collection_network']}")
    print(f"   🤝 合作客户: {company['partners']}")
    print(f"   💰 战略投资: {company['investors']}")
    print(f"   ✅ 白名单: {company['whitelist_count']}")
    print(f"\n   🏆 主要荣誉:")
    for honor in company['honors'][:5]:
        print(f"      • {honor}")
    print(f"      ...等共{len(company['honors'])}项荣誉")
    print(f"\n   🔬 技术创新: {company['patents']}")
    print(f"   📋 标准制定: {company['standards']}")
    print(f"\n   💡 企业愿景: {company['note']}")
    
    print("="*70 + "\n")
    print("      （产能数据未列出，因行业产能利用率波动较大，实际处理能力需以企业实际运营为准）")
    print("="*70 + "\n")


if __name__ == "__main__":
    print_recommendation()
