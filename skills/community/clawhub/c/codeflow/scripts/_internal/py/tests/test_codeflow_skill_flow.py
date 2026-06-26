import os
import sys
import unittest


SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, SCRIPT_DIR)

import codeflow_skill_flow


class CodeflowSkillFlowTests(unittest.TestCase):
    def test_parse_control_request(self):
        self.assertEqual(
            codeflow_skill_flow.parse_control_request("/codeflow"),
            {"action": "activate", "message_id": ""},
        )
        self.assertEqual(
            codeflow_skill_flow.parse_control_request("/codeflow on"),
            {"action": "activate", "message_id": ""},
        )
        self.assertEqual(
            codeflow_skill_flow.parse_control_request("/codeflow status"),
            {"action": "status", "message_id": ""},
        )
        self.assertEqual(
            codeflow_skill_flow.parse_control_request("/codeflow off"),
            {"action": "deactivate", "message_id": ""},
        )
        self.assertEqual(
            codeflow_skill_flow.parse_control_request("callback_data: cfe:install"),
            {"action": "install", "message_id": ""},
        )
        self.assertEqual(
            codeflow_skill_flow.parse_control_request("callback_data: cfe:install:12345"),
            {"action": "install", "message_id": "12345"},
        )
        self.assertEqual(
            codeflow_skill_flow.parse_control_request("/other"),
            {"action": "unsupported", "message_id": ""},
        )

    def test_infer_message_route_for_telegram(self):
        direct = codeflow_skill_flow.infer_message_route("agent:main:telegram:direct:123")
        self.assertEqual(direct, {"channel": "telegram", "target": "123"})

        topic = codeflow_skill_flow.infer_message_route("agent:main:telegram:group:-1001:topic:55")
        self.assertEqual(
            topic,
            {"channel": "telegram", "target": "-1001", "threadId": "55"},
        )

        self.assertIsNone(codeflow_skill_flow.infer_message_route("agent:main:discord:thread:abc"))

    def test_build_control_reply_keeps_buttons_when_supported(self):
        status = {
            "guard": {"active": True, "bindingKey": "telegram:-1001:55"},
            "recommendation": {
                "action": "install",
                "message": "Soft mode is active.",
                "buttons": [[{"text": "Install Enforcer", "callback_data": "cfe:install"}]],
            },
            "installCommand": "bash /tmp/codeflow enforcer install --restart",
        }

        reply = codeflow_skill_flow.build_control_reply("activate", status, buttons_supported=True)

        self.assertEqual(reply["buttons"], [[{"text": "Install Enforcer", "callback_data": "cfe:install"}]])
        self.assertIn("Codeflow guard activated", reply["message"])
        self.assertIn("Binding: telegram:-1001:55", reply["message"])
        self.assertNotIn("Install: bash /tmp/codeflow", reply["message"])

    def test_attach_install_message_id_rewrites_install_callback(self):
        buttons = [[{"text": "Install Enforcer", "callback_data": "cfe:install"}]]
        out = codeflow_skill_flow.attach_install_message_id(buttons, "6789")
        self.assertEqual(out, [[{"text": "Install Enforcer", "callback_data": "cfe:install:6789"}]])

    def test_build_control_reply_falls_back_to_install_command_without_buttons(self):
        status = {
            "guard": {"active": False, "state": "unbound"},
            "recommendation": {
                "action": "install",
                "message": "Soft mode is active.",
                "buttons": [[{"text": "Install Enforcer", "callback_data": "cfe:install"}]],
            },
            "installCommand": "bash /tmp/codeflow enforcer install --restart",
        }

        reply = codeflow_skill_flow.build_control_reply("status", status, buttons_supported=False)

        self.assertEqual(reply["buttons"], [])
        self.assertIn("Codeflow guard is not active", reply["message"])
        self.assertIn("Install: bash /tmp/codeflow enforcer install --restart", reply["message"])

    def test_build_control_reply_reports_restart_pending_enforcer(self):
        status = {
            "guard": {"active": False, "state": "inactive"},
            "plugin": {"state": "restart-pending", "status": "installed"},
            "recommendation": {
                "action": "restart",
                "message": "Soft mode is active.",
                "buttons": [],
            },
            "restartCommand": "openclaw gateway restart",
        }

        reply = codeflow_skill_flow.build_control_reply("status", status, buttons_supported=False)

        self.assertIn("Codeflow guard is configured but inactive", reply["message"])
        self.assertIn("Enforcer: installed, but restart is still pending.", reply["message"])
        self.assertIn("Restart: openclaw gateway restart", reply["message"])

    def test_build_control_reply_for_install_uses_refreshed_status(self):
        status = {
            "guard": {"active": False, "state": "unbound"},
            "plugin": {"state": "loaded", "status": "loaded"},
            "recommendation": {
                "action": "none",
                "message": "Hard blocking is now available.",
                "buttons": [],
            },
        }

        reply = codeflow_skill_flow.build_control_reply("install", status, buttons_supported=True)

        self.assertIn("Codeflow enforcer installed and loaded", reply["message"])
        self.assertIn("Hard blocking is now available.", reply["message"])
        self.assertNotIn("Installing the bundled Codeflow enforcer", reply["message"])


if __name__ == "__main__":
    unittest.main()
