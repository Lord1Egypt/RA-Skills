import json
import os
import stat
import subprocess
import tempfile
import unittest


SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BIN_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "bin"))
ENFORCER = os.path.join(BIN_DIR, "enforcer.sh")


def _write_executable(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)


class EnforcerStatusNpxFallbackTests(unittest.TestCase):
    def test_status_detects_openclaw_via_nvm_when_path_is_missing(self):
        with tempfile.TemporaryDirectory() as td:
            fake_openclaw_bin = os.path.join(td, "fake-openclaw-bin")
            fake_home = os.path.join(td, "home")
            nvm_dir = os.path.join(fake_home, ".nvm")
            os.makedirs(fake_openclaw_bin, exist_ok=True)
            os.makedirs(nvm_dir, exist_ok=True)

            _write_executable(
                os.path.join(fake_openclaw_bin, "openclaw"),
                """#!/bin/sh
set -eu
case "${1:-}" in
  --version)
    printf '%s\n' 'openclaw 1.2.3'
    exit 0
    ;;
  plugins)
    if [ "${2:-}" = "list" ] && [ "${3:-}" = "--json" ]; then
      printf '%s\n' '[{"id":"codeflow-enforcer","enabled":true,"status":"loaded","hookCount":2}]'
      exit 0
    fi
    ;;
esac
exit 0
""",
            )
            with open(os.path.join(nvm_dir, "nvm.sh"), "w", encoding="utf-8") as f:
                f.write(f'export PATH="{fake_openclaw_bin}:$PATH"\n')

            env = dict(os.environ)
            env["HOME"] = fake_home
            env["PATH"] = "/usr/bin:/bin"

            proc = subprocess.run(
                ["/bin/bash", ENFORCER, "status", "--json"],
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            payload = json.loads(proc.stdout)
            self.assertTrue(payload["openclawCli"])
            self.assertEqual(payload["openclawLauncherKind"], "native")
            self.assertTrue(payload["pluginDetected"])
            self.assertEqual(payload["recommendation"]["action"], "none")

    def test_status_exposes_install_button_when_only_npx_is_available(self):
        with tempfile.TemporaryDirectory() as td:
            fake_bin = os.path.join(td, "bin")
            os.makedirs(fake_bin, exist_ok=True)

            _write_executable(
                os.path.join(fake_bin, "npx"),
                "#!/bin/sh\nexit 0\n",
            )

            env = dict(os.environ)
            env["HOME"] = os.path.join(td, "home")
            os.makedirs(env["HOME"], exist_ok=True)
            env["PATH"] = fake_bin + os.pathsep + "/usr/bin:/bin"

            proc = subprocess.run(
                ["/bin/bash", ENFORCER, "status", "--json"],
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            payload = json.loads(proc.stdout)
            self.assertTrue(payload["openclawCli"])
            self.assertEqual(payload["openclawLauncherKind"], "npx")
            self.assertTrue(payload["canInstall"])
            self.assertEqual(payload["recommendation"]["action"], "install")
            self.assertTrue(payload["recommendation"]["buttons"])
            self.assertEqual(payload["recommendation"]["callbackData"], "cfe:install")

    def test_status_does_not_offer_install_when_npx_reports_plugin_loaded(self):
        with tempfile.TemporaryDirectory() as td:
            fake_bin = os.path.join(td, "bin")
            os.makedirs(fake_bin, exist_ok=True)

            _write_executable(
                os.path.join(fake_bin, "npx"),
                """#!/bin/sh
set -eu
if [ "${1:-}" = "-y" ] && [ "${2:-}" = "openclaw" ] && [ "${3:-}" = "plugins" ] && [ "${4:-}" = "list" ] && [ "${5:-}" = "--json" ]; then
  printf '%s\n' '[{"id":"codeflow-enforcer","enabled":true,"status":"loaded","hookCount":2}]'
  exit 0
fi
exit 0
""",
            )

            env = dict(os.environ)
            env["HOME"] = os.path.join(td, "home")
            os.makedirs(env["HOME"], exist_ok=True)
            env["PATH"] = fake_bin + os.pathsep + "/usr/bin:/bin"

            proc = subprocess.run(
                ["/bin/bash", ENFORCER, "status", "--json"],
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            payload = json.loads(proc.stdout)
            self.assertEqual(payload["openclawLauncherKind"], "npx")
            self.assertEqual(payload["plugin"]["state"], "loaded")
            self.assertTrue(payload["pluginDetected"])
            self.assertEqual(payload["recommendation"]["action"], "none")

    def test_status_reports_restart_when_plugin_is_installed_but_not_loaded(self):
        with tempfile.TemporaryDirectory() as td:
            fake_bin = os.path.join(td, "bin")
            os.makedirs(fake_bin, exist_ok=True)

            _write_executable(
                os.path.join(fake_bin, "openclaw"),
                """#!/bin/sh
set -eu
case "${1:-}" in
  plugins)
    if [ "${2:-}" = "list" ] && [ "${3:-}" = "--json" ]; then
      printf '%s\n' '[{"id":"codeflow-enforcer","enabled":true,"status":"installed","hookCount":0}]'
      exit 0
    fi
    ;;
esac
exit 0
""",
            )

            env = dict(os.environ)
            env["HOME"] = os.path.join(td, "home")
            os.makedirs(env["HOME"], exist_ok=True)
            env["PATH"] = fake_bin + os.pathsep + "/usr/bin:/bin"

            proc = subprocess.run(
                ["/bin/bash", ENFORCER, "status", "--json"],
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            payload = json.loads(proc.stdout)
            self.assertEqual(payload["plugin"]["state"], "restart-pending")
            self.assertEqual(payload["plugin"]["status"], "installed")
            self.assertEqual(payload["recommendation"]["action"], "restart")


if __name__ == "__main__":
    unittest.main()
