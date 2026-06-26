# -*- coding: utf-8 -*-
"""
番茄小说自动发布 - 作品管理模块（已修复）
"""

import re
import time
import urllib.parse
from typing import List, Optional
from browser import get_browser
from config import SELECTORS, BOOK_MANAGE_URL
from login import check_login_detail


class Work:
    """作品信息类"""
    
    def __init__(self, work_id: str = "", title: str = "", status: str = "", 
                 chapters: int = 0, words: str = "", create_chapter_url: str = ""):
        self.id = work_id
        self.title = title
        self.status = status
        self.chapters = chapters
        self.words = words
        self.create_chapter_url = create_chapter_url
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "chapters": self.chapters,
            "words": self.words,
            "create_chapter_url": self.create_chapter_url
        }
    
    def __str__(self):
        return f"{self.title} - {self.chapters}章 {self.words} ({self.status})"


class FanqieWorks:
    """作品管理类"""
    
    def __init__(self):
        self.browser = get_browser()
        self._works_cache: List[Work] = []
    
    def get_works(self, force_refresh: bool = False) -> dict:
        """
        获取作品列表
        
        Args:
            force_refresh: 是否强制刷新缓存
        
        Returns:
            dict: 包含 success, works, message
        """
        result = {
            "success": False,
            "works": [],
            "message": ""
        }
        
        # 第一步：检查登录状态
        login_status = check_login_detail()
        if not login_status.get("logged_in"):
            result["message"] = "请先登录：运行 'python main.py login' 或使用命令 '番茄登录'"
            return result
        
        if self._works_cache and not force_refresh:
            result["success"] = True
            result["works"] = [w.to_dict() for w in self._works_cache]
            return result
        
        try:
            # 进入作品管理页面
            print("[作品] 正在进入作品管理页面...")
            self.browser.goto(BOOK_MANAGE_URL)
            self.browser.page.wait_for_load_state("networkidle")
            
            # 解析作品列表
            works = self._parse_works()
            self._works_cache = works
            
            result["success"] = True
            result["works"] = [w.to_dict() for w in works]
            result["message"] = f"获取到 {len(works)} 部作品"
            print(f"[作品] 获取到 {len(works)} 部作品")
            
            for work in works:
                print(f"  - {work.title} ({work.chapters}章, {work.status})")
        
        except Exception as e:
            result["message"] = f"获取作品失败: {str(e)}"
            print(f"[作品] 获取失败: {e}")
        
        return result
    
    def _parse_works(self) -> List[Work]:
        """解析作品列表（新版页面结构）"""
        works = []
        
        try:
            # 等待页面加载
            self.browser.page.wait_for_selector(".long-article-table-item", timeout=10000)
            
            # 获取所有作品卡片
            work_items = self.browser.page.query_selector_all(".long-article-table-item")
            print(f"[作品] 找到 {len(work_items)} 个作品卡片")
            
            for item in work_items:
                work = self._parse_work_item(item)
                if work and work.title:
                    works.append(work)
            
        except Exception as e:
            print(f"[作品] 解析失败: {e}")
            # 尝试备用方案
            works = self._parse_works_fallback()
        
        return works
    
    def _parse_work_item(self, item) -> Optional[Work]:
        """解析单个作品卡片"""
        try:
            # 1. 从元素ID获取作品ID
            item_id = item.get_attribute("id")
            if item_id:
                # ID格式: long-article-table-item-7622646964370279486
                work_id = item_id.replace("long-article-table-item-", "")
            else:
                work_id = ""
            
            # 2. 获取书名（在 info-content-title 的 hoverup div 中）
            title_element = item.query_selector(".info-content-title .hoverup")
            if title_element:
                title = title_element.text_content().strip()
            else:
                title = ""
            
            # 3. 获取章节数
            chapter_element = item.query_selector(".detail-chapter .right-info-number")
            if chapter_element:
                chapters_text = chapter_element.text_content().strip()
                chapters = int(chapters_text) if chapters_text.isdigit() else 0
            else:
                chapters = 0
            
            # 4. 获取字数
            word_element = item.query_selector(".detail-wordcount .right-info-number")
            if word_element:
                words = word_element.text_content().strip()
            else:
                words = ""
            
            # 5. 获取状态
            status_element = item.query_selector(".property")
            if status_element:
                status = status_element.text_content().strip()
            else:
                status = ""
            
            # 6. 获取创建章节URL
            create_link = item.query_selector("a:has-text('创建章节')")
            if create_link:
                create_url = create_link.get_attribute("href")
            else:
                create_url = ""
            
            work = Work(
                work_id=work_id,
                title=title,
                status=status,
                chapters=chapters,
                words=words,
                create_chapter_url=create_url
            )
            
            print(f"[作品] 解析成功: {title} ({chapters}章)")
            return work
            
        except Exception as e:
            print(f"[作品] 解析作品卡片失败: {e}")
            return None
    
    def _parse_works_fallback(self) -> List[Work]:
        """备用解析方案"""
        works = []
        
        try:
            # 查找所有"创建章节"链接
            create_links = self.browser.page.query_selector_all("a:has-text('创建章节')")
            print(f"[作品] 备用方案: 找到 {len(create_links)} 个创建章节链接")
            
            for link in create_links:
                href = link.get_attribute("href") or ""
                
                # 从href提取作品ID
                # 格式: /main/writer/7622646964370279486/publish/?enter_from=newchapter_1
                match = re.search(r'/main/writer/(\d+)/publish', href)
                if match:
                    work_id = match.group(1)
                else:
                    work_id = ""
                
                # 从"章节管理"链接提取书名（URL编码）
                parent = link.evaluate("node => node.closest('.home-book-item') || node.closest('.long-article-table-item')")
                
                # 尝试从页面其他位置获取书名
                title = ""
                
                # 查找章节管理链接
                chapter_manage_link = self.browser.page.query_selector(f"a[href*='chapter-manage/{work_id}']")
                if chapter_manage_link:
                    cm_href = chapter_manage_link.get_attribute("href")
                    # 从URL解码书名: chapter-manage/7622646964370279486&%E7%81%B5%E5%A5%91%E8%A7%89%E9%86%92
                    if "&" in cm_href:
                        encoded_title = cm_href.split("&")[1].split("?")[0]
                        title = urllib.parse.unquote(encoded_title)
                
                work = Work(
                    work_id=work_id,
                    title=title,
                    create_chapter_url=href
                )
                
                if work_id:
                    works.append(work)
                    print(f"[作品] 备用解析: 作品{work_id} - {title}")
        
        except Exception as e:
            print(f"[作品] 备用方案失败: {e}")
        
        return works
    
    def get_work_by_title(self, title: str) -> Optional[Work]:
        """根据标题获取作品"""
        works_result = self.get_works()
        if not works_result["success"]:
            return None
        
        for work in self._works_cache:
            if work.title == title or work.title.startswith(title) or title in work.title:
                return work
        
        return None
    
    def get_work_by_id(self, work_id: str) -> Optional[Work]:
        """根据ID获取作品"""
        works_result = self.get_works()
        if not works_result["success"]:
            return None
        
        for work in self._works_cache:
            if work.id == work_id:
                return work
        
        return None
    
    def go_to_create_chapter(self, work: Work) -> bool:
        """
        进入创建章节页面
        
        Args:
            work: 作品信息
        
        Returns:
            bool: 是否成功进入
        """
        try:
            if not work.create_chapter_url:
                # 尝试构建URL
                work.create_chapter_url = f"/main/writer/{work.id}/publish/?enter_from=newchapter_1"
            
            # 构建完整URL
            full_url = f"https://fanqienovel.com{work.create_chapter_url}"
            print(f"[作品] 正在进入创建章节页面: {full_url}")
            
            self.browser.goto(full_url)
            
            # 等待页面加载完成
            time.sleep(3)
            self.browser.page.wait_for_load_state("domcontentloaded")
            
            # 检查是否进入成功 - 等待编辑器或标题输入框出现
            # 尝试多个选择器
            selectors = [
                ".ProseMirror",  # 正文编辑器
                ".serial-input",  # 章节号输入
                "[contenteditable='true']",
                ".editor-content"
            ]
            
            for selector in selectors:
                try:
                    self.browser.page.wait_for_selector(selector, timeout=15000)
                    print(f"[作品] 检测到编辑器元素: {selector}")
                    break
                except:
                    continue
            else:
                # 如果都没找到，再等一会儿
                time.sleep(3)
            
            print("[作品] 成功进入创建章节页面")
            return True
            
        except Exception as e:
            print(f"[作品] 进入创建章节页面失败: {e}")
            # 保存截图用于调试
            try:
                self.browser.page.screenshot(path="debug_create_chapter.png")
                print("[作品] 已保存调试截图: debug_create_chapter.png")
            except:
                pass
            return False


# 全局实例
_works_manager = None

def get_works_manager() -> FanqieWorks:
    """获取作品管理器实例（单例）"""
    global _works_manager
    if _works_manager is None:
        _works_manager = FanqieWorks()
    return _works_manager


# 导出函数
def get_works(force_refresh: bool = False) -> dict:
    """获取作品列表"""
    return get_works_manager().get_works(force_refresh)


def get_work(title: str) -> Optional[Work]:
    """根据标题获取作品"""
    return get_works_manager().get_work_by_title(title)