import sys
import subprocess
from pathlib import Path
from argparse import ArgumentParser, Namespace
from ghostclaw.cli.commander import Command

class UpdateCommand(Command):
    @property
    def name(self) -> str:
        return "update"

    @property
    def description(self) -> str:
        return "Self-update Ghostclaw via pip or git"

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    async def execute(self, args: Namespace) -> int:
        print("🔄 Checking for Ghostclaw updates...")
        package_root = Path(__file__).parent.parent.parent.parent
        try:
            is_git = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=package_root,
                capture_output=True,
                text=True,
                check=False
            ).returncode == 0

            if is_git:
                print(f"Detected git repository at {package_root}. Pulling latest changes...")
                subprocess.run(["git", "pull"], cwd=package_root, check=True)
                print("✅ Updated via git.")
                subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], cwd=package_root, check=True)
                return 0

        except Exception as e:
            print(f"⚠️ Git update failed or skipped: {e}")

        try:
            print("Updating via pip...")
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "ghostclaw"], check=True)
            print("✅ Updated via pip.")
            return 0
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to update via pip: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"❌ Error during update: {e}", file=sys.stderr)
            return 1
