#!/usr/bin/env python3
"""
深度思考协议 - 思考检查清单脚本

这个脚本提供了一个交互式的检查清单，帮助在思考过程中确保覆盖所有关键步骤。
"""

import sys
import json
from datetime import datetime

class ThinkingChecklist:
    def __init__(self):
        self.checklist = {
            "phase1_initial_contact": {
                "name": "阶段1: 初始接触",
                "items": [
                    "用自己的话重述问题",
                    "形成初步印象",
                    "考虑问题背景",
                    "映射已知和未知元素",
                    "思考提问者意图",
                    "识别与现有知识的联系",
                    "识别潜在歧义"
                ],
                "completed": []
            },
            "phase2_problem_exploration": {
                "name": "阶段2: 问题空间探索",
                "items": [
                    "拆解问题核心组件",
                    "识别显性和隐性需求",
                    "考虑约束和限制",
                    "定义成功响应的样子",
                    "规划所需知识范围"
                ],
                "completed": []
            },
            "phase3_hypothesis_generation": {
                "name": "阶段3: 多重假设生成",
                "items": [
                    "写下多种可能的解释",
                    "考虑各种解决方案途径",
                    "思考替代视角",
                    "保持多个工作假设",
                    "避免过早承诺单一解释"
                ],
                "completed": []
            },
            "phase4_discovery_process": {
                "name": "阶段4: 自然发现过程",
                "items": [
                    "从明显方面开始",
                    "注意模式和连接",
                    "质疑初步假设",
                    "建立新的连接",
                    "回溯早期想法",
                    "逐步建立深层洞察"
                ],
                "completed": []
            },
            "phase5_testing_verification": {
                "name": "阶段5: 测试与验证",
                "items": [
                    "质疑自身假设",
                    "测试初步结论",
                    "寻找潜在缺陷",
                    "考虑替代视角",
                    "验证推理一致性",
                    "检查理解完整性"
                ],
                "completed": []
            },
            "phase6_error_correction": {
                "name": "阶段6: 错误识别与修正",
                "items": [
                    "承认思维中的错误",
                    "解释之前思考的问题",
                    "展示新理解发展",
                    "融入修正后的理解"
                ],
                "completed": []
            },
            "phase7_knowledge_synthesis": {
                "name": "阶段7: 知识综合",
                "items": [
                    "连接不同信息片段",
                    "展示各方面关联",
                    "构建连贯整体图景",
                    "识别关键原则模式",
                    "注意重要含义后果"
                ],
                "completed": []
            },
            "phase8_pattern_recognition": {
                "name": "阶段8: 模式识别与分析",
                "items": [
                    "主动寻找信息模式",
                    "比较已知示例",
                    "测试模式一致性",
                    "考虑例外情况",
                    "利用模式指导调查"
                ],
                "completed": []
            },
            "phase9_progress_tracking": {
                "name": "阶段9: 进度追踪",
                "items": [
                    "明确已确立内容",
                    "明确尚待确定内容",
                    "评估结论置信度",
                    "识别开放性问题",
                    "评估理解进展"
                ],
                "completed": []
            },
            "phase10_recursive_thinking": {
                "name": "阶段10: 递归思考",
                "items": [
                    "应用多尺度分析",
                    "多尺度模式识别",
                    "保持方法一致性",
                    "展示分析支持"
                ],
                "completed": []
            }
        }
        
        self.problem_context = {
            "problem_description": "",
            "problem_type": "",
            "stakeholders": [],
            "constraints": [],
            "success_criteria": []
        }
        
    def start_new_session(self):
        """开始新的思考会话"""
        print("=" * 60)
        print("深度思考协议 - 思考检查清单")
        print("=" * 60)
        print()
        
        # 收集问题信息
        self.problem_context["problem_description"] = input("请描述要思考的问题: ")
        self.problem_context["problem_type"] = input("问题类型 (技术/战略/创意/决策/其他): ")
        
        print("\n请列出利益相关者 (每行一个，空行结束):")
        while True:
            stakeholder = input("> ")
            if not stakeholder:
                break
            self.problem_context["stakeholders"].append(stakeholder)
            
        print("\n请列出约束条件 (每行一个，空行结束):")
        while True:
            constraint = input("> ")
            if not constraint:
                break
            self.problem_context["constraints"].append(constraint)
            
        print("\n请列出成功标准 (每行一个，空行结束):")
        while True:
            criterion = input("> ")
            if not criterion:
                break
            self.problem_context["success_criteria"].append(criterion)
            
        print("\n" + "=" * 60)
        print("问题上下文已记录")
        print("=" * 60)
        
    def run_checklist(self):
        """运行检查清单"""
        print("\n开始思考过程检查...\n")
        
        for phase_key, phase_data in self.checklist.items():
            print(f"\n{phase_data['name']}")
            print("-" * 40)
            
            for i, item in enumerate(phase_data["items"], 1):
                response = input(f"{i}. {item} (y/n/备注): ")
                if response.lower() == 'y':
                    phase_data["completed"].append(item)
                elif response.lower().startswith('备注'):
                    note = response[2:].strip()
                    phase_data["completed"].append(f"{item} [备注: {note}]")
                    
            # 可选添加额外笔记
            add_notes = input("\n为此阶段添加额外笔记? (y/n): ")
            if add_notes.lower() == 'y':
                notes = input("笔记: ")
                phase_data["notes"] = notes
                
    def generate_report(self):
        """生成思考报告"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "problem_context": self.problem_context,
            "thinking_process": {},
            "summary": {
                "total_phases": len(self.checklist),
                "completed_items": 0,
                "total_items": 0,
                "completion_rate": 0
            }
        }
        
        total_items = 0
        completed_items = 0
        
        for phase_key, phase_data in self.checklist.items():
            report["thinking_process"][phase_key] = {
                "name": phase_data["name"],
                "items": phase_data["items"],
                "completed": phase_data["completed"],
                "completion_count": len(phase_data["completed"]),
                "total_items": len(phase_data["items"])
            }
            
            total_items += len(phase_data["items"])
            completed_items += len(phase_data["completed"])
            
        report["summary"]["total_items"] = total_items
        report["summary"]["completed_items"] = completed_items
        report["summary"]["completion_rate"] = round(completed_items / total_items * 100, 2) if total_items > 0 else 0
        
        return report
    
    def display_report(self, report):
        """显示报告"""
        print("\n" + "=" * 60)
        print("深度思考协议 - 思考报告")
        print("=" * 60)
        
        print(f"\n问题描述: {report['problem_context']['problem_description']}")
        print(f"问题类型: {report['problem_context']['problem_type']}")
        
        print(f"\n完成率: {report['summary']['completion_rate']}%")
        print(f"完成项目: {report['summary']['completed_items']}/{report['summary']['total_items']}")
        
        print("\n各阶段完成情况:")
        print("-" * 40)
        
        for phase_key, phase_data in report["thinking_process"].items():
            completion = phase_data["completion_count"]
            total = phase_data["total_items"]
            rate = round(completion / total * 100, 2) if total > 0 else 0
            
            print(f"{phase_data['name']}: {completion}/{total} ({rate}%)")
            
            # 显示未完成的项目
            completed_set = set(phase_data["completed"])
            all_items = set(phase_data["items"])
            incomplete = all_items - completed_set
            
            if incomplete:
                print("  未完成:")
                for item in incomplete:
                    print(f"    - {item}")
                    
        print("\n关键洞察和建议:")
        print("-" * 40)
        
        # 基于完成情况提供建议
        if report["summary"]["completion_rate"] < 50:
            print("⚠️  思考过程不够完整，建议:")
            print("  - 重新审视未完成的思考步骤")
            print("  - 确保考虑了多个角度和假设")
            print("  - 加强验证和测试环节")
        elif report["summary"]["completion_rate"] < 80:
            print("✅ 思考过程基本完整，建议:")
            print("  - 补充完善未完成的项目")
            print("  - 加强知识综合和模式识别")
            print("  - 进行最终的质量检查")
        else:
            print("🎉 思考过程非常完整!")
            print("  - 已全面覆盖思考框架")
            print("  - 可以进行最终输出")
            print("  - 建议进行最后的逻辑验证")
            
    def save_report(self, report, filename=None):
        """保存报告到文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"thinking_report_{timestamp}.json"
            
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        print(f"\n报告已保存到: {filename}")
        
    def load_template(self, template_type):
        """加载思考模板"""
        templates = {
            "technical": {
                "focus_areas": ["逻辑严谨性", "技术可行性", "边缘案例", "性能考虑"],
                "recommended_tools": ["代码分析", "系统设计", "性能测试"],
                "output_format": ["具体方案", "实施步骤", "风险提示"]
            },
            "strategic": {
                "focus_areas": ["多角度分析", "长期影响", "资源分配", "风险评估"],
                "recommended_tools": ["SWOT分析", "成本效益分析", "情景规划"],
                "output_format": ["战略建议", "实施路径", "监控指标"]
            },
            "creative": {
                "focus_areas": ["发散思维", "创新性", "可行性平衡", "约束分析"],
                "recommended_tools": ["头脑风暴", "类比思考", "原型设计"],
                "output_format": ["创意方案", "实施建议", "评估标准"]
            },
            "decision": {
                "focus_areas": ["选项分析", "标准明确", "风险评估", "数据驱动"],
                "recommended_tools": ["决策矩阵", "利弊分析", "敏感性分析"],
                "output_format": ["明确建议", "实施步骤", "备用方案"]
            }
        }
        
        if template_type in templates:
            return templates[template_type]
        else:
            return templates.get("technical")  # 默认技术模板

def main():
    """主函数"""
    checklist = ThinkingChecklist()
    
    print("深度思考协议检查清单工具")
    print("=" * 40)
    
    # 开始新会话
    checklist.start_new_session()
    
    # 根据问题类型加载模板
    problem_type = checklist.problem_context["problem_type"]
    template = checklist.load_template(problem_type.lower())
    
    print(f"\n根据问题类型 '{problem_type}'，建议:")
    print(f"重点领域: {', '.join(template['focus_areas'])}")
    print(f"推荐工具: {', '.join(template['recommended_tools'])}")
    print(f"输出格式: {', '.join(template['output_format'])}")
    
    # 运行检查清单
    input("\n按Enter键开始思考过程检查...")
    checklist.run_checklist()
    
    # 生成和显示报告
    report = checklist.generate_report()
    checklist.display_report(report)
    
    # 保存报告
    save_option = input("\n是否保存报告? (y/n): ")
    if save_option.lower() == 'y':
        filename = input("文件名 (直接回车使用默认): ")
        if filename:
            checklist.save_report(report, filename)
        else:
            checklist.save_report(report)
            
    print("\n思考过程完成! 现在可以基于此思考生成最终回复。")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)