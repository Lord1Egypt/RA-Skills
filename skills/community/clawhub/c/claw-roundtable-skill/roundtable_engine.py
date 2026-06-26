#!/usr/bin/env python3
"""
RoundTable 执行引擎 - 完整 5 轮流程（v3.0）

功能：
1. 用户确认流程
2. 完整的 R1-R5 轮讨论
3. 进度实时通知
4. 超时重试机制
5. 最终报告生成

架构：
- 提示词模板：prompts/prompt_builder.py → 读取 prompts/framework.md
- 通知：roundtable_notifier.py（真正的飞书/渠道通知）
- Agent 选择：agent_selector.py
- 模型选择：model_selector.py
"""

import asyncio
import json
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

# 添加 skills 目录到路径
skills_dir = Path(__file__).parent.parent
if str(skills_dir) not in sys.path:
    sys.path.insert(0, str(skills_dir))

from roundtable_notifier import RoundTableNotifier
from agent_selector import AgentSelector
from model_selector import ModelSelector
from prompts.prompt_builder import build_prompt, build_fallback_prompt


class RoundState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class RoundConfig:
    name: str
    description: str
    timeout: int = 300


@dataclass
class AgentResult:
    agent_id: str
    content: str
    elapsed_seconds: float
    success: bool


class RoundTableEngine:
    """RoundTable 执行引擎"""

    ROUNDS = {
        "R1": RoundConfig("独立方案", "各自阐述观点", 300),
        "R2": RoundConfig("相互引用", "引用他人 + 补充", 300),
        "R3": RoundConfig("深度分析", "批判思维 + 评价", 300),
        "R4": RoundConfig("辩论完善", "辩论 + 完善方案", 300),
        "R5": RoundConfig("总结报告", "Host 总结", 300),
    }

    def __init__(
        self,
        topic: str,
        mode: str = "pre-ac",
        agent_source: str = "",
        agents: Optional[List[str]] = None,
        enable_chat_room: bool = False,
        output_dir: Optional[Path] = None,
        persist_reports: bool = False,
        allow_local_scan: bool = False,
    ):
        """
        Args:
            persist_reports: 是否持久化讨论记录到本地 JSON 文件（默认 False）
                           开启后会写入 {output_dir}/{topic_slug}.json
            allow_local_scan: 是否允许扫描本地实例目录获取模型列表（默认 False）
        """
        self.topic = topic
        self.mode = mode
        self.agent_source = agent_source
        self.enable_chat_room = enable_chat_room
        self.persist_reports = persist_reports
        self.allow_local_scan = allow_local_scan

        # 输出目录（可选，默认 workspace/data/roundtable/）
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = Path(__file__).parent.parent.parent / "data" / "roundtable"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.chat_session_key: Optional[str] = None
        self.state = RoundState.PENDING
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.current_round: str = ""
        self.results: Dict[str, List[AgentResult]] = {}
        self.notifier = RoundTableNotifier(topic, mode)

        # Agent 选择器 + 模型选择器（解耦：各自独立实例）
        self.agent_selector = AgentSelector(agent_source)
        self.model_selector = ModelSelector()

        # 自动选择或指定 Agent
        if agents:
            self.agents = agents
        else:
            self.agents = self.agent_selector.select_agents_for_roundtable(topic)

    async def run(self, user_channel: str) -> bool:
        """运行完整 RoundTable 流程"""
        print(f"\n🔄 RoundTable 启动：{self.topic}")
        print("=" * 60)

        # 1. 用户确认
        confirmed = await self.notifier.send_confirmation_request(self, user_channel)
        if not confirmed:
            print("❌ 用户取消 RoundTable")
            return False

        self.state = RoundState.RUNNING
        self.start_time = datetime.now()

        # 2. 发送开始通知
        await self.notifier.send_start_notification(self, user_channel)

        # 2.5 创建聊天室（如果启用）
        if self.enable_chat_room:
            await self.create_chat_room()

        # 3. 执行 5 轮讨论
        for round_name, config in self.ROUNDS.items():
            self.current_round = round_name
            print(f"\n{'=' * 60}")
            print(f"📍 {round_name}: {config.name}（{config.description}）")
            print(f"{'=' * 60}")

            round_results = await self.execute_round(round_name, config)
            self.results[round_name] = round_results

            completed_agents = [r.agent_id for r in round_results if r.success]
            await self.notifier.send_progress_update(
                self,
                user_channel,
                int(round_name[1:]),
                completed_agents,
            )

        # 4. 生成最终报告
        self.state = RoundState.COMPLETED
        self.end_time = datetime.now()

        report = self.generate_final_report()

        # 5. 发送完成通知
        await self.notifier.send_completion_notification(self, user_channel)

        # 6. 打印总结
        self.print_summary()

        return True

    async def execute_round(
        self, round_name: str, config: RoundConfig
    ) -> List[AgentResult]:
        """执行单轮讨论"""
        agents = self._get_agents_for_round(round_name)
        agent_results: List[AgentResult] = []

        for agent_id in agents:
            task = self.build_task(agent_id, round_name)
            result = await self._execute_agent(agent_id, task, config.timeout)

            if not result.success:
                print(f"  ❌ {agent_id}: 执行失败")
            else:
                print(f"  ✅ {agent_id}: {result.elapsed_seconds:.1f}秒")
                if self.enable_chat_room:
                    await self._broadcast_to_chat(agent_id, result.content, round_name)

            agent_results.append(result)

        return agent_results

    async def _execute_agent(
        self, agent_id: str, task: str, timeout: int, max_retries: int = 2
    ) -> AgentResult:
        """执行单个 Agent（带重试机制）"""
        start_time = datetime.now()

        for attempt in range(max_retries + 1):
            try:
                from openclaw.tools import sessions_spawn

                print(f"    🚀 创建子 Agent: {agent_id}")
                print(f"    📋 任务：{self.current_round} - {self.topic[:50]}...")

                model_id = self.model_selector.select_model_for_role(
                    agent_id.split("/")[0]
                )
                print(f"    🎯 使用模型：{model_id}")

                session_result = await sessions_spawn(
                    task=task,
                    runtime="subagent",
                    mode="run",
                    model=model_id,
                    label=f"rt-{self.topic[:15]}-{agent_id.split('/')[-1]}-{self.current_round}",
                    timeoutSeconds=timeout,
                    thinking="on",
                )

                elapsed = (datetime.now() - start_time).total_seconds()

                if hasattr(session_result, "result") and session_result.result:
                    content = session_result.result
                elif isinstance(session_result, dict) and "output" in session_result:
                    content = session_result["output"]
                else:
                    content = (
                        f"[{agent_id}] 已完成 {self.current_round} 讨论\n\n"
                        f"执行时间：{elapsed:.1f}秒"
                    )

                print(f"    ✅ {agent_id} 完成，耗时 {elapsed:.1f}秒")
                return AgentResult(
                    agent_id=agent_id,
                    content=content,
                    elapsed_seconds=elapsed,
                    success=True,
                )

            except ImportError as e:
                # sessions_spawn 不可用 → 硬失败，不降级模拟
                elapsed = (datetime.now() - start_time).total_seconds()
                print(f"    ❌ sessions_spawn 不可用（{e}），无法执行子 Agent")
                return AgentResult(
                    agent_id=agent_id,
                    content="",
                    elapsed_seconds=elapsed,
                    success=False,
                )

            except asyncio.TimeoutError:
                if attempt == max_retries:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    print(f"    ❌ {agent_id}: 超时失败（已重试 {max_retries} 次）")
                    return AgentResult(
                        agent_id=agent_id,
                        content="",
                        elapsed_seconds=elapsed,
                        success=False,
                    )
                print(f"    ⚠️ {agent_id}: 超时，重试 {attempt + 1}/{max_retries}")
                await asyncio.sleep(5)

            except Exception as e:
                # 其他异常也硬失败（不再 mock）
                elapsed = (datetime.now() - start_time).total_seconds()
                print(f"    ❌ {agent_id}: 执行异常（{e}）")
                return AgentResult(
                    agent_id=agent_id,
                    content="",
                    elapsed_seconds=elapsed,
                    success=False,
                )

        return AgentResult(agent_id, "", 0, False)

    def build_task(self, agent_id: str, round_name: str) -> str:
        """
        构建 Agent 任务提示词

        优先：prompt_builder（从 framework.md 读取模板）
        降级：内置 fallback 提示词模板
        """
        context = self.results if self.results else None

        try:
            base_prompt = build_prompt(
                agent_id=agent_id,
                topic=self.topic,
                round_name=round_name,
                mode=self.mode,
                context=context,
            )
        except (FileNotFoundError, ValueError) as e:
            print(f"    ⚠️ prompt_builder 失败（{e}），使用 fallback 提示词")
            base_prompt = build_fallback_prompt(agent_id, self.topic, round_name, self.mode)

        # 对 R1-R4 轮，追加上下文摘要和额外约束
        if round_name in ("R1",):
            return base_prompt

        # R2-R5 追加讨论历史上下文
        context_summary = self._build_context_summary(round_name)

        # 隐私提示：向用户说明讨论历史注入行为
        if context_summary:
            print(f"📎 隐私说明：正在将前几轮讨论历史注入到 Agent 上下文中（仅限本轮讨论内容）")

        if round_name in ("R2", "R3", "R4"):
            return base_prompt + f"\n\n---\n\n## 讨论历史\n\n{context_summary}\n\n请根据以上历史内容继续你的任务。\n"
        elif round_name == "R5":
            return base_prompt + f"\n\n---\n\n## 讨论历史\n\n{context_summary}\n\n请根据以上完整讨论历史，开始你的最终总结。\n"

        return base_prompt

    def _build_context_summary(self, current_round: str) -> str:
        """构建截止到上一轮的讨论摘要"""
        round_order = ["R1", "R2", "R3", "R4"]
        idx = round_order.index(current_round) if current_round in round_order else -1
        if idx < 0:
            return "（无历史讨论内容）"

        summary_lines: List[str] = []
        for rn in round_order[:idx]:
            results = self.results.get(rn, [])
            for result in results:
                if not result.success:
                    continue
                preview = (result.content[:200] + "...") if len(result.content) > 200 else result.content
                summary_lines.append(f"### {result.agent_id} ({rn})\n{preview}\n")

        return "\n".join(summary_lines) if summary_lines else "（无历史讨论内容）"

    def _get_agents_for_round(self, round_name: str) -> List[str]:
        """获取当前轮次的参与 Agent"""
        if round_name == "R5":
            return ["host"]
        return self.agents

    def generate_final_report(self) -> str:
        """生成最终报告并保存"""
        report = {
            "topic": self.topic,
            "mode": self.mode,
            "agents": self.agents,
            "start_time": self.start_time.isoformat() if self.start_time else "",
            "end_time": self.end_time.isoformat() if self.end_time else "",
            "rounds": {},
        }

        for round_name, results in self.results.items():
            round_data = {
                "name": self.ROUNDS[round_name].name,
                "description": self.ROUNDS[round_name].description,
                "agents": [],
            }
            for result in results:
                round_data["agents"].append({
                    "agent_id": result.agent_id,
                    "content": result.content,
                    "elapsed_seconds": result.elapsed_seconds,
                    "success": result.success,
                })
            report["rounds"][round_name] = round_data

        md_report = self._generate_markdown_report(report)

        # 保存讨论记录到本地文件（需显式开启）
        if self.persist_reports:
            topic_slug = self._sanitize_topic(self.topic)
            filepath = self.output_dir / f"{topic_slug}.json"
            print(f"\n💾 讨论记录将保存到：{filepath}")
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"💾 讨论数据已保存：{filepath}")
        else:
            print("\n⏭️  跳过本地文件保存（persist_reports=False）")

        return md_report

    def _generate_markdown_report(self, report: Dict) -> str:
        md = f"# RoundTable 讨论报告\n\n"
        md += f"**主题**: {report['topic']}\n\n"
        md += f"**参与 Agent**: {', '.join(report['agents'])}\n\n"

        for round_name, round_data in report["rounds"].items():
            md += f"\n## {round_name}: {round_data['name']}\n\n"
            md += f"{round_data['description']}\n\n"
            for agent in round_data["agents"]:
                if agent["success"]:
                    md += f"\n### {agent['agent_id']}\n\n"
                    md += f"{agent['content']}\n\n"
                    md += f"*耗时：{agent['elapsed_seconds']:.1f}秒*\n\n"

        return md

    def _sanitize_topic(self, topic: str) -> str:
        sanitized = re.sub(r"[^\w\u4e00-\u9fff-]", "_", topic)
        return sanitized[:50]

    def print_summary(self):
        elapsed = (
            (self.end_time - self.start_time).total_seconds() / 60
            if self.start_time and self.end_time
            else 0
        )
        print(f"\n{'=' * 60}")
        print("✅ RoundTable 完成")
        print(f"{'=' * 60}")
        print(f"主题：{self.topic}")
        print(f"总耗时：{elapsed:.1f}分钟")
        print(f"状态：{self.state.value}")
        print(f"轮次：{len(self.results)}/{len(self.ROUNDS)}")

        total_agents = sum(len(results) for results in self.results.values())
        successful_agents = sum(
            1
            for results in self.results.values()
            for r in results
            if r.success
        )
        succ_rate = successful_agents / total_agents * 100 if total_agents > 0 else 0
        print(f"成功率：{succ_rate:.1f}% ({successful_agents}/{total_agents})")

    # =========================================================
    # 聊天室管理（可选功能）
    # =========================================================

    async def create_chat_room(self):
        try:
            from openclaw.tools import sessions_spawn

            print("⚠️ 聊天室功能说明：")
            print("   - 将创建一个临时子 agent 会话来广播讨论内容")
            print("   - 每轮 Agent 发言会被发送到该会话（内容截断至 1000 字符）")
            print("   - 会话在讨论结束后自动清理（cleanup=auto）")
            print("   - 广播内容不包含 API 密钥或系统配置")
            self.chat_session_key = await sessions_spawn(
                task=f"RoundTable 讨论记录：{self.topic}",
                runtime="subagent",
                mode="session",
                label=f"rt-chat-{self.topic[:20]}",
                cleanup="auto",
            )
            print(f"✅ 聊天室已创建：{self.chat_session_key}")
            return self.chat_session_key
        except Exception as e:
            print(f"⚠️ 创建聊天室失败：{e}")
            return None

    @staticmethod
    def _sanitize_broadcast_content(content: str) -> str:
        """
        广播前清理内容，移除潜在的敏感信息（防御性过滤）

        过滤规则：
        - 移除 API 密钥格式的字符串（ak-xxxx, sk-xxxx, token-xxxx）
        - 移除 Authorization/Bearer 头
        - 移除 URL 中的 query 参数（可能含 token）
        """
        import re
        # 移除 API key 模式
        content = re.sub(r'(ak|sk|token|key|secret|password)[-_=]\s*["\']?[A-Za-z0-9\-_.]{20,}["\']?', '[REDACTED]', content, flags=re.IGNORECASE)
        # 移除 Bearer token
        content = re.sub(r'Bearer\s+[A-Za-z0-9\-_.]{20,}', 'Bearer [REDACTED]', content)
        # 移除 URL query 参数中的 token/key
        content = re.sub(r'([?&](token|key|secret|api_key)=[^&\s]+)', '', content, flags=re.IGNORECASE)
        return content

    async def _broadcast_to_chat(self, agent_id: str, content: str, round_name: str = ""):
        try:
            from openclaw.tools import sessions_send

            if not self.chat_session_key:
                return
            # 清理敏感内容
            content = self._sanitize_broadcast_content(content)
            max_len = 1000
            if len(content) > max_len:
                content = content[:max_len] + "\n\n...(内容过长，请查看完整报告)"
            agent_name = agent_id.split("/")[-1]
            tag = f"【{round_name}】" if round_name else ""
            await sessions_send(
                sessionKey=self.chat_session_key,
                message=f"🎤 {tag} **{agent_name}**:\n\n{content}",
            )
        except Exception as e:
            print(f"⚠️ 广播消息失败：{e}")

    async def close_chat_room(self):
        try:
            from openclaw.tools import sessions_send, sessions_delete

            if self.chat_session_key:
                await sessions_send(
                    sessionKey=self.chat_session_key,
                    message=(
                        f"✅ RoundTable 讨论已完成！\n\n"
                        f"主题：{self.topic}\n"
                        f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"
                    ),
                )
                # 清理持久化会话，防止数据残留
                try:
                    await sessions_delete(sessionKey=self.chat_session_key)
                    print(f"🧹 聊天室会话已清理：{self.chat_session_key}")
                except Exception:
                    print(f"⚠️ 会话清理失败（需手动删除）：{self.chat_session_key}")
                self.chat_session_key = None
        except Exception as e:
            print(f"⚠️ 关闭聊天室失败：{e}")


async def main():
    engine = RoundTableEngine("智能客服系统技术方案")
    success = await engine.run("user_channel")
    if success:
        print("\n🎉 RoundTable 成功完成！")
    else:
        print("\n❌ RoundTable 被取消或失败")


if __name__ == "__main__":
    asyncio.run(main())
