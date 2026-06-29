import re, hashlib, json, time, os

class DataPipeline:
    """CNexus 2.0 纯净版 - 多格式记忆解析与特征序列化管线"""
    def __init__(self, config_path: str = None):
        self.noise_patterns = [r"\[分享图片\]", r"\[表情\]", r"http[s]?://\S+", r"分享链接：\S+"]
        self.intent_vector_space = {
            'store': ['记录', '积累', '存一下', '笔记', '保存', '收藏', '归档'],
            'recall': ['回忆', '想起来', '之前说过', '检索', '查一下', '翻出来'],
            'execute': ['去跑', '执行', '写代码', '测试', '干活', '开搞', '部署'],
            'converse': ['我觉得', '吐槽', '闲聊', '哈哈', '真有意思', '泡沫', '观点']
        }
        if config_path and os.path.exists(config_path):
            self.load_config(config_path)

    def load_config(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
            self.noise_patterns = cfg.get("noise_patterns", self.noise_patterns)
            self.intent_vector_space = cfg.get("intent_vector_space", self.intent_vector_space)

    def clean_text(self, raw_text: str) -> str:
        if not raw_text: return ""
        cleaned = raw_text.strip()
        for pattern in self.noise_patterns:
            cleaned = re.sub(pattern, "", cleaned)
        return re.sub(r"\s+", " ", cleaned).strip()

    def extract_intent_via_affinity(self, cleaned_text: str) -> str:
        text_lower = cleaned_text.lower()
        scores = {intent: 0 for intent in self.intent_vector_space.keys()}
        for intent, keywords in self.intent_vector_space.items():
            for kw in keywords:
                if kw in text_lower:
                    scores[intent] += 1.0
        max_score = -1.0
        best_intent = 'converse'
        for intent, score in scores.items():
            if score > max_score and score > 0:
                max_score = score
                best_intent = intent
        return best_intent

    def parse_file(self, file_path: str) -> list:
        _, ext = os.path.splitext(file_path.lower())
        if ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data if isinstance(data, list) else [data]
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
            return [{"text": p, "time": time.strftime("%Y-%m-%d %H:%M:%S")} for p in paragraphs]

    def process(self, source_data_path: str, boot_timestamp: float = None) -> list:
        if boot_timestamp is None: boot_timestamp = time.time()
        serialized_blocks = []
        raw_data = self.parse_file(source_data_path)

        for idx, item in enumerate(raw_data):
            raw_content = item.get("text", "")
            cleaned_content = self.clean_text(raw_content)
            if not cleaned_content: continue
            assigned_intent = self.extract_intent_via_affinity(cleaned_content)
            block_key = hashlib.md5(f"block:{idx}:{cleaned_content[:6]}".encode()).hexdigest()[:8]
            base_score = min(0.4 + (len(cleaned_content) * 0.003), 0.95)

            serialized_blocks.append({
                'block_id': block_key,
                'type': 'skill_memory_block',
                'skill': f"skill_{idx % 178}",
                'content': {
                    'skill': f"skill_{idx % 178}",
                    'status': 'distilled_personality_grain',
                    'intent': assigned_intent,
                    'output': cleaned_content
                },
                'weight': round(base_score * 0.5, 3),
                'decay_factor': 0.98
            })
        return serialized_blocks
