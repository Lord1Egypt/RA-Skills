#!/usr/bin/env python3
"""
A2A - Agent互联互通 简洁优雅实现
"""
import asyncio, json, uuid
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Callable
from enum import Enum

# ==================== 协议 ====================
class MsgType(Enum): CALL="call"; CAST="cast"; TASK="task"

@dataclass
class Msg:
    id: str=""; typ: str="call"; src: str=""; dst: str=""; action: str=""; params: dict=None
    def __post_init__(self): self.params=self.params or {}
    def to_dict(self): return {k:v for k,v in asdict(self).items() if v}

@dataclass  
class Resp:
    id: str; status: str; result: dict=None; error: str=None
    def __post_init__(self): self.result=self.result or {}
    def to_dict(self): return {k:v for k,v in asdict(self).items() if v}

@dataclass
class Agent:
    id: str; name: str; endpoint: str; caps: dict

# ==================== 核心组件 ====================
class Registry:
    """轻量注册中心"""
    def __init__(s): s.agents={}
    def reg(s, a): s.agents[a.id]=a
    def find(s,c=None)->List[Agent]: return [a for a in s.agents.values() if not c or c in a.caps]

class Server:
    """优雅服务端 - 装饰器注册"""
    def __init__(s, id, host="0.0.0.0", port=8766):
        s.id, s.host, s.port, s.h={}, host, port, {}
    def action(s, n): return lambda f: s.h.__setitem__(n,f) or f
    async def handle(s, m:dict)->dict:
        try:
            msg=Msg(**{k:v for k,v in m.items() if k in Msg.__annotations__})
            h=s.h.get(msg.action)
            r=await h(msg.params) if h else None
            return Resp(id=m.get("id",""), status="ok", result=r).to_dict()
        except Exception as e:
            return Resp(id=m.get("id",""), status="error", error=str(e)).to_dict()

class Client:
    """高性能客户端 - 连接池"""
    def __init__(s, aid, pool=10):
        s.aid, s.pool, s.conn=aid, pool, {}
    async def call(s, ep, act, p, to=30)->dict:
        import websockets
        if ep not in s.conn:
            s.conn[ep]=await websockets.connect(ep, max_size=s.pool)
        msg=Msg(id=uuid.uuid4().hex[:8], typ="call", src=s.aid, action=act, params=p).to_dict()
        await s.conn[ep].send(json.dumps(msg))
        return json.loads(await asyncio.wait_for(s.conn[ep].recv(), timeout=to))
    async def cast(s, ep, act, p):
        import websockets
        if ep not in s.conn:
            s.conn[ep]=await websockets.connect(ep, max_size=s.pool)
        msg=Msg(id=uuid.uuid4().hex[:8], typ="cast", src=s.aid, action=act, params=p).to_dict()
        await s.conn[ep].send(json.dumps(msg))

# ==================== 导出 ====================
__all__=["Msg","Resp","Agent","Registry","Server","Client","MsgType"]
