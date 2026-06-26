"""
Amazon监控任务调度模块
功能：创建和管理定时监控任务，支持触发条件
"""
import json
import os
from datetime import datetime
from amazon_monitor_core import get_product_data, save_history, generate_trend_chart, check_trigger_conditions

# 任务配置文件
TASK_CONFIG_FILE = "amazon_monitor_tasks.json"


def create_monitor_task(asin, zip_code="10001", frequency_minutes=5, 
                        triggers=None, enabled=True):
    """
    创建监控任务
    triggers: 触发条件 dict
        {
            'price_change': True/False,  # 价格变化时通知
            'review_change': True/False,  # 评论数变化时通知
            'rating_change': True/False,  # 星级变化时通知
            'link_invalid': True/False    # 链接失效时通知
        }
    """
    if triggers is None:
        triggers = {
            'price_change': True,
            'review_change': True,
            'rating_change': False,
            'link_invalid': True
        }
    
    task = {
        'asin': asin,
        'zipCode': zip_code,
        'frequencyMinutes': frequency_minutes,
        'triggers': triggers,
        'enabled': enabled,
        'createdAt': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'lastRun': None,
        'lastData': None,
        'alertCount': 0
    }
    
    # 加载现有任务
    tasks = load_tasks()
    
    # 检查是否已存在相同ASIN的任务
    existing_idx = None
    for i, t in enumerate(tasks):
        if t['asin'] == asin:
            existing_idx = i
            break
    
    if existing_idx is not None:
        tasks[existing_idx] = task
        print(f"已更新ASIN {asin}的监控任务")
    else:
        tasks.append(task)
        print(f"已创建ASIN {asin}的监控任务")
    
    save_tasks(tasks)
    
    return task


def load_tasks():
    """加载所有任务"""
    if os.path.exists(TASK_CONFIG_FILE):
        try:
            with open(TASK_CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_tasks(tasks):
    """保存任务列表"""
    with open(TASK_CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def delete_task(asin):
    """删除任务"""
    tasks = load_tasks()
    tasks = [t for t in tasks if t['asin'] != asin]
    save_tasks(tasks)
    print(f"已删除ASIN {asin}的监控任务")


def list_tasks():
    """列出所有任务"""
    tasks = load_tasks()
    if not tasks:
        print("暂无监控任务")
        return
    
    print(f"\n{'='*60}")
    print(f"Amazon监控任务列表 (共{len(tasks)}个)")
    print(f"{'='*60}")
    
    for i, task in enumerate(tasks, 1):
        status = "启用" if task.get('enabled', True) else "停用"
        print(f"\n[{i}] ASIN: {task['asin']}")
        print(f"    邮编: {task.get('zipCode', '10001')}")
        print(f"    频率: 每{task.get('frequencyMinutes', 5)}分钟")
        print(f"    状态: {status}")
        print(f"    触发条件:")
        triggers = task.get('triggers', {})
        print(f"      - 价格变化: {'是' if triggers.get('price_change') else '否'}")
        print(f"      - 评论变化: {'是' if triggers.get('review_change') else '否'}")
        print(f"      - 星级变化: {'是' if triggers.get('rating_change') else '否'}")
        print(f"      - 链接失效: {'是' if triggers.get('link_invalid') else '否'}")
        print(f"    最后运行: {task.get('lastRun', '从未运行')}")
        print(f"    警报次数: {task.get('alertCount', 0)}")


def run_task(asin, verbose=True):
    """
    运行单个监控任务
    返回: (是否发送警报, 警报消息)
    """
    tasks = load_tasks()
    task = None
    for t in tasks:
        if t['asin'] == asin:
            task = t
            break
    
    if not task:
        return False, f"未找到ASIN {asin}的任务"
    
    if not task.get('enabled', True):
        return False, f"ASIN {asin}的任务已停用"
    
    zip_code = task.get('zipCode', '10001')
    
    if verbose:
        print(f"运行监控任务: ASIN={asin}, 邮编={zip_code}")
    
    # 获取当前数据
    data = get_product_data(asin, zip_code)
    
    # 检查链接有效性
    if not data.get('valid', True):
        error_msg = f"⚠️ 链接失效! ASIN: {asin}"
        if verbose:
            print(error_msg)
        
        # 更新任务状态
        task['lastRun'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        task['lastData'] = data
        
        triggers = task.get('triggers', {})
        if triggers.get('link_invalid', True):
            task['alertCount'] = task.get('alertCount', 0) + 1
            save_tasks(tasks)
            return True, error_msg
        return False, None
    
    # 保存历史数据
    history = save_history(asin, data, zip_code)
    
    # 获取上次数据
    previous_data = task.get('lastData')
    
    # 检查触发条件
    trigger_results = check_trigger_conditions(data, previous_data)
    
    # 更新任务状态
    task['lastRun'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    task['lastData'] = data
    save_tasks(tasks)
    
    # 生成趋势图
    chart_file = None
    if len(history) >= 2:
        chart_file = generate_trend_chart(asin, history)
    
    # 检查是否有触发
    alerts = []
    triggers = task.get('triggers', {})
    
    for condition, (triggered, message) in trigger_results.items():
        if triggered and triggers.get(condition, False):
            alerts.append(message)
    
    if verbose:
        print(f"商品名称: {data.get('productName', '')[:50]}...")
        print(f"价格: {data.get('price')}")
        print(f"星级: {data.get('rating')}")
        print(f"评论数: {data.get('reviewCount')}")
        
        if alerts:
            print(f"\n⚠️ 触发警报 ({len(alerts)}个):")
            for alert in alerts:
                print(f"  - {alert}")
        else:
            print("\n✓ 无异常")
    
    should_alert = len(alerts) > 0
    alert_msg = "\n".join(alerts) if alerts else None
    
    return should_alert, alert_msg


def run_all_tasks(verbose=True):
    """运行所有启用的任务"""
    tasks = load_tasks()
    enabled_tasks = [t for t in tasks if t.get('enabled', True)]
    
    if not enabled_tasks:
        print("没有启用的监控任务")
        return
    
    print(f"运行 {len(enabled_tasks)} 个监控任务...")
    
    results = []
    for task in enabled_tasks:
        should_alert, alert_msg = run_task(task['asin'], verbose)
        results.append({
            'asin': task['asin'],
            'alert': should_alert,
            'message': alert_msg
        })
    
    # 汇总
    alert_count = sum(1 for r in results if r['alert'])
    print(f"\n完成! 共{len(enabled_tasks)}个任务, {alert_count}个触发警报")
    
    return results


def update_task(asin, **kwargs):
    """更新任务配置"""
    tasks = load_tasks()
    
    for i, task in enumerate(tasks):
        if task['asin'] == asin:
            # 更新字段
            for key, value in kwargs.items():
                if key in ['frequencyMinutes', 'triggers', 'enabled', 'zipCode']:
                    task[key] = value
            
            task['updatedAt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            tasks[i] = task
            save_tasks(tasks)
            print(f"已更新ASIN {asin}的任务")
            return task
    
    print(f"未找到ASIN {asin}的任务")
    return None


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python amazon_task_scheduler.py create <ASIN> [ZIP] [频率分钟]  - 创建任务")
        print("  python amazon_task_scheduler.py list                                    - 列出任务")
        print("  python amazon_task_scheduler.py run <ASIN>                              - 运行任务")
        print("  python amazon_task_scheduler.py runall                                  - 运行所有任务")
        print("  python amazon_task_scheduler.py delete <ASIN>                           - 删除任务")
        print("  python amazon_task_scheduler.py update <ASIN> <key=value>               - 更新任务")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == 'create':
        asin = sys.argv[2] if len(sys.argv) > 2 else None
        if not asin:
            print("错误: 请提供ASIN，例如: python amazon_task_scheduler.py create B0XXXXXXX 10001 5")
            sys.exit(1)
        zip_code = sys.argv[3] if len(sys.argv) > 3 else '10001'
        frequency = int(sys.argv[4]) if len(sys.argv) > 4 else 5
        create_monitor_task(asin, zip_code, frequency)
    
    elif action == 'list':
        list_tasks()
    
    elif action == 'run':
        if len(sys.argv) > 2:
            run_task(sys.argv[2])
        else:
            print("请指定ASIN")
    
    elif action == 'runall':
        run_all_tasks()
    
    elif action == 'delete':
        if len(sys.argv) > 2:
            delete_task(sys.argv[2])
    
    elif action == 'update':
        if len(sys.argv) > 3:
            asin = sys.argv[2]
            # 解析 key=value 对
            updates = {}
            for arg in sys.argv[3:]:
                if '=' in arg:
                    key, value = arg.split('=', 1)
                    if key == 'frequencyMinutes':
                        value = int(value)
                    elif key == 'enabled':
                        value = value.lower() == 'true'
                    updates[key] = value
            update_task(asin, **updates)
    
    else:
        print(f"未知操作: {action}")
