#!/usr/bin/env python3
"""
意向性守护协程

功能：
- 独立运行的外环守护进程（协程级别）
- 持续收集、分类、分析意向性数据
- 生成软调节建议并推送到建议池
- 实现真正的"阴性后台默默运行"

设计原则：
- 完全独立运行，不依赖主循环触发
- 轻量级轮询，非阻塞
- 异常隔离，崩溃不影响主循环
- 支持优雅启动和停止

架构设计：
┌─────────────────────────────────────────────────────────┐
│         intentionality_daemon (守护协程)                  │
│                                                           │
│  while running:                                           │
│    1. 收集意向性数据 (collector)                          │
│    2. 分类 (classifier)                                    │
│    3. 三维分析 (analyzer)                                 │
│    4. 生成软调节 (regulator)                              │
│    5. 推送到建议池 (advice_pool)                          │
│    6. 轻量级休眠 (100ms)                                  │
└─────────────────────────────────────────────────────────┘
           ↓                    ↓                    ↓
    collection_queue     classification_queue    advice_queue
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

# 导入同步版本组件（后续会异步化）
from intentionality_collector import IntentionalityCollector
from intentionality_classifier import IntentionalityClassifier
from intentionality_analyzer import IntentionalityAnalyzer
from intentionality_regulator import IntentionalityRegulator
from intentionality_trigger import IntentionalityTrigger

# 导入异步建议池
from memory_store_async import AsyncMemoryStore


class IntentionalityDaemon:
    """意向性守护协程（外环独立运行）"""

    def __init__(self, memory_dir: str = "./agi_memory", advice_pool=None):
        """
        初始化守护协程

        Args:
            memory_dir: 记忆存储目录
            advice_pool: 建议池实例（AsyncAdvicePool）
        """
        self.memory_dir = Path(memory_dir)
        self.running = False
        self.advice_pool = advice_pool

        # 初始化各个组件
        self.collector = IntentionalityCollector()
        self.classifier = IntentionalityClassifier()
        self.analyzer = IntentionalityAnalyzer()
        self.regulator = IntentionalityRegulator()
        self.trigger = IntentionalityTrigger()

        # 内部队列（用于组件间传递数据）
        self.collection_queue = asyncio.Queue(maxsize=1000)
        self.classification_queue = asyncio.Queue(maxsize=1000)
        self.analysis_queue = asyncio.Queue(maxsize=1000)

        # 统计信息
        self.stats = {
            'total_iterations': 0,
            'total_collected': 0,
            'total_classified': 0,
            'total_analyzed': 0,
            'total_regulations': 0,
            'last_activity': None,
            'errors': 0
        }

        # 配置
        self.poll_interval = 0.1  # 100ms轮询间隔
        self.max_queue_size = 1000

        # 日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('IntentionalityDaemon')

    async def start(self):
        """启动守护协程"""
        if self.running:
            self.logger.warning("守护协程已在运行")
            return

        self.running = True
        self.logger.info("意向性守护协程启动")

        # 启动所有阶段
        tasks = [
            asyncio.create_task(self._collection_loop()),
            asyncio.create_task(self._classification_loop()),
            asyncio.create_task(self._analysis_loop()),
            asyncio.create_task(self._regulation_loop())
        ]

        # 等待所有任务完成（理论上不会完成，除非stop被调用）
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            self.logger.error(f"守护协程异常: {e}", exc_info=True)
            self.running = False

    async def stop(self):
        """停止守护协程"""
        self.running = False
        self.logger.info("意向性守护协程停止")

        # 等待队列清空
        await asyncio.sleep(0.5)

        # 打印统计信息
        self.logger.info(f"守护协程统计: {self.stats}")

    async def _collection_loop(self):
        """收集循环：持续收集意向性数据"""
        self.logger.info("收集循环启动")

        while self.running:
            try:
                # 模拟收集数据（实际应该从消息队列获取）
                # 这里先模拟空运行，后续会集成真正的数据源
                # data = await self.collection_queue.get(timeout=0.05)
                # await self.classification_queue.put(data)
                
                # 轻量级休眠
                await asyncio.sleep(self.poll_interval)

                self.stats['total_iterations'] += 1

            except asyncio.TimeoutError:
                # 超时是正常的，继续循环
                continue
            except Exception as e:
                self.logger.error(f"收集循环异常: {e}", exc_info=True)
                self.stats['errors'] += 1
                await asyncio.sleep(1.0)  # 错误后休眠更长时间

    async def _classification_loop(self):
        """分类循环：对接收到的数据进行分类"""
        self.logger.info("分类循环启动")

        while self.running:
            try:
                # 获取待分类数据
                try:
                    data = await asyncio.wait_for(
                        self.classification_queue.get(),
                        timeout=0.05
                    )
                except asyncio.TimeoutError:
                    await asyncio.sleep(self.poll_interval)
                    continue

                # 分类
                classification = self.classifier.classify(data)
                self.stats['total_classified'] += 1

                # 传递到分析阶段
                await self.analysis_queue.put({
                    'original': data,
                    'classification': classification
                })

            except Exception as e:
                self.logger.error(f"分类循环异常: {e}", exc_info=True)
                self.stats['errors'] += 1
                await asyncio.sleep(1.0)

    async def _analysis_loop(self):
        """分析循环：对分类后的数据进行三维分析"""
        self.logger.info("分析循环启动")

        while self.running:
            try:
                # 获取待分析数据
                try:
                    data = await asyncio.wait_for(
                        self.analysis_queue.get(),
                        timeout=0.05
                    )
                except asyncio.TimeoutError:
                    await asyncio.sleep(self.poll_interval)
                    continue

                # 三维分析：强度/紧迫性/优先级
                analysis = self.analyzer.analyze(data['classification'])
                self.stats['total_analyzed'] += 1

                # 触发判断
                should_trigger = self.trigger.check(analysis)

                if should_trigger:
                    # 生成软调节建议
                    regulation = self.regulator.regulate(analysis)
                    self.stats['total_regulations'] += 1

                    # 推送到建议池
                    if self.advice_pool:
                        await self.advice_pool.add_advice_async(
                            vertex=regulation.get('vertex', 'iteration'),
                            suggestion=regulation
                        )
                        self.logger.info(f"生成软调节建议: {regulation.get('vertex')}")

            except Exception as e:
                self.logger.error(f"分析循环异常: {e}", exc_info=True)
                self.stats['errors'] += 1
                await asyncio.sleep(1.0)

    async def _regulation_loop(self):
        """调节循环：生成软调节建议（未来扩展）"""
        self.logger.info("调节循环启动")

        while self.running:
            try:
                # 当前调节逻辑已在analysis_loop中实现
                # 这个循环预留用于未来扩展
                await asyncio.sleep(1.0)

            except Exception as e:
                self.logger.error(f"调节循环异常: {e}", exc_info=True)
                self.stats['errors'] += 1
                await asyncio.sleep(1.0)

    async def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return self.stats.copy()

    async def add_intentionality_data(self, data: Dict[str, Any]):
        """
        添加意向性数据（供外部调用）

        Args:
            data: 意向性数据
        """
        if not self.running:
            self.logger.warning("守护协程未运行，数据被丢弃")
            return

        try:
            await asyncio.wait_for(
                self.collection_queue.put(data),
                timeout=1.0
            )
            self.stats['total_collected'] += 1
            self.logger.debug(f"收到意向性数据: {data.get('id')}")
        except asyncio.TimeoutError:
            self.logger.warning("队列已满，数据被丢弃")
        except Exception as e:
            self.logger.error(f"添加数据异常: {e}", exc_info=True)


class AsyncAdvicePool:
    """异步建议池（简化版，用于推拉机制）"""

    def __init__(self, memory_dir: str = "./agi_memory"):
        self.memory_dir = memory_dir
        self.advice_queue = asyncio.PriorityQueue(maxsize=1000)
        self.subscribers = set()
        self.stats = {
            'total_added': 0,
            'total_pulled': 0,
            'total_subscribers': 0
        }

    async def add_advice_async(self, vertex: str, suggestion: Dict[str, Any]) -> str:
        """
        添加建议（异步）

        Args:
            vertex: 目标顶点
            suggestion: 建议内容

        Returns:
            建议ID
        """
        import uuid
        from datetime import datetime, timedelta

        suggestion_with_metadata = {
            "id": str(uuid.uuid4()),
            "generation_time": datetime.now().isoformat(),
            "valid_until": (datetime.now() + timedelta(minutes=30)).isoformat(),
            "vertex": vertex,
            "priority": suggestion.get('priority', 0.5),
            "content": suggestion.get('content', ''),
            "confidence": suggestion.get('confidence', 0.5),
            "based_on_intentionality": suggestion.get('based_on_intentionality', {})
        }

        # 使用优先级队列（负数表示高优先级）
        # priority必须是数字，不能是dict
        priority = -float(suggestion_with_metadata['priority'])
        await self.advice_queue.put((priority, suggestion_with_metadata['id'], suggestion_with_metadata))

        self.stats['total_added'] += 1

        # 通知订阅者（可选功能）
        for subscriber in self.subscribers:
            asyncio.create_task(subscriber(suggestion_with_metadata))

        return suggestion_with_metadata['id']

    async def pull_advice_async(self, vertex: str = None, timeout: float = 0.1) -> Optional[Dict[str, Any]]:
        """
        拉取建议（异步）

        Args:
            vertex: 目标顶点（可选，过滤用）
            timeout: 超时时间

        Returns:
            建议对象或None
        """
        try:
            _, _, advice = await asyncio.wait_for(
                self.advice_queue.get(),
                timeout=timeout
            )

            # 如果指定了vertex，进行过滤
            if vertex and advice.get('vertex') != vertex:
                # 不匹配，放回队列
                await self.advice_queue.put((_, _, advice))
                return None

            self.stats['total_pulled'] += 1
            return advice

        except asyncio.TimeoutError:
            return None

    async def subscribe(self, callback):
        """订阅建议（可选功能）"""
        self.subscribers.add(callback)
        self.stats['total_subscribers'] += 1

    async def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        self.stats['queue_size'] = self.advice_queue.qsize()
        return self.stats.copy()


# 便捷函数
async def create_intentionality_daemon(memory_dir: str = "./agi_memory") -> IntentionalityDaemon:
    """创建并启动意向性守护协程"""
    advice_pool = AsyncAdvicePool(memory_dir)
    daemon = IntentionalityDaemon(memory_dir, advice_pool)
    asyncio.create_task(daemon.start())
    return daemon


if __name__ == "__main__":
    # 测试守护协程
    import argparse

    parser = argparse.ArgumentParser(description="意向性守护协程")
    parser.add_argument("--memory-dir", default="./agi_memory", help="记忆存储目录")
    parser.add_argument("--duration", type=int, default=10, help="运行时长（秒）")
    args = parser.parse_args()

    async def test_daemon():
        daemon = await create_intentionality_daemon(args.memory_dir)

        print(f"守护协程运行中，持续{args.duration}秒...")
        await asyncio.sleep(args.duration)

        # 打印统计信息
        stats = await daemon.get_stats()
        print(f"\n守护协程统计:")
        print(f"  总迭代次数: {stats['total_iterations']}")
        print(f"  总收集: {stats['total_collected']}")
        print(f"  总分类: {stats['total_classified']}")
        print(f"  总分析: {stats['total_analyzed']}")
        print(f"  总调节: {stats['total_regulations']}")
        print(f"  错误次数: {stats['errors']}")

        advice_pool_stats = await daemon.advice_pool.get_stats()
        print(f"\n建议池统计:")
        print(f"  总添加: {advice_pool_stats['total_added']}")
        print(f"  总拉取: {advice_pool_stats['total_pulled']}")
        print(f"  队列大小: {advice_pool_stats['queue_size']}")

        await daemon.stop()

    asyncio.run(test_daemon())
