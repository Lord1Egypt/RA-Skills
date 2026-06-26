#!/usr/bin/env python3

import argparse
import json
import statistics
import sys
from collections import Counter


def parse_args():
    parser = argparse.ArgumentParser(description="Generate mall.yy.com game account market overview markdown.")
    parser.add_argument("input", nargs="?", help="Input JSON path. Reads stdin when omitted.")
    return parser.parse_args()


def load_payload(path):
    if path:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    return json.load(sys.stdin)


def yuan(cents):
    if cents is None:
        return "-"
    return f"¥{cents / 100:,.2f}"


def percentile(values, ratio):
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * ratio
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return round(ordered[lower] * (1 - weight) + ordered[upper] * weight)


def short_text(value, max_length=60):
    text = str(value or "").replace("\n", " ").strip()
    if len(text) <= max_length:
        return text
    return text[: max_length - 1] + "…"


def numeric(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def format_counter(items):
    if not items:
        return "-"
    return "、".join(f"{name}({count})" for name, count in items)


def detail_url(item):
    goods_id = item.get("goodsId")
    if goods_id is None:
        return None
    return f"https://mall.yy.com/?pageId=20000#/shop/detail/{goods_id}?exp_cause=2"


def item_line(item):
    price = yuan(item.get("salePrice") if numeric(item.get("salePrice")) else None)
    popularity = item.get("popularity") if numeric(item.get("popularity")) else "-"
    region = item.get("regionServer") or "-"
    title = short_text(item.get("goodsName"))
    url = detail_url(item)
    link = f"｜[详情]({url})" if url else ""
    return f"{price}｜热度 {popularity}｜{region}｜{title}{link}"


def compute_game_metrics(game):
    items = game.get("items") if isinstance(game.get("items"), list) else []
    prices = [item.get("salePrice") for item in items if numeric(item.get("salePrice"))]
    popularities = [item.get("popularity") for item in items if numeric(item.get("popularity"))]
    regions = Counter(item.get("regionServer") for item in items if item.get("regionServer"))
    labels = Counter()

    for item in items:
        for label in item.get("goodsLabels") or []:
            label_name = label.get("labelName") if isinstance(label, dict) else None
            if label_name:
                labels[label_name] += 1

    sample_count = len(items)
    p25 = percentile(prices, 0.25)
    median = round(statistics.median(prices)) if prices else None
    p75 = percentile(prices, 0.75)
    max_price = max(prices) if prices else None
    warnings = []
    error = game.get("error")
    has_more = bool(game.get("pagination", {}).get("hasMore"))

    if error:
        warnings.append(f"接口或分类异常：{error}")
    if sample_count == 0 and not error:
        warnings.append("当前采样无挂牌")
    if sample_count < 5:
        warnings.append("样本较少，价格代表性弱")
    if max_price is not None and p75 and max_price > p75 * 3:
        warnings.append("存在高价极端样本")
    if has_more:
        warnings.append("当前仅为前几页采样，仍有更多挂牌")

    return {
        "name": game.get("name") or "未知游戏",
        "sample_count": sample_count,
        "raw_count": game.get("pagination", {}).get("rawItemCount"),
        "min_price": min(prices) if prices else None,
        "p25": p25,
        "median": median,
        "p75": p75,
        "avg_price": round(sum(prices) / len(prices)) if prices else None,
        "max_price": max_price,
        "avg_popularity": round(sum(popularities) / len(popularities)) if popularities else None,
        "max_popularity": max(popularities) if popularities else None,
        "top_regions": regions.most_common(5),
        "top_labels": labels.most_common(5),
        "top_high_price": sorted(
            [item for item in items if numeric(item.get("salePrice"))],
            key=lambda item: item.get("salePrice"),
            reverse=True,
        )[:3],
        "top_popularity": sorted(
            [item for item in items if numeric(item.get("popularity"))],
            key=lambda item: item.get("popularity"),
            reverse=True,
        )[:3],
        "has_more": has_more,
        "error": error,
        "warnings": warnings,
    }


def sampling_text(payload):
    sampling = payload.get("sampling") or {}
    profiles = sampling.get("sortProfiles") or []
    if not sampling:
        return "未提供采样元信息"
    return (
        f"每游戏 {len(profiles)} 个排序视角({', '.join(profiles) or '-'})，"
        f"每视角最多 {sampling.get('pagesPerSort', '-')} 页，"
        f"每页 {sampling.get('pageSize', '-')} 条，按 goodsId 去重"
    )


def remark(metric):
    flags = []
    if metric["error"]:
        flags.append("异常")
    if metric["sample_count"] < 5:
        flags.append("样本少")
    if metric["has_more"]:
        flags.append("有更多页")
    return "、".join(flags) or "-"


def render_ranking(metrics):
    lines = ["| 排名 | 游戏 | 样本量 | 中位价 | 均价 | 最高价 | 热门区服 | 备注 |", "| --- | --- | ---: | ---: | ---: | ---: | --- | --- |"]
    for index, metric in enumerate(sorted(metrics, key=lambda item: item["sample_count"], reverse=True), 1):
        top_region = metric["top_regions"][0][0] if metric["top_regions"] else "-"
        lines.append(
            f"| {index} | {metric['name']} | {metric['sample_count']} | {yuan(metric['median'])} | "
            f"{yuan(metric['avg_price'])} | {yuan(metric['max_price'])} | {top_region} | {remark(metric)} |"
        )
    return "\n".join(lines)


def render_report(payload):
    games = payload.get("games") if isinstance(payload.get("games"), list) else []
    metrics = [compute_game_metrics(game) for game in games]
    total_samples = sum(metric["sample_count"] for metric in metrics)
    valid_metrics = [metric for metric in metrics if metric["sample_count"] > 0]

    lines = [
        "# 游戏账号交易大盘摘要",
        "",
        f"数据源：{payload.get('source', '-')}",
        f"采样时间：{payload.get('generatedAt', '-')}",
        f"采样口径：{sampling_text(payload)}",
        "",
        "## 总览",
        f"- 覆盖游戏：{len(games)}",
        f"- 有效样本：{total_samples}",
    ]

    if valid_metrics:
        most_samples = max(valid_metrics, key=lambda item: item["sample_count"])
        highest_avg = max(valid_metrics, key=lambda item: item["avg_price"] or 0)
        highest_median = max(valid_metrics, key=lambda item: item["median"] or 0)
        highest_price = max(valid_metrics, key=lambda item: item["max_price"] or 0)
        highest_popularity = max(valid_metrics, key=lambda item: item["avg_popularity"] or 0)
        lines.extend(
            [
                f"- 样本最多游戏：{most_samples['name']}（{most_samples['sample_count']} 条）",
                f"- 均价最高游戏：{highest_avg['name']}（{yuan(highest_avg['avg_price'])}）",
                f"- 中位价最高游戏：{highest_median['name']}（{yuan(highest_median['median'])}）",
                f"- 最高价样本游戏：{highest_price['name']}（{yuan(highest_price['max_price'])}）",
                f"- 平均热度最高游戏：{highest_popularity['name']}（{highest_popularity['avg_popularity']}）",
            ]
        )
    else:
        lines.append("- 暂无有效挂牌样本")

    lines.extend(["", "## 游戏排行", render_ranking(metrics) if metrics else "暂无游戏数据", "", "## 单游戏摘要"])

    for metric in metrics:
        lines.extend(
            [
                "",
                f"### {metric['name']}",
                f"- 样本量：{metric['sample_count']}（原始采样 {metric['raw_count'] if metric['raw_count'] is not None else '-'}）",
                "- 价格："
                f"最低 {yuan(metric['min_price'])} / P25 {yuan(metric['p25'])} / 中位 {yuan(metric['median'])} / "
                f"P75 {yuan(metric['p75'])} / 最高 {yuan(metric['max_price'])}",
                f"- 热度：平均 {metric['avg_popularity'] if metric['avg_popularity'] is not None else '-'} / 最高 {metric['max_popularity'] if metric['max_popularity'] is not None else '-'}",
                f"- 热门区服：{format_counter(metric['top_regions'])}",
                f"- 热门标签：{format_counter(metric['top_labels'])}",
            ]
        )

        if metric["top_high_price"]:
            lines.append("- 高价样本：")
            for index, item in enumerate(metric["top_high_price"], 1):
                lines.append(f"  {index}. {item_line(item)}")

        if metric["top_popularity"]:
            lines.append("- 人气样本：")
            for index, item in enumerate(metric["top_popularity"], 1):
                lines.append(f"  {index}. {item_line(item)}")

        if metric["warnings"]:
            lines.append(f"- 提示：{'；'.join(metric['warnings'])}")

    lines.extend(["", "## 异常与解读"])
    warning_lines = []
    for metric in metrics:
        for warning in metric["warnings"]:
            warning_lines.append(f"- {metric['name']}：{warning}")
    if warning_lines:
        lines.extend(warning_lines)
    else:
        lines.append("- 未发现明显采样异常。")
    lines.append("- 本报告基于挂牌采样，不代表全量市场，也不代表成交价。")

    return "\n".join(lines)


def main():
    args = parse_args()
    payload = load_payload(args.input)
    sys.stdout.write(render_report(payload))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
