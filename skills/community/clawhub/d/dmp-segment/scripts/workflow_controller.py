#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
明日DMP人群圈选工作流程控制器

功能：
1. 定义工作流程的8个步骤及其执行要求
2. 跟踪每个步骤的执行状态
3. 验证流程完整性
4. 生成执行报告

使用方式：
    from workflow_controller import WorkflowController
    
    controller = WorkflowController()
    controller.mark_step_completed(1, "已识别为创建人群请求")
    controller.mark_step_completed(2, "凭证检查通过")
    # ...
    controller.validate_workflow()
"""

import json
from typing import Dict, List, Optional
from datetime import datetime


class WorkflowStep:
    """工作流程步骤定义"""
    
    def __init__(self, step_id: int, name: str, requirement: str, description: str):
        self.step_id = step_id
        self.name = name
        self.requirement = requirement  # "必须执行", "必须检查", "可选"
        self.description = description
        self.status = "未执行"  # 未执行, 已完成, 已跳过, 失败
        self.notes = ""
        self.timestamp = None
    
    def mark_completed(self, notes: str = ""):
        """标记步骤为已完成"""
        self.status = "已完成"
        self.notes = notes
        self.timestamp = datetime.now().isoformat()
    
    def mark_skipped(self, notes: str = ""):
        """标记步骤为已跳过"""
        self.status = "已跳过"
        self.notes = notes
        self.timestamp = datetime.now().isoformat()
    
    def mark_failed(self, notes: str = ""):
        """标记步骤为失败"""
        self.status = "失败"
        self.notes = notes
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "step_id": self.step_id,
            "name": self.name,
            "requirement": self.requirement,
            "description": self.description,
            "status": self.status,
            "notes": self.notes,
            "timestamp": self.timestamp
        }


class WorkflowController:
    """工作流程控制器"""
    
    def __init__(self):
        self.steps: Dict[int, WorkflowStep] = {}
        self._initialize_steps()
    
    def _initialize_steps(self):
        """初始化工作流程步骤"""
        steps_definition = [
            (1, "请求类型识别", "必须执行", "识别用户请求类型(咨询/查询/创建)"),
            (2, "凭证检查", "必须执行", "检查API凭证是否存在,不存在则引导配置"),
            (3, "圈选方式确认", "必须执行", "向用户展示识别的圈选方式并等待确认"),
            (4, "参数补充", "必须执行", "收集所有必填参数并进行格式校验"),
            (5, "参数确认", "必须执行", "以表格形式展示所有参数并等待用户确认"),
            (6, "执行创建", "必须执行", "调用API创建人群任务"),
            (7, "任务记录", "必须检查", "检查skill-logger是否安装,询问用户是否需要下载"),
            (8, "结果展示", "必须执行", "展示任务ID、预计完成时间和后续操作建议")
        ]
        
        for step_id, name, requirement, description in steps_definition:
            self.steps[step_id] = WorkflowStep(step_id, name, requirement, description)
    
    def mark_step_completed(self, step_id: int, notes: str = ""):
        """标记步骤为已完成"""
        if step_id in self.steps:
            self.steps[step_id].mark_completed(notes)
        else:
            raise ValueError(f"无效的步骤ID: {step_id}")
    
    def mark_step_skipped(self, step_id: int, notes: str = ""):
        """标记步骤为已跳过"""
        if step_id in self.steps:
            self.steps[step_id].mark_skipped(notes)
        else:
            raise ValueError(f"无效的步骤ID: {step_id}")
    
    def mark_step_failed(self, step_id: int, notes: str = ""):
        """标记步骤为失败"""
        if step_id in self.steps:
            self.steps[step_id].mark_failed(notes)
        else:
            raise ValueError(f"无效的步骤ID: {step_id}")
    
    def get_step_status(self, step_id: int) -> str:
        """获取步骤状态"""
        if step_id in self.steps:
            return self.steps[step_id].status
        else:
            raise ValueError(f"无效的步骤ID: {step_id}")
    
    def validate_workflow(self) -> tuple[bool, List[str]]:
        """
        验证工作流程完整性
        
        返回:
            (is_valid, errors): 是否有效, 错误列表
        """
        errors = []
        
        for step_id, step in self.steps.items():
            # 检查"必须执行"步骤
            if step.requirement == "必须执行":
                if step.status not in ["已完成"]:
                    errors.append(f"第{step_id}步({step.name})标记为[必须执行],但状态为'{step.status}'")
            
            # 检查"必须检查"步骤
            elif step.requirement == "必须检查":
                if step.status not in ["已完成", "已跳过"]:
                    errors.append(f"第{step_id}步({step.name})标记为[必须检查],但状态为'{step.status}'")
                elif step.status == "未执行":
                    errors.append(f"第{step_id}步({step.name})标记为[必须检查],必须执行检查逻辑(即使用户选择跳过)")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def generate_report(self) -> str:
        """生成执行报告"""
        report_lines = ["=" * 60]
        report_lines.append("明日DMP人群圈选工作流程执行报告")
        report_lines.append("=" * 60)
        report_lines.append("")
        
        for step_id in sorted(self.steps.keys()):
            step = self.steps[step_id]
            status_icon = {
                "已完成": "✅",
                "已跳过": "⏭️",
                "失败": "❌",
                "未执行": "⚠️"
            }.get(step.status, "❓")
            
            report_lines.append(f"{status_icon} 第{step_id}步: {step.name} [{step.requirement}]")
            report_lines.append(f"   状态: {step.status}")
            if step.notes:
                report_lines.append(f"   说明: {step.notes}")
            if step.timestamp:
                report_lines.append(f"   时间: {step.timestamp}")
            report_lines.append("")
        
        # 验证结果
        is_valid, errors = self.validate_workflow()
        report_lines.append("-" * 60)
        if is_valid:
            report_lines.append("✅ 流程完整性验证: 通过")
        else:
            report_lines.append("❌ 流程完整性验证: 失败")
            report_lines.append("")
            report_lines.append("发现以下问题:")
            for error in errors:
                report_lines.append(f"  - {error}")
        
        report_lines.append("=" * 60)
        
        return "\n".join(report_lines)
    
    def export_to_json(self, filepath: str):
        """导出执行记录为JSON文件"""
        data = {
            "workflow_name": "明日DMP人群圈选",
            "export_time": datetime.now().isoformat(),
            "steps": [step.to_dict() for step in self.steps.values()],
            "validation": {
                "is_valid": self.validate_workflow()[0],
                "errors": self.validate_workflow()[1]
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_from_json(self, filepath: str):
        """从JSON文件加载执行记录"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for step_data in data.get("steps", []):
            step_id = step_data["step_id"]
            if step_id in self.steps:
                step = self.steps[step_id]
                step.status = step_data.get("status", "未执行")
                step.notes = step_data.get("notes", "")
                step.timestamp = step_data.get("timestamp")


# 使用示例
if __name__ == "__main__":
    # 创建控制器
    controller = WorkflowController()
    
    # 模拟执行流程
    controller.mark_step_completed(1, "已识别为创建组合人群请求")
    controller.mark_step_completed(2, "凭证检查通过")
    controller.mark_step_completed(3, "用户确认创建组合人群")
    controller.mark_step_completed(4, "已收集人群名称、平台类型、标签等参数")
    controller.mark_step_completed(5, "用户确认参数无误")
    controller.mark_step_completed(6, "API调用成功,任务ID: 133717")
    # 注意: 第7步被跳过了!
    controller.mark_step_completed(8, "已展示任务ID和后续操作建议")
    
    # 生成报告
    print(controller.generate_report())
    
    # 导出JSON
    controller.export_to_json("workflow_execution.json")
    print("\n执行记录已导出到 workflow_execution.json")
