import importlib.util
import os
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "esa_acme_issue.py"
SPEC = importlib.util.spec_from_file_location("esa_acme_issue", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class DomainPlanTests(unittest.TestCase):
    def test_build_domain_plan_prefers_non_wildcard_primary(self):
        plan = MODULE.build_domain_plan(["*.example.com", "example.com", "*.example.com"])
        self.assertEqual(plan["primary_domain"], "example.com")
        self.assertEqual(plan["issue_domains"], ["example.com", "*.example.com"])
        self.assertEqual(plan["base_domain"], "example.com")
        self.assertEqual(plan["cert_basename"], "example.com")

    def test_build_domain_plan_keeps_wildcard_only_request(self):
        plan = MODULE.build_domain_plan(["*.example.com"])
        self.assertEqual(plan["primary_domain"], "*.example.com")
        self.assertEqual(plan["issue_domains"], ["*.example.com"])
        self.assertEqual(plan["base_domain"], "example.com")
        self.assertEqual(plan["cert_basename"], "example.com")

    def test_build_domain_plan_rejects_invalid_domain(self):
        with self.assertRaises(ValueError):
            MODULE.build_domain_plan(["bad..example.com"])


class ParsingTests(unittest.TestCase):
    def test_parse_challenges_reads_multiple_blocks(self):
        output = """
        Domain: '*.example.com'
        TXT value: 'token-one'

        Domain: '_acme-challenge.example.com'
        TXT value: 'token-two'
        """
        self.assertEqual(
            MODULE.parse_challenges(output),
            [
                {"fqdn": "*.example.com", "token": "token-one"},
                {"fqdn": "_acme-challenge.example.com", "token": "token-two"},
            ],
        )

    def test_record_type_for_ip_supports_ipv4_and_ipv6(self):
        self.assertEqual(MODULE.record_type_for_ip("1.2.3.4"), "A")
        self.assertEqual(MODULE.record_type_for_ip("2001:db8::1"), "AAAA")

    def test_normalize_ip_canonicalizes_ipv6(self):
        self.assertEqual(MODULE.normalize_ip("2001:0db8:0000::0001"), "2001:db8::1")

    def test_parse_ensure_a_records_validates_and_trims(self):
        self.assertEqual(
            MODULE.parse_ensure_a_records([" test.example.com = 1.2.3.4 ", "ipv6.example.com=2001:db8::1"]),
            [("test.example.com", "1.2.3.4"), ("ipv6.example.com", "2001:db8::1")],
        )


class CommandBuildTests(unittest.TestCase):
    def test_build_issue_and_renew_commands(self):
        self.assertEqual(
            MODULE.build_issue_command("/mock/acme.sh", ["example.com", "*.example.com"]),
            [
                "/mock/acme.sh",
                "--issue",
                "--dns",
                "-d",
                "example.com",
                "-d",
                "*.example.com",
                "--yes-I-know-dns-manual-mode-enough-go-ahead-please",
                "--keylength",
                "ec-256",
            ],
        )
        self.assertEqual(
            MODULE.build_renew_command("/mock/acme.sh", "example.com"),
            [
                "/mock/acme.sh",
                "--renew",
                "-d",
                "example.com",
                "--ecc",
                "--yes-I-know-dns-manual-mode-enough-go-ahead-please",
                "--keylength",
                "ec-256",
            ],
        )


class ArgParseTests(unittest.TestCase):
    def test_install_cert_is_opt_in(self):
        args = MODULE.parse_args(["-d", "example.com"])
        self.assertFalse(args.install_cert)

    def test_install_cert_flag_enables_installation(self):
        args = MODULE.parse_args(["-d", "example.com", "--install-cert"])
        self.assertTrue(args.install_cert)

    def test_parse_args_supports_alibabacloud_env_aliases(self):
        with patch.dict(
            os.environ,
            {
                "ALIBABACLOUD_ACCESS_KEY_ID": "ak",
                "ALIBABACLOUD_ACCESS_KEY_SECRET": "sk",
                "ALIBABACLOUD_SECURITY_TOKEN": "sts",
                "ALIBABACLOUD_ESA_REGION": "ap-southeast-1",
            },
            clear=False,
        ):
            args = MODULE.parse_args(["-d", "example.com"])
        self.assertEqual(args.ak, "ak")
        self.assertEqual(args.sk, "sk")
        self.assertEqual(args.sts_token, "sts")
        self.assertEqual(args.region, "ap-southeast-1")


class EsaRegionTests(unittest.TestCase):
    def test_discover_regions_falls_back_to_candidates_when_describe_regions_missing(self):
        client = {"region": "ap-southeast-1"}
        with patch.object(MODULE, "esa_req", side_effect=RuntimeError("ESA API HTTP 404: InvalidAction.NotFound")):
            regions = MODULE._discover_esa_regions(client, preferred_region="ap-southeast-7")
        self.assertEqual(regions[0:3], ["ap-southeast-7", "ap-southeast-1", "cn-hangzhou"])
        self.assertIn("eu-central-1", regions)

    def test_resolve_site_context_passes_region_hint_into_auto_detection(self):
        with patch.object(MODULE, "make_acs_client", side_effect=["probe-client", "active-client"]) as make_client_mock, \
             patch.object(MODULE, "auto_detect_region", return_value=("ap-southeast-1", "site-1", "dogeow.com")) as auto_detect_mock:
            client, site_id, zone = MODULE.resolve_site_context("ak", "sk", None, "dogeow.com", region="ap-southeast-7")
        self.assertEqual((client, site_id, zone), ("active-client", "site-1", "dogeow.com"))
        auto_detect_mock.assert_called_once_with("probe-client", "dogeow.com", preferred_region="ap-southeast-7")
        self.assertEqual(make_client_mock.call_args_list[0].args, ("ak", "sk", "ap-southeast-7"))


class CommandTests(unittest.TestCase):
    def test_run_returns_not_found_for_missing_command(self):
        code, out = MODULE.run(["definitely-not-a-command-123"])
        self.assertEqual(code, 127)
        self.assertIn("command not found", out)


if __name__ == "__main__":
    unittest.main()
