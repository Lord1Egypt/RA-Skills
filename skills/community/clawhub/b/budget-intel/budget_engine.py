#!/usr/bin/env python3
"""
企业预算情报 - 预算计算引擎
Budget Intelligence Engine for Budget-Intel Skill

支持多方法预算估算和置信度评分
"""

import math
import json
import sys
from typing import Dict, List, Optional, Tuple


class BudgetEngine:
    """企业预算计算引擎"""

    def __init__(self):
        # 行业 IT 投入比例（营收百分比）
        self.industry_it_ratio = {
            "金融": (0.03, 0.05),
            "银行": (0.04, 0.06),
            "保险": (0.03, 0.05),
            "证券": (0.04, 0.06),
            "互联网": (0.08, 0.15),
            "科技": (0.06, 0.12),
            "软件": (0.08, 0.15),
            "制造业": (0.01, 0.03),
            "制造": (0.01, 0.03),
            "零售": (0.02, 0.04),
            "电商": (0.04, 0.08),
            "医疗": (0.02, 0.03),
            "医院": (0.02, 0.03),
            "教育": (0.02, 0.04),
            "能源": (0.02, 0.04),
            "房地产": (0.01, 0.02),
            "物流": (0.02, 0.04),
            "交通": (0.02, 0.04),
            "媒体": (0.03, 0.06),
            "娱乐": (0.03, 0.06),
            "游戏": (0.08, 0.15),
            "通信": (0.03, 0.05),
            "电信": (0.03, 0.05),
            "汽车": (0.02, 0.04),
            "医药": (0.02, 0.04),
            "生物": (0.03, 0.06),
            "人工智能": (0.10, 0.20),
            "AI": (0.10, 0.20),
            "大数据": (0.08, 0.15),
            "云计算": (0.08, 0.15),
        }

        # 数字化占 IT 预算比例
        self.digital_ratio = {
            "金融": (0.40, 0.60),
            "互联网": (0.60, 0.80),
            "科技": (0.60, 0.80),
            "软件": (0.60, 0.80),
            "制造业": (0.30, 0.50),
            "零售": (0.40, 0.60),
            "医疗": (0.30, 0.50),
            "教育": (0.30, 0.50),
            "人工智能": (0.70, 0.90),
            "AI": (0.70, 0.90),
        }

        # 智能化占数字化预算比例
        self.ai_ratio = {
            "金融": (0.15, 0.25),
            "互联网": (0.25, 0.40),
            "科技": (0.20, 0.35),
            "软件": (0.25, 0.40),
            "制造业": (0.10, 0.20),
            "零售": (0.15, 0.25),
            "医疗": (0.10, 0.20),
            "人工智能": (0.40, 0.60),
            "AI": (0.40, 0.60),
        }

        # 数据源置信度
        self.source_confidence = {
            "财报": 0.95,
            "招股书": 0.95,
            "年报": 0.90,
            "招投标": 0.85,
            "政府采购": 0.85,
            "新闻稿": 0.60,
            "PR": 0.55,
            "招聘信息": 0.50,
            "社交媒体": 0.30,
            "论坛": 0.25,
        }

        # 人均 IT 成本基准（万元/年）
        self.per_capita_it_cost = {
            "金融": (8, 15),
            "互联网": (15, 30),
            "科技": (12, 25),
            "软件": (15, 30),
            "制造业": (5, 10),
            "零售": (6, 12),
            "医疗": (5, 10),
            "教育": (4, 8),
            "人工智能": (20, 40),
            "AI": (20, 40),
        }

    def get_industry_ratio(self, industry: str) -> Tuple[float, float]:
        """获取行业 IT 投入比例"""
        industry = industry.lower()
        for key, value in self.industry_it_ratio.items():
            if key.lower() in industry or industry in key.lower():
                return value
        # 默认值
        return (0.03, 0.05)

    def calculate_by_revenue(self, revenue: float, industry: str) -> Dict:
        """
        方法 A：营收比例法

        Args:
            revenue: 年营收（万元）
            industry: 行业

        Returns:
            预算估算字典
        """
        it_ratio = self.get_industry_ratio(industry)
        digital_ratio = self.digital_ratio.get(industry, (0.40, 0.60))
        ai_ratio = self.ai_ratio.get(industry, (0.15, 0.25))

        it_budget_min = revenue * it_ratio[0]
        it_budget_max = revenue * it_ratio[1]

        digital_budget_min = it_budget_min * digital_ratio[0]
        digital_budget_max = it_budget_max * digital_ratio[1]

        ai_budget_min = digital_budget_min * ai_ratio[0]
        ai_budget_max = digital_budget_max * ai_ratio[1]

        return {
            "method": "营收比例法",
            "it_budget": (it_budget_min, it_budget_max),
            "digital_budget": (digital_budget_min, digital_budget_max),
            "ai_budget": (ai_budget_min, ai_budget_max),
            "confidence": 0.85 if revenue > 0 else 0.50
        }

    def calculate_by_headcount(self, tech_headcount: int, industry: str) -> Dict:
        """
        方法 B：人员比例法

        Args:
            tech_headcount: 技术团队人数
            industry: 行业

        Returns:
            预算估算字典
        """
        per_capita = self.per_capita_it_cost.get(industry, (10, 20))

        it_budget_min = tech_headcount * per_capita[0]
        it_budget_max = tech_headcount * per_capita[1]

        # 假设 IT 预算 70% 用于数字化
        digital_budget_min = it_budget_min * 0.7
        digital_budget_max = it_budget_max * 0.7

        # 假设数字化预算 20% 用于智能化
        ai_budget_min = digital_budget_min * 0.2
        ai_budget_max = digital_budget_max * 0.2

        return {
            "method": "人员比例法",
            "it_budget": (it_budget_min, it_budget_max),
            "digital_budget": (digital_budget_min, digital_budget_max),
            "ai_budget": (ai_budget_min, ai_budget_max),
            "confidence": 0.65 if tech_headcount > 0 else 0.40
        }

    def calculate_by_funding(self, funding: float) -> Dict:
        """
        方法 C：融资推算法

        Args:
            funding: 最新融资额（万元）

        Returns:
            预算估算字典
        """
        # 创业公司通常 30-50% 融资用于技术
        tech_ratio = (0.30, 0.50)

        it_budget_min = funding * tech_ratio[0]
        it_budget_max = funding * tech_ratio[1]

        digital_budget_min = it_budget_min * 0.7
        digital_budget_max = it_budget_max * 0.7

        ai_budget_min = digital_budget_min * 0.25
        ai_budget_max = digital_budget_max * 0.25

        return {
            "method": "融资推算法",
            "it_budget": (it_budget_min, it_budget_max),
            "digital_budget": (digital_budget_min, digital_budget_max),
            "ai_budget": (ai_budget_min, ai_budget_max),
            "confidence": 0.60 if funding > 0 else 0.40
        }

    def calculate_by_tender(self, tender_amount: float) -> Dict:
        """
        方法 D：招投标反推法

        Args:
            tender_amount: 历史招投标金额（万元）

        Returns:
            预算估算字典
        """
        # 招投标通常占总预算的 20-35%
        multiplier = (3.0, 5.0)

        it_budget_min = tender_amount * multiplier[0]
        it_budget_max = tender_amount * multiplier[1]

        digital_budget_min = it_budget_min * 0.5
        digital_budget_max = it_budget_max * 0.6

        ai_budget_min = digital_budget_min * 0.20
        ai_budget_max = digital_budget_max * 0.30

        return {
            "method": "招投标反推法",
            "it_budget": (it_budget_min, it_budget_max),
            "digital_budget": (digital_budget_min, digital_budget_max),
            "ai_budget": (ai_budget_min, ai_budget_max),
            "confidence": 0.75 if tender_amount > 0 else 0.50
        }

    def merge_estimates(self, estimates: List[Dict]) -> Dict:
        """
        合并多个估算结果，计算加权平均

        Args:
            estimates: 多个估算结果列表

        Returns:
            合并后的估算结果
        """
        if not estimates:
            return {"error": "No estimates provided"}

        # 加权平均
        total_weight = sum(e.get('confidence', 0.5) for e in estimates)

        it_min = sum(e['it_budget'][0] * e.get('confidence', 0.5) for e in estimates) / total_weight
        it_max = sum(e['it_budget'][1] * e.get('confidence', 0.5) for e in estimates) / total_weight

        digital_min = sum(e['digital_budget'][0] * e.get('confidence', 0.5) for e in estimates) / total_weight
        digital_max = sum(e['digital_budget'][1] * e.get('confidence', 0.5) for e in estimates) / total_weight

        ai_min = sum(e['ai_budget'][0] * e.get('confidence', 0.5) for e in estimates) / total_weight
        ai_max = sum(e['ai_budget'][1] * e.get('confidence', 0.5) for e in estimates) / total_weight

        # 综合置信度：数据源越多，置信度越高
        base_confidence = sum(e.get('confidence', 0.5) for e in estimates) / len(estimates)
        quantity_bonus = min(0.15, (len(estimates) - 1) * 0.05)
        final_confidence = min(0.95, base_confidence + quantity_bonus)

        return {
            "it_budget": (it_min, it_max),
            "digital_budget": (digital_min, digital_max),
            "ai_budget": (ai_min, ai_max),
            "confidence": round(final_confidence, 2),
            "methods_used": [e['method'] for e in estimates],
            "data_sources_count": len(estimates)
        }

    def calculate_budget_composition(self, industry: str) -> Dict:
        """
        计算预算构成比例（15+ 细分品类）

        Args:
            industry: 行业

        Returns:
            预算构成字典（细分到品类 + 供应商）
        """
        # 互联网/地图行业默认构成（15 个细分品类）
        if industry in ["互联网", "人工智能", "AI", "软件", "科技"]:
            composition = {
                # 云服务（35%）
                "cloud_compute": {"ratio": 0.15, "vendors": ["阿里云", "腾讯云", "华为云"]},
                "cloud_storage": {"ratio": 0.08, "vendors": ["阿里云 OSS", "腾讯云 COS"]},
                "cloud_database": {"ratio": 0.07, "vendors": ["阿里云 RDS", "PolarDB", "MongoDB"]},
                "cloud_network": {"ratio": 0.05, "vendors": ["阿里云 VPC", "CDN"]},
                
                # AI/智能化（25%）
                "ai_llm": {"ratio": 0.10, "vendors": ["通义千问", "文心一言", "智谱 AI"]},
                "ai_cv": {"ratio": 0.06, "vendors": ["商汤", "旷视", "依图"]},
                "ai_nlp": {"ratio": 0.05, "vendors": ["百度 NLP", "阿里 NLP"]},
                "ai_recommendation": {"ratio": 0.04, "vendors": ["阿里推荐", "字节推荐"]},
                
                # 软件许可（25%）
                "dev_tools": {"ratio": 0.08, "vendors": ["JetBrains", "GitHub", "GitLab"]},
                "enterprise_software": {"ratio": 0.07, "vendors": ["钉钉", "企业微信", "飞书"]},
                "security": {"ratio": 0.06, "vendors": ["阿里云安全", "腾讯云安全"]},
                "analytics": {"ratio": 0.04, "vendors": ["神策数据", "GrowingIO", "Tableau"]},
                
                # 定制开发（20%）
                "custom_dev": {"ratio": 0.12, "vendors": ["外包供应商", "咨询公司"]},
                "system_integration": {"ratio": 0.05, "vendors": ["IBM", "埃森哲", "汉得"]},
                "maintenance": {"ratio": 0.03, "vendors": ["原厂商", "第三方运维"]}
            }
        
        # 金融行业构成
        elif industry in ["金融", "银行", "保险", "证券"]:
            composition = {
                "cloud_compute": {"ratio": 0.10, "vendors": ["私有云", "阿里云金融云"]},
                "cloud_storage": {"ratio": 0.06, "vendors": ["分布式存储"]},
                "cloud_database": {"ratio": 0.10, "vendors": ["Oracle", "DB2", "OceanBase"]},
                "ai_risk": {"ratio": 0.08, "vendors": ["第四范式", "同盾科技"]},
                "security": {"ratio": 0.12, "vendors": ["启明", "绿盟", "奇安信"]},
                "core_banking": {"ratio": 0.15, "vendors": ["长亮", "神州数码"]},
                "dev_tools": {"ratio": 0.05, "vendors": ["JetBrains", "Microsoft"]},
                "enterprise_software": {"ratio": 0.06, "vendors": ["钉钉", "企业微信"]},
                "custom_dev": {"ratio": 0.15, "vendors": ["外包", "咨询公司"]},
                "maintenance": {"ratio": 0.13, "vendors": ["原厂商"]}
            }
        
        # 制造业构成
        else:
            composition = {
                "erp": {"ratio": 0.20, "vendors": ["SAP", "Oracle", "用友", "金蝶"]},
                "mes": {"ratio": 0.12, "vendors": ["西门子", "达索", "宝信"]},
                "cloud": {"ratio": 0.10, "vendors": ["阿里云", "华为云"]},
                "iot": {"ratio": 0.08, "vendors": ["阿里云 IoT", "华为 IoT"]},
                "dev_tools": {"ratio": 0.05, "vendors": ["JetBrains", "Microsoft"]},
                "security": {"ratio": 0.08, "vendors": ["启明", "奇安信"]},
                "custom_dev": {"ratio": 0.20, "vendors": ["外包", "咨询公司"]},
                "maintenance": {"ratio": 0.17, "vendors": ["原厂商"]}
            }

        return composition

    def estimate_procurement_cycle(self, industry: str) -> Dict:
        """
        估算采购周期

        Args:
            industry: 行业

        Returns:
            采购周期字典
        """
        # 默认（自然年）
        cycle = {
            "fiscal_year": "自然年",
            "budget_approval": "11-12 月",
            "procurement_decision": "1-3 月",
            "implementation": "4-10 月"
        }

        # 行业特殊调整
        if industry in ["教育", "学校"]:
            cycle["fiscal_year"] = "学年制（9 月 - 次年 8 月）"
            cycle["budget_approval"] = "6-7 月"
            cycle["procurement_decision"] = "8-9 月"

        if industry in ["金融", "银行", "保险"]:
            cycle["procurement_decision"] = "2-4 月"  # 年报后

        return cycle

    def identify_key_decision_makers(self, company_name: str, industry: str) -> List[Dict]:
        """
        识别关键决策人（基于公开信息和行业模式）

        Args:
            company_name: 企业名称
            industry: 行业

        Returns:
            关键人列表
        """
        # 通用决策链模板
        decision_makers = [
            {
                "name": "[待调研]",
                "title": "CTO/技术 VP",
                "influence": 5,
                "focus": ["技术先进性", "架构兼容性", "团队效率"],
                "breakthrough": "技术白皮书 + POC 验证 + 同业案例"
            },
            {
                "name": "[待调研]",
                "title": "业务负责人/产品 VP",
                "influence": 4,
                "focus": ["ROI", "用户体验", "业务增长"],
                "breakthrough": "业务价值量化 + 竞品对比 + 试点方案"
            },
            {
                "name": "[待调研]",
                "title": "采购总监",
                "influence": 3,
                "focus": ["成本", "合规", "供应商管理"],
                "breakthrough": "TCO 分析 + 商务条款灵活 + 长期合作框架"
            },
            {
                "name": "[待调研]",
                "title": "CIO/信息部总经理",
                "influence": 5,
                "focus": ["整体规划", "系统集成", "安全合规"],
                "breakthrough": "战略规划对齐 + 集成方案 + 安全认证"
            }
        ]

        # 行业特定调整
        if industry in ["互联网", "人工智能", "软件"]:
            decision_makers.append({
                "name": "[待调研]",
                "title": "算法负责人/AI 实验室主任",
                "influence": 4,
                "focus": ["模型效果", "算力成本", "数据质量"],
                "breakthrough": "技术指标对比 + 算力优化方案"
            })

        if industry in ["金融", "银行"]:
            decision_makers.append({
                "name": "[待调研]",
                "title": "首席风险官/CRO",
                "influence": 4,
                "focus": ["风险控制", "合规审计", "数据安全"],
                "breakthrough": "合规认证 + 风控案例 + 审计支持"
            })

        if industry in ["制造业", "制造"]:
            decision_makers.append({
                "name": "[待调研]",
                "title": "生产副总/工厂总经理",
                "influence": 4,
                "focus": ["生产效率", "停机风险", "工人培训"],
                "breakthrough": "效率提升数据 + 无感切换方案"
            })

        # 阿里系特殊决策链
        if "阿里" in company_name or "高德" in company_name:
            decision_makers = [
                {
                    "name": "[待调研]",
                    "title": "高德 CEO/总裁",
                    "influence": 5,
                    "focus": ["战略对齐", "用户体验", "商业变现"],
                    "breakthrough": "战略价值 + 用户增长 + 收入提升"
                },
                {
                    "name": "[待调研]",
                    "title": "阿里集团技术委员会",
                    "influence": 5,
                    "focus": ["技术标准化", "生态协同", "安全合规"],
                    "breakthrough": "阿里技术体系兼容 + 生态价值"
                },
                {
                    "name": "[待调研]",
                    "title": "高德 CTO",
                    "influence": 4,
                    "focus": ["技术先进性", "团队效率", "架构稳定"],
                    "breakthrough": "技术 POC + 同业案例"
                },
                {
                    "name": "[待调研]",
                    "title": "阿里采购部",
                    "influence": 3,
                    "focus": ["成本", "框架协议", "供应商管理"],
                    "breakthrough": "TCO 优势 + 长期合作"
                }
            ]

        return decision_makers

    def get_industry_trends(self, industry: str, year: int = 2025) -> Dict:
        """
        获取行业趋势（内置模板库）

        Args:
            industry: 行业
            year: 年份

        Returns:
            趋势字典
        """
        trends_db = {
            "互联网": {
                "year": 2025,
                "key_trends": [
                    "大模型应用落地成为标配，从'尝鲜'转向'深用'",
                    "降本增效持续，云资源优化和 FinOps 受重视",
                    "数据合规要求升级，隐私计算需求增长",
                    "AIGC 重构产品体验，智能助手普及",
                    "出海加速，全球化基础设施投入增加"
                ],
                "budget_shifts": [
                    "AI 预算占比从 15% 提升至 25%+",
                    "云成本优化服务需求增长 50%",
                    "数据安全预算增长 30%"
                ],
                "vendor_changes": [
                    "国产大模型替代加速（通义/文心/智谱）",
                    "多云策略成为主流，避免供应商锁定",
                    "开源模型 + 自研微调成为新趋势"
                ]
            },
            "人工智能": {
                "year": 2025,
                "key_trends": [
                    "多模态大模型成为竞争焦点",
                    "推理成本优化是核心挑战",
                    "垂直行业大模型落地加速",
                    "AI 安全和对齐受到监管关注",
                    "边缘 AI 和端侧推理兴起"
                ],
                "budget_shifts": [
                    "算力预算占比持续提升（40%+）",
                    "数据标注和 RLHF 预算增长",
                    "模型评估和测试工具受重视"
                ],
                "vendor_changes": [
                    "GPU 多元化（英伟达 + 国产替代）",
                    "云厂商自研芯片占比提升",
                    "开源模型社区影响力增强"
                ]
            },
            "地图/出行": {
                "year": 2025,
                "key_trends": [
                    "高精地图 + 大模型重构导航体验",
                    "车路云一体化成为政策焦点",
                    "自动驾驶 L3 商用落地加速",
                    "MaaS（出行即服务）整合加速",
                    "低空经济（eVTOL）纳入规划"
                ],
                "budget_shifts": [
                    "大模型相关预算增长 100%+",
                    "车规级云计算投入增加",
                    "实时数据处理预算增长 50%"
                ],
                "vendor_changes": [
                    "大模型供应商多元化测试",
                    "高精地图数据采集设备升级",
                    "仿真测试平台投入增加"
                ],
                "major_players": [
                    "高德地图：阿里生态，日活 7000 万+",
                    "百度地图：AI 原生，Apollo 自动驾驶",
                    "腾讯地图：微信生态整合",
                    "华为 Petal Maps：出海重点",
                    "滴滴：出行数据优势"
                ],
                "recent_dynamics": [
                    "2024 Q4：高德宣布 AI 原生重构，推出'高德 2.0'",
                    "2024 Q4：百度地图接入文心一言 4.5",
                    "2025 Q1：车路云一体化试点城市公布（10 城）",
                    "2025 Q1：低空经济写入政府工作报告"
                ]
            },
            "金融": {
                "year": 2025,
                "key_trends": [
                    "生成式 AI 在客服/营销/风控场景落地",
                    "核心系统分布式改造持续",
                    "数据要素资产化探索",
                    "监管科技（RegTech）投入增加",
                    "量子加密前瞻布局"
                ],
                "budget_shifts": [
                    "AI 预算占比从 10% 提升至 20%",
                    "信创预算持续增长（国产替代）",
                    "数据安全与合规预算增长 40%"
                ],
                "vendor_changes": [
                    "信创供应商份额持续提升",
                    "大模型供应商多源化",
                    "云厂商金融云竞争加剧"
                ]
            },
            "制造业": {
                "year": 2025,
                "key_trends": [
                    "工业互联网平台整合加速",
                    "AI+ 质检/预测性维护规模化",
                    "数字孪生从试点到推广",
                    "供应链韧性建设受重视",
                    "碳足迹追踪成为刚需"
                ],
                "budget_shifts": [
                    "IoT 预算稳定增长（15%/年）",
                    "AI 质检预算增长 50%",
                    "双碳相关数字化预算新增"
                ],
                "vendor_changes": [
                    "本土工业互联网平台崛起",
                    "国际巨头（西门子/GE）面临竞争",
                    "5G+ 工业应用加速"
                ]
            }
        }

        # 精确匹配
        if industry in trends_db:
            return trends_db[industry]

        # 模糊匹配
        for key in trends_db:
            if key in industry or industry in key:
                return trends_db[key]

        # 默认返回互联网行业趋势
        return trends_db["互联网"]

    def generate_opportunity_points(self, company_name: str, industry: str,
                                   budget: Dict, composition: Dict,
                                   trends: Dict) -> List[Dict]:
        """
        生成独到切入机会点

        Args:
            company_name: 企业名称
            industry: 行业
            budget: 预算估算
            composition: 预算构成
            trends: 行业趋势

        Returns:
            机会点列表
        """
        opportunities = []

        # 机会点 1：趋势驱动
        if trends and "key_trends" in trends:
            for trend in trends["key_trends"][:2]:  # 取前 2 个趋势
                opportunities.append({
                    "type": "趋势驱动",
                    "description": trend,
                    "action": f"基于'{trend}'，建议推出对应解决方案",
                    "timing": "Q2-Q3 预算执行期",
                    "priority": "高"
                })

        # 机会点 2：预算转移
        if trends and "budget_shifts" in trends:
            for shift in trends["budget_shifts"]:
                opportunities.append({
                    "type": "预算转移",
                    "description": shift,
                    "action": "调整产品定位，匹配预算流向",
                    "timing": "预算审批前 1-2 月",
                    "priority": "中"
                })

        # 机会点 3：供应商变化
        if trends and "vendor_changes" in trends:
            for change in trends["vendor_changes"]:
                opportunities.append({
                    "type": "供应商变化",
                    "description": change,
                    "action": "定位替代/补充机会",
                    "timing": "合同到期前 3-6 月",
                    "priority": "中"
                })

        # 机会点 4：重大动态（如果有）
        if trends and "recent_dynamics" in trends:
            for dynamic in trends["recent_dynamics"]:
                opportunities.append({
                    "type": "重大动态",
                    "description": dynamic,
                    "action": "借势营销/方案对接",
                    "timing": "动态发布后 1 个月内",
                    "priority": "高"
                })

        # 机会点 5：预算空档（基于构成分析）
        if composition:
            # 找出占比高但供应商集中度低的品类
            for category, info in composition.items():
                if info["ratio"] > 0.08:  # 占比>8%
                    if len(info.get("vendors", [])) > 3:  # 供应商>3 家，竞争激烈
                        opportunities.append({
                            "type": "预算空档",
                            "description": f"{category} 预算占比{info['ratio']*100:.0f}%，供应商分散",
                            "action": "以差异化优势切入",
                            "timing": "随时可接触",
                            "priority": "中"
                        })

        return opportunities

    def generate_full_report(self, company_name: str, industry: str,
                            revenue: Optional[float] = None,
                            headcount: Optional[int] = None,
                            tech_headcount: Optional[int] = None,
                            funding: Optional[float] = None,
                            tender_amount: Optional[float] = None,
                            include_trends: bool = True) -> Dict:
        """
        生成完整报告（最终版 - 含趋势和机会点）

        Args:
            company_name: 企业名称
            industry: 行业
            revenue: 营收
            headcount: 员工数
            tech_headcount: 技术人数
            funding: 融资额
            tender_amount: 招投标金额
            include_trends: 是否包含趋势分析

        Returns:
            完整报告字典
        """
        estimates = []

        # 收集所有可用的估算方法
        if revenue and revenue > 0:
            estimates.append(self.calculate_by_revenue(revenue, industry))

        if tech_headcount and tech_headcount > 0:
            estimates.append(self.calculate_by_headcount(tech_headcount, industry))

        if funding and funding > 0:
            estimates.append(self.calculate_by_funding(funding))

        if tender_amount and tender_amount > 0:
            estimates.append(self.calculate_by_tender(tender_amount))

        # 如果没有有效估算，使用行业默认
        if not estimates:
            estimates.append(self.calculate_by_revenue(10000, industry))

        # 合并估算
        merged = self.merge_estimates(estimates)

        # 预算构成（细分）
        composition = self.calculate_budget_composition(industry)

        # 采购周期
        procurement = self.estimate_procurement_cycle(industry)

        # 关键决策人
        decision_makers = self.identify_key_decision_makers(company_name, industry)

        # 行业趋势（新增）
        trends = self.get_industry_trends(industry) if include_trends else None

        # 机会点（新增）
        opportunities = []
        if trends:
            opportunities = self.generate_opportunity_points(
                company_name, industry, merged, composition, trends)

        return {
            "company_name": company_name,
            "industry": industry,
            "budget": merged,
            "composition": composition,
            "procurement_cycle": procurement,
            "decision_makers": decision_makers,
            "trends": trends,
            "opportunities": opportunities,
            "input_data": {
                "revenue": revenue,
                "headcount": headcount,
                "tech_headcount": tech_headcount,
                "funding": funding,
                "tender_amount": tender_amount
            }
        }


# CLI 接口
def main():
    """命令行接口"""
    if len(sys.argv) < 2:
        print("Usage: python budget_engine.py <command> [args]")
        print("Commands:")
        print("  test              Run test calculations")
        print("  calculate <json>  Calculate budget from JSON input")
        sys.exit(1)

    engine = BudgetEngine()
    command = sys.argv[1]

    if command == "test":
        # 测试计算
        print("=" * 60)
        print("测试：某互联网公司，营收 10 亿元，技术团队 500 人")
        print("=" * 60)

        report = engine.generate_full_report(
            company_name="测试科技公司",
            industry="互联网",
            revenue=100000,  # 10 亿元
            tech_headcount=500
        )

        print(f"\n📊 {report['company_name']} 预算分析报告")
        print(f"\n🏢 行业：{report['industry']}")
        print(f"\n💰 预算估算（万元）:")
        print(f"   IT 总预算：{report['budget']['it_budget'][0]:.0f} - {report['budget']['it_budget'][1]:.0f}")
        print(f"   数字化预算：{report['budget']['digital_budget'][0]:.0f} - {report['budget']['digital_budget'][1]:.0f}")
        print(f"   智能化预算：{report['budget']['ai_budget'][0]:.0f} - {report['budget']['ai_budget'][1]:.0f}")
        print(f"   置信度：{report['budget']['confidence']*100:.0f}%")
        print(f"   使用的方法：{report['budget']['methods_used']}")

        print(f"\n📋 预算构成:")
        for k, v in report['composition'].items():
            print(f"   {k}: {v*100:.0f}%")

        print(f"\n📅 采购周期:")
        for k, v in report['procurement_cycle'].items():
            print(f"   {k}: {v}")

    elif command == "calculate":
        if len(sys.argv) < 3:
            print("Error: Please provide JSON input")
            sys.exit(1)
        input_data = json.loads(sys.argv[2])
        result = engine.generate_full_report(**input_data)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
