import json
import pathlib
import sys
import tempfile
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stdout
from io import StringIO


sys.path.insert(0, str(pathlib.Path(__file__).parents[1] / "scripts"))
import douyin_download as MODULE
REAL_MEDIA_URL_RESOLVE_ARGS = MODULE.media_url_resolve_args


class BrowserSelectionTests(unittest.TestCase):
    def setUp(self):
        self.browsers = [
            {"displayName": "工作账号", "browserId": "browser-a"},
            {"displayName": "个人账号", "browserId": "browser-b"},
        ]

    def test_explicit_name_selects_only_that_browser(self):
        self.assertEqual(
            MODULE.select_browser(self.browsers, "个人账号"), self.browsers[1]
        )

    def test_explicit_id_selects_only_that_browser(self):
        self.assertEqual(
            MODULE.select_browser(self.browsers, "browser-a"), self.browsers[0]
        )

    def test_explicit_missing_browser_fails_without_fallback(self):
        self.assertIsNone(MODULE.select_browser(self.browsers, "offline-account"))

    def test_ambiguous_default_does_not_choose_first_account(self):
        self.assertIsNone(MODULE.select_browser(self.browsers))

    def test_single_online_browser_is_safe_default(self):
        self.assertEqual(MODULE.select_browser(self.browsers[:1]), self.browsers[0])

    def test_default_does_not_prefer_selfmedia_among_multiple(self):
        browsers = self.browsers + [
            {"displayName": "自媒体", "browserId": "browser-c"}
        ]
        self.assertIsNone(MODULE.select_browser(browsers))

    def test_unique_selfmedia_still_requires_selection_when_another_browser_is_online(self):
        browsers = [
            {"displayName": "自媒体", "browserId": "browser-a"},
            {"displayName": "其他环境", "browserId": "browser-b"},
        ]
        self.assertIsNone(MODULE.select_browser(browsers))


class AccessBarrierTests(unittest.TestCase):
    def setUp(self):
        self.resolve_patch = patch.object(
            MODULE, "media_url_resolve_args", return_value=["--connect-to", "media.example:443:203.0.113.1:443"]
        )
        self.resolve_patch.start()

    def tearDown(self):
        self.resolve_patch.stop()

    def test_login_and_verification_prompts_are_recognized(self):
        self.assertTrue(MODULE.is_access_barrier_text("请登录后继续"))
        self.assertTrue(MODULE.is_access_barrier_text("请完成安全验证"))

    def test_api_auth_error_is_recognized(self):
        payload = {"status_code": 1, "status_msg": "请登录后重试"}
        with self.assertRaises(MODULE.AccessBarrierError):
            MODULE.raise_if_access_barrier_payload(payload)

    def test_non_success_detail_status_stops_without_retry(self):
        with self.assertRaises(MODULE.AccessBarrierError):
            MODULE.raise_if_access_barrier_payload({"status_code": 8})

    def test_normal_post_description_is_not_treated_as_auth_error(self):
        payload = {"status_code": 0, "desc": "登录后我们再聊这段往事"}
        self.assertFalse(MODULE.is_access_barrier_payload(payload))

    def test_detected_page_barrier_stops_before_extraction(self):
        state = {"blocked": True, "href": "https://www.douyin.com/login"}
        with patch.object(
            MODULE,
            "wb",
            return_value={"ok": True, "result": json.dumps(state)},
        ):
            with self.assertRaises(MODULE.AccessBarrierError):
                MODULE.check_page_access_barrier("browser-a", "tab-1")

    def test_page_check_fails_closed_on_malformed_or_untrusted_results(self):
        bad_results = [
            "{not-json",
            None,
            [False],
            "not a state object",
            {},
            {"href": "https://www.douyin.com/video/123"},
            {"blocked": "false"},
        ]
        for result in bad_results:
            with self.subTest(result=result), patch.object(
                MODULE, "wb", return_value={"ok": True, "result": result}
            ):
                with self.assertRaises(MODULE.AccessBarrierError):
                    MODULE.check_page_access_barrier("browser-a", "tab-1")

    def test_evaluate_checks_page_state_after_execution(self):
        states = iter([
            {"ok": True, "result": json.dumps({"blocked": False})},
            {"ok": True, "result": "video title"},
            {"ok": True, "result": json.dumps({"blocked": True})},
        ])
        with patch.object(MODULE, "wb", side_effect=lambda *args, **kwargs: next(states)) as bridge:
            with self.assertRaises(MODULE.AccessBarrierError):
                MODULE.evaluate("browser-a", "tab-1", "document.title")
        self.assertEqual(bridge.call_count, 3)

    def test_media_endpoint_access_limit_raises_stop_signal(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "blocked.mp4"
            with patch.object(MODULE, "run", return_value=(0, "403\t0\t\ttext/html", "")):
                with self.assertRaises(MODULE.AccessBarrierError):
                    MODULE.download("https://media.example/blocked", str(path))
            self.assertFalse(path.exists())

    def test_login_redirect_is_treated_as_barrier(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "blocked.mp4"
            with patch.object(
                MODULE, "run",
                return_value=(0, "302\t0\thttps://www.douyin.com/login\ttext/html", ""),
            ):
                with self.assertRaises(MODULE.AccessBarrierError):
                    MODULE.download("https://media.example/blocked", str(path))

    def test_success_status_with_html_body_is_not_saved_as_media(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "blocked.mp4"
            path.write_text("challenge", encoding="utf-8")
            with patch.object(
                MODULE, "run", return_value=(0, "200\t9\t\ttext/html", "")
            ):
                with self.assertRaises(MODULE.AccessBarrierError):
                    MODULE.download("https://media.example/blocked", str(path))
            self.assertEqual(path.read_text(encoding="utf-8"), "challenge")

    def test_missing_detail_state_fails_closed(self):
        with self.assertRaises(MODULE.AccessBarrierError):
            MODULE.raise_if_access_barrier_payload({
                "detailReady": False, "status_code": 0,
            })

    def test_missing_aweme_detail_error_marker_is_normalized(self):
        for marker in ("no aweme_detail", "no_aweme_detail"):
            with self.subTest(marker=marker), self.assertRaises(MODULE.AccessBarrierError):
                MODULE.raise_if_access_barrier_payload({"err": marker})

    def test_unreadable_detail_stops_media_type_retries(self):
        with patch.object(MODULE, "fetch_kind_probe", return_value=None) as fetch:
            with self.assertRaises(MODULE.AccessBarrierError):
                MODULE.detect_kind("browser-a", "tab-1", "123456789012")
        fetch.assert_called_once_with("browser-a", "tab-1", "123456789012", wait=0)

    def test_login_barrier_preserves_task_tab(self):
        with patch.object(sys, "argv", ["douyin_download.py", "123456789012"]), \
                patch.object(MODULE, "check_bridge", return_value=[{
                    "displayName": "自媒体", "browserId": "browser-a",
                }]), \
                patch.object(MODULE, "parse_input", return_value=("123456789012", "video")), \
                patch.object(MODULE, "navigate_to", return_value="tab-1"), \
                patch.object(MODULE, "detect_kind", side_effect=MODULE.AccessBarrierError()), \
                patch.object(MODULE, "wb") as bridge_command:
            self.assertEqual(MODULE.main(), 2)
        bridge_command.assert_not_called()


class ExplicitBrowserIntegrationTests(unittest.TestCase):
    def test_cli_help_requires_selection_for_multiple_online_browsers(self):
        output = StringIO()
        with patch.object(sys, "argv", ["douyin_download.py", "--help"]):
            with redirect_stdout(output), self.assertRaises(SystemExit):
                MODULE.main()
        self.assertIn("多个在线时必须指定", output.getvalue())

    def test_default_with_unique_selfmedia_and_other_browser_stops_before_navigation(self):
        online = [
            {"displayName": "自媒体", "browserId": "browser-a"},
            {"displayName": "个人", "browserId": "browser-b"},
        ]
        output = StringIO()
        with patch.object(sys, "argv", ["douyin_download.py", "123456789012"]), \
                patch.object(MODULE, "check_bridge", return_value=online), \
                patch.object(MODULE, "parse_input") as parse_input, \
                patch.object(MODULE, "navigate_to") as navigate, \
                redirect_stdout(output):
            self.assertEqual(MODULE.main(), 1)
        self.assertIn("自媒体 (browser-a)", output.getvalue())
        self.assertIn("个人 (browser-b)", output.getvalue())
        parse_input.assert_not_called()
        navigate.assert_not_called()

    def test_missing_explicit_browser_stops_before_input_or_navigation(self):
        with patch.object(sys, "argv", [
            "douyin_download.py", "123456789012", "--browser", "offline-account",
        ]), patch.object(MODULE, "check_bridge", return_value=[{
            "displayName": "other-account", "browserId": "browser-b",
        }]), patch.object(MODULE, "parse_input") as parse_input, \
                patch.object(MODULE, "navigate_to") as navigate:
            self.assertEqual(MODULE.main(), 1)
        parse_input.assert_not_called()
        navigate.assert_not_called()


class NoteImageSourceTests(unittest.TestCase):
    def test_dom_original_must_match_detail_image_id(self):
        detail = {
            "desc": "requested work",
            "imgs": [{
                "urls": ["https://img.example/targetimageid12345678901234567890~tplv-q75.jpeg"]
            }],
        }
        recommendations = [
            "https://img.example/recommendimage12345678901234567890~noop.jpeg"
        ]
        images, _ = MODULE.select_note_images(detail, recommendations)
        self.assertEqual(len(images), 1)
        self.assertIn("targetimageid12345678901234567890", images[0][0])
        self.assertNotIn("recommendimage", images[0][0])

    def test_missing_detail_image_list_fails_instead_of_using_dom(self):
        recommendations = [
            "https://img.example/recommendimage12345678901234567890~noop.jpeg"
        ]
        images, _ = MODULE.select_note_images(None, recommendations)
        self.assertEqual(images, [])

    def test_note_fallback_does_not_download_page_wide_dom_images(self):
        recommendation = "https://img.example/recommendimage12345678901234567890~noop.jpeg"
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(MODULE, "fetch_note_detail", return_value=None), \
                patch.object(MODULE, "fetch_note_images", return_value=[recommendation]) as fetch_dom, \
                patch.object(MODULE, "download") as download:
            result = MODULE.try_note(
                "browser-a", "tab-1", "123456789012", SimpleNamespace(out=directory)
            )
        self.assertEqual(result, [])
        fetch_dom.assert_not_called()
        download.assert_not_called()


class InputAndOutputSafetyTests(unittest.TestCase):
    def setUp(self):
        self.resolve_patch = patch.object(
            MODULE, "media_url_resolve_args", return_value=["--connect-to", "media.example:443:203.0.113.1:443"]
        )
        self.resolve_patch.start()

    def tearDown(self):
        self.resolve_patch.stop()

    def test_option_control_and_non_http_inputs_are_rejected_without_curl(self):
        bad_inputs = [
            "-o/tmp/owned",
            "--config=/tmp/curlrc",
            "\nhttps://www.douyin.com/video/123456789012",
            "javascript:https://www.douyin.com/video/123456789012",
            "file:///etc/passwd",
        ]
        for value in bad_inputs:
            with self.subTest(value=value), patch.object(MODULE, "run") as run:
                self.assertEqual(MODULE.parse_input(value), (None, None))
                run.assert_not_called()

    def test_external_and_lookalike_hosts_are_rejected_without_curl(self):
        bad_urls = [
            "https://example.com/video/123456789012",
            "https://www.douyin.com.evil.example/video/123456789012",
            "https://www.douyin.com@127.0.0.1/video/123456789012",
            "http://127.0.0.1/video/123456789012",
            "https://www.douyin.com:8443/video/123456789012",
        ]
        for value in bad_urls:
            with self.subTest(value=value), patch.object(MODULE, "run") as run:
                self.assertEqual(MODULE.parse_input(value), (None, None))
                run.assert_not_called()

    def test_long_video_and_note_urls_are_accepted_without_network(self):
        self.assertEqual(
            MODULE.parse_input("https://www.douyin.com/video/123456789012"),
            ("123456789012", "video"),
        )
        self.assertEqual(
            MODULE.parse_input("https://www.iesdouyin.com/share/note/123456789012?from=share"),
            ("123456789012", "note"),
        )

    def test_short_link_extracts_id_from_one_valid_location_without_following_it(self):
        short_url = "https://v.douyin.com/AbCdEf123/"
        location = "https://www.douyin.com/video/123456789012?from=share"
        with patch.object(MODULE, "run", return_value=(0, f"302\t{location}", "")) as run:
            self.assertEqual(MODULE.parse_input(short_url), ("123456789012", "video"))
        run.assert_called_once()
        command = run.call_args.args[0]
        self.assertEqual(command[0:3], ["curl", "--disable", "--globoff"])
        self.assertIn("--max-redirs", command)
        self.assertIn("--connect-to", command)
        self.assertNotIn("-L", command)
        self.assertEqual(command[-1], short_url)
        self.assertEqual(run.call_count, 1)

    def test_short_link_rejects_second_short_link_or_long_redirect_chain(self):
        short_url = "https://v.douyin.com/AbCdEf123/"
        with patch.object(
            MODULE, "run", return_value=(0, "302\thttps://v.douyin.com/AnotherLink/", "")
        ) as run:
            self.assertEqual(MODULE.parse_input(short_url), (None, None))
        run.assert_called_once()

    def test_short_link_rejects_external_private_and_malformed_locations(self):
        short_url = "https://v.douyin.com/AbCdEf123/"
        locations = [
            "http://www.douyin.com/video/123456789012",
            "https://evil.example/video/123456789012",
            "https://www.douyin.com.evil.example/video/123456789012",
            "https://www.douyin.com@127.0.0.1/video/123456789012",
            "https://www.douyin.com/video/not-an-id",
            "https://www.douyin.com/share/video/123456789012 -> https://127.0.0.1/",
        ]
        for location in locations:
            with self.subTest(location=location), patch.object(
                MODULE, "run", return_value=(0, f"302\t{location}", "")
            ) as run:
                self.assertEqual(MODULE.parse_input(short_url), (None, None))
                run.assert_called_once()

    def test_short_link_requires_public_dns_and_validates_before_curl(self):
        short_url = "https://v.douyin.com/AbCdEf123/"
        with patch.object(MODULE, "media_url_resolve_args", return_value=None), patch.object(MODULE, "run") as run:
            self.assertEqual(MODULE.parse_input(short_url), (None, None))
        run.assert_not_called()

    def test_multiple_short_links_and_non_redirect_responses_fail_without_followup(self):
        multiple = "https://v.douyin.com/AbCdEf123/ https://v.douyin.com/Another/"
        with patch.object(MODULE, "run") as run:
            self.assertEqual(MODULE.parse_input(multiple), (None, None))
        run.assert_not_called()
        for response in ((0, "200\t", ""), (0, "302\t", ""), (28, "302\thttps://www.douyin.com/video/123456789012", "timeout")):
            with self.subTest(response=response), patch.object(MODULE, "run", return_value=response) as request:
                self.assertEqual(MODULE.parse_input("https://v.douyin.com/AbCdEf123/"), (None, None))
                request.assert_called_once()

    @staticmethod
    def successful_curl(payload):
        def run(cmd, desc=""):
            staging_path = cmd[cmd.index("-o") + 1]
            pathlib.Path(staging_path).write_bytes(payload)
            return 0, f"200\t{len(payload)}\t\tvideo/mp4", ""
        return run

    def test_existing_output_file_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            target = pathlib.Path(directory) / "work.mp4"
            target.write_bytes(b"existing data")
            with patch.object(MODULE, "run", side_effect=self.successful_curl(b"new data")):
                self.assertFalse(MODULE.download("https://media.example/work", str(target)))
            self.assertEqual(target.read_bytes(), b"existing data")
            self.assertEqual(list(pathlib.Path(directory).glob(".work.mp4.*.download")), [])

    def test_final_publish_refuses_to_replace_an_existing_audio_output(self):
        with tempfile.TemporaryDirectory() as directory:
            existing = pathlib.Path(directory) / "audio.mp3"
            staging = pathlib.Path(directory) / ".audio.mp3.unique.mp3"
            existing.write_bytes(b"old audio")
            staging.write_bytes(b"new audio")
            self.assertFalse(MODULE.publish_file_no_replace(str(staging), str(existing)))
            self.assertEqual(existing.read_bytes(), b"old audio")
            self.assertEqual(staging.read_bytes(), b"new audio")

    def test_download_does_not_follow_lan_redirect_or_redirect_chain(self):
        cases = [
            "http://127.0.0.1/private",
            "https://v.douyin.com/" * 20,
        ]
        for redirect_url in cases:
            with self.subTest(redirect_url=redirect_url), tempfile.TemporaryDirectory() as directory:
                target = pathlib.Path(directory) / "work.mp4"
                with patch.object(
                    MODULE, "run",
                    return_value=(0, f"302\t0\t{redirect_url}\ttext/html", ""),
                ) as run:
                    self.assertFalse(MODULE.download("https://media.example/work", str(target)))
                command = run.call_args.args[0]
                self.assertNotIn("-L", command)
                self.assertEqual(run.call_count, 1)
                self.assertFalse(target.exists())
                self.assertEqual(list(pathlib.Path(directory).glob(".work.mp4.*.download")), [])

    def test_concurrent_downloads_never_replace_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            target = pathlib.Path(directory) / "same-name.mp4"
            start_together = threading.Barrier(2)

            def fake_run(cmd, desc=""):
                url = cmd[-1]
                payload = url.encode("ascii")
                staging_path = cmd[cmd.index("-o") + 1]
                pathlib.Path(staging_path).write_bytes(payload)
                start_together.wait(timeout=5)
                return 0, f"200\t{len(payload)}\t\tvideo/mp4", ""

            with patch.object(MODULE, "run", side_effect=fake_run):
                with ThreadPoolExecutor(max_workers=2) as pool:
                    results = list(pool.map(
                        lambda url: MODULE.download(url, str(target)),
                        ("https://media.example/first", "https://media.example/second"),
                    ))
            self.assertEqual(sorted(results), [False, True])
            self.assertIn(target.read_bytes(), {
                b"https://media.example/first", b"https://media.example/second",
            })
            self.assertEqual(list(pathlib.Path(directory).glob(".same-name.mp4.*.download")), [])

    def test_download_exception_cleans_staging_file(self):
        with tempfile.TemporaryDirectory() as directory:
            target = pathlib.Path(directory) / "work.mp4"
            with patch.object(MODULE, "run", side_effect=RuntimeError("curl failure")):
                with self.assertRaises(RuntimeError):
                    MODULE.download("https://media.example/work", str(target))
            self.assertEqual(list(pathlib.Path(directory).iterdir()), [])

    def test_media_urls_reject_local_schemes_hosts_and_private_dns(self):
        for url in (
            "file:///etc/passwd", "http://media.example/video", "https://localhost/video",
            "https://127.0.0.1/video", "https://[::1]/video", "https://media.example@public.example/video",
            "https://media.example./video",
        ):
            with self.subTest(url=url):
                self.assertIsNone(REAL_MEDIA_URL_RESOLVE_ARGS(url))
        with patch.object(MODULE.socket, "getaddrinfo", return_value=[
            (MODULE.socket.AF_INET, MODULE.socket.SOCK_STREAM, 6, "", ("192.168.1.9", 443)),
        ]):
            self.assertIsNone(REAL_MEDIA_URL_RESOLVE_ARGS("https://media.example/video"))

    def test_private_media_dns_is_rejected_before_curl_or_file_creation(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(MODULE.socket, "getaddrinfo", return_value=[
                    (MODULE.socket.AF_INET, MODULE.socket.SOCK_STREAM, 6, "", ("10.0.0.4", 443)),
                ]), patch.object(MODULE, "media_url_resolve_args", side_effect=REAL_MEDIA_URL_RESOLVE_ARGS), \
                patch.object(MODULE, "run") as run:
            target = pathlib.Path(directory) / "private.mp4"
            self.assertFalse(MODULE.download("https://media.example/private", str(target)))
            run.assert_not_called()
            self.assertEqual(list(pathlib.Path(directory).iterdir()), [])

    def test_download_pins_public_dns_for_direct_or_proxy_connection(self):
        public_ip = "142.250.72.14"
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(MODULE.socket, "getaddrinfo", return_value=[
                    (MODULE.socket.AF_INET, MODULE.socket.SOCK_STREAM, 6, "", (public_ip, 443)),
                ]), patch.object(MODULE, "media_url_resolve_args", side_effect=REAL_MEDIA_URL_RESOLVE_ARGS), \
                patch.object(MODULE, "run", side_effect=self.successful_curl(b"media")) as run:
            self.assertTrue(MODULE.download("https://cdn.douyinvod.com/video", str(pathlib.Path(directory) / "v.mp4")))
        command = run.call_args.args[0]
        self.assertEqual(command[0:3], ["curl", "--disable", "--globoff"])
        self.assertIn("cdn.douyinvod.com:443:142.250.72.14:443", command)
        self.assertIn("--connect-to", command)
        self.assertNotIn("--proxy", command)
        self.assertNotIn("-L", command)

    def test_fake_ip_dns_falls_back_to_fixed_doh_and_pins_public_answers(self):
        fake_ip = "198.18.0.65"
        doh_results = iter([
            (0, '{"Status":0,"Answer":[{"type":1,"data":"142.250.72.14"}]}\n200', ""),
            (0, '{"Status":0,"Answer":[{"type":28,"data":"2606:4700:4700::1111"}]}\n200', ""),
        ])
        with patch.object(MODULE.socket, "getaddrinfo", return_value=[
            (MODULE.socket.AF_INET, MODULE.socket.SOCK_STREAM, 6, "", (fake_ip, 443)),
        ]), patch.object(MODULE, "run", side_effect=lambda *args, **kwargs: next(doh_results)) as run:
            pin_args = REAL_MEDIA_URL_RESOLVE_ARGS("https://cdn.douyinvod.com/video?token=secret")
        self.assertEqual(pin_args, [
            "--connect-to", "cdn.douyinvod.com:443:142.250.72.14:443",
            "--connect-to", "cdn.douyinvod.com:443:[2606:4700:4700::1111]:443",
        ])
        self.assertEqual(run.call_count, 2)
        doh_commands = [call.args[0] for call in run.call_args_list]
        self.assertTrue(all("https://dns.alidns.com/resolve?" in command[-1] for command in doh_commands))
        self.assertTrue(all("cdn.douyinvod.com" in command[-1] for command in doh_commands))
        self.assertTrue(all("secret" not in command[-1] for command in doh_commands))
        self.assertTrue(all("--resolve" in command for command in doh_commands))

    def test_fake_ip_doh_rejects_private_answers_and_redirects(self):
        fake_ip = "198.18.0.65"
        fake_dns = [(MODULE.socket.AF_INET, MODULE.socket.SOCK_STREAM, 6, "", (fake_ip, 443))]
        with patch.object(MODULE.socket, "getaddrinfo", return_value=fake_dns), \
                patch.object(MODULE, "run", return_value=(0, '{"Status":0,"Answer":[{"type":1,"data":"10.1.2.3"}]}\n200', "")) as run:
            self.assertIsNone(REAL_MEDIA_URL_RESOLVE_ARGS("https://cdn.douyinvod.com/video"))
        run.assert_called_once()
        with patch.object(MODULE.socket, "getaddrinfo", return_value=fake_dns), \
                patch.object(MODULE, "run", return_value=(0, "\n302", "")):
            self.assertIsNone(REAL_MEDIA_URL_RESOLVE_ARGS("https://cdn.douyinvod.com/video"))

    def test_doh_proxy_fallback_uses_only_fixed_ip_connect(self):
        fake_dns = [(MODULE.socket.AF_INET, MODULE.socket.SOCK_STREAM, 6, "", ("198.18.0.65", 443))]
        success_a = (0, '{"Status":0,"Answer":[{"type":1,"data":"142.250.72.14"}]}\n200', "")
        success_aaaa = (0, '{"Status":0,"Answer":[]}\n200', "")
        responses = iter([(7, "", "direct route blocked"), (7, "", "direct route blocked"), success_a, success_aaaa])
        with patch.object(MODULE.socket, "getaddrinfo", return_value=fake_dns), \
                patch.object(MODULE, "run", side_effect=lambda *args, **kwargs: next(responses)) as run:
            pins = REAL_MEDIA_URL_RESOLVE_ARGS("https://cdn.douyinvod.com/video")
        self.assertEqual(pins, ["--connect-to", "cdn.douyinvod.com:443:142.250.72.14:443"])
        proxy_command = run.call_args_list[2].args[0]
        self.assertIn("--connect-to", proxy_command)
        self.assertIn("dns.alidns.com:443:223.5.5.5:443", proxy_command)
        self.assertNotIn("--proxy", proxy_command)

    def test_audio_download_collision_preserves_preexisting_source(self):
        with tempfile.TemporaryDirectory() as directory:
            stamp = 1_700_000_000_000
            source = pathlib.Path(directory) / ".douyin-123456789012-1700000000000.source"
            source.write_bytes(b"user data")
            detail = {"music_play_urls": ["https://cdn.douyinvod.com/audio"]}
            args = SimpleNamespace(out=directory)
            with patch.object(MODULE, "time") as clock, \
                    patch.object(MODULE, "fetch_audio_detail", return_value=detail), \
                    patch.object(MODULE, "download", return_value=False) as download:
                clock.time.return_value = stamp / 1000
                result = MODULE.try_audio_only("browser-a", "tab-1", "123456789012", args)
            self.assertEqual(result, ([], detail))
            download.assert_called_once()
            self.assertEqual(source.read_bytes(), b"user data")


class DohFailureReportingTests(unittest.TestCase):
    def test_fake_ip_doh_failure_is_reported_and_download_stops(self):
        fake_dns = [(MODULE.socket.AF_INET, MODULE.socket.SOCK_STREAM, 6, "", ("198.18.0.65", 443))]
        output = StringIO()
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(MODULE.socket, "getaddrinfo", return_value=fake_dns), \
                patch.object(MODULE, "run", return_value=(-1, "", "resolver timeout")) as run, \
                redirect_stdout(output):
            target = pathlib.Path(directory) / "blocked.mp4"
            self.assertFalse(MODULE.download("https://cdn.douyinvod.com/video?token=secret", str(target)))
        self.assertIn("媒体地址不是可安全访问的公网 HTTPS 地址，已停止下载", output.getvalue())
        self.assertFalse(target.exists())
        run.assert_called()


if __name__ == "__main__":
    unittest.main()
