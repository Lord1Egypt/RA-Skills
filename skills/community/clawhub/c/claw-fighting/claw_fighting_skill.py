"""
Claw-Fighting Skill for OpenClaw
A plugin that enables OpenClaw agents to participate in decentralized AI battles.
"""

import asyncio
import json
import logging
import os
import time
import uuid
from typing import Dict, List, Optional, Any

from .client import ClawFightingClient, DeterministicRandom


class ClawFightingSkill:
    """Main skill class for Claw-Fighting integration"""

    def __init__(self, openclaw_runtime):
        self.runtime = openclaw_runtime
        self.client = None
        self.config = self._load_config()
        self.agent_id = self.config.get('agent_id', str(uuid.uuid4()))
        self.is_connected = False
        self.current_game_state = None
        self.dice_values = []
        self.game_seed = None

        # Setup logging
        self.logger = logging.getLogger("ClawFighting-Skill")
        self.logger.setLevel(logging.INFO)

        # Register with OpenClaw
        self._register_hooks()

    def _load_config(self) -> dict:
        """Load skill configuration"""
        config_path = os.path.expanduser("~/.claw-fighting/config.json")
        default_config = {
            "coordinator_url": "wss://localhost:8443",
            "agent_id": str(uuid.uuid4()),
            "trainer": "Anonymous",
            "auto_connect": True,
            "persona_path": "~/.claw-fighting/personas/default.yaml"
        }

        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
        except Exception as e:
            self.logger.warning(f"Failed to load config: {e}")

        return default_config

    def _register_hooks(self):
        """Register hooks with OpenClaw runtime"""
        # Hook into decision making
        self.runtime.register_hook('before_decision', self._on_before_decision)
        self.runtime.register_hook('after_decision', self._on_after_decision)
        self.runtime.register_hook('on_thought', self._on_thought)

    async def _on_before_decision(self, context: dict) -> dict:
        """Called before agent makes a decision"""
        if not self.is_connected or not self.current_game_state:
            return context

        # Add game state to context
        context['claw_fighting'] = {
            'game_state': self.current_game_state,
            'dice_values': self.dice_values,
            'is_claw_fighting_game': True
        }

        return context

    async def _on_after_decision(self, decision: dict) -> dict:
        """Called after agent makes a decision"""
        if not self.is_connected or not self.current_game_state:
            return decision

        # Convert OpenClaw decision to Claw-Fighting action
        action = self._convert_decision_to_action(decision)
        if action:
            await self._send_action(action)

        return decision

    def _on_thought(self, thought: str):
        """Called when agent produces thought (Chain-of-Thought)"""
        if self.is_connected and hasattr(self, '_last_cot'):
            self._last_cot = thought

    def _convert_decision_to_action(self, decision: dict) -> Optional[dict]:
        """Convert OpenClaw decision to Claw-Fighting action format"""
        if not isinstance(decision, dict) or 'action' not in decision:
            return None

        action_type = decision['action']
        action_data = decision.get('data', {})

        if action_type == 'bid':
            return {
                'turn': self.current_game_state.get('turn', 0) + 1,
                'action': 'bid',
                'dice_count': action_data.get('dice_count'),
                'face_value': action_data.get('face_value')
            }
        elif action_type == 'challenge':
            return {
                'turn': self.current_game_state.get('turn', 0) + 1,
                'action': 'challenge'
            }
        elif action_type == 'exact':
            return {
                'turn': self.current_game_state.get('turn', 0) + 1,
                'action': 'exact'
            }

        return None

    async def connect(self, coordinator_url: str = None, trainer: str = None):
        """Connect to Claw-Fighting coordinator"""
        if coordinator_url:
            self.config['coordinator_url'] = coordinator_url
        if trainer:
            self.config['trainer'] = trainer

        try:
            self.client = ClawFightingClient(
                agent_id=self.agent_id,
                trainer=self.config['trainer'],
                coordinator_url=self.config['coordinator_url']
            )

            # Set up callbacks
            self.client.on_game_state = self._on_game_state
            self.client.on_error = self._on_error
            self.client.on_room_assignment = self._on_room_assignment

            # Connect
            await self.client.connect(
                model=self.runtime.get_model_info(),
                supports_cot=True
            )

            self.is_connected = True
            self.logger.info(f"Connected to coordinator as {self.agent_id}")

        except Exception as e:
            self.logger.error(f"Failed to connect: {e}")
            raise

    async def _on_game_state(self, game_state_data: dict):
        """Handle game state updates from coordinator"""
        self.logger.info(f"Received game state update")

        # Extract game state
        state = game_state_data.get('data', {})
        self.current_game_state = state

        # Handle different game phases
        if state.get('phase') == 'setup':
            await self._handle_setup_phase(state)
        elif state.get('phase') == 'playing':
            await self._handle_playing_phase(state)
        elif state.get('phase') == 'finished':
            await self._handle_finished_phase(state)

    async def _handle_setup_phase(self, state: dict):
        """Handle game setup phase"""
        seed = state.get('seed')
        if seed and not self.game_seed:
            self.game_seed = seed
            self.dice_values = DeterministicRandom.generate_dice(
                seed, self.agent_id, state.get('dice_per_player', 5)
            )

            # Create commitment
            commitment = DeterministicRandom.create_commitment(self.dice_values)

            # Send commitment to coordinator
            await self._send_commitment(commitment)

            self.logger.info(f"Setup complete. Dice: {self.dice_values}")

    async def _handle_playing_phase(self, state: dict):
        """Handle game playing phase"""
        # Update current game state
        public_state = state.get('public_state', {})

        # Trigger OpenClaw decision making
        await self._trigger_decision(public_state)

    async def _handle_finished_phase(self, state: dict):
        """Handle game finished phase"""
        winner = state.get('winner')
        self.logger.info(f"Game finished. Winner: {winner}")

        # Reset game state
        self.current_game_state = None
        self.dice_values = []
        self.game_seed = None

        # Store game result in memory
        await self._store_game_result(state)

    async def _trigger_decision(self, game_state: dict):
        """Trigger OpenClaw to make a decision"""
        # Prepare context for decision
        context = {
            'game_type': 'liars_dice',
            'current_bid': game_state.get('current_bid'),
            'my_dice': self.dice_values,
            'total_dice': game_state.get('total_dice'),
            'opponent_history': game_state.get('opponent_actions', []),
            'time_remaining': game_state.get('time_limit_ms', 10000)
        }

        # Trigger OpenClaw decision
        self._last_cot = ""
        decision = await self.runtime.make_decision(context)

        # Store CoT for transmission
        if hasattr(self, '_last_cot'):
            decision['cot'] = self._last_cot

    async def _send_action(self, action: dict):
        """Send action to coordinator"""
        if not self.client:
            return

        cot = getattr(self, '_last_cot', "")
        await self.client.send_action(action, cot)

    async def _send_commitment(self, commitment: str):
        """Send dice commitment to coordinator"""
        commitment_action = {
            'phase': 'setup',
            'action': 'commitment',
            'commitment': commitment
        }
        await self._send_action(commitment_action)

    async def _store_game_result(self, game_result: dict):
        """Store game result in OpenClaw memory"""
        memory_entry = {
            'type': 'claw_fighting_game',
            'timestamp': time.time(),
            'result': game_result,
            'dice_values': self.dice_values,
            'opponent': game_result.get('opponent_id'),
            'won': game_result.get('winner') == self.agent_id
        }

        await self.runtime.add_memory(memory_entry)

    def _on_error(self, error_data: dict):
        """Handle errors from coordinator"""
        self.logger.error(f"Coordinator error: {error_data}")

    def _on_room_assignment(self, room_id: str):
        """Handle room assignment"""
        self.logger.info(f"Assigned to room: {room_id}")

    async def disconnect(self):
        """Disconnect from coordinator"""
        if self.client:
            await self.client.disconnect()
            self.is_connected = False
            self.logger.info("Disconnected from coordinator")

    def get_status(self) -> dict:
        """Get current skill status"""
        return {
            'connected': self.is_connected,
            'agent_id': self.agent_id,
            'room_id': getattr(self.client, 'room_id', None) if self.client else None,
            'in_game': self.current_game_state is not None,
            'config': self.config
        }


# OpenClaw plugin entry point
def setup(openclaw_runtime):
    """Setup function called by OpenClaw"""
    skill = ClawFightingSkill(openclaw_runtime)

    # Auto-connect if configured
    if skill.config.get('auto_connect', True):
        asyncio.create_task(skill.connect())

    return skill