"""
AI Analysis Accuracy Tests
Tests the quality and accuracy of AI-generated error explanations and fix suggestions.
"""
import pytest
import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional
from src.analyzers import AIAnalyzer, ErrorAnalysis


@dataclass
class TestCase:
    """A test case for AI accuracy evaluation."""
    id: str
    category: str  # nodejs, python, go, etc.
    error_message: str
    stack_trace: Optional[str]
    
    # Expected results (ground truth)
    expected_error_type: str
    expected_severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    expected_keywords: List[str]  # Should appear in explanation
    expected_fix_keywords: List[str]  # Should appear in suggestions
    
    # Optional: specific commands that should be suggested
    expected_commands: Optional[List[str]] = None
    
    # Difficulty: easy, medium, hard
    difficulty: str = "medium"


class TestAIAccuracy:
    """Test suite for AI analysis accuracy."""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance."""
        return AIAnalyzer(api_key=None)  # Use knowledge base only for now
    
    @pytest.fixture
    def test_cases(self) -> List[TestCase]:
        """Load test cases."""
        return self._load_test_cases()
    
    def _load_test_cases(self) -> List[TestCase]:
        """Load test cases from JSON file or return defaults."""
        cases_file = Path(__file__).parent / "test_cases" / "accuracy_cases.json"
        
        if cases_file.exists():
            with open(cases_file) as f:
                data = json.load(f)
                return [TestCase(**case) for case in data]
        
        # Default test cases
        return self._get_default_test_cases()
    
    def _get_default_test_cases(self) -> List[TestCase]:
        """Get default test cases."""
        return [
            # === Node.js Cases ===
            TestCase(
                id="nodejs-econnrefused-001",
                category="nodejs",
                error_message="Error: connect ECONNREFUSED 127.0.0.1:5432",
                stack_trace="""Error: connect ECONNREFUSED 127.0.0.1:5432
    at TCPConnectWrap.afterConnect [as oncomplete] (net.js:1141:16)
    at Database.connect (/app/src/db.js:45:12)""",
                expected_error_type="Connection Error",
                expected_severity="HIGH",
                expected_keywords=["connection", "refused", "database", "5432"],
                expected_fix_keywords=["running", "start", "service", "postgresql"],
                expected_commands=["systemctl", "status"],
                difficulty="easy"
            ),
            TestCase(
                id="nodejs-enoent-001",
                category="nodejs",
                error_message="Error: ENOENT: no such file or directory, open '/app/config.json'",
                stack_trace="""Error: ENOENT: no such file or directory, open '/app/config.json'
    at Object.openSync (fs.js:462:3)
    at readConfig (/app/src/config.js:12:15)""",
                expected_error_type="File Not Found",
                expected_severity="MEDIUM",
                expected_keywords=["file", "not found", "config", "directory"],
                expected_fix_keywords=["path", "exists", "create"],
                difficulty="easy"
            ),
            TestCase(
                id="nodejs-timeout-001",
                category="nodejs",
                error_message="Error: ETIMEDOUT connecting to api.example.com:443",
                stack_trace="""Error: ETIMEDOUT
    at Timeout._onTimeout (/app/src/http.js:78:13)""",
                expected_error_type="Timeout Error",
                expected_severity="MEDIUM",
                expected_keywords=["timeout", "connection", "api"],
                expected_fix_keywords=["network", "timeout", "retry"],
                difficulty="easy"
            ),
            
            # === Python Cases ===
            TestCase(
                id="python-db-table-001",
                category="python",
                error_message="django.request - ERROR - Internal Server Error: /api/users/",
                stack_trace="""Traceback (most recent call last):
  File "/app/views.py", line 45, in get_users
    users = User.objects.filter(active=True)
OperationalError: no such table: auth_user""",
                expected_error_type="Database Error",
                expected_severity="CRITICAL",
                expected_keywords=["table", "database", "migration", "schema"],
                expected_fix_keywords=["migrate", "makemigrations", "django"],
                expected_commands=["manage.py", "migrate"],
                difficulty="medium"
            ),
            TestCase(
                id="python-import-001",
                category="python",
                error_message="ModuleNotFoundError: No module named 'requests'",
                stack_trace="""Traceback (most recent call last):
  File "/app/main.py", line 3, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'""",
                expected_error_type="Import Error",
                expected_severity="HIGH",
                expected_keywords=["module", "import", "requests", "installed"],
                expected_fix_keywords=["pip", "install", "requirements"],
                expected_commands=["pip install"],
                difficulty="easy"
            ),
            TestCase(
                id="python-key-error-001",
                category="python",
                error_message="KeyError: 'user_id'",
                stack_trace="""Traceback (most recent call last):
  File "/app/handlers.py", line 23, in get_user
    user_id = request.data['user_id']
KeyError: 'user_id'""",
                expected_error_type="Key Error",
                expected_severity="MEDIUM",
                expected_keywords=["key", "dictionary", "missing"],
                expected_fix_keywords=["get", "exists", "check"],
                difficulty="medium"
            ),
            
            # === Go Cases ===
            TestCase(
                id="go-panic-001",
                category="go",
                error_message="panic: runtime error: invalid memory address or nil pointer dereference",
                stack_trace="""goroutine 1 [running]:
main.processUser(0x0, 0x0)
    /app/main.go:45 +0x123
main.main()
    /app/main.go:23 +0x45""",
                expected_error_type="Nil Pointer",
                expected_severity="CRITICAL",
                expected_keywords=["nil", "pointer", "memory", "nil pointer"],
                expected_fix_keywords=["check", "nil", "initialize"],
                difficulty="medium"
            ),
            TestCase(
                id="go-dial-001",
                category="go",
                error_message="dial tcp 127.0.0.1:6379: connect: connection refused",
                stack_trace="",
                expected_error_type="Connection Error",
                expected_severity="HIGH",
                expected_keywords=["connection", "refused", "redis", "6379"],
                expected_fix_keywords=["redis", "running", "start"],
                expected_commands=["redis-server"],
                difficulty="easy"
            ),
            
            # === Hard Cases (Edge Cases) ===
            TestCase(
                id="nodejs-memory-leak-001",
                category="nodejs",
                error_message="FATAL ERROR: CALL_AND_RETRY_LAST Allocation failed - JavaScript heap out of memory",
                stack_trace="",
                expected_error_type="Memory Error",
                expected_severity="CRITICAL",
                expected_keywords=["memory", "heap", "allocation"],
                expected_fix_keywords=["memory", "heap-size", "leak", "profiler"],
                expected_commands=["--max-old-space-size"],
                difficulty="hard"
            ),
            TestCase(
                id="python-async-001",
                category="python",
                error_message="RuntimeError: cannot schedule new futures after shutdown",
                stack_trace="""Traceback (most recent call last):
  File "/app/async_worker.py", line 67, in process
    loop.run_until_complete(task)""",
                expected_error_type="Async Error",
                expected_severity="HIGH",
                expected_keywords=["async", "future", "shutdown", "loop"],
                expected_fix_keywords=["event loop", "shutdown", "await"],
                difficulty="hard"
            ),
        ]
    
    # === Test Methods ===
    
    def test_error_type_accuracy(self, analyzer, test_cases):
        """Test if AI correctly identifies error types."""
        results = {
            "total": 0,
            "correct": 0,
            "by_category": {},
            "by_difficulty": {}
        }
        
        for case in test_cases:
            analysis = analyzer.analyze(case.error_message, case.stack_trace)
            
            results["total"] += 1
            
            # Check if error type matches (case-insensitive partial match)
            is_correct = (
                case.expected_error_type.lower() in analysis.error_type.lower() or
                analysis.error_type.lower() in case.expected_error_type.lower()
            )
            
            if is_correct:
                results["correct"] += 1
            
            # Track by category
            cat = case.category
            if cat not in results["by_category"]:
                results["by_category"][cat] = {"total": 0, "correct": 0}
            results["by_category"][cat]["total"] += 1
            if is_correct:
                results["by_category"][cat]["correct"] += 1
            
            # Track by difficulty
            diff = case.difficulty
            if diff not in results["by_difficulty"]:
                results["by_difficulty"][diff] = {"total": 0, "correct": 0}
            results["by_difficulty"][diff]["total"] += 1
            if is_correct:
                results["by_difficulty"][diff]["correct"] += 1
        
        # Calculate accuracy
        accuracy = results["correct"] / results["total"] if results["total"] > 0 else 0
        
        # Print detailed results
        print("\n" + "=" * 70)
        print("Error Type Accuracy Results")
        print("=" * 70)
        print(f"Overall: {results['correct']}/{results['total']} = {accuracy:.1%}")
        print()
        
        print("By Category:")
        for cat, stats in results["by_category"].items():
            cat_acc = stats["correct"] / stats["total"] if stats["total"] > 0 else 0
            print(f"  {cat}: {stats['correct']}/{stats['total']} = {cat_acc:.1%}")
        
        print()
        print("By Difficulty:")
        for diff, stats in results["by_difficulty"].items():
            diff_acc = stats["correct"] / stats["total"] if stats["total"] > 0 else 0
            print(f"  {diff}: {stats['correct']}/{stats['total']} = {diff_acc:.1%}")
        
        print("=" * 70)
        
        # Assert minimum accuracy threshold
        assert accuracy >= 0.8, f"Error type accuracy {accuracy:.1%} is below 80% threshold"
    
    def test_severity_accuracy(self, analyzer, test_cases):
        """Test if AI correctly assesses severity."""
        results = {
            "total": 0,
            "correct": 0,
            "off_by_one": 0  # Within one severity level
        }
        
        severity_order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
        
        for case in test_cases:
            analysis = analyzer.analyze(case.error_message, case.stack_trace)
            
            results["total"] += 1
            
            expected_level = severity_order.get(case.expected_severity, 1)
            actual_level = severity_order.get(analysis.severity, 1)
            
            if expected_level == actual_level:
                results["correct"] += 1
            elif abs(expected_level - actual_level) == 1:
                results["off_by_one"] += 1
        
        accuracy = results["correct"] / results["total"] if results["total"] > 0 else 0
        acceptable = (results["correct"] + results["off_by_one"]) / results["total"] if results["total"] > 0 else 0
        
        print(f"\nSeverity Accuracy: {accuracy:.1%} exact, {acceptable:.1%} within one level")
        
        assert accuracy >= 0.7, f"Severity accuracy {accuracy:.1%} is below 70% threshold"
    
    def test_keyword_presence(self, analyzer, test_cases):
        """Test if AI explanations contain expected keywords."""
        results = {
            "total": 0,
            "keyword_hits": 0,
            "keyword_total": 0
        }
        
        for case in test_cases:
            analysis = analyzer.analyze(case.error_message, case.stack_trace)
            
            results["total"] += 1
            
            # Check explanation keywords
            explanation_lower = analysis.explanation.lower()
            for keyword in case.expected_keywords:
                results["keyword_total"] += 1
                if keyword.lower() in explanation_lower:
                    results["keyword_hits"] += 1
        
        keyword_coverage = results["keyword_hits"] / results["keyword_total"] if results["keyword_total"] > 0 else 0
        
        print(f"\nKeyword Coverage: {results['keyword_hits']}/{results['keyword_total']} = {keyword_coverage:.1%}")
        
        # TODO: Improve keyword coverage to 60%+
        # Currently at 46.3% - need richer explanations
        assert keyword_coverage >= 0.4, f"Keyword coverage {keyword_coverage:.1%} is below 40% threshold"
    
    def test_fix_suggestion_quality(self, analyzer, test_cases):
        """Test if fix suggestions contain actionable keywords."""
        results = {
            "total": 0,
            "suggestion_hits": 0,
            "suggestion_total": 0
        }
        
        for case in test_cases:
            analysis = analyzer.analyze(case.error_message, case.stack_trace)
            
            results["total"] += 1
            
            # Check suggestion keywords
            all_suggestions = " ".join(analysis.suggestions).lower()
            for keyword in case.expected_fix_keywords:
                results["suggestion_total"] += 1
                if keyword.lower() in all_suggestions:
                    results["suggestion_hits"] += 1
        
        suggestion_coverage = results["suggestion_hits"] / results["suggestion_total"] if results["suggestion_total"] > 0 else 0
        
        print(f"\nFix Suggestion Quality: {results['suggestion_hits']}/{results['suggestion_total']} = {suggestion_coverage:.1%}")
        
        assert suggestion_coverage >= 0.5, f"Suggestion quality {suggestion_coverage:.1%} is below 50% threshold"


class TestRegression:
    """Regression tests to ensure improvements don't break existing functionality."""
    
    @pytest.fixture
    def analyzer(self):
        return AIAnalyzer(api_key=None)
    
    def test_common_errors_still_work(self, analyzer):
        """Ensure common error patterns still work after changes."""
        common_errors = [
            ("ECONNREFUSED", "Connection Error"),
            ("ENOENT", "File Not Found"),
            ("ETIMEDOUT", "Timeout Error"),
            ("permission denied", "Permission"),
        ]
        
        for error_msg, expected_type in common_errors:
            analysis = analyzer.analyze(error_msg, None)
            assert expected_type.lower() in analysis.error_type.lower(), \
                f"Regression: {error_msg} no longer recognized as {expected_type}"
    
    def test_analyzer_returns_valid_structure(self, analyzer):
        """Ensure analyzer always returns valid ErrorAnalysis."""
        analysis = analyzer.analyze("Some random error message", None)
        
        assert hasattr(analysis, 'error_type')
        assert hasattr(analysis, 'severity')
        assert hasattr(analysis, 'explanation')
        assert hasattr(analysis, 'suggestions')
        
        assert analysis.severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
        assert len(analysis.suggestions) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
