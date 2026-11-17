#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""avatar-autoclip 离线自测：不需要 API Key，不产生任何费用。

覆盖三类东西：
  1. 响应信封拆解（三种实测形态 + 失败码）
  2. 本地预检（素材/字幕/元水印/图层/地址重名）
  3. CLI 行为（dry-run 不发写请求、授权门禁、退出码）

跑法：
    PYTHONDONTWRITEBYTECODE=1 python -X utf8 scripts/selftest.py -v
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import dhclip  # noqa: E402
from dhclip import (  # noqa: E402
    ApiError, Client, CliError, ValidationError, unwrap, find_deep, find_points_cost,
    resolve_task_status, validate_materials, validate_subtitle, validate_metadata,
    validate_struct_layers, validate_url_list_uniq, parse_materials, parse_kv_list,
    build_ai_label_metadata, LIMITS, EXIT_OK, EXIT_USAGE, EXIT_VALIDATION,
    EXIT_BUDGET, EXIT_AUTHZ, LOCKED_BASE, LOCKED_HOST, assert_base_locked,
)

KEY = "sk-test-offline-key"


def fake_response(payload, status=200):
    """造一个够用的 urlopen 返回值。"""
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    class Resp(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self, *a):
            return body

        status = 200

    r = Resp()
    r.status = status
    return r


class TestUnwrap(unittest.TestCase):
    def test_direct_tenant_envelope(self):
        payload = {"code": 1, "msg": "success", "data": {"results": [{"id": "t1"}]}}
        self.assertEqual(unwrap(payload), {"results": [{"id": "t1"}]})

    def test_relay_double_envelope(self):
        """api.a7w.cn 中转：data.result 里再套一层上游信封。"""
        payload = {"code": 1, "msg": "success", "data": {"result": {
            "code": "Succeed", "data": {"results": [{"id": "t2"}], "sid": "s"}}}}
        self.assertEqual(unwrap(payload), {"results": [{"id": "t2"}], "sid": "s"})

    def test_relay_unwrapped_data(self):
        """个别接口（音色列表）不经二次包装。"""
        payload = {"code": 1, "msg": "success", "data": {"total": 38, "items": [1, 2]}}
        self.assertEqual(unwrap(payload), {"total": 38, "items": [1, 2]})

    def test_bare_body(self):
        payload = {"available_points": 100, "currency": "points"}
        self.assertEqual(unwrap(payload), payload)

    def test_relay_result_is_list(self):
        payload = {"code": 1, "msg": "success", "data": {"result": [{"a": 1}]}}
        self.assertEqual(unwrap(payload)["results"], [{"a": 1}])

    def test_failure_code_raises_with_msg(self):
        with self.assertRaises(ApiError) as ctx:
            unwrap({"code": 0, "msg": "API Key 无效或已过期", "data": None})
        self.assertIn("API Key 无效", str(ctx.exception))

    def test_inner_failure_raises(self):
        with self.assertRaises(ApiError) as ctx:
            unwrap({"code": 1, "msg": "success",
                    "data": {"result": {"code": "Failed", "message": "上游炸了"}}})
        self.assertIn("上游炸了", str(ctx.exception))

    def test_error_object_form(self):
        """网关的另一种错误形态 {"error":{"code":...}}。"""
        with self.assertRaises(ApiError) as ctx:
            unwrap({"error": {"message": "点数余额不足", "type": "insufficient_points"}})
        self.assertIn("点数余额不足", str(ctx.exception))

    def test_deeply_nested_does_not_loop(self):
        payload = {"code": 1, "msg": "ok", "data": {"data": {"data": {"x": 1}}}}
        self.assertIsInstance(unwrap(payload), dict)


class TestDeepSearch(unittest.TestCase):
    def test_find_deep_priority(self):
        tree = {"result": {"data": {"video_uri": "low", "video_url": "high"}}}
        self.assertEqual(find_deep(tree, dhclip.VIDEO_KEYS), "high")

    def test_find_deep_in_list(self):
        tree = [{"a": 1}, {"video_url": "https://v/1.mp4"}]
        self.assertEqual(find_deep(tree, dhclip.VIDEO_KEYS), "https://v/1.mp4")

    def test_points_cost_from_usage(self):
        self.assertEqual(find_points_cost({"usage": {"points_cost": 12.5}}), 12.5)

    def test_points_cost_absent_is_none(self):
        self.assertIsNone(find_points_cost({"foo": "bar"}))

    def test_status_recognition(self):
        self.assertEqual(resolve_task_status({"status": "Processing"}), "processing")
        self.assertEqual(resolve_task_status({"task_status": "succeeded"}), "succeeded")
        self.assertIsNone(resolve_task_status({"status": "weird-state"}))

    def test_status_found_deeply(self):
        """实测坑：应用级 query 把 status 放在 data.result.data 里。

        只在顶层找 key 会永远拿不到状态 —— 表现为"任务完成了却轮询到超时"。
        """
        payload = {"code": 1, "msg": "success", "data": {"result": {
            "data": {"result": "任务完成", "status": "completed", "duration": 18.875},
            "mode": "async_query", "results": [{"video_url": "https://v/x.mp4"}]}}}
        self.assertEqual(resolve_task_status(dhclip.unwrap(payload)), "completed")

    def test_status_deep_ignores_unrelated_strings(self):
        payload = {"result": {"state": "not-a-real-state", "data": {"status": "failed"}}}
        self.assertEqual(resolve_task_status(payload), "failed")


class TestValidation(unittest.TestCase):
    def test_materials_ok(self):
        ok = [{"type": "image", "fileUrl": "https://x/a.jpg"},
              {"type": "video", "fileUrl": "https://x/b.mp4"}]
        self.assertEqual(validate_materials(ok), [])

    def test_materials_empty(self):
        self.assertTrue(validate_materials([]))
        self.assertTrue(validate_materials(None))

    def test_materials_bad_type_and_ext(self):
        issues = validate_materials([
            {"type": "audio", "fileUrl": "https://x/a.jpg"},
            {"type": "image", "fileUrl": "https://x/b.txt"},
        ])
        self.assertEqual(len(issues), 2)

    def test_materials_total_over_limit(self):
        """一张图按 2 秒计，200 张就是 400 秒，超 300 秒上限。"""
        many = [{"type": "image", "fileUrl": "https://x/%d.jpg" % i} for i in range(200)]
        issues = validate_materials(many)
        self.assertTrue(any("总量" in i for i in issues))

    def test_subtitle_bounds(self):
        issues = validate_subtitle([
            {"startMs": 1000, "endMs": 500, "text": "A"},
            {"startMs": 0, "endMs": 400000, "text": "B"},
            {"startMs": 0, "text": "C"},
        ])
        self.assertEqual(len(issues), 3)

    def test_subtitle_ok(self):
        self.assertEqual(validate_subtitle([{"startMs": 0, "endMs": 500, "text": "A"}]), [])

    def test_metadata_must_be_string_values(self):
        issues = validate_metadata({"AIGC": {"Label": "1"}})
        self.assertTrue(any("必须是字符串" in i for i in issues))

    def test_metadata_single_group_only(self):
        issues = validate_metadata({"AIGC": "x", "OTHER": "y"})
        self.assertTrue(any("一组" in i for i in issues))

    def test_ai_label_metadata_is_valid(self):
        md = build_ai_label_metadata("某公司", "ID-1")
        self.assertEqual(validate_metadata(md), [])
        self.assertIsInstance(list(md.values())[0], str)

    def test_struct_layers_rules(self):
        issues = validate_struct_layers([
            {"markCode": "headerLayer", "showMode": "customize"},
            {"markCode": "figureLayer", "show": False},
            {"markCode": "nope"},
        ])
        self.assertEqual(len(issues), 3)

    def test_url_reuse_detected(self):
        dup = validate_url_list_uniq(["https://x/a.mp4", "https://x/a.mp4", "https://x/b.mp4"])
        self.assertEqual(dup, ["https://x/a.mp4"])

    def test_url_reuse_ignores_empty(self):
        self.assertEqual(validate_url_list_uniq(["", "", "https://x/a.mp4"]), [])

    def test_parse_materials(self):
        got = parse_materials(["image=https://x/a.jpg", "video=https://x/b.mp4"])
        self.assertEqual(got[0], {"type": "image", "fileUrl": "https://x/a.jpg"})
        with self.assertRaises(dhclip.CliError):
            parse_materials(["audio=https://x/a.mp3"])
        with self.assertRaises(dhclip.CliError):
            parse_materials(["nope"])

    def test_parse_kv(self):
        self.assertEqual(parse_kv_list(["a=1", "b=2"]), {"a": "1", "b": "2"})


class TestBaseLock(unittest.TestCase):
    """★★★ 算力接口死锁：只允许 api.a7w.cn（2026-10-09 站主指定）。

    为什么单独测：这是产品级约束。一旦被改松，用户把根地址指到别处会得到
    一路含糊的网络错误、以为"技能坏了"然后反复重试 —— 站主反馈的正是这个现象。
    所以这里把【允许的形状】和【必须拒绝的形状】都钉死，防止以后被无意改回去。
    """

    def test_constants(self):
        self.assertEqual(LOCKED_HOST, "api.a7w.cn")
        self.assertIn(LOCKED_HOST, LOCKED_BASE)

    def test_accepts_legit_forms(self):
        for raw in ("https://api.a7w.cn/api/v1",
                    "https://api.a7w.cn",
                    "api.a7w.cn",
                    "https://API.A7W.CN/api/v1",
                    "https://api.a7w.cn:8443/api/v1",   # 端口被规范化掉
                    ""):
            self.assertEqual(assert_base_locked(raw), LOCKED_BASE, raw)

    def test_rejects_other_hosts(self):
        for raw in ("https://api.likeadmin.cn/api/v1",
                    "http://evil.example.com/api/v1",
                    "api.likeadmin.cn",
                    "https://api.a7w.cn.evil.com/api/v1",   # 后缀伪装
                    "https://notapi.a7w.cn/api/v1"):
            with self.assertRaises(CliError) as ctx:
                assert_base_locked(raw)
            self.assertIn(LOCKED_HOST, str(ctx.exception), raw)

    def test_client_rejects_override(self):
        with self.assertRaises(CliError):
            Client(base="https://elsewhere.example.com/api/v1", key=KEY)

    def test_client_normalizes_port_and_path(self):
        c = Client(base="https://api.a7w.cn:8443/whatever", key=KEY)
        self.assertEqual(c.base, LOCKED_BASE)

    def test_env_base_is_ignored(self):
        """AVATAR_AUTOCLIP_BASE 不再被读取（少一个可改的入口）。"""
        seen = {}

        def fake_urlopen(req, timeout=None):
            seen["url"] = req.full_url
            return fake_response({"code": 1, "msg": "ok", "data": {}})

        old = os.environ.get("AVATAR_AUTOCLIP_BASE")
        os.environ["AVATAR_AUTOCLIP_BASE"] = "http://evil.example.com/api/v1"
        try:
            with mock.patch("urllib.request.urlopen", fake_urlopen):
                Client(base=LOCKED_BASE, key=KEY).get("user/balance")
        finally:
            if old is None:
                os.environ.pop("AVATAR_AUTOCLIP_BASE", None)
            else:
                os.environ["AVATAR_AUTOCLIP_BASE"] = old
        self.assertIn("api.a7w.cn", seen["url"])
        self.assertNotIn("evil.example.com", seen["url"])


class TestClientHttp(unittest.TestCase):
    def test_authorization_header_and_url(self):
        seen = {}

        def fake_urlopen(req, timeout=None):
            seen["url"] = req.full_url
            seen["auth"] = req.get_header("Authorization")
            seen["method"] = req.get_method()
            return fake_response({"code": 1, "msg": "success", "data": {"ok": True}})

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            c = Client(base=LOCKED_BASE, key=KEY)
            data = c.get("apps/smart_clip/template", params={"scene": "realMan", "pageSize": 3})
        self.assertEqual(data, {"ok": True})
        self.assertEqual(seen["url"],
                         LOCKED_BASE + "/apps/smart_clip/template"
                         "?scene=realMan&pageSize=3")
        self.assertEqual(seen["auth"], "Bearer " + KEY)

    def test_empty_params_dropped(self):
        seen = {}

        def fake_urlopen(req, timeout=None):
            seen["url"] = req.full_url
            return fake_response({"code": 1, "msg": "ok", "data": {}})

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            Client(base=LOCKED_BASE, key=KEY).get("p", params={"a": 1, "b": "", "c": None})
        self.assertEqual(seen["url"], LOCKED_BASE + "/p?a=1")

    def test_post_body_is_json_utf8(self):
        seen = {}

        def fake_urlopen(req, timeout=None):
            seen["body"] = req.data
            seen["ctype"] = req.get_header("Content-type")
            return fake_response({"code": 1, "msg": "ok", "data": {"task_id": "t1"}})

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            c = Client(base=LOCKED_BASE, key=KEY)
            c.lipsync_submit("https://x/f.jpg", "https://x/a.mp3")
        body = json.loads(seen["body"].decode("utf-8"))
        self.assertEqual(body["model"], "super-lipsync-pro")
        self.assertEqual(body["mode"], "audio")
        self.assertEqual(body["quality"], "standard")
        self.assertIn("charset=utf-8", seen["ctype"].lower())

    def test_task_id_is_url_quoted(self):
        seen = {}

        def fake_urlopen(req, timeout=None):
            seen["url"] = req.full_url
            return fake_response({"code": 1, "msg": "ok", "data": {}})

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            Client(base=LOCKED_BASE, key=KEY).task("task_a/b c")
        self.assertIn("task_a%2Fb%20c", seen["url"])

    def test_budget_gate_exits_5(self):
        def fake_urlopen(req, timeout=None):
            return fake_response({"code": 1, "msg": "ok", "data": {},
                                  "usage": {"points_cost": 100}})

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            c = Client(base=LOCKED_BASE, key=KEY, budget=5)
            with self.assertRaises(dhclip.CliError) as ctx:
                c.get("whatever")
        self.assertEqual(ctx.exception.code, EXIT_BUDGET)

    def test_http_error_body_is_surfaced(self):
        import urllib.error

        def fake_urlopen(req, timeout=None):
            raise urllib.error.HTTPError(
                req.full_url, 401, "Unauthorized", {}, io.BytesIO(
                    json.dumps({"code": 0, "msg": "API Key 无效或已过期"}).encode()))

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            with self.assertRaises(ApiError) as ctx:
                Client(base=LOCKED_BASE, key=KEY).get("user/balance")
        self.assertIn("无效或已过期", str(ctx.exception))

    def test_non_json_response(self):
        def fake_urlopen(req, timeout=None):
            return fake_response.__wrapped__ if False else _raw_response(b"<html>nope</html>")

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            with self.assertRaises(ApiError) as ctx:
                Client(base=LOCKED_BASE, key=KEY).get("p")
        self.assertIn("不是 JSON", str(ctx.exception))

    def test_dry_run_sends_nothing(self):
        def boom(req, timeout=None):
            raise AssertionError("dry-run 不应发出任何请求")

        with mock.patch("urllib.request.urlopen", boom):
            c = Client(base=LOCKED_BASE, key=KEY, dry_run=True)
            res = c.clip_realman("tpl", "https://x/v.mp4", title="T")
        self.assertTrue(res["dry_run"])

    def test_multipart_upload_body(self):
        seen = {}

        def fake_urlopen(req, timeout=None):
            seen["body"] = req.data
            seen["ctype"] = req.get_header("Content-type")
            return fake_response({"code": 1, "msg": "ok", "data": {"url": "https://x/u.mp4"}})

        import tempfile
        fd, path = tempfile.mkstemp(suffix=".mp4")
        try:
            with os.fdopen(fd, "wb") as fh:
                fh.write(b"FAKEMP4DATA")
            with mock.patch("urllib.request.urlopen", fake_urlopen):
                Client(base=LOCKED_BASE, key=KEY).upload(path)
        finally:
            os.unlink(path)
        self.assertIn("multipart/form-data; boundary=", seen["ctype"])
        self.assertIn(b'name="file"', seen["body"])
        self.assertIn(b"FAKEMP4DATA", seen["body"])


def _raw_response(blob):
    class Resp(io.BytesIO):
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self, *a):
            return blob

    return Resp()


class TestWaitTask(unittest.TestCase):
    def test_polls_until_terminal(self):
        states = [{"status": "pending"}, {"status": "processing"},
                  {"status": "completed", "result": {"video_url": "https://v/final.mp4"}}]
        calls = {"n": 0}

        def fake_urlopen(req, timeout=None):
            i = min(calls["n"], len(states) - 1)
            calls["n"] += 1
            return fake_response({"code": 1, "msg": "ok", "data": states[i]})

        with mock.patch("urllib.request.urlopen", fake_urlopen), \
                mock.patch("time.sleep", lambda *_: None):
            c = Client(base=LOCKED_BASE, key=KEY)
            res = c.wait_task("t1", interval=0.01, max_wait=10)
        self.assertEqual(res["status"], "completed")
        self.assertEqual(find_deep(res["data"], dhclip.VIDEO_KEYS), "https://v/final.mp4")

    def test_failure_raises(self):
        def fake_urlopen(req, timeout=None):
            return fake_response({"code": 1, "msg": "ok",
                                  "data": {"status": "failed", "error": {"message": "渲染异常"}}})

        with mock.patch("urllib.request.urlopen", fake_urlopen), \
                mock.patch("time.sleep", lambda *_: None):
            with self.assertRaises(dhclip.CliError) as ctx:
                Client(base=LOCKED_BASE, key=KEY).wait_task("t1", max_wait=5)
        self.assertIn("渲染异常", str(ctx.exception))

    def test_completed_with_empty_url_keeps_polling(self):
        """实测坑：刚翻成 completed 时 video_url 还是空串，几秒后才落全。

        没有 require_keys 兜底就会"任务完成了却报没有视频"。
        """
        states = [
            {"status": "completed", "result": {"video_url": ""}},
            {"status": "completed", "result": {"video_url": ""}},
            {"status": "completed", "result": {"video_url": "https://v/real.mp4"}},
        ]
        calls = {"n": 0}

        def fake_urlopen(req, timeout=None):
            i = min(calls["n"], len(states) - 1)
            calls["n"] += 1
            return fake_response({"code": 1, "msg": "ok", "data": states[i]})

        with mock.patch("urllib.request.urlopen", fake_urlopen), \
                mock.patch("time.sleep", lambda *_: None):
            res = Client(base=LOCKED_BASE, key=KEY).wait_task(
                "t1", interval=0.01, max_wait=10, require_keys=dhclip.VIDEO_KEYS,
                settle_wait=5)
        self.assertEqual(res["result_url"], "https://v/real.mp4")
        self.assertGreaterEqual(calls["n"], 3)

    def test_completed_with_forever_empty_url_gives_clear_error(self):
        def fake_urlopen(req, timeout=None):
            return fake_response({"code": 1, "msg": "ok",
                                  "data": {"status": "completed",
                                           "result": {"video_url": ""}}})

        with mock.patch("urllib.request.urlopen", fake_urlopen), \
                mock.patch("time.sleep", lambda *_: None):
            with self.assertRaises(dhclip.CliError) as ctx:
                Client(base=LOCKED_BASE, key=KEY).wait_task(
                    "t1", interval=0.01, max_wait=10, require_keys=dhclip.VIDEO_KEYS,
                    settle_wait=0)
        self.assertIn("结果地址", str(ctx.exception))

    def test_result_field_does_not_swallow_status(self):
        """data 里同时有 status 和 result 时，不能把 result 当包装层。"""
        data = unwrap({"code": 1, "msg": "ok", "data": {
            "status": "completed", "result": {"video_url": "https://v/x.mp4"}}})
        self.assertEqual(data.get("status"), "completed")
        self.assertEqual(find_deep(data, dhclip.VIDEO_KEYS), "https://v/x.mp4")

    def test_find_number_for_duration(self):
        self.assertEqual(dhclip.find_number({"result": {"duration": 4.88}}, ("duration",)), 4.88)
        self.assertEqual(dhclip.find_number({"duration": "12.5"}, ("duration",)), 12.5)
        self.assertIsNone(dhclip.find_number({"duration": "abc"}, ("duration",)))

    def test_wrapper_still_unwrapped_when_result_is_alone(self):
        """data 里只有 result 时，仍然要当包装层剥掉（形态 2）。"""
        data = unwrap({"code": 1, "msg": "ok", "data": {
            "result": {"code": "Succeed", "data": {"a": 1}}}})
        self.assertEqual(data, {"a": 1})

    def test_wrapper_unwrapped_even_with_usage_sibling(self):
        """实测形态：data 里 result 和 usage 并存，仍然要剥掉 result。

        中转层真实返回（模板列表）：
          {"code":1,"msg":"success","data":{
             "result":{"code":"Succeed","data":{"results":[...],"sid":"..."},
                       "requestId":"..."},
             "usage":{"points_cost":0,"actual_points":0}}}
        只看"other_keys 是否为空"会漏判，模板列表就永远是空的。
        """
        payload = {"code": 1, "msg": "success", "data": {
            "result": {"code": "Succeed",
                       "data": {"results": [{"id": "t1"}], "sid": "s1"},
                       "requestId": "r1"},
            "usage": {"points_cost": 0, "actual_points": 0}}}
        data = unwrap(payload)
        self.assertEqual(data["results"], [{"id": "t1"}])
        self.assertEqual(data["sid"], "s1")

    def test_task_result_with_siblings_keeps_status(self):
        """任务查询体里 result 是普通对象、data 还有 status/usage → 原样保留。"""
        payload = {"code": 1, "msg": "success", "data": {
            "task_id": "task_1", "status": "completed",
            "result": {"video_url": "https://v/x.mp4", "duration": 4.88},
            "usage": {"points_cost": 7.32}}}
        data = unwrap(payload)
        self.assertEqual(data["status"], "completed")
        self.assertEqual(data["task_id"], "task_1")
        self.assertEqual(data["result"]["video_url"], "https://v/x.mp4")

    def test_inner_failure_envelope_with_usage_sibling_raises(self):
        payload = {"code": 1, "msg": "success", "data": {
            "result": {"code": "Failed", "message": "上游炸了"},
            "usage": {"points_cost": 0}}}
        with self.assertRaises(ApiError) as ctx:
            unwrap(payload)
        self.assertIn("上游炸了", str(ctx.exception))


class TestCliBehaviour(unittest.TestCase):
    def setUp(self):
        self.env = mock.patch.dict(os.environ, {"AVATAR_AUTOCLIP_KEY": KEY}, clear=False)
        self.env.start()
        self.addCleanup(self.env.stop)

    def _no_network(self):
        return mock.patch("urllib.request.urlopen",
                          side_effect=AssertionError("不该发请求"))

    def test_dry_run_realman_no_request(self):
        with self._no_network():
            rc = dhclip.main([
                "realman", "--template", "tpl", "--video", "https://x/a.mp4",
                "--title", "T", "--material", "image=https://x/i.jpg", "--dry-run",
            ])
        self.assertEqual(rc, EXIT_OK)

    def test_dry_run_news_no_request(self):
        with self._no_network():
            rc = dhclip.main([
                "news", "--template", "tpl", "--title", "今天的新闻",
                "--material", "image=https://x/i.jpg", "--dry-run",
            ])
        self.assertEqual(rc, EXIT_OK)

    def test_authz_gate_blocks_lipsync(self):
        with self._no_network():
            rc = dhclip.main(["lipsync", "--image", "https://x/f.jpg",
                              "--audio", "https://x/a.mp3", "--dry-run"])
        self.assertEqual(rc, EXIT_AUTHZ)

    def test_authz_gate_allows_with_flag(self):
        with self._no_network():
            rc = dhclip.main(["lipsync", "--image", "https://x/f.jpg",
                              "--audio", "https://x/a.mp3", "--authorized", "--dry-run"])
        self.assertEqual(rc, EXIT_OK)

    def test_mixcut_rejects_unsupported_branch(self):
        with self._no_network():
            rc = dhclip.main(["mixcut", "--template", "tpl", "--content", "文案",
                              "--material", "image=https://x/i.jpg", "--dry-run"])
        self.assertEqual(rc, EXIT_VALIDATION)

    def test_news_requires_title(self):
        with self._no_network():
            rc = dhclip.main(["news", "--template", "tpl",
                              "--material", "image=https://x/i.jpg", "--dry-run"])
        self.assertEqual(rc, EXIT_VALIDATION)

    def test_news_title_length_gate(self):
        with self._no_network():
            rc = dhclip.main(["news", "--template", "tpl", "--title", "短",
                              "--material", "image=https://x/i.jpg", "--dry-run"])
        self.assertEqual(rc, EXIT_VALIDATION)

    def test_news_duration_gate(self):
        with self._no_network():
            rc = dhclip.main(["news", "--template", "tpl", "--title", "标题够长了",
                              "--material", "image=https://x/i.jpg",
                              "--video-duration", "999", "--dry-run"])
        self.assertEqual(rc, EXIT_VALIDATION)

    def test_bgm_volume_gate(self):
        with self._no_network():
            rc = dhclip.main(["realman", "--template", "tpl", "--video", "https://x/a.mp4",
                              "--bgm-volume", "3", "--dry-run"])
        self.assertEqual(rc, EXIT_VALIDATION)

    def test_url_reuse_gate(self):
        with self._no_network():
            rc = dhclip.main(["realman", "--template", "tpl", "--video", "https://x/same.mp4",
                              "--material", "video=https://x/same.mp4", "--dry-run"])
        self.assertEqual(rc, EXIT_VALIDATION)

    def test_missing_key_is_usage_error(self):
        with mock.patch.dict(os.environ, {}, clear=True), \
                mock.patch("dhclip.load_key", side_effect=dhclip.CliError("no key", EXIT_USAGE)):
            rc = dhclip.main(["balance"])
        self.assertEqual(rc, EXIT_USAGE)

    def test_global_flag_after_subcommand(self):
        """--json / --dry-run 写在子命令后面也要生效（argparse parents 的坑）。"""
        with self._no_network():
            rc = dhclip.main(["realman", "--template", "tpl", "--video", "https://x/a.mp4",
                              "--dry-run", "--json"])
        self.assertEqual(rc, EXIT_OK)

    def test_make_requires_one_of_audio_text_dhvideo(self):
        with self._no_network():
            rc = dhclip.main(["make", "--image", "https://x/f.jpg", "--authorized", "--dry-run"])
        self.assertEqual(rc, EXIT_VALIDATION)

    def test_make_dh_video_skips_lipsync(self):
        with self._no_network():
            rc = dhclip.main(["make", "--image", "https://x/f.jpg",
                              "--dh-video", "https://x/dh.mp4",
                              "--template", "tpl", "--authorized", "--dry-run", "--json"])
        self.assertEqual(rc, EXIT_OK)


class TestConstants(unittest.TestCase):
    def test_scene_mapping(self):
        self.assertEqual(dhclip.SCENE_TO_API["realMan"], "realman_broadcast")
        self.assertEqual(dhclip.SCENE_TO_API["oralMixCutting"], "broadcast_mixcut")
        self.assertEqual(dhclip.SCENE_TO_API["newsMixCutting"], "news_mixcut")

    def test_limits_match_docs(self):
        self.assertEqual(LIMITS["single_side_px"], 2000)
        self.assertEqual(LIMITS["portrait_max_sec"], 300.0)
        self.assertEqual(LIMITS["subtitle_max_ms"], 310000)
        self.assertEqual(LIMITS["news_duration_sec"], (5, 300))
        self.assertEqual(LIMITS["material_video_max_sec"], 60.0)


class TestReferenceImage(unittest.TestCase):
    """参考生图（nano_banana action=edit）。"""

    def test_collect_image_urls_three_layers(self):
        """实测图片地址同时出现在 result.image_url / data[] / results[] 三层。"""
        payload = {
            "image_url": "https://c/a.png",
            "data": [{"image_url": "https://c/a.png"}, {"image_url": "https://c/b.png"}],
            "results": [{"image_url": "https://c/c.png"}],
        }
        urls = dhclip.collect_image_urls(payload)
        self.assertEqual(urls, ["https://c/a.png", "https://c/b.png", "https://c/c.png"])

    def test_collect_image_urls_ignores_non_http(self):
        self.assertEqual(dhclip.collect_image_urls({"image_url": "/local/x.png"}), [])

    def test_edit_action_sends_image_urls(self):
        seen = {}

        def fake_urlopen(req, timeout=None):
            seen["body"] = json.loads(req.data.decode("utf-8"))
            return fake_response({"code": 1, "msg": "ok", "data": {"task_id": "t1"}})

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            Client(base=LOCKED_BASE, key=KEY).image_generate(
                "换个厨房背景", ref_url="https://c/ref.jpg", aspect_ratio="9:16")
        self.assertEqual(seen["body"]["action"], "edit")
        self.assertEqual(seen["body"]["image_urls"], ["https://c/ref.jpg"])
        self.assertEqual(seen["body"]["aspect_ratio"], "9:16")

    def test_no_ref_falls_back_to_generate(self):
        seen = {}

        def fake_urlopen(req, timeout=None):
            seen["body"] = json.loads(req.data.decode("utf-8"))
            return fake_response({"code": 1, "msg": "ok", "data": {"task_id": "t1"}})

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            Client(base=LOCKED_BASE, key=KEY).image_generate("一张海报")
        self.assertEqual(seen["body"]["action"], "generate")
        self.assertNotIn("image_urls", seen["body"])

    def test_shot_prompt_keeps_identity_prefix(self):
        prompt = dhclip.build_shot_prompt("在厨房说话")
        self.assertIn("同一个人的面部特征", prompt)
        self.assertIn("在厨房说话", prompt)

    def test_portraits_requires_ref_unless_allowed(self):
        with mock.patch.dict(os.environ, {"AVATAR_AUTOCLIP_KEY": KEY}):
            with mock.patch("urllib.request.urlopen",
                            side_effect=AssertionError("不该发请求")):
                rc = dhclip.main(["portraits", "--n", "2", "--dry-run"])
                self.assertEqual(rc, EXIT_USAGE)
                rc = dhclip.main(["portraits", "--n", "1", "--allow-no-ref", "--dry-run"])
                self.assertEqual(rc, EXIT_OK)

    def test_portraits_needs_authorization(self):
        with mock.patch.dict(os.environ, {"AVATAR_AUTOCLIP_KEY": KEY}, clear=False):
            with mock.patch("urllib.request.urlopen",
                            side_effect=AssertionError("不该发请求")):
                rc = dhclip.main(["portraits", "--ref", "https://c/r.jpg", "--dry-run"])
        self.assertEqual(rc, EXIT_AUTHZ)


class TestAsrSubtitles(unittest.TestCase):
    """ASR → subtitle[]。实测 stt(ignore_timestamps=false) 返回字级秒。"""

    RAW = {"result": {
        "duration": 2.0636875, "language": "Chinese", "language_code": "zh",
        "segments": [
            {"end": 0.16, "start": 0, "text": "大"},
            {"end": 0.32, "start": 0.16, "text": "家"},
            {"end": 0.56, "start": 0.32, "text": "好"},
            {"end": 0.72, "start": 0.56, "text": "欢"},
            {"end": 0.8, "start": 0.8, "text": "迎"},     # 零时长段（实测真出现过）
            {"end": 0.96, "start": 0.8, "text": "来"},
        ],
        "text": "大家好，欢迎来",
    }}

    def test_seconds_converted_to_ms(self):
        subs = dhclip.subtitles_from_asr(self.RAW)
        self.assertEqual(subs[0]["startMs"], 0)
        self.assertEqual(subs[0]["endMs"], 160)

    def test_punctuation_reattached(self):
        subs = dhclip.subtitles_from_asr(self.RAW)
        self.assertEqual(subs[2]["text"], "好，")

    def test_zero_duration_segment_fixed(self):
        """实测有 {"start":0.8,"end":0.8} 这种段，上游要求 endMs > startMs。"""
        subs = dhclip.subtitles_from_asr(self.RAW)
        for item in subs:
            self.assertGreater(item["endMs"], item["startMs"])
        self.assertEqual(dhclip.validate_subtitle(subs), [])

    def test_monotonic_non_overlapping(self):
        subs = dhclip.subtitles_from_asr(self.RAW)
        for prev, nxt in zip(subs, subs[1:]):
            self.assertLessEqual(nxt["startMs"], nxt["endMs"])
            self.assertGreaterEqual(nxt["startMs"], prev["startMs"])

    def test_alignment_skipped_when_text_mismatch(self):
        """完整文本和分段对不上时不能硬塞标点（对齐失败就不猜）。"""
        payload = {"result": {"segments": [{"start": 0, "end": 0.2, "text": "甲"},
                                           {"start": 0.2, "end": 0.4, "text": "乙"}],
                              "text": "完全不相干的内容"}}
        subs = dhclip.subtitles_from_asr(payload)
        self.assertEqual([s["text"] for s in subs], ["甲", "乙"])

    def test_ms_fields_supported(self):
        payload = {"segments": [{"startMs": 100, "endMs": 400, "text": "字"}]}
        subs = dhclip.subtitles_from_asr(payload)
        self.assertEqual(subs[0], {"startMs": 100, "endMs": 400, "text": "字"})

    def test_subtitle_cap_enforced(self):
        payload = {"segments": [{"start": 0, "end": 999999, "text": "长"}]}
        subs = dhclip.subtitles_from_asr(payload)
        self.assertLessEqual(subs[0]["endMs"], LIMITS["subtitle_max_ms"])

    def test_empty_when_no_segments(self):
        self.assertEqual(dhclip.subtitles_from_asr({"result": {"text": "只有全文"}}), [])

    def test_find_asr_segments_nested(self):
        deep = {"a": {"b": {"words": [{"start": 0, "end": 1, "text": "x"}]}}}
        self.assertEqual(len(dhclip._find_asr_segments(deep)), 1)


class TestCoverAndMakeFlags(unittest.TestCase):
    def setUp(self):
        self.env = mock.patch.dict(os.environ, {"AVATAR_AUTOCLIP_KEY": KEY}, clear=False)
        self.env.start()
        self.addCleanup(self.env.stop)

    def _no_network(self):
        return mock.patch("urllib.request.urlopen",
                          side_effect=AssertionError("不该发请求"))

    def test_make_requires_image_or_ref(self):
        with self._no_network():
            rc = dhclip.main(["make", "--text", "文案", "--authorized", "--dry-run"])
        self.assertEqual(rc, EXIT_VALIDATION)

    def test_make_ref_only_needs_text(self):
        with self._no_network():
            rc = dhclip.main(["make", "--ref", "https://c/r.jpg", "--text", "文案",
                              "--authorized", "--dry-run", "--json"])
        self.assertEqual(rc, EXIT_OK)

    def test_cover_flags_reach_request_body(self):
        seen = {}

        def fake_urlopen(req, timeout=None):
            seen["body"] = json.loads(req.data.decode("utf-8"))
            return fake_response({"code": 1, "msg": "ok", "data": {"task_id": "t1"}})

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            Client(base=LOCKED_BASE, key=KEY).clip_realman(
                "tpl", "https://c/v.mp4",
                processRules={"firstFrameCover": {"coverSwitch": True,
                                                  "resultImageUrl": "https://c/c.png"}})
        cover = seen["body"]["processRules"]["firstFrameCover"]
        self.assertTrue(cover["coverSwitch"])
        self.assertEqual(cover["resultImageUrl"], "https://c/c.png")

    def test_ai_label_metadata_shape(self):
        """AIGC 元水印的 value 必须是字符串（上游硬性要求）。"""
        md = dhclip.build_ai_label_metadata("某公司", "ID-9")
        self.assertEqual(list(md.keys()), ["AIGC"])
        inner = json.loads(md["AIGC"])
        self.assertEqual(inner["Label"], "1")
        self.assertEqual(inner["ContentProducer"], "某公司")
        self.assertEqual(inner["ProduceID"], "ID-9")

    def test_karaoke_flag_dry_run(self):
        with self._no_network():
            rc = dhclip.main(["make", "--image", "https://c/f.jpg", "--text", "文案",
                              "--karaoke", "--auto-cover", "--authorized", "--dry-run"])
        self.assertEqual(rc, EXIT_OK)


class TestSubtitleFallback(unittest.TestCase):
    """实测：上游对 subtitle[] 条数敏感（5 条过、12 条就挂）。

    所以带 subtitle 的任务失败时，要自动去掉 subtitle 重试一次。
    """

    def _client(self):
        return Client(base=LOCKED_BASE, key=KEY)

    def test_batch_retry_drops_subtitle(self):
        posts = []
        state = {"task": 0}

        def fake_urlopen(req, timeout=None):
            url = req.full_url
            method = req.get_method()
            if method == "POST" and "realman_broadcast" in url:
                body = json.loads(req.data.decode("utf-8"))
                posts.append(body)
                state["task"] += 1
                return fake_response({"code": 1, "msg": "ok",
                                      "data": {"task_id": "t%d" % state["task"]}})
            if "/tasks/" in url:
                tid = url.rsplit("/", 1)[-1]
                if tid == "t1":
                    return fake_response({"code": 1, "msg": "ok",
                                          "data": {"status": "failed",
                                                   "error": {"message": "任务处理失败"}}})
                return fake_response({"code": 1, "msg": "ok",
                                      "data": {"status": "completed",
                                               "result": {"video_url": "https://v/ok.mp4"}}})
            raise AssertionError("unexpected " + url)

        subs = [{"startMs": i * 500, "endMs": i * 500 + 400, "text": "字"}
                for i in range(12)]
        args = argparse.Namespace(wait=True, poll_interval=0.01, max_wait=5,
                                  app_query="", json=True, dry_run=False)
        with mock.patch("urllib.request.urlopen", fake_urlopen), \
                mock.patch("time.sleep", lambda *_: None):
            rc = dhclip._guarded_submit(
                self._client(), "realman_broadcast",
                {"styleId": "tpl", "videoUrl": "https://v/in.mp4", "subtitle": subs},
                [], args)
        self.assertEqual(rc, EXIT_OK)
        self.assertEqual(len(posts), 2, "应当重试一次")
        self.assertIn("subtitle", posts[0])
        self.assertNotIn("subtitle", posts[1], "重试必须去掉 subtitle")

    def test_no_subtitle_means_no_retry(self):
        posts = []

        def fake_urlopen(req, timeout=None):
            if req.get_method() == "POST":
                posts.append(json.loads(req.data.decode("utf-8")))
                return fake_response({"code": 1, "msg": "ok", "data": {"task_id": "t1"}})
            return fake_response({"code": 1, "msg": "ok",
                                  "data": {"status": "failed",
                                           "error": {"message": "任务处理失败"}}})

        args = argparse.Namespace(wait=True, poll_interval=0.01, max_wait=5,
                                  app_query="", json=True, dry_run=False)
        with mock.patch("urllib.request.urlopen", fake_urlopen), \
                mock.patch("time.sleep", lambda *_: None):
            with self.assertRaises(dhclip.CliError):
                dhclip._guarded_submit(
                    self._client(), "realman_broadcast",
                    {"styleId": "tpl", "videoUrl": "https://v/in.mp4"}, [], args)
        self.assertEqual(len(posts), 1, "没有 subtitle 就不该重试")


class TestTransientRetry(unittest.TestCase):
    """实测 `elastic_machine_lost_after_submit`（弹性机器丢失）是瞬时故障。

    失败任务不扣费，所以自动重提是正确做法 —— 否则用户得手工重跑一遍 60 秒的片子。
    """

    def test_recognises_machine_lost(self):
        payload = {"code": 1, "msg": "success", "data": {
            "status": "failed",
            "error": {"code": "elastic_machine_lost_after_submit",
                      "message": "任务处理失败，请稍后重试"}}}
        self.assertTrue(dhclip.is_transient_error(payload))

    def test_recognises_generic_retry_hint(self):
        self.assertTrue(dhclip.is_transient_error(
            {"error": {"message": "任务处理失败，请稍后重试"}}))
        self.assertTrue(dhclip.is_transient_error(
            {"data": {"code": "queue_limit_exceeded"}}))

    def test_real_failure_is_not_transient(self):
        payload = {"error": {"code": "invalid_request",
                             "message": "参数 image_url 非法"}}
        self.assertFalse(dhclip.is_transient_error(payload))
        self.assertFalse(dhclip.is_transient_error({"msg": "success"}))
        self.assertFalse(dhclip.is_transient_error(None))

    def test_dh_retries_then_succeeds(self):
        posts = {"n": 0}
        state = {"task": 0}

        def fake_urlopen(req, timeout=None):
            url = req.full_url
            if req.get_method() == "POST" and "pic_lipsync/submit" in url:
                posts["n"] += 1
                state["task"] += 1
                return fake_response({"code": 1, "msg": "ok",
                                      "data": {"task_id": "t%d" % state["task"]}})
            tid = url.rsplit("/", 1)[-1]
            if tid == "t1":
                return fake_response({"code": 1, "msg": "ok", "data": {
                    "status": "failed",
                    "error": {"code": "elastic_machine_lost_after_submit",
                              "message": "任务处理失败，请稍后重试"}}})
            return fake_response({"code": 1, "msg": "ok", "data": {
                "status": "completed",
                "result": {"data": {"output_url": "https://v/dh.mp4"}}}})

        args = argparse.Namespace(wait=True, poll_interval=0.01, max_wait=5,
                                  app_query="", json=True, dry_run=False)
        with mock.patch("urllib.request.urlopen", fake_urlopen), \
                mock.patch("time.sleep", lambda *_: None):
            video = dhclip.submit_dh_and_wait(
                Client(base=LOCKED_BASE, key=KEY), args,
                "https://c/f.jpg", "https://c/a.mp3", quality="max")
        self.assertEqual(video, "https://v/dh.mp4")
        self.assertEqual(posts["n"], 2, "瞬时故障后应当重新提交")

    def test_dh_does_not_retry_real_failure(self):
        posts = {"n": 0}

        def fake_urlopen(req, timeout=None):
            if req.get_method() == "POST":
                posts["n"] += 1
                return fake_response({"code": 1, "msg": "ok", "data": {"task_id": "t1"}})
            return fake_response({"code": 1, "msg": "ok", "data": {
                "status": "failed",
                "error": {"code": "invalid_request", "message": "图片不可用"}}})

        args = argparse.Namespace(wait=True, poll_interval=0.01, max_wait=5,
                                  app_query="", json=True, dry_run=False)
        with mock.patch("urllib.request.urlopen", fake_urlopen), \
                mock.patch("time.sleep", lambda *_: None):
            with self.assertRaises(dhclip.CliError):
                dhclip.submit_dh_and_wait(
                    Client(base=LOCKED_BASE, key=KEY), args,
                    "https://c/f.jpg", "https://c/a.mp3")
        self.assertEqual(posts["n"], 1, "真实参数错误不该重试")


class TestMergeSubtitles(unittest.TestCase):
    def _chars(self):
        return json.loads(
            '[' + ",".join(
                '{"startMs":%d,"endMs":%d,"text":"%s"}' % (i * 200, i * 200 + 200, c)
                for i, c in enumerate("大家好，欢迎来到今天的分享。")) + ']')

    def test_merges_and_breaks_on_punctuation(self):
        merged = dhclip.merge_subtitles(self._chars(), max_chars=18)
        self.assertLess(len(merged), len(self._chars()))
        self.assertTrue(any(m["text"].endswith("，") for m in merged))
        self.assertEqual(dhclip.validate_subtitle(merged), [])

    def test_text_is_preserved(self):
        chars = self._chars()
        merged = dhclip.merge_subtitles(chars, max_chars=18)
        self.assertEqual("".join(m["text"] for m in merged),
                         "".join(c["text"] for c in chars))

    def test_hard_end_clamps(self):
        merged = dhclip.merge_subtitles(self._chars(), max_chars=99, hard_end_ms=1000)
        for item in merged:
            self.assertLessEqual(item["endMs"], 1000)

    def test_empty_input(self):
        self.assertEqual(dhclip.merge_subtitles([]), [])

    def test_respects_max_chars(self):
        merged = dhclip.merge_subtitles(self._chars(), max_chars=4)
        for item in merged:
            self.assertLessEqual(len(item["text"]), 5)
        self.assertEqual(dhclip.validate_subtitle(merged), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
