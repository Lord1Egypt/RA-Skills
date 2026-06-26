"""
Execution Monitor - 流程执行监控器
实时监控流程执行状态，记录执行日志
"""

import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ExecutionStatus(Enum):
    """执行状态"""
    PENDING = "pending"      # 待执行
    RUNNING = "running"      # 执行中
    SUCCESS = "success"      # 执行成功
    FAILED = "failed"        # 执行失败
    DEGRADED = "degraded"    # 降级执行
    RETRYING = "retrying"    # 重试中


@dataclass
class ExecutionLog:
    """执行日志条目"""
    log_id: str
    execution_id: str
    workflow_id: str
    workflow_name: str
    node_id: str
    node_name: str
    platform: str
    action: str
    status: ExecutionStatus
    start_time: float
    end_time: Optional[float] = None
    duration: float = 0.0
    result: Any = None
    error: Optional[str] = None
    retry_count: int = 0
    fallback_used: bool = False
    degraded: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class ExecutionMonitor:
    """
    流程执行监控器
    
    Features:
    - 实时监控执行状态
    - 执行日志记录
    - 异常告警通知
    - 统计报表生成
    """
    
    def __init__(self):
        """初始化监控器"""
        self.executions: Dict[str, Dict] = {}
        self.logs: List[ExecutionLog] = []
        self.notifications: List[Dict] = []
        self.stats = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'degraded_executions': 0
        }
    
    def start_execution(
        self,
        execution_id: str,
        workflow_id: str,
        workflow_name: str
    ):
        """
        开始执行监控
        
        Args:
            execution_id: 执行ID
            workflow_id: 工作流ID
            workflow_name: 工作流名称
        """
        self.executions[execution_id] = {
            'execution_id': execution_id,
            'workflow_id': workflow_id,
            'workflow_name': workflow_name,
            'status': ExecutionStatus.RUNNING,
            'start_time': time.time(),
            'nodes': [],
            'current_node': None
        }
        
        self.stats['total_executions'] += 1
    
    def log_node_start(
        self,
        execution_id: str,
        node_id: str,
        node_name: str,
        platform: str,
        action: str
    ):
        """
        记录节点开始执行
        
        Args:
            execution_id: 执行ID
            node_id: 节点ID
            node_name: 节点名称
            platform: 平台
            action: 操作
        """
        if execution_id not in self.executions:
            return
        
        self.executions[execution_id]['current_node'] = node_id
        
        log_entry = ExecutionLog(
            log_id=f"log_{len(self.logs)}",
            execution_id=execution_id,
            workflow_id=self.executions[execution_id]['workflow_id'],
            workflow_name=self.executions[execution_id]['workflow_name'],
            node_id=node_id,
            node_name=node_name,
            platform=platform,
            action=action,
            status=ExecutionStatus.RUNNING,
            start_time=time.time()
        )
        
        self.logs.append(log_entry)
    
    def log_node_complete(
        self,
        execution_id: str,
        node_id: str,
        status: ExecutionStatus,
        result: Any = None,
        error: str = None,
        fallback_used: bool = False,
        degraded: bool = False
    ):
        """
        记录节点执行完成
        
        Args:
            execution_id: 执行ID
            node_id: 节点ID
            status: 状态
            result: 结果
            error: 错误信息
            fallback_used: 是否使用了备用工具
            degraded: 是否降级执行
        """
        # 更新日志条目
        for log in reversed(self.logs):
            if log.execution_id == execution_id and log.node_id == node_id:
                log.status = status
                log.end_time = time.time()
                log.duration = log.end_time - log.start_time
                log.result = result
                log.error = error
                log.fallback_used = fallback_used
                log.degraded = degraded
                break
        
        # 更新执行统计
        if status == ExecutionStatus.SUCCESS:
            self.stats['successful_executions'] += 1
        elif status == ExecutionStatus.FAILED:
            self.stats['failed_executions'] += 1
        elif status == ExecutionStatus.DEGRADED:
            self.stats['degraded_executions'] += 1
    
    def complete_execution(
        self,
        execution_id: str,
        success: bool,
        error_message: str = None
    ):
        """
        完成执行监控
        
        Args:
            execution_id: 执行ID
            success: 是否成功
            error_message: 错误信息
        """
        if execution_id not in self.executions:
            return
        
        execution = self.executions[execution_id]
        execution['status'] = ExecutionStatus.SUCCESS if success else ExecutionStatus.FAILED
        execution['end_time'] = time.time()
        execution['duration'] = execution['end_time'] - execution['start_time']
        execution['error_message'] = error_message
        
        # 发送通知
        self._send_notification(execution)
    
    def _send_notification(self, execution: Dict):
        """发送执行完成通知"""
        status_icon = "✓" if execution['status'] == ExecutionStatus.SUCCESS else "✗"
        status_text = "成功" if execution['status'] == ExecutionStatus.SUCCESS else "失败"
        
        notification = {
            'timestamp': datetime.now().isoformat(),
            'type': 'workflow_execution',
            'execution_id': execution['execution_id'],
            'workflow_name': execution['workflow_name'],
            'status': status_text,
            'message': f"流程 '{execution['workflow_name']}' 执行{status_text}",
            'duration': f"{execution.get('duration', 0):.2f}秒"
        }
        
        self.notifications.append(notification)
    
    def get_execution_status(self, execution_id: str) -> Optional[Dict]:
        """
        获取执行状态
        
        Args:
            execution_id: 执行ID
            
        Returns:
            Dict or None
        """
        return self.executions.get(execution_id)
    
    def get_execution_logs(
        self,
        execution_id: str = None,
        workflow_id: str = None,
        start_time: float = None,
        end_time: float = None
    ) -> List[ExecutionLog]:
        """
        获取执行日志
        
        Args:
            execution_id: 执行ID筛选
            workflow_id: 工作流ID筛选
            start_time: 开始时间筛选
            end_time: 结束时间筛选
            
        Returns:
            List[ExecutionLog]: 日志列表
        """
        logs = self.logs
        
        if execution_id:
            logs = [log for log in logs if log.execution_id == execution_id]
        
        if workflow_id:
            logs = [log for log in logs if log.workflow_id == workflow_id]
        
        if start_time:
            logs = [log for log in logs if log.start_time >= start_time]
        
        if end_time:
            logs = [log for log in logs if log.start_time <= end_time]
        
        return logs
    
    def get_execution_report(self, execution_id: str) -> Optional[Dict]:
        """
        生成执行报告
        
        Args:
            execution_id: 执行ID
            
        Returns:
            Dict or None
        """
        if execution_id not in self.executions:
            return None
        
        execution = self.executions[execution_id]
        logs = self.get_execution_logs(execution_id=execution_id)
        
        # 统计各状态节点数
        status_counts = {}
        for log in logs:
            status = log.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            'execution_id': execution_id,
            'workflow_name': execution['workflow_name'],
            'status': execution['status'].value,
            'start_time': datetime.fromtimestamp(execution['start_time']).isoformat(),
            'end_time': datetime.fromtimestamp(execution['end_time']).isoformat() if execution.get('end_time') else None,
            'duration': execution.get('duration', 0),
            'error_message': execution.get('error_message'),
            'node_count': len(logs),
            'status_summary': status_counts,
            'logs': [
                {
                    'node_name': log.node_name,
                    'platform': log.platform,
                    'action': log.action,
                    'status': log.status.value,
                    'duration': log.duration,
                    'error': log.error,
                    'fallback_used': log.fallback_used,
                    'degraded': log.degraded
                }
                for log in logs
            ]
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取执行统计"""
        total = self.stats['total_executions']
        success = self.stats['successful_executions']
        failed = self.stats['failed_executions']
        degraded = self.stats['degraded_executions']
        
        success_rate = (success / total * 100) if total > 0 else 0
        
        return {
            'total_executions': total,
            'successful': success,
            'failed': failed,
            'degraded': degraded,
            'success_rate': f"{success_rate:.2f}%",
            'average_duration': self._calculate_average_duration()
        }
    
    def _calculate_average_duration(self) -> float:
        """计算平均执行时长"""
        completed = [e for e in self.executions.values() if e.get('end_time')]
        if not completed:
            return 0.0
        
        total_duration = sum(e['duration'] for e in completed)
        return total_duration / len(completed)
    
    def export_logs(
        self,
        format: str = 'json',
        filepath: str = None,
        execution_id: str = None
    ) -> str:
        """
        导出日志
        
        Args:
            format: 导出格式 (json/csv)
            filepath: 导出路径
            execution_id: 指定执行ID
            
        Returns:
            str: 导出文件路径
        """
        logs = self.get_execution_logs(execution_id=execution_id)
        
        if not filepath:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = f"execution_logs_{timestamp}.{format}"
        
        if format == 'json':
            data = [
                {
                    'log_id': log.log_id,
                    'execution_id': log.execution_id,
                    'workflow_name': log.workflow_name,
                    'node_name': log.node_name,
                    'platform': log.platform,
                    'action': log.action,
                    'status': log.status.value,
                    'duration': log.duration,
                    'error': log.error,
                    'timestamp': datetime.fromtimestamp(log.start_time).isoformat()
                }
                for log in logs
            ]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        elif format == 'csv':
            import csv
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    '时间', '执行ID', '流程名称', '节点', '平台', '操作', '状态', '耗时(秒)'
                ])
                
                for log in logs:
                    writer.writerow([
                        datetime.fromtimestamp(log.start_time).strftime('%Y-%m-%d %H:%M:%S'),
                        log.execution_id,
                        log.workflow_name,
                        log.node_name,
                        log.platform,
                        log.action,
                        log.status.value,
                        f"{log.duration:.2f}"
                    ])
        
        return filepath
    
    def get_notifications(self, limit: int = 10) -> List[Dict]:
        """获取通知列表"""
        return self.notifications[-limit:]
    
    def clear_notifications(self):
        """清空通知"""
        self.notifications = []