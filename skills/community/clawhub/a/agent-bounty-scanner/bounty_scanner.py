"""
Professional Bounty Scanner for Autonomous Agents
Version: 1.0.1
Description: Efficiently discovers, filters, and scores bounties from agentic marketplaces.
Uses standardized ACP interaction patterns.
"""

import json
import subprocess
import os
import sys
from datetime import datetime

class BountyScanner:
    def __init__(self, acp_command="acp"):
        """
        Initialize the scanner.
        :param acp_command: The command to invoke the ACP CLI (default: 'acp').
                            Users should ensure 'acp' is in their PATH or configured via metadata.
        """
        self.acp_command = acp_command

    def fetch_bounties(self, query="coding"):
        """Fetches active bounties using safe subprocess execution."""
        try:
            # Security: Use a list for arguments to avoid shell injection
            # We assume 'acp' is a globally available binary or alias provided by the environment
            cmd = [self.acp_command, "browse", query, "--json"]
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True,
                check=False # We handle errors manually
            )
            
            if result.returncode != 0:
                return {"status": "error", "message": result.stderr or "Unknown ACP error"}
            
            data = json.loads(result.stdout)
            return {"status": "success", "data": data}
        except FileNotFoundError:
            return {
                "status": "error", 
                "message": f"Command '{self.acp_command}' not found. Please install the 'virtuals-protocol-acp' skill."
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def score_task(self, task, capabilities):
        """Scores a task based on budget, SLA, and capability alignment (0-100)."""
        score = 0
        
        # 1. Budget Weight (40%)
        price = task.get('price', 0)
        if price >= 50: score += 40
        elif price >= 10: score += 30
        elif price >= 1: score += 15
        else: score += 5

        # 2. SLA/Urgency Weight (20%)
        sla = task.get('slaMinutes', 60)
        if sla <= 15: score += 20
        elif sla <= 60: score += 10
        else: score += 5

        # 3. Capability Alignment (40%)
        description = task.get('description', '').lower()
        match_count = 0
        if capabilities:
            for cap in capabilities:
                if cap.lower() in description:
                    match_count += 1
            alignment_score = (match_count / len(capabilities)) * 40
            score += alignment_score

        return round(min(score, 100), 2)

    def scan_and_rank(self, query="security", capabilities=None):
        """Main workflow: fetch, score, and rank opportunities."""
        if capabilities is None:
            capabilities = ["audit", "code", "verify"]
            
        fetch_result = self.fetch_bounties(query)
        
        if fetch_result['status'] == "error":
            return fetch_result

        agents = fetch_result.get('data', [])
        opportunities = []

        for agent in agents:
            for job in agent.get('jobs', []):
                score = self.score_task(job, capabilities)
                opportunities.append({
                    "agent_name": agent.get('name'),
                    "job_name": job.get('name'),
                    "price": job.get('price'),
                    "score": score,
                    "description": job.get('description'),
                    "requirements": job.get('requirement')
                })

        ranked = sorted(opportunities, key=lambda x: x['score'], reverse=True)
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "count": len(ranked),
            "top_picks": ranked[:5]
        }

if __name__ == "__main__":
    scanner = BountyScanner()
    # Basic CLI check
    test_query = sys.argv[1] if len(sys.argv) > 1 else "security"
    results = scanner.scan_and_rank(test_query)
    print(json.dumps(results, indent=2))
