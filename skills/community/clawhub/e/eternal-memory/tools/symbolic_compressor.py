#!/usr/bin/env python3
"""
L1b_pre 符号化压缩器 v1.0 — 吸收TencentDB Agent Memory符号化思想
=========================================================================
设计原则：
  1. 只压缩不蒸馏 —— 原始数据永不丢失（在L1a归档中完整保留）
  2. 符号化 ≠ 摘要化 —— 转换为结构化符号（Mermaid/JSON）而非自然语言摘要
  3. 渐进解压 —— 符号版→压缩版→原始版，按需加载
  4. 类型感知 —— 回测报告/命令输出/对话日志 各自有专属符号模板

收益：
  - Token减少50-60%（TencentDB实测61%，我们保守估计50%）
  - 检索精确度提升（结构化符号比自然语言更容易匹配）
  - 原始在L1a，校验用L1c，检索用符号版

用法：
  from tools.symbolic_compressor import SymbolicCompressor
  sc = SymbolicCompressor()
  result = sc.compress(content, content_type="backtest")
  # result.symbolic -> 符号版（用于检索）
  # result.raw_hash -> 原始SHA256（用于校验）
"""

import json, hashlib, re, os, sys
from datetime import datetime
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class CompressedMemory:
    """压缩后的记忆单元"""
    raw_hash: str              # 原始内容SHA256（链接到L1a归档）
    content_type: str           # 类型：backtest/command/dialogue/code/trade
    symbols: Dict              # 结构化符号表示
    key_metrics: Dict          # 关键指标（快速检索用）
    mermaid: Optional[str] = None  # 可选Mermaid图
    compressed_text: str = ""  # 压缩后文本（~原长的40%）
    original_size: int = 0
    compressed_size: int = 0
    compression_ratio: float = 0.0


class SymbolicCompressor:
    """符号化压缩器 —— 将原始内容转为结构化符号"""
    
    def compress(self, content: str, content_type: str = "auto", 
                 source: str = "", metadata: Dict = None) -> CompressedMemory:
        """压缩入口 —— 根据类型路由到专属压缩器"""
        if content_type == "auto":
            content_type = self._detect_type(content)
        
        raw_hash = hashlib.sha256(content.encode()).hexdigest()
        
        # 路由到专属压缩器
        compressors = {
            "backtest": self._compress_backtest,
            "command": self._compress_command,
            "dialogue": self._compress_dialogue,
            "code": self._compress_code,
            "trade": self._compress_trade,
            "default": self._compress_default,
        }
        
        compressor = compressors.get(content_type, compressors["default"])
        result = compressor(content, raw_hash, source, metadata or {})
        
        # 计算压缩比
        result.original_size = len(content)
        result.compressed_size = len(result.compressed_text) + len(json.dumps(result.symbols, ensure_ascii=False))
        result.compression_ratio = 1 - (result.compressed_size / max(result.original_size, 1))
        
        return result
    
    def _detect_type(self, content: str) -> str:
        """自动检测内容类型"""
        patterns = {
            "backtest": [r"回测", r"backtest", r"夏普", r"Sharpe", r"最大回撤", r"胜率", r"盈亏比"],
            "command": [r"^❯ ", r"^➜ ", r"^\\$ ", r"execut", r"stdout", r"stderr", r"exit.*code"],
            "code": [r"def ", r"class ", r"import ", r"function", r"^#!", r"```python"],
            "trade": [r"开仓", r"平仓", r"止损", r"止盈", r"持仓", r"保证金", r"仓位"],
            "dialogue": [r"大伯", r"小P", r"小四", r"智库", r"小智", r"我认为", r"建议"],
        }
        scores = {}
        for ctype, pats in patterns.items():
            score = sum(1 for p in pats if re.search(p, content, re.IGNORECASE))
            if score > 0:
                scores[ctype] = score
        
        if not scores:
            return "default"
        return max(scores, key=scores.get)
    
    # ══════════════════════════════════════════════
    # 回测报告压缩器
    # ══════════════════════════════════════════════
    
    def _compress_backtest(self, content: str, raw_hash: str, source: str, meta: Dict) -> CompressedMemory:
        """回测报告 → 结构化关键指标"""
        symbols = {
            "type": "backtest",
            "raw_hash": raw_hash[:16],
            "source": source,
        }
        
        # 提取关键指标
        metric_patterns = {
            "total_return": [r"总收益[率]?[:：]\s*([+-]?\d+\.?\d*%?)", r"total.*return[:：]\s*([+-]?\d+\.?\d*)"],
            "sharpe": [r"夏普[比率]?[:：]\s*(\d+\.?\d*)", r"[Ss]harpe[:：]\s*(\d+\.?\d*)"],
            "max_drawdown": [r"最大回撤[:：]\s*([+-]?\d+\.?\d*%?)", r"max.*drawdown[:：]\s*([+-]?\d+\.?\d*)"],
            "win_rate": [r"胜率[:：]\s*(\d+\.?\d*%?)", r"win.*rate[:：]\s*(\d+\.?\d*)"],
            "total_trades": [r"总交易[次数]?[:：]\s*(\d+)", r"total.*trades[:：]\s*(\d+)"],
            "profit_factor": [r"盈亏比[:：]\s*(\d+\.?\d*)", r"profit.*factor[:：]\s*(\d+\.?\d*)"],
            "annual_return": [r"年化收益[率]?[:：]\s*([+-]?\d+\.?\d*%?)"],
        }
        
        key_metrics = {}
        for metric, patterns in metric_patterns.items():
            for pat in patterns:
                m = re.search(pat, content, re.IGNORECASE)
                if m:
                    key_metrics[metric] = m.group(1)
                    break
        
        symbols["metrics"] = key_metrics
        
        # 压缩文本：保留关键行
        lines = content.split("\n")
        important_lines = []
        keywords = ["收益", "回撤", "夏普", "胜率", "盈亏", "交易", "return", "drawdown", 
                     "sharpe", "win", "profit", "trade", "ATR", "止损", "仓位"]
        
        for line in lines:
            if any(kw in line.lower() for kw in keywords):
                important_lines.append(line.strip())
        
        compressed = "\n".join(important_lines[:50])
        
        # Mermaid盈亏曲线（如果有数据）
        mermaid = None
        if key_metrics:
            mermaid = "```mermaid\ngraph TD\n"
            mermaid += f"    A[回测结果] --> B[总收益:{key_metrics.get('total_return','N/A')}]\n"
            mermaid += f"    A --> C[夏普:{key_metrics.get('sharpe','N/A')}]\n"
            mermaid += f"    A --> D[最大回撤:{key_metrics.get('max_drawdown','N/A')}]\n"
            mermaid += f"    A --> E[胜率:{key_metrics.get('win_rate','N/A')}]\n"
            mermaid += "```"
        
        return CompressedMemory(
            raw_hash=raw_hash, content_type="backtest",
            symbols=symbols, key_metrics=key_metrics,
            mermaid=mermaid, compressed_text=compressed
        )
    
    # ══════════════════════════════════════════════
    # 命令输出压缩器
    # ══════════════════════════════════════════════
    
    def _compress_command(self, content: str, raw_hash: str, source: str, meta: Dict) -> CompressedMemory:
        """命令输出 → 成功/失败+关键数据"""
        symbols = {
            "type": "command",
            "raw_hash": raw_hash[:16],
            "source": source,
        }
        
        # 判断成功/失败
        is_error = bool(re.search(r'(error|Error|ERROR|failed|Failed|FAILED|exception|Exception|Traceback)', content))
        has_data = len(content.strip().split("\n")) > 3
        
        # 提取数字型结果
        numbers = re.findall(r'(\d+\.?\d*)\s*(ms|秒|%|KB|MB|GB|条|个|次)', content)
        key_metrics = {
            "status": "❌ 失败" if is_error else "✅ 成功",
            "lines": len(content.split("\n")),
            "has_data": has_data,
            "key_values": [f"{n}{u}" for n, u in numbers[:5]],
        }
        
        symbols["metrics"] = key_metrics
        
        # 压缩版：前20行+最后5行
        lines = content.strip().split("\n")
        if len(lines) > 30:
            compressed = "\n".join(lines[:20] + ["..."] + lines[-5:])
        else:
            compressed = content[:800]
        
        return CompressedMemory(
            raw_hash=raw_hash, content_type="command",
            symbols=symbols, key_metrics=key_metrics,
            compressed_text=compressed
        )
    
    # ══════════════════════════════════════════════
    # 对话日志压缩器
    # ══════════════════════════════════════════════
    
    def _compress_dialogue(self, content: str, raw_hash: str, source: str, meta: Dict) -> CompressedMemory:
        """对话 → 主题+决策+行动项"""
        symbols = {
            "type": "dialogue",
            "raw_hash": raw_hash[:16],
            "source": source,
        }
        
        # 提取主题标签
        topic_patterns = {
            "交易": [r"止损", r"开仓", r"平仓", r"持仓", r"AP", r"PVC", r"MA", r"甲醇", r"苹果"],
            "记忆系统": [r"记忆", r"memory", r"FTS5", r"向量", r"图谱"],
            "系统架构": [r"架构", r"系统", r"引擎", r"升级", r"v\d"],
            "数据分析": [r"回测", r"量化", r"策略", r"指标", r"夏普", r"ATR"],
        }
        
        topics = []
        for topic, pats in topic_patterns.items():
            if any(re.search(p, content) for p in pats):
                topics.append(topic)
        
        symbols["topics"] = topics
        
        # 提取决策（包含"决定"/"确认"/"👍"/"可以"的行）
        decisions = []
        for line in content.split("\n"):
            if re.search(r'(决定|确认|👍|可以|开始|执行|立即|OK|好[的了]|同意|批准)', line):
                decisions.append(line.strip()[:200])
        symbols["decisions"] = decisions[:5]
        
        key_metrics = {
            "topics": topics,
            "decision_count": len(decisions),
            "total_lines": len(content.split("\n")),
        }
        
        # 压缩：保留关键行
        compressed = "\n".join(decisions[:10])
        
        return CompressedMemory(
            raw_hash=raw_hash, content_type="dialogue",
            symbols=symbols, key_metrics=key_metrics,
            compressed_text=compressed
        )
    
    # ══════════════════════════════════════════════
    # 代码压缩器
    # ══════════════════════════════════════════════
    
    def _compress_code(self, content: str, raw_hash: str, source: str, meta: Dict) -> CompressedMemory:
        """代码 → 函数签名+类名+导入+关键参数"""
        symbols = {
            "type": "code",
            "raw_hash": raw_hash[:16],
            "source": source,
        }
        
        # 提取函数定义
        functions = re.findall(r'(?:async\s+)?def\s+(\w+)\s*\((.*?)\)', content)
        # 提取类定义
        classes = re.findall(r'class\s+(\w+)\s*(?:\(.*?\))?:', content)
        # 提取导入
        imports = re.findall(r'(?:from\s+\S+\s+)?import\s+(.+?)(?:\s+#.*)?$', content, re.MULTILINE)
        # 提取关键常量/参数
        constants = re.findall(r'(\w+)\s*=\s*([0-9.]+(?:e[+-]?\d+)?)', content)
        
        symbols["structure"] = {
            "functions": functions,
            "classes": classes,
            "imports": [i.strip() for i in imports[:10]],
            "constants": constants[:20],
        }
        
        key_metrics = {
            "func_count": len(functions),
            "class_count": len(classes),
            "total_lines": len(content.split("\n")),
            "functions": functions[:15],
            "classes": classes[:5],
        }
        
        # 压缩：保留函数签名+类定义
        func_lines = re.findall(r'((?:async\s+)?def\s+\w+\s*\(.*?\).*)', content)
        class_lines = re.findall(r'(class\s+\w+.*?:.*)', content)
        compressed = "\n".join(class_lines + func_lines)[:1000]
        
        return CompressedMemory(
            raw_hash=raw_hash, content_type="code",
            symbols=symbols, key_metrics=key_metrics,
            compressed_text=compressed
        )
    
    # ══════════════════════════════════════════════
    # 交易记录压缩器
    # ══════════════════════════════════════════════
    
    def _compress_trade(self, content: str, raw_hash: str, source: str, meta: Dict) -> CompressedMemory:
        """交易记录 → 品种+方向+价格+仓位+时间"""
        symbols = {
            "type": "trade",
            "raw_hash": raw_hash[:16],
            "source": source,
        }
        
        # 提取交易要素
        patterns = {
            "symbol": [r'(AP|PVC|MA|甲醇|苹果)\d*'],
            "direction": [r'(多|空|多头|空头|做多|做空|买入|卖出|buy|sell|long|short)'],
            "price": [r'(?:价格|价)[:：]\s*(\d+\.?\d*)', r'(\d{2,5})\d*元?[\/每]'],
            "volume": [r'(\d+)\s*手', r'仓位[:：]\s*(\d+\.?\d*)'],
            "stop_loss": [r'止损[:：]\s*(\d+\.?\d*)'],
            "take_profit": [r'止盈[:：]\s*(\d+\.?\d*)'],
        }
        
        key_metrics = {}
        for metric, pats in patterns.items():
            for pat in pats:
                m = re.search(pat, content, re.IGNORECASE)
                if m:
                    val = m.group(1) if m.lastindex else m.group(0)
                    key_metrics[metric] = val
                    break
        
        symbols["trade"] = key_metrics
        
        # 压缩文本
        trade_lines = []
        for line in content.split("\n"):
            if any(kw in line for kw in ["开仓", "平仓", "止损", "止盈", "持仓", "价格", "手"]):
                trade_lines.append(line.strip())
        
        compressed = "\n".join(trade_lines[:30])
        
        # Mermaid状态图
        mermaid = None
        if key_metrics:
            mermaid = "```mermaid\ngraph LR\n"
            mermaid += f"    T[{key_metrics.get('symbol','交易')}]"
            mermaid += f" --> D[{key_metrics.get('direction','?')}]\n"
            if 'price' in key_metrics:
                mermaid += f"    T --> P[价格:{key_metrics['price']}]\n"
            if 'stop_loss' in key_metrics:
                mermaid += f"    T --> SL[止损:{key_metrics['stop_loss']}]\n"
            mermaid += "```"
        
        return CompressedMemory(
            raw_hash=raw_hash, content_type="trade",
            symbols=symbols, key_metrics=key_metrics,
            mermaid=mermaid, compressed_text=compressed
        )
    
    # ══════════════════════════════════════════════
    # 默认压缩器
    # ══════════════════════════════════════════════
    
    def _compress_default(self, content: str, raw_hash: str, source: str, meta: Dict) -> CompressedMemory:
        """默认压缩策略 —— 保留首尾"""
        lines = content.strip().split("\n")
        if len(lines) > 40:
            compressed = "\n".join(lines[:25] + ["..."] + lines[-10:])
        else:
            compressed = content[:1000]
        
        return CompressedMemory(
            raw_hash=raw_hash, content_type="default",
            symbols={"type": "default", "raw_hash": raw_hash[:16]},
            key_metrics={"total_lines": len(lines)},
            compressed_text=compressed
        )


# ── CLI测试 ──
if __name__ == "__main__":
    sc = SymbolicCompressor()
    
    # 测试回测压缩
    bt = """
    总收益率: +45.2%
    夏普比率: 2.31
    最大回撤: -12.8%
    胜率: 58.3%
    总交易次数: 940
    盈亏比: 1.85
    年化收益: +78.6%
    """
    result = sc.compress(bt, "backtest")
    print(f"回测压缩: {result.original_size}→{result.compressed_size}字节(压缩{result.compression_ratio:.0%})")
    print(f"  指标: {result.key_metrics}")
    
    # 测试代码压缩
    code_sample = """
import numpy as np
def calculate_atr(high, low, close, period=14):
    tr = np.maximum(high - low, np.abs(high - close.shift()))
    return tr.rolling(period).mean()

class TradeSystem:
    def __init__(self, symbol, capital=100000):
        self.symbol = symbol
        self.capital = capital
    
    def open_position(self, direction, price, volume):
        return {"direction": direction, "price": price, "volume": volume}
    """
    result = sc.compress(code_sample, "code")
    print(f"代码压缩: {result.original_size}→{result.compressed_size}字节(压缩{result.compression_ratio:.0%})")
    print(f"  函数: {result.key_metrics.get('functions',[])} 类: {result.key_metrics.get('classes',[])}")
    
    # 测试命令输出压缩
    cmd = """
❯ python3 tools/unified_search_ng.py "记忆系统"
=== 融合搜索v3.0(RRF+MMR): 记忆系统 ===
[L1 记忆轨迹 Top8]
1. [L1_fts5] 记忆系统v3.0 — 五层架构...
660ms | RRF+MMR v3.0
技能:0 轨迹:5 世界:0 →3
"""
    result = sc.compress(cmd, "command")
    print(f"命令压缩: {result.original_size}→{result.compressed_size}字节(压缩{result.compression_ratio:.0%})")
    print(f"  状态: {result.key_metrics.get('status')}")
    
    print("\n✅ 符号化压缩器测试完成")
