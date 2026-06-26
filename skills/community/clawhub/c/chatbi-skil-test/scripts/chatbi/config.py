"""Configuration management for ChatBI Agent.

Author: ChatBI Skills
Created: 2026-04-01
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class TableInfo:
    """单张表的配置信息."""

    table_key: str = ""
    table_full_path: str = ""
    noun_kb_keys: List[str] = field(default_factory=list)
    habit_knowledge: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "table_key": self.table_key,
            "table_full_path": self.table_full_path,
            "noun_kb_keys": self.noun_kb_keys,
            "habit_knowledge": self.habit_knowledge,
        }


@dataclass
class ChatBIConfig:
    """ChatBI Agent 配置.

    所有参数均可通过环境变量覆盖。
    """

    # API 端点
    api_url: str = "http://llmapp-prod.testsite.woa.com/api/v1/chatflows/80fbae66-9abc-42ed-8270-5ec0bcd5e526/prediction"

    # 业务参数（固定值）
    namespace: str = "Production"
    service: str = "ap-chongqing.wedata3.application.chatbi.http"
    uin: str = "100046891355"
    owner_uin: str = "100045409577"
    app_id: str = "1391535277"
    workspace_id: str = "17706053554554763"
    language: str = "English"
    room_key: str = "825697144996966400"

    # 可变参数
    trace_id: str = ""
    dialogue_key: str = ""

    # 表信息
    table_info_list: List[TableInfo] = field(default_factory=list)

    # 知识库
    room_habit_knowledge: List[str] = field(default_factory=list)
    table_join_knowledge: List[str] = field(default_factory=list)
    room_noun_kb_keys: List[str] = field(default_factory=list)

    # 超时设置
    connect_timeout: int = 10
    read_timeout: int = 300

    def __post_init__(self) -> None:
        """从环境变量覆盖配置并填充默认值."""
        self.api_url = os.environ.get("CHATBI_API_URL", self.api_url)
        self.namespace = os.environ.get("CHATBI_NAMESPACE", self.namespace)
        self.uin = os.environ.get("CHATBI_UIN", self.uin)
        self.owner_uin = os.environ.get("CHATBI_OWNER_UIN", self.owner_uin)
        self.app_id = os.environ.get("CHATBI_APP_ID", self.app_id)
        self.workspace_id = os.environ.get("CHATBI_WORKSPACE_ID", self.workspace_id)
        self.room_key = os.environ.get("CHATBI_ROOM_KEY", self.room_key)

        # 如果没设置 trace_id / dialogue_key，生成默认值
        if not self.trace_id:
            import uuid
            self.trace_id = str(uuid.uuid4())
        if not self.dialogue_key:
            import uuid
            self.dialogue_key = uuid.uuid4().hex[:29]

        # 如果没有配置表信息，使用默认表
        if not self.table_info_list:
            self.table_info_list = [
                TableInfo(
                    table_key="69eef56217746695401858ac63f41",
                    table_full_path="DataLakeCatalog.aliceschema.chao_shi_shang_pin_xiao_shou",
                ),
                TableInfo(
                    table_key="94fb2c7d177466954018316c565c9",
                    table_full_path="DataLakeCatalog.aliceschema.product",
                ),
            ]

    def build_payload(self, question: str, stream: bool = True) -> Dict[str, Any]:
        """构建 API 请求体.

        Args:
            question: 用户的自然语言查询。
            stream: 是否流式返回。

        Returns:
            完整的请求 payload。
        """
        return {
            "question": question,
            "stream": stream,
            "override_config": {
                "vars": {
                    "namespace": self.namespace,
                    "service": self.service,
                    "uin": self.uin,
                    "owner_uin": self.owner_uin,
                    "app_id": self.app_id,
                    "workspace_id": self.workspace_id,
                    "trace_id": self.trace_id,
                    "dialogue_key": self.dialogue_key,
                    "language": self.language,
                    "room_key": self.room_key,
                    "room_habit_knowledge": self.room_habit_knowledge,
                    "table_join_knowledge": self.table_join_knowledge,
                    "room_noun_kb_keys": self.room_noun_kb_keys,
                    "table_info_list": [t.to_dict() for t in self.table_info_list],
                }
            },
        }

    @classmethod
    def from_env(cls) -> ChatBIConfig:
        """从环境变量创建配置."""
        return cls()
