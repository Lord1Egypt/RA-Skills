#!/usr/bin/env python3
"""
1688-item-batch-opt-apply 全局常量

台账与产物落在当前工作目录（AccioWork 会话工作区）下与本技能同名的
1688-item-batch-opt-apply/ 目录内（与 one-click 等其他技能的产物目录隔离）；
本技能通过宿主 MCP 查询实际商品属性，商品写入由外部应用组件完成。
"""

import os
import re

# Skill 名称（供输出文案使用；.env 中的 SKILL_NAME 由平台替换，不在代码里读取）
SKILL_NAME = "1688-item-batch-opt-apply"

# ── 台账与产物路径（均相对当前工作目录）────────────────────────────────────
# 目录名与技能名一致（会话工作区/<技能名>/），与其他技能（如 one-click）的
# 产物目录隔离，避免多技能产物混放或互相覆盖。
LEDGER_DIR_NAME = "1688-item-batch-opt-apply"
LEDGER_FILE_NAME = "tasks.json"

# 台账结构版本（schema 不兼容变更时递增，读取时校验）
LEDGER_VERSION = 1

# 任务来源（台账 source 字段值）：所有输入均由主 Agent 结构化后统一走 context；
# 不再有 excel/folder 通道，脚本不解析任何文件。
SOURCE_CONTEXT = "context"

# ── 任务状态机 ───────────────────────────────────────────────────────────────
# 执行状态：parsed(已解析) → confirmed(已确认执行) / skipped(用户跳过)
#           → running(执行中) → success / failed / cancelled
TASK_STATUSES = ("parsed", "confirmed", "skipped", "running", "success", "failed", "cancelled")

# 应用状态（独立于执行状态，记录写入回执）：
# pending(未申请) → requested(已弹卡待回执) → applied / failed / unknown / cancelled
APPLY_STATUSES = ("pending", "requested", "applied", "failed", "unknown", "cancelled")

# ── 优化项白名单 ─────────────────────────────────────────────────────────────
# op 与执行技能的映射见 references/task-contract.md；此处只做合法性校验与中文标签。
# 标签同时是主 Agent 结构化任务时 op 字段的合法输入（大小写/全半角不敏感，
# 兼容从 Excel 等文件转述而来的中文列值）。
OP_LABELS = {
    "title_opt": "标题优化",
    "main_img_opt": "主图优化",
    "white_img_opt": "白底图",
    "img_opt": "图片优化",
    "bg_change": "背景替换",
    "carousel_opt": "副图轮播图",
    "detail_img_opt": "详情图",
    "full_img_set": "一套主图",
    "full_listing_set": "全套上架图",
    "multi_img_merge": "多图合成",
}

# 「优化项」列的常见别名 → op（解析时归一化）
OP_ALIASES = {
    "标题": "title_opt",
    "优化标题": "title_opt",
    "标题优化": "title_opt",
    "主图": "main_img_opt",
    "优化主图": "main_img_opt",
    "主图优化": "main_img_opt",
    "白底": "white_img_opt",
    "白底图": "white_img_opt",
    "抠图": "white_img_opt",
    "图片优化": "img_opt",
    "一键优化": "img_opt",
    "修图": "img_opt",
    "换背景": "bg_change",
    "背景替换": "bg_change",
    "副图": "carousel_opt",
    "轮播图": "carousel_opt",
    "副图轮播图": "carousel_opt",
    "详情图": "detail_img_opt",
    "一套主图": "full_img_set",
    "套图": "full_img_set",
    "全套上架图": "full_listing_set",
    "上架图": "full_listing_set",
    "多图合成": "multi_img_merge",
    "图片合成": "multi_img_merge",
    "多图融合": "multi_img_merge",
    "融合": "multi_img_merge",
    "合成": "multi_img_merge",
}



def ledger_dir(base_dir: str = None) -> str:
    """台账目录。默认当前工作目录，可用 base_dir 显式指定（如会话工作区根）。"""
    root = base_dir or os.getcwd()
    return os.path.join(root, LEDGER_DIR_NAME)


def store_file_prefix(store_name: str) -> str:
    """店铺展示名 → 产物文件名前缀。

    店铺名由主 Agent 从宿主店铺上下文/选店结果（phoenix-pc 多店铺策略侧）
    取得并经 parse_tasks --store_name 写入台账；仅用于产物文件名前缀
    （归档台账 tasks_<店铺>_<旧批次ID>.json、导出 批量任务结果_<店铺>_<批次ID>），
    避免多店铺同会话运行时产物文件名重叠；不参与鉴权。
    非法字符与空白转下划线、限长 20；清洗后为空（未传/全非法字符）时返回
    空串，调用方拼名时不加前缀（与旧版无前缀命名兼容）。
    """
    cleaned = re.sub(r"[\\/:*?\"<>|\s'`]+", "_", str(store_name or "").strip())
    return cleaned[:20].strip("_")


def ledger_file(base_dir: str = None) -> str:
    return os.path.join(ledger_dir(base_dir), LEDGER_FILE_NAME)
