"""
ClawHub Retry & Fallback Skill - 使用示例
Basic Usage Examples - 基础到高级用法完整示例
"""

import json
import random
import sys
import time
import os

# 添加scripts到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 导入所有核心模块
from scripts.retry_handler import RetryHandler, RetryResult
from scripts.exception_classifier import ExceptionClassifier, ExceptionCategory
from scripts.fallback_manager import FallbackManager, FallbackPriority
from scripts.degradation_handler import DegradationHandler, TaskStep, StepPriority, DegradationLevel
from scripts.audit_logger import AuditLogger
from scripts.config_manager import ConfigManager


def example_1_basic_retry():
    """示例1: 基础重试功能 - 装饰器方式"""
    print("=" * 60)
    print("示例1: 基础重试功能 - 装饰器方式")
    print("=" * 60)
    
    handler = RetryHandler()
    call_count = [0]
    
    @handler.with_retry(max_attempts=3, backoff_strategy='exponential')
    def unreliable_api():
        """模拟不可靠的API调用"""
        call_count[0] += 1
        
        # 前2次调用失败，第3次成功
        if call_count[0] < 3:
            raise ConnectionError(f"连接超时 (尝试 {call_count[0]})")
        
        return {"status": "success", "data": "API响应数据"}
    
    result = unreliable_api()
    
    print(f"✓ 调用次数: {call_count[0]}")
    print(f"✓ 返回结果: {result}")
    print()


def example_2_programmatic_retry():
    """示例2: 编程式重试调用"""
    print("=" * 60)
    print("示例2: 编程式重试调用")
    print("=" * 60)
    
    handler = RetryHandler()
    call_count = [0]
    
    def unstable_function(param1, param2):
        call_count[0] += 1
        if call_count[0] < 3:
            raise TimeoutError(f"超时 #{call_count[0]}")
        return {"param1": param1, "param2": param2, "status": "ok"}
    
    # 编程式调用，获取完整结果
    result = handler.execute_with_retry(
        func=unstable_function,
        args=("value1", "value2"),
        max_attempts=3,
        backoff_strategy='exponential'
    )
    
    print(f"✓ 是否成功: {result.success}")
    print(f"✓ 尝试次数: {result.attempts}")
    print(f"✓ 总耗时: {result.total_duration:.3f}s")
    print(f"✓ 结果: {result.result}")
    print(f"✓ 重试历史: {len(result.retry_history)} 次")
    for h in result.retry_history:
        print(f"  - 尝试 {h['attempt']}: {h['exception_type']} - {h['category']}")
    print()


def example_3_exception_classification():
    """示例3: 异常分类与识别"""
    print("=" * 60)
    print("示例3: 异常分类与识别")
    print("=" * 60)
    
    classifier = ExceptionClassifier()
    
    # 测试不同类型的异常
    test_cases = [
        ConnectionError("网络连接失败"),
        TimeoutError("请求超时"),
        ValueError("参数错误：缺少必填字段"),
        PermissionError("权限不足，无法访问资源"),
    ]
    
    print("异常分类结果:")
    for exc in test_cases:
        category = classifier.classify(exc)
        is_retryable = classifier.is_retryable(exc)
        details = classifier.get_exception_details(exc)
        
        retry_icon = "✓" if is_retryable else "✗"
        print(f"  {retry_icon} {exc.__class__.__name__}: {category.value}")
        print(f"    建议: {details['recommendation']}")
    
    # HTTP状态码测试
    print("\nHTTP状态码分类:")
    status_codes = [429, 503, 400, 404, 500]
    for code in status_codes:
        is_retryable = classifier.is_retryable({'status_code': code})
        icon = "✓" if is_retryable else "✗"
        print(f"  {icon} HTTP {code}: {'可重试' if is_retryable else '不可重试'}")
    print()


def example_4_fallback_switching():
    """示例4: 备用工具自动切换"""
    print("=" * 60)
    print("示例4: 备用工具自动切换")
    print("=" * 60)
    
    fallback = FallbackManager()
    
    # 主工具（会失败）
    def primary_weather_api(city: str):
        print(f"  [主API] 调用失败: 服务不可用")
        raise ConnectionError("主API服务不可用")
    
    # 备用工具1
    def backup_weather_api_v1(location: str):
        print(f"  [备用API v1] 调用成功")
        return {"city": location, "weather": "晴朗", "temp": "25°C", "source": "v1"}
    
    # 备用工具2
    def backup_weather_api_v2(location: str):
        print(f"  [备用API v2] 调用成功")
        return {"city": location, "weather": "多云", "temp": "23°C", "source": "v2"}
    
    # 注册备用工具（带优先级）
    fallback.register_backup(
        primary='weather_primary',
        backup='weather_backup_v1',
        backup_func=backup_weather_api_v1,
        param_mapping={'city': 'location'},  # 参数映射
        priority=FallbackPriority.HIGH_QUALITY,
        success_rate=0.95
    )
    
    fallback.register_backup(
        primary='weather_primary',
        backup='weather_backup_v2',
        backup_func=backup_weather_api_v2,
        param_mapping={'city': 'location'},
        priority=FallbackPriority.STANDARD,
        success_rate=0.90
    )
    
    # 执行并自动切换
    print("执行流程:")
    result = fallback.execute_with_fallback(
        primary_func=primary_weather_api,
        primary_name='weather_primary',
        args=(),
        kwargs={'city': '北京'},
        on_switch=lambda p, b, c: print(f"  → 切换到备用工具: {b} (第{c}次切换)")
    )
    
    print(f"\n✓ 切换成功: {result.success}")
    print(f"✓ 使用的工具: {result.backup_tool or result.primary_tool}")
    print(f"✓ 切换次数: {result.switch_count}")
    print(f"✓ 执行耗时: {result.duration:.3f}s")
    print(f"✓ 结果: {result.result}")
    print()


def example_5_degradation():
    """示例5: 三级降级处理机制"""
    print("=" * 60)
    print("示例5: 三级降级处理机制")
    print("=" * 60)
    
    degradation = DegradationHandler()
    
    # 场景1: 轻度降级（跳过可选步骤）
    print("\n【场景1: 轻度降级 - 跳过可选步骤】")
    steps = [
        TaskStep(name="fetch_data", func=lambda: {"users": ["u1", "u2"]}, priority=StepPriority.CRITICAL),
        TaskStep(name="enrich_data", func=lambda: (_ for _ in ()).throw(Exception("增强服务不可用")), priority=StepPriority.OPTIONAL),
        TaskStep(name="generate_report", func=lambda: "报告已生成", priority=StepPriority.IMPORTANT)
    ]
    
    result = degradation.execute_with_degradation(steps)
    
    print(f"✓ 执行成功: {result.success}")
    print(f"✓ 降级等级: {result.level.name}")
    print(f"✓ 完成步骤: {result.completed_steps}")
    print(f"✓ 跳过步骤: {result.skipped_steps}")
    
    # 场景2: 中度降级（保留已完成结果）
    print("\n【场景2: 中度降级 - 保留已完成结果】")
    steps2 = [
        TaskStep(name="fetch_data", func=lambda: {"data": "原始数据"}, priority=StepPriority.CRITICAL),
        TaskStep(name="process_data", func=lambda: (_ for _ in ()).throw(Exception("处理失败")), priority=StepPriority.CRITICAL),
        TaskStep(name="save_result", func=lambda: "保存完成", priority=StepPriority.IMPORTANT)
    ]
    
    result2 = degradation.execute_with_degradation(steps2)
    
    print(f"✓ 执行成功: {result2.success}")
    print(f"✓ 降级等级: {result2.level.name}")
    print(f"✓ 完成步骤: {result2.completed_steps}")
    print(f"✓ 失败步骤: {result2.failed_steps}")
    print(f"✓ 可用结果: {result2.results}")
    
    # 场景3: 重度降级（输出分析报告）
    print("\n【场景3: 重度降级 - 核心步骤完全失败】")
    steps3 = [
        TaskStep(name="init", func=lambda: "初始化完成", priority=StepPriority.OPTIONAL),
        TaskStep(name="core_process", func=lambda: (_ for _ in ()).throw(Exception("核心处理失败")), priority=StepPriority.CRITICAL),
    ]
    
    result3 = degradation.execute_with_degradation(steps3)
    
    print(f"✓ 执行成功: {result3.success}")
    print(f"✓ 降级等级: {result3.level.name}")
    print(f"✓ 是否包含根因分析: {'root_cause_analysis' in result3.report}")
    print()


def example_6_audit_logging():
    """示例6: 审计日志与报告"""
    print("=" * 60)
    print("示例6: 审计日志与报告")
    print("=" * 60)
    
    logger = AuditLogger()
    
    task_id = "task-001"
    
    # 记录重试操作
    logger.log_retry(
        task_id=task_id,
        exception_type="ConnectionTimeout",
        attempt=1,
        max_attempts=3,
        delay=1.0,
        exception_message="连接超时"
    )
    
    logger.log_retry(
        task_id=task_id,
        exception_type="ConnectionTimeout",
        attempt=2,
        max_attempts=3,
        delay=3.0,
        exception_message="连接超时"
    )
    
    # 记录备用工具切换
    logger.log_fallback(
        task_id=task_id,
        primary_tool="api_v1",
        backup_tool="api_v2",
        success=True,
        param_mapping={"city": "location"},
        duration=2.5
    )
    
    # 记录降级操作
    logger.log_degradation(
        task_id=task_id,
        level="LIGHT",
        failed_step="enrich_data",
        error="服务不可用",
        completed_steps=["fetch_data"],
        skipped_steps=["enrich_data"]
    )
    
    # 记录任务完成
    logger.log_task_completion(
        task_id=task_id,
        success=True,
        execution_time=5.2,
        retry_count=2,
        fallback_count=1,
        degradation_level="LIGHT"
    )
    
    # 查询日志
    logs = logger.get_logs(task_id=task_id)
    print(f"✓ 任务日志数量: {len(logs)}")
    print(f"  - 重试日志: {len([l for l in logs if l.operation == 'retry'])}")
    print(f"  - 切换日志: {len([l for l in logs if l.operation == 'fallback'])}")
    print(f"  - 降级日志: {len([l for l in logs if l.operation == 'degradation'])}")
    
    # 生成报告
    report = logger.generate_report(task_id)
    print(f"\n执行报告:")
    print(f"  - 任务ID: {report['task_id']}")
    print(f"  - 总操作数: {report['execution_summary']['total_operations']}")
    print(f"  - 重试次数: {report['execution_summary']['retry_count']}")
    print(f"  - 切换次数: {report['execution_summary']['fallback_count']}")
    
    # 导出日志（示例）
    # filepath = logger.export_logs(format='json', task_id=task_id)
    # print(f"\n✓ 日志已导出: {filepath}")
    print()


def example_7_config_management():
    """示例7: 配置管理"""
    print("=" * 60)
    print("示例7: 配置管理")
    print("=" * 60)
    
    config = ConfigManager()
    
    # 查看默认策略
    print("【平台默认策略】")
    for policy_name in ['network_timeout', 'rate_limit', 'server_error']:
        policy = config.get_policy(policy_name)
        print(f"  {policy_name}:")
        print(f"    - 最大重试: {policy.max_attempts}")
        print(f"    - 退避策略: {policy.backoff_strategy}")
        print(f"    - 间隔: {policy.delays}")
    
    # 查看异常规则
    print("\n【异常分类规则】")
    rules = config.get_exception_rules()
    print(f"  可重试异常: {len(rules.retryable)} 种")
    print(f"  不可重试异常: {len(rules.non_retryable)} 种")
    
    # 测试异常分类
    print("\n【异常分类测试】")
    test_cases = [
        ('ConnectionError', True),
        ('TimeoutError', True),
        ('ValueError', False),
        ('429', True),
        ('404', False),
    ]
    for exc_name, expected in test_cases:
        result = config.is_retryable_exception(exc_name)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {exc_name}: {'可重试' if result else '不可重试'}")
    
    # 平台限制
    print("\n【平台强制限制】")
    limits = config.get_platform_limits()
    for key, value in limits.items():
        print(f"  - {key}: {value}")
    print()


def example_8_real_world_scenario():
    """示例8: 真实场景 - 数据处理管道"""
    print("=" * 60)
    print("示例8: 真实场景 - 数据处理管道")
    print("=" * 60)
    
    # 模拟外部服务
    class MockServices:
        @staticmethod
        def fetch_from_api():
            if random.random() < 0.3:
                raise ConnectionError("API连接失败")
            return {"raw_data": [1, 2, 3, 4, 5]}
        
        @staticmethod
        def ai_enhance_v1(data):
            if random.random() < 0.5:
                raise TimeoutError("AI服务v1超时")
            return {"enhanced": True, "data": data}
        
        @staticmethod
        def ai_enhance_v2(data):
            # 更稳定的备用服务
            return {"enhanced": True, "data": data, "source": "v2"}
        
        @staticmethod
        def save_to_db(result):
            return {"saved": True, "id": "record-123"}
    
    services = MockServices()
    
    # 初始化组件
    handler = RetryHandler()
    fallback = FallbackManager()
    degradation = DegradationHandler()
    logger = AuditLogger()
    
    task_id = "data-pipeline-001"
    
    # 注册备用AI服务
    fallback.register_backup(
        primary='ai-enhance',
        backup='ai-enhance-v2',
        backup_func=services.ai_enhance_v2,
        priority=FallbackPriority.HIGH_QUALITY
    )
    
    print("执行数据处理管道:\n")
    
    # 步骤1: 获取数据（带重试）
    @handler.with_retry(max_attempts=3)
    def step_fetch():
        print("  [1/3] 从API获取数据...")
        result = services.fetch_from_api()
        print(f"      ✓ 成功获取 {len(result['raw_data'])} 条数据")
        return result
    
    # 步骤2: AI增强（带备用工具）
    def step_enhance(data):
        print("  [2/3] AI增强处理...")
        try:
            return services.ai_enhance_v1(data)
        except TimeoutError:
            print("      ! v1失败，切换到v2...")
            return services.ai_enhance_v2(data)
    
    # 步骤3: 保存结果
    def step_save(enhanced_data):
        print("  [3/3] 保存到数据库...")
        return services.save_to_db(enhanced_data)
    
    # 构建任务链
    steps = [
        TaskStep(name="fetch", func=step_fetch, priority=StepPriority.CRITICAL),
        TaskStep(name="enhance", func=lambda: fallback.execute_with_fallback(
            services.ai_enhance_v1, 'ai-enhance', args=(step_fetch(),)
        ).result, priority=StepPriority.IMPORTANT),
        TaskStep(name="save", func=lambda: step_save(step_enhance(step_fetch())), priority=StepPriority.CRITICAL)
    ]
    
    # 执行任务
    result = degradation.execute_with_degradation(steps)
    
    print(f"\n执行结果:")
    print(f"  ✓ 整体成功: {result.success}")
    print(f"  ✓ 降级等级: {result.level.name}")
    print(f"  ✓ 完成步骤: {result.completed_steps}")
    print(f"  ✓ 总耗时: {result.duration:.3f}s")
    print()


def example_9_callback_hooks():
    """示例9: 使用回调函数监控执行"""
    print("=" * 60)
    print("示例9: 使用回调函数监控执行")
    print("=" * 60)
    
    handler = RetryHandler()
    
    retry_events = []
    
    def on_retry(exception, attempt, delay):
        retry_events.append({
            'type': 'retry',
            'attempt': attempt,
            'exception': exception.__class__.__name__,
            'delay': delay
        })
        print(f"  [重试回调] 第{attempt}次重试，等待{delay:.1f}秒...")
    
    def on_failure(exception, attempt, max_attempts):
        retry_events.append({
            'type': 'failure',
            'attempt': attempt,
            'exception': exception.__class__.__name__
        })
        print(f"  [失败回调] 最终失败于第{attempt}次尝试")
    
    call_count = [0]
    
    @handler.with_retry(
        max_attempts=3,
        on_retry=on_retry,
        on_failure=on_failure
    )
    def monitored_operation():
        call_count[0] += 1
        if call_count[0] < 3:
            raise ConnectionError(f"失败 #{call_count[0]}")
        return "成功!"
    
    print("执行监控操作:\n")
    result = monitored_operation()
    
    print(f"\n监控事件: {len(retry_events)} 个")
    for event in retry_events:
        print(f"  - {event['type']}: attempt={event.get('attempt')}")
    print(f"最终结果: {result}")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("ClawHub Retry & Fallback Skill")
    print("工具调用失败自动重试与降级处理")
    print("=" * 60 + "\n")
    
    examples = [
        ("基础重试", example_1_basic_retry),
        ("编程式重试", example_2_programmatic_retry),
        ("异常分类", example_3_exception_classification),
        ("备用工具切换", example_4_fallback_switching),
        ("降级处理", example_5_degradation),
        ("审计日志", example_6_audit_logging),
        ("配置管理", example_7_config_management),
        ("真实场景", example_8_real_world_scenario),
        ("回调监控", example_9_callback_hooks),
    ]
    
    print(f"共有 {len(examples)} 个示例\n")
    print("-" * 60)
    
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n✗ 示例 '{name}' 执行出错: {e}\n")
        print("-" * 60)
    
    print("\n" + "=" * 60)
    print("所有示例执行完成!")
    print("=" * 60)