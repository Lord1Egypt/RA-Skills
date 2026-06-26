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


class EnforcerInstallUpdatesPluginsAllowTests(unittest.TestCase):
    def test_install_merges_plugin_into_plugins_allow_via_config_set(self):
        with tempfile.TemporaryDirectory() as td:
            fake_bin = os.path.join(td, "bin")
            calls_dir = os.path.join(td, "calls")
            os.makedirs(fake_bin, exist_ok=True)
            os.makedirs(calls_dir, exist_ok=True)

            set_payload = os.path.join(td, "plugins-allow.json")

            _write_executable(
                os.path.join(fake_bin, "openclaw"),
                f"""#!/bin/sh
set -eu
cmd="$1"
shift
case "$cmd" in
  config)
    sub="$1"
    shift
    case "$sub" in
      get)
        if [ "$1" = "plugins.allow" ]; then
          printf '%s\\n' '["trusted-plugin"]'
          exit 0
        fi
        ;;
      set)
        if [ "$1" = "plugins.allow" ]; then
          printf '%s' "$2" > "{set_payload}"
          exit 0
        fi
        ;;
    esac
    ;;
  plugins)
    if [ "$1" = "install" ]; then
      exit 0
    fi
    ;;
  gateway)
    if [ "$1" = "restart" ]; then
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
                ["/bin/bash", ENFORCER, "install", "--restart"],
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            with open(set_payload, "r", encoding="utf-8") as f:
                merged = json.loads(f.read())
            self.assertEqual(merged, ["trusted-plugin", "codeflow-enforcer"])


if __name__ == "__main__":
    unittest.main()
