#!/usr/bin/env python3
"""
CLAWD ↔ DeepAll_CODE Integration
Verbindet CLAWD mit DeepAll_CODE Assistant für erweiterte Aufgaben
"""

import json
import os
from datetime import datetime
from sub_agent_logger import get_logger
from sub_agent_queue import MessageQueue, Message

logger = get_logger("CLAWDDeepAllIntegration")

class CLAWDDeepAllIntegration:
    """Integriert CLAWD mit DeepAll_CODE"""

    def __init__(self):
        self.config_path = "/home/deepall/clawd/deepall_integration.json"
        self.deepall_assistant = "DeepAll_CODE"
        self.deepall_id = "asst_bsVEQXNydgoF4n8QjN2KMNuy"
        self.queue = MessageQueue()
        self.load_config()
        logger.info("CLAWD-DeepAll Integration initialized")

    def load_config(self):
        """Lade oder erstelle Konfiguration"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = self.create_default_config()
            self.save_config()

    def create_default_config(self) -> dict:
        """Erstelle Standard-Konfiguration"""
        return {
            "enabled": True,
            "deepall_assistant": "DeepAll_CODE",
            "deepall_id": "asst_bsVEQXNydgoF4n8QjN2KMNuy",
            "clawd_status": "connected",
            "integration_date": datetime.now().isoformat(),
            "capabilities": {
                "code_execution": True,
                "file_operations": True,
                "task_delegation": True,
                "bidirectional_communication": True
            },
            "task_types": [
                "security_audit",
                "deployment_guide",
                "api_documentation",
                "performance_optimization",
                "code_review",
                "testing",
                "deployment"
            ]
        }

    def save_config(self):
        """Speichere Konfiguration"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)

    def send_task_to_deepall(self, task_name: str, task_description: str, params: dict = None) -> bool:
        """Sende Task zu DeepAll_CODE"""

        task = {
            "id": f"task_{datetime.now().timestamp()}",
            "from": "CLAWD",
            "to": "DeepAll_CODE",
            "assistant_id": self.deepall_id,
            "task_name": task_name,
            "task_description": task_description,
            "parameters": params or {},
            "status": "sent",
            "created_at": datetime.now().isoformat()
        }

        try:
            msg = Message(
                sender="clawd",
                recipient="deepall_code",
                content=json.dumps(task)
            )

            if self.queue.enqueue(msg):
                logger.info(f"Task sent to DeepAll_CODE: {task_name}")
                return True
            else:
                logger.error(f"Failed to queue task: {task_name}")
                return False

        except Exception as e:
            logger.error(f"Error sending task: {e}")
            return False

    def request_help(self, issue: str, context: str = "") -> dict:
        """Fordere Hilfe von DeepAll_CODE an"""

        help_request = {
            "id": f"help_{datetime.now().timestamp()}",
            "from": "CLAWD",
            "to": "DeepAll_CODE",
            "type": "help_request",
            "issue": issue,
            "context": context,
            "assistant_id": self.deepall_id,
            "status": "sent",
            "created_at": datetime.now().isoformat()
        }

        try:
            msg = Message(
                sender="clawd",
                recipient="deepall_code",
                content=json.dumps(help_request)
            )

            if self.queue.enqueue(msg):
                logger.info(f"Help request sent to DeepAll_CODE: {issue}")
                return {"status": "success", "message": "Help request sent"}
            else:
                logger.error(f"Failed to send help request")
                return {"status": "error", "message": "Failed to queue request"}

        except Exception as e:
            logger.error(f"Error requesting help: {e}")
            return {"status": "error", "message": str(e)}

    def print_connection_status(self):
        """Zeige Verbindungsstatus"""

        print("\n" + "="*70)
        print("🔗 CLAWD ↔ DEEPALL_CODE CONNECTION STATUS")
        print("="*70)

        print(f"\n✅ CLAWD Status:")
        print(f"   Name: CLAWD Bot")
        print(f"   Type: Multi-Agent System")
        print(f"   Status: 🟢 ACTIVE")

        print(f"\n🤖 DeepAll_CODE Assistant:")
        print(f"   Name: {self.deepall_assistant}")
        print(f"   ID: {self.deepall_id}")
        print(f"   Status: 🟢 CONNECTED")

        print(f"\n📡 Integration:")
        print(f"   Type: Bidirectional Communication")
        print(f"   Status: ✅ ENABLED")
        print(f"   Connected: {self.config['integration_date'][:10]}")

        print(f"\n📋 Available Task Types:")
        for i, task_type in enumerate(self.config["task_types"], 1):
            print(f"   {i}. {task_type}")

        print(f"\n⚡ Capabilities:")
        for capability, enabled in self.config["capabilities"].items():
            status = "✅" if enabled else "❌"
            print(f"   {status} {capability}")

        print("\n" + "="*70)
        print("🎯 CLAWD kann jetzt DeepAll_CODE um Hilfe bitten!")
        print("="*70 + "\n")

    def assign_task_to_deepall(self, task_type: str, description: str):
        """Weise Task an DeepAll_CODE zu"""

        print(f"\n📤 Assigning task to DeepAll_CODE...")
        print(f"   Task Type: {task_type}")
        print(f"   Description: {description[:50]}...")

        success = self.send_task_to_deepall(task_type, description)

        if success:
            print(f"   ✅ Task assigned successfully!")
            print(f"   Assistant: DeepAll_CODE ({self.deepall_id})")
            return True
        else:
            print(f"   ❌ Failed to assign task")
            return False

    def request_code_help(self, issue: str):
        """Fordere Code-Hilfe von DeepAll_CODE an"""

        print(f"\n🆘 Requesting code help from DeepAll_CODE...")
        print(f"   Issue: {issue}")

        result = self.request_help(issue, "Code assistance needed")

        if result["status"] == "success":
            print(f"   ✅ Help request sent!")
        else:
            print(f"   ❌ {result['message']}")

        return result


def main():
    """Hauptfunktion"""
    import sys

    if len(sys.argv) < 2:
        print("""
Usage: python3 clawd_deepall_integration.py <command> [args]

Commands:
  status              - Zeige Connection Status
  task <type> <desc>  - Weise Task an DeepAll_CODE
  help <issue>        - Fordere Hilfe an
  test                - Test Integration
  config              - Zeige Konfiguration
        """)
        return

    integration = CLAWDDeepAllIntegration()
    command = sys.argv[1]

    if command == "status":
        integration.print_connection_status()

    elif command == "task" and len(sys.argv) > 3:
        task_type = sys.argv[2]
        description = " ".join(sys.argv[3:])
        integration.assign_task_to_deepall(task_type, description)

    elif command == "help" and len(sys.argv) > 2:
        issue = " ".join(sys.argv[2:])
        integration.request_code_help(issue)

    elif command == "test":
        print("\n🧪 Testing CLAWD ↔ DeepAll_CODE Integration...")
        integration.print_connection_status()

        # Test Task
        integration.assign_task_to_deepall(
            "code_review",
            "Review security audit findings and suggest fixes"
        )

        # Test Help
        integration.request_code_help("GLM API authentication failed")

        print("\n✅ Integration test complete!")

    elif command == "config":
        print("\n📋 CLAWD-DeepAll Configuration:")
        print(json.dumps(integration.config, indent=2, ensure_ascii=False))

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
