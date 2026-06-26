#!/usr/bin/env python3
"""
ACP-Based Self-Correction Engine
ACP 하네스를 통한 자가 수정 루프
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class ACPBasedSelfCorrection:
    """ACP 하네스 기반 자가 수정 엔진"""
    
    MAX_RETRIES = 3
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.retry_count = 0
        self.error_history = []
        
    def develop_with_acp_retry(self, project_idea: Dict) -> Dict:
        """ACP 하네스를 통한 자가 수정 루프"""
        
        print(f"🚀 Starting ACP-based development: {project_idea['title']}")
        
        for attempt in range(self.MAX_RETRIES):
            self.retry_count = attempt + 1
            print(f"\n📍 Attempt {self.retry_count}/{self.MAX_RETRIES}")
            
            # 1. 개발/수정 실행
            if attempt == 0:
                # 첫 시도: 초기 개발
                print("  📝 Initial development via ACP...")
                dev_result = self._develop_via_acp(project_idea, complexity=project_idea.get('complexity', 'medium'))
            else:
                # 재시도: 에러 기반 수정
                last_error = self.error_history[-1]
                print(f"  🔧 Fixing via ACP: {last_error['type']}")
                dev_result = self._fix_via_acp(project_idea, last_error)
            
            # 2. 테스트 실행
            print("  🧪 Running tests...")
            test_result = self._run_tests()
            
            # 3. 결과 분석
            if test_result['success']:
                print("✅ All tests passed!")
                
                # 성공 패턴 저장
                self._save_success(project_idea, dev_result)
                
                return {
                    'success': True,
                    'project_path': str(self.project_path),
                    'retry_count': self.retry_count,
                    'test_output': test_result['output']
                }
            
            else:
                print(f"❌ Tests failed")
                
                # 에러 분석
                error_analysis = self._analyze_error(test_result)
                self.error_history.append(error_analysis)
                
                # 실패 로깅
                self._log_failure(project_idea, error_analysis)
        
        # 최대 재시도 초과
        print(f"⚠️  Max retries exceeded")
        return {
            'success': False,
            'project_path': str(self.project_path),
            'retry_count': self.retry_count,
            'errors': self.error_history
        }
    
    def _develop_via_acp(self, project_idea: Dict, complexity: str = 'medium') -> Dict:
        """ACP 하네스로 개발 실행"""
        
        # 복잡도별 에이전트 선택
        agent_map = {
            'simple': None,  # 직접 구현
            'medium': 'codex',
            'complex': 'claude-code'
        }
        
        agent_id = agent_map.get(complexity, 'codex')
        
        if not agent_id:
            # Simple: 직접 파일 확인만
            return {'status': 'direct', 'files': list(self.project_path.rglob('*.py'))}
        
        # ACP 하네스 호출 (실제로는 sessions_spawn 사용)
        # 여기서는 시뮬레이션
        print(f"    → Would call ACP agent: {agent_id}")
        
        # 실제 ACP 호출은 OpenClaw에서만 가능
        # 시뮬레이션 결과 반환
        return {
            'status': 'acp_simulated',
            'agent': agent_id,
            'note': 'In production, this would call sessions_spawn'
        }
    
    def _fix_via_acp(self, project_idea: Dict, error: Dict) -> Dict:
        """ACP 하네스로 수정 실행"""
        
        # 수정 프롬프트 생성
        fix_prompt = self._generate_fix_prompt(project_idea, error)
        
        print(f"    → Fix prompt generated ({len(fix_prompt)} chars)")
        
        # ACP 하네스 호출 (시뮬레이션)
        # 실제로는:
        # result = await sessions_spawn(
        #     agentId="claude-code",
        #     mode="run",
        #     task=fix_prompt,
        #     cwd=str(self.project_path),
        #     runTimeoutSeconds=120
        # )
        
        # 시뮬레이션: 직접 수정 시도
        fix_result = self._apply_fix_locally(error)
        
        return {
            'status': 'fixed_locally',
            'fix': fix_result,
            'prompt': fix_prompt[:200] + '...'
        }
    
    def _generate_fix_prompt(self, project_idea: Dict, error: Dict) -> str:
        """수정용 프롬프트 생성"""
        
        prompt = f"""
Fix the following error in {project_idea['title']}:

**Error Type**: {error['type']}
**Error Details**: {error['raw_output'][:300]}

**Project Context**:
- Path: {self.project_path}
- Tech Stack: {', '.join(project_idea.get('tech_stack', []))}
- Complexity: {project_idea.get('complexity', 'unknown')}

**Suggested Fix**: {error['fix_suggestion']}

**Instructions**:
1. Analyze the error
2. Identify the root cause
3. Apply minimal, targeted fix
4. Ensure fix doesn't break existing functionality
5. Focus on the specific error, don't refactor unrelated code

**Memory Context** (learn from past failures):
{self._get_memory_context()}

Return the fixed code or explain what needs to be changed.
"""
        return prompt
    
    def _apply_fix_locally(self, error: Dict) -> Dict:
        """로컬에서 직접 수정 적용"""
        
        error_type = error['type']
        
        # 에러 타입별 수정 전략
        if error_type == 'type_error':
            return self._fix_type_error_locally(error)
        elif error_type == 'import_error':
            return self._fix_import_error_locally(error)
        elif error_type == 'missing_method':
            return self._fix_missing_method_locally(error)
        else:
            return {'status': 'manual_required', 'reason': f'Cannot auto-fix {error_type}'}
    
    def _fix_type_error_locally(self, error: Dict) -> Dict:
        """Type 에러 로컬 수정"""
        
        import re
        
        raw_output = error['raw_output']
        
        # KeyError 패턴
        key_match = re.search(r"KeyError: '(\w+)'", raw_output)
        if key_match:
            missing_key = key_match.group(1)
            
            # 해당 키를 사용하는 파일 찾기
            for py_file in self.project_path.rglob('*.py'):
                content = py_file.read_text()
                
                if f"['{missing_key}']" in content or f'["{missing_key}"]' in content:
                    print(f"    ✓ Found usage in: {py_file.name}")
                    
                    # .get()으로 변경 제안 (실제로는 더 정교한 수정 필요)
                    return {
                        'status': 'identified',
                        'file': str(py_file),
                        'key': missing_key,
                        'suggestion': f"Use .get('{missing_key}', default) instead of ['{missing_key}']"
                    }
        
        # AttributeError 패턴
        attr_match = re.search(r"'(\w+)' object has no attribute '(\w+)'", raw_output)
        if attr_match:
            obj_type = attr_match.group(1)
            missing_attr = attr_match.group(2)
            
            return {
                'status': 'identified',
                'object_type': obj_type,
                'missing_attribute': missing_attr,
                'suggestion': f"Add '{missing_attr}' to {obj_type} class or check data structure"
            }
        
        return {'status': 'not_identified', 'raw': raw_output[:200]}
    
    def _fix_import_error_locally(self, error: Dict) -> Dict:
        """Import 에러 로컬 수정"""
        
        import re
        
        module_match = re.search(r"No module named '([\w.]+)'", error['raw_output'])
        if module_match:
            missing_module = module_match.group(1)
            
            # PYTHONPATH 문제인지 확인
            return {
                'status': 'identified',
                'module': missing_module,
                'suggestion': f"Add 'src' to PYTHONPATH or fix import from '{missing_module}'"
            }
        
        return {'status': 'not_identified'}
    
    def _fix_missing_method_locally(self, error: Dict) -> Dict:
        """누락된 메서드 로컬 수정"""
        
        import re
        
        method_match = re.search(r"has no attribute '(\w+)'", error['raw_output'])
        if method_match:
            method_name = method_match.group(1)
            
            # 해당 메서드를 호출하는 파일 찾기
            for py_file in self.project_path.rglob('*.py'):
                if method_name in py_file.read_text():
                    print(f"    ✓ Method '{method_name}' called in: {py_file.name}")
            
            return {
                'status': 'identified',
                'method_name': method_name,
                'suggestion': f"Implement method '{method_name}' in the class"
            }
        
        return {'status': 'not_identified'}
    
    def _run_tests(self) -> Dict:
        """테스트 실행"""
        
        if not self.project_path.exists():
            return {'success': False, 'output': 'Project not found'}
        
        try:
            result = subprocess.run(
                ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=30,
                env={**os.environ, 'PYTHONPATH': 'src'}
            )
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout + result.stderr,
                'returncode': result.returncode
            }
            
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    def _analyze_error(self, test_result: Dict) -> Dict:
        """에러 분석"""
        
        output = test_result['output']
        
        error_patterns = {
            'type_error': ['KeyError', 'TypeError', 'AttributeError'],
            'import_error': ['ModuleNotFoundError', 'ImportError'],
            'missing_method': ['has no attribute'],
            'test_failure': ['FAIL:', 'AssertionError']
        }
        
        for error_type, patterns in error_patterns.items():
            for pattern in patterns:
                if pattern in output:
                    return {
                        'type': error_type,
                        'raw_output': output[:500],
                        'fix_suggestion': self._get_fix_suggestion(error_type)
                    }
        
        return {
            'type': 'unknown',
            'raw_output': output[:500],
            'fix_suggestion': 'Manual review required'
        }
    
    def _get_fix_suggestion(self, error_type: str) -> str:
        """에러 타입별 수정 제안"""
        
        suggestions = {
            'type_error': 'Check data structure and use .get() for optional keys',
            'import_error': 'Fix import paths or add module to PYTHONPATH',
            'missing_method': 'Implement the missing method in the class',
            'test_failure': 'Review test assertions and fix implementation'
        }
        
        return suggestions.get(error_type, 'Review and fix manually')
    
    def _get_memory_context(self) -> str:
        """self-improving에서 관련 컨텍스트 가져오기"""
        
        si_dir = Path.home() / "self-improving"
        reflections_file = si_dir / "reflections.md"
        
        if reflections_file.exists():
            # 최근 5개 성찰만 가져오기
            with open(reflections_file, 'r') as f:
                lines = f.readlines()
            
            # 최근 섹션 찾기
            recent = []
            for line in lines[-50:]:  # 마지막 50줄만
                if line.startswith('###') or line.startswith('**'):
                    recent.append(line.strip())
            
            return '\n'.join(recent[-10:])  # 최근 10개 라인
        
        return "No previous learnings found"
    
    def _save_success(self, project_idea: Dict, dev_result: Dict):
        """성공 패턴 저장"""
        
        si_dir = Path.home() / "self-improving"
        si_dir.mkdir(parents=True, exist_ok=True)
        
        reflections_file = si_dir / "reflections.md"
        
        with open(reflections_file, 'a') as f:
            f.write(f"\n### {datetime.now().isoformat()}\n")
            f.write(f"**CONTEXT**: {project_idea['title']} ({project_idea.get('complexity', 'unknown')})\n")
            f.write(f"**REFLECTION**: Succeeded after {self.retry_count} attempt(s)\n")
            f.write(f"**LESSON**: {', '.join(self._extract_lessons())}\n")
        
        print(f"  💾 Saved to self-improving")
    
    def _log_failure(self, project_idea: Dict, error: Dict):
        """실패 로깅"""
        
        si_dir = Path.home() / "self-improving"
        si_dir.mkdir(parents=True, exist_ok=True)
        
        corrections_file = si_dir / "corrections.md"
        
        with open(corrections_file, 'a') as f:
            f.write(f"\n### {datetime.now().isoformat()}\n")
            f.write(f"**PROJECT**: {project_idea['title']}\n")
            f.write(f"**ATTEMPT**: {self.retry_count}/{self.MAX_RETRIES}\n")
            f.write(f"**ERROR**: {error['type']}\n")
            f.write(f"**SUGGESTION**: {error['fix_suggestion']}\n")
        
        print(f"  📝 Logged to self-improving")
    
    def _extract_lessons(self) -> List[str]:
        """교훈 추출"""
        
        lessons = []
        
        if self.retry_count == 1:
            lessons.append("First attempt success - well-structured initial code")
        else:
            lessons.append(f"Required {self.retry_count} iterations - improve initial planning")
        
        if self.error_history:
            error_types = set(e['type'] for e in self.error_history)
            lessons.append(f"Encountered: {', '.join(error_types)}")
        
        return lessons


# 사용 예시
if __name__ == "__main__":
    # CVE Scanner로 테스트
    engine = ACPBasedSelfCorrection("/tmp/builder-projects/cve-scanner-cli")
    
    project_idea = {
        'title': 'CVE Scanner CLI',
        'complexity': 'medium',
        'tech_stack': ['Python', 'urllib', 'json']
    }
    
    result = engine.develop_with_acp_retry(project_idea)
    
    print("\n" + "="*70)
    print("FINAL RESULT:")
    print(f"Success: {result['success']}")
    print(f"Retries: {result['retry_count']}")
    
    if result['success']:
        print(f"\n✅ Project completed successfully!")
    else:
        print(f"\n❌ Failed after {result['retry_count']} attempts")
        print(f"Errors encountered: {len(result.get('errors', []))}")
