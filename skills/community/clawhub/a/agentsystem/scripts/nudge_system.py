"""
Nudge System - Self-prompting for proactive behavior

This module implements:
- Scheduled nudges for memory persistence
- Skill creation triggers
- Evolution check reminders
- Learning reminders
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum


class NudgeType(Enum):
    """Types of nudges."""
    MEMORY_PERSISTENCE = "memory_persistence"
    SKILL_CREATION = "skill_creation"
    EVOLUTION_CHECK = "evolution_check"
    LEARNING_REMINDER = "learning_reminder"
    PERFORMANCE_ALERT = "performance_alert"
    USER_FOLLOWUP = "user_followup"


class NudgeStatus(Enum):
    """Status of nudges."""
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TriggerType(Enum):
    """Types of triggers."""
    TIME_BASED = "time_based"
    CONDITION_BASED = "condition_based"
    EVENT_BASED = "event_based"
    INTERVAL_BASED = "interval_based"


@dataclass
class Nudge:
    """Nudge definition."""
    id: str
    type: NudgeType
    trigger_type: TriggerType
    trigger_config: Dict
    data: Dict = field(default_factory=dict)
    status: NudgeStatus = NudgeStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    scheduled_for: Optional[str] = None
    executed_at: Optional[str] = None
    result: Optional[Dict] = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3


class NudgeScheduler:
    """
    Schedules and manages nudges.
    """
    
    def __init__(self, storage_path: str = './nudges'):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.nudges_file = self.storage_path / 'nudges.json'
        self.nudges: Dict[str, Nudge] = {}
        
        self._load_nudges()
    
    def _load_nudges(self):
        """Load nudges from storage."""
        if self.nudges_file.exists():
            with open(self.nudges_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for nudge_data in data.get('nudges', []):
                    nudge = Nudge(
                        id=nudge_data['id'],
                        type=NudgeType(nudge_data['type']),
                        trigger_type=TriggerType(nudge_data['trigger_type']),
                        trigger_config=nudge_data['trigger_config'],
                        data=nudge_data.get('data', {}),
                        status=NudgeStatus(nudge_data['status']),
                        created_at=nudge_data['created_at'],
                        scheduled_for=nudge_data.get('scheduled_for'),
                        executed_at=nudge_data.get('executed_at'),
                        result=nudge_data.get('result'),
                        error=nudge_data.get('error'),
                        retry_count=nudge_data.get('retry_count', 0),
                        max_retries=nudge_data.get('max_retries', 3)
                    )
                    self.nudges[nudge.id] = nudge
    
    def _save_nudges(self):
        """Save nudges to storage."""
        data = {
            'nudges': [
                {
                    'id': n.id,
                    'type': n.type.value,
                    'trigger_type': n.trigger_type.value,
                    'trigger_config': n.trigger_config,
                    'data': n.data,
                    'status': n.status.value,
                    'created_at': n.created_at,
                    'scheduled_for': n.scheduled_for,
                    'executed_at': n.executed_at,
                    'result': n.result,
                    'error': n.error,
                    'retry_count': n.retry_count,
                    'max_retries': n.max_retries
                }
                for n in self.nudges.values()
            ]
        }
        
        with open(self.nudges_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def schedule(self, nudge_type: NudgeType, trigger_type: TriggerType,
                 trigger_config: Dict, data: Dict = None) -> str:
        """
        Schedule a new nudge.
        
        Args:
            nudge_type: Type of nudge
            trigger_type: Type of trigger
            trigger_config: Trigger configuration
            data: Additional data for the nudge
            
        Returns:
            Nudge ID
        """
        nudge_id = f"nudge_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.nudges)}"
        
        # Calculate scheduled time
        scheduled_for = None
        if trigger_type == TriggerType.TIME_BASED:
            scheduled_for = trigger_config.get('execute_at')
        elif trigger_type == TriggerType.INTERVAL_BASED:
            interval_seconds = trigger_config.get('interval_seconds', 3600)
            scheduled_for = (datetime.now() + timedelta(seconds=interval_seconds)).isoformat()
        
        nudge = Nudge(
            id=nudge_id,
            type=nudge_type,
            trigger_type=trigger_type,
            trigger_config=trigger_config,
            data=data or {},
            scheduled_for=scheduled_for
        )
        
        self.nudges[nudge_id] = nudge
        self._save_nudges()
        
        return nudge_id
    
    def cancel(self, nudge_id: str) -> bool:
        """Cancel a scheduled nudge."""
        if nudge_id in self.nudges:
            self.nudges[nudge_id].status = NudgeStatus.CANCELLED
            self._save_nudges()
            return True
        return False
    
    def get_due_nudges(self) -> List[Nudge]:
        """Get nudges that are due for execution."""
        due = []
        now = datetime.now()
        
        for nudge in self.nudges.values():
            if nudge.status != NudgeStatus.PENDING:
                continue
            
            if nudge.trigger_type == TriggerType.TIME_BASED:
                if nudge.scheduled_for:
                    scheduled_time = datetime.fromisoformat(nudge.scheduled_for)
                    if now >= scheduled_time:
                        due.append(nudge)
            
            elif nudge.trigger_type == TriggerType.INTERVAL_BASED:
                if nudge.scheduled_for:
                    scheduled_time = datetime.fromisoformat(nudge.scheduled_for)
                    if now >= scheduled_time:
                        due.append(nudge)
            
            elif nudge.trigger_type == TriggerType.CONDITION_BASED:
                # Check condition
                if self._check_condition(nudge.trigger_config):
                    due.append(nudge)
            
            elif nudge.trigger_type == TriggerType.EVENT_BASED:
                # Event-based nudges are triggered externally
                pass
        
        return due
    
    def _check_condition(self, config: Dict) -> bool:
        """Check if condition is met."""
        condition_type = config.get('condition_type')
        
        if condition_type == 'experience_count':
            # Check if enough experiences collected
            min_count = config.get('min_count', 10)
            # This would check actual experience count
            return True  # Simplified
        
        elif condition_type == 'time_elapsed':
            elapsed_seconds = config.get('elapsed_seconds', 3600)
            last_execution = config.get('last_execution')
            if last_execution:
                elapsed = (datetime.now() - datetime.fromisoformat(last_execution)).total_seconds()
                return elapsed >= elapsed_seconds
            return True
        
        return False
    
    def update_status(self, nudge_id: str, status: NudgeStatus, 
                      result: Dict = None, error: str = None):
        """Update nudge status."""
        if nudge_id in self.nudges:
            self.nudges[nudge_id].status = status
            if result:
                self.nudges[nudge_id].result = result
            if error:
                self.nudges[nudge_id].error = error
            if status == NudgeStatus.COMPLETED or status == NudgeStatus.FAILED:
                self.nudges[nudge_id].executed_at = datetime.now().isoformat()
            self._save_nudges()


class NudgeHandler:
    """Base class for nudge handlers."""
    
    def execute(self, nudge: Nudge) -> Dict:
        raise NotImplementedError


class MemoryPersistenceHandler(NudgeHandler):
    """Handler for memory persistence nudges."""
    
    def __init__(self, memory_manager):
        self.memory = memory_manager
    
    def execute(self, nudge: Nudge) -> Dict:
        """Execute memory persistence nudge."""
        # Perform memory cleanup or backup
        stats = self.memory.get_stats()
        
        if nudge.data.get('action') == 'cleanup':
            cleanup_result = self.memory.cleanup()
            return {'action': 'cleanup', 'result': cleanup_result}
        
        elif nudge.data.get('action') == 'backup':
            backup_path = nudge.data.get('backup_path', './memory_backup.json')
            self.memory.backup(backup_path)
            return {'action': 'backup', 'path': backup_path}
        
        return {'action': 'stats', 'stats': stats}


class SkillCreationHandler(NudgeHandler):
    """Handler for skill creation nudges."""
    
    def __init__(self, skill_creator):
        self.creator = skill_creator
    
    def execute(self, nudge: Nudge) -> Dict:
        """Execute skill creation nudge."""
        experiences = nudge.data.get('experiences', [])
        
        if experiences:
            results = self.creator.scan_and_create(experiences)
            return {'created_skills': len([r for r in results if r['success']]), 'results': results}
        
        return {'created_skills': 0, 'reason': 'no experiences provided'}


class EvolutionCheckHandler(NudgeHandler):
    """Handler for evolution check nudges."""
    
    def __init__(self, evolution_system):
        self.evolution = evolution_system
    
    def execute(self, nudge: Nudge) -> Dict:
        """Execute evolution check nudge."""
        result = self.evolution.evolve()
        return {'evolution_result': result}


class LearningReminderHandler(NudgeHandler):
    """Handler for learning reminders."""
    
    def __init__(self, memory_manager):
        self.memory = memory_manager
    
    def execute(self, nudge: Nudge) -> Dict:
        """Execute learning reminder nudge."""
        # Analyze recent experiences and suggest improvements
        recent = self.memory.get_recent_episodes(limit=10)
        
        suggestions = []
        for episode in recent:
            if episode.outcome and 'fail' in episode.outcome.lower():
                suggestions.append({
                    'type': 'improvement',
                    'context': episode.context,
                    'suggestion': f"Review failure pattern in: {episode.user_input[:50]}"
                })
        
        return {'suggestions': suggestions, 'episodes_analyzed': len(recent)}


class NudgeSystem:
    """
    Main nudge system for proactive behavior.
    """
    
    def __init__(self, config: Dict = None, memory_manager=None, 
                 skill_creator=None, evolution_system=None):
        self.config = config or {
            'max_scheduled': 100,
            'check_interval': 60,  # seconds
            'user_can_disable': True
        }
        
        self.scheduler = NudgeScheduler()
        
        # Initialize handlers
        self.handlers: Dict[NudgeType, NudgeHandler] = {}
        
        if memory_manager:
            self.handlers[NudgeType.MEMORY_PERSISTENCE] = MemoryPersistenceHandler(memory_manager)
            self.handlers[NudgeType.LEARNING_REMINDER] = LearningReminderHandler(memory_manager)
        
        if skill_creator:
            self.handlers[NudgeType.SKILL_CREATION] = SkillCreationHandler(skill_creator)
        
        if evolution_system:
            self.handlers[NudgeType.EVOLUTION_CHECK] = EvolutionCheckHandler(evolution_system)
        
        self.execution_log: List[Dict] = []
    
    def schedule_memory_persistence(self, action: str = 'cleanup', 
                                    interval_seconds: int = 3600) -> str:
        """Schedule memory persistence nudge."""
        return self.scheduler.schedule(
            nudge_type=NudgeType.MEMORY_PERSISTENCE,
            trigger_type=TriggerType.INTERVAL_BASED,
            trigger_config={'interval_seconds': interval_seconds},
            data={'action': action}
        )
    
    def schedule_skill_creation(self, experiences: List[Dict], 
                                when: str = None) -> str:
        """Schedule skill creation nudge."""
        if when:
            trigger_type = TriggerType.TIME_BASED
            trigger_config = {'execute_at': when}
        else:
            trigger_type = TriggerType.CONDITION_BASED
            trigger_config = {'condition_type': 'experience_count', 'min_count': 5}
        
        return self.scheduler.schedule(
            nudge_type=NudgeType.SKILL_CREATION,
            trigger_type=trigger_type,
            trigger_config=trigger_config,
            data={'experiences': experiences}
        )
    
    def schedule_evolution_check(self, interval_seconds: int = 7200) -> str:
        """Schedule evolution check nudge."""
        return self.scheduler.schedule(
            nudge_type=NudgeType.EVOLUTION_CHECK,
            trigger_type=TriggerType.INTERVAL_BASED,
            trigger_config={'interval_seconds': interval_seconds}
        )
    
    def schedule_learning_reminder(self, interval_seconds: int = 1800) -> str:
        """Schedule learning reminder nudge."""
        return self.scheduler.schedule(
            nudge_type=NudgeType.LEARNING_REMINDER,
            trigger_type=TriggerType.INTERVAL_BASED,
            trigger_config={'interval_seconds': interval_seconds}
        )
    
    def check_and_execute(self) -> List[Dict]:
        """
        Check for due nudges and execute them.
        
        Returns:
            List of execution results
        """
        results = []
        due_nudges = self.scheduler.get_due_nudges()
        
        for nudge in due_nudges:
            result = self._execute_nudge(nudge)
            results.append(result)
        
        return results
    
    def _execute_nudge(self, nudge: Nudge) -> Dict:
        """Execute a single nudge."""
        execution_record = {
            'nudge_id': nudge.id,
            'type': nudge.type.value,
            'started_at': datetime.now().isoformat()
        }
        
        # Mark as executing
        self.scheduler.update_status(nudge.id, NudgeStatus.EXECUTING)
        
        try:
            # Get handler
            handler = self.handlers.get(nudge.type)
            
            if handler:
                result = handler.execute(nudge)
                
                self.scheduler.update_status(nudge.id, NudgeStatus.COMPLETED, result=result)
                
                execution_record['status'] = 'completed'
                execution_record['result'] = result
            else:
                raise ValueError(f"No handler for nudge type: {nudge.type}")
                
        except Exception as e:
            # Handle failure
            nudge.retry_count += 1
            
            if nudge.retry_count >= nudge.max_retries:
                self.scheduler.update_status(nudge.id, NudgeStatus.FAILED, error=str(e))
                execution_record['status'] = 'failed'
            else:
                self.scheduler.update_status(nudge.id, NudgeStatus.PENDING, error=str(e))
                execution_record['status'] = 'will_retry'
            
            execution_record['error'] = str(e)
        
        execution_record['completed_at'] = datetime.now().isoformat()
        self.execution_log.append(execution_record)
        
        return execution_record
    
    def trigger_event(self, event_type: str, event_data: Dict):
        """Trigger event-based nudges."""
        for nudge in self.scheduler.nudges.values():
            if (nudge.trigger_type == TriggerType.EVENT_BASED and
                nudge.trigger_config.get('event_type') == event_type and
                nudge.status == NudgeStatus.PENDING):
                
                nudge.data.update(event_data)
                self._execute_nudge(nudge)
    
    def get_status(self) -> Dict:
        """Get nudge system status."""
        pending = sum(1 for n in self.scheduler.nudges.values() 
                     if n.status == NudgeStatus.PENDING)
        completed = sum(1 for n in self.scheduler.nudges.values() 
                       if n.status == NudgeStatus.COMPLETED)
        failed = sum(1 for n in self.scheduler.nudges.values() 
                    if n.status == NudgeStatus.FAILED)
        
        return {
            'total_nudges': len(self.scheduler.nudges),
            'pending': pending,
            'completed': completed,
            'failed': failed,
            'recent_executions': len([e for e in self.execution_log 
                                     if datetime.fromisoformat(e['started_at']) > 
                                     datetime.now() - timedelta(hours=24)])
        }
    
    def clear_completed(self):
        """Clear completed nudges."""
        to_remove = [
            nudge_id for nudge_id, nudge in self.scheduler.nudges.items()
            if nudge.status in [NudgeStatus.COMPLETED, NudgeStatus.FAILED, NudgeStatus.CANCELLED]
        ]
        
        for nudge_id in to_remove:
            del self.scheduler.nudges[nudge_id]
        
        self.scheduler._save_nudges()
        
        return len(to_remove)


# Example usage
if __name__ == "__main__":
    # Initialize
    nudge_system = NudgeSystem()
    
    # Schedule some nudges
    nudge_system.schedule_memory_persistence(action='cleanup', interval_seconds=60)
    nudge_system.schedule_evolution_check(interval_seconds=120)
    nudge_system.schedule_learning_reminder(interval_seconds=30)
    
    print("Scheduled nudges:")
    for nudge in nudge_system.scheduler.nudges.values():
        print(f"  - {nudge.type.value}: {nudge.status.value}")
    
    # Check and execute (simulated)
    print("\nChecking for due nudges...")
    time.sleep(35)  # Wait for some to become due
    
    results = nudge_system.check_and_execute()
    print(f"\nExecuted {len(results)} nudges")
    
    # Get status
    print(f"\nStatus: {nudge_system.get_status()}")
