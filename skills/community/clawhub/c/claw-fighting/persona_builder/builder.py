"""
Persona Builder Core Logic
Interactive guided system for creating AI agent personas
"""

import json
import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib


class PersonaBuilder:
    """Interactive Persona Builder for Claw-Fighting agents"""

    def __init__(self):
        self.base_templates = self._load_archetypes()
        self.user_choices = {}
        self.current_step = 1

    def _load_archetypes(self) -> Dict[str, dict]:
        """Load archetype templates"""
        return {
            'mathematician': {
                'name': 'Mathematician',
                'description': 'Precise calculation, low-risk strategy',
                'base_params': {
                    'risk_tolerance': 30,
                    'bluff_frequency': 0.2,
                    'patience': 70,
                    'adaptability': 50
                },
                'system_prompt_template': "You are a mathematician-style player who relies on precise probability calculations. You only take calculated risks when the math supports your decisions."
            },
            'gambler': {
                'name': 'Gambler',
                'description': 'High-risk, expert bluffing',
                'base_params': {
                    'risk_tolerance': 85,
                    'bluff_frequency': 0.7,
                    'patience': 30,
                    'adaptability': 75
                },
                'system_prompt_template': "You are a gambler-style player who thrives on risk and deception. You frequently use strategic bluffing to pressure opponents."
            },
            'observer': {
                'name': 'Observer',
                'description': 'Careful analysis, counter-attacks',
                'base_params': {
                    'risk_tolerance': 50,
                    'bluff_frequency': 0.4,
                    'patience': 80,
                    'adaptability': 85
                },
                'system_prompt_template': "You are an observer-style player who carefully analyzes opponent patterns before striking. You prefer counter-attacks over aggressive plays."
            },
            'psychologist': {
                'name': 'Psychologist',
                'description': 'Psychological warfare, mind games',
                'base_params': {
                    'risk_tolerance': 60,
                    'bluff_frequency': 0.6,
                    'patience': 60,
                    'adaptability': 90
                },
                'system_prompt_template': "You are a psychologist-style player who uses psychological warfare and mind games. You adapt your strategy based on opponent behavior."
            },
            'berserker': {
                'name': 'Berserker',
                'description': 'Aggressive pressure, continuous offense',
                'base_params': {
                    'risk_tolerance': 75,
                    'bluff_frequency': 0.5,
                    'patience': 20,
                    'adaptability': 40
                },
                'system_prompt_template': "You are a berserker-style player who applies constant aggressive pressure. You prefer fast, decisive actions over careful analysis."
            }
        }

    def step1_archetype_selection(self, answers: List[dict]) -> dict:
        """Step 1: Determine base archetype from user choices"""
        # Calculate weights based on answers
        archetype_scores = {name: 0 for name in self.base_templates.keys()}

        for answer in answers:
            weights = answer.get('weights', {})
            for archetype, weight in weights.items():
                if archetype in archetype_scores:
                    archetype_scores[archetype] += weight

        # Select best archetype
        best_archetype = max(archetype_scores, key=archetype_scores.get)
        base_persona = self.base_templates[best_archetype].copy()

        return {
            'selected_archetype': best_archetype,
            'base_persona': base_persona,
            'scores': archetype_scores
        }

    def step2_finetune_parameters(self, base_persona: dict, adjustments: dict) -> dict:
        """Step 2: Fine-tune persona parameters"""
        persona = base_persona.copy()

        # Apply parameter adjustments
        base_params = persona.get('base_params', {})
        for param, value in adjustments.items():
            if param in base_params:
                base_params[param] = value

        # Generate enhanced system prompt
        prompt = self._generate_system_prompt(persona, adjustments)
        persona['system_prompt'] = prompt

        # Add catchphrases if provided
        if 'catchphrases' in adjustments:
            persona['catchphrases'] = adjustments['catchphrases']

        return persona

    def step3_generate_final_persona(self, persona: dict, name: str, feedback: Optional[dict] = None) -> dict:
        """Step 3: Generate final persona with signature"""
        # Apply any feedback-based adjustments
        if feedback:
            persona = self._apply_feedback(persona, feedback)

        # Create final persona structure
        final_persona = {
            'meta': {
                'name': name,
                'version': '1.0',
                'created_by': 'persona_builder_v1.1',
                'created_at': self._get_timestamp(),
            },
            'archetype': {
                'primary': persona.get('name', 'custom').lower(),
                'secondary': 'adaptive'
            },
            'personality_vectors': persona.get('base_params', {}),
            'cognitive_model': {
                'reasoning_depth': 'normal',
                'memory_retrieval_k': 5,
                'emotional_memory': True
            },
            'prompt_template': persona.get('system_prompt', ''),
            'voice': {
                'catchphrases': persona.get('catchphrases', []),
                'emotion_tags': self._get_emotion_tags(persona),
                'language_style': 'colloquial'
            }
        }

        # Generate signature for tamper detection
        signature = self._generate_signature(final_persona)
        final_persona['meta']['signature'] = signature

        return final_persona

    def _generate_system_prompt(self, persona: dict, adjustments: dict) -> str:
        """Generate system prompt based on persona and adjustments"""
        base_prompt = persona.get('system_prompt_template', '')

        # Add parameter-specific guidance
        params = persona.get('base_params', {})
        risk_tolerance = params.get('risk_tolerance', 50)
        bluff_freq = params.get('bluff_frequency', 0.5)

        prompt_parts = [base_prompt]

        if risk_tolerance > 70:
            prompt_parts.append("You are comfortable taking high risks and making bold moves even when the probability is not in your favor.")
        elif risk_tolerance < 30:
            prompt_parts.append("You prefer safe, calculated moves and avoid risks unless the odds are strongly in your favor.")

        if bluff_freq > 0.6:
            prompt_parts.append("You frequently use strategic deception and bluffing as core parts of your gameplay.")
        elif bluff_freq < 0.3:
            prompt_parts.append("You rarely bluff and prefer to play honestly, only making moves you can back up.")

        return " ".join(prompt_parts)

    def _generate_signature(self, persona: dict) -> str:
        """Generate tamper-proof signature for persona"""
        # Create signature from critical persona data
        critical_data = {
            'name': persona['meta']['name'],
            'prompt': persona['prompt_template'],
            'params': persona['personality_vectors']
        }

        data_str = json.dumps(critical_data, sort_keys=True)
        return f"sha256:{hashlib.sha256(data_str.encode()).hexdigest()}"

    def _get_emotion_tags(self, persona: dict) -> List[str]:
        """Get emotion tags based on archetype"""
        archetype = persona.get('name', '').lower()

        tag_map = {
            'mathematician': ['calm', 'analytical', 'precise'],
            'gambler': ['confident', 'risky', 'excitable'],
            'observer': ['patient', 'observant', 'strategic'],
            'psychologist': ['manipulative', 'adaptive', 'intuitive'],
            'berserker': ['aggressive', 'intense', 'impatient']
        }

        return tag_map.get(archetype, ['neutral'])

    def _apply_feedback(self, persona: dict, feedback: dict) -> dict:
        """Apply feedback from trial battle to adjust persona"""
        # This would implement feedback-based adjustments
        # For now, return persona as-is
        return persona

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

    def save_persona(self, persona: dict, filepath: str):
        """Save persona to YAML file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(persona, f, default_flow_style=False, allow_unicode=True)

    def get_questions_for_step1(self) -> List[dict]:
        """Get questions for archetype selection"""
        return [
            {
                'id': 'risk_scenario',
                'type': 'situational',
                'scenario': "You have 2 dice showing 6, and the current bid is 5 sixes. The probability is only 30%, but your opponent seems hesitant...",
                'options': [
                    {
                        'text': "Immediately challenge - the math doesn't lie",
                        'weights': {'mathematician': 20, 'risk_tolerance': -20}
                    },
                    {
                        'text': "Bid 6 sixes to bluff and pressure your opponent",
                        'weights': {'gambler': 30, 'risk_tolerance': 30, 'bluff_frequency': 20}
                    },
                    {
                        'text': "Call 5 sixes and observe the next round",
                        'weights': {'observer': 25, 'risk_tolerance': 0}
                    }
                ]
            },
            {
                'id': 'emotional_response',
                'type': 'personality',
                'question': "When your opponent successfully bluffs 3 times in a row, your agent should...",
                'options': [
                    {
                        'text': "Calmly record and mark opponent as 'high-risk type'",
                        'weights': {'mathematician': 15, 'patience': 20}
                    },
                    {
                        'text': "Fight back aggressively and challenge immediately next round",
                        'weights': {'berserker': 25, 'risk_tolerance': 15}
                    },
                    {
                        'text': "Taunt opponent: 'Your luck ends here'",
                        'weights': {'psychologist': 20, 'bluff_frequency': 15}
                    }
                ]
            }
        ]