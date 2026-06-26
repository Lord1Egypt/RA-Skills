import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from pathlib import Path


@dataclass
class GenerationRecord:
    turn_id: int
    timestamp: str
    user_prompt: str
    enhanced_prompt: str
    generated_text: str
    consistency_check: Dict[str, Any]
    anchors_snapshot: Dict[str, str]
    token_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class HistoryManager:
    def __init__(self, max_history: int = 100, auto_save: bool = False, save_path: str = None):
        self.max_history = max_history
        self.auto_save = auto_save
        self.save_path = Path(save_path) if save_path else None
        self.history: List[GenerationRecord] = []
        self.turn_counter = 0
        self.character_state: Dict[str, Dict[str, Any]] = {}
        self.plot_timeline: List[Dict[str, Any]] = []

    def add_record(
        self,
        user_prompt: str,
        enhanced_prompt: str,
        generated_text: str,
        consistency_check: Dict[str, Any],
        anchors: Dict[str, str],
        metadata: Dict[str, Any] = None
    ) -> GenerationRecord:
        self.turn_counter += 1

        record = GenerationRecord(
            turn_id=self.turn_counter,
            timestamp=datetime.now().isoformat(),
            user_prompt=user_prompt,
            enhanced_prompt=enhanced_prompt,
            generated_text=generated_text,
            consistency_check=consistency_check,
            anchors_snapshot=anchors.copy(),
            token_count=self._estimate_tokens(generated_text),
            metadata=metadata or {}
        )

        self.history.append(record)

        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

        if self.auto_save and self.save_path:
            self.save_to_file(self.save_path)

        return record

    def _estimate_tokens(self, text: str) -> int:
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        other_chars = len(text) - chinese_chars
        return chinese_chars + other_chars // 4

    def get_recent_context(self, n: int = 3) -> str:
        if not self.history:
            return ""

        recent_records = self.history[-n:]
        context_parts = []

        for record in recent_records:
            context_parts.append(f"[第{record.turn_id}轮]")
            context_parts.append(f"用户需求：{record.user_prompt[:100]}...")
            context_parts.append(f"生成内容：{record.generated_text[:200]}...")
            context_parts.append("")

        return "\n".join(context_parts)

    def get_full_story(self) -> str:
        return "\n\n".join([
            record.generated_text
            for record in self.history
        ])

    def update_character_state(self, character_name: str, state_update: Dict[str, Any]):
        if character_name not in self.character_state:
            self.character_state[character_name] = {
                'first_appearance': datetime.now().isoformat(),
                'mentions': 0,
                'attributes': {},
                'history': []
            }

        self.character_state[character_name]['mentions'] += 1
        self.character_state[character_name]['last_updated'] = datetime.now().isoformat()

        for key, value in state_update.items():
            if key == 'history':
                self.character_state[character_name]['history'].append(value)
            else:
                self.character_state[character_name]['attributes'][key] = value

    def add_plot_event(self, event: str, characters: List[str] = None, importance: int = 1):
        self.plot_timeline.append({
            'turn_id': self.turn_counter,
            'event': event,
            'characters': characters or [],
            'importance': importance,
            'timestamp': datetime.now().isoformat()
        })

    def get_character_summary(self, character_name: str) -> str:
        if character_name not in self.character_state:
            return f"角色 '{character_name}' 尚未出现"

        state = self.character_state[character_name]
        summary_parts = [f"角色：{character_name}"]
        summary_parts.append(f"出现次数：{state['mentions']}")

        if state['attributes']:
            attrs = '；'.join([f"{k}：{v}" for k, v in state['attributes'].items()])
            summary_parts.append(f"属性：{attrs}")

        return '\n'.join(summary_parts)

    def get_plot_summary(self) -> str:
        if not self.plot_timeline:
            return "暂无剧情记录"

        important_events = [
            event for event in self.plot_timeline
            if event['importance'] >= 2
        ]

        if not important_events:
            important_events = self.plot_timeline[-5:]

        return ' → '.join([e['event'] for e in important_events])

    def check_repetition(self, new_text: str, threshold: float = 0.8) -> Dict[str, Any]:
        if not self.history:
            return {'is_repetitive': False, 'similar_records': []}

        new_hash = self._get_text_hash(new_text)
        similar_records = []

        for record in self.history:
            similarity = self._calculate_similarity(new_text, record.generated_text)
            if similarity > threshold:
                similar_records.append({
                    'turn_id': record.turn_id,
                    'similarity': similarity,
                    'original_text': record.generated_text[:100]
                })

        return {
            'is_repetitive': len(similar_records) > 0,
            'similar_records': similar_records
        }

    def _get_text_hash(self, text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        words1 = set(text1)
        words2 = set(text2)

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union)

    def save_to_file(self, filepath: Path = None):
        filepath = filepath or self.save_path
        if not filepath:
            return

        data = {
            'history': [asdict(record) for record in self.history],
            'character_state': self.character_state,
            'plot_timeline': self.plot_timeline,
            'turn_counter': self.turn_counter
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_file(self, filepath: Path):
        if not filepath.exists():
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.history = [
            GenerationRecord(**record) for record in data.get('history', [])
        ]
        self.character_state = data.get('character_state', {})
        self.plot_timeline = data.get('plot_timeline', [])
        self.turn_counter = data.get('turn_counter', 0)

    def get_statistics(self) -> Dict[str, Any]:
        if not self.history:
            return {'total_turns': 0}

        total_tokens = sum(r.token_count for r in self.history)
        consistency_rate = sum(
            1 for r in self.history if r.consistency_check.get('is_consistent', False)
        ) / len(self.history)

        return {
            'total_turns': len(self.history),
            'total_tokens': total_tokens,
            'consistency_rate': f"{consistency_rate:.1%}",
            'unique_characters': len(self.character_state),
            'plot_events': len(self.plot_timeline)
        }

    def export_story(self, output_path: str, format: str = 'txt'):
        full_story = self.get_full_story()

        if format == 'txt':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_story)
        elif format == 'json':
            data = {
                'story': full_story,
                'chapters': [
                    {
                        'chapter': i + 1,
                        'content': record.generated_text,
                        'prompt': record.user_prompt
                    }
                    for i, record in enumerate(self.history)
                ]
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
