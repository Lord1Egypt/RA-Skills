#!/usr/bin/env python3
"""
Pipeline Monitor | 流水线监控工具
"""

import argparse
import requests
import json
from datetime import datetime


def monitor_github_actions(repo, token=None):
    """监控GitHub Actions流水线"""
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    if token:
        headers["Authorization"] = f"token {token}"
    
    url = f"https://api.github.com/repos/{repo}/actions/runs"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 GitHub Actions Status for {repo}")
            print("=" * 50)
            for run in data.get("workflow_runs", [])[:5]:
                status_icon = "✅" if run["conclusion"] == "success" else "❌" if run["conclusion"] == "failure" else "🔄"
                print(f"{status_icon} {run['name']}: {run['conclusion'] or run['status']}")
                print(f"   Branch: {run['head_branch']} | Time: {run['created_at']}")
        else:
            print(f"❌ Failed to fetch: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")


def monitor_gitlab_ci(project_id, token=None, gitlab_url="https://gitlab.com"):
    """监控GitLab CI流水线"""
    headers = {}
    if token:
        headers["PRIVATE-TOKEN"] = token
    
    url = f"{gitlab_url}/api/v4/projects/{project_id}/pipelines"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            pipelines = response.json()
            print(f"\n📊 GitLab CI Status for project {project_id}")
            print("=" * 50)
            for pipeline in pipelines[:5]:
                status_icon = "✅" if pipeline["status"] == "success" else "❌" if pipeline["status"] == "failed" else "🔄"
                print(f"{status_icon} Pipeline #{pipeline['id']}: {pipeline['status']}")
                print(f"   Ref: {pipeline['ref']} | Created: {pipeline['created_at']}")
        else:
            print(f"❌ Failed to fetch: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Pipeline Monitor")
    parser.add_argument("--platform", required=True, choices=["github", "gitlab"], help="CI platform")
    parser.add_argument("--repo", help="Repository (owner/repo for GitHub)")
    parser.add_argument("--project-id", help="Project ID (for GitLab)")
    parser.add_argument("--token", help="API token")
    parser.add_argument("--gitlab-url", default="https://gitlab.com", help="GitLab URL")
    args = parser.parse_args()
    
    if args.platform == "github" and args.repo:
        monitor_github_actions(args.repo, args.token)
    elif args.platform == "gitlab" and args.project_id:
        monitor_gitlab_ci(args.project_id, args.token, args.gitlab_url)
    else:
        print("❌ Missing required arguments. Use --help for usage.")


if __name__ == "__main__":
    main()
