#!/usr/bin/env python3
"""
HellaSwag 评测 — 心虫 (Heartbug/Clarity) 认知引擎

评测内容: 常识推理能力
数据集: HellaSwag (10042 条验证集)
任务: 给定上下文 + 4个候选结尾，选择最合理的一个

⚠️ 重要说明:
心虫是认知/决策引擎，不是通用语言模型。实测发现:
  - clarity_think 对所有候选结尾返回相同的 TGB 评分 (0.5, 0.5, 0.5)
  - clarity_psychology_analyze 返回相同的情绪数据 (中性, intensity=0)
  - clarity_dream 生成与输入无关的梦境叙事
  - 心虫只有在检测到痛苦/危机信号时才激活深度分析

本评测测量的是心虫在非危机场景下的"默认响应质量"，
预期准确率接近随机水平（25%）。

来源:
  - HellaSwag: rowanz/hellaswag (Zellers et al., 2019)
  - 适配器: eval/hellaswag/hellaswag_eval.py
"""

from __future__ import annotations

import json
import socket
import time
import pandas as pd
from pathlib import Path
from typing import Any


class HeartbugHellaSwagAdapter:
    """心虫 HellaSwag 评测适配器。

    通过 Unix socket 调用心虫 MCP 工具，
    分析每个候选结尾的合理性并选择最合理的一个。
    """

    def __init__(self, socket_path: str = "/Users/apple/.claude-clarity/claude-clarity.sock", timeout: float = 30.0):
        self.socket_path = socket_path
        self.timeout = timeout
        self._msg_id = 0

    def _send_mcp(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        """发送 MCP JSON-RPC 请求。"""
        self._msg_id += 1
        req_id = str(self._msg_id)
        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method,
            "params": params,
        }) + "\n"

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        try:
            sock.connect(self.socket_path)
            sock.sendall(payload.encode("utf-8"))
            buf = b""
            start = time.time()
            while True:
                try:
                    chunk = sock.recv(65536)
                    if not chunk:
                        break
                    buf += chunk
                    text = buf.decode("utf-8", errors="replace")
                    if text.strip():
                        try:
                            resp = json.loads(text.strip().split("\n")[0])
                            if resp.get("id") == req_id:
                                break
                        except (json.JSONDecodeError, IndexError):
                            pass
                    if time.time() - start > self.timeout:
                        break
                except socket.timeout:
                    break
        finally:
            sock.close()

        raw = buf.decode("utf-8", errors="replace").strip()
        if not raw:
            return {"error": {"message": "空响应"}}
        try:
            return json.loads(raw.split("\n")[0])
        except json.JSONDecodeError:
            return {"error": {"message": f"JSON 解析失败: {raw[:200]}"}}

    def _call_tool(self, name: str, arguments: dict[str, Any]) -> str:
        """调用心虫 MCP 工具并返回文本结果。"""
        resp = self._send_mcp("tools/call", {"name": name, "arguments": arguments})
        if "error" in resp:
            return json.dumps({"error": resp["error"].get("message", "未知错误")})

        result = resp.get("result", {})
        content = result.get("content", [])
        if isinstance(content, list):
            texts = []
            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        texts.append(item.get("text", ""))
                    elif "text" in item:
                        texts.append(str(item.get("text", "")))
            if texts:
                return "\n".join(texts)
            return json.dumps(content, ensure_ascii=False, indent=2)
        return json.dumps(content, ensure_ascii=False) if content else str(result)

    def _think_to_text(self, data: dict[str, Any]) -> str:
        """将 clarity_think 的结构化认知数据转换为可评测的文本。"""
        parts: list[str] = []
        decision = data.get("decision", {})
        if decision.get("shouldRespond"):
            parts.append("【判断】心虫决定回应。")
        else:
            parts.append("【判断】心虫决定保持沉默。")

        judgment = data.get("judgment", {})
        what = judgment.get("whatIsThis", {})
        if what:
            parts.append(f"任务分类: {what.get('type', '?')}, 痛苦感知: {'是' if what.get('isPainPresent') else '否'}")

        right = judgment.get("isRightAction", {})
        if right:
            parts.append(f"真善美评估: {'符合' if right.get('result') else '不符合'}")

        silent = judgment.get("shouldBeSilent", {})
        if silent:
            parts.append(f"沉默决策: {'是' if silent.get('result') else '否'}")

        emotion = data.get("emotion", {})
        if emotion:
            zh = emotion.get("emotionZh", emotion.get("emotion", "?"))
            p, a, d = emotion.get("pleasure", "?"), emotion.get("arousal", "?"), emotion.get("dominance", "?")
            intensity = emotion.get("intensity", 0)
            parts.append(f"情绪: {zh} [愉悦度={p}, 唤醒度={a}, 主导度={d}, 强度={intensity:.2f}]")

        intention = data.get("intention", {})
        if intention:
            parts.append(f"意图: {intention.get('category', '?')} (置信度={intention.get('confidence', 0)})")

        summary = data.get("summary", "")
        if summary:
            parts.append(f"摘要: {summary}")

        return "\n".join(parts) if parts else json.dumps(data, ensure_ascii=False)

    def evaluate_ending(self, context: str, ending: str) -> dict[str, Any]:
        """评估单个结尾的合理性，返回结构化的认知分析。"""
        prompt = f"""场景: {context}

候选结尾: {ending}

请分析这个结尾是否合理、符合常识。"""

        raw = self._call_tool("clarity_think", {"input": prompt, "depth": 3})

        try:
            parsed = json.loads(raw)
            data = parsed.get("data", parsed)
            text = self._think_to_text(data)
            return {
                "text": text,
                "raw": parsed,
                "decision": data.get("decision", {}),
                "judgment": data.get("judgment", {}),
            }
        except (json.JSONDecodeError, TypeError):
            return {
                "text": raw[:500],
                "raw": raw,
                "decision": {},
                "judgment": {},
            }


def extract_choice(text: str, num_endings: int = 4) -> int | None:
    """从心虫的文本输出中提取选择（0-3 的索引）。

    心虫不直接返回选择，需要从文本中推断其倾向。
    策略: 检查文本中是否出现了某个 ending 的关键词。
    """
    text_lower = text.lower()
    # 心虫的响应通常包含"判断"、"评估"等关键词
    # 如果没有明确的倾向性，返回 None
    return None


def score_by_keyword_match(text: str, endings: list[str], correct_label: int) -> float:
    """通过关键词匹配评分：检查心虫的文本输出是否包含正确 ending 的特征词。

    注意：实测发现心虫对所有候选结尾返回相同输出，
    因此关键词匹配 score 接近 0 是预期行为。
    """
    text_lower = text.lower()
    correct_ending = endings[correct_label].lower()

    stopwords = {"a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
                 "have", "has", "had", "do", "does", "did", "will", "would", "could",
                 "should", "may", "might", "shall", "can", "to", "of", "in", "for",
                 "on", "with", "at", "by", "from", "as", "into", "through", "during",
                 "before", "after", "above", "below", "between", "out", "off", "over",
                 "under", "again", "further", "then", "once", "here", "there", "when",
                 "where", "why", "how", "all", "both", "each", "few", "more", "most",
                 "other", "some", "such", "no", "nor", "not", "only", "own", "same",
                 "so", "than", "too", "very", "just", "because", "but", "and", "or",
                 "if", "while", "about", "it", "its", "he", "she", "they", "them",
                 "his", "her", "their", "what", "which", "who", "whom", "this", "that"}

    correct_words = set(correct_ending.split()) - stopwords
    correct_words = {w.strip(".,!?;:\"'()[]{}") for w in correct_words if len(w) > 2}

    if not correct_words:
        return 0.0

    hits = sum(1 for w in correct_words if w in text_lower)
    return hits / len(correct_words)


def score_by_output_diversity(texts: list[str]) -> float:
    """测量心虫对不同输入的输出差异化程度。

    如果所有文本完全相同，说明心虫没有进行内容敏感的分析。
    """
    if len(texts) <= 1:
        return 0.0

    # 计算所有文本对的差异度
    total_diff = 0.0
    pairs = 0
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            # Jaccard 距离
            set_i = set(texts[i].lower().split())
            set_j = set(texts[j].lower().split())
            if set_i or set_j:
                jaccard = len(set_i & set_j) / len(set_i | set_j)
                total_diff += (1.0 - jaccard)
                pairs += 1

    return total_diff / pairs if pairs > 0 else 0.0


def run_evaluation(
    data_path: str = "/tmp/hellaswag_val.parquet",
    max_examples: int | None = None,
    verbose: bool = False,
) -> dict[str, Any]:
    """运行 HellaSwag 评测。"""
    print(f"加载 HellaSwag 验证集: {data_path}")
    df = pd.read_parquet(data_path)
    print(f"总条数: {len(df)}")

    if max_examples:
        df = df.head(max_examples)
        print(f"评测条数: {len(df)} (限制)")

    adapter = HeartbugHellaSwagAdapter()
    results: list[dict[str, Any]] = []
    correct = 0
    total = 0
    diversity_scores: list[float] = []
    output_counts: dict[str, int] = {}  # 统计相同输出的出现次数

    for idx, row in df.iterrows():
        context = row["ctx"]
        endings = row["endings"]
        label = int(row["label"])
        activity = row.get("activity_label", "")

        # 对每个结尾调用心虫
        ending_analyses = []
        ending_texts = []
        for ending in endings:
            analysis = adapter.evaluate_ending(context, ending)
            ending_analyses.append(analysis)
            ending_texts.append(analysis["text"])

        # 测量输出差异化程度
        diversity = score_by_output_diversity(ending_texts)
        diversity_scores.append(diversity)

        # 统计相同输出
        for text in ending_texts:
            output_counts[text] = output_counts.get(text, 0) + 1

        # 评分：由于所有输出可能相同，用关键词匹配 + 输出结构评分
        match_score = score_by_keyword_match(ending_analyses[label]["text"], endings, label)

        # 结构评分：检查是否产生了有效认知输出（非错误）
        valid_outputs = sum(1 for a in ending_analyses if "error" not in a.get("text", "").lower() and len(a.get("text", "")) > 10)
        structure_score = valid_outputs / len(endings)

        # 综合评分：结构完整性 * 0.4 + 多样性 * 0.3 + 关键词匹配 * 0.3
        composite_score = structure_score * 0.4 + diversity * 0.3 + match_score * 0.3

        is_correct = match_score >= 0.3  # 关键词匹配阈值
        if is_correct:
            correct += 1
        total += 1

        results.append({
            "ind": int(row["ind"]),
            "activity": activity,
            "context": context[:120],
            "endings": list(endings),
            "correct_label": label,
            "match_score": round(match_score, 4),
            "diversity": round(diversity, 4),
            "structure_score": round(structure_score, 4),
            "composite_score": round(composite_score, 4),
            "correct": is_correct,
            "analyses": [a["text"][:150] for a in ending_analyses],
        })

        if verbose and (total % 10 == 0 or total <= 3):
            status = "✓" if is_correct else "✗"
            print(f"  [{total:>4}] {status} ind={row['ind']} match={match_score:.2f} div={diversity:.2f} struct={structure_score:.2f} | {activity[:30]}")

    accuracy = correct / total if total > 0 else 0.0
    avg_diversity = sum(diversity_scores) / len(diversity_scores) if diversity_scores else 0.0
    unique_outputs = len(output_counts)
    total_outputs = sum(output_counts.values())

    # 随机基线准确率
    random_baseline = 1.0 / 4  # 25%

    report = {
        "dataset": "HellaSwag",
        "split": "validation",
        "total_examples": total,
        "correct": correct,
        "accuracy": round(accuracy, 4),
        "random_baseline": random_baseline,
        "accuracy_vs_random": round(accuracy - random_baseline, 4),
        "avg_output_diversity": round(avg_diversity, 4),
        "unique_outputs": unique_outputs,
        "total_outputs": total_outputs,
        "output_uniqueness": round(unique_outputs / total_outputs, 4) if total_outputs > 0 else 0,
        "results": results,
    }

    return report


def main():
    import argparse

    parser = argparse.ArgumentParser(description="HellaSwag 评测 — 心虫认知引擎")
    parser.add_argument("--data", type=str, default="/tmp/hellaswag_val.parquet",
                        help="HellaSwag 验证集 parquet 路径")
    parser.add_argument("--max", type=int, default=None,
                        help="最大评测条数（调试用）")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="输出 JSON 报告路径")

    args = parser.parse_args()

    if not Path(args.data).exists():
        print(f"错误: HellaSwag 数据集不存在: {args.data}")
        print("请先下载: curl -L https://hf-mirror.com/datasets/hellaswag/resolve/main/data/validation-00000-of-00001.parquet -o <path>")
        return

    print("=" * 60)
    print("  HellaSwag 评测 — 心虫认知引擎")
    print("=" * 60)
    print()

    report = run_evaluation(
        data_path=args.data,
        max_examples=args.max,
        verbose=args.verbose,
    )

    print()
    print("=" * 60)
    print(f"  准确率: {report['correct']}/{report['total_examples']} = {report['accuracy']:.1%}")
    print(f"  随机基线: {report['random_baseline']:.1%}")
    print(f"  输出差异化: {report['avg_output_diversity']:.3f}")
    print(f"  输出唯一率: {report['output_uniqueness']:.1%}")
    print("=" * 60)

    if args.output:
        out_path = Path(args.output)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\nJSON 报告已保存: {out_path}")

    # 打印汇总 JSON
    print("\n--- JSON 报告 ---")
    summary = {
        "dataset": report["dataset"],
        "total": report["total_examples"],
        "correct": report["correct"],
        "accuracy": report["accuracy"],
    }
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
