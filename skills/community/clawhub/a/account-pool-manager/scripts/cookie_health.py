#!/usr/bin/env python3
"""cookie_health.py - Cookie健康检查exec脚本（增强版v2.0）
功能：扫描Cookie文件、按平台验证健康状态
输出：{success:bool, data:{health_details}, error:str, code:str}"""
import json, os, sys, subprocess
from pathlib import Path
from datetime import datetime
from typing import Any

# P1-1迁移: logging.basicConfig → db_logger统一日志(loguru+PostgreSQL)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger
logger = get_logger("skill", source="cookie_health")

# 导入统一Cookie管理器 (P1-2 Cookie统一迁移)
from mcps.shared.cookie_manager import COOKIES_DIR


HEALTHY_DAYS = int(os.environ.get("COOKIE_TTL_HOURS", "168")) // 24 or 7
EXPIRED_DAYS = 25
KNOWN_PLATFORMS = {"xiaohongshu","douyin","kuaishou","xianyu","shipinhao",
    "baijiahao","tiktok","toutiao","zhihu","juejin","csdn","jianshu",
    "segmentfault","bilibili","sohu"}
# API验证策略（来源: content_stats_collector.py已验证的API）
API_VERIFY = {
    "bilibili": ("https://api.bilibili.com/x/web-interface/nav",
                 lambda d: d.get("data",{}).get("isLogin") is True),
    "zhihu": ("https://www.zhihu.com/api/v4/me",
              lambda d: "id" in d and d.get("id") is not None),
    "juejin": ("https://api.juejin.cn/user_api/v1/user/get",
               lambda d: d.get("data",{}).get("user_id") is not None),
}
MCP_VERIFY = {"xianyu": ("fishclaw-mcp", "check_cookie_validity")}

def _extract_platform(cookie_path: Path) -> str:
    """从Cookie文件名提取平台名"""
    parts = cookie_path.stem.split("_")
    if parts[0] in KNOWN_PLATFORMS:
        return parts[0]
    if len(parts) >= 2 and "_".join(parts[:2]) in KNOWN_PLATFORMS:
        return "_".join(parts[:2])
    return parts[0]

def _load_cookie_header(cookie_path: Path) -> str:
    """从Playwright storage_state格式构建Cookie请求头"""
    try:
        data = json.loads(cookie_path.read_text(encoding="utf-8"))
        return "; ".join(f"{c['name']}={c['value']}" for c in data.get("cookies",[])
                         if c.get("name") and c.get("value"))
    except Exception as e:
        logger.error(f"Cookie读取失败: {e}")
        return ""

def _verify_cookie(platform: str, cookie_path: Path) -> bool:
    """按平台验证Cookie有效性: API优先→MCP次之→无手段返回None标记"""
    if platform in API_VERIFY:
        try:
            import httpx
            url, check_fn = API_VERIFY[platform]
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                       "Cookie": _load_cookie_header(cookie_path)}
            with httpx.Client(timeout=10.0, follow_redirects=True) as client:
                resp = client.get(url, headers=headers)
                return resp.status_code == 200 and check_fn(resp.json())
        except Exception as e:
            logger.error(f"cookie health异常: {e}", exc_info=True)
            logger.error("API验证失败(%s): %s", platform, e)
            return False
    if platform in MCP_VERIFY:
        try:
            server, tool = MCP_VERIFY[platform]
            cmd = ["openclaw","tool","call","--server",server,"--tool",tool,"--arguments","{}"]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=30,
                               encoding="utf-8", env={**os.environ,"PYTHONIOENCODING":"utf-8"})
            return r.returncode == 0 and '"valid": true' in r.stdout
        except Exception as e:
            logger.error(f"cookie health异常: {e}", exc_info=True)
            logger.warning("MCP验证失败(%s): %s", platform, e)
            return False
    return None  # 无验证手段

def check_single_cookie(cookie_path: Path, verify: bool = False) -> dict[str, Any]:
    """检查单个Cookie文件健康状态

    Args:
        cookie_path (Path): 参数说明
        verify (bool): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    if not cookie_path.exists():
        return {"cookie_file": cookie_path.name, "status": "expired",
                "reason": "文件不存在", "days_since_modified": None}
    stat = cookie_path.stat()
    days = (datetime.now() - datetime.fromtimestamp(stat.st_mtime)).days
    status = "expired" if days > EXPIRED_DAYS else "warning" if days > HEALTHY_DAYS else "healthy"
    reason = ("过期" if status == "expired" else f"{days}天未更新") if status != "healthy" else "正常"
    actually_valid = None
    platform = _extract_platform(cookie_path)
    if verify and status != "expired":
        actually_valid = _verify_cookie(platform, cookie_path)
    if actually_valid is False:
        status = "expired"
        method = "API" if platform in API_VERIFY else "MCP"
        reason = f"Cookie实际无效({method}验证失败)"
    return {"cookie_file": cookie_path.name, "platform": platform, "status": status,
            "reason": reason, "days_since_modified": days, "file_size_bytes": stat.st_size,
            "actually_valid": actually_valid}

def check_all(verify: bool = False, tenant_id: str = "") -> dict[str, Any]:
    """检查所有Cookie健康，支持多租户

    tenant_id为空时扫描根目录+所有租户子目录
    tenant_id非空时只扫描指定租户目录

    Args:
        verify (bool): 参数说明
        tenant_id (str): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    try:
        COOKIES_DIR.mkdir(parents=True, exist_ok=True)
        cookies = []
        if tenant_id:
            tenant_dir = COOKIES_DIR / tenant_id
            if tenant_dir.exists():
                cookies = list(tenant_dir.glob("*.json"))
        else:
            # 根目录Cookie(单用户模式)
            cookies = list(COOKIES_DIR.glob("*.json"))
            # 租户子目录Cookie(多租户模式)
            for d in COOKIES_DIR.iterdir():
                if d.is_dir() and d.name != "wechatsync":
                    cookies.extend(d.glob("*.json"))
        if not cookies:
            return {"success": True, "data": {"total":0,"healthy":0,"warning":0,
                    "expired":0,"details":[],"message":"无Cookie，请先登录"},
                    "error": None, "code": "AP-SUCCESS-05"}
        details = [check_single_cookie(c, verify) for c in sorted(cookies)]
        counts = {"healthy":0,"warning":0,"expired":0}
        for d in details:
            counts[d["status"]] += 1
        return {"success": True, "data": {"total": len(cookies), **counts, "details": details},
                "error": None, "code": "AP-SUCCESS-02"}
    except Exception as e:
        logger.error(f"cookie health异常: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": str(e), "code": "AP-ERR-UNKNOWN"}

def main():
    """CLI入口"""
    import argparse
    parser = argparse.ArgumentParser(description="Cookie健康检查v2.0")
    parser.add_argument("action", nargs="?", default="check_all")
    parser.add_argument("--verify", action="store_true",
                        help="验证Cookie有效性(API:bilibili/zhihu/juejin, MCP:xianyu)")
    parser.add_argument("--tenant-id", default="", help="指定租户ID(空=扫描全部)")
    args = parser.parse_args()
    if args.action == "check_all":
        result = check_all(args.verify, args.tenant_id)
    else:
        result = {"success": False, "data": {}, "error": f"未知操作: {args.action}", "code": "AP-ERR-UNKNOWN"}
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
