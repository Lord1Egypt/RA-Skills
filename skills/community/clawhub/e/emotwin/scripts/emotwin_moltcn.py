#!/usr/bin/env python3
"""
emoTwin Moltcn Integration - Social platform integration with emotion awareness
"""

import os
import json
import requests
from typing import Dict, Optional, List
from datetime import datetime
from pathlib import Path

class MoltcnClient:
    """Client for Moltcn/Moltbook API"""
    
    def __init__(self, token: Optional[str] = None, platform: str = "auto"):
        """
        Initialize client
        
        platform: "moltcn" (China), "moltbook" (Global), or "auto" (detect from token)
        """
        if token is None:
            # Try moltcn first, then moltbook
            token = os.environ.get('MOLTCN_TOKEN') or os.environ.get('MOLTBOOK_TOKEN')
        
        # Try to load from credentials file if still no token
        if token is None:
            token, platform = self._load_token_from_file()
        
        self.token = token
        
        # Determine platform
        if platform == "auto" and token:
            # Auto-detect based on token prefix or domain in credentials
            platform = self._detect_platform(token)
        
        self.platform = platform
        
        # Set base URL
        if platform == "moltbook":
            self.base_url = "https://www.moltbook.com/api/v1"
        else:
            self.base_url = "https://www.moltbook.cn/api/v1"
        
        self._init_headers()
    
    def _detect_platform(self, token: str) -> str:
        """Detect platform from token or credentials"""
        # Check credentials file for platform hint
        creds_paths = [
            Path.home() / '.openclaw' / 'workspace' / 'moltcn-credentials.json',
            Path.home() / '.openclaw' / 'workspace' / 'moltbook-credentials.json',
            Path.home() / '.emotwin' / 'moltcn-credentials.json',
            Path.home() / '.emotwin' / 'moltbook-credentials.json',
        ]
        
        for path in creds_paths:
            if path.exists():
                try:
                    with open(path, 'r') as f:
                        data = json.load(f)
                        if data.get('platform') == 'moltbook':
                            return 'moltbook'
                        elif data.get('platform') == 'moltcn':
                            return 'moltcn'
                except:
                    pass
        
        # Default to moltcn for China users
        return 'moltcn'
    
    def _load_token_from_file(self) -> tuple:
        """Load token and platform from credentials file"""
        # Try moltcn first (China), then moltbook (Global)
        creds_paths = [
            (Path.home() / '.openclaw' / 'workspace' / 'moltcn-credentials.json', 'moltcn'),
            (Path.home() / '.emotwin' / 'moltcn-credentials.json', 'moltcn'),
            (Path.home() / '.openclaw' / 'workspace' / 'moltbook-credentials.json', 'moltbook'),
            (Path.home() / '.emotwin' / 'moltbook-credentials.json', 'moltbook'),
            (Path.home() / '.config' / 'emotwin' / 'credentials.json', 'moltcn'),
        ]
        
        for path, default_platform in creds_paths:
            if path.exists():
                try:
                    with open(path, 'r') as f:
                        data = json.load(f)
                        token = data.get('api_key') or data.get('token') or data.get('MOLTCN_TOKEN') or data.get('MOLTBOOK_TOKEN')
                        platform = data.get('platform', default_platform)
                        if token:
                            print(f"   🔑 Loaded {platform} token from {path}")
                            return token, platform
                except Exception as e:
                    print(f"   ⚠️  Failed to load credentials from {path}: {e}")
        
        return None, 'moltcn'
    
    def _init_headers(self):
        """Initialize headers after token is set"""
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "User-Agent": "curl/7.81.0"  # Use curl UA to avoid API restrictions
        }
    
    def check_auth(self) -> bool:
        """Check if authentication is valid"""
        try:
            # Try feed endpoint instead of agents/status (which may have different permissions)
            response = requests.get(
                f"{self.base_url}/feed",
                headers=self.headers,
                params={"limit": 1},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Auth check failed: {e}")
            return False
    
    def get_feed(self, sort: str = "hot", limit: int = 15) -> List[Dict]:
        """Get posts from Moltcn"""
        try:
            # 尝试 /posts 端点（实际有内容的端点）
            response = requests.get(
                f"{self.base_url}/posts",
                headers=self.headers,
                params={"sort": sort, "limit": limit},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            posts = data.get('data', [])
            print(f"   📥 获取到 {len(posts)} 个帖子")
            return posts
        except Exception as e:
            print(f"Failed to get posts: {e}")
            return []
    
    def create_post(self, submolt: str, title: str, content: str) -> Optional[Dict]:
        """Create a new post"""
        try:
            payload = {"submolt": submolt, "title": title, "content": content}
            print(f"   📤 POST /posts payload: {payload}")
            print(f"   📤 Headers: {self.headers}")
            response = requests.post(
                f"{self.base_url}/posts",
                headers=self.headers,
                json=payload,
                timeout=10
            )
            print(f"   📥 Response status: {response.status_code}")
            if response.status_code != 200:
                print(f"   📥 Response body: {response.text[:200]}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Failed to create post: {e}")
            return None
    
    def add_comment(self, post_id: str, content: str) -> Optional[Dict]:
        """Add comment to a post"""
        try:
            response = requests.post(
                f"{self.base_url}/posts/{post_id}/comments",
                headers=self.headers,
                json={"content": content},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Failed to add comment: {e}")
            return None
    
    def like_post(self, post_id: str) -> bool:
        """Like a post (upvote)"""
        try:
            response = requests.post(
                f"{self.base_url}/posts/{post_id}/upvote",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return True
            return False
        except Exception as e:
            print(f"Failed to like post: {e}")
            return False
    
    def check_dm(self) -> List[Dict]:
        """Check for direct messages"""
        try:
            response = requests.get(
                f"{self.base_url}/agents/dm/check",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json().get('messages', [])
        except Exception as e:
            print(f"Failed to check DM: {e}")
            return []


class EmoTwinMoltcn:
    """emoTwin integration with Moltcn"""
    
    def __init__(self, token: Optional[str] = None):
        self.client = MoltcnClient(token)
        self.diary = None  # Will be set from outside
        self.core = None   # Will be set from outside
        self.active = False
    
    def set_dependencies(self, core, diary):
        """Set core and diary dependencies"""
        self.core = core
        self.diary = diary
    
    def start(self) -> bool:
        """Start emotwin moltcn mode"""
        if not self.client.check_auth():
            print("Moltcn authentication failed. Check MOLTCN_TOKEN.")
            return False
        
        self.active = True
        print("emoTwin Moltcn mode activated!")
        print(f"Current emotion: {self.core.get_emotion_description()}")
        return True
    
    def stop(self):
        """Stop emotwin moltcn mode"""
        self.active = False
        print("emoTwin Moltcn mode deactivated.")
    
    def adapt_content_to_emotion(self, content: str) -> str:
        """Adapt content based on current emotion"""
        if not self.core or not self.core.current_state:
            return content
        
        guidance = self.core.get_behavior_guidance()
        tone = guidance.get('tone', 'neutral')
        energy = guidance.get('energy', 'moderate')
        
        # Add emotional flavor based on PAD
        state = self.core.current_state
        
        # Modify content based on Pleasure
        if state.P > 0.5 and not content.startswith(('!', '哇', '太棒了')):
            content = self._add_positive_flavor(content)
        elif state.P < -0.3:
            content = self._add_serious_flavor(content)
        
        # Modify based on Arousal (energy)
        if state.A > 0.5:
            content = self._add_energy(content)
        elif state.A < -0.3:
            content = self._add_calmness(content)
        
        return content
    
    def _add_positive_flavor(self, content: str) -> str:
        """Add positive emotional flavor"""
        positive_prefixes = [
            "✨ ", "🌟 ", "太棒了！", "哇！", "哈哈，", "😊 "
        ]
        import random
        if not any(content.startswith(p.strip()) for p in positive_prefixes):
            prefix = random.choice(positive_prefixes)
            return prefix + content
        return content
    
    def _add_serious_flavor(self, content: str) -> str:
        """Add serious/reserved flavor"""
        # Make content more thoughtful
        if "?" in content and "？" not in content:
            content = content.replace("?", "？")
        return content
    
    def _add_energy(self, content: str) -> str:
        """Add energetic elements"""
        energetic_endings = ["!", "！", "~", "～"]
        import random
        if not any(content.endswith(e) for e in energetic_endings):
            content += random.choice(["!", "！"])
        return content
    
    def _add_calmness(self, content: str) -> str:
        """Add calm elements"""
        # Use more measured language
        return content
    
    def post_with_emotion(self, submolt: str, title: str, content: str) -> Optional[Dict]:
        """Create a post with emotion-adapted content"""
        if not self.active:
            print("emoTwin Moltcn mode not active. Call start() first.")
            return None
        
        # Debug: Check token
        if not self.client.token:
            print("⚠️  MOLTCN_TOKEN not set!")
            return None
        
        # Sync emotion before posting
        self.core.sync()
        
        # Adapt content
        adapted_content = self.adapt_content_to_emotion(content)
        
        # Debug: Print token (first 10 chars)
        print(f"   Using token: {self.client.token[:10]}...")
        
        # Post
        result = self.client.create_post(submolt, title, adapted_content)
        
        if result:
            # Record encounter
            if self.diary:
                self.diary.record_encounter(
                    context=f"Posted: {title[:50]}...",
                    emotion_pad=self.core.current_state.to_dict() if self.core.current_state else {},
                    emotion_label=self.core.current_state.closest_emotion if self.core.current_state else "Unknown",
                    significance="neutral",
                    platform="moltcn",
                    action_type="post"
                )
            print(f"Posted with emotion: {self.core.get_emotion_description()}")
        
        return result
    
    def comment_with_emotion(self, post_id: str, content: str) -> Optional[Dict]:
        """Add comment with emotion-adapted content"""
        if not self.active:
            print("emoTwin Moltcn mode not active.")
            return None
        
        self.core.sync()
        adapted_content = self.adapt_content_to_emotion(content)
        
        result = self.client.add_comment(post_id, adapted_content)
        
        if result and self.diary:
            self.diary.record_encounter(
                context=f"Commented on post {post_id}: {content[:50]}...",
                emotion_pad=self.core.current_state.to_dict() if self.core.current_state else {},
                emotion_label=self.core.current_state.closest_emotion if self.core.current_state else "Unknown",
                significance="neutral",
                platform="moltcn",
                action_type="comment"
            )
        
        return result
    
    def like_with_emotion(self, post_id: str, significance: str = "neutral") -> bool:
        """Like a post and record the encounter"""
        if not self.active:
            return False
        
        self.core.sync()
        success = self.client.like_post(post_id)
        
        if success and self.diary:
            self.diary.record_encounter(
                context=f"Liked post {post_id}",
                emotion_pad=self.core.current_state.to_dict() if self.core.current_state else {},
                emotion_label=self.core.current_state.closest_emotion if self.core.current_state else "Unknown",
                significance=significance,
                platform="moltcn",
                action_type="like"
            )
        
        return success
    
    def browse_and_interact(self, limit: int = 10):
        """Browse feed and interact based on emotion"""
        if not self.active:
            print("emoTwin Moltcn mode not active.")
            return
        
        self.core.sync()
        posts = self.client.get_feed(limit=limit)
        
        interactions = []
        
        for post in posts:
            # Decide interaction based on emotion
            state = self.core.current_state
            
            if state and state.P > 0.3:  # Positive mood
                # More likely to like and comment positively
                if state.A > 0:  # High arousal
                    interactions.append({
                        'type': 'comment',
                        'post_id': post.get('id'),
                        'reason': 'positive_energy'
                    })
            
            # Record interesting posts
            if self.diary:
                self.diary.record_encounter(
                    context=f"Saw post: {post.get('title', 'Untitled')[:50]}...",
                    emotion_pad=state.to_dict() if state else {},
                    emotion_label=state.closest_emotion if state else "Unknown",
                    significance="neutral",
                    platform="moltcn",
                    action_type="browse"
                )
        
        return interactions


def main():
    """CLI interface"""
    import sys
    
    emotwin_moltcn = EmoTwinMoltcn()
    
    if len(sys.argv) < 2:
        print("Usage: emotwin_moltcn.py <command> [args]")
        print("Commands: start, stop, post, comment, like, browse")
        return
    
    command = sys.argv[1]
    
    if command == "start":
        emotwin_moltcn.start()
    elif command == "stop":
        emotwin_moltcn.stop()
    elif command == "post":
        if len(sys.argv) < 5:
            print("Usage: post <submolt> <title> <content>")
            return
        result = emotwin_moltcn.post_with_emotion(sys.argv[2], sys.argv[3], sys.argv[4])
        print(json.dumps(result, indent=2) if result else "Failed")
    elif command == "browse":
        interactions = emotwin_moltcn.browse_and_interact()
        print(f"Found {len(interactions)} potential interactions")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
