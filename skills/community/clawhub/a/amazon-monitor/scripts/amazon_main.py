"""
Amazon商品监控主程序
整合：数据采集、趋势图生成、竞品分析、任务调度
"""
import sys
import os
import io

# Windows 控制台 UTF-8 输出支持
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 添加scripts目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amazon_monitor_core import get_product_data, save_history, generate_trend_chart, check_trigger_conditions
from amazon_competitor_search import search_competitors, get_competitor_details, generate_analysis_report
from amazon_task_scheduler import create_monitor_task, list_tasks, run_task, run_all_tasks, update_task, delete_task


def main():
    """
    主入口
    用法:
      python amazon_main.py <命令> [参数]
      
    命令:
      1. scrape <ASIN> [ZIP]           - 抓取单个商品数据
      2. monitor <ASIN> [ZIP] [频率]   - 创建监控任务
      3. list                          - 列出所有监控任务
      4. run <ASIN>                     - 运行单个任务
      5. runall                        - 运行所有任务
      6. update <ASIN> <key=value>     - 更新任务配置
      7. delete <ASIN>                 - 删除任务
      8. search <关键词>                - 搜索竞品
      9. compare <ASIN> [ZIP]          - 对比分析
      10. help                         - 显示帮助
    """
    if len(sys.argv) < 2:
        print(main.__doc__)
        return
    
    command = sys.argv[1].lower()
    
    # 1. 抓取数据
    if command == 'scrape':
        asin = sys.argv[2] if len(sys.argv) > 2 else None
        if not asin:
            print("错误: 请提供ASIN，例如: scrape B0XXXXXXX 10001")
            return
        zip_code = sys.argv[3] if len(sys.argv) > 3 else '10001'
        
        print(f"正在采集 ASIN: {asin}, 邮编: {zip_code}")
        data = get_product_data(asin, zip_code)
        
        if data.get('valid', True):
            print(f"\n商品名称: {data.get('productName', '')[:80]}...")
            print(f"价格: {data.get('price')}")
            print(f"星级: {data.get('rating')}")
            print(f"评论数: {data.get('reviewCount')}")
            print(f"配送地址: {data.get('location')}")
            
            history = save_history(asin, data, zip_code)
            print(f"\n历史记录已保存，共 {len(history)} 条")
            
            if len(history) >= 2:
                chart_file = generate_trend_chart(asin, history)
                if chart_file:
                    print(f"趋势图已生成: {chart_file}")
            
            # 数据分析
            if len(history) >= 2:
                prev = history[-2]
                curr = history[-1]
                triggers = check_trigger_conditions(curr, prev)
                
                print("\n" + "="*50)
                print("[数据分析]")
                print("="*50)
                for name, (triggered, msg) in triggers.items():
                    status = "⚠️ " if triggered else "✓ "
                    print(f"{status}{name}: {msg}")
        else:
            print(f"错误: {data.get('error', '链接失效')}")
    
    # 2. 创建监控任务
    elif command == 'monitor':
        asin = sys.argv[2] if len(sys.argv) > 2 else None
        if not asin:
            print("错误: 请提供ASIN，例如: monitor B0XXXXXXX 10001 5")
            return
        zip_code = sys.argv[3] if len(sys.argv) > 3 else '10001'
        frequency = int(sys.argv[4]) if len(sys.argv) > 4 else 5
        
        # 默认触发条件
        triggers = {
            'price_change': True,
            'review_change': True,
            'rating_change': False,
            'link_invalid': True
        }
        
        task = create_monitor_task(asin, zip_code, frequency, triggers)
        print(f"\n✓ 监控任务已创建!")
        print(f"  ASIN: {task['asin']}")
        print(f"  邮编: {task['zipCode']}")
        print(f"  频率: 每{task['frequencyMinutes']}分钟")
        print(f"  触发条件:")
        for k, v in task['triggers'].items():
            print(f"    - {k}: {v}")
        
        # 立即运行一次
        print("\n首次运行...")
        run_task(asin)
    
    # 3. 列出任务
    elif command == 'list':
        list_tasks()
    
    # 4. 运行单个任务
    elif command == 'run':
        if len(sys.argv) > 2:
            run_task(sys.argv[2])
        else:
            print("请指定ASIN")
    
    # 5. 运行所有任务
    elif command == 'runall':
        run_all_tasks()
    
    # 6. 更新任务
    elif command == 'update':
        if len(sys.argv) > 3:
            asin = sys.argv[2]
            updates = {}
            for arg in sys.argv[3:]:
                if '=' in arg:
                    key, value = arg.split('=', 1)
                    if key == 'frequency':
                        updates['frequencyMinutes'] = int(value)
                    elif key == 'enabled':
                        updates['enabled'] = value.lower() == 'true'
                    elif key == 'price_trigger':
                        updates.setdefault('triggers', {})['price_change'] = value.lower() == 'true'
                    elif key == 'review_trigger':
                        updates.setdefault('triggers', {})['review_change'] = value.lower() == 'true'
                    elif key == 'rating_trigger':
                        updates.setdefault('triggers', {})['rating_change'] = value.lower() == 'true'
                    elif key == 'invalid_trigger':
                        updates.setdefault('triggers', {})['link_invalid'] = value.lower() == 'true'
            update_task(asin, **updates)
        else:
            print("用法: python amazon_main.py update <ASIN> <key=value>")
    
    # 7. 删除任务
    elif command == 'delete':
        if len(sys.argv) > 2:
            delete_task(sys.argv[2])
    
    # 8. 搜索竞品
    elif command == 'search':
        if len(sys.argv) > 2:
            args = sys.argv[2:]
            # 如果最后一个参数是5位数字，视为邮编
            if args[-1].isdigit() and len(args[-1]) == 5:
                zip_code = args[-1]
                keyword = ' '.join(args[:-1])
            else:
                zip_code = '10001'
                keyword = ' '.join(args)
            print(f"搜索竞品: {keyword}, 邮编: {zip_code}")
            competitors = search_competitors(keyword, max_results=10, zip_code=zip_code)
            
            if competitors:
                print(f"\n找到 {len(competitors)} 个竞品")
                for i, comp in enumerate(competitors[:5], 1):
                    print(f"\n[{i}] {comp['title'][:60]}...")
                    print(f"    ASIN: {comp['asin']}")
                    print(f"    价格: {comp['price']}")
                    print(f"    评分: {comp['rating']}")
                    print(f"    评论: {comp['reviewCount']}")
            else:
                print("未找到竞品")
        else:
            print("用法: python amazon_main.py search <关键词> [邮编]")
    
    # 9. 对比分析
    elif command == 'compare':
        my_asin = sys.argv[2] if len(sys.argv) > 2 else input("请输入自有产品ASIN: ")
        zip_code = sys.argv[3] if len(sys.argv) > 3 else '10001'
        
        print(f"\n正在获取自有产品数据...")
        my_data = get_product_data(my_asin, zip_code)
        
        if not my_data.get('valid', True):
            print(f"自有产品链接失效: {my_data.get('error')}")
            return
        
        # 提取品类关键词
        product_name = my_data.get('productName', '')
        # 简单提取前几个有意义的词作为搜索关键词
        words = product_name.split()
        keyword = ' '.join(words[:4]) if len(words) >= 4 else product_name
        
        print(f"商品名称: {product_name[:60]}...")
        print(f"\n正在搜索竞品...")
        competitors = search_competitors(keyword, max_results=10)
        
        if not competitors:
            print("未找到竞品")
            return
        
        # 获取前3竞品详细信息
        print("\n正在获取竞品详情...")
        top3 = []
        for comp in competitors[:3]:
            print(f"  获取 {comp['asin']}...")
            detail = get_competitor_details(comp['asin'], zip_code)
            if detail and detail.get('productName') != '未找到':
                top3.append({
                    'asin': comp['asin'],
                    'title': detail.get('productName', comp.get('title', '')),
                    'price': detail.get('price', 'N/A'),
                    'rating': detail.get('rating', 'N/A'),
                    'reviewCount': detail.get('reviewCount', 'N/A'),
                    'isBestSeller': comp.get('isBestSeller', False)
                })
        
        # 生成分析报告
        my_product = {
            'asin': my_asin,
            'productName': product_name,
            'price': my_data.get('price', 'N/A'),
            'rating': my_data.get('rating', 'N/A'),
            'reviewCount': my_data.get('reviewCount', 'N/A')
        }
        
        report = generate_analysis_report(my_product, top3)
        print("\n" + report)
        
        # 保存报告
        report_file = f"competitor_analysis_{my_asin}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n报告已保存: {report_file}")
    
    # 10. 帮助
    elif command == 'help':
        print(main.__doc__)
    
    else:
        print(f"未知命令: {command}")
        print("输入 'help' 查看帮助")


if __name__ == '__main__':
    main()
