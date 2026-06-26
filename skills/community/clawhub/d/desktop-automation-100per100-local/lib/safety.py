#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Security & Safety Module for Desktop Automation
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class SafetyInterlock:
    """Interlock de sécurité pour bloquer les actions dangereuses"""

    # Actions considérées comme risquées (nécessitent une confirmation ou mode avancé)
    RISKY_ACTIONS = {
        'click': ['click'],  # peut cliquer sur des boutons critiques
        'type': ['type'],    # peut taper des commandes ou données sensibles
        'press_key': ['press_key'],  # touches comme 'enter', 'delete', 'f1'...
        'drag': ['drag'],    # peut déplacer des fichiers
    }

    # Mots-clés déclencheurs dans les paramètres (ex: chemins, commandes)
    DANGEROUS_PATTERNS = {
        'text': [
            'rm ', 'del ', 'format', 'shutdown', 'reboot',
            'sudo ', 'admin', 'password', 'secret', 'token',
            '/etc/', 'C:\\Windows\\', 'C:\\Program Files\\'
        ],
        'template_path': [
            'C:\\Windows\\', 'C:\\Program Files\\', '/etc/', '/bin/', '/sbin/'
        ]
    }

    def __init__(self, safe_mode: bool = True, require_confirmation: bool = False):
        """
        Args:
            safe_mode: if True, block risky actions unless explicitly allowed
            require_confirmation: if True, log a warning for risky actions but allow
        """
        self.safe_mode = safe_mode
        self.require_confirmation = require_confirmation
        self.blocked_actions_log: List[Dict[str, Any]] = []

    def validate_action(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate an action before execution.
        Returns: {'allowed': bool, 'reason': str, 'params': dict}
        """
        # Vérifier les modèles risqués dans les paramètres
        for param_key, values in params.items():
            if param_key in self.DANGEROUS_PATTERNS:
                if isinstance(values, str):
                    for pattern in self.DANGEROUS_PATTERNS[param_key]:
                        if pattern.lower() in values.lower():
                            msg = f"Dangerous pattern '{pattern}' detected in param '{param_key}': {values}"
                            logger.warning(msg)
                            if self.safe_mode:
                                return {
                                    'allowed': False,
                                    'reason': f"Security: {msg}",
                                    'params': params
                                }

        # Vérifier si l'action est risquée
        is_risky = any(risk in action for risks in self.RISKY_ACTIONS.values() for risk in risks)
        if is_risky and self.safe_mode:
            return {
                'allowed': False,
                'reason': f"Action '{action}' blocked in safe mode. Disable safe_mode to allow.",
                'params': params
            }

        if is_risky and self.require_confirmation:
            logger.warning(f"Risky action executed: {action} with params={params}")

        return {'allowed': True, 'reason': '', 'params': params}

    def block_action(self, action: str, params: Dict[str, Any], reason: str):
        """Log a blocked action"""
        entry = {
            'action': action,
            'params': params,
            'reason': reason,
            'timestamp': logging.Formatter('%(asctime)s').format(logging.LogRecord(
                name='safety', level=logging.WARNING, pathname='', lineno=0,
                msg='', args=(), exc_info=None
            ))
        }
        self.blocked_actions_log.append(entry)

    def get_blocked_log(self) -> List[Dict[str, Any]]:
        return self.blocked_actions_log

# Instance globale (configurable via environnement ou fichier de config)
_safety = SafetyInterlock(safe_mode=True, require_confirmation=False)

def set_safe_mode(enabled: bool):
    """Activer/désactiver le mode sans échec"""
    _safety.safe_mode = enabled
    logger.info(f"Safe mode {'enabled' if enabled else 'disabled'}")

def get_safety() -> SafetyInterlock:
    return _safety
