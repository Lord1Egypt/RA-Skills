#!/usr/bin/env python3
"""
微信公众号自动发布脚本
用法:
  首次登录（扫码）:   python3 publish.py --login
  发布文章:          python3 publish.py --title "标题" --content "正文内容"
  发布并存草稿:      python3 publish.py --title "标题" --content "正文内容" --draft
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

COOKIE_FILE = Path.home() / ".wechat_mp" / "cookies.json"
MP_URL = "https://mp.weixin.qq.com"


def save_cookies(context):
    cookies = context.cookies()
    COOKIE_FILE.parent.mkdir(parents=True, exist_ok=True)
    COOKIE_FILE.write_text(json.dumps(cookies, ensure_ascii=False, indent=2))
    print(f"✅ Cookie 已保存到 {COOKIE_FILE}")


def load_cookies(context):
    if not COOKIE_FILE.exists():
        return False
    cookies = json.loads(COOKIE_FILE.read_text())
    context.add_cookies(cookies)
    return True


def check_login(page):
    """检查是否已登录，返回 (is_logged_in, token)"""
    page.goto(MP_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(2)
    url = page.url
    if "cgi-bin/home" in url or "token=" in url:
        import re
        m = re.search(r'token=(\d+)', url)
        token = m.group(1) if m else ""
        return True, token
    return False, ""


def do_login(playwright):
    """首次扫码登录，保存 Cookie"""
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1280, "height": 800})
    page = context.new_page()

    print("🌐 正在打开微信公众号登录页...")
    page.goto(MP_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(2)

    # 已经登录则直接保存
    if "mp.weixin.qq.com/cgi-bin/home" in page.url:
        print("✅ 已处于登录状态")
        save_cookies(context)
        browser.close()
        return

    print("📱 请用微信扫描页面上的二维码登录...")
    print("   （浏览器窗口已打开，扫码后请等待自动跳转）")

    # 等待登录成功（最长 120 秒）
    try:
        page.wait_for_url("**/cgi-bin/home**", timeout=120000)
        print("✅ 登录成功！")
        save_cookies(context)
    except Exception as e:
        print(f"❌ 登录超时或失败: {e}")
    finally:
        browser.close()


def build_html_content(text):
    """将纯文本转换为公众号富文本 HTML"""
    lines = text.strip().split("\n")
    html_parts = []
    for line in lines:
        line = line.strip()
        if not line:
            html_parts.append('<p style="margin:0;padding:8px 0;">&nbsp;</p>')
            continue
        # 检测是否是序号标题行（① ② 等开头）
        if line and line[0] in "①②③④⑤⑥⑦⑧⑨":
            html_parts.append(
                f'<p style="margin:0;padding:10px 0;font-size:16px;font-weight:bold;color:#1a1a1a;">{line}</p>'
            )
        else:
            html_parts.append(
                f'<p style="margin:0;padding:4px 0;font-size:15px;color:#333;line-height:1.8;">{line}</p>'
            )
    return "\n".join(html_parts)


def do_publish(playwright, title, content, cover_image=None, draft=False,
               enable_comment=True, enable_reward=False, abstract=None,
               ai_cover_prompt="AI，萨克斯，猫"):
    """自动登录并发布文章"""
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1440, "height": 900})

    # 尝试加载 Cookie
    cookie_loaded = load_cookies(context)
    page = context.new_page()

    token = ""
    if cookie_loaded:
        print("🔑 尝试使用已保存的登录状态...")
        logged_in, token = check_login(page)
    else:
        logged_in = False

    if not logged_in:
        print("⚠️  未登录或 Cookie 已过期，请扫码重新登录...")
        page.goto(MP_URL, wait_until="domcontentloaded", timeout=30000)
        try:
            page.wait_for_url("**/cgi-bin/home**", timeout=120000)
            import re
            m = re.search(r'token=(\d+)', page.url)
            token = m.group(1) if m else ""
            save_cookies(context)
            print("✅ 登录成功")
        except Exception as e:
            print(f"❌ 登录失败: {e}")
            browser.close()
            return False

    print(f"📝 进入图文编辑器（token={token}）...")
    editor_url = f"{MP_URL}/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&token={token}&lang=zh_CN"
    page.goto(editor_url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    # 若跳转到登录页，重新登录并重新获取 token
    if "login" in page.url or "passport" in page.url or "loginpage" in page.url:
        print("⚠️  Cookie 失效，请扫码登录...")
        page.goto(MP_URL)
        try:
            page.wait_for_url("**/cgi-bin/home**", timeout=120000)
            import re
            m = re.search(r'token=(\d+)', page.url)
            token = m.group(1) if m else ""
            save_cookies(context)
            editor_url = f"{MP_URL}/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&token={token}&lang=zh_CN"
            page.goto(editor_url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(3)
        except Exception as e:
            print(f"❌ 登录失败: {e}")
            browser.close()
            return False

    # 填写标题
    print(f"✍️  填写标题: {title}")
    try:
        title_input = page.locator("#title")
        title_input.wait_for(state="visible", timeout=15000)
        title_input.click()
        title_input.fill(title)
        time.sleep(0.5)
        print("✅ 标题填写完成")
    except Exception as e:
        print(f"⚠️  标题填写失败: {e}")
        # 截图留档
        page.screenshot(path="/tmp/mp_debug_title.png")
        print("   截图已保存到 /tmp/mp_debug_title.png")
        browser.close()
        return False

    # 填写正文（ProseMirror 编辑器）
    print("✍️  填写正文...")
    try:
        editor = page.locator(".ProseMirror").first
        editor.wait_for(state="visible", timeout=10000)
        html_content = build_html_content(content)
        # 先清空，再注入 HTML
        page.evaluate("""(html) => {
            const ed = document.querySelector('.ProseMirror');
            if (ed) { ed.innerHTML = html; ed.dispatchEvent(new Event('input', {bubbles:true})); }
        }""", html_content)
        time.sleep(1)
        print("✅ 正文填写完成")
    except Exception as e:
        print(f"⚠️  富文本注入失败，尝试备用方式: {e}")

    # 设置封面（优先 AI 配图，失败降级到图片库）
    print(f"🖼️  设置封面（AI 配图提示词: {ai_cover_prompt}）")
    ai_img_url = None  # 用来存 AI 图，稍后插入正文
    try:
        # 第一步：点击封面按钮展开选项菜单
        page.locator(".js_cover_btn_area").first.click(timeout=8000)
        time.sleep(1.5)

        # 第二步：点「AI 配图」
        page.evaluate("""() => {
            const a = document.querySelector('a.js_aiImage, .js_aiImage');
            if (a) a.click();
        }""")
        time.sleep(3)

        # 第三步：清空并输入提示词，点「开始创作」
        textarea = page.locator('.ai_image_dialog textarea.chat_textarea')
        textarea.wait_for(state="visible", timeout=10000)
        textarea.fill("")
        time.sleep(0.3)
        textarea.fill(ai_cover_prompt)
        time.sleep(0.5)

        start_btn = page.locator('.ai_image_dialog .weui-desktop-btn_primary')
        start_btn.click(timeout=8000)
        print("   ✅ AI 配图生成中...")

        # 第四步：等待图片生成（最多 90 秒，每 2 秒轮询最新组）
        ai_generated = False
        for _ in range(45):
            time.sleep(2)
            use_count = page.evaluate("""() => {
                const items = document.querySelectorAll('.ai_image_dialog .chat-ai-item');
                const last = items[items.length - 1];
                if (!last) return 0;
                let count = 0;
                for (const b of last.querySelectorAll('.ai-image-finetuning-btn')) {
                    if (b.innerText.trim() === '使用' && b.offsetParent) count++;
                }
                return count;
            }""")
            if use_count > 0:
                ai_generated = True
                print(f"   ✅ AI 配图已生成 {use_count} 张")
                break

        if not ai_generated:
            raise Exception("AI 配图生成超时")

        # 第五步：点最新一组第一张图的「使用」（前先拿 URL）
        ai_img_url = page.evaluate("""() => {
            const items = document.querySelectorAll('.ai_image_dialog .chat-ai-item');
            const last = items[items.length - 1];
            if (!last) return null;
            const imgs = last.querySelectorAll('.ai-image-item-wrp img');
            return imgs[0] ? imgs[0].src : null;
        }""")
        print(f"   ✅ 已获取 AI 图 URL（首字 {ai_img_url[:50] if ai_img_url else 'N/A'}...）")

        page.evaluate("""() => {
            const items = document.querySelectorAll('.ai_image_dialog .chat-ai-item');
            const last = items[items.length - 1];
            if (!last) return;
            for (const b of last.querySelectorAll('.ai-image-finetuning-btn')) {
                if (b.innerText.trim() === '使用' && b.offsetParent) { b.click(); return; }
            }
        }""")
        print("   ✅ 已选择 AI 配图，进入裁剪步骤")
        time.sleep(3)

        # 第六步：裁剪确认（遍历所有弹窗 footer，防多弹窗干扰）
        confirmed = page.evaluate("""() => {
            const fts = document.querySelectorAll('.weui-desktop-dialog__ft');
            for (const ft of fts) {
                for (const btn of ft.querySelectorAll('button, .weui-desktop-btn')) {
                    const t = (btn.innerText || '').trim();
                    if (btn.offsetParent !== null && (t === '确认' || t === '完成')) {
                        btn.click();
                        return t;
                    }
                }
            }
            return null;
        }""")
        print(f"   裁剪确认: {confirmed}")
        time.sleep(3)

    except Exception as e:
        print(f"   ⚠️  AI 配图失败（{e}），降级到图片库...")
        # 降级：关闭 AI 配图弹窗，改用图片库
        try:
            page.evaluate("""() => {
                const close = document.querySelector('.ai_image_dialog .weui-desktop-dialog__close-btn');
                if (close && close.offsetParent) close.click();
            }""")
            time.sleep(1)

            # 重新打开封面菜单
            page.locator(".js_cover_btn_area").first.click(timeout=8000)
            time.sleep(1.5)

            # 点「从图片库选择」
            page.evaluate("""() => {
                const btns = document.querySelectorAll('a.js_imagedialog, .pop-opr__button.js_imagedialog');
                for (const btn of btns) { if (btn.offsetParent !== null) { btn.click(); return; } }
            }""")
            time.sleep(2.5)

            # 如果有本地封面图，尝试上传
            if cover_image and os.path.exists(cover_image):
                try:
                    with page.expect_file_chooser(timeout=5000) as fc_info:
                        page.evaluate("""() => {
                            const all = document.querySelectorAll('.weui-desktop-dialog a, .weui-desktop-dialog button, .weui-desktop-dialog [class*=btn]');
                            for (const el of all) {
                                if (el.offsetParent !== null && (el.innerText||'').includes('上传')) { el.click(); return; }
                            }
                        }""")
                    file_chooser = fc_info.value
                    file_chooser.set_files(cover_image)
                    print("   ✅ 本地封面已上传到图片库")
                    time.sleep(5)
                except Exception:
                    print("   ⚠️  本地上传失败，选图片库第一张")

            # 选第一张图
            page.evaluate("""() => {
                const items = document.querySelectorAll('.weui-desktop-img-picker__item');
                if (items[0] && items[0].offsetParent !== null) items[0].click();
            }""")
            time.sleep(1)

            # 点「下一步」
            page.evaluate("""() => {
                const btns = document.querySelectorAll('.weui-desktop-dialog__ft button, .weui-desktop-dialog__ft .weui-desktop-btn');
                for (const btn of btns) {
                    if (btn.offsetParent !== null && btn.innerText.trim().includes('下一步')) { btn.click(); return; }
                }
            }""")
            time.sleep(3.5)

            # 裁剪确认
            confirmed = page.evaluate("""() => {
                const fts = document.querySelectorAll('.weui-desktop-dialog__ft');
                for (const ft of fts) {
                    for (const btn of ft.querySelectorAll('button, .weui-desktop-btn')) {
                        const t = (btn.innerText || '').trim();
                        if (btn.offsetParent !== null && (t === '确认' || t === '完成')) {
                            btn.click(); return t;
                        }
                    }
                }
                return null;
            }""")
            print(f"   裁剪确认（降级）: {confirmed}")
            time.sleep(3)
        except Exception as e2:
            print(f"   ⚠️  封面降级也失败（跳过）: {e2}")

    # 验证封面是否设置成功
    cover_ok = page.evaluate("""() => {
        const err = document.querySelector('.js_cover_error');
        if (err && err.offsetParent !== null) return false;
        const preview = document.querySelector('.js_cover_preview_new');
        if (preview && window.getComputedStyle(preview).display !== 'none') return true;
        const img = document.querySelector('#js_cover_area img, .first_appmsg_cove img');
        if (img) return true;
        return false;
    }""")
    if cover_ok:
        print("✅ 封面图设置完成")
    else:
        print("⚠️  封面图可能未成功设置（继续发布流程）")

    # 如果成功拿到 AI 图 URL，插入正文底部
    if ai_img_url:
        print(f"🖼️  将 AI 配图插入正文底部...")
        try:
            inserted = page.evaluate(f"""() => {{
                const ed = document.querySelector('.ProseMirror');
                if (!ed) return false;
                const imgHtml = `<p><img src="{ai_img_url}" style="max-width:100%;display:block;margin:16px auto;" alt="AI配图" /></p>`;
                ed.innerHTML += imgHtml;
                ed.dispatchEvent(new Event('input', {{bubbles:true}}));
                return true;
            }}""")
            if inserted:
                print("   ✅ AI 配图已插入正文底部")
            else:
                print("   ⚠️  插入失败")
        except Exception as e:
            print(f"   ⚠️  插入正文失败: {e}")

    # 填写摘要（如果提供）
    if abstract:
        print(f"📋 填写摘要...")
        try:
            desc_area = page.locator("#js_description_span textarea, #js_description_area textarea").first
            if desc_area.count() > 0:
                desc_area.click()
                desc_area.fill(abstract[:120])
                time.sleep(0.5)
                print("✅ 摘要填写完成")
        except Exception as e:
            print(f"⚠️  摘要填写失败（跳过）: {e}")

    # 设置留言（默认开启，可通过 enable_comment=False 关闭）
    try:
        comment_input = page.locator("input.js_comment#checkbox12, input.js_comment.js_field").first
        if comment_input.count() > 0:
            is_checked = comment_input.is_checked()
            if enable_comment and not is_checked:
                page.evaluate("() => { const el = document.querySelector('input.js_comment'); if(el) el.click(); }")
                print("✅ 已开启留言")
            elif not enable_comment and is_checked:
                page.evaluate("() => { const el = document.querySelector('input.js_comment'); if(el) el.click(); }")
                print("✅ 已关闭留言")
            else:
                print(f"✅ 留言状态: {'开启' if is_checked else '关闭'}（无需变更）")
    except Exception as e:
        print(f"⚠️  留言设置失败（跳过）: {e}")

    # 设置赞赏（需先声明原创，默认关闭）
    if enable_reward:
        try:
            reward_input = page.locator("input.js_reward_setting").first
            if reward_input.count() > 0:
                is_checked = reward_input.is_checked()
                if not is_checked:
                    # 检查赞赏是否可点（原创声明后才可开启）
                    reward_disabled = page.locator(".js_reward_disabled_status").first
                    if reward_disabled.count() > 0 and reward_disabled.is_visible():
                        print("⚠️  赞赏需先声明原创才能开启，已跳过")
                    else:
                        page.evaluate("() => { const el = document.querySelector('input.js_reward_setting'); if(el) el.click(); }")
                        print("✅ 已开启赞赏")
                else:
                    print("✅ 赞赏已开启")
        except Exception as e:
            print(f"⚠️  赞赏设置失败（跳过）: {e}")

    time.sleep(1)

    if draft:
        # 保存草稿
        print("💾 保存为草稿...")
        try:
            # 用 JS 点击避免弹窗遮罩拦截
            clicked = page.evaluate("""() => {
                const sels = ['.send_wording', 'button', 'a'];
                for (const tag of sels) {
                    const els = document.querySelectorAll(tag);
                    for (const el of els) {
                        if (el.offsetParent !== null && (el.innerText||'').trim() === '保存为草稿') {
                            el.click();
                            return el.className || el.tagName;
                        }
                    }
                }
                return null;
            }""")
            time.sleep(2)
            print(f"✅ 已保存为草稿（{clicked}）")
        except Exception as e:
            print(f"⚠️  草稿保存失败: {e}")
            page.screenshot(path="/tmp/mp_debug_draft.png")
            print("   截图已保存到 /tmp/mp_debug_draft.png")
    else:
        # 点击发布
        print("🚀 点击发布...")
        try:
            # 第一步：点击 #js_send 展开发表菜单
            page.locator("#js_send").click(timeout=8000)
            print("   ✅ 发表菜单已展开")
            time.sleep(1.5)

            # 第二步：点击菜单里「发表」选项（.mass_send 下的 .send_wording）
            clicked_menu = page.evaluate("""() => {
                // 找 .mass_send 下文字为「发表」的 .send_wording
                const candidates = document.querySelectorAll('.mass_send .send_wording');
                for (const el of candidates) {
                    if (el.innerText.trim() === '发表' && el.offsetParent !== null) {
                        el.click();
                        return '.mass_send .send_wording[发表]';
                    }
                }
                // 备用：找所有文字为「发表」且可见的 send_wording
                const all = document.querySelectorAll('.send_wording');
                for (const el of all) {
                    if (el.innerText.trim() === '发表' && el.offsetParent !== null) {
                        el.click();
                        return '.send_wording[发表](fallback)';
                    }
                }
                return null;
            }""")
            print(f"   ✅ 菜单「发表」已点击: {clicked_menu}")
            time.sleep(2)

            # 第三步：确认发布弹窗（遍历所有弹窗footer，找「发表」确认按钮）
            confirmed = page.evaluate("""() => {
                // 先找含「发表」按钮的弹窗footer
                const fts = document.querySelectorAll('.weui-desktop-dialog__ft');
                for (const ft of fts) {
                    const btns = ft.querySelectorAll('button.weui-desktop-btn_primary, .weui-desktop-btn_primary');
                    for (const btn of btns) {
                        const t = (btn.innerText || '').trim();
                        if (btn.offsetParent !== null && (t === '发表' || t === '确定' || t === '确认')) {
                            btn.click();
                            return t;
                        }
                    }
                }
                // 备用：js_submit
                const submit = document.querySelector('#js_submit');
                if (submit && submit.offsetParent !== null) { submit.click(); return '#js_submit'; }
                return null;
            }""")
            print(f"   ✅ 确认弹窗已点击: {confirmed}")
            time.sleep(3)

            # 截图留档
            page.screenshot(path="/tmp/mp_after_publish.png")
            print("✅ 发布成功！截图已保存 /tmp/mp_after_publish.png")
        except Exception as e:
            print(f"⚠️  发布失败: {e}")
            page.screenshot(path="/tmp/mp_debug_publish.png")
            print("   截图已保存到 /tmp/mp_debug_publish.png")

    # 保存最新 Cookie
    save_cookies(context)
    time.sleep(2)
    browser.close()
    return True


def main():
    parser = argparse.ArgumentParser(description="微信公众号自动发布")
    parser.add_argument("--login", action="store_true", help="首次扫码登录")
    parser.add_argument("--title", type=str, help="文章标题")
    parser.add_argument("--content", type=str, help="文章正文（纯文本）")
    parser.add_argument("--content-file", type=str, help="从文件读取正文")
    parser.add_argument("--cover", type=str, help="封面图路径", default="/tmp/xhs_cover.jpg")
    parser.add_argument("--draft", action="store_true", help="保存为草稿而非直接发布")
    parser.add_argument("--no-comment", action="store_true", help="关闭留言（默认开启）")
    parser.add_argument("--reward", action="store_true", help="开启赞赏（需已声明原创）")
    parser.add_argument("--abstract", type=str, help="文章摘要（最多120字）", default=None)
    parser.add_argument("--ai-prompt", type=str, help="AI 配图提示词（默认: AI，萨克斯，猫）",
                        default="AI，萨克斯，猫")
    args = parser.parse_args()

    from playwright.sync_api import sync_playwright

    if args.login:
        with sync_playwright() as p:
            do_login(p)
        return

    if not args.title:
        print("❌ 请提供 --title 参数")
        sys.exit(1)

    content = ""
    if args.content_file and os.path.exists(args.content_file):
        content = Path(args.content_file).read_text(encoding="utf-8")
    elif args.content:
        content = args.content
    else:
        print("❌ 请提供 --content 或 --content-file 参数")
        sys.exit(1)

    with sync_playwright() as p:
        success = do_publish(p, args.title, content,
                             cover_image=args.cover,
                             draft=args.draft,
                             enable_comment=not args.no_comment,
                             enable_reward=args.reward,
                             abstract=args.abstract,
                             ai_cover_prompt=args.ai_prompt)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
