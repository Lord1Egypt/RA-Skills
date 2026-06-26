#!/usr/bin/env python3
"""
Contact Department Members

Search for a department by name and list all members.
Usage: python contact_dept_members.py --keyword "Engineering"
"""

import argparse
import subprocess
import json
import sys


def run_dws(args):
    """Run dws command and return JSON output."""
    cmd = ["dws"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def search_department(keyword):
    """Search for department by keyword."""
    result = run_dws(["contact", "dept", "search", "--keyword", keyword])
    if not result:
        return []
    return result.get("result", [])


def get_department_members(dept_id):
    """Get all members of a department."""
    result = run_dws(["contact", "dept", "members", "--dept-id", dept_id])
    if not result:
        return []
    return result.get("result", [])


def main():
    parser = argparse.ArgumentParser(description="Search department and list members")
    parser.add_argument("--keyword", required=True, help="Department name keyword")
    parser.add_argument("--format", choices=["table", "json", "csv"], default="table")
    
    args = parser.parse_args()
    
    # Search for department
    print(f"Searching for department: {args.keyword}")
    depts = search_department(args.keyword)
    
    if not depts:
        print("No departments found")
        sys.exit(0)
    
    print(f"Found {len(depts)} department(s):")
    for dept in depts:
        print(f"  - {dept.get('deptName', 'Unknown')} (ID: {dept.get('deptId', 'N/A')})")
    
    # Get members for first result
    dept = depts[0]
    dept_id = dept.get("deptId")
    dept_name = dept.get("deptName", "Unknown")
    
    print(f"\nGetting members of '{dept_name}'...")
    members = get_department_members(dept_id)
    
    if not members:
        print("No members found")
        sys.exit(0)
    
    print(f"\nFound {len(members)} member(s):\n")
    
    if args.format == "json":
        print(json.dumps(members, indent=2, ensure_ascii=False))
    elif args.format == "csv":
        print("name,userId,mobile")
        for member in members:
            name = member.get("name", member.get("orgUserName", ""))
            user_id = member.get("userId", "")
            mobile = member.get("mobile", "")
            print(f"{name},{user_id},{mobile}")
    else:  # table
        # Calculate column widths
        names = [m.get("name", m.get("orgUserName", "")) for m in members]
        ids = [m.get("userId", "") for m in members]
        
        name_width = max(len("Name"), max(len(n) for n in names) if names else 0)
        id_width = max(len("User ID"), max(len(i) for i in ids) if ids else 0)
        
        print(f"{'Name':<{name_width}} | {'User ID':<{id_width}} | Mobile")
        print("-" * (name_width + id_width + 15))
        
        for member in members:
            name = member.get("name", member.get("orgUserName", ""))
            user_id = member.get("userId", "")
            mobile = member.get("mobile", "")
            print(f"{name:<{name_width}} | {user_id:<{id_width}} | {mobile or 'N/A'}")
    
    print(f"\nTotal: {len(members)} members")


if __name__ == "__main__":
    main()
