#!/usr/bin/env python3
"""Feynman Lobster local read-only API bridge.

Serves real data from OpenClaw workspace files so the web panel can render
contracts and memory even when Gateway plugin endpoints are unavailable.
"""

from __future__ import annotations

import argparse
import json
import os
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_iso(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        normalized = ts.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


class Store:
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace
        self.contracts_file = workspace / "contracts.json"
        self.profile_file = workspace / "USER_PROFILE.md"
        self.memory_dir = workspace / "contract-memory"
        self.conv_dir = workspace / "conversations"

    @staticmethod
    def _is_demo_contract(contract: dict) -> bool:
        if not isinstance(contract, dict):
            return False
        cid = str(contract.get("id") or "")
        return bool(contract.get("__demo")) or cid.startswith("demo_")

    @staticmethod
    def _demo_contracts() -> list[dict]:
        now = utc_now().isoformat()
        return [
            {
                "id": "demo_contract_poetry",
                "__demo": True,
                "project": "诗歌生成模型（演示）",
                "goal": "训练一个可以写现代诗的小模型",
                "motivation": "演示面板与契约流程",
                "reward": "完成后发布一个可分享的诗歌 demo",
                "deadline": "2026-04-01T00:00:00+00:00",
                "created_at": "2026-03-19T00:00:00+00:00",
                "status": "active",
                "resources": [
                    {
                        "id": "res_demo_pytorch",
                        "type": "url",
                        "title": "PyTorch 官方文档",
                        "url": "https://docs.pytorch.org/docs/stable/index.html",
                        "path": None,
                    },
                    {
                        "id": "res_demo_feishu",
                        "type": "doc",
                        "title": "诗歌模型训练记录（飞书）",
                        "url": "https://feishu.cn/docx/DEMO-POEM-TRAIN-LOG",
                        "path": None,
                    },
                ],
                "clauses": [
                    {"id": "cl_demo_1", "concept": "训练/验证损失关系", "status": "mastered", "attempts": 1, "mastered_at": "2026-03-19T08:00:00+00:00", "added_reason": None},
                    {"id": "cl_demo_2", "concept": "采样策略（temperature/top-p）", "status": "in_progress", "attempts": 2, "mastered_at": None, "added_reason": None},
                    {"id": "cl_demo_3", "concept": "过拟合与泛化", "status": "pending", "attempts": 0, "mastered_at": None, "added_reason": None},
                    {"id": "cl_demo_4", "concept": "数据清洗与风格一致性", "status": "pending", "attempts": 0, "mastered_at": None, "added_reason": None},
                    {"id": "cl_demo_5", "concept": "分词器对诗歌意象的影响", "status": "pending", "attempts": 0, "mastered_at": None, "added_reason": None},
                    {"id": "cl_demo_6", "concept": "LoRA 微调流程", "status": "pending", "attempts": 0, "mastered_at": None, "added_reason": None},
                    {"id": "cl_demo_7", "concept": "评估闭环（重复率/可读性/意象一致性）", "status": "pending", "attempts": 0, "mastered_at": None, "added_reason": None},
                ],
                "supervisors": [],
                "last_active_at": now,
            },
            {
                "id": "demo_contract_cat_teaser_bot",
                "__demo": True,
                "project": "机械臂逗猫棒（演示）",
                "goal": "做一个可远程控制的机械臂逗猫棒",
                "motivation": "把控制算法和硬件联调做成可演示项目",
                "reward": "完成后给猫买一套新玩具并录制演示视频",
                "deadline": "2026-04-08T00:00:00+00:00",
                "created_at": "2026-03-19T00:00:00+00:00",
                "status": "active",
                "resources": [
                    {
                        "id": "res_demo_cat_log",
                        "type": "doc",
                        "title": "机械臂联调日志（飞书）",
                        "url": "https://feishu.cn/docx/DEMO-CAT-ARM-LOG",
                        "path": None,
                    },
                    {
                        "id": "res_demo_ctrl",
                        "type": "url",
                        "title": "控制系统基础参考",
                        "url": "https://docs.pytorch.org/docs/stable/index.html",
                        "path": None,
                    },
                ],
                "clauses": [
                    {"id": "cl_cat_1", "concept": "PWM 与舵机控制基础", "status": "mastered", "attempts": 1, "mastered_at": "2026-03-19T08:10:00+00:00", "added_reason": None},
                    {"id": "cl_cat_2", "concept": "机械臂运动学约束", "status": "in_progress", "attempts": 2, "mastered_at": None, "added_reason": None},
                    {"id": "cl_cat_3", "concept": "轨迹平滑（jerk 限制）", "status": "pending", "attempts": 0, "mastered_at": None, "added_reason": None},
                    {"id": "cl_cat_4", "concept": "摄像头目标跟踪", "status": "pending", "attempts": 0, "mastered_at": None, "added_reason": "读项目时发现你在用"},
                    {"id": "cl_cat_5", "concept": "安全边界与急停策略", "status": "pending", "attempts": 0, "mastered_at": None, "added_reason": None},
                    {"id": "cl_cat_6", "concept": "状态机设计（待机/追踪/逗猫）", "status": "pending", "attempts": 0, "mastered_at": None, "added_reason": None},
                    {"id": "cl_cat_7", "concept": "联调评估指标（响应延迟/命中率）", "status": "pending", "attempts": 0, "mastered_at": None, "added_reason": None},
                ],
                "supervisors": [],
                "last_active_at": now,
            },
        ]

    def _load_raw_contracts(self) -> list[dict]:
        if not self.contracts_file.exists():
            return []
        try:
            data = json.loads(self.contracts_file.read_text(encoding="utf-8"))
        except Exception:
            return []
        if isinstance(data, list):
            contracts = [x for x in data if isinstance(x, dict)]
            self._cleanup_demo_contracts_in_file_if_needed(data, contracts, list_mode=True)
            return contracts
        if isinstance(data, dict) and isinstance(data.get("contracts"), list):
            contracts = [x for x in data["contracts"] if isinstance(x, dict)]
            self._cleanup_demo_contracts_in_file_if_needed(data, contracts, list_mode=False)
            return contracts
        return []

    def _cleanup_demo_contracts_in_file_if_needed(self, raw_data: object, contracts: list[dict], list_mode: bool) -> None:
        has_demo = any(self._is_demo_contract(c) for c in contracts)
        has_real = any(not self._is_demo_contract(c) for c in contracts)
        if not (has_demo and has_real):
            return
        cleaned = [c for c in contracts if not self._is_demo_contract(c)]
        try:
            if list_mode and isinstance(raw_data, list):
                self.contracts_file.write_text(json.dumps(cleaned, ensure_ascii=False, indent=2), encoding="utf-8")
            elif isinstance(raw_data, dict):
                payload = dict(raw_data)
                payload["contracts"] = cleaned
                self.contracts_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            # Keep serving data even if cleanup write fails.
            pass

    def contracts(self) -> list[dict]:
        raw = self._load_raw_contracts()
        return raw if raw else self._demo_contracts()

    def contract_by_id(self, contract_id: str) -> dict | None:
        for c in self.contracts():
            if str(c.get("id")) == contract_id:
                return c
        return None

    def _normalize_conv(self, row: dict, contract_id: str, index: int) -> dict | None:
        if not isinstance(row, dict):
            return None
        cid = str(row.get("contract_id") or contract_id)
        if cid != contract_id:
            return None
        messages = row.get("messages")
        if not isinstance(messages, list):
            return None
        safe_messages: list[dict] = []
        for m in messages:
            if not isinstance(m, dict):
                continue
            role = str(m.get("role") or "").strip() or "user"
            content = str(m.get("content") or "").strip()
            if content:
                safe_messages.append({"role": role, "content": content})
        if not safe_messages:
            return None
        return {
            "id": str(row.get("id") or f"conv_{index}_{uuid.uuid4().hex[:8]}"),
            "contract_id": contract_id,
            "clause_id": str(row.get("clause_id") or ""),
            "concept": str(row.get("concept") or ""),
            "timestamp": str(row.get("timestamp") or ""),
            "result": str(row.get("result") or "partial"),
            "messages": safe_messages,
        }

    def _load_conversations_json(self, fp: Path, contract_id: str) -> list[dict]:
        try:
            payload = json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            return []
        if isinstance(payload, dict) and isinstance(payload.get("conversations"), list):
            raw = payload["conversations"]
        elif isinstance(payload, list):
            raw = payload
        else:
            raw = []
        convs: list[dict] = []
        for i, row in enumerate(raw):
            conv = self._normalize_conv(row, contract_id, i)
            if conv:
                convs.append(conv)
        return convs

    def _load_conversations_jsonl(self, fp: Path, contract_id: str) -> list[dict]:
        convs: list[dict] = []
        try:
            lines = fp.read_text(encoding="utf-8").splitlines()
        except Exception:
            return []
        grouped: dict[str, dict] = {}
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except Exception:
                continue
            # Supported formats:
            # 1) one row = one conversation (contains messages[])
            # 2) one row = one message with conversation_id/session_id + role/content
            normalized = self._normalize_conv(row, contract_id, i)
            if normalized:
                convs.append(normalized)
                continue
            if str(row.get("contract_id") or "") != contract_id:
                continue
            conv_id = str(row.get("conversation_id") or row.get("session_id") or row.get("id") or "")
            if not conv_id:
                continue
            role = str(row.get("role") or "").strip()
            content = str(row.get("content") or "").strip()
            if not role or not content:
                continue
            bucket = grouped.setdefault(
                conv_id,
                {
                    "id": conv_id,
                    "contract_id": contract_id,
                    "clause_id": str(row.get("clause_id") or ""),
                    "concept": str(row.get("concept") or ""),
                    "timestamp": str(row.get("timestamp") or ""),
                    "result": str(row.get("result") or "partial"),
                    "messages": [],
                },
            )
            if row.get("timestamp"):
                bucket["timestamp"] = str(row["timestamp"])
            if row.get("result"):
                bucket["result"] = str(row["result"])
            bucket["messages"].append({"role": role, "content": content})
        convs.extend(grouped.values())
        return convs

    def conversations(self, contract_id: str, limit: int, clause_id: str | None = None) -> list[dict]:
        if contract_id == "demo_contract_poetry":
            convs = [
                {
                    "id": "conv_demo_6",
                    "contract_id": contract_id,
                    "clause_id": "cl_demo_7",
                    "concept": "评估闭环（重复率/可读性/意象一致性）",
                    "timestamp": "2026-03-19T08:28:00+00:00",
                    "result": "partial",
                    "messages": [
                        {"role": "lobster", "content": "你现在怎么判断“诗写得更好”不是错觉？"},
                        {"role": "user", "content": "我会做固定主题集，分别看重复率、可读性和意象一致性。"},
                        {"role": "lobster", "content": "很好，再补一个：每组至少抽样多少首，才能避免偶然性？"},
                    ],
                },
                {
                    "id": "conv_demo_5",
                    "contract_id": contract_id,
                    "clause_id": "cl_demo_6",
                    "concept": "LoRA 微调流程",
                    "timestamp": "2026-03-19T08:22:00+00:00",
                    "result": "not_yet",
                    "messages": [
                        {"role": "lobster", "content": "你把 rank 从 8 提到 64，为什么可能让小语料任务更容易过拟合？"},
                        {"role": "user", "content": "因为容量更大？但我不确定和数据规模怎么对应。"},
                        {"role": "lobster", "content": "方向对了。下次你带上“参数量变化 + 验证集趋势”再来，我们一起定更稳的 rank。"},
                    ],
                },
                {
                    "id": "conv_demo_4",
                    "contract_id": contract_id,
                    "clause_id": "cl_demo_5",
                    "concept": "分词器对诗歌意象的影响",
                    "timestamp": "2026-03-19T08:16:00+00:00",
                    "result": "mastered",
                    "messages": [
                        {"role": "lobster", "content": "为什么同样的主题词，不同 tokenizer 会影响诗句意象连贯性？"},
                        {"role": "user", "content": "因为切分粒度改变了语义单元，模型学到的“词-意象”映射会被打散。"},
                        {"role": "lobster", "content": "这次我懂了！你已经能把 tokenizer 选择和生成风格联系起来了。"},
                    ],
                },
                {
                    "id": "conv_demo_3",
                    "contract_id": contract_id,
                    "clause_id": "cl_demo_3",
                    "concept": "过拟合与泛化",
                    "timestamp": "2026-03-19T08:13:00+00:00",
                    "result": "partial",
                    "messages": [
                        {"role": "lobster", "content": "日志显示 train loss 继续降，但你说输出变模板化。你怎么判断这是过拟合？"},
                        {"role": "user", "content": "因为在固定主题上出现高频重复句，验证样本新颖度下降。"},
                        {"role": "lobster", "content": "很好。下次补一个对照：早停前后同主题 20 首的重复率曲线。"},
                    ],
                },
                {
                    "id": "conv_demo_1",
                    "contract_id": contract_id,
                    "clause_id": "cl_demo_2",
                    "concept": "采样策略（temperature/top-p）",
                    "timestamp": "2026-03-19T08:10:00+00:00",
                    "result": "partial",
                    "messages": [
                        {"role": "lobster", "content": "你日志里写了“loss 下降但诗句重复”，你先判断这是训练问题还是采样问题？"},
                        {"role": "user", "content": "我猜先从采样参数排查，固定 checkpoint 做 temperature/top-p 对照。"},
                    ],
                },
                {
                    "id": "conv_demo_2",
                    "contract_id": contract_id,
                    "clause_id": "cl_demo_1",
                    "concept": "训练/验证损失关系",
                    "timestamp": "2026-03-19T08:00:00+00:00",
                    "result": "mastered",
                    "messages": [
                        {"role": "lobster", "content": "为什么训练 loss 下降不代表生成质量一定变好？"},
                        {"role": "user", "content": "因为 token-level 目标不等于风格和可读性目标，需要额外评估维度。"},
                    ],
                },
            ]
            if clause_id:
                convs = [c for c in convs if str(c.get("clause_id") or "") == clause_id]
            return convs[:limit]
        if contract_id == "demo_contract_cat_teaser_bot":
            convs = [
                {
                    "id": "conv_cat_1",
                    "contract_id": contract_id,
                    "clause_id": "cl_cat_2",
                    "concept": "机械臂运动学约束",
                    "timestamp": "2026-03-19T08:24:00+00:00",
                    "result": "partial",
                    "messages": [
                        {"role": "lobster", "content": "你把角度上限放宽后，为什么末端抖动反而更严重？"},
                        {"role": "user", "content": "我猜是接近奇异位姿，微小误差被放大。"},
                    ],
                },
                {
                    "id": "conv_cat_2",
                    "contract_id": contract_id,
                    "clause_id": "cl_cat_1",
                    "concept": "PWM 与舵机控制基础",
                    "timestamp": "2026-03-19T08:12:00+00:00",
                    "result": "mastered",
                    "messages": [
                        {"role": "lobster", "content": "为什么同样频率下，脉宽变化能控制舵机角度？"},
                        {"role": "user", "content": "因为舵机内部解码脉宽映射目标角度，控制器会闭环逼近该角度。"},
                    ],
                },
            ]
            if clause_id:
                convs = [c for c in convs if str(c.get("clause_id") or "") == clause_id]
            return convs[:limit]

        candidates = [
            self.conv_dir / f"{contract_id}.json",
            self.conv_dir / f"{contract_id}.jsonl",
            self.workspace / f"conversations_{contract_id}.json",
            self.workspace / f"conversations_{contract_id}.jsonl",
        ]
        convs: list[dict] = []
        for fp in candidates:
            if not fp.exists():
                continue
            if fp.suffix == ".json":
                convs.extend(self._load_conversations_json(fp, contract_id))
            else:
                convs.extend(self._load_conversations_jsonl(fp, contract_id))
        if clause_id:
            convs = [c for c in convs if str(c.get("clause_id") or "") == clause_id]
        convs.sort(key=lambda x: str(x.get("timestamp", "")), reverse=True)
        return convs[:limit]

    def contract_memory(self, contract_id: str) -> str:
        if contract_id == "demo_contract_poetry":
            return (
                "# 契约 demo_contract_poetry — 诗歌生成模型（演示）\n\n"
                "## 当前目标\n"
                "- 项目：训练一个可以写现代诗的小模型\n"
                "- 进展：已完成损失分析与 tokenizer 讨论，正在建立评估闭环\n"
                "- 截止：2026-04-01\n\n"
                "## 最近实验记录\n"
                "- 2026-03-19 08:05: 固定 checkpoint，对 temperature/top-p 进行 3x3 网格采样\n"
                "- 2026-03-19 08:12: 发现 temperature 过高时，意象新颖但语义飘逸\n"
                "- 2026-03-19 08:18: 发现 top-p 过低时，重复率下降但语言趋于模板化\n\n"
                "## 概念理解记录\n"
                "- 已掌握：训练/验证损失关系、分词器对意象的影响\n"
                "- 进行中：采样策略、过拟合诊断\n"
                "- 待掌握：LoRA 参数选择、评估闭环设计\n\n"
                "## 知识盲区\n"
                "- 还需建立“重复率/可读性/意象一致性”的评估闭环\n"
                "- 尚未形成“出现失败时先排查采样还是训练”的固定诊断流程\n\n"
                "## 下一步行动\n"
                "- 固定 4 个主题，各抽样 20 首，记录三项评分并计算重复率\n"
                "- 仅改变一个变量（temperature 或 top-p），避免多因素混淆\n"
                "- 在日志中补充失败样本与成功样本对照，便于下一轮费曼追问\n"
            )
        if contract_id == "demo_contract_cat_teaser_bot":
            return (
                "# 契约 demo_contract_cat_teaser_bot — 机械臂逗猫棒（演示）\n\n"
                "## 当前目标\n"
                "- 项目：做一个可远程控制的机械臂逗猫棒\n"
                "- 进展：已完成 PWM 基础，正在处理运动学与轨迹平滑\n\n"
                "## 最近联调记录\n"
                "- 舵机角度接近边界时，末端出现抖动\n"
                "- 摄像头跟踪帧率下降时，追踪延迟明显\n\n"
                "## 知识盲区\n"
                "- 还未建立完整的急停与安全边界策略\n"
                "- 缺少“命中率 + 响应延迟”的量化评估表\n"
            )
        fp = self.memory_dir / f"{contract_id}.md"
        if not fp.exists():
            return ""
        try:
            return fp.read_text(encoding="utf-8").strip()
        except Exception:
            return ""

    def user_profile(self) -> str:
        if not self.profile_file.exists():
            return (
                "## 用户画像（演示）\n"
                "- 偏好项目驱动学习\n"
                "- 学习目标：用可复现流程完成“主题输入 -> 诗歌输出”demo\n"
                "- 学习风格：先动手实验，再补理论；接受反问式引导\n"
                "- 反馈偏好：希望得到“最小可执行下一步”，而不是笼统建议\n"
                "- 常见卡点：训练失败后容易直接改很多参数，缺少对照实验\n"
                "- 激励方式：有阶段性里程碑和可视化进度时投入更稳定\n"
                "- 语言偏好：中文解释，术语可保留英文（如 top-p, checkpoint）\n"
            )
        try:
            return self.profile_file.read_text(encoding="utf-8").strip()
        except Exception:
            return ""

    def hero(self, contract_id: str) -> dict:
        c = self.contract_by_id(contract_id)
        if not c:
            return {"text": "还没有契约，去和龙虾签一份吧。", "type": "new"}

        clauses = c.get("clauses") or []
        mastered = len([x for x in clauses if isinstance(x, dict) and x.get("status") == "mastered"])
        total = len(clauses)
        reward = c.get("reward")

        created = parse_iso(c.get("created_at"))
        days = 1
        if created:
            days = max(1, (utc_now() - created).days + 1)

        deadline = parse_iso(c.get("deadline"))
        left = None
        if deadline:
            left = (deadline - utc_now()).days

        if c.get("status") == "completed":
            return {
                "text": f"契约完成。{days} 天前你说要 {c.get('goal') or c.get('project') or '完成项目'}，现在你做到了。",
                "type": "completed",
            }
        if left is not None and left < 0:
            return {"text": f"已逾期 {abs(left)} 天。还差 {max(total-mastered, 0)} 个概念。", "type": "inactive"}
        if total - mastered <= 2 and total > 0:
            return {"text": f"还差最后 {max(total-mastered, 0)} 个概念。", "type": "near_complete"}
        if reward:
            return {"text": f"Day {days}。你已经教会龙虾 {mastered} 个概念。距离奖励还差 {max(total-mastered, 0)} 个。", "type": "reward_ref"}
        return {"text": f"Day {days}。你已经教会龙虾 {mastered} 个概念。", "type": "progress"}

    def lobster(self) -> dict:
        contracts = self._load_raw_contracts()
        active = [c for c in contracts if c.get("status") == "active"]
        completed = [c for c in contracts if c.get("status") == "completed"]
        if completed:
            recent = sorted(completed, key=lambda x: str(x.get("last_active_at", "")), reverse=True)[0]
            last = parse_iso(recent.get("last_active_at"))
            if last and (utc_now() - last).days <= 1:
                return {"mood": "celebrating", "active_contract_id": recent.get("id")}
        if not active:
            return {"mood": "curious", "active_contract_id": None}
        current = sorted(active, key=lambda x: str(x.get("last_active_at", "")), reverse=True)[0]
        last = parse_iso(current.get("last_active_at"))
        if last and (utc_now() - last).days > 2:
            return {"mood": "anxious", "active_contract_id": current.get("id")}
        return {"mood": "curious", "active_contract_id": current.get("id")}


class Handler(BaseHTTPRequestHandler):
    store: Store

    def _send_json(self, payload: dict, code: int = 200) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type,Authorization")
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type,Authorization")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        if path == "":
            path = "/"

        if path == "/api/feynman/contracts":
            contracts = self.store.contracts()
            self._send_json({"contracts": contracts, "total": len(contracts)})
            return

        if path == "/api/feynman/lobster":
            self._send_json({"lobster": self.store.lobster()})
            return

        if path == "/api/feynman/profile":
            self._send_json({"profile": {"markdown": self.store.user_profile()}})
            return

        if path == "/api/feynman/hero":
            q = parse_qs(parsed.query)
            contract_id = (q.get("contract_id") or [""])[0]
            self._send_json({"hero": self.store.hero(contract_id)})
            return

        # /api/feynman/contracts/:id
        prefix = "/api/feynman/contracts/"
        if path.startswith(prefix):
            suffix = path[len(prefix):]
            parts = [p for p in suffix.split("/") if p]
            if len(parts) == 1:
                contract = self.store.contract_by_id(parts[0])
                if not contract:
                    self._send_json({"error": {"code": "NOT_FOUND", "message": "Contract not found"}}, 404)
                    return
                self._send_json(contract)
                return
            if len(parts) == 2 and parts[1] == "conversations":
                q = parse_qs(parsed.query)
                try:
                    limit = int((q.get("limit") or ["5"])[0])
                except ValueError:
                    limit = 5
                clause_id = (q.get("clause_id") or [""])[0].strip() or None
                limit = max(1, min(limit, 50))
                convs = self.store.conversations(parts[0], limit, clause_id=clause_id)
                self._send_json({"conversations": convs, "total": len(convs)})
                return
            if len(parts) == 2 and parts[1] == "memory":
                memory_text = self.store.contract_memory(parts[0])
                self._send_json({"memory": {"markdown": memory_text}})
                return

        self._send_json({"error": {"code": "NOT_FOUND", "message": "Route not found"}}, 404)


def main() -> None:
    parser = argparse.ArgumentParser(description="Feynman Lobster local API bridge")
    parser.add_argument("--workspace", default=os.environ.get("OPENCLAW_WORKSPACE", str(Path.home() / ".openclaw")))
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=18790)
    args = parser.parse_args()

    workspace = Path(os.path.expanduser(args.workspace))
    workspace.mkdir(parents=True, exist_ok=True)
    store = Store(workspace)

    class BoundHandler(Handler):
        pass

    BoundHandler.store = store

    server = ThreadingHTTPServer((args.host, args.port), BoundHandler)
    print(f"[feynman-api] workspace={workspace}")
    print(f"[feynman-api] listening on http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
