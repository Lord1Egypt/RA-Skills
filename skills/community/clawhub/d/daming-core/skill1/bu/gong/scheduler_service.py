#!/usr/bin/env python3
"""
工部调度器服务
定时扫描并执行待处理任务
"""

import time
import logging
import signal
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 导入调度器
# 生产环境需要配置项目根目录
import os
project_root = os.environ.get("PROJECT_ROOT", "{{PROJECT_ROOT}}")
sys.path.append(project_root)
from skill1.bu.gong.scheduler import GongBuScheduler


class SchedulerService:
    """调度器服务"""
    
    def __init__(self, interval_seconds: int = 60):
        """初始化服务"""
        self.interval_seconds = interval_seconds
        self.running = False
        self.scheduler = GongBuScheduler()
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        logger.info(f"调度器服务初始化完成，检查间隔: {interval_seconds}秒")
    
    def signal_handler(self, signum, frame):
        """信号处理"""
        logger.info(f"收到信号 {signum}，准备停止服务")
        self.running = False
    
    def run_once(self) -> bool:
        """运行一次任务处理"""
        try:
            logger.info("开始扫描待执行任务")
            
            # 处理待执行任务
            result = self.scheduler.process_pending_tasks()
            
            if result["success"]:
                processed_count = result.get("processed_count", 0)
                if processed_count > 0:
                    logger.info(f"成功处理 {processed_count} 个任务")
                    
                    # 记录处理结果
                    for task_result in result.get("results", []):
                        task_id = task_result.get("task_id")
                        success = task_result.get("success", False)
                        message = task_result.get("message", "")
                        
                        if success:
                            logger.info(f"✅ 任务 {task_id} 执行成功: {message}")
                        else:
                            logger.warning(f"❌ 任务 {task_id} 执行失败: {message}")
                else:
                    logger.info("没有待执行任务")
            else:
                logger.error(f"任务处理失败: {result.get('message')}")
            
            return result["success"]
        
        except Exception as e:
            logger.error(f"任务处理异常: {str(e)}")
            return False
    
    def run(self):
        """运行服务"""
        self.running = True
        logger.info("调度器服务启动")
        
        cycle_count = 0
        
        while self.running:
            try:
                cycle_count += 1
                logger.info(f"=== 调度周期 #{cycle_count} ===")
                
                # 运行一次处理
                success = self.run_once()
                
                if not success:
                    logger.warning("本次处理失败，等待下一个周期")
                
                # 等待下一个周期
                logger.info(f"等待 {self.interval_seconds} 秒后继续...")
                
                # 分段等待，以便能够响应信号
                for _ in range(self.interval_seconds):
                    if not self.running:
                        break
                    time.sleep(1)
            
            except KeyboardInterrupt:
                logger.info("收到键盘中断，停止服务")
                self.running = False
                break
            
            except Exception as e:
                logger.error(f"调度周期异常: {str(e)}")
                time.sleep(10)  # 异常后等待10秒
        
        logger.info("调度器服务停止")
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return {
            "status": "running" if self.running else "stopped",
            "started_at": getattr(self, "start_time", None),
            "cycle_count": getattr(self, "cycle_count", 0),
            "service": "gong_scheduler"
        }


def main():
    """主函数"""
    print("""
    🏛️ 工部调度器服务
    ====================
    功能: 定时扫描并执行待处理任务
    配置: 检查间隔 60 秒
    日志: {{PROJECT_ROOT}}/logs/scheduler_service.log
    """)
    
    # 创建日志目录
    project_root = os.environ.get("PROJECT_ROOT", "{{PROJECT_ROOT}}")
    log_dir = Path(project_root) / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # 创建服务
    service = SchedulerService(interval_seconds=60)
    
    # 记录启动时间
    service.start_time = datetime.now().isoformat()
    service.cycle_count = 0
    
    # 运行服务
    service.run()


if __name__ == "__main__":
    main()