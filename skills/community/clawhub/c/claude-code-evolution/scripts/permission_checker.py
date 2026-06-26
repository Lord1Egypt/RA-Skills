#!/usr/bin/env python3
"""
权限检查脚本（基于Claude Code四层权限模型）

功能：
1. 读取工具分类配置
2. 检查工具权限级别
3. 模拟审批流程
4. 记录审计日志

使用方法：
  python permission_checker.py check --tool read --params "path=MEMORY.md"
  python permission_checker.py simulate --tool exec --command "rm -rf /tmp/test"
  python permission_checker.py audit --days 7
"""

import yaml
import sys
import os
import json
import re
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

# 配置路径
CONFIG_PATH = "memory/tools-classification-config.yaml"
AUDIT_LOG_DIR = "memory/audit-logs/"
import os
# 工作区根目录：优先从环境变量获取，否则使用当前工作目录
WORKSPACE_ROOT = os.environ.get("OPENCLAW_WORKSPACE", os.getcwd())

class PermissionChecker:
    """权限检查器"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.join(WORKSPACE_ROOT, CONFIG_PATH)
        self.audit_log_dir = os.path.join(WORKSPACE_ROOT, AUDIT_LOG_DIR)
        self.config = None
        self.tools_config = None
        self.load_config()
        
        # 确保审计日志目录存在
        os.makedirs(self.audit_log_dir, exist_ok=True)
    
    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            
            # 提取工具配置
            self.tools_config = self.config.get('tools', {})
            
            # 构建权限级别映射
            self.permission_levels = self.config.get('permission_levels', {})
            
        except Exception as e:
            print(f"加载配置文件失败: {str(e)}")
            self.config = {}
            self.tools_config = {}
            self.permission_levels = {}
    
    def get_tool_permission(self, tool_name: str, params: Dict = None) -> Dict:
        """获取工具权限信息"""
        tool_config = self.tools_config.get(tool_name)
        
        if not tool_config:
            # 未知工具，默认视为L2（需要审批）
            return {
                "tool": tool_name,
                "permission": "L2",
                "category": "unknown",
                "risk_level": "medium",
                "description": "未知工具",
                "found": False,
                "default": True
            }
        
        permission = tool_config.get('permission', 'L2')
        
        # 检查权限升级条件
        upgraded_permission = self.check_permission_upgrade(tool_name, permission, params)
        
        return {
            "tool": tool_name,
            "permission": upgraded_permission,
            "category": tool_config.get('category', 'unknown'),
            "risk_level": tool_config.get('risk_level', 'medium'),
            "description": tool_config.get('description', ''),
            "always_available": tool_config.get('always_available', False),
            "defer_loading": tool_config.get('defer_loading', True),
            "require_approval": tool_config.get('require_approval', False),
            "found": True,
            "original_permission": permission,
            "upgraded": upgraded_permission != permission
        }
    
    def check_permission_upgrade(self, tool_name: str, permission: str, params: Dict) -> str:
        """检查是否需要权限升级"""
        if not params:
            return permission
        
        # 处理权限范围（如"L1-L2"）
        current_permission = permission
        if '-' in permission:
            # 取最严格的权限作为基础权限
            permission_levels = permission.split('-')
            # 按数字排序，取数字大的（更严格）
            permission_levels.sort(key=lambda x: int(x[1]) if len(x) > 1 else 0, reverse=True)
            current_permission = permission_levels[0]
        
        # 检查路径敏感升级
        if self.is_path_sensitive(params):
            if current_permission in ['L1', 'L2']:
                current_permission = 'L3'
        
        # 检查危险命令升级
        if tool_name == 'exec' and 'command' in params:
            command = params['command']
            if self.is_dangerous_command(command):
                if current_permission == 'L1':
                    current_permission = 'L2' if self.is_moderately_dangerous(command) else 'L3'
                elif current_permission == 'L2':
                    current_permission = 'L3'
        
        # 检查外部通信升级
        if tool_name == 'message' and 'target' in params:
            target = params['target']
            if self.is_external_target(target):
                if current_permission == 'L1':
                    current_permission = 'L2'
        
        return current_permission
    
    def is_path_sensitive(self, params: Dict) -> bool:
        """检查是否涉及敏感路径"""
        sensitive_paths = ['~/.ssh/', '/etc/', '/root/', '/var/log/', '/usr/bin/']
        
        for key, value in params.items():
            if isinstance(value, str):
                for path in sensitive_paths:
                    if path in value:
                        return True
        return False
    
    def is_dangerous_command(self, command: str) -> bool:
        """检查是否为危险命令"""
        dangerous_patterns = [
            r'rm\s+-rf',
            r'format\s+',
            r'dd\s+',
            r'mkfs\s+',
            r'chmod\s+777',
            r'chown\s+root',
            r'>\s+/dev/',
            r'\|\s*sh\s*$',
            r'\|\s*bash\s*$',
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return True
        return False
    
    def is_moderately_dangerous(self, command: str) -> bool:
        """检查是否为中等危险命令"""
        moderate_patterns = [
            r'rm\s+',
            r'mv\s+',
            r'cp\s+',
            r'sudo\s+',
        ]
        
        for pattern in moderate_patterns:
            if re.search(pattern, command, re.IGNORECASE) and not self.is_dangerous_command(command):
                return True
        return False
    
    def is_external_target(self, target: str) -> bool:
        """检查是否为外部目标"""
        # 这里简化处理，实际应该根据配置判断
        external_indicators = ['@', 'http://', 'https://', 'mailto:', 'slack', 'telegram']
        
        for indicator in external_indicators:
            if indicator in target.lower():
                return True
        return False
    
    def get_approval_required(self, permission_info: Dict) -> bool:
        """检查是否需要审批"""
        permission = permission_info['permission']
        
        if permission == 'L0':
            return False
        elif permission == 'L1':
            return False  # L1只需告知，无需明确审批
        elif permission in ['L2', 'L3']:
            return True
        
        return True  # 默认需要审批
    
    def generate_approval_message(self, tool_name: str, permission_info: Dict, 
                                 params: Dict = None) -> str:
        """生成审批消息"""
        permission = permission_info['permission']
        description = permission_info['description']
        
        if permission == 'L0':
            return f"🟢 L0操作自动执行: {tool_name} - {description}"
        
        elif permission == 'L1':
            # 简化显示参数
            params_summary = self.summarize_params(params) if params else ""
            return f"🟡 L1操作告知: {tool_name} - {description}\n参数: {params_summary}\n(3秒内无反对则执行)"
        
        elif permission == 'L2':
            # 显示完整命令/参数
            full_command = self.format_full_command(tool_name, params)
            return (
                f"🔴 L2操作需要审批: {tool_name}\n\n"
                f"完整操作:\n{full_command}\n\n"
                f"请确认后发送: /approve"
            )
        
        elif permission == 'L3':
            # L3默认禁止
            full_command = self.format_full_command(tool_name, params)
            return (
                f"⛔ L3操作默认禁止: {tool_name}\n\n"
                f"危险操作:\n{full_command}\n\n"
                f"原因: {permission_info.get('risk_level', '高风险')}操作\n"
                f"如需执行，需要特殊授权流程。"
            )
        
        return f"未知权限级别: {permission}"
    
    def summarize_params(self, params: Dict) -> str:
        """简化参数显示"""
        if not params:
            return "无参数"
        
        summary = []
        for key, value in params.items():
            if isinstance(value, str) and len(value) > 50:
                summary.append(f"{key}=[{len(value)}字符]")
            else:
                summary.append(f"{key}={repr(value)[:30]}")
        
        return ", ".join(summary)
    
    def format_full_command(self, tool_name: str, params: Dict) -> str:
        """格式化完整命令"""
        if tool_name == 'exec' and 'command' in params:
            return params['command']
        
        # 其他工具格式化
        lines = [f"{tool_name}("]
        if params:
            for key, value in params.items():
                lines.append(f"  {key}={repr(value)},")
        lines.append(")")
        
        return "\n".join(lines)
    
    def log_audit(self, tool_name: str, permission_info: Dict, 
                  params: Dict = None, approved: bool = False,
                  result: str = None, user_context: str = None):
        """记录审计日志"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "tool": tool_name,
            "permission_level": permission_info['permission'],
            "original_permission": permission_info.get('original_permission', permission_info['permission']),
            "upgraded": permission_info.get('upgraded', False),
            "params": params,
            "approved": approved,
            "result": result,
            "user_context": user_context,
            "risk_level": permission_info.get('risk_level', 'unknown'),
            "category": permission_info.get('category', 'unknown')
        }
        
        # 按日期保存日志
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self.audit_log_dir, f"audit-{date_str}.jsonl")
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"记录审计日志失败: {str(e)}")
    
    def check_tool(self, tool_name: str, params: Dict = None) -> Dict:
        """检查工具权限"""
        permission_info = self.get_tool_permission(tool_name, params)
        approval_required = self.get_approval_required(permission_info)
        approval_message = self.generate_approval_message(tool_name, permission_info, params)
        
        # 记录检查日志（不记录L0的每次检查）
        if permission_info['permission'] != 'L0':
            self.log_audit(tool_name, permission_info, params, approved=False, 
                          result="permission_checked", user_context="check")
        
        return {
            "permission_info": permission_info,
            "approval_required": approval_required,
            "approval_message": approval_message,
            "can_proceed": permission_info['permission'] in ['L0', 'L1']  # L0自动，L1告知后
        }
    
    def simulate_workflow(self, tool_name: str, params: Dict = None) -> Dict:
        """模拟完整工作流"""
        result = self.check_tool(tool_name, params)
        
        # 模拟L1等待
        if result['permission_info']['permission'] == 'L1':
            result['simulated_wait'] = 3  # 秒
            result['simulated_action'] = "告知后执行（模拟等待3秒）"
        
        # 模拟L2审批
        elif result['permission_info']['permission'] == 'L2':
            result['simulated_approval'] = {
                "required": True,
                "command": "/approve",
                "timeout": 120,
                "status": "等待审批"
            }
        
        # 模拟L3拒绝
        elif result['permission_info']['permission'] == 'L3':
            result['simulated_action'] = "拒绝执行，需要特殊授权"
        
        return result
    
    def get_audit_summary(self, days: int = 7) -> Dict:
        """获取审计摘要"""
        summary = {
            "total_checks": 0,
            "by_permission": {"L0": 0, "L1": 0, "L2": 0, "L3": 0},
            "by_tool": {},
            "recent_activities": []
        }
        
        try:
            for i in range(days):
                date_str = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-d")
                log_file = os.path.join(self.audit_log_dir, f"audit-{date_str}.jsonl")
                
                if os.path.exists(log_file):
                    with open(log_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            try:
                                entry = json.loads(line.strip())
                                summary["total_checks"] += 1
                                
                                # 按权限统计
                                perm = entry.get("permission_level", "unknown")
                                if perm in summary["by_permission"]:
                                    summary["by_permission"][perm] += 1
                                
                                # 按工具统计
                                tool = entry.get("tool", "unknown")
                                summary["by_tool"][tool] = summary["by_tool"].get(tool, 0) + 1
                                
                                # 最近活动
                                if i == 0:  # 只记录当天的
                                    summary["recent_activities"].append({
                                        "time": entry.get("timestamp", ""),
                                        "tool": tool,
                                        "permission": perm,
                                        "approved": entry.get("approved", False)
                                    })
                                
                            except json.JSONDecodeError:
                                continue
            
            # 只保留最近的5个活动
            summary["recent_activities"] = summary["recent_activities"][-5:]
            
        except Exception as e:
            summary["error"] = str(e)
        
        return summary

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="权限检查工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # check命令
    check_parser = subparsers.add_parser("check", help="检查工具权限")
    check_parser.add_argument("--tool", required=True, help="工具名称")
    check_parser.add_argument("--params", type=json.loads, help="参数（JSON格式）")
    
    # simulate命令
    simulate_parser = subparsers.add_parser("simulate", help="模拟完整工作流")
    simulate_parser.add_argument("--tool", required=True, help="工具名称")
    simulate_parser.add_argument("--command", help="命令（对于exec工具）")
    simulate_parser.add_argument("--params", type=json.loads, help="参数（JSON格式）")
    
    # audit命令
    audit_parser = subparsers.add_parser("audit", help="查看审计日志")
    audit_parser.add_argument("--days", type=int, default=7, help="查看最近几天")
    
    args = parser.parse_args()
    
    checker = PermissionChecker()
    
    if args.command == "check":
        params = args.params
        if args.command == "simulate" and args.command:
            params = params or {}
            params["command"] = args.command
        
        result = checker.check_tool(args.tool, params)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == "simulate":
        params = args.params or {}
        if args.command:
            params["command"] = args.command
        
        result = checker.simulate_workflow(args.tool, params)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == "audit":
        summary = checker.get_audit_summary(args.days)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()