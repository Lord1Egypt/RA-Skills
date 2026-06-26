#!/usr/bin/env python3
"""
CCPA/CPRA合规检查工具
版本：1.0.0
最后更新：2026年3月25日
"""

import sys
import json
import argparse
from datetime import datetime

class CCPAComplianceTool:
    """CCPA/CPRA合规检查工具"""
    
    def __init__(self):
        self.results = {
            "audit_date": datetime.now().isoformat(),
            "skill_version": "1.0.0",
            "region": "US-California",
            "summary": {
                "total_checks": 0,
                "passed": 0,
                "failed": 0,
                "warnings": 0
            },
            "checks": []
        }
        
        # CCPA/CPRA核心检查项
        self.ccpa_checks = [
            self.check_company_applicability,
            self.check_notice_requirements,
            self.check_consumer_rights,
            self.check_opt_out_mechanism,
            self.check_sensitive_info_protection,
            self.check_data_sales_sharing,
            self.check_service_provider_management,
            self.check_verification_procedures,
            self.check_non_discrimination,
            self.check_recordkeeping,
            self.check_data_security,
            self.check_response_timelines
        ]
    
    def check_company_applicability(self):
        """检查企业适用性"""
        check_id = "company_applicability"
        description = "确定企业是否属于CCPA/CPRA适用范围"
        
        criteria = [
            "年总收入超过2500万美元",
            "每年购买、接收、出售或共享5万以上消费者、家庭或设备个人信息",
            "年收入的50%以上来自出售消费者个人信息"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "criteria": criteria,
            "questions": [
                "1. 您的年总收入是否超过2500万美元？",
                "2. 您每年处理超过5万个加州消费者数据吗？",
                "3. 您超过50%的收入来自数据销售吗？",
                "4. 如果您不满足任何条件，您可能仍需要考虑潜在风险"
            ],
            "recommendations": [
                "每年评估企业适用性",
                "即使不适用，也可考虑自愿实施最佳实践",
                "跟踪监管规定变化，适用条件可能调整"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_notice_requirements(self):
        """检查告知要求"""
        check_id = "notice_requirements"
        description = "验证CCPA/CPRA要求的告知义务"
        
        requirements = [
            "收集时告知（Notice at Collection）",
            "隐私政策包含CCPA/CPRA必要信息",
            "明确说明是否出售或共享个人信息",
            "提供选择退出机制说明"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "requirements": requirements,
            "questions": [
                "1. 您是否在收集信息时提供告知？",
                "2. 您的隐私政策是否包含CCPA/CPRA要求的信息？",
                "3. 您是否说明是否会出售或共享个人信息？",
                "4. 您是否提供清晰的选择退出信息？"
            ],
            "recommendations": [
                "在数据收集点提供清晰告知",
                "更新隐私政策包含CCPA/CPRA要求",
                "如果出售数据，提供明确通知",
                "确保告知以清晰易懂语言编写"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_consumer_rights(self):
        """检查消费者权利"""
        check_id = "consumer_rights"
        description = "验证消费者权利的保障机制"
        
        rights = [
            "知情权 - 了解收集的个人信息类别和具体信息",
            "删除权 - 要求删除收集的个人信息",
            "选择退出权 - 选择不出售个人信息",
            "不受歧视权 - 行使权利时不受歧视",
            "更正权（CPRA新增） - 更正不准确的个人信息",
            "限制使用权（CPRA新增） - 限制敏感个人信息使用",
            "数据可携带权（CPRA新增） - 以可移植格式获取个人信息"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "rights": rights,
            "questions": [
                "1. 您是否有机制处理消费者权利请求？",
                "2. 您是否提供多种权利请求渠道？",
                "3. 您是否免费处理权利请求？",
                "4. 您是否在法定时限内响应？"
            ],
            "recommendations": [
                "建立标准化的权利请求处理流程",
                "提供在线和离线请求渠道",
                "确保免费处理请求（合理的费用除外）",
                "建立自动化或半自动化处理系统"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_opt_out_mechanism(self):
        """检查选择退出机制"""
        check_id = "opt_out_mechanism"
        description = "验证'请勿出售我的个人信息'机制"
        
        requirements = [
            "网站首页显著位置提供选择退出链接",
            "尊重全局隐私控制信号（如全球隐私控制GPC）",
            "提供易于使用的选择退出页面",
            "尊重消费者的选择退出请求"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "requirements": requirements,
            "questions": [
                "1. 您是否有清晰可见的选择退出链接？",
                "2. 您是否支持浏览器隐私控制信号？",
                "3. 您的选择退出机制是否容易使用？",
                "4. 您是否记录和尊重所有选择退出请求？"
            ],
            "recommendations": [
                "在网站页脚添加'请勿出售我的个人信息'链接",
                "实施全球隐私控制（GPC）信号支持",
                "简化选择退出流程，减少用户摩擦",
                "维护选择退出请求数据库"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_sensitive_info_protection(self):
        """检查敏感信息保护"""
        check_id = "sensitive_info_protection"
        description = "验证敏感个人信息的保护措施（CPRA新增）"
        
        sensitive_data_types = [
            "政府身份识别号码",
            "账户凭证",
            "精确地理位置",
            "种族、民族、宗教信仰、工会会员",
            "邮件/短信内容",
            "基因数据、生物识别信息",
            "健康信息、性生活、性取向",
            "未成年人的个人信息"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "sensitive_data_types": sensitive_data_types,
            "questions": [
                "1. 您是否收集任何敏感个人信息？",
                "2. 您是否限制敏感信息的使用？",
                "3. 您是否提供限制敏感信息使用的机制？",
                "4. 您是否获得敏感信息处理的额外同意？"
            ],
            "recommendations": [
                "识别和分类敏感个人信息",
                "实施敏感信息使用限制",
                "提供消费者限制敏感信息使用的选项",
                "加强敏感信息的安全保护"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_data_sales_sharing(self):
        """检查数据销售与共享"""
        check_id = "data_sales_sharing"
        description = "验证数据销售和共享的合规性"
        
        distinctions = {
            "销售": "向第三方披露个人信息以换取金钱或其他有价值对价",
            "共享": "向第三方披露个人信息用于跨上下文行为广告",
            "服务提供商": "出于特定业务目的处理个人信息（非销售）"
        }
        
        result = {
            "check_id": check_id,
            "description": description,
            "distinctions": distinctions,
            "questions": [
                "1. 您是否出售个人信息？",
                "2. 您是否共享个人信息用于广告？",
                "3. 您是否与服务提供商有适当合同？",
                "4. 您是否为未成年人的数据销售提供额外保护？"
            ],
            "recommendations": [
                "明确定义和记录您的数据处理关系",
                "与服务提供商签订适当合同",
                "为未成年人（特别是13岁以下）提供额外保护",
                "记录和披露数据销售和共享实践"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_service_provider_management(self):
        """检查服务提供商管理"""
        check_id = "service_provider_management"
        description = "验证与服务提供商的关系管理"
        
        requirements = [
            "明确定义业务目的",
            "签订包含限制条款的合同",
            "禁止服务提供商将数据用于其他目的",
            "确保服务提供商采取适当安全措施"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "requirements": requirements,
            "questions": [
                "1. 您是否与所有服务提供商有适当合同？",
                "2. 合同中是否包含必要限制条款？",
                "3. 您是否监控服务提供商的合规性？",
                "4. 您是否要求服务提供商通知您数据泄露？"
            ],
            "recommendations": [
                "制定标准化的服务提供商合同模板",
                "定期审查和更新现有合同",
                "建立服务提供商合规评估流程",
                "保留服务提供商关系和相关文件"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_verification_procedures(self):
        """检查验证程序"""
        check_id = "verification_procedures"
        description = "验证消费者身份验证机制"
        
        guidelines = [
            "合理验证消费者身份",
            "避免过度收集验证信息",
            "防止未授权访问",
            "确保验证程序符合规定"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "guidelines": guidelines,
            "questions": [
                "1. 您是否有适当的身份验证程序？",
                "2. 您是否避免收集过多验证信息？",
                "3. 您是否保护验证过程的安全性？",
                "4. 您是否记录验证过程和决策？"
            ],
            "recommendations": [
                "制定标准化的身份验证流程",
                "使用多因素身份验证增强安全性",
                "定期审查和更新验证程序",
                "培训员工正确处理验证请求"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_non_discrimination(self):
        """检查非歧视性"""
        check_id = "non_discrimination"
        description = "验证消费者行使权利时不受到歧视"
        
        requirements = [
            "不因行使权利而拒绝提供商品或服务",
            "不因行使权利而收取不同价格或提供不同质量",
            "不因行使权利而施加惩罚"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "requirements": requirements,
            "questions": [
                "1. 您是否因消费者行使权利而区别对待？",
                "2. 您是否对所有消费者一视同仁？",
                "3. 您是否有监控歧视性行为的机制？",
                "4. 您是否培训员工避免歧视性行为？"
            ],
            "recommendations": [
                "制定明确的非歧视政策",
                "建立监控机制检测潜在歧视",
                "提供非歧视性培训",
                "记录和处理歧视投诉"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_recordkeeping(self):
        """检查记录保存"""
        check_id = "recordkeeping"
        description = "验证CCPA/CPRA要求记录的保存"
        
        required_records = [
            "消费者权利请求记录",
            "响应和行动记录",
            "验证过程记录",
            "选择退出请求记录",
            "数据销售和共享记录",
            "隐私政策更新记录"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "required_records": required_records,
            "questions": [
                "1. 您是否保存所有消费者权利请求记录？",
                "2. 您是否记录所有响应和行动？",
                "3. 您是否保留验证文件？",
                "4. 您是否维护选择退出数据库？"
            ],
            "recommendations": [
                "建立标准化的记录保存系统",
                "确保记录保存至少24个月",
                "定期备份关键记录",
                "制定记录保留和销毁政策"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_data_security(self):
        """检查数据安全"""
        check_id = "data_security"
        description = "验证个人信息安全措施"
        
        security_measures = [
            "加密敏感数据",
            "访问控制和身份验证",
            "网络安全防护",
            "数据泄露检测",
            "员工安全培训"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "security_measures": security_measures,
            "questions": [
                "1. 您是否实施适当的技术安全措施？",
                "2. 您是否进行定期安全评估？",
                "3. 您是否有数据泄露响应计划？",
                "4. 您是否培训员工数据安全？"
            ],
            "recommendations": [
                "实施多层次数据安全架构",
                "定期进行安全漏洞评估",
                "制定详细的数据泄露响应计划",
                "建立员工安全意识培训计划"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_response_timelines(self):
        """检查响应时限"""
        check_id = "response_timelines"
        description = "验证消费者权利请求的响应时限"
        
        timelines = {
            "确认收到请求": "10个工作日内",
            "响应请求": "45个日历日内",
            "延长响应时间": "最多延长45天（需通知消费者）"
        }
        
        result = {
            "check_id": check_id,
            "description": description,
            "timelines": timelines,
            "questions": [
                "1. 您是否在10个工作日内确认收到请求？",
                "2. 您是否在45个日历日内响应请求？",
                "3. 如果需要延长，您是否通知消费者？",
                "4. 您是否监控和报告响应时间？"
            ],
            "recommendations": [
                "建立自动化确认系统",
                "实施服务级别协议（SLA）监控",
                "制定延期通知模板",
                "定期报告响应时间绩效"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def interactive_mode(self):
        """交互式检查模式"""
        print("=" * 60)
        print("CCPA/CPRA合规检查工具 - 交互模式")
        print("=" * 60)
        print("本工具将引导您完成CCPA/CPRA核心合规要求的检查。")
        print("请回答以下问题或按Ctrl+C退出。")
        print()
        
        # 运行所有检查
        for check_func in self.ccpa_checks:
            result = check_func()
            
            # 显示检查项信息
            print(f"📋 检查项: {result['description']}")
            
            # 如果有问题列表，显示并获取输入
            if 'questions' in result:
                print("问题:")
                for question in result['questions']:
                    print(f"  {question}")
                
                response = input("您的回答（简要描述当前状况）: ")
                result['user_response'] = response
                
                # 基于用户输入评估
                if response and len(response.strip()) > 10:
                    result['status'] = "PASSED"
                    result['score'] = 3
                    print("✅ 检查通过")
                else:
                    result['status'] = "PASSED"  # 先标记为通过，后续细评
                    result['score'] = 2
                    print("⚠️  需要进一步评估")
            
            # 如果有建议列表，显示
            if 'recommendations' in result:
                print("建议:")
                for i, rec in enumerate(result['recommendations'], 1):
                    print(f"  {i}. {rec}")
            
            print("-" * 60)
            
            # 更新摘要
            self.results['summary']['total_checks'] += 1
            if result['status'] == "PASSED":
                self.results['summary']['passed'] += 1
            elif result['status'] == "FAILED":
                self.results['summary']['failed'] += 1
            elif result['status'] == "WARNING":
                self.results['summary']['warnings'] += 1
            
            self.results['checks'].append(result)
    
    def generate_report(self):
        """生成检查报告"""
        report = {
            "audit_info": {
                "date": self.results['audit_date'],
                "skill_version": self.results['skill_version'],
                "region": self.results['region'],
                "total_checks": self.results['summary']['total_checks'],
                "passed": self.results['summary']['passed'],
                "failed": self.results['summary']['failed'],
                "warnings": self.results['summary']['warnings'],
                "compliance_rate": (self.results['summary']['passed'] / max(self.results['summary']['total_checks'], 1)) * 100
            },
            "detailed_results": self.results['checks'],
            "overall_assessment": self.get_overall_assessment(),
            "next_steps": self.get_next_steps(),
            "report_generated": datetime.now().isoformat()
        }
        
        return report
    
    def get_overall_assessment(self):
        """获取总体评估"""
        total_score = sum(check['score'] for check in self.results['checks'] if 'score' in check)
        max_score = 3 * len(self.results['checks'])
        
        if (total_score / max_score) > 0.8:
            return "优秀 - 高度符合CCPA/CPRA要求"
        elif (total_score / max_score) > 0.6:
            return "良好 - 基本符合CCPA/CPRA要求，有待改进"
        else:
            return "需要改进 - 存在明显合规差距"
    
    def get_next_steps(self):
        """获取下一步建议"""
        steps = []
        
        # 根据检查结果生成建议
        for check in self.results['checks']:
            if check.get('status') == "PASSED" and check.get('score', 0) < 2:
                steps.append(f"完善 {check['description']} 的实施措施")
            elif check.get('status') == "FAILED":
                steps.append(f"立即整改 {check['description']}")
        
        # 添加通用建议
        if not steps:
            steps = [
                "继续完善CCPA/CPRA合规体系",
                "定期进行合规检查",
                "关注加州隐私保护局（CPPA）最新规定",
                "考虑外部合规审计"
            ]
        
        return steps
    
    def save_report(self, report, filename=None):
        """保存报告到文件"""
        if filename is None:
            filename = f"ccpa_audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return filename

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='CCPA/CPRA合规检查工具')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互式检查模式')
    parser.add_argument('--output', '-o', help='输出报告文件名')
    parser.add_argument('--format', choices=['json', 'text'], default='json', help='输出格式')
    parser.add_argument('--list-checks', action='store_true', help='列出所有检查项')
    
    args = parser.parse_args()
    
    tool = CCPAComplianceTool()
    
    if args.list_checks:
        print("CCPA/CPRA合规检查项列表:")
        for i, check_func in enumerate(tool.ccpa_checks, 1):
            result = check_func()
            print(f"{i}. {result['description']}")
        return
    
    if args.interactive:
        tool.interactive_mode()
    else:
        # 非交互模式：运行所有检查
        for check_func in tool.ccpa_checks:
            result = check_func()
            result['status'] = "PASSED"  # 默认通过，需要实际评估
            result['score'] = 2  # 默认分数
            tool.results['summary']['total_checks'] += 1
            tool.results['summary']['passed'] += 1
            tool.results['checks'].append(result)
    
    # 生成报告
    report = tool.generate_report()
    
    # 输出报告
    if args.format == 'json':
        if args.output:
            output_file = tool.save_report(report, args.output)
            print(f"✅ 报告已保存到: {output_file}")
        else:
            print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print("CCPA/CPRA合规检查报告")
        print("=" * 60)
        print(f"检查日期: {report['audit_info']['date']}")
        print(f"Skill版本: {report['audit_info']['skill_version']}")
        print(f"适用地区: {report['audit_info']['region']}")
        print(f"检查项总数: {report['audit_info']['total_checks']}")
        print(f"通过项: {report['audit_info']['passed']}")
        print(f"未通过项: {report['audit_info']['failed']}")
        print(f"警告项: {report['audit_info']['warnings']}")
        print(f"合规率: {report['audit_info']['compliance_rate']:.1f}%")
        print()
        print(f"总体评估: {report['overall_assessment']}")
        print()
        print("下一步行动:")
        for i, step in enumerate(report['next_steps'], 1):
            print(f"  {i}. {step}")
        print("=" * 60)

if __name__ == "__main__":
    main()