"""输出格式化 - PDF Reader"""
import json
from pathlib import Path
from typing import Dict, Any, List

from ..reader.state import ReadingState
from ..constants import PAYLOAD_MARKER


class OutputFormatter:
    """输出格式化器"""
    
    def format_block(self, data: Dict[str, Any], state: ReadingState) -> str:
        """格式化块内容（块级导航，可选 LLM 模板加工后的文本）"""
        block = data.get("block", {})
        page = data.get("page", 1)
        block_idx = data.get("block_idx", 0)
        # 进度信息
        progress = self._format_progress(state)
        
        # 块类型标签
        block_type = block.get("type", "paragraph")
        
        # 标题（如果有）
        lines = block.get("lines", [])
        title = ""
        if block_type == "heading":
            if lines:
                title = f"【{lines[0]['text']}】\n"
        
        # 构建输出
        output = []
        output.append(f"📄 第{page}页 · 块{block_idx + 1}/{state.total_blocks} · {progress}")
        output.append("━" * 24)
        
        if title:
            output.append(title)
        
        # 文本内容
        for line in lines:
            output.append(line.get("text", ""))

        # 若有 template_payload：供 Agent 解析后调用 LLM 加工
        payload = data.get("template_payload")
        if payload:
            output.append("")
            output.append(f"--- [{PAYLOAD_MARKER}] ---")
            output.append("Agent: 请用下方 template_prompt 对 original 调用 LLM 加工（如 原文/翻译/解读），将 LLM 输出呈现给用户。")
            output.append(json.dumps(payload, ensure_ascii=False))
            output.append(f"--- [/{PAYLOAD_MARKER}] ---")
        
        # 图片信息
        images = block.get("images", [])
        if images:
            output.append("")
            for img in images:
                ref = img.get("ref", "")
                w = img.get("width", 0)
                h = img.get("height", 0)
                path = img.get("path") or ""
                if path:
                    output.append(f"[图片 {ref}] {w}x{h} · {path}")
                else:
                    output.append(f"[图片 {ref}] {w}x{h}")
        
        return "\n".join(output)
    
    def format_line(self, data: Dict[str, Any], state: ReadingState) -> str:
        """格式化单行内容"""
        block = data.get("block", {})
        page = data.get("page", 1)
        line_idx = data.get("line_idx", 0)
        
        lines = block.get("lines", [])
        
        if line_idx < len(lines):
            line = lines[line_idx]
            line_num = line.get("line_num", 0)
            text = line.get("text", "")
            
            progress = self._format_progress(state)
            output = [
                f"📄 第{page}页 · 行{line_num} · {progress}",
                "━" * 24,
                text
            ]
            return "\n".join(output)
        
        return "无法获取当前行"
    
    def format_sentence(self, data: Dict[str, Any], state: ReadingState) -> str:
        """格式化句子内容"""
        sentence = data.get("sentence", {})
        page = data.get("page", 1)
        block_idx = data.get("block_idx", 0)
        sentence_idx = data.get("sentence_idx", 0)
        
        # 获取的总句子数
        block = data.get("block", {})
        sentences = block.get("sentences", [])
        total_sentences = len(sentences)
        
        text = sentence.get("text", "")
        
        output = [
            f"📄 第{page}页 · 句{sentence_idx + 1}/{total_sentences}",
            "━" * 24,
            text,
            "",
            "💡 发送「下一句」继续"
        ]
        
        return "\n".join(output)
    
    def format_progress(self, state: ReadingState) -> str:
        """格式化进度"""
        progress = self._format_progress(state)
        output = [
            "📊 阅读进度",
            "━" * 16,
            f"📄 页码: {state.current_page}/{state.total_pages}",
            f"📦 块: {state.current_block_idx}/{state.total_blocks}",
            f"📈 进度: {progress}"
        ]
        return "\n".join(output)
    
    def format_search_results(self, results: List[Dict], keyword: str) -> str:
        """格式化搜索结果"""
        if not results:
            return f"未找到关键词: {keyword}"
        
        output = [f"🔍 搜索结果: '{keyword}' (共{len(results)}条)", "━" * 24]
        
        for i, r in enumerate(results[:10], 1):  # 最多显示10条
            page = r.get("page", 1)
            block_id = r.get("block_id", 0)
            snippet = r.get("snippet", "")
            
            output.append(f"{i}. 第{page}页 · 块{block_id}")
            output.append(f"   {snippet}")
            output.append("")
        
        if len(results) > 10:
            output.append(f"... 还有 {len(results) - 10} 条结果")
        
        return "\n".join(output)
    
    def format_bookmarks(self, bookmarks: List) -> str:
        """格式化书签列表"""
        if not bookmarks:
            return "暂无书签"
        
        output = ["🔖 书签列表", "━" * 16]
        
        for b in bookmarks:
            bid = b.id
            page = b.page
            block_id = b.block_id
            note = b.note
            created = b.created_at
            
            note_str = f" - {note}" if note else ""
            output.append(f"{bid}. 第{page}页 · 块{block_id}{note_str}")
            output.append(f"   添加于: {created}")
        
        return "\n".join(output)
    
    def format_help(self) -> str:
        """格式化帮助信息"""
        commands = [
            ("📖 开始读 <文件/序号>", "打开PDF，无参数时显示索引"),
            ("📚 列出PDF / 列表", "扫描 workspace 下所有 PDF 建立索引"),
            ("➡️ 下一句 / 继续", "读取下一块"),
            ("⬅️ 上一句 / 后退", "返回上一块"),
            ("🔄 重读", "重新读取当前块"),
            ("⏭️ 跳过", "跳过当前块"),
            ("📑 去第X页", "跳转到指定页"),
            ("🔢 跳到第X块", "跳转到指定块"),
            ("🔍 搜索 <关键词>", "搜索关键词"),
            ("🔖 书签", "查看/添加书签"),
            ("📝 模板 列表/使用/定义", "LLM 加工模板：按块导航、按句加工"),
            ("📊 进度", "显示阅读进度"),
            ("⏸️ 暂停", "暂停并保存位置"),
            ("❓ 帮助", "显示帮助信息"),
        ]
        
        output = ["❓ 可用指令", "━" * 16]
        
        for cmd, desc in commands:
            output.append(f"{cmd}")
            output.append(f"   {desc}")
            output.append("")
        
        return "\n".join(output)
    
    def format_pdf_list(self, workspace_root: Path, pdfs: List[Path]) -> str:
        """格式化 PDF 索引列表"""
        output = [
            f"📚 当前 Workspace 可读 PDF 索引",
            f"   路径: {workspace_root}",
            "━" * 24,
        ]
        if not pdfs:
            output.append("未找到 PDF 文件")
            output.append("")
            output.append("💡 使用「开始读 <路径>」打开 PDF")
            return "\n".join(output)
        output.append(f"共 {len(pdfs)} 个 PDF：")
        output.append("")
        try:
            root_str = str(workspace_root)
            for i, p in enumerate(pdfs, 1):
                path_str = str(p)
                if path_str.startswith(root_str):
                    rel = path_str[len(root_str) :].lstrip("/")
                else:
                    rel = path_str
                output.append(f"  {i}. {rel}")
        except Exception:
            for i, p in enumerate(pdfs, 1):
                output.append(f"  {i}. {p}")
        output.append("")
        output.append("💡 使用「开始读 <序号或路径>」打开，例如：")
        output.append(f"   开始读 1  或  开始读 {pdfs[0].name}")
        return "\n".join(output)
    
    def format_error(self, error: str) -> str:
        """格式化错误信息"""
        return f"❌ 错误: {error}"
    
    def format_end(self) -> str:
        """到达末尾"""
        return "✅ 已到达文档末尾"
    
    def format_start(self, data: Dict[str, Any], state: ReadingState) -> str:
        """格式化开始阅读"""
        return self.format_block(data, state)
    
    def _format_progress(self, state: ReadingState) -> str:
        """格式化进度条"""
        if state.total_blocks == 0:
            return "[░░░░░░░░░░] 0%"
        
        percentage = int((state.current_block_idx / state.total_blocks) * 100)
        filled = int(percentage / 10)
        bar = "█" * filled + "░" * (10 - filled)
        
        return f"[{bar}] {percentage}%"
    
    def _get_type_label(self, block_type: str) -> str:
        """获取块类型标签"""
        labels = {
            "heading": "标题",
            "paragraph": "正文",
            "caption": "图注",
            "image": "图片",
            "table": "表格",
            "formula": "公式",
            "mixed": "图文"
        }
        return labels.get(block_type, "正文")
