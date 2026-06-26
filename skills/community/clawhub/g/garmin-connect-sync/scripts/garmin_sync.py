#!/usr/bin/env python3
"""
Garmin International → China Account Sync Tool
===============================================
Reads activities from Garmin Connect International, downloads FIT files,
and uploads them to Garmin Connect China.

Usage:
  python3 garmin_sync.py sync              # One-time sync
  python3 garmin_sync.py status            # Show sync status
  python3 garmin_sync.py list [--days=7]   # Show recent activities
  python3 garmin_sync.py auth-test         # Test authentication only

Environment variables:
  GARMIN_INTL_USERNAME   - International account email
  GARMIN_INTL_PASSWORD   - International account password
  GARMIN_CN_USERNAME     - China account email
  GARMIN_CN_PASSWORD     - China account password
  GARMIN_SYNC_DIR        - Sync storage directory (default: ~/.garmin-sync)
  GARMIN_TOKEN_DIR       - Token storage directory (default: ~/.garmin-sync/tokens)
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("garmin_sync")


def get_env(name: str, required: bool = True) -> str:
    val = os.environ.get(name, "")
    if required and not val:
        logger.error("❌ Missing required env var: %s", name)
        sys.exit(1)
    return val


class GarminSync:
    def __init__(self):
        self.intl_email = get_env("GARMIN_INTL_USERNAME")
        self.intl_password = get_env("GARMIN_INTL_PASSWORD")
        self.cn_email = get_env("GARMIN_CN_USERNAME")
        self.cn_password = get_env("GARMIN_CN_PASSWORD")

        sync_dir = os.environ.get("GARMIN_SYNC_DIR", str(Path.home() / ".garmin-sync"))
        token_dir = os.environ.get(
            "GARMIN_TOKEN_DIR", str(Path(sync_dir) / "tokens")
        )

        self.sync_dir = Path(sync_dir)
        self.token_dir = Path(token_dir)
        self.fit_dir = Path(sync_dir) / "fit"
        self.state_file = Path(sync_dir) / "sync-state.json"

        self.sync_dir.mkdir(parents=True, exist_ok=True)
        self.token_dir.mkdir(parents=True, exist_ok=True)
        self.fit_dir.mkdir(parents=True, exist_ok=True)

        self.intl_api = None
        self.cn_api = None

    def _create_intl_client(self):
        """Create and authenticate international Garmin client."""
        from garminconnect import Garmin

        token_path = str(self.token_dir / "intl.json")
        api = Garmin(
            email=self.intl_email,
            password=self.intl_password,
            is_cn=False,
        )
        api.login(tokenstore=token_path)
        logger.info("✅ International account logged in: %s", api.display_name or self.intl_email)
        return api

    def _create_cn_client(self):
        """Create and authenticate China Garmin client."""
        from garminconnect import Garmin

        token_path = str(self.token_dir / "cn.json")
        api = Garmin(
            email=self.cn_email,
            password=self.cn_password,
            is_cn=True,
        )
        api.login(tokenstore=token_path)
        logger.info("✅ China account logged in: %s", api.display_name or self.cn_email)
        return api

    def test_auth(self):
        """Test authentication for both accounts."""
        try:
            logger.info("🔐 Testing international account...")
            intl = self._create_intl_client()
            profile = intl.get_full_name() or intl.display_name
            logger.info("   Name: %s", profile)

            logger.info("🔐 Testing China account...")
            cn = self._create_cn_client()
            profile_cn = cn.get_full_name() or cn.display_name
            logger.info("   Name: %s", profile_cn)

            logger.info("\n✅ Both accounts authenticated successfully!")
            return True
        except Exception as e:
            logger.error("❌ Auth test failed: %s", e)
            return False

    def get_recent_activities(self, days: int = 7, limit: int = 20):
        """List recent activities from international account."""
        if not self.intl_api:
            self.intl_api = self._create_intl_client()

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        logger.info("📋 Fetching activities from %s to %s...", start_date, end_date)
        activities = self.intl_api.get_activities_by_date(start_date, end_date)

        if not activities:
            logger.info("   No activities found.")
            return []

        logger.info("   Found %d activities:", len(activities))
        result = []
        for act in activities[:limit]:
            line = (
                f"   [{act.get('activityId')}] "
                f"{act.get('activityName', 'Unnamed')} "
                f"({act.get('activityType', {}).get('typeKey', 'unknown')}) "
                f"{act.get('startLocal', '')[:10]} "
                f"{act.get('distance', 0)/1000:.1f}km"
            )
            logger.info(line)
            result.append(act)
        return result

    def sync(self, days_back: int = 7, max_activities: int = 10):
        """
        Main sync: Read activities from international, download FIT,
        and upload to China account.
        """
        # Authenticate both accounts
        logger.info("🔐 Logging in to international account...")
        self.intl_api = self._create_intl_client()

        logger.info("🔐 Logging in to China account...")
        self.cn_api = self._create_cn_client()

        # Get recently synced IDs to avoid duplicates
        synced_ids = self._load_synced_ids()

        # Fetch recent activities from international
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")

        logger.info("📋 Fetching activities from %s to %s...", start_date, end_date)
        activities = self.intl_api.get_activities_by_date(start_date, end_date)

        if not activities:
            logger.info("✅ No new activities to sync.")
            self._save_state({"last_sync": datetime.now().isoformat()})
            return

        # Filter out already synced activities
        new_activities = [a for a in activities if a.get("activityId") not in synced_ids]

        if not new_activities:
            logger.info("✅ All %d activities already synced.", len(activities))
            self._save_state({"last_sync": datetime.now().isoformat()})
            return

        logger.info("🔄 %d new activities to sync (of %d total)...",
                     len(new_activities), len(activities))

        # Limit to avoid rate limiting
        to_sync = new_activities[:max_activities]
        success_count = 0
        fail_count = 0
        skipped = 0

        for i, act in enumerate(to_sync, 1):
            act_id = act.get("activityId")
            act_name = act.get("activityName", f"Activity_{act_id}")
            act_type = act.get("activityType", {}).get("typeKey", "unknown")
            act_date = (act.get("startLocal") or "")[:10]

            logger.info(
                "[%d/%d] Processing: %s (%s) %s",
                i, len(to_sync), act_name, act_type, act_date
            )

            try:
                # Download FIT file
                fit_bytes = self.intl_api.download_activity(
                    str(act_id),
                    self.intl_api.ActivityDownloadFormat.ORIGINAL,
                )

                # Save to temp file
                from io import BytesIO
                import zipfile

                fit_path = None
                # The download may return a zip file containing the FIT
                try:
                    with zipfile.ZipFile(BytesIO(fit_bytes)) as zf:
                        fit_files = [n for n in zf.namelist() if n.lower().endswith('.fit')]
                        if fit_files:
                            fit_path = str(self.fit_dir / fit_files[0])
                            with open(fit_path, 'wb') as f:
                                f.write(zf.read(fit_files[0]))
                        else:
                            logger.warning("   ⚠️ No FIT found in zip, trying raw bytes")
                            fit_path = str(self.fit_dir / f"{act_id}.fit")
                            with open(fit_path, 'wb') as f:
                                f.write(fit_bytes)
                except zipfile.BadZipFile:
                    fit_path = str(self.fit_dir / f"{act_id}.fit")
                    with open(fit_path, 'wb') as f:
                        f.write(fit_bytes)

                if not fit_path or not Path(fit_path).exists():
                    raise Exception("Failed to extract FIT file")

                # Upload to China account
                logger.info("   📤 Uploading to China account...")
                result = self.cn_api.upload_activity(fit_path)
                logger.info("   ✅ Uploaded successfully: %s", result)

                # Mark as synced
                synced_ids.add(str(act_id))
                success_count += 1

                # Rate limiting delay between uploads
                if i < len(to_sync):
                    delay = 5
                    logger.info("   ⏳ Waiting %ds for rate limiting...", delay)
                    time.sleep(delay)

            except Exception as e:
                err_str = str(e)
                if "duplicate" in err_str.lower() or "409" in err_str:
                    logger.info("   ⏭️ Already on China account (duplicate): %s", act_name)
                    synced_ids.add(str(act_id))
                    skipped += 1
                else:
                    logger.error("   ❌ Failed: %s", e)
                    fail_count += 1

        # Save state
        self._save_state({
            "last_sync": datetime.now().isoformat(),
            "synced_ids": list(synced_ids),
            "last_sync_summary": {
                "success": success_count,
                "fail": fail_count,
                "skipped": skipped,
                "total_new": len(new_activities),
            },
        })

        logger.info(
            "\n📊 Sync complete: ✅ %d success, ⏭️ %d skipped, ❌ %d failed (of %d new)",
            success_count, skipped, fail_count, len(new_activities)
        )

    def _load_synced_ids(self) -> set:
        """Load list of already-synced activity IDs."""
        state = self._load_state()
        return set(str(i) for i in state.get("synced_ids", []))

    def _load_state(self) -> dict:
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text())
            except (json.JSONDecodeError, Exception):
                pass
        return {}

    def _save_state(self, updates: dict):
        state = self._load_state()
        state.update(updates)
        self.state_file.write_text(json.dumps(state, indent=2, ensure_ascii=False))
        logger.debug("State saved to %s", self.state_file)

    def show_status(self):
        """Show sync status."""
        state = self._load_state()
        last_sync = state.get("last_sync", "Never")
        synced_count = len(state.get("synced_ids", []))
        summary = state.get("last_sync_summary", {})

        logger.info("📊 Garmin Sync Status")
        logger.info("   Last sync: %s", last_sync)
        logger.info("   Total synced activities: %d", synced_count)

        if summary:
            logger.info("   Last sync results:")
            logger.info("     ✅ Successful: %d", summary.get("success", 0))
            logger.info("     ⏭️ Skipped (duplicates): %d", summary.get("skipped", 0))
            logger.info("     ❌ Failed: %d", summary.get("fail", 0))

        # Check disk usage
        fit_files = list(self.fit_dir.glob("*.fit"))
        total_size = sum(f.stat().st_size for f in fit_files)
        logger.info("   Cached FIT files: %d (%.1f MB)", len(fit_files), total_size / 1024 / 1024)

        return {
            "last_sync": last_sync,
            "synced_count": synced_count,
            "summary": summary,
            "cached_fits": len(fit_files),
        }


def main():
    parser = argparse.ArgumentParser(description="Garmin International → China Sync")
    parser.add_argument(
        "command",
        choices=["sync", "status", "list", "auth-test"],
        help="Command to run",
    )
    parser.add_argument("--days", type=int, default=7, help="Days back to look (default: 7)")
    parser.add_argument("--max", type=int, default=10, help="Max activities to sync (default: 10)")

    args = parser.parse_args()
    sync = GarminSync()

    if args.command == "auth-test":
        success = sync.test_auth()
        sys.exit(0 if success else 1)

    elif args.command == "sync":
        sync.sync(days_back=args.days, max_activities=args.max)

    elif args.command == "status":
        sync.show_status()

    elif args.command == "list":
        sync.get_recent_activities(days=args.days)


if __name__ == "__main__":
    main()
