#!/usr/bin/env python3
"""
Error Recovery: Handle subordinate failures with retries and fallbacks.
- Retry with modified prompt
- Fall back to simpler approach
- Log failure patterns
- Update metrics
"""
import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from enum import Enum

LOG_DIR = Path('/a0/usr/projects/frugal_orchestrator/logs')
LOG_DIR.mkdir(parents=True, exist_ok=True)

class FailureType(Enum):
    TIMEOUT = "timeout"
    PARSE_ERROR = "parse_error"
    EXECUTION_ERROR = "execution_error"
    CONTEXT_LIMIT = "context_limit"
    UNKNOWN = "unknown"

class ErrorRecovery:
    """Handle subordinate failures with intelligent retry and fallback"""

    DEFAULT_MAX_RETRIES = 3
    DEFAULT_BACKOFF_BASE = 1.5

    def __init__(self, max_retries: int = DEFAULT_MAX_RETRIES, backoff_base: float = DEFAULT_BACKOFF_BASE):
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.retry_history = {}

    def _hash_task(self, task_type: str, params: Dict[str, Any]) -> str:
        content = json.dumps({'type': task_type, 'params': params}, sort_keys=True, default=str)
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _log_failure(self, task_type: str, error: str, recovery_action: str, success: bool):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'task_type': task_type,
            'error_type': self._classify_error(error),
            'error_message': error[:200],
            'recovery_action': recovery_action,
            'success': success
        }

        log_path = LOG_DIR / 'failures.json'
        failures = []
        if log_path.exists():
            try:
                with open(log_path) as f:
                    failures = json.load(f)
            except:
                pass
        failures.append(entry)
        failures = failures[-1000:]
        with open(log_path, 'w') as f:
            json.dump(failures, f, default=str)

    def _classify_error(self, error: str) -> str:
        error = error.lower()
        if 'timeout' in error or 'timed out' in error:
            return FailureType.TIMEOUT.value
        elif 'json' in error or 'parse' in error or 'decode' in error:
            return FailureType.PARSE_ERROR.value
        elif 'context' in error or 'token' in error:
            return FailureType.CONTEXT_LIMIT.value
        elif any(x in error for x in ['permission', 'denied', 'not found', 'failed']):
            return FailureType.EXECUTION_ERROR.value
        return FailureType.UNKNOWN.value

    def _simplify_prompt(self, original_prompt: str, attempt: int) -> str:
        simplifications = [
            original_prompt,
            f"{original_prompt}\n\nFocus on the most important output only.",
            f"{original_prompt}\n\nProvide minimal output. Bullet points preferred.",
            "Summarize the key points only. Be brief."
        ]
        return simplifications[min(attempt, len(simplifications) - 1)]

    def _get_fallback_strategy(self, failure_type: FailureType, attempt: int) -> str:
        strategies = {
            FailureType.CONTEXT_LIMIT: ["system_command", "summarize_input", "external_temp_file"],
            FailureType.TIMEOUT: ["reduce_scope", "parallel_chunks", "async_defer"],
            FailureType.PARSE_ERROR: ["simpler_output", "structured_format", "retry_validation"],
            FailureType.EXECUTION_ERROR: ["simplified_prompt", "alternative_tool", "skip_optional"],
            FailureType.UNKNOWN: ["retry", "simplified_prompt", "manual_review"]
        }
        type_strategies = strategies.get(failure_type, strategies[FailureType.UNKNOWN])
        if attempt < len(type_strategies):
            return type_strategies[attempt]
        return "manual_review"

    def recover(self, task_type: str, params: Dict[str, Any], error: str, original_prompt: str, execute_fn: Optional[Callable] = None) -> Dict[str, Any]:
        task_hash = self._hash_task(task_type, params)
        failure_type = FailureType(self._classify_error(error))
        start_time = time.time()

        for attempt in range(1, self.max_retries + 1):
            strategy = self._get_fallback_strategy(failure_type, attempt - 1)
            modified_prompt = self._simplify_prompt(original_prompt, attempt)

            success = False
            result = None
            if execute_fn:
                try:
                    result = execute_fn(task_type, {**params, 'prompt': modified_prompt})
                    success = True
                except Exception as e:
                    result = str(e)

            self._log_failure(task_type, error, f"{strategy}_attempt_{attempt}", success)

            if success:
                return {
                    'recovered': True,
                    'result': result,
                    'attempts': attempt,
                    'strategy': strategy,
                    'time_taken': round(time.time() - start_time, 3)
                }

            time.sleep(self.backoff_base ** attempt)

        return {
            'recovered': False,
            'error': error,
            'attempts': self.max_retries,
            'final_strategy': "failed_all",
            'time_taken': round(time.time() - start_time, 3)
        }

    def get_failure_stats(self) -> Dict[str, Any]:
        stats_file = LOG_DIR / 'recovery_stats.json'
        if stats_file.exists():
            with open(stats_file) as f:
                return json.load(f)
        return {'total_recoveries': 0, 'total_failures': 0}


def main():
    import sys
    recovery = ErrorRecovery()

    if len(sys.argv) < 2:
        print(json.dumps({
            'module': 'error_recovery',
            'status': 'ready',
            'max_retries': recovery.max_retries,
            'failure_stats': recovery.get_failure_stats()
        }, indent=2))
        return

    cmd = sys.argv[1]
    if cmd == 'stats':
        print(json.dumps(recovery.get_failure_stats(), indent=2))
    elif cmd == 'classify':
        error = ' '.join(sys.argv[2:])
        print(json.dumps({'error': error, 'type': recovery._classify_error(error)}))
    else:
        print(json.dumps({'error': f'Unknown command: {cmd}', 'available': ['stats', 'classify']}))


if __name__ == '__main__':
    main()
