"""Tests for the feature extractor."""

import pytest
from agent_memory.routing.feature_extractor import TaskFeatureExtractor


class TestFeatureExtractor:
    def setup_method(self):
        self.extractor = TaskFeatureExtractor()

    def test_knowledge_query(self):
        features = self.extractor.extract("How do I optimize a SQL query?")
        assert features.requires_knowledge is True
        assert features.domain == "database"

    def test_complex_query(self):
        features = self.extractor.extract(
            "First, collect the data from the API. Then, clean it. After that, build a model. "
            "Additionally, evaluate the results and also write a report."
        )
        assert features.is_complex is True

    def test_simple_query(self):
        features = self.extractor.extract("Fix the login bug")
        assert features.is_complex is False
        assert features.task_type == "debugging"

    def test_domain_detection_ml(self):
        features = self.extractor.extract("Train a machine learning model for prediction")
        assert features.domain == "ml"

    def test_domain_detection_web(self):
        features = self.extractor.extract("Build a React frontend component")
        assert features.domain == "web"

    def test_task_type_implementation(self):
        features = self.extractor.extract("Implement a new feature for user authentication")
        assert features.task_type == "implementation"

    def test_task_type_analysis(self):
        features = self.extractor.extract("Analyze the performance of the system")
        assert features.task_type == "analysis"

    def test_has_history_with_context(self):
        features = self.extractor.extract(
            "Continue working on the report",
            context={"continuation": True, "active_tasks": ["task_1"]},
        )
        assert features.has_history is True

    def test_keywords_extraction(self):
        features = self.extractor.extract("How to optimize database query performance")
        assert "optimize" in features.keywords
        assert "database" in features.keywords
        assert "query" in features.keywords
