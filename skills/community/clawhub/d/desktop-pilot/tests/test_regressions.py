"""Isolated wrapper tests. Fake platform adapters never control the desktop."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class WrapperTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.p = Path(self.tmp.name)
        self.bin = self.p / 'bin'
        self.bin.mkdir()
        self.state = self.p / 'desktop-pilot/overlay'
        self.state.mkdir(parents=True)
        self.log = self.p / 'calls'
        adapters = {
            'uname': '#!/bin/bash\necho "${FAKE_OS}"\n',
            'powershell.exe': '''#!/bin/bash
if [[ " $* " == *" -Command "* ]]; then
  if [[ "$*" == *GetTempPath* ]]; then printf 'C:\\\\DPTest\\\\'; fi
else printf '%s\\n' "$*" >> "$FAKE_LOG"; fi
''',
            'cygpath': '#!/bin/bash\nif [[ "$1" == -u ]]; then echo "$FAKE_TEMP"; else echo "$2"; fi\n',
            'wslpath': '#!/bin/bash\necho "$FAKE_TEMP"\n',
        }
        for name, content in adapters.items():
            f = self.bin / name
            f.write_text(content)
            f.chmod(0o755)
        (self.p / 'desktop-pilot.wtemp').write_text('C:\\DPTest\\')
        # Whitelist only fixture values; do not copy ambient credentials into children.
        self.env = {'PATH': f'{self.bin}:/usr/bin:/bin',
                    'FAKE_TEMP': str(self.p), 'FAKE_LOG': str(self.log),
                    'XDG_RUNTIME_DIR': str(self.p), 'XDG_CONFIG_HOME': str(self.p/'config'),
                    'DESKTOP_PILOT_AUTO_OVERLAY': '0'}

    def run_cli(self, platform, *args):
        return subprocess.run(['bash', str(ROOT/'scripts/desktop.sh'), *args],
                              env=dict(self.env, FAKE_OS=platform), capture_output=True, text=True)

    def test_stop_survives_all_restart_and_action_paths(self):
        for platform in ('MINGW64_NT', 'Linux'):
            for args in [('overlay','start'), ('overlay','text','--text','restart'),
                         ('overlay','lock'), ('type','--text','NOT SENT'),
                         ('key','--keys','enter'), ('mouse','--x','1','--y','1'),
                         ('screenshot',), ('windows',)]:
                with self.subTest(platform=platform, args=args):
                    flag=self.state/'stop.flag'
                    flag.write_text('user stop')
                    result=self.run_cli(platform,*args)
                    self.assertEqual(result.returncode,3,result.stderr)
                    self.assertTrue(flag.exists())
                    self.assertFalse(self.log.exists(), 'Backend must not run after Stop')

    def test_clear_is_explicit_resume(self):
        for platform in ('MINGW64_NT', 'Linux'):
            (self.state/'stop.flag').write_text('stop')
            r=self.run_cli(platform,'overlay','clear')
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertFalse((self.state/'stop.flag').exists())
            r=self.run_cli(platform,'windows')
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertIn('desktop.ps1',self.log.read_text())
            self.log.unlink()

    def test_invalid_parameters_rejected_before_execution(self):
        for args in [('overlay','start','--idle',"1'; whoami; '"),
                     ('overlay','start','--idle','0'),('overlay','start','--idle','9999'),
                     ('overlay','start','--lock','yes'),('overlay','start','--capture','2'),
                     ('type','--text'),('unknown',)]:
            with self.subTest(args=args):
                r=self.run_cli('MINGW64_NT',*args)
                self.assertNotEqual(r.returncode,0)
                self.assertFalse(self.log.exists())

    def test_auto_mode_cannot_clear_stop(self):
        self.env['DESKTOP_PILOT_AUTO_OVERLAY']='1'
        flag=self.state/'stop.flag';flag.write_text('stop')
        r=self.run_cli('Linux','windows')
        self.assertEqual(r.returncode,3,r.stderr)
        self.assertTrue(flag.exists())
        self.assertFalse(self.log.exists())

if __name__ == '__main__':
    unittest.main(verbosity=2)
