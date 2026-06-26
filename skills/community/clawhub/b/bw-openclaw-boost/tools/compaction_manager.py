#!/usr/bin/env python3
"""
多层压缩管理系统
参考 Claude Code 的 autoCompact / microCompact / timeBased 设计

压缩层级：
1. microCompact — 快速清理：只清理工具调用的中间结果
2. autoCompact — 自动压缩：当 token 达到阈值时压缩对话历史
3. timeBasedCompact — 时间基准：每小时压缩一次

阈值配置：
- microCompact: 60% context
- autoCompact: 80% context
- timeBased: 每60分钟

压缩策略：
- 保留系统提示词
- 保留最近 N 条消息
- 保留重要上下文（项目状态、任务目标）
- 其他压缩为摘要
"""

import os
import re
import json
from pathlib import Path

# 技能本地目录
SKILL_ROOT = Path(__file__).parent.parent
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, field
from threading import Lock

MEMORY_ROOT = SKILL_ROOT / "memory"
COMPACTION_LOG_DIR = MEMORY_ROOT / "logs" / "compaction"

# 上下文窗口阈值（MiniMax-M2.7-highspeed: 205k tokens）
CONTEXT_WINDOW = 205_000

# 压缩阈值
THRESHOLDS = {
    "microCompact": 0.60,   # 60% = 123k tokens
    "autoCompact": 0.80,    # 80% = 164k tokens
    "timeBased": 60,        # 60 分钟
}

# 保留策略
PRESERVE = {
    "recent_messages": 10,   # 保留最近10条消息
    "system_prompt": True,   # 保留系统提示词
    "today_summary": True,  # 保留今日摘要
}

@dataclass
class CompactionRecord:
    """压缩记录"""
    timestamp: str
    level: str  # microCompact / autoCompact / timeBased
    tokens_before: int
    tokens_after: int
    messages_before: int
    messages_after: int
    duration_ms: int
    summary: str


class CompactionManager:
    """多层压缩管理器"""
    
    _instance: Optional['CompactionManager'] = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.last_compaction: Optional[datetime] = None
        self.compaction_count = 0
        self.total_tokens_freed = 0
        self._load_state()
    
    def _load_state(self):
        """加载压缩状态"""
        state_file = COMPACTION_LOG_DIR / "state.json"
        if state_file.exists():
            try:
                data = json.loads(state_file.read_text())
                self.last_compaction = datetime.fromisoformat(data.get("last_compaction", "2000-01-01T00:00:00"))
                self.compaction_count = data.get("compaction_count", 0)
                self.total_tokens_freed = data.get("total_tokens_freed", 0)
            except:
                pass
    
    def _save_state(self):
        """保存压缩状态"""
        COMPACTION_LOG_DIR.mkdir(parents=True, exist_ok=True)
        state_file = COMPACTION_LOG_DIR / "state.json"
        data = {
            "last_compaction": (self.last_compaction or datetime.now()).isoformat(),
            "compaction_count": self.compaction_count,
            "total_tokens_freed": self.total_tokens_freed,
        }
        state_file.write_text(json.dumps(data, indent=2))
    
    def estimate_tokens(self, text: str) -> int:
        """估算文本的 token 数量（粗略：中文约 2 字符/token，英文约 4 字符/token）"""
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        other_chars = len(text) - chinese_chars
        return int(chinese_chars / 2 + other_chars / 4)
    
    def get_context_usage(self, session_key: str = "main") -> Dict[str, Any]:
        """获取当前上下文使用情况"""
        try:
            import subprocess
            result = subprocess.run(
                ["openclaw", "status"],
                capture_output=True, text=True, timeout=30
            )
            output = result.stdout + result.stderr
            
            # 解析当前 session 的 context 使用
            for line in output.split('\n'):
                if session_key in line and '/205k' in line:
                    match = re.search(r'(\d+)k/(\d+)k\s*\((\d+)%\)', line)
                    if match:
                        used_k = int(match.group(1))
                        max_k = int(match.group(2))
                        pct = int(match.group(3))
                        return {
                            "used_tokens": used_k * 1000,
                            "max_tokens": max_k * 1000,
                            "percent": pct,
                            "level": self._get_level(pct / 100)
                        }
        except:
            pass
        
        return {"used_tokens": 0, "max_tokens": CONTEXT_WINDOW, "percent": 0, "level": "none"}
    
    def _get_level(self, usage_ratio: float) -> str:
        """根据使用率确定压缩级别"""
        if usage_ratio >= THRESHOLDS["autoCompact"]:
            return "autoCompact"
        elif usage_ratio >= THRESHOLDS["microCompact"]:
            return "microCompact"
        elif self._should_time_compact():
            return "timeBased"
        return "none"
    
    def _should_time_compact(self) -> bool:
        """检查是否应该进行时间基准压缩"""
        if self.last_compaction is None:
            return True
        elapsed = datetime.now() - self.last_compaction
        return elapsed.total_seconds() >= THRESHOLDS["timeBased"] * 60
    
    def micro_compact(self, messages: List[Dict]) -> Tuple[List[Dict], CompactionRecord]:
        """
        microCompact — 快速清理
        只清理工具调用的中间结果，保留消息结构
        """
        start_time = datetime.now()
        tokens_before = sum(self.estimate_tokens(m.get("content", "")) for m in messages)
        
        # 保留策略：
        # 1. 保留用户消息和助手最终回复
        # 2. 压缩或删除工具调用的中间结果
        compacted = []
        tool_result_count = 0
        
        for msg in messages:
            msg_type = msg.get("type", "")
            content = msg.get("content", "")
            
            if msg_type in ["user", "assistant"]:
                compacted.append(msg)
            elif msg_type == "tool_result":
                # 保留工具结果但截断长内容
                tokens = self.estimate_tokens(content)
                if tokens > 500:  # 超过500 tokens 的工具结果截断
                    compacted.append({
                        **msg,
                        "content": content[:1000] + f"\n[... 已压缩，原始长度 {tokens} tokens ...]",
                        "_compact": "micro"
                    })
                    tool_result_count += 1
                else:
                    compacted.append(msg)
            else:
                compacted.append(msg)
        
        tokens_after = sum(self.estimate_tokens(m.get("content", "")) for m in compacted)
        duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        record = CompactionRecord(
            timestamp=datetime.now().isoformat(),
            level="microCompact",
            tokens_before=tokens_before,
            tokens_after=tokens_after,
            messages_before=len(messages),
            messages_after=len(compacted),
            duration_ms=duration_ms,
            summary=f"压缩了 {tool_result_count} 个工具结果"
        )
        
        return compacted, record
    
    def auto_compact(self, messages: List[Dict]) -> Tuple[List[Dict], CompactionRecord]:
        """
        autoCompact — 自动压缩
        将较旧的对话压缩为摘要，保留最近消息
        """
        start_time = datetime.now()
        tokens_before = sum(self.estimate_tokens(m.get("content", "")) for m in messages)
        
        if len(messages) <= PRESERVE["recent_messages"]:
            # 消息太少，不压缩
            return messages, CompactionRecord(
                timestamp=datetime.now().isoformat(),
                level="autoCompact",
                tokens_before=tokens_before,
                tokens_after=tokens_before,
                messages_before=len(messages),
                messages_after=len(messages),
                duration_ms=0,
                summary="消息太少，跳过压缩"
            )
        
        # 保留最近 N 条消息
        recent = messages[-PRESERVE["recent_messages"]:]
        older = messages[:-PRESERVE["recent_messages"]]
        
        # 生成旧消息的摘要
        older_summary = self._summarize_messages(older)
        
        # 构建压缩后的消息列表
        compacted = [
            {
                "type": "system",
                "role": "system",
                "content": f"[早期对话已压缩为摘要，共 {len(older)} 条消息，约 {self.estimate_tokens(''.join(m.get('content','') for m in older))} tokens]\n\n摘要：{older_summary}",
                "_compact": "auto"
            }
        ] + recent
        
        tokens_after = sum(self.estimate_tokens(m.get("content", "")) for m in compacted)
        duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        freed = tokens_before - tokens_after
        self.total_tokens_freed += freed
        
        record = CompactionRecord(
            timestamp=datetime.now().isoformat(),
            level="autoCompact",
            tokens_before=tokens_before,
            tokens_after=tokens_after,
            messages_before=len(messages),
            messages_after=len(compacted),
            duration_ms=duration_ms,
            summary=f"释放 {freed} tokens，压缩了 {len(older)} 条旧消息"
        )
        
        return compacted, record
    
    def _summarize_messages(self, messages: List[Dict], max_length: int = 2000) -> str:
        """生成消息摘要"""
        if not messages:
            return "无"
        
        # 提取关键信息
        topics = []
        for msg in messages:
            content = msg.get("content", "")[:200]  # 每条取前200字符
            if content:
                # 提取前几个字作为主题
                first_line = content.split('\n')[0][:50]
                if first_line:
                    topics.append(first_line)
        
        summary = f"讨论了 {len(messages)} 条消息，主题包括：{'；'.join(topics[:5])}"
        
        if len(summary) > max_length:
            summary = summary[:max_length] + "..."
        
        return summary
    
    def time_based_compact(self, messages: List[Dict]) -> Tuple[List[Dict], CompactionRecord]:
        """
        timeBased — 时间基准压缩
        每隔一段时间进行一次轻度压缩
        """
        start_time = datetime.now()
        tokens_before = sum(self.estimate_tokens(m.get("content", "")) for m in messages)
        
        # 只做轻度清理
        compacted = []
        removed = 0
        
        for msg in messages:
            msg_type = msg.get("type", "")
            content = msg.get("content", "")
            
            # 保留所有用户消息和最终助手回复
            if msg_type in ["user", "assistant"]:
                compacted.append(msg)
            # 工具结果保留但截断
            elif msg_type == "tool_result":
                if self.estimate_tokens(content) > 300:
                    compacted.append({
                        **msg,
                        "content": content[:500] + "\n[...已截断...]",
                        "_compact": "timeBased"
                    })
                    removed += 1
                else:
                    compacted.append(msg)
            else:
                compacted.append(msg)
        
        tokens_after = sum(self.estimate_tokens(m.get("content", "")) for m in compacted)
        duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        self.last_compaction = datetime.now()
        self.compaction_count += 1
        self._save_state()
        
        freed = tokens_before - tokens_after
        
        record = CompactionRecord(
            timestamp=datetime.now().isoformat(),
            level="timeBased",
            tokens_before=tokens_before,
            tokens_after=tokens_after,
            messages_before=len(messages),
            messages_after=len(compacted),
            duration_ms=duration_ms,
            summary=f"时间基准压缩，移除 {removed} 个长工具结果"
        )
        
        return compacted, record
    
    def should_compact(self) -> Tuple[bool, str]:
        """
        检查是否应该进行压缩
        返回: (是否压缩, 压缩级别)
        """
        usage = self.get_context_usage()
        level = usage.get("level", "none")
        
        if level != "none":
            return True, level
        
        # 检查时间基准
        if self._should_time_compact():
            return True, "timeBased"
        
        return False, "none"
    
    def compact_if_needed(self, messages: List[Dict]) -> Tuple[List[Dict], Optional[CompactionRecord]]:
        """
        主入口：如果需要则压缩
        """
        should, level = self.should_compact()
        
        if not should:
            return messages, None
        
        if level == "microCompact":
            return self.micro_compact(messages)
        elif level == "autoCompact":
            return self.auto_compact(messages)
        elif level == "timeBased":
            return self.time_based_compact(messages)
        
        return messages, None
    
    def get_status(self) -> str:
        """获取压缩状态"""
        usage = self.get_context_usage()
        last = self.last_compaction.strftime("%Y-%m-%d %H:%M") if self.last_compaction else "从未"
        
        return f"""=== 压缩系统状态 ===

上下文使用: {usage['percent']}%
级别: {usage['level']}
上次压缩: {last}
压缩次数: {self.compaction_count}
累计释放: {self.total_tokens_freed:,} tokens

阈值配置:
  microCompact: {int(THRESHOLDS['microCompact']*100)}% ({int(CONTEXT_WINDOW * THRESHOLDS['microCompact']/1000)}k tokens)
  autoCompact: {int(THRESHOLDS['autoCompact']*100)}% ({int(CONTEXT_WINDOW * THRESHOLDS['autoCompact']/1000)}k tokens)
  timeBased: {THRESHOLDS['timeBased']} 分钟"""


if __name__ == "__main__":
    import sys
    
    manager = CompactionManager()
    
    if len(sys.argv) < 2:
        print(manager.get_status())
    else:
        cmd = sys.argv[1]
        
        if cmd == "status":
            print(manager.get_status())
        
        elif cmd == "check":
            print("检查压缩需求...")
            should, level = manager.should_compact()
            if should:
                print(f"建议压缩级别: {level}")
                print("""
压缩触发条件：
- microCompact: 上下文使用 ≥ 60%
- autoCompact: 上下文使用 ≥ 80%
- timeBased: 距离上次压缩 ≥ 60分钟
""")
            else:
                print("不需要压缩")
        
        elif cmd == "compact":
            # 执行压缩
            print("执行压缩...")
            should, level = manager.should_compact()
            if not should:
                print("不需要压缩")
            else:
                print(f"执行 {level}...")
                # 注意：实际压缩需要传入消息列表，这里只记录状态
                print(f"已记录压缩需求: {level}")
        
        elif cmd == "test":
            # 测试压缩
            test_messages = [
                {"type": "user", "content": "你好，帮我查一下今天的天气"},
                {"type": "assistant", "content": "好的，我来帮你查天气。"},
                {"type": "tool_result", "content": "北京今天晴，25度"},
                {"type": "assistant", "content": "北京今天天气晴朗，气温25度。"},
                {"type": "tool_result", "content": "x" * 2000},  # 长工具结果
            ] * 5  # 多条
            
            print(f"测试消息数: {len(test_messages)}")
            
            compact, record = manager.micro_compact(test_messages)
            print(f"microCompact: {record.summary}")
            
            compact, record = manager.auto_compact(test_messages)
            print(f"autoCompact: {record.summary}")
