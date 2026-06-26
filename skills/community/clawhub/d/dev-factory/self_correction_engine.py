#!/usr/bin/env python3
"""
Self-Correction Engine for Builder Agent
자가 수정 루프 구현
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class SelfCorrectionEngine:
    """자가 수정 엔진"""
    
    MAX_RETRIES = 3
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.retry_count = 0
        self.error_history = []
        self.success_patterns = []
        self.failure_patterns = []
        
    def develop_with_retry(self, project_idea: Dict) -> Dict:
        """
        자가 수정 루프를 통한 개발
        
        Returns:
            {
                'success': bool,
                'project_path': str,
                'retry_count': int,
                'errors': List[Dict],
                'corrections': List[Dict]
            }
        """
        print(f"🚀 Starting development: {project_idea['title']}")
        
        for attempt in range(self.MAX_RETRIES):
            self.retry_count = attempt + 1
            print(f"\n📍 Attempt {self.retry_count}/{self.MAX_RETRIES}")
            
            # 1. 개발 실행
            if attempt == 0:
                # 첫 시도: 초기 개발
                dev_result = self._initial_development(project_idea)
            else:
                # 재시도: 이전 에러 기반 수정
                dev_result = self._correct_and_retry(project_idea, self.error_history[-1])
            
            # 2. 테스트 실행
            test_result = self._run_tests()
            
            # 3. 결과 분석
            if test_result['success']:
                # 성공!
                print("✅ Tests passed!")
                
                # 성공 패턴 저장
                self._save_success_pattern(project_idea, dev_result, test_result)
                
                return {
                    'success': True,
                    'project_path': str(self.project_path),
                    'retry_count': self.retry_count,
                    'errors': self.error_history,
                    'test_output': test_result['output']
                }
            
            else:
                # 실패 - 에러 분석
                print(f"❌ Tests failed (attempt {self.retry_count})")
                
                error_analysis = self._analyze_error(test_result)
                self.error_history.append(error_analysis)
                
                # self-improving에 로깅
                self._log_failure(project_idea, error_analysis)
                
                # 다음 시도를 위한 수정 방안 준비
                print(f"🔍 Error analysis: {error_analysis['type']}")
                print(f"💡 Suggested fix: {error_analysis['fix_suggestion']}")
        
        # 최대 재시도 초과
        print(f"⚠️  Max retries ({self.MAX_RETRIES}) exceeded")
        
        return {
            'success': False,
            'project_path': str(self.project_path),
            'retry_count': self.retry_count,
            'errors': self.error_history,
            'final_error': self.error_history[-1] if self.error_history else None
        }
    
    def _initial_development(self, project_idea: Dict) -> Dict:
        """초기 개발 실행"""
        print("  📝 Initial development...")
        
        # 실제로는 ACP 하네스 또는 직접 구현 호출
        # 여기서는 간단히 파일 존재 여부만 확인
        
        return {
            'status': 'completed',
            'files_created': list(self.project_path.rglob('*.py')) if self.project_path.exists() else []
        }
    
    def _correct_and_retry(self, project_idea: Dict, last_error: Dict) -> Dict:
        """이전 에러 기반 수정"""
        print(f"  🔧 Correcting based on: {last_error['type']}")
        
        # 에러 타입별 수정 전략
        correction_strategies = {
            'missing_method': self._fix_missing_method,
            'import_error': self._fix_import_error,
            'test_failure': self._fix_test_failure,
            'attribute_error': self._fix_attribute_error,
            'type_error': self._fix_type_error
        }
        
        strategy = correction_strategies.get(last_error['type'], self._generic_fix)
        correction_result = strategy(last_error)
        
        return {
            'status': 'corrected',
            'correction': correction_result
        }
    
    def _run_tests(self) -> Dict:
        """테스트 실행"""
        print("  🧪 Running tests...")
        
        if not self.project_path.exists():
            return {'success': False, 'output': 'Project path does not exist'}
        
        try:
            # unittest 실행
            result = subprocess.run(
                ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=30,
                env={**os.environ, 'PYTHONPATH': 'src'}
            )
            
            success = result.returncode == 0
            
            return {
                'success': success,
                'output': result.stdout + result.stderr,
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'output': 'Test timeout'}
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    def _analyze_error(self, test_result: Dict) -> Dict:
        """에러 분석"""
        output = test_result['output']
        
        # 에러 타입 감지
        error_patterns = {
            'missing_method': [
                'AttributeError.*has no attribute',
                'does not have the attribute'
            ],
            'import_error': [
                'ModuleNotFoundError',
                'ImportError'
            ],
            'test_failure': [
                'FAIL:',
                'AssertionError'
            ],
            'attribute_error': [
                'AttributeError'
            ],
            'type_error': [
                'TypeError',
                'KeyError'
            ]
        }
        
        import re
        
        for error_type, patterns in error_patterns.items():
            for pattern in patterns:
                if re.search(pattern, output):
                    return {
                        'type': error_type,
                        'raw_output': output[:500],
                        'fix_suggestion': self._suggest_fix(error_type, output)
                    }
        
        return {
            'type': 'unknown',
            'raw_output': output[:500],
            'fix_suggestion': 'Manual review required'
        }
    
    def _suggest_fix(self, error_type: str, error_output: str) -> str:
        """에러 타입별 수정 제안"""
        suggestions = {
            'missing_method': 'Add missing method to the class',
            'import_error': 'Check import paths or install missing module',
            'test_failure': 'Review test assertions and fix implementation',
            'attribute_error': 'Add missing attribute or check object initialization',
            'type_error': 'Fix data type or key access patterns'
        }
        return suggestions.get(error_type, 'Review error and fix accordingly')
    
    # 수정 전략들
    def _fix_missing_method(self, error: Dict) -> Dict:
        """누락된 메서드 수정"""
        import re
        
        # 에러에서 메서드 이름 추출
        match = re.search(r"has no attribute '(\w+)'", error['raw_output'])
        if match:
            method_name = match.group(1)
            return {
                'action': 'add_method',
                'method_name': method_name,
                'suggestion': f"Add method '{method_name}' to the class"
            }
        
        return {'action': 'manual_review', 'reason': 'Could not extract method name'}
    
    def _fix_import_error(self, error: Dict) -> Dict:
        """Import 에러 수정"""
        import re
        
        match = re.search(r"No module named '([\w.]+)'", error['raw_output'])
        if match:
            module_name = match.group(1)
            return {
                'action': 'fix_import',
                'module': module_name,
                'suggestion': f"Fix import path for '{module_name}' or add PYTHONPATH"
            }
        
        return {'action': 'manual_review', 'reason': 'Could not extract module name'}
    
    def _fix_test_failure(self, error: Dict) -> Dict:
        """테스트 실패 수정"""
        return {
            'action': 'fix_implementation',
            'suggestion': 'Review test output and fix implementation to match expected behavior'
        }
    
    def _fix_attribute_error(self, error: Dict) -> Dict:
        """Attribute 에러 수정"""
        return self._fix_missing_method(error)
    
    def _fix_type_error(self, error: Dict) -> Dict:
        """Type 에러 수정"""
        import re
        
        if 'KeyError' in error['raw_output']:
            match = re.search(r"KeyError: '(\w+)'", error['raw_output'])
            if match:
                key = match.group(1)
                return {
                    'action': 'fix_key_access',
                    'key': key,
                    'suggestion': f"Key '{key}' not found. Check data structure or add default value"
                }
        
        return {
            'action': 'fix_types',
            'suggestion': 'Review data types and fix type mismatches'
        }
    
    def _generic_fix(self, error: Dict) -> Dict:
        """일반적인 수정"""
        return {
            'action': 'manual_review',
            'error': error['raw_output'][:200]
        }
    
    def _save_success_pattern(self, project_idea: Dict, dev_result: Dict, test_result: Dict):
        """성공 패턴을 메모리에 저장"""
        
        # self-improving 디렉토리
        si_dir = Path.home() / "self-improving"
        si_dir.mkdir(parents=True, exist_ok=True)
        
        # 성공 패턴 기록
        pattern = {
            'timestamp': datetime.now().isoformat(),
            'project': project_idea['title'],
            'complexity': project_idea.get('complexity', 'unknown'),
            'retry_count': self.retry_count,
            'approach': 'direct' if self.retry_count == 1 else f'corrected_{self.retry_count}',
            'tech_stack': project_idea.get('tech_stack', []),
            'success_factors': self._extract_success_factors(project_idea)
        }
        
        # reflections.md에 추가
        reflections_file = si_dir / "reflections.md"
        
        with open(reflections_file, 'a') as f:
            f.write(f"\n### {pattern['timestamp']}\n")
            f.write(f"**CONTEXT**: {pattern['project']} ({pattern['complexity']})\n")
            f.write(f"**REFLECTION**: Succeeded after {pattern['retry_count']} attempt(s)\n")
            f.write(f"**LESSON**: {', '.join(pattern['success_factors'])}\n")
        
        print(f"  💾 Success pattern saved to self-improving")
    
    def _log_failure(self, project_idea: Dict, error_analysis: Dict):
        """실패 패턴을 self-improving에 로깅"""
        
        si_dir = Path.home() / "self-improving"
        si_dir.mkdir(parents=True, exist_ok=True)
        
        # corrections.md에 추가
        corrections_file = si_dir / "corrections.md"
        
        with open(corrections_file, 'a') as f:
            f.write(f"\n### {datetime.now().isoformat()}\n")
            f.write(f"**PROJECT**: {project_idea['title']}\n")
            f.write(f"**ATTEMPT**: {self.retry_count}/{self.MAX_RETRIES}\n")
            f.write(f"**ERROR TYPE**: {error_analysis['type']}\n")
            f.write(f"**SUGGESTION**: {error_analysis['fix_suggestion']}\n")
        
        print(f"  📝 Failure logged to self-improving")
    
    def _extract_success_factors(self, project_idea: Dict) -> List[str]:
        """성공 요인 추출"""
        factors = []
        
        if self.retry_count == 1:
            factors.append("First attempt success")
        else:
            factors.append(f"Corrected after {self.retry_count - 1} failure(s)")
        
        if project_idea.get('complexity') == 'simple':
            factors.append("Simple complexity - direct implementation")
        
        return factors


# 사용 예시
if __name__ == "__main__":
    # CVE Scanner 프로젝트로 테스트
    engine = SelfCorrectionEngine("/tmp/builder-projects/cve-scanner-cli")
    
    project_idea = {
        'title': 'CVE Scanner CLI',
        'complexity': 'medium',
        'tech_stack': ['Python', 'urllib', 'json']
    }
    
    result = engine.develop_with_retry(project_idea)
    
    print("\n" + "="*70)
    print("FINAL RESULT:")
    print(f"Success: {result['success']}")
    print(f"Retries: {result['retry_count']}")
    if not result['success']:
        print(f"Final Error: {result.get('final_error', {}).get('type', 'Unknown')}")
