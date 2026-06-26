#!/usr/bin/env python3
"""
OpenClaw Skill Wrapper for Canvas LMS Student
This wrapper provides a unified interface for OpenClaw to call Python scripts.
"""

import json
import subprocess
import sys
from pathlib import Path

# Tool mapping
TOOLS = {
    "list_courses": {
        "script": "scripts/list_courses.py",
        "args_builder": lambda p: build_list_courses_args(p)
    },
    "resolve_course": {
        "script": "scripts/list_courses.py",
        "args_builder": lambda p: ["--resolve", p.get("name", ""), "--json"]
    },
    "get_assignments": {
        "script": "scripts/get_assignments.py",
        "args_builder": lambda p: build_get_assignments_args(p)
    },
    "get_assignment_detail": {
        "script": "scripts/get_assignment_detail.py",
        "args_builder": lambda p: ["--course", str(p.get("course", "")), 
                                   "--assignment", str(p.get("assignment", "")), "--json"]
    },
    "search_canvas": {
        "script": "scripts/search_canvas.py",
        "args_builder": lambda p: build_search_args(p)
    },
    "download_files": {
        "script": "scripts/download_files.py",
        "args_builder": lambda p: build_download_args(p)
    },
    "export_calendar": {
        "script": "scripts/export_calendar.py",
        "args_builder": lambda p: build_export_args(p)
    }
}


def build_list_courses_args(params):
    args = ["--json"]
    if params.get("active_only"):
        args.append("--active-only")
    if params.get("with_grades"):
        args.append("--with-grades")
    return args


def build_get_assignments_args(params):
    args = ["--json"]
    
    course = params.get("course", "")
    # Check if course is numeric ID or name
    try:
        int(course)
        args.extend(["--course", course])
    except ValueError:
        # It's a name, use resolve
        args.extend(["--course", course, "--resolve-name"])
    
    if params.get("upcoming"):
        args.append("--upcoming")
    if params.get("overdue"):
        args.append("--overdue")
    if params.get("unsubmitted"):
        args.append("--unsubmitted")
    
    return args


def build_search_args(params):
    args = ["--query", params.get("query", ""), "--json"]
    
    if params.get("type") and params["type"] != "all":
        args.extend(["--type", params["type"]])
    
    if params.get("course"):
        args.extend(["--course", str(params["course"])])
    
    return args


def build_download_args(params):
    args = ["--course", str(params.get("course", ""))]
    
    if params.get("output"):
        args.extend(["--output", params["output"]])
    if params.get("type"):
        args.extend(["--type", params["type"]])
    if params.get("folder"):
        args.extend(["--folder", params["folder"]])
    
    return args


def build_export_args(params):
    args = ["--courses", params.get("courses", "")]
    
    if params.get("output"):
        args.extend(["--output", params["output"]])
    if params.get("unsubmitted_only"):
        args.append("--unsubmitted-only")
    
    return args


def build_success_result(tool_name: str, parameters: dict, stdout: str, stderr: str, parsed_output=None) -> dict:
    """Build a consistent JSON result for wrapper callers."""
    result = {
        "ok": True,
        "tool": tool_name,
    }

    if parsed_output is not None:
        result["result"] = parsed_output
    elif stdout.strip():
        result["stdout"] = stdout.strip()

    if stderr.strip():
        result["stderr"] = stderr.strip()

    if tool_name == "download_files":
        result["output_dir"] = parameters.get("output", "./course-materials")
    elif tool_name == "export_calendar":
        result["output_file"] = parameters.get("output", "canvas-deadlines.ics")

    return result


def run_tool(tool_name: str, parameters: dict) -> dict:
    """Run a tool with given parameters."""
    if tool_name not in TOOLS:
        return {
            "ok": False,
            "error": f"Unknown tool: {tool_name}",
            "available_tools": list(TOOLS.keys())
        }
    
    tool = TOOLS[tool_name]
    script_dir = Path(__file__).parent
    script_path = script_dir / tool["script"]
    
    if not script_path.exists():
        return {
            "ok": False,
            "error": f"Script not found: {tool['script']}"
        }
    
    # Build command
    args = tool["args_builder"](parameters)
    cmd = ["python3", str(script_path)] + args
    
    try:
        # Run script
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            return {
                "ok": False,
                "error": "Tool execution failed",
                "tool": tool_name,
                "command": cmd,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        
        # Try to parse as JSON
        try:
            parsed = json.loads(result.stdout)
            return build_success_result(tool_name, parameters, result.stdout, result.stderr, parsed)
        except json.JSONDecodeError:
            return build_success_result(tool_name, parameters, result.stdout, result.stderr)
    
    except subprocess.TimeoutExpired:
        return {"ok": False, "tool": tool_name, "error": "Tool execution timed out"}
    except Exception as e:
        return {"ok": False, "tool": tool_name, "error": f"Failed to run tool: {str(e)}"}


def main():
    """Main entry point for wrapper."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "No tool specified",
            "usage": "wrapper.py <tool_name> [parameters_json]",
            "available_tools": list(TOOLS.keys())
        }))
        sys.exit(1)
    
    tool_name = sys.argv[1]
    
    # Parse parameters
    if len(sys.argv) >= 3:
        try:
            parameters = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"Invalid JSON parameters: {str(e)}"}))
            sys.exit(1)
    else:
        parameters = {}
    
    # Run tool
    result = run_tool(tool_name, parameters)
    
    # Output result
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
