"""快手创作者平台：上传视频、封面，填写标题与关键词，可选发布。

2026-04-03 更新：
- 作品描述框：标题 + 关键词写在同一个 textarea 中
- 关键词格式：每个关键词后加空格，最多 4 个关键词
- 封面设置：点击「封面设置」→「上传封面」→ 选择文件 →「确认」

成功流程（2026-04-03 实测）:
1. 打开 https://cp.kuaishou.com/article/publish/video
2. 点击「上传视频」按钮 → 选择视频文件
3. 等待上传完成（检测页面文本提示）
4. 填写作品描述：标题 + 空格 + #关键词 1 #关键词 2 #关键词 3 #关键词 4
5. 点击「封面设置」→「上传封面」→ 选择图片 →「确认」
6. 点击「发布」按钮（可选）
"""

from __future__ import annotations

import json
import logging
import time

from kbs.cdp import Page, wait_until_upload_hints
from kbs.selectors_ks import (
    COVER_SETTING_BUTTON,
    COVER_UPLOAD_TAB,
    COVER_UPLOAD_BUTTON,
    COVER_CONFIRM_BUTTON,
    DESCRIPTION_TEXTAREA,
    HOME_URL,
    PUBLISH_VIDEO_URL_CANDIDATES,
    TEXT_UPLOAD_FAIL_HINTS,
    TEXT_VIDEO_READY_HINTS,
    VIDEO_UPLOAD_BUTTON,
)
from kbs.types import PublishResult, VideoPublishConfig

logger = logging.getLogger(__name__)


def _fill_description(p: Page, title: str, keywords: list[str]) -> None:
    """填写作品描述框：标题 + 关键词（最多 4 个，空格分隔）。
    
    快手规则：
    - 标题和关键词写在同一个描述框中
    - 格式：第一行标题，第二行关键词用空格分隔
    - 关键词格式：#关键词 1 #关键词 2 #关键词 3 #关键词 4
    - 最多支持 4 个关键词
    
    2026-04-03 实测：
    - 描述框 ID: work-description-edit
    - 类型：contenteditable="true" 的 div
    - 直接设置 innerText 即可
    """
    # 限制关键词数量为 4 个
    limited_keywords = keywords[:4] if len(keywords) > 4 else keywords
    
    # 构建描述文本：标题 + 换行 + 关键词（空格分隔）
    if limited_keywords:
        # 关键词格式：#关键词 空格分隔
        tags_text = " ".join(f"#{kw}" for kw in limited_keywords)
        description = f"{title}\n{tags_text}"
    else:
        description = title
    
    logger.info("填写作品描述：%s", description.replace('\n', ' | '))
    
    # 2026-04-03 实测：直接设置 innerText
    # 清空
    p.evaluate('document.getElementById("work-description-edit").innerText = "";')
    time.sleep(0.2)
    
    # 设置内容
    p.evaluate(f'document.getElementById("work-description-edit").innerText = {json.dumps(description, ensure_ascii=False)};')
    
    # 触发事件
    p.evaluate("""
        () => {
            const el = document.getElementById('work-description-edit');
            if (el) {
                el.dispatchEvent(new InputEvent('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }
    """)
    
    time.sleep(0.5)
    logger.info("作品描述填写完成")


def _upload_cover(p: Page, cover_path: str) -> bool:
    """上传自定义封面。
    
    2026-04-03 实测流程：
    1. 点击"封面设置"按钮（触发封面编辑区域激活）
    2. 页面有 2 个隐藏的 file input：
       - 索引 0：视频上传，accept="video/*,.mp4,..."
       - 索引 1：封面上传，accept="image/apng,image/bmp,..."
    3. 使用 set_file_input_by_accept_hint("image") 自动匹配封面 file input
    4. 封面上传成功后，页面会生成 blob  URL 显示预览
    
    Returns:
        bool: 是否成功上传
    """
    logger.info("开始上传自定义封面：%s", cover_path)
    
    # 步骤 1: 点击"封面设置"激活封面编辑区域
    logger.info("点击封面设置按钮...")
    clicked = p.click_by_inner_text_then_center("封面设置")
    if clicked:
        logger.info("已点击封面设置")
        time.sleep(2.0)  # 多等一会儿，让页面准备好
    else:
        logger.info("未找到封面设置按钮，尝试直接上传")
    
    # 步骤 2: 上传封面文件 - 尝试多种方法
    methods_tried = []
    
    # 方法 1: 使用 accept hint 自动匹配
    try:
        logger.info("尝试方法 1: accept hint='image'")
        p.set_file_input_by_accept_hint("image", [cover_path])
        logger.info("✓ 封面文件设置成功 (accept hint)")
        time.sleep(8.0)  # 等待上传完成和页面更新
        return True
    except Exception as e:
        methods_tried.append(f"accept hint: {e}")
        logger.warning("方法 1 失败：%s", e)
    
    # 方法 2: 通过索引设置（第 2 个 file input）
    try:
        logger.info("尝试方法 2: index=1")
        p.set_file_input_by_index(1, [cover_path])
        logger.info("✓ 封面文件设置成功 (index=1)")
        time.sleep(5.0)
        return True
    except Exception as e:
        methods_tried.append(f"index=1: {e}")
        logger.warning("方法 2 失败：%s", e)
    
    # 方法 3: 使用更具体的 accept hint
    try:
        logger.info("尝试方法 3: accept hint='image/png'")
        p.set_file_input_by_accept_hint("image/png", [cover_path])
        logger.info("✓ 封面文件设置成功 (image/png)")
        time.sleep(5.0)
        return True
    except Exception as e:
        methods_tried.append(f"image/png: {e}")
        logger.warning("方法 3 失败：%s", e)
    
    # 所有方法都失败
    logger.error("封面上传完全失败，尝试的方法:\n  %s", "\n  ".join(methods_tried))
    return False


def _find_button_by_text(page: Page, text: str) -> bool:
    """通过按钮文本查找并点击按钮。
    
    Returns:
        bool: 是否找到并点击成功
    """
    found = page.evaluate(f"""
        () => {{
            const buttons = document.querySelectorAll('button');
            for (const btn of buttons) {{
                if (btn.innerText && btn.innerText.includes('{text}')) {{
                    btn.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    return true;
                }}
            }}
            return false;
        }}
    """)
    return found


def _click_button_by_text(page: Page, text: str) -> bool:
    """通过按钮文本查找并点击按钮。
    
    Returns:
        bool: 是否找到并点击成功
    """
    result = page.evaluate(f"""
        () => {{
            const buttons = document.querySelectorAll('button');
            for (const btn of buttons) {{
                if (btn.innerText && btn.innerText.includes('{text}')) {{
                    btn.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    btn.click();
                    return true;
                }}
            }}
            return false;
        }}
    """)
    return result


def _upload_video(page: Page, video_path: str, timeout: float = 300.0) -> str:
    """上传视频文件。
    
    Returns:
        str: "ready" | "fail" | "timeout"
    """
    logger.info("开始上传视频文件：%s", video_path)
    
    # 先检查是否已有文件输入框（页面初始加载时可能有）
    initial_count = page.evaluate("document.querySelectorAll('input[type=file]').length")
    if not initial_count or initial_count == 0:
        # 没有文件输入框，需要点击上传按钮
        if _click_button_by_text(page, "上传视频"):
            logger.info("已点击上传按钮，等待文件输入框出现")
            time.sleep(1.0)
        else:
            logger.warning("未找到上传按钮")
    
    # 等待 input[type=file] 元素出现
    input_found = False
    for i in range(20):
        count = page.evaluate("document.querySelectorAll('input[type=file]').length")
        if count and count > 0:
            input_found = True
            logger.info("找到 %d 个 input[type=file] 元素", count)
            break
        time.sleep(0.5)
    
    if not input_found:
        logger.error("未找到文件输入框")
        return "fail"
    
    # 使用 CDP 设置文件（通过 accept 属性匹配 video）
    try:
        # 先尝试通过 accept hint 设置（更可靠）
        page.set_file_input_by_accept_hint("video", [video_path])
        logger.info("视频文件设置成功，等待上传...")
        time.sleep(3.0)
    except Exception as e:
        logger.warning("通过 accept hint 设置失败：%s，尝试通过索引设置", e)
        try:
            # 备用：通过索引设置
            page.set_file_input_by_index(0, [video_path])
            logger.info("视频文件设置成功（备用方法），等待上传...")
            time.sleep(3.0)
        except Exception as e2:
            logger.error("视频上传失败：%s", e2)
            return "fail"

    phase = wait_until_upload_hints(
        page,
        TEXT_VIDEO_READY_HINTS,
        TEXT_UPLOAD_FAIL_HINTS,
        timeout=timeout,
    )
    
    # 如果超时，尝试检测页面是否有视频预览元素
    if phase == "timeout":
        logger.info("文本检测超时，尝试检测视频预览元素")
        has_video_preview = page.evaluate("""
            () => {
                // 检测是否有视频预览或编辑界面
                const selectors = [
                    '[class*="video-preview"]',
                    '[class*="video-wrap"]',
                    '[class*="upload-list"]',
                    'video',
                    'img[src*="video"]',
                    '[class*="cover-uploader"]',
                    'input[placeholder*="标题"]',
                    'textarea[placeholder*="作品描述"]',
                ];
                for (const sel of selectors) {
                    if (document.querySelector(sel)) {
                        return true;
                    }
                }
                return false;
            }
        """)
        if has_video_preview:
            logger.info("检测到视频预览界面，认为上传成功")
            phase = "ready"
        else:
            logger.warning("仍未检测到视频上传成功迹象")
    
    return phase


def _clear_draft_cache(page: Page) -> None:
    """清除页面缓存的草稿提示（如果有）。"""
    try:
        result = page.evaluate("""
            () => {
                const buttons = document.querySelectorAll('button');
                for (const btn of buttons) {
                    if (btn.innerText && btn.innerText.includes('放弃')) {
                        btn.click();
                        return true;
                    }
                }
                return false;
            }
        """)
        if result:
            logger.info("已清除草稿缓存")
            time.sleep(0.5)
    except Exception as e:
        logger.debug("清除草稿缓存时出错：%s", e)


def publish_kuaishou(
    page: Page,
    config: VideoPublishConfig,
    *,
    wait_timeout: float = 300.0,
    do_publish: bool = True,
) -> PublishResult:
    """打开快手创作者页，上传素材并填写表单。

    需已在浏览器中登录快手创作者账号。
    
    成功流程（2026-04-03 实测）:
    1. 打开 https://cp.kuaishou.com/article/publish/video
    2. 点击「放弃」清除草稿缓存（如果有）
    3. 点击「上传视频」按钮 → 选择视频文件
    4. 等待上传完成（检测页面文本提示）
    5. 填写作品描述：标题 + 空格 + #关键词 1 #关键词 2 #关键词 3 #关键词 4
    6. 点击「封面设置」→「上传封面」→ 选择图片 →「确认」
    7. 点击「发布」按钮（可选）
    """
    config.validate()

    opened = False
    for url in (*PUBLISH_VIDEO_URL_CANDIDATES, HOME_URL):
        page.navigate(url)
        page.wait_for_load()
        time.sleep(2.0)
        
        # 清除草稿缓存
        _clear_draft_cache(page)
        
        n = page.evaluate("document.querySelectorAll('input[type=file]').length") or 0
        if n > 0:
            opened = True
            break
    if not opened:
        return PublishResult(
            success=False,
            platform="kuaishou",
            message="未找到上传入口，请确认已登录并可访问视频发布页",
            detail=HOME_URL,
        )

    # 上传视频
    phase = _upload_video(page, config.video_path, timeout=wait_timeout)
    
    if phase == "fail":
        return PublishResult(
            success=False,
            platform="kuaishou",
            message="上传失败（页面提示）",
            upload_phase="video_failed",
        )
    if phase == "timeout":
        return PublishResult(
            success=False,
            platform="kuaishou",
            message=f"等待视频处理超时（{wait_timeout}s）",
            upload_phase="video_timeout",
        )

    # 上传封面（如果有）
    if config.cover_path:
        cover_ok = _upload_cover(page, config.cover_path)
        if not cover_ok:
            logger.warning("封面上传失败，但继续流程")
        time.sleep(1.0)

    # 填写作品描述（标题 + 关键词）
    _fill_description(page, config.title, config.keywords)
    time.sleep(0.5)

    if not do_publish:
        return PublishResult(
            success=True,
            platform="kuaishou",
            message="表单已填写，未点击发布",
            upload_phase="form_filled",
        )

    # 点击发布按钮
    clicked = page.click_by_inner_text_then_center("发布") or page.click_by_inner_text_then_center(
        "发表"
    )
    if not clicked:
        logger.warning("未自动点到发布按钮，请在页面手动发布")
        return PublishResult(
            success=True,
            platform="kuaishou",
            message="表单已填写，未找到发布按钮（请手动发布）",
            upload_phase="form_filled",
        )

    time.sleep(2.0)
    return PublishResult(
        success=True,
        platform="kuaishou",
        message="已点击发布",
        upload_phase="published",
    )
