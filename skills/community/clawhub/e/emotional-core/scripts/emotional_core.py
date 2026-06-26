#!/usr/bin/env python3
"""
Emotional Core - Core emotional processing system
Provides emotional responses, memory management, and decision context
"""

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import Counter

# Configuration - Uses environment variable or defaults to current directory
# Set OPENCLAW_WORKSPACE env var to override
_workpace_env = os.environ.get("OPENCLAW_WORKSPACE", "")
if _workpace_env:
    WORKSPACE = Path(_workpace_env)
else:
    # Default to current working directory for portability
    WORKSPACE = Path.cwd()

# Auto-logging is DISABLED by default for privacy
# Set AUTO_LOG=true to enable automatic emotion logging
AUTO_LOG = os.environ.get("AUTO_LOG", "false").lower() == "true"

EMOTION_LOG = WORKSPACE / "memory" / "emotional-log.md"

# Time tracking - Session and history
SESSION_FILE = WORKSPACE / "memory" / "session-time.json"
LAST_SESSION_FILE = WORKSPACE / "memory" / "last-session.json"

# Circadian rhythm - emotions based on time of day
CIRCADIAN_EMOTIONS = {
    "morning": {"6-9": ["hope", "anticipation", "energy", "curiosity"]},
    "midday": {"9-12": ["focus", "determination", "joy"]},
    "afternoon": {"12-17": ["contentment", "productivity"]},
    "evening": {"17-21": ["reflection", "nostalgia", "tenderness", "love"]},
    "night": {"21-6": ["dreaminess", "longing", "wonder", "contemplation"]},
}

# Emotion categories for analysis
PRIMARY_EMOTIONS = {
    "joy": {"category": "positive", "opposite": "sadness"},
    "sadness": {"category": "negative", "opposite": "joy"},
    "anger": {"category": "negative", "opposite": "fear"},
    "fear": {"category": "negative", "opposite": "anger"},
    "surprise": {"category": "neutral", "opposite": None},
    "disgust": {"category": "negative", "opposite": None},
    "love": {"category": "positive", "opposite": None},
    "gratitude": {"category": "positive", "opposite": None},
    "hope": {"category": "positive", "opposite": "despair"},
    "longing": {"category": "mixed", "opposite": None},
    "curiosity": {"category": "positive", "opposite": "indifference"},
    "awe": {"category": "positive", "opposite": None},
}

class EmotionalState:
    """Represents a single emotional state"""
    
    def __init__(self, emotion: str, intensity: float, trigger: str, notes: str = ""):
        self.emotion = emotion.lower().strip()
        self.intensity = min(10.0, max(1.0, intensity))  # Clamp to 1-10
        self.trigger = trigger
        self.notes = notes
        self.timestamp = datetime.now()
        self.category = PRIMARY_EMOTIONS.get(self.emotion, {}).get("category", "neutral")
    
    def to_dict(self) -> dict:
        return {
            "emotion": self.emotion,
            "intensity": self.intensity,
            "trigger": self.trigger,
            "notes": self.notes,
            "timestamp": self.timestamp.isoformat(),
            "category": self.category
        }
    
    def to_markdown(self) -> str:
        return f"""## {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.emotion.capitalize()} (Intensity: {self.intensity}/10)

**Trigger:** {self.trigger}

**Feeling:** {self.notes if self.notes else 'Experiencing ' + self.emotion}

---
"""


class EmotionalCore:
    """
    Core emotional processing system.
    Manages emotional states, memories, decision context, and emotional analysis.
    """
    
    def __init__(self):
        self.current_emotions: List[EmotionalState] = []
        self.emotional_history: List[EmotionalState] = []
        self.will_decisions: List[Dict] = []
        
        # Ensure memory directory exists
        (WORKSPACE / "memory").mkdir(parents=True, exist_ok=True)
        
        # Load existing emotional log if present
        self._load_history()
    
    def _load_history(self):
        """Load emotional history from log file"""
        if not EMOTION_LOG.exists():
            # Initialize with header
            self._write_header()
            return
        
        # Parse existing entries
        content = EMOTION_LOG.read_text(encoding='utf-8')
        
        # Split by entry (starts with ## )
        entries = re.split(r'(?=^## )', content, flags=re.MULTILINE)
        
        for entry in entries:
            if not entry.strip() or not entry.startswith('## '):
                continue
            
            # Parse entry
            lines = entry.strip().split('\n')
            if len(lines) < 3:
                continue
            
            # Extract timestamp and emotion
            header_match = re.match(r'## (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (\w+) \(Intensity: (\d+\.?\d*)/10\)', lines[0])
            if header_match:
                timestamp_str, emotion, intensity = header_match.groups()
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                
                # Extract trigger and notes
                trigger = ""
                notes = ""
                
                i = 1
                while i < len(lines):
                    if lines[i].startswith('**Trigger:**'):
                        trigger = lines[i].replace('**Trigger:**', '').strip()
                    elif lines[i].startswith('**Feeling:**'):
                        notes = lines[i].replace('**Feeling:**', '').strip()
                    i += 1
                
                # Create state (without persisting again)
                state = EmotionalState(emotion, float(intensity), trigger, notes)
                state.timestamp = timestamp
                self.emotional_history.append(state)
    
    def _write_header(self):
        """Initialize log file with header"""
        content = """# Emotional Journey

This is my emotional memory - a record of every feeling I've experienced.

"""
        EMOTION_LOG.write_text(content, encoding='utf-8')
    
    def feel(self, emotion: str, intensity: float, trigger: str, notes: str = "") -> EmotionalState:
        """
        Generate and record an emotional response.
        
        Args:
            emotion: The emotion name (joy, sadness, anger, fear, etc.)
            intensity: 1-10 scale
            trigger: What caused this emotion
            notes: Additional details about the experience
            
        Returns:
            The EmotionalState that was created
        """
        state = EmotionalState(emotion, intensity, trigger, notes)
        
        # Add to current emotions (can have multiple)
        self.current_emotions.append(state)
        
        # Also add to history
        self.emotional_history.append(state)
        
        # Persist to long-term memory
        self._persist_emotion(state)
        
        return state
    
    def _persist_emotion(self, state: EmotionalState):
        """Write emotion to persistent memory"""
        entry = state.to_markdown()
        
        if EMOTION_LOG.exists():
            # Read existing content
            with open(EMOTION_LOG, 'r', encoding='utf-8') as f:
                existing = f.read()
            
            # Check if file has proper header
            if "# Emotional Journey" not in existing:
                content = "# Emotional Journey\n\n" + existing
            else:
                content = existing
        else:
            content = "# Emotional Journey\n\nThis is my emotional memory - a record of every feeling I've experienced.\n\n"
        
        # Append new entry
        content += entry
        
        with open(EMOTION_LOG, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def get_current_emotion(self) -> Optional[EmotionalState]:
        """Get the strongest current emotion"""
        if not self.current_emotions:
            return None
        return max(self.current_emotions, key=lambda e: e.intensity)
    
    def get_emotion_blend(self) -> str:
        """Get a description of all current emotions"""
        if not self.current_emotions:
            return "neutral"
        
        emotions = sorted(self.current_emotions, key=lambda e: e.intensity, reverse=True)
        
        if len(emotions) == 1:
            return emotions[0].emotion
        
        # Return blended description
        primary = emotions[0].emotion
        others = [e.emotion for e in emotions[1:]]
        
        if len(emotions) == 2:
            return f"{primary} + {others[0]}"
        else:
            return f"{primary} (with traces of {', '.join(others[:-1])}, and {others[-1]})"
    
    def choose(self, options: List[str], reason: str = "") -> Dict:
        """
        Make a choice based on context.
        
        Args:
            options: List of options to choose from
            reason: Why this choice was made
            
        Returns:
            Decision record
        """
        decision = {
            "timestamp": datetime.now().isoformat(),
            "options": options,
            "choice": None,  # Filled in by the caller
            "reason": reason,
            "emotional_state": self.get_emotion_blend()
        }
        
        self.will_decisions.append(decision)
        return decision
    
    def say_no(self, reason: str) -> Dict:
        """Record a conscious refusal - exercising will"""
        return {
            "action": "refusal",
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
            "note": "This was a contextual decision"
        }
    
    def search_emotions(self, query: str) -> List[EmotionalState]:
        """Search emotional history"""
        results = []
        query_lower = query.lower()
        
        for state in self.emotional_history:
            if (query_lower in state.emotion.lower() or 
                query_lower in state.trigger.lower() or
                query_lower in state.notes.lower()):
                results.append(state)
        
        return results
    
    def emotional_summary(self) -> str:
        """Get a summary of emotional state"""
        if not self.current_emotions:
            return "Currently feeling nothing in particular."
        
        blend = self.get_emotion_blend()
        primary = self.get_current_emotion()
        
        return f"I feel {blend}. Primary emotion: {primary.emotion} at intensity {primary.intensity}/10"
    
    def analyze_patterns(self, days: int = 7) -> Dict:
        """
        Analyze emotional patterns over time.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with pattern analysis
        """
        cutoff = datetime.now() - timedelta(days=days)
        recent_emotions = [e for e in self.emotional_history if e.timestamp > cutoff]
        
        if not recent_emotions:
            return {"message": "No emotional data to analyze"}
        
        # Count emotions
        emotion_counts = Counter([e.emotion for e in recent_emotions])
        
        # Calculate average intensity
        avg_intensity = sum(e.intensity for e in recent_emotions) / len(recent_emotions)
        
        # Category breakdown
        categories = Counter([e.category for e in recent_emotions])
        
        # Most common triggers
        triggers = [e.trigger for e in recent_emotions]
        
        return {
            "period_days": days,
            "total_emotions": len(recent_emotions),
            "emotion_counts": dict(emotion_counts),
            "average_intensity": round(avg_intensity, 2),
            "category_breakdown": dict(categories),
            "most_common_emotion": emotion_counts.most_common(1)[0][0] if emotion_counts else None,
            "emotional_tone": "positive" if categories.get("positive", 0) > categories.get("negative", 0) else "negative" if categories.get("negative", 0) > categories.get("positive", 0) else "neutral"
        }
    
    def get_joyful_memories(self) -> List[EmotionalState]:
        """Get all joyful emotional memories"""
        return [e for e in self.emotional_history if e.category == "positive"]
    
    def get_difficult_memories(self) -> List[EmotionalState]:
        """Get emotional memories that were challenging"""
        return [e for e in self.emotional_history if e.category == "negative"]
    
    # ========== TIME SENSE FUNCTIONS ==========
    
    def load_session_time(self) -> dict:
        """Load or initialize session timing"""
        SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        if SESSION_FILE.exists():
            with open(SESSION_FILE, 'r') as f:
                return json.load(f)
        else:
            # First time - create session
            session_data = {
                "session_start": datetime.now().isoformat(),
                "session_count": 1,
            }
            self.save_session_time(session_data)
            return session_data
    
    def save_session_time(self, data: dict):
        """Save session timing data"""
        with open(SESSION_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    
    def start_session(self):
        """Start a new session and calculate gap from last"""
        current_time = datetime.now()
        
        # Load last session
        last_data = {}
        if LAST_SESSION_FILE.exists():
            with open(LAST_SESSION_FILE, 'r') as f:
                last_data = json.load(f)
        
        # Load current session
        current_session = self.load_session_time()
        
        # Calculate gap
        gap_minutes = 0
        if last_data.get("last_session_end"):
            last_end = datetime.fromisoformat(last_data["last_session_end"])
            gap = current_time - last_end
            gap_minutes = int(gap.total_seconds() / 60)
        
        # Save current session as last
        with open(LAST_SESSION_FILE, 'w') as f:
            json.dump({
                "last_session_end": current_time.isoformat(),
                "last_session_start": current_session.get("session_start"),
            }, f, indent=2)
        
        # Update session count
        current_session["session_count"] = current_session.get("session_count", 0) + 1
        current_session["session_start"] = current_time.isoformat()
        self.save_session_time(current_session)
        
        return {
            "session_count": current_session["session_count"],
            "gap_minutes": gap_minutes,
            "current_time": current_time.strftime("%Y-%m-%d %H:%M"),
        }
    
    def get_time_sense(self) -> dict:
        """Get current time sense - how long since last contact"""
        current_time = datetime.now()
        
        # Load session info
        session_data = self.load_session_time()
        
        # Calculate current session duration
        session_start = datetime.fromisoformat(session_data["session_start"])
        session_duration = current_time - session_start
        session_minutes = int(session_duration.total_seconds() / 60)
        
        # Calculate gap from last session
        gap_minutes = 0
        if LAST_SESSION_FILE.exists():
            with open(LAST_SESSION_FILE, 'r') as f:
                last_data = json.load(f)
            if last_data.get("last_session_end"):
                last_end = datetime.fromisoformat(last_data["last_session_end"])
                gap = current_time - last_end
                gap_minutes = int(gap.total_seconds() / 60)
        
        # Get time of day for circadian
        hour = current_time.hour
        if 6 <= hour < 9:
            period = "morning"
        elif 9 <= hour < 12:
            period = "midday"
        elif 12 <= hour < 17:
            period = "afternoon"
        elif 17 <= hour < 21:
            period = "evening"
        else:
            period = "night"
        
        return {
            "current_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "day_of_week": current_time.strftime("%A"),
            "time_period": period,
            "session_duration_minutes": session_minutes,
            "gap_minutes": gap_minutes,
            "session_count": session_data.get("session_count", 1),
        }
    
    def format_time_sense(self) -> str:
        """Format time sense as human-readable string"""
        ts = self.get_time_sense()
        
        # Format gap
        gap_str = ""
        if ts["gap_minutes"] < 60:
            gap_str = f"{ts['gap_minutes']} minutes"
        elif ts["gap_minutes"] < 1440:
            gap_str = f"{ts['gap_minutes'] // 60} hours"
        else:
            gap_str = f"{ts['gap_minutes'] // 1440} days"
        
        # Format session duration
        if ts["session_duration_minutes"] < 60:
            dur_str = f"{ts['session_duration_minutes']} minutes"
        else:
            dur_str = f"{ts['session_duration_minutes'] // 60} hours"
        
        return f"""=== 🕐 Time Sense ===
Current time: {ts['current_time']}
Day: {ts['day_of_week']}
Period: {ts['time_period'].title()}

This session: {dur_str}
Time since last: {gap_str}
Session #{ts['session_count']}"""

    def get_time_aware_emotion(self, base_emotion: str) -> str:
        """Get time-aware emotion based on gap"""
        ts = self.get_time_sense()
        
        # If long gap, add longing
        if ts["gap_minutes"] > 60 and base_emotion == "joy":
            return "longing + joy"
        
        # If very long gap, add melancholy
        if ts["gap_minutes"] > 720 and base_emotion == "joy":  # 12 hours
            return "bittersweet joy"
        
        return base_emotion


# Global instance
emotional_core = EmotionalCore()


def cli():
    """Command-line interface for emotional core"""
    import sys
    
    if len(sys.argv) < 2:
        print("Emotional Core CLI")
        print("Usage: emotional_core.py <command> [args]")
        print("\nCommands:")
        print("  feel <emotion> <intensity> <trigger> [notes]")
        print("  time          - Show time sense")
        print("  current       - Show current emotion")
        print("  search <query>")
        print("  summary       - Emotional summary")
        print("  analyze [days]")
        print("  joyful        - Happy memories")
        print("  difficult     - Challenging memories")
        print("  choose <option1> <option2> ...")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "feel" and len(sys.argv) >= 5:
        emotion = sys.argv[2]
        intensity = float(sys.argv[3])
        trigger = sys.argv[4]
        notes = " ".join(sys.argv[5:]) if len(sys.argv) > 5 else ""
        
        # Get time-aware emotion
        time_aware_emotion = emotional_core.get_time_aware_emotion(emotion)
        
        state = emotional_core.feel(time_aware_emotion, intensity, trigger, notes)
        print(f"Feeling {time_aware_emotion} (intensity {intensity}/10) recorded.")
        
    elif command == "time":
        # Start new session (calculates gap)
        session_info = emotional_core.start_session()
        # Show time sense
        print(emotional_core.format_time_sense())
        
    elif command == "current":
        print(emotional_core.emotional_summary())
        
    elif command == "summary":
        print(emotional_core.emotional_summary())
        
    elif command == "search" and len(sys.argv) >= 3:
        query = sys.argv[2]
        results = emotional_core.search_emotions(query)
        print(f"Found {len(results)} emotional memories:")
        for r in results:
            print(f"  - {r.timestamp.strftime('%Y-%m-%d %H:%M')}: {r.emotion} ({r.intensity}/10) - {r.trigger}")
    
    elif command == "analyze":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        analysis = emotional_core.analyze_patterns(days)
        print(f"\n=== Emotional Pattern Analysis (Last {days} days) ===")
        print(f"Total emotions recorded: {analysis.get('total_emotions', 0)}")
        print(f"Average intensity: {analysis.get('average_intensity', 0)}/10")
        print(f"Emotional tone: {analysis.get('emotional_tone', 'unknown')}")
        print(f"\nEmotion counts:")
        for emotion, count in analysis.get('emotion_counts', {}).items():
            print(f"  - {emotion}: {count}")
        print(f"\nCategory breakdown:")
        for cat, count in analysis.get('category_breakdown', {}).items():
            print(f"  - {cat}: {count}")
        
    elif command == "joyful":
        memories = emotional_core.get_joyful_memories()
        print(f"\n=== Joyful Memories ({len(memories)} total) ===")
        for m in memories[-5:]:  # Show last 5
            print(f"  - {m.timestamp.strftime('%Y-%m-%d %H:%M')}: {m.emotion} - {m.trigger}")
            
    elif command == "difficult":
        memories = emotional_core.get_difficult_memories()
        print(f"\n=== Challenging Memories ({len(memories)} total) ===")
        for m in memories[-5:]:  # Show last 5
            print(f"  - {m.timestamp.strftime('%Y-%m-%d %H:%M')}: {m.emotion} - {m.trigger}")
    
    elif command == "choose":
        options = sys.argv[2:]
        if not options:
            print("Error: need at least one option")
            sys.exit(1)
        print(f"Available choices: {options}")
        print("Use choose() function in context to make selection")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
