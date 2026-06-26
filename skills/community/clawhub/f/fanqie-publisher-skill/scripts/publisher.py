# -*- coding: utf-8 -*-
"""
番茄小说自动发布 - 章节发布模块（修复版 v3）

支持两种发布模式：
- publish: 直接发布章节（默认）
- draft: 存入草稿箱

完整发布流程：
1. 进入创建章节页面
2. 填写章节号
3. 填写标题
4. 填写正文内容（使用剪贴板粘贴）
5. 根据模式选择：
   - publish模式: 点击"下一步" → 处理弹窗 → 确认发布
   - draft模式: 点击右上角"存入草稿箱" → 确认保存
"""

import time
import subprocess
import re
import platform
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass
from browser import get_browser
from works import FanqieWorks, Work
from login import check_login_detail


@dataclass
class Chapter:
    """章节信息"""
    title: str
    content: str
    chapter_number: str = ""
    
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "content": self.content,
            "chapter_number": self.chapter_number
        }


class FanqiePublisher:
    """章节发布类"""
    
    def __init__(self):
        self.browser = get_browser()
        self.works_manager = FanqieWorks()
    
    def publish_chapter(self, work_title: str, chapter: Chapter, mode: str = "publish") -> dict:
        """
        发布单个章节
        
        Args:
            work_title: 作品标题
            chapter: 章节信息
            mode: 发布模式，可选值：
                - "publish": 直接发布章节（默认）
                - "draft": 存入草稿箱
        
        Returns:
            dict: 发布结果 {"success": bool, "message": str}
        """
        result = {
            "success": False,
            "message": "",
            "chapter_title": chapter.title,
            "mode": mode
        }
        
        # 检查登录状态
        login_status = check_login_detail()
        if not login_status.get("logged_in"):
            result["message"] = "请先登录"
            return result
        
        # 验证模式参数
        if mode not in ["publish", "draft"]:
            result["message"] = f"无效的发布模式: {mode}，请使用 'publish' 或 'draft'"
            return result
        
        try:
            mode_desc = "存入草稿箱" if mode == "draft" else "直接发布"
            print(f"[发布] 准备发布章节: {chapter.title} ({mode_desc})")
            
            # 获取作品
            work = self.works_manager.get_work_by_title(work_title)
            if not work:
                result["message"] = f"未找到作品: {work_title}"
                return result
            
            print(f"[发布] 作品: {work.title} ({work.chapters}章)")
            
            # 进入创建章节页面
            if not self.works_manager.go_to_create_chapter(work):
                result["message"] = "进入创建章节页面失败"
                return result
            
            time.sleep(3)
            
            # 处理初始弹窗
            self._handle_initial_popups()
            
            # 填写章节内容
            if not self._fill_chapter(chapter):
                result["message"] = "填写章节内容失败"
                return result
            
            # 根据模式选择不同的后续流程
            if mode == "draft":
                # 存入草稿箱
                if not self._save_to_draft():
                    result["message"] = "存入草稿箱失败"
                    return result
                result["success"] = True
                result["message"] = f"章节 '{chapter.title}' 已存入草稿箱"
            else:
                # 直接发布
                # 点击下一步
                if not self._click_next():
                    result["message"] = "点击下一步失败"
                    return result
                
                # 处理确认流程
                if not self._handle_confirm_flow():
                    result["message"] = "确认发布失败"
                    return result
                result["success"] = True
                result["message"] = f"章节 '{chapter.title}' 发布成功，等待审核"
            
            print(f"[发布] [OK] {result['message']}")
            
        except Exception as e:
            result["message"] = f"发布出错: {str(e)}"
            print(f"[发布] ✗ 错误: {e}")
            self.browser.page.screenshot(path="publish_error.png")
        
        return result
    
    def _handle_initial_popups(self):
        """处理初始弹窗"""
        print("[发布] 棄查初始弹窗...")
        time.sleep(2)
        
        # 关闭作者有话说引导
        try:
            close_btn = self.browser.page.query_selector(".author-speak-guide-close")
            if close_btn and close_btn.is_visible():
                close_btn.click()
                print("[发布] 关闭作者有话说引导")
                time.sleep(0.5)
        except:
            pass
        
        # 关闭编辑器分区引导弹窗（___reactour div）
        try:
            # 直接查找 ___reactour 容器中的关闭按钮
            reactour_close = self.browser.page.query_selector("#___reactour button, #___reactour .close, #___reactour [class*='close']")
            if reactour_close:
                reactour_close.click()
                print("[发布] 关闭 reactour 引导弹窗")
                time.sleep(0.5)
            else:
                # 尝试隐藏整个 reactour 容器
                self.browser.page.evaluate("document.getElementById('___reactour')?.style?.display = 'none'")
                print("[发布] 隐藏 reactour 弹窗容器")
                time.sleep(0.3)
        except:
            pass
        
        # ESC 键关闭通用弹窗
        try:
            self.browser.page.keyboard.press("Escape")
            time.sleep(0.3)
        except:
            pass
        
        # 再次检查其他可能的弹窗
        try:
            generic_close = self.browser.page.query_selector(".modal-close, .popup-close, .dialog-close, [aria-label='关闭']")
            if generic_close and generic_close.is_visible():
                generic_close.click()
                print("[发布] 关闭通用弹窗")
                time.sleep(0.5)
        except:
            pass
    
    def _fill_chapter(self, chapter: Chapter) -> bool:
        """填写章节内容"""
        print("[发布] 填写章节内容...")
        
        try:
            # 1. 填写章节号
            chapter_input = self.browser.page.query_selector(
                ".serial-input.byte-input.byte-input-size-default:not(.serial-editor-input-hint-area)"
            )
            if chapter_input:
                chapter_input.click()
                time.sleep(0.3)
                chapter_input.fill("")
                time.sleep(0.3)
                
                # 提取章节号
                chapter_num = chapter.chapter_number
                if not chapter_num:
                    match = re.search(r'第\s*(\d+)\s*章', chapter.title)
                    chapter_num = match.group(1) if match else ""
                
                if chapter_num:
                    chapter_input.fill(str(int(chapter_num)))
                    print(f"[发布] 章节号: {chapter_num}")
                    time.sleep(0.5)
            
            # 2. 填写标题
            title_input = self.browser.page.query_selector(".serial-editor-input-hint-area")
            if title_input:
                title_input.click()
                time.sleep(0.3)
                title_input.fill("")
                time.sleep(0.3)
                
                pure_title = re.sub(r'第\s*\d+\s*章\s*', '', chapter.title).strip()
                title_input.fill(pure_title)
                print(f"[发布] 标题: {pure_title}")
                time.sleep(0.5)
            
            # 3. 填写正文（使用剪贴板粘贴）
            editor = self.browser.page.query_selector(".ProseMirror")
            if editor:
                editor.click()
                time.sleep(0.5)
                
                # 复制内容到剪贴板
                if not self._copy_to_clipboard(chapter.content):
                    print("[发布] 警告: 剪贴板复制失败，尝试直接输入")
                    editor.fill(chapter.content)
                else:
                    time.sleep(0.3)
                    # 跨平台粘贴快捷键
                    paste_key = "Meta+v" if platform.system() == "Darwin" else "Control+v"
                    self.browser.page.keyboard.press(paste_key)
                print(f"[发布] 正文: 已粘贴 {len(chapter.content)} 字")
                time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"[发布] 填写失败: {e}")
            return False
    
    def _copy_to_clipboard(self, text: str) -> bool:
        """
        复制文本到系统剪贴板（跨平台支持）
        
        支持平台:
        - macOS: 使用 pbcopy
        - Linux: 优先使用 xclip，其次 xsel
        - Windows: 使用 clip 命令
        
        Args:
            text: 要复制的文本内容
        
        Returns:
            bool: 是否复制成功
        """
        system = platform.system()
        
        try:
            if system == "Darwin":  # macOS
                proc = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
                proc.communicate(text.encode('utf-8'))
                return True
            
            elif system == "Windows":
                # Windows 使用 clip 命令，需要 utf-16le 编码
                proc = subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True)
                proc.communicate(text.encode('utf-16le'))
                return True
            
            elif system == "Linux":
                # Linux 优先尝试 xclip，其次 xsel
                try:
                    proc = subprocess.Popen(['xclip', '-selection', 'clipboard'], 
                                          stdin=subprocess.PIPE)
                    proc.communicate(text.encode('utf-8'))
                    return True
                except FileNotFoundError:
                    # xclip 不可用，尝试 xsel
                    try:
                        proc = subprocess.Popen(['xsel', '--clipboard', '--input'], 
                                              stdin=subprocess.PIPE)
                        proc.communicate(text.encode('utf-8'))
                        return True
                    except FileNotFoundError:
                        print("[剪贴板] 错误: 请安装 xclip 或 xsel")
                        print("  Ubuntu/Debian: sudo apt install xclip")
                        print("  Arch Linux: sudo pacman -S xclip")
                        print("  Fedora: sudo dnf install xclip")
                        return False
            
            else:
                print(f"[剪贴板] 不支持的系统: {system}")
                return False
                
        except Exception as e:
            print(f"[剪贴板] 复制失败: {e}")
            return False
    
    def _click_next(self) -> bool:
        """点击下一步"""
        print("[发布] 点击下一步...")
        
        try:
            next_btn = self.browser.page.query_selector("button:has-text('下一步')")
            if next_btn and not next_btn.is_disabled():
                next_btn.click()
                print("[发布] [OK] 点击下一步")
                time.sleep(3)
                return True
            return False
        except Exception as e:
            print(f"[发布] 点击下一步失败: {e}")
            return False
    
    def _handle_confirm_flow(self) -> bool:
        """处理确认发布流程"""
        print("[发布] 处理确认流程...")
        
        try:
            # 1. 处理错别字检测弹窗
            time.sleep(2)
            submit_btn = self.browser.page.query_selector("button:has-text('提交')")
            if submit_btn and submit_btn.is_visible():
                submit_btn.click()
                print("[发布] [OK] 错别字弹窗: 点击提交")
                time.sleep(3)
            
            # 2. 处理内容风险检测弹窗
            confirm_btn = self.browser.page.query_selector("button:has-text('确定')")
            if confirm_btn and confirm_btn.is_visible():
                confirm_btn.click()
                print("[发布] [OK] 风险检测弹窗: 点击确定")
                time.sleep(5)
            
            # 3. 处理发布设置弹窗 - 选择"否"不使用AI
            no_label = self.browser.page.query_selector("label:has-text('否')")
            if no_label and no_label.is_visible():
                no_label.click()
                print("[发布] [OK] AI选项: 选择否")
                time.sleep(0.5)
            
            # 4. 点击确认发布
            publish_btn = self.browser.page.query_selector("button:has-text('确认发布')")
            if publish_btn and publish_btn.is_visible():
                publish_btn.click()
                print("[发布] [OK] 点击确认发布")
                time.sleep(3)
            
            # 5. 检查是否成功
            time.sleep(2)
            current_url = self.browser.page.url
            
            if "chapter-manage" in current_url:
                print("[发布] [OK] 已跳转到章节管理页面")
                
                # 检查成功提示
                page_text = self.browser.page.content()
                if "已提交" in page_text or "审核中" in page_text:
                    print("[发布] [OK] 检测到成功提交提示")
                    return True
            
            # 截图当前状态
            self.browser.page.screenshot(path="confirm_final.png")
            return True
            
        except Exception as e:
            print(f"[发布] 确认流程失败: {e}")
            self.browser.page.screenshot(path="confirm_error.png")
            return False
    
    def _save_to_draft(self) -> bool:
        """
        存入草稿箱
        
        点击右上角的"存入草稿箱"按钮，保存章节到草稿箱而不发布。
        
        Returns:
            bool: 是否成功存入草稿箱
        """
        print("[草稿] 存入草稿箱...")
        
        try:
            # 等待页面稳定
            time.sleep(2)
            
            # 查找存入草稿箱按钮（通常在右上角）
            # 可能的选择器：
            # 1. 包含"草稿箱"文字的按钮
            # 2. 包含"存入草稿"文字的按钮
            # 3. 特定的class名称
            
            draft_btn_selectors = [
                "button:has-text('存入草稿箱')",
                "button:has-text('草稿箱')",
                "button:has-text('存草稿')",
                "[class*='draft']",
                ".draft-btn",
                "a:has-text('存入草稿箱')",
                "a:has-text('草稿箱')",
            ]
            
            draft_btn = None
            for selector in draft_btn_selectors:
                try:
                    btn = self.browser.page.query_selector(selector)
                    if btn and btn.is_visible():
                        draft_btn = btn
                        print(f"[草稿] 找到草稿按钮: {selector}")
                        break
                except:
                    continue
            
            if not draft_btn:
                # 尝试通过XPath查找
                try:
                    draft_btn = self.browser.page.locator("//button[contains(text(), '草稿')]").first
                    if draft_btn and draft_btn.is_visible():
                        print("[草稿] 通过XPath找到草稿按钮")
                except:
                    pass
            
            if draft_btn:
                draft_btn.click()
                print("[草稿] [OK] 点击存入草稿箱")
                time.sleep(3)
                
                # 处理可能的确认弹窗
                time.sleep(2)
                confirm_btn = self.browser.page.query_selector("button:has-text('确定'), button:has-text('确认'), button:has-text('保存')")
                if confirm_btn and confirm_btn.is_visible():
                    confirm_btn.click()
                    print("[草稿] [OK] 确认保存")
                    time.sleep(2)
                
                # 检查是否成功（跳转到章节管理或显示成功提示）
                time.sleep(2)
                current_url = self.browser.page.url
                
                if "chapter-manage" in current_url or "book-manage" in current_url:
                    print("[草稿] [OK] 已跳转到管理页面")
                    return True
                
                # 检查页面是否有成功提示
                page_content = self.browser.page.content()
                success_keywords = ["已保存", "存入成功", "草稿", "保存成功"]
                for keyword in success_keywords:
                    if keyword in page_content:
                        print(f"[草稿] [OK] 检测到成功提示: {keyword}")
                        return True
                
                # 截图当前状态
                self.browser.page.screenshot(path="draft_final.png")
                return True
            else:
                print("[草稿] ✗ 未找到存入草稿箱按钮")
                self.browser.page.screenshot(path="draft_no_button.png")
                return False
                
        except Exception as e:
            print(f"[草稿] 存入草稿箱失败: {e}")
            self.browser.page.screenshot(path="draft_error.png")
            return False
    
    def publish_batch(self, work_title: str, chapters: List[Chapter], interval: int = 5, mode: str = "publish") -> List[dict]:
        """
        批量发布章节
        
        Args:
            work_title: 作品名称
            chapters: 章节列表
            interval: 发布间隔（秒）
            mode: 发布模式，"publish" 直接发布，"draft" 存入草稿箱
        
        Returns:
            发布结果列表
        """
        results = []
        
        mode_desc = "存入草稿箱" if mode == "draft" else "直接发布"
        print(f"[批量] 开始批量{mode_desc}，共 {len(chapters)} 章")
        
        for i, chapter in enumerate(chapters):
            print(f"\n[批量] 进度: {i+1}/{len(chapters)}")
            result = self.publish_chapter(work_title, chapter, mode=mode)
            results.append(result)
            
            if i < len(chapters) - 1:
                print(f"[批量] 等待 {interval} 秒...")
                time.sleep(interval)
        
        return results


# 便捷函数
def publish_chapter(work_title: str, title: str, content: str, mode: str = "publish") -> dict:
    """
    发布单个章节
    
    Args:
        work_title: 作品名称
        title: 章节标题
        content: 章节内容
        mode: 发布模式，"publish" 直接发布，"draft" 存入草稿箱
    
    Returns:
        发布结果
    """
    publisher = FanqiePublisher()
    chapter = Chapter(title=title, content=content)
    return publisher.publish_chapter(work_title, chapter, mode=mode)


def publish_batch(work_title: str, chapters: List[dict], interval: int = 5, mode: str = "publish") -> List[dict]:
    """
    批量发布章节
    
    Args:
        work_title: 作品名称
        chapters: 章节列表，每个元素为 {"title": "标题", "content": "内容"}
        interval: 发布间隔（秒）
        mode: 发布模式，"publish" 直接发布，"draft" 存入草稿箱
    
    Returns:
        发布结果列表
    """
    publisher = FanqiePublisher()
    chapter_list = [Chapter(title=c["title"], content=c["content"]) for c in chapters]
    return publisher.publish_batch(work_title, chapter_list, interval, mode=mode)


def publish_from_file(work_title: str, file_path: str, mode: str = "publish") -> dict:
    """
    从文件发布章节
    
    Args:
        work_title: 作品名称
        file_path: 章节文件路径
        mode: 发布模式，"publish" 直接发布，"draft" 存入草稿箱
    
    Returns:
        发布结果
    """
    from main import extract_content
    
    content = Path(file_path).read_text(encoding='utf-8')
    chapter_data = extract_content(content)
    
    if not chapter_data.get("title") or not chapter_data.get("content"):
        return {"success": False, "message": "无法提取章节内容"}
    
    publisher = FanqiePublisher()
    chapter = Chapter(
        title=chapter_data["title"],
        content=chapter_data["content"]
    )
    return publisher.publish_chapter(work_title, chapter, mode=mode)