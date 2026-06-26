from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import deque
import hashlib


@dataclass
class ContextWindow:
    window_id: int
    content: str
    token_count: int
    importance_score: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class SlidingWindowManager:
    def __init__(
        self,
        max_window_size: int = 4000,
        overlap_size: int = 500,
        min_chunk_size: int = 200
    ):
        self.max_window_size = max_window_size
        self.overlap_size = overlap_size
        self.min_chunk_size = min_chunk_size
        self.windows: deque = deque()
        self.window_counter = 0
        self.total_content = ""
        self.important_segments: List[Dict[str, Any]] = []

    def add_content(self, content: str, importance: float = 1.0) -> List[ContextWindow]:
        self.total_content += content

        new_windows = []

        if self.windows:
            last_window = self.windows[-1]
            combined = last_window.content + content

            if self._estimate_tokens(combined) <= self.max_window_size:
                updated_window = ContextWindow(
                    window_id=last_window.window_id,
                    content=combined,
                    token_count=self._estimate_tokens(combined),
                    importance_score=max(last_window.importance_score, importance)
                )
                self.windows[-1] = updated_window
                new_windows.append(updated_window)
                return new_windows

        chunks = self._split_into_chunks(content)

        for chunk in chunks:
            self.window_counter += 1
            window = ContextWindow(
                window_id=self.window_counter,
                content=chunk,
                token_count=self._estimate_tokens(chunk),
                importance_score=importance
            )
            self.windows.append(window)
            new_windows.append(window)

        self._enforce_window_limit()

        return new_windows

    def _split_into_chunks(self, content: str) -> List[str]:
        chunks = []
        current_chunk = ""

        paragraphs = content.split('\n')

        for para in paragraphs:
            if self._estimate_tokens(current_chunk + para) > self.max_window_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    overlap_text = self._get_overlap_text(current_chunk)
                    current_chunk = overlap_text + para + '\n'
                else:
                    sentences = self._split_long_paragraph(para)
                    for sentence in sentences:
                        if self._estimate_tokens(current_chunk + sentence) > self.max_window_size:
                            if current_chunk:
                                chunks.append(current_chunk.strip())
                                overlap_text = self._get_overlap_text(current_chunk)
                                current_chunk = overlap_text + sentence
                            else:
                                chunks.append(sentence)
                        else:
                            current_chunk += sentence
            else:
                current_chunk += para + '\n'

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks if chunks else [content]

    def _split_long_paragraph(self, text: str) -> List[str]:
        sentences = []
        current = ""

        for char in text:
            current += char
            if char in '。！？':
                if self._estimate_tokens(current) >= self.min_chunk_size:
                    sentences.append(current)
                    current = ""

        if current:
            sentences.append(current)

        return sentences if sentences else [text]

    def _get_overlap_text(self, text: str) -> str:
        tokens = list(text)
        if len(tokens) <= self.overlap_size:
            return text

        overlap_start = len(tokens) - self.overlap_size
        overlap_text = ''.join(tokens[overlap_start:])

        sentence_start = overlap_text.find('。')
        if sentence_start != -1:
            overlap_text = overlap_text[sentence_start + 1:]

        return overlap_text

    def _estimate_tokens(self, text: str) -> int:
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        other_chars = len(text) - chinese_chars
        return chinese_chars + other_chars // 4

    def _enforce_window_limit(self, max_windows: int = 20):
        while len(self.windows) > max_windows:
            self.windows.popleft()

    def get_active_context(self, max_tokens: int = None) -> str:
        max_tokens = max_tokens or self.max_window_size

        context_parts = []
        current_tokens = 0

        for window in reversed(list(self.windows)):
            if current_tokens + window.token_count <= max_tokens:
                context_parts.insert(0, window.content)
                current_tokens += window.token_count
            else:
                remaining = max_tokens - current_tokens
                if remaining > self.min_chunk_size:
                    truncated = self._truncate_to_tokens(window.content, remaining)
                    context_parts.insert(0, truncated)
                break

        return '\n\n'.join(context_parts)

    def _truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        tokens = list(text)
        if len(tokens) <= max_tokens:
            return text

        truncated = ''.join(tokens[:max_tokens])
        last_sentence = max(
            truncated.rfind('。'),
            truncated.rfind('！'),
            truncated.rfind('？')
        )

        if last_sentence > max_tokens * 0.5:
            return truncated[:last_sentence + 1]

        return truncated

    def mark_important_segment(
        self,
        content: str,
        reason: str,
        importance: float = 2.0
    ):
        segment_hash = hashlib.md5(content.encode()).hexdigest()

        self.important_segments.append({
            'hash': segment_hash,
            'content': content,
            'reason': reason,
            'importance': importance
        })

        for i, window in enumerate(self.windows):
            if content in window.content:
                self.windows[i] = ContextWindow(
                    window_id=window.window_id,
                    content=window.content,
                    token_count=window.token_count,
                    importance_score=max(window.importance_score, importance),
                    metadata={'important_reason': reason}
                )

    def get_important_context(self) -> str:
        if not self.important_segments:
            return ""

        important_parts = []
        for segment in self.important_segments:
            important_parts.append(f"[重要：{segment['reason']}]\n{segment['content']}")

        return '\n\n'.join(important_parts)

    def get_context_for_query(
        self,
        query: str,
        max_tokens: int = 2000
    ) -> Tuple[str, Dict[str, Any]]:
        active_context = self.get_active_context(max_tokens)
        important_context = self.get_important_context()

        combined_context = ""
        if important_context:
            combined_context = f"【重要上下文】\n{important_context}\n\n"
        combined_context += f"【近期上下文】\n{active_context}"

        metadata = {
            'total_windows': len(self.windows),
            'total_tokens': sum(w.token_count for w in self.windows),
            'important_segments': len(self.important_segments),
            'active_tokens': self._estimate_tokens(active_context)
        }

        return combined_context, metadata

    def summarize_windows(self) -> str:
        if not self.windows:
            return "暂无上下文"

        summary_parts = []
        for i, window in enumerate(self.windows):
            preview = window.content[:100] + "..." if len(window.content) > 100 else window.content
            importance_marker = "★" if window.importance_score >= 2.0 else ""
            summary_parts.append(
                f"[窗口{window.window_id}] {window.token_count}tokens {importance_marker}\n{preview}"
            )

        return '\n\n'.join(summary_parts)

    def clear_old_windows(self, keep_recent: int = 5):
        while len(self.windows) > keep_recent:
            self.windows.popleft()

    def get_statistics(self) -> Dict[str, Any]:
        return {
            'total_windows': len(self.windows),
            'total_tokens': sum(w.token_count for w in self.windows),
            'avg_window_tokens': sum(w.token_count for w in self.windows) / max(len(self.windows), 1),
            'important_segments': len(self.important_segments),
            'oldest_window_id': self.windows[0].window_id if self.windows else None,
            'newest_window_id': self.windows[-1].window_id if self.windows else None
        }
