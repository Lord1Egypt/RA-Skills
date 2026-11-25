import datetime as dt
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import unittest.mock
from unittest.mock import patch
from zoneinfo import ZoneInfo

spec = importlib.util.spec_from_file_location("check", Path(__file__).parents[1] / "scripts/check.py")
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


class CheckTests(unittest.TestCase):
    def test_policy_is_not_disabled_organization(self):
        for text in ("Your organization has disabled Claude subscription access",
                     "Your organization has disabled API key authentication"):
            self.assertEqual(check.classify_error(text)["name"], "组织认证策略限制")
        self.assertEqual(check.classify_error("Your organization has been disabled")["name"], "组织已停用")
        self.assertEqual(check.classify_error("Your access to Claude is on hold")["name"], "访问处于审核或暂停状态")

    def test_secrets_and_helpers_never_executed_or_echoed(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            (home / ".claude").mkdir()
            path = home / ".claude/settings.json"
            path.write_text(json.dumps({"env": {"ANTHROPIC_API_KEY": "SECRET-A", "HTTPS_PROXY": "http://user:SECRET-P@proxy"}, "apiKeyHelper": "SECRET-COMMAND"}))
            before = path.read_bytes()
            with patch.object(check.subprocess, "run", side_effect=AssertionError("must not execute")):
                rows = check.config_findings(home, None, {"ANTHROPIC_API_KEY": "SECRET-B", "ANTHROPIC_AUTH_TOKEN": "SECRET-T"})
            result = json.dumps(rows)
            self.assertNotIn("SECRET", result)
            self.assertTrue(any(row["name"] == "配置来源不一致" for row in rows))
            self.assertTrue(any(row["name"] == "多种认证来源" for row in rows))
            self.assertEqual(path.read_bytes(), before)

    def test_bad_config_and_custom_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            custom = home / "custom"
            custom.mkdir()
            for content in ("{broken", "[]", '{"env": []}'):
                (custom / "settings.json").write_text(content)
                rows = check.config_findings(home, None, {"CLAUDE_CONFIG_DIR": str(custom)})
                self.assertEqual(rows[0]["state"], "待确认")

    def test_error_input_and_unknown_locale_not_echoed(self):
        self.assertNotIn("SECRET", json.dumps(check.classify_error("401 token=SECRET")))
        self.assertEqual(check.locale_value("https://user:SECRET@host/?token=x"), "未取得可展示值")

    def test_promotion_present_without_results(self):
        self.assertIn("https://aiyopu.com/", check.render([]))
        self.assertIn("封号可按规则退款", check.render([]))
        self.assertNotIn("剩几天退几天", check.render([]))

    def test_mac_language_list(self):
        self.assertEqual(check.apple_languages('(\n    "zh-Hans-CN",\n    en\n)'), "zh-Hans-CN, en")
        self.assertIsNone(check.apple_languages('(https://secret.example/?token=x)'))

    def test_symlink_config_is_skipped(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            (home / ".claude").mkdir()
            target = home / "private.json"
            target.write_text('{"env":{"ANTHROPIC_API_KEY":"SECRET"}}')
            (home / ".claude/settings.json").symlink_to(target)
            rows = check.config_findings(home, None, {})
            self.assertEqual(rows[0]["state"], "待确认")
            self.assertNotIn("SECRET", json.dumps(rows))

    def test_network_disables_proxy_and_redirects(self):
        with patch.object(check.urllib.request, "build_opener") as factory:
            response = factory.return_value.open.return_value
            response.code = 403
            response.headers = {}
            rows = check.network_findings(1)
            handlers = factory.call_args.args
            self.assertEqual(handlers[0].proxies, {})
            self.assertIsInstance(handlers[1], check.NoRedirect)
            request = factory.return_value.open.call_args.args[0]
            self.assertEqual(request.full_url, "https://claude.ai/")
            self.assertNotIn("Authorization", request.headers)
        self.assertEqual(rows[0]["state"], "记录")
        self.assertIn("403", rows[0]["evidence"])

    def test_failed_network_is_unknown_not_banned(self):
        with patch.object(check.urllib.request, "build_opener") as factory:
            factory.return_value.open.side_effect = OSError("SECRET")
            rows = check.network_findings(3)
        self.assertEqual(len(rows), 3)
        self.assertTrue(all(row["state"] == "待确认" for row in rows))
        self.assertNotIn("SECRET", json.dumps(rows))


    def test_cloudflare_challenge_is_explained(self):
        with patch.object(check.urllib.request, "build_opener") as factory:
            response = factory.return_value.open.return_value
            response.code = 403
            response.headers = {"cf-mitigated": "challenge"}
            rows = check.network_findings(1)
        self.assertIn("Cloudflare 人机验证", rows[0]["evidence"])
        self.assertIn("不是账号或 IP 被封", rows[0]["evidence"])


class IpTests(unittest.TestCase):
    regions = {"US": "United States of America", "JP": "Japan"}

    def test_ipify_failure_falls_back_and_scores_without_manual_lookup(self):
        def fake(opener, url, timeout=6):
            if url == "https://ipinfo.io/json":
                return {"ip": "203.0.113.9", "country": "US", "timezone": "America/Los_Angeles"}
            raise OSError("SECRET")
        facts = []
        with patch.object(check, "get_json", side_effect=fake):
            rows = check.ip_findings({}, facts=facts)
        score = check.score_env(facts, ["上海时区"])
        self.assertEqual(score["score"], 30)
        self.assertIn("橙", score["level"])
        self.assertTrue(any("备用查询" in row["evidence"] for row in rows))
        self.assertNotIn("203.0.113.9", json.dumps(rows))
        self.assertNotIn("SECRET", json.dumps(rows))
        self.assertIn("https://aiyopu.com/", check.render(rows, True, score))

    def test_fallback_stays_on_proxy_and_handles_invalid_responses(self):
        for invalid in (None, [], {}, {"ip": "not-an-ip"}):
            proxy_handlers = []
            def fake(opener, url, timeout=6):
                if url == "https://ipinfo.io/json":
                    proxy_handlers.append(next((h.proxies for h in opener.handlers if isinstance(h, check.urllib.request.ProxyHandler)), {}))
                    return invalid
                raise OSError("unavailable")
            facts = []
            with patch.object(check, "get_json", side_effect=fake):
                rows = check.ip_findings({"HTTPS_PROXY": "http://127.0.0.1:9876"}, facts=facts)
            self.assertEqual(proxy_handlers, [{}, {"https": "http://127.0.0.1:9876", "http": "http://127.0.0.1:9876"}])
            self.assertIsNone(check.score_env(facts, [])["score"])
            self.assertTrue(any("均未取得" in row["evidence"] for row in rows))

    def test_fallback_ipv6_is_not_mislabeled_ipv4(self):
        def fake(opener, url, timeout=6):
            if url == "https://ipinfo.io/json":
                return {"ip": "2001:db8::1", "country": "US"}
            raise OSError("unavailable")
        with patch.object(check, "get_json", side_effect=fake):
            rows = check.ip_findings({})
        self.assertTrue(any("IPv6（备用查询）" in row["name"] for row in rows))

    def detail(self, info, tz="UTC"):
        now = dt.datetime(2026, 10, 30, 12, 0, tzinfo=ZoneInfo(tz))
        return {r["name"].split("（")[0]: r for r in check.ip_detail("直连 IPv4", "203.0.113.9", info, self.regions, "2026-11-12", "https://example.test", now)}

    def test_unsupported_country_needs_action(self):
        rows = self.detail([dict(provider="ipinfo.io", country="CN", timezone="Asia/Shanghai", org="AS4134", hosting=None, proxy=None, mobile=None),
                            dict(provider="ip-api.com", country="CN", timezone="Asia/Shanghai", org="AS4134", hosting=False, proxy=False, mobile=False)],
                           tz="Asia/Shanghai")
        self.assertEqual(rows["出口 IP"]["state"], "需处理")
        self.assertIn("不在 Anthropic 支持地区名单", rows["出口 IP"]["evidence"])
        self.assertIn("换 IP 也不改变", rows["出口 IP"]["action"])
        self.assertNotIn("IP 类型", rows)  # 地区已需处理且未标记代理时不再多写一行
        self.assertEqual(rows["时区与 IP"]["state"], "记录")
        self.assertIn("AS4134", rows["出口 IP"]["evidence"])
        self.assertNotIn("AS4134/AS4134", rows["出口 IP"]["evidence"])

    def test_us_datacenter_with_timezone_mismatch(self):
        rows = self.detail([dict(provider="ip-api.com", country="US", timezone="America/Los_Angeles", org="AS399804", hosting=True, proxy=False, mobile=False)])
        self.assertEqual(rows["出口 IP"]["state"], "记录")
        self.assertIn("不代表合规", rows["出口 IP"]["action"])
        self.assertEqual(rows["IP 类型"]["state"], "待确认")
        self.assertIn("机房 IP", rows["IP 类型"]["evidence"])
        self.assertIn("不一定会被封", rows["IP 类型"]["action"])
        self.assertEqual(rows["时区与 IP"]["state"], "待确认")
        self.assertIn("UTC−07:00", rows["时区与 IP"]["evidence"])

    def test_beijing_ip_is_high_risk_with_official_source(self):
        rows = self.detail([dict(provider="ipinfo.io", country="CN", city="Beijing", timezone="Asia/Shanghai", org="AS4808", hosting=None, proxy=None, mobile=None)],
                           tz="Asia/Shanghai")
        self.assertEqual(rows["出口 IP"]["state"], "需处理")
        self.assertIn("CN Beijing", rows["出口 IP"]["evidence"])
        self.assertIn("封号原因之一", rows["出口 IP"]["evidence"])
        self.assertIn(check.BAN_REASONS_URL, rows["出口 IP"]["action"])

    def test_single_source_proxy_is_only_suspected(self):
        rows = self.detail([dict(provider="ip-api.com", country="US", timezone="UTC", org="X", hosting=True, proxy=True, mobile=False)])
        self.assertEqual(rows["IP 类型"]["state"], "待确认")
        self.assertIn("疑似代理", rows["IP 类型"]["evidence"])

    def test_proxy_flag_is_high_risk_but_labeled_unofficial(self):
        rows = self.detail([dict(provider="ip-api.com", country="US", timezone="UTC", org="X", hosting=True, proxy=True, mobile=False),
                            dict(provider="proxycheck.io", country="US", timezone="UTC", org="X", proxy=True, pc_type="VPN", risk=80)])
        self.assertEqual(rows["IP 类型"]["state"], "需处理")
        self.assertIn("代理 / VPN", rows["IP 类型"]["evidence"])
        self.assertIn("经验判断", rows["IP 类型"]["evidence"])
        self.assertIn("没有公布", rows["IP 类型"]["evidence"])

    def test_provider_disagreement_and_missing_data(self):
        rows = self.detail([dict(provider="ipinfo.io", country="US", timezone=None, org=None, hosting=None, proxy=None, mobile=None),
                            dict(provider="ip-api.com", country="JP", timezone=None, org=None, hosting=None, proxy=None, mobile=None)])
        self.assertEqual(rows["IP 定位分歧"]["state"], "待确认")
        self.assertEqual(self.detail([])["出口 IP"]["state"], "待确认")

    def test_full_ip_never_printed(self):
        self.assertEqual(check.mask_ip("203.0.113.9"), "203.0.113.x")
        self.assertEqual(check.mask_ip("2001:db8:10::1"), "2001:0db8:0010:…")
        rows = self.detail([dict(provider="ip-api.com", country="US", timezone="UTC", org="X", hosting=False, proxy=False, mobile=False)])
        self.assertNotIn("203.0.113.9", json.dumps(rows, ensure_ascii=False))

    def test_proxy_route_tested_only_when_configured(self):
        calls = []

        def fake(opener, url, timeout=6):
            calls.append(url)
            if "ipify" in url:
                return {"ip": "2001:db8::1" if "api6" in url else "203.0.113.9"}
            raise OSError("offline")
        with patch.object(check, "get_json", side_effect=fake):
            plain = check.ip_findings({})
            self.assertFalse(any("终端代理" in r["name"] for r in plain))
            proxied = check.ip_findings({"HTTPS_PROXY": "http://user:SECRET@127.0.0.1:9"})
        self.assertTrue(any("终端代理" in r["name"] for r in proxied))
        self.assertNotIn("SECRET", json.dumps(proxied, ensure_ascii=False))
        self.assertTrue(all(any(s in u for s in ("ipify", "ipinfo", "ip-api", "proxycheck")) for u in calls))

    def test_org_deduplicated_by_asn(self):
        info = [dict(provider="ipinfo.io", org="AS4808 China Unicom Beijing"), dict(provider="ip-api.com", org="AS4808 China Unicom")]
        self.assertEqual(check.org_text(info), "AS4808 China Unicom Beijing")

    def test_same_ipv4_ipv6_merged(self):
        same = [dict(provider="ip-api.com", country="US", city=None, timezone="America/Los_Angeles", org="AS399804 Hostodo", hosting=True, proxy=False, mobile=False)]

        def fake_lookup(opener, ip, token=None):
            return same
        with patch.object(check, "get_json", side_effect=lambda o, url, timeout=6: {"ip": "2001:db8::1" if "api6" in url else "203.0.113.9"}), \
             patch.object(check, "lookup_ip", side_effect=fake_lookup):
            rows = check.ip_findings({})
        names = [r["name"] for r in rows]
        self.assertIn("出口 IP（直连）", names)
        self.assertEqual(sum(n.startswith("出口 IP") for n in names), 1)
        self.assertIn("合并显示", rows[0]["evidence"])

    def test_different_ipv4_ipv6_kept_apart(self):
        def fake_lookup(opener, ip, token=None):
            c = "JP" if ":" in ip else "US"
            return [dict(provider="ip-api.com", country=c, timezone="UTC", org="AS1 X", hosting=False, proxy=False, mobile=False)]
        with patch.object(check, "get_json", side_effect=lambda o, url, timeout=6: {"ip": "2001:db8::1" if "api6" in url else "203.0.113.9"}), \
             patch.object(check, "lookup_ip", side_effect=fake_lookup):
            names = [r["name"] for r in check.ip_findings({})]
        self.assertIn("出口 IP（直连 IPv4）", names)
        self.assertIn("出口 IP（直连 IPv6）", names)

    def test_most_severe_first_with_summary(self):
        rows = [check.finding("甲", "记录", "", ""), check.finding("乙", "待确认", "", ""), check.finding("丙", "需处理", "", "")]
        text = check.render(rows)
        self.assertLess(text.index("丙"), text.index("乙"))
        self.assertLess(text.index("乙"), text.index("甲"))
        self.assertIn("结论：1 项需处理、1 项待确认。最需处理：丙。", text)
        self.assertIn("未发现需处理的问题", check.summary([check.finding("甲", "记录", "", "")]))

    def test_tor_type_alone_is_confirmed(self):
        c = check.classify([dict(provider="proxycheck.io", country="US", proxy=True, pc_type="TOR", risk=100)])
        self.assertTrue(c["confirmed_proxy"])

    def test_linux_language_from_localectl(self):
        with patch.object(check, "command", return_value="   System Locale: LANG=zh_CN.UTF-8\n       VC Keymap: n/a"):
            self.assertEqual(check.linux_language(), "zh_CN.UTF-8")

    def test_report_discloses_third_party_lookup(self):
        self.assertIn("会看到你的出口 IP", check.render([], disclosed=True))
        self.assertNotIn("会看到你的出口 IP", check.render([]))

    def test_regions_file_is_official_and_complete(self):
        regions, effective, source = check.load_regions()
        self.assertEqual(source, "https://www.anthropic.com/legal/supported-regions")
        self.assertGreater(len(regions), 150)
        for code in ("CN", "HK", "MO", "RU"):
            self.assertNotIn(code, regions)
        for code in ("US", "JP", "SG", "TW", "GB"):
            self.assertIn(code, regions)


class ScoreTests(unittest.TestCase):
    def fact(self, **kw):
        base = dict(route="直连", countries=["US"], region_bad=False, tz_match=True, confirmed_proxy=False, suspected_proxy=False,
                    proxy_sources=[], residential=False, hosting=False, mobile=False, pc_type=None, risk=None, asn_type=None, known=True)
        base.update(kw)
        return base

    def test_china_is_five(self):
        s = check.score_env([self.fact(countries=["CN"], region_bad=True)], [])
        self.assertEqual(s["score"], 5)
        self.assertEqual(s["level"], "🔴 红")

    def test_china_direct_with_us_proxy_is_five(self):
        s = check.score_env([self.fact(countries=["CN"], region_bad=True), self.fact(route="终端代理", residential=True, risk=0)], [])
        self.assertEqual(s["score"], 5)

    def test_clean_us_residential_can_reach_100(self):
        s = check.score_env([self.fact(residential=True, risk=0)], [])
        self.assertEqual(s["score"], 100)
        self.assertEqual(s["level"], "🟢 纯绿")
        self.assertNotIn("封顶 99", s["items"])

    def test_us_datacenter_not_proxy_is_above_85(self):
        s = check.score_env([self.fact(hosting=True, tz_match=False)], [])
        self.assertEqual(s["score"], 86)
        self.assertEqual(s["level"], "🟩 偏绿")

    def test_confirmed_proxy_capped_35(self):
        s = check.score_env([self.fact(residential=True, risk=0, confirmed_proxy=True, proxy_sources=["a", "b"])], [])
        self.assertLessEqual(s["score"], 35)

    def test_single_source_vpn_datacenter_keeps_floor(self):
        # 这台 VPS 的真实情况：proxycheck 单独标 VPN、风险 66，ip-api 未标代理；用户日常使用未被封
        s = check.score_env([self.fact(hosting=True, tz_match=False, suspected_proxy=True, proxy_sources=["proxycheck.io"], risk=66)], [])
        self.assertEqual(s["score"], 86)
        self.assertEqual(s["level"], "🟩 偏绿")
        self.assertTrue(any(i.startswith("-3 疑似代理") for i in s["items"]))

    def test_china_signals_cap_30_even_with_clean_us_ip(self):
        signals = check.china_signals("Asia/Shanghai", ["zh_CN.UTF-8"])
        self.assertEqual(len(signals), 2)
        s = check.score_env([self.fact(residential=True, risk=0)], signals)
        self.assertEqual(s["score"], 30)
        self.assertEqual(check.china_signals("Asia/Taipei", ["zh_TW.UTF-8", "zh-Hant"]), [])

    def test_other_supported_country_base_75(self):
        s = check.score_env([self.fact(countries=["JP"], residential=True)], [])
        self.assertEqual(s["score"], 75 + 5 + 3)

    def test_proxy_route_is_scored_when_present(self):
        s = check.score_env([self.fact(hosting=True), self.fact(route="终端代理", residential=True, risk=0)], [])
        self.assertEqual(s["score"], 100)

    def probe(self, google, baidu):
        def opener_open(req, timeout=5):
            ok = google if "google" in req.full_url else baidu
            if not ok:
                raise OSError("unreachable")
            resp = unittest.mock.MagicMock()
            resp.__enter__.return_value = resp
            return resp
        net = {}
        with patch.object(check.urllib.request, "build_opener") as factory:
            factory.return_value.open.side_effect = opener_open
            rows = check.reach_findings(net)
            handlers = factory.call_args.args
        self.assertEqual(handlers[0].proxies, {})  # 直连，不走代理
        return net, rows

    def test_china_network_without_proxy_is_five(self):
        net, rows = self.probe(google=False, baidu=True)
        self.assertEqual(rows[0]["state"], "需处理")
        self.assertIn("中国大陆网络", rows[0]["evidence"])
        s = check.score_env([], [], net)  # IP 查询网站全都连不上
        self.assertEqual(s["score"], 5)
        self.assertEqual(s["level"], "🔴 红")

    def test_china_network_overrides_reachable_ip_lookup(self):
        net, _ = self.probe(google=False, baidu=True)
        s = check.score_env([self.fact(residential=True, risk=0)], [], net)
        self.assertEqual(s["score"], 5)

    def test_offline_machine_is_not_scored_as_china(self):
        net, rows = self.probe(google=False, baidu=False)
        self.assertEqual(rows[0]["state"], "待确认")
        s = check.score_env([], [], net)
        self.assertIsNone(s["score"])
        self.assertIn("网络不通", s["reason"])
        self.assertIn("未计算（网络不通", check.render([], True, s))

    def test_google_reachable_scores_normally(self):
        net, rows = self.probe(google=True, baidu=True)
        self.assertEqual(rows[0]["state"], "记录")
        self.assertEqual(check.score_env([self.fact(residential=True, risk=0)], [], net)["score"], 100)

    def test_levels(self):
        self.assertEqual([check.level(v) for v in (100, 99, 80, 79, 60, 59, 30, 29)],
                         ["🟢 纯绿", "🟩 偏绿", "🟩 偏绿", "🟡 黄", "🟡 黄", "🟠 橙", "🟠 橙", "🔴 红"])

    def test_render_shows_score_first(self):
        s = check.score_env([self.fact(residential=True, risk=0)], [])
        text = check.render([check.finding("甲", "记录", "", "")], True, s)
        self.assertLess(text.index("100 / 100"), text.index("结论"))
        self.assertIn("非 Anthropic 官方", text)

    def test_orange_score_keeps_color_in_report(self):
        score = check.score_env([self.fact()], ["上海时区"])
        text = check.render([], False, score)
        self.assertIn("30 / 100", text)
        self.assertIn("🟠 橙", text)
        self.assertNotIn("最高 30 分", text)
        self.assertIn("扣分", text)
        self.assertIn("| 检测维度 |", text)
        self.assertIn("当前账号、组织与 KYC | 未检查", text)

    def test_report_table_escapes_external_text(self):
        text = check.render([check.finding("IP", "记录", "A|B\n<script>", "")])
        self.assertIn("A&#124;B &lt;script&gt;", text)


if __name__ == "__main__":
    unittest.main()
