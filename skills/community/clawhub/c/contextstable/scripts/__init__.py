from typing import Dict, Any, Optional, List
from pathlib import Path

from .vector_store import VectorContextStore
from .anchor_manager import AnchorManager
from .anchor_extractor import AnchorExtractor
from .consistency_checker import ConsistencyChecker
from .history_manager import HistoryManager
from .context_window import SlidingWindowManager
from .cache_manager import CacheManager
from .config import ContextConfig, config


class LongTextContextStabilizer:
    def __init__(self, custom_config: ContextConfig = None):
        self.config = custom_config or config

        self.vector_store = VectorContextStore()
        self.anchor_manager = AnchorManager()
        self.anchor_extractor = AnchorExtractor()
        self.consistency_checker = ConsistencyChecker(self.vector_store)
        self.history_manager = HistoryManager(
            max_history=self.config.history.max_history,
            auto_save=self.config.history.auto_save,
            save_path=self.config.history.save_path
        )
        self.window_manager = SlidingWindowManager(
            max_window_size=self.config.window.max_window_size,
            overlap_size=self.config.window.overlap_size,
            min_chunk_size=self.config.window.min_chunk_size
        )
        self.cache_manager = CacheManager(
            embedding_cache_size=self.config.embedding.cache_size,
            prompt_cache_size=100,
            summary_cache_size=50,
            ttl_seconds=self.config.embedding.cache_ttl
        )

        self._initialized = False
        self._source_text = ""

    def init_long_text(
        self,
        long_text: str,
        manual_anchors: Dict[str, str] = None,
        auto_extract: bool = True
    ):
        self._source_text = long_text
        self._initialized = True

        self.vector_store.add_long_text(long_text)

        self.window_manager.add_content(long_text)

        if manual_anchors:
            self.anchor_manager.set_anchors_manually(manual_anchors)

        if auto_extract and not manual_anchors:
            extracted_anchors = self.anchor_extractor.extract_anchors(long_text)
            self.anchor_manager.set_anchors_manually(extracted_anchors)
        elif auto_extract and manual_anchors:
            extracted_anchors = self.anchor_extractor.extract_anchors(long_text)
            combined = {**extracted_anchors, **manual_anchors}
            self.anchor_manager.set_anchors_manually(combined)

    def get_enhanced_prompt(
        self,
        user_prompt: str,
        include_history: bool = True,
        include_important_context: bool = True
    ) -> str:
        if not self._initialized:
            raise RuntimeError("请先调用 init_long_text() 初始化文本")

        cached_prompt = self.cache_manager.prompt_cache.get_enhanced_prompt(
            user_prompt, self._source_text
        )
        if cached_prompt:
            return cached_prompt

        relevant_context = self.vector_store.retrieve_relevant_context(
            user_prompt,
            k=3
        )

        window_context, window_metadata = self.window_manager.get_context_for_query(
            user_prompt,
            max_tokens=self.config.prompt.max_context_length
        )

        anchor_prompt = self.anchor_manager.get_anchor_prompt()

        history_context = ""
        if include_history:
            history_context = self._format_history_context()

        important_context = ""
        if include_important_context:
            important_context = self.window_manager.get_important_context()

        final_prompt = self._build_final_prompt(
            user_prompt=user_prompt,
            relevant_context=relevant_context,
            window_context=window_context,
            anchor_prompt=anchor_prompt,
            history_context=history_context,
            important_context=important_context
        )

        self.cache_manager.prompt_cache.set_enhanced_prompt(
            user_prompt, self._source_text, final_prompt
        )

        return final_prompt

    def _format_history_context(self) -> str:
        recent_history = self.history_manager.get_recent_context(n=2)
        if not recent_history:
            return ""

        return f"\n\n【前情提要】\n{recent_history}"

    def _build_final_prompt(
        self,
        user_prompt: str,
        relevant_context: str,
        window_context: str,
        anchor_prompt: str,
        history_context: str,
        important_context: str
    ) -> str:
        context_parts = []

        if important_context:
            context_parts.append(important_context)

        if relevant_context:
            context_parts.append(relevant_context)

        if window_context:
            context_parts.append(f"\n\n【当前上下文窗口】\n{window_context}")

        combined_context = "\n".join(context_parts)

        template = self.config.prompt.template

        final_prompt = template.format(
            user_prompt=user_prompt,
            relevant_context=combined_context,
            anchor_prompt=anchor_prompt
        )

        if history_context:
            final_prompt = history_context + "\n\n" + final_prompt

        return final_prompt.strip()

    def check_consistency(
        self,
        generated_text: str,
        detailed: bool = False
    ) -> Dict[str, Any]:
        if detailed:
            report = self.consistency_checker.get_detailed_report(
                generated_text,
                self.anchor_manager.anchors
            )
            return report

        is_consistent, check_result = self.consistency_checker.check_consistency(
            generated_text, self.anchor_manager.anchors
        )
        return {
            "is_consistent": is_consistent,
            "message": check_result
        }

    def record_generation(
        self,
        user_prompt: str,
        enhanced_prompt: str,
        generated_text: str,
        consistency_check: Dict[str, Any] = None
    ):
        record = self.history_manager.add_record(
            user_prompt=user_prompt,
            enhanced_prompt=enhanced_prompt,
            generated_text=generated_text,
            consistency_check=consistency_check or {},
            anchors=self.anchor_manager.anchors
        )

        self.window_manager.add_content(generated_text)

        self._update_anchors_from_generation(generated_text)

        return record

    def _update_anchors_from_generation(self, generated_text: str):
        new_anchors = self.anchor_extractor.extract_anchors(generated_text)
        if new_anchors:
            updated = self.anchor_extractor.update_anchors_with_new_content(
                self.anchor_manager.anchors,
                generated_text
            )
            self.anchor_manager.set_anchors_manually(updated)

    def mark_important_segment(
        self,
        content: str,
        reason: str,
        importance: float = 2.0
    ):
        self.window_manager.mark_important_segment(content, reason, importance)

    def update_character_state(
        self,
        character_name: str,
        state_update: Dict[str, Any]
    ):
        self.history_manager.update_character_state(character_name, state_update)

    def add_plot_event(
        self,
        event: str,
        characters: List[str] = None,
        importance: int = 1
    ):
        self.history_manager.add_plot_event(event, characters, importance)

    def get_character_summary(self, character_name: str) -> str:
        return self.history_manager.get_character_summary(character_name)

    def get_plot_summary(self) -> str:
        return self.history_manager.get_plot_summary()

    def get_full_story(self) -> str:
        return self.history_manager.get_full_story()

    def check_repetition(self, new_text: str, threshold: float = 0.8) -> Dict[str, Any]:
        return self.history_manager.check_repetition(new_text, threshold)

    def get_statistics(self) -> Dict[str, Any]:
        return {
            'history': self.history_manager.get_statistics(),
            'window': self.window_manager.get_statistics(),
            'cache': self.cache_manager.get_all_statistics(),
            'anchors': list(self.anchor_manager.anchors.keys())
        }

    def export_story(self, output_path: str, format: str = 'txt'):
        self.history_manager.export_story(output_path, format)

    def save_session(self, filepath: str):
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        self.config.save_to_file(str(path.with_suffix('.config.json')))
        self.history_manager.save_to_file(Path(str(path.with_suffix('.history.json'))))
        self.cache_manager.save_all()

    def load_session(self, filepath: str):
        config_path = Path(filepath).with_suffix('.config.json')
        if config_path.exists():
            self.config = ContextConfig.load_from_file(str(config_path))

        history_path = Path(filepath).with_suffix('.history.json')
        if history_path.exists():
            self.history_manager.load_from_file(history_path)

    def reset(self):
        self.vector_store = VectorContextStore()
        self.anchor_manager = AnchorManager()
        self.consistency_checker = ConsistencyChecker(self.vector_store)
        self.history_manager = HistoryManager(
            max_history=self.config.history.max_history,
            auto_save=self.config.history.auto_save,
            save_path=self.config.history.save_path
        )
        self.window_manager = SlidingWindowManager(
            max_window_size=self.config.window.max_window_size,
            overlap_size=self.config.window.overlap_size,
            min_chunk_size=self.config.window.min_chunk_size
        )
        self.cache_manager.clear_all()
        self._initialized = False
        self._source_text = ""

    def update_config(self, **kwargs):
        self.config = self.config.update(**kwargs)

    def set_prompt_template(self, template: str):
        self.config.prompt.template = template
