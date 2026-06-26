#!/usr/bin/env python3
"""
Test suite for the Feishu Integration Solver skill.
This script validates the skill's ability to handle various Feishu integration scenarios.
"""

import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock

# Add the skill directory to Python path
skill_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, skill_dir)

try:
    from solve_feishu_integration import (
        FeishuIntegrationSolver,
        AuthenticationError,
        APIError,
        ConfigurationError
    )
except ImportError as e:
    print(f"Failed to import solver: {e}")
    sys.exit(1)


class TestFeishuIntegrationSolver(unittest.TestCase):
    """Test cases for Feishu Integration Solver."""

    def setUp(self):
        """Set up test fixtures."""
        self.solver = FeishuIntegrationSolver()
        
    def test_initialization(self):
        """Test solver initialization."""
        self.assertIsNotNone(self.solver)
        self.assertEqual(self.solver.integration_type, "auto")
        self.assertFalse(self.solver.use_webhook)
        
    def test_parse_problem_simple(self):
        """Test parsing simple integration problems."""
        problem = "I need to send messages to Feishu chat"
        result = self.solver.parse_problem(problem)
        self.assertIn("message", result['required_capabilities'])
        self.assertIn("chat", result['required_capabilities'])
        
    def test_parse_problem_complex(self):
        """Test parsing complex integration problems."""
        problem = "I want to create a bot that monitors documents and sends notifications when they are updated"
        result = self.solver.parse_problem(problem)
        self.assertIn("document", result['required_capabilities'])
        self.assertIn("notification", result['required_capabilities'])
        self.assertIn("monitoring", result['required_capabilities'])
        
    def test_determine_integration_type_bot(self):
        """Test determining integration type for bot scenarios."""
        capabilities = ["message", "chat", "bot"]
        integration_type = self.solver.determine_integration_type(capabilities)
        self.assertEqual(integration_type, "bot")
        
    def test_determine_integration_type_api(self):
        """Test determining integration type for API scenarios."""
        capabilities = ["document", "user", "department"]
        integration_type = self.solver.determine_integration_type(capabilities)
        self.assertEqual(integration_type, "api")
        
    def test_determine_integration_type_webhook(self):
        """Test determining integration type for webhook scenarios."""
        capabilities = ["event", "notification", "realtime"]
        integration_type = self.solver.determine_integration_type(capabilities)
        self.assertEqual(integration_type, "webhook")
        
    @patch('solve_feishu_integration.requests.post')
    def test_get_tenant_access_token_success(self, mock_post):
        """Test successful tenant access token retrieval."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'tenant_access_token': 'test_token',
            'expire': 7200
        }
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        token = self.solver.get_tenant_access_token("test_app_id", "test_app_secret")
        self.assertEqual(token, "test_token")
        mock_post.assert_called_once()
        
    @patch('solve_feishu_integration.requests.post')
    def test_get_tenant_access_token_failure(self, mock_post):
        """Test failed tenant access token retrieval."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'code': 99991663,
            'msg': 'Invalid app credentials'
        }
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        
        with self.assertRaises(AuthenticationError):
            self.solver.get_tenant_access_token("invalid_app_id", "invalid_app_secret")
            
    def test_generate_bot_solution(self):
        """Test generating bot integration solution."""
        config = {
            'app_id': 'cli_xxx',
            'app_secret': 'xxx',
            'verification_token': 'xxx'
        }
        solution = self.solver.generate_bot_solution(config)
        self.assertIn('code', solution)
        self.assertIn('python', solution['code'].lower())
        self.assertIn('app_id', solution['code'])
        self.assertIn('app_secret', solution['code'])
        
    def test_generate_api_solution(self):
        """Test generating API integration solution."""
        config = {
            'app_id': 'cli_xxx',
            'app_secret': 'xxx'
        }
        solution = self.solver.generate_api_solution(config)
        self.assertIn('code', solution)
        self.assertIn('tenant_access_token', solution['code'])
        self.assertIn('send_message', solution['code'])
        
    def test_generate_webhook_solution(self):
        """Test generating webhook integration solution."""
        config = {
            'app_id': 'cli_xxx',
            'app_secret': 'xxx',
            'verification_token': 'xxx'
        }
        solution = self.solver.generate_webhook_solution(config)
        self.assertIn('code', solution)
        self.assertIn('webhook', solution['code'].lower())
        self.assertIn('event', solution['code'])
        
    def test_generate_fallback_solution(self):
        """Test generating fallback solution for unsupported scenarios."""
        problem = "I need to integrate with Feishu using SOAP protocol"
        solution = self.solver.generate_fallback_solution(problem)
        self.assertIn('manual', solution['approach'])
        self.assertIn('documentation', solution['resources'])
        self.assertIn('community', solution['resources'])
        
    def test_validate_configuration_complete(self):
        """Test validating complete configuration."""
        config = {
            'app_id': 'cli_xxx',
            'app_secret': 'xxx',
            'verification_token': 'xxx'
        }
        is_valid, missing = self.solver.validate_configuration(config)
        self.assertTrue(is_valid)
        self.assertEqual(missing, [])
        
    def test_validate_configuration_incomplete(self):
        """Test validating incomplete configuration."""
        config = {
            'app_id': 'cli_xxx'
        }
        is_valid, missing = self.solver.validate_configuration(config)
        self.assertFalse(is_valid)
        self.assertIn('app_secret', missing)
        
    def test_end_to_end_simple_problem(self):
        """Test end-to-end solution for a simple problem."""
        problem = "Send a message to Feishu chat"
        config = {
            'app_id': 'cli_xxx',
            'app_secret': 'xxx'
        }
        
        with patch.object(self.solver, 'get_tenant_access_token') as mock_token:
            mock_token.return_value = 'test_token'
            solution = self.solver.solve(problem, config)
            
        self.assertIn('solution', solution)
        self.assertIn('code', solution['solution'])
        self.assertIn('explanation', solution['solution'])
        self.assertEqual(solution['status'], 'success')
        
    def test_end_to_end_unsupported_problem(self):
        """Test end-to-end solution for an unsupported problem."""
        problem = "Integrate Feishu with legacy COBOL system"
        config = {}
        
        solution = self.solver.solve(problem, config)
        self.assertEqual(solution['status'], 'partial')
        self.assertIn('fallback', solution['approach'])


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)