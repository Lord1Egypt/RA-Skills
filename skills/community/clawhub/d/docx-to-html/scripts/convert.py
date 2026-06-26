import subprocess
import sys
import os

def convert_docx_to_html(input_path, output_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    js_script = os.path.join(script_dir, "docx-converter.js")
    
    try:
        result = subprocess.run(
            ["node", js_script, input_path, output_path],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during DOCX to HTML conversion: {e.stderr}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 convert.py <input_path> <output_path>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if convert_docx_to_html(input_file, output_file):
        sys.exit(0)
    else:
        sys.exit(1)
