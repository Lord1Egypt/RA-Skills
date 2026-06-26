"""
Proactive Work System - Task Queue + Proactive Heartbeat
Enables continuous work and active service capability
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Callable
from datetime import datetime, timedelta
from pathlib import Path
import json
import asyncio


class TaskStatus(Enum):
    """Task status"""
    READY = "ready"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    DONE = "done"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority"""
    LOW = 3
    MEDIUM = 2
    HIGH = 1
    CRITICAL = 0


@dataclass
class Task:
    """Task data structure"""
    id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.READY
    priority: TaskPriority = TaskPriority.MEDIUM
    depends_on: List[str] = field(default_factory=list)  # Task IDs this depends on
    assigned_to: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    blocked_reason: Optional[str] = None
    progress: float = 0.0  # 0-100
    metadata: Dict = field(default_factory=dict)
    
    def can_start(self, completed_tasks: Set[str]) -> bool:
        """Check if task can start (dependencies met)"""
        if self.status != TaskStatus.READY:
            return False
        return all(dep_id in completed_tasks for dep_id in self.depends_on)


@dataclass
class TaskQueue:
    """Task queue for managing work"""
    name: str
    ready: List[Task] = field(default_factory=list)
    in_progress: List[Task] = field(default_factory=list)
    blocked: List[Task] = field(default_factory=list)
    done: List[Task] = field(default_factory=list)


class TaskQueueManager:
    """
    Task Queue Manager
    
    Manages Ready/In Progress/Blocked/Done task states.
    """
    
    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize Task Queue Manager
        
        Args:
            storage_path: Path to store queue (default: ~/.anima/tasks/)
        """
        self.storage_path = Path(storage_path) if storage_path else Path("~/.anima/tasks").expanduser()
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.queue_file = self.storage_path / "QUEUE.md"
        
        self.queues: Dict[str, TaskQueue] = {
            "default": TaskQueue(name="default")
        }
        
        self.tasks: Dict[str, Task] = {}
        
        self._load_tasks()
    
    def _load_tasks(self):
        """Load tasks from storage"""
        if self.queue_file.exists():
            self._parse_queue_file(self.queue_file.read_text())
    
    def _parse_queue_file(self, content: str):
        """Parse QUEUE.md file"""
        current_section = None
        current_tasks = []
        
        for line in content.split("\n"):
            line = line.strip()
            
            if line.startswith("## ") and not line.startswith("###"):
                # Save previous section
                if current_section and current_tasks:
                    self._update_section_tasks(current_section, current_tasks)
                
                section_name = line.replace("## ", "").strip()
                current_section = section_name
                current_tasks = []
            
            elif line.startswith("- [ ]") or line.startswith("- [x]"):
                # Task line
                task_info = line.lstrip("- []x ")
                if task_info.startswith("@"):
                    # Has assignee
                    parts = task_info.split(":", 1)
                    if len(parts) > 1:
                        assignee = parts[0].replace("@", "").strip()
                        title = parts[1].strip()
                    else:
                        assignee = None
                        title = task_info.replace("@", "").strip()
                else:
                    title = task_info
                    assignee = None
                
                task = Task(
                    id=self._generate_id(),
                    title=title,
                    assigned_to=assignee
                )
                current_tasks.append(task)
                
                if "In Progress" in (current_section or ""):
                    task.status = TaskStatus.IN_PROGRESS
                elif "Blocked" in (current_section or ""):
                    task.status = TaskStatus.BLOCKED
                elif "Done" in (current_section or ""):
                    task.status = TaskStatus.DONE
        
        # Save last section
        if current_section and current_tasks:
            self._update_section_tasks(current_section, current_tasks)
    
    def _update_section_tasks(self, section: str, tasks: List[Task]):
        """Update tasks for a section"""
        for task in tasks:
            self.tasks[task.id] = task
    
    def _generate_id(self) -> str:
        """Generate unique task ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def _has_circular_dependency(self, task_id: str, visited: Set[str] = None) -> bool:
        """
        Detect circular dependency.
        
        Args:
            task_id: Task ID to check
            visited: Set of visited task IDs (for recursion)
            
        Returns:
            True if circular dependency exists
        """
        if visited is None:
            visited = set()
        
        if task_id in visited:
            return True
        
        visited.add(task_id)
        task = self.tasks.get(task_id)
        
        if task and task.depends_on:
            for dep_id in task.depends_on:
                if dep_id in self.tasks:  # Only check existing tasks
                    if self._has_circular_dependency(dep_id, visited.copy()):
                        return True
        
        return False
    
    def add_task(
        self,
        title: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.MEDIUM,
        depends_on: Optional[List[str]] = None,
        assigned_to: Optional[str] = None
    ) -> Task:
        """
        Add a new task
        
        Args:
            title: Task title
            description: Task description
            priority: Task priority
            depends_on: List of task IDs this depends on
            assigned_to: Agent ID to assign to
            
        Returns:
            Created task
        """
        task = Task(
            id=self._generate_id(),
            title=title,
            description=description,
            priority=priority,
            depends_on=depends_on or [],
            assigned_to=assigned_to
        )
        
        # Check for circular dependency
        if depends_on:
            for dep_id in depends_on:
                temp_task = Task(id=task.id, title=task.title, depends_on=depends_on)
                temp_tasks_backup = self.tasks.copy()
                self.tasks[task.id] = temp_task
                if self._has_circular_dependency(task.id):
                    self.tasks = temp_tasks_backup
                    raise ValueError(f"Circular dependency detected: {task.id} depends on {dep_id}")
                self.tasks.pop(task.id, None)
        
        self.tasks[task.id] = task
        self._update_queue_file()
        
        return task
    
    def get_ready_tasks(self, assignee: Optional[str] = None) -> List[Task]:
        """Get tasks that are ready to start"""
        completed = {t.id for t in self.tasks.values() if t.status == TaskStatus.DONE}
        
        ready_tasks = []
        for task in self.tasks.values():
            if task.can_start(completed):
                if assignee is None or task.assigned_to == assignee:
                    ready_tasks.append(task)
        
        # Sort by priority
        ready_tasks.sort(key=lambda t: t.priority.value)
        
        return ready_tasks
    
    def start_task(self, task_id: str, assignee: str) -> bool:
        """Start a task"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        completed = {t.id for t in self.tasks.values() if t.status == TaskStatus.DONE}
        
        if not task.can_start(completed):
            return False
        
        task.status = TaskStatus.IN_PROGRESS
        task.assigned_to = assignee
        task.started_at = datetime.now()
        task.updated_at = datetime.now()
        
        self._update_queue_file()
        return True
    
    def complete_task(self, task_id: str, progress: float = 100.0):
        """Mark task as completed"""
        task = self.tasks.get(task_id)
        if not task:
            return
        
        task.status = TaskStatus.DONE
        task.completed_at = datetime.now()
        task.progress = progress
        task.updated_at = datetime.now()
        
        self._update_queue_file()
    
    def block_task(self, task_id: str, reason: str):
        """Block a task"""
        task = self.tasks.get(task_id)
        if not task:
            return
        
        task.status = TaskStatus.BLOCKED
        task.blocked_reason = reason
        task.updated_at = datetime.now()
        
        self._update_queue_file()
    
    def unblock_task(self, task_id: str) -> bool:
        """Unblock a task"""
        task = self.tasks.get(task_id)
        if not task or task.status != TaskStatus.BLOCKED:
            return False
        
        task.status = TaskStatus.READY
        task.blocked_reason = None
        task.updated_at = datetime.now()
        
        self._update_queue_file()
        return True
    
    def update_progress(self, task_id: str, progress: float):
        """Update task progress"""
        task = self.tasks.get(task_id)
        if not task:
            return
        
        task.progress = min(100.0, max(0.0, progress))
        task.updated_at = datetime.now()
        
        self._update_queue_file()
    
    def cancel_task(self, task_id: str):
        """Cancel a task"""
        task = self.tasks.get(task_id)
        if not task:
            return
        
        task.status = TaskStatus.CANCELLED
        task.updated_at = datetime.now()
        
        self._update_queue_file()
    
    def _update_queue_file(self):
        """Update QUEUE.md file"""
        lines = [
            "# Task Queue",
            "",
            f"> Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
        ]
        
        # Ready tasks
        lines.append("## 🔴 Ready (can be picked up)")
        ready_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.READY]
        ready_tasks.sort(key=lambda t: t.priority.value)
        
        if ready_tasks:
            # Group by priority
            for priority in [TaskPriority.CRITICAL, TaskPriority.HIGH, TaskPriority.MEDIUM, TaskPriority.LOW]:
                priority_tasks = [t for t in ready_tasks if t.priority == priority]
                if priority_tasks:
                    priority_name = {TaskPriority.CRITICAL: "Critical", TaskPriority.HIGH: "High", TaskPriority.MEDIUM: "Medium", TaskPriority.LOW: "Low"}[priority]
                    lines.append(f"### {priority_name} Priority")
                    for task in priority_tasks:
                        assignee = f"@{task.assigned_to}: " if task.assigned_to else ""
                        lines.append(f"- [ ] {assignee}{task.title}")
                    lines.append("")
        else:
            lines.append("- (No ready tasks)")
            lines.append("")
        
        # In Progress tasks
        lines.append("## 🟡 In Progress")
        in_progress_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS]
        if in_progress_tasks:
            for task in in_progress_tasks:
                progress_str = f"[{task.progress:.0f}%]"
                assignee = f"@{task.assigned_to}: " if task.assigned_to else ""
                lines.append(f"- [ ] {assignee}{task.title} {progress_str}")
            lines.append("")
        else:
            lines.append("- (No tasks in progress)")
            lines.append("")
        
        # Blocked tasks
        lines.append("## 🔵 Blocked")
        blocked_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.BLOCKED]
        if blocked_tasks:
            for task in blocked_tasks:
                reason = f"(blocked: {task.blocked_reason})" if task.blocked_reason else ""
                lines.append(f"- [ ] {task.title} {reason}")
            lines.append("")
        else:
            lines.append("- (No blocked tasks)")
            lines.append("")
        
        # Done tasks
        lines.append("## ✅ Done Today")
        done_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.DONE]
        today = datetime.now().date()
        done_today = [t for t in done_tasks if t.completed_at and t.completed_at.date() == today]
        
        if done_today:
            for task in done_today:
                assignee = f"@{task.assigned_to}: " if task.assigned_to else ""
                lines.append(f"- [x] {assignee}{task.title}")
            lines.append("")
        else:
            lines.append("- (No tasks completed today)")
            lines.append("")
        
        # Ideas section
        lines.append("## 💡 Ideas (not yet tasks)")
        lines.append("- (Add your ideas here)")
        
        self.queue_file.write_text("\n".join(lines), encoding="utf-8")
    
    def get_stats(self) -> Dict:
        """Get queue statistics"""
        all_tasks = list(self.tasks.values())
        today = datetime.now().date()
        
        return {
            "total": len(all_tasks),
            "ready": sum(1 for t in all_tasks if t.status == TaskStatus.READY),
            "in_progress": sum(1 for t in all_tasks if t.status == TaskStatus.IN_PROGRESS),
            "blocked": sum(1 for t in all_tasks if t.status == TaskStatus.BLOCKED),
            "done": sum(1 for t in all_tasks if t.status == TaskStatus.DONE),
            "done_today": sum(1 for t in all_tasks if t.status == TaskStatus.DONE and t.completed_at and t.completed_at.date() == today),
            "total_today": sum(1 for t in all_tasks if t.created_at.date() == today)
        }


class ProactiveHeartbeat:
    """
    Proactive Heartbeat
    
    Performs meaningful work during heartbeat intervals.
    """
    
    def __init__(
        self,
        task_queue: Optional[TaskQueueManager] = None,
        learning_logger=None,
        min_work_interval_seconds: int = 300  # 5 minutes minimum
    ):
        """
        Initialize Proactive Heartbeat
        
        Args:
            task_queue: Task queue manager
            learning_logger: Learning logger instance
            min_work_interval_seconds: Minimum interval between proactive work
        """
        self.task_queue = task_queue or TaskQueueManager()
        self.learning_logger = learning_logger
        self.min_work_interval = min_work_interval_seconds
        self.last_work_time: Optional[datetime] = None
        self.work_count = 0
    
    async def run_heartbeat(
        self,
        agent_id: str,
        agent_name: str,
        has_human_messages: bool = False,
        check_callback: Optional[Callable] = None
    ) -> Dict:
        """
        Run proactive heartbeat
        
        Args:
            agent_id: Agent ID
            agent_name: Agent name
            has_human_messages: Whether there are urgent human messages
            check_callback: Optional callback for checks
            
        Returns:
            Heartbeat result dict
        """
        result = {
            "action": None,
            "task_id": None,
            "task_title": None,
            "work_done": False,
            "messages_handled": False
        }
        
        # 1. Quick checks - always prioritize human messages
        if has_human_messages:
            result["action"] = "handle_messages"
            return result
        
        if check_callback:
            check_result = await check_callback()
            if check_result.get("has_urgent"):
                result["action"] = "handle_urgent"
                return result
        
        # 2. Check if we should do proactive work
        if not self._should_do_work():
            result["action"] = "skip"
            return result
        
        # 3. Get next task from queue
        ready_tasks = self.task_queue.get_ready_tasks()
        
        if not ready_tasks:
            result["action"] = "no_tasks"
            return result
        
        # 4. Pick highest priority task
        task = ready_tasks[0]
        
        # 5. Start task
        self.task_queue.start_task(task.id, agent_name)
        
        result["action"] = "work"
        result["task_id"] = task.id
        result["task_title"] = task.title
        
        # 6. Do the work (placeholder - actual work done by caller)
        result["work_done"] = True
        self.last_work_time = datetime.now()
        self.work_count += 1
        
        return result
    
    def _should_do_work(self) -> bool:
        """Check if we should do proactive work"""
        if self.last_work_time is None:
            return True
        
        elapsed = (datetime.now() - self.last_work_time).total_seconds()
        return elapsed >= self.min_work_interval
    
    def complete_current_task(self, task_id: str, success: bool = True):
        """Mark current task as completed"""
        self.task_queue.complete_task(task_id, progress=100.0 if success else 0)
    
    def get_stats(self) -> Dict:
        """Get heartbeat statistics"""
        return {
            "total_work_sessions": self.work_count,
            "last_work_time": self.last_work_time.isoformat() if self.last_work_time else None,
            "should_work": self._should_do_work(),
            "queue_stats": self.task_queue.get_stats()
        }


class ActiveServiceManager:
    """
    Active Service Manager
    
    Manages continuous work and active service capabilities.
    """
    
    def __init__(
        self,
        task_queue: Optional[TaskQueueManager] = None,
        proactive_heartbeat: Optional[ProactiveHeartbeat] = None
    ):
        self.task_queue = task_queue or TaskQueueManager()
        self.heartbeat = proactive_heartbeat or ProactiveHeartbeat(task_queue=self.task_queue)
        
        self.active_hours = {
            "start": 6,   # 6 AM
            "end": 23    # 11 PM
        }
    
    def is_active_hours(self) -> bool:
        """Check if current time is within active hours"""
        current_hour = datetime.now().hour
        return self.active_hours["start"] <= current_hour < self.active_hours["end"]
    
    async def run_active_service(
        self,
        agent_id: str,
        agent_name: str,
        has_messages: bool = False
    ) -> Dict:
        """
        Run active service cycle
        
        Args:
            agent_id: Agent ID
            agent_name: Agent name
            has_messages: Whether there are messages to handle
            
        Returns:
            Service result
        """
        result = {
            "in_active_hours": self.is_active_hours(),
            "heartbeat_result": None,
            "tasks_completed": 0
        }
        
        # Only run during active hours
        if not self.is_active_hours():
            result["reason"] = "outside_active_hours"
            return result
        
        # Run proactive heartbeat
        heartbeat_result = await self.heartbeat.run_heartbeat(
            agent_id=agent_id,
            agent_name=agent_name,
            has_human_messages=has_messages
        )
        
        result["heartbeat_result"] = heartbeat_result
        
        if heartbeat_result.get("work_done"):
            result["tasks_completed"] = 1
        
        return result
    
    def get_daily_summary(self) -> Dict:
        """Get daily work summary"""
        stats = self.task_queue.get_stats()
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "tasks_total": stats["total"],
            "tasks_completed": stats["done"],
            "tasks_in_progress": stats["in_progress"],
            "tasks_pending": stats["ready"],
            "work_sessions": self.heartbeat.work_count,
            "active_hours": self.active_hours
        }
