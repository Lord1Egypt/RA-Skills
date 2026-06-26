"""
Feedback Collection and AI Accuracy Improvement System
Collects user feedback on AI analyses and tracks accuracy metrics over time.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import statistics


@dataclass
class FeedbackEntry:
    """A single feedback entry from a user."""
    id: str
    timestamp: str
    
    # Original error
    error_message: str
    stack_trace: Optional[str]
    
    # AI analysis result
    ai_error_type: str
    ai_severity: str
    ai_explanation: str
    ai_suggestions: List[str]
    
    # User feedback
    is_error_type_correct: bool
    is_severity_correct: bool
    is_explanation_helpful: bool
    did_fix_work: Optional[bool]  # None = not tried yet
    rating: int  # 1-5
    user_correction: Optional[str] = None  # User's own explanation if AI was wrong
    
    # Metadata
    category: Optional[str] = None  # nodejs, python, go, etc.


class FeedbackCollector:
    """Collects and stores user feedback on AI analyses."""
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path(__file__).parent.parent.parent / "data" / "feedback.jsonl"
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
    
    def record_feedback(
        self,
        error_message: str,
        stack_trace: Optional[str],
        ai_analysis: Dict,
        user_feedback: Dict
    ) -> str:
        """Record user feedback on an AI analysis."""
        
        feedback_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        
        entry = FeedbackEntry(
            id=feedback_id,
            timestamp=datetime.now().isoformat(),
            error_message=error_message,
            stack_trace=stack_trace,
            ai_error_type=ai_analysis.get('error_type', ''),
            ai_severity=ai_analysis.get('severity', ''),
            ai_explanation=ai_analysis.get('explanation', ''),
            ai_suggestions=ai_analysis.get('suggestions', []),
            is_error_type_correct=user_feedback.get('error_type_correct', True),
            is_severity_correct=user_feedback.get('severity_correct', True),
            is_explanation_helpful=user_feedback.get('explanation_helpful', True),
            did_fix_work=user_feedback.get('fix_worked'),
            rating=user_feedback.get('rating', 3),
            user_correction=user_feedback.get('correction'),
            category=user_feedback.get('category')
        )
        
        # Append to JSONL file
        with open(self.storage_path, 'a') as f:
            f.write(json.dumps(asdict(entry)) + '\n')
        
        return feedback_id
    
    def get_all_feedback(self) -> List[FeedbackEntry]:
        """Load all feedback entries."""
        if not self.storage_path.exists():
            return []
        
        entries = []
        with open(self.storage_path, 'r') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    entries.append(FeedbackEntry(**data))
        
        return entries
    
    def get_feedback_stats(self) -> Dict:
        """Calculate statistics from feedback."""
        entries = self.get_all_feedback()
        
        if not entries:
            return {
                "total_feedback": 0,
                "message": "No feedback collected yet"
            }
        
        stats = {
            "total_feedback": len(entries),
            "avg_rating": statistics.mean([e.rating for e in entries]),
            "error_type_accuracy": sum(1 for e in entries if e.is_error_type_correct) / len(entries),
            "severity_accuracy": sum(1 for e in entries if e.is_severity_correct) / len(entries),
            "explanation_helpful_rate": sum(1 for e in entries if e.is_explanation_helpful) / len(entries),
            "fix_success_rate": None,
            "common_issues": {},
            "by_category": {}
        }
        
        # Fix success rate (only count where user tried the fix)
        fix_attempts = [e for e in entries if e.did_fix_work is not None]
        if fix_attempts:
            stats["fix_success_rate"] = sum(1 for e in fix_attempts if e.did_fix_work) / len(fix_attempts)
        
        # Common issues (where AI was wrong)
        wrong_entries = [e for e in entries if not e.is_error_type_correct]
        if wrong_entries:
            issue_counts = {}
            for e in wrong_entries:
                key = e.ai_error_type
                issue_counts[key] = issue_counts.get(key, 0) + 1
            stats["common_issues"] = dict(sorted(issue_counts.items(), key=lambda x: -x[1])[:5])
        
        # By category
        categories = {}
        for e in entries:
            cat = e.category or "unknown"
            if cat not in categories:
                categories[cat] = {"count": 0, "ratings": [], "correct": 0}
            categories[cat]["count"] += 1
            categories[cat]["ratings"].append(e.rating)
            if e.is_error_type_correct:
                categories[cat]["correct"] += 1
        
        for cat, data in categories.items():
            stats["by_category"][cat] = {
                "count": data["count"],
                "avg_rating": statistics.mean(data["ratings"]),
                "accuracy": data["correct"] / data["count"]
            }
        
        return stats
    
    def get_training_data(self) -> List[Dict]:
        """Get feedback entries suitable for training/fine-tuning.
        
        Returns entries where:
        - User gave high rating (4-5) AND confirmed error type was correct
        - OR user provided a correction
        """
        entries = self.get_all_feedback()
        
        training_data = []
        
        for e in entries:
            # High-quality correct entries
            if e.rating >= 4 and e.is_error_type_correct:
                training_data.append({
                    "type": "correct",
                    "error_message": e.error_message,
                    "stack_trace": e.stack_trace,
                    "expected_error_type": e.ai_error_type,
                    "expected_severity": e.ai_severity,
                    "expected_explanation": e.ai_explanation,
                    "expected_suggestions": e.ai_suggestions
                })
            
            # Entries with user corrections
            elif e.user_correction:
                training_data.append({
                    "type": "corrected",
                    "error_message": e.error_message,
                    "stack_trace": e.stack_trace,
                    "ai_error_type": e.ai_error_type,
                    "ai_was_wrong": not e.is_error_type_correct,
                    "user_correction": e.user_correction
                })
        
        return training_data
    
    def export_for_fine_tuning(self, output_path: Optional[Path] = None) -> Path:
        """Export training data in a format suitable for fine-tuning."""
        output_path = output_path or self.storage_path.parent / "training_data.json"
        
        training_data = self.get_training_data()
        
        with open(output_path, 'w') as f:
            json.dump(training_data, f, indent=2)
        
        return output_path


class AccuracyTracker:
    """Tracks AI accuracy metrics over time."""
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path(__file__).parent.parent.parent / "data" / "accuracy_history.jsonl"
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
    
    def record_test_results(self, results: Dict):
        """Record accuracy test results with timestamp."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            **results
        }
        
        with open(self.storage_path, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def get_accuracy_trend(self, metric: str = "overall_accuracy", days: int = 30) -> List[Dict]:
        """Get accuracy trend over time for a specific metric."""
        if not self.storage_path.exists():
            return []
        
        entries = []
        cutoff = datetime.now().timestamp() - (days * 86400)
        
        with open(self.storage_path, 'r') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    entry_time = datetime.fromisoformat(data["timestamp"]).timestamp()
                    if entry_time >= cutoff and metric in data:
                        entries.append({
                            "date": data["timestamp"][:10],
                            "value": data[metric]
                        })
        
        return entries
    
    def get_latest_metrics(self) -> Optional[Dict]:
        """Get the most recent accuracy metrics."""
        if not self.storage_path.exists():
            return None
        
        last_entry = None
        with open(self.storage_path, 'r') as f:
            for line in f:
                if line.strip():
                    last_entry = json.loads(line)
        
        return last_entry


def print_accuracy_report(stats: Dict):
    """Print a formatted accuracy report."""
    print("\n" + "=" * 70)
    print(" 📊 AI Accuracy Report")
    print("=" * 70)
    
    if stats.get("total_feedback", 0) == 0:
        print("\nNo feedback collected yet.")
        print("Start using the analyzer and providing feedback to see metrics.")
        return
    
    print(f"\nTotal feedback entries: {stats['total_feedback']}")
    print(f"Average rating: {stats['avg_rating']:.1f}/5 ⭐")
    
    print("\n📈 Accuracy Metrics:")
    print(f"  Error type accuracy: {stats['error_type_accuracy']:.1%}")
    print(f"  Severity accuracy: {stats['severity_accuracy']:.1%}")
    print(f"  Explanation helpful: {stats['explanation_helpful_rate']:.1%}")
    
    if stats.get("fix_success_rate"):
        print(f"  Fix success rate: {stats['fix_success_rate']:.1%}")
    
    if stats.get("common_issues"):
        print("\n⚠️  Common Misclassifications:")
        for issue, count in stats["common_issues"].items():
            print(f"  {issue}: {count} times")
    
    if stats.get("by_category"):
        print("\n📂 By Category:")
        for cat, data in stats["by_category"].items():
            print(f"  {cat}: {data['accuracy']:.1%} accuracy ({data['count']} entries)")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    # Demo: print current stats
    collector = FeedbackCollector()
    stats = collector.get_feedback_stats()
    print_accuracy_report(stats)
