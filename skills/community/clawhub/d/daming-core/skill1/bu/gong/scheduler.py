"""
工部 - 资源调度、外部执行
负责调度任务执行，管理Token预算，调用外部高算力设备
"""

import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

# 导入其他部门
from ...config import ACTIVE_TASKS_DIR

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GongBuScheduler:
    """工部调度器"""
    
    def __init__(self):
        self.execution_records = {}
    
    def check_token_budget(self, task_id: str, required_tokens: int) -> Dict[str, Any]:
        """
        检查Token预算
        返回预算检查结果
        """
        task_dir = Path(ACTIVE_TASKS_DIR) / task_id
        
        # 检查任务档案
        task_file = task_dir / "task_draft.json"
        if not task_file.exists():
            return {
                "success": False,
                "error": f"任务档案不存在: {task_id}",
                "has_sufficient_budget": False
            }
        
        with open(task_file, 'r', encoding='utf-8') as f:
            task_draft = json.load(f)
        
        # 检查Token账本
        ledger_file = task_dir / "token_ledger.json"
        if not ledger_file.exists():
            return {
                "success": False,
                "error": f"Token账本不存在: {task_id}",
                "has_sufficient_budget": False
            }
        
        with open(ledger_file, 'r', encoding='utf-8') as f:
            token_ledger = json.load(f)
        
        # 计算可用预算
        total_budget = task_draft.get("token_budget", 0)
        used_tokens = token_ledger.get("used_tokens", 0)
        available_tokens = total_budget - used_tokens
        
        has_sufficient = available_tokens >= required_tokens
        
        return {
            "success": True,
            "task_id": task_id,
            "total_budget": total_budget,
            "used_tokens": used_tokens,
            "available_tokens": available_tokens,
            "required_tokens": required_tokens,
            "has_sufficient_budget": has_sufficient,
            "can_proceed": has_sufficient
        }
    
    def dispatch_with_budget_check(self, task_id: str, execution_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        带预算检查的调度执行
        返回调度结果
        """
        # 默认需要100个Token
        required_tokens = execution_params.get("estimated_tokens", 100)
        
        # 检查预算
        budget_check = self.check_token_budget(task_id, required_tokens)
        if not budget_check.get("success", False):
            return {
                "success": False,
                "error": f"预算检查失败: {budget_check.get('error', '未知错误')}",
                "task_id": task_id,
                "dispatched": False
            }
        
        if not budget_check.get("has_sufficient_budget", False):
            return {
                "success": False,
                "error": f"Token预算不足: 需要{required_tokens}，可用{budget_check['available_tokens']}",
                "task_id": task_id,
                "dispatched": False,
                "budget_details": budget_check
            }
        
        # 记录Token使用
        task_dir = Path(ACTIVE_TASKS_DIR) / task_id
        ledger_file = task_dir / "token_ledger.json"
        
        with open(ledger_file, 'r', encoding='utf-8') as f:
            token_ledger = json.load(f)
        
        # 更新已使用Token
        token_ledger["used_tokens"] = token_ledger.get("used_tokens", 0) + required_tokens
        token_ledger["transactions"].append({
            "type": "execution",
            "amount": required_tokens,
            "description": f"工部调度执行: {execution_params.get('action', '未知')}",
            "timestamp": datetime.now().isoformat()
        })
        
        with open(ledger_file, 'w', encoding='utf-8') as f:
            json.dump(token_ledger, f, ensure_ascii=False, indent=2)
        
        # 创建执行记录
        execution_id = f"EXEC-{int(time.time())}"
        execution_record = {
            "execution_id": execution_id,
            "task_id": task_id,
            "action": "dispatch",
            "params": execution_params,
            "required_tokens": required_tokens,
            "dispatched_at": datetime.now().isoformat(),
            "status": "dispatched",
            "department_checks": {
                "gong": True  # 工部已处理
            }
        }
        
        # 保存执行记录
        exec_file = task_dir / "execution_records.json"
        execution_data = []
        if exec_file.exists():
            with open(exec_file, 'r', encoding='utf-8') as f:
                execution_data = json.load(f)
        
        execution_data.append(execution_record)
        
        with open(exec_file, 'w', encoding='utf-8') as f:
            json.dump(execution_data, f, ensure_ascii=False, indent=2)
        
        # 更新任务状态
        task_file = task_dir / "task_draft.json"
        with open(task_file, 'r', encoding='utf-8') as f:
            task_draft = json.load(f)
        
        task_draft["status"] = "executing"
        task_draft["department_checks"]["gong"] = True
        
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_draft, f, ensure_ascii=False, indent=2)
        
        print(f"🔧 工部：任务调度成功")
        print(f"  任务ID: {task_id}")
        print(f"  执行ID: {execution_id}")
        print(f"  消耗Token: {required_tokens}")
        print(f"  剩余预算: {budget_check['available_tokens'] - required_tokens}")
        
        return {
            "success": True,
            "task_id": task_id,
            "execution_id": execution_id,
            "dispatched": True,
            "required_tokens": required_tokens,
            "remaining_budget": budget_check['available_tokens'] - required_tokens,
            "execution_record": execution_record
        }
    
    def get_execution_status(self, task_id: str, execution_id: str) -> Dict[str, Any]:
        """获取执行状态"""
        task_dir = Path(ACTIVE_TASKS_DIR) / task_id
        exec_file = task_dir / "execution_records.json"
        
        if not exec_file.exists():
            return {
                "success": False,
                "error": f"执行记录不存在: {task_id}"
            }
        
        with open(exec_file, 'r', encoding='utf-8') as f:
            execution_data = json.load(f)
        
        for record in execution_data:
            if record.get("execution_id") == execution_id:
                return {
                    "success": True,
                    "execution_record": record,
                    "task_id": task_id,
                    "execution_id": execution_id
                }
        
        return {
            "success": False,
            "error": f"执行记录未找到: {execution_id}"
        }


    def execute_with_external_agent(self, task_id: str, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        使用外部高算力设备执行任务
        
        Args:
            task_id: 任务ID
            workflow_config: 工作流配置
        
        Returns:
            执行结果
        """
        try:
            logger.info(f"开始执行外部agent任务: {task_id}")
            
            # 导入ComfyUI客户端
            try:
                from .comfyui_client import ComfyUIClient
            except ImportError as e:
                logger.error(f"导入ComfyUI客户端失败: {str(e)}")
                return {
                    "success": False,
                    "error": f"ComfyUI客户端未配置: {str(e)}",
                    "task_id": task_id,
                    "message": "请先配置ComfyUI客户端"
                }
            
            # 创建客户端
            client = ComfyUIClient()
            
            # 健康检查
            health = client.health_check()
            if not health["success"]:
                logger.error(f"ComfyUI服务器健康检查失败: {health.get('message')}")
                return {
                    "success": False,
                    "error": "ComfyUI服务器不可用",
                    "task_id": task_id,
                    "health_check": health,
                    "message": f"高算力设备连接失败: {health.get('message')}"
                }
            
            logger.info(f"ComfyUI服务器状态: {health['status']}")
            
            # 执行工作流
            execution_result = client.execute_workflow(workflow_config)
            
            # 更新执行记录
            task_dir = Path(ACTIVE_TASKS_DIR) / task_id
            exec_file = task_dir / "execution_records.json"
            
            execution_data = []
            if exec_file.exists():
                with open(exec_file, 'r', encoding='utf-8') as f:
                    execution_data = json.load(f)
            
            # 查找最新的执行记录
            latest_record = None
            for record in reversed(execution_data):
                if record.get("status") == "dispatched":
                    latest_record = record
                    break
            
            if latest_record:
                # 更新执行记录
                latest_record["status"] = "executed" if execution_result["success"] else "failed"
                latest_record["external_agent"] = "comfyui"
                latest_record["execution_result"] = execution_result
                latest_record["completed_at"] = datetime.now().isoformat()
                latest_record["last_updated"] = datetime.now().isoformat()
                
                # 保存更新
                with open(exec_file, 'w', encoding='utf-8') as f:
                    json.dump(execution_data, f, ensure_ascii=False, indent=2)
            
            # 更新任务状态
            task_file = task_dir / "task_draft.json"
            if task_file.exists():
                with open(task_file, 'r', encoding='utf-8') as f:
                    task_draft = json.load(f)
                
                task_draft["status"] = "completed" if execution_result["success"] else "failed"
                task_draft["last_updated"] = datetime.now().isoformat()
                
                with open(task_file, 'w', encoding='utf-8') as f:
                    json.dump(task_draft, f, ensure_ascii=False, indent=2)
            
            logger.info(f"外部agent执行完成: 成功={execution_result['success']}")
            
            return {
                "success": execution_result["success"],
                "task_id": task_id,
                "execution_result": execution_result,
                "health_check": health,
                "message": execution_result.get("message", "执行完成")
            }
        
        except Exception as e:
            logger.error(f"外部agent执行异常: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task_id,
                "message": f"外部agent执行异常: {str(e)}"
            }
    
    def process_pending_tasks(self) -> Dict[str, Any]:
        """
        处理待执行任务
        扫描所有待执行任务，调用外部agent执行
        
        Returns:
            处理结果
        """
        try:
            logger.info("开始扫描待执行任务")
            
            pending_tasks = []
            task_dirs = list(Path(ACTIVE_TASKS_DIR).iterdir())
            
            for task_dir in task_dirs:
                if not task_dir.is_dir():
                    continue
                
                task_file = task_dir / "task_draft.json"
                if not task_file.exists():
                    continue
                
                with open(task_file, 'r', encoding='utf-8') as f:
                    task_draft = json.load(f)
                
                # 检查任务状态
                status = task_draft.get("status", "")
                if status in ["audited_pass", "dispatched"]:
                    pending_tasks.append({
                        "task_id": task_dir.name,
                        "task_draft": task_draft,
                        "task_dir": task_dir
                    })
            
            logger.info(f"找到 {len(pending_tasks)} 个待执行任务")
            
            results = []
            for task_info in pending_tasks:
                task_id = task_info["task_id"]
                task_draft = task_info["task_draft"]
                
                logger.info(f"处理任务: {task_id}")
                
                # 检查是否已调度
                exec_file = task_info["task_dir"] / "execution_records.json"
                if exec_file.exists():
                    with open(exec_file, 'r', encoding='utf-8') as f:
                        execution_data = json.load(f)
                    
                    # 检查是否有已调度但未执行的记录
                    has_dispatched = False
                    has_executed = False
                    
                    for record in execution_data:
                        if record.get("status") == "dispatched":
                            has_dispatched = True
                        elif record.get("status") in ["executed", "failed"]:
                            has_executed = True
                    
                    if has_executed:
                        logger.info(f"任务 {task_id} 已执行，跳过")
                        continue
                    
                    if has_dispatched:
                        # 已有调度记录，直接执行
                        logger.info(f"任务 {task_id} 已调度，开始执行")
                    else:
                        # 需要先调度
                        logger.info(f"任务 {task_id} 未调度，先进行调度")
                        
                        # 创建调度记录
                        execution_id = f"EXEC-{int(time.time())}"
                        execution_record = {
                            "execution_id": execution_id,
                            "task_id": task_id,
                            "action": "dispatch",
                            "params": {},
                            "required_tokens": 100,
                            "dispatched_at": datetime.now().isoformat(),
                            "status": "dispatched",
                            "department_checks": {"gong": True}
                        }
                        
                        execution_data.append(execution_record)
                        with open(exec_file, 'w', encoding='utf-8') as f:
                            json.dump(execution_data, f, ensure_ascii=False, indent=2)
                
                # 执行任务
                # TODO: 根据任务类型构建工作流配置
                workflow_config = {
                    "workflow": {
                        "3": {
                            "class_type": "KSampler",
                            "inputs": {
                                "seed": 12345,
                                "steps": 20,
                                "cfg": 7,
                                "sampler_name": "euler",
                                "scheduler": "normal",
                                "denoise": 1,
                                "model": ["4", 0],
                                "positive": ["6", 0],
                                "negative": ["7", 0],
                                "latent_image": ["5", 0]
                            }
                        }
                    },
                    "client_id": "daming_court",
                    "extra_data": {}
                }
                
                # 调用外部agent执行
                result = self.execute_with_external_agent(task_id, workflow_config)
                results.append({
                    "task_id": task_id,
                    "success": result["success"],
                    "message": result.get("message", "")
                })
            
            return {
                "success": True,
                "processed_count": len(results),
                "results": results,
                "message": f"处理完成，共处理 {len(results)} 个任务"
            }
        
        except Exception as e:
            logger.error(f"处理待执行任务异常: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"处理待执行任务异常: {str(e)}"
            }


def create_gong_scheduler() -> GongBuScheduler:
    """创建工部调度器（工厂函数）"""
    return GongBuScheduler()


if __name__ == "__main__":
    # 测试工部功能
    print("🏛️ 工部功能测试")
    
    # 需要先创建任务和Token账本
    print("⚠️  需要完整的任务环境才能测试")
    print("✅ 工部调度器类已定义")