#!/usr/bin/env python3
"""
RoundTable 用户确认和进度通知模块

功能：
1. 发送确认消息（说明耗时和风险）
2. 进度通知（每轮完成）
3. 完成报告通知

⚠️ 数据处理说明：
- 确认消息包含：讨论主题名称、参与 Agent 角色列表、预计耗时
- 进度通知包含：当前轮次、已完成 Agent 列表、耗时统计
- 完成通知包含：讨论主题、总耗时、输出路径
- 所有通知均通过用户指定的渠道发送，不存储渠道 ID
- 不读取、不传输 API 密钥、系统配置等敏感信息
"""

import asyncio
from datetime import datetime
from typing import Optional, List


class RoundTableNotifier:
    """RoundTable 通知器"""

    def __init__(self, topic: str, mode: str = "pre-ac"):
        self.topic = topic
        self.mode = mode
        self.start_time: Optional[datetime] = None

    def _send_message(self, engine, user_channel: str, message: str):
        """通用消息发送 — 尝试多种渠道"""
        sent = False

        # 1. 尝试飞书 message 工具（主要渠道）
        try:
            from openclaw.tools import message as feishu_msg

            asyncio.ensure_future(
                feishu_msg(action="send", target=user_channel, message=message)
            )
            sent = True
        except ImportError:
            pass
        except Exception as e:
            print(f"    ⚠️ 飞书消息发送失败：{e}")

        # 2. 尝试 engine.chat_session_key 用 sessions_send（聊天室模式）
        if not sent and hasattr(engine, "chat_session_key") and engine.chat_session_key:
            try:
                from openclaw.tools import sessions_send

                asyncio.ensure_future(
                    sessions_send(
                        sessionKey=engine.chat_session_key,
                        message=message,
                    )
                )
                sent = True
            except ImportError:
                pass
            except Exception as e:
                print(f"    ⚠️ 聊天室消息发送失败：{e}")

        # 3. 最后 fallback：打印到 stdout（至少开发者能看到）
        if not sent:
            print(f"📤 通知（{user_channel}）：\n{message}")

    async def send_confirmation_request(self, engine, user_channel: str) -> bool:
        """
        发送 RoundTable 确认请求
        注：真正的"等待回复确认"由调用方实现，这里只发送消息
        """
        message = (
            f"🔄 **RoundTable 多 Agent 深度讨论**\n\n"
            f"**讨论主题**：{self.topic}\n\n"
            f"📋 **讨论说明**：\n"
            f"- 参与 Agent：{', '.join(engine.agents[:5])}\n"
            f"- 讨论轮次：5 轮深度讨论（R1-R5）\n"
            f"- 预计耗时：**10-30 分钟**\n"
            f"- 输出内容：完整技术方案 + 多方观点 + 行动建议\n\n"
            f"⚠️ **请注意**：\n"
            f"- RoundTable 适合需要深度分析的场景\n"
            f"- 如果您需要快速回答，请使用普通对话\n"
            f"- 讨论过程中您可以随时查看进度\n\n"
            f"**请确认您的需求**：\n"
            f'回复 "**确认**" 开始 RoundTable 深度讨论\n'
            f'回复 "**快速**" 获取简要方案（<1 分钟）'
        )

        self._send_message(engine, user_channel, message)
        print(f"📤 已发送确认请求到 {user_channel}")

        # 注意：此方法仅发送确认消息，不等待用户回复
        # 真正的"等待确认"逻辑由调用方（engine 或 skill runner）实现
        # 当前为演示模式，调用方可直接继续执行
        return True

    async def send_start_notification(self, engine, user_channel: str):
        """发送开始通知"""
        self.start_time = datetime.now()
        message = (
            f"🚀 **RoundTable 已启动**\n\n"
            f"**主题**：{self.topic}\n"
            f"**状态**：R1 轮讨论中（1/5）\n"
            f"**参与**：{', '.join(engine.agents)}\n"
            f"**预计**：10-30 分钟\n\n"
            f"您可以在讨论过程中随时查看进度，\n"
            f"完成时会收到最终报告通知。"
        )
        self._send_message(engine, user_channel, message)

    async def send_progress_update(
        self,
        engine,
        user_channel: str,
        round_num: int,
        completed_agents: List[str],
    ):
        """发送进度更新"""
        progress = round_num / 5 * 100
        elapsed = (
            (datetime.now() - self.start_time).total_seconds() / 60
            if self.start_time
            else 0
        )
        remaining = max(0, 30 - elapsed)

        bar = "█" * int(progress / 10) + "░" * (10 - int(progress / 10))
        message = (
            f"📊 **RoundTable 进度更新**\n\n"
            f"**当前**：R{round_num} 轮完成（{round_num}/5）\n"
            f"**进度**：{bar} {progress:.0f}%\n"
            f"**已完成**：{', '.join(completed_agents)}\n"
            f"**已耗时**：{elapsed:.1f} 分钟\n"
            f"**预计剩余**：{remaining:.0f}-{remaining + 10:.0f} 分钟"
        )
        self._send_message(engine, user_channel, message)

    async def send_completion_notification(self, engine, user_channel: str):
        """发送完成通知"""
        elapsed = (
            (datetime.now() - self.start_time).total_seconds() / 60
            if self.start_time
            else 0
        )
        message = (
            f"✅ **RoundTable 讨论完成**\n\n"
            f"**主题**：{self.topic}\n"
            f"**总耗时**：{elapsed:.1f} 分钟\n"
            f"**讨论轮次**：R1-R5（完整 5 轮）\n\n"
            f"📄 报告已保存到 {engine.output_dir}"
        )
        self._send_message(engine, user_channel, message)

    async def send_timeout_warning(
        self,
        engine,
        user_channel: str,
        round_num: int,
        timed_out_agents: List[str],
    ):
        """发送超时警告"""
        message = (
            f"⚠️ **RoundTable 超时警告**\n\n"
            f"**当前轮次**：R{round_num}\n"
            f"**超时 Agent**：{', '.join(timed_out_agents)}\n\n"
            f"系统已自动重试或启用降级方案。\n"
            f"讨论将继续进行，最终报告可能缺少部分观点。"
        )
        self._send_message(engine, user_channel, message)
