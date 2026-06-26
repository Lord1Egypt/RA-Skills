#!/usr/bin/env python3
import os
import sys
import json
import argparse
import asyncio
import importlib
import inspect
import yaml
from datetime import datetime
from typing import Dict, List, Callable, Optional
from urllib.parse import urlparse

# 导入scripts目录到模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置文件路径（YAML 格式）
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml')
LEGACY_JSON_CONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

def generate_task_id() -> str:
    """生成任务ID：YYYYMMDDHHMMSS格式的时间戳"""
    return datetime.now().strftime("%Y%m%d%H%M%S")

def get_site_from_url(url: str, config: dict) -> tuple[str, dict]:
    """
    根据URL匹配对应的站点配置
    匹配顺序：精确站点匹配 > 通用节点(general) > unknown
    返回：(站点标识, 站点配置字典)
    """
    try:
        # 提取URL域名
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()

        fetch_site_config = config.get('fetch_site', {})
        # 第一优先级：精确匹配站点
        for site_key, site_config in fetch_site_config.items():
            # 跳过全局配置和通用节点
            if site_key == 'proxy' or site_key == 'general':
                continue
            # 检查domain匹配
            site_domain = site_config.get('domain', '').lower()
            if site_domain and site_domain in domain:
                return site_key, site_config

        # 第二优先级：使用通用节点
        if 'general' in fetch_site_config:
            return 'general', fetch_site_config['general']
    except Exception:
        pass

    # 最后 fallback 到unknown
    return 'unknown', {}

def load_config() -> dict:
    """加载配置文件（优先 config.yaml，其次兼容旧的 config.json）"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
                print(f"✅ 成功加载配置文件: {CONFIG_FILE}")
                return config
        except Exception as e:
            print(f"⚠️ 配置文件读取失败: {e}，将使用默认配置")
            return {}

    # 兼容旧版 config.json：自动迁移到 config.yaml
    if os.path.exists(LEGACY_JSON_CONFIG):
        try:
            with open(LEGACY_JSON_CONFIG, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"ℹ️ 检测到旧版 {os.path.basename(LEGACY_JSON_CONFIG)}，正在迁移到 {os.path.basename(CONFIG_FILE)}...")
            save_config(config)
            return config
        except Exception as e:
            print(f"⚠️ 旧版 JSON 配置迁移失败: {e}")
    return {}

def save_config(config: dict):
    """以 YAML 格式保存配置到文件"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            yaml.safe_dump(
                config, f,
                allow_unicode=True,
                sort_keys=False,
                default_flow_style=False,
                indent=2,
            )
        print(f"✅ 配置已保存到: {CONFIG_FILE}，下次运行将自动读取")
    except Exception as e:
        print(f"⚠️ 配置保存失败: {e}")

def prompt_input(prompt: str, default: str = None) -> str:
    """提示用户输入，有默认值时显示默认值，非交互环境下直接返回默认值"""
    try:
        if default:
            user_input = input(f"  {prompt} \033[90m[默认: {default}]\033[0m: ").strip()
            return user_input if user_input else default
        else:
            while True:
                user_input = input(f"  {prompt}: ").strip()
                if user_input:
                    return user_input
                print("  ⚠️ 输入不能为空，请重新输入")
    except EOFError:
        # 非交互环境下，有默认值直接返回，否则报错
        if default is not None:
            print(f"\n⚠️ 非交互环境，使用默认值: {default}")
            return default
        else:
            print(f"\n❌ 非交互环境下必须通过命令行参数或配置文件提供 {prompt}")
            print("💡 使用方式: python workflow.py --url 推文链接 [--proxy 代理地址] [--cookies Cookie文件路径]")
            sys.exit(1)

def print_step(step: int, total: int, title: str):
    """打印步骤标题，带统一的视觉样式"""
    print(f"\n\033[36m━━━ 步骤 {step}/{total}: {title} ━━━\033[0m")

def print_section(title: str):
    """打印分节标题"""
    print(f"\n\033[1m{title}\033[0m")

def is_valid_url(url: str) -> bool:
    """简单校验 URL 是否合法（http/https 开头且有 host）"""
    try:
        p = urlparse(url)
        return p.scheme in ('http', 'https') and bool(p.netloc)
    except Exception:
        return False

def prompt_url(default: str = '') -> str:
    """提示输入 URL 并校验，循环直到拿到合法值"""
    while True:
        url = prompt_input("请输入要爬取的页面 URL", default if default else None)
        if is_valid_url(url):
            return url
        print(f"  ⚠️ URL 格式无效，需以 http:// 或 https:// 开头：{url}")

def prompt_proxy(default: str = 'http://127.0.0.1:17890') -> str:
    """提示输入代理，输入 none 表示不使用代理，返回处理后的代理地址（空串表示不用）"""
    proxy = prompt_input("代理地址（输入 none 表示不使用代理）", default)
    return '' if proxy.lower() == 'none' else proxy

def open_file_dialog(title: str = "选择文件", filetypes: list = None) -> str:
    """尝试打开系统文件选择对话框，返回选中的文件路径。无 GUI 环境返回空串。"""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        ft = filetypes or [("JSON 文件", "*.json"), ("所有文件", "*.*")]
        path = filedialog.askopenfilename(title=title, filetypes=ft)
        root.destroy()
        return path or ''
    except Exception:
        return ''

def prompt_cookies(site_key: str) -> str:
    """提示输入 Cookie 文件路径，支持文件对话框选择，循环到文件存在为止"""
    default_cookies = {
        'twitter': 'x_cookie.json',
        'zhihu': 'zhihu_cookie.json',
        'toutiao': 'toutiao_cookie.json',
        'huxiu': 'huxiu_cookie.json',
    }.get(site_key, 'cookies.json')
    print(f"  💡 该站点需要登录态，请使用浏览器扩展（如 EditThisCookie）导出 Cookie JSON 文件")
    print(f"  💡 输入 [dialog] 可打开文件选择对话框")
    cookies = prompt_input("Cookie 文件路径", default_cookies)
    if cookies.lower().strip() == '[dialog]':
        selected = open_file_dialog(title=f"选择 {site_key} 的 Cookie 文件")
        if selected:
            cookies = selected
            print(f"  ✅ 已选择: {cookies}")
        else:
            print(f"  ⚠️ 未选择文件，请手动输入路径")
            cookies = prompt_input("Cookie 文件路径", default_cookies)
    while not os.path.exists(cookies):
        print(f"  ⚠️ Cookie 文件不存在：{cookies}")
        print(f"  💡 输入 [dialog] 可打开文件选择对话框")
        cookies = prompt_input("请重新输入 Cookie 文件路径")
        if cookies.lower().strip() == '[dialog]':
            selected = open_file_dialog(title=f"选择 {site_key} 的 Cookie 文件")
            if selected:
                cookies = selected
                print(f"  ✅ 已选择: {cookies}")
            else:
                print(f"  ⚠️ 未选择文件")
                cookies = ''
    return cookies

def diff_config(old: dict, new: dict, prefix: str = '') -> List[str]:
    """递归对比两个配置字典，返回变更列表（用于保存前预览）"""
    changes = []
    all_keys = set(old.keys()) | set(new.keys())
    for k in sorted(all_keys):
        path = f"{prefix}.{k}" if prefix else k
        ov, nv = old.get(k), new.get(k)
        if isinstance(ov, dict) and isinstance(nv, dict):
            changes.extend(diff_config(ov, nv, path))
        elif ov != nv:
            if ov is None:
                changes.append(f"  \033[32m+ {path}: {nv}\033[0m")
            elif nv is None:
                changes.append(f"  \033[31m- {path}: {ov}\033[0m")
            else:
                changes.append(f"  \033[33m~ {path}: {ov} → {nv}\033[0m")
    return changes

# ──────────────── Cookie 导入子命令 ────────────────

COOKIES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cookies')
KNOWN_SITES = ['twitter', 'zhihu', 'wechat', 'toutiao', 'huxiu', 'general']

def validate_cookie_json(file_path: str) -> tuple[bool, str]:
    """校验 Cookie JSON 文件格式，返回 (是否有效, 错误信息)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"JSON 解析失败: {e}"
    except Exception as e:
        return False, f"文件读取失败: {e}"

    if not isinstance(data, list):
        return False, "Cookie 文件应为 JSON 数组（列表），当前为其他类型"

    if len(data) == 0:
        return False, "Cookie 列表为空"

    # 检查第一个 cookie 是否有必要字段
    sample = data[0]
    if not isinstance(sample, dict):
        return False, "Cookie 列表中的元素应为对象（字典）"
    if 'name' not in sample or 'value' not in sample:
        return False, "Cookie 缺少必要字段 name/value"

    return True, f"有效，共 {len(data)} 个 Cookie 条目"

def import_cookie(file_path: str, site: str, auto_detect: bool = True) -> bool:
    """
    导入 Cookie 文件到项目中并更新 config.yaml。
    1. 校验 JSON 格式
    2. 复制到 cookies/ 目录
    3. 更新 config.yaml 中对应站点的 cookies_path
    返回是否成功。
    """
    import shutil

    # 校验文件存在
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False

    # 校验格式
    valid, msg = validate_cookie_json(file_path)
    if not valid:
        print(f"❌ Cookie 文件格式无效: {msg}")
        return False
    print(f"✅ Cookie 格式校验通过: {msg}")

    # 自动检测站点（从文件名推断）
    if not site and auto_detect:
        basename = os.path.basename(file_path).lower()
        for s in KNOWN_SITES:
            if s in basename or (s == 'twitter' and 'x_' in basename):
                site = s
                print(f"ℹ️ 从文件名自动识别站点: {site}")
                break

    if not site:
        print("❌ 无法确定目标站点，请通过 --site 参数指定")
        print(f"   可选站点: {', '.join(KNOWN_SITES)}")
        return False

    if site not in KNOWN_SITES:
        print(f"⚠️ 未知站点 '{site}'，将作为新站点添加到配置")

    # 复制文件到 cookies/ 目录
    os.makedirs(COOKIES_DIR, exist_ok=True)
    dest_filename = f"{site}_cookie.json"
    dest_path = os.path.join(COOKIES_DIR, dest_filename)
    shutil.copy2(file_path, dest_path)
    print(f"✅ Cookie 文件已复制到: {dest_path}")

    # 更新 config.yaml
    config = load_config()
    if 'fetch_site' not in config:
        config['fetch_site'] = {}
    if site not in config['fetch_site']:
        config['fetch_site'][site] = {}

    # 使用相对路径
    rel_path = os.path.join('cookies', dest_filename)
    old_path = config['fetch_site'][site].get('cookies_path', '')
    config['fetch_site'][site]['cookies_path'] = rel_path
    save_config(config)

    # 输出摘要
    print_section("📋 导入完成")
    print(f"  站点:       {site}")
    print(f"  源文件:     {file_path}")
    print(f"  存储位置:   {rel_path}")
    if old_path and old_path != rel_path:
        print(f"  旧路径:     {old_path} (已替换)")
    print(f"\n💡 下次运行 workflow.py 抓取 {site} 站点时将自动使用此 Cookie")
    return True

def create_output_dir(site_key: str, task_id: str) -> str:
    """创建任务输出目录，返回目录路径：fetch_data/{站点标识}/{任务ID}"""
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fetch_data", site_key, task_id)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def load_site_scraper(site_key: str) -> Optional[Callable]:
    """
    动态加载对应站点的爬取脚本
    脚本命名规则：scrape_{站点标识}.py，如scrape_twitter.py
    必须导出scrape_task异步函数
    """
    try:
        # 尝试导入对应站点的爬取模块
        module_name = f"scripts.scrape_{site_key}"
        scraper_module = importlib.import_module(module_name)

        # 检查是否有scrape_task函数
        if hasattr(scraper_module, 'scrape_task') and inspect.iscoroutinefunction(scraper_module.scrape_task):
            return scraper_module.scrape_task
        else:
            print(f"⚠️ 站点 {site_key} 的爬取脚本未导出有效的scrape_task异步函数")
    except ImportError:
        print(f"⚠️ 未找到站点 {site_key} 对应的爬取脚本 scripts/scrape_{site_key}.py")
    except Exception as e:
        print(f"⚠️ 加载站点 {site_key} 爬取脚本失败: {e}")

    return None

def save_result(output_dir: str, result: List[Dict]) -> str:
    """保存爬取结果到JSON文件，返回文件路径"""
    result_file = os.path.join(output_dir, "result.json")
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return result_file

async def main():
    parser = argparse.ArgumentParser(description="多站点内容抓取工作流入口")
    parser.add_argument("--proxy", help="代理地址，例如：http://127.0.0.1:17890；传 none 表示不使用代理")
    parser.add_argument("--url", help="要爬取的页面 URL")
    parser.add_argument("--cookies", help="Cookie 文件路径（JSON 格式）")
    parser.add_argument("--headless", action="store_true", default=None, help="是否使用无头模式，默认开启")
    parser.add_argument("--no-save-config", action="store_true", help="不保存当前配置到文件")
    parser.add_argument("--import-cookie", metavar="FILE", help="导入 Cookie 文件：校验格式、复制到 cookies/ 目录、更新 config.yaml")
    parser.add_argument("--site", help="配合 --import-cookie 使用，指定目标站点（twitter/zhihu/wechat/toutiao/huxiu/general）")

    args = parser.parse_args()

    # ──────────────── 子命令：导入 Cookie ────────────────
    if args.import_cookie:
        success = import_cookie(args.import_cookie, args.site)
        sys.exit(0 if success else 1)

    # 加载已有配置
    config = load_config()
    SITES_REQUIRING_COOKIE = ['twitter', 'zhihu']

    # ──────────────── 步骤 1：确定目标 URL ────────────────
    print_step(1, 5, "目标页面")
    url = args.url or config.get('default_url') or ''
    if args.url:
        if not is_valid_url(args.url):
            print(f"  ❌ 命令行传入的 URL 无效：{args.url}")
            sys.exit(1)
        print(f"  ✅ 使用命令行 URL: {url}")
    else:
        url = prompt_url(default=url)

    # ──────────────── 步骤 2：识别站点 ────────────────
    print_step(2, 5, "站点识别")
    site_key, site_config = get_site_from_url(url, config)
    if site_key == 'unknown':
        print(f"  ⚠️ 未匹配到站点配置，输出将保存到 fetch_data/unknown/")
    elif site_key == 'general':
        print(f"  📍 未匹配到专属脚本，使用通用爬取模式（general）")
    else:
        print(f"  📍 匹配站点: \033[1m{site_key}\033[0m (domain: {site_config.get('domain', '-')})")

    # ──────────────── 步骤 3：代理设置 ────────────────
    print_step(3, 5, "代理设置")
    proxy = args.proxy or site_config.get('proxy') or config.get('fetch_site', {}).get('proxy')
    if args.proxy:
        proxy = '' if args.proxy.lower() == 'none' else args.proxy
        print(f"  ✅ 使用命令行代理: {proxy or '(不使用代理)'}")
    elif proxy:
        proxy = '' if proxy.lower() == 'none' else proxy
        print(f"  ✅ 使用配置中的代理: {proxy or '(不使用代理)'}")
    else:
        proxy = prompt_proxy()

    # ──────────────── 步骤 4：Cookie 设置 ────────────────
    print_step(4, 5, "Cookie 设置")
    cookies = args.cookies or site_config.get('cookies_path') or ''
    if site_key in SITES_REQUIRING_COOKIE:
        if cookies and os.path.exists(cookies):
            print(f"  ✅ 使用 Cookie 文件: {cookies}")
        else:
            if cookies:
                print(f"  ⚠️ 配置中的 Cookie 文件不存在：{cookies}")
            cookies = prompt_cookies(site_key)
    else:
        if cookies and os.path.exists(cookies):
            print(f"  ✅ 使用 Cookie 文件: {cookies}")
        else:
            print(f"  ℹ️ 该站点 Cookie 可选，跳过")
            cookies = ''

    # ──────────────── 步骤 5：高级选项 & 配置预览 ────────────────
    print_step(5, 5, "高级选项")
    headless = args.headless if args.headless is not None else config.get('headless', True)
    print(f"  无头模式: {'开启' if headless else '关闭'}")

    print_section("📋 本次运行配置预览")
    print(f"  URL:      {url}")
    print(f"  站点:     {site_key}")
    print(f"  代理:     {proxy or '(不使用)'}")
    print(f"  Cookie:   {cookies or '(无)'}")
    print(f"  无头模式: {'开启' if headless else '关闭'}")

    # ──────────────── 配置保存（变更确认） ────────────────
    if not args.no_save_config:
        new_config = config.copy()
        if 'fetch_site' not in new_config:
            new_config['fetch_site'] = {}
        new_config['fetch_site']['proxy'] = 'none' if proxy == '' else proxy

        if site_key != 'unknown':
            if site_key not in new_config['fetch_site']:
                new_config['fetch_site'][site_key] = {}
            existing_domain = new_config['fetch_site'][site_key].get('domain', site_config.get('domain', ''))
            update_config = {
                'proxy': 'none' if proxy == '' else proxy,
                'cookies_path': cookies,
            }
            if site_key != 'general' and existing_domain:
                update_config['domain'] = existing_domain
            new_config['fetch_site'][site_key].update(update_config)

        new_config['headless'] = headless
        new_config['default_url'] = url

        if new_config != config:
            changes = diff_config(config, new_config)
            print_section("📝 配置变更")
            for line in changes:
                print(line)
            try:
                save = input(f"\n💾 保存以上变更到 {os.path.basename(CONFIG_FILE)}？下次运行可跳过提问 (y/N): ").strip().lower()
                if save in ['y', 'yes', '是']:
                    save_config(new_config)
                else:
                    print("  ℹ️ 本次不保存配置")
            except EOFError:
                pass

    # ──────────────── 执行抓取任务 ────────────────
    task_id = generate_task_id()
    output_dir = create_output_dir(site_key, task_id)
    print_section("🚀 开始执行抓取任务")
    print(f"  任务 ID:   {task_id}")
    print(f"  输出目录: {output_dir}")

    # 3. 执行爬取任务
    print("🚀 开始执行爬取任务...")
    try:
        # 动态加载对应站点的爬取脚本
        scraper_func = load_site_scraper(site_key)
        if not scraper_func:
            print(f"❌ 未找到站点 {site_key} 对应的爬取脚本，无法执行爬取任务")
            sys.exit(1)

        result_file = os.path.join(output_dir, "result.json")
        print(f"🔧 使用站点 {site_key} 的爬取脚本执行任务...")
        result = await scraper_func(
            proxy=proxy,
            url=url,
            cookies=cookies,
            headless=headless,
            output_dir=output_dir,
            output=result_file
        )

        print_section("✅ 任务执行完成")
        print(f"  结果文件: {result_file}")
        print(f"  内容条数: {len(result)}")

        for i, item in enumerate(result):
            if item.get('title'):
                print(f"  [{i+1}] {item.get('created_at', 'N/A')[:10]} {item.get('title')[:50]}...")
            else:
                print(f"  [{i+1}] {item.get('created_at', 'N/A')[:10]} {item.get('content', '无内容')[:50]}...")

    except Exception as e:
        print(f"\n❌ 任务执行失败: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
