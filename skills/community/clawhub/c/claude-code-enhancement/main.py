#!/usr/bin/env python3
"""
Claude Code Enhancement Skill - 主入口
整合所有增强模块的统一接口
"""

import sys
import os
from pathlib import Path
from typing import Optional

# 添加模块路径
SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))

# 导入子模块
from coordinator.coordinator import Coordinator, get_coordinator
from permission.permission import PermissionSystem as PermSystem, get_permission_system
from memory.memory import MemorySystem, get_memory_system
from workflow.workflow import TaskWorkflow, get_workflow
from agent.agent_tool import EnhancedAgentTool, get_agent_tool


class ClaudeCodeEnhancement:
    """Claude Code 增强主类"""
    
    def __init__(self):
        self.coordinator = get_coordinator()
        self.permission = get_permission_system()
        self.memory = get_memory_system()
        self.workflow = get_workflow()
        self.agent = get_agent_tool()
    
    def help(self) -> str:
        """帮助信息"""
        return """
🤖 Claude Code Enhancement Skill

基于 Claude Code 51万行源码设计的 OpenClaw 增强模块

---

### 📋 可用命令

**Coordinator 模式 (多 Agent 协调)**
- `/coord start` - 启动协调者模式
- `/coord spawn <描述> <提示>` - 派生新 Worker
- `/coord status` - 查看 Worker 状态
- `/coord stop` - 退出协调者模式

**权限系统**
- `/perm status` - 查看权限状态
- `/perm mode <模式>` - 设置权限模式 (default/auto/bypass/plan)

**记忆系统**
- `/memory` - 显示记忆摘要
- `/memory add <类型> <内容>` - 添加记忆
- `/memory search <关键词>` - 搜索记忆

**任务工作流**
- `/task create <描述>` - 创建任务
- `/task progress` - 查看任务进度
- `/task next` - 进入下一阶段
- `/task complete <结果>` - 标记完成

**增强 Agent**
- `/agent create <描述> <提示>` - 创建 Agent
- `/agent status <id>` - 查看 Agent 状态
- `/agent list` - 列出所有 Agent

---

### 🔧 配置

默认配置位于: `~/.openclaw/workspace/skills/claude-code-enhancement/config.yaml`

如需修改配置，请编辑该文件。

---

### 📚 文档

完整文档: `~/.openclaw/workspace/skills/claude-code-enhancement/SKILL.md`

"""
    
    def status(self) -> str:
        """获取整体状态"""
        lines = [
            "🔧 **Claude Code Enhancement 状态**",
            "",
            "**Coordinator:** " + ("✅ 已启动" if self.coordinator.active else "❌ 未启动"),
            f"   Worker 数量: {len(self.coordinator.workers)}",
            "",
            f"**权限模式:** {self.permission.mode.value}",
            f"   规则数量: {len(self.permission.rules)}",
            "",
            f"**记忆条目:** {sum(len(v) for v in self.memory.entries.values())}",
            "",
            f"**任务数量:** {len(self.workflow.tasks)}",
            "",
            f"**Agent 数量:** {len(self.agent.agents)}",
        ]
        return "\n".join(lines)


# 全局实例
_enhancement: Optional[ClaudeCodeEnhancement] = None


def get_enhancement() -> ClaudeCodeEnhancement:
    """获取全局增强实例"""
    global _enhancement
    if _enhancement is None:
        _enhancement = ClaudeCodeEnhancement()
    return _enhancement


# CLI 接口
if __name__ == "__main__":
    enhancement = get_enhancement()
    
    if len(sys.argv) < 2:
        print(enhancement.help())
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "help":
        print(enhancement.help())
    elif cmd == "status":
        print(enhancement.status())
    else:
        # 传递命令给子模块
        if cmd == "coord":
            from coordinator.coordinator import get_coordinator
            coord = get_coordinator()
            subcmd = sys.argv[2] if len(sys.argv) > 2 else "status"
            
            if subcmd == "start":
                print(coord.start())
            elif subcmd == "status":
                print(coord.status())
            elif subcmd == "stop":
                print(coord.stop(sys.argv[3] if len(sys.argv) > 3 else None))
            elif subcmd == "spawn" and len(sys.argv) > 4:
                print(coord.spawn(sys.argv[3], " ".join(sys.argv[4:])))
            else:
                print(f"未知 coord 命令: {subcmd}")
        
        elif cmd == "perm":
            perm = get_permission_system()
            subcmd = sys.argv[2] if len(sys.argv) > 2 else "status"
            
            if subcmd == "status":
                print(perm.get_status())
            elif subcmd == "mode" and len(sys.argv) > 3:
                perm.set_mode(sys.argv[3])
                print(f"✅ 权限模式已设置为: {sys.argv[3]}")
            else:
                print(f"未知 perm 命令: {subcmd}")
        
        elif cmd == "memory":
            mem = get_memory_system()
            subcmd = sys.argv[2] if len(sys.argv) > 2 else "summary"
            
            if subcmd == "summary" or subcmd == "status":
                print(mem.get_summary())
            elif subcmd == "add" and len(sys.argv) > 4:
                print(mem.add(sys.argv[3], " ".join(sys.argv[4:])))
            elif subcmd == "search" and len(sys.argv) > 3:
                results = mem.search(" ".join(sys.argv[3:]))
                print(f"找到 {len(results)} 条结果:")
                for r in results:
                    print(f"  [{r.type}] {r.content}")
            elif subcmd == "clear":
                print(mem.clear(sys.argv[3] if len(sys.argv) > 3 else None))
            else:
                print(f"未知 memory 命令: {subcmd}")
        
        elif cmd == "task":
            wf = get_workflow()
            subcmd = sys.argv[2] if len(sys.argv) > 2 else "list"
            
            if subcmd == "list":
                print(wf.list_tasks())
            elif subcmd == "create" and len(sys.argv) > 3:
                print(wf.create(" ".join(sys.argv[3:])))
            elif subcmd == "progress":
                print(wf.progress(sys.argv[3] if len(sys.argv) > 3 else None))
            elif subcmd == "next":
                print(wf.next_stage(task_id=sys.argv[3] if len(sys.argv) > 3 else None))
            elif subcmd == "complete" and len(sys.argv) > 3:
                print(wf.complete(" ".join(sys.argv[3:]), sys.argv[3] if len(sys.argv) > 4 else None))
            else:
                print(f"未知 task 命令: {subcmd}")
        
        elif cmd == "agent":
            agt = get_agent_tool()
            subcmd = sys.argv[2] if len(sys.argv) > 2 else "list"
            
            if subcmd == "list":
                print(agt.list_agents())
            elif subcmd == "status" and len(sys.argv) > 3:
                print(agt.get_status(sys.argv[3]))
            elif subcmd == "stop" and len(sys.argv) > 3:
                print(agt.stop_agent(sys.argv[3]))
            else:
                print(f"未知 agent 命令: {subcmd}")
        
        else:
            print(f"未知命令: {cmd}")
            print("运行 'python3 main.py help' 查看帮助")


from typing import Optional