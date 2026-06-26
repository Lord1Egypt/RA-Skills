#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive test suite for Auto-Create-AI-Team Skill - Generic Version
"""

import os
import sys
import tempfile
import shutil
import subprocess
import unittest


class TestAutoCreateAITeam(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        # Use relative path from test file location
        self.skill_path = os.path.dirname(os.path.abspath(__file__))
        self.create_ai_team_script = os.path.join(self.skill_path, "create_ai_team.py")
        
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
        
    def test_generic_project_single_team(self):
        """Test creating single team for generic project"""
        project_path = os.path.join(self.test_dir, "test-generic-project")
        os.makedirs(project_path)
        
        result = subprocess.run([
            "python3", self.create_ai_team_script,
            "--project-path", project_path,
            "--project-type", "generic",
            "--team-type", "single"
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("AI团队创建成功", result.stdout)
        
        # Check only internal team exists
        ai_team_dir = os.path.join(project_path, "ai-team")
        internal_team = os.path.join(ai_team_dir, "internal-team")
        internet_team = os.path.join(ai_team_dir, "internet-team")
        
        self.assertTrue(os.path.exists(internal_team))
        self.assertFalse(os.path.exists(internet_team))
        
    def test_generic_project_dual_team(self):
        """Test creating dual team for generic project"""
        project_path = os.path.join(self.test_dir, "test-generic-dual-project")
        os.makedirs(project_path)
        
        result = subprocess.run([
            "python3", self.create_ai_team_script,
            "--project-path", project_path,
            "--project-type", "generic",
            "--team-type", "dual"
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("AI团队创建成功", result.stdout)
        
        # Check both teams exist
        ai_team_dir = os.path.join(project_path, "ai-team")
        internal_team = os.path.join(ai_team_dir, "internal-team")
        internet_team = os.path.join(ai_team_dir, "internet-team")
        
        self.assertTrue(os.path.exists(internal_team))
        self.assertTrue(os.path.exists(internet_team))
        
    def test_auto_detection(self):
        """Test automatic project type detection (should default to generic)"""
        generic_project = os.path.join(self.test_dir, "my-generic-project")
        os.makedirs(generic_project)
        
        result = subprocess.run([
            "python3", self.create_ai_team_script,
            "--project-path", generic_project,
            "--auto-detect"
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        # Should detect as generic project and create single team
        
    def test_error_handling_invalid_path(self):
        """Test error handling for invalid project path"""
        invalid_path = "/nonexistent/path"
        
        result = subprocess.run([
            "python3", self.create_ai_team_script,
            "--project-path", invalid_path,
            "--project-type", "generic"
        ], capture_output=True, text=True)
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("错误", result.stdout)
        
    def test_progress_file_creation(self):
        """Test PROJECT_PROGRESS.md file creation"""
        project_path = os.path.join(self.test_dir, "test-progress-project")
        os.makedirs(project_path)
        
        subprocess.run([
            "python3", self.create_ai_team_script,
            "--project-path", project_path,
            "--project-type", "generic",
            "--team-type", "dual"
        ], capture_output=True, text=True)
        
        progress_file = os.path.join(project_path, "ai-team", "PROJECT_PROGRESS.md")
        self.assertTrue(os.path.exists(progress_file))
        
        # Check content
        with open(progress_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("项目进展概览", content)

if __name__ == '__main__':
    unittest.main()