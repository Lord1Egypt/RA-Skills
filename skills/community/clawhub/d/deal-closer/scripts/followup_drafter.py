#!/usr/bin/env python3
"""
deal-closer AI 跟进邮件起草模块（付费功能）

根据商机历史和最近交互，生成上下文相关的跟进邮件草稿。
支持多种模板、定时提醒和待办列表。
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from utils import (
    check_subscription,
    generate_id,
    get_data_file,
    load_input_data,
    now_iso,
    today_str,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    require_paid_feature,
    write_json_file,
    format_currency,
    calculate_days_since,
    days_until,
    mask_email,
    DEAL_STAGES,
    FOLLOWUP_TEMPLATES,
)

# 延迟导入 IMAP 和学习模块
_imap_module = None
_learning_module = None


def _get_imap_module():
    """延迟加载 imap_email 模块。"""
    global _imap_module
    if _imap_module is None:
        try:
            import imap_email as _mod
            _imap_module = _mod
        except ImportError:
            _imap_module = False
    return _imap_module if _imap_module is not False else None


def _get_learning_module():
    """延迟加载 learning_engine 模块。"""
    global _learning_module
    if _learning_module is None:
        try:
            import learning_engine as _mod
            _learning_module = _mod
        except ImportError:
            _learning_module = False
    return _learning_module if _learning_module is not False else None


# ============================================================
# 数据文件
# ============================================================

FOLLOWUPS_FILE = "followups.json"
DEALS_FILE = "deals.json"
MEETINGS_FILE = "meetings.json"
EMAILS_FILE = "emails.json"


def _get_followups() -> List[Dict[str, Any]]:
    """读取所有跟进任务。"""
    return read_json_file(get_data_file(FOLLOWUPS_FILE))


def _save_followups(followups: List[Dict[str, Any]]) -> None:
    """保存跟进任务到文件。"""
    write_json_file(get_data_file(FOLLOWUPS_FILE), followups)


def _get_deals() -> List[Dict[str, Any]]:
    """读取所有商机数据。"""
    return read_json_file(get_data_file(DEALS_FILE))


def _get_meetings() -> List[Dict[str, Any]]:
    """读取所有会议记录。"""
    return read_json_file(get_data_file(MEETINGS_FILE))


def _get_emails() -> List[Dict[str, Any]]:
    """读取所有邮件记录。"""
    return read_json_file(get_data_file(EMAILS_FILE))


# ============================================================
# 邮件模板
# ============================================================

_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "introduction": {
        "name": "初次介绍",
        "description": "首次接触客户，介绍公司和产品",
        "subject_template": "您好，{contact_name} — 关于{company_or_product}的合作机会",
        "body_template": (
            "{contact_name}您好，\n\n"
            "感谢您对我们的关注。我是{sender_name}，负责{product_area}业务。\n\n"
            "了解到贵公司在{industry_or_need}方面有需求，我们的解决方案在此领域有丰富的经验"
            "和成功案例。\n\n"
            "希望能与您进一步沟通，了解贵公司的具体需求，为您提供针对性的方案。\n\n"
            "请问您本周是否方便安排一次简短的交流？\n\n"
            "期待您的回复。\n\n"
            "此致\n{sender_name}"
        ),
    },
    "proposal_followup": {
        "name": "方案跟进",
        "description": "发送方案后的跟进",
        "subject_template": "关于{deal_name}方案的跟进",
        "body_template": (
            "{contact_name}您好，\n\n"
            "上次为您发送了{deal_name}的详细方案，不知您是否有时间查阅？\n\n"
            "如有任何疑问或需要调整的地方，我很乐意为您详细解答。\n\n"
            "该方案的核心优势包括：\n"
            "- 针对贵公司需求的定制化设计\n"
            "- 具有竞争力的价格方案\n"
            "- 完善的售后服务体系\n\n"
            "期待您的反馈，我们可以进一步讨论细节。\n\n"
            "此致\n{sender_name}"
        ),
    },
    "negotiation": {
        "name": "商务谈判",
        "description": "商务谈判阶段的跟进",
        "subject_template": "关于{deal_name}合作条款的确认",
        "body_template": (
            "{contact_name}您好，\n\n"
            "感谢您在上次会谈中的深入交流。根据讨论的结果，我已整理了以下要点：\n\n"
            "{meeting_summary}\n\n"
            "关于价格和交付条款，我们愿意在以下方面做出灵活安排，以促成双方的合作。\n\n"
            "如您方便，我们可以安排下一次沟通，具体讨论合同细节。\n\n"
            "此致\n{sender_name}"
        ),
    },
    "closing": {
        "name": "促成签约",
        "description": "推进签约的跟进",
        "subject_template": "关于{deal_name}合同签署事宜",
        "body_template": (
            "{contact_name}您好，\n\n"
            "经过前期的充分沟通，我们对双方的合作充满信心。\n\n"
            "附件中是最终版合同，已根据您上次提出的意见做了调整。"
            "主要变更包括：\n"
            "{contract_changes}\n\n"
            "如无异议，烦请您签署后返回，我们将在收到合同后立即启动项目。\n\n"
            "如有任何问题，请随时联系我。\n\n"
            "此致\n{sender_name}"
        ),
    },
    "win_back": {
        "name": "赢回客户",
        "description": "针对流失客户的重新激活",
        "subject_template": "{contact_name}，我们有了新的方案想与您分享",
        "body_template": (
            "{contact_name}您好，\n\n"
            "距离我们上次沟通已经有一段时间了。\n\n"
            "我们最近对产品进行了重大升级，新增了以下功能：\n"
            "{new_features}\n\n"
            "这些改进正好可以解决您之前提到的顾虑。\n\n"
            "如果您有兴趣了解更多，我非常乐意为您安排一次演示。"
            "另外，针对老客户我们也准备了特别优惠方案。\n\n"
            "期待与您重新建立联系。\n\n"
            "此致\n{sender_name}"
        ),
    },
}


# ============================================================
# 操作函数
# ============================================================

def draft_followup(data: Dict[str, Any]) -> None:
    """起草跟进邮件。

    必填字段: deal_id
    可选字段: template（模板类型）, sender_name, custom_notes

    Args:
        data: 参数字典。
    """
    if not require_paid_feature("ai_followup", "AI跟进邮件"):
        return

    deal_id = data.get("deal_id")
    if not deal_id:
        output_error("商机ID（deal_id）为必填字段", code="VALIDATION_ERROR")
        return

    # 加载商机
    deals = _get_deals()
    target_deal = None
    for d in deals:
        if d.get("id") == deal_id:
            target_deal = d
            break

    if not target_deal:
        output_error(f"未找到ID为 {deal_id} 的商机", code="NOT_FOUND")
        return

    # 确定模板
    template_key = data.get("template", "")
    if not template_key:
        # 根据商机阶段自动选择模板
        stage = target_deal.get("stage", "")
        stage_template_map = {
            "线索": "introduction",
            "初步接触": "introduction",
            "需求确认": "proposal_followup",
            "方案报价": "proposal_followup",
            "商务谈判": "negotiation",
            "合同签署": "closing",
            "流失": "win_back",
        }
        template_key = stage_template_map.get(stage, "proposal_followup")

    if template_key not in _TEMPLATES:
        valid = "、".join(_TEMPLATES.keys())
        output_error(f"未知模板: {template_key}，可用模板: {valid}", code="VALIDATION_ERROR")
        return

    template = _TEMPLATES[template_key]
    sender_name = data.get("sender_name", "销售顾问")

    # 获取最近会议摘要
    meetings = _get_meetings()
    deal_meetings = [m for m in meetings if m.get("deal_id") == deal_id]
    deal_meetings.sort(key=lambda m: m.get("date", ""), reverse=True)

    meeting_summary = "（暂无会议记录）"
    if deal_meetings:
        latest = deal_meetings[0]
        notes = latest.get("notes", "")
        action_items = latest.get("action_items", [])
        if notes or action_items:
            parts = []
            if notes:
                parts.append(f"会议纪要: {notes}")
            if action_items:
                parts.append("行动项: " + "；".join(action_items))
            meeting_summary = "\n".join(parts)

    # 获取最近邮件
    emails = _get_emails()
    deal_emails = [e for e in emails if e.get("linked_deal_id") == deal_id]
    deal_emails.sort(key=lambda e: e.get("date", ""), reverse=True)

    last_email_info = ""
    if deal_emails:
        latest_email = deal_emails[0]
        last_email_info = f"最近邮件主题: {latest_email.get('subject', '')}"

    # 填充模板变量
    variables = {
        "contact_name": target_deal.get("contact_name", "客户"),
        "company_or_product": target_deal.get("company", "") or target_deal.get("name", ""),
        "deal_name": target_deal.get("name", ""),
        "sender_name": sender_name,
        "product_area": "解决方案",
        "industry_or_need": target_deal.get("notes", "相关领域"),
        "meeting_summary": meeting_summary,
        "contract_changes": data.get("contract_changes", "- 根据双方协商结果调整了相关条款"),
        "new_features": data.get("new_features", "- 性能提升\n- 新增定制化功能\n- 优化用户体验"),
    }

    subject = template["subject_template"]
    body = template["body_template"]

    for key, value in variables.items():
        placeholder = "{" + key + "}"
        subject = subject.replace(placeholder, str(value))
        body = body.replace(placeholder, str(value))

    # 添加上下文信息
    context_info = []
    context_info.append(f"商机阶段: {target_deal.get('stage', '')}")
    context_info.append(f"商机金额: {format_currency(target_deal.get('amount', 0))}")
    if target_deal.get("expected_close_date"):
        context_info.append(f"预计成交: {target_deal['expected_close_date']}")
    if last_email_info:
        context_info.append(last_email_info)
    if deal_meetings:
        context_info.append(f"最近会议: {deal_meetings[0].get('date', '')}")

    custom_notes = data.get("custom_notes", "")

    output_success({
        "template": template_key,
        "template_name": template["name"],
        "subject": subject,
        "body": body,
        "context": context_info,
        "custom_notes": custom_notes,
        "deal_id": deal_id,
        "deal_name": target_deal.get("name", ""),
        "contact_email": mask_email(target_deal.get("contact_email", "")),
    })


def list_templates(data: Optional[Dict[str, Any]] = None) -> None:
    """列出所有可用的跟进邮件模板。

    Args:
        data: 未使用，保留接口一致性。
    """
    templates = []
    for key, tmpl in _TEMPLATES.items():
        templates.append({
            "key": key,
            "name": tmpl["name"],
            "description": tmpl["description"],
            "subject_preview": tmpl["subject_template"],
        })

    output_success({
        "total": len(templates),
        "templates": templates,
    })


def schedule_followup(data: Dict[str, Any]) -> None:
    """创建跟进提醒计划。

    必填字段: deal_id, scheduled_date
    可选字段: template, notes, priority

    Args:
        data: 参数字典。
    """
    if not require_paid_feature("ai_followup", "跟进计划"):
        return

    deal_id = data.get("deal_id")
    if not deal_id:
        output_error("商机ID（deal_id）为必填字段", code="VALIDATION_ERROR")
        return

    scheduled_date = data.get("scheduled_date")
    if not scheduled_date:
        output_error("计划日期（scheduled_date）为必填字段", code="VALIDATION_ERROR")
        return

    # 验证商机存在
    deals = _get_deals()
    target_deal = None
    for d in deals:
        if d.get("id") == deal_id:
            target_deal = d
            break

    if not target_deal:
        output_error(f"未找到ID为 {deal_id} 的商机", code="NOT_FOUND")
        return

    # 优先级校验
    priority = data.get("priority", "normal")
    if priority not in ("low", "normal", "high", "urgent"):
        priority = "normal"

    template_key = data.get("template", "")
    if template_key and template_key not in _TEMPLATES:
        valid = "、".join(_TEMPLATES.keys())
        output_error(f"未知模板: {template_key}，可用模板: {valid}", code="VALIDATION_ERROR")
        return

    followup = {
        "id": generate_id("F"),
        "deal_id": deal_id,
        "deal_name": target_deal.get("name", ""),
        "scheduled_date": scheduled_date,
        "template": template_key,
        "notes": data.get("notes", ""),
        "priority": priority,
        "status": "pending",
        "created_at": now_iso(),
    }

    followups = _get_followups()
    followups.append(followup)
    _save_followups(followups)

    output_success({
        "message": f"跟进计划已创建（{scheduled_date}，商机: {target_deal.get('name', '')}）",
        "followup": followup,
    })


def list_pending(data: Optional[Dict[str, Any]] = None) -> None:
    """列出待处理的跟进任务。

    按紧急程度和日期排序，优先显示最紧急的。

    Args:
        data: 可选参数，支持 deal_id、status 过滤。
    """
    if not require_paid_feature("ai_followup", "跟进列表"):
        return

    followups = _get_followups()

    if data:
        # 按商机过滤
        deal_id = data.get("deal_id")
        if deal_id:
            followups = [f for f in followups if f.get("deal_id") == deal_id]

        # 按状态过滤
        status = data.get("status")
        if status:
            followups = [f for f in followups if f.get("status") == status]
    else:
        # 默认只显示待处理
        followups = [f for f in followups if f.get("status") == "pending"]

    # 优先级权重
    priority_weight = {
        "urgent": 0,
        "high": 1,
        "normal": 2,
        "low": 3,
    }

    today = today_str()

    # 计算紧急度并排序
    for f in followups:
        f["_priority_weight"] = priority_weight.get(f.get("priority", "normal"), 2)
        scheduled = f.get("scheduled_date", "")
        if scheduled:
            f["days_remaining"] = days_until(scheduled)
            f["is_overdue"] = scheduled < today
        else:
            f["days_remaining"] = 999
            f["is_overdue"] = False

    # 先按是否逾期、再按优先级、最后按日期排序
    followups.sort(key=lambda f: (
        not f.get("is_overdue", False),
        f.get("_priority_weight", 2),
        f.get("scheduled_date", ""),
    ))

    # 清理临时字段
    display_list = []
    for f in followups:
        display = dict(f)
        display.pop("_priority_weight", None)
        display_list.append(display)

    # 统计
    overdue = sum(1 for f in display_list if f.get("is_overdue"))
    today_count = sum(1 for f in display_list if f.get("scheduled_date") == today)

    output_success({
        "total": len(display_list),
        "overdue": overdue,
        "today": today_count,
        "followups": display_list,
    })


def send_draft(data: Dict[str, Any]) -> None:
    """通过 IMAP/SMTP 直接发送已起草的跟进邮件。

    必填字段: deal_id, subject, body
    可选字段: template（用于学习记录）

    Args:
        data: 参数字典。
    """
    if not require_paid_feature("ai_followup", "SMTP邮件发送"):
        return

    imap_mod = _get_imap_module()
    if imap_mod is None:
        output_error(
            "IMAP/SMTP 模块未加载，请确认 imap_email.py 存在",
            code="MODULE_ERROR",
        )
        return

    deal_id = data.get("deal_id")
    if not deal_id:
        output_error("商机ID（deal_id）为必填字段", code="VALIDATION_ERROR")
        return

    # 获取商机联系人邮箱
    deals = _get_deals()
    target_deal = None
    for d in deals:
        if d.get("id") == deal_id:
            target_deal = d
            break

    if not target_deal:
        output_error(f"未找到ID为 {deal_id} 的商机", code="NOT_FOUND")
        return

    to_addr = data.get("to", target_deal.get("contact_email", ""))
    if not to_addr:
        output_error("未找到收件人邮箱，请提供 to 字段或确保商机有联系人邮箱", code="VALIDATION_ERROR")
        return

    subject = data.get("subject", "")
    body = data.get("body", "")

    if not subject or not body:
        output_error("subject 和 body 为必填字段", code="VALIDATION_ERROR")
        return

    # 调用 imap_email 的发送功能
    send_data = {"to": to_addr, "subject": subject, "body": body}
    cc = data.get("cc", "")
    if cc:
        send_data["cc"] = cc

    imap_mod.send_email(send_data)

    # 记录发送到学习引擎
    _record_followup_sent(deal_id, data.get("template", ""), target_deal)


def _record_followup_sent(deal_id: str, template: str, deal: Dict[str, Any]) -> None:
    """记录跟进邮件发送到学习引擎。

    Args:
        deal_id: 商机ID。
        template: 使用的模板。
        deal: 商机数据。
    """
    learning_mod = _get_learning_module()
    if learning_mod is None:
        return

    try:
        learning_data = learning_mod._get_learning_data()
        patterns = learning_data.get("patterns", [])

        pattern = {
            "id": generate_id("LP"),
            "category": "followup",
            "description": (
                f"通过SMTP发送跟进邮件，商机「{deal.get('name', '')}」，"
                f"阶段: {deal.get('stage', '')}，模板: {template or '自定义'}"
            ),
            "success_rate": 0.5,  # 初始成功率，后续根据回复情况更新
            "applicable_stages": [deal.get("stage", "")],
            "notes": f"deal_id: {deal_id}",
            "recorded_at": now_iso(),
        }
        patterns.append(pattern)
        learning_data["patterns"] = patterns
        learning_mod._save_learning_data(learning_data)
    except Exception:
        pass


def auto_draft(data: Optional[Dict[str, Any]] = None) -> None:
    """主动为停滞商机起草跟进邮件。

    自动识别超过指定天数未更新的活跃商机，并生成跟进邮件草稿。

    可选字段: stale_days（停滞天数阈值，默认 7）、max_drafts（最大草稿数，默认 5）

    Args:
        data: 可选参数。
    """
    if not require_paid_feature("ai_followup", "自动跟进起草"):
        return

    data = data or {}
    stale_days = int(data.get("stale_days", 7))
    max_drafts = int(data.get("max_drafts", 5))

    deals = _get_deals()
    active_deals = [
        d for d in deals
        if d.get("stage") not in ("成交", "流失")
    ]

    if not active_deals:
        output_error("暂无活跃商机", code="NO_DATA")
        return

    # 筛选停滞商机
    stale_deals = []
    for deal in active_deals:
        updated = deal.get("updated_at", "")
        if updated:
            days = calculate_days_since(updated)
            if days >= stale_days:
                stale_deals.append((deal, days))

    if not stale_deals:
        output_success({
            "message": f"没有超过 {stale_days} 天未更新的商机，管道状态良好",
            "drafts": [],
            "total": 0,
        })
        return

    # 按停滞时间排序
    stale_deals.sort(key=lambda x: x[1], reverse=True)
    stale_deals = stale_deals[:max_drafts]

    drafts = []
    for deal, days_stale in stale_deals:
        stage = deal.get("stage", "")
        # 根据阶段选择模板
        stage_template_map = {
            "线索": "introduction",
            "初步接触": "introduction",
            "需求确认": "proposal_followup",
            "方案报价": "proposal_followup",
            "商务谈判": "negotiation",
            "合同签署": "closing",
        }
        template_key = stage_template_map.get(stage, "proposal_followup")

        if template_key not in _TEMPLATES:
            template_key = "proposal_followup"

        template = _TEMPLATES[template_key]

        # 简单填充模板
        variables = {
            "contact_name": deal.get("contact_name", "客户"),
            "company_or_product": deal.get("company", "") or deal.get("name", ""),
            "deal_name": deal.get("name", ""),
            "sender_name": "销售顾问",
            "product_area": "解决方案",
            "industry_or_need": deal.get("notes", "相关领域"),
            "meeting_summary": "（自动生成草稿）",
            "contract_changes": "- 根据协商结果调整",
            "new_features": "- 产品更新内容",
        }

        subject = template["subject_template"]
        body = template["body_template"]
        for key, value in variables.items():
            placeholder = "{" + key + "}"
            subject = subject.replace(placeholder, str(value))
            body = body.replace(placeholder, str(value))

        drafts.append({
            "deal_id": deal.get("id", ""),
            "deal_name": deal.get("name", ""),
            "stage": stage,
            "days_stale": days_stale,
            "template": template_key,
            "subject": subject,
            "body": body,
            "contact_email": mask_email(deal.get("contact_email", "")),
            "reason": f"已 {days_stale} 天未更新",
        })

    output_success({
        "message": f"已为 {len(drafts)} 个停滞商机生成跟进草稿",
        "total": len(drafts),
        "stale_threshold_days": stale_days,
        "drafts": drafts,
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("deal-closer AI跟进邮件")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "draft": lambda: draft_followup(data or {}),
        "templates": lambda: list_templates(data),
        "schedule": lambda: schedule_followup(data or {}),
        "list-pending": lambda: list_pending(data),
        "send": lambda: send_draft(data or {}),
        "auto-draft": lambda: auto_draft(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
