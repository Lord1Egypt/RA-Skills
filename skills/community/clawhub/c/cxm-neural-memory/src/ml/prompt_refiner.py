# src/cxm/ml/prompt_refiner.py

"""
Prompt Refiner - Turns vague prompts into precise ones
through progressive questioning and context inference
"""

from typing import Dict, List, Optional, Tuple
from pathlib import Path
import re


class PromptRefiner:
    """
    Turns vague prompts into precise ones through:
    
    1. Context Inference (automatically guessing context)
    2. Gap Detection (identifying missing information)
    3. Clarifying Questions (targeted inquiries)
    4. Progressive Refinement (iterative improvement)
    """
    
    # What an AI typically needs per intent
    REQUIRED_CONTEXT = {
        'code_optimization': {
            'must_have': [
                ('target', 'Which function/file should be optimized?'),
                ('current_performance', 'How slow is it currently?'),
                ('goal_performance', 'What would be acceptable performance?'),
            ],
            'nice_to_have': [
                ('constraints', 'Are there any constraints? (Memory, CPU, compatibility)'),
                ('tried_before', 'What have you tried already?'),
                ('measurement', 'How do you measure performance?'),
            ],
        },
        'bug_fixing': {
            'must_have': [
                ('error_message', 'What is the error message?'),
                ('reproduction', 'How can the error be reproduced?'),
                ('expected', 'What should happen instead?'),
            ],
            'nice_to_have': [
                ('when_started', 'When did the error first occur?'),
                ('what_changed', 'What was changed recently?'),
                ('environment', 'Which environment? (OS, Python version, etc.)'),
            ],
        },
        'code_generation': {
            'must_have': [
                ('what', 'What exactly should be generated?'),
                ('language', 'Which language/framework?'),
                ('behavior', 'How should it behave?'),
            ],
            'nice_to_have': [
                ('style', 'Code style preferences?'),
                ('integration', 'Where will it be integrated?'),
                ('tests', 'Should tests be generated as well?'),
            ],
        },
        'general': {
            'must_have': [
                ('goal', 'What exactly do you want to achieve?'),
            ],
            'nice_to_have': [
                ('context', 'What is the background?'),
                ('constraints', 'Are there any constraints?'),
            ],
        },
    }
    
    def __init__(self, context_gatherer=None, rag=None):
        """
        Args:
            context_gatherer: Automatic system context gatherer
            rag: RAG Engine for historical context
        """
        self.context_gatherer = context_gatherer
        self.rag = rag
    
    def analyze_gaps(
        self,
        prompt: str,
        intent: str,
        auto_context: Dict = None
    ) -> Dict:
        """
        Analyzes what is missing in the prompt
        
        Returns:
            {
                'provided': {key: value},      # What is already there
                'inferred': {key: value},      # What was automatically detected
                'missing_critical': [(key, question)],  # MUST be answered
                'missing_optional': [(key, question)],  # Would be helpful
                'completeness': float           # 0-1 how complete
            }
        """
        
        requirements = self.REQUIRED_CONTEXT.get(intent, self.REQUIRED_CONTEXT['general'])
        
        provided = {}
        inferred = {}
        missing_critical = []
        missing_optional = []
        
        # 1. Check what is already in the prompt
        provided = self._extract_provided(prompt, intent)
        
        # 2. What can be automatically inferred?
        if auto_context:
            inferred = self._infer_from_context(auto_context, intent)
        
        # 3. What is still missing?
        all_known = {**provided, **inferred}
        
        for key, question in requirements.get('must_have', []):
            if key not in all_known:
                missing_critical.append((key, question))
        
        for key, question in requirements.get('nice_to_have', []):
            if key not in all_known:
                missing_optional.append((key, question))
        
        # Completeness score
        total_fields = len(requirements.get('must_have', [])) + len(requirements.get('nice_to_have', []))
        filled_fields = len(all_known)
        completeness = filled_fields / max(total_fields, 1)
        
        return {
            'provided': provided,
            'inferred': inferred,
            'missing_critical': missing_critical,
            'missing_optional': missing_optional,
            'completeness': completeness,
        }
    
    def _extract_provided(self, prompt: str, intent: str) -> Dict:
        """Extract what the user has already said"""
        
        provided = {}
        prompt_lower = prompt.lower()
        
        # File names
        files = re.findall(
            r'\b[\w/.-]+\.(?:py|js|ts|rs|go|md|java|c|cpp|h)\b',
            prompt
        )
        if files:
            provided['target'] = files[0]
        
        # Function names
        funcs = re.findall(r'\b[a-zA-Z_]\w*\(\)', prompt)
        if funcs:
            provided['target'] = funcs[0]
        
        # Error messages
        errors = re.findall(
            r'(Error|Exception|Traceback|Failed|TypeError|ValueError'
            r'|KeyError|AttributeError|ImportError|NameError).*',
            prompt
        )
        if errors:
            provided['error_message'] = errors[0]
        
        # Performance numbers
        perf = re.findall(r'(\d+\.?\d*)\s*(ms|seconds?|s|minutes?|min)', prompt_lower)
        if perf:
            provided['current_performance'] = f"{perf[0][0]} {perf[0][1]}"
        
        # Language
        langs = re.findall(
            r'\b(python|javascript|typescript|rust|go|java|c\+\+|ruby)\b',
            prompt_lower
        )
        if langs:
            provided['language'] = langs[0]
        
        # "I already tried X"
        tried = re.findall(
            r'(?:tried|probiert|versucht|already)\s+(.+?)(?:\.|,|$)',
            prompt_lower
        )
        if tried:
            provided['tried_before'] = tried[0]
        
        return provided
    
    def _infer_from_context(self, context: Dict, intent: str) -> Dict:
        """Infer missing info from system context"""
        
        inferred = {}
        
        # Git context
        git = context.get('git')
        if git:
            if git.get('status'):
                # Which files changed?
                changed_files = [
                    line.split()[-1]
                    for line in (git['status'] or '').split('\n')
                    if line.strip()
                ]
                if changed_files:
                    inferred['target'] = changed_files[0]
                    inferred['what_changed'] = ', '.join(changed_files)
            
            if git.get('branch'):
                inferred['branch'] = git['branch']
        
        # File context
        files = context.get('files', {})
        if files.get('cwd'):
            inferred['working_directory'] = files['cwd']
        
        if files.get('recent_edits'):
            edits = files['recent_edits']
            if edits and 'target' not in inferred:
                # Recently edited file = likely the target
                inferred['target'] = edits[0]
        
        # Infer language from file extension
        target = inferred.get('target', '')
        if target.endswith('.py'):
            inferred['language'] = 'python'
        elif target.endswith('.js') or target.endswith('.ts'):
            inferred['language'] = 'javascript/typescript'
        elif target.endswith('.rs'):
            inferred['language'] = 'rust'
        
        return inferred
    
    def generate_clarifying_questions(
        self,
        gaps: Dict,
        max_questions: int = 3
    ) -> List[Dict]:
        """
        Generate the most important questions
        
        Returns:
            List of {
                'key': str,
                'question': str,
                'priority': 'critical' | 'optional',
                'suggestions': List[str]  # Possible answers
            }
        """
        
        questions = []
        
        # Critical first
        for key, question in gaps['missing_critical'][:max_questions]:
            q = {
                'key': key,
                'question': question,
                'priority': 'critical',
                'suggestions': self._generate_suggestions(key, gaps),
            }
            questions.append(q)
        
        # Then optional (if space)
        remaining = max_questions - len(questions)
        for key, question in gaps['missing_optional'][:remaining]:
            q = {
                'key': key,
                'question': question,
                'priority': 'optional',
                'suggestions': self._generate_suggestions(key, gaps),
            }
            questions.append(q)
        
        return questions
    
    def _generate_suggestions(self, key: str, gaps: Dict) -> List[str]:
        """Generate suggestions for answers based on context"""
        
        suggestions = []
        inferred = gaps.get('inferred', {})
        
        if key == 'target':
            # Suggest files from context
            if 'target' in inferred:
                suggestions.append(inferred['target'])
        
        elif key == 'language':
            if 'language' in inferred:
                suggestions.append(inferred['language'])
        
        elif key == 'current_performance':
            suggestions.extend(['< 1 second', '1-5 seconds', '> 10 seconds'])
        
        elif key == 'goal_performance':
            suggestions.extend(['As fast as possible', '< 100ms', '< 1 second'])
        
        elif key == 'error_message':
            suggestions.append('(Paste the error message)')
        
        return suggestions
    
    def refine_prompt(
        self,
        original_prompt: str,
        intent: str,
        answers: Dict,
        auto_context: Dict = None
    ) -> str:
        """
        Build refined prompt from original + answers + context
        
        Args:
            original_prompt: Original vague prompt
            intent: Detected intent
            answers: Answers to clarifying questions {key: answer}
            auto_context: Automatically gathered context
        
        Returns:
            Refined prompt
        """
        
        parts = [original_prompt, ""]
        
        # Context section
        context_parts = []
        
        # Automatic context
        if auto_context:
            inferred = self._infer_from_context(auto_context, intent)
            for key, value in inferred.items():
                if key not in answers and value and str(value).strip() not in ["./", "n", "none", "no", "."]:  
                    context_parts.append(f"- {key}: {value}")
        
        # User answers
        for key, answer in answers.items():
            if answer and answer.strip() and answer.lower() not in ["n", "none", "no"]:
                context_parts.append(f"- {key}: {answer}")
        
        if context_parts:
            parts.append("Additional context:")
            parts.extend(context_parts)
        
        return "\n".join(parts)
    
    def auto_refine(
        self,
        prompt: str,
        intent: str,
        auto_context: Dict = None
    ) -> Dict:
        """
        Automatic refinement WITHOUT user interaction
        
        Uses only automatically available context
        
        Returns:
            {
                'refined_prompt': str,
                'added_context': Dict,
                'still_missing': List,
                'completeness': float
            }
        """
        
        gaps = self.analyze_gaps(prompt, intent, auto_context)
        
        refined = self.refine_prompt(
            original_prompt=prompt,
            intent=intent,
            answers={},  # No manual answers
            auto_context=auto_context,
        )
        
        return {
            'refined_prompt': refined,
            'added_context': gaps['inferred'],
            'still_missing': gaps['missing_critical'],
            'completeness': gaps['completeness'],
        }
