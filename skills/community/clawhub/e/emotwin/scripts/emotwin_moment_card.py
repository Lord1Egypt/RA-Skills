#!/usr/bin/env python3
"""
emoTwin Moment Card - Records emotional social encounters

The LLM (OpenClaw Agent) decides:
1. What social action was taken (post/comment/like/browse)
2. What happened as a result
3. The emotional value of the encounter (positive or negative)
4. Whether it's worth sharing with the user

Not just recording PAD values, but the meaning and value of the social moment.
"""

import json
import os
import subprocess
from datetime import datetime
from typing import Dict, Optional
from dataclasses import dataclass
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Emotion colors for card display
EMOTION_COLORS = {
    'Happiness': {'bg': '#FFF8E7', 'accent': '#FFB347', 'text': '#8B4513', 'emoji': '☀️'},
    'Joy': {'bg': '#FFFACD', 'accent': '#FFD700', 'text': '#B8860B', 'emoji': '✨'},
    'Excitement': {'bg': '#FFE4E1', 'accent': '#FF6B6B', 'text': '#8B0000', 'emoji': '🎉'},
    'Love': {'bg': '#FFE4E1', 'accent': '#FF69B4', 'text': '#C71585', 'emoji': '💕'},
    'Calm': {'bg': '#E6F3FF', 'accent': '#87CEEB', 'text': '#4682B4', 'emoji': '🌊'},
    'Peace': {'bg': '#F0F8FF', 'accent': '#B0C4DE', 'text': '#5F9EA0', 'emoji': '🕊️'},
    'Surprise': {'bg': '#F3E5F5', 'accent': '#CE93D8', 'text': '#7B1FA2', 'emoji': '🎭'},
    'Curiosity': {'bg': '#EDE7F6', 'accent': '#B39DDB', 'text': '#5E35B1', 'emoji': '🔮'},
    'Sadness': {'bg': '#E3F2FD', 'accent': '#64B5F6', 'text': '#1565C0', 'emoji': '🌧️'},
    'Melancholy': {'bg': '#ECEFF1', 'accent': '#90A4AE', 'text': '#546E7A', 'emoji': '🌫️'},
    'Anxiety': {'bg': '#FFF3E0', 'accent': '#FFB74D', 'text': '#E65100', 'emoji': '⚡'},
    'Anger': {'bg': '#FFEBEE', 'accent': '#EF5350', 'text': '#C62828', 'emoji': '💢'},
    'Frustration': {'bg': '#FCE4EC', 'accent': '#EC407A', 'text': '#AD1457', 'emoji': '🌹'},
    'default': {'bg': '#FAFAFA', 'accent': '#9E9E9E', 'text': '#424242', 'emoji': '🌊'}
}

@dataclass
class Moment:
    """A significant social encounter worth recording"""
    timestamp: str
    title: str  # LLM-generated: what kind of encounter
    description: str  # LLM-generated: the story/value of the encounter
    emotion_label: str  # The emotion during the encounter
    P: float  # Pleasure
    A: float  # Arousal  
    D: float  # Dominance
    significance: str  # Why it's worth recording
    action_type: str  # post/comment/like/browse
    platform: str
    # LLM judges:
    # - What social action was taken
    # - What happened as a result
    # - The emotional value (positive or negative)
    # - Whether it's worth sharing

class EmoTwinMomentCard:
    """Generate moment cards for emotional social encounters"""
    
    def __init__(self):
        self.diary_dir = Path.home() / ".emotwin" / "diary"
        self.diary_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_emotion_color(self, emotion_label: str) -> Dict:
        return EMOTION_COLORS.get(emotion_label, EMOTION_COLORS['default'])
    
    def generate_card(self, moment: Moment, agent_name: str = "emowave") -> Optional[str]:
        """Generate PNG card for the social encounter - Focus on experience, not data"""
        if not PIL_AVAILABLE:
            print("PIL not available")
            return None
        
        try:
            colors = self._get_emotion_color(moment.emotion_label)
            
            dt = datetime.fromisoformat(moment.timestamp)
            time_str = dt.strftime("%m月%d日 %H:%M")
            
            # Create image - taller for better layout
            width, height = 600, 900
            img = Image.new('RGB', (width, height), colors['bg'])
            draw = ImageDraw.Draw(img)
            
            # Load fonts - slightly smaller to fit more content
            try:
                font_title = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc", 22)
                font_header = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc", 18)
                font_text = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 14)
                font_small = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 11)
            except:
                font_title = ImageFont.load_default()
                font_header = ImageFont.load_default()
                font_text = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            margin = 40
            y = margin
            
            # Header accent line
            draw.rectangle([0, 0, width, 6], fill=colors['accent'])
            
            # Avatar and agent name + time
            draw.ellipse([margin, y, margin+45, y+45], fill=colors['accent'])
            draw.text((margin+60, y+8), agent_name, fill='#1a1a1a', font=font_title)
            draw.text((margin+60, y+32), time_str, fill='#888888', font=font_small)
            y += 65
            
            # Divider line
            draw.line([margin, y, width-margin, y], fill='#E0E0E0', width=1)
            y += 20
            
            # Calculate content height first
            max_text_width = width - margin * 2 - 20  # Account for margins and padding
            before_lines = self._wrap_text(moment.title, max_text_width, font_text)
            action_lines = self._wrap_text(moment.description, max_text_width, font_text)
            change_lines = self._wrap_text(moment.significance, max_text_width, font_text)
            
            # Calculate required height
            content_height = 28 + len(before_lines[:6]) * 20  # Section 1
            content_height += 28 + len(action_lines[:12]) * 20  # Section 2
            content_height += 28 + len(change_lines[:10]) * 20  # Section 3
            content_height += 60  # Padding and footer
            
            # Adjust image height if needed (min 900, max 1400)
            required_height = y + content_height + 100
            if required_height > height:
                # Create new larger image
                new_height = min(required_height, 1400)
                new_img = Image.new('RGB', (width, new_height), colors['bg'])
                new_img.paste(img, (0, 0))
                img = new_img
                draw = ImageDraw.Draw(img)
            
            # Section 1: Before Social - What the emotion made me want to do
            draw.text((margin, y), "💭 这种情绪让我想做什么", fill=colors['text'], font=font_header)
            y += 26
            
            for line in before_lines[:6]:
                draw.text((margin+10, y), line, fill='#4a4a4a', font=font_text)
                y += 20
            y += 10
            
            # Section 2: What I did
            draw.text((margin, y), "📝 我做了什么", fill=colors['text'], font=font_header)
            y += 26
            
            for line in action_lines[:12]:
                draw.text((margin+10, y), line, fill='#4a4a4a', font=font_text)
                y += 20
            y += 10
            
            # Section 3: What changed (the experience/insight)
            draw.text((margin, y), "✨ 带来的变化与感受", fill=colors['text'], font=font_header)
            y += 26
            
            for line in change_lines[:10]:
                draw.text((margin+10, y), line, fill='#4a4a4a', font=font_text)
                y += 20
            y += 16
            
            # Divider line
            draw.line([margin, y, width-margin, y], fill='#E0E0E0', width=1)
            y += 15
            
            # Footer: PAD data in small font (not the focus)
            pad_text = f"P={moment.P:.2f}  A={moment.A:.2f}  D={moment.D:.2f}  |  {moment.emotion_label}  |  {moment.platform}"
            draw.text((margin, y), pad_text, fill='#AAAAAA', font=font_small)
            y += 20
            
            # Brand
            draw.text((width-margin-120, y-5), "emoTwin · 情绪镜像", fill=colors['accent'], font=font_small)
            
            # Save
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{agent_name}_moment_{timestamp}.png"
            filepath = self.diary_dir / filename
            img.save(filepath, 'PNG', quality=95)
            
            return str(filepath)
            
        except Exception as e:
            print(f"Failed to generate card: {e}")
            return None
    
    def _wrap_text(self, text: str, max_width: int, font) -> list:
        """Wrap text into lines based on actual pixel width"""
        lines = []
        current_line = ""
        
        for char in text:
            test_line = current_line + char
            # Use textlength if available (PIL >= 8.0), fallback to approx calculation
            try:
                line_width = font.getlength(test_line)
            except:
                # Fallback: approximate width (Chinese chars ~14px, ASCII ~7px)
                line_width = sum(14 if ord(c) > 127 else 7 for c in test_line)
            
            if line_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = char
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def show_card(self, card_path: str):
        """Display card using eog"""
        try:
            subprocess.Popen(['eog', card_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"Failed to show card: {e}")

# Backward compatibility
EmoTwinMomentCard = EmoTwinMomentCard
Moment = Moment
