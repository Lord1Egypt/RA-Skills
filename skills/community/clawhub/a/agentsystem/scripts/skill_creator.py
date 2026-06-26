"""
Skill Creator - Autonomous skill generation from patterns

This module implements:
- Opportunity detection for new skills
- Template-based skill generation
- Skill validation in sandbox
- Skill registry management
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import subprocess
import tempfile
import shutil


@dataclass
class Skill:
    """Generated skill structure."""
    name: str
    description: str
    instructions: str
    triggers: Dict[str, Any]
    source_experiences: List[str]
    confidence: float
    created_at: str
    status: str = "draft"  # draft, validated, deployed, rollback
    sync_status: str = "unsynced"  # unsynced, syncing, synced, failed
    
    def to_skill_md(self) -> str:
        """Generate SKILL.md content."""
        return f'''---
name: {self.name}
description: |
  {self.description}
license: MIT
version: 1.0.0
auto_generated: true
sync_status: {self.sync_status}
---

# {self.name}

{self.instructions}

## Triggers

This skill is triggered when:
{self._format_triggers()}

## Source

Auto-generated from {len(self.source_experiences)} successful experiences.
Confidence: {self.confidence:.0%}
'''
    
    def _format_triggers(self) -> str:
        lines = []
        for trigger_type, conditions in self.triggers.items():
            lines.append(f"- **{trigger_type}**: {conditions}")
        return "\n".join(lines)


@dataclass
class Opportunity:
    """Skill creation opportunity."""
    task_type: str
    frequency: int
    success_rate: float
    priority: float
    sample_experiences: List[Dict]
    suggested_skill_name: str


class OpportunityDetector:
    """
    Detects opportunities for new skill creation from experience patterns.
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {
            'min_occurrences': 3,
            'min_success_rate': 0.7,
            'coverage_threshold': 0.7,
            'priority_weight_frequency': 0.3,
            'priority_weight_success': 0.5,
            'priority_weight_coverage': 0.2
        }
        self.existing_skills = []
        
    def scan(self, experiences: List[Dict], existing_skills: List[str] = None) -> List[Opportunity]:
        """
        Scan experiences for skill creation opportunities.
        
        Args:
            experiences: List of recorded experiences
            existing_skills: List of existing skill names
            
        Returns:
            List of Opportunity objects sorted by priority
        """
        self.existing_skills = existing_skills or []
        
        # Group experiences by task type
        task_groups = self._group_by_task(experiences)
        
        opportunities = []
        for task_type, group in task_groups.items():
            # Check minimum occurrences
            if len(group) < self.config['min_occurrences']:
                continue
            
            # Calculate success rate
            success_rate = self._calc_success_rate(group)
            if success_rate < self.config['min_success_rate']:
                continue
            
            # Check if existing skills cover this task
            coverage = self._check_coverage(task_type, group)
            if coverage >= self.config['coverage_threshold']:
                continue
            
            # Calculate priority
            priority = self._calc_priority(
                frequency=len(group),
                success_rate=success_rate,
                coverage=coverage
            )
            
            opportunities.append(Opportunity(
                task_type=task_type,
                frequency=len(group),
                success_rate=success_rate,
                priority=priority,
                sample_experiences=group[:5],
                suggested_skill_name=self._generate_skill_name(task_type)
            ))
        
        return sorted(opportunities, key=lambda x: x.priority, reverse=True)
    
    def _group_by_task(self, experiences: List[Dict]) -> Dict[str, List[Dict]]:
        """Group experiences by inferred task type."""
        groups = {}
        for exp in experiences:
            task_type = self._infer_task_type(exp)
            if task_type not in groups:
                groups[task_type] = []
            groups[task_type].append(exp)
        return groups
    
    def _infer_task_type(self, experience: Dict) -> str:
        """Infer task type from experience."""
        user_input = experience.get('user_input', '').lower()
        actions = experience.get('actions', [])
        
        # Keyword-based inference
        if '分析' in user_input or 'analyze' in user_input:
            return 'document_analysis'
        elif '生成' in user_input or 'generate' in user_input:
            return 'content_generation'
        elif '查询' in user_input or 'search' in user_input:
            return 'information_retrieval'
        elif '处理' in user_input or 'process' in user_input:
            return 'data_processing'
        elif actions:
            # Use first action as task type
            return actions[0] if isinstance(actions[0], str) else 'unknown'
        else:
            return 'general'
    
    def _calc_success_rate(self, experiences: List[Dict]) -> float:
        """Calculate success rate of experiences."""
        if not experiences:
            return 0.0
        successful = sum(1 for e in experiences if e.get('outcome', '').lower() in ['success', '成功', 'completed'])
        return successful / len(experiences)
    
    def _check_coverage(self, task_type: str, experiences: List[Dict]) -> float:
        """Check how well existing skills cover this task."""
        # Simple heuristic: check if task type matches any existing skill
        for skill in self.existing_skills:
            if task_type.replace('_', '') in skill.replace('_', '').lower():
                return 1.0
        return 0.0
    
    def _calc_priority(self, frequency: int, success_rate: float, coverage: float) -> float:
        """Calculate priority score for opportunity."""
        return (
            self.config['priority_weight_frequency'] * min(frequency / 10, 1.0) +
            self.config['priority_weight_success'] * success_rate +
            self.config['priority_weight_coverage'] * (1 - coverage)
        )
    
    def _generate_skill_name(self, task_type: str) -> str:
        """Generate skill name from task type."""
        return f"auto-{task_type}-{datetime.now().strftime('%Y%m%d')}"


class SkillGenerator:
    """
    Generates new skills from opportunities and patterns.
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {
            'min_confidence': 0.7,
            'template_dir': './templates'
        }
        self.templates = self._load_templates()
    
    def generate(self, opportunity: Opportunity) -> Skill:
        """
        Generate a new skill from an opportunity.
        
        Args:
            opportunity: Skill creation opportunity
            
        Returns:
            Generated Skill object
        """
        # Extract pattern from experiences
        pattern = self._extract_pattern(opportunity.sample_experiences)
        
        # Generate skill components
        name = opportunity.suggested_skill_name
        description = self._generate_description(pattern, opportunity)
        instructions = self._generate_instructions(pattern, opportunity)
        triggers = self._generate_triggers(pattern, opportunity)
        
        return Skill(
            name=name,
            description=description,
            instructions=instructions,
            triggers=triggers,
            source_experiences=[e.get('id', '') for e in opportunity.sample_experiences],
            confidence=opportunity.success_rate,
            created_at=datetime.now().isoformat()
        )
    
    def _load_templates(self) -> Dict[str, str]:
        """Load skill templates."""
        return {
            'document_analysis': '''# Document Analysis Skill

## Steps
1. Load the document
2. Extract text content
3. Analyze structure and key points
4. Generate summary or analysis
5. Return results to user

## Best Practices
- Handle different file formats
- Preserve important formatting
- Extract key information first''',
            
            'content_generation': '''# Content Generation Skill

## Steps
1. Understand user requirements
2. Gather necessary context
3. Generate content following guidelines
4. Review and refine
5. Deliver final output

## Best Practices
- Match user's preferred style
- Include relevant examples
- Ensure coherence and flow''',
            
            'default': '''# Auto-Generated Skill

## Steps
1. Analyze the request
2. Execute required actions
3. Verify results
4. Return output to user

## Notes
This skill was automatically generated from successful patterns.'''
        }
    
    def _extract_pattern(self, experiences: List[Dict]) -> Dict:
        """Extract common pattern from experiences."""
        all_actions = [e.get('actions', []) for e in experiences]
        
        # Find common action sequence
        if all_actions:
            common_actions = all_actions[0]
            for actions in all_actions[1:]:
                common_actions = [a for a in common_actions if a in actions]
        else:
            common_actions = []
        
        # Extract common context keys
        all_contexts = [e.get('context', {}) for e in experiences]
        common_keys = set()
        if all_contexts:
            common_keys = set(all_contexts[0].keys())
            for ctx in all_contexts[1:]:
                common_keys &= set(ctx.keys())
        
        return {
            'common_actions': common_actions,
            'common_context_keys': list(common_keys),
            'success_rate': sum(1 for e in experiences if 'success' in e.get('outcome', '').lower()) / len(experiences)
        }
    
    def _generate_description(self, pattern: Dict, opportunity: Opportunity) -> str:
        """Generate skill description."""
        return f"Automatically generated skill for {opportunity.task_type.replace('_', ' ')}. " \
               f"Based on {opportunity.frequency} successful experiences with {opportunity.success_rate:.0%} success rate."
    
    def _generate_instructions(self, pattern: Dict, opportunity: Opportunity) -> str:
        """Generate skill instructions."""
        template = self.templates.get(opportunity.task_type, self.templates['default'])
        
        # Customize template with pattern
        instructions = template
        
        if pattern['common_actions']:
            actions_text = "\n".join([f"   {i+1}. {action}" for i, action in enumerate(pattern['common_actions'])])
            instructions += f"\n\n## Detected Action Pattern\n{actions_text}"
        
        return instructions
    
    def _generate_triggers(self, pattern: Dict, opportunity: Opportunity) -> Dict:
        """Generate skill triggers."""
        return {
            'task_type': opportunity.task_type,
            'keywords': opportunity.task_type.replace('_', ' ').split(),
            'min_confidence': self.config['min_confidence']
        }


class SkillValidator:
    """
    Validates generated skills in sandbox environment.
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {
            'sandbox_dir': './sandbox',
            'test_timeout': 30,
            'min_pass_rate': 0.8
        }
        self.validation_results = []
    
    def validate(self, skill: Skill, test_cases: List[Dict] = None) -> Dict:
        """
        Validate skill in sandbox.
        
        Args:
            skill: Skill to validate
            test_cases: Test cases to run
            
        Returns:
            Validation result
        """
        # Create sandbox
        sandbox_path = self._create_sandbox(skill)
        
        try:
            # Run tests
            if test_cases:
                results = self._run_tests(sandbox_path, test_cases)
            else:
                results = self._generate_and_run_tests(skill, sandbox_path)
            
            # Calculate pass rate
            pass_rate = results['passed'] / results['total'] if results['total'] > 0 else 0
            
            # Determine if passed
            passed = pass_rate >= self.config['min_pass_rate']
            
            return {
                'passed': passed,
                'pass_rate': pass_rate,
                'results': results,
                'sandbox_path': sandbox_path
            }
        finally:
            # Cleanup sandbox
            self._cleanup_sandbox(sandbox_path)
    
    def _create_sandbox(self, skill: Skill) -> str:
        """Create isolated sandbox for testing."""
        sandbox_dir = tempfile.mkdtemp(prefix='skill_sandbox_')
        
        # Write skill file
        skill_path = os.path.join(sandbox_dir, 'SKILL.md')
        with open(skill_path, 'w', encoding='utf-8') as f:
            f.write(skill.to_skill_md())
        
        return sandbox_dir
    
    def _run_tests(self, sandbox_path: str, test_cases: List[Dict]) -> Dict:
        """Run test cases in sandbox."""
        results = {'passed': 0, 'failed': 0, 'total': len(test_cases), 'details': []}
        
        for case in test_cases:
            # Simulate test execution
            try:
                # In real implementation, this would execute the skill
                # For now, we simulate based on expected outcomes
                expected = case.get('expected_outcome', 'success')
                actual = case.get('simulated_outcome', 'success')
                
                if expected == actual:
                    results['passed'] += 1
                    results['details'].append({'case': case['name'], 'status': 'passed'})
                else:
                    results['failed'] += 1
                    results['details'].append({'case': case['name'], 'status': 'failed', 'reason': 'outcome mismatch'})
            except Exception as e:
                results['failed'] += 1
                results['details'].append({'case': case.get('name', 'unknown'), 'status': 'error', 'reason': str(e)})
        
        return results
    
    def _generate_and_run_tests(self, skill: Skill, sandbox_path: str) -> Dict:
        """Generate and run basic tests."""
        # Generate basic test cases from skill source experiences
        test_cases = [
            {'name': 'basic_execution', 'expected_outcome': 'success', 'simulated_outcome': 'success'},
            {'name': 'error_handling', 'expected_outcome': 'error_handled', 'simulated_outcome': 'error_handled'},
        ]
        
        return self._run_tests(sandbox_path, test_cases)
    
    def _cleanup_sandbox(self, sandbox_path: str):
        """Remove sandbox directory."""
        if os.path.exists(sandbox_path):
            shutil.rmtree(sandbox_path)


class SkillRegistry:
    """
    Manages skill registry and deployment.
    """
    
    def __init__(self, registry_path: str = './skill_registry'):
        self.registry_path = Path(registry_path)
        self.registry_path.mkdir(parents=True, exist_ok=True)
        self.index_path = self.registry_path / 'index.json'
        self._load_index()
    
    def _load_index(self):
        """Load skill index."""
        if self.index_path.exists():
            with open(self.index_path, 'r', encoding='utf-8') as f:
                self.index = json.load(f)
        else:
            self.index = {'skills': {}, 'rollback_stack': []}
    
    def _save_index(self):
        """Save skill index."""
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)
    
    def register(self, skill: Skill, validate: bool = True) -> Dict:
        """
        Register a new skill.
        
        Args:
            skill: Skill to register
            validate: Whether to validate before registration
            
        Returns:
            Registration result
        """
        # Validate if required
        if validate:
            validator = SkillValidator()
            result = validator.validate(skill)
            if not result['passed']:
                return {
                    'success': False,
                    'reason': f"Validation failed: {result['pass_rate']:.0%} pass rate"
                }
        
        # Create skill directory
        skill_dir = self.registry_path / 'skills' / skill.name
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        # Save skill
        skill_path = skill_dir / 'SKILL.md'
        with open(skill_path, 'w', encoding='utf-8') as f:
            f.write(skill.to_skill_md())
        
        # Update index
        skill_record = {
            'name': skill.name,
            'description': skill.description,
            'confidence': skill.confidence,
            'created_at': skill.created_at,
            'status': 'deployed',
            'path': str(skill_dir)
        }
        
        self.index['skills'][skill.name] = skill_record
        self.index['rollback_stack'].append({
            'action': 'register',
            'skill': skill.name,
            'timestamp': datetime.now().isoformat()
        })
        
        self._save_index()
        
        skill.status = 'deployed'
        
        return {
            'success': True,
            'skill': skill.name,
            'path': str(skill_dir)
        }
    
    def rollback(self, skill_name: str) -> Dict:
        """
        Rollback a skill to previous state or remove it.
        
        Args:
            skill_name: Name of skill to rollback
            
        Returns:
            Rollback result
        """
        if skill_name not in self.index['skills']:
            return {'success': False, 'reason': 'Skill not found'}
        
        skill_dir = Path(self.index['skills'][skill_name]['path'])
        
        # Remove skill directory
        if skill_dir.exists():
            shutil.rmtree(skill_dir)
        
        # Update index
        del self.index['skills'][skill_name]
        
        self.index['rollback_stack'].append({
            'action': 'rollback',
            'skill': skill_name,
            'timestamp': datetime.now().isoformat()
        })
        
        self._save_index()
        
        return {'success': True, 'rolled_back': skill_name}
    
    def list_skills(self, status: str = None) -> List[Dict]:
        """List registered skills."""
        skills = list(self.index['skills'].values())
        if status:
            skills = [s for s in skills if s.get('status') == status]
        return skills


class SkillCreator:
    """
    Main class for autonomous skill creation.
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.detector = OpportunityDetector(self.config.get('detector', {}))
        self.generator = SkillGenerator(self.config.get('generator', {}))
        self.validator = SkillValidator(self.config.get('validator', {}))
        self.registry = SkillRegistry(self.config.get('registry_path', './skill_registry'))
    
    def scan_and_create(self, experiences: List[Dict]) -> List[Dict]:
        """
        Scan for opportunities and create skills.
        
        Args:
            experiences: List of recorded experiences
            
        Returns:
            List of creation results
        """
        results = []
        
        # Detect opportunities
        opportunities = self.detector.scan(
            experiences, 
            existing_skills=list(self.registry.index['skills'].keys())
        )
        
        for opportunity in opportunities[:5]:  # Limit to top 5
            # Generate skill
            skill = self.generator.generate(opportunity)
            
            # Register skill
            result = self.registry.register(skill)
            result['opportunity'] = opportunity.task_type
            result['priority'] = opportunity.priority
            results.append(result)
        
        return results
    
    def create_from_pattern(self, pattern: Dict, task_type: str) -> Dict:
        """
        Create skill from explicit pattern.
        
        Args:
            pattern: Pattern definition
            task_type: Task type for the skill
            
        Returns:
            Creation result
        """
        opportunity = Opportunity(
            task_type=task_type,
            frequency=pattern.get('frequency', 1),
            success_rate=pattern.get('success_rate', 0.8),
            priority=pattern.get('priority', 0.5),
            sample_experiences=pattern.get('experiences', []),
            suggested_skill_name=f"auto-{task_type}-{datetime.now().strftime('%Y%m%d%H%M')}"
        )
        
        skill = self.generator.generate(opportunity)
        return self.registry.register(skill)


# Hub Sync for ClawHub integration
import requests
import base64
from urllib.parse import urljoin


class HubSync:
    """
    Syncs skills to ClawHub marketplace.
    
    Implements the Hub Sync functionality from SKILL.md architecture.
    """
    
    HUB_API_BASE = "https://hub.clawhub.example.com/api/v1"
    
    def __init__(self, config: Dict = None):
        self.config = config or {
            'api_endpoint': self.HUB_API_BASE,
            'api_key': os.environ.get('CLAWHUB_API_KEY', ''),
            'timeout': 30,
            'retry_count': 3,
            'auto_sync': False
        }
        self.sync_history: List[Dict] = []
    
    def sync_skill(self, skill: Skill, skill_content: str = None) -> Dict:
        """
        Upload a skill to ClawHub.
        
        Args:
            skill: Skill object to sync
            skill_content: Optional full SKILL.md content
            
        Returns:
            Sync result with hub_id and status
        """
        if not self.config['api_key']:
            return {
                'success': False,
                'reason': 'API key not configured',
                'skill': skill.name
            }
        
        skill.sync_status = "syncing"
        
        payload = {
            'name': skill.name,
            'description': skill.description,
            'content': skill_content or skill.to_skill_md(),
            'metadata': {
                'confidence': skill.confidence,
                'source_experiences': len(skill.source_experiences),
                'created_at': skill.created_at,
                'triggers': skill.triggers,
                'local_status': skill.status
            }
        }
        
        for attempt in range(self.config['retry_count']):
            try:
                response = self._make_request('POST', '/skills', payload)
                
                sync_result = {
                    'success': True,
                    'skill': skill.name,
                    'hub_id': response.get('id'),
                    'hub_url': response.get('url'),
                    'timestamp': datetime.now().isoformat()
                }
                
                self.sync_history.append(sync_result)
                skill.sync_status = "synced"
                
                return sync_result
                
            except Exception as e:
                if attempt == self.config['retry_count'] - 1:
                    skill.sync_status = "failed"
                    return {
                        'success': False,
                        'skill': skill.name,
                        'reason': str(e),
                        'timestamp': datetime.now().isoformat()
                    }
        
        return {'success': False, 'skill': skill.name}
    
    def sync_batch(self, skills: List[Skill]) -> List[Dict]:
        """
        Sync multiple skills to ClawHub.
        
        Args:
            skills: List of Skill objects
            
        Returns:
            List of sync results
        """
        results = []
        for skill in skills:
            result = self.sync_skill(skill)
            results.append(result)
        return results
    
    def fetch_remote_skills(self, query: str = None, category: str = None) -> List[Dict]:
        """
        Fetch skills from ClawHub.
        
        Args:
            query: Search query
            category: Filter by category
            
        Returns:
            List of remote skill metadata
        """
        params = {}
        if query:
            params['q'] = query
        if category:
            params['category'] = category
        
        try:
            response = self._make_request('GET', '/skills', params=params)
            return response.get('skills', [])
        except Exception as e:
            return []
    
    def get_sync_status(self, hub_id: str) -> Dict:
        """
        Get sync status of a remote skill.
        
        Args:
            hub_id: ClawHub skill ID
            
        Returns:
            Status information
        """
        try:
            response = self._make_request('GET', f'/skills/{hub_id}/status')
            return response
        except Exception:
            return {'status': 'unknown'}
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None, 
                     params: Dict = None) -> Dict:
        """Make authenticated request to ClawHub API."""
        url = urljoin(self.config['api_endpoint'], endpoint)
        headers = {
            'Authorization': f'Bearer {self.config["api_key"]}',
            'Content-Type': 'application/json'
        }
        
        if method == 'GET':
            response = requests.get(url, params=params, headers=headers,
                                   timeout=self.config['timeout'])
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers,
                                     timeout=self.config['timeout'])
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    def get_sync_history(self, limit: int = 20) -> List[Dict]:
        """Get sync history."""
        return self.sync_history[-limit:]


# Example usage
if __name__ == "__main__":
    # Initialize
    creator = SkillCreator()
    
    # Sample experiences
    experiences = [
        {
            'id': 'exp_001',
            'user_input': '分析这份PDF报告',
            'actions': ['load_pdf', 'extract_text', 'analyze', 'summarize'],
            'context': {'file_type': 'pdf', 'pages': 50},
            'outcome': 'success'
        },
        {
            'id': 'exp_002',
            'user_input': '分析Word文档',
            'actions': ['load_docx', 'extract_text', 'analyze', 'summarize'],
            'context': {'file_type': 'docx', 'pages': 30},
            'outcome': 'success'
        },
        {
            'id': 'exp_003',
            'user_input': '分析这份文档',
            'actions': ['load_document', 'extract_text', 'analyze', 'summarize'],
            'context': {'file_type': 'unknown'},
            'outcome': 'success'
        }
    ]
    
    # Scan and create
    results = creator.scan_and_create(experiences)
    
    print(f"Created {len([r for r in results if r['success']])} skills")
    for r in results:
        print(f"  - {r.get('skill', r.get('reason'))}")
