import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from urllib import error


MODULE_PATH = Path(__file__).resolve().parents[1] / "worker_server.py"
SPEC = importlib.util.spec_from_file_location("worker_server_module", MODULE_PATH)
worker_server = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(worker_server)


class WorkerServerTests(unittest.TestCase):
    def test_memory_command_supports_python_script_and_binary(self):
        py_cmd = worker_server._memory_command("/tmp/cli.py", "query", "hello")
        self.assertEqual(py_cmd[1:], ["/tmp/cli.py", "query", "hello"])

        bin_cmd = worker_server._memory_command("/usr/local/bin/memory-cli", "query", "hello")
        self.assertEqual(bin_cmd, ["/usr/local/bin/memory-cli", "query", "hello"])

    def test_build_prompt_uses_task_title_argument(self):
        server = worker_server.WorkerServer.__new__(worker_server.WorkerServer)
        server.worker_id = "xiaolong"
        server.worker_name = "小龙"
        server.worker_role = "research"
        prompt = server._build_prompt("research", "竞品分析", "分析 A 和 B", [])
        self.assertIn("任务标题：竞品分析", prompt)
        self.assertIn("任务描述：分析 A 和 B", prompt)

    def test_parse_openclaw_result_accepts_log_prefixed_json(self):
        server = worker_server.WorkerServer.__new__(worker_server.WorkerServer)
        raw = '[info] running\n{"result":{"payloads":[{"text":"done"}]}}'
        self.assertEqual(server._parse_openclaw_result(raw), "done")

    def test_run_openclaw_uses_worker_id_not_display_name(self):
        server = worker_server.WorkerServer.__new__(worker_server.WorkerServer)
        server.worker_id = "xiaolong"
        server.worker_name = "小龙"
        server.workspace_dir = "/tmp"

        completed = mock.Mock(returncode=0, stdout='{"result":{"payloads":[{"text":"ok"}]}}', stderr="")
        with mock.patch.object(worker_server.subprocess, "run", return_value=completed) as run_mock:
            result = server._run_openclaw("hello")

        self.assertEqual(result, "ok")
        args = run_mock.call_args.args[0]
        self.assertEqual(args[:4], ["openclaw", "agent", "--agent", "xiaolong"])

    def test_build_cli_command_supports_arg_profile(self):
        server = worker_server.WorkerServer.__new__(worker_server.WorkerServer)
        server.cli_cmd = ""
        server.cli_args = "--model sonnet"
        with mock.patch.object(worker_server, "get_cli_profile", return_value={
            "display_name": "Aider",
            "executables": ("aider",),
            "base_args": (),
            "prompt_mode": "arg",
            "prompt_flag": "--message",
            "timeout": 600,
        }):
            with mock.patch.object(worker_server, "shutil") as shutil_mock:
                shutil_mock.which.return_value = "/usr/local/bin/aider"
                cmd = worker_server.WorkerServer._build_cli_command(
                    server,
                    worker_server.get_cli_profile("aider"),
                    "fix bug",
                )
        self.assertEqual(cmd[:3], ["/usr/local/bin/aider", "--model", "sonnet"])
        self.assertEqual(cmd[-2:], ["--message", "fix bug"])

    def test_build_cli_command_uses_codex_exec_defaults(self):
        server = worker_server.WorkerServer.__new__(worker_server.WorkerServer)
        server.cli_cmd = ""
        server.cli_args = "--model gpt-5.4"

        with mock.patch.object(worker_server, "shutil") as shutil_mock:
            shutil_mock.which.return_value = "/usr/local/bin/codex"
            cmd = worker_server.WorkerServer._build_cli_command(
                server,
                worker_server.get_cli_profile("codex"),
                "hello cli",
            )

        self.assertEqual(
            cmd,
            [
                "/usr/local/bin/codex",
                "exec",
                "--skip-git-repo-check",
                "--model",
                "gpt-5.4",
            ],
        )

    def test_run_cli_uses_stdin_profile(self):
        server = worker_server.WorkerServer.__new__(worker_server.WorkerServer)
        server.cli_profile = "codex"
        server.cli_cmd = ""
        server.cli_args = ""
        server.cli_timeout = 123
        server.workspace_dir = "/tmp"

        completed = mock.Mock(returncode=0, stdout="cli ok", stderr="")
        with mock.patch.object(worker_server, "shutil") as shutil_mock:
            shutil_mock.which.return_value = "/usr/local/bin/codex"
            with mock.patch.object(worker_server.subprocess, "run", return_value=completed) as run_mock:
                result = worker_server.WorkerServer._run_cli(server, "hello cli")

        self.assertEqual(result, "cli ok")
        self.assertEqual(
            run_mock.call_args.args[0],
            ["/usr/local/bin/codex", "exec", "--skip-git-repo-check"],
        )
        self.assertEqual(run_mock.call_args.kwargs["input"], "hello cli")

    def test_build_deerflow_prompt_includes_shared_memory(self):
        server = worker_server.WorkerServer.__new__(worker_server.WorkerServer)
        server.worker_id = "xiaod2"
        server.worker_name = "小D2"
        server.worker_role = "complex"
        prompt = server._build_deerflow_prompt(
            "大任务拆解",
            "请给出方案和风险",
            [
                {
                    "title": "派单规则",
                    "worker": "manager",
                    "room": "office",
                    "summary_text": "复杂任务优先交给 DeerFlow 团队",
                }
            ],
        )
        self.assertIn("小D2", prompt)
        self.assertIn("复杂任务优先交给 DeerFlow 团队", prompt)
        self.assertIn("deerflow_team", prompt)

    def test_run_deerflow_uses_embedded_runtime_runner(self):
        server = worker_server.WorkerServer.__new__(worker_server.WorkerServer)
        server.worker_id = "xiaod2"
        server.worker_name = "小D2"
        server.worker_role = "complex"
        server.workspace_dir = "/tmp"
        server.deerflow_runtime_python = __file__
        server.deerflow_config = __file__
        server.deerflow_home = tempfile.gettempdir()
        server.deerflow_agent_name = "xiaod2"
        server.deerflow_model = "gpt-5.4"
        server.deerflow_reasoning_effort = "medium"
        server.deerflow_recursion_limit = 48
        server.deerflow_timeout = 300

        completed = mock.Mock(
            returncode=0,
            stdout=json.dumps(
                {
                    "team_summary": "团队已处理",
                    "current_scope": ["拆分任务"],
                    "next_step_suggestions": ["继续推进"],
                    "handoff_note": "已回传",
                    "delegation_trace": ["subagent started: audit"],
                },
                ensure_ascii=False,
            ),
            stderr="",
        )
        with mock.patch.object(worker_server.subprocess, "run", return_value=completed) as run_mock:
            result = server._run_deerflow("大任务", "请拆解", [])

        self.assertIn("团队已处理", result)
        self.assertIn("subagent started: audit", result)
        cmd = run_mock.call_args.args[0]
        self.assertEqual(Path(cmd[1]), worker_server.DEERFLOW_RUNTIME_RUNNER)
        self.assertIn("--config", cmd)

    def test_build_external_description_includes_shared_memory(self):
        server = worker_server.WorkerServer.__new__(worker_server.WorkerServer)
        server.worker_name = "外挂小龙"
        description = server._build_external_description(
            "同步办公室状态",
            "看看最近任务",
            [
                {
                    "title": "办公室规则",
                    "worker": "manager",
                    "room": "office",
                    "summary_text": "优先参考共享记忆，不改上游员工设定",
                }
            ],
        )
        self.assertIn("外挂小龙", description)
        self.assertIn("同步办公室状态", description)
        self.assertIn("优先参考共享记忆", description)

    def test_run_external_submits_and_polls_upstream_worker(self):
        server = worker_server.WorkerServer.__new__(worker_server.WorkerServer)
        server.worker_name = "外挂小龙"
        server.external_upstream_url = "http://127.0.0.1:18750"
        server.external_timeout = 20
        server.external_poll_interval = 0

        with mock.patch.object(
            worker_server.WorkerServer,
            "_external_request",
            side_effect=[
                (202, {"task_id": "up-1", "status": "pending"}),
                (
                    200,
                    {
                        "task_id": "up-1",
                        "status": "done",
                        "result": {"content": "上游完成", "format": "markdown"},
                    },
                ),
            ],
        ) as request_mock:
            result = server._run_external(
                "接入测试",
                "请返回当前状态",
                [{"summary_text": "共享记忆：最近有新任务"}],
            )

        self.assertEqual(result, "上游完成")
        first_call = request_mock.call_args_list[0]
        self.assertEqual(first_call.args[:2], ("POST", "/tasks"))
        forwarded_description = first_call.args[2]["description"]
        self.assertIn("共享记忆：最近有新任务", forwarded_description)

    def test_run_external_handles_upstream_http_error(self):
        server = worker_server.WorkerServer.__new__(worker_server.WorkerServer)
        server.worker_name = "外挂小龙"
        server.external_upstream_url = "http://127.0.0.1:18750"
        server.external_timeout = 20
        server.external_poll_interval = 0

        with mock.patch.object(
            worker_server.WorkerServer,
            "_external_request",
            side_effect=error.HTTPError(
                url="http://127.0.0.1:18750/tasks",
                code=500,
                msg="boom",
                hdrs=None,
                fp=None,
            ),
        ):
            result = server._run_external("接入测试", "请返回当前状态", [])

        self.assertIn("HTTP 500", result)


if __name__ == "__main__":
    unittest.main()
