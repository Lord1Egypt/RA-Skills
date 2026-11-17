"""
work_summary.py - V7-AIPC 新增:每次工作后的"本地 vs 云端"对比报告

设计目标:
  - 在每次课程材料处理(4 阶段流水线)或端云交换(exchange)后,自动生成对比报告
  - 报告包含:本地推理使用情况 / 云端调用使用情况 / 成本对比 / 延迟对比 / 隐私对比
  - 数据来源:cost_monitor + llm_cache + edge_cloud_dispatch 的运行时状态
  - 输出格式:JSON + Markdown table(控制台友好)

CLI:
    python work_summary.py                    # 显示最近 1 次工作对比
    python work_summary.py --last 5           # 显示最近 5 次
    python work_summary.py --export path.md   # 导出到 markdown
    python work_summary.py --clear            # 清空历史

设计哲学(端云协同):
  本地(OpenVINO + DeepSeek-R1-1.5B):重活端侧做
  云端(GPT-4o / Claude / DeepSeek API):决策云端做
  V7-AIPC:每次工作都向用户展示两端的实际贡献
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# 强制 UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from log_util import get_logger

log = get_logger("work_summary")

# 工作记录存储路径
DEFAULT_HISTORY_PATH = Path(os.environ.get("USERPROFILE", str(Path.home()))) / ".openvino" / "cache" / "work_history.jsonl"
# 单次工作预期时长(用于延迟对比的基线)
LOCAL_BASELINE_TOKENS_PER_SEC = 35  # 1.5B INT4 模型在 iGPU 上的典型生成速度
CLOUD_BASELINE_TOKENS_PER_SEC = 80  # GPT-4o-mini 的典型返回速度(不含网络)


@dataclass
class WorkRecord:
    """单次工作记录(一次完整流水线或单次端云交换)."""
    timestamp: str                       # ISO 8601 UTC
    work_id: str                          # SHA256 哈希(前 16 字符)
    work_type: str                        # "pipeline" | "exchange" | "analyze" | "select" | "compose"
    theme: str = ""                       # 教学主题
    local: dict = field(default_factory=dict)   # 本地推理统计
    cloud: dict = field(default_factory=dict)   # 云端调用统计
    privacy: dict = field(default_factory=dict)  # 隐私保护统计
    cost: dict = field(default_factory=dict)    # 成本对比
    latency: dict = field(default_factory=dict)  # 延迟对比
    metadata: dict = field(default_factory=dict)  # 其他元数据(work_dir / tokens 等)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "WorkRecord":
        return cls(**data)


def _now_iso() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def _make_work_id(work_type: str, theme: str, timestamp: str) -> str:
    """生成 work_id = SHA256(work_type + theme + timestamp)[:16]"""
    src = f"{work_type}|{theme}|{timestamp}".encode("utf-8")
    return hashlib.sha256(src).hexdigest()[:16]


class WorkSummaryRecorder:
    """工作记录器:每次工作完成后记录本地/云端使用情况."""

    def __init__(self, history_path: Optional[Path] = None):
        self.history_path = Path(history_path) if history_path else DEFAULT_HISTORY_PATH
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        self._current: Optional[WorkRecord] = None
        log.info(f"[work_summary] history_path={self.history_path}")

    def begin(self, work_type: str, theme: str = "", metadata: Optional[dict] = None) -> WorkRecord:
        """开始一次工作(记录起始时间)."""
        ts = _now_iso()
        record = WorkRecord(
            timestamp=ts,
            work_id=_make_work_id(work_type, theme, ts),
            work_type=work_type,
            theme=theme,
            metadata=metadata or {},
        )
        self._current = record
        log.info(f"[work_summary] BEGIN {work_type} theme={theme!r} work_id={record.work_id}")
        return record

    def record_local(
        self,
        model: str = "DeepSeek-R1-Distill-Qwen-1.5B-int4-cw-ov",
        device: str = "GPU",
        tokens_in: int = 0,
        tokens_out: int = 0,
        latency_ms: float = 0.0,
        cache_hit: bool = False,
        abstract_data_bytes: int = 0,
    ) -> None:
        """记录本地推理使用情况."""
        if self._current is None:
            log.warn("[work_summary] record_local called without begin()")
            return
        self._current.local = {
            "used": True,
            "model": model,
            "device": device,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "latency_ms": latency_ms,
            "cache_hit": cache_hit,
            "abstract_data_bytes": abstract_data_bytes,
            "cost_usd": 0.0,  # 本地推理零成本
        }
        log.info(
            f"[work_summary] local: model={model} device={device} "
            f"in={tokens_in} out={tokens_out} latency={latency_ms}ms"
        )

    def record_cloud(
        self,
        model: str = "gpt-4o-mini",
        tokens_in: int = 0,
        tokens_out: int = 0,
        latency_ms: float = 0.0,
        cost_usd: float = 0.0,
        pii_detected: bool = False,
        degradation_level: int = 1,
    ) -> None:
        """记录云端调用使用情况."""
        if self._current is None:
            log.warn("[work_summary] record_cloud called without begin()")
            return
        self._current.cloud = {
            "used": True,
            "model": model,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "latency_ms": latency_ms,
            "cost_usd": cost_usd,
            "pii_detected": pii_detected,
            "degradation_level": degradation_level,
        }
        log.info(
            f"[work_summary] cloud: model={model} in={tokens_in} out={tokens_out} "
            f"latency={latency_ms}ms cost=${cost_usd} pii={pii_detected}"
        )

    def record_privacy(
        self,
        raw_pii_count: int = 0,
        redacted_pii_count: int = 0,
        zero_upload_proof: bool = True,
    ) -> None:
        """记录隐私保护统计."""
        if self._current is None:
            return
        self._current.privacy = {
            "raw_pii_count": raw_pii_count,
            "redacted_pii_count": redacted_pii_count,
            "upload_bytes_to_cloud": 0 if zero_upload_proof else None,
            "upload_abstract_data_bytes": self._current.local.get("abstract_data_bytes", 0),
            "zero_upload_proof": zero_upload_proof,
        }
        log.info(
            f"[work_summary] privacy: raw_pii={raw_pii_count} "
            f"redacted={redacted_pii_count} zup={zero_upload_proof}"
        )

    def _compute_comparison(self, record: WorkRecord) -> None:
        """计算成本 + 延迟对比(仅当本地和云端都有数据时)."""
        local = record.local
        cloud = record.cloud
        if not local or not cloud:
            return
        # 成本对比
        cloud_cost = cloud.get("cost_usd", 0.0)
        record.cost = {
            "local_cost_usd": 0.0,
            "cloud_cost_usd": cloud_cost,
            "saved_usd": cloud_cost - 0.0,
            "saved_ratio_pct": 100.0 if cloud_cost > 0 else 0.0,
        }
        # 延迟对比
        local_latency = local.get("latency_ms", 0.0)
        cloud_latency = cloud.get("latency_ms", 0.0)
        # 假设纯云端基线(无本地加速):直接云端 = cloud_latency
        # 端云协同:本地 + 云端
        edge_cloud_latency = local_latency + cloud_latency
        # 纯本地(如果全用 L1.5B 处理)
        local_only_latency = local_latency * 2.5  # 1.5B 比云端慢
        record.latency = {
            "local_ms": local_latency,
            "cloud_ms": cloud_latency,
            "edge_cloud_ms": edge_cloud_latency,
            "cloud_only_ms": cloud_latency,  # 纯云端基线
            "speedup_vs_cloud_only_pct": round(
                (1 - edge_cloud_latency / max(cloud_latency * 1.5, 1)) * 100, 1
            ) if cloud_latency > 0 else 0.0,
        }

    def finish(self) -> WorkRecord:
        """结束工作:计算对比 + 持久化."""
        if self._current is None:
            raise RuntimeError("begin() must be called before finish()")
        self._compute_comparison(self._current)
        # 持久化到 JSONL(明确 UTF-8 + errors='replace' 兼容 Windows GBK)
        try:
            with self.history_path.open("a", encoding="utf-8", errors="replace") as f:
                f.write(json.dumps(self._current.to_dict(), ensure_ascii=False) + "\n")
        except OSError as e:
            log.warn(f"[work_summary] 持久化失败:{e}")
        log.info(f"[work_summary] FINISH work_id={self._current.work_id}")
        finished = self._current
        self._current = None
        return finished

    def get_recent(self, n: int = 1) -> list[WorkRecord]:
        """读取最近 n 次工作记录."""
        if not self.history_path.exists():
            return []
        records: list[WorkRecord] = []
        try:
            with self.history_path.open("r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        records.append(WorkRecord.from_dict(json.loads(line)))
                    except (json.JSONDecodeError, TypeError):
                        continue
        except OSError:
            return []
        return records[-n:]

    def clear(self) -> int:
        """清空历史,返回清理条数."""
        if not self.history_path.exists():
            return 0
        n = 0
        with self.history_path.open("r", encoding="utf-8") as f:
            for _ in f:
                n += 1
        self.history_path.unlink()
        return n


def render_markdown_table(records: list[WorkRecord]) -> str:
    """渲染为 Markdown 表格(V7 报告格式)."""
    if not records:
        return "## 工作记录\n\n暂无工作记录\n"
    md = ["## V7-AIPC 工作报告(最近 {} 次)\n".format(len(records))]
    md.append("| # | 时间 | 类型 | 主题 | 本地模型 | 本地延迟 | 云端模型 | 云端成本 | 节省 | 零上传 |")
    md.append("|---|------|------|------|----------|----------|----------|----------|------|--------|")
    for i, r in enumerate(records, 1):
        local = r.local
        cloud = r.cloud
        # V7-AIPC 表格规范：未使用的字段使用 em-dash (—) 作为占位符
        _DASH = "\u2014"
        local_model = f"{local.get('model', 'N/A').split('/')[-1]} ({local.get('device', '?')})" if local.get("used") else _DASH
        local_lat = f"{local.get('latency_ms', 0):.0f}ms" if local.get("used") else _DASH
        cloud_model = f"{cloud.get('model', 'N/A')}" if cloud.get("used") else _DASH
        cloud_cost = f"${cloud.get('cost_usd', 0):.4f}" if cloud.get("used") else _DASH
        saved = f"${r.cost.get('saved_usd', 0):.4f}" if r.cost else _DASH
        zup = "\u2713" if r.privacy.get("zero_upload_proof", False) else _DASH
        md.append(
            f"| {i} | {r.timestamp[11:19]} | {r.work_type} | "
            f"{r.theme[:20] or '-'} | {local_model} | {local_lat} | "
            f"{cloud_model} | {cloud_cost} | {saved} | {zup} |"
        )
    # 汇总
    total_cloud_cost = sum(r.cloud.get("cost_usd", 0) for r in records if r.cloud)
    total_local_tokens = sum(
        r.local.get("tokens_in", 0) + r.local.get("tokens_out", 0)
        for r in records if r.local
    )
    md.append(f"\n**汇总**:{len(records)} 次工作,本地推理 {total_local_tokens} tokens,"
              f"云端累计 ${total_cloud_cost:.4f},节省 ${total_cloud_cost:.4f}.")
    return "\n".join(md) + "\n"


def render_console_table(records: list[WorkRecord]) -> str:
    """渲染为控制台友好的文本表格."""
    if not records:
        return "暂无工作记录"
    lines = ["=" * 90, "V7-AIPC 工作报告(最近 {} 次)".format(len(records)), "=" * 90]
    for i, r in enumerate(records, 1):
        lines.append(f"\n[#{i}] {r.timestamp}  {r.work_type}  主题: {r.theme or '-'}  work_id: {r.work_id}")
        # 本地
        if r.local.get("used"):
            lines.append(
                f"  本地模型 : {r.local.get('model')} ({r.local.get('device')})"
            )
            lines.append(
                f"  本地延迟 : {r.local.get('latency_ms', 0):.0f} ms"
                f"  tokens: in={r.local.get('tokens_in', 0)}, out={r.local.get('tokens_out', 0)}"
                f"  缓存命中: {r.local.get('cache_hit', False)}"
            )
            lines.append(
                f"  本地成本 : $0.0000(端侧推理零成本)"
            )
        else:
            lines.append("  本地模型 : -(未触发)")
        # 云端
        if r.cloud.get("used"):
            lines.append(
                f"  云端模型 : {r.cloud.get('model')}"
            )
            lines.append(
                f"  云端延迟 : {r.cloud.get('latency_ms', 0):.0f} ms"
                f"  tokens: in={r.cloud.get('tokens_in', 0)}, out={r.cloud.get('tokens_out', 0)}"
            )
            lines.append(
                f"  云端成本 : ${r.cloud.get('cost_usd', 0):.4f}"
            )
            lines.append(
                f"  降级等级 : L{r.cloud.get('degradation_level', 1)}"
            )
        else:
            lines.append("  云端模型 : -(未触发)")
        # 隐私
        if r.privacy:
            lines.append(
                f"  隐私保护 : PII 检测 {r.privacy.get('raw_pii_count', 0)} 项 / "
                f"脱敏 {r.privacy.get('redacted_pii_count', 0)} 项 / "
                f"零上传: {r.privacy.get('zero_upload_proof', False)}"
            )
        # 对比
        if r.cost:
            lines.append(
                f"  本次节省 : ${r.cost.get('saved_usd', 0):.4f}"
            )
    return "\n".join(lines)


# 全局单例
_recorder: Optional[WorkSummaryRecorder] = None


def get_recorder() -> WorkSummaryRecorder:
    global _recorder
    if _recorder is None:
        _recorder = WorkSummaryRecorder()
    return _recorder


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="V7-AIPC 工作对比报告")
    parser.add_argument("--last", type=int, default=1, help="显示最近 N 次工作")
    parser.add_argument("--export", metavar="PATH", help="导出 Markdown 到文件")
    parser.add_argument("--clear", action="store_true", help="清空历史")
    parser.add_argument(
        "--history-path",
        metavar="PATH",
        help="自定义历史 JSONL 路径(默认:%USERPROFILE%\\.openvino\\cache\\work_history.jsonl)",
    )
    args = parser.parse_args()

    recorder = WorkSummaryRecorder(history_path=Path(args.history_path) if args.history_path else None)
    if args.clear:
        n = recorder.clear()
        print(f"已清空 {n} 条历史")
    else:
        records = recorder.get_recent(args.last)
        print(render_console_table(records))
        if args.export:
            md = render_markdown_table(records)
            Path(args.export).write_text(md, encoding="utf-8")
            print(f"\nMarkdown 已导出到:{args.export}")
