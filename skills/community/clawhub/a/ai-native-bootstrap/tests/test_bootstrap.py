"""Offline acceptance and negative tests for the bootstrapper (stdlib unittest)."""
from __future__ import annotations
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
BOOT=ROOT/'scripts/bootstrap.py'
INSTALL=ROOT/'scripts/install.py'
PY=sys.executable

def call(script,*args):
    return subprocess.run([PY,str(script),*map(str,args)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=25)

def git(folder,*args):
    return subprocess.run(['git','-C',str(folder),*args],capture_output=True,text=True,timeout=10)

class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'project';self.root.mkdir()
    def mkrepo(self, branch='feature/bootstrap', content=True):
        self.assertEqual(git(self.root,'init','-q').returncode,0)
        self.assertEqual(git(self.root,'config','user.email','test@example.invalid').returncode,0)
        self.assertEqual(git(self.root,'config','user.name','Acceptance Test').returncode,0)
        if content:(self.root/'main.py').write_text('VALUE = 42\n')
        else:(self.root/'.gitignore').write_text('# fixture\n')
        self.assertEqual(git(self.root,'add','.').returncode,0)
        self.assertEqual(git(self.root,'commit','-qm','seed').returncode,0)
        self.assertEqual(git(self.root,'checkout','-qb',branch).returncode,0)
    def test_empty_new_directory_plan_is_read_only(self):
        r=call(BOOT,'plan','--project',self.root)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(list(self.root.iterdir()),[])
        self.assertIn('docs/ai-sdlc/audit.md',r.stdout)
    def test_read_only_audit_never_leaks_env_values(self):
        (self.root/'.env').write_text('SENSITIVE_DONT_PRINT=topsecretmarker')
        r=call(BOOT,'audit','--project',self.root)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertNotIn('topsecretmarker',r.stdout+r.stderr)
        self.assertEqual(set(x.name for x in self.root.iterdir()),{'.env'})
    def test_init_non_git_empty_and_verify(self):
        r=call(BOOT,'init','--project',self.root,'--apply')
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertTrue((self.root/'AGENTS.md').is_file())
        self.assertTrue((self.root/'CLAUDE.md').is_file())
        self.assertTrue((self.root/'docs/ai-sdlc/templates/intent.md').is_file())
        self.assertTrue((self.root/'scripts/ai-sdlc/check.py').is_file())
        self.assertEqual(call(BOOT,'verify','--project',self.root).returncode,0)
        check=call(self.root/'scripts/ai-sdlc/check.py')
        self.assertEqual(check.returncode,2)
        self.assertIn('BLOCKED',check.stderr)
    def test_fixture_gitrepo_preserves_existing_policy(self):
        (self.root/'AGENTS.md').write_text('MY INSTRUCTIONS\n')
        (self.root/'package.json').write_text(json.dumps({'scripts':{'test':'exit 1','lint':'eslint .'}}))
        self.mkrepo()
        r=call(BOOT,'init','--project',self.root,'--adapter','claude','--apply')
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual((self.root/'AGENTS.md').read_text(),'MY INSTRUCTIONS\n')
        checks=json.loads((self.root/'scripts/ai-sdlc/checks.json').read_text())['checks']
        self.assertTrue(any(x['name']=='test' and x['enabled'] is False for x in checks))
        self.assertTrue((self.root/'CLAUDE.md').is_file())
    def test_existing_claude_policy_is_not_clobbered(self):
        (self.root/'CLAUDE.md').write_text('CANONICAL CLAUDE POLICY\n')
        self.mkrepo()
        r=call(BOOT,'init','--project',self.root,'--adapter','all','--apply')
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual((self.root/'CLAUDE.md').read_text(),'CANONICAL CLAUDE POLICY\n')
        self.assertIn('CLAUDE.md',(self.root/'AGENTS.md').read_text())
    def test_dirty_git_blocks_without_writes(self):
        self.mkrepo()
        (self.root/'main.py').write_text('VALUE = 41\n')
        r=call(BOOT,'init','--project',self.root,'--apply')
        self.assertEqual(r.returncode,2)
        self.assertFalse((self.root/'docs/ai-sdlc').exists())
    def test_main_branch_blocks(self):
        self.mkrepo(branch='main')
        r=call(BOOT,'init','--project',self.root,'--apply')
        self.assertEqual(r.returncode,2)
        self.assertFalse((self.root/'docs').exists())
    def test_existing_non_git_project_blocks(self):
        (self.root/'app.py').write_text('print(123)\n')
        r=call(BOOT,'init','--project',self.root,'--apply')
        self.assertEqual(r.returncode,2)
        self.assertFalse((self.root/'docs').exists())
    def test_symlinked_target_parent_blocks(self):
        self.mkrepo()
        outside=Path(self.tmp.name)/'outside';outside.mkdir()
        (self.root/'docs').symlink_to(outside,target_is_directory=True)
        # Dirty worktree also blocks; explicitly check no outside write.
        r=call(BOOT,'init','--project',self.root,'--apply')
        self.assertEqual(r.returncode,2)
        self.assertEqual(list(outside.iterdir()),[])
    def test_clean_git_symlink_target_is_blocked(self):
        self.mkrepo()
        outside=Path(self.tmp.name)/'outside';outside.mkdir()
        (self.root/'docs').symlink_to(outside,target_is_directory=True)
        self.assertEqual(git(self.root,'add','docs').returncode,0)
        self.assertEqual(git(self.root,'commit','-qm','symlink fixture').returncode,0)
        r=call(BOOT,'init','--project',self.root,'--apply')
        self.assertEqual(r.returncode,2,r.stdout+r.stderr)
        self.assertIn('symlink',r.stderr.lower())
        self.assertEqual(list(outside.iterdir()),[])
    def test_clean_git_nested_repo_refuses(self):
        self.mkrepo()
        inner=self.root/'subdir';inner.mkdir()
        r=call(BOOT,'init','--project',inner,'--apply')
        self.assertEqual(r.returncode,2)
        self.assertIn('root',r.stderr.lower())

    def test_verify_detects_drift(self):
        self.assertEqual(call(BOOT,'init','--project',self.root,'--apply').returncode,0)
        (self.root/'AGENTS.md').write_text('modified\n')
        r=call(BOOT,'verify','--project',self.root)
        self.assertEqual(r.returncode,1)
        self.assertIn('AGENTS.md',r.stdout)
    def test_upgrade_after_committed_bootstrap_preserves_changes(self):
        self.mkrepo()
        first=call(BOOT,'init','--project',self.root,'--apply')
        self.assertEqual(first.returncode,0,first.stderr)
        self.assertEqual(git(self.root,'add','.').returncode,0)
        self.assertEqual(git(self.root,'commit','-qm','bootstrap baseline').returncode,0)
        prior=(self.root/'AGENTS.md').read_bytes()
        r=call(BOOT,'init','--project',self.root,'--upgrade','--apply')
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual((self.root/'AGENTS.md').read_bytes(),prior)
        self.assertEqual(call(BOOT,'verify','--project',self.root).returncode,0)
        self.assertEqual(r.stdout.count('UPGRADE'),1)

    def test_check_runner_success_and_failure(self):
        self.assertEqual(call(BOOT,'init','--project',self.root,'--apply').returncode,0)
        cfg=self.root/'scripts/ai-sdlc/checks.json'
        for exit_code in (0,3):
            cfg.write_text(json.dumps({'schema':1,'checks':[{'name':'fixture','argv':[PY,'-c',f'import sys; sys.exit({exit_code})'],'enabled':True}]}))
            r=call(self.root/'scripts/ai-sdlc/check.py')
            self.assertEqual(r.returncode,0 if exit_code==0 else 1,r.stdout+r.stderr)
            self.assertIn('PASS' if exit_code==0 else 'FAIL',r.stdout)
    def test_check_runner_blocks_shell_launcher(self):
        self.assertEqual(call(BOOT,'init','--project',self.root,'--apply').returncode,0)
        cfg=self.root/'scripts/ai-sdlc/checks.json'
        cfg.write_text(json.dumps({'schema':1,'checks':[{'name':'bad','argv':['bash','-c','echo unsafe'],'enabled':True}]}))
        r=call(self.root/'scripts/ai-sdlc/check.py')
        self.assertEqual(r.returncode,2)
        self.assertIn('BLOCKED',r.stderr)
    def test_init_without_apply_does_not_write(self):
        r=call(BOOT,'init','--project',self.root)
        self.assertEqual(r.returncode,0)
        self.assertEqual(list(self.root.iterdir()),[])

class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.home=Path(self.tmp.name)/'home';self.home.mkdir()
    def test_all_agent_scopes_preview_and_install(self):
        for agent in ('codex','claude','opencode'):
            r=call(INSTALL,'--agent',agent,'--scope','user','--home',self.home)
            self.assertEqual(r.returncode,0,r.stderr)
            expected={'codex':'.agents','claude':'.claude','opencode':'.config'}[agent]
            self.assertFalse((self.home/expected).exists())
            r=call(INSTALL,'--agent',agent,'--scope','user','--home',self.home,'--apply')
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertIn('INSTALLED',r.stdout)
        d=self.home/'.agents/skills/ai-native-bootstrap'
        self.assertTrue((d/'SKILL.md').is_file())
        self.assertTrue((d/'scripts/bootstrap.py').is_file())
    def test_collision_modified_upgrade_refuses(self):
        args=['--agent','codex','--scope','user','--home',str(self.home)]
        self.assertEqual(call(INSTALL,*args,'--apply').returncode,0)
        self.assertEqual(call(INSTALL,*args,'--apply').returncode,2)
        dest=self.home/'.agents/skills/ai-native-bootstrap'
        (dest/'SKILL.md').write_text('locally edited')
        r=call(INSTALL,*args,'--upgrade','--apply')
        self.assertEqual(r.returncode,2)
        self.assertEqual((dest/'SKILL.md').read_text(),'locally edited')
    def test_upgrade_creates_backup(self):
        args=['--agent','claude','--scope','user','--home',str(self.home)]
        self.assertEqual(call(INSTALL,*args,'--apply').returncode,0)
        r=call(INSTALL,*args,'--upgrade','--apply')
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertIn('previous_backup',r.stdout)
        self.assertEqual(len(list((self.home/'.claude/skills').glob('ai-native-bootstrap.backup-*'))),1)

class EvalRunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'project';self.root.mkdir()
        r=call(BOOT,'init','--project',self.root,'--apply')
        self.assertEqual(r.returncode,0,r.stderr)
    def test_empty_real_evals_are_blocked(self):
        p=call(self.root/'scripts/ai-sdlc/eval.py')
        self.assertEqual(p.returncode,2)
        self.assertIn('BLOCKED',p.stderr)
    def test_deterministic_case_actual_exit_code(self):
        cases=self.root/'evals/cases.json'
        fixture={'schema':1,'cases':[{'id':'EVAL-TEST','source':'Fixture-only, not a real product regression',
            'kind':'deterministic','argv':[PY,'-c','import sys;sys.exit(5)'], 'expected_exit_code':0,'enabled':True}]}
        cases.write_text(json.dumps(fixture))
        r=call(self.root/'scripts/ai-sdlc/eval.py')
        self.assertEqual(r.returncode,1)
        self.assertIn('FAIL',r.stdout)
        fixture['cases'][0]['expected_exit_code']=5
        cases.write_text(json.dumps(fixture))
        r=call(self.root/'scripts/ai-sdlc/eval.py')
        self.assertEqual(r.returncode,0)
        self.assertIn('PASS',r.stdout)


class PlatformCompatibilityTests(unittest.TestCase):
    def test_os_level_symlink_ancestors_are_tolerated(self):
        # macOS ships /var -> /private/var and /tmp -> /private/tmp; tempfile
        # workspaces live below them. Only the project root itself may be a
        # symlink escape; ancestor OS links must not block a valid project.
        import os, sys
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'project'; root.mkdir()
            sys.path.insert(0, str(ROOT/'scripts'))
            try:
                import _core
                got = _core.safe_project(root)
                self.assertEqual(got, Path(os.path.abspath(root)))
                self.assertTrue(got.is_dir())
            finally:
                sys.path.remove(str(ROOT/'scripts'))


if __name__=='__main__': unittest.main()
