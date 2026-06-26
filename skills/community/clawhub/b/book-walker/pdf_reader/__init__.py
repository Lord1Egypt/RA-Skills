"""PDF Reader - 交互式PDF逐行阅读器"""
import os
import re
import logging
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any

from .reader.parser import PDFParser
from .reader.state import StateManager
from .reader.cache import PDFCache
from .reader.exceptions import (
    PDFReaderError, PDFEncrypted, PDFCorrupted,
    NoPDFLoaded, InvalidCommand
)
from .commands.navigation import NavigationCommand
from .ui.formatter import OutputFormatter
from .template.manager import TemplateManager
from .constants import PAYLOAD_MARKER

logger = logging.getLogger(__name__)


def _get_workspace_root() -> Path:
    """获取当前 workspace 根目录。优先环境变量，否则从 skill 路径推导。"""
    env_root = os.environ.get("OPENCLAW_WORKSPACE") or os.environ.get("WORKSPACE_ROOT")
    if env_root and Path(env_root).is_dir():
        return Path(env_root)
    # pdf_reader/__init__.py -> pdf_reader -> pdf-reader -> skills -> workspace
    skill_init = Path(__file__).resolve()
    skills_dir = skill_init.parent.parent.parent
    if skills_dir.name == "skills" and skills_dir.parent.is_dir():
        return skills_dir.parent
    return skill_init.parent.parent


def scan_workspace_pdfs() -> Tuple[Path, List[Path]]:
    """扫描 workspace 下所有 PDF 文件。返回 (workspace_root, [pdf_paths])"""
    root = _get_workspace_root()
    pdfs: List[Path] = []
    try:
        for p in root.rglob("*.pdf"):
            if p.is_file():
                pdfs.append(p.resolve())
    except (PermissionError, OSError) as e:
        logger.warning("扫描 workspace 时出错: %s", e)
    pdfs.sort(key=lambda x: str(x).lower())
    return root, pdfs


class PDFReader:
    """PDF阅读器主类 - 块级导航，返回 structured payload 供 Agent 调用 LLM 加工"""

    def __init__(self):
        self.parser: Optional[PDFParser] = None
        self.state_mgr = StateManager()
        self.cache = PDFCache()
        self.formatter = OutputFormatter()
        self.nav_cmd: Optional[NavigationCommand] = None
        self.template_mgr = TemplateManager()

    def _block_text(self, data: Dict[str, Any]) -> str:
        """从块数据提取纯文本"""
        block = data.get("block", {})
        lines = block.get("lines", [])
        return "\n".join(line.get("text", "") for line in lines).strip()

    def _attach_template_payload(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """附加模板 payload，供 Agent 解析后调用 LLM"""
        if "block" not in result or "end" in result or "error" in result:
            return result
        template = self.template_mgr.get_current_prompt()
        if not template or template == "请直接输出原文。":
            return result
        text = self._block_text(result)
        if not text:
            return result
        result = dict(result)
        result["template_payload"] = {
            "template_prompt": template,
            "original": text,
            "page": result.get("page", 1),
            "block_id": result.get("block_idx", 0),
        }
        return result
    
    def _ensure_parser(self) -> bool:
        """确保parser已初始化，如果状态中有PDF则恢复"""
        if self.parser is not None:
            return True
        
        # 检查状态中是否有已打开的PDF
        state = self.state_mgr.get_state()
        if state.pdf_path:
            try:
                self.parser = PDFParser(state.pdf_path, cache=self.cache)
                self.parser.open()
                self.nav_cmd = NavigationCommand(self.parser, self.state_mgr)
                return True
            except Exception:
                return False
        
        return False
    
    def open(self, pdf_path: str) -> str:
        """打开PDF文件"""
        path = Path(pdf_path)
        
        if not path.exists():
            return self.formatter.format_error(f"文件不存在: {pdf_path}")
        
        if self.parser:
            self.parser.close()
        
        self.state_mgr.switch_to_pdf(pdf_path, self.cache)
        
        try:
            self.parser = PDFParser(pdf_path, cache=self.cache)
            metadata = self.parser.open()
            total_blocks = self.parser.get_total_blocks()
            metadata.total_blocks = total_blocks
            
            state = self.state_mgr.get_state()
            if state.pdf_path != pdf_path or state.total_blocks != total_blocks:
                first_blocks = self.parser.parse_page(1)
                first_block_id = first_blocks[0].block_id if first_blocks else 0
                self.state_mgr.set_pdf(
                    pdf_path=pdf_path,
                    total_pages=metadata.total_pages,
                    total_blocks=total_blocks,
                    first_block_id=first_block_id
                )
            
            # 初始化导航命令
            self.nav_cmd = NavigationCommand(self.parser, self.state_mgr)
            
            # 获取第一块
            result = self.nav_cmd.get_current_content()
            result = self._attach_template_payload(result)
            return self.formatter.format_start(result, self.state_mgr.get_state())
            
        except PDFEncrypted:
            return self.formatter.format_error("PDF已加密，无法打开")
        except PDFCorrupted as e:
            return self.formatter.format_error(f"PDF损坏: {e}")
        except Exception as e:
            logger.exception("打开PDF失败")
            return self.formatter.format_error(f"打开失败: {e}")
    
    def next(self) -> str:
        """下一块/行"""
        # 确保PDF已打开
        if not self._ensure_parser():
            return self.formatter.format_error("请先打开PDF")
        
        try:
            result = self.nav_cmd.next()
            if result.get("end"):
                return self.formatter.format_end()
            result = self._attach_template_payload(result)
            state = self.state_mgr.get_state()
            return self.formatter.format_block(result, state)
            
        except Exception as e:
            logger.exception("读取下一块失败")
            return self.formatter.format_error(str(e))
    
    def previous(self) -> str:
        """上一块"""
        if not self._ensure_parser():
            return self.formatter.format_error("请先打开PDF")
        
        try:
            result = self.nav_cmd.previous()
            if result.get("end"):
                return "已到达文档开头"
            result = self._attach_template_payload(result)
            state = self.state_mgr.get_state()
            return self.formatter.format_block(result, state)
            
        except Exception as e:
            logger.exception("读取上一块失败")
            return self.formatter.format_error(str(e))
    
    def reread(self) -> str:
        """重读当前块"""
        if not self._ensure_parser():
            return self.formatter.format_error("请先打开PDF")
        
        try:
            result = self.nav_cmd.reread()
            result = self._attach_template_payload(result)
            state = self.state_mgr.get_state()
            return self.formatter.format_block(result, state)
            
        except Exception as e:
            logger.exception("重读失败")
            return self.formatter.format_error(str(e))
    
    def jump_to_page(self, page_num: int) -> str:
        """跳转到指定页"""
        if not self._ensure_parser():
            return self.formatter.format_error("请先打开PDF")
        
        try:
            result = self.nav_cmd.jump_to_page(page_num)
            if "error" in result:
                return self.formatter.format_error(result["error"])
            result = self._attach_template_payload(result)
            state = self.state_mgr.get_state()
            return self.formatter.format_block(result, state)
            
        except Exception as e:
            logger.exception("跳转失败")
            return self.formatter.format_error(str(e))
    
    def jump_to_block(self, block_id: int) -> str:
        """跳转到指定块"""
        if not self._ensure_parser():
            return self.formatter.format_error("请先打开PDF")
        
        try:
            result = self.nav_cmd.jump_to_block(block_id)
            if "error" in result:
                return self.formatter.format_error(result["error"])
            result = self._attach_template_payload(result)
            state = self.state_mgr.get_state()
            return self.formatter.format_block(result, state)
            
        except Exception as e:
            logger.exception("跳转失败")
            return self.formatter.format_error(str(e))
    
    def search(self, keyword: str) -> str:
        """搜索关键词"""
        if not self._ensure_parser():
            return self.formatter.format_error("请先打开PDF")
        
        try:
            results = self.parser.search(keyword)
            return self.formatter.format_search_results(results, keyword)
            
        except Exception as e:
            logger.exception("搜索失败")
            return self.formatter.format_error(str(e))
    
    def bookmarks(self, action: str = "list", note: str = "") -> str:
        """书签操作"""
        if not self._ensure_parser():
            return self.formatter.format_error("请先打开PDF")
        
        try:
            if action == "list":
                bookmarks = self.state_mgr.get_bookmarks()
                return self.formatter.format_bookmarks(bookmarks)
            
            elif action == "add":
                state = self.state_mgr.get_state()
                bookmark = self.state_mgr.add_bookmark(
                    page=state.current_page,
                    block_id=state.current_block_idx,
                    note=note
                )
                return f"✅ 已添加书签: 第{bookmark.page}页 · 块{bookmark.block_id}"
            
            return self.formatter.format_error(f"未知操作: {action}")
            
        except Exception as e:
            logger.exception("书签操作失败")
            return self.formatter.format_error(str(e))
    
    def progress(self) -> str:
        """显示进度"""
        if not self._ensure_parser():
            return self.formatter.format_error("请先打开PDF")
        
        state = self.state_mgr.get_state()
        return self.formatter.format_progress(state)
    
    def help(self) -> str:
        """显示帮助"""
        return self.formatter.format_help()
    
    def list_pdfs(self) -> str:
        """扫描 workspace 下的 PDF 并返回索引"""
        root, pdfs = scan_workspace_pdfs()
        return self.formatter.format_pdf_list(root, pdfs)
    
    def execute(self, command: str) -> str:
        """执行指令"""
        command = command.strip()
        
        # 解析指令
        if command.startswith("开始读 ") or command.startswith("打开 "):
            arg = command.split(" ", 1)[1].strip()
            if not arg:
                return self.list_pdfs()
            _, pdfs = scan_workspace_pdfs()
            if arg.isdigit() and pdfs:
                idx = int(arg)
                if 1 <= idx <= len(pdfs):
                    return self.open(str(pdfs[idx - 1]))
            return self.open(arg)
        
        elif command in ["列出PDF", "有哪些PDF", "PDF列表", "列表", "list"]:
            return self.list_pdfs()
        
        elif command in ["下一句", "继续", "next"]:
            return self.next()
        
        elif command in ["上一句", "后退", "previous", "prev"]:
            return self.previous()
        
        elif command in ["重读", "再念一遍", "reread"]:
            return self.reread()
        
        elif command.startswith("去第"):
            # 提取页码
            match = re.search(r"去第(\d+)页", command)
            if match:
                page_num = int(match.group(1))
                return self.jump_to_page(page_num)
            return self.formatter.format_error("指令格式错误")
        
        elif command.startswith("跳到第") and "块" in command:
            # 跳转到块
            match = re.search(r"跳到第(\d+)块", command)
            if match:
                block_id = int(match.group(1))
                return self.jump_to_block(block_id)
            return self.formatter.format_error("指令格式错误")
        
        elif command.startswith("跳到第") and "行" in command:
            # 跳转到行（暂按块处理）
            match = re.search(r"跳到第(\d+)行", command)
            if match:
                line_num = int(match.group(1))
                # 简化处理：跳到对应块
                return self.jump_to_block(line_num)
            return self.formatter.format_error("指令格式错误")
        
        elif command.startswith("搜索 "):
            keyword = command.split(" ", 1)[1].strip()
            return self.search(keyword)
        
        elif command.startswith("书签"):
            parts = command.split()
            if len(parts) == 1:
                return self.bookmarks("list")
            elif parts[1] == "添加":
                note = " ".join(parts[2:]) if len(parts) > 2 else ""
                return self.bookmarks("add", note)
            elif parts[1] == "列表":
                return self.bookmarks("list")
            return self.formatter.format_error("指令格式错误")
        
        elif command in ["进度", "progress"]:
            return self.progress()
        
        elif command.startswith("模式 "):
            # 切换提取模式：模式 text | 模式 ocr
            parts = command[3:].strip().split()
            if not parts:
                current = self.parser.get_extract_mode() if self.parser else "text"
                return f"当前模式: {current}\n用法: 模式 text | 模式 ocr\n- text: 文本模式（默认，使用 pdfplumber 提取）\n- ocr: OCR 模式（需要 tesseract，适合扫描件）"
            mode = parts[0]
            if mode in ("text", "ocr"):
                if self.parser:
                    # 清除缓存，确保用新模式重新解析
                    self.parser._pages_data.clear()
                    self.parser.set_extract_mode(mode)
                # 保存到状态
                state = self.state_mgr.get_state()
                state.extract_mode = mode
                self.state_mgr.update_position(state.current_page, state.current_block_idx)
                return f"✅ 已切换到 {mode} 模式。下次读取时会用新模式解析当前页。"
            return self.formatter.format_error("未知模式: text 或 ocr")
        
        elif command in ["帮助", "help", "?"]:
            return self.help()

        elif command.startswith("模板 "):
            parts = command[3:].strip().split(None, 2)  # 模板 <cmd> [args...]
            if not parts:
                current = self.template_mgr.get_current_name()
                return f"当前模板: {current}\n用法: 模板 列表 | 模板 使用 <名> | 模板 定义 <名> <内容>"
            cmd = parts[0]
            if cmd == "列表":
                names = self.template_mgr.list_templates()
                cur = self.template_mgr.get_current_name()
                lines = [f"可用模板: {', '.join(names)}", f"当前: {cur}"]
                return "\n".join(lines)
            elif cmd == "使用" and len(parts) >= 2:
                return self.template_mgr.use(parts[1])
            elif cmd == "定义" and len(parts) >= 3:
                return self.template_mgr.define(parts[1], parts[2])
            elif cmd == "定义" and len(parts) == 2:
                return self.formatter.format_error("请提供模板内容，如: 模板 定义 名 请翻译...")
            return self.formatter.format_error(f"未知子命令: 模板 {cmd}")
        
        elif command in ["暂停", "pause"]:
            return "⏸️ 已暂停阅读，下次继续"
        
        elif command in ["关闭", "结束", "close"]:
            if self.parser:
                self.parser.close()
                self.parser = None
                self.nav_cmd = None
            self.state_mgr.clear_active_pdf()
            return "✅ 已关闭PDF"
        
        else:
            return self.formatter.format_error(f"未知指令: {command}\n输入'帮助'查看可用指令")
    
    def close(self):
        """关闭PDF"""
        if self.parser:
            self.parser.close()
            self.parser = None
            self.nav_cmd = None
        self.state_mgr.clear_active_pdf()


# 全局实例
_reader: Optional[PDFReader] = None


def get_reader() -> PDFReader:
    """获取全局Reader实例"""
    global _reader
    if _reader is None:
        _reader = PDFReader()
    return _reader


def handle_message(message: str) -> str:
    """处理消息"""
    reader = get_reader()
    return reader.execute(message)
