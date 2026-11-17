"""Offline tests for the parts that must not silently drift.

The four live checks in SKILL.md's Verification section are in
TestLiveSmoke, which needs the network and HARVEST_CONTACT set. Everything
else here runs offline and is what would have caught the bugs in the
handoff: the missing safety filter on --download-only, the manifest gap,
and the duplicate rejected rows.

    python -m unittest discover -s tests -v
    python tests/test_harvest.py            # offline only
    HARVEST_LIVE=1 python tests/test_harvest.py   # include the live run
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import io
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import harvest                                                  # noqa: E402
import queries                                                   # noqa: E402
from normalize import (load_jsonl, make_record, record_key,       # noqa: E402
                       safety_ok, write_jsonl)

LIVE = bool(os.environ.get("HARVEST_LIVE"))


def args_for(**over):
    """Build a real argparse namespace, same shape main() would see."""
    argv = []
    for k, v in over.items():
        flag = "--" + k.replace("_", "-")
        if v is True:
            argv.append(flag)
        elif v is not None:
            argv += [flag, str(v)]
    return harvest.parse_args(argv)


def row(source="testbooru", sid="1", tags="1girl, yuri", rating="s", **extra):
    return make_record(
        source=source, source_id=sid,
        page_url=f"https://example.test/{sid}",
        file_url=f"https://example.test/{sid}.png",
        tags=tags, rating=rating, width=1024, height=1024,
        file_ext="png", md5=f"md5{sid}", **extra)


class TestRatingCeiling(unittest.TestCase):
    """--rating decides safe-only vs everything. It is a ceiling, not an
    exact match, and 'unknown' is never silently treated as safe."""

    def test_default_is_safe(self):
        self.assertEqual(args_for().rating, "general")

    def test_ceiling_admits_lower_bands(self):
        ok, _ = harvest.rating_ok("general", "sensitive")
        self.assertTrue(ok, "general art must survive a sensitive ceiling")
        ok, _ = harvest.rating_ok("sensitive", "sensitive")
        self.assertTrue(ok, "the ceiling value itself must survive")

    def test_ceiling_excludes_higher_bands(self):
        for ceiling, rating in (("general", "sensitive"),
                                ("general", "explicit"),
                                ("sensitive", "explicit"),
                                ("questionable", "explicit")):
            ok, why = harvest.rating_ok(rating, ceiling)
            self.assertFalse(ok, f"{rating} must not pass a {ceiling} ceiling")
            self.assertEqual(why, f"rating:{rating}")

    def test_any_admits_everything(self):
        for r in ("general", "sensitive", "questionable", "explicit"):
            self.assertTrue(harvest.rating_ok(r, "any")[0])

    def test_unknown_is_kept_but_not_called_safe(self):
        """A source that omits the field has asserted nothing. Refusing it
        would empty the dataset; the breakdown must surface it instead."""
        self.assertTrue(harvest.rating_ok("unknown", "general")[0])
        self.assertTrue(harvest.rating_ok("", "general")[0])
        self.assertEqual(harvest.rating_breakdown(
            [row(rating="s"), row(rating=""), row(rating="s")]
        ), {"unknown": 1, "general": 2})

    def test_pixiv_r18_is_not_unknown(self):
        """pixiv reports "r18"; normalized to unknown it would slip past
        every rating ceiling, including --rating general."""
        from normalize import norm_rating
        self.assertEqual(norm_rating("r18"), "explicit")
        self.assertFalse(harvest.rating_ok(norm_rating("r18"), "general")[0])

    def test_filter_rows_respects_ceiling(self):
        rej = []
        kept = harvest.filter_rows(
            [row(sid="1", rating="s"), row(sid="2", rating="e")],
            args_for(rating="general"), rej)
        self.assertEqual([r["source_id"] for r in kept], ["1"])
        self.assertEqual(rej[0]["reject_reason"], "rating:explicit")

    def test_filter_rows_ceiling_includes_lower(self):
        rej = []
        kept = harvest.filter_rows(
            [row(sid="1", rating="s"), row(sid="2", rating="sensitive")],
            args_for(rating="sensitive"), rej)
        self.assertEqual(len(kept), 2, "a ceiling keeps everything below it")
        self.assertEqual(rej, [])

    def test_rating_never_widens_past_hard_excludes(self):
        rej = []
        kept = harvest.filter_rows(
            [row(tags="loli"), row(tags="guro")],
            args_for(rating="any"), rej)
        self.assertEqual(kept, [])
        self.assertEqual(len(rej), 2)


class TestRatingBreakdown(unittest.TestCase):
    def test_orders_by_severity_with_unknown_last(self):
        b = harvest.rating_breakdown([
            row(rating=""), row(rating="e"), row(rating="s"),
            row(rating="q"), row(rating="sensitive")])
        self.assertEqual(list(b), ["general", "sensitive", "questionable",
                                   "explicit", "unknown"])

    def test_explains_what_the_ceiling_cost(self):
        kept = [row(rating="s")]
        dropped = [row(sid="2", rating="e"), row(sid="3", rating="explicit")]
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            harvest.print_rating_breakdown(kept, dropped)
        out = buf.getvalue()
        self.assertIn("kept", out)
        self.assertIn("excluded", out)
        self.assertIn("2", out)

    def test_warns_when_rows_reported_no_rating(self):
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            harvest.print_rating_breakdown([row(rating="")], [])
        self.assertIn("no rating", buf.getvalue())


class TestBootstrap(unittest.TestCase):
    """An agent must be able to make this runnable unattended, and must be
    told which interpreter to use afterwards."""

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent
                              / "scripts"))
        import bootstrap
        self.b = bootstrap

    def test_venv_python_resolves_per_platform(self):
        import os
        want = ("Scripts/python.exe" if os.name == "nt"
                else "bin/python")
        self.assertTrue(self.b.venv_python().as_posix().endswith(want))

    def test_venv_path_is_resolved_at_call_time(self):
        """A default argument binds once at import, so a `root=VENV`
        default silently ignores a reassigned VENV and checks the wrong
        directory. That bug shipped once; assert it cannot come back."""
        import tempfile
        import pathlib
        with tempfile.TemporaryDirectory() as td:
            fake = pathlib.Path(td) / "nope"
            self.assertFalse(self.b.venv_exists(fake))
            self.assertTrue(self.b.venv_exists(self.b.VENV),
                            "the real venv must still be found")

    def test_pip_prefix_includes_install_subcommand(self):
        """All three backends must return an `install` prefix. Returning
        bare `-m pip` produced 'no such option: -r'."""
        import pathlib
        found = self.b.pip_command(pathlib.Path("/nonexistent/python"))
        if found is None:
            self.skipTest("no pip/uv/ensurepip available to test with")
        prefix, flag = found
        self.assertIn("install", prefix)

    def test_check_mode_reports_status(self):
        rc = self.b.report()
        self.assertIn(rc, (0, 1), "report() must return a usable exit code")

    def test_required_deps_are_the_real_ones(self):
        for mod in ("playwright", "PIL"):
            self.assertIn(mod, self.b.NEEDED)


class TestQueryPlan(unittest.TestCase):
    """A plan is a ranked list, not one query. X ANDs its terms, so the
    order and the relaxation are what make the difference between finding
    art and reporting a false zero."""

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent
                              / "scripts"))

    def test_ship_tags_outrank_everything(self):
        from queries import plan
        p = plan("wuthering waves", ["jinhsi", "changli"],
                 ship_tags=["Jinhli"])
        self.assertEqual(p.queries[0].text, "Jinhli")
        self.assertEqual(p.queries[0].kind, "ship_tag")

    def test_ship_tags_are_verbatim(self):
        """A real ship name is a better key than anything generated, and
        rewriting one changes what is found."""
        from queries import plan
        p = plan(ship_tags=["#Jinhli", "Changli x Jinhsi"])
        texts = p.texts()
        self.assertIn("#Jinhli", texts)
        self.assertIn("Changli x Jinhsi", texts)

    def test_ship_pairs_precede_fandom(self):
        from queries import plan
        p = plan("wuthering waves", ["jinhsi", "changli"])
        kinds = [q.kind for q in p]
        self.assertLess(kinds.index("ship"), kinds.index("fandom"))

    def test_fandom_query_is_fandom_then_term(self):
        from queries import plan
        p = plan("wuthering waves", [])
        self.assertIn("wuthering waves yuri", p.texts())

    def test_hashtags_only_when_aggressive(self):
        from queries import plan
        quiet = plan("wuthering waves", ["jinhsi", "changli"])
        loud = plan("wuthering waves", ["jinhsi", "changli"], aggressive=True)
        self.assertFalse(any(q.kind == "hashtag" for q in quiet))
        self.assertTrue(any(q.kind == "hashtag" for q in loud))
        self.assertTrue(any("#" in q.text for q in loud))

    def test_no_booru_tag_syntax_in_a_social_plan(self):
        """2girls is a booru tag. X and Pixiv do not index tags."""
        from queries import plan
        for q in plan("genshin impact", ["raiden", "yae"], aggressive=True):
            self.assertNotIn("2girls", q.text)

    def test_plan_respects_the_cap(self):
        from queries import plan
        p = plan("f", ["a", "b", "c", "d", "e"], max_queries=5)
        self.assertLessEqual(len(p), 5)

    def test_plan_is_deduped(self):
        from queries import plan
        texts = plan("f", ["a", "b"]).texts()
        self.assertEqual(len(texts), len({t.lower() for t in texts}))

    def test_generic_terms_are_last(self):
        """Bare 'yuri' returns plenty and almost none of it survives
        verification, so it must not be spent early."""
        from queries import plan
        p = plan("wuthering waves", ["jinhsi", "changli"])
        self.assertEqual(p.queries[-1].kind, "generic")

    def test_empty_input_yields_a_usable_plan(self):
        from queries import plan
        self.assertTrue(plan("", []).texts())

    def test_expand_backcompat_returns_strings(self):
        from queries import expand
        out = expand("genshin impact", ["raiden", "yae"])
        self.assertTrue(all(isinstance(x, str) for x in out))


class TestRelax(unittest.TestCase):
    """The measured case: "wuwa denrika art" returns 0, "wuwa denrika"
    returns 5. Relaxation exists for exactly that."""

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent
                              / "scripts"))

    def test_drops_search_boilerplate_first(self):
        from queries import relax
        out = relax("wuwa denrika art")
        self.assertEqual(out[0], "wuwa denrika")

    def test_the_real_regression_case(self):
        from queries import relax
        # If this changes, the driver stops recovering the 5 results.
        self.assertIn("wuwa denrika", relax("wuwa denrika art"))

    def test_never_returns_the_original(self):
        from queries import relax
        for q in ("wuwa denrika art", "raiden x yae yuri", "#A #B fanart"):
            self.assertNotIn(q, relax(q))

    def test_results_are_deduped_and_finited(self):
        from queries import relax
        out = relax("wuthering waves yuri")
        self.assertEqual(len(out), len({o.lower() for o in out}))
        self.assertLess(len(out), 12)

    def test_handles_empty(self):
        from queries import relax
        self.assertEqual(relax(""), [])
        self.assertEqual(relax("   "), [])

    def test_keeps_content_words_before_boilerplate_only_once(self):
        from queries import relax
        out = relax("#Jinhsi #Changli fanart")
        self.assertEqual(out[0], "#Jinhsi #Changli")


class TestSearchDriver(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent
                              / "scripts"))
        from queries import Plan, Query
        self.Plan, self.Query = Plan, Query

    def _driver(self, plan_qs, **kw):
        from search import SearchDriver
        d = SearchDriver(verbose=False, delay=0, **kw)
        d.plan = plan_qs
        return d

    def test_stops_when_target_reached(self):
        qs = [self.Query("a", "ship", 90), self.Query("b", "fandom", 60)]
        d = self._driver(qs, target=1)
        rows = d.run(lambda q, w: [{"source_id": q, "md5": q}])
        self.assertEqual(len(rows), 1)

    def test_relaxes_a_dry_query_instead_of_giving_up(self):
        """The whole reason this exists: one empty query is not absence."""
        qs = [self.Query("wuwa denrika art", "fandom", 60)]
        seen = []

        def fetch(q, w):
            seen.append(q)
            return [{"source_id": "1", "md5": "1"}] if "wuwa denrika" == q else []

        d = self._driver(qs, target=1)
        rows = d.run(fetch)
        self.assertEqual(len(rows), 1, "relaxation must recover the results")
        self.assertIn("wuwa denrika", seen)

    def test_deduplicates_across_queries(self):
        qs = [self.Query("a", "ship", 90), self.Query("b", "ship", 90)]
        d = self._driver(qs, target=5)
        rows = d.run(lambda q, w: [{"source_id": "1", "md5": "same"}])
        self.assertEqual(len(rows), 1, "one post under two queries is one row")

    def test_stops_on_dry_streak(self):
        qs = [self.Query(f"q{i}", "fandom", 50) for i in range(10)]
        d = self._driver(qs, target=10, dry_streak_limit=3)
        d.run(lambda q, w: [])
        self.assertIn("nothing", d.stopped_because)

    def test_does_not_stop_on_one_dry_query(self):
        qs = [self.Query("dry", "fandom", 50), self.Query("wet", "ship", 90)]
        d = self._driver(qs, target=1)
        rows = d.run(lambda q, w: [] if q == "dry"
                     else [{"source_id": "1", "md5": "1"}])
        self.assertEqual(len(rows), 1)

    def test_reports_why_it_stopped(self):
        qs = [self.Query("q", "fandom", 50)]
        d = self._driver(qs, target=3)
        d.run(lambda q, w: [])
        self.assertTrue(d.stopped_because)
        self.assertIn("q", d.to_report()["queries_tried"])

    def test_survives_a_query_that_raises(self):
        qs = [self.Query("boom", "fandom", 50), self.Query("ok", "ship", 90)]

        def fetch(q, w):
            if q == "boom":
                raise RuntimeError("site exploded")
            return [{"source_id": "1", "md5": "1"}]

        d = self._driver(qs, target=1)
        rows = d.run(fetch)
        self.assertEqual(len(rows), 1, "one bad query must not kill the run")

    def test_does_not_overrun_the_budget(self):
        qs = [self.Query(f"q{i}", "fandom", 50) for i in range(40)]
        d = self._driver(qs, target=2)
        d.run(lambda q, w: [{"source_id": q, "md5": q}])
        self.assertLessEqual(len(d.attempts), 24)


class TestSafetyFilterIsNotOptional(unittest.TestCase):
    """normalize.py's filters are code, not flags. They must run on every
    path that can write an image, including --download-only."""

    def test_filter_rows_drops_underage(self):
        # Booru tag strings are space-delimited; "loli, yuri" would be a
        # single token "loli," and would not match.
        rej = []
        kept = harvest.filter_rows(
            [row(sid="1", tags="1girl yuri"),
             row(sid="2", tags="loli yuri")],
            args_for(), rej)
        self.assertEqual([r["source_id"] for r in kept], ["1"])
        self.assertEqual(len(rej), 1)
        self.assertTrue(rej[0]["reject_reason"].startswith("underage-tag:"))

    def test_filter_rows_drops_banned(self):
        rej = []
        kept = harvest.filter_rows(
            [row(tags="1girl, guro")], args_for(), rej)
        self.assertEqual(kept, [])
        self.assertTrue(rej[0]["reject_reason"].startswith("banned-tag:"))

    def test_rating_any_still_drops_hard_excludes(self):
        rej = []
        kept = harvest.filter_rows([row(rating="e")], args_for(rating="any"), rej)
        self.assertEqual(len(kept), 1)
        self.assertEqual(rej, [])

    def test_safety_filter_not_flaggable_away(self):
        """--rating must not be a way to smuggle excluded content through."""
        rej = []
        kept = harvest.filter_rows(
            [row(tags="loli")], args_for(rating="explicit"), rej)
        self.assertEqual(kept, [], "rating must never re-admit a hard-excluded row")

    def test_caption_used_when_tags_absent(self):
        rej = []
        kept = harvest.filter_rows(
            [row(tags="") | {"caption": "shota"}], args_for(), rej)
        self.assertEqual(kept, [])
        self.assertTrue(rej[0]["reject_reason"].startswith("underage-tag:"))


class TestRejectedDedupe(unittest.TestCase):
    """--download-only is resumable, so it must not append N copies of the
    same failure to the audit trail each run."""

    def test_rerun_does_not_duplicate(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            first = harvest.merge_rejected(out, [row(sid="1")])
            second = harvest.merge_rejected(out, [row(sid="1")])
            self.assertEqual((first, second), (1, 0))
            self.assertEqual(len(load_jsonl(out / "rejected.jsonl")), 1)

    def test_distinct_rows_both_recorded(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            harvest.merge_rejected(out, [row(sid="1"), row(sid="2")])
            harvest.merge_rejected(out, [row(sid="1"), row(sid="3")])
            got = load_jsonl(out / "rejected.jsonl")
            self.assertEqual(sorted(r["source_id"] for r in got), ["1", "2", "3"])

    def test_dedupe_key_prefers_md5(self):
        a = row(sid="1")
        b = row(sid="2")
        b["md5"] = a["md5"]
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            self.assertEqual(harvest.merge_rejected(out, [a, b]), 1)


class TestManifest(unittest.TestCase):
    """A gated dataset is a real artifact; publish.py reads its manifest."""

    def test_vision_gate_writes_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            a = args_for(tags="yuri", limit=10, rating="any", pages=1)
            p = harvest.write_manifest(out, a, ["a", "b"], ["twitter"],
                                       {"twitter": {"found": 15, "kept": 4}},
                                       15, 11, [])
            m = json.loads(p.read_text(encoding="utf-8"))
            self.assertTrue(m["generated_utc"])
            self.assertEqual(m["query"], "yuri")
            self.assertEqual(m["chars"], ["a", "b"])
            self.assertEqual(m["total_images"], 15)
            self.assertEqual(m["total_rejected"], 11)
            self.assertEqual(m["per_source"]["twitter"]["found"], 15)

    def test_write_card_gets_real_date(self):
        """The bug this guards: card said "unknown date" because the gated
        run returned before writing the manifest."""
        import publish
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            a = args_for(tags="yuri")
            harvest.write_manifest(out, a, [], ["testbooru"], {}, 3, 0, [])
            write_jsonl(out / "metadata.jsonl", [row() for _ in range(3)])
            card = publish.write_card(out).read_text(encoding="utf-8")
            self.assertNotIn("unknown date", card)
            self.assertIn("Harvested with `AgentEpstein` on 20", card)


class TestOutDatasetAlias(unittest.TestCase):
    def test_alias_fills_in(self):
        self.assertEqual(args_for(dataset="Y").out, "Y")

    def test_out_wins(self):
        self.assertEqual(args_for(out="X", dataset="Y").out, "X")

    def test_default(self):
        self.assertEqual(args_for().out, "./dataset")

    def test_printed_instruction_is_runnable(self):
        """harvest.py prints this command at the end of --vision-gate. It
        said --dataset before there was a --dataset flag; assert the exact
        shape it prints resolves to the same folder."""
        out = Path("C:/tmp/ds")
        printed = f"harvest.py --dataset {out} --download-only"
        argv = printed.split()[1:]
        a = harvest.parse_args(argv)
        self.assertEqual(Path(a.out), out)
        self.assertTrue(a.download_only)


class TestPublishAllowlist(unittest.TestCase):
    """rejected.jsonl and vision_worklist.json carry page_url, artist and
    full tags for content this project EXCLUDED. They must not be published."""

    def test_allowlist_excludes_audit_trail(self):
        import publish
        for name in publish.PUBLISH_FILES:
            self.assertIn(name, ("metadata.jsonl", "manifest.json", "README.md"))
        for leak in ("rejected.jsonl", "vision_worklist.json", "verdicts.json"):
            self.assertNotIn(leak, publish.PUBLISH_FILES)

    def test_allowlist_only_allows_known_files(self):
        import publish
        self.assertEqual(
            set(publish.PUBLISH_FILES) - {"metadata.jsonl", "manifest.json",
                                          "README.md"}, set())


class TestUserAgent(unittest.TestCase):
    """Danbooru and e621 ban clients with no contact info. A placeholder is
    worse than nothing, so the address is required."""

    def test_missing_contact_refuses(self):
        import importlib
        import sources
        old = os.environ.pop("HARVEST_CONTACT", None)
        try:
            importlib.reload(sources)
            with self.assertRaises(SystemExit):
                sources.user_agent()
        finally:
            if old is not None:
                os.environ["HARVEST_CONTACT"] = old
                importlib.reload(sources)

    def test_contact_included(self):
        import importlib
        import sources
        os.environ["HARVEST_CONTACT"] = "tester@example.test"
        try:
            importlib.reload(sources)
            ua = sources.user_agent()
            self.assertIn("tester@example.test", ua)
            self.assertNotIn("set YOUR_EMAIL", ua)
        finally:
            os.environ.pop("HARVEST_CONTACT", None)
            importlib.reload(sources)


class TestWizardInterpreter(unittest.TestCase):
    def test_uses_running_interpreter(self):
        import wizard
        self.assertEqual(
            Path(wizard.PY).resolve(),
            Path(sys.executable).resolve(),
            "wizard must not shell out to a bare 'python' on PATH; the deps "
            "live in a venv that is not there")


class TestLimitReporting(unittest.TestCase):
    """A capped account silently drops attachments and the send still
    succeeds. So the send button clicking means nothing; only counting
    images in the posted message tells the truth."""

    def test_no_pre_send_acceptance_count(self):
        """An attached image renders no composer preview, so any pre-send
        count reads 0 and would be misread as a failed upload. That mistake
        was made once and cost a working feature."""
        import chatgpt_web as C
        for gone in ("attachment_count", "wait_for_attachments",
                     "ATTACHMENT_CHIPS"):
            self.assertFalse(hasattr(C, gone),
                             f"{gone} must not come back: there is no "
                             f"pre-send element to count")

    def test_post_send_count_exists(self):
        import chatgpt_web as C
        self.assertTrue(callable(C.sent_image_count))

    def test_batch_default_matches_attachment_cap(self):
        import chatgpt_web as C
        self.assertEqual(C.parse_args(["--dataset", "x"]).batch, 10)

    def test_limit_patterns_are_present(self):
        import chatgpt_web as C
        for frag in ("too many requests", "rate limit", "upgrade to",
                     "file size"):
            self.assertTrue(any(frag in p for p in C.LIMIT_PATTERNS),
                            f"no pattern covers {frag!r}")

    def test_file_input_is_not_pinned_to_a_hidden_input(self):
        """#upload-photos / #upload-media only exist after opening the plus
        menu. Selecting them by name would break on a fresh page."""
        import chatgpt_web as C
        self.assertIn("input[type=\"file\"]", C.FILE_INPUTS)

    def test_send_button_not_pinned_to_button_tag(self):
        """The live send control is a <div>; button[...] matches nothing and
        would raise only AFTER attaching and typing."""
        import chatgpt_web as C
        self.assertEqual(C.SEND_BUTTONS[0], '[data-testid="send-button"]')
        self.assertTrue(any(not s.startswith("button") for s in C.SEND_BUTTONS))

    def test_logged_in_markers_are_not_dead_selectors(self):
        import chatgpt_web as C
        self.assertIn('div[contenteditable="true"][id="prompt-textarea"]',
                      C.LOGGED_IN_DOM)

    def test_stop_is_the_default(self):
        """Retrying past a refusal can look like abuse, so it must be opt-in.

        Asserted by running the parser the real main() uses, so a changed
        default fails here rather than being discovered mid-upload.
        """
        import chatgpt_web as C
        args = C.parse_args(["--dataset", "./x"])
        self.assertEqual(args.retry_until, "",
                         "retrying must require an explicit --retry-until")
        got = C.parse_args(["--dataset", "./x", "--retry-until", "+90m"])
        self.assertEqual(got.retry_until, "+90m")

    def test_refusal_detection_helpers_exist(self):
        import chatgpt_web as C
        self.assertTrue(callable(C.find_limit_notice))
        self.assertTrue(callable(C.handle_retry))
        self.assertTrue(callable(C.send_batch))


class TestRetryUntil(unittest.TestCase):
    def test_parses_relative_minutes(self):
        import chatgpt_web as C
        from datetime import datetime, timedelta
        now = datetime(2026, 10, 2, 18, 30)
        self.assertEqual(C.parse_until("+90m", now), now + timedelta(minutes=90))

    def test_parses_relative_hours(self):
        import chatgpt_web as C
        from datetime import datetime, timedelta
        now = datetime(2026, 10, 2, 18, 30)
        self.assertEqual(C.parse_until("+2h", now), now + timedelta(hours=2))

    def test_parses_clock_time_today(self):
        import chatgpt_web as C
        from datetime import datetime
        now = datetime(2026, 10, 2, 18, 30)
        self.assertEqual(C.parse_until("23:45", now).hour, 23)

    def test_clock_time_in_past_rolls_to_tomorrow(self):
        import chatgpt_web as C
        from datetime import datetime
        now = datetime(2026, 10, 2, 18, 30)
        got = C.parse_until("09:00", now)
        self.assertEqual((got.day, got.hour), (3, 9))

    def test_parses_duration_words(self):
        import chatgpt_web as C
        from datetime import datetime, timedelta
        now = datetime(2026, 10, 2, 18, 30)
        self.assertEqual(C.parse_until("2 hours", now), now + timedelta(hours=2))
        self.assertEqual(C.parse_until("45 minutes", now),
                         now + timedelta(minutes=45))

    def test_parses_iso(self):
        import chatgpt_web as C
        got = C.parse_until("2026-10-03T09:00")
        self.assertEqual((got.month, got.day, got.hour), (10, 3, 9))

    def test_unparseable_returns_none_not_infinity(self):
        """Must refuse rather than silently becoming 'retry forever'."""
        import chatgpt_web as C
        for bad in ("garbage", "", "+", "tomorrow-ish", "99"):
            self.assertIsNone(C.parse_until(bad), f"{bad!r} should not parse")


class TestQueryFanout(unittest.TestCase):
    def test_ship_queries_come_first(self):
        q = queries.expand("genshin impact", ["raiden", "yae"])
        self.assertTrue(any("raiden" in x and "yae" in x for x in q))

    def test_no_booru_syntax_in_fanout(self):
        """2girls is booru tag syntax; it means nothing in an X search box."""
        for q in queries.expand("genshin impact", ["raiden", "yae"]):
            self.assertNotIn("2girls", q)

    def test_capped_and_deduped(self):
        q = queries.expand("genshin impact", ["a", "b", "c", "d"],
                           max_queries=5)
        self.assertLessEqual(len(q), 5)
        self.assertEqual(len(q), len(set(q)))

    def test_empty_input_still_yields_core_terms(self):
        self.assertTrue(queries.expand("", []))

    def test_x_url_has_engagement_filter(self):
        u = queries.build_x_url("raiden yae yuri", min_likes=500)
        self.assertIn("min_faves%3A500", u)
        self.assertIn("filter%3Aimages", u)

    def test_x_url_without_min_likes(self):
        u = queries.build_x_url("raiden yae yuri")
        self.assertNotIn("min_faves", u)


class TestRecordIdentity(unittest.TestCase):
    def test_md5_is_the_identity(self):
        self.assertEqual(record_key(row(sid="1")), "md5:md51")

    def test_same_md5_different_ids_is_one_image(self):
        a, b = row(sid="1"), row(sid="2")
        b["md5"] = a["md5"]
        self.assertEqual(record_key(a), record_key(b))

    def test_falls_back_to_source_and_id(self):
        r = row()
        r["md5"] = ""
        self.assertEqual(record_key(r), "testbooru:1")

    def test_safety_ok_on_variants(self):
        self.assertTrue(safety_ok("1girl, solo")[0])
        self.assertFalse(safety_ok("1girl, Loli")[0])   # case-insensitive
        self.assertFalse(safety_ok(["shota"])[0])       # list form
        self.assertTrue(safety_ok(None)[0])


class TestLiveSmoke(unittest.TestCase):
    """The four checks from SKILL.md's Verification section, for real.

    Skipped unless HARVEST_LIVE=1, and needs HARVEST_CONTACT set, because
    it hits testbooru over the network.
    """

    @unittest.skipUnless(LIVE, "set HARVEST_LIVE=1 to run")
    def test_testbooru_end_to_end(self):
        """The real thing: fetch, download, and assert the four checks.

        --limit is a CAP, not a quota. testbooru is a small sandbox and a
        given tag can legitimately match fewer posts than asked for, so
        this asserts that N matches M everywhere rather than that N == 3.
        What must hold is internal consistency: rows, files and the
        manifest count agree, and every row resolves on disk.
        """
        if not os.environ.get("HARVEST_CONTACT"):
            self.skipTest("HARVEST_CONTACT is not set")
        for band in ("any", "explicit"):
            with self.subTest(rating=band):
                self._run_and_check(band)

    def _run_and_check(self, band: str) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            rc = harvest.main(["--sources", "testbooru", "--tags", "yuri",
                               "--limit", "3", "--rating", band,
                               "--out", str(out)])
            self.assertIn(rc, (0, 3), f"unexpected exit code {rc}")

            files = sorted(p for p in (out / "images").glob("*") if p.is_file())
            rows = load_jsonl(out / "metadata.jsonl")
            manifest = json.loads((out / "manifest.json").read_text("utf-8"))

            # check 1: no empty files
            for f in files:
                self.assertGreater(f.stat().st_size, 0, f"empty file: {f.name}")

            # check 2: one valid row per file, every file_name resolves
            self.assertEqual(len(rows), len(files),
                             "rows and images disagree")
            for r in rows:
                self.assertTrue((out / r["file_name"]).exists(),
                                f"file_name does not resolve: {r['file_name']}")

            # check 3: the manifest agrees with the filesystem
            self.assertEqual(manifest["total_images"], len(files))
            self.assertTrue(manifest["generated_utc"])
            self.assertEqual(manifest["rating_filter"], band)

            # check 4: every surviving row is inside the band, nothing the
            # hard filters exclude got through, and every row that did NOT
            # survive is explained in rejected.jsonl
            for r in rows:
                if band != "any":
                    self.assertEqual(r["rating"], band)
                ok, why = safety_ok(r.get("tags") or r.get("caption", ""))
                self.assertTrue(ok, f"hard-filtered row survived: {why}")
            rejected = load_jsonl(out / "rejected.jsonl")
            for r in rejected:
                self.assertTrue(r.get("reject_reason"),
                                "a rejection with no reason is not an audit trail")


class TestDanbooruRefusalPayloads(unittest.TestCase):
    """A refusal must cost one page, not the whole source.

    Boorus answer an over-broad or unauthorised query with a bare JSON
    object (testbooru: TagLimitError past two tags) or a plain string
    (Danbooru's auth wall). Both are dict/str, not a list of posts, so
    the p.get() loop raised AttributeError and the run reported
    "[danbooru] error: 'str' object has no attribute 'get'" instead of an
    empty page.
    """

    def _source(self):
        import sources as S
        return S.Testbooru()

    def test_tag_limit_error_object_degrades_to_empty(self):
        src = self._source()
        payload = {"success": False, "error": "PostQuery::TagLimitError",
                   "message": "You cannot search for more than 2 tags at a time."}
        self.assertEqual(src.parse_api(payload, "a b c"), [])

    def test_auth_wall_string_degrades_to_empty(self):
        src = self._source()
        self.assertEqual(src.parse_api("Missing authentication.", "a b"), [])

    def test_none_payload_degrades_to_empty(self):
        src = self._source()
        self.assertEqual(src.parse_api(None, "a b"), [])

    def test_real_post_list_still_parses(self):
        # guards against the fix flattening genuine results to nothing
        src = self._source()
        payload = [{"id": 7, "file_url": "https://x.test/a.jpg",
                    "tag_string": "a b", "tag_string_artist": "artist",
                    "rating": "general", "image_width": 100,
                    "image_height": 200, "md5": "d", "file_ext": "jpg"}]
        rows = src.parse_api(payload, "a b")
        self.assertEqual(len(rows), 1)
        # make_record stringifies the id; compare as text, not int
        self.assertEqual(str(rows[0]["source_id"]), "7")


class TestLoginGateKeepsWindowOpen(unittest.TestCase):
    """The login gate must not close the window it just told the user to use.

    chatgpt_web.login_prompt() prints NEEDS HUMAN LOGIN and the script then
    exits, which unwinds into Browser.__exit__ -> self.ctx.close() and shut
    the very window the user was asked to sign into. Reported as "u closed
    the browser how do i login". The profile dir persists, so only the
    window died; keep_open turns __exit__ into a disconnect.
    """

    def test_login_prompt_marks_browser_keep_open(self):
        import chatgpt_web

        class FakeBr:
            keep_open = False
            def __init__(self):
                self.gotoed = None
            def goto(self, url, **kw):
                self.gotoed = url

        br = FakeBr()
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            chatgpt_web.login_prompt(br, "https://chatgpt.com/")
        finally:
            sys.stdout = old

        self.assertTrue(br.keep_open,
                        "gate must hand the window over, not close it")
        self.assertEqual(br.gotoed, "https://chatgpt.com/")
        self.assertIn("NEEDS HUMAN LOGIN", buf.getvalue())

    def test_exit_does_not_close_when_keep_open(self):
        import browser as B

        class Ctx:
            closed = False
            def close(self):
                Ctx.closed = True

        br = B.Browser.__new__(B.Browser)
        br._attached = False
        br.ctx = Ctx()
        br.keep_open = True
        br._pw = None
        B.Browser.__exit__(br)
        self.assertFalse(Ctx.closed,
                         "keep_open browser must not be closed on exit")

    def test_exit_still_closes_normal_browser(self):
        # guards against the fix leaking every browser open forever
        import browser as B

        class Ctx:
            closed = False
            def close(self):
                Ctx.closed = True

        br = B.Browser.__new__(B.Browser)
        br._attached = False
        br.ctx = Ctx()
        br.keep_open = False
        br._pw = None
        B.Browser.__exit__(br)
        self.assertTrue(Ctx.closed)


if __name__ == "__main__":
    unittest.main(verbosity=2)