#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""marketing_polish.py - Thin wrapper re-exporting from mcps/shared (dedup R75.5)

R75.5 Skill去重: skills/content-template/scripts/marketing_polish.py 已统一到
mcps/shared/marketing_polish.py(权威源)。本文件仅保留向后兼容入口。
来源: 09设计文档U11 + R56迁移(从_lazy迁至mcps/shared) + R75.5去重

调用方式不变:
  python marketing_polish.py --action polish --content "..." --tone enthusiastic
  python marketing_polish.py --action rewrite --content "..." --tone restrained
  python marketing_polish.py --action full_process --content "..." --tone conversion

所有函数/常量从 mcps/shared/marketing_polish.py 重导出,保持向后兼容。
"""
import sys
from pathlib import Path

# 添加项目根到sys.path以支持mcps.shared导入
# skills/content-template/scripts/marketing_polish.py → 上溯4级到项目根(d:\JueJin)
# parents[0]=scripts/ parents[1]=content-template/ parents[2]=skills/ parents[3]=d:\JueJin
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

# 从权威源统一导入(R75.5: Skill去重,消除复制粘贴)
# mcps/shared/marketing_polish.py 是唯一权威实现,包含:
# - DEF-U49 P3: style_fingerprint 智能调整tone
# - v2.0: 去重逻辑+日期感知注入
# - 正确的路径层级(R56修复)
from mcps.shared.marketing_polish import (  # noqa: E402
    # 配置常量
    COPYWRITING_CONFIG_PATH,
    USAGE_HISTORY_PATH,
    PROHIBITED_WORDS,
    PROHIBITED_REPLACEMENTS,
    DIVERSITY_CFG,
    TONE_TEMPLATES,
    TRANSITION_WORDS,
    AI_FLAVOR_PATTERNS,
    # 四步法函数
    step1_extract_info,
    step2_optimize_structure,
    step3_inject_tone,
    step4_compliance_check,
    polish_four_steps,
    # 语气改写函数
    rewrite_tone,
    full_process,
    # 模板选择函数
    select_emotional_hook,
    select_narrative_template,
    select_cta_template,
    # CLI入口
    main,
)

# 显式声明 __all__ 以明确公开API(从权威源继承)
__all__ = [
    "COPYWRITING_CONFIG_PATH", "USAGE_HISTORY_PATH",
    "PROHIBITED_WORDS", "PROHIBITED_REPLACEMENTS", "DIVERSITY_CFG",
    "TONE_TEMPLATES", "TRANSITION_WORDS", "AI_FLAVOR_PATTERNS",
    "step1_extract_info", "step2_optimize_structure",
    "step3_inject_tone", "step4_compliance_check",
    "polish_four_steps", "rewrite_tone", "full_process",
    "select_emotional_hook", "select_narrative_template", "select_cta_template",
    "main",
]


if __name__ == "__main__":
    main()
