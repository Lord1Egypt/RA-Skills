"""Offline smoke tests; no Gmail, OAuth, or merchant connection is required."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import discover_store
import import_browser_discovery


class RuntimeTests(unittest.TestCase):
    def test_memory_permissions_and_confirmation_events_are_independent(self):
        with tempfile.TemporaryDirectory() as state:
            env = {**os.environ, "OPENCLAW_STATE_DIR": state}
            runtime = Path(state) / "ecommerce-gmail-customer-service"

            def call(*parts, check=True):
                return subprocess.run(
                    [sys.executable, *parts],
                    cwd=ROOT,
                    env=env,
                    check=check,
                    capture_output=True,
                    text=True,
                )

            def write_issues(path: Path, *categories: tuple[str, str]):
                path.write_text(
                    json.dumps(
                        {
                            "atomic_issues": [
                                {"intent_id": intent, "scenario_key": scenario}
                                for intent, scenario in categories
                            ]
                        }
                    ),
                    encoding="utf-8",
                )

            call("scripts/configure.py", "init")
            call("scripts/configure.py", "verify")
            help_text = call("scripts/configure.py", "--help").stdout
            self.assertNotIn(" edit ", help_text)
            self.assertIn(" show ", help_text)
            config_path = runtime / "config.json"
            config = json.loads(config_path.read_text())
            self.assertEqual(config["version"], 7)
            self.assertTrue((runtime / "auto_reply_permissions.json").is_file())
            self.assertTrue((runtime / "pending_category_confirmations.json").is_file())

            config["gmail"]["account"] = "support@example.com"
            config_path.write_text(json.dumps(config), encoding="utf-8")
            shown_config = call("scripts/configure.py", "show", "config").stdout
            self.assertIn("[REDACTED]", shown_config)
            self.assertNotIn("support@example.com", shown_config)
            self.assertEqual(
                Path(call("scripts/configure.py", "path", "user-memory").stdout.strip()),
                runtime / "user_memory.md",
            )
            self.assertIn(
                "ECS_MEMORY_JSON_BEGIN",
                call("scripts/configure.py", "show", "user-memory").stdout,
            )

            memory_update = Path(state) / "memory-update.json"
            memory_update.write_text(
                json.dumps(
                    {
                        "handling_playbooks": [
                            {
                                "intent_id": "SHIP-DELAY",
                                "scenario_key": "scanned",
                                "status": "approved",
                                "handling_steps": ["Check the latest carrier scan"],
                                "observation_ids": ["offline-1"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            unconfirmed_memory = call(
                "scripts/user_memory.py",
                "merge",
                "--source",
                "onboarding",
                "--input",
                str(memory_update),
                check=False,
            )
            self.assertNotEqual(unconfirmed_memory.returncode, 0)
            self.assertIn("--confirm-owner-request", unconfirmed_memory.stderr)
            call(
                "scripts/user_memory.py",
                "merge",
                "--source",
                "onboarding",
                "--input",
                str(memory_update),
                "--confirm-owner-request",
                "--delete-input",
            )
            self.assertFalse(memory_update.exists())

            permission_in_memory = Path(state) / "invalid-memory-update.json"
            permission_in_memory.write_text(
                json.dumps(
                    {
                        "handling_playbooks": [
                            {
                                "intent_id": "SHIP-DELAY",
                                "scenario_key": "scanned",
                                "auto_send_approved": True,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            rejected = call(
                "scripts/user_memory.py",
                "merge",
                "--source",
                "onboarding",
                "--input",
                str(permission_in_memory),
                "--confirm-owner-request",
                check=False,
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("stored separately", rejected.stderr)

            unconfirmed_global = call(
                "scripts/configure.py", "set", "auto-send", "on", check=False
            )
            self.assertNotEqual(unconfirmed_global.returncode, 0)
            self.assertIn("--confirm-owner-request", unconfirmed_global.stderr)
            call(
                "scripts/configure.py",
                "set",
                "auto-send",
                "on",
                "--confirm-owner-request",
            )

            issue_input = Path(state) / "issues.json"
            write_issues(issue_input, ("SHIP-DELAY", "scanned"))
            missing_permission = call(
                "scripts/auto_reply_permissions.py",
                "check",
                "--input",
                str(issue_input),
                check=False,
            )
            self.assertNotEqual(missing_permission.returncode, 0)
            self.assertIn("auto_reply_permission_missing", missing_permission.stdout)

            event_input = Path(state) / "event-issues.json"
            write_issues(event_input, ("SHIP-DELAY", "scanned"))
            event = json.loads(
                call(
                    "scripts/auto_reply_permissions.py",
                    "record-sent",
                    "--source",
                    "gmail-sent",
                    "--draft-id",
                    "draft-a",
                    "--thread-id",
                    "thread-a",
                    "--sent-message-id",
                    "message-a",
                    "--input",
                    str(event_input),
                    "--delete-input",
                ).stdout
            )
            self.assertTrue(event["created"])
            self.assertFalse(event_input.exists())
            permissions_path = runtime / "auto_reply_permissions.json"
            permissions = json.loads(permissions_path.read_text())
            self.assertFalse(permissions["categories"]["SHIP-DELAY::scanned"]["enabled"])
            disabled_permission = call(
                "scripts/auto_reply_permissions.py",
                "check",
                "--input",
                str(issue_input),
                check=False,
            )
            self.assertNotEqual(disabled_permission.returncode, 0)
            self.assertIn("auto_reply_permission_disabled", disabled_permission.stdout)
            no_owner_confirmation = call(
                "scripts/auto_reply_permissions.py",
                "confirm",
                "--event-id",
                event["event_id"],
                "--intent-id",
                "SHIP-DELAY",
                "--scenario-key",
                "scanned",
                "on",
                check=False,
            )
            self.assertNotEqual(no_owner_confirmation.returncode, 0)
            self.assertIn("--confirm-owner-request", no_owner_confirmation.stderr)
            call(
                "scripts/auto_reply_permissions.py",
                "confirm",
                "--event-id",
                event["event_id"],
                "--intent-id",
                "SHIP-DELAY",
                "--scenario-key",
                "scanned",
                "on",
                "--confirm-owner-request",
            )
            self.assertTrue(
                json.loads(
                    call(
                        "scripts/auto_reply_permissions.py",
                        "check",
                        "--input",
                        str(issue_input),
                    ).stdout
                )["allowed"]
            )

            call(
                "scripts/configure.py",
                "set",
                "memory-usage",
                "off",
                "--confirm-owner-request",
            )
            self.assertTrue(
                json.loads(
                    call(
                        "scripts/auto_reply_permissions.py",
                        "check",
                        "--input",
                        str(issue_input),
                    ).stdout
                )["allowed"]
            )
            clear_without_owner = call(
                "scripts/user_memory.py",
                "clear",
                "--confirm-delete-all",
                check=False,
            )
            self.assertNotEqual(clear_without_owner.returncode, 0)
            clear_without_second_confirmation = call(
                "scripts/user_memory.py",
                "clear",
                "--confirm-owner-request",
                check=False,
            )
            self.assertNotEqual(clear_without_second_confirmation.returncode, 0)
            call(
                "scripts/user_memory.py",
                "clear",
                "--confirm-owner-request",
                "--confirm-delete-all",
            )
            memory_text = (runtime / "user_memory.md").read_text(encoding="utf-8")
            self.assertIn('"handling_playbooks": []', memory_text)
            self.assertTrue(
                json.loads(permissions_path.read_text())["categories"]["SHIP-DELAY::scanned"][
                    "enabled"
                ]
            )
            self.assertTrue(
                json.loads(
                    call(
                        "scripts/auto_reply_permissions.py",
                        "check",
                        "--input",
                        str(issue_input),
                    ).stdout
                )["allowed"]
            )
            call(
                "scripts/auto_reply_permissions.py",
                "disable",
                "--intent-id",
                "SHIP-DELAY",
                "--scenario-key",
                "scanned",
                "--confirm-owner-request",
            )
            self.assertNotEqual(
                call(
                    "scripts/auto_reply_permissions.py",
                    "check",
                    "--input",
                    str(issue_input),
                    check=False,
                ).returncode,
                0,
            )

            openclaw_input = Path(state) / "openclaw-issues.json"
            write_issues(openclaw_input, ("CANCEL-ORDER", "before-fulfillment"))
            openclaw_event = json.loads(
                call(
                    "scripts/auto_reply_permissions.py",
                    "record-sent",
                    "--source",
                    "openclaw-sent",
                    "--draft-id",
                    "draft-b",
                    "--thread-id",
                    "thread-b",
                    "--sent-message-id",
                    "message-b",
                    "--input",
                    str(openclaw_input),
                ).stdout
            )
            call(
                "scripts/auto_reply_permissions.py",
                "confirm",
                "--event-id",
                openclaw_event["event_id"],
                "--intent-id",
                "CANCEL-ORDER",
                "--scenario-key",
                "before-fulfillment",
                "on",
                "--confirm-owner-request",
            )
            self.assertEqual(
                json.loads(call("scripts/auto_reply_permissions.py", "status").stdout)[
                    "enabled_categories"
                ],
                1,
            )
            call(
                "scripts/auto_reply_permissions.py",
                "disable-all",
                "--confirm-owner-request",
            )
            status = json.loads(call("scripts/auto_reply_permissions.py", "status").stdout)
            self.assertEqual(status["enabled_categories"], 0)
            self.assertIn('"handling_playbooks": []', (runtime / "user_memory.md").read_text())

            expiry_input = Path(state) / "expiry-issues.json"
            write_issues(expiry_input, ("SHIP-STATUS", "waiting"))
            expiry_event = json.loads(
                call(
                    "scripts/auto_reply_permissions.py",
                    "record-sent",
                    "--source",
                    "gmail-sent",
                    "--draft-id",
                    "draft-expired",
                    "--thread-id",
                    "thread-expired",
                    "--sent-message-id",
                    "message-expired",
                    "--input",
                    str(expiry_input),
                ).stdout
            )
            pending_path = runtime / "pending_category_confirmations.json"
            pending = json.loads(pending_path.read_text())
            pending["events"][expiry_event["event_id"]]["created_at"] = (
                "2000-01-01T00:00:00+00:00"
            )
            pending_path.write_text(json.dumps(pending), encoding="utf-8")
            purge_result = json.loads(
                call("scripts/auto_reply_permissions.py", "purge-events").stdout
            )
            self.assertEqual(purge_result["deleted"], 1)
            self.assertNotIn(
                expiry_event["event_id"],
                json.loads(pending_path.read_text())["events"],
            )

            before = Path(state) / "before.txt"
            after = Path(state) / "after.txt"
            before.write_text("Hello customer, your order 123456 is in transit.")
            after.write_text("Hello, I checked the latest carrier scan for your order 123456.")
            disabled_snapshot = call(
                "scripts/draft_learning.py",
                "snapshot",
                "--draft-id",
                "d1",
                "--thread-id",
                "t1",
                "--message-id",
                "m1",
                "--intent",
                "SHIP-DELAY",
                "--body-file",
                str(before),
                check=False,
            )
            self.assertNotEqual(disabled_snapshot.returncode, 0)
            call(
                "scripts/configure.py",
                "set",
                "learning",
                "on",
                "--confirm-owner-request",
            )
            call(
                "scripts/draft_learning.py",
                "snapshot",
                "--draft-id",
                "d1",
                "--thread-id",
                "t1",
                "--message-id",
                "m1",
                "--intent",
                "SHIP-DELAY",
                "--body-file",
                str(before),
            )
            self.assertTrue(
                json.loads(
                    call(
                        "scripts/draft_learning.py",
                        "compare",
                        "--draft-id",
                        "d1",
                        "--body-file",
                        str(after),
                    ).stdout
                )["changed"]
            )
            draft_update = Path(state) / "draft-update.json"
            draft_update.write_text(
                json.dumps(
                    {
                        "style_profile": {
                            "items": [
                                {
                                    "key": "opening",
                                    "summary": "Acknowledge the issue before the status.",
                                    "observation_id": "draft-d1-v1",
                                }
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )
            call(
                "scripts/user_memory.py",
                "merge",
                "--source",
                "draft-edit",
                "--input",
                str(draft_update),
                "--delete-input",
            )
            self.assertFalse(draft_update.exists())
            call("scripts/draft_learning.py", "finalize", "--draft-id", "d1")

            reports_dir = runtime / "case-reports"
            reports_dir.mkdir()
            expired_report = reports_dir / "expired.json"
            expired_report.write_text("{}")
            os.utime(expired_report, (0, 0))
            call("scripts/retention.py", "purge")
            self.assertFalse(expired_report.exists())

    def test_migration_storefront_and_legacy_permission_flags_fail_closed(self):
        with tempfile.TemporaryDirectory() as state:
            env = {**os.environ, "OPENCLAW_STATE_DIR": state}
            runtime = Path(state) / "ecommerce-gmail-customer-service"

            def call(*parts, check=True):
                return subprocess.run(
                    [sys.executable, *parts],
                    cwd=ROOT,
                    env=env,
                    check=check,
                    capture_output=True,
                    text=True,
                )

            call("scripts/configure.py", "init")
            config_path = runtime / "config.json"
            discovery_path = runtime / "store-discovery.json"
            discovery_path.write_text(
                json.dumps(
                    {
                        "storefront_url": "https://shop.example/",
                        "public_sources_only": True,
                    }
                ),
                encoding="utf-8",
            )
            legacy = json.loads(config_path.read_text())
            legacy["version"] = 4
            legacy["automation"]["send_mode"] = "auto_send"
            legacy["automation"]["auto_send_allowlist"] = ["customer@example.com"]
            legacy["storefront"].update(
                {
                    "status": "confirmed",
                    "url": "https://shop.example/",
                    "discovery_file": str(discovery_path),
                    "owner_confirmed_at": "2026-01-01T00:00:00+00:00",
                }
            )
            config_path.write_text(json.dumps(legacy), encoding="utf-8")
            memory_path = runtime / "user_memory.md"
            text = memory_path.read_text(encoding="utf-8")
            memory_payload = {
                "schema_version": 4,
                "history_learning": {"status": "not_started", "window_days": 30},
                "style_profile": {"status": "not_reviewed", "items": []},
                "handling_playbooks": [
                    {
                        "intent_id": "SHIP-DELAY",
                        "scenario_key": "scanned",
                        "status": "approved",
                        "auto_send_approved": True,
                        "auto_send_approved_at": "2026-01-01T00:00:00+00:00",
                    }
                ],
                "updated_at": None,
            }
            replacement = "<!-- ECS_MEMORY_JSON_BEGIN -->\n```json\n" + json.dumps(
                memory_payload, indent=2
            ) + "\n```\n<!-- ECS_MEMORY_JSON_END -->"
            memory_path.write_text(
                text.split("<!-- ECS_MEMORY_JSON_BEGIN -->", 1)[0]
                + replacement
                + text.split("<!-- ECS_MEMORY_JSON_END -->", 1)[1],
                encoding="utf-8",
            )

            call("scripts/configure.py", "init")
            migrated = json.loads(config_path.read_text())
            self.assertEqual(migrated["version"], 7)
            self.assertEqual(migrated["automation"]["send_mode"], "draft_only")
            self.assertNotIn("auto_send_allowlist", migrated["automation"])
            self.assertEqual(migrated["storefront"]["status"], "discovered")
            self.assertIsNone(migrated["storefront"]["owner_confirmed_at"])
            self.assertNotIn("auto_send_approved", memory_path.read_text())
            permissions = json.loads((runtime / "auto_reply_permissions.json").read_text())
            self.assertFalse(permissions["categories"]["SHIP-DELAY::scanned"]["enabled"])

            unconfirmed = call(
                "scripts/configure.py", "storefront", "confirmed", check=False
            )
            self.assertNotEqual(unconfirmed.returncode, 0)
            self.assertIn("--confirm-owner-request", unconfirmed.stderr)
            call(
                "scripts/configure.py",
                "storefront",
                "confirmed",
                "--confirm-owner-request",
            )
            self.assertEqual(
                json.loads(config_path.read_text())["storefront"]["status"], "confirmed"
            )
            call("scripts/configure.py", "verify")

    def test_public_storefront_parser_and_network_guard(self):
        html = """
        <html><head><title>Example Store</title>
        <script src="https://cdn.shopify.com/theme.js"></script>
        <script type="application/ld+json">
        {"@context": "https://schema.org", "@type": "Product", "name": "Trail Bottle", "sku": "TB-1", "url": "/products/trail-bottle", "offers": {"price": "24.00", "priceCurrency": "USD", "availability": "https://schema.org/InStock"}}
        </script></head><body>
        <p>Summer sale: save 20% today.</p>
        <a href="/policies/refund-policy">Refund policy</a>
        <a href="/products/trail-bottle">Trail Bottle</a>
        </body></html>
        """
        result = discover_store.analyze_html(html, "https://shop.example/")
        self.assertEqual(result["platform"]["name"], "shopify")
        self.assertEqual(result["products"][0]["sku"], "TB-1")
        self.assertEqual(result["policy_links"][0]["kind"], "refund")
        self.assertTrue(result["campaign_evidence"])
        with self.assertRaises(ValueError):
            discover_store.validate_public_url("http://127.0.0.1/private")
        confirmed_storefront = {
            "status": "confirmed",
            "url": "https://shop.example/",
            "owner_confirmed_at": "2026-01-01T00:00:00+00:00",
        }
        self.assertEqual(
            discover_store.resolve_discovery_url(
                None, confirmed_storefront, owner_confirmed_request=False
            ),
            "https://shop.example/",
        )
        with self.assertRaisesRegex(ValueError, "previously owner-confirmed"):
            discover_store.resolve_discovery_url(
                None,
                {"status": "discovered", "url": "https://shop.example/"},
                owner_confirmed_request=False,
            )
        with self.assertRaisesRegex(ValueError, "--confirm-owner-request"):
            discover_store.resolve_discovery_url(
                "https://new-shop.example/",
                confirmed_storefront,
                owner_confirmed_request=False,
            )

    def test_guarded_browser_discovery_import(self):
        snapshot = {
            "storefront_url": "https://shop.example/",
            "public_sources_only": True,
            "read_only": True,
            "fallback_reason": "direct_fetch_failed",
            "browser_tool": "browser",
            "robots": {"status": "enforced_by_browser_tool", "respected": True},
            "platform": {
                "name": "shopify",
                "confidence": 0.9,
                "evidence": ["Shopify marker on a public page"],
            },
            "products": [
                {
                    "name": "Trail Bottle",
                    "url": "https://shop.example/products/trail-bottle",
                    "source_url": "https://shop.example/products/trail-bottle",
                    "price": "24.00",
                    "currency": "USD",
                }
            ],
            "campaigns": [
                {
                    "evidence": "Summer sale: save 20% today.",
                    "url": "https://shop.example/collections/sale",
                }
            ],
            "policies": [
                {
                    "kind": "refund",
                    "title": "Refund policy",
                    "url": "https://shop.example/policies/refund-policy",
                    "text_excerpt": "Returns are accepted within 30 days.",
                }
            ],
            "sources": [{"url": "https://shop.example/", "type": "page"}],
            "warnings": [],
        }
        normalized = import_browser_discovery.normalize_snapshot(snapshot)
        self.assertEqual(normalized["discovery_method"], "browser_fallback")
        self.assertTrue(normalized["read_only"])
        self.assertEqual(
            normalized["products"][0]["status"],
            "public_source_unverified_applicability",
        )
        cross_host = json.loads(json.dumps(snapshot))
        cross_host["policies"][0]["url"] = "https://support.example.net/refunds"
        with self.assertRaises(ValueError):
            import_browser_discovery.normalize_snapshot(cross_host)

        with tempfile.TemporaryDirectory() as state:
            env = {**os.environ, "OPENCLAW_STATE_DIR": state}
            subprocess.run(
                [sys.executable, "scripts/configure.py", "init"],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            input_path = Path(state) / "browser-input.json"
            input_path.write_text(json.dumps(snapshot), encoding="utf-8")
            unconfirmed = subprocess.run(
                [
                    sys.executable,
                    "scripts/import_browser_discovery.py",
                    "--input",
                    str(input_path),
                ],
                cwd=ROOT,
                env=env,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(unconfirmed.returncode, 0)
            self.assertIn("--confirm-owner-request", unconfirmed.stderr)
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/import_browser_discovery.py",
                    "--input",
                    str(input_path),
                    "--confirm-owner-request",
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            summary = json.loads(result.stdout)
            self.assertEqual(summary["discovery_method"], "browser_fallback")
            output = Path(summary["output"])
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["platform"]["name"], "shopify")
            config_path = Path(state) / "ecommerce-gmail-customer-service" / "config.json"
            imported_storefront = json.loads(config_path.read_text())["storefront"]
            self.assertEqual(imported_storefront["status"], "discovered")
            self.assertIsNone(imported_storefront["owner_confirmed_at"])


if __name__ == "__main__":
    unittest.main()
