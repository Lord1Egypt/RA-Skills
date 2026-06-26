#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业AI应用诊断工具 - 主程序
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class EnterpriseAIDiagnosis:
    """企业AI应用诊断工具"""
    
    def __init__(self):
        """初始化"""
        self.workspace = os.path.expanduser('~/.openclaw/workspace')
        self.output_dir = os.path.join(self.workspace, 'ai_diagnosis_reports')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def collect_enterprise_info(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """
        收集企业信息
        
        Args:
            info: 企业信息字典
            
        Returns:
            整理后的企业信息
        """
        return {
            'basic_info': {
                'company_name': info.get('company_name', '未提供'),
                'industry': info.get('industry', '未提供'),
                'scale': info.get('scale', '未提供'),
                'employees': info.get('employees', 0),
                'annual_revenue': info.get('annual_revenue', 0),
            },
            'current_status': {
                'tech_level': info.get('tech_level', '中等'),
                'ai_usage': info.get('ai_usage', []),
                'pain_points': info.get('pain_points', []),
            },
            'expectations': {
                'goals': info.get('goals', []),
                'budget': info.get('budget', 0),
                'timeline': info.get('timeline', '3个月'),
            }
        }
    
    def analyze_business_processes(self, processes: List[Dict]) -> Dict[str, Any]:
        """
        分析业务流程的AI适用性
        
        Args:
            processes: 业务流程列表
            
        Returns:
            分析结果
        """
        results = {}
        
        for process in processes:
            name = process.get('name', '未命名流程')
            time_cost = process.get('time_cost', 0)
            labor_cost = process.get('labor_cost', 0)
            pain_level = process.get('pain_level', '中等')
            
            # AI适用性评分（0-100）
            score = self._calculate_ai_score(process)
            
            # 推荐的AI应用场景
            ai_scenarios = self._recommend_ai_scenarios(name, process)
            
            # 预估收益
            estimated_savings = self._estimate_savings(time_cost, labor_cost, score)
            
            results[name] = {
                'ai_score': score,
                'time_cost': time_cost,
                'labor_cost': labor_cost,
                'pain_level': pain_level,
                'ai_scenarios': ai_scenarios,
                'estimated_savings': estimated_savings,
                'implementation_difficulty': self._assess_difficulty(score, process),
            }
        
        return results
    
    def _calculate_ai_score(self, process: Dict) -> int:
        """
        计算AI适用性评分
        
        Args:
            process: 流程信息
            
        Returns:
            评分（0-100）
        """
        score = 50  # 基础分
        
        # 根据流程特点调整分数
        if process.get('repetitive', False):
            score += 20  # 重复性工作适合AI
        
        if process.get('data_driven', False):
            score += 15  # 数据驱动适合AI
        
        if process.get('customer_facing', False):
            score += 10  # 客户接触适合AI
        
        if process.get('creative', False):
            score -= 10  # 创意工作AI适用性稍低
        
        # 根据痛点级别调整
        pain_level = process.get('pain_level', '中等')
        if pain_level == '高':
            score += 10
        elif pain_level == '低':
            score -= 10
        
        return min(max(score, 0), 100)  # 限制在0-100
    
    def _recommend_ai_scenarios(self, process_name: str, process: Dict) -> List[Dict]:
        """
        推荐AI应用场景
        
        Args:
            process_name: 流程名称
            process: 流程信息
            
        Returns:
            AI场景列表
        """
        scenarios = []
        
        # 根据流程名称推荐场景
        if '客服' in process_name or '售后' in process_name:
            scenarios = [
                {'name': '智能客服机器人', 'savings': '80%人力', 'difficulty': '中等'},
                {'name': '自动回复系统', 'savings': '90%响应时间', 'difficulty': '低'},
                {'name': '客户情绪分析', 'savings': '30%投诉率', 'difficulty': '高'},
            ]
        elif '销售' in process_name or '营销' in process_name:
            scenarios = [
                {'name': 'AI内容生成', 'savings': '70%内容创作时间', 'difficulty': '低'},
                {'name': '客户画像分析', 'savings': '50%营销精准度', 'difficulty': '中等'},
                {'name': '销售话术优化', 'savings': '30%转化率', 'difficulty': '低'},
            ]
        elif '财务' in process_name or '会计' in process_name:
            scenarios = [
                {'name': '发票自动识别', 'savings': '60%录入时间', 'difficulty': '低'},
                {'name': '财务报表生成', 'savings': '50%报表时间', 'difficulty': '低'},
                {'name': '风险预警', 'savings': '40%风险损失', 'difficulty': '高'},
            ]
        elif '人力' in process_name or 'HR' in process_name:
            scenarios = [
                {'name': '简历筛选', 'savings': '70%筛选时间', 'difficulty': '低'},
                {'name': '员工培训', 'savings': '40%培训成本', 'difficulty': '中等'},
                {'name': '绩效分析', 'savings': '50%评估时间', 'difficulty': '中等'},
            ]
        else:
            scenarios = [
                {'name': '流程自动化', 'savings': '30-50%时间', 'difficulty': '中等'},
                {'name': '数据分析', 'savings': '40%分析时间', 'difficulty': '低'},
            ]
        
        return scenarios
    
    def _estimate_savings(self, time_cost: float, labor_cost: float, ai_score: int) -> Dict:
        """
        预估收益
        
        Args:
            time_cost: 时间成本（小时/月）
            labor_cost: 人力成本（元/月）
            ai_score: AI适用性评分
            
        Returns:
            预估收益
        """
        # 基于AI评分计算节省比例
        savings_ratio = ai_score / 100 * 0.7  # 最高70%节省
        
        time_savings = time_cost * savings_ratio
        labor_savings = labor_cost * savings_ratio
        
        return {
            'time_savings_hours': round(time_savings, 1),
            'labor_savings_yuan': round(labor_savings, 2),
            'savings_ratio': f'{int(savings_ratio * 100)}%',
        }
    
    def _assess_difficulty(self, ai_score: int, process: Dict) -> str:
        """
        评估实施难度
        
        Args:
            ai_score: AI评分
            process: 流程信息
            
        Returns:
            难度等级（低/中等/高）
        """
        if ai_score >= 80:
            return '低'
        elif ai_score >= 60:
            return '中等'
        else:
            return '高'
    
    def calculate_roi(self, 
                     investment: Dict[str, float],
                     savings: Dict[str, float],
                     timeline_months: int = 12) -> Dict[str, Any]:
        """
        计算ROI
        
        Args:
            investment: 投入成本
                - tools: 工具费用（元/年）
                - training: 培训成本（元）
                - time: 时间成本（元）
            savings: 节省收益
                - labor: 人力节省（元/年）
                - efficiency: 效率提升价值（元/年）
                - error_reduction: 错误减少价值（元/年）
            timeline_months: 时间周期（月）
            
        Returns:
            ROI分析结果
        """
        # 总投入
        total_investment = (
            investment.get('tools', 0) +
            investment.get('training', 0) +
            investment.get('time', 0)
        )
        
        # 年化收益
        annual_savings = (
            savings.get('labor', 0) +
            savings.get('efficiency', 0) +
            savings.get('error_reduction', 0)
        )
        
        # 月均收益
        monthly_savings = annual_savings / 12
        
        # 计算周期内的收益
        period_savings = monthly_savings * timeline_months
        
        # ROI计算
        if total_investment > 0:
            roi = ((period_savings - total_investment) / total_investment) * 100
        else:
            roi = 0
        
        # 回报周期（月）
        if monthly_savings > 0:
            payback_months = total_investment / monthly_savings
        else:
            payback_months = float('inf')
        
        return {
            'total_investment': round(total_investment, 2),
            'annual_savings': round(annual_savings, 2),
            'monthly_savings': round(monthly_savings, 2),
            'period_savings': round(period_savings, 2),
            'roi_percentage': round(roi, 2),
            'payback_months': round(payback_months, 1),
            'timeline_months': timeline_months,
        }
    
    def generate_implementation_plan(self, 
                                    processes: Dict,
                                    budget: float) -> Dict[str, Any]:
        """
        生成实施计划
        
        Args:
            processes: 流程分析结果
            budget: 预算
            
        Returns:
            实施计划
        """
        # 按AI评分排序
        sorted_processes = sorted(
            processes.items(),
            key=lambda x: x[1]['ai_score'],
            reverse=True
        )
        
        plan = {
            'phase1': {
                'timeline': '1-2周',
                'goal': '快速见效，建立信心',
                'processes': [],
                'tools': [],
                'expected_result': '立即可见的效果',
            },
            'phase2': {
                'timeline': '1个月',
                'goal': '深度应用，扩大范围',
                'processes': [],
                'tools': [],
                'expected_result': '效率提升30%',
            },
            'phase3': {
                'timeline': '3个月',
                'goal': '全面融合，持续优化',
                'processes': [],
                'tools': [],
                'expected_result': '效率提升100%',
            },
        }
        
        # 分配流程到各阶段
        for i, (name, data) in enumerate(sorted_processes):
            if i < 2:
                plan['phase1']['processes'].append(name)
            elif i < 5:
                plan['phase2']['processes'].append(name)
            else:
                plan['phase3']['processes'].append(name)
        
        # 工具推荐
        if budget < 1000:
            plan['phase1']['tools'] = ['ChatGPT免费版', 'Canva', '剪映']
            plan['phase2']['tools'] = ['ChatGPT Plus', 'OpenClaw基础版']
        elif budget < 10000:
            plan['phase1']['tools'] = ['ChatGPT Plus', 'OpenClaw', 'Notion AI']
            plan['phase2']['tools'] = ['Midjourney', '企业版工具']
        else:
            plan['phase1']['tools'] = ['企业版ChatGPT', 'OpenClaw专业版', '定制工具']
        
        return plan
    
    def generate_report(self,
                       enterprise_info: Dict,
                       process_analysis: Dict,
                       roi_analysis: Dict,
                       implementation_plan: Dict) -> str:
        """
        生成诊断报告
        
        Args:
            enterprise_info: 企业信息
            process_analysis: 流程分析
            roi_analysis: ROI分析
            implementation_plan: 实施计划
            
        Returns:
            Markdown格式的报告
        """
        report = f"""# 企业AI应用诊断报告

**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 企业概况

- **企业名称**：{enterprise_info['basic_info']['company_name']}
- **所属行业**：{enterprise_info['basic_info']['industry']}
- **企业规模**：{enterprise_info['basic_info']['scale']}
- **员工人数**：{enterprise_info['basic_info']['employees']}人
- **年营收**：{enterprise_info['basic_info']['annual_revenue']}万元

---

## 🎯 AI应用现状

- **当前技术水平**：{enterprise_info['current_status']['tech_level']}
- **已使用的AI工具**：{', '.join(enterprise_info['current_status']['ai_usage']) or '无'}
- **主要痛点**：{', '.join(enterprise_info['current_status']['pain_points'])}

---

## 💡 业务流程AI适用性分析

"""
        
        # 添加每个流程的分析
        for name, data in process_analysis.items():
            report += f"""### {name}

- **AI适用性评分**：{data['ai_score']}/100
- **当前成本**：
  - 时间成本：{data['time_cost']}小时/月
  - 人力成本：{data['labor_cost']}元/月
  - 痛点级别：{data['pain_level']}

**推荐的AI应用场景**：

"""
            for scenario in data['ai_scenarios']:
                report += f"- **{scenario['name']}**\n"
                report += f"  - 预估节省：{scenario['savings']}\n"
                report += f"  - 实施难度：{scenario['difficulty']}\n\n"
            
            report += f"""**预估收益**：
- 时间节省：{data['estimated_savings']['time_savings_hours']}小时/月
- 成本节省：{data['estimated_savings']['labor_savings_yuan']}元/月
- 节省比例：{data['estimated_savings']['savings_ratio']}

**实施难度**：{data['implementation_difficulty']}

---

"""
        
        # ROI分析
        report += f"""## 💰 ROI分析（{roi_analysis['timeline_months']}个月）

### 投入成本

- 工具费用：{roi_analysis['total_investment']}元
- 培训成本：已包含
- 时间成本：已包含

**总投入**：{roi_analysis['total_investment']}元

### 预期收益

- 月均节省：{roi_analysis['monthly_savings']}元
- 周期总收益：{roi_analysis['period_savings']}元
- 年化收益：{roi_analysis['annual_savings']}元

### ROI结果

- **投资回报率**：{roi_analysis['roi_percentage']}%
- **回报周期**：{roi_analysis['payback_months']}个月

---

## 🚀 实施路径规划

### 第1阶段：{implementation_plan['phase1']['timeline']}

**目标**：{implementation_plan['phase1']['goal']}

**优先实施流程**：
"""
        for process in implementation_plan['phase1']['processes']:
            report += f"- {process}\n"
        
        report += f"""
**推荐工具**：
"""
        for tool in implementation_plan['phase1']['tools']:
            report += f"- {tool}\n"
        
        report += f"""
**预期效果**：{implementation_plan['phase1']['expected_result']}

---

### 第2阶段：{implementation_plan['phase2']['timeline']}

**目标**：{implementation_plan['phase2']['goal']}

**扩展流程**：
"""
        for process in implementation_plan['phase2']['processes']:
            report += f"- {process}\n"
        
        report += f"""
**推荐工具**：
"""
        for tool in implementation_plan['phase2']['tools']:
            report += f"- {tool}\n"
        
        report += f"""
**预期效果**：{implementation_plan['phase2']['expected_result']}

---

### 第3阶段：{implementation_plan['phase3']['timeline']}

**目标**：{implementation_plan['phase3']['goal']}

**全面融合流程**：
"""
        for process in implementation_plan['phase3']['processes']:
            report += f"- {process}\n"
        
        report += f"""
**预期效果**：{implementation_plan['phase3']['expected_result']}

---

## ⚠️ 风险提示

1. **数据安全**
   - 使用AI工具时注意数据隐私
   - 敏感数据不要上传到公共AI平台
   - 建议使用企业版工具

2. **员工抵触**
   - 提前沟通AI应用的目的
   - 强调AI是辅助工具而非替代
   - 提供充分的培训

3. **依赖性风险**
   - 不要过度依赖单一AI工具
   - 保持人工备份方案
   - 定期评估AI工具效果

---

## ✅ 执行清单

### 第1周任务

- [ ] 注册ChatGPT账号（1小时）
- [ ] 学习基础提示词（2小时）
- [ ] 配置OpenClaw（3小时）
- [ ] 测试第一个AI场景（5小时）

### 工具配置指南

详见：`references/tool-setup-guide.md`

### 培训材料

- 员工培训PPT：`templates/training.pptx`
- 操作手册：`references/user-manual.md`
- 视频教程：待录制

### 效果追踪

每周记录以下指标：
- AI工具使用时长
- 节省的时间
- 节省的成本
- 遇到的问题

---

## 📞 后续支持

如需进一步咨询或定制方案，请联系：
- 邮箱：87287416@qq.com
- 飞书：@胡大大

---

**报告生成**：企业AI应用诊断工具 v1.0
**小龙虾协助制作** 🦞
"""
        
        return report
    
    def save_report(self, report: str, filename: str = None) -> str:
        """
        保存Markdown报告
        
        Args:
            report: 报告内容
            filename: 文件名（可选）
            
        Returns:
            文件路径
        """
        if filename is None:
            filename = f"ai_diagnosis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return filepath
    
    def save_html_report(self, enterprise_info, process_analysis, roi_analysis, implementation_plan, filename=None):
        """
        保存HTML报告
        
        Args:
            enterprise_info: 企业信息
            process_analysis: 流程分析
            roi_analysis: ROI分析
            implementation_plan: 实施计划
            filename: 文件名（可选）
            
        Returns:
            文件路径
        """
        from html_generator import generate_and_save_html_report
        
        if filename is None:
            company_name = enterprise_info['basic_info']['company_name'].replace(' ', '_').replace('/', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{company_name}_AI诊断报告_{timestamp}.html"
        
        return generate_and_save_html_report(
            enterprise_info, process_analysis, roi_analysis, implementation_plan, self.output_dir
        )


def main():
    """示例使用"""
    # 创建诊断工具实例
    diagnosis = EnterpriseAIDiagnosis()
    
    # 示例：企业信息
    enterprise_info = diagnosis.collect_enterprise_info({
        'company_name': '示例科技有限公司',
        'industry': '互联网',
        'scale': '50-100人',
        'employees': 80,
        'annual_revenue': 1000,
        'tech_level': '中等',
        'ai_usage': ['ChatGPT'],
        'pain_points': ['客服成本高', '内容创作慢'],
        'goals': ['降低成本', '提升效率'],
        'budget': 10000,
        'timeline': '3个月',
    })
    
    # 示例：业务流程
    processes = diagnosis.analyze_business_processes([
        {
            'name': '客服支持',
            'time_cost': 200,
            'labor_cost': 30000,
            'pain_level': '高',
            'repetitive': True,
            'customer_facing': True,
        },
        {
            'name': '内容营销',
            'time_cost': 100,
            'labor_cost': 20000,
            'pain_level': '中等',
            'repetitive': True,
            'creative': True,
        },
    ])
    
    # 示例：ROI计算
    roi = diagnosis.calculate_roi(
        investment={
            'tools': 10000,
            'training': 5000,
            'time': 8000,
        },
        savings={
            'labor': 50000,
            'efficiency': 30000,
            'error_reduction': 10000,
        },
        timeline_months=12
    )
    
    # 示例：实施计划
    plan = diagnosis.generate_implementation_plan(processes, budget=10000)
    
    # 生成报告
    report = diagnosis.generate_report(enterprise_info, processes, roi, plan)
    
    # 保存报告
    filepath = diagnosis.save_report(report)
    
    print(f"✅ 诊断报告已生成：{filepath}")
    print(f"\n报告预览：\n{report[:500]}...")


if __name__ == '__main__':
    main()
