import json
import os

class TelegramParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.messages = []
        
    def parse(self) -> list:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Telegram export file not found: {self.file_path}")
            
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if 'messages' not in data:
            raise ValueError("Invalid Telegram export: 'messages' array not found.")
            
        parsed = []
        for msg in data['messages']:
            if msg.get('type') != 'message':
                continue
                
            raw_text = msg.get('text', '')
            if isinstance(raw_text, list):
                text = "".join(part['text'] if isinstance(part, dict) else part for part in raw_text)
            else:
                text = str(raw_text)
                
            if text.strip():
                parsed.append({
                    'id': msg.get('id'),
                    'date': msg.get('date'),
                    'sender': msg.get('from'),
                    'text': text
                })
                
        self.messages = parsed
        return parsed
