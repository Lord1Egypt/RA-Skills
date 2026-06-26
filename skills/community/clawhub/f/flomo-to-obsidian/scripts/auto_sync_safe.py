#!/usr/bin/env python3
"""
Flomo Auto Sync to Obsidian (Safe Mode)
安全模式：不保存密码，首次需要手动登录，之后自动使用浏览器保存的登录状态
"""

import argparse
import json
import logging
import os
import shutil
import sys
import time
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("错误：缺少 Playwright。请运行: pip install playwright && playwright install chromium")
    sys.exit(1)

# 导入转换脚本
sys.path.insert(0, str(Path(__file__).parent))
from convert_v2 import FlomoParser, ObsidianConverter

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_sync.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FlomoAutoSyncSafe:
    """Flomo 自动同步器（安全模式 - 使用浏览器会话）"""
    
    def __init__(
        self,
        output_dir: str,
        download_dir: str,
        user_data_dir: str,
        state_file: str = '.flomo_sync_state.json',
        tag_prefix: str = '',
        headless: bool = False
    ):
        self.output_dir = Path(output_dir)
        self.download_dir = Path(download_dir)
        self.user_data_dir = Path(user_data_dir)
        self.state_file = Path(state_file)
        self.tag_prefix = tag_prefix
        self.headless = headless
        
        # 创建必要的目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载同步状态
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """加载同步状态"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"加载状态文件失败: {e}")
        
        return {
            'last_sync_time': None,
            'synced_notes': {},
            'last_export_file': None,
            'sync_count': 0,
            'first_login_completed': False
        }
    
    def _save_state(self):
        """保存同步状态"""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, ensure_ascii=False, indent=2)
            logger.info(f"状态已保存到: {self.state_file}")
        except Exception as e:
            logger.error(f"保存状态文件失败: {e}")
    
    def _wait_for_user_login(self, page) -> bool:
        """等待用户手动登录"""
        logger.info("=" * 60)
        logger.info("🔐 首次使用需要手动登录")
        logger.info("=" * 60)
        logger.info("请在打开的浏览器中完成以下操作：")
        logger.info("1. 输入你的手机号/邮箱")
        logger.info("2. 输入密码")
        logger.info("3. 点击登录")
        logger.info("4. 等待跳转到主页")
        logger.info("")
        logger.info("登录后，浏览器会记住你的登录状态")
        logger.info("下次运行时将自动使用已保存的登录信息")
        logger.info("=" * 60)
        
        # 等待用户登录（最多等待 5 分钟）
        try:
            logger.info("等待登录中...")
            page.wait_for_url('**/mine**', timeout=300000)  # 5 分钟
            logger.info("✅ 登录成功！")
            
            # 标记首次登录已完成
            self.state['first_login_completed'] = True
            self._save_state()
            
            return True
        except PlaywrightTimeout:
            logger.error("❌ 登录超时（5分钟）")
            return False
    
    def export_from_flomo(self) -> Optional[Path]:
        """使用浏览器自动化从 flomo 导出数据"""
        logger.info("开始浏览器自动化导出...")
        
        # 使用持久化的用户数据目录，保存登录状态
        with sync_playwright() as p:
            # 启动浏览器，使用持久化上下文
            context = p.chromium.launch_persistent_context(
                str(self.user_data_dir),
                headless=self.headless,
                accept_downloads=True,
                viewport={'width': 1280, 'height': 720}
            )
            page = context.pages[0] if context.pages else context.new_page()
            
            try:
                # 1. 访问 flomo 登录页
                logger.info("访问 flomo 登录页...")
                page.goto('https://v.flomoapp.com/login', wait_until='networkidle', timeout=30000)
                time.sleep(2)
                
                # 2. 检查是否已经登录
                current_url = page.url
                if '/mine' in current_url:
                    logger.info("✅ 检测到已登录状态")
                else:
                    # 未登录，需要手动登录
                    logger.info("检测到未登录状态，请手动登录...")
                    if not self._wait_for_user_login(page):
                        return None
                
                time.sleep(3)
                
                # 3. 点击用户名打开菜单
                logger.info("点击用户名打开菜单...")
                
                try:
                    # 方法1: 通过文本匹配用户名
                    username_selectors = [
                        'text=Ryan.B',  # 使用实际用户名
                        '[class*="user"]',
                        '[class*="avatar"]',
                        '[class*="profile"]'
                    ]
                    
                    clicked = False
                    for selector in username_selectors:
                        try:
                            locator = page.locator(selector).first
                            if locator.count() > 0:
                                locator.click()
                                logger.info(f"成功点击用户名: {selector}")
                                clicked = True
                                time.sleep(2)
                                break
                        except:
                            continue
                    
                    if not clicked:
                        # 方法2: 点击左上角区域
                        page.mouse.click(100, 50)
                        logger.info("点击用户区域（左上角）")
                        time.sleep(2)
                        
                except Exception as e:
                    logger.warning(f"点击用户名失败: {e}")
                    screenshot_path = self.download_dir / f'error_user_{int(time.time())}.png'
                    page.screenshot(path=str(screenshot_path))
                    logger.error(f"已保存错误截图: {screenshot_path}")
                    return None
                
                # 4. 点击"导出/导入笔记"菜单项
                logger.info("点击导出/导入笔记...")
                
                try:
                    export_menu = page.get_by_text('导出/导入笔记', exact=False).first
                    if export_menu.count() > 0:
                        export_menu.click()
                        logger.info("成功点击导出/导入笔记")
                        time.sleep(1)
                    else:
                        raise Exception("找不到导出/导入笔记菜单项")
                except Exception as e:
                    logger.error(f"点击导出/导入笔记失败: {e}")
                    screenshot_path = self.download_dir / f'error_menu_{int(time.time())}.png'
                    page.screenshot(path=str(screenshot_path))
                    logger.error(f"已保存错误截图: {screenshot_path}")
                    return None
                
                # 5. 点击"导出笔记"子菜单
                logger.info("点击导出笔记...")
                
                try:
                    export_submenu = page.get_by_text('导出笔记', exact=True).first
                    if export_submenu.count() > 0:
                        export_submenu.click()
                        logger.info("成功点击导出笔记")
                        time.sleep(2)
                    else:
                        raise Exception("找不到导出笔记子菜单")
                except Exception as e:
                    logger.error(f"点击导出笔记失败: {e}")
                    screenshot_path = self.download_dir / f'error_submenu_{int(time.time())}.png'
                    page.screenshot(path=str(screenshot_path))
                    logger.error(f"已保存错误截图: {screenshot_path}")
                    return None
                
                # 6. 在弹窗中点击"导出"按钮，并监听下载
                logger.info("点击导出按钮，开始下载...")
                
                try:
                    # 设置下载路径
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    download_path = self.download_dir / f'flomo_export_{timestamp}.zip'
                    
                    # 监听下载事件
                    with page.expect_download(timeout=120000) as download_info:
                        # 在弹窗中查找并点击"导出"按钮
                        export_button = page.get_by_role('button', name='导出').first
                        if export_button.count() > 0:
                            export_button.click()
                            logger.info("成功点击导出按钮，等待下载...")
                        else:
                            raise Exception("找不到导出按钮")
                    
                    download = download_info.value
                    logger.info("下载已开始...")
                except Exception as e:
                    logger.error(f"点击导出按钮或下载失败: {e}")
                    screenshot_path = self.download_dir / f'error_download_{int(time.time())}.png'
                    page.screenshot(path=str(screenshot_path))
                    logger.error(f"已保存错误截图: {screenshot_path}")
                    return None
                
                # 7. 保存下载的文件
                download.save_as(str(download_path))
                
                logger.info(f"下载完成: {download_path}")
                
                # 8. 解压文件
                extract_dir = self.download_dir / f'flomo_export_{timestamp}'
                extract_dir.mkdir(exist_ok=True)
                
                with zipfile.ZipFile(download_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                
                logger.info(f"解压完成: {extract_dir}")
                
                # 9. 查找 HTML 文件（递归查找）
                html_files = list(extract_dir.glob('**/*.html'))
                if not html_files:
                    logger.error("解压后找不到 HTML 文件")
                    logger.error(f"解压目录内容: {list(extract_dir.iterdir())}")
                    return None
                
                html_file = html_files[0]
                logger.info(f"找到 HTML 文件: {html_file}")
                
                # 记录 file 目录路径
                file_dir = html_file.parent / 'file'
                if file_dir.exists():
                    logger.info(f"找到附件目录: {file_dir}")
                else:
                    logger.warning("未找到附件目录")
                
                return html_file
                
            except Exception as e:
                logger.error(f"浏览器自动化出错: {e}", exc_info=True)
                try:
                    screenshot_path = self.download_dir / 'error_screenshot.png'
                    page.screenshot(path=str(screenshot_path))
                    logger.info(f"已保存错误截图: {screenshot_path}")
                except:
                    pass
                return None
            
            finally:
                context.close()
    
    def sync(self, force_full: bool = False) -> Dict[str, int]:
        """执行同步"""
        logger.info("=" * 60)
        logger.info("开始 Flomo 自动同步（安全模式）")
        logger.info("=" * 60)
        
        stats = {
            'exported': False,
            'new_notes': 0,
            'updated_notes': 0,
            'total_notes': 0,
            'attachments': 0,
            'errors': 0
        }
        
        # 1. 从 flomo 导出数据
        html_file = self.export_from_flomo()
        if not html_file:
            logger.error("导出失败，同步中止")
            return stats
        
        stats['exported'] = True
        
        # 2. 解析和转换
        try:
            parser = FlomoParser(str(html_file))
            notes = parser.parse()
            
            converter = ObsidianConverter(
                output_dir=str(self.output_dir),
                flomo_html_dir=str(html_file.parent),
                mode='by-date',
                tag_prefix=self.tag_prefix,
                copy_attachments=True,
                convert_to_wikilinks=True
            )
            
            result = converter.convert(notes)
            
            stats['new_notes'] = result['notes']
            stats['total_notes'] = result['notes']
            stats['attachments'] = result['attachments']
            stats['errors'] = result['errors']
            
            # 更新状态
            self.state['last_sync_time'] = datetime.now().isoformat()
            self.state['sync_count'] = self.state.get('sync_count', 0) + 1
            self._save_state()
            
            logger.info("=" * 60)
            logger.info("同步完成！")
            logger.info(f"  新笔记: {stats['new_notes']}")
            logger.info(f"  总笔记: {stats['total_notes']}")
            logger.info(f"  附件: {stats['attachments']}")
            logger.info(f"  错误: {stats['errors']}")
            logger.info(f"  同步次数: {self.state['sync_count']}")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"转换失败: {e}", exc_info=True)
            stats['errors'] = 1
        
        # 3. 清理旧的导出文件
        self._cleanup_old_exports()
        
        return stats
    
    def _cleanup_old_exports(self, keep_recent: int = 3):
        """清理旧的导出文件"""
        logger.info(f"清理旧的导出文件，保留最近 {keep_recent} 次...")
        
        # 查找所有导出目录
        export_dirs = sorted(
            [d for d in self.download_dir.glob('flomo_export_*') if d.is_dir()],
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        # 删除旧的
        for old_dir in export_dirs[keep_recent:]:
            try:
                shutil.rmtree(old_dir)
                logger.info(f"删除旧目录: {old_dir.name}")
            except Exception as e:
                logger.warning(f"删除失败: {old_dir}, {e}")
        
        # 删除旧的 ZIP 文件
        zip_files = sorted(
            [f for f in self.download_dir.glob('flomo_export_*.zip')],
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        for old_zip in zip_files[keep_recent:]:
            try:
                old_zip.unlink()
                logger.info(f"删除旧文件: {old_zip.name}")
            except Exception as e:
                logger.warning(f"删除失败: {old_zip}, {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Flomo 自动同步到 Obsidian（安全模式 - 不保存密码）'
    )
    parser.add_argument('--output', required=True, help='Obsidian vault 输出目录')
    parser.add_argument('--download-dir', default='flomo_downloads', help='下载目录')
    parser.add_argument('--user-data-dir', default='flomo_browser_data', 
                       help='浏览器数据目录（保存登录状态）')
    parser.add_argument('--tag-prefix', default='', help='标签前缀')
    parser.add_argument('--no-headless', action='store_true', help='显示浏览器窗口')
    parser.add_argument('--force-full', action='store_true', help='强制完整同步')
    parser.add_argument('--verbose', action='store_true', help='显示详细日志')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    syncer = FlomoAutoSyncSafe(
        output_dir=args.output,
        download_dir=args.download_dir,
        user_data_dir=args.user_data_dir,
        tag_prefix=args.tag_prefix,
        headless=not args.no_headless
    )
    
    stats = syncer.sync(force_full=args.force_full)
    
    # 输出结果
    print("\n" + "=" * 60)
    print("同步结果:")
    print(f"  导出成功: {'是' if stats['exported'] else '否'}")
    print(f"  新笔记: {stats['new_notes']}")
    print(f"  总笔记: {stats['total_notes']}")
    print(f"  附件: {stats['attachments']}")
    print(f"  错误: {stats['errors']}")
    print("=" * 60)


if __name__ == '__main__':
    main()
