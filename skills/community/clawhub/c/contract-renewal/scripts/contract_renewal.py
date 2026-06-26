#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合同续租管理主程序
基于《园区运营项目客户服务标准指引》续扩租管理章节
"""

import pandas as pd
import json
from datetime import datetime, timedelta
import os
import sys

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
from data_manager import ContractRenewalDataManager
from reminder_generator import ContractRenewalReminderGenerator
from wecom_sender import WecomSender

class ContractRenewalManager:
    """合同续租管理主类"""
    
    def __init__(self, excel_path="/Users/mac/美兰中心C+服务.xlsx"):
        """初始化"""
        self.excel_path = excel_path
        self.data_manager = ContractRenewalDataManager(excel_path)
        self.reminder = ContractRenewalReminderGenerator()
        self.sender = WecomSender()
        
        # 预警时间节点（提前月数）
        self.warning_months = {
            '红色预警': 3,   # 提前3个月
            '黄色预警': 4,   # 提前4个月
            '绿色预警': 6    # 提前6个月
        }
        
        # 企业画像维度
        self.profile_dimensions = {
            '企业规模': ['大型', '中型', '小型', '微型'],
            '行业类型': ['制造业', '科技研发', '商务服务', '商贸物流', '其他'],
            '经营状况': ['优秀', '良好', '一般', '困难'],
            '租金承受力': ['强', '中', '弱'],
            '合作意愿': ['强', '中', '弱'],
            '增值服务需求': ['高', '中', '低']
        }
        
        # 续租方案模板
        self.renewal_templates = {
            'A类-稳租方案': {
                '适用条件': {
                    '经营状况': ['优秀', '良好'],
                    '合作意愿': '强',
                    '租金承受力': ['强', '中']
                },
                '方案要点': [
                    '提供续租优惠（如免租期、装修补贴）',
                    '优先扩租权',
                    'C+增值服务套餐',
                    '长期合同锁定（3-5年）'
                ],
                '租金策略': '市场价或略有优惠'
            },
            'B类-保持方案': {
                '适用条件': {
                    '经营状况': ['良好', '一般'],
                    '合作意愿': '中',
                    '租金承受力': '中'
                },
                '方案要点': [
                    '维持现有租金水平',
                    '灵活租期（1-2年）',
                    '基础物业服务',
                    '适度扩租机会'
                ],
                '租金策略': '市场价'
            },
            'C类-调整方案': {
                '适用条件': {
                    '经营状况': ['一般', '困难'],
                    '合作意愿': '弱',
                    '租金承受力': '弱'
                },
                '方案要点': [
                    '租金调整方案',
                    '缩租或换租建议',
                    '协助招商转租',
                    '提前解约谈判'
                ],
                '租金策略': '协商调整或市场化退出'
            }
        }
    
    def check_renewal_warnings(self):
        """检查合同续租预警"""
        print("检查合同续租预警...")
        
        warnings = {
            '红色预警': [],
            '黄色预警': [],
            '绿色预警': []
        }
        
        # 获取所有客户信息
        customers = self.data_manager.get_all_customers()
        
        if customers.empty:
            print("无客户信息")
            return warnings
        
        today = datetime.now()
        
        for _, customer in customers.iterrows():
            # 获取合同到期日期
            expiry_date_str = customer.get('合同到期日期', '')
            
            if not expiry_date_str:
                continue
            
            try:
                expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d')
                months_to_expiry = (expiry_date.year - today.year) * 12 + (expiry_date.month - today.month)
                
                # 判断预警等级
                if months_to_expiry <= self.warning_months['红色预警']:
                    warning_level = '红色预警'
                elif months_to_expiry <= self.warning_months['黄色预警']:
                    warning_level = '黄色预警'
                elif months_to_expiry <= self.warning_months['绿色预警']:
                    warning_level = '绿色预警'
                else:
                    continue
                
                # 添加预警信息
                warning_info = {
                    '客户ID': customer.get('客户ID', ''),
                    '客户名称': customer.get('客户名称', ''),
                    '房号': customer.get('房号', ''),
                    '合同到期日期': expiry_date_str,
                    '距到期月数': months_to_expiry,
                    '预警等级': warning_level,
                    '企业规模': customer.get('企业规模', ''),
                    '行业类型': customer.get('行业类型', ''),
                    '经营状况': customer.get('经营状况', '')
                }
                
                warnings[warning_level].append(warning_info)
                
            except Exception as e:
                print(f"处理客户 {customer.get('客户名称', '')} 时出错: {e}")
                continue
        
        # 发送预警通知
        for level, warning_list in warnings.items():
            if warning_list:
                self.sender.send_renewal_warning(level, warning_list)
        
        print(f"预警统计: 红色{len(warnings['红色预警'])}个, 黄色{len(warnings['黄色预警'])}个, 绿色{len(warnings['绿色预警'])}个")
        return warnings
    
    def analyze_enterprise_profile(self, customer_id):
        """分析企业画像"""
        print(f"分析企业画像: {customer_id}")
        
        # 获取客户数据
        customer = self.data_manager.get_customer_by_id(customer_id)
        
        if not customer:
            print("客户不存在")
            return None
        
        # 构建企业画像
        profile = {
            '客户ID': customer_id,
            '客户名称': customer.get('客户名称', ''),
            '房号': customer.get('房号', ''),
            '企业规模': customer.get('企业规模', '未知'),
            '行业类型': customer.get('行业类型', '未知'),
            '经营状况': self._assess_business_status(customer),
            '租金承受力': self._assess_rent_affordability(customer),
            '合作意愿': self._assess_cooperation_willingness(customer),
            '增值服务需求': self._assess_service_demand(customer),
            '分析时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 综合评价
        profile['综合评价'] = self._generate_overall_assessment(profile)
        
        return profile
    
    def _assess_business_status(self, customer):
        """评估经营状况"""
        # 基于多维度评估
        # 简化实现，实际应基于更复杂的数据分析
        complaints = customer.get('投诉次数', 0)
        arrears = customer.get('欠费金额', 0)
        
        if arrears > 0:
            return '困难'
        elif complaints > 3:
            return '一般'
        else:
            return customer.get('经营状况', '良好')
    
    def _assess_rent_affordability(self, customer):
        """评估租金承受力"""
        # 基于企业规模和行业评估
        scale = customer.get('企业规模', '小型')
        industry = customer.get('行业类型', '')
        
        if scale == '大型':
            return '强'
        elif scale == '中型' and industry in ['科技研发', '商务服务']:
            return '强'
        elif scale == '中型':
            return '中'
        elif scale == '小型' and industry in ['科技研发', '制造业']:
            return '中'
        else:
            return '弱'
    
    def _assess_cooperation_willingness(self, customer):
        """评估合作意愿"""
        # 基于历史行为评估
        # 简化实现
        payment_record = customer.get('缴费记录', '良好')
        complaints = customer.get('投诉次数', 0)
        
        if payment_record == '良好' and complaints < 2:
            return '强'
        elif payment_record == '一般' or complaints < 5:
            return '中'
        else:
            return '弱'
    
    def _assess_service_demand(self, customer):
        """评估增值服务需求"""
        # 基于企业类型和行业评估
        industry = customer.get('行业类型', '')
        
        if industry in ['科技研发', '商务服务']:
            return '高'
        elif industry in ['制造业', '商贸物流']:
            return '中'
        else:
            return '低'
    
    def _generate_overall_assessment(self, profile):
        """生成综合评价"""
        score = 0
        
        # 企业规模评分
        scale_scores = {'大型': 3, '中型': 2, '小型': 1, '微型': 0}
        score += scale_scores.get(profile['企业规模'], 0)
        
        # 经营状况评分
        status_scores = {'优秀': 3, '良好': 2, '一般': 1, '困难': 0}
        score += status_scores.get(profile['经营状况'], 0)
        
        # 租金承受力评分
        afford_scores = {'强': 2, '中': 1, '弱': 0}
        score += afford_scores.get(profile['租金承受力'], 0)
        
        # 合作意愿评分
        willing_scores = {'强': 2, '中': 1, '弱': 0}
        score += willing_scores.get(profile['合作意愿'], 0)
        
        # 综合评价
        if score >= 8:
            return '优质客户-重点稳租'
        elif score >= 6:
            return '稳定客户-保持关系'
        elif score >= 4:
            return '一般客户-适度关注'
        else:
            return '风险客户-重点关注'
    
    def generate_renewal_plan(self, customer_id):
        """生成续租方案"""
        print(f"生成续租方案: {customer_id}")
        
        # 获取企业画像
        profile = self.analyze_enterprise_profile(customer_id)
        
        if not profile:
            return None
        
        # 匹配续租方案
        matched_template = self._match_renewal_template(profile)
        
        # 生成续租计划
        plan = {
            '计划ID': f"RENEW-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            '客户ID': customer_id,
            '客户名称': profile['客户名称'],
            '房号': profile['房号'],
            '企业画像': profile,
            '匹配方案': matched_template['方案名称'],
            '方案要点': matched_template['方案要点'],
            '租金策略': matched_template['租金策略'],
            '建议措施': self._generate_recommendations(profile, matched_template),
            '预计成功率': self._estimate_success_rate(profile, matched_template),
            '创建时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 保存续租计划
        self.data_manager.add_renewal_plan(plan)
        
        print(f"续租方案已生成: {plan['计划ID']}")
        return plan
    
    def _match_renewal_template(self, profile):
        """匹配续租方案模板"""
        # 匹配A类方案
        if (profile['经营状况'] in ['优秀', '良好'] and
            profile['合作意愿'] == '强' and
            profile['租金承受力'] in ['强', '中']):
            return {
                '方案名称': 'A类-稳租方案',
                '方案要点': self.renewal_templates['A类-稳租方案']['方案要点'],
                '租金策略': self.renewal_templates['A类-稳租方案']['租金策略']
            }
        
        # 匹配B类方案
        elif (profile['经营状况'] in ['良好', '一般'] and
              profile['合作意愿'] == '中' and
              profile['租金承受力'] == '中'):
            return {
                '方案名称': 'B类-保持方案',
                '方案要点': self.renewal_templates['B类-保持方案']['方案要点'],
                '租金策略': self.renewal_templates['B类-保持方案']['租金策略']
            }
        
        # 匹配C类方案
        else:
            return {
                '方案名称': 'C类-调整方案',
                '方案要点': self.renewal_templates['C类-调整方案']['方案要点'],
                '租金策略': self.renewal_templates['C类-调整方案']['租金策略']
            }
    
    def _generate_recommendations(self, profile, template):
        """生成建议措施"""
        recommendations = []
        
        # 根据企业画像和方案生成具体建议
        if template['方案名称'] == 'A类-稳租方案':
            recommendations = [
                f"安排高层拜访，表达续租诚意",
                f"提供{profile['行业类型']}行业定制服务方案",
                "提前锁定扩租面积，避免竞争",
                "邀请参加园区重要活动，增强归属感"
            ]
        elif template['方案名称'] == 'B类-保持方案':
            recommendations = [
                "定期走访，了解经营需求",
                "提供适度优惠，维持关系",
                "关注竞品动态，及时响应",
                "提升服务质量，增强粘性"
            ]
        else:  # C类方案
            recommendations = [
                "深入调研经营困难原因",
                "提供灵活的租金支付方案",
                "协助招商转租或换租",
                "准备替代客户预案"
            ]
        
        return recommendations
    
    def _estimate_success_rate(self, profile, template):
        """预测续租成功率"""
        base_rate = 50
        
        # 根据各维度调整
        if profile['经营状况'] in ['优秀', '良好']:
            base_rate += 20
        elif profile['经营状况'] == '困难':
            base_rate -= 20
        
        if profile['合作意愿'] == '强':
            base_rate += 15
        elif profile['合作意愿'] == '弱':
            base_rate -= 15
        
        if profile['租金承受力'] == '强':
            base_rate += 10
        elif profile['租金承受力'] == '弱':
            base_rate -= 10
        
        # 方案匹配度
        if template['方案名称'] == 'A类-稳租方案':
            base_rate += 10
        
        return min(max(base_rate, 10), 95)  # 限制在10%-95%
    
    def track_renewal_progress(self, plan_id, progress_data):
        """跟踪续租进度"""
        print(f"跟踪续租进度: {plan_id}")
        
        # 更新续租计划状态
        self.data_manager.update_renewal_plan(plan_id, progress_data)
        
        # 发送进度更新通知
        self.sender.send_progress_update(plan_id, progress_data)
        
        print(f"续租进度已更新: {plan_id}")
        return True
    
    def generate_renewal_report(self, start_date, end_date):
        """生成续租工作报告"""
        print(f"生成续租工作报告: {start_date} 至 {end_date}")
        
        # 获取报告期间的续租计划
        plans = self.data_manager.get_renewal_plans_by_date_range(start_date, end_date)
        
        if plans.empty:
            print("该期间无续租计划")
            return None
        
        # 统计分析
        status_distribution = plans['状态'].value_counts().to_dict() if '状态' in plans.columns else {}
        plan_distribution = plans['匹配方案'].value_counts().to_dict() if '匹配方案' in plans.columns else {}
        
        # 成功率统计
        completed = plans[plans['状态'] == '已完成'] if '状态' in plans.columns else pd.DataFrame()
        success_rate = (len(completed) / len(plans) * 100) if len(plans) > 0 else 0
        
        # 生成报告
        report = {
            '报告ID': f"RENEW-RPT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            '报告名称': f"合同续租工作报告({start_date}至{end_date})",
            '报告期间': f"{start_date} 至 {end_date}",
            '生成时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '总计划数': len(plans),
            '已完成数': len(completed),
            '成功率': round(success_rate, 1),
            '状态分布': status_distribution,
            '方案分布': plan_distribution,
            '预警统计': self._get_warning_statistics()
        }
        
        # 保存报告
        report_path = f"/Users/mac/.qclaw/skills/contract-renewal/reports/续租工作报告_{start_date}_{end_date}.json"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"续租工作报告已生成: {report_path}")
        return report
    
    def _get_warning_statistics(self):
        """获取预警统计"""
        warnings = self.check_renewal_warnings()
        
        return {
            '红色预警': len(warnings['红色预警']),
            '黄色预警': len(warnings['黄色预警']),
            '绿色预警': len(warnings['绿色预警']),
            '总预警数': sum(len(w) for w in warnings.values())
        }
    
    def run_monthly_task(self):
        """每月任务"""
        print(f"开始合同续租管理每月任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        result = {
            '任务时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '操作': []
        }
        
        # 1. 检查续租预警
        warnings = self.check_renewal_warnings()
        result['操作'].append(f"检查续租预警: 红色{len(warnings['红色预警'])}个, 黄色{len(warnings['黄色预警'])}个, 绿色{len(warnings['绿色预警'])}个")
        
        # 2. 为红色预警客户生成续租方案
        for warning in warnings['红色预警']:
            plan = self.generate_renewal_plan(warning['客户ID'])
            if plan:
                result['操作'].append(f"生成续租方案: {warning['客户名称']}")
        
        return result

def main():
    """主函数"""
    manager = ContractRenewalManager()
    
    # 根据命令行参数执行不同任务
    if len(sys.argv) > 1:
        task = sys.argv[1]
        
        if task == 'check':
            # 检查预警
            warnings = manager.check_renewal_warnings()
            print("\n续租预警统计:")
            for level, warning_list in warnings.items():
                if warning_list:
                    print(f"\n{level}:")
                    for i, warning in enumerate(warning_list, 1):
                        print(f"  {i}. {warning['客户名称']} - {warning['房号']} - 距到期{warning['距到期月数']}个月")
        
        elif task == 'profile':
            # 分析企业画像
            if len(sys.argv) > 2:
                customer_id = sys.argv[2]
                profile = manager.analyze_enterprise_profile(customer_id)
                if profile:
                    print("\n企业画像:")
                    print(f"  客户名称: {profile['客户名称']}")
                    print(f"  企业规模: {profile['企业规模']}")
                    print(f"  行业类型: {profile['行业类型']}")
                    print(f"  经营状况: {profile['经营状况']}")
                    print(f"  租金承受力: {profile['租金承受力']}")
                    print(f"  合作意愿: {profile['合作意愿']}")
                    print(f"  综合评价: {profile['综合评价']}")
            else:
                print("用法: python main.py profile <客户ID>")
        
        elif task == 'plan':
            # 生成续租方案
            if len(sys.argv) > 2:
                customer_id = sys.argv[2]
                plan = manager.generate_renewal_plan(customer_id)
                if plan:
                    print(f"\n续租方案已生成:")
                    print(f"  计划ID: {plan['计划ID']}")
                    print(f"  匹配方案: {plan['匹配方案']}")
                    print(f"  租金策略: {plan['租金策略']}")
                    print(f"  预计成功率: {plan['预计成功率']}%")
                    print(f"\n方案要点:")
                    for i, point in enumerate(plan['方案要点'], 1):
                        print(f"  {i}. {point}")
            else:
                print("用法: python main.py plan <客户ID>")
        
        elif task == 'track':
            # 跟踪进度
            print("跟踪续租进度功能（需传入参数）")
        
        elif task == 'report':
            # 生成报告
            if len(sys.argv) > 3:
                start_date = sys.argv[2]
                end_date = sys.argv[3]
                report = manager.generate_renewal_report(start_date, end_date)
                if report:
                    print(f"\n{report['报告名称']}:")
                    print(f"  总计划数: {report['总计划数']}")
                    print(f"  已完成数: {report['已完成数']}")
                    print(f"  成功率: {report['成功率']}%")
            else:
                print("用法: python main.py report <开始日期> <结束日期>")
        
        elif task == 'monthly':
            # 执行每月任务
            result = manager.run_monthly_task()
            print("\n每月任务完成:")
            for action in result['操作']:
                print(f"  - {action}")
        
        else:
            print(f"未知任务: {task}")
            print_usage()
    
    else:
        # 默认检查预警
        manager.check_renewal_warnings()

def print_usage():
    """打印使用说明"""
    print("""
合同续租管理技能使用说明:

1. 检查续租预警:
   python main.py check

2. 分析企业画像:
   python main.py profile <客户ID>
   示例: python main.py profile C-001

3. 生成续租方案:
   python main.py plan <客户ID>
   示例: python main.py plan C-001

4. 跟踪续租进度:
   python main.py track <计划ID> <进度数据JSON>

5. 生成续租报告:
   python main.py report <开始日期> <结束日期>
   示例: python main.py report 2026-01-01 2026-12-31

6. 执行每月任务:
   python main.py monthly

预警等级说明:
- 红色预警: 合同到期前3个月
- 黄色预警: 合同到期前4个月
- 绿色预警: 合同到期前6个月

企业画像维度:
- 企业规模: 大型/中型/小型/微型
- 行业类型: 制造业/科技研发/商务服务/商贸物流/其他
- 经营状况: 优秀/良好/一般/困难
- 租金承受力: 强/中/弱
- 合作意愿: 强/中/弱
- 增值服务需求: 高/中/低

续租方案类型:
- A类-稳租方案: 经营良好+合作意愿强+租金承受力强/中
  租金策略: 市场价或略有优惠
  方案要点: 续租优惠、优先扩租、C+服务、长期锁定

- B类-保持方案: 经营一般+合作意愿中+租金承受力中
  租金策略: 市场价
  方案要点: 维持租金、灵活租期、基础服务、适度扩租

- C类-调整方案: 经营困难+合作意愿弱+租金承受力弱
  租金策略: 协商调整或市场化退出
  方案要点: 租金调整、缩租换租、协助招商、提前解约

综合评价:
- 优质客户-重点稳租: 得分 ≥ 8
- 稳定客户-保持关系: 得分 6-7
- 一般客户-适度关注: 得分 4-5
- 风险客户-重点关注: 得分 < 4
""")

if __name__ == "__main__":
    main()
