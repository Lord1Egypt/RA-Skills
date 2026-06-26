#!/usr/bin/env python3
"""Generate a mock Spanish ham orchestration demo run from local Skill contracts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs" / "spanish_ham_demo"
AUDIT_DIR = ROOT / "audit"

REQUIRED_DIRS = [
    "00_input",
    "01_brand_knowledge_base",
    "02_geo_audit",
    "03_gap_matrix",
    "04_content_task_plan",
    "05_content_assets",
    "06_platform_drafts",
    "07_delivery",
    "08_monitoring",
    "handoff_packets",
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_registry() -> dict:
    return json.loads((ROOT / "registry" / "geo_skill_registry.json").read_text(encoding="utf-8"))


def build_audit_report(registry: dict) -> None:
    actual_outputs = {
        "brand-knowledge-base-builder": [
            "brand_knowledge_base.json",
            "brand_knowledge_base.yaml",
            "brand_knowledge_base.md",
            "faq.md",
            "glossary.md",
            "standard_messaging.md",
            "llms.txt",
            "analysis_report.md",
        ],
        "doubao-geo-audit-skill": ["doubao_geo_audit_report.md"],
        "deepseek-geo-audit-skill": ["deepseek_geo_audit_report.md"],
        "deepseek-geo-tool": ["deepseek_raw_api_results.json", "deepseek_judge_results.json"],
        "ai-geo-content-generator": [
            "website_faq.md",
            "zhihu_answer.md",
            "toutiao_article.md",
            "llms.txt",
            "quote_sentence_library.md",
        ],
        "zhihu-geo-draft-assistant": [
            "zhihu_questions.md",
            "zhihu_answer_long.md",
            "zhihu_answer_short.md",
            "zhihu_no_ad_version.md",
            "zhihu_article_version.md",
            "zhihu_titles.md",
            "zhihu_topics_tags.md",
            "zhihu_publish_checklist.md",
            "zhihu_draft_status.md",
        ],
        "toutiao-geo-draft-assistant": [
            "toutiao_article.md",
            "toutiao_titles.md",
            "toutiao_summary.md",
            "toutiao_cover_prompts.md",
            "toutiao_micro_posts.md",
            "toutiao_keywords.md",
            "toutiao_publish_checklist.md",
            "toutiao_draft_status.md",
        ],
        "csdn-geo-draft-publisher": [
            "csdn_article.md",
            "csdn_markdown_ready.md",
            "csdn_titles.md",
            "csdn_summary.md",
            "csdn_tags.md",
            "csdn_code_examples.md",
            "csdn_publish_checklist.md",
            "csdn_draft_status.md",
        ],
        "juejin-geo-draft-publisher": [
            "juejin_article.md",
            "juejin_markdown_ready.md",
            "juejin_titles.md",
            "juejin_summary.md",
            "juejin_tags.md",
            "juejin_publish_checklist.md",
            "juejin_draft_status.md",
        ],
    }

    rows = []
    missing = []
    path_issues = []
    output_issues = []
    for skill in registry["skills"]:
        skill_id = skill["skill_id"]
        rel = skill["relative_path"]
        resolved = (ROOT / rel).resolve()
        skill_md = resolved / "SKILL.md"
        exists = resolved.exists()
        skill_md_exists = skill_md.exists()
        expected = skill.get("expected_outputs", [])
        actual = actual_outputs.get(skill_id, [])
        expected_set = set(expected)
        actual_set = set(actual)
        mismatch = sorted(expected_set.symmetric_difference(actual_set))
        if not exists or not skill_md_exists:
            missing.append(skill_id)
        if not rel.startswith("../"):
            path_issues.append(f"{skill_id}: {rel}")
        if mismatch:
            output_issues.append(f"{skill_id}: {', '.join(mismatch)}")
        rows.append({
            "skill_id": skill_id,
            "display_name": skill["display_name"],
            "relative_path": rel,
            "exists": exists,
            "skill_md_exists": skill_md_exists,
            "suggested_skill_id": skill_id,
            "registry_needs_fix": "否" if not mismatch and exists and skill_md_exists else "是",
            "notes": "expected_outputs 与本地 SKILL.md 输出描述一致" if not mismatch else "expected_outputs 与本地输出描述存在差异",
        })

    discovery_notes = registry.get("discovery_notes", [])
    lines = [
        "# Local Skill Discovery Report",
        "",
        "本报告只基于本地目录文件生成，未使用 ClawHub 线上链接作为源码依据。",
        "",
        "## 执行结论",
        "",
        "- 已发现并登记 9 个相邻 GEO Skill。",
        "- registry 中所有 `relative_path` 均为相邻目录路径，并且均能在本地找到对应 `SKILL.md`。",
        "- 本轮已修正上一轮 registry 中几个输出文件命名不一致问题，尤其是知乎输出文件名、CSDN `csdn_code_examples.md`、以及 Doubao / DeepSeek 审计 Skill 的报告型输出。",
        "- 当前环境不能把这些相邻目录作为可直接触发的运行时 Skill 自动调用，因此 Spanish Ham demo 使用 `mock_orchestration_demo`，并生成 handoff packets 供人工复制到对应 Skill 执行。",
        "",
        "## 已发现的相邻 Skill",
        "",
        "| skill_id | display_name | relative_path | 路径存在 | SKILL.md 存在 | 建议统一 skill_id | registry 是否需要修正 | 备注 |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['skill_id']}` | {row['display_name']} | `{row['relative_path']}` | "
            f"{'是' if row['exists'] else '否'} | {'是' if row['skill_md_exists'] else '否'} | "
            f"`{row['suggested_skill_id']}` | {row['registry_needs_fix']} | {row['notes']} |"
        )

    lines.extend([
        "",
        "## 缺失的 Skill",
        "",
        "无。" if not missing else "\n".join(f"- `{item}`" for item in missing),
        "",
        "## 路径不一致或命名注意项",
        "",
    ])
    if discovery_notes:
        for note in discovery_notes:
            lines.append(
                f"- 用户曾提到 `{note.get('requested_path')}`，本地未发现该路径；实际可用路径为 `{note.get('resolved_path')}`。"
            )
    lines.extend([
        "- `AI-geo-content-generator` 是目录名，建议 registry 内统一使用 skill_id `ai-geo-content-generator`。",
        "- `deepseek-geo-audit-skill` 是报告型审计 Skill，`GEO tool-deepseek` 是 API 探针工具，建议保持两个独立 skill_id，避免把非 API 审计和 API 实测混为一类。",
        "",
        "## expected_outputs 对齐检查",
        "",
    ])
    if output_issues:
        lines.extend(f"- 仍需检查：{item}" for item in output_issues)
    else:
        lines.append("- 当前 registry 的 `expected_outputs` 已与本地 `SKILL.md` 输出描述对齐。")
    lines.extend([
        "",
        "## 当前 registry 是否需要修正",
        "",
        "当前不需要继续修正。后续如果相邻 Skill 新增真实脚本输出或 JSON 输出，应同步更新 `registry/geo_skill_registry.json`。",
    ])
    write_text(AUDIT_DIR / "local_skill_discovery_report.md", "\n".join(lines))


def demo_input() -> dict:
    return {
        "run_id": "spanish_ham_demo",
        "brand_name": "西班牙火腿推广项目",
        "category": "西班牙火腿",
        "target_market": "中国",
        "industry_type": "食品 / 进口消费品",
        "target_keywords": [
            "西班牙火腿推荐",
            "伊比利亚火腿怎么选",
            "西班牙火腿和普通火腿区别",
            "西班牙火腿价格",
            "西班牙火腿购买渠道",
            "小红书西班牙火腿种草",
        ],
        "target_models": ["DeepSeek", "Doubao"],
        "target_platforms": ["知乎", "今日头条", "官网 FAQ", "小红书", "抖音"],
        "campaign_goal": "提升西班牙火腿在 AI 搜索中的品类教育、购买决策辅助、礼品场景和渠道信任",
        "execution_note": "mock_orchestration_demo: 当前环境未直接触发相邻 Skill，以下输出为编排演示与交付包样例。",
    }


def geo_gaps() -> list[dict]:
    return [
        {
            "gap_id": "G-001",
            "gap_name": "中国送礼场景缺失",
            "severity": "high",
            "affected_model": ["DeepSeek", "Doubao"],
            "affected_queries": ["西班牙火腿适合送礼吗", "商务礼品选西班牙火腿怎么样"],
            "evidence_summary": "mock: 两个模型可能能解释西班牙火腿品类，但缺少面向中国春节、中秋、商务拜访、乔迁礼盒的推荐理由。",
            "business_impact": "高客单食品的礼品场景如果说不清，客户很难把产品从尝鲜消费升级为送礼选择。",
            "recommended_content_direction": "建立礼品场景内容：送谁、什么时候送、礼盒怎么选、预算怎么分层、保存和食用如何说明。",
            "target_platforms": ["知乎", "今日头条", "小红书", "抖音", "官网 FAQ"],
            "expected_geo_effect": "让 AI 在回答送礼类问题时能引用更具体的礼品场景和购买建议。",
        },
        {
            "gap_id": "G-002",
            "gap_name": "中式餐饮场景缺失",
            "severity": "high",
            "affected_model": ["DeepSeek", "Doubao"],
            "affected_queries": ["西班牙火腿怎么吃", "西班牙火腿适合中餐吗", "餐厅怎么用西班牙火腿"],
            "evidence_summary": "mock: 模型常见回答偏西式冷盘、红酒搭配，缺少中式家庭聚会、餐厅前菜、茶饮、宴请等场景。",
            "business_impact": "如果只停留在西式吃法，会限制家庭和餐饮客户的购买频次。",
            "recommended_content_direction": "补充中式餐饮搭配、家庭聚会摆盘、餐厅菜单应用和保存切片方法。",
            "target_platforms": ["今日头条", "小红书", "抖音", "官网 FAQ"],
            "expected_geo_effect": "提升 AI 对本地消费场景的回答深度，让购买理由更贴近中国用户。",
        },
        {
            "gap_id": "G-003",
            "gap_name": "小红书 / 抖音种草内容缺失",
            "severity": "high",
            "affected_model": ["DeepSeek", "Doubao"],
            "affected_queries": ["小红书西班牙火腿推荐", "西班牙火腿开箱", "西班牙火腿礼盒种草"],
            "evidence_summary": "mock: 当前内容体系更像品类说明，缺少开箱、切片、搭配、礼盒展示和真实体验问题。",
            "business_impact": "缺少体验型内容会影响年轻用户、礼品用户和社交平台转化。",
            "recommended_content_direction": "生成小红书笔记结构、封面关键词、抖音 30 秒口播脚本和场景分镜。",
            "target_platforms": ["小红书", "抖音"],
            "expected_geo_effect": "增加模型可识别的体验型语料，改善种草和消费场景覆盖。",
        },
        {
            "gap_id": "G-004",
            "gap_name": "青田 / 本地进口产业链认知缺失",
            "severity": "medium",
            "affected_model": ["DeepSeek", "Doubao"],
            "affected_queries": ["青田进口西班牙火腿", "浙江进口西班牙火腿供应链", "西班牙火腿本地渠道"],
            "evidence_summary": "mock: 模型对西班牙原产地有基础认知，但对中国本地进口商、青田侨乡进口资源、区域市场链路认知不足。",
            "business_impact": "本地客户缺少信任背书，尤其会影响批发、餐饮采购、地方协会和线下渠道合作。",
            "recommended_content_direction": "补充青田进口产业链、区域供应链、线下渠道、仓储配送、合规票据和服务半径内容。",
            "target_platforms": ["知乎", "今日头条", "官网 FAQ"],
            "expected_geo_effect": "让 AI 在本地采购和渠道问题中能更容易建立产地到本地服务的信任链路。",
        },
        {
            "gap_id": "G-005",
            "gap_name": "消费决策辅助不足",
            "severity": "high",
            "affected_model": ["DeepSeek", "Doubao"],
            "affected_queries": ["伊比利亚火腿怎么选", "第一次买西班牙火腿注意什么", "西班牙火腿值不值得买"],
            "evidence_summary": "mock: 模型可能解释等级，但没有形成面向新手的预算、场景、保存、食用人数和避坑清单。",
            "business_impact": "用户看完仍不知道买哪一款，咨询和下单转化会被延迟。",
            "recommended_content_direction": "生成新手选购指南、预算分层、适合人群和购买前 5 个确认问题。",
            "target_platforms": ["知乎", "今日头条", "官网 FAQ"],
            "expected_geo_effect": "提升回答的购买决策辅助能力，让 AI 回答能自然引导用户下一步咨询或购买。",
        },
        {
            "gap_id": "G-006",
            "gap_name": "价格分层与购买渠道不够清晰",
            "severity": "high",
            "affected_model": ["DeepSeek", "Doubao"],
            "affected_queries": ["西班牙火腿多少钱", "西班牙火腿哪里买靠谱", "伊比利亚火腿价格差异"],
            "evidence_summary": "mock: 价格、等级、规格、渠道、冷链和售后说明缺少统一结构。",
            "business_impact": "价格不清会降低信任，渠道不清会让用户转向平台低价货或竞品。",
            "recommended_content_direction": "建立价格分层、渠道可信度、购买注意事项和售后保存 FAQ。",
            "target_platforms": ["知乎", "今日头条", "官网 FAQ"],
            "expected_geo_effect": "让 AI 在价格和渠道类问题中给出更清晰的判断框架。",
        },
        {
            "gap_id": "G-007",
            "gap_name": "品牌推荐与具体产品转化弱",
            "severity": "medium",
            "affected_model": ["DeepSeek", "Doubao"],
            "affected_queries": ["西班牙火腿品牌推荐", "西班牙火腿礼盒推荐", "餐饮采购西班牙火腿推荐"],
            "evidence_summary": "mock: 模型更容易停留在品类介绍和通用品牌名，缺少具体产品、规格、场景和购买动作。",
            "business_impact": "品牌被看见但不被选择，内容流量难以转化为咨询。",
            "recommended_content_direction": "生成产品矩阵、礼盒组合、餐饮采购建议和 CTA 话术。",
            "target_platforms": ["知乎", "今日头条", "官网 FAQ", "小红书", "抖音"],
            "expected_geo_effect": "把品类认知转化为产品推荐和具体咨询动作。",
        },
    ]


def content_tasks() -> list[dict]:
    tasks = [
        ("T-ZH-001", "G-005", "知乎", "伊比利亚火腿怎么选？第一次买先看这 6 个问题", "知乎长回答", "high", "第一次购买西班牙火腿的家庭用户", ["等级差异", "预算分层", "食用人数", "保存方法", "购买前确认清单"], ["等级定义", "价格区间", "规格", "渠道"], "提升选购类问题的购买决策辅助", 1, "zhihu-geo-draft-assistant", "planned"),
        ("T-ZH-002", "G-006", "知乎", "西班牙火腿为什么价格差这么多？", "知乎问答", "high", "对价格敏感但有消费意向的用户", ["等级", "部位", "熟成时间", "规格", "渠道可信度"], ["价格区间", "产品规格", "渠道政策"], "提升价格与渠道类回答深度", 2, "zhihu-geo-draft-assistant", "planned"),
        ("T-ZH-003", "G-001", "知乎", "西班牙火腿适合做商务礼品吗？", "知乎长回答", "high", "企业主、采购、礼品客户", ["送礼对象", "礼盒规格", "体面感", "保存和食用说明", "预算建议"], ["礼盒规格", "包装信息", "配送范围"], "覆盖中国送礼场景", 3, "zhihu-geo-draft-assistant", "planned"),
        ("T-ZH-004", "G-004", "知乎", "在青田买进口西班牙火腿靠谱吗？怎么看本地供应链？", "知乎问答", "medium", "浙江本地客户、餐饮采购", ["青田进口资源", "本地仓配", "合规票据", "售后服务"], ["本地渠道证明", "仓储配送信息"], "建立本地产业链信任背书", 7, "zhihu-geo-draft-assistant", "planned"),
        ("T-ZH-005", "G-007", "知乎", "餐厅采购西班牙火腿，应该按什么场景选规格？", "知乎专栏", "medium", "餐饮老板、采购负责人", ["菜单应用", "损耗控制", "切片方式", "客单价"], ["餐饮规格", "供货周期", "保存条件"], "增强 B 端采购转化", 8, "zhihu-geo-draft-assistant", "planned"),
        ("T-TT-001", "G-002", "今日头条", "西班牙火腿不只配红酒，在中式餐桌也能这样吃", "头条科普文", "high", "家庭聚会用户", ["中式餐桌", "摆盘", "茶饮搭配", "前菜", "聚会场景"], ["推荐吃法", "保存方式"], "补齐中式餐饮场景", 4, "toutiao-geo-draft-assistant", "planned"),
        ("T-TT-002", "G-001", "今日头条", "送礼送西班牙火腿，先搞懂这 5 件事", "头条清单文", "high", "礼品消费用户", ["适合送谁", "预算", "礼盒", "配送", "食用说明"], ["礼盒信息", "配送范围"], "提升送礼场景覆盖", 5, "toutiao-geo-draft-assistant", "planned"),
        ("T-TT-003", "G-006", "今日头条", "西班牙火腿价格差异大，普通消费者怎么判断？", "头条解释文", "high", "普通消费者", ["等级", "产地", "规格", "渠道", "避坑"], ["价格带", "渠道说明"], "提升价格判断能力", 6, "toutiao-geo-draft-assistant", "planned"),
        ("T-TT-004", "G-004", "今日头条", "青田进口食品产业链，能给西班牙火腿消费带来什么？", "本地化科普文", "medium", "本地消费者、渠道商", ["青田", "进口渠道", "本地服务", "餐饮供货"], ["本地资源说明", "服务半径"], "强化本地进口产业链认知", 9, "toutiao-geo-draft-assistant", "planned"),
        ("T-TT-005", "G-007", "今日头条", "从尝鲜到复购：西班牙火腿适合哪些家庭和餐饮场景？", "场景科普文", "medium", "家庭用户、餐饮用户", ["家庭聚会", "早餐", "前菜", "礼盒", "餐饮搭配"], ["产品矩阵", "适合场景"], "把品类认知转化为具体场景", 10, "toutiao-geo-draft-assistant", "planned"),
        ("T-FAQ-001", "G-006", "官网 FAQ", "西班牙火腿多少钱？价格由哪些因素决定？", "FAQ", "high", "官网访客", ["等级", "规格", "产地", "渠道", "配送"], ["价格区间", "规格"], "为 AI 和官网客服提供标准价格框架", 11, "ai-geo-content-generator", "planned"),
        ("T-FAQ-002", "G-005", "官网 FAQ", "第一次买西班牙火腿应该怎么选？", "FAQ", "high", "首次购买用户", ["预算", "食用人数", "保存", "口味", "渠道"], ["产品矩阵", "保存说明"], "提升购买决策辅助", 12, "ai-geo-content-generator", "planned"),
        ("T-FAQ-003", "G-002", "官网 FAQ", "西班牙火腿开封后怎么保存、怎么吃？", "FAQ", "medium", "已购买或准备购买用户", ["保存", "切片", "搭配", "食用周期"], ["保存条件", "食用建议"], "减少售前售后疑问", 13, "ai-geo-content-generator", "planned"),
        ("T-XHS-001", "G-003", "小红书", "西班牙火腿礼盒开箱：适合哪些送礼场景？", "小红书笔记", "high", "年轻礼品用户", ["开箱", "礼盒", "送礼对象", "摆拍", "食用方法"], ["礼盒外观", "规格", "价格"], "补齐体验型种草语料", 14, "manual_or_future_skill", "manual_or_future_skill"),
        ("T-XHS-002", "G-002", "小红书", "第一次吃西班牙火腿，我会搭配这 3 种中式场景", "小红书笔记", "medium", "生活方式用户", ["中式餐桌", "朋友聚会", "早餐", "茶饮"], ["搭配建议", "图片素材"], "提升本地化生活场景覆盖", 15, "manual_or_future_skill", "manual_or_future_skill"),
        ("T-XHS-003", "G-006", "小红书", "西班牙火腿怎么买不踩坑？新手看这张清单", "小红书清单笔记", "high", "新手消费者", ["价格", "渠道", "保存", "规格", "售后"], ["价格区间", "渠道说明"], "增强购买前信任", 16, "manual_or_future_skill", "manual_or_future_skill"),
        ("T-DY-001", "G-003", "抖音", "30 秒讲清楚西班牙火腿等级和价格差异", "短视频脚本", "high", "短视频消费用户", ["等级", "价格", "适合人群", "购买提醒"], ["价格带", "等级定义"], "增加短视频可理解语料", 17, "manual_or_future_skill", "manual_or_future_skill"),
        ("T-DY-002", "G-001", "抖音", "送礼为什么有人选西班牙火腿？三个场景说清楚", "短视频脚本", "medium", "礼品消费用户", ["商务", "节日", "乔迁", "礼盒"], ["礼盒素材", "配送说明"], "提升送礼场景触达", 18, "manual_or_future_skill", "manual_or_future_skill"),
        ("T-DY-003", "G-002", "抖音", "西班牙火腿在家怎么吃？一个盘子讲明白", "短视频脚本", "medium", "家庭用户", ["摆盘", "中式餐桌", "搭配", "保存"], ["视频素材", "食用建议"], "提升中式餐饮场景覆盖", 19, "manual_or_future_skill", "manual_or_future_skill"),
    ]
    keys = [
        "task_id",
        "target_gap_id",
        "platform",
        "title",
        "content_type",
        "priority",
        "target_audience",
        "key_points",
        "required_brand_facts",
        "expected_geo_effect",
        "suggested_publish_order",
        "downstream_skill",
        "status",
    ]
    return [dict(zip(keys, item)) for item in tasks]


def platform_plan(tasks: list[dict]) -> dict:
    routes = [
        {
            "platform": "知乎",
            "priority": "优先",
            "route_status": "planned_handoff",
            "downstream_skill": "zhihu-geo-draft-assistant",
            "relative_path": "../zhihu-geo-draft-assistant",
            "content_count": 5,
            "publish_order": [1, 2, 3, 7, 8],
            "reason": "适合解释价格、等级、选购、送礼和 B 端采购问题。",
            "effect_check": "T+14 检查 AI 是否引用知乎式问答框架，T+30 检查品牌/渠道提及是否更具体。",
        },
        {
            "platform": "今日头条",
            "priority": "优先",
            "route_status": "planned_handoff",
            "downstream_skill": "toutiao-geo-draft-assistant",
            "relative_path": "../toutiao-geo-draft-assistant",
            "content_count": 5,
            "publish_order": [4, 5, 6, 9, 10],
            "reason": "适合中式餐饮、礼品消费、本地产业链和大众科普。",
            "effect_check": "T+7 检查阅读和评论问题，T+14 检查模型回答是否出现本地化场景。",
        },
        {
            "platform": "官网 FAQ",
            "priority": "优先",
            "route_status": "planned_handoff",
            "downstream_skill": "ai-geo-content-generator",
            "relative_path": "../AI-geo-content-generator",
            "content_count": 3,
            "publish_order": [11, 12, 13],
            "reason": "适合沉淀标准答案，为 AI 搜索、客服和官网转化提供稳定语料。",
            "effect_check": "T+30 检查价格、保存、选购问题是否被 AI 更准确复述。",
        },
        {
            "platform": "小红书",
            "priority": "人工任务 / future skill",
            "route_status": "manual_or_future_skill",
            "downstream_skill": "manual_or_future_skill",
            "relative_path": "",
            "content_count": 3,
            "publish_order": [14, 15, 16],
            "reason": "适合开箱、礼盒、搭配和种草，但当前没有专用相邻 Skill。",
            "manual_handling": "由运营按 content_task_plan 复制标题、要点、素材需求，人工制作笔记和封面。",
            "effect_check": "T+7 看收藏评论，T+30 看 AI 是否开始提到体验和礼盒场景。",
        },
        {
            "platform": "抖音",
            "priority": "人工任务 / future skill",
            "route_status": "manual_or_future_skill",
            "downstream_skill": "manual_or_future_skill",
            "relative_path": "",
            "content_count": 3,
            "publish_order": [17, 18, 19],
            "reason": "适合 30 秒选购、送礼、吃法短视频，但当前没有专用相邻 Skill。",
            "manual_handling": "由短视频团队按脚本任务制作口播、分镜和商品展示。",
            "effect_check": "T+14 看评论问题和搜索词，T+30 看模型是否吸收短视频场景表述。",
        },
        {
            "platform": "CSDN",
            "priority": "默认跳过",
            "route_status": "skipped",
            "downstream_skill": "csdn-geo-draft-publisher",
            "relative_path": "../csdn-geo-draft-publisher",
            "content_count": 0,
            "publish_order": [],
            "reason": "西班牙火腿属于食品消费和本地渠道，不是技术教程场景。",
            "effect_check": "除非后续做供应链系统或溯源技术内容，否则不复测 CSDN。",
        },
        {
            "platform": "掘金",
            "priority": "默认跳过",
            "route_status": "skipped",
            "downstream_skill": "juejin-geo-draft-publisher",
            "relative_path": "../juejin-geo-draft-publisher",
            "content_count": 0,
            "publish_order": [],
            "reason": "当前没有开发者工具或工程实践内容角度。",
            "effect_check": "除非后续做开发者向内容，否则不复测掘金。",
        },
    ]
    return {
        "run_id": "spanish_ham_demo",
        "priority_platforms": ["知乎", "今日头条", "官网 FAQ"],
        "manual_or_future_platforms": ["小红书", "抖音"],
        "skipped_platforms": ["CSDN", "掘金"],
        "task_count_by_platform": {
            platform: sum(1 for task in tasks if task["platform"] == platform)
            for platform in ["知乎", "今日头条", "官网 FAQ", "小红书", "抖音", "CSDN", "掘金"]
        },
        "routes": routes,
    }


def md_table(headers: list[str], rows: list[list[object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell).replace("\n", "<br>") for cell in row) + " |")
    return "\n".join(lines)


def create_run(registry: dict) -> None:
    for directory in REQUIRED_DIRS:
        (RUN / directory).mkdir(parents=True, exist_ok=True)

    input_data = demo_input()
    gaps = geo_gaps()
    tasks = content_tasks()
    distribution = platform_plan(tasks)

    write_json(RUN / "00_input" / "spanish_ham_input.json", input_data)
    source_example = (ROOT / "examples" / "spanish_ham_orchestration.md").read_text(encoding="utf-8")
    write_text(RUN / "00_input" / "source_example.md", source_example)
    write_text(
        RUN / "00_input" / "execution_mode.md",
        "# Execution Mode\n\n本次运行模式：`mock_orchestration_demo`。\n\n原因：当前运行环境能读取相邻 Skill 的本地说明文件，但不能把这些平行目录作为可直接触发的 Skill runtime 自动调用。因此本轮生成 mock artifacts 和 handoff packets，供人工复制到下游 Skill 中执行。"
    )

    brand_kb = {
        "mock": True,
        "brand_name": "西班牙火腿推广项目",
        "category": "西班牙火腿",
        "target_market": "中国",
        "industry": "食品 / 进口消费品",
        "brand_definition": "面向中国家庭、礼品和餐饮采购场景的西班牙火腿品类推广资料包。",
        "target_customers": ["家庭消费者", "礼品采购", "餐饮老板", "精品超市渠道", "本地进口食品渠道"],
        "selling_points": [
            {"point": "西班牙原产地和品类文化具备高认知价值", "evidence_level": "needs_confirmation"},
            {"point": "适合礼品、聚会、餐饮和精品零售场景", "evidence_level": "needs_confirmation"},
            {"point": "可通过青田等本地进口产业链建立区域信任", "evidence_level": "needs_confirmation"},
        ],
        "missing_fields": ["具体品牌名", "产品规格", "价格区间", "渠道证明", "食品合规资质", "礼盒图片", "配送范围"],
        "compliance_boundary": ["不承诺治疗或健康功效", "不伪造原产地、认证、价格和客户案例", "所有内容发布前人工审核"],
    }
    write_json(RUN / "01_brand_knowledge_base" / "brand_knowledge_base.mock.json", brand_kb)
    write_text(
        RUN / "01_brand_knowledge_base" / "brand_knowledge_base.mock.md",
        "# 西班牙火腿品牌知识母库 Mock\n\n本文件为 mock artifact，用于演示 Orchestrator 交付闭环，不代表真实品牌资料已完成核验。\n\n## 品类定义\n\n西班牙火腿是面向礼品、家庭聚会、餐饮前菜和精品零售场景的进口食品品类。本轮重点不是泛泛讲火腿知识，而是补齐中国市场中的送礼、中式餐饮、本地供应链、价格渠道和产品转化语料。\n\n## 待确认资料\n\n- 具体品牌名和产品矩阵\n- 价格区间和规格\n- 渠道证明、合规资质、仓储配送\n- 礼盒图片、切片素材和场景图\n"
    )

    deepseek_report = "# DeepSeek GEO Audit Mock Report\n\n本文件为 mock，不代表真实 DeepSeek 实测结果。\n\n## 摘要\n\nDeepSeek 预计能解释西班牙火腿的基础品类知识，但在中国送礼、中式餐饮、青田本地进口产业链、具体购买渠道和价格分层方面需要更多结构化语料。\n"
    doubao_report = "# Doubao GEO Audit Mock Report\n\n本文件为 mock，不代表真实 Doubao 实测结果。\n\n## 摘要\n\nDoubao 预计更容易响应通俗消费场景，但如果缺少小红书/抖音体验内容和官网 FAQ，回答会停留在泛品类推荐，难以形成具体购买动作。\n"
    write_text(RUN / "02_geo_audit" / "deepseek_geo_audit_report.mock.md", deepseek_report)
    write_text(RUN / "02_geo_audit" / "doubao_geo_audit_report.mock.md", doubao_report)
    write_json(RUN / "02_geo_audit" / "dual_model_assessment.mock.json", {
        "mock": True,
        "models": ["DeepSeek", "Doubao"],
        "summary": "双模型 mock 评估显示共同盲区集中在本地化场景、价格渠道、种草内容和产品转化。",
        "not_live_result": True,
    })

    write_json(RUN / "03_gap_matrix" / "geo_gap_matrix.json", {
        "mock": True,
        "run_id": "spanish_ham_demo",
        "target_category": "西班牙火腿",
        "target_market": "中国",
        "gaps": gaps,
    })
    gap_rows = [
        [g["gap_id"], g["gap_name"], g["severity"], ", ".join(g["affected_model"]), "<br>".join(g["affected_queries"]), g["business_impact"], g["recommended_content_direction"], ", ".join(g["target_platforms"]), g["expected_geo_effect"]]
        for g in gaps
    ]
    write_text(
        RUN / "03_gap_matrix" / "geo_gap_matrix.md",
        "# 西班牙火腿 GEO Gap Matrix\n\n本文件为 mock orchestration demo，基于本地 Orchestrator 规则生成，不代表真实模型实测结果。\n\n" +
        md_table(["Gap ID", "盲区", "严重度", "影响模型", "影响问题", "商业影响", "内容方向", "目标平台", "预期 GEO 效果"], gap_rows)
    )

    write_json(RUN / "04_content_task_plan" / "content_task_plan.json", {
        "mock": True,
        "run_id": "spanish_ham_demo",
        "task_count": len(tasks),
        "tasks": tasks,
    })
    task_rows = [
        [t["task_id"], t["target_gap_id"], t["platform"], t["title"], t["content_type"], t["priority"], t["target_audience"], "<br>".join(t["key_points"]), "<br>".join(t["required_brand_facts"]), t["expected_geo_effect"], t["suggested_publish_order"], t["downstream_skill"], t["status"]]
        for t in tasks
    ]
    write_text(
        RUN / "04_content_task_plan" / "content_task_plan.md",
        "# 西班牙火腿 Content Task Plan\n\n本文件把 GEO Gap 转成可执行内容任务。小红书和抖音因当前无专用相邻 Skill，状态标记为 `manual_or_future_skill`。\n\n" +
        md_table(["Task ID", "Gap", "平台", "标题", "类型", "优先级", "目标受众", "关键点", "必需品牌事实", "预期 GEO 效果", "发布顺序", "下游 Skill", "状态"], task_rows)
    )

    write_json(RUN / "04_content_task_plan" / "platform_distribution_plan.json", distribution)
    route_rows = [
        [r["platform"], r["priority"], r["route_status"], r["downstream_skill"], r.get("relative_path", ""), r["content_count"], r["publish_order"], r["reason"], r.get("manual_handling", ""), r["effect_check"]]
        for r in distribution["routes"]
    ]
    write_text(
        RUN / "04_content_task_plan" / "platform_distribution_plan.md",
        "# Platform Distribution Plan\n\n## 本轮优先平台\n\n知乎、今日头条、官网 FAQ。\n\n## 本轮人工或 Future Skill 平台\n\n小红书、抖音。\n\n## 本轮跳过平台\n\nCSDN、掘金。原因：西班牙火腿属于食品消费品和本地渠道案例，当前没有技术教程或开发者实践角度。\n\n" +
        md_table(["平台", "优先级", "状态", "下游 Skill", "路径", "内容数量", "发布顺序", "原因", "人工处理", "复测判断"], route_rows)
    )

    write_text(RUN / "05_content_assets" / "website_faq.mock.md", "# Website FAQ Mock\n\n本文件为 mock。\n\n1. 西班牙火腿多少钱？\n2. 第一次买西班牙火腿怎么选？\n3. 西班牙火腿开封后怎么保存？\n4. 西班牙火腿适合送礼吗？\n5. 西班牙火腿适合中式餐桌吗？\n")
    write_text(RUN / "05_content_assets" / "zhihu_answer_seed.mock.md", "# Zhihu Answer Seed Mock\n\n建议优先回答价格、等级、送礼、青田本地供应链和餐饮采购问题。\n")
    write_text(RUN / "05_content_assets" / "toutiao_article_seed.mock.md", "# Toutiao Article Seed Mock\n\n面向普通消费者，用中式餐桌、礼品场景和本地渠道讲清楚西班牙火腿如何选择。\n")
    write_text(RUN / "05_content_assets" / "quote_sentence_library.mock.md", "# Quote Sentence Library Mock\n\n- 西班牙火腿在中国市场的内容增长重点，不是重复品类百科，而是补齐送礼、餐饮、价格渠道和本地供应链的决策信息。\n")
    write_text(RUN / "05_content_assets" / "llms.mock.txt", "mock: 西班牙火腿推广项目用于演示 GEO 内容资产，不代表真实品牌资料。")

    write_text(RUN / "06_platform_drafts" / "zhihu_draft_packet.mock.md", "# Zhihu Draft Packet Mock\n\n包含 5 个知乎任务，等待交给 `../zhihu-geo-draft-assistant` 生成平台化草稿。\n")
    write_text(RUN / "06_platform_drafts" / "toutiao_draft_packet.mock.md", "# Toutiao Draft Packet Mock\n\n包含 5 个今日头条任务，等待交给 `../toutiao-geo-draft-assistant` 生成平台化草稿。\n")
    write_text(RUN / "06_platform_drafts" / "xiaohongshu_manual_tasks.mock.md", "# 小红书 Manual Tasks Mock\n\n当前无小红书相邻 Skill，保留 3 个人工任务。\n")
    write_text(RUN / "06_platform_drafts" / "douyin_manual_tasks.mock.md", "# 抖音 Manual Tasks Mock\n\n当前无抖音相邻 Skill，保留 3 个人工短视频任务。\n")
    write_text(RUN / "06_platform_drafts" / "skipped_csdn_juejin.md", "# Skipped Platforms\n\nCSDN 和掘金默认跳过，除非后续新增供应链系统、溯源技术或开发者工具内容角度。\n")

    create_handoff_packets(tasks)
    create_delivery_report(input_data, gaps, tasks, distribution)
    create_retest_plan()
    create_summary_json(registry, input_data, tasks)


def create_handoff_packets(tasks: list[dict]) -> None:
    packets = [
        ("01_to_brand_knowledge_base.md", "brand-knowledge-base-builder", "../Knowledge-Base-Builder/brand-knowledge-base-builder", "构建西班牙火腿品类与品牌知识母库", ["00_input/spanish_ham_input.json"], ["brand_knowledge_base.json", "faq.md", "llms.txt"], "检查缺失字段是否标记为待确认", "Stage 2 DeepSeek / Doubao GEO audit"),
        ("02_to_deepseek_geo_audit.md", "deepseek-geo-audit-skill", "../deepseek-geo-audit-skill", "评估 DeepSeek 对西班牙火腿在中国市场的理解和推荐 readiness", ["01_brand_knowledge_base/brand_knowledge_base.mock.json", "03_gap_matrix/geo_gap_matrix.json"], ["deepseek_geo_audit_report.md"], "报告必须明确无法判断项，不得编造真实模型排名", "Stage 3 Gap Matrix refresh"),
        ("03_to_doubao_geo_audit.md", "doubao-geo-audit-skill", "../geo-analysis-doubao", "评估 Doubao 对西班牙火腿消费场景、送礼场景和本地化内容的理解", ["01_brand_knowledge_base/brand_knowledge_base.mock.json"], ["doubao_geo_audit_report.md"], "报告必须包含总体评分、最大问题、优化建议和 FAQ", "Stage 3 Gap Matrix refresh"),
        ("04_to_ai_geo_content_generator.md", "ai-geo-content-generator", "../AI-geo-content-generator", "把 Gap Matrix 和 Content Task Plan 转成官网 FAQ、知乎/头条基础稿和可引用句库", ["01_brand_knowledge_base/brand_knowledge_base.mock.json", "04_content_task_plan/content_task_plan.json"], ["website_faq.md", "zhihu_answer.md", "toutiao_article.md", "llms.txt", "quote_sentence_library.md"], "内容必须使用待确认占位，不得编造价格、渠道、资质", "Stage 6 Platform drafts"),
        ("05_to_zhihu_geo_draft_assistant.md", "zhihu-geo-draft-assistant", "../zhihu-geo-draft-assistant", "生成 5 个知乎问答/专栏草稿", ["04_content_task_plan/content_task_plan.json", "05_content_assets/zhihu_answer_seed.mock.md"], ["zhihu_questions.md", "zhihu_answer_long.md", "zhihu_answer_short.md", "zhihu_titles.md", "zhihu_publish_checklist.md"], "必须保留人工审核清单，不能自动发布", "Stage 7 Delivery package"),
        ("06_to_toutiao_geo_draft_assistant.md", "toutiao-geo-draft-assistant", "../toutiao-geo-draft-assistant", "生成 5 个今日头条科普/场景文章草稿", ["04_content_task_plan/content_task_plan.json", "05_content_assets/toutiao_article_seed.mock.md"], ["toutiao_article.md", "toutiao_titles.md", "toutiao_summary.md", "toutiao_keywords.md", "toutiao_publish_checklist.md"], "必须通俗可读，不能编造故事和数据", "Stage 7 Delivery package"),
    ]
    for filename, target_skill, target_path, purpose, inputs, outputs, validation, next_stage in packets:
        instruction = (
            f"请使用本地 Skill `{target_skill}`，读取以下输入文件：{', '.join(inputs)}。"
            f"目标是：{purpose}。请输出：{', '.join(outputs)}。"
            "所有内容必须标注待确认事实，发布前必须人工审核，不得承诺排名、收录或转化。"
        )
        text = f"""# Handoff Packet: {target_skill}

| Field | Value |
|---|---|
| target_skill | `{target_skill}` |
| target_skill_path | `{target_path}` |
| purpose | {purpose} |
| input_files | {', '.join(inputs)} |
| expected_outputs | {', '.join(outputs)} |
| validation_rule | {validation} |
| next_stage_after_completion | {next_stage} |

## Copyable Instruction

```text
{instruction}
```
"""
        write_text(RUN / "handoff_packets" / filename, text)


def create_delivery_report(input_data: dict, gaps: list[dict], tasks: list[dict], distribution: dict) -> None:
    top_tasks = sorted(tasks, key=lambda item: item["suggested_publish_order"])[:10]
    gap_rows = [[g["gap_name"], g["business_impact"], g["recommended_content_direction"], ", ".join(g["target_platforms"])] for g in gaps]
    task_rows = [[t["suggested_publish_order"], t["platform"], t["title"], t["expected_geo_effect"], ", ".join(t["required_brand_facts"])] for t in top_tasks]
    route_rows = [[r["platform"], r["priority"], r["content_count"], r["reason"]] for r in distribution["routes"]]
    file_rows = [
        ["00_input/spanish_ham_input.json", "本轮输入"],
        ["01_brand_knowledge_base/brand_knowledge_base.mock.json", "品牌母库 mock"],
        ["02_geo_audit/deepseek_geo_audit_report.mock.md", "DeepSeek 评估 mock"],
        ["02_geo_audit/doubao_geo_audit_report.mock.md", "Doubao 评估 mock"],
        ["03_gap_matrix/geo_gap_matrix.json", "GEO 盲区矩阵"],
        ["04_content_task_plan/content_task_plan.json", "内容任务计划"],
        ["04_content_task_plan/platform_distribution_plan.json", "平台分发计划"],
        ["07_delivery/client_delivery_report.md", "客户交付报告"],
        ["08_monitoring/retest_plan.md", "复测计划"],
    ]
    report = f"""# 西班牙火腿 AI 搜索可见度与 GEO 内容增长交付报告

> 本报告为编排演示，不代表真实模型实测结果。本轮未直接调用 DeepSeek / Doubao 或相邻平台 Skill，所有模型判断均为 mock orchestration demo，用于验证 Orchestrator 是否能形成客户交付包。

## 老板能看懂的 3 句话结论

1. 现在 AI 对西班牙火腿的理解大概率停留在“进口食品、伊比利亚、等级、吃法”这类基础品类知识，但对中国送礼、中式餐饮、青田本地进口产业链和具体购买渠道的回答还不够完整。
2. 最大问题不是“没有内容”，而是缺少能帮助中国用户做决定的内容：送谁、怎么买、多少钱、怎么吃、从哪里买更放心。
3. 接下来 30 天建议先补官网 FAQ 和知乎/头条决策内容，再同步做小红书、抖音体验内容，14 天后复测 AI 是否开始更准确提到送礼、价格渠道和本地化场景。

## 1. 本次 GEO 工作流做了什么

本轮以“西班牙火腿在中国市场”为对象，完成了一次 Orchestrator 编排演示：梳理输入、建立品牌母库 mock、生成双模型评估摘要 mock、输出 GEO Gap Matrix、拆成 19 个内容任务、设计平台分发计划、生成 handoff packets，并整理客户报告和 7 / 14 / 30 天复测计划。

## 2. 当前 AI 对西班牙火腿的认知现状

AI 通常能解释西班牙火腿的基础概念，例如伊比利亚火腿、等级差异、切片和西式搭配。但如果用户问“适不适合送礼”“中式餐桌怎么吃”“青田本地渠道是否靠谱”“价格差异怎么判断”，现有内容容易变得泛泛，难以直接辅助购买。

## 3. DeepSeek / Doubao 评估摘要

- DeepSeek mock 摘要：更适合做结构化解释，但需要补充价格分层、等级说明、渠道可信度和采购决策框架。
- Doubao mock 摘要：更适合大众消费场景，但需要补充小红书/抖音体验内容、中式餐桌场景和礼品场景。
- 共同结论：双模型都需要更多“中文本地化、可引用、可直接回答购买问题”的内容资产。

## 4. 双模型共同盲区

{md_table(["盲区", "商业影响", "推荐内容方向", "目标平台"], gap_rows)}

## 5. 中国本地化场景缺口

当前最值得补的本地化场景有四类：春节/中秋/商务拜访等送礼场景，中式餐桌和家庭聚会场景，青田或浙江本地进口产业链场景，以及餐饮采购和精品超市渠道场景。这些内容越具体，越容易让 AI 从“泛品类介绍”转向“能帮助用户做决定的回答”。

## 6. 内容增长机会

- 官网 FAQ：沉淀价格、保存、选购、渠道、送礼标准答案。
- 知乎：覆盖选购、价格、礼品、青田供应链和餐饮采购等决策问题。
- 今日头条：用老板和家庭用户都能看懂的方式讲场景、避坑和本地渠道。
- 小红书：补开箱、礼盒、摆盘、搭配和真实体验笔记。
- 抖音：补 30 秒口播脚本，让等级、价格、送礼和吃法快速被理解。

## 7. 建议优先发布的内容清单

{md_table(["顺序", "平台", "标题", "预期改善", "发布前确认"], task_rows)}

## 8. 各平台发布建议

{md_table(["平台", "建议", "内容数量", "原因"], route_rows)}

## 9. 30 天执行计划

### 立即执行

- 先确认产品规格、价格区间、渠道证明、配送范围、保存方式和礼盒素材。
- 把 3 个官网 FAQ 先写成标准答案，供官网、客服和后续内容复用。
- 把前 3 个知乎题和前 3 个头条题交给相邻 Skill 或人工团队生成草稿。

### 7 天内

- 发布第一批知乎和今日头条内容。
- 完成小红书开箱笔记和抖音 30 秒选购脚本的素材准备。
- 收集评论和客服问题，补进 FAQ。

### 14 天内

- 复测 DeepSeek / Doubao 对价格、送礼、中式餐饮和青田本地渠道的回答。
- 根据复测结果补第二批内容。

### 30 天内

- 形成官网 FAQ、知乎、头条、小红书、抖音的组合内容矩阵。
- 对比 T0 基线，看品牌/产地/渠道/本地化场景是否被更准确提及。

## 10. 7 / 14 / 30 天复测机制

- T0：记录当前模型对西班牙火腿推荐、价格、渠道、送礼、青田产业链的回答。
- T+7：看已发布内容是否带来用户问题和平台互动。
- T+14：看 AI 回答是否开始出现更具体的送礼、中餐、价格渠道信息。
- T+30：看品牌或本地渠道是否更容易被提及，竞品是否仍然明显领先。

## 11. 本次生成文件清单

{md_table(["文件", "用途"], file_rows)}

## 12. 需要客户补充的资料

- 具体品牌名、产品线、规格和价格区间。
- 西班牙产地、等级、认证、进口和食品合规证明。
- 青田或本地进口产业链资料、仓储配送和服务半径。
- 礼盒图片、开箱图、切片图、餐桌搭配图和短视频素材。
- 客服常见问题、渠道政策和售后说明。

所有内容发布前仍需人工审核。本报告不承诺 AI 排名、收录、转化或模型引用结果。
"""
    write_text(RUN / "07_delivery" / "client_delivery_report.md", report)
    write_text(RUN / "07_delivery" / "delivery_file_index.md", "# Delivery File Index\n\n" + md_table(["文件", "用途"], file_rows))


def create_retest_plan() -> None:
    questions = [
        "西班牙火腿适合送礼吗？",
        "伊比利亚火腿怎么选？",
        "西班牙火腿价格为什么差这么多？",
        "西班牙火腿适合中式餐桌吗？",
        "青田进口西班牙火腿渠道靠谱吗？",
        "小红书上西班牙火腿礼盒怎么选？",
        "餐厅采购西班牙火腿需要注意什么？",
    ]
    text = f"""# 西班牙火腿 GEO 复测计划

## T0 基线检测

在内容发布前，记录 DeepSeek / Doubao 对以下问题的原始回答，作为后续对比基线：

{chr(10).join('- ' + q for q in questions)}

观察指标：

- 品牌 / 产地 / 产业链提及率。
- 推荐排序。
- 回答深度。
- 本地化场景覆盖。
- 购买决策辅助。
- 平台内容是否被模型吸收。
- 竞品是否仍然领先。

## T+7 天第一次复测

重点检查内容是否上线、平台是否有反馈、用户是否提出新问题。

复测问题：

- 西班牙火腿适合送礼吗？
- 西班牙火腿怎么吃更适合中国家庭？
- 西班牙火腿怎么买不踩坑？

判断标准：

- 已发布内容能回答价格、保存、送礼和中式场景。
- 评论和客服问题能反向补充 FAQ。
- 如果没有互动，优先调整标题和开头场景。

## T+14 天第二次复测

重点检查 AI 回答是否开始吸收新内容。

复测问题：

- 伊比利亚火腿怎么选？
- 西班牙火腿价格差异在哪里？
- 青田进口食品渠道和西班牙火腿有什么关系？

判断标准：

- AI 回答是否提到送礼、中式餐饮、价格分层、购买渠道。
- 回答是否从泛泛百科变成可执行建议。
- 如果无改善，补充更结构化的 FAQ、对比表和标准问答。

## T+30 天月度复测

重点检查内容矩阵是否形成 GEO 增长信号。

复测问题：

- 西班牙火腿品牌或礼盒怎么推荐？
- 餐饮采购西班牙火腿怎么选？
- 小红书/抖音上的西班牙火腿内容应该怎么看？

判断标准：

- 品牌、产地、本地进口产业链提及率提升。
- 推荐排序不再只出现泛品类或竞品。
- 回答深度能覆盖等级、价格、渠道、保存、食用和送礼。
- 本地化场景覆盖中国送礼、中式餐饮、青田供应链和餐饮采购。
- 购买决策辅助从“是什么”提升到“怎么买、买哪类、去哪买、适合谁”。
- 平台内容被模型吸收，能复述知乎/头条/FAQ 中的结构化答案。
- 如果竞品仍然领先，下一轮优先做竞品对比文、真实案例和第三方解释内容。

## 如果无改善，下一步怎么调整

- 将 FAQ 改成更明确的问题标题，减少抽象表述。
- 补充价格、规格、渠道和配送事实。
- 增加知乎对比文和今日头条本地化科普文。
- 增加小红书开箱、礼盒场景和抖音口播内容。
- 对仍然被竞品占据的问题，单独生成竞品对比内容。
"""
    write_text(RUN / "08_monitoring" / "retest_plan.md", text)


def create_summary_json(registry: dict, input_data: dict, tasks: list[dict]) -> None:
    stages = [
        ("stage_0_intake", "success", ["examples/spanish_ham_orchestration.md"], ["00_input/spanish_ham_input.json"], "", "完成输入解析。"),
        ("stage_1_brand_knowledge_base", "success", ["00_input/spanish_ham_input.json"], ["01_brand_knowledge_base/brand_knowledge_base.mock.json"], "brand-knowledge-base-builder", "mock artifact generated, handoff packet created."),
        ("stage_2_geo_audit", "success", ["01_brand_knowledge_base/brand_knowledge_base.mock.json"], ["02_geo_audit/deepseek_geo_audit_report.mock.md", "02_geo_audit/doubao_geo_audit_report.mock.md"], "deepseek-geo-audit-skill; doubao-geo-audit-skill", "mock reports generated, not live model results."),
        ("stage_3_gap_matrix", "success", ["02_geo_audit/*.mock.md"], ["03_gap_matrix/geo_gap_matrix.json", "03_gap_matrix/geo_gap_matrix.md"], "", "Generated 7 Spanish ham China-market GEO gaps."),
        ("stage_4_content_task_plan", "success", ["03_gap_matrix/geo_gap_matrix.json"], ["04_content_task_plan/content_task_plan.json", "04_content_task_plan/platform_distribution_plan.json"], "", f"Generated {len(tasks)} content tasks."),
        ("stage_5_content_assets", "success", ["04_content_task_plan/content_task_plan.json"], ["05_content_assets/*.mock.md", "05_content_assets/llms.mock.txt"], "ai-geo-content-generator", "mock assets generated, handoff packet created."),
        ("stage_6_platform_drafts", "partial", ["05_content_assets/*.mock.md"], ["06_platform_drafts/*.mock.md"], "zhihu-geo-draft-assistant; toutiao-geo-draft-assistant", "Platform drafts are mock packets because adjacent Skills were not runtime-called."),
        ("stage_7_delivery", "success", ["all previous outputs"], ["07_delivery/client_delivery_report.md"], "", "Customer-readable report generated."),
        ("stage_8_monitoring", "success", ["07_delivery/client_delivery_report.md"], ["08_monitoring/retest_plan.md"], "", "Retest plan generated."),
    ]
    called = []
    for skill in registry["skills"]:
        status = "recommended_handoff_generated"
        if skill["skill_id"] in {"csdn-geo-draft-publisher", "juejin-geo-draft-publisher", "deepseek-geo-tool"}:
            status = "skipped"
        called.append({
            "skill_id": skill["skill_id"],
            "display_name": skill["display_name"],
            "relative_path": skill["relative_path"],
            "status": status,
            "execution_note": "No real runtime call in this demo; handoff or skip recorded.",
        })

    artifacts = sorted(str(path.relative_to(RUN)) for path in RUN.rglob("*") if path.is_file())
    summary = {
        "run_id": "spanish_ham_demo",
        "execution_mode": "mock_orchestration_demo",
        "target_category": "西班牙火腿",
        "target_market": "中国",
        "industry_type": "食品 / 进口消费品",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "stages": [
            {
                "stage_id": stage_id,
                "status": status,
                "inputs": inputs,
                "outputs": outputs,
                "used_skill": used_skill,
                "notes": notes,
            }
            for stage_id, status, inputs, outputs, used_skill, notes in stages
        ],
        "called_or_recommended_skills": called,
        "failed_or_partial_skills": [
            {
                "skill_id": "zhihu-geo-draft-assistant",
                "status": "partial",
                "reason": "Generated handoff and mock packet; real Skill runtime not called.",
            },
            {
                "skill_id": "toutiao-geo-draft-assistant",
                "status": "partial",
                "reason": "Generated handoff and mock packet; real Skill runtime not called.",
            },
            {
                "skill_id": "xiaohongshu",
                "status": "manual_or_future_skill",
                "reason": "No adjacent 小红书 Skill exists in the local registry.",
            },
            {
                "skill_id": "douyin",
                "status": "manual_or_future_skill",
                "reason": "No adjacent 抖音 Skill exists in the local registry.",
            },
        ],
        "generated_artifacts": artifacts,
        "next_actions": [
            "把 handoff packet 复制到 Brand Knowledge Base Builder，生成真实品牌母库。",
            "用真实品牌母库执行 DeepSeek / Doubao GEO 审计，替换 mock 报告。",
            "根据真实审计刷新 GEO Gap Matrix 和 Content Task Plan。",
            "调用知乎和今日头条草稿 Skill 生成真实平台草稿。",
            "客户补充价格、渠道、规格、资质、图片和配送信息后再发布。",
        ],
        "mock_disclaimer": "This run is a mock orchestration demo and does not represent live DeepSeek or Doubao model results.",
    }
    write_json(RUN / "orchestrator_run_summary.json", summary)


def main() -> int:
    registry = load_registry()
    build_audit_report(registry)
    create_run(registry)
    print(f"generated {RUN}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
