#!/usr/bin/env python3
"""
Hybrid ACP Self-Correction Engine
현재 환경에서 가능한 ACP 통합 방식
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime


class HybridACPSelfCorrection:
    """하이브리드 ACP 자가 수정 엔진"""
    
    MAX_RETRIES = 3
    
    # ACP 호출 방식
    ACP_MODES = {
        'direct': '현재 세션에서 직접 수정 (GLM-5)',
        'cli': 'openclaw CLI 통한 subprocess 호출',
        'manual': '수동 수정 (사용자 가이드 제공)'
    }
    
    def __init__(self, project_path: str, acp_mode: str = 'direct'):
        self.project_path = Path(project_path)
        self.acp_mode = acp_mode
        self.retry_count = 0
        self.error_history = []
        
    def develop_with_hybrid_acp(self, project_idea: Dict) -> Dict:
        """하이브리드 ACP 자가 수정 루프"""
        
        print(f"🚀 Starting Hybrid ACP development: {project_idea['title']}")
        print(f"   Mode: {self.ACP_MODES[self.acp_mode]}")
        
        for attempt in range(self.MAX_RETRIES):
            self.retry_count = attempt + 1
            print(f"\n📍 Attempt {self.retry_count}/{self.MAX_RETRIES}")
            
            # 1. 개발/수정 실행
            if attempt == 0:
                dev_result = self._initial_development(project_idea)
            else:
                dev_result = self._fix_via_hybrid_acp(project_idea, self.error_history[-1])
            
            # 2. 테스트 실행
            test_result = self._run_tests()
            
            # 3. 결과 분석
            if test_result['success']:
                print("✅ All tests passed!")
                self._save_success(project_idea, dev_result)
                
                return {
                    'success': True,
                    'project_path': str(self.project_path),
                    'retry_count': self.retry_count,
                    'mode': self.acp_mode,
                    'test_output': test_result['output']
                }
            
            else:
                print(f"❌ Tests failed")
                error_analysis = self._analyze_error(test_result)
                self.error_history.append(error_analysis)
                self._log_failure(project_idea, error_analysis)
        
        print(f"⚠️  Max retries exceeded")
        return {
            'success': False,
            'project_path': str(self.project_path),
            'retry_count': self.retry_count,
            'errors': self.error_history
        }
    
    def _initial_development(self, project_idea: Dict) -> Dict:
        """초기 개발"""
        
        complexity = project_idea.get('complexity', 'medium')
        
        if complexity == 'simple':
            # Simple: 직접 구현
            print("  📝 Direct implementation (simple complexity)")
            return {'status': 'direct', 'mode': 'simple'}
        
        elif self.acp_mode == 'cli':
            # CLI 모드: openclaw agent 호출
            return self._call_via_cli(project_idea)
        
        else:
            # Direct 모드: 현재 세션에서 수행
            print("  📝 Development in current session")
            return {'status': 'direct', 'mode': 'current_session'}
    
    def _fix_via_hybrid_acp(self, project_idea: Dict, error: Dict) -> Dict:
        """하이브리드 ACP 수정"""
        
        print(f"  🔧 Fixing: {error['type']}")
        
        if self.acp_mode == 'cli':
            # CLI로 수정 요청
            return self._call_fix_via_cli(project_idea, error)
        
        elif self.acp_mode == 'manual':
            # 수동 수정 가이드 제공
            return self._provide_manual_fix_guide(error)
        
        else:
            # 직접 수정 시도
            return self._apply_direct_fix(error)
    
    def _call_via_cli(self, project_idea: Dict) -> Dict:
        """OpenClaw CLI 통한 호출"""
        
        # 프롬프트 생성
        prompt = self._generate_development_prompt(project_idea)
        
        # openclaw agent 명령 실행
        try:
            result = subprocess.run([
                'openclaw', 'agent',
                '--message', prompt,
                '--json'
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                return {
                    'status': 'cli_success',
                    'output': result.stdout[:500]
                }
            else:
                return {
                    'status': 'cli_failed',
                    'error': result.stderr[:200]
                }
        
        except subprocess.TimeoutExpired:
            return {'status': 'cli_timeout'}
        except Exception as e:
            return {'status': 'cli_error', 'error': str(e)}
    
    def _call_fix_via_cli(self, project_idea: Dict, error: Dict) -> Dict:
        """CLI 통한 수정 요청"""
        
        prompt = self._generate_fix_prompt(project_idea, error)
        
        try:
            result = subprocess.run([
                'openclaw', 'agent',
                '--message', prompt
            ], capture_output=True, text=True, timeout=60)
            
            return {
                'status': 'cli_fix_requested',
                'prompt_length': len(prompt)
            }
        
        except Exception as e:
            return {'status': 'cli_error', 'error': str(e)}
    
    def _provide_manual_fix_guide(self, error: Dict) -> Dict:
        """수동 수정 가이드 제공"""
        
        guide = f"""
🔧 Manual Fix Required

Error Type: {error['type']}
Suggestion: {error['fix_suggestion']}

To fix this using Codex or Claude Code:

1. Open a new terminal
2. Navigate to: {self.project_path}
3. Run one of:

   # Using Claude Code
   claude-code --task "Fix {error['type']} in this project: {error['raw_output'][:100]}"
   
   # Using Codex
   codex "Fix the error: {error['raw_output'][:100]}"

4. Review and apply the suggested changes
5. Re-run tests

Context:
- Project: {self.project_path.name}
- Attempt: {self.retry_count}/{self.MAX_RETRIES}
"""
        
        print(guide)
        
        return {
            'status': 'manual_guide',
            'guide': guide,
            'requires_user_action': True
        }
    
    def _apply_direct_fix(self, error: Dict) -> Dict:
        """직접 수정 적용"""
        
        error_type = error['type']
        
        if error_type == 'type_error':
            return self._fix_type_error(error)
        elif error_type == 'import_error':
            return self._fix_import_error(error)
        elif error_type == 'missing_method':
            return self._fix_missing_method(error)
        else:
            return self._provide_manual_fix_guide(error)
    
    def _fix_type_error(self, error: Dict) -> Dict:
        """Type 에러 수정"""
        
        import re
        
        # KeyError
        key_match = re.search(r"KeyError: '(\w+)'", error['raw_output'])
        if key_match:
            missing_key = key_match.group(1)
            
            # 사용자에게 구체적인 수정 방법 제안
            print(f"\n💡 Fix Suggestion:")
            print(f"   Key '{missing_key}' not found in dictionary")
            print(f"   Change: data['{missing_key}']")
            print(f"   To: data.get('{missing_key}', default_value)")
            
            return {
                'status': 'fix_suggested',
                'type': 'key_error',
                'key': missing_key,
                'suggestion': f"Use .get('{missing_key}', default) instead of ['{missing_key}']"
            }
        
        # AttributeError
        attr_match = re.search(r"'(\w+)' object has no attribute '(\w+)'", error['raw_output'])
        if attr_match:
            obj_type = attr_match.group(1)
            missing_attr = attr_match.group(2)
            
            print(f"\n💡 Fix Suggestion:")
            print(f"   {obj_type} doesn't have attribute '{missing_attr}'")
            print(f"   Check if the object is properly initialized")
            print(f"   Or add the missing attribute/method")
            
            return {
                'status': 'fix_suggested',
                'type': 'attribute_error',
                'object': obj_type,
                'attribute': missing_attr
            }
        
        return {'status': 'unknown_type_error'}
    
    def _fix_import_error(self, error: Dict) -> Dict:
        """Import 에러 수정"""
        
        import re
        
        module_match = re.search(r"No module named '([\w.]+)'", error['raw_output'])
        if module_match:
            module = module_match.group(1)
            
            print(f"\n💡 Fix Suggestion:")
            print(f"   Module '{module}' not found")
            print(f"   Add to PYTHONPATH: export PYTHONPATH=src:$PYTHONPATH")
            print(f"   Or fix import: from {module} import ...")
            
            return {
                'status': 'fix_suggested',
                'type': 'import_error',
                'module': module
            }
        
        return {'status': 'unknown_import_error'}
    
    def _fix_missing_method(self, error: Dict) -> Dict:
        """누락된 메서드 수정"""
        
        import re
        
        method_match = re.search(r"has no attribute '(\w+)'", error['raw_output'])
        if method_match:
            method = method_match.group(1)
            
            print(f"\n💡 Fix Suggestion:")
            print(f"   Method '{method}' not found")
            print(f"   Add the method to the class or check spelling")
            
            return {
                'status': 'fix_suggested',
                'type': 'missing_method',
                'method': method
            }
        
        return {'status': 'unknown_method_error'}
    
    def _generate_development_prompt(self, project_idea: Dict) -> str:
        """개발 프롬프트 생성"""
        
        return f"""
Develop: {project_idea['title']}

Requirements:
{project_idea.get('description', 'See requirements')}

Complexity: {project_idea.get('complexity', 'medium')}
Tech Stack: {', '.join(project_idea.get('tech_stack', []))}

Output Path: {self.project_path}

Instructions:
1. Create all necessary files
2. Include comprehensive error handling
3. Add unit tests
4. Ensure code is production-ready
"""
    
    def _generate_fix_prompt(self, project_idea: Dict, error: Dict) -> str:
        """수정 프롬프트 생성"""
        
        return f"""
Fix error in: {project_idea['title']}

Error Type: {error['type']}
Error Details: {error['raw_output'][:300]}

Project Path: {self.project_path}
Attempt: {self.retry_count}/{self.MAX_RETRIES}

Instructions:
1. Analyze the error
2. Identify root cause
3. Apply minimal fix
4. Ensure fix doesn't break other functionality
"""
    
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
                'output': result.stdout + result.stderr
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
        """수정 제안"""
        
        suggestions = {
            'type_error': 'Check data structure and use .get() for optional keys',
            'import_error': 'Fix import paths or add module to PYTHONPATH',
            'missing_method': 'Implement the missing method in the class',
            'test_failure': 'Review test assertions and fix implementation'
        }
        
        return suggestions.get(error_type, 'Review and fix manually')
    
    def _save_success(self, project_idea: Dict, dev_result: Dict):
        """성공 패턴 저장"""
        
        si_dir = Path.home() / "self-improving"
        si_dir.mkdir(parents=True, exist_ok=True)
        
        reflections_file = si_dir / "reflections.md"
        
        with open(reflections_file, 'a') as f:
            f.write(f"\n### {datetime.now().isoformat()}\n")
            f.write(f"**CONTEXT**: {project_idea['title']} ({project_idea.get('complexity', 'unknown')})\n")
            f.write(f"**REFLECTION**: Succeeded after {self.retry_count} attempt(s) via {self.acp_mode}\n")
            f.write(f"**LESSON**: Mode={self.acp_mode}, Retries={self.retry_count}\n")
        
        print(f"  💾 Saved to self-improving")
    
    def _log_failure(self, project_idea: Dict, error: Dict):
        """실패 로깅"""
        
        si_dir = Path.home() / "self-improving"
        si_dir.mkdir(parents=True, exist_ok=True)
        
        corrections_file = si_dir / "corrections.md"
        
        with open(corrections_file, 'a') as f:
            f.write(f"\n### {datetime.now().isoformat()}\n")
            f.write(f"**PROJECT**: {project_idea['title']}\n")
            f.write(f"**MODE**: {self.acp_mode}\n")
            f.write(f"**ATTEMPT**: {self.retry_count}/{self.MAX_RETRIES}\n")
            f.write(f"**ERROR**: {error['type']}\n")
            f.write(f"**SUGGESTION**: {error['fix_suggestion']}\n")
        
        print(f"  📝 Logged to self-improving")


# 사용 예시
if __name__ == "__main__":
    # CVE Scanner로 테스트
    engine = HybridACPSelfCorrection(
        "/tmp/builder-projects/cve-scanner-cli",
        acp_mode='direct'  # 'direct', 'cli', 'manual'
    )
    
    project_idea = {
        'title': 'CVE Scanner CLI',
        'complexity': 'medium',
        'tech_stack': ['Python', 'urllib', 'json']
    }
    
    result = engine.develop_with_hybrid_acp(project_idea)
    
    print("\n" + "="*70)
    print("FINAL RESULT:")
    print(f"Success: {result['success']}")
    print(f"Mode: {result.get('mode', 'N/A')}")
    print(f"Retries: {result['retry_count']}")
