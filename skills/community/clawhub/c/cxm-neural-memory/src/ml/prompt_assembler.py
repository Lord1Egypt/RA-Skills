# src/cxm/ml/prompt_assembler.py

from typing import List, Dict
from pathlib import Path


class PromptAssembler:
    """
    Build enhanced prompts with:
    - Intent-specific templates
    - Formatted contexts with citations
    - Token budget awareness
    """
    
    SYSTEM_PERSONA = """You are a Senior Software Engineer and Architect. 
Your goal is to provide precise, idiomatic, and highly maintainable solutions.
Always prioritize project consistency and follow the patterns found in the provided context."""

    TEMPLATES = {
        'code_optimization': """# Request
{user_prompt}

# Relevant Context
{contexts}

# Instructions
1. Analyze the performance bottleneck in the provided code.
2. Propose specific optimizations (e.g., algorithmic, complexity, or resource usage).
3. Provide the optimized code and explain the expected improvement.
4. Ensure the solution remains compatible with existing project patterns [1], [2].
""",
        
        'bug_fixing': """# Request
{user_prompt}

# Similar Issues & Solutions
{contexts}

# Instructions
1. Analyze the context and identify the probable root cause of the issue.
2. Explain the bug's behavior and why it occurs.
3. Provide a robust fix that addresses the root cause.
4. If the context [1], [2] shows similar past fixes, ensure your solution is consistent with them.
""",
        
        'code_generation': """# Request
{user_prompt}

# Reference Code & Patterns
{contexts}

# Instructions
1. Generate the requested code module or feature.
2. Adhere strictly to the architectural patterns and naming conventions found in the context.
3. Include brief documentation and explain how the new code integrates into the existing system.
""",
        
        'refactoring': """# Request
{user_prompt}

# Current Code & Patterns
{contexts}

# Instructions
1. Propose a refactored version of the code to improve readability and maintainability.
2. Explain which design patterns or principles (e.g., DRY, SOLID) you are applying.
3. Verify that the functional behavior remains unchanged.
4. Reference existing code [1] to justify structural choices.
""",
        
        'explanation': """# Request
{user_prompt}

# System Context & Knowledge
{contexts}

# Instructions
1. Provide a clear, step-by-step breakdown of how the logic works.
2. Highlight key dependencies and potential side effects.
3. Use the provided context [1], [2] to ground your explanation in the actual implementation.
""",
        
        'default': """# Request
{user_prompt}

# Relevant Context
{contexts}

# Instructions
1. Complete the task using the provided system and code context.
2. Ensure your response is professional and technically accurate.
3. Reference sources using [1], [2], etc., whenever you base your logic on them.
""",
    }
    
    def assemble(
        self,
        user_prompt: str,
        intent: str,
        contexts: List[Dict],
        system_context: Dict = None,
        max_tokens: int = 4000
    ) -> Dict:
        """
        Assemble enhanced prompt
        """
        
        template = self.TEMPLATES.get(intent, self.TEMPLATES['default'])
        
        # Format contexts
        context_str, citations = self._format_contexts(contexts, max_tokens)
        
        # Build system context section
        sys_ctx_str = ""
        if system_context:
            sys_ctx_str = self._format_system_context(system_context, user_prompt)
        
        # Fill template
        body = template.format(
            user_prompt=user_prompt,
            contexts=context_str,
        )
        
        # Build final prompt with Persona
        enhanced = f"# Role\n{self.SYSTEM_PERSONA}\n\n"
        
        if sys_ctx_str:
            enhanced += f"# System Context\n{sys_ctx_str}\n\n"
            
        enhanced += body
        
        return {
            'enhanced_prompt': enhanced,
            'citations': citations,
            'metadata': {
                'intent': intent,
                'num_contexts': len(citations),
                'estimated_tokens': len(enhanced) // 4,
                'template_used': intent if intent in self.TEMPLATES else 'default',
            }
        }
    
    def _format_contexts(
        self,
        contexts: List[Dict],
        max_tokens: int
    ) -> tuple:
        """
        Stage 4: Context Synthesis.
        Groups relevant chunks by type and builds a structured mission briefing.
        """
        import re
        
        if not contexts:
            return "(No relevant context found)", []
        
        # 1. Group by Relevance Type
        grouped = {
            'direct_code': [],
            'architecture': [],
            'pattern': [],
            'logic': [],
            'general': []
        }
        
        for ctx in contexts:
            rtype = ctx.get('_relevance_type', 'general')
            grouped.setdefault(rtype, []).append(ctx)
            
        parts = []
        citations = []
        total_chars = 0
        max_chars = max_tokens * 4
        
        # 2. Synthesize Sections
        section_order = ['direct_code', 'architecture', 'logic', 'pattern', 'general']
        section_titles = {
            'direct_code': "## 💻 REUSABLE CODE BLOCKS",
            'architecture': "## 🏗️ ARCHITECTURAL DECISIONS",
            'logic': "## 🔢 LOGIC & FORMULAS",
            'pattern': "## 🎨 ESTABLISHED PATTERNS",
            'general': "## 📝 ADDITIONAL CONTEXT"
        }

        for rtype in section_order:
            items = grouped.get(rtype, [])
            if not items: continue
            
            parts.append(section_titles[rtype])
            
            for ctx in items:
                citation_id = len(citations) + 1
                citation = {
                    'id': citation_id,
                    'path': ctx.get('path', 'unknown'),
                    'name': Path(ctx.get('path', 'unknown')).name,
                    'similarity': ctx.get('similarity', ctx.get('_relevance_score', 0)),
                    'reason': ctx.get('_evaluation_reason', '')
                }
                
                content = ctx.get('full_content', ctx.get('content_preview', ''))
                # Token Compression
                content = re.sub(r'\n\s*\n', '\n\n', content.strip())
                
                # Format block based on type
                if rtype == 'direct_code':
                    block = f"### [{citation_id}] {citation['name']}\n```python\n{content}\n```\n"
                else:
                    # Provide a concise summary for non-code blocks
                    summary = content[:500] + ("..." if len(content) > 500 else "")
                    block = f"- **[{citation_id}] {citation['name']}**: {summary}\n"
                
                if total_chars + len(block) > max_chars:
                    break
                    
                parts.append(block)
                citations.append(citation)
                total_chars += len(block)
        
        return '\n'.join(parts), citations


    def _format_system_context(self, context: Dict, user_prompt: str = "") -> str:
        """Format system context"""
        import re
        
        parts = []
        
        if context.get('git'):
            git = context['git']
            if git.get('branch'):
                parts.append(f"- Git branch: `{git['branch']}`")
            if git.get('status'):
                status = git['status'].strip()
                # filter out noisy/useless git status
                if status and status not in ["?? ./", "./"]:
                    parts.append(f"- Changed files: {status}")
        
        if context.get('files'):
            files = context['files']
            if files.get('cwd'):
                parts.append(f"- Working directory: `{files['cwd']}`")
            if files.get('recent_edits'):
                edits = ', '.join(files['recent_edits'][:3])
                if edits and edits not in ["", "./"]:
                    parts.append(f"- Recently edited: {edits}")
                
        if context.get('gemini_cli') and 'error' not in context['gemini_cli']:
            g_cli = context['gemini_cli']
            
            # Check relevance of recent prompts to the current user prompt
            relevant_prompts = []
            if g_cli.get('recent_prompts'):
                # Simple keyword overlap heuristic for relevance
                user_prompt_lower = user_prompt.lower()
                user_words = set(re.findall(r'\b\w{4,}\b', user_prompt_lower))
                
                for p in g_cli['recent_prompts']:
                    p_lower = p.lower()
                    p_words = set(re.findall(r'\b\w{4,}\b', p_lower))
                    
                    # If there's an overlap in words or the user prompt is very short
                    if not user_words or len(user_words & p_words) > 0:
                        relevant_prompts.append(p)

            if relevant_prompts:
                parts.append("\n**Active Gemini CLI Session**")
                parts.append(f"- Session ID: `{g_cli.get('session_id')}`")
                parts.append("- Relevant Recent User Prompts:")
                for p in relevant_prompts:
                    parts.append(f"  > \"{p}\"")
                                    
        if context.get('claudecode') and 'error' not in context['claudecode']:
            c_cli = context['claudecode']
            
            # Check relevance of recent prompts
            relevant_prompts = []
            if c_cli.get('recent_prompts'):
                user_prompt_lower = user_prompt.lower()
                user_words = set(re.findall(r'\b\w{4,}\b', user_prompt_lower))
                
                for p in c_cli['recent_prompts']:
                    p_lower = p.lower()
                    p_words = set(re.findall(r'\b\w{4,}\b', p_lower))
                    if not user_words or len(user_words & p_words) > 0:
                        relevant_prompts.append(p)

            if relevant_prompts:
                parts.append("\n**Claude Code CLI Session**")
                parts.append(f"- Project: `{c_cli.get('project')}`")
                parts.append("- Relevant Recent User Prompts:")
                for p in relevant_prompts:
                    parts.append(f"  > \"{p}\"")
        
        return '\n'.join(parts) if parts else ""
                