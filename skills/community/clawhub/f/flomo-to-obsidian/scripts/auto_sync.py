#!/usr/bin/env python3
"""
Flomo Auto Sync to Obsidian
使用浏览器自动化实现 flomo 到 Obsidian 的自动同步
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


class FlomoAutoSync:
    """Flomo 自动同步器"""
    
    def __init__(
        self,
        email: str,
        password: str,
        output_dir: str,
        download_dir: str,
        state_file: str = '.flomo_sync_state.json',
        tag_prefix: str = '',
        headless: bool = True
    ):
        self.email = email
        self.password = password
        self.output_dir = Path(output_dir)
        self.download_dir = Path(download_dir)
        self.state_file = Path(state_file)
        self.tag_prefix = tag_prefix
        self.headless = headless
        
        # 创建必要的目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.download_dir.mkdir(parents=True, exist_ok=True)
        
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
            'synced_notes': {},  # timestamp -> note_id
            'last_export_file': None,
            'sync_count': 0
        }
    
    def _save_state(self):
        """保存同步状态"""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, ensure_ascii=False, indent=2)
            logger.info(f"状态已保存到: {self.state_file}")
        except Exception as e:
            logger.error(f"保存状态文件失败: {e}")
    
    def export_from_flomo(self) -> Optional[Path]:
        """使用浏览器自动化从 flomo 导出数据"""
        logger.info("开始浏览器自动化导出...")
        
        with sync_playwright() as p:
            # 启动浏览器
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(
                accept_downloads=True,
                viewport={'width': 1280, 'height': 720}
            )
            page = context.new_page()
            
            try:
                # 1. 访问 flomo 登录页
                logger.info("访问 flomo 登录页...")
                page.goto('https://v.flomoapp.com/login', wait_until='networkidle', timeout=30000)
                time.sleep(2)
                
                # 检查是否已经登录（如果已跳转到 mine 页面）
                current_url = page.url
                if '/mine' in current_url:
                    logger.info("检测到已登录状态，跳过登录步骤")
                else:
                    # 2. 登录
                    logger.info("正在登录...")
                    
                    # 输入邮箱/手机号（支持多种输入框类型）
                    email_selectors = [
                        'input[type="email"]',
                        'input[type="tel"]',
                        'input[type="text"]',
                        'input[placeholder*="邮箱"]',
                        'input[placeholder*="手机"]',
                        'input[placeholder*="账号"]',
                        'input[name*="email"]',
                        'input[name*="phone"]',
                        'input[name*="account"]'
                    ]
                    
                    email_input = None
                    for selector in email_selectors:
                        locator = page.locator(selector).first
                        if locator.count() > 0:
                            email_input = locator
                            logger.info(f"找到账号输入框: {selector}")
                            break
                    
                    if email_input:
                        email_input.fill(self.email)
                    else:
                        logger.error("找不到邮箱/手机号输入框")
                        # 截图调试
                        screenshot_path = self.download_dir / f'error_login_{int(time.time())}.png'
                        page.screenshot(path=str(screenshot_path))
                        logger.error(f"已保存错误截图: {screenshot_path}")
                        return None
                    
                    # 输入密码
                    password_input = page.locator('input[type="password"], input[placeholder*="密码"], input[name*="password"]').first
                    if password_input.count() > 0:
                        password_input.fill(self.password)
                    else:
                        logger.error("找不到密码输入框")
                        return None
                    
                    # 点击登录按钮
                    login_button = page.locator('button:has-text("登录"), button:has-text("登錄"), button[type="submit"]').first
                    if login_button.count() > 0:
                        login_button.click()
                        logger.info("已点击登录按钮，等待跳转...")
                    else:
                        logger.error("找不到登录按钮")
                        return None
                    
                    # 等待登录成功（等待跳转到主页）
                    try:
                        page.wait_for_url('**/mine**', timeout=15000)
                        logger.info("登录成功！")
                    except PlaywrightTimeout:
                        logger.warning("登录跳转超时，尝试继续...")
                
                time.sleep(3)
                
                # 3. 点击用户名打开菜单
                logger.info("点击用户名打开菜单...")
                
                # 通过文本查找用户名（更可靠）
                try:
                    # 尝试多种方式
                    user_element = None
                    if page.get_by_text(self.email).count() > 0:
                        user_element = page.get_by_text(self.email).first
                    elif page.locator('text=/Ryan\\.B|用户|头像/i').count() > 0:
                        user_element = page.locator('text=/Ryan\\.B|用户|头像/i').first
                    
                    if user_element:
                        user_element.click()
                        logger.info("成功点击用户名")
                    else:
                        # 如果找不到，尝试点击左上角区域
                        page.mouse.click(100, 50)
                        logger.info("尝试点击左上角用户区域")
                    
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
                
                # 6. 保存下载的文件
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                download_path = self.download_dir / f'flomo_export_{timestamp}.zip'
                download.save_as(str(download_path))
                
                logger.info(f"下载完成: {download_path}")
                
                # 7. 解压文件
                extract_dir = self.download_dir / f'flomo_export_{timestamp}'
                extract_dir.mkdir(exist_ok=True)
                
                with zipfile.ZipFile(download_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                
                logger.info(f"解压完成: {extract_dir}")
                
                # 查找 HTML 文件（递归查找，因为可能在子目录中）
                html_files = list(extract_dir.glob('**/*.html'))
                if not html_files:
                    logger.error("解压后找不到 HTML 文件")
                    logger.error(f"解压目录内容: {list(extract_dir.iterdir())}")
                    return None
                
                html_file = html_files[0]
                logger.info(f"找到 HTML 文件: {html_file}")
                
                # 记录 file 目录路径（用于复制附件）
                file_dir = html_file.parent / 'file'
                if file_dir.exists():
                    logger.info(f"找到附件目录: {file_dir}")
                else:
                    logger.warning("未找到附件目录")
                
                return html_file
                
            except Exception as e:
                logger.error(f"浏览器自动化出错: {e}", exc_info=True)
                # 截图调试
                try:
                    screenshot_path = self.download_dir / 'error_screenshot.png'
                    page.screenshot(path=str(screenshot_path))
                    logger.info(f"已保存错误截图: {screenshot_path}")
                except:
                    pass
                return None
            
            finally:
                browser.close()
    
    def sync(self, force_full: bool = False) -> Dict[str, int]:
        """执行同步"""
        logger.info("=" * 60)
        logger.info("开始 Flomo 自动同步")
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
        
        # 2. 解析 HTML
        try:
            parser = FlomoParser(str(html_file))
            notes = parser.parse()
            stats['total_notes'] = len(notes)
            
            logger.info(f"解析到 {len(notes)} 条笔记")
            
        except Exception as e:
            logger.error(f"解析 HTML 失败: {e}", exc_info=True)
            stats['errors'] += 1
            return stats
        
        # 3. 增量检测
        if not force_full and self.state['synced_notes']:
            logger.info("执行增量同步...")
            
            # 找出新笔记
            new_notes = []
            for note in notes:
                timestamp = note.timestamp
                if timestamp not in self.state['synced_notes']:
                    new_notes.append(note)
            
            if not new_notes:
                logger.info("没有新笔记，同步完成")
                self.state['last_sync_time'] = datetime.now().isoformat()
                self._save_state()
                return stats
            
            logger.info(f"发现 {len(new_notes)} 条新笔记")
            notes = new_notes
            stats['new_notes'] = len(new_notes)
        else:
            logger.info("执行完整同步...")
            stats['new_notes'] = len(notes)
        
        # 4. 转换为 Obsidian 格式
        try:
            html_dir = html_file.parent
            converter = ObsidianConverter(
                output_dir=str(self.output_dir),
                flomo_html_dir=str(html_dir),
                mode='by-date',
                tag_prefix=self.tag_prefix,
                preserve_time=False,
                copy_attachments=True,
                convert_to_wikilinks=True
            )
            
            conversion_stats = converter.convert(notes)
            stats['attachments'] = conversion_stats.get('attachments', 0)
            stats['errors'] = conversion_stats.get('errors', 0)
            
            logger.info(f"转换完成: {conversion_stats}")
            
        except Exception as e:
            logger.error(f"转换失败: {e}", exc_info=True)
            stats['errors'] += 1
            return stats
        
        # 5. 更新同步状态
        for note in notes:
            self.state['synced_notes'][note.timestamp] = note.note_id
        
        self.state['last_sync_time'] = datetime.now().isoformat()
        self.state['last_export_file'] = str(html_file)
        self.state['sync_count'] += 1
        self._save_state()
        
        logger.info("=" * 60)
        logger.info("同步完成！")
        logger.info(f"  新笔记: {stats['new_notes']}")
        logger.info(f"  总笔记: {stats['total_notes']}")
        logger.info(f"  附件: {stats['attachments']}")
        logger.info(f"  错误: {stats['errors']}")
        logger.info(f"  同步次数: {self.state['sync_count']}")
        logger.info("=" * 60)
        
        return stats
    
    def cleanup_old_exports(self, keep_last: int = 3):
        """清理旧的导出文件"""
        logger.info(f"清理旧的导出文件，保留最近 {keep_last} 次...")
        
        # 查找所有导出文件和目录
        export_files = sorted(self.download_dir.glob('flomo_export_*.zip'))
        export_dirs = sorted(self.download_dir.glob('flomo_export_*'))
        
        # 删除旧文件
        for f in export_files[:-keep_last]:
            try:
                f.unlink()
                logger.info(f"删除旧文件: {f.name}")
            except Exception as e:
                logger.warning(f"删除文件失败 {f}: {e}")
        
        # 删除旧目录
        for d in export_dirs[:-keep_last]:
            try:
                if d.is_dir():
                    shutil.rmtree(d)
                    logger.info(f"删除旧目录: {d.name}")
            except Exception as e:
                logger.warning(f"删除目录失败 {d}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Flomo 自动同步到 Obsidian（使用浏览器自动化）'
    )
    parser.add_argument('--email', required=True, help='Flomo 登录邮箱')
    parser.add_argument('--password', required=True, help='Flomo 登录密码')
    parser.add_argument('--output', '-o', required=True, help='Obsidian vault 输出目录')
    parser.add_argument('--download-dir', default='./flomo_downloads', help='下载临时目录')
    parser.add_argument('--state-file', default='.flomo_sync_state.json', help='同步状态文件')
    parser.add_argument('--tag-prefix', default='flomo/', help='标签前缀')
    parser.add_argument('--force-full', action='store_true', help='强制完整同步')
    parser.add_argument('--no-headless', action='store_true', help='显示浏览器窗口（调试用）')
    parser.add_argument('--cleanup', type=int, default=3, help='保留最近 N 次导出文件')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细日志')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        syncer = FlomoAutoSync(
            email=args.email,
            password=args.password,
            output_dir=args.output,
            download_dir=args.download_dir,
            state_file=args.state_file,
            tag_prefix=args.tag_prefix,
            headless=not args.no_headless
        )
        
        # 执行同步
        stats = syncer.sync(force_full=args.force_full)
        
        # 清理旧文件
        if args.cleanup > 0:
            syncer.cleanup_old_exports(keep_last=args.cleanup)
        
        # 输出结果
        print("\n" + "=" * 60)
        print("同步结果:")
        print(f"  导出成功: {'是' if stats['exported'] else '否'}")
        print(f"  新笔记: {stats['new_notes']}")
        print(f"  总笔记: {stats['total_notes']}")
        print(f"  附件: {stats['attachments']}")
        print(f"  错误: {stats['errors']}")
        print("=" * 60)
        
        return 0 if stats['errors'] == 0 else 1
        
    except KeyboardInterrupt:
        logger.info("用户中断同步")
        return 130
    except Exception as e:
        logger.error(f"同步失败: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
