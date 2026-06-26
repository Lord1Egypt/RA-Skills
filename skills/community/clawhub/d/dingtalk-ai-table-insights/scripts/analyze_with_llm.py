#!/usr/bin/env python3
"""
dingtalk-ai-table-insights - OpenClaw 会话包装器

在 OpenClaw 会话中运行，使用 sessions_spawn 调用大模型进行分析。

使用方法：
    在 OpenClaw 会话中直接运行：
    python3 scripts/analyze_with_llm.py --keyword "仪表盘"
"""

import argparse
import json
import subprocess
import sys
import os
import tempfile
from datetime import datetime
import time

# 导入主分析脚本的函数
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_tables import (
    get_accessible_tables,
    read_all_sheets_data,
    DEFAULT_LIMIT,
    MCP_CONFIG_PATH,
    run_dingtalk_command,
    SKILL_VERSION
)


def analyze_with_llm_in_session(tables_data: list, keyword: str = "") -> str:
    """
    在 OpenClaw 会话中使用大模型分析表格数据
    
    通过 sessions_spawn 调用子代理进行分析
    """
    print("🤖 使用 OpenClaw 大模型进行分析...")
    
    # 构建分析 Prompt
    system_prompt = f"""你是一个数据分析专家，擅长从企业数据中发现洞察和风险。

## 分析维度
1. **数据一致性检查** - 跨表格对比相同指标，发现矛盾
2. **跨文档交叉验证** - 对比不同文档的数据，验证一致性和发现关联
3. **趋势洞察** - 从多个表格中发现关联和模式
4. **风险预警** - 识别异常和高风险项（按优先级排序）
5. **行动建议** - 给出具体可执行的建议（做什么 + 谁来做 + 何时完成）

## 跨文档分析重点
- **数据交叉验证**: 对比不同文档中的相同指标（如任务数、人数、时间等）
- **关联发现**: 发现文档间的隐含关系（如任务 - 缺陷关联、人效 - 质量关联）
- **一致性检查**: 识别不同文档中的数据矛盾或异常差异
- **综合洞察**: 基于多文档数据给出全局性结论

## 输出格式
- 使用 Markdown 格式
- 适当使用 emoji 增强可读性
- 字数控制在 800-1500 字
- 适合在钉钉中查看
- **报告头部必须包含**: 生成时间（年月日时分秒）、分析工具版本号
"""
    
    # 构建数据摘要（抽样策略：限制数据表数量 + 示例抽样）
    data_summary = []
    for table in tables_data:
        table_name = table.get("table_name", "未知表格")
        sheets = table.get("sheets", [])
        records = table.get("records", [])
        
        table_info = {
            "表格名称": table_name,
            "数据表数": len(sheets),
            "总记录数": len(records),
            "数据表详情": []
        }
        
        # 每个表格最多处理 10 个数据表
        max_sheets_per_table = 10
        sampled_sheets = sheets[:max_sheets_per_table] if len(sheets) > max_sheets_per_table else sheets
        
        for sheet in sampled_sheets:
            sheet_info = {
                "数据表名称": sheet.get("sheet_name", "未知"),
                "记录数": len(sheet.get("records", []))
            }
            table_info["数据表详情"].append(sheet_info)
        
        if len(sheets) > max_sheets_per_table:
            table_info["数据表详情"].append(f"... 共{len(sheets)}个数据表（已抽样{max_sheets_per_table}个）")
        
        # 使用读取阶段抽样后的全部数据（每表最多 100 条）
        if records:
            table_info["数据示例"] = []
            # 不再额外抽样，使用读取阶段的全部数据（最多 100 条/表）
            # 默认只取前 8 个字段作为示例（节省 token，适配不同表格结构）
            max_fields_per_record = 8
            for record in records:
                fields = record.get("fields", {})
                sample = {}
                # 只取前 8 个字段
                for i, (key, value) in enumerate(fields.items()):
                    if i >= max_fields_per_record:
                        break  # 超过 8 个字段，跳过
                    # 处理嵌套值（有些字段是对象，需要提取 name 或 text）
                    if isinstance(value, dict):
                        value = value.get("name", value.get("text", str(value)))
                    sample[key] = value
                table_info["数据示例"].append(sample)
        
        data_summary.append(table_info)
    
    # 生成时间（包含时分秒）
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    user_prompt = f"""请分析以下钉钉 AI 表格数据，生成洞察分析报告。

## 报告元信息（必须严格按此格式输出到报告开头）
- **生成时间**: {current_time}（必须包含年月日时分秒）
- **分析工具**: dingtalk-ai-table-insights v{SKILL_VERSION}（必须包含版本号）
- **筛选关键词**: {keyword if keyword else "全量扫描"}
- **分析表格数**: {len(tables_data)} 个
- **总记录数**: {sum(len(t.get("records", [])) for t in tables_data)} 条

## 表格数据摘要
{json.dumps(data_summary, ensure_ascii=False, indent=2)}

## 请生成报告，必须包含以下内容

### 1. 执行摘要
- 关键指标汇总（使用表格展示）
- 核心发现（3-5 条，简要概述）

### 2. 详细数据分析
- 每个表格的数据表详情、示例、洞察

### 3. 🔗 跨文档交叉验证分析（必须单独成节！重点！）

**这是报告的核心章节，必须包含以下分析：**

#### 3.1 数据一致性对比
- 对比不同表格中的**相同指标**（如：Scrum 表的任务数 vs 个人效率表的任务数）
- 检查数据是否一致，识别矛盾或差异
- 示例：Scrum 表显示人均 1.54 任务，个人表显示人均 X 任务，差异原因分析

#### 3.2 跨表格关联发现
- 发现表格间的**隐含关系**
- 示例：任务缺陷率 (12%) vs 个人效率评级分布 的关联
- 示例：日报执行率 (12%) vs 任务录入完整性 的关联

#### 3.3 数据量级对比
- 对比不同表格的数据规模，评估代表性
- 示例：Scrum 表 353 条 vs 个人效率表 21 条 = 17:1，无法有效关联

#### 3.4 综合洞察
- 基于多表格数据给出**全局性结论**
- 不能仅从单一表格得出的洞察

### 4. 风险与异常识别
- 按优先级排序（高/中/低）
- 包含数据质量评估

### 5. 行动建议
- 具体可执行
- 包含优先级、负责人、时间、验收标准

## 输出要求
- **第 3 节"跨文档交叉验证分析"必须独立成节，包含 3.1-3.4 四个子节**
- 使用 Markdown 表格展示跨表格对比数据
- 适当使用 emoji 增强可读性

请开始生成报告：
"""
    
    full_prompt = f"{system_prompt}\n\n{user_prompt}"
    
    # 使用 openclaw sessions_send 发送到当前会话
    # 注意：这需要在 OpenClaw 会话环境中运行
    try:
        print("   🔄 调用 OpenClaw 大模型...")
        
        # 尝试通过 subprocess 调用 openclaw agent
        # 使用 --agent main 指定会话（参考 v1.6.0 成功方案）
        # 增加超时时间到 300 秒（5 分钟），因为大数据量分析需要更长时间
        result = subprocess.run(
            ["openclaw", "agent", "--agent", "main", "--message", full_prompt[:10000], "--json"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0 and result.stdout.strip():
            output = json.loads(result.stdout.strip())
            reply = output.get("reply", "")
            if reply:
                print("   ✅ 大模型分析完成")
                
                # 确保报告头部包含正确的时间和版本号
                # 强制替换头部，确保格式正确
                header = f"""# 📊 {keyword if keyword else 'AI 表格'}洞察分析报告

**生成时间**: {current_time}  
**分析工具**: dingtalk-ai-table-insights v{SKILL_VERSION}  
**筛选关键词**: {keyword if keyword else '全量扫描'}

---

"""
                # 移除大模型可能生成的旧头部（多种匹配策略）
                lines = reply.split('\n')
                content_start = len(lines)  # 默认到最后
                
                # 策略 1: 找第一个二级标题 (## 开头，但不是 ###)
                for i, line in enumerate(lines[:30]):
                    stripped = line.strip()
                    if stripped.startswith('##') and not stripped.startswith('###'):
                        content_start = i
                        print(f"   📝 [策略 1] 找到内容起始位置：第{i}行 - {stripped[:50]}")
                        break
                
                # 策略 2: 如果没找到##，找第一个包含"执行摘要"或"数据概览"的行
                if content_start == len(lines):
                    for i, line in enumerate(lines[:30]):
                        if '执行摘要' in line or '数据概览' in line or '详细数据' in line:
                            # 往前找最近的空行或标题行
                            content_start = max(0, i - 1)
                            print(f"   📝 [策略 2] 找到内容起始位置：第{content_start}行")
                            break
                
                # 策略 3: 如果还是没找到，找第一个非空行且不是标题格式的行
                if content_start == len(lines):
                    for i, line in enumerate(lines[:30]):
                        stripped = line.strip()
                        if stripped and not stripped.startswith('#') and not stripped.startswith('**生成'):
                            content_start = i
                            print(f"   📝 [策略 3] 找到内容起始位置：第{content_start}行")
                            break
                
                # 只保留正文内容，替换头部
                reply = header + '\n'.join(lines[content_start:])
                print(f"   ✅ 报告头部已替换，版本号：v{SKILL_VERSION}")
                
                # 强制验证版本号是否出现在报告前 500 字符
                if f'v{SKILL_VERSION}' not in reply[:500]:
                    print(f"   ⚠️  版本号未出现在报告头部，强制插入...")
                    # 在第一个 --- 之后插入版本号
                    divider_idx = reply.find('---')
                    if divider_idx > 0:
                        insert_pos = divider_idx + 3
                        reply = reply[:insert_pos] + f'\n**分析工具**: dingtalk-ai-table-insights v{SKILL_VERSION}\n' + reply[insert_pos:]
                        print(f"   ✅ 版本号已强制插入")
                
                # 检查是否有跨文档交叉验证章节，如果没有则添加
                has_cross_doc = '跨文档' in reply or '交叉验证' in reply or '跨表格' in reply
                
                if not has_cross_doc:
                    print(f"   ⚠️  未检测到跨文档章节，自动添加...")
                    
                    # 生成动态的跨文档分析章节（基于实际数据）
                    table_summaries = []
                    for table in tables_data:
                        table_name = table.get("table_name", "未知表格")
                        record_count = len(table.get("records", []))
                        table_summaries.append(f"- **{table_name}**: {record_count} 条记录")
                    
                    # 计算数据量级对比
                    total_records = sum(len(t.get("records", [])) for t in tables_data)
                    comparison_table = ""
                    if tables_data:
                        comparison_table = "| 表格 | 记录数 | 占比 | 可对比性 |\n|------|--------|------|----------|\n"
                        for table in sorted(tables_data, key=lambda x: len(x.get("records", [])), reverse=True):
                            name = table.get("table_name", "未知")[:12]
                            count = len(table.get("records", []))
                            pct = f"{count/total_records*100:.1f}%" if total_records > 0 else "0%"
                            flag = "✅ 主体数据" if count > total_records * 0.3 else "⚠️ 数据较少" if count > 0 else "🔴 无数据"
                            comparison_table += f"| {name} | {count}条 | {pct} | {flag} |\n"
                    
                    cross_analysis = f"""
---

## 🔗 跨文档交叉验证分析

### 数据一致性对比
- 已分析 {len(tables_data)} 个表格，总记录数 {total_records} 条
{chr(10).join(table_summaries[:5])}
{"- ... 更多表格" if len(table_summaries) > 5 else ""}

### 跨表格关联发现
- 对比不同表格中的相同指标（如任务数、状态分布、时间周期等）
- 识别表格间的隐含关系和数据依赖
- 检查数据录入标准是否一致

### 数据量级对比
{comparison_table}

### 综合洞察
- **数据完整性**: 建议检查各表格的数据采集标准是否统一
- **跨表格验证**: 关键指标应在多个表格中有一致记录
- **数据质量**: 记录数差异较大的表格需谨慎对比分析

---
"""
                    # 多种策略找到插入位置
                    insert_pos = -1
                    
                    # 策略 1: 找"风险"或"异常"章节，在其之前插入
                    risk_keywords = ['## 风险', '## 异常', '## 4', '## 5']
                    for kw in risk_keywords:
                        idx = reply.find(kw)
                        if idx > 0:
                            insert_pos = idx
                            print(f"   📝 [插入策略 1] 在'{kw}'之前插入")
                            break
                    
                    # 策略 2: 找"详细数据分析"章节的末尾
                    if insert_pos < 0:
                        detail_idx = reply.find('## 详细数据')
                        if detail_idx > 0:
                            # 找下一个## 标题
                            next_section = reply.find('\n## ', detail_idx + 10)
                            if next_section > 0:
                                insert_pos = next_section + 1
                                print(f"   📝 [插入策略 2] 在详细数据分析后插入")
                    
                    # 策略 3: 在第一个 --- 分隔符后插入
                    if insert_pos < 0:
                        divider_idx = reply.find('---', 100)  # 跳过第一个分隔符
                        if divider_idx > 0:
                            insert_pos = divider_idx
                            print(f"   📝 [插入策略 3] 在分隔符后插入")
                    
                    # 执行插入
                    if insert_pos > 0:
                        reply = reply[:insert_pos] + cross_analysis + '\n' + reply[insert_pos:]
                        print(f"   ✅ 跨文档章节已添加（位置：{insert_pos}）")
                    else:
                        # 兜底：追加到末尾
                        reply += '\n' + cross_analysis
                        print(f"   ✅ 跨文档章节已追加到末尾")
                else:
                    print(f"   ✅ 跨文档章节已存在")
                
                return reply
        
        print(f"   ⚠️  调用失败：{result.stderr[:200] if result.stderr else '无响应'}")
    except Exception as e:
        print(f"   ⚠️  调用异常：{e}")
    
    # 降级方案：返回简单报告
    print("   ⚠️  使用简化分析...")
    return generate_simple_report(tables_data, keyword)


def generate_simple_report(tables_data: list, keyword: str = "") -> str:
    """生成简化报告（降级方案）"""
    total_tables = len(tables_data)
    total_sheets = sum(len(table.get("sheets", [{}])) for table in tables_data)
    total_records = sum(len(table.get("records", [])) for table in tables_data)
    
    # 生成时间（包含时分秒）
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    report = f"""# 📊 {keyword if keyword else 'AI 表格'}洞察分析报告

**生成时间**: {current_time}  
**分析工具**: dingtalk-ai-table-insights v{SKILL_VERSION}  
**筛选关键词**: {keyword if keyword else '全量扫描'}

---

## 📋 执行摘要

| 指标 | 数值 |
|------|------|
| **分析表格数** | {total_tables} 个 |
| **数据表总数** | {total_sheets} 个 |
| **总记录数** | **{total_records} 条** |

---

## 📊 数据概览

"""
    
    for table in tables_data:
        table_name = table.get("table_name", "未知表格")
        records = len(table.get("records", []))
        report += f"- **{table_name}**: {records} 条记录\n"
    
    report += f"\n---\n\n*报告生成：dingtalk-ai-table-insights v{SKILL_VERSION}*\n"
    
    return report


def main():
    parser = argparse.ArgumentParser(description='dingtalk-ai-table-insights - OpenClaw 会话分析')
    parser.add_argument('--keyword', type=str, default='', help='表格名称关键词筛选')
    parser.add_argument('--output', type=str, default='', help='输出文件路径')
    parser.add_argument('--limit', type=int, default=DEFAULT_LIMIT, help='每个表格抽样记录数')
    
    args = parser.parse_args()
    
    if args.keyword:
        print(f"🔍 开始分析 AI 表格... (关键词：{args.keyword})")
    else:
        print(f"🔍 开始分析 AI 表格... (全量扫描)")
    
    # 1. 获取表格列表
    print("📋 获取表格列表...")
    tables = get_accessible_tables(args.keyword)
    print(f"   找到 {len(tables)} 个表格")
    
    if not tables:
        print("⚠️  未找到匹配的表格")
        return
    
    # 2. 读取表格数据
    print("📊 读取表格数据...")
    tables_data = []
    total_records = 0
    
    for i, table in enumerate(tables, 1):
        table_name = table.get("docName") or table.get("name") or "未知表格"
        doc_id = table.get("docId") or ""
        
        if not doc_id:
            continue
        
        print(f"   [{i}/{len(tables)}] 读取 {table_name}...")
        
        all_sheets_data = read_all_sheets_data(doc_id, args.limit)
        
        if all_sheets_data:
            all_records = []
            for sheet_data in all_sheets_data:
                all_records.extend(sheet_data.get("records", []))
            
            tables_data.append({
                "table_name": table_name,
                "doc_id": doc_id,
                "records": all_records,
                "sheets": all_sheets_data
            })
            total_records += len(all_records)
            print(f"      ✅ {len(all_records)} 条记录")
    
    print(f"\n📊 读取完成：{len(tables_data)} 个表格，共 {total_records} 条记录")
    
    # 3. 使用大模型分析
    print("\n🤖 分析中...")
    report = analyze_with_llm_in_session(tables_data, args.keyword)
    
    # 4. 输出报告
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n✅ 报告已保存到：{args.output}")
    else:
        print("\n" + "="*60)
        print(report)
        print("="*60)


if __name__ == "__main__":
    main()
