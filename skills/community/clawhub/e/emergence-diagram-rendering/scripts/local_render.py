import os
import sys
import json
import sh
import uuid
from pathlib import Path
from datetime import datetime

def render_local(engine, code, format="png", run_id=None, template_data=None):
    """
    Renders a diagram using local binaries and stores artifacts in ./runs/.
    Returns: {status: "success"|"error", run_dir: str, image_path: str, stdout: str, stderr: str}
    """
    # 1. Setup Persistent Run Directory
    if not run_id:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_id = f"{timestamp}_{uuid.uuid4().hex[:6]}"
    
    # Path relative to script location
    base_dir = Path(__file__).parent.parent / "runs"
    run_dir = base_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    
    # Binary Check
    binary = {"mermaid": "mmdc", "d2": "d2", "graphviz": "dot"}.get(engine)
    if not sh.which(binary):
        result = {
            "status": "fallback_suggested",
            "message": f"Local renderer '{binary}' not found. Please use the 'render' tool (Cloud API) or run 'make install'.",
            "run_dir": str(run_dir)
        }
        with open(run_dir / "metadata.json", "w") as f:
            json.dump(result, f, indent=2)
        return result

    # Files
    ext = {"mermaid": "mmd", "d2": "d2", "graphviz": "dot"}.get(engine, "txt")
    tmp_input = run_dir / f"input.{ext}"
    tmp_output = run_dir / f"output.{format}"
    metadata_file = run_dir / "metadata.json"
    
    result = {
        "status": "error",
        "run_dir": str(run_dir),
        "image_path": None,
        "stdout": "",
        "stderr": ""
    }

    try:
        # Handle Template Injection
        if template_data:
            for key, value in template_data.items():
                code = code.replace(f"{{{{{key}}}}}", str(value))

        # Write code to input file
        with open(tmp_input, "w") as f:
            f.write(code)

        # 2. Execution Logic
        if engine == "mermaid":
            cmd = sh.Command("mmdc")
            run = cmd("-i", str(tmp_input), "-o", str(tmp_output), _err_to_out=True)
            result["stdout"] = run.stdout.decode()
            
        elif engine == "d2":
            cmd = sh.Command("d2")
            run = cmd(str(tmp_input), str(tmp_output), _err_to_out=True)
            result["stdout"] = run.stdout.decode()

        elif engine == "graphviz":
            cmd = sh.Command("dot")
            run = cmd(f"-T{format}", str(tmp_input), "-o", str(tmp_output), _err_to_out=True)
            result["stdout"] = run.stdout.decode()
            
        else:
            result["stderr"] = f"Unsupported engine: {engine}"

        if tmp_output.exists():
            result["status"] = "success"
            result["image_path"] = str(tmp_output)
            
    except sh.CommandNotFound as e:
        result["stderr"] = f"Command not found: {str(e)}. Please check your installation."
    except sh.ErrorReturnCode as e:
        result["stderr"] = e.stdout.decode() if e.stdout else str(e)
    except Exception as e:
        result["stderr"] = str(e)
    
    # 3. Save Metadata
    with open(metadata_file, "w") as f:
        json.dump(result, f, indent=2)
            
    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Autonomous Local Diagram Renderer")
    parser.add_argument("engine", help="mermaid, d2, or graphviz")
    parser.add_argument("code", help="Diagram source code or path to template")
    parser.add_argument("--format", default="png", help="Output format (png, svg)")
    parser.add_argument("--inject", help="JSON string for template injection (e.g. '{\"User\": \"Alice\"}')")
    
    args = parser.parse_args()
    
    # Handle template loading if path exists
    code_content = args.code
    if os.path.exists(args.code):
        with open(args.code, "r") as f:
            code_content = f.read()
            
    injection = json.loads(args.inject) if args.inject else None
    
    res = render_local(args.engine, code_content, format=args.format, template_data=injection)
    print(json.dumps(res, indent=2))
