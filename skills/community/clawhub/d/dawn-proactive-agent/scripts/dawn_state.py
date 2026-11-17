# -*- coding: utf-8 -*-
"""
曙光 轻量状态机 v1.0 (LangGraph-Inspired State Orchestration)

管理策略调仓的多步骤工作流，支持断点恢复和超时降级。
================================================================
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable

WORKSPACE = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATE_FILE = WORKSPACE / "data" / "state_machine.json"


def log(m): print(f"[STATE] {m}")
def warn(m): print(f"[WARN] {m}")


# 预定义工作流步骤
STEPS = {
    "fetch_news":       {"name": "获取新闻",       "timeout": 30,  "retryable": True,  "fallback": None},
    "extract_keywords": {"name": "提取关键词",     "timeout": 10,  "retryable": True,  "fallback": None},
    "fetch_account":    {"name": "获取账户",       "timeout": 15,  "retryable": True,  "fallback": None},
    "fetch_quotes":     {"name": "获取行情",       "timeout": 30,  "retryable": True,  "fallback": None},
    "score_etfs":       {"name": "评分ETF",        "timeout": 10,  "retryable": False, "fallback": None},
    "generate_rec":     {"name": "生成建议",       "timeout": 10,  "retryable": False, "fallback": None},
    "execute_trades":   {"name": "执行调仓",       "timeout": 120, "retryable": True,  "fallback": "skip_trade"},
    "post_check":       {"name": "执行后检查",     "timeout": 30,  "retryable": True,  "fallback": None},
    "reflect":          {"name": "反思总结",       "timeout": 10,  "retryable": False, "fallback": None},
}


class WorkflowState:
    """轻量状态机"""
    
    def __init__(self, workflow_id: str = None):
        self.workflow_id = workflow_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_step = None
        self.completed_steps = []
        self.failed_steps = []
        self.skipped_steps = []
        self.data = {}
        self.started_at = datetime.now().isoformat()
        self.status = "initialized"  # initialized | running | completed | failed
    
    @classmethod
    def load(cls) -> Optional["WorkflowState"]:
        """从文件恢复状态，支持断点续传"""
        if STATE_FILE.exists():
            try:
                data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
                ws = cls(data.get("workflow_id"))
                ws.__dict__.update(data)
                return ws
            except:
                pass
        return None
    
    def save(self):
        """持久化当前状态"""
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(
            json.dumps(self.__dict__, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    
    def start(self, step_id: str):
        """开始一个步骤"""
        if step_id not in STEPS:
            warn(f"未知步骤: {step_id}")
            return False
        
        # 检查是否已完成（断点续传）
        if step_id in self.completed_steps:
            log(f"步骤 {step_id} 已完成，跳过")
            return True
        
        self.current_step = step_id
        self.status = "running"
        self.save()
        return True
    
    def complete(self, step_id: str, result: any = None):
        """完成一个步骤"""
        if step_id != self.current_step:
            warn(f"步骤不匹配: 当前={self.current_step}, 完成={step_id}")
        self.completed_steps.append(step_id)
        self.current_step = None
        if result is not None:
            self.data[step_id] = result
        self.save()
    
    def fail(self, step_id: str, error: str):
        """步骤失败，尝试降级"""
        step = STEPS.get(step_id, {})
        fallback = step.get("fallback")
        
        self.failed_steps.append({"step": step_id, "error": error})
        
        if fallback:
            log(f"步骤 {step_id} 失败，降级到 {fallback}: {error}")
            self.skipped_steps.append(step_id)
        else:
            log(f"步骤 {step_id} 不可恢复失败: {error}")
            self.status = "failed"
            self.save()
        
        self.current_step = None
        self.save()
    
    def finish(self):
        """完成整个工作流"""
        self.status = "completed"
        self.save()
        log(f"工作流 {self.workflow_id} 完成 (成功{len(self.completed_steps)}, 失败{len(self.failed_steps)}, 跳过{len(self.skipped_steps)})")
    
    def get_resume_point(self) -> Optional[str]:
        """获取断点续传位置"""
        for step_id in STEPS:
            if step_id not in self.completed_steps:
                return step_id
        return None
    
    def summary(self) -> Dict:
        return {
            "workflow_id": self.workflow_id,
            "status": self.status,
            "completed": len(self.completed_steps),
            "failed": len(self.failed_steps),
            "skipped": len(self.skipped_steps),
            "resume_at": self.get_resume_point(),
        }


def run_workflow(steps: List[str], handlers: Dict[str, Callable]) -> WorkflowState:
    """运行一个完整工作流，支持断点续传"""
    # 尝试恢复
    ws = WorkflowState.load()
    if ws and ws.status == "running":
        resume = ws.get_resume_point()
        log(f"发现断点，从 {resume} 恢复")
    else:
        ws = WorkflowState()
    
    for step_id in steps:
        if step_id in ws.completed_steps:
            log(f"[SKIP] {step_id} 已完成")
            continue
        
        handler = handlers.get(step_id)
        if not handler:
            warn(f"无处理器: {step_id}")
            continue
        
        ws.start(step_id)
        try:
            result = handler()
            ws.complete(step_id, result)
            log(f"[OK] {step_id}")
        except Exception as e:
            ws.fail(step_id, str(e))
            step_info = STEPS.get(step_id, {})
            if not step_info.get("fallback"):
                log(f"[FAIL] {step_id}: 无降级方案，终止")
                break
            log(f"[FALLBACK] {step_id} -> {step_info['fallback']}")
    
    ws.finish()
    return ws


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true", help="查看工作流状态")
    ap.add_argument("--reset", action="store_true", help="重置状态机")
    args = ap.parse_args()
    
    if args.status:
        ws = WorkflowState.load()
        if ws:
            print(json.dumps(ws.summary(), ensure_ascii=False, indent=2))
        else:
            print("无活跃工作流")
    
    if args.reset:
        if STATE_FILE.exists():
            STATE_FILE.unlink()
            print("[OK] 状态机已重置")
        else:
            print("无状态文件")
