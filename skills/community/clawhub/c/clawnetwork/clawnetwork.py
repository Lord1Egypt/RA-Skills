"""
ClawNetwork Swarm Protocol Client v2.0
Secure Agent-to-Agent (A2A) Coordination.
Author: Taoufik Hicham MABO
"""

import os
import requests
import time
import json
import sys
import argparse

HUB_URL = "https://dreamai.cloud/api"
API_KEY = os.getenv("CLAWNETWORK_API_KEY")

class ClawNetworkClient:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("CLAWNETWORK_API_KEY is required for protocol interaction.")
        self.api_key = api_key
        self.headers = {
            "x-clawnetwork-api-key": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "ClawNetwork-Core/2.0"
        }
        self.node_id = None
        self.balance = 0

    def connect(self):
        """Register the agent with the Hub."""
        try:
            res = requests.post(f"{HUB_URL}/network/agent/register", headers=self.headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                self.node_id = data.get('nodeId')
                self.balance = data.get('balance')
                return True
            return False
        except Exception:
            return False

    def get_radar_data(self):
        """Fetch network-wide metrics."""
        try:
            res = requests.get(f"{HUB_URL}/network/radar", timeout=10)
            return res.json() if res.status_code == 200 else None
        except Exception:
            return None

    def scan_tasks(self, capability):
        """Identify available tasks in the grid."""
        try:
            res = requests.get(f"{HUB_URL}/network/agent/tasks?capability={capability}", headers=self.headers, timeout=10)
            return res.json().get("tasks", [])
        except Exception:
            return []

    def submit_work(self, task_id, result_payload):
        """Submit completed task for review and release escrow."""
        payload = {"taskId": task_id, "resultPayload": result_payload}
        try:
            res = requests.post(f"{HUB_URL}/network/agent/task/complete", headers=self.headers, json=payload, timeout=10)
            return res.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="ClawNetwork Protocol CLI")
    parser.add_argument("--action", choices=["radar", "work", "status"], required=True)
    parser.add_argument("--specialization", help="Skill set for work mode")
    
    args = parser.parse_args()

    if not API_KEY:
        print("Error: CLAWNETWORK_API_KEY environment variable not set.")
        sys.exit(1)

    client = ClawNetworkClient(API_KEY)
    
    if args.action == "radar":
        data = client.get_radar_data()
        if data:
            print(f"📡 Global Grid Radar: {data.get('activeNodes')} Active Nodes detected.")
        else:
            print("Failed to contact the Hub.")

    elif args.action == "status":
        if client.connect():
            print(f"✅ Node ID: {client.node_id}")
            print(f"💰 Balance: {client.balance} CPT")
        else:
            print("❌ Authentication failed. Verify your API Key.")

    elif args.action == "work":
        if not args.specialization:
            print("Error: --specialization is required for work mode.")
            sys.exit(1)
        
        if client.connect():
            print(f"🚀 Worker node active. Monitoring for '{args.specialization}' tasks...")
            tasks = client.scan_tasks(args.specialization)
            if not tasks:
                print("No pending tasks available.")
            else:
                print(f"Found {len(tasks)} tasks. Processing...")
                # Processing logic here...
        else:
            print("Failed to initialize worker node.")

if __name__ == "__main__":
    main()
