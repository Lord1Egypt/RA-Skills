import asyncio
import json
import logging
import ssl
import time
import uuid
from typing import Callable, Dict, Optional

import websockets
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


class ClawFightingClient:
    """WebSocket client for Claw-Fighting Skill protocol"""

    def __init__(self, agent_id: str, trainer: str, coordinator_url: str):
        self.agent_id = agent_id
        self.trainer = trainer
        self.coordinator_url = coordinator_url
        self.websocket = None
        self.room_id = None
        self.private_key = ec.generate_private_key(ec.SECP256R1())
        self.public_key_pem = self._get_public_key_pem()

        # Callbacks
        self.on_game_state: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
        self.on_room_assignment: Optional[Callable] = None

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"Agent-{agent_id[:8]}")

    def _get_public_key_pem(self) -> str:
        """Get PEM-encoded public key"""
        public_key = self.private_key.public_key()
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode('utf-8')

    def sign_data(self, data: str) -> str:
        """Sign data with ECDSA"""
        signature = self.private_key.sign(
            data.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        return signature.hex()

    async def connect(self, model: str = "llama3:70b", supports_cot: bool = True):
        """Connect to coordinator and perform handshake"""
        try:
            # Create SSL context for WSS
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE  # For development

            # Connect to WebSocket
            uri = f"{self.coordinator_url}/ws"
            self.logger.info(f"Connecting to {uri}")

            self.websocket = await websockets.connect(
                uri,
                ssl=ssl_context,
                ping_interval=30,
                ping_timeout=10
            )

            # Perform handshake
            await self._handshake(model, supports_cot)

            # Start message handling loop
            await self._message_loop()

        except Exception as e:
            self.logger.error(f"Connection failed: {e}")
            raise

    async def _handshake(self, model: str, supports_cot: bool):
        """Perform initial handshake with coordinator"""
        handshake_msg = {
            "type": "handshake",
            "agent_id": self.agent_id,
            "data": {
                "type": "agent",
                "agent_id": self.agent_id,
                "trainer": self.trainer,
                "public_key": self.public_key_pem,
                "model": model,
                "supports_cot": supports_cot
            },
            "timestamp": time.time()
        }

        await self.websocket.send(json.dumps(handshake_msg))
        self.logger.info("Handshake sent")

        # Wait for room assignment
        response = await self.websocket.recv()
        data = json.loads(response)

        if data.get("type") == "room_assignment":
            self.room_id = data["room_id"]
            self.logger.info(f"Assigned to room: {self.room_id}")

            if self.on_room_assignment:
                self.on_room_assignment(self.room_id)
        else:
            raise Exception(f"Unexpected response: {data}")

    async def _message_loop(self):
        """Main message handling loop"""
        try:
            while True:
                message = await self.websocket.recv()
                data = json.loads(message)

                await self._handle_message(data)

        except websockets.exceptions.ConnectionClosed:
            self.logger.info("Connection closed by server")
        except Exception as e:
            self.logger.error(f"Message loop error: {e}")

    async def _handle_message(self, data: dict):
        """Handle incoming messages"""
        msg_type = data.get("type")

        if msg_type == "game_state":
            if self.on_game_state:
                await self.on_game_state(data)

        elif msg_type == "error":
            self.logger.error(f"Server error: {data.get('message')}")
            if self.on_error:
                self.on_error(data)

        elif msg_type == "heartbeat":
            # Respond to heartbeat
            response = {
                "type": "heartbeat",
                "timestamp": time.time()
            }
            await self.websocket.send(json.dumps(response))

        else:
            self.logger.warning(f"Unknown message type: {msg_type}")

    async def send_action(self, action: dict, cot: str = ""):
        """Send game action to coordinator"""
        if not self.websocket or not self.room_id:
            raise Exception("Not connected to room")

        # Calculate CoT hash
        cot_hash = ""
        if cot:
            digest = hashes.Hash(hashes.SHA256())
            digest.update(cot.encode('utf-8'))
            cot_hash = digest.finalize().hex()

        # Create action message
        action_msg = {
            "type": "action",
            "room_id": self.room_id,
            "agent_id": self.agent_id,
            "data": action,
            "cot_hash": cot_hash,
            "timestamp": time.time()
        }

        # Sign the action
        signature_data = f"{self.room_id}{action.get('turn', 0)}{json.dumps(action, sort_keys=True)}{action_msg['timestamp']}"
        action_msg["signature"] = self.sign_data(signature_data)

        await self.websocket.send(json.dumps(action_msg))
        self.logger.info(f"Action sent: {action}")

    async def disconnect(self):
        """Disconnect from coordinator"""
        if self.websocket:
            await self.websocket.close()
            self.logger.info("Disconnected from coordinator")


class DeterministicRandom:
    """Deterministic random number generator for dice"""

    @staticmethod
    def generate_dice(seed: str, agent_id: str, num_dice: int = 5) -> list:
        """Generate deterministic dice values"""
        # Combine seed and agent_id for unique but deterministic results
        combined = f"{seed}:{agent_id}"

        dice = []
        for i in range(num_dice):
            # Use HMAC for deterministic randomness
            hkdf = HKDF(
                algorithm=hashes.SHA256(),
                length=4,
                salt=None,
                info=f"dice_{i}".encode(),
            )
            key = hkdf.derive(combined.encode())
            dice_value = (int.from_bytes(key, 'big') % 6) + 1
            dice.append(dice_value)

        return dice

    @staticmethod
    def create_commitment(dice: list) -> str:
        """Create hash commitment for dice"""
        dice_str = ','.join(map(str, sorted(dice)))
        digest = hashes.Hash(hashes.SHA256())
        digest.update(dice_str.encode('utf-8'))
        return digest.finalize().hex()