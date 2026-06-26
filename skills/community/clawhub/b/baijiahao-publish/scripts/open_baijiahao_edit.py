#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 auth 打开百家号发布页面，可选填入标题与正文。支持两种 auth 格式：
  1. auth.json：Playwright storage_state
  2. .txt：百家号 Cookie 文本（可选前缀 账号----账号---- 后接 name=value; name2=value2; ...）
正文支持：纯文本 --content，或 Markdown 文件 --content-file（依赖 markdown 库转为富文本 HTML，需 pip install markdown）。
用法：
  python open_baijiahao_edit.py [--auth auth.json] [--headless]
  python open_baijiahao_edit.py --auth test/baijiahao.txt --title "文章标题" --content "正文内容"
  python open_baijiahao_edit.py --auth test/baijiahao.txt --title "标题" --content-file article.md
"""

import argparse
import os
import re
import sys

# Mac 上全选用 Command，Windows/Linux 用 Control
_MOD_KEY = "Meta" if sys.platform == "darwin" else "Control"
_SELECT_ALL = f"{_MOD_KEY}+a"

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("未检测到 playwright，请在本脚本使用的 Python 环境中安装：")
    print(f"  当前 Python: {sys.executable}")
    print("  执行: python -m pip install playwright")
    print("  然后: python -m playwright install chromium")
    sys.exit(1)

# Markdown 转 HTML 使用标准库 markdown（Python-Markdown），不手写转换。需 pip install markdown
def _collapse_blank_lines(text: str, max_empty: int = 1) -> str:
    """将连续多行空行压成最多 max_empty 个空行，减少多余空白段落。"""
    lines = text.split("\n")
    out: list[str] = []
    empty_count = 0
    for line in lines:
        if not line.strip():
            empty_count += 1
            if empty_count <= max_empty:
                out.append("")
        else:
            empty_count = 0
            out.append(line)
    return "\n".join(out)


def _html_collapse_blank_paragraphs(html: str) -> str:
    """把连续多个空白段落压成最多一个，减少富文本里的大片空白。"""
    html = re.sub(r"(<p>\s*</p>\s*)+", "<p><br></p>", html)
    html = re.sub(r"(<p><br>\s*</p>\s*)+", "<p><br></p>", html)
    return html


def _md_to_html(md_text: str) -> str:
    """使用 markdown 库将 Markdown 转为 HTML，支持图片、表格、列表等。未安装则报错退出。"""
    import markdown  # type: ignore[import-untyped]

    md_text = _collapse_blank_lines(md_text.strip(), max_empty=1)
    html = markdown.markdown(md_text, extensions=["extra", "nl2br"])
    return _html_collapse_blank_paragraphs(html)

# 百家号发布页
BAIJIAHAO_EDIT_URL = "https://baijiahao.baidu.com/builder/rc/edit?type=news&is_from_cms=1"
# 百度系 Cookie 默认域名与路径
BAIDU_COOKIE_DOMAIN = ".baidu.com"
BAIDU_COOKIE_PATH = "/"


def parse_baijiahao_txt_cookies(auth_path: str) -> list:
    """
    解析 baijiahao.txt 格式：一行内可能含 前缀----前缀---- 后面是 Cookie 字符串。
    Cookie 字符串格式：name1=value1; name2=value2; ...
    返回 Playwright add_cookies 所需的列表：[{"name","value","domain","path"}, ...]
    """
    with open(auth_path, "r", encoding="utf-8", errors="replace") as f:
        line = f.read().strip()
    if not line:
        return []

    # 去掉可能的前缀（例如 账号----账号---- 或 用户名----xxx----）
    if "----" in line:
        parts = line.split("----")
        # 取最后一段作为 cookie 串（通常格式为 前缀----前缀----cookie_string）
        cookie_part = parts[-1].strip()
        if "=" in cookie_part and (";" in cookie_part or re.search(r"^[a-zA-Z0-9_]+=", cookie_part)):
            line = cookie_part
    # 兼容整行就是 cookie 的情况
    cookie_str = line.strip().rstrip(";")

    cookies = []
    for part in cookie_str.split(";"):
        part = part.strip()
        if not part or "=" not in part:
            continue
        idx = part.index("=")
        name = part[:idx].strip()
        value = part[idx + 1 :].strip()
        if name:
            cookies.append({
                "name": name,
                "value": value,
                "domain": BAIDU_COOKIE_DOMAIN,
                "path": BAIDU_COOKIE_PATH,
            })
    return cookies


def is_txt_cookie_file(auth_path: str) -> bool:
    """根据扩展名或内容判断是否为 baijiahao.txt 类 Cookie 文本。"""
    if not os.path.isfile(auth_path):
        return False
    if auth_path.lower().endswith(".txt"):
        return True
    # 可选：读首行判断是否像 cookie 行（含 = 和 ;）
    try:
        with open(auth_path, "r", encoding="utf-8", errors="replace") as f:
            first = (f.readline() or "").strip()
        return "=" in first and (";" in first or "----" in first)
    except Exception:
        return False


def _dismiss_baijiahao_popups(page) -> None:
    """
    若页面上出现「新增风险检测」或「AI工具收起」弹窗，自动点击关闭。
    - 「新增风险检测」：点击「我知道了」
    - 「AI工具收起」：点击该框右上角关闭按钮（X）
    """
    # 等待弹窗可能出现的短暂时间
    try:
        page.wait_for_timeout(800)
    except Exception:
        pass

    # 1. 「新增风险检测」弹窗：点击「我知道了」
    try:
        btn = page.get_by_role("button", name="我知道了")
        if btn.count() > 0:
            btn.first.click(timeout=2000)
            print("[*] 已关闭「新增风险检测」弹窗。")
            page.wait_for_timeout(300)
    except Exception:
        pass

    # 2. 「AI工具收起」弹窗：你提供的 class
    #    cheetah-tour css-1r1altd cheetah-public acss-3alehe acss-pqw5ug cheetah-tour-default-width cheetah-tour-placement-bottomLeft
    #    弹窗内有一个 SVG（关闭图标），点击该 SVG 或包住它的按钮即可关闭
    _closed_ai_tool = False
    try:
        # 用两个特征 class 精确定位该弹窗（避免点到别的 cheetah-tour）
        tour_selector = "[class*='cheetah-tour'][class*='cheetah-tour-placement-bottomLeft']"
        tour = page.locator(tour_selector)
        print("[*] 正在查找「AI工具收起」弹窗（class 含 cheetah-tour）...")
        try:
            tour.first.wait_for(state="visible", timeout=3500)
        except Exception:
            pass
        n_tour = tour.count()
        if n_tour == 0:
            print("[*] 未找到 cheetah-tour 弹窗，可能未出现或已关闭。")
        else:
            print(f"[*] 已找到弹窗（共 {n_tour} 个），正在查找内部 SVG...")
            svg = tour.locator("svg").first
            try:
                svg.wait_for(state="visible", timeout=2000)
            except Exception:
                pass
            n_svg = svg.count()
            if n_svg == 0:
                print("[*] 弹窗内未找到 SVG。")
            else:
                print("[*] 已找到 SVG，正在点击关闭...")
                try:
                    svg.click(timeout=2500)
                    _closed_ai_tool = True
                except Exception as e1:
                    # 若 SVG 不可点，点击其父元素（如包住图标的 button）
                    print(f"[*] 直接点 SVG 未成功 ({e1!r})，尝试点击其父元素...")
                    try:
                        parent = svg.locator("xpath=./..").first
                        parent.click(timeout=2500)
                        _closed_ai_tool = True
                    except Exception as e2:
                        print(f"[*] 点击父元素也未成功: {e2!r}")
        if _closed_ai_tool:
            print("[*] 已关闭「AI工具收起」弹窗。")
            page.wait_for_timeout(400)
    except Exception as e:
        print(f"[*] 处理「AI工具收起」弹窗时出错: {e!r}")


def _fill_title_and_content(page, title: str, content: str, content_is_html: bool = False) -> None:
    """
    在百家号编辑页填入标题和正文。每一步都先点击目标区域聚焦，再填入。
    - 标题：通过占位符「请输入标题」或字数「/64」定位，先点击再填。
    - 正文：在 edui iframe 内填入。content_is_html 为 True 时 content 为 HTML，直接插入富文本；否则为纯文本 keyboard.type。
    """
    if not title and not content:
        return
    try:
        page.wait_for_timeout(600)
    except Exception:
        pass

    if title:
        print("[*] 正在填入标题...")
        _title_ok = False
        # 方式一：占位符（多种写法）
        for ph in ["请输入标题 (2-64字)", "请输入标题(2-64字)", "请输入标题"]:
            try:
                inp = page.get_by_placeholder(ph).first
                inp.wait_for(state="visible", timeout=2500)
                inp.click()  # 先点击聚焦
                page.wait_for_timeout(200)
                inp.fill("")
                inp.fill(title)
                _title_ok = True
                print(f"[*] 已填入标题（{len(title)} 字）。")
                break
            except Exception:
                continue
        # 方式二：通过字数「/64」定位标题区（标题 2-64 字，右侧有 x/64），再找其中的 input 或 contenteditable，点击后填
        if not _title_ok:
            try:
                counter = page.get_by_text("/64").first
                counter.wait_for(state="visible", timeout=2500)
                # 同一行/容器内的可输入元素：先找 input，再找 contenteditable
                container = counter.locator("xpath=./ancestor::*[.//input or .//*[@contenteditable='true']][1]")
                inp = container.locator("input").first
                if inp.count() > 0:
                    inp.click()
                    page.wait_for_timeout(200)
                    inp.fill("")
                    inp.fill(title)
                    _title_ok = True
                    print(f"[*] 已填入标题（{len(title)} 字）。")
                if not _title_ok and container.locator("div[contenteditable='true']").count() > 0:
                    ed = container.locator("div[contenteditable='true']").first
                    ed.click()
                    page.wait_for_timeout(200)
                    page.keyboard.press(_SELECT_ALL)
                    page.keyboard.press("Backspace")
                    page.keyboard.type(title)
                    _title_ok = True
                    print(f"[*] 已填入标题（{len(title)} 字）。")
            except Exception:
                pass
        if not _title_ok:
            print("[!] 填入标题失败，未找到标题输入区域。")

    if content:
        print("[*] 正在填入正文..." + ("（富文本 HTML）" if content_is_html else "（纯文本）"))
        _content_ok = False
        # 正文在 class="edui-editor-iframeholder edui-default" 下的 iframe 里
        #
        # 为何用「模拟粘贴」而不是直接 innerHTML：
        # - 你手动复制粘贴时，编辑器会触发 paste 事件，内部会解析 HTML、登记图片等，下面的「封面」会从这套流程里取图。
        # - 若脚本直接写 document.body.innerHTML = html，DOM 变了但编辑器的内部状态/事件没走，封面组件拿不到新插入的图片。
        # - 所以富文本改为：构造 ClipboardEvent('paste') 并带上 text/html，让编辑器和真实粘贴一样处理，封面才能识别正文里的图。
        for iframe_sel in ["[class*='edui-editor-iframeholder'] iframe", "[class*='edui-default'] iframe"]:
            try:
                if page.locator(iframe_sel).count() == 0:
                    continue
                iframe_elem = page.query_selector(iframe_sel)
                if not iframe_elem:
                    continue
                frame = iframe_elem.content_frame()
                if not frame:
                    continue
                # 先点击 body 聚焦
                frame_loc = page.frame_locator(iframe_sel)
                body_in_frame = frame_loc.locator("body").first
                body_in_frame.wait_for(state="visible", timeout=4000)
                body_in_frame.click()
                page.wait_for_timeout(400)
                if content_is_html:
                    # 富文本：先清空再「模拟粘贴」插入，走和用户 Ctrl+V 一样的流程，封面才能识别正文里的图。
                    page.keyboard.press(_SELECT_ALL)
                    page.keyboard.press("Backspace")
                    page.wait_for_timeout(100)
                    try:
                        frame.evaluate(
                            """(html) => {
                                document.body.focus();
                                var dt = new DataTransfer();
                                dt.setData('text/html', html);
                                dt.setData('text/plain', (new DOMParser()).parseFromString(html, 'text/html').body.innerText || '');
                                document.body.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true }));
                            }""",
                            content,
                        )
                    except Exception:
                        # 若模拟粘贴报错（如部分环境无 DataTransfer），回退为直接写 innerHTML（封面可能不识别图）
                        frame.evaluate(
                            """(html) => {
                                document.body.focus();
                                document.body.innerHTML = html;
                            }""",
                            content,
                        )
                    _content_ok = True
                    print(f"[*] 已填入正文（富文本，约 {len(content)} 字符）。")
                else:
                    page.keyboard.press(_SELECT_ALL)
                    page.keyboard.press("Backspace")
                    page.keyboard.type(content)
                    _content_ok = True
                    print(f"[*] 已填入正文（{len(content)} 字）。")
                break
            except Exception:
                continue
        if not _content_ok:
            # 备用：仅用 frame_locator 点击后输入（不插入 HTML）
            for iframe_sel in ["[class*='edui-editor-iframeholder'] iframe", "[class*='edui-default'] iframe"]:
                try:
                    if page.locator(iframe_sel).count() == 0:
                        continue
                    frame_loc = page.frame_locator(iframe_sel)
                    body_in_frame = frame_loc.locator("body").first
                    body_in_frame.wait_for(state="visible", timeout=4000)
                    body_in_frame.click()
                    page.wait_for_timeout(400)
                    if not content_is_html:
                        page.keyboard.press(_SELECT_ALL)
                        page.keyboard.press("Backspace")
                        page.keyboard.type(content)
                        _content_ok = True
                        print(f"[*] 已填入正文（{len(content)} 字）。")
                    break
                except Exception:
                    continue
        if not _content_ok:
            print("[!] 未找到正文输入区域（edui iframe），请手动粘贴。")


def open_baijiahao_edit(
    auth_path: str,
    headless: bool = False,
    title: str = "",
    content: str = "",
    content_is_html: bool = False,
    click_publish: bool = False,
    click_draft: bool = False,
    keep_open: bool = False,
) -> bool:
    """
    使用 auth_path 对应的登录态打开百家号编辑页。
    支持：auth.json（Playwright storage_state）或 .txt（Cookie 文本，会自动转为 Cookie 注入）。
    :param auth_path: auth 文件路径（.json 或 .txt）
    :param headless: 是否无头模式
    :return: 是否成功打开并停留在编辑页（未跳转登录页）
    """
    auth_path = os.path.abspath(auth_path)
    if not os.path.isfile(auth_path):
        print(f"[!] 未找到 auth 文件: {auth_path}")
        print("[RESULT] failed")
        return False

    use_txt_cookies = is_txt_cookie_file(auth_path)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        try:
            if use_txt_cookies:
                cookie_list = parse_baijiahao_txt_cookies(auth_path)
                if not cookie_list:
                    print("[!] .txt 文件中未解析到有效 Cookie。")
                    browser.close()
                    print("[RESULT] failed")
                    return False
                context = browser.new_context()
                # 先访问域名再注入 Cookie，否则部分 Cookie 可能不生效
                page = context.new_page()
                page.goto("https://baijiahao.baidu.com/", wait_until="domcontentloaded")
                context.add_cookies(cookie_list)
                page.goto(BAIJIAHAO_EDIT_URL, wait_until="domcontentloaded")
            else:
                context = browser.new_context(storage_state=auth_path)
                page = context.new_page()
                page.goto(BAIJIAHAO_EDIT_URL, wait_until="domcontentloaded")

            page.wait_for_load_state("networkidle", timeout=15000)
        except Exception as e:
            print(f"[!] 启动或加载失败: {e}")
            browser.close()
            print("[RESULT] failed")
            return False

        # 简单判断是否被重定向到登录页
        if "login" in page.url or "passport" in page.url:
            print("[!] 当前可能未登录或 Cookie 已失效，请检查 auth 文件或重新登录导出。")
            if keep_open and not headless:
                input("按回车关闭浏览器...")
            browser.close()
            print("[RESULT] failed")
            return False

        # 自动关闭可能出现的弹窗：先「我知道了」，再「AI工具收起」的关闭按钮
        _dismiss_baijiahao_popups(page)

        # 若传入了标题或正文，自动填入对应区域
        if title or content:
            _fill_title_and_content(page, title or "", content or "", content_is_html=content_is_html)

        # 若指定了 --publish 或 --draft：正文后等 2 秒 → 选择封面 → 确定 → 等 2 秒 → 按文字匹配点「发布」或「存草稿」
        if click_publish or click_draft:
            page.wait_for_timeout(2000)  # 输入完正文后等 2 秒
            try:
                # 用文本匹配点击「选择封面」
                cover_btn = page.get_by_text("选择封面", exact=False).first
                if cover_btn.count() == 0:
                    cover_btn = page.get_by_text("封面", exact=False).first
                if cover_btn.count() > 0:
                    cover_btn.click(timeout=3000)
                    print("[*] 已点击「选择封面」。")
                page.wait_for_timeout(2000)
                # 用文本匹配点击「确定」
                ok_btn = page.get_by_role("button", name="确定").first
                if ok_btn.count() == 0:
                    ok_btn = page.get_by_text("确定", exact=True).first
                if ok_btn.count() > 0:
                    ok_btn.click(timeout=3000)
                    print("[*] 已点击「确定」。")
                page.wait_for_timeout(2000)
                # 存草稿：按文字完全匹配点「存草稿」；发布：按文字完全匹配点「发布」（--draft 优先）
                if click_draft:
                    draft_btn = page.get_by_text("存草稿", exact=True).first
                    if draft_btn.count() > 0:
                        draft_btn.click(timeout=3000)
                        print("[*] 已点击「存草稿」。")
                    else:
                        print("[!] 未找到「存草稿」按钮。")
                else:
                    publish_btn = page.get_by_text("发布", exact=True).first
                    if publish_btn.count() > 0:
                        publish_btn.click(timeout=3000)
                        print("[*] 已点击「发布」按钮。")
                    else:
                        print("[!] 未找到「发布」按钮。")
            except Exception as e:
                print(f"[!] 流程异常: {e!r}")

        print("[+] 百家号发布页操作已完成。")
        if keep_open and not headless:
            input("确认后按回车关闭浏览器...")
        browser.close()
        # 输出固定结果行，便于 OpenClaw 等调用方解析；默认视为成功
        print("[RESULT] success")
        return True


def main():
    parser = argparse.ArgumentParser(description="使用 auth.json 打开百家号发布页面")
    parser.add_argument(
        "--auth",
        default="auth.json",
        help="登录态文件：auth.json（Playwright 导出）或 .txt（百家号 Cookie 文本，如 test/baijiahao.txt）",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="使用无头模式（不显示浏览器窗口）",
    )
    parser.add_argument("--title", default="", help="文章标题（填入「请输入标题」输入框）")
    parser.add_argument("--content", default="", help="正文纯文本（直接填入编辑区）")
    parser.add_argument(
        "--content-file",
        default="",
        help="正文来源：本地文件路径。若为 .md 则转为富文本 HTML 后填入；否则按纯文本读取。与 --content 二选一，优先 --content-file。",
    )
    parser.add_argument(
        "--strip-title-from-content",
        action="store_true",
        dest="strip_title_from_content",
        help="当同时提供 --title 和 --content-file 时，在正文文件中用标题做第一次匹配并截断，只把匹配到的那一行之后的内容当作正文（避免 md 里的标题和页面标题重复）。",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="填完标题和正文后，选封面、确定，再按文字匹配点击「发布」。",
    )
    parser.add_argument(
        "--draft",
        action="store_true",
        help="与 --publish 流程相同，但最后按文字匹配点击「存草稿」保存到草稿。",
    )
    parser.add_argument(
        "--keep-open",
        action="store_true",
        dest="keep_open",
        help="执行完成后不立即关闭浏览器，等待用户按回车确认后再关闭；未指定则执行完直接关闭并返回结果。",
    )
    args = parser.parse_args()

    # 解析正文：优先 --content-file，.md 转 HTML
    body_content = args.content or ""
    body_is_html = False
    if args.content_file:
        # 去掉粘贴时可能带上的不可见字符（如 U+202A），并正确处理绝对路径
        raw_path = args.content_file.strip().strip("\u202a\u202b\u202c\u200e\u200f\u200d")
        if os.path.isabs(raw_path):
            path = os.path.normpath(raw_path)
        else:
            path = os.path.abspath(raw_path)
        if not os.path.isfile(path):
            print(f"[!] 正文文件不存在: {path}")
        else:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                raw = f.read()
            # 若指定了用标题截断：在文件中找第一次出现 --title 的那一行，只保留该行之后的内容作为正文
            if args.strip_title_from_content and args.title:
                idx = raw.find(args.title)
                if idx >= 0:
                    line_start = raw.rfind("\n", 0, idx) + 1
                    line_end = raw.find("\n", idx)
                    if line_end < 0:
                        line_end = len(raw)
                    raw = raw[line_end:].lstrip("\n\r")
                else:
                    pass  # 未匹配到则全文当正文
            if path.lower().endswith(".md"):
                try:
                    import markdown  # noqa: F401
                except ImportError:
                    print("[!] 使用 .md 文件需要安装 markdown 库，请执行: pip install markdown")
                    sys.exit(1)
                body_content = _md_to_html(raw)
                body_is_html = True
            else:
                body_content = raw

    # 解析 auth 路径：支持绝对路径，并去掉粘贴可能带来的不可见字符
    raw_auth = (args.auth or "").strip().strip("\u202a\u202b\u202c\u200e\u200f\u200d")
    if not raw_auth:
        raw_auth = "auth.json"
    if os.path.isabs(raw_auth):
        auth_path = os.path.normpath(raw_auth)
    else:
        auth_path = os.path.abspath(raw_auth)
    # 仅当用户用的是默认名 auth.json 且该路径下不存在时，再在多个目录里查找
    if (args.auth in ("", "auth.json")) and not os.path.isfile(auth_path):
        _script_dir = os.path.dirname(os.path.abspath(__file__))
        _project_root = os.path.dirname(os.path.dirname(_script_dir))
        _project_root = os.path.dirname(_project_root)
        for root in [os.getcwd(), _script_dir, _project_root]:
            candidate = os.path.join(root, "auth.json")
            if os.path.isfile(candidate):
                auth_path = candidate
                break

    success = open_baijiahao_edit(
        auth_path,
        headless=args.headless,
        title=args.title or "",
        content=body_content,
        content_is_html=body_is_html,
        click_publish=args.publish,
        click_draft=args.draft,
        keep_open=args.keep_open,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
