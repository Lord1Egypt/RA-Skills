#!/usr/bin/env python3
"""
Prompt优化器生产部署脚本

功能：
1. 验证系统依赖和配置
2. 部署优化器配置
3. 设置监控和日志
4. 创建备份和回滚机制
"""

import os
import sys
import json
import shutil
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from prompt_optimizer import PromptOptimizer, PromptOptimizerConfig
    print("✅ Prompt优化器模块导入成功")
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)

class DeploymentValidator:
    """部署验证器"""
    
    def __init__(self, workspace_root: str = None):
        if workspace_root is None:
            workspace_root = os.environ.get("OPENCLAW_WORKSPACE", os.getcwd())
        self.workspace_root = workspace_root
        self.required_files = [
            "scripts/prompt_optimizer.py",
            "memory/tools-classification-config.yaml",
            "memory/phase-5-prompt-optimization-design.md"
        ]
        
        self.required_directories = [
            "scripts/",
            "memory/",
            "memory/audit-logs/"
        ]
    
    def validate_system(self) -> Dict[str, Any]:
        """验证系统完整性"""
        print("\n" + "="*60)
        print("系统完整性验证")
        print("="*60)
        
        validation_results = {
            "validation_time": datetime.now().isoformat(),
            "files": [],
            "directories": [],
            "dependencies": [],
            "overall_status": "pending"
        }
        
        # 验证文件
        print("\n验证必需文件:")
        all_files_ok = True
        for filepath in self.required_files:
            full_path = os.path.join(self.workspace_root, filepath)
            exists = os.path.exists(full_path)
            status = "✅" if exists else "❌"
            print(f"  {status} {filepath}")
            
            validation_results["files"].append({
                "file": filepath,
                "exists": exists,
                "status": "ok" if exists else "missing"
            })
            
            if not exists:
                all_files_ok = False
        
        # 验证目录
        print("\n验证必需目录:")
        all_dirs_ok = True
        for dirpath in self.required_directories:
            full_path = os.path.join(self.workspace_root, dirpath)
            exists = os.path.exists(full_path)
            status = "✅" if exists else "❌"
            print(f"  {status} {dirpath}")
            
            validation_results["directories"].append({
                "directory": dirpath,
                "exists": exists,
                "status": "ok" if exists else "missing"
            })
            
            if not exists:
                all_dirs_ok = False
        
        # 验证Python依赖
        print("\n验证Python依赖:")
        dependencies = [
            ("json", "标准库"),
            ("re", "标准库"),
            ("hashlib", "标准库"),
            ("datetime", "标准库"),
            ("typing", "标准库")
        ]
        
        all_deps_ok = True
        for module_name, module_type in dependencies:
            try:
                __import__(module_name)
                status = "✅"
                print(f"  {status} {module_name} ({module_type})")
                validation_results["dependencies"].append({
                    "module": module_name,
                    "type": module_type,
                    "status": "ok"
                })
            except ImportError:
                status = "❌"
                print(f"  {status} {module_name} ({module_type}) - 缺失")
                validation_results["dependencies"].append({
                    "module": module_name,
                    "type": module_type,
                    "status": "missing"
                })
                all_deps_ok = False
        
        # 验证优化器功能
        print("\n验证优化器功能:")
        try:
            config = PromptOptimizerConfig()
            optimizer = PromptOptimizer(config)
            
            # 简单测试
            test_context = {"task_type": "deployment_test", "description": "部署验证"}
            optimized = optimizer.optimize_for_task(test_context)
            
            if optimized.system_prompt and optimized.token_estimate > 0:
                print("  ✅ 优化器功能正常")
                validation_results["optimizer_functional"] = True
                validation_results["optimizer_test"] = {
                    "system_prompt_length": len(optimized.system_prompt),
                    "token_estimate": optimized.token_estimate,
                    "status": "ok"
                }
            else:
                print("  ❌ 优化器功能异常")
                validation_results["optimizer_functional"] = False
                validation_results["optimizer_test"] = {"status": "failed"}
        except Exception as e:
            print(f"  ❌ 优化器验证失败: {e}")
            validation_results["optimizer_functional"] = False
            validation_results["optimizer_test"] = {"status": f"error: {str(e)}"}
        
        # 总体状态
        overall_ok = all_files_ok and all_dirs_ok and all_deps_ok and validation_results.get("optimizer_functional", False)
        validation_results["overall_status"] = "passed" if overall_ok else "failed"
        
        print(f"\n总体验证状态: {'✅ 通过' if overall_ok else '❌ 失败'}")
        
        return validation_results
    
    def backup_existing_config(self) -> bool:
        """备份现有配置"""
        print("\n" + "="*60)
        print("备份现有配置")
        print("="*60)
        
        backup_dir = os.path.join(self.workspace_root, "backups", "prompt-optimizer")
        backup_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            os.makedirs(backup_dir, exist_ok=True)
            
            # 备份文件列表
            files_to_backup = [
                "memory/tools-classification-config.yaml",
                "memory/prompt-config.json",  # 如果存在
            ]
            
            backed_up_files = []
            
            for filepath in files_to_backup:
                source_path = os.path.join(self.workspace_root, filepath)
                if os.path.exists(source_path):
                    # 创建带时间戳的备份
                    filename = os.path.basename(filepath)
                    backup_path = os.path.join(backup_dir, f"{backup_time}_{filename}")
                    
                    shutil.copy2(source_path, backup_path)
                    backed_up_files.append({
                        "source": filepath,
                        "backup": backup_path,
                        "size": os.path.getsize(source_path)
                    })
                    print(f"  ✅ 备份: {filepath} → {backup_path}")
            
            # 保存备份清单
            backup_manifest = {
                "backup_time": backup_time,
                "backup_dir": backup_dir,
                "files": backed_up_files
            }
            
            manifest_path = os.path.join(backup_dir, f"{backup_time}_manifest.json")
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(backup_manifest, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 备份完成: {len(backed_up_files)}个文件已备份")
            print(f"备份清单: {manifest_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ 备份失败: {e}")
            return False

class DeploymentManager:
    """部署管理器"""
    
    def __init__(self):
        self.validator = DeploymentValidator()
    
    def deploy_configuration(self) -> Dict[str, Any]:
        """部署配置"""
        print("\n" + "="*60)
        print("部署优化器配置")
        print("="*60)
        
        deployment_results = {
            "deployment_time": datetime.now().isoformat(),
            "steps": [],
            "status": "pending"
        }
        
        try:
            # 步骤1: 验证系统
            step1_start = time.time()
            print("\n步骤1: 系统验证...")
            validation = self.validator.validate_system()
            
            deployment_results["steps"].append({
                "step": 1,
                "name": "system_validation",
                "start_time": step1_start,
                "end_time": time.time(),
                "duration": time.time() - step1_start,
                "status": validation["overall_status"],
                "details": validation
            })
            
            if validation["overall_status"] != "passed":
                print("❌ 系统验证失败，停止部署")
                deployment_results["status"] = "failed"
                return deployment_results
            
            print("✅ 系统验证通过")
            
            # 步骤2: 备份现有配置
            step2_start = time.time()
            print("\n步骤2: 备份现有配置...")
            backup_success = self.validator.backup_existing_config()
            
            deployment_results["steps"].append({
                "step": 2,
                "name": "backup_configuration",
                "start_time": step2_start,
                "end_time": time.time(),
                "duration": time.time() - step2_start,
                "status": "success" if backup_success else "failed",
                "details": {"success": backup_success}
            })
            
            if not backup_success:
                print("⚠️  备份失败，继续部署但风险较高")
            
            # 步骤3: 创建默认配置
            step3_start = time.time()
            print("\n步骤3: 创建默认配置...")
            
            default_config_path = os.path.join(self.validator.workspace_root, "memory", "prompt-optimizer-config.json")
            
            default_config = {
                "version": "1.0",
                "created_at": datetime.now().isoformat(),
                "config": {
                    "default_fragment_priority_threshold": 6,
                    "default_max_tokens": 1500,
                    "default_compression_level": 2,
                    "memory_integration_enabled": True,
                    "tool_optimization_enabled": True,
                    "context_compression_enabled": True,
                    "performance_monitoring_enabled": True
                },
                "task_profiles": {
                    "file_operations": {
                        "fragment_priority_threshold": 6,
                        "max_tokens": 1200,
                        "compression_level": 2
                    },
                    "security_sensitive": {
                        "fragment_priority_threshold": 8,
                        "max_tokens": 2000,
                        "compression_level": 1
                    },
                    "multi_agent_collaboration": {
                        "fragment_priority_threshold": 7,
                        "max_tokens": 1800,
                        "compression_level": 2
                    },
                    "light_task": {
                        "fragment_priority_threshold": 5,
                        "max_tokens": 1000,
                        "compression_level": 3
                    }
                },
                "monitoring": {
                    "log_level": "info",
                    "performance_log_interval": 3600,  # 1小时
                    "error_log_path": "memory/prompt-optimizer-errors.log",
                    "performance_log_path": "memory/prompt-optimizer-performance.log"
                }
            }
            
            with open(default_config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            
            deployment_results["steps"].append({
                "step": 3,
                "name": "create_default_config",
                "start_time": step3_start,
                "end_time": time.time(),
                "duration": time.time() - step3_start,
                "status": "success",
                "details": {"config_path": default_config_path, "config_size": os.path.getsize(default_config_path)}
            })
            
            print(f"✅ 默认配置创建: {default_config_path}")
            
            # 步骤4: 创建监控脚本
            step4_start = time.time()
            print("\n步骤4: 创建监控脚本...")
            
            monitor_script = """#!/usr/bin/env python3
# Prompt优化器监控脚本

import sys
import os
import time
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from prompt_optimizer import PromptOptimizer, PromptOptimizerConfig
    print(f"[{datetime.now().isoformat()}] ✅ 监控脚本启动")
    
    # 简单健康检查
    config = PromptOptimizerConfig()
    optimizer = PromptOptimizer(config)
    
    test_context = {"task_type": "health_check", "description": "监控健康检查"}
    optimized = optimizer.optimize_for_task(test_context)
    
    health_status = {
        "timestamp": datetime.now().isoformat(),
        "status": "healthy",
        "system_prompt_length": len(optimized.system_prompt),
        "token_estimate": optimized.token_estimate,
        "optimizer_version": "1.0"
    }
    
    print(f"[{datetime.now().isoformat()}] 健康状态: {json.dumps(health_status)}")
    
except Exception as e:
    print(f"[{datetime.now().isoformat()}] ❌ 健康检查失败: {e}")
    sys.exit(1)
"""
            
            monitor_script_path = os.path.join(self.validator.workspace_root, "scripts", "monitor_prompt_optimizer.py")
            with open(monitor_script_path, 'w', encoding='utf-8') as f:
                f.write(monitor_script)
            
            # 设置可执行权限
            os.chmod(monitor_script_path, 0o755)
            
            deployment_results["steps"].append({
                "step": 4,
                "name": "create_monitor_script",
                "start_time": step4_start,
                "end_time": time.time(),
                "duration": time.time() - step4_start,
                "status": "success",
                "details": {"script_path": monitor_script_path}
            })
            
            print(f"✅ 监控脚本创建: {monitor_script_path}")
            
            # 步骤5: 创建部署完成标志
            step5_start = time.time()
            print("\n步骤5: 创建部署完成标志...")
            
            deployment_complete = {
                "deployment_time": datetime.now().isoformat(),
                "deployment_version": "1.0",
                "deployment_steps": len(deployment_results["steps"]),
                "config_files": [
                    "memory/prompt-optimizer-config.json",
                    "scripts/monitor_prompt_optimizer.py"
                ],
                "status": "completed"
            }
            
            complete_path = os.path.join(self.validator.workspace_root, "memory", "prompt-optimizer-deployment-complete.json")
            with open(complete_path, 'w', encoding='utf-8') as f:
                json.dump(deployment_complete, f, indent=2, ensure_ascii=False)
            
            deployment_results["steps"].append({
                "step": 5,
                "name": "create_deployment_complete_marker",
                "start_time": step5_start,
                "end_time": time.time(),
                "duration": time.time() - step5_start,
                "status": "success",
                "details": {"marker_path": complete_path}
            })
            
            print(f"✅ 部署完成标志创建: {complete_path}")
            
            # 总体状态
            deployment_results["status"] = "success"
            deployment_results["deployment_duration"] = time.time() - step1_start
            
            print("\n" + "="*60)
            print("✅ 部署完成!")
            print("="*60)
            print(f"总耗时: {deployment_results['deployment_duration']:.2f}秒")
            print(f"部署步骤: {len(deployment_results['steps'])}个")
            print(f"配置文件: memory/prompt-optimizer-config.json")
            print(f"监控脚本: scripts/monitor_prompt_optimizer.py")
            
            return deployment_results
            
        except Exception as e:
            print(f"\n❌ 部署失败: {e}")
            deployment_results["status"] = "failed"
            deployment_results["error"] = str(e)
            return deployment_results
    
    def generate_deployment_report(self, deployment_results: Dict[str, Any]) -> str:
        """生成部署报告"""
        report_path = os.path.join(self.validator.workspace_root, "memory", "prompt-optimizer-deployment-report.json")
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(deployment_results, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ 部署报告已保存: {report_path}")
            return report_path
        except Exception as e:
            print(f"❌ 部署报告保存失败: {e}")
            return ""

def main():
    """主部署函数"""
    print("="*60)
    print("Prompt优化器生产部署")
    print("="*60)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    manager = DeploymentManager()
    
    # 运行部署
    deployment_results = manager.deploy_configuration()
    
    # 生成报告
    if deployment_results["status"] == "success":
        report_path = manager.generate_deployment_report(deployment_results)
        
        print("\n" + "="*60)
        print("部署摘要")
        print("="*60)
        print(f"状态: ✅ 成功")
        print(f"耗时: {deployment_results.get('deployment_duration', 0):.2f}秒")
        print(f"步骤: {len(deployment_results.get('steps', []))}")
        
        # 显示下一步建议
        print("\n下一步建议:")
        print("1. 运行集成测试: python scripts/test_prompt_optimizer_integration.py")
        print("2. 运行基准测试: python scripts/benchmark_original_vs_optimized.py")
        print("3. 测试监控脚本: python scripts/monitor_prompt_optimizer.py")
        print("4. 集成到OpenClaw工作流")
        
    else:
        print("\n" + "="*60)
        print("部署失败")
        print("="*60)
        print(f"错误: {deployment_results.get('error', '未知错误')}")
        
        # 显示故障排除建议
        print("\n故障排除建议:")
        print("1. 检查系统完整性: 确保所有必需文件存在")
        print("2. 检查Python依赖: 确保所有必需模块可用")
        print("3. 检查文件权限: 确保有读写权限")
        print("4. 查看详细错误日志")
    
    print(f"\n结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()