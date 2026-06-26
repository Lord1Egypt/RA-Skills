"""Double-Loop Learning integration."""
import subprocess
from datetime import datetime
from zoneinfo import ZoneInfo

from .paths import PYTHON_BIN, get_prediction_logger_path

SHANGHAI_TZ = ZoneInfo('Asia/Shanghai')

def now_shanghai() -> datetime:
    return datetime.now(SHANGHAI_TZ)

def _run_prediction_logger(*args: str) -> None:
    """Invoke the prediction logger when it is available."""
    logger_path = get_prediction_logger_path()
    if logger_path is None:
        return

    try:
        subprocess.run(
            [PYTHON_BIN, str(logger_path), *args],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        # Missing interpreter/binary should not break the main task flow.
        return

def log_prediction(task: str, prediction: str, confidence: str = "M", uncertainty: str = ""):
    """Record a prediction before starting a task."""
    _run_prediction_logger("log", task, prediction, confidence, uncertainty)

def log_outcome(task: str, outcome: str, delta: str, lesson: str):
    """Record outcome after task completion."""
    _run_prediction_logger("complete", task, outcome, delta, lesson)

class LearningContext:
    """Context manager for automatic prediction/outcome logging."""
    
    def __init__(self, task: str, prediction: str, confidence: str = "M", uncertainty: str = ""):
        self.task = task
        self.prediction = prediction
        self.confidence = confidence
        self.uncertainty = uncertainty
        self.outcome = None
        self.delta = None
        self.lesson = None
    
    def __enter__(self):
        log_prediction(self.task, self.prediction, self.confidence, self.uncertainty)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.outcome = f"Failed: {exc_val}"
            self.delta = "Error occurred"
            self.lesson = "Need error handling improvement"
        else:
            # Outcome must be set via set_outcome() before exit
            pass
        log_outcome(self.task, self.outcome or "Completed", self.delta or "", self.lesson or "")
    
    def set_outcome(self, outcome: str, delta: str, lesson: str):
        self.outcome = outcome
        self.delta = delta
        self.lesson = lesson
