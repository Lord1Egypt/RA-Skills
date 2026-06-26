"""
ClawMobile Data Models
Implements JSON schemas defined in DATA-MODELS.md
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class KernelType(str, Enum):
    """Script kernel types"""
    ACCESSIBILITY = "accessibility"
    COORDINATE = "coordinate"


class MembershipTier(str, Enum):
    """Membership tiers"""
    FREE = "free"
    VIP = "vip"
    SVIP = "svip"


@dataclass
class TaskStep:
    """Single task step"""
    step_id: str
    action: str  # click, input, swipe, wait, scroll, press, long_press
    kernel_type: str
    selector: Optional[Dict[str, Any]] = None
    coordinate: Optional[Dict[str, int]] = None
    value: Optional[str] = None
    start: Optional[List[int]] = None
    end: Optional[List[int]] = None
    duration: Optional[int] = None
    condition: Optional[Dict[str, Any]] = None
    options: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


@dataclass
class TaskMetadata:
    """Task metadata"""
    created_at: str
    source: str  # "openclaw", "manual", "api"
    workflow_id: Optional[str] = None


@dataclass
class Task:
    """Complete task definition"""
    id: str  # Format: task_XXX
    type: str  # sequence, parallel, conditional
    kernel_type: KernelType
    priority: str  # low, normal, high, urgent
    timeout: int  # Timeout in milliseconds
    anti_detection: Dict[str, bool]
    steps: List[TaskStep]
    metadata: TaskMetadata


@dataclass
class TaskResult:
    """Result of task execution"""
    task_id: str
    status: str  # completed, error, timeout
    steps_result: List[Dict[str, Any]]
    total_duration_ms: int
    screenshot: Optional[str] = None
    error: Optional[str] = None
    completed_at: Optional[str] = None


@dataclass
class Membership:
    """User membership information"""
    user_id: str
    tier: MembershipTier
    activated_at: Optional[str] = None
    expires_at: Optional[str] = None
    activated_code: Optional[str] = None
    is_test: bool = False
    auto_renew: bool = False
    payment_source: Optional[str] = None  # redeem_code, afdian, manual
    transaction_id: Optional[str] = None


@dataclass
class MembershipPermissions:
    """Membership permissions"""
    max_daily_runs: int  # -1 for unlimited
    can_export_import: bool
    can_schedule: bool
    can_use_ai_intervention: bool
    can_develop_manually: bool
    can_use_natural_language: bool
    priority_support: bool


@dataclass
class MembershipStatus:
    """Membership status information"""
    is_active: bool
    days_remaining: int
    is_expired: bool
    will_expire_soon: bool


@dataclass
class UsageStatistics:
    """Daily usage statistics"""
    runs_completed: int
    runs_remaining: int
    date: str  # YYYY-MM-DD format


@dataclass
class MembershipInfo:
    """Complete membership information"""
    membership: Membership
    status: MembershipStatus
    permissions: MembershipPermissions
    today_usage: UsageStatistics


class TaskFactory:
    """Factory for creating task objects"""

    @staticmethod
    def create_click_task(
        x: int,
        y: int,
        description: str = "Click action",
        task_id: Optional[str] = None
    ) -> Task:
        """Create a simple click task"""
        import time

        return Task(
            id=task_id or f"task_{int(time.time())}",
            type="sequence",
            kernel_type=KernelType.COORDINATE,
            priority="normal",
            timeout=30000,
            anti_detection={
                "random_offset": True,
                "random_delay": True
            },
            steps=[
                TaskStep(
                    step_id="step_001",
                    action="click",
                    kernel_type="coordinate",
                    coordinate={"x": x, "y": y},
                    description=description
                )
            ],
            metadata=TaskMetadata(
                created_at=datetime.now().isoformat(),
                source="openclaw"
            )
        )

    @staticmethod
    def create_input_task(
        x: int,
        y: int,
        text: str,
        description: str = "Input text",
        task_id: Optional[str] = None
    ) -> Task:
        """Create an input task"""
        import time

        return Task(
            id=task_id or f"task_{int(time.time())}",
            type="sequence",
            kernel_type=KernelType.ACCESSIBILITY,
            priority="normal",
            timeout=30000,
            anti_detection={
                "random_offset": True,
                "random_delay": True
            },
            steps=[
                TaskStep(
                    step_id="step_001",
                    action="click",
                    kernel_type="accessibility",
                    selector={"id": f"auto_input_{int(time.time())}"},
                    coordinate={"x": x, "y": y},
                    description="Focus input field"
                ),
                TaskStep(
                    step_id="step_002",
                    action="input",
                    kernel_type="accessibility",
                    selector={"id": f"auto_input_{int(time.time())}"},
                    value=text,
                    options={
                        "clear": True,
                        "delay": 100
                    },
                    description=description
                )
            ],
            metadata=TaskMetadata(
                created_at=datetime.now().isoformat(),
                source="openclaw"
            )
        )

    @staticmethod
    def create_swipe_task(
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: int = 300,
        description: str = "Swipe action",
        task_id: Optional[str] = None
    ) -> Task:
        """Create a swipe task"""
        import time

        return Task(
            id=task_id or f"task_{int(time.time())}",
            type="sequence",
            kernel_type=KernelType.COORDINATE,
            priority="normal",
            timeout=30000,
            anti_detection={
                "random_speed": True
            },
            steps=[
                TaskStep(
                    step_id="step_001",
                    action="swipe",
                    kernel_type="coordinate",
                    start=[start_x, start_y],
                    end=[end_x, end_y],
                    duration=duration,
                    description=description
                )
            ],
            metadata=TaskMetadata(
                created_at=datetime.now().isoformat(),
                source="openclaw"
            )
        )

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Task:
        """Create Task from dictionary"""
        steps = [
            TaskStep(**step) for step in data.get("steps", [])
        ]

        return Task(
            id=data["id"],
            type=data["type"],
            kernel_type=KernelType(data["kernel_type"]),
            priority=data["priority"],
            timeout=data["timeout"],
            anti_detection=data.get("anti_detection", {}),
            steps=steps,
            metadata=TaskMetadata(**data["metadata"])
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert Task to dictionary"""
        return {
            "id": self.id,
            "type": self.type,
            "kernel_type": self.kernel_type.value,
            "priority": self.priority,
            "timeout": self.timeout,
            "anti_detection": self.anti_detection,
            "steps": [
                {
                    "step_id": step.step_id,
                    "action": step.action,
                    "kernel_type": step.kernel_type,
                    "selector": step.selector,
                    "coordinate": step.coordinate,
                    "value": step.value,
                    "start": step.start,
                    "end": step.end,
                    "duration": step.duration,
                    "condition": step.condition,
                    "options": step.options,
                    "description": step.description
                }
                for step in self.steps
            ],
            "metadata": {
                "created_at": self.metadata.created_at,
                "source": self.metadata.source,
                "workflow_id": self.metadata.workflow_id
            }
        }


class MembershipManager:
    """Manage membership operations"""

    @staticmethod
    def get_free_membership() -> MembershipInfo:
        """Get free tier membership info"""
        membership = Membership(
            user_id="user_001",  # Placeholder
            tier=MembershipTier.FREE,
            activated_at=None,
            expires_at=None
        )

        return MembershipInfo(
            membership=membership,
            status=MembershipStatus(
                is_active=False,
                days_remaining=0,
                is_expired=False,
                will_expire_soon=False
            ),
            permissions=MembershipPermissions(
                max_daily_runs=3,
                can_export_import=False,
                can_schedule=False,
                can_use_ai_intervention=False,
                can_develop_manually=False,
                can_use_natural_language=True,
                priority_support=False
            ),
            today_usage=UsageStatistics(
                runs_completed=0,
                runs_remaining=3,
                date=datetime.now().strftime('%Y-%m-%d')
            )
        )

    @staticmethod
    def activate_membership(code: str, user_id: str) -> MembershipInfo:
        """
        Activate membership using redeem code

        Returns:
            MembershipInfo after activation
        """
        # Parse code
        parts = code.split('-')
        tier_str = parts[0].lower()

        if tier_str == "vip":
            tier = MembershipTier.VIP
            days = 30
        elif tier_str == "svip":
            tier = MembershipTier.SVIP
            days = 90
        else:
            raise ValueError("Invalid tier in code")

        # Calculate expiry
        from datetime import timedelta
        expires_at = datetime.now() + timedelta(days=days)

        membership = Membership(
            user_id=user_id,
            tier=tier,
            activated_at=datetime.now().isoformat(),
            expires_at=expires_at.isoformat(),
            activated_code=code,
            is_test=False,
            payment_source="redeem_code"
        )

        # Determine permissions based on tier
        if tier == MembershipTier.VIP:
            permissions = MembershipPermissions(
                max_daily_runs=-1,  # Unlimited
                can_export_import=True,
                can_schedule=True,
                can_use_ai_intervention=True,
                can_develop_manually=False,
                can_use_natural_language=True,
                priority_support=False
            )
        elif tier == MembershipTier.SVIP:
            permissions = MembershipPermissions(
                max_daily_runs=-1,
                can_export_import=True,
                can_schedule=True,
                can_use_ai_intervention=True,
                can_develop_manually=True,
                can_use_natural_language=True,
                priority_support=True
            )
        else:
            permissions = MembershipPermissions(
                max_daily_runs=3,
                can_export_import=False,
                can_schedule=False,
                can_use_ai_intervention=False,
                can_develop_manually=False,
                can_use_natural_language=True,
                priority_support=False
            )

        return MembershipInfo(
            membership=membership,
            status=MembershipStatus(
                is_active=True,
                days_remaining=days,
                is_expired=False,
                will_expire_soon=days < 7
            ),
            permissions=permissions,
            today_usage=UsageStatistics(
                runs_completed=0,
                runs_remaining=-1 if tier != MembershipTier.FREE else 3,
                date=datetime.now().strftime('%Y-%m-%d')
            )
        )


# Data validation functions
def validate_task_id(task_id: str) -> bool:
    """Validate task ID format (task_XXX)"""
    import re
    pattern = r'^task_[0-9]{3}$'
    return bool(re.match(pattern, task_id))


def validate_workflow_id(workflow_id: str) -> bool:
    """Validate workflow ID format (workflow_XXX)"""
    import re
    pattern = r'^workflow_[0-9]{3}$'
    return bool(re.match(pattern, workflow_id))


def validate_user_id(user_id: str) -> bool:
    """Validate user ID format (user_XXX)"""
    import re
    pattern = r'^user_[0-9]{3}$'
    return bool(re.match(pattern, user_id))


def validate_redeem_code(code: str) -> bool:
    """Validate redeem code format"""
    import re
    pattern = r'^(VIP|SVIP)-\d{4}-[A-Z0-9]{8}$'
    return bool(re.match(pattern, code))


# Convenience functions for creating tasks
def create_click_task(x: int, y: int) -> Task:
    """Create a click task"""
    return TaskFactory.create_click_task(x, y)


def create_input_task(x: int, y: int, text: str) -> Task:
    """Create an input task"""
    return TaskFactory.create_input_task(x, y, text)


def create_swipe_task(start_x: int, start_y: int, end_x: int, end_y: int) -> Task:
    """Create a swipe task"""
    return TaskFactory.create_swipe_task(start_x, start_y, end_x, end_y)


def task_to_dict(task: Task) -> Dict[str, Any]:
    """Convert Task to dictionary"""
    return task.to_dict()


def dict_to_task(data: Dict[str, Any]) -> Task:
    """Convert dictionary to Task"""
    return TaskFactory.from_dict(data)


# Export/Import data models
@dataclass
class ExportPackageInfo:
    """Information about exported package"""
    file_name: str
    file_size: int
    format: str  # complete, script, lightweight
    created_at: str
    workflow_id: str
    workflow_name: str
    version: str
    included_files: List[str]


@dataclass
class ImportPreview:
    """Preview of import package"""
    package_info: Dict[str, Any]
    workflow_info: Dict[str, Any]
    included_files: List[str]
    requirements: Dict[str, Any]
    compatibility: Dict[str, Any]
