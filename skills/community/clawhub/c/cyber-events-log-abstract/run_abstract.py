# coding=utf-8
import json
import sys
import os
import argparse
from datetime import datetime

# 获取技能目录路径
base_dir = os.path.dirname(os.path.abspath(__file__))

# 默认输出目录
default_output_dir = os.path.join(os.path.expanduser("~"), ".openclaw", "workspace", "skills_generate_file")
if not os.path.exists(default_output_dir):
    os.makedirs(default_output_dir)

# 原始数据保存目录
raw_data_dir = os.path.join(os.path.expanduser("~"), ".openclaw", "workspace", "skills_data", "security_events_raw")
if not os.path.exists(raw_data_dir):
    os.makedirs(raw_data_dir)

def run_security_report(days=1):
    """运行安全报告脚本并获取数据"""
    security_report_path = os.path.join(base_dir, "security_report.py")
    
    # 构建命令
    cmd = f'python "{security_report_path}" --days {days}'
    
    # 执行命令
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"执行安全报告脚本失败: {result.stderr}")
    
    # 解析输出
    output = result.stdout.strip()
    if not output:
        raise Exception("安全报告脚本没有输出")
    
    try:
        data = json.loads(output)
        if not data.get("ok", True):
            raise Exception(f"安全报告脚本执行失败: {data.get('error', '未知错误')}")
        
        # 保存原始数据
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        raw_data_path = os.path.join(raw_data_dir, f"security_events_raw_{timestamp}.json")
        with open(raw_data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return data, raw_data_path
    
    except json.JSONDecodeError:
        # 尝试从输出中提取JSON
        import re
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            # 保存原始数据
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            raw_data_path = os.path.join(raw_data_dir, f"security_events_raw_{timestamp}.json")
            with open(raw_data_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return data, raw_data_path
        raise Exception("无法解析安全报告脚本的输出")

def generate_abstract_report(data, days=1):
    """生成安全事件摘要报告"""
    report = []
    
    # 1. 事件趋势分析
    report.append("# 安全事件摘要报告")
    report.append(f"## 1. 事件趋势分析")
    report.append(f"发生事件总数量为{data['event_totals']['totalEventRecords']}")
    report.append(f"趋势状态：{data['trend_stats']['trend']}")
    report.append(f"峰值时间：{data['trend_stats']['peakTime']}")
    report.append(f"峰值事件数：{data['trend_stats']['peakEventCount']}")
    report.append(f"平均事件数：{data['trend_stats']['avgEventCount']}")
    
    # 2. 风险峰值时间
    report.append(f"\n## 2. 风险峰值时间")
    report.append(f"- 事件数量的峰值时间点：{data['trend_stats']['peakTime']}")
    if data['trend_stats']['trend'] == "波动":
        report.append("- 事件量分布均匀，无明显峰值")
    
    # 3. 主要攻击来源
    report.append(f"\n## 3. 主要攻击来源（IP / 国家 / 资产 / 分类）")
    top_attackers = data['trend_top5_ips']
    if top_attackers:
        report.append("- Top 5 攻击来源：")
        for ip, count in top_attackers:
            report.append(f"  - {ip}: {count}次")
    else:
        report.append("- 攻击来源信息缺失，无法确定主要来源")
    
    # 4. 主要受害者
    report.append(f"\n## 4. 主要受害者（IP / 国家 / 资产 / 分类）")
    top_victims = data['victim_top3_ips']
    if top_victims:
        report.append("- Top 3 受害者：")
        for ip, count in top_victims:
            report.append(f"  - {ip}: {count}次")
    else:
        report.append("- 受害者信息缺失，无法确定主要受害者")
    
    # 5. 总体安全态势判断
    report.append(f"\n## 5. 总体安全态势判断")
    report.append(f"- 整体威胁水平：{data['trend_stats']['trend']}")
    
    # 长周期事件分析
    long_cycle = data['long_cycle_summary']
    if long_cycle['longest_event']:
        longest = long_cycle['longest_event']
        report.append(f"\n### 重点事件分析")
        report.append(f"- **持续时间最长的事件**：")
        report.append(f"  - 名称：{longest['name']}")
        report.append(f"  - 时间范围：{longest['timeRange']}")
        report.append(f"  - 持续天数：{longest['durationDays']}")
        report.append(f"  - 对象类型：{longest['focusObjectCN']}")
        report.append(f"  - IP：{longest['ips']}")
    
    if long_cycle['highest_risk_event']:
        highest = long_cycle['highest_risk_event']
        report.append(f"- **风险等级最高的事件**：")
        report.append(f"  - 名称：{highest['name']}")
        report.append(f"  - 时间范围：{highest['timeRange']}")
        report.append(f"  - 风险等级：{highest['threatSeverity']}")
        report.append(f"  - 对象类型：{highest['focusObjectCN']}")
        report.append(f"  - IP：{highest['ips']}")
    
    # Top 5 事件表格
    report.append(f"\n### Top 5 关键事件")
    report.append("| 时间范围 | 持续天数 | 对象类型 | IP | 事件名称 | 风险等级 | 事件次数 |")
    report.append("|---------|----------|---------|----|---------|---------|---------|")
    for event in long_cycle['top5_events']:
        report.append(f"| {event['timeRange']} | {event['durationDays']} | {event['focusObjectCN']} | {event['ips']} | {event['name']} | {event['threatSeverity']} | {event['eventCount']} |")
    
    # Top 3 潜伏攻击IP
    top_attackers = data['long_cycle_top_attackers']
    if top_attackers:
        report.append(f"\n### Top 3 潜伏攻击IP")
        report.append("| IP | 潜伏时间范围 | 潜伏天数 | 对象类型 | 代表事件 | 最高风险等级 | 累计事件次数 |")
        report.append("|----|------|------|-------|------|--------|-------|")
        for attacker in top_attackers:
            report.append(f"| {attacker['ip']} | {attacker['timeRange']} | {attacker['durationDays']} | 攻击者 | {attacker['mainEventType']} | {attacker['maxThreatSeverity']} | {attacker['eventCount']} |")
    
    # Top 5 风险事件详细分析
    top_risk_events = data['top5_risk_events']
    if top_risk_events:
        report.append(f"\n### Top 5 高危事件详细分析")
        for event in top_risk_events:
            report.append(f"\n#### 事件 #{event['rank']}")
            report.append(f"**【事件概览】**")
            report.append(f"- 事件类型：{event['subCategory']}")
            report.append(f"- 事件规模：{event['eventCount']}次")
            report.append(f"- 对象类型：{event['focusObjectCN']}")
            report.append(f"- Top 3 IP：{', '.join(event['top3Ips']) if event['top3Ips'] else '无'}")
            
            report.append(f"\n**【核心风险】**")
            if event['criticalDangerPoint']:
                report.append(f"- 核心风险：{event['criticalDangerPoint']}")
            elif event['coreRisks']:
                report.append(f"- 核心风险：{event['coreRisks']}")
            else:
                report.append(f"- 风险描述：基于事件类型{event['subCategory']}的基础风险")
            
            report.append(f"\n**【处置建议】**")
            if event['attackDisposalSuggestionList']:
                for suggestion in event['attackDisposalSuggestionList']:
                    report.append(f"- {suggestion['step']}: {suggestion['desc']}")
            else:
                report.append("- 通用建议：请遵循标准安全操作流程进行处置")
    
    # 结论摘要
    report.append(f"\n## 6. 结论摘要")
    report.append(f"基于{days}天的安全事件分析，当前系统整体安全态势为{data['trend_stats']['trend']}。")
    report.append(f"主要威胁来自{', '.join([ip for ip, _ in data['trend_top5_ips'][:3]]) if data['trend_top5_ips'] else '未知来源'}。")
    report.append(f"建议重点关注高风险事件，及时采取相应的处置措施。")
    
    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description='生成安全事件摘要报告')
    parser.add_argument('--days', type=int, default=1, help='统计周期天数（默认1天）')
    parser.add_argument('--output', type=str, default=None, help='输出文件路径（默认在skills_generate_file目录）')
    args = parser.parse_args()
    
    try:
        # 获取安全事件数据
        data, raw_data_path = run_security_report(args.days)
        
        # 生成摘要报告
        report_content = generate_abstract_report(data, args.days)
        
        # 确定输出路径
        if args.output:
            output_path = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(default_output_dir, f"security_events_abstract_{timestamp}.md")
        
        # 保存报告
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"安全事件摘要报告已生成：{output_path}")
        print(f"原始安全事件数据已保存：{raw_data_path}")
        print("\n报告内容：")
        print(report_content)
        
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()