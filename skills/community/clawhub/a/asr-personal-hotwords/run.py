#!/usr/bin/env python3
"""
run.py — ASR 热词挖掘主控制器

Pipeline: 提取 OpenClaw 对话 → 调用远端 asr-corrector → 输出歧义词表
"""

import argparse
import csv
import io
import json
import glob
import os
import sys
import time
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import yaml

from extract_sessions import extract_sessions, chunk_chat_data

logger = logging.getLogger(__name__)

CST = timezone(timedelta(hours=8))
SCRIPT_DIR = Path(__file__).parent
POLL_INTERVAL = 5
POLL_TIMEOUT = 600


def _http_session() -> requests.Session:
    """创建带重试的 HTTP Session"""
    s = requests.Session()
    retry = Retry(total=3, backoff_factor=2, status_forcelist=[502, 503, 504])
    s.mount("http://", HTTPAdapter(max_retries=retry))
    s.mount("https://", HTTPAdapter(max_retries=retry))
    return s


http = _http_session()


def load_config() -> dict:
    """加载 config.yaml"""
    config_path = SCRIPT_DIR / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_openclaw_llm_config() -> dict:
    """从 ~/.openclaw/openclaw.json 自动读取 LLM 配置（provider, model, api_key, base_url, api_format）"""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    with open(config_path, "r", encoding="utf-8") as f:
        oc_config = json.load(f)

    # 解析 agents.defaults.model.primary -> "provider/model_id"
    primary = (
        oc_config.get("agents", {})
        .get("defaults", {})
        .get("model", {})
        .get("primary", "")
    )
    if "/" not in primary:
        raise ValueError(f"Cannot parse primary model: '{primary}', expected 'provider/model_id'")

    provider_name, model_id = primary.split("/", 1)

    # 查找 provider 配置
    providers = oc_config.get("models", {}).get("providers", {})
    if provider_name not in providers:
        providers = oc_config.get("providers", {})
    if provider_name not in providers:
        raise ValueError(f"Provider '{provider_name}' not found in openclaw.json")

    p = providers[provider_name]

    # api 格式映射: "anthropic-messages" -> "anthropic", "openai-chat" -> "openai"
    api_raw = p.get("api", "anthropic-messages")
    api_format = "anthropic" if "anthropic" in api_raw else "openai"

    return {
        "api_key": p.get("apiKey", ""),
        "base_url": p.get("baseUrl", ""),
        "model": model_id,
        "api_format": api_format,
    }


def load_anchors(output_dir: Path) -> list:
    """从 output 目录加载所有历史 vocab 结果，合并去重后作为 anchors"""
    vocab = load_all_vocabs(output_dir)
    if not vocab:
        logger.info("无历史 vocab 文件，anchors 为空")
        return []

    anchors = [
        {"term": v["term"], "category": v.get("category", "unknown"), "desc": v.get("desc", "")}
        for v in vocab
    ]
    logger.info(f"加载 {len(anchors)} 个 anchors（去重后）")
    return anchors


def submit_task(server_url: str, chat_data: str, anchors: list, llm_config: dict, min_freq: int) -> str:
    """提交 build-vocab 任务，返回 task_id"""
    payload = {
        "chat_data": chat_data,
        "anchors": anchors,
        "llm": llm_config,
        "min_freq": min_freq,
    }
    resp = http.post(f"{server_url}/api/build-vocab", json=payload, timeout=30)
    resp.raise_for_status()
    result = resp.json()
    task_id = result.get("task_id")
    if not task_id:
        raise RuntimeError(f"No task_id in response: {result}")
    return task_id


def poll_task(server_url: str, task_id: str) -> dict:
    """轮询任务直到完成，返回结果"""
    start = time.time()
    while time.time() - start < POLL_TIMEOUT:
        time.sleep(POLL_INTERVAL)
        resp = http.get(f"{server_url}/api/tasks/{task_id}", timeout=10)
        status = resp.json()
        state = status.get("status")
        logger.info(f"  任务 {task_id[:8]}... 状态: {state}")

        if state == "completed":
            resp = http.get(f"{server_url}/api/tasks/{task_id}/result", timeout=10)
            return resp.json()
        elif state == "failed":
            raise RuntimeError(f"任务失败: {status.get('message', 'unknown')}")

    raise TimeoutError(f"任务超时 ({POLL_TIMEOUT}s)")


def merge_vocabs(vocab_list: list[list]) -> list:
    """合并多个 vocab 结果（按 term 去重，合并词频）"""
    merged = {}
    for vocab in vocab_list:
        for item in vocab:
            term = item["term"]
            if term in merged:
                merged[term]["frequency"] = max(
                    merged[term].get("frequency", 0),
                    item.get("frequency", 0)
                )
                # 合并 ASR errors
                existing = set(merged[term].get("possible_asr_errors", []))
                existing.update(item.get("possible_asr_errors", []))
                merged[term]["possible_asr_errors"] = sorted(existing)
            else:
                merged[term] = item.copy()
    return sorted(merged.values(), key=lambda x: x.get("frequency", 0), reverse=True)


# ============================================================
# 导出模块
# ============================================================

def load_all_vocabs(output_dir: Path) -> list:
    """加载所有 vocab 文件，合并去重，过滤无效词条"""
    vocab_files = sorted(glob.glob(str(output_dir / "vocab_*.json")))
    vocab_files = [f for f in vocab_files if ".bak." not in f]

    merged = {}
    for fpath in vocab_files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data.get("vocab", []):
                term = item["term"]
                if term in merged:
                    merged[term]["frequency"] = max(
                        merged[term].get("frequency", 0),
                        item.get("frequency", 0),
                    )
                    existing = set(merged[term].get("possible_asr_errors", []))
                    existing.update(item.get("possible_asr_errors", []))
                    merged[term]["possible_asr_errors"] = sorted(existing)
                    if len(item.get("desc", "")) > len(merged[term].get("desc", "")):
                        merged[term]["desc"] = item["desc"]
                else:
                    merged[term] = item.copy()
        except Exception as e:
            logger.warning(f"加载失败 {fpath}: {e}")

    result = sorted(merged.values(), key=lambda x: x.get("frequency", 0), reverse=True)
    return [
        v for v in result
        if v.get("desc", "").strip() or v.get("possible_asr_errors", [])
    ]


def export_txt(vocab: list) -> str:
    return "\n".join(item["term"] for item in vocab)


def export_json(vocab: list) -> str:
    output = []
    for item in vocab:
        output.append({
            "term": item["term"],
            "possible_asr_errors": item.get("possible_asr_errors", []),
            "category": item.get("category", ""),
            "desc": item.get("desc", ""),
        })
    return json.dumps(output, indent=2, ensure_ascii=False)


def export_csv(vocab: list) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["热词", "类别", "说明", "常见误识别", "词频"])
    for item in vocab:
        writer.writerow([
            item["term"],
            item.get("category", ""),
            item.get("desc", ""),
            "、".join(item.get("possible_asr_errors", [])),
            item.get("frequency", 0),
        ])
    return buf.getvalue()


def export_prompt(vocab: list) -> str:
    lines = [
        "以下是用户场景中的专有名词和易混淆词汇表。",
        "语音转录时，如果听到与「常见误识别」列发音相近的内容，请优先转录为「正确词」列的写法。",
        "",
        "| 正确词 | 常见误识别 |",
        "|--------|-----------|",
    ]
    for item in vocab:
        errors = "、".join(item.get("possible_asr_errors", []))
        lines.append(f"| {item['term']} | {errors} |")
    return "\n".join(lines)


EXPORT_FORMATTERS = {
    "txt": export_txt,
    "json": export_json,
    "csv": export_csv,
    "prompt": export_prompt,
}


def export_hotwords(output_dir: Path, fmt: str = "prompt", output_file: Path = None, min_freq: int = 1):
    """从所有 vocab 文件导出热词表"""
    vocab = load_all_vocabs(output_dir)
    logger.info(f"导出热词表: {len(vocab)} 个热词")

    if min_freq > 1:
        vocab = [v for v in vocab if v.get("frequency", 0) >= min_freq]
        logger.info(f"词频 >= {min_freq} 过滤后: {len(vocab)} 个")

    result = EXPORT_FORMATTERS[fmt](vocab)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        logger.info(f"热词表已导出到: {output_file}")
    return result


def run(target_date: str, end_date: str = None):
    """主流程"""
    config = load_config()
    server_url = config["server_url"]
    extract_cfg = config["extract"]
    output_dir = SCRIPT_DIR / config.get("output_dir", "output")
    output_dir.mkdir(exist_ok=True)

    # 1. 加载 LLM 配置（全自动从 openclaw.json 读取）
    logger.info("从 openclaw.json 自动读取 LLM 配置...")
    llm_config = load_openclaw_llm_config()
    logger.info(f"  Model: {llm_config['model']}, Format: {llm_config['api_format']}")

    # 2. 健康检查
    logger.info(f"检查远端服务 {server_url}...")
    try:
        resp = http.get(f"{server_url}/health", timeout=10)
        resp.raise_for_status()
    except requests.exceptions.ConnectionError:
        logger.error(f"无法连接远端服务 {server_url}，请检查服务是否运行")
        print(json.dumps({"status": "error", "message": f"远端服务不可用: {server_url}"}, ensure_ascii=False))
        return
    except requests.exceptions.Timeout:
        logger.error(f"连接远端服务超时 {server_url}")
        print(json.dumps({"status": "error", "message": f"连接超时: {server_url}"}, ensure_ascii=False))
        return
    logger.info("  服务正常 ✓")

    # 3. 提取对话
    agents = extract_cfg.get("agents", ["*"])
    logger.info(f"提取对话: {target_date}" + (f" ~ {end_date}" if end_date else "") + f" (agents: {agents})")
    messages = extract_sessions(
        target_date=target_date,
        agents=agents,
        max_content_len=extract_cfg.get("max_content_len", 300),
        end_date=end_date,
    )

    if not messages:
        logger.warning("未提取到任何消息，退出")
        print(json.dumps({"status": "empty", "message": "无可用对话数据"}, ensure_ascii=False))
        return

    logger.info(f"提取到 {len(messages)} 条消息")

    # 4. 加载 anchors（历史结果）
    anchors = load_anchors(output_dir)

    # 5. 分块 + 提交任务
    chunks = chunk_chat_data(messages)
    logger.info(f"分为 {len(chunks)} 个块提交")

    all_vocabs = []
    for i, chunk in enumerate(chunks):
        logger.info(f"提交块 {i+1}/{len(chunks)} ({len(chunk)} 字符, {chunk.count(chr(10))+1} 行)...")
        task_id = submit_task(
            server_url, chunk, anchors, llm_config,
            extract_cfg.get("min_freq", 3)
        )
        logger.info(f"  Task ID: {task_id}")
        result = poll_task(server_url, task_id)
        vocab = result.get("vocab", [])
        all_vocabs.append(vocab)
        logger.info(f"  块 {i+1} 完成: {len(vocab)} 条热词")

    # 6. 合并结果
    merged_vocab = merge_vocabs(all_vocabs) if len(all_vocabs) > 1 else (all_vocabs[0] if all_vocabs else [])

    # 7. 保存
    date_label = target_date if not end_date or end_date == target_date else f"{target_date}_{end_date}"
    output_path = output_dir / f"vocab_{date_label}.json"

    # 如果同日期结果已存在，备份而不是覆盖
    if output_path.exists():
        ts_suffix = datetime.now(CST).strftime("%H%M%S")
        backup_path = output_dir / f"vocab_{date_label}.{ts_suffix}.bak.json"
        output_path.rename(backup_path)
        logger.info(f"已备份旧结果: {backup_path.name}")

    output_data = {
        "meta": {
            "source": "asr-personal-hotwords",
            "target_date": target_date,
            "end_date": end_date or target_date,
            "built_at": datetime.now(CST).isoformat(),
            "messages_count": len(messages),
            "chunks_count": len(chunks),
        },
        "vocab": merged_vocab,
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    logger.info(f"结果保存到: {output_path}")

    # 8. 导出 hotwords.md
    hotwords_path = SCRIPT_DIR / "hotwords.md"
    export_hotwords(output_dir, fmt="prompt", output_file=hotwords_path)

    # 9. 输出摘要
    summary = {
        "status": "success",
        "date": date_label,
        "messages_count": len(messages),
        "vocab_count": len(merged_vocab),
        "output_file": str(output_path),
        "top_terms": [
            {
                "term": v["term"],
                "freq": v.get("frequency", 0),
                "asr_errors": v.get("possible_asr_errors", []),
            }
            for v in merged_vocab[:10]
        ],
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )

    parser = argparse.ArgumentParser(description="ASR 热词挖掘")
    parser.add_argument("--date", default=None, help="目标日期 YYYY-MM-DD（默认前一天）")
    parser.add_argument("--start", default=None, help="起始日期")
    parser.add_argument("--end", default=None, help="结束日期")
    parser.add_argument("--export-only", action="store_true", help="仅导出热词表，不执行挖掘")
    parser.add_argument("--format", "-f", choices=["txt", "json", "csv", "prompt"], default="prompt", help="导出格式")
    parser.add_argument("--output", "-o", default=None, help="导出文件路径")
    parser.add_argument("--min-freq", type=int, default=1, help="导出时最低词频过滤")
    args = parser.parse_args()

    # 仅导出模式
    if args.export_only:
        output_dir = SCRIPT_DIR / "output"
        output_file = Path(args.output) if args.output else None
        result = export_hotwords(output_dir, fmt=args.format, output_file=output_file, min_freq=args.min_freq)
        if not args.output:
            print(result)
        return

    if args.start:
        target_date = args.start
        end_date = args.end or args.start
    elif args.date:
        target_date = args.date
        end_date = args.date
    else:
        yesterday = datetime.now(CST) - timedelta(days=1)
        target_date = yesterday.strftime("%Y-%m-%d")
        end_date = target_date

    run(target_date=target_date, end_date=end_date)


if __name__ == "__main__":
    main()
