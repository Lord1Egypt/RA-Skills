#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Memory Integration Module

Integrates LanceDB memory system with OpenClaw agent.
"""

import os
import sys
from datetime import datetime

# Add path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lancedb_memory import LanceDBMemory


class OpenClawMemoryIntegration:
    """OpenClaw Memory Integration"""
    
    def __init__(self, user_id: str = "default"):
        """
        Initialize memory integration
        
        Args:
            user_id: User ID
        """
        self.user_id = user_id
        
        # Database path
        self.db_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "memory_lancedb"
        )
        
        # Initialize LanceDB memory manager
        self.memory = LanceDBMemory(
            db_path=self.db_path,
            embedding_model="embedding-3"
        )
    
    def get_session_system_prompt(self, base_prompt: str = "") -> str:
        """
        Generate session system prompt with memory
        
        Args:
            base_prompt: Base system prompt
            
        Returns:
            Full system prompt with memory
        """
        # Search recent memories
        recent_memories = self.memory.search_memories(
            query="recent work and projects",
            user_id=self.user_id,
            k=5
        )
        
        formatted_recent = self.memory.format_memories_for_prompt(recent_memories)
        
        # Build full prompt
        full_prompt = base_prompt
        
        if formatted_recent:
            full_prompt += "\n\n" + "="*60 + "\n"
            full_prompt += "【User Memory】\n\n"
            full_prompt += formatted_recent
            full_prompt += "\n" + "="*60
        
        return full_prompt
    
    def search_memory(self, query: str, k: int = 5):
        """Search memories"""
        return self.memory.search_memories(query, self.user_id, k=k)
    
    def add_memory(self, content: str, type: str = "general", **kwargs):
        """Add memory"""
        return self.memory.add_memory(content, self.user_id, type=type, **kwargs)
    
    def get_user_profile(self):
        """Get user profile"""
        return self.memory.get_user_profile(self.user_id)
    
    def cleanup_expired(self):
        """Cleanup expired memories"""
        return self.memory.cleanup_expired()


# Convenience functions
def init_memory(user_id: str = "default") -> OpenClawMemoryIntegration:
    """Initialize memory system"""
    return OpenClawMemoryIntegration(user_id)


def build_system_prompt(base_prompt: str, memory_integration: OpenClawMemoryIntegration) -> str:
    """Build system prompt with memory"""
    return memory_integration.get_session_system_prompt(base_prompt)
