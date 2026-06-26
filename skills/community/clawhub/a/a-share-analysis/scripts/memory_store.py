#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股分析记忆存储脚本
使用 Elite Long-term Memory 系统存储历史分析记录
"""

import json
import os
import sys
import codecs
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Windows 编码处理
if sys.platform == 'win32':
    try:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    except:
        pass

# Windows UTF-8 输出设置

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AShareMemoryStore:
    """A 股分析记忆存储器"""

    def __init__(self, workspace_path: str = None):
        # 获取工作区路径
        if workspace_path is None:
            workspace_path = os.path.expanduser("~/.openclaw/workspace")
        
        self.workspace_path = workspace_path
        self.memory_dir = os.path.join(workspace_path, "memory")
        self.a_share_memory_dir = os.path.join(self.memory_dir, "a-share")
        self.session_state_path = os.path.join(workspace_path, "SESSION-STATE.md")
        self.memory_md_path = os.path.join(workspace_path, "MEMORY.md")
        
        # 确保目录存在
        os.makedirs(self.a_share_memory_dir, exist_ok=True)

    def _get_today_file(self) -> str:
        """获取今日记忆文件路径"""
        today = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.memory_dir, f"{today}.md")

    def store_analysis(self, analysis_data: Dict) -> str:
        """存储一次分析记录"""
        stock_code = analysis_data.get('stock_code', 'unknown')
        stock_name = analysis_data.get('stock_name', '未知股票')
        timestamp = datetime.now()
        
        # 创建分析记录
        record = {
            "timestamp": timestamp.isoformat(),
            "date": timestamp.strftime("%Y-%m-%d"),
            "time": timestamp.strftime("%H:%M:%S"),
            "stock_code": stock_code,
            "stock_name": stock_name,
            "price": analysis_data.get('price'),
            "change_percent": analysis_data.get('change_percent'),
            "technical_signal": analysis_data.get('technical', {}).get('signal', 'unknown'),
            "sentiment": analysis_data.get('sentiment', {}).get('overall_sentiment', 'unknown'),
            "recommendation": analysis_data.get('recommendation', 'unknown'),
            "key_points": analysis_data.get('key_points', [])
        }

        # 1. 写入今日记忆文件
        today_file = self._get_today_file()
        self._append_to_daily_log(today_file, record)

        # 2. 写入股票专用记忆
        stock_memory_file = os.path.join(self.a_share_memory_dir, f"{stock_code}.json")
        self._append_to_stock_memory(stock_memory_file, record)

        # 3. 更新 SESSION-STATE.md
        self._update_session_state(record)

        # 4. 更新 MEMORY.md（如果是重要分析）
        if analysis_data.get('importance', 0) > 0.7:
            self._update_memory_md(record)

        logger.info(f"分析记录已存储：{stock_name} ({stock_code})")
        return f"a-share/{stock_code}"

    def _append_to_daily_log(self, file_path: str, record: Dict):
        """追加到每日日志"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        content = f"""
## 📈 A 股分析 - {record['time']}

**股票**: {record['stock_name']} ({record['stock_code']})
**价格**: ¥{record['price']:.2f} ({record['change_percent']:+.2f}%)
**技术信号**: {record['technical_signal']}
**市场情绪**: {record['sentiment']}
**建议**: {record['recommendation']}

"""
        if record['key_points']:
            content += "**关键点**:\n"
            for point in record['key_points'][:5]:
                content += f"- {point}\n"
            content += "\n"

        # 如果文件不存在，添加标题
        if not os.path.exists(file_path):
            header = f"# {today} 记忆日志\n\n"
            with open(file_path, 'w', encoding='utf-8', errors='replace') as f:
                f.write(header + content)
        else:
            with open(file_path, 'a', encoding='utf-8', errors='replace') as f:
                f.write(content)

    def _append_to_stock_memory(self, file_path: str, record: Dict):
        """追加到股票专用记忆"""
        records = []
        
        # 读取现有记录
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    records = json.load(f)
            except:
                records = []

        # 添加新记录
        records.append(record)
        
        # 只保留最近 50 条记录
        records = records[-50:]

        # 写回文件
        with open(file_path, 'w', encoding='utf-8', errors='replace') as f:
            json.dump(records, f, ensure_ascii=False, indent=2, default=str)

    def _update_session_state(self, record: Dict):
        """更新 SESSION-STATE.md"""
        content = f"""# SESSION-STATE.md — A 股分析活跃上下文

## 最近分析
- **时间**: {record['date']} {record['time']}
- **股票**: {record['stock_name']} ({record['stock_code']})
- **价格**: ¥{record['price']:.2f}
- **建议**: {record['recommendation']}

## 当前市场情绪
- 技术信号：{record['technical_signal']}
- 新闻情绪：{record['sentiment']}

## 待跟进
- [ ] 监控 {record['stock_name']} 后续走势
- [ ] 更新分析记录

---
*最后更新：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
        with open(self.session_state_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _update_memory_md(self, record: Dict):
        """更新 MEMORY.md（重要分析）"""
        # 检查 MEMORY.md 是否存在
        if not os.path.exists(self.memory_md_path):
            # 创建基础 MEMORY.md
            header = """# MEMORY.md - A 股分析长期记忆

这是 A 股分析的长期记忆文件，记录重要的投资决策和分析经验。

---

"""
            with open(self.memory_md_path, 'w', encoding='utf-8') as f:
                f.write(header)

        # 读取现有内容
        with open(self.memory_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 添加新记录（在文件开头）
        new_entry = f"""
## 📊 {record['date']} - {record['stock_name']} ({record['stock_code']})

- **分析时价格**: ¥{record['price']:.2f}
- **技术信号**: {record['technical_signal']}
- **市场情绪**: {record['sentiment']}
- **投资建议**: {record['recommendation']}
- **关键点**: {'; '.join(record['key_points'][:3]) if record['key_points'] else '无'}

"""
        # 找到第一个 "---" 之后插入
        if "---" in content:
            parts = content.split("---", 1)
            new_content = parts[0] + "---\n" + new_entry + parts[1]
        else:
            new_content = content + new_entry

        with open(self.memory_md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    def get_stock_history(self, stock_code: str, limit: int = 10) -> List[Dict]:
        """获取股票历史分析记录"""
        stock_memory_file = os.path.join(self.a_share_memory_dir, f"{stock_code}.json")
        
        if not os.path.exists(stock_memory_file):
            return []

        try:
            with open(stock_memory_file, 'r', encoding='utf-8') as f:
                records = json.load(f)
            return records[-limit:]  # 返回最近的记录
        except:
            return []

    def get_analysis_summary(self, stock_code: str) -> Optional[Dict]:
        """获取股票分析摘要"""
        history = self.get_stock_history(stock_code)
        
        if not history:
            return None

        # 计算平均建议
        recommendations = [r.get('recommendation', '') for r in history if r.get('recommendation')]
        if recommendations:
            from collections import Counter
            most_common = Counter(recommendations).most_common(1)[0][0]
        else:
            most_common = "unknown"

        # 计算平均情绪
        sentiments = [r.get('sentiment', '') for r in history if r.get('sentiment')]
        if sentiments:
            sentiment_counter = Counter(sentiments)
            avg_sentiment = sentiment_counter.most_common(1)[0][0]
        else:
            avg_sentiment = "unknown"

        return {
            "stock_code": stock_code,
            "analysis_count": len(history),
            "first_analysis": history[0]['date'] if history else None,
            "last_analysis": history[-1]['date'] if history else None,
            "most_common_recommendation": most_common,
            "average_sentiment": avg_sentiment,
            "price_history": [
                {"date": r['date'], "price": r['price']}
                for r in history[-10:] if r.get('price')
            ]
        }


if __name__ == "__main__":
    store = AShareMemoryStore()

    # 测试存储
    print("=" * 60)
    print("A 股分析记忆存储测试")
    print("=" * 60)

    test_data = {
        "stock_code": "600519",
        "stock_name": "贵州茅台",
        "price": 1800.50,
        "change_percent": 1.25,
        "technical": {"signal": "bullish"},
        "sentiment": {"overall_sentiment": "BULLISH"},
        "recommendation": "买入",
        "key_points": [
            "均线多头排列",
            "MACD 金叉",
            "北向资金流入",
            "业绩超预期"
        ],
        "importance": 0.85
    }

    result = store.store_analysis(test_data)
    print(f"✓ 分析记录已存储：{result}")

    # 测试获取历史
    print("\n📊 贵州茅台历史分析摘要:")
    summary = store.get_analysis_summary("600519")
    if summary:
        print(f"  分析次数：{summary['analysis_count']}")
        print(f"  首次分析：{summary['first_analysis']}")
        print(f"  最近分析：{summary['last_analysis']}")
        print(f"  主要建议：{summary['most_common_recommendation']}")
        print(f"  平均情绪：{summary['average_sentiment']}")
