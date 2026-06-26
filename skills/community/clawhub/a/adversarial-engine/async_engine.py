#!/usr/bin/env python3
"""
异步多模型对抗引擎 - 支持WebSocket实时推送
基于engine.py的异步版本

作者: 海狸 🦫
"""

import asyncio
import json
import time
import sqlite3
import aiohttp
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import subprocess
import tempfile

sys.path.insert(0, "/home/admin/.openclaw/workspace/multi_agent_engine")
try:
    from api_key_manager import get_key_router
    HAS_KEY_ROUTER = True
except ImportError:
    HAS_KEY_ROUTER = False

# 配置
BASE_URL = "https://coding.dashscope.aliyuncs.com/v1/chat/completions"
DEFAULT_API_KEY = "sk-sp-2b89d1b9a55d4cb9a8094c9127459aab"

ROLES = {
    "architect": {
        "model": "qwen3.5-plus",
        "name": "架构师",
        "emoji": "🏗️",
        "persona": "严谨、系统化、追求框架完整性",
        "task": "提出方案框架，设计整体架构",
        "key_type": "primary"
    },
    "engineer": {
        "model": "qwen3-coder-plus",
        "name": "工程师",
        "emoji": "🔧",
        "persona": "务实、高效、代码优先",
        "task": "实现方案，生成可执行代码",
        "key_type": "coder"
    },
    "security": {
        "model": "kimi-k2.5",
        "name": "安全官",
        "emoji": "🔍",
        "persona": "挑剔、攻击性、找漏洞",
        "task": "挑错攻击，指出方案缺陷",
        "key_type": "vision"
    },
    "judge": {
        "model": "MiniMax-M2.5",
        "name": "仲裁者",
        "emoji": "✅",
        "persona": "中立、公正、综合评判",
        "task": "评判辩论，判断是否收敛",
        "key_type": "primary"
    }
}


@dataclass
class DebateRound:
    round_num: int
    role: str
    model: str
    input_prompt: str
    output_content: str
    reasoning: str = ""
    tokens_used: int = 0
    latency_ms: int = 0
    code_executed: str = ""
    code_result: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class DebateSession:
    session_id: str
    topic: str
    rounds: List[DebateRound] = field(default_factory=list)
    final_consensus: str = ""
    total_tokens: int = 0
    total_time_ms: int = 0
    status: str = "pending"
    convergence_score: float = 0.0
    knowledge_used: List[str] = field(default_factory=list)


class CodeSandbox:
    """代码沙箱"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
    
    def run_safely(self, code: str) -> Tuple[bool, str]:
        if not code or not code.strip():
            return False, "无代码可执行"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name
        
        try:
            result = subprocess.run(
                ['python3', temp_path],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd='/tmp'
            )
            
            if result.returncode == 0:
                return True, result.stdout or "(执行成功)"
            else:
                return False, f"执行错误:\n{result.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, f"超时(>{self.timeout}秒)"
        except Exception as e:
            return False, f"异常: {str(e)}"
        finally:
            os.unlink(temp_path)


class ConvergenceChecker:
    """收敛判断器"""
    
    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold
    
    def check(self, content: str) -> Tuple[bool, float]:
        positive = ["共识达成", "方案收敛", "最终方案", "一致同意"]
        negative = ["未收敛", "继续辩论", "仍有分歧"]
        
        score = 0.5
        for kw in positive:
            if kw in content:
                score += 0.15
        for kw in negative:
            if kw in content:
                score -= 0.15
        
        score = max(0.0, min(1.0, score))
        return score >= self.threshold, score


async def call_llm_async(model: str, system_prompt: str, user_prompt: str) -> Dict:
    """异步调用LLM"""
    start_time = time.time()
    
    api_key = DEFAULT_API_KEY
    if HAS_KEY_ROUTER:
        router = get_key_router()
        api_key = router.request_key(model)
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 2000,
        "temperature": 0.7
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(BASE_URL, headers=headers, json=payload, timeout=90) as resp:
                if resp.status != 200:
                    return {"success": False, "error": f"API错误 {resp.status}", "model": model}
                
                data = await resp.json()
                choice = data.get("choices", [{}])[0]
                message = choice.get("message", {})
                
                latency_ms = int((time.time() - start_time) * 1000)
                
                return {
                    "content": message.get("content", ""),
                    "reasoning": message.get("reasoning_content", ""),
                    "tokens": data.get("usage", {}).get("total_tokens", 0),
                    "latency_ms": latency_ms,
                    "model": model,
                    "success": True
                }
                
    except asyncio.TimeoutError:
        return {"success": False, "error": "超时90秒", "model": model}
    except Exception as e:
        return {"success": False, "error": str(e), "model": model}


class AsyncAdversarialEngine:
    """异步多模型对抗引擎"""
    
    def __init__(self, db_path: str = "/home/admin/.openclaw/workspace/data/adversarial_debates.db"):
        self.db_path = db_path
        self.code_sandbox = CodeSandbox()
        self.convergence_checker = ConvergenceChecker()
        self.ws_manager = None  # WebSocket管理器（外部注入）
        self._init_db()
    
    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS debates (
                session_id TEXT PRIMARY KEY,
                topic TEXT,
                final_consensus TEXT,
                total_tokens INTEGER,
                total_time_ms INTEGER,
                status TEXT,
                convergence_score REAL,
                knowledge_used TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rounds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                round_num INTEGER,
                role TEXT,
                model TEXT,
                input_prompt TEXT,
                output_content TEXT,
                reasoning TEXT,
                code_executed TEXT,
                code_result TEXT,
                tokens_used INTEGER,
                latency_ms INTEGER,
                timestamp TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES debates(session_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _build_prompt(self, role_key: str, round_num: int, history: List[DebateRound], topic: str) -> Tuple[str, str]:
        role = ROLES[role_key]
        
        system_prompt = f"""你是{role['emoji']} {role['name']}。

你的性格：{role['persona']}
你的任务：{role['task']}

辩论规则：
1. 必须基于事实和逻辑发言
2. 每轮必须有新内容推进
3. 最终目标是达成共识

请用中文回复，保持专业但有个性的风格。"""
        
        history_text = ""
        if history:
            history_text = "\n\n=== 前几轮辩论 ===\n"
            for r in history[-4:]:
                r_info = ROLES.get(r.role, {})
                history_text += f"\n{r_info.get('emoji', '?')} {r_info.get('name', r.role)}:\n{r.output_content[:400]}\n"
                if r.code_result:
                    history_text += f"  💻 代码结果: {r.code_result[:150]}\n"
        
        if role_key == "architect":
            user_prompt = f"主题：{topic}\n\n请提出方案框架。" if round_num == 1 else f"{history_text}\n\n请修正方案。"
        elif role_key == "engineer":
            user_prompt = f"{history_text}\n\n请实现方案并生成Python代码(用```python包裹)。"
        elif role_key == "security":
            user_prompt = f"{history_text}\n\n请攻击方案，找漏洞。"
        else:
            user_prompt = f"{history_text}\n\n评判辩论：是否有共识？"
        
        return system_prompt, user_prompt
    
    def _extract_code(self, content: str) -> str:
        if "```python" in content:
            start = content.find("```python") + 9
            end = content.find("```", start)
            return content[start:end].strip() if end > start else ""
        return ""
    
    async def broadcast(self, msg: dict):
        """广播到WebSocket"""
        if self.ws_manager:
            await self.ws_manager.broadcast(msg)
    
    async def run_debate(self, topic: str, max_rounds: int = 3, enable_code_sandbox: bool = True) -> DebateSession:
        """执行辩论"""
        session_id = f"DEBATE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        session = DebateSession(session_id=session_id, topic=topic)
        
        # 广播开始
        await self.broadcast({
            "type": "debate_started",
            "session_id": session_id,
            "topic": topic,
            "max_rounds": max_rounds
        })
        
        print(f"\n🚀 辩论启动: {topic}")
        
        round_sequence = ["architect", "engineer", "security", "judge"]
        
        for round_num in range(1, max_rounds + 1):
            print(f"\n--- Round {round_num} ---")
            
            for role_key in round_sequence:
                role = ROLES[role_key]
                
                system_prompt, user_prompt = self._build_prompt(role_key, round_num, session.rounds, topic)
                
                print(f"{role['emoji']} {role['name']} 发言中...")
                
                # 广播开始发言
                await self.broadcast({
                    "type": "round_started",
                    "session_id": session_id,
                    "round": round_num,
                    "role": role_key,
                    "role_name": role["name"]
                })
                
                result = await call_llm_async(role["model"], system_prompt, user_prompt)
                
                if not result.get("success"):
                    print(f"❌ 失败: {result.get('error')}")
                    session.status = "error"
                    return session
                
                # 代码执行
                code_executed = ""
                code_result = ""
                if role_key == "engineer" and enable_code_sandbox:
                    code_executed = self._extract_code(result["content"])
                    if code_executed:
                        success, code_result = self.code_sandbox.run_safely(code_executed)
                        print(f"💻 代码执行: {'✅' if success else '❌'}")
                
                # 记录
                debate_round = DebateRound(
                    round_num=round_num,
                    role=role_key,
                    model=role["model"],
                    input_prompt=user_prompt,
                    output_content=result["content"],
                    reasoning=result.get("reasoning", ""),
                    tokens_used=result["tokens"],
                    latency_ms=result["latency_ms"],
                    code_executed=code_executed,
                    code_result=code_result
                )
                session.rounds.append(debate_round)
                session.total_tokens += result["tokens"]
                session.total_time_ms += result["latency_ms"]
                
                # 广播完成
                await self.broadcast({
                    "type": "round_completed",
                    "session_id": session_id,
                    "round": round_num,
                    "role": role_key,
                    "content": result["content"][:500],
                    "tokens": result["tokens"],
                    "latency_ms": result["latency_ms"],
                    "code_result": code_result[:200] if code_result else None
                })
                
                print(f"✅ {result['tokens']} tokens, {result['latency_ms']}ms")
                
                # 收敛判断
                if role_key == "judge":
                    is_converged, score = self.convergence_checker.check(result["content"])
                    session.convergence_score = score
                    
                    if is_converged:
                        print(f"✅ 共识达成！收敛度: {score:.2f}")
                        session.final_consensus = result["content"]
                        session.status = "done"
                        break
                
                await asyncio.sleep(0.3)
            
            if session.status == "done":
                break
        else:
            last_judge = [r for r in session.rounds if r.role == "judge"][-1]
            session.final_consensus = last_judge.output_content
            session.status = "partial"
        
        # 保存
        self._save_session(session)
        
        # 广播完成
        await self.broadcast({
            "type": "debate_completed",
            "session_id": session_id,
            "status": session.status,
            "convergence_score": session.convergence_score,
            "total_tokens": session.total_tokens,
            "consensus": session.final_consensus[:500]
        })
        
        print(f"\n🎉 完成！状态: {session.status}, 收敛度: {session.convergence_score:.2f}")
        return session
    
    def _save_session(self, session: DebateSession):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO debates 
            (session_id, topic, final_consensus, total_tokens, total_time_ms, status, convergence_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (session.session_id, session.topic, session.final_consensus,
              session.total_tokens, session.total_time_ms, session.status, session.convergence_score))
        
        for r in session.rounds:
            cursor.execute("""
                INSERT INTO rounds 
                (session_id, round_num, role, model, input_prompt, output_content,
                 reasoning, code_executed, code_result, tokens_used, latency_ms, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (session.session_id, r.round_num, r.role, r.model, r.input_prompt,
                  r.output_content, r.reasoning, r.code_executed, r.code_result,
                  r.tokens_used, r.latency_ms, r.timestamp))
        
        conn.commit()
        conn.close()


# 测试
if __name__ == "__main__":
    engine = AsyncAdversarialEngine()
    session = asyncio.run(engine.run_debate("6061铝合金CNC加工优化", max_rounds=1))
    print(f"\n结果: {session.status}")