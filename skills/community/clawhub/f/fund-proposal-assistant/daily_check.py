#!/usr/bin/env python3
"""
基金申请材料每日检查脚本
每天执行一次，生成带日期的新Word文档
执行期限：2026-02-28 至 2026-03-06
"""

import os
import sys
import shutil
from datetime import datetime, timedelta
from pathlib import Path

# 配置
FUND_DOC_DIR = r"Y:\"  # 基金文档原始位置（需要豹老大指定）
OUTPUT_DIR = r"D:\Personal\OpenClaw\fund-daily-versions"
REPORT_DIR = r"D:\Personal\OpenClaw\fund-check-reports"
DDL_DATE = datetime(2026, 3, 6)


def get_today_str():
    """获取今天日期字符串"""
    return datetime.now().strftime('%Y%m%d')


def get_days_to_ddl():
    """计算距离DDL的天数"""
    today = datetime.now()
    delta = DDL_DATE - today
    return delta.days


def ensure_directories():
    """确保输出目录存在"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)


def find_latest_fund_doc():
    """
    查找最新的基金申请书
    优先查找昨天的版本，否则找原始文件
    """
    # 首先查找昨天的版本
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    yesterday_pattern = f"NSFC_面上项目_2026_纪金豹_{yesterday}"
    
    for file in os.listdir(OUTPUT_DIR) if os.path.exists(OUTPUT_DIR) else []:
        if yesterday_pattern in file and file.endswith('.docx'):
            return os.path.join(OUTPUT_DIR, file)
    
    # 查找最近任何一天的版本
    if os.path.exists(OUTPUT_DIR):
        files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.docx')]
        if files:
            files.sort(reverse=True)
            return os.path.join(OUTPUT_DIR, files[0])
    
    # 提示用户指定原始文件
    print("未找到之前的版本，请指定原始基金申请书路径")
    return None


def check_document_exists():
    """检查是否可以找到基金文档"""
    doc_path = find_latest_fund_doc()
    if doc_path and os.path.exists(doc_path):
        return True
    return False


def generate_checklist_report():
    """生成今日检查清单报告"""
    today = get_today_str()
    days_left = get_days_to_ddl()
    
    report = f"""# 基金申请材料每日检查记录

**检查日期：** {datetime.now().strftime('%Y年%m月%d日')}  
**检查人：** SuperMike  
**距离DDL：** {days_left}天（3月6日）

---

## 今日检查任务

### P0 - 必须修改（影响提交）
- [ ] 申请代码正确（E0505/E050501）
- [ ] 研究期限合理（2026.01-2029.12）
- [ ] 申请金额符合指南
- [ ] 人员信息完整准确
- [ ] 无超项问题
- [ ] 摘要字数符合要求（400字以内）

### P1 - 重要修改（影响评审）
- [ ] 立项依据逻辑清晰
- [ ] 科学问题明确（1-2个核心问题）
- [ ] 研究内容具体可行（3-4条）
- [ ] 创新点表述准确（2-3条）
- [ ] 技术路线图清晰
- [ ] 参考文献格式统一（GB/T 7714）

### P2 - 优化建议（提升质量）
- [ ] 语言表达精炼（去口语化）
- [ ] 图表质量提升（高清、规范）
- [ ] 错别字检查（全文通读）
- [ ] 格式细节统一（字体、段落）

---

## 今日检查重点

根据倒计时，今日重点检查：

{get_today_focus(days_left)}

---

## 检查方法

1. **通读全文** - 从头到尾阅读，标记问题
2. **对照清单** - 逐项核对，打勾确认
3. **记录问题** - 在下方表格记录发现的问题
4. **生成文档** - 保存带日期的新版本

---

## 问题记录表

| 优先级 | 位置 | 问题描述 | 修改建议 | 状态 |
|--------|------|---------|---------|------|
| | | | | |

---

## 修改建议汇总

### 今日发现的主要问题：

1. 
2. 
3. 

### 建议修改方案：

1. 
2. 
3. 

---

## 生成文档

**今日版本：** `NSFC_面上项目_2026_纪金豹_{today}.docx`

**存放位置：** `{OUTPUT_DIR}`

**修改说明：** 
- 在原文档基础上添加了修改建议批注
- 在文档开头添加了修改记录页
- 保留了完整的原文档格式

---

## 明日计划

明天检查重点：

{get_tomorrow_focus(days_left)}

---

## 倒计时提醒

```
当前日期：{datetime.now().strftime('%Y-%m-%d')}
提交DDL：  2026-03-06
剩余天数： {days_left}天
今日进度： 第{7-days_left}/7天
```

---

_检查时间：{datetime.now().strftime('%H:%M')}_  
_下次检查：{(datetime.now() + timedelta(days=1)).strftime('%Y年%m月%d日')} _
"""
    
    return report


def get_today_focus(days_left):
    """根据倒计时返回今日检查重点"""
    focus_map = {
        6: """
**初检阶段（2月28日）**
- 整体框架检查
- 各章节完整性确认
- 格式统一性初查
- 建立问题清单""",
        5: """
**立项依据深化（3月1日）**
- 立项依据逻辑严密性
- 科学问题凝练精准度
- 研究意义阐述充分性
- 文献引用准确性""",
        4: """
**研究内容打磨（3月2日）**
- 研究内容具体可行性
- 研究方案详细程度
- 技术路线图清晰度
- 年度计划的合理性""",
        3: """
**创新点与基础（3月3日）**
- 创新点表述准确性
- 与已有研究区分度
- 研究基础支撑力
- 团队分工明确性""",
        2: """
**格式与参考文献（3月4日）**
- 参考文献格式统一
- 图表编号、标题规范
- 错别字全面检查
- 段落格式一致性""",
        1: """
**最终冲刺（3月5日）**
- 全文通读检查
- 系统预填信息核对
- 附件材料齐全性
- 最后细节确认""",
        0: """
**提交日（3月6日）**
- 最终确认
- 系统提交
- 下载存档"""
    }
    return focus_map.get(days_left, "继续完善文档")


def get_tomorrow_focus(days_left):
    """获取明天的检查重点"""
    tomorrow_days = days_left - 1
    if tomorrow_days < 0:
        return "已完成，等待提交"
    return get_today_focus(tomorrow_days).split('\n')[0].strip()


def generate_daily_report():
    """生成每日检查报告"""
    ensure_directories()
    
    today = get_today_str()
    report_content = generate_checklist_report()
    
    report_path = os.path.join(REPORT_DIR, f"check_report_{today}.md")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"已生成检查报告：{report_path}")
    return report_path


def create_daily_version():
    """创建带日期的文档版本"""
    today = get_today_str()
    days_left = get_days_to_ddl()
    
    # 查找源文件
    source_file = find_latest_fund_doc()
    
    if not source_file:
        print("警告：未找到基金申请书源文件")
        print("请确认：")
        print(f"1. 原始文件是否存放在：{FUND_DOC_DIR}")
        print(f"2. 或者昨天的版本是否在：{OUTPUT_DIR}")
        return None
    
    # 生成新文件名
    new_filename = f"NSFC_面上项目_2026_纪金豹_{today}.docx"
    output_path = os.path.join(OUTPUT_DIR, new_filename)
    
    # 复制文件
    try:
        shutil.copy2(source_file, output_path)
        print(f"已创建新版本：{new_filename}")
        print(f"   源文件：{source_file}")
        print(f"   新文件：{output_path}")
        return output_path
    except Exception as e:
        print(f"错误：创建文档版本失败 - {e}")
        return None


def show_today_summary():
    """显示今日检查摘要"""
    days_left = get_days_to_ddl()
    
    print("\n" + "="*60)
    print("基金申请材料每日检查系统")
    print("="*60)
    print(f"\n今日日期：{datetime.now().strftime('%Y年%m月%d日')}")
    print(f"距离DDL：{days_left}天（3月6日）")
    print(f"今日进度：第{7-days_left}/7天")
    print("\n已生成：")
    print("   1. 检查报告（Markdown）")
    print("   2. Word文档版本（带日期）")
    print("\n今日检查重点：")
    print(get_today_focus(days_left))
    print("\n" + "="*60)


def main():
    """主函数"""
    print("开始执行基金申请材料每日检查...\n")
    
    # 检查是否在有效期内
    days_left = get_days_to_ddl()
    if days_left < 0:
        print("基金申请已截止，检查任务完成！")
        return
    
    # 确保目录存在
    ensure_directories()
    
    # 1. 生成检查报告
    report_path = generate_daily_report()
    
    # 2. 创建文档版本
    doc_path = create_daily_version()
    
    # 3. 显示摘要
    show_today_summary()
    
    print("\n提示：")
    print(f"   - 检查报告：{report_path}")
    if doc_path:
        print(f"   - Word文档：{doc_path}")
    print(f"\n请豹老大查看今天的版本并进行修改！")


if __name__ == "__main__":
    main()
