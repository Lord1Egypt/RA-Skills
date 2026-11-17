"""品牌知识库管理脚本 - 支持品牌创建/查询/一致性检查/切换/列表"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[4] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger
logger = get_logger("_lazy", source="skills/_lazy/brand-knowledge/scripts/brand_manager.py")
from mcps.shared.atomic_write import atomic_read_json, safe_read_json, atomic_write_json

# 品牌数据目录
DATA_DIR = Path(os.environ.get("BRAND_DATA_DIR", "data/brands"))
ACTIVE_BRAND_FILE = DATA_DIR / "active_brand.json"
BRAND_TONES = ["专业", "活泼", "温暖", "高端"]


def _ensure_data_dir() -> None:
    """确保品牌数据目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _brand_id_from_name(name: str) -> str:
    """品牌名转brand_id(kebab-case)"""
    return name.lower().replace(" ", "-").replace("_", "-")


def _load_brand(brand_id: str) -> dict[str, Any] | None:
    """加载品牌档案，不存在返回None"""
    path = DATA_DIR / f"{brand_id}.json"
    if not path.exists():
        return None
    return atomic_read_json(path, {})


def _save_brand(brand_data: dict[str, Any]) -> None:
    """保存品牌档案到JSON文件"""
    path = DATA_DIR / f"{brand_data['brand_id']}.json"
    atomic_write_json(path, brand_data, indent=2, ensure_ascii=False)


def _load_active_brand() -> str | None:
    """加载当前活跃品牌名"""
    if not ACTIVE_BRAND_FILE.exists():
        return None
    data = atomic_read_json(ACTIVE_BRAND_FILE, {})
    return data.get("active_brand")


def _save_active_brand(brand_name: str) -> None:
    """保存当前活跃品牌"""
    atomic_write_json(ACTIVE_BRAND_FILE, {"active_brand": brand_name, "updated_at": datetime.now().isoformat()}, indent=2, ensure_ascii=False)


def cmd_create(args: argparse.Namespace) -> None:
    """创建品牌档案"""
    try:
        _ensure_data_dir()
        brand_id = _brand_id_from_name(args.name)
        # 检查品牌是否已存在
        if _load_brand(brand_id):
            print(json.dumps({"success": False, "data": {}, "error": f"品牌'{args.name}'已存在，请使用update或换名", "code": "BRAND_EXISTS"}, ensure_ascii=False))
            return
        # 验证调性
        if args.tone not in BRAND_TONES:
            print(json.dumps({"success": False, "data": {}, "error": f"调性值非法，合法值: {BRAND_TONES}", "code": "INVALID_TONE"}, ensure_ascii=False))
            return
        # 构建品牌档案
        brand_data: dict[str, Any] = {
            "brand_id": brand_id,
            "name": args.name,
            "slogan": args.slogan or "",
            "story": args.story or "",
            "tone": args.tone,
            "target_audience": args.target_audience or "",
            "visual": {
                "primary_color": args.primary_color or "#000000",
                "secondary_color": args.secondary_color or "#FFFFFF",
                "font": args.font or "",
                "logo_description": args.logo_description or ""
            },
            "templates": {
                "presale": args.presale or "",
                "aftersale": args.aftersale or "",
                "promo": args.promo or ""
            },
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        _save_brand(brand_data)
        # 尝试同步向量库(降级处理)
        qdrant_status = "not_synced"
        try:
            # 向量库同步: 通过memory-qdrant MCP调用
            # 当前为降级模式,仅保存JSON,向量索引自下次MCP可用时同步
            qdrant_status = "pending_sync"
        except Exception as e:
            logger.error(f"[brand_manager] 向量库同步异常: {e}")
            qdrant_status = "fallback_json_only"
        print(json.dumps({
            "success": True,
            "data": {"brand_id": brand_id, "name": args.name, "slogan": args.slogan, "tone": args.tone, "qdrant_status": qdrant_status, "created_at": brand_data["created_at"]},
            "error": None, "code": None
        }, ensure_ascii=False))
    except Exception as e:
        logger.error(f"brand manager异常: {e}", exc_info=True)
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "IO_ERROR"}, ensure_ascii=False))
        sys.exit(2)


def cmd_query(args: argparse.Namespace) -> None:
    """查询品牌档案"""
    try:
        brand_id = _brand_id_from_name(args.keyword)
        brand = _load_brand(brand_id)
        # 精确匹配失败时模糊搜索
        if not brand:
            for f in DATA_DIR.glob("*.json"):
                if f.name == "active_brand.json":
                    continue
                data = atomic_read_json(f, {})
                if args.keyword.lower() in data.get("name", "").lower() or args.keyword.lower() in data.get("slogan", "").lower():
                    brand = data
                    break
        if not brand:
            print(json.dumps({"success": False, "data": {}, "error": f"品牌'{args.keyword}'不存在，请先创建", "code": "BRAND_NOT_FOUND"}, ensure_ascii=False))
            return
        print(json.dumps({
            "success": True,
            "data": {"tone": brand["tone"], "visual": brand.get("visual", {}), "templates": brand.get("templates", {}), "name": brand["name"]},
            "error": None, "code": None
        }, ensure_ascii=False))
    except Exception as e:
        logger.error(f"brand manager异常: {e}", exc_info=True)
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "IO_ERROR"}, ensure_ascii=False))
        sys.exit(2)


def cmd_check(args: argparse.Namespace) -> None:
    """品牌一致性检查"""
    try:
        brand_id = _brand_id_from_name(args.brand)
        brand = _load_brand(brand_id)
        if not brand:
            print(json.dumps({"success": False, "data": {}, "error": f"品牌'{args.brand}'不存在，请先创建", "code": "BRAND_NOT_FOUND"}, ensure_ascii=False))
            return
        content = args.content
        violations: list[dict[str, str]] = []
        tone = brand.get("tone", "")
        templates = brand.get("templates", {})
        # 调性检查(40分): 简单关键词匹配
        tone_score = 40
        casual_words = ["哈喽", "亲", "超便宜", "快来抢", "随便", "凑合"]
        formal_words = ["专业", "保障", "服务", "品质", "信赖", "定制"]
        if tone == "专业":
            if any(w in content for w in casual_words):
                tone_score = 10
                violations.append({"category": "调性不匹配", "detail": f"内容语气过于随意，品牌调性为'{tone}'", "suggestion": "改用正式商务用语"})
            elif any(w in content for w in formal_words):
                tone_score = 40
        elif tone == "活泼":
            if any(w in content for w in formal_words) and not any(w in content for w in casual_words):
                tone_score = 20
                violations.append({"category": "调性不匹配", "detail": f"内容语气过于正式，品牌调性为'{tone}'", "suggestion": "改用轻松活泼用语"})
        # 话术模板检查(30分)
        template_score = 30
        brand_name = brand.get("name", "")
        if brand_name and brand_name not in content:
            template_score = 10
            violations.append({"category": "话术模板不匹配", "detail": "未提及品牌名", "suggestion": f"参考模板: '{templates.get('presale', '')}'"})
        # 视觉规范检查(30分): 检查是否提及品牌主色相关描述
        visual_score = 30
        visual = brand.get("visual", {})
        primary = visual.get("primary_color", "")
        if primary and ("红" in content and "蓝" in primary) or ("绿" in content and "红" in primary):
            visual_score = 15
            violations.append({"category": "视觉规范不匹配", "detail": "内容色彩描述与品牌主色冲突", "suggestion": f"品牌主色为{primary}"})
        score = tone_score + template_score + visual_score
        compliant = score >= 60
        if not compliant:
            violations.insert(0, {"category": "合规度不足", "detail": f"评分{score}分，低于60分阈值", "suggestion": "请根据以下不合规项修改内容"})
        print(json.dumps({
            "success": True,
            "data": {"score": score, "compliant": compliant, "violations": violations},
            "error": None, "code": None
        }, ensure_ascii=False))
    except Exception as e:
        logger.error(f"brand manager异常: {e}", exc_info=True)
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "IO_ERROR"}, ensure_ascii=False))
        sys.exit(2)


def cmd_switch(args: argparse.Namespace) -> None:
    """切换活跃品牌"""
    try:
        _ensure_data_dir()
        brand_id = _brand_id_from_name(args.brand)
        brand = _load_brand(brand_id)
        if not brand:
            print(json.dumps({"success": False, "data": {}, "error": f"品牌'{args.brand}'不存在，请先创建", "code": "BRAND_NOT_FOUND"}, ensure_ascii=False))
            return
        _save_active_brand(args.brand)
        print(json.dumps({
            "success": True,
            "data": {"active_brand": args.brand, "tone": brand["tone"], "slogan": brand.get("slogan", "")},
            "error": None, "code": None
        }, ensure_ascii=False))
    except Exception as e:
        logger.error(f"brand manager异常: {e}", exc_info=True)
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "IO_ERROR"}, ensure_ascii=False))
        sys.exit(2)


def cmd_list(args: argparse.Namespace) -> None:
    """列出所有品牌"""
    try:
        _ensure_data_dir()
        brands: list[dict[str, str]] = []
        for f in DATA_DIR.glob("*.json"):
            if f.name == "active_brand.json":
                continue
            data = atomic_read_json(f, {})
            brands.append({"brand_id": data.get("brand_id", ""), "name": data.get("name", ""), "tone": data.get("tone", "")})
        active = _load_active_brand()
        print(json.dumps({
            "success": True,
            "data": {"brands": brands, "active_brand": active, "total": len(brands)},
            "error": None, "code": None
        }, ensure_ascii=False))
    except Exception as e:
        logger.error(f"brand manager异常: {e}", exc_info=True)
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "IO_ERROR"}, ensure_ascii=False))
        sys.exit(2)


def main() -> None:
    """主入口: 解析子命令并执行"""
    parser = argparse.ArgumentParser(description="品牌知识库管理工具")
    sub = parser.add_subparsers(dest="command")
    # create子命令
    p_create = sub.add_parser("create", help="创建品牌档案")
    p_create.add_argument("--name", required=True, help="品牌名")
    p_create.add_argument("--slogan", default="", help="品牌Slogan")
    p_create.add_argument("--story", default="", help="品牌故事")
    p_create.add_argument("--tone", required=True, help="品牌调性(专业/活泼/温暖/高端)")
    p_create.add_argument("--target-audience", default="", help="目标人群")
    p_create.add_argument("--primary-color", default="#000000", help="主色HEX")
    p_create.add_argument("--secondary-color", default="#FFFFFF", help="辅色HEX")
    p_create.add_argument("--font", default="", help="字体")
    p_create.add_argument("--logo-description", default="", help="Logo描述")
    p_create.add_argument("--presale", default="", help="售前话术模板")
    p_create.add_argument("--aftersale", default="", help="售后话术模板")
    p_create.add_argument("--promo", default="", help="推广话术模板")
    # query子命令
    p_query = sub.add_parser("query", help="查询品牌档案")
    p_query.add_argument("--keyword", required=True, help="品牌名或关键词")
    # check子命令
    p_check = sub.add_parser("check", help="品牌一致性检查")
    p_check.add_argument("--brand", required=True, help="目标品牌名")
    p_check.add_argument("--content", required=True, help="待检查内容")
    # switch子命令
    p_switch = sub.add_parser("switch", help="切换活跃品牌")
    p_switch.add_argument("--brand", required=True, help="目标品牌名")
    # list子命令
    sub.add_parser("list", help="列出所有品牌")

    args = parser.parse_args()
    if args.command == "create":
        cmd_create(args)
    elif args.command == "query":
        cmd_query(args)
    elif args.command == "check":
        cmd_check(args)
    elif args.command == "switch":
        cmd_switch(args)
    elif args.command == "list":
        cmd_list(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
