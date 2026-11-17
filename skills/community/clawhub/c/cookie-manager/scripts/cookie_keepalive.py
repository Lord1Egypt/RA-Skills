"""Cookie Playwright保活引擎 v1.0

通过Playwright持久化上下文定期访问平台页面,维持Cookie有效性。
每次访问后导出storageState到JSON文件,供SAU发布时使用。

核心设计:
  - 保活阶段: launch_persistent_context(user_data_dir=profiles/{platform}_{account})
    → 访问创作者后台 → 触发JS端Session刷新 → 导出storageState
  - 发布阶段: new_context(storage_state={platform}_{account}.json)
    → 从导出的JSON加载 → 执行发布 → 回写更新

多账号隔离:
  - 每个账号独立的user_data_dir目录: data/content/profiles/{platform}_{account}/
  - 每个账号独立的Cookie JSON: data/content/cookies/{platform}_{account}.json

保活频率:
  - B站: 每3天refresh_token刷新(不需要Playwright保活)
  - 小红书: 每6小时Playwright访问一次
  - 抖音: 每6小时Playwright访问一次
  - 快手: 每12小时Playwright访问一次
  - 闲鱼: 每6小时Playwright访问一次

诚实说明:
  - Playwright保活不能保证Cookie永远有效,只是延长有效期
  - 小红书/抖音实际有效期1-3天,保活可能延长到3-7天
  - Cookie失效后仍需QQBot扫码重新登录
  - HTTP心跳对国内平台几乎无效,Playwright访问是更可靠的替代方案
  - Playwright保活!=Cookie刷新: 保活仅延长Cookie有效期,平台主动失效时保活无效
  - 20个平台无自动登录恢复机制,Cookie失效后需人工扫码(R74.4降级标注)

用法:
  python skills/cookie-manager/scripts/cookie_keepalive.py run                     # 保活所有平台
  python skills/cookie-manager/scripts/cookie_keepalive.py run --platform douyin   # 保活指定平台
  python skills/cookie-manager/scripts/cookie_keepalive.py export --platform douyin --account default  # 导出storageState
  python skills/cookie-manager/scripts/cookie_keepalive.py status                  # 查看保活状态
"""
import argparse
import asyncio
from datetime import datetime
import json
import os
from pathlib import Path
import sys
import time

# 原子写入 + 统一日志 + Cookie管理(统一入口规则: cookie_manager为唯一权威源)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_SCRIPTS_DIR = PROJECT_ROOT / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from typing import Any, Optional
from utils import json_out  # P1-3: 统一JSON输出函数
from mcps.shared.atomic_write import atomic_write_text, atomic_write_json
from mcps.shared.cookie_manager import resolve_cookie_path, COOKIES_DIR as _CM_COOKIES_DIR
from mcps.shared.db_logger import get_logger
logger = get_logger("cookie-keepalive", source="cookie-keepalive")
PROFILES_DIR = PROJECT_ROOT / "data" / "content" / "profiles"
# Cookie目录统一从cookie_manager获取(统一入口规则: 禁止硬编码Cookie路径)
COOKIES_DIR = _CM_COOKIES_DIR
STATUS_FILE = PROJECT_ROOT / "data" / "content" / "keepalive_status.json"

# 加载.env
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    logger.error("python-dotenv未安装,跳过.env加载")

# 平台保活配置
KEEPALIVE_CONFIG = {
    "xiaohongshu": {
        "name": "小红书",
        "visit_url": "https://creator.xiaohongshu.com/creator/home",
        "login_marker": "passport",
        "interval_hours": 6,
        "timeout_seconds": 30,
        # MediaCrawler竞品采集需要web_session cookie,创作者后台不产生
        # 保活后额外访问搜索页,使storage_state包含web_session
        "crawler_visit_url": "https://www.xiaohongshu.com/explore",
    },
    "douyin": {
        "name": "抖音",
        "visit_url": "https://creator.douyin.com/creator-micro/home",
        "login_marker": "login",
        "interval_hours": 6,
        "timeout_seconds": 30,
    },
    "kuaishou": {
        "name": "快手",
        "visit_url": "https://cp.kuaishou.com/article/publish/video",
        "login_marker": "passport",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    "xianyu": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "闲鱼",
        "visit_url": "https://www.goofish.com/personal?spm=a21ybx",
        "login_marker": "login",
        "interval_hours": 6,
        "timeout_seconds": 30,
    },
    "shipinhao": {
        "name": "微信视频号",
        "visit_url": "https://channels.weixin.qq.com/platform",
        "login_marker": "login",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    "baijiahao": {
        "name": "百家号",
        "visit_url": "https://baijiahao.baidu.com/builder/rc/home",
        "login_marker": "login",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    "tiktok": {
        "name": "TikTok",
        "visit_url": "https://www.tiktok.com/tiktokstudio/upload?lang=en",
        "login_marker": "login",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    "toutiao": {
        "name": "头条号",
        "visit_url": "https://mp.toutiao.com/profile_v4/graphic/articles",
        "login_marker": "login",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    "zhihu": {
        "name": "知乎",
        "visit_url": "https://www.zhihu.com/creator",
        "login_marker": "signin",
        "interval_hours": 12,
        "timeout_seconds": 30,
        # MediaCrawler竞品采集需要z_c0 cookie,创作者后台不产生
        "crawler_visit_url": "https://www.zhihu.com/search?type=content&q=AI",
    },
    "juejin": {
        "name": "掘金",
        "visit_url": "https://juejin.cn/creator/home",
        "login_marker": "login",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    "csdn": {
        "name": "CSDN",
        "visit_url": "https://mp.csdn.net/mp_blog/creation/editor",
        "login_marker": "login",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    "jianshu": {
        "name": "简书",
        "visit_url": "https://www.jianshu.com/writer",
        "login_marker": "sign_in",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    "segmentfault": {
        "name": "思否",
        "visit_url": "https://segmentfault.com/user",
        "login_marker": "login",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    # P1-4: Cookie保活扩展(Wechatsync扩容新增平台)
    "weibo": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "微博",
        # AD-ARCH-19修复(R9): 浏览器实测确认原URL正确,回滚myprofile改动
        # 实测证据: weibo.com/ 未登录→重定向到newlogin(含"login"关键词)→keepalive检测有效
        #           weibo.com/myprofile 未登录→不重定向→keepalive误判为已登录(已回滚)
        "visit_url": "https://weibo.com/",
        "login_marker": "login",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    "douban": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "豆瓣",
        "visit_url": "https://www.douban.com/mine/",
        "login_marker": "login",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    "cnblogs": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "博客园",
        "visit_url": "https://www.cnblogs.com/",
        "login_marker": "signin",
        "interval_hours": 24,
        "timeout_seconds": 30,
    },
    "51cto": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "51CTO",
        "visit_url": "https://blog.51cto.com/",
        "login_marker": "login",
        "interval_hours": 24,
        "timeout_seconds": 30,
    },
    "oschina": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "开源中国",
        "visit_url": "https://my.oschina.net/",
        "login_marker": "login",
        "interval_hours": 24,
        "timeout_seconds": 30,
    },
    "yuque": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "语雀",
        "visit_url": "https://www.yuque.com/dashboard",
        "login_marker": "login",
        "interval_hours": 24,
        "timeout_seconds": 30,
    },
    "imooc": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "慕课网",
        "visit_url": "https://www.imooc.com/u/index",
        "login_marker": "login",
        "interval_hours": 24,
        "timeout_seconds": 30,
    },
    "xueqiu": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "雪球",
        "visit_url": "https://xueqiu.com/",
        "login_marker": "login",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    "eastmoney": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "东方财富",
        "visit_url": "https://caifuhao.eastmoney.com/",
        "login_marker": "login",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    "smzdm": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "什么值得买",
        "visit_url": "https://zhiyou.smzdm.com/",
        "login_marker": "login",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    "woshipm": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "人人PM",
        "visit_url": "https://www.woshipm.com/",
        "login_marker": "login",
        "interval_hours": 24,
        "timeout_seconds": 30,
    },
    "yidian": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "一点资讯",
        "visit_url": "https://www.yidianzixun.com/",
        "login_marker": "login",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    "sohu": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "搜狐号",
        "visit_url": "https://mp.sohu.com/mpfe/v3/",
        "login_marker": "login",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    "dayu": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "大鱼号",
        "visit_url": "https://mp.dayu.com/",
        "login_marker": "login",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    "netease": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "网易号",
        "visit_url": "https://mp.163.com/",
        "login_marker": "login",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    "bilibili_col": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "B站专栏",
        "visit_url": "https://member.bilibili.com/article-text/home",
        "login_marker": "login",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    # AD-ARCH-46修复(R13): 移除douyin_img保活配置
    # 原因: douyin_img与douyin共享同一账号/Cookie/URL(https://creator.douyin.com/creator-micro/home)
    # 保留两者会导致每6小时访问同一URL两次,可能触发抖音反爬检测
    # douyin保活已覆盖douyin_img的Cookie需求(同一storage_state文件)
    "sohufocus": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "搜狐焦点",
        "visit_url": "https://house.focus.cn/",
        "login_marker": "login",
        "interval_hours": 12,
        "timeout_seconds": 30,
    },
    "x_twitter": {  # DOWNGRADE: 无自动登录恢复,需人工扫码
        "name": "X(Twitter)",
        "visit_url": "https://x.com/home",
        "login_marker": "login",
        "interval_hours": 24,
        "timeout_seconds": 30,
    },
    # AD-ARCH-18修复(R9): WordPress/Typecho使用MetaWeblog API(XML-RPC认证),
    # 不依赖Cookie,且保活URL需从租户配置获取实际博客URL(非官方站wordpress.com/typecho.org)
    # 移除无效的保活配置,避免浪费资源访问错误站点
    # "wordpress": {"name": "WordPress", "visit_url": "https://wordpress.com/", ...},
    # "typecho": {"name": "Typecho", "visit_url": "https://typecho.org/", ...},
    # wechat_official(微信公众号)未列入Cookie保活配置:
    # 微信公众号是API平台(使用appid+appsecret获取access_token),不依赖Cookie认证,
    # 无需Playwright保活。凭证有效性通过agency-portal-mcp的portal_test_api_credential验证。
}

# T-A07: 并发保活配置(原串行930Cookie需7.75h,并发后约18.6min)
# R72.1保护: 不修改Cron频率(仍每6h),仅执行模型变更(串行->并发)
MAX_CONCURRENT = 25   # 最大并发租户数(资源限制: 每个Playwright实例约100MB内存,25个约2.5GB)
BATCH_SIZE = 10       # 每批租户数(30租户分3批,避免内存峰值)
BATCH_INTERVAL = 60   # 批间间隔秒数(等待GC释放内存)

# T-A02: 无QQBot自动登录恢复的平台列表(R74.4降级标注)
# 来源: scripts/qqbot_login.py PLATFORM_INFO, 13个平台有扫码登录实现,其余无
# 这些平台Cookie失效后只能通过QQBot告警通知用户,需人工扫码重新登录
PLATFORMS_NO_AUTO_RECOVERY = frozenset({
    "xianyu", "weibo", "douban", "cnblogs", "51cto", "oschina", "yuque",
    "imooc", "xueqiu", "eastmoney", "smzdm", "woshipm", "yidian", "sohu",
    "dayu", "netease", "bilibili_col", "sohufocus", "x_twitter",
})


def _get_profile_dir(platform: str, account: str, tenant_id: str = "") -> Path:
    """获取Playwright持久化上下文的用户数据目录,支持租户隔离

    有tenant_id时: data/content/profiles/{tenant_id}/{platform}_{account}/
    无tenant_id时: data/content/profiles/{platform}_{account}/ (自有商品场景)
    """
    if tenant_id:
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', tenant_id):
            logger.warning(f"[cookie_keepalive] 非法tenant_id(路径遍历风险): {tenant_id!r},回退到无租户路径")
            profile_dir = PROFILES_DIR / f"{platform}_{account}"
            profile_dir.mkdir(parents=True, exist_ok=True)
            return profile_dir
        profile_dir = PROFILES_DIR / tenant_id / f"{platform}_{account}"
        profile_dir.mkdir(parents=True, exist_ok=True)
        return profile_dir
    profile_dir = PROFILES_DIR / f"{platform}_{account}"
    profile_dir.mkdir(parents=True, exist_ok=True)
    return profile_dir


def _get_cookie_file(platform: str, account: str, tenant_id: str = "") -> Path:
    """获取Cookie JSON文件路径,支持租户隔离

    委托给cookie_manager.resolve_cookie_path(统一入口规则: cookie_manager为唯一权威源)
    闲鱼特殊处理: 与fishclaw-mcp保持一致的Cookie路径
    - 有tenant_id: data/content/cookies/{tenant_id}/xianyu_cookies.json
    - 无tenant_id: data/fishclaw_cache/cookies/xianyu_cookies.json (fishclaw默认路径)
    来源: 04部署文档§2.3 多租户Cookie隔离
    """
    return resolve_cookie_path(platform, account, tenant_id)


async def _quick_cookie_check(platform: str, cookie_file: Path) -> bool:
    """快速HTTP API检查Cookie是否有效（不依赖Playwright，避免误报）

    页面加载超时时调用此函数进行二次验证：
    - 闲鱼: 调用h5api.m.goofish.com验证
    - 其他平台: 检查Cookie文件是否存在且非空+最近修改时间<7天
    """
    # 闲鱼有专门的API验证
    if platform == "xianyu":
        try:
            import urllib.request
            if not cookie_file.exists():
                return False
            cookies = json.loads(cookie_file.read_text(encoding="utf-8"))
            cookie_list = cookies if isinstance(cookies, list) else cookies.get("cookies", [])
            cookie_str = "; ".join(
                f"{c.get('name', '')}={c.get('value', '')}"
                for c in cookie_list if c.get("name") and c.get("value")
            )
            if not cookie_str:
                return False
            req = urllib.request.Request(
                "https://h5api.m.goofish.com/h5/mtop.taobao.idlefish.user.items/1.0/",
                headers={"Cookie": cookie_str, "User-Agent": "Mozilla/5.0"},
            )
            loop = asyncio.get_event_loop()
            resp = await loop.run_in_executor(None, lambda: urllib.request.urlopen(req, timeout=10))
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                return "SUCCESS" in str(data.get("ret", []))
        except (OSError, urllib.error.URLError, json.JSONDecodeError, ValueError) as e:
            logger.debug(f"[cookie_keepalive] 闲鱼Cookie HTTP验证失败: {e}")
        return False

    # 其他平台：检查Cookie文件是否存在且最近修改时间<7天
    if not cookie_file.exists() or cookie_file.stat().st_size == 0:
        return False
    try:
        mtime = cookie_file.stat().st_mtime
        age_hours = (time.time() - mtime) / 3600
        return age_hours < 168  # 7天
    except OSError as e:
        logger.error(f"cookie keepalive异常: {e}", exc_info=True)
        logger.error(f"[cookie_keepalive] Cookie文件时间戳读取失败: {e}")
        return False


def _load_keepalive_status() -> dict:
    """加载保活状态文件"""
    if STATUS_FILE.exists():
        try:
            return json.loads(STATUS_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            logger.debug(f"[cookie_keepalive] 保活状态文件加载失败: {e}")
    return {}


def _save_keepalive_status(status: dict):
    """保存保活状态文件"""
    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(str(STATUS_FILE), json.dumps(status, ensure_ascii=False, indent=2))


async def _playwright_keepalive(platform: str, account: str, tenant_id: str = "") -> dict:
    """对单个平台执行Playwright保活

    流程:
    1. 启动Playwright持久化上下文(使用user_data_dir)
    2. 访问创作者后台页面
    3. 等待页面加载完成
    4. 检查是否仍在登录状态
    5. 导出storageState到Cookie JSON文件
    6. 关闭浏览器
    """
    config = KEEPALIVE_CONFIG.get(platform)
    if not config:
        return {"success": False, "error": f"无保活配置: {platform}"}

    profile_dir = _get_profile_dir(platform, account, tenant_id)
    cookie_file = _get_cookie_file(platform, account, tenant_id)

    # 如果没有Cookie文件也没有profile,无法保活
    has_profile = any(profile_dir.iterdir()) if profile_dir.exists() else False
    has_cookie = cookie_file.exists() and cookie_file.stat().st_size > 0

    if not has_profile and not has_cookie:
        return {"success": False, "error": f"无Cookie且无浏览器profile,需先登录: {platform}"}

    try:
        from patchright.async_api import async_playwright
    except ImportError:
        return {"success": False, "error": "需要安装patchright: pip install patchright && patchright install chromium"}

    pw = await async_playwright().start()
    try:
        # 启动持久化上下文
        # 如果有Cookie JSON但没有profile,先从Cookie创建profile
        launch_args = {
            "headless": True,
            "args": [],
        }

        # 优先使用persistent context(保持完整浏览器状态)
        context = await pw.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            **launch_args,
        )

        # 如果有Cookie JSON但profile是新的,注入Cookie
        if has_cookie and not has_profile:
            try:
                state = json.loads(cookie_file.read_text(encoding="utf-8"))
                if isinstance(state, dict) and "cookies" in state:
                    for cookie in state["cookies"]:
                        await context.add_cookies([{
                            "name": cookie.get("name", ""),
                            "value": cookie.get("value", ""),
                            "domain": cookie.get("domain", ""),
                            "path": cookie.get("path", "/"),
                        }])
            except (OSError, json.JSONDecodeError, KeyError, TypeError) as e:
                logger.debug(f"[cookie_keepalive] Cookie注入到Playwright失败: {e}")

        page = await context.new_page()

        # 访问创作者后台
        try:
            await page.goto(config["visit_url"], timeout=config["timeout_seconds"] * 1000, wait_until="domcontentloaded")
        except Exception as e:
            logger.error(f"异常: {e}", exc_info=True)
            # patchright/Playwright的TimeoutError不一定继承内置TimeoutError,使用Exception捕获所有异常
            # 二次验证：用HTTP API检查Cookie是否仍然有效
            is_cookie_valid = await _quick_cookie_check(platform, cookie_file)
            if is_cookie_valid:
                # Cookie有效但页面加载超时 → 网络问题，不是Cookie过期
                await context.close()
                return {
                    "success": True,
                    "platform": platform,
                    "account": account,
                    "is_logged_in": True,  # Cookie有效，保守认为已登录
                    "warning": f"页面加载超时但Cookie有效(网络问题): {str(e)[:80]}",
                    "cookie_exported": cookie_file.exists(),
                }
            else:
                # Cookie也无效 → 确实过期
                await context.close()
                return {"success": False, "error": f"页面加载超时且Cookie无效(已过期): {str(e)[:80]}", "platform": platform}

        # 等待页面渲染
        await asyncio.sleep(3)

        # 检查是否仍在登录状态
        current_url = page.url
        page_content = await page.content()
        is_logged_in = config["login_marker"] not in current_url.lower()

        # 进一步检查页面内容(有些平台不重定向但显示登录框)
        if is_logged_in:
            content_lower = page_content[:5000].lower()
            # 检查是否有用户信息标记(表示已登录)
            login_indicators = ["userinfo", "nickname", "avatar", "creator", "dashboard"]
            logout_indicators = ["请登录", "立即登录", "sign in", "login-btn"]
            has_login_indicator = any(ind in content_lower for ind in login_indicators)
            has_logout_indicator = any(ind in content_lower for ind in logout_indicators)
            if has_logout_indicator and not has_login_indicator:
                is_logged_in = False

        # 无论是否登录,都导出storageState(可能包含更新的Cookie)
        # 如果配置了crawler_visit_url,额外访问搜索页以获取web_session等爬虫所需cookie
        crawler_visit_url = config.get("crawler_visit_url")
        if crawler_visit_url and is_logged_in:
            try:
                crawler_page = await context.new_page()
                await crawler_page.goto(crawler_visit_url, timeout=15000, wait_until="domcontentloaded")
                await asyncio.sleep(2)  # 等待cookie设置
                await crawler_page.close()
                logger.info(f"[cookie_keepalive] {platform} 额外访问搜索页: {crawler_visit_url}")
            except (TimeoutError, ConnectionError, RuntimeError) as e:
                # 搜索页访问失败不影响保活结果
                logger.debug(f"[cookie_keepalive] {platform} 搜索页访问失败(非致命): {e}")

        # AD-ARCH-21修复(R9): 仅在登录状态下导出storageState
        # 原代码无条件导出,未登录时可能用过期/重定向Cookie覆盖有效Cookie文件
        if is_logged_in:
            # 蚕食v16.0-AD修复: 原子写入替代Playwright直接写入,防止并发读取时读到半写文件
            _ss = await context.storage_state()
            atomic_write_json(str(cookie_file), _ss)
        else:
            logger.warning(f"[cookie_keepalive] {platform} 未登录,跳过storageState导出(保留现有Cookie文件)")

        # 保活成功后推送WebSocket通知给客户端(非致命,失败不影响保活)
        if is_logged_in:
            try:
                import urllib.request
                import urllib.error
                notif_data = json.dumps({
                    "type": "cookie_refreshed",
                    "platform": platform,
                    "tenant_id": tenant_id,
                    "timestamp": int(time.time()),
                }).encode("utf-8")
                # 端口修复(V106-003): portal_server监听8000(AGENCY_PORTAL_PORT),原800端口不一致
                notify_url = os.environ.get("PORTAL_NOTIFY_URL", "http://localhost:8000/api/notify")
                req = urllib.request.Request(
                    notify_url,
                    data=notif_data,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=5) as resp:
                    if resp.status == 200:
                        logger.info(f"[cookie_keepalive] 通知推送成功: {platform}")
                    else:
                        logger.warning(f"[cookie_keepalive] 通知推送失败: HTTP {resp.status}")
            except Exception as notify_err:
                logger.error(f"cookie keepalive异常: {notify_err}", exc_info=True)
                logger.warning(f"[cookie_keepalive] 通知推送异常(非致命): {notify_err}")

        await context.close()

        result = {
            "success": True,
            "platform": platform,
            "account": account,
            "is_logged_in": is_logged_in,
            "visited_url": current_url[:100],
            "cookie_exported": cookie_file.exists(),
        }

        if not is_logged_in:
            result["warning"] = "Cookie可能已失效,需要重新登录"

        return result

    except (RuntimeError, OSError, KeyError, TimeoutError) as e:
        logger.error(f"[cookie_keepalive] Playwright保活异常({platform}): {e}")
        return {"success": False, "error": f"Playwright保活异常: {str(e)[:150]}", "platform": platform}
    finally:
        await pw.stop()


async def _export_storage_state(platform: str, account: str, tenant_id: str = "") -> dict:
    """从持久化上下文导出storageState到Cookie JSON文件

    不访问页面,仅启动浏览器导出当前状态。
    用于在保活间隔期间手动同步Cookie。
    """
    profile_dir = _get_profile_dir(platform, account, tenant_id)
    cookie_file = _get_cookie_file(platform, account, tenant_id)

    if not profile_dir.exists() or not any(profile_dir.iterdir()):
        return {"success": False, "error": f"浏览器profile不存在: {profile_dir}"}

    try:
        from patchright.async_api import async_playwright
    except ImportError:
        return {"success": False, "error": "需要安装patchright"}

    pw = await async_playwright().start()
    try:
        context = await pw.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=True,
        )
        _ss = await context.storage_state()
        atomic_write_json(str(cookie_file), _ss)
        await context.close()
        return {"success": True, "platform": platform, "cookie_file": str(cookie_file)}
    except (RuntimeError, OSError, KeyError, TimeoutError) as e:
        logger.error(f"[cookie_keepalive] Cookie导出异常({platform}): {e}")
        return {"success": False, "error": str(e)[:150]}
    finally:
        await pw.stop()


def _notify_expired(platform: str, account: str, tenant_id: str = ""):
    """Cookie过期时通过QQBot推送提醒 + WebSocket通知客户端(来源:39_client_server_refactor_plan_v1.0.md §4.2)"""
    try:
        sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
        from notification import send_alert
        config = KEEPALIVE_CONFIG.get(platform, {})
        name = config.get("name", platform)
        tenant_line = f"租户: {tenant_id}\n" if tenant_id else ""
        # AD-ARCH-44修复(R13): level从WARN改为ERROR,确保QQBot OpenAPI能推送(仅CRITICAL/ERROR级别)
        # 30天无人值守要求: Cookie失效必须通过QQBot推送到用户手机,WARN级别会被QQBot过滤
        logger.info(f"[notify] Cookie失效告警推送开始: {platform}/{account} (level=ERROR, QQBot+企业微信)")
        send_alert(
            f"🔑 {name}Cookie已失效\n"
            f"平台: {name}({platform})\n"
            f"{tenant_line}"
            f"账号: {account}\n"
            f"请运行: python skills/cookie-manager/scripts/cookie_keepalive.py login --platform {platform} --account {account}"
            f"{' --tenant_id ' + tenant_id if tenant_id else ''}\n",
            level="ERROR",
        )
        logger.info(f"[notify] Cookie失效告警推送完成: {platform}/{account}")
    except (ImportError, ConnectionError, TimeoutError, OSError) as e:
        # 告警推送失败时至少写入本地日志，避免完全静默
        logger.error(f"[notify] QQBot推送失败({platform}): {e}")

    # 补齐cookie_expired sender(来源:39_client_server_refactor_plan_v1.0.md §4.2)
    # 客户端ws-notification.ts L126已有cookie_expired处理器,但服务端无sender=死代码
    # AD-ARCH-45修复(R13): 移除if tenant_id条件,单用户模式也推送WebSocket通知
    # 30天无人值守要求: 无论单用户还是多租户,Cookie失效都必须通知客户端
    effective_tenant = tenant_id or "default"
    logger.info(f"[notify] WebSocket cookie_expired推送开始: {platform}/{effective_tenant} (URL={os.environ.get('PORTAL_NOTIFY_URL', 'http://localhost:8000/api/notify')})")
    try:
        import urllib.request
        notif_data = json.dumps({
            "type": "cookie_expired",
            "platform": platform,
            "account": account,
            "tenant_id": effective_tenant,
            "message": f"{platform} Cookie已失效,请重新登录",
            "timestamp": int(time.time()),
        }).encode("utf-8")
        notify_url = os.environ.get("PORTAL_NOTIFY_URL", "http://localhost:8000/api/notify")
        req = urllib.request.Request(
            notify_url,
            data=notif_data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                logger.info(f"[cookie_keepalive] cookie_expired通知推送成功: {platform}/{effective_tenant}")
            else:
                logger.warning(f"[cookie_keepalive] cookie_expired通知推送失败: HTTP {resp.status}")
    except Exception as ws_err:
        logger.warning(f"[cookie_keepalive] cookie_expired WebSocket通知异常(非致命): {ws_err}")


def _discover_tenants() -> dict[str, list[str]]:
    """扫描data/content/cookies/下所有租户目录

    返回 {tenant_id: [platform1, platform2, ...]}，仅含[a-zA-Z0-9_-]的子目录。
    用于cmd_run的--all-tenants模式,自动发现并保活所有租户的所有平台Cookie。
    """
    tenants: dict[str, list[str]] = {}
    if not COOKIES_DIR.exists():
        return tenants
    import re
    for entry in COOKIES_DIR.iterdir():
        if entry.is_dir() and re.match(r'^[a-zA-Z0-9_-]+$', entry.name):
            platforms = set()
            for json_file in entry.glob("*.json"):
                fname = json_file.stem
                if fname == "xianyu_cookies":
                    platforms.add("xianyu")
                elif "_" in fname:
                    plat = fname.split("_")[0]
                    if plat in KEEPALIVE_CONFIG:
                        platforms.add(plat)
            if platforms:
                tenants[entry.name] = sorted(platforms)
    return dict(sorted(tenants.items()))


async def cmd_run(platform: Optional[str] = None, account: str = "default", tenant_id: str = "", all_tenants: bool = False) -> None:
    """执行保活所有平台(或指定平台),支持租户隔离

    --all-tenants模式: 扫描data/content/cookies/下所有租户目录,
    对每个租户拥有的所有平台Cookie分别执行保活。

    Args:
        platform (Optional[str]): 参数说明
        account (str): 参数说明
        tenant_id (str): 参数说明
        all_tenants (bool): 参数说明
    """
    results = {}
    status = _load_keepalive_status()

    platforms_to_keep = [platform] if platform else list(KEEPALIVE_CONFIG.keys())

    # 多租户扫描模式: 对每个租户分别保活其拥有的所有平台Cookie
    # T-A07: 串行->并发保活(原930Cookie串行需7.75h,并发后约18.6min)
    if all_tenants:
        tenants_map = _discover_tenants()
        if tenants_map:
            logger.info(f"[cookie_keepalive] 发现{len(tenants_map)}个租户: {list(tenants_map.keys())}")

            # T-A07: 并发保活 - Semaphore控制最大并发,分批执行避免内存峰值
            semaphore = asyncio.Semaphore(MAX_CONCURRENT)
            # asyncio单线程模型: status字典在await点之间安全,_keepalive_for_tenant
            # 内部每个租户写入唯一tenant_id子键,无跨租户写冲突,无需额外锁

            async def _keepalive_tenant_task(tid: str, tid_platforms: list[str]) -> tuple[str, dict]:
                # 单个租户的保活任务(受信号量控制并发)
                # 内存监控: 内存>80%时暂停新任务(避免OOM)
                try:
                    import psutil
                    mem = psutil.virtual_memory()
                    if mem.percent > 80:
                        logger.warning(f"[cookie_keepalive] 内存使用{mem.percent}%>80%,暂停任务{tid}等待30s")
                        await asyncio.sleep(30)
                except ImportError as e:
                    logger.debug(f"psutil不可用,跳过内存检查: {e}")

                # 如果指定了--platform，只保活该平台(且租户拥有该平台)
                if platform:
                    tid_platforms = [p for p in tid_platforms if p == platform]
                if not tid_platforms:
                    return tid, {}

                async with semaphore:
                    tenant_results = await _keepalive_for_tenant(
                        tid_platforms, account, tid, status
                    )
                    return tid, tenant_results

            # 分批执行: BATCH_SIZE个租户一批,批间间隔BATCH_INTERVAL秒
            tenant_items = list(tenants_map.items())
            total_batches = (len(tenant_items) + BATCH_SIZE - 1) // BATCH_SIZE
            for batch_idx in range(total_batches):
                batch_start = batch_idx * BATCH_SIZE
                batch_end = min(batch_start + BATCH_SIZE, len(tenant_items))
                batch = tenant_items[batch_start:batch_end]

                # 批间间隔(第一批不等待)
                if batch_idx > 0:
                    logger.info(f"[cookie_keepalive] 批次{batch_idx + 1}/{total_batches}开始,等待{BATCH_INTERVAL}s(内存恢复)")
                    await asyncio.sleep(BATCH_INTERVAL)

                batch_tids = [t[0] for t in batch]
                logger.info(f"[cookie_keepalive] 执行批次{batch_idx + 1}/{total_batches}: 租户{batch_tids}")

                # 并发执行当前批次的所有租户保活任务
                tasks = [_keepalive_tenant_task(tid, tid_plats) for tid, tid_plats in batch]
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)

                for result in batch_results:
                    if isinstance(result, Exception):
                        logger.error(f"[cookie_keepalive] 租户保活任务异常: {result}", exc_info=True)
                    elif isinstance(result, tuple):
                        tid, tenant_results = result
                        for plat, res in tenant_results.items():
                            results[f"{plat}@{tid}"] = res
                            # T-A02: 保活失败时记录DOWNGRADE警告(R74.4降级标注)
                            if plat in PLATFORMS_NO_AUTO_RECOVERY:
                                if not res.get('success'):
                                    logger.warning(
                                        f"[DOWNGRADE] cookie_keepalive_failed: platform={plat}, "
                                        f"tenant={tid}, downgraded=True, reason=no_auto_recovery"
                                    )
                                elif res.get('success') and not res.get('is_logged_in') and not res.get('skipped'):
                                    logger.warning(
                                        f"[DOWNGRADE] cookie_keepalive_failed: platform={plat}, "
                                        f"tenant={tid}, downgraded=True, reason=no_auto_recovery"
                                    )

            # 保存状态
            _save_keepalive_status(status)
        else:
            logger.info("[cookie_keepalive] 未发现租户目录,回退到单用户模式")

    # 单租户保活(非--all-tenants模式)
    if not all_tenants:
        for plat in platforms_to_keep:
            # 闲鱼保活由下方独立块处理,此处跳过避免重复执行
            if plat == "xianyu":
                continue
            config = KEEPALIVE_CONFIG.get(plat)
            if not config:
                results[plat] = {"success": False, "error": f"无保活配置: {plat}"}
                continue

            # 检查是否需要保活(距上次保活不足间隔时间则跳过)
            # 兼容多租户模式写入的三层层级结构
            _plat_status = status.get(plat, {}).get(account, {})
            if isinstance(_plat_status, dict) and "last_keepalive" in _plat_status:
                last_keepalive = _plat_status.get("last_keepalive", "")
            elif isinstance(_plat_status, dict) and tenant_id and tenant_id in _plat_status:
                last_keepalive = _plat_status.get(tenant_id, {}).get("last_keepalive", "")
            else:
                last_keepalive = ""
            if last_keepalive:
                try:
                    last_time = datetime.fromisoformat(last_keepalive)
                    elapsed_hours = (datetime.now() - last_time).total_seconds() / 3600
                    if elapsed_hours < config["interval_hours"]:
                        results[plat] = {
                            "success": True,
                            "skipped": True,
                            "reason": f"距上次保活仅{elapsed_hours:.1f}小时,间隔{config['interval_hours']}小时",
                        }
                        continue
                except (ValueError, TypeError) as e:
                    logger.debug(f"[cookie_keepalive] 保活时间解析失败,将重新执行保活: {e}")
                    pass

            # 检查Cookie文件是否存在
            cookie_file = _get_cookie_file(plat, account, tenant_id)
            if not cookie_file.exists():
                results[plat] = {"success": False, "error": "Cookie文件不存在,需先登录"}
                continue

            # 执行Playwright保活
            result = await _playwright_keepalive(plat, account, tenant_id)
            results[plat] = result

            # 更新保活状态
            if plat not in status:
                status[plat] = {}
            if account not in status[plat]:
                status[plat][account] = {}
            status[plat][account]["last_keepalive"] = datetime.now().isoformat()
            status[plat][account]["is_logged_in"] = result.get("is_logged_in", False)
            status[plat][account]["last_result"] = "ok" if result.get("success") else result.get("error", "unknown")[:80]
            logger.info(f"[keepalive] {plat}/{account}: success={result.get('success')} logged_in={result.get('is_logged_in')} result={status[plat][account]['last_result']}")

            # Cookie失效时推送QQBot提醒
            if result.get("success") and not result.get("is_logged_in"):
                logger.warning(f"[keepalive] {plat}/{account}: Cookie已失效,触发_notify_expired")
                _notify_expired(plat, account, tenant_id)
                # T-A02: 无自动登录恢复的平台记录DOWNGRADE警告(R74.4降级标注)
                if plat in PLATFORMS_NO_AUTO_RECOVERY:
                    logger.warning(
                        f"[DOWNGRADE] cookie_keepalive_failed: platform={plat}, "
                        f"downgraded=True, reason=no_auto_recovery"
                    )
            elif not result.get("success") and plat in PLATFORMS_NO_AUTO_RECOVERY:
                # 保活执行失败且平台无自动恢复
                logger.warning(
                    f"[DOWNGRADE] cookie_keepalive_failed: platform={plat}, "
                    f"downgraded=True, reason=no_auto_recovery"
                )

        # 闲鱼单用户保活(非--all-tenants模式)
        if not all_tenants and (platform is None or platform == "xianyu"):
            plat = "xianyu"
            config = KEEPALIVE_CONFIG.get(plat)
            if config:
                last_keepalive = status.get(plat, {}).get(account, {}).get("last_keepalive", "")
                skip = False
                if last_keepalive:
                    try:
                        last_time = datetime.fromisoformat(last_keepalive)
                        elapsed_hours = (datetime.now() - last_time).total_seconds() / 3600
                        if elapsed_hours < config["interval_hours"]:
                            results[plat] = {
                                "success": True,
                                "skipped": True,
                                "reason": f"距上次保活仅{elapsed_hours:.1f}小时,间隔{config['interval_hours']}小时",
                            }
                            skip = True
                    except (ValueError, TypeError) as e:
                        logger.error(f"[cookie_keepalive] 保活时间解析失败,将重新执行保活: {e}")

                if not skip:
                    cookie_file = _get_cookie_file(plat, account, tenant_id)
                    if not cookie_file.exists():
                        results[plat] = {"success": False, "error": "Cookie文件不存在,需先登录"}
                    else:
                        result = await _playwright_keepalive(plat, account, tenant_id)
                        results[plat] = result

                        if plat not in status:
                            status[plat] = {}
                        if account not in status[plat]:
                            status[plat][account] = {}
                        status[plat][account]["last_keepalive"] = datetime.now().isoformat()
                        status[plat][account]["is_logged_in"] = result.get("is_logged_in", False)
                        status[plat][account]["last_result"] = "ok" if result.get("success") else result.get("error", "unknown")[:80]

                        if result.get("success") and not result.get("is_logged_in"):
                            _notify_expired(plat, account, tenant_id)
                            # T-A02: 闲鱼无自动登录恢复,记录DOWNGRADE警告(R74.4降级标注)
                            if plat in PLATFORMS_NO_AUTO_RECOVERY:
                                logger.warning(
                                    f"[DOWNGRADE] cookie_keepalive_failed: platform={plat}, "
                                    f"downgraded=True, reason=no_auto_recovery"
                                )

    _save_keepalive_status(status)
    json_out(True, {
        "keepalive_results": results,
        "executed_at": datetime.now().isoformat(),
        "all_tenants": all_tenants,
        "note": "Playwright保活: 访问创作者后台+导出storageState; B站使用refresh_token无需保活",
    })


async def _keepalive_for_tenant(platforms: list[str], account: str, tenant_id: str, status: dict) -> dict:
    """对指定租户执行保活(内部函数,供cmd_run的多租户模式调用)"""
    results = {}
    for plat in platforms:
        config = KEEPALIVE_CONFIG.get(plat)
        if not config:
            results[plat] = {"success": False, "error": f"无保活配置: {plat}"}
            continue

        # 检查是否需要保活
        last_keepalive = status.get(plat, {}).get(account, {}).get(tenant_id, {}).get("last_keepalive", "")
        if last_keepalive:
            try:
                last_time = datetime.fromisoformat(last_keepalive)
                elapsed_hours = (datetime.now() - last_time).total_seconds() / 3600
                if elapsed_hours < config["interval_hours"]:
                    results[plat] = {
                        "success": True,
                        "skipped": True,
                        "reason": f"距上次保活仅{elapsed_hours:.1f}小时,间隔{config['interval_hours']}小时",
                    }
                    continue
            except (ValueError, TypeError) as e:
                logger.error(f"[cookie_keepalive] 保活时间解析失败,将重新执行保活: {e}")

        # 检查Cookie文件
        cookie_file = _get_cookie_file(plat, account, tenant_id)
        if not cookie_file.exists():
            results[plat] = {"success": False, "error": f"Cookie文件不存在(tenant={tenant_id}),需先登录"}
            continue

        # 执行保活
        result = await _playwright_keepalive(plat, account, tenant_id)
        results[plat] = result

        # 更新状态(按tenant_id隔离)
        if plat not in status:
            status[plat] = {}
        if account not in status[plat]:
            status[plat][account] = {}
        if tenant_id not in status[plat][account]:
            status[plat][account][tenant_id] = {}
        status[plat][account][tenant_id]["last_keepalive"] = datetime.now().isoformat()
        status[plat][account][tenant_id]["is_logged_in"] = result.get("is_logged_in", False)
        status[plat][account][tenant_id]["last_result"] = "ok" if result.get("success") else result.get("error", "unknown")[:80]
        logger.info(f"[keepalive] {plat}/{account}/{tenant_id}: success={result.get('success')} logged_in={result.get('is_logged_in')} result={status[plat][account][tenant_id]['last_result']}")

        # Cookie失效时推送QQBot提醒
        if result.get("success") and not result.get("is_logged_in"):
            logger.warning(f"[keepalive] {plat}/{account}/{tenant_id}: Cookie已失效,触发_notify_expired")
            _notify_expired(plat, account, tenant_id=tenant_id)

    return results


async def cmd_export(platform: str, account: str = "default", tenant_id: str = "") -> None:
    """导出指定平台的storageState

    Args:
        platform (str): 参数说明
        account (str): 参数说明
        tenant_id (str): 参数说明
    """
    result = await _export_storage_state(platform, account, tenant_id)
    json_out(result.get("success", False), result)


async def cmd_login(platform: str, account: str = "default", tenant_id: str = "", timeout: int = 300) -> None:
    """扫码登录模式: 打开浏览器→导航到登录页→等待客户扫码→导出Cookie

    流程:
    1. 启动Playwright持久化上下文(使用user_data_dir)
    2. 导航到平台登录页(headless=False, 显示浏览器窗口供扫码)
    3. 等待用户扫码登录(最长timeout秒)
    4. 检测登录成功后导出storageState到Cookie JSON文件
    5. 关闭浏览器

    Args:
        platform (str): 参数说明
        account (str): 参数说明
        tenant_id (str): 参数说明
        timeout (int): 参数说明
    """
    config = KEEPALIVE_CONFIG.get(platform)
    if not config:
        json_out(False, error=f"不支持的平台: {platform}, 支持: {list(KEEPALIVE_CONFIG.keys())}", code="INVALID_PLATFORM")

    profile_dir = _get_profile_dir(platform, account, tenant_id)
    cookie_file = _get_cookie_file(platform, account, tenant_id)

    try:
        from patchright.async_api import async_playwright
    except ImportError:
        json_out(False, error="需要安装patchright: pip install patchright && patchright install chromium", code="MISSING_DEPENDENCY")

    pw = await async_playwright().start()
    try:
        # 启动持久化上下文(headless=False, 显示浏览器窗口供扫码)
        context = await pw.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=False,
            args=[],
        )

        page = await context.new_page()

        # 导航到登录页
        visit_url = config["visit_url"]
        try:
            await page.goto(visit_url, timeout=60000, wait_until="domcontentloaded")
        except Exception as e:
            logger.error(f"[cookie_keepalive] 登录页加载超时({platform}): {e}, 继续等待用户操作")

        # 等待用户扫码登录: 检测URL不再包含login_marker
        login_marker = config["login_marker"]
        start_time = time.time()
        is_logged_in = False

        while time.time() - start_time < timeout:
            current_url = page.url
            if login_marker not in current_url.lower():
                # 进一步验证: 检查页面内容是否有登录成功标记
                try:
                    page_content = await page.content()
                    content_lower = page_content[:5000].lower()
                    login_indicators = ["userinfo", "nickname", "avatar", "creator", "dashboard"]
                    logout_indicators = ["请登录", "立即登录", "sign in", "login-btn"]
                    has_login = any(ind in content_lower for ind in login_indicators)
                    has_logout = any(ind in content_lower for ind in logout_indicators)
                    if has_login or not has_logout:
                        is_logged_in = True
                        break
                except (RuntimeError, OSError) as e:
                    logger.error(f"[cookie_keepalive] 登录状态检查异常: {e}")
            # 每隔2秒检查一次
            await asyncio.sleep(2)

        if not is_logged_in:
            # 超时,仍然导出当前状态(可能用户已登录但检测不到)
            _ss = await context.storage_state()
            atomic_write_json(str(cookie_file), _ss)
            await context.close()
            json_out(False, error=f"扫码登录超时({timeout}秒),Cookie已导出但可能无效", code="LOGIN_TIMEOUT")

        # 登录成功,导出storageState
        _ss = await context.storage_state()
        atomic_write_json(str(cookie_file), _ss)
        await context.close()

        json_out(True, {
            "platform": platform,
            "account": account,
            "tenant_id": tenant_id,
            "is_logged_in": True,
            "cookie_file": str(cookie_file),
            "profile_dir": str(profile_dir),
            "message": f"{config['name']}扫码登录成功,Cookie已导出",
        })

    except (RuntimeError, OSError, KeyError, TimeoutError) as e:
        logger.error(f"[cookie_keepalive] 扫码登录异常({platform}): {e}")
        json_out(False, error=f"扫码登录异常: {str(e)[:150]}", code="LOGIN_ERROR")
    finally:
        await pw.stop()


def cmd_status() -> None:
    """查看保活状态"""
    status = _load_keepalive_status()

    # 补充Cookie文件信息
    cookie_info = {}
    for plat in KEEPALIVE_CONFIG:
        cookie_file = _get_cookie_file(plat, "default")
        if cookie_file.exists():
            try:
                stat = cookie_file.stat()
                age_hours = (datetime.now() - datetime.fromtimestamp(stat.st_mtime)).total_seconds() / 3600
                cookie_info[plat] = {
                    "cookie_exists": True,
                    "cookie_age_hours": round(age_hours, 1),
                    "cookie_size": stat.st_size,
                }
            except (OSError, ValueError) as e:
                logger.debug(f"[cookie_keepalive] Cookie文件信息读取失败({plat}): {e}")
                cookie_info[plat] = {"cookie_exists": True}
        else:
            cookie_info[plat] = {"cookie_exists": False}

    # 补充profile信息
    profile_info = {}
    for plat in KEEPALIVE_CONFIG:
        profile_dir = _get_profile_dir(plat, "default")
        if profile_dir.exists() and any(profile_dir.iterdir()):
            profile_info[plat] = {"profile_exists": True}
        else:
            profile_info[plat] = {"profile_exists": False}

    json_out(True, {
        "keepalive_status": status,
        "cookie_info": cookie_info,
        "profile_info": profile_info,
        "config": {k: {"name": v["name"], "interval_hours": v["interval_hours"]} for k, v in KEEPALIVE_CONFIG.items()},
    })


# ============================================================
# BUG-V4-021: cookie_keepalive_detail.py合并到此文件
# Cookie 30天保活细节治理(来源: v8.0方案§5.2.5 OPS-5)
# ============================================================

PROACTIVE_REFRESH_INTERVAL_HOURS = 6
REACTIVE_REFRESH_ON_FAILURE = True
HEALTH_SCORE_REFRESH_THRESHOLD = 60
RISK_DETECTION_THRESHOLD = 3
RISK_DEGRADE_MULTIPLIER = 2
MAX_REFRESH_RETRY = 3

_DETAIL_STATE_DIR = Path(os.environ.get("JUEJIN_HOME", str(Path(__file__).resolve().parent.parent.parent.parent))) / "data" / "cookie_keepalive"
_DETAIL_STATE_FILE = _DETAIL_STATE_DIR / "keepalive_state.json"


class CookieKeepaliveDetail:
    """Cookie 30天保活细节管理器(来源: v8.0 OPS-5 §5.2.5, BUG-V4-021合并)"""

    def __init__(self):
        try:
            from check_cookie_health import CookieHealthScorer  # v25.0: 合并自cookie_health_scorer.py
            self.health_scorer = CookieHealthScorer()
        except ImportError:
            self.health_scorer = None
            logger.error("check_cookie_health.CookieHealthScorer不可用,健康度检查将跳过")
        _DETAIL_STATE_DIR.mkdir(parents=True, exist_ok=True)

    async def proactive_refresh(self, tenant_id: str, platform: str, account: str="default") -> dict[str, Any]:
        """主动刷新: 每6小时检查健康度, <60分触发刷新

        Args:
            tenant_id (str): 参数说明
            platform (str): 参数说明
            account (str): 参数说明

        Returns:
            dict[str, Any]: 返回值说明
        """
        try:
            if self.health_scorer:
                health_result = await self.health_scorer.score(tenant_id, platform, account)
                if not health_result.get("success"):
                    return health_result
                health_data = health_result["data"]
                total_score = health_data.get("total_score", 0)
            else:
                total_score = 100  # 无health_scorer时默认健康

            last_refresh = self._get_last_refresh(tenant_id, platform, account)
            hours_since = self._hours_since(last_refresh) if last_refresh else PROACTIVE_REFRESH_INTERVAL_HOURS + 1
            need_refresh = total_score < HEALTH_SCORE_REFRESH_THRESHOLD or hours_since >= PROACTIVE_REFRESH_INTERVAL_HOURS

            if not need_refresh:
                return {"success": True, "data": {"refreshed": False, "health_score": total_score, "action": "monitor",
                        "reason": f"健康度{total_score}+最近刷新{hours_since:.1f}h, 无需刷新"}, "error": None, "code": None}

            refresh_result = await self._do_refresh(tenant_id, platform, account)
            if refresh_result.get("success"):
                self._record_refresh(tenant_id, platform, account, success=True)
            else:
                self._record_refresh(tenant_id, platform, account, success=False, error=refresh_result.get("error", "unknown"))

            return {"success": refresh_result.get("success", False),
                    "data": {"refreshed": refresh_result.get("success", False), "health_score": total_score,
                             "action": "refreshed" if refresh_result.get("success") else "refresh_failed",
                             "reason": refresh_result.get("error", "主动刷新完成")},
                    "error": refresh_result.get("error"), "code": refresh_result.get("code")}
        except Exception as e:
            logger.error(f"proactive_refresh异常: {e}", exc_info=True)
            return {"success": False, "data": {}, "error": str(e), "code": "PROACTIVE_REFRESH_EXCEPTION"}

    async def reactive_refresh(self, tenant_id: str, platform: str, account: str="default", failure_reason: str="") -> dict[str, Any]:
        """被动刷新: 失效后立即触发刷新

        Args:
            tenant_id (str): 参数说明
            platform (str): 参数说明
            account (str): 参数说明
            failure_reason (str): 参数说明

        Returns:
            dict[str, Any]: 返回值说明
        """
        try:
            logger.warning(f"被动刷新触发: tenant={tenant_id} platform={platform} account={account} reason={failure_reason}")
            refresh_result = await self._do_refresh_with_retry(tenant_id, platform, account)
            if refresh_result.get("success"):
                self._record_refresh(tenant_id, platform, account, success=True, trigger="reactive")
                return {"success": True, "data": {"refreshed": True, "trigger": "reactive", "reason": failure_reason}, "error": None, "code": None}
            else:
                self._record_refresh(tenant_id, platform, account, success=False, trigger="reactive", error=refresh_result.get("error"))
                return refresh_result
        except Exception as e:
            logger.error(f"reactive_refresh异常: {e}", exc_info=True)
            return {"success": False, "data": {}, "error": str(e), "code": "REACTIVE_REFRESH_EXCEPTION"}

    async def _do_refresh(self, tenant_id, platform, account):
        """执行Cookie刷新(直接调用本文件的_playwright_keepalive, BUG-V4-021合并)

        P1-04修复: patchright不可用(ImportError)时通过subprocess调用cookie_keepalive.py run
        """
        try:
            # 尝试直接调用_playwright_keepalive(需要patchright)
            from patchright.async_api import async_playwright  # noqa: F401
            result = await _playwright_keepalive(platform=platform, account=account, tenant_id=tenant_id)
            if isinstance(result, dict) and result.get("success"):
                return {"success": True, "data": result, "error": None, "code": None}
            else:
                error_msg = result.get("error", "保活失败") if isinstance(result, dict) else str(result)
                return {"success": False, "data": {}, "error": error_msg, "code": "KEEPALIVE_FAILED"}
        except ImportError:
            # P1-04修复: subprocess调用cookie_keepalive.py run子命令
            try:
                proc = await asyncio.create_subprocess_exec(
                    sys.executable,
                    str(Path(__file__)),  # cookie_keepalive.py
                    "run",
                    "--platform", platform,
                    "--account", account,
                    "--tenant_id", tenant_id,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=300)
                if proc.returncode == 0:
                    result = json.loads(stdout.decode("utf-8")) if stdout else {}
                    return {"success": True, "data": result, "error": None, "code": None}
                else:
                    logger.error(f"cookie keepalive subprocess失败 returncode={proc.returncode}: {stderr.decode('utf-8', errors='replace')[:200]}")
                    return {"success": False, "data": {}, "error": f"subprocess返回非零退出码 returncode={proc.returncode}", "code": "KEEPALIVE_SUBPROCESS_FAILED"}
            except asyncio.TimeoutError:
                logger.error(f"cookie keepalive subprocess超时(300秒): tenant={tenant_id} platform={platform}")
                return {"success": False, "data": {}, "error": "subprocess执行超时(300秒)", "code": "KEEPALIVE_SUBPROCESS_TIMEOUT"}
            except Exception as sub_e:
                logger.error(f"cookie keepalive subprocess启动失败: {sub_e}", exc_info=True)
                return {"success": False, "data": {}, "error": f"subprocess启动失败: {sub_e}", "code": "COOKIE_KEEPALIVE_UNAVAILABLE"}
        except Exception as e:
            logger.error(f"_do_refresh异常: {e}", exc_info=True)
            return {"success": False, "data": {}, "error": str(e), "code": "REFRESH_EXCEPTION"}

    async def _do_refresh_with_retry(self, tenant_id, platform, account):
        """带重试的刷新(最大MAX_REFRESH_RETRY次)"""
        last_error = None
        for attempt in range(1, MAX_REFRESH_RETRY + 1):
            try:
                result = await self._do_refresh(tenant_id, platform, account)
                if result.get("success"):
                    return result
                last_error = result.get("error", "unknown")
                logger.warning(f"刷新失败(尝试{attempt}/{MAX_REFRESH_RETRY}): {last_error}")
                if attempt < MAX_REFRESH_RETRY:
                    await asyncio.sleep(2 ** attempt)
            except Exception as e:
                last_error = str(e)
                logger.error(f"刷新异常(尝试{attempt}/{MAX_REFRESH_RETRY}): {e}")
        return {"success": False, "data": {}, "error": f"重试{MAX_REFRESH_RETRY}次仍失败: {last_error}", "code": "MAX_RETRY_EXCEEDED"}

    def _get_last_refresh(self, tenant_id, platform, account):
        try:
            state = self._load_state()
            key = f"{tenant_id}_{platform}_{account}"
            return state.get("refresh_records", {}).get(key, {}).get("last_refresh")
        except Exception as e:
            logger.warning(f"Unexpected error: {e}", exc_info=True)
            return None

    def _hours_since(self, iso_time):
        try:
            dt = datetime.fromisoformat(iso_time)
            return (datetime.now() - dt).total_seconds() / 3600
        except (ValueError, TypeError):
            return float("inf")

    def _record_refresh(self, tenant_id, platform, account, success, trigger="proactive", error=None):
        try:
            state = self._load_state()
            key = f"{tenant_id}_{platform}_{account}"
            records = state.setdefault("refresh_records", {})
            records[key] = {
                "last_refresh": datetime.now().isoformat(),
                "success": success, "trigger": trigger, "error": error,
                "consecutive_failures": records.get(key, {}).get("consecutive_failures", 0) + 1 if not success else 0,
            }
            if records[key]["consecutive_failures"] >= RISK_DETECTION_THRESHOLD:
                records[key]["degraded"] = True
                records[key]["degrade_multiplier"] = RISK_DEGRADE_MULTIPLIER
                logger.warning(f"风控触发降频: {key} 连续失败{records[key]['consecutive_failures']}次")
            state["refresh_records"][key] = records[key]
            self._save_state(state)
        except Exception as e:
            logger.error(f"_record_refresh异常: {e}", exc_info=True)

    def _load_state(self):
        try:
            from mcps.shared.atomic_write import atomic_read_json
            return atomic_read_json(_DETAIL_STATE_FILE, default={"refresh_records": {}})
        except Exception as e:
            logger.warning(f"Unexpected error: {e}", exc_info=True)
            return {"refresh_records": {}}

    def _save_state(self, state):
        atomic_write_json(_DETAIL_STATE_FILE, state)


async def _detail_proactive_all_tenants():
    """Cron入口: 对所有租户所有平台执行主动刷新检查(BUG-V4-021合并)"""
    from mcps.shared.cookie_manager import _discover_tenants
    manager = CookieKeepaliveDetail()
    tenants = _discover_tenants()
    results = []
    for tenant_id in tenants:
        cookie_dir = Path(os.environ.get("JUEJIN_HOME", str(PROJECT_ROOT))) / "data" / "content" / "cookies" / tenant_id
        if not cookie_dir.exists():
            continue
        for cookie_file in cookie_dir.glob("*.json"):
            # BUG-15修复: 跳过非标准Cookie文件(如xianyu_cookies.json)
            stem = cookie_file.stem
            if stem in ("xianyu_cookies", "cookie_locks"):
                continue
            platform = stem.rsplit("_", 1)[0]
            account = stem.rsplit("_", 1)[1] if "_" in stem else "default"
            result = await manager.proactive_refresh(tenant_id, platform, account)
            results.append({"tenant": tenant_id, "platform": platform, "account": account, "result": result})
    print(json.dumps({"success": True, "data": {"total": len(results), "results": results}, "error": None, "code": None}, ensure_ascii=False, indent=2))


def main():
    """main"""
    parser = argparse.ArgumentParser(description="Cookie Playwright保活引擎 v1.0 (BUG-V4-021: 合并cookie_keepalive_detail+cookie_utils)")
    sub = parser.add_subparsers(dest="command")

    run_parser = sub.add_parser("run", help="执行保活")
    run_parser.add_argument("--platform", choices=list(KEEPALIVE_CONFIG.keys()), help="指定平台(默认全部)")
    run_parser.add_argument("--account", default="default", help="账号名(默认default)")
    run_parser.add_argument("--tenant_id", default="", help="租户ID(代运营场景,用于Cookie/profile隔离)")
    run_parser.add_argument("--all-tenants", action="store_true", help="扫描所有租户目录,对每个租户的所有平台Cookie分别保活")

    export_parser = sub.add_parser("export", help="导出storageState")
    export_parser.add_argument("--platform", required=True, choices=list(KEEPALIVE_CONFIG.keys()))
    export_parser.add_argument("--account", default="default")
    export_parser.add_argument("--tenant_id", default="", help="租户ID(代运营场景,用于Cookie/profile隔离)")

    login_parser = sub.add_parser("login", help="扫码登录(打开浏览器等待扫码)")
    login_parser.add_argument("--platform", required=True, choices=list(KEEPALIVE_CONFIG.keys()))
    login_parser.add_argument("--account", default="default")
    login_parser.add_argument("--tenant_id", default="", help="租户ID(代运营场景,用于Cookie/profile隔离)")
    login_parser.add_argument("--timeout", type=int, default=300, help="扫码等待超时秒数(默认300)")

    sub.add_parser("status", help="查看保活状态")

    # BUG-V4-021: 合并cookie_keepalive_detail的子命令
    detail_parser = sub.add_parser("detail", help="保活细节治理(来源: cookie_keepalive_detail合并)")
    detail_sub = detail_parser.add_subparsers(dest="detail_cmd")
    p_proactive = detail_sub.add_parser("proactive", help="主动刷新检查")
    p_proactive.add_argument("--tenant", required=True)
    p_proactive.add_argument("--platform", required=True)
    p_proactive.add_argument("--account", default="default")
    p_reactive = detail_sub.add_parser("reactive", help="被动刷新(失效后立即)")
    p_reactive.add_argument("--tenant", required=True)
    p_reactive.add_argument("--platform", required=True)
    p_reactive.add_argument("--account", default="default")
    p_reactive.add_argument("--reason", default="")
    detail_sub.add_parser("proactive-all", help="对所有租户执行主动刷新(Cron入口)")

    args = parser.parse_args()

    if args.command == "run":
        # Phase 12.7: IdempotencyChecker集成 - 防止Cron重复执行
        from idempotency_checker import check_idempotent, record_idempotent
        from datetime import datetime as _dt
        _idem_key = f"cron-cookie-keepalive-{_dt.now().strftime('%Y-%m-%d')}-{args.platform or 'all'}"
        if check_idempotent(_idem_key, task_id="cookie-keepalive-daily", tenant_id="system"):
            logger.info(f"任务已执行，跳过(idempotency_check): {_idem_key}")
            print(json.dumps({"success": True, "data": {"skipped": True, "reason": "idempotency_check", "key": _idem_key}, "error": None, "code": "IDEMPOTENT_SKIP"}))
            return
        asyncio.run(cmd_run(args.platform, args.account, args.tenant_id, args.all_tenants))
        # Phase 12.7: 记录幂等键(任务成功完成后)
        record_idempotent(_idem_key, task_id="cookie-keepalive-daily", tenant_id="system")
    elif args.command == "export":
        asyncio.run(cmd_export(args.platform, args.account, args.tenant_id))
    elif args.command == "login":
        asyncio.run(cmd_login(args.platform, args.account, args.tenant_id, args.timeout))
    elif args.command == "status":
        cmd_status()
    elif args.command == "detail":
        manager = CookieKeepaliveDetail()
        if args.detail_cmd == "proactive":
            result = asyncio.run(manager.proactive_refresh(args.tenant, args.platform, args.account))
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.detail_cmd == "reactive":
            result = asyncio.run(manager.reactive_refresh(args.tenant, args.platform, args.account, args.reason))
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.detail_cmd == "proactive-all":
            asyncio.run(_detail_proactive_all_tenants())
        else:
            detail_parser.print_help()
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
