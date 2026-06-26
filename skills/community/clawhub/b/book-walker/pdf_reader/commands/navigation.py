"""导航指令 - PDF Reader"""
from typing import Optional, Tuple, List, Dict, Any

from ..reader.parser import PDFParser
from ..reader.state import StateManager, ReadingState
from ..reader.blocks import BlockData
from ..reader.exceptions import NoPDFLoaded, InvalidCommand


class NavigationCommand:
    """导航指令处理器"""
    
    def __init__(self, parser: PDFParser, state_mgr: StateManager):
        self.parser = parser
        self.state_mgr = state_mgr
    
    def get_current_block(self) -> Tuple[Optional[int], Optional[BlockData]]:
        """获取当前块（按 global block_id 定位）"""
        state = self.state_mgr.get_state()
        
        if not state.pdf_path:
            raise NoPDFLoaded("未加载PDF")
        
        result = self.parser.get_block_by_global_id(state.current_block_idx)
        return result if result else (None, None)
    
    def next(self, mode: str = None) -> Dict[str, Any]:
        """下一块（块级导航，上层可按模板对整段加工）"""
        state = self.state_mgr.get_state()
        
        if not state.pdf_path:
            raise NoPDFLoaded("未加载PDF")
        
        return self._next_block()
    
    def _next_block(self) -> Dict[str, Any]:
        """下一块"""
        state = self.state_mgr.get_state()
        
        # 获取当前页的所有块
        blocks = self.parser.parse_page(state.current_page)
        
        if not blocks:
            # 当前页无块，翻页
            if state.current_page < state.total_pages:
                next_page = state.current_page + 1
                next_blocks = self.parser.parse_page(next_page)
                if next_blocks:
                    next_block = next_blocks[0]
                    self.state_mgr.update_position(
                        page=next_page,
                        block_idx=next_block.block_id,
                        line_idx=0
                    )
                    return {
                        "page": next_page,
                        "block": next_block.to_dict(),
                        "block_idx": next_block.block_id,
                        "line_idx": 0
                    }
            return {"end": True, "message": "已到达文档末尾"}
        
        # 查找当前块在页面中的位置
        local_idx = -1
        for i, b in enumerate(blocks):
            if b.block_id == state.current_block_idx:
                local_idx = i
                break
        
        # 如果当前块不在此页，使用第一块
        if local_idx == -1:
            local_idx = 0
        
        if local_idx < len(blocks) - 1:
            # 当前页还有块
            next_block = blocks[local_idx + 1]
            self.state_mgr.update_position(
                page=state.current_page,
                block_idx=next_block.block_id,
                line_idx=0
            )
            return {
                "page": state.current_page,
                "block": next_block.to_dict(),
                "block_idx": next_block.block_id,
                "line_idx": 0
            }
        else:
            # 翻到下一页
            if state.current_page < state.total_pages:
                next_page = state.current_page + 1
                next_blocks = self.parser.parse_page(next_page)
                
                if next_blocks:
                    next_block = next_blocks[0]
                    self.state_mgr.update_position(
                        page=next_page,
                        block_idx=next_block.block_id,
                        line_idx=0
                    )
                    return {
                        "page": next_page,
                        "block": next_block.to_dict(),
                        "block_idx": next_block.block_id,
                        "line_idx": 0
                    }
            
            # 已到末尾
            return {"end": True, "message": "已到达文档末尾"}
    
    def _next_line(self) -> Dict[str, Any]:
        """下一行"""
        state = self.state_mgr.get_state()
        
        page_num, block = self.get_current_block()
        
        if not block:
            return self._next_block()
        
        if state.current_line_idx < len(block.lines) - 1:
            # 当前块内还有行
            new_line_idx = state.current_line_idx + 1
            self.state_mgr.update_position(
                page=page_num,
                block_idx=block.block_id,
                line_idx=new_line_idx
            )
            
            line = block.lines[new_line_idx]
            return {
                "page": page_num,
                "block": block.to_dict(),
                "block_idx": block.block_id,
                "line_idx": new_line_idx,
                "line": line.to_dict()
            }
        else:
            # 当前块已读完，进入下一块
            return self._next_block()
    
    def _next_sentence(self) -> Dict[str, Any]:
        """下一句"""
        state = self.state_mgr.get_state()
        
        # 获取当前块
        page_num, block = self.get_current_block()
        
        if not block:
            return self._next_block()
        
        # 如果块还没有解析句子，先解析
        if not block.sentences:
            block.parse_sentences()
        
        # 当前块内还有句子
        if state.current_sentence_idx < len(block.sentences) - 1:
            next_idx = state.current_sentence_idx + 1
            self.state_mgr.update_position(
                page=page_num,
                block_idx=block.block_id,
                line_idx=0,
                sentence_idx=next_idx
            )
            sentence = block.sentences[next_idx]
            return {
                "page": page_num,
                "block": block.to_dict(),
                "block_idx": block.block_id,
                "sentence_idx": next_idx,
                "sentence": sentence.to_dict()
            }
        else:
            # 当前块句子已读完，进入下一块的第一句
            block_result = self._next_block()
            if block_result.get("end"):
                return block_result
            
            # 获取新块的第一句
            new_page = block_result["page"]
            new_block_id = block_result["block_idx"]
            _, new_block = self.parser.get_block_by_global_id(new_block_id)
            
            if new_block:
                if not new_block.sentences:
                    new_block.parse_sentences()
                
                if new_block.sentences:
                    self.state_mgr.update_position(
                        page=new_page,
                        block_idx=new_block_id,
                        line_idx=0,
                        sentence_idx=0
                    )
                    return {
                        "page": new_page,
                        "block": new_block.to_dict(),
                        "block_idx": new_block_id,
                        "sentence_idx": 0,
                        "sentence": new_block.sentences[0].to_dict()
                    }
            
            return block_result
    
    def previous(self) -> Dict[str, Any]:
        """上一块"""
        state = self.state_mgr.get_state()
        
        if not state.pdf_path:
            raise NoPDFLoaded("未加载PDF")
        
        # 获取前一全局块
        if state.current_block_idx > 0:
            prev_block_idx = state.current_block_idx - 1
            result = self.parser.get_block_by_global_id(prev_block_idx)
            
            if result:
                page_num, block = result
                self.state_mgr.update_position(
                    page=page_num,
                    block_idx=block.block_id,
                    line_idx=0
                )
                return {
                    "page": page_num,
                    "block": block.to_dict(),
                    "block_idx": block.block_id,
                    "line_idx": 0
                }
        
        return {"end": True, "message": "已到达文档开头"}
    
    def reread(self) -> Dict[str, Any]:
        """重读当前块"""
        return self.get_current_content()
    
    def get_current_content(self) -> Dict[str, Any]:
        """获取当前内容"""
        state = self.state_mgr.get_state()
        
        if not state.pdf_path:
            raise NoPDFLoaded("未加载PDF")
        
        page_num, block = self.get_current_block()
        
        if not block:
            return {"error": "无法获取当前内容"}
        
        return {
            "page": page_num,
            "block": block.to_dict(),
            "block_idx": block.block_id,
            "line_idx": state.current_line_idx
        }
    
    def jump_to_page(self, page_num: int) -> Dict[str, Any]:
        """跳转到指定页"""
        state = self.state_mgr.get_state()
        
        if not state.pdf_path:
            raise NoPDFLoaded("未加载PDF")
        
        if page_num < 1 or page_num > state.total_pages:
            raise InvalidCommand(f"页码无效: {page_num}")
        
        blocks = self.parser.parse_page(page_num)
        
        if not blocks:
            return {"error": f"第{page_num}页无内容"}
        
        first_block = blocks[0]
        self.state_mgr.update_position(
            page=page_num,
            block_idx=first_block.block_id,
            line_idx=0
        )
        
        return {
            "page": page_num,
            "block": first_block.to_dict(),
            "block_idx": first_block.block_id,
            "line_idx": 0
        }
    
    def jump_to_block(self, block_id: int) -> Dict[str, Any]:
        """跳转到指定块"""
        state = self.state_mgr.get_state()
        
        if not state.pdf_path:
            raise NoPDFLoaded("未加载PDF")
        
        if block_id < 0 or block_id >= state.total_blocks:
            raise InvalidCommand(f"块ID无效: {block_id}")
        
        result = self.parser.get_block_by_global_id(block_id)
        
        if not result:
            return {"error": f"无法跳转到块{block_id}"}
        
        page_num, block = result
        self.state_mgr.update_position(
            page=page_num,
            block_idx=block.block_id,
            line_idx=0
        )
        
        return {
            "page": page_num,
            "block": block.to_dict(),
            "block_idx": block.block_id,
            "line_idx": 0
        }
    
    def go_back(self) -> Optional[Dict]:
        """后退"""
        return self.state_mgr.go_back()
    
    def go_forward(self) -> Optional[Dict]:
        """前进"""
        return self.state_mgr.go_forward()
    
    def can_navigate(self) -> Dict[str, bool]:
        """是否可以导航"""
        return {
            "can_back": self.state_mgr.can_go_back(),
            "can_forward": self.state_mgr.can_go_forward()
        }
