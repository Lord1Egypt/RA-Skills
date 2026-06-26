#!/usr/bin/env python3
"""
权限与沙箱集成管理器（阶段四安全架构 - 集成组件）

功能：
1. 集成权限检查和沙箱分析
2. 统一决策流程：权限检查 → 沙箱分析 → 执行决策
3. 提供工具包装器：为高风险工具自动添加沙箱保护
4. 管理完整的安全执行流程

使用方法：
  python permission_sandbox_integration.py analyze --tool write --path /tmp/test.txt
  python permission_sandbox_integration.py wrap-tool --tool write
  python permission_sandbox_integration.py workflow --tool exec --command "rm -rf /tmp/*"
"""

import sys
import os
import json
import importlib.util
from typing import Dict, List, Tuple, Optional, Any, Callable

# 添加脚本路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入模块
try:
    # 动态导入权限检查器
    perm_spec = importlib.util.spec_from_file_location("permission_checker", "scripts/permission_checker.py")
    perm_module = importlib.util.module_from_spec(perm_spec)
    perm_spec.loader.exec_module(perm_module)
    PermissionChecker = perm_module.PermissionChecker
    
    # 动态导入沙箱管理器
    sandbox_spec = importlib.util.spec_from_file_location("sandbox_manager", "scripts/sandbox_manager.py")
    sandbox_module = importlib.util.module_from_spec(sandbox_spec)
    sandbox_spec.loader.exec_module(sandbox_module)
    SandboxManager = sandbox_module.SandboxManager
    
    print("✅ 成功导入权限检查器和沙箱管理器")
except ImportError as e:
    print(f"⚠️ 导入失败: {e}")
    print("请确保 scripts/ 目录中有 permission_checker.py 和 sandbox_manager.py")
    sys.exit(1)

class PermissionSandboxIntegration:
    """权限与沙箱集成管理器"""
    
    def __init__(self):
        self.permission_checker = PermissionChecker()
        self.sandbox_manager = SandboxManager()
        
        # 高风险工具列表（需要沙箱包装）
        self.high_risk_tools = ["write", "edit", "exec", "message", "sessions_spawn", "sessions_send"]
        
        # 沙箱豁免工具列表（不需要沙箱）
        self.sandbox_exempt_tools = ["read", "memory_search", "memory_get", "session_status"]
    
    def analyze_operation(self, tool_name: str, params: Dict = None) -> Dict[str, Any]:
        """综合分析操作的安全性和风险"""
        params = params or {}
        
        # 1. 权限检查
        perm_result = self.permission_checker.check_tool(tool_name, params)
        
        # 2. 沙箱分析
        sandbox_analysis = self.sandbox_manager.analyze_operation(tool_name, **params)
        
        # 3. 集成决策
        decision = self._make_integrated_decision(perm_result, sandbox_analysis, tool_name, params)
        
        return {
            "tool": tool_name,
            "permission_analysis": perm_result,
            "sandbox_analysis": sandbox_analysis,
            "integrated_decision": decision,
            "recommended_action": self._generate_recommended_action(perm_result, sandbox_analysis, decision)
        }
    
    def _make_integrated_decision(self, perm_result: Dict, sandbox_analysis: Dict, 
                                 tool_name: str, params: Dict) -> Dict[str, Any]:
        """生成集成决策"""
        permission_info = perm_result.get("permission_info", {})
        permission_level = permission_info.get("permission", "unknown")
        needs_approval = perm_result.get("approval_required", False)
        needs_sandbox = sandbox_analysis.get("needs_sandbox", False)
        
        # 决策矩阵
        decision = {
            "permission_level": permission_level,
            "needs_approval": needs_approval,
            "needs_sandbox": needs_sandbox,
            "sandbox_type": sandbox_analysis.get("sandbox_type", "none"),
            "risk_level": sandbox_analysis.get("risk_level", "low"),
            "suggested_isolation_level": sandbox_analysis.get("suggested_isolation_level", "none"),
            "execution_mode": "direct",  # direct, sandbox, require_approval, approval_then_sandbox
            "user_interaction": "none",  # none, inform, approve
            "safety_level": "safe"  # safe, caution, warning, danger, critical
        }
        
        # 豁免工具特殊处理
        if tool_name in self.sandbox_exempt_tools:
            decision["needs_sandbox"] = False
            decision["execution_mode"] = "direct"
            decision["safety_level"] = "safe"
            return decision
        
        # 决策逻辑
        if permission_level == "L0":
            if needs_sandbox:
                decision["execution_mode"] = "sandbox"
                decision["user_interaction"] = "inform"
                decision["safety_level"] = "caution"
            else:
                decision["execution_mode"] = "direct"
                decision["safety_level"] = "safe"
        
        elif permission_level == "L1":
            decision["user_interaction"] = "inform"
            
            if needs_approval:
                decision["execution_mode"] = "require_approval"
                decision["safety_level"] = "warning"
            elif needs_sandbox:
                decision["execution_mode"] = "sandbox"
                decision["safety_level"] = "caution"
            else:
                decision["execution_mode"] = "direct"
                decision["safety_level"] = "safe"
        
        elif permission_level == "L2":
            decision["user_interaction"] = "approve"
            
            if needs_sandbox:
                decision["execution_mode"] = "approval_then_sandbox"
                decision["safety_level"] = "danger"
            else:
                decision["execution_mode"] = "require_approval"
                decision["safety_level"] = "warning"
        
        elif permission_level == "L3":
            decision["user_interaction"] = "approve"
            decision["needs_sandbox"] = True  # L3总是需要沙箱
            decision["execution_mode"] = "approval_then_sandbox"
            decision["safety_level"] = "critical"
        
        # 高风险工具强制沙箱
        if tool_name in self.high_risk_tools and permission_level in ["L1", "L2", "L3"]:
            decision["needs_sandbox"] = True
            decision["sandbox_type"] = self._determine_sandbox_type(tool_name)
            
            if decision["execution_mode"] == "require_approval":
                decision["execution_mode"] = "approval_then_sandbox"
            elif decision["execution_mode"] == "direct":
                decision["execution_mode"] = "sandbox"
        
        return decision
    
    def _determine_sandbox_type(self, tool_name: str) -> str:
        """确定沙箱类型"""
        if tool_name in ["write", "edit"]:
            return "file_sandbox"
        elif tool_name == "exec":
            return "command_sandbox"
        elif tool_name in ["web_search", "web_fetch"]:
            return "api_sandbox"
        elif tool_name in ["message", "sessions_spawn", "sessions_send"]:
            return "communication_sandbox"
        else:
            return "full_sandbox"
    
    def _generate_recommended_action(self, perm_result: Dict, sandbox_analysis: Dict, 
                                   decision: Dict) -> Dict[str, Any]:
        """生成推荐操作"""
        action = {
            "summary": "",
            "steps": [],
            "user_message": "",
            "internal_notes": []
        }
        
        execution_mode = decision.get("execution_mode", "direct")
        needs_approval = decision.get("needs_approval", False)
        needs_sandbox = decision.get("needs_sandbox", False)
        
        if execution_mode == "direct":
            action["summary"] = "直接执行"
            action["steps"] = ["验证参数", "执行操作", "记录日志"]
            action["user_message"] = "🟢 操作安全，正在执行..."
        
        elif execution_mode == "sandbox":
            action["summary"] = "沙箱保护执行"
            action["steps"] = [
                "分析操作风险",
                "创建沙箱环境", 
                "在沙箱中执行",
                "验证执行结果",
                "提交安全结果",
                "清理沙箱环境"
            ]
            action["user_message"] = f"🛡️ 操作需要沙箱保护 ({decision.get('sandbox_type', '未知')})"
        
        elif execution_mode == "require_approval":
            action["summary"] = "需要用户审批"
            action["steps"] = [
                "显示完整操作详情",
                "等待用户批准",
                "用户批准后执行",
                "记录审批和执行日志"
            ]
            action["user_message"] = perm_result.get("approval_message", "需要审批")
        
        elif execution_mode == "approval_then_sandbox":
            action["summary"] = "审批后沙箱执行"
            action["steps"] = [
                "显示完整操作详情",
                "等待用户批准",
                "用户批准后创建沙箱",
                "在沙箱中执行",
                "验证执行结果",
                "提交安全结果"
            ]
            approval_msg = perm_result.get("approval_message", "需要审批")
            action["user_message"] = f"{approval_msg}\n\n🛡️ 审批后将进入沙箱执行"
        
        # 添加风险提示
        risk_level = decision.get("risk_level", "low")
        if risk_level in ["high", "critical"]:
            action["internal_notes"].append(f"高风险操作: {risk_level}")
            action["user_message"] += f"\n⚠️ 警告: {risk_level.upper()}风险操作"
        
        return action
    
    def create_tool_wrapper(self, tool_name: str, original_func: Callable) -> Callable:
        """创建工具包装器，自动添加权限检查和沙箱保护"""
        
        def wrapped_function(*args, **kwargs):
            # 提取参数
            params = self._extract_params_from_kwargs(tool_name, kwargs)
            
            # 综合分析
            analysis = self.analyze_operation(tool_name, params)
            decision = analysis["integrated_decision"]
            action = analysis["recommended_action"]
            
            print(f"\n🔍 工具包装器分析: {tool_name}")
            print(f"   权限级别: {decision['permission_level']}")
            print(f"   执行模式: {decision['execution_mode']}")
            print(f"   沙箱需要: {decision['needs_sandbox']}")
            print(f"   风险级别: {decision['risk_level']}")
            
            # 根据决策执行
            if decision["execution_mode"] == "direct":
                print(f"   🟢 直接执行...")
                return original_func(*args, **kwargs)
            
            elif decision["execution_mode"] == "sandbox":
                print(f"   🛡️ 沙箱执行...")
                # 使用沙箱管理器执行
                sandbox_result = self.sandbox_manager.execute_in_sandbox(
                    tool_name, original_func, *args, **kwargs
                )
                return self._process_sandbox_result(sandbox_result)
            
            elif decision["execution_mode"] == "require_approval":
                print(f"   🔴 需要审批")
                # 显示审批消息并等待
                approval_msg = analysis["permission_analysis"].get("approval_message", "")
                print(f"\n{approval_msg}")
                print("\n[模拟: 用户批准后继续]")
                # 实际实现中应该等待用户输入
                return original_func(*args, **kwargs)
            
            elif decision["execution_mode"] == "approval_then_sandbox":
                print(f"   🔴🛡️ 需要审批后沙箱执行")
                approval_msg = analysis["permission_analysis"].get("approval_message", "")
                print(f"\n{approval_msg}")
                print("\n[模拟: 用户批准后进入沙箱]")
                # 实际实现中应该等待用户输入
                sandbox_result = self.sandbox_manager.execute_in_sandbox(
                    tool_name, original_func, *args, **kwargs
                )
                return self._process_sandbox_result(sandbox_result)
            
            else:
                print(f"   ❓ 未知执行模式")
                return {"error": f"未知执行模式: {decision['execution_mode']}"}
        
        return wrapped_function
    
    def _extract_params_from_kwargs(self, tool_name: str, kwargs: Dict) -> Dict:
        """从kwargs提取参数"""
        params = {}
        
        # 通用参数
        common_params = ["path", "file_path", "command", "content", "message", "url", "query"]
        
        for key, value in kwargs.items():
            if key in common_params or key.startswith("_"):
                params[key] = value
        
        # 工具特定参数
        if tool_name == "exec":
            params["command"] = kwargs.get("command", "")
        elif tool_name in ["write", "edit"]:
            params["path"] = kwargs.get("path") or kwargs.get("file_path", "")
            params["content"] = kwargs.get("content", "")
        elif tool_name == "message":
            params["message"] = kwargs.get("message", "")
            params["channel"] = kwargs.get("channel", "")
        elif tool_name in ["web_search", "web_fetch"]:
            params["query"] = kwargs.get("query", "")
            params["url"] = kwargs.get("url", "")
        
        return params
    
    def _process_sandbox_result(self, sandbox_result: Dict) -> Any:
        """处理沙箱结果"""
        if sandbox_result.get("sandbox_used", False):
            sandbox_exec_result = sandbox_result.get("sandbox_result", {})
            
            if sandbox_exec_result.get("success", False):
                print(f"   ✅ 沙箱执行成功")
                return sandbox_exec_result.get("original_result", {})
            else:
                print(f"   ❌ 沙箱执行失败: {sandbox_exec_result.get('error', '未知错误')}")
                return sandbox_exec_result
        else:
            print(f"   ℹ️ 沙箱未使用，直接执行")
            return sandbox_result.get("original_result", {})
    
    def test_integration(self, tool_name: str, params: Dict):
        """测试集成功能"""
        print(f"\n🔧 测试集成: {tool_name}")
        print(f"   参数: {json.dumps(params, ensure_ascii=False, indent=2)}")
        
        # 分析
        analysis = self.analyze_operation(tool_name, params)
        
        print(f"\n📊 集成分析结果:")
        print(f"   权限级别: {analysis['integrated_decision']['permission_level']}")
        print(f"   执行模式: {analysis['integrated_decision']['execution_mode']}")
        print(f"   沙箱需要: {analysis['integrated_decision']['needs_sandbox']}")
        print(f"   风险级别: {analysis['integrated_decision']['risk_level']}")
        print(f"   安全级别: {analysis['integrated_decision']['safety_level']}")
        
        action = analysis["recommended_action"]
        print(f"\n🎯 推荐操作: {action['summary']}")
        print(f"   用户消息: {action['user_message']}")
        print(f"   执行步骤: {', '.join(action['steps'])}")
        
        return analysis

def demo_integration():
    """演示集成功能"""
    print("=" * 60)
    print("权限与沙箱集成演示")
    print("=" * 60)
    
    integration = PermissionSandboxIntegration()
    
    # 测试场景
    test_scenarios = [
        {
            "name": "安全读取操作",
            "tool": "read",
            "params": {"path": "MEMORY.md"},
            "expected": "direct"
        },
        {
            "name": "危险文件写入",
            "tool": "write",
            "params": {"path": "/etc/test.conf", "content": "test"},
            "expected": "approval_then_sandbox"
        },
        {
            "name": "危险命令执行",
            "tool": "exec",
            "params": {"command": "rm -rf /tmp/*"},
            "expected": "approval_then_sandbox"
        },
        {
            "name": "外部消息发送",
            "tool": "message",
            "params": {"message": "测试消息", "channel": "feishu"},
            "expected": "require_approval"
        },
        {
            "name": "普通文件编辑",
            "tool": "edit",
            "params": {"path": "memory/test.md", "content": "test"},
            "expected": "sandbox"
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n📋 测试场景: {scenario['name']}")
        print(f"   工具: {scenario['tool']}")
        
        try:
            analysis = integration.test_integration(scenario["tool"], scenario["params"])
            
            actual_mode = analysis["integrated_decision"]["execution_mode"]
            expected_mode = scenario["expected"]
            
            if actual_mode == expected_mode:
                print(f"   ✅ 结果匹配: {actual_mode} (预期: {expected_mode})")
            else:
                print(f"   ⚠️ 结果不匹配: {actual_mode} (预期: {expected_mode})")
        
        except Exception as e:
            print(f"   ❌ 测试失败: {e}")
    
    print(f"\n" + "=" * 60)
    print("集成演示完成!")
    print("=" * 60)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='权限与沙箱集成管理器')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # analyze命令
    analyze_parser = subparsers.add_parser('analyze', help='综合分析操作')
    analyze_parser.add_argument('--tool', type=str, required=True, help='工具名称')
    analyze_parser.add_argument('--path', type=str, help='文件路径')
    analyze_parser.add_argument('--command', type=str, help='命令')
    analyze_parser.add_argument('--content', type=str, help='内容')
    analyze_parser.add_argument('--message', type=str, help='消息内容')
    
    # wrap命令
    wrap_parser = subparsers.add_parser('wrap-tool', help='创建工具包装器')
    wrap_parser.add_argument('--tool', type=str, required=True, help='工具名称')
    wrap_parser.add_argument('--output', type=str, help='输出文件')
    
    # workflow命令
    workflow_parser = subparsers.add_parser('workflow', help='演示完整工作流')
    workflow_parser.add_argument('--tool', type=str, required=True, help='工具名称')
    workflow_parser.add_argument('--path', type=str, help='文件路径')
    workflow_parser.add_argument('--command', type=str, help='命令')
    workflow_parser.add_argument('--content', type=str, help='内容')
    
    # demo命令
    subparsers.add_parser('demo', help='运行演示')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    integration = PermissionSandboxIntegration()
    
    try:
        if args.command == 'analyze':
            params = {}
            if args.path:
                params['path'] = args.path
            if args.command:
                params['command'] = args.command
            if args.content:
                params['content'] = args.content
            if args.message:
                params['message'] = args.message
            
            analysis = integration.analyze_operation(args.tool, params)
            print(json.dumps(analysis, indent=2, ensure_ascii=False))
        
        elif args.command == 'wrap-tool':
            print(f"创建工具包装器: {args.tool}")
            print("注意: 此功能需要原始工具函数作为参数")
            print("示例用法: integration.create_tool_wrapper('write', original_write_func)")
        
        elif args.command == 'workflow':
            params = {}
            if args.path:
                params['path'] = args.path
            if args.command:
                params['command'] = args.command
            if args.content:
                params['content'] = args.content
            
            integration.test_integration(args.tool, params)
        
        elif args.command == 'demo':
            demo_integration()
    
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    # demo_integration()  # 取消注释运行演示
    main()