"""cookie-manager Cookie保活服务

扫描所有租户Cookie文件健康度+健康度<60触发HTTP保活+3次连续失败写tenant_notification+cookie_access_audit审计。
来源: v4.0设计文档§3.7.6 Cookie保活服务
R18统一入口: db_logger + atomic_write + cookie_manager
R72.1保护: Cookie保活(健康度评分+主动/被动刷新)不可删除
Schema防drift: 字段对照orchestration_schema.py实际DDL
  - cookie_access_audit: audit_id/tenant_id/platform/access_type/accessor_id/created_at
  - tenant_notification: notification_id/tenant_id/notification_type/level/message/payload/is_read/created_at/read_at
"""

import os
import sys
import json
import asyncio
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_SCRIPTS_DIR = _PROJECT_ROOT / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from mcps.shared.db_logger import get_logger
from mcps.shared.atomic_write import atomic_read_json, atomic_write_json
from mcps.shared.cookie_manager import COOKIES_DIR as COOKIE_DIR

logger = get_logger("cookie-manager", source="skills/cookie-manager/scripts/keepalive.py")

sys.path.insert(0, str(_SCRIPT_ROOT := _PROJECT_ROOT / "scripts"))

HEALTH_REFRESH_THRESHOLD = 60.0
MAX_CONSECUTIVE_FAILURES = 3
AGE_PENALTY_START_DAYS = 7
AGE_PENALTY_MAX = 30
INVALID_PENALTY = 50
STATE_FILE = _PROJECT_ROOT / "data" / "cookie_keepalive_state.json"

PLATFORM_HTTP_CHECK = {
    "xianyu": ("https://goofish.com", "cookie2"),
    "douyin": ("https://www.douyin.com", "sessionid"),
    "kuaishou": ("https://www.kuaishou.com", "userId"),
    "xiaohongshu": ("https://www.xiaohongshu.com", "customerClientId"),
    "bilibili": ("https://www.bilibili.com", "SESSDATA"),
    "csdn": ("https://www.csdn.net", "UserName"),
    "juejin": ("https://juejin.cn", "sessionid"),
    "weibo": ("https://weibo.com", "SUB"),
    "toutiao": ("https://www.toutiao.com", "sessionid"),
    "baijiahao": ("https://baijiahao.baidu.com", "BDUSS"),
    "sohu": ("https://mp.sohu.com", "SUV"),
    "jianshu": ("https://www.jianshu.com", "remember_mango"),
    "douban": ("https://www.douban.com", "dbcl2"),
    # v39.0 Task21: 从cookie_auto_manager.py合并的平台(R75.5去重)
    "shipinhao": ("https://channels.weixin.qq.com/platform", "login"),
    "tiktok": ("https://www.tiktok.com/tiktokstudio/upload?lang=en", "login"),
    "zhihu": ("https://www.zhihu.com/creator", "signin"),
    "segmentfault": ("https://segmentfault.com/user", "login"),
}


class CookieKeepaliveService:
    """Cookie Keepalive Service 类"""
    def __init__(self, db_pool=None):
        self.db_pool = db_pool
        self._state = self._load_state()

    def _load_state(self) -> dict:
        return atomic_read_json(str(STATE_FILE), default={})

    def _save_state(self):
        try:
            atomic_write_json(str(STATE_FILE), self._state, indent=2)
        except Exception as e:
            logger.error(f"保存状态文件失败: {e}")

    def _scan_cookie_files(self) -> List[Tuple[str, str, Path]]:
        """扫描data/content/cookies/目录,返回(tenant_id, platform, file_path)列表"""
        results = []
        if not COOKIE_DIR.exists():
            return results

        for item in COOKIE_DIR.iterdir():
            if item.is_dir():
                tenant_id = item.name
                for cookie_file in item.glob("*.json"):
                    if cookie_file.name == "cookie_locks.json":
                        continue
                    platform = self._extract_platform(cookie_file.name)
                    if platform:
                        results.append((tenant_id, platform, cookie_file))
            elif item.is_file() and item.suffix == ".json" and item.name != "cookie_locks.json":
                platform = self._extract_platform(item.name)
                if platform:
                    results.append(("default", platform, item))
        return results

    def _extract_platform(self, filename: str) -> Optional[str]:
        """从文件名提取平台名(如douyin_default.json→douyin)"""
        name = filename.replace(".json", "")
        # 最长匹配优先: douyin_img_default应匹配douyin_img而非douyin
        for plat in sorted(PLATFORM_HTTP_CHECK, key=len, reverse=True):
            if name.startswith(plat + "_") or name == plat:
                return plat
        parts = name.split("_", 1)
        return parts[0] if parts and parts[0] else None

    def _calculate_age_days(self, file_path: Path) -> float:
        """计算Cookie文件年龄(天)"""
        try:
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc)
            age = (datetime.now(timezone.utc) - mtime).total_seconds() / 86400
            return max(0.0, age)
        except Exception as e:
            logger.warning(f"Unexpected error: {e}", exc_info=True)
            return 999.0

    def _calculate_health_score(self, age_days: float, is_valid: bool, file_exists: bool) -> float:
        """计算健康度评分(0-100)

        - 文件不存在: 0
        - 年龄惩罚: age>7天 → 扣(age-7)*5, 最多扣30
        - 有效性惩罚: HTTP检查失败 → 扣50
        """
        if not file_exists:
            return 0.0
        score = 100.0
        if age_days > AGE_PENALTY_START_DAYS:
            age_penalty = min((age_days - AGE_PENALTY_START_DAYS) * 5, AGE_PENALTY_MAX)
            score -= age_penalty
        if is_valid is False:
            score -= INVALID_PENALTY
        return max(0.0, min(100.0, score))

    async def _http_check_cookie(self, platform: str, cookie_str: str) -> Optional[bool]:
        """HTTP检查Cookie有效性"""
        if not cookie_str or platform not in PLATFORM_HTTP_CHECK:
            return None
        try:
            import httpx
        except ImportError:
            return None
        url, marker = PLATFORM_HTTP_CHECK[platform]
        try:
            resp = await asyncio.to_thread(
                httpx.get, url,
                headers={"User-Agent": "Mozilla/5.0", "Cookie": cookie_str},
                follow_redirects=False, timeout=10.0,
            )
            if resp.status_code == 200:
                return marker in cookie_str
            if resp.status_code in (301, 302, 303, 307, 308):
                location = resp.headers.get("location", "")
                if "login" in location.lower() or "passport" in location.lower():
                    return False
                return True
            return False
        except Exception as e:
            logger.error(f"HTTP检查失败 platform={platform}: {e}")
            return None

    def _load_cookie_str(self, file_path: Path) -> str:
        """从Cookie文件加载Cookie字符串(支持JSON数组格式)"""
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                parts = []
                for c in data:
                    if isinstance(c, dict) and "name" in c and "value" in c:
                        parts.append(f'{c["name"]}={c["value"]}')
                return "; ".join(parts)
            if isinstance(data, dict):
                cookies = data.get("cookies", [])
                if isinstance(cookies, list):
                    parts = []
                    for c in cookies:
                        if isinstance(c, dict) and "name" in c and "value" in c:
                            parts.append(f'{c["name"]}={c["value"]}')
                    return "; ".join(parts)
            return ""
        except Exception as e:
            logger.error(f"加载Cookie失败 {file_path}: {e}")
            return ""

    async def _write_audit(self, tenant_id: str, platform: str, access_type: str):
        """写入cookie_access_audit审计日志

        Schema来源: orchestration_schema.py cookie_access_audit表
        字段: audit_id(BIGSERIAL自增)/tenant_id/platform/access_type/accessor_id/created_at
        RLS修复: 设置SET LOCAL app.tenant_id以通过RLS策略
        """
        if not self.db_pool:
            return
        try:
            async with self.db_pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute("SELECT set_config('app.tenant_id', $1, true)", tenant_id)
                    await conn.execute(
                        """INSERT INTO cookie_access_audit(tenant_id, platform, access_type, accessor_id)
                           VALUES($1, $2, $3, $4)""",
                        tenant_id, platform, access_type, "cookie-manager",
                    )
        except Exception as e:
            logger.error(f"写入cookie_access_audit失败: {e}")

    async def _send_notification(self, tenant_id: str, message: str, payload: dict):
        """写入tenant_notification告警

        Schema来源: orchestration_schema.py tenant_notification表
        字段: notification_id(BIGSERIAL自增)/tenant_id/notification_type/level(默认INFO)/message(必填)/payload/is_read/created_at/read_at
        RLS修复: 设置SET LOCAL app.tenant_id以通过RLS策略
        """
        if not self.db_pool:
            return
        try:
            async with self.db_pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute("SELECT set_config('app.tenant_id', $1, true)", tenant_id)
                    await conn.execute(
                        """INSERT INTO tenant_notification(tenant_id, notification_type, level, message, payload)
                           VALUES($1, $2, $3, $4, $5)""",
                        tenant_id, "cookie_keepalive_failure", "WARNING", message,
                        json.dumps(payload, ensure_ascii=False),
                    )
            logger.warning(f"Cookie保活失败告警已发送 tenant={tenant_id}")
        except Exception as e:
            logger.error(f"发送告警失败: {e}")

    async def check_and_keepalive(self, tenant_filter: Optional[str] = None, force_refresh: bool = False) -> Dict[str, Any]:
        """检查 and keepalive

        Args:
            tenant_filter (Optional[str]): 参数说明
            force_refresh (bool): 参数说明

        Returns:
            Dict[str, Any]: 返回值说明
        """
        try:
            cookie_files = self._scan_cookie_files()
            if tenant_filter:
                cookie_files = [(t, p, f) for t, p, f in cookie_files if t == tenant_filter]

            if not cookie_files:
                logger.info("未发现Cookie文件")
                return {"success": True, "data": {"total": 0, "healthy": 0, "refreshed": 0, "failed": 0, "skipped": 0, "alerts_sent": 0, "details": []}, "error": None, "code": "NO_COOKIES"}

            total = len(cookie_files)
            healthy = 0
            refreshed = 0
            failed = 0
            skipped = 0
            alerts_sent = 0
            details = []

            for tenant_id, platform, file_path in cookie_files:
                try:
                    await self._write_audit(tenant_id, platform, "check")
                    age_days = self._calculate_age_days(file_path)
                    cookie_str = self._load_cookie_str(file_path)
                    is_valid = await self._http_check_cookie(platform, cookie_str)
                    health_score = self._calculate_health_score(age_days, is_valid, True)

                    state_key = f"{tenant_id}:{platform}"
                    state_entry = self._state.get(state_key, {"consecutive_failures": 0})
                    consecutive_failures = state_entry.get("consecutive_failures", 0)

                    action = "none"
                    if force_refresh or health_score < HEALTH_REFRESH_THRESHOLD:
                        action = "keepalive"
                        await self._write_audit(tenant_id, platform, "keepalive")
                        keepalive_ok = await self._http_check_cookie(platform, cookie_str)
                        # Fix 3: None(httpx未安装或平台不支持HTTP检查)不应计为刷新成功
                        # 根因: 原 `keepalive_ok is True or keepalive_ok is None` 将None当成功,
                        #       导致未实际保活的Cookie被计入refreshed,虚报健康状态
                        if keepalive_ok is True:
                            refreshed += 1
                            consecutive_failures = 0
                        elif keepalive_ok is None:
                            skipped += 1
                            logger.warning(
                                f"Cookie保活跳过(HTTP检查不可用) tenant={tenant_id} platform={platform}"
                            )
                        else:
                            failed += 1
                            consecutive_failures += 1
                            await self._write_audit(tenant_id, platform, "refresh_failed")

                        if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                            await self._send_notification(
                                tenant_id,
                                f"Cookie连续{consecutive_failures}次保活失败(platform={platform}),需人工介入",
                                {"platform": platform, "consecutive_failures": consecutive_failures, "health_score": health_score, "file": str(file_path)},
                            )
                            alerts_sent += 1
                    else:
                        healthy += 1
                        consecutive_failures = 0

                    self._state[state_key] = {
                        "consecutive_failures": consecutive_failures,
                        "last_check": datetime.now(timezone.utc).isoformat(),
                        "last_health_score": round(health_score, 2),
                    }

                    details.append({
                        "tenant_id": tenant_id,
                        "platform": platform,
                        "health_score": round(health_score, 2),
                        "age_days": round(age_days, 1),
                        "action": action,
                        "consecutive_failures": consecutive_failures,
                    })
                except Exception as e:
                    logger.error(f"处理Cookie异常 tenant={tenant_id} platform={platform}: {e}")
                    failed += 1

            self._save_state()
            result = {
                "total": total,
                "healthy": healthy,
                "refreshed": refreshed,
                "failed": failed,
                "skipped": skipped,
                "alerts_sent": alerts_sent,
                "details": details,
            }
            logger.info(f"Cookie保活扫描完成 total={total} healthy={healthy} refreshed={refreshed} failed={failed} skipped={skipped} alerts={alerts_sent}")
            return {"success": True, "data": result, "error": None, "code": None if self.db_pool else "DB_NOT_CONNECTED"}
        except Exception as e:
            logger.error(f"Cookie保活扫描异常: {e}")
            return {"success": False, "data": {}, "error": str(e), "code": "KEEPALIVE_EXCEPTION"}


async def _get_db_pool():
    pg_dsn = os.getenv("PG_DSN")
    if not pg_dsn:
        return None
    try:
        import asyncpg
        return await asyncpg.create_pool(pg_dsn, min_size=1, max_size=5)
    except ImportError:
        logger.warning("asyncpg未安装,DB功能降级")
        return None
    except Exception as e:
        logger.error(f"DB连接失败: {e}")
        return None


def main():
    """main"""
    parser = argparse.ArgumentParser(description="Cookie保活服务")
    parser.add_argument("--tenant", default=None, help="指定租户ID")
    parser.add_argument("--force-refresh", action="store_true", help="强制刷新所有Cookie")
    args = parser.parse_args()

    async def _run():
        pool = await _get_db_pool()
        try:
            service = CookieKeepaliveService(db_pool=pool)
            result = await service.check_and_keepalive(args.tenant, args.force_refresh)
            print(json.dumps(result, ensure_ascii=False, default=str))
        finally:
            if pool:
                await pool.close()

    asyncio.run(_run())


if __name__ == "__main__":
    main()
