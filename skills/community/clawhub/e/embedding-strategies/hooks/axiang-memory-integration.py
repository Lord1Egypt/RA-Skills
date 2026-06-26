#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Axiang (阿香) Integration with Memory Search
Enhances responses with retrieved memories
"""

import sys
import os

# Add hooks directory to path
hooks_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, hooks_dir)

from memory_retriever import enhance_prompt, retrieve_context

class AxiangMemoryEnhancer:
    """Enhance Axiang's responses with memory context"""
    
    def __init__(self):
        self.enabled = True
        self.debug = False
    
    def before_respond(self, user_message: str, history: list = None) -> dict:
        """
        Called before Axiang generates a response
        
        Args:
            user_message: User's current message
            history: Conversation history
        
        Returns:
            Enhanced context dict
        """
        if not self.enabled:
            return {"message": user_message, "memories": None}
        
        # Retrieve relevant memories
        memory_context = retrieve_context(user_message, k=3)
        
        if self.debug:
            print(f"[DEBUG] Retrieved memories for: '{user_message}'")
            if memory_context:
                print(f"[DEBUG] Found relevant memories")
            else:
                print(f"[DEBUG] No relevant memories")
        
        return {
            "message": user_message,
            "memories": memory_context,
            "enhanced_prompt": enhance_prompt(user_message, history) if memory_context else user_message
        }
    
    def after_respond(self, response: str, memories: str = None) -> str:
        """
        Called after Axiang generates a response
        
        Args:
            response: LLM's generated response
            memories: Retrieved memory context (if any)
        
        Returns:
            Potentially enhanced response
        """
        # For now, just return the response as-is
        # Future: Add memory citations, confidence scores, etc.
        return response
    
    def format_memory_summary(self, memories: str) -> str:
        """
        Format retrieved memories as a summary for the user
        
        Args:
            memories: Raw memory context
        
        Returns:
            User-friendly summary
        """
        if not memories:
            return ""
        
        # Extract key info
        lines = memories.strip().split('\n')
        sources = []
        
        for line in lines:
            if line.startswith('[Memory'):
                # Extract source
                parts = line.split('from ')
                if len(parts) > 1:
                    source = parts[1].replace(']', '').strip()
                    sources.append(source)
        
        if sources:
            return f"📚 找到 {len(sources)} 条相关记忆：{', '.join(sources)}"
        else:
            return ""


# Singleton instance
_enhancer = None

def get_enhancer() -> AxiangMemoryEnhancer:
    """Get or create singleton enhancer"""
    global _enhancer
    if _enhancer is None:
        _enhancer = AxiangMemoryEnhancer()
    return _enhancer


# Convenience functions
def enhance_before_respond(user_message: str, history: list = None) -> dict:
    """Enhance user message before LLM processing"""
    enhancer = get_enhancer()
    return enhancer.before_respond(user_message, history)

def enhance_after_respond(response: str, memories: str = None) -> str:
    """Enhance LLM response before sending to user"""
    enhancer = get_enhancer()
    return enhancer.after_respond(response, memories)


# Test interface
if __name__ == "__main__":
    print("=" * 60)
    print("Axiang Memory Integration Test")
    print("=" * 60)
    
    enhancer = AxiangMemoryEnhancer(debug=True)
    
    test_messages = [
        "我之前说过瀑布的事情吗？",
        "TTS 应该怎么用？",
        "阿里云 Embedding 配置好了吗？",
        "今天天气怎么样？"  # Should not find relevant memories
    ]
    
    for msg in test_messages:
        print(f"\n{'='*60}")
        print(f"User: {msg}")
        print(f"{'='*60}")
        
        result = enhancer.before_respond(msg)
        
        if result['memories']:
            print(f"[Memories Found]")
            print(result['memories'][:500])
            
            summary = enhancer.format_memory_summary(result['memories'])
            print(f"\n{summary}")
        else:
            print("[No relevant memories]")
        
        print(f"\nEnhanced prompt: {result['enhanced_prompt'][:200]}...")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
