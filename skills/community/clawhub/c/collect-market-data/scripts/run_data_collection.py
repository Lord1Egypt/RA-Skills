# -*- coding: utf-8 -*-
"""
数据采集主控脚本
执行顺序：
  Step 1: collect_market_data.py - 市场表现类 + 经济数据类
  Step 2: collect_news_websearch.py - 政策类 + 企业类 + 汇总类

覆盖地区：美国、中国、中国香港、欧洲、亚太（日本、韩国）
输出分类：市场表现类、经济数据类、政策类、企业类、汇总类（每日环球市场速览）
"""
import sys
sys.path.insert(0, r"C:\Users\qu669\.openclaw\workspace-yoyo")
sys.stdout.reconfigure(encoding='utf-8')
import os, subprocess, logging
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(config.LOG_FILE, encoding="utf-8"), logging.StreamHandler(sys.stdout)])
log = logging.getLogger(__name__)

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(script_name):
    """运行采集脚本"""
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    if not os.path.exists(script_path):
        log.error(f"❌ 脚本不存在: {script_path}")
        return False
    
    log.info(f"\n{'=' * 60}")
    log.info(f"🚀 开始执行: {script_name}")
    log.info(f"{'=' * 60}")
    
    try:
        result = subprocess.run(
            [config.PYTHON, script_path],
            capture_output=False,
            text=True,
            encoding='utf-8'
        )
        return result.returncode == 0
    except Exception as e:
        log.error(f"❌ 执行 {script_name} 失败: {e}")
        return False

def main():
    log.info("\n" + "=" * 70)
    log.info("🌍 全球金融市场数据采集系统")
    log.info("=" * 70)
    log.info(f"📅 报告日期: {config.REPORT_DATE}")
    log.info(f"📁 输出目录: {config.OUTPUT_DIR}")
    log.info("\n数据覆盖:")
    log.info("  • 地区: 美国、中国、中国香港、欧洲、亚太（日本、韩国）")
    log.info("  • 分类: 市场表现、政策、企业、经济数据、汇总")
    log.info("")
    
    # Step 1: 市场表现 + 经济数据
    log.info("【Step 1】市场表现类 + 经济数据类（API采集）")
    success1 = run_script('collect_market_data.py')
    
    if not success1:
        log.warning("⚠️ Step 1 部分数据采集失败，继续执行 Step 2 补充...")
    
    # Step 2: 政策 + 企业 + 汇总
    log.info("\n" + "=" * 70)
    log.info("【Step 2】政策类 + 企业类 + 汇总类（Web Search）")
    success2 = run_script('collect_news_websearch.py')
    
    # 最终汇总
    log.info("\n" + "=" * 70)
    log.info("📊 数据采集执行完毕")
    log.info("=" * 70)
    
    output_file = os.path.join(config.OUTPUT_DIR, "market_data.json")
    if os.path.exists(output_file):
        import json
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        log.info("\n数据采集结果:")
        log.info(f"  • 市场表现: {len(data.get('市场表现', {}))} 个地区")
        log.info(f"  • 经济数据: {len(data.get('经济数据', {}))} 个地区")
        log.info(f"  • 政策动态: {sum(len(v) for v in data.get('政策动态', {}).values())} 条")
        log.info(f"  • 科技企业动态: {sum(len(v) for v in data.get('科技企业动态', {}).values())} 条")
        log.info(f"  • 市场速览: 已生成")
        log.info(f"\n✅ 完整数据已保存: {output_file}")
    else:
        log.error(f"❌ 未找到输出文件: {output_file}")
    
    log.info("\n" + "=" * 70)
    if success1 and success2:
        log.info("🎉 所有数据采集完成！")
    else:
        log.info("⚠️ 部分数据采集遇到问题，请检查日志")
    log.info("=" * 70)

if __name__ == '__main__':
    main()
